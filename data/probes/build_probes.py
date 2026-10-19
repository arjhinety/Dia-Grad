"""Tranche-1 probe sets for po/opo and ay-inversion (D29, roadmap A4).

Run in diagrad:t1 (config data/probes/probes-v1.yaml; outputs under ~/data/t1/probes, never published):
    python -m data.probes.build_probes candidates CONFIG   # pool, held-out removal, positives + matched negatives
    python -m data.probes.build_probes translate CONFIG    # MADLAD-400-3B fil->en of every candidate (GPU)
    python -m data.probes.build_probes calpack CONFIG      # blind Codex alignment prompts for the calibration sample
    python -m data.probes.build_probes calibrate CONFIG    # threshold on sentence chrF, from Codex labels
    python -m data.probes.build_probes select CONFIG       # screen, length-match, cap per class, write sets

Pool: OpenSubtitles en-tl pairs whose Filipino side has 3-40 words after diagrad.t1.contamination.norm,
one pair per unique Filipino side (the first). Removed from the pool: pairs matching a held-out or E1
item (D20 rule in full for SMOL; 8-word runs only for MASSIVE and WMT24++, as D28 item 6), on either
side. Per feature, positives are every pool pair with the label; negatives are drawn by seeded rank
within the positives' word-length bins, `neg_ratio` per positive, so both classes have the same length
mix. Labels: diagrad.t1.gate (the ay rule is provisional until the A5 hand labels).

Screen: sentence chrF (sacrebleu) between MADLAD's English and the subtitle English. The threshold is
fixed by `calibrate` from Codex labels on a random calibration sample before any probe is run: the
lowest chrF at which at least `min_precision` of calibration pairs at or above it are rated fully
aligned (2). Unit of every rate: pairs.
"""
import hashlib
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

from data.mix.measure_mono import h64
from data.mix.measure_sources import READERS
from data.mix.build_mono_slice import heldout_hit
from diagrad.t1.contamination import Index, norm
from diagrad.t1.gate import label_ay_inversion, label_po_opo

MIN_W, MAX_W = 3, 40
CUE = re.compile(r"\b(sir|ma'?am|madam|miss|mister|mr|mrs|please|lord|your honou?r|grandma|grandpa|mom|dad"
                 r"|father|mother|aunt|uncle)\b", re.I)
FEATURES = {"po_opo": label_po_opo, "ay": label_ay_inversion}


def seeded(seed, s):
    return int.from_bytes(hashlib.blake2b(f"{seed}:{s}".encode("utf-8"), digest_size=8).digest(), "little")


def length_bin(n_words, edges=(5, 8, 12, 18, 25)):
    return sum(n_words >= e for e in edges)


def load_jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def pool(pairs, full_index, run8_index):
    """Unique-Filipino-side pairs of probe-able length, minus held-out matches; with labels and cue."""
    seen, out, removed = set(), [], 0
    for en, fil in pairs:
        n = norm(fil)
        w = n.count(" ") + 1 if n else 0
        if not MIN_W <= w <= MAX_W:
            continue
        h = h64(n)
        if h in seen:
            continue
        seen.add(h)
        ne = norm(en)
        if any(heldout_hit(full_index, x) or heldout_hit(run8_index, x, whole_short_sides=False) for x in (n, ne)):
            removed += 1
            continue
        out.append({"id": h, "en": en.strip(), "fil": fil.strip(), "words": w,
                    "po_opo": label_po_opo(fil), "ay": label_ay_inversion(fil), "cue": int(bool(CUE.search(en)))})
    return out, removed


def matched_negatives(rows, feature, seed, ratio):
    """Negatives drawn by seeded rank inside each positive length bin, `ratio` per positive."""
    pos = [r for r in rows if r[feature]]
    by_bin = defaultdict(list)
    for r in rows:
        if not r[feature]:
            by_bin[length_bin(r["words"])].append(r)
    need = defaultdict(int)
    for r in pos:
        need[length_bin(r["words"])] += ratio
    neg = []
    for b, k in need.items():
        cands = sorted(by_bin[b], key=lambda r: seeded(f"{seed}:{feature}", r["fil"]))
        neg += cands[:k]
    return pos, neg


def candidates(cfg):
    out = Path(cfg["out_dir"])
    out.mkdir(parents=True, exist_ok=True)
    full = Index([x for f in cfg["heldout"]["full_rule"] for x in load_jsonl(f)])
    run8 = Index([x for f in cfg["heldout"]["eight_word_runs_only"] for x in load_jsonl(f)])
    rows, removed = pool(READERS["moses"](cfg["source"]["path"]), full, run8)
    rng = {r["id"]: seeded(cfg["seed"], r["fil"]) for r in rows}
    keep = {}
    stats = {"pool": len(rows), "removed_heldout": removed, "features": {}}
    for feat in FEATURES:
        # cap the positives first, then draw negatives for the capped set
        mp = cfg["max_positives"][feat] if isinstance(cfg["max_positives"], dict) else cfg["max_positives"]
        cap = set(r["id"] for r in sorted((r for r in rows if r[feat]), key=lambda r: rng[r["id"]])[:mp])
        pos, neg = matched_negatives([r for r in rows if not r[feat] or r["id"] in cap], feat, cfg["seed"], cfg["neg_ratio"])
        stats["features"][feat] = {"positives_in_pool": sum(r[feat] for r in rows), "positives": len(pos),
                                   "negatives": len(neg)}
        for r in pos + neg:
            keep[r["id"]] = r
    with open(out / "candidates.jsonl", "w", encoding="utf-8") as f, \
            open(out / "candidates-as-tests.jsonl", "w", encoding="utf-8") as g:
        for r in keep.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            # the D20 checker's input format, to check candidates against the monolingual slice
            g.write(json.dumps({"id": str(r["id"]), "src": r["en"], "tgt": r["fil"]}, ensure_ascii=False) + "\n")
    stats["candidates"] = len(keep)
    (out / "candidates-stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    print(json.dumps(stats))


def translate(cfg):
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    out = Path(cfg["out_dir"])
    rows = load_jsonl(out / "candidates.jsonl")
    repo, rev = cfg["translator"]["repo"], cfg["translator"]["revision"]
    tok = AutoTokenizer.from_pretrained(repo, revision=rev)
    model = AutoModelForSeq2SeqLM.from_pretrained(repo, revision=rev, dtype=torch.bfloat16, device_map="cuda").eval()
    bs, gen = cfg["translator"]["batch_size"], dict(num_beams=cfg["translator"]["num_beams"],
                                                     max_new_tokens=cfg["translator"]["max_new_tokens"])
    done = set()
    if (out / "translations.jsonl").exists():       # resume: candidates translated earlier keep their output
        done = {r["id"] for r in load_jsonl(out / "translations.jsonl")}
    rows = [r for r in rows if r["id"] not in done]
    with open(out / "translations.jsonl", "a", encoding="utf-8") as f:
        for i in range(0, len(rows), bs):
            batch = rows[i:i + bs]
            enc = tok([f"<2en> {r['fil']}" for r in batch], return_tensors="pt", padding=True)
            with torch.inference_mode():
                seq = model.generate(**{k: v.cuda() for k, v in enc.items()}, **gen)
            for r, h in zip(batch, tok.batch_decode(seq, skip_special_tokens=True)):
                f.write(json.dumps({"id": r["id"], "mt_en": h.strip()}, ensure_ascii=False) + "\n")
            if i % (bs * 50) == 0:
                print(f"{i}/{len(rows)}", flush=True)


def with_chrf(cfg):
    from sacrebleu.metrics import CHRF
    out = Path(cfg["out_dir"])
    mt = {r["id"]: r["mt_en"] for r in load_jsonl(out / "translations.jsonl")}
    chrf = CHRF()
    rows = load_jsonl(out / "candidates.jsonl")
    for r in rows:
        r["mt_en"] = mt[r["id"]]
        r["chrf"] = chrf.sentence_score(r["mt_en"], [r["en"]]).score
    return rows


CAL_RUBRIC = """You are checking English-Filipino subtitle pairs that may be used as a probe set. For each pair:
- alignment: 2 = the English and Filipino say the same thing (politeness markers such as "po" have no
  English equivalent, so their absence in English is fine; ordinary subtitle condensation is fine);
  1 = mostly the same, with a missing or extra part; 0 = different content, or not a translation.
Judge each item on its own. Confidence [certain]/[likely]/[unsure]. Reply as JSON lines only:
{"item": "<id>", "alignment": 0|1|2, "confidence": "...", "note": "<short>"}
"""


def calpack(cfg):
    out = Path(cfg["out_dir"])
    rows = load_jsonl(out / "candidates.jsonl")
    rng = random.Random(cfg["seed"] + 2)
    sample = rng.sample(rows, cfg["calibration"]["n"])
    key, items = {}, []
    for r in sample:
        iid = f"{rng.getrandbits(40):010x}"
        key[iid] = r["id"]
        items.append({"item": iid, "english": r["en"], "filipino": r["fil"]})
    nb = cfg["calibration"]["batches"]
    cal = out / "calibration"
    cal.mkdir(exist_ok=True)
    for b in range(nb):
        its = items[b::nb]
        (cal / f"batch-{b}.prompt.md").write_text(
            f"{CAL_RUBRIC}\n{len(its)} items.\n\n" + "\n".join(json.dumps(i, ensure_ascii=False) for i in its) + "\n",
            encoding="utf-8")
    (cal / "key.json").write_text(json.dumps(key, indent=1) + "\n")


def parse_answers(text):
    rows = {}
    for line in text.splitlines():
        line = line.strip().strip(",")
        if line.startswith("{"):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows[r["item"]] = r
    return rows


def threshold(points, min_precision):
    """points: (chrf, aligned 0/1). The lowest t such that the share aligned among points >= t is at least
    min_precision; None if no t reaches it."""
    best = None
    for t in sorted({c for c, _ in points}, reverse=True):
        above = [a for c, a in points if c >= t]
        if sum(above) / len(above) >= min_precision:
            best = t
    return best


def calibrate(cfg):
    out = Path(cfg["out_dir"])
    cal = out / "calibration"
    key = json.loads((cal / "key.json").read_text())
    ans = {}
    for b in range(cfg["calibration"]["batches"]):
        ans.update(parse_answers((cal / f"batch-{b}.answer.md").read_text(encoding="utf-8")))
    rows = {r["id"]: r for r in with_chrf(cfg)}
    pts = [(rows[key[i]]["chrf"], int(a["alignment"] == 2)) for i, a in ans.items() if i in key]
    t = threshold(pts, cfg["calibration"]["min_precision"])
    above = [a for c, a in pts if t is not None and c >= t]
    res = {"labelled": len(pts), "fully_aligned": sum(a for _, a in pts), "threshold_chrf": t,
           "kept": len(above), "kept_fully_aligned": sum(above),
           "recall_fully_aligned": sum(above) / max(1, sum(a for _, a in pts)),
           "alignment_counts": {v: sum(int(a["alignment"]) == v for a in ans.values()) for v in (0, 1, 2)}}
    (cal / "threshold.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res))


def excluded_by_slice(cfg):
    """Candidate ids the slice check flags (rule in cfg["slice_check"]["rule"]: "8word" or "full")."""
    rep = json.loads(Path(cfg["slice_check"]["report"]).read_text())
    rule, bad = cfg["slice_check"]["rule"], set()
    for it in rep["sets"]["candidates-as-tests"]["items"]:
        f = it["fold"]
        if (rule == "full" and f["flag8"]) or any(f[s]["longest"] >= 8 for s in ("src", "tgt")):
            bad.add(int(it["id"]))
    return bad


def select(cfg):
    out = Path(cfg["out_dir"])
    t = json.loads((out / "calibration" / "threshold.json").read_text())["threshold_chrf"]
    bad = excluded_by_slice(cfg)
    rows = [r for r in with_chrf(cfg) if r["chrf"] >= t and r["id"] not in bad]
    stats = {"threshold_chrf": t, "excluded_by_slice": len(bad), "passed_screen": len(rows), "features": {}}
    sides = set()
    cap = cfg["per_class"]
    for feat in FEATURES:
        pos = sorted((r for r in rows if r[feat]), key=lambda r: seeded(f"{cfg['seed']}:sel", r["fil"]))
        neg_by_bin = defaultdict(list)
        for r in sorted((r for r in rows if not r[feat]), key=lambda r: seeded(f"{cfg['seed']}:{feat}", r["fil"])):
            neg_by_bin[length_bin(r["words"])].append(r)
        chosen_pos, chosen_neg = [], []
        for r in pos:                            # each positive takes one negative from its length bin
            b = neg_by_bin[length_bin(r["words"])]
            if b and len(chosen_pos) < cap:
                chosen_pos.append(r)
                chosen_neg.append(b.pop(0))
        with open(out / f"probe-{feat}.jsonl", "w", encoding="utf-8") as f:
            for r in chosen_pos + chosen_neg:
                sides.update((h64(norm(r["en"])), h64(norm(r["fil"]))))
                f.write(json.dumps({"id": r["id"], "en": r["en"], "fil": r["fil"], "label": r[feat], "words": r["words"],
                                    "cue": r["cue"], "chrf": round(r["chrf"], 2)}, ensure_ascii=False) + "\n")
        stats["features"][feat] = {"positives": len(chosen_pos), "negatives": len(chosen_neg),
                                   "positives_with_cue": sum(r["cue"] for r in chosen_pos),
                                   "negatives_with_cue": sum(r["cue"] for r in chosen_neg),
                                   "mean_words_pos": sum(r["words"] for r in chosen_pos) / max(1, len(chosen_pos)),
                                   "mean_words_neg": sum(r["words"] for r in chosen_neg) / max(1, len(chosen_neg))}
    # For the training-mix cut (A3, D29 item 3): drop any training pair with either normalised side here.
    (out / "probe-exclusion-sides.json").write_text(json.dumps(
        {"unit": "h64(diagrad.t1.contamination.norm(side)) of every probe English and Filipino side",
         "hashes": sorted(sides)}) + "\n")
    stats["exclusion_sides"] = len(sides)
    (out / "select-stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    print(json.dumps(stats))


if __name__ == "__main__":
    import yaml
    cmd, cfg = sys.argv[1], yaml.safe_load(open(sys.argv[2], encoding="utf-8"))
    {"candidates": candidates, "translate": translate, "calpack": calpack, "calibrate": calibrate,
     "select": select}[cmd](cfg)
