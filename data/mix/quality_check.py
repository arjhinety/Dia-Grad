"""D28 quality check: are paragraphs the MADLAD filter drops clearly better than the ones it keeps?

Run record: experiments/runs/20261018-mono-filter-quality-1/RUN.md.

    python -m data.mix.quality_check sample CONFIG   # in diagrad:t1: pool, MADLAD membership, 2 x n paragraphs
    python -m data.mix.quality_check pack CONFIG     # blind, shuffled Codex prompts + key (hidden repeats)
    python -m data.mix.quality_check score CONFIG    # after the Codex answers are saved next to the prompts

Population: unique normalised paragraphs (>= 5 words, measure_mono.doc_lines rules) of the option A
pool, FineWeb-2 fil_Latn train and HPLT 2.0 tgl_Latn. "dropped" = the paragraph's hash is in any
MADLAD-400 fil split (clean or noisy); "kept" = it is in none. A paragraph is a candidate when a seeded
hash of its normalised text falls in a 1-in-`select_mod` subset, so the choice cannot depend on content;
the first n per group by that hash are taken. Paragraphs over `max_words` raw words are left out of the
sample (both groups alike) and the share left out is reported.

Unit of every rate: rated paragraphs (first ratings; hidden repeats only measure consistency). Scores:
"eligible" (1 if Codex labels the paragraph Filipino/Tagalog or Taglish, else 0) over all paragraphs;
quality and naturalness (0-2) over eligible paragraphs only. Gap = mean(dropped) - mean(kept), per
score; its 95% interval is a percentile bootstrap resampling each group independently.
"""
import hashlib
import json
import random
import sys
from pathlib import Path

from diagrad.t1.contamination import norm

RUBRIC = """You are judging paragraphs of Filipino (Tagalog) web text that may be used to train a
language model. Each item is one paragraph, shown as found (it may be cut from a longer page). Judge
the paragraph itself, not its topic or opinions.

First, language_status: "filipino_tagalog" | "taglish" | "other_language" | "mixed_uncertain" |
"insufficient_text". Cebuano, Ilokano, Hiligaynon, Waray and other Philippine languages are
"other_language" (name it in other_language), never defective Tagalog; regional Tagalog or unfamiliar
borrowings are not another language. Base this on several grammatical and lexical cues, not one word.
Predominantly English material where Filipino contributes only isolated words is "other_language".

Then, only when language_status is "filipino_tagalog" or "taglish", two independent scores (otherwise
give null for both). Quality measures coherent, usable textual content; naturalness measures how
idiomatic the language is for its register. Fluent wording can occur in low-quality material, and
coherent prose can contain unnatural language.

- quality: 2 = coherent, usable content for human readers; 1 = usable but flawed (disconnected
  fragments, excessive non-informative repetition or keyword stuffing, partial garbling, template
  material mixed with content); 0 = not usable (spam or keyword lists, navigation or template material
  that dominates the item, broken encoding, machine-garbled text). Do not downgrade a useful list,
  advertisement, legal passage, recipe, FAQ or repeated rhetorical phrase solely for its format or
  genre. Do not penalise dependence on surrounding context or boundary clipping alone; lower quality
  only when clipping or extraction damage substantially prevents understanding.
- naturalness: 2 = what a fluent writer would write in this register; 1 = understandable but unnatural
  (translationese, calques, odd word order or word choice); 0 = substantially unintelligible. Idiomatic
  Taglish can be 2, including substantial English stretches; English proportion alone is not a defect.
  Judge fluency relative to the apparent register and variety: accept intelligible regional, historical,
  literary, religious, colloquial and online usage. Do not require contemporary KWF spelling; forms such
  as siya/sya, hindi/di, puwede/pwede do not lower a score. Formality is neither a bonus nor a defect;
  "po"/"opo" is neutral. Penalise spelling or grammar only when it materially impairs understanding or
  produces clearly unnatural constructions.

translation_artifacts: "present" | "absent" | "uncertain". "present" means several conspicuous
translation-like artifacts (implausible literal senses, collocations, argument structure, pronoun
reference, source-shaped phrasing across clauses). It does not establish machine origin; "absent"
means no positive evidence, not confirmed human authorship. Do not infer it from genre, formality,
borrowing or spelling alone.

confidence concerns quality and naturalness only: [certain] = the anchors apply clearly; [likely] =
one adjacent score is plausible; [unsure] = substantial ambiguity. Some items may repeat; judge each on
its own. Reply as JSON lines only, one per item:
{"item": "<id>", "language_status": "...", "other_language": "<name or empty>", "quality": 0|1|2|null, "naturalness": 0|1|2|null, "translation_artifacts": "...", "confidence": "...", "note": "<short>"}
"""


def seeded(seed, s):
    return int.from_bytes(hashlib.blake2b(f"{seed}:{s}".encode("utf-8"), digest_size=8).digest(), "little")


def candidates(cfg, docs_by_source):
    """{h64(norm): {"text", "norm", "sources", "rank"}} for paragraphs selected by the seeded hash."""
    from data.mix.measure_mono import MIN_WORDS, h64
    seed, mod = cfg["seed"], cfg["select_mod"]
    out = {}
    for source, docs in docs_by_source:
        for text in docs:
            for raw in text.split("\n"):
                n = norm(raw)
                if n.count(" ") + 1 < MIN_WORDS:
                    continue
                r = seeded(seed, n)
                if r % mod:
                    continue
                h = h64(n)
                c = out.setdefault(h, {"text": raw.strip(), "norm": n, "sources": [], "rank": r})
                if source not in c["sources"]:
                    c["sources"].append(source)
    return out


def choose(cands, madlad_clean, madlad_all, n, max_words):
    """Split candidates by MADLAD membership; first n per group by rank among those <= max_words."""
    import numpy as np
    hs = np.array(sorted(cands), dtype=np.int64)
    in_all = dict(zip(hs.tolist(), np.isin(hs, madlad_all).tolist()))
    in_clean = dict(zip(hs.tolist(), np.isin(hs, madlad_clean).tolist()))
    groups = {"dropped": [], "kept": []}
    counts = {g: {"candidates": 0, "over_max_words": 0} for g in groups}
    for h in sorted(cands, key=lambda k: cands[k]["rank"]):
        g = "dropped" if in_all[h] else "kept"
        counts[g]["candidates"] += 1
        c = cands[h]
        if len(c["text"].split()) > max_words:
            counts[g]["over_max_words"] += 1
            continue
        if len(groups[g]) < n:
            groups[g].append({"hash": h, "text": c["text"], "sources": c["sources"], "group": g,
                              "madlad": "clean" if in_clean[h] else ("noisy_only" if in_all[h] else "none")})
    return groups, counts


def pack(cfg, out):
    sample = json.loads((out / "sample.json").read_text(encoding="utf-8"))
    rng = random.Random(cfg["seed"] + 1)
    items, key = [], {}
    for g in ("dropped", "kept"):
        for p in sample["groups"][g]:
            iid = f"{rng.getrandbits(40):010x}"
            key[iid] = {"group": g, "hash": p["hash"], "madlad": p["madlad"], "sources": p["sources"]}
            items.append({"item": iid, "text": p["text"]})
    rng.shuffle(items)
    nb = cfg["batches"]
    batches = [items[i::nb] for i in range(nb)]
    # Hidden repeats go into a different batch (a different Codex call) from their original.
    placed = [(b, it) for b in range(nb) for it in batches[b]]
    for b, orig in rng.sample(placed, cfg["hidden_repeats"]):
        iid = f"{rng.getrandbits(40):010x}"
        key[iid] = {**key[orig["item"]], "repeat_of": orig["item"]}
        batches[(b + nb // 2) % nb].append({**orig, "item": iid})
    for b, its in enumerate(batches):
        rng.shuffle(its)
        body = "\n".join(json.dumps(i, ensure_ascii=False) for i in its)
        (out / f"batch-{b}.prompt.md").write_text(f"{RUBRIC}\n{len(its)} items.\n\n{body}\n", encoding="utf-8")
    (out / "key.json").write_text(json.dumps(key, indent=1) + "\n", encoding="utf-8")


def parse_answers(text):
    rows = {}
    for line in text.splitlines():
        line = line.strip().strip(",")
        if line.startswith("{"):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue                     # e.g. the rubric's own format line echoed back
            rows[r["item"]] = r
    return rows


def gap_interval(a, b, resamples, seed):
    """mean(a) - mean(b) and its 95% percentile bootstrap interval, each group resampled on its own."""
    import numpy as np
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    ga = a[rng.integers(0, a.size, (resamples, a.size))].mean(1)
    gb = b[rng.integers(0, b.size, (resamples, b.size))].mean(1)
    lo, hi = np.percentile(ga - gb, [2.5, 97.5])
    return float(a.mean() - b.mean()), float(lo), float(hi)


ELIGIBLE = ("filipino_tagalog", "taglish")


def value(row, s):
    """A row's value on score s: 'eligible' is 1/0 for every item; quality and naturalness exist only for
    eligible items (None otherwise, left out of that score's mean)."""
    ok = row.get("language_status") in ELIGIBLE
    if s == "eligible":
        return int(ok)
    return row.get(s) if ok else None


def score(cfg, out):
    key = json.loads((out / "key.json").read_text(encoding="utf-8"))
    ans = {}
    for b in range(cfg["batches"]):
        ans.update(parse_answers((out / f"batch-{b}.answer.md").read_text(encoding="utf-8")))
    missing = sorted(set(key) - set(ans))
    rule = cfg["decision_rule"]
    res = {"missing": missing, "groups": {}, "gaps": {}, "repeats": {}}
    first = {g: [ans[i] for i, k in key.items() if k["group"] == g and "repeat_of" not in k and i in ans]
             for g in ("dropped", "kept")}
    for g, rows in first.items():
        res["groups"][g] = {"n": len(rows),
                            "language_status": {v: sum(r.get("language_status") == v for r in rows)
                                                for v in sorted({r.get("language_status") for r in rows}, key=str)},
                            "translation_artifacts_present": sum(r.get("translation_artifacts") == "present" for r in rows)}
        for s in rule["min_gap"]:
            vals = [v for v in (value(r, s) for r in rows) if v is not None]
            res["groups"][g][s] = {"n": len(vals), "mean": sum(vals) / len(vals) if vals else None,
                                   "zeros": sum(v == 0 for v in vals)}
    tripped = False
    for s, min_gap in rule["min_gap"].items():
        a = [v for v in (value(r, s) for r in first["dropped"]) if v is not None]
        b = [v for v in (value(r, s) for r in first["kept"]) if v is not None]
        gap, lo, hi = gap_interval(a, b, cfg["bootstrap_resamples"], cfg["seed"])
        hit = gap >= min_gap and lo > 0
        tripped |= hit
        res["gaps"][s] = {"dropped_minus_kept": gap, "ci95": [lo, hi], "min_gap": min_gap, "meets_rule": hit}
    reps = [(i, k["repeat_of"]) for i, k in key.items() if "repeat_of" in k and i in ans and k["repeat_of"] in ans]
    fields = ("language_status", "quality", "naturalness")
    diff = sum(any(ans[i].get(f) != ans[o].get(f) for f in fields) for i, o in reps)
    res["repeats"] = {"pairs": len(reps), "any_label_differs": diff,
                      "judge_usable": diff <= rule["max_repeat_disagreement"] * len(reps)}
    res["decision_rule"] = {**rule, "tripped": tripped,
                            "outcome": ("revisit as option B" if tripped else "option A stands")
                            if res["repeats"]["judge_usable"] else "judge not consistent enough; no verdict"}
    (out / "scores.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=1))
    return res


def sample(cfg, out):
    import numpy as np
    from data.mix.measure_mono import open_spec
    srcs = [open_spec(s) for s in cfg["pool"]]
    cands = candidates(cfg, srcs)
    mdir = Path(cfg["lines_dir"])
    clean = np.load(mdir / cfg["madlad_clean"])
    allm = np.unique(np.concatenate([clean] + [np.load(mdir / f) for f in cfg["madlad_noisy"]]))
    groups, counts = choose(cands, clean, allm, cfg["n_per_group"], cfg["max_words"])
    out.mkdir(parents=True, exist_ok=True)
    rep = {"candidates": len(cands), "counts": counts, "groups": groups}
    (out / "sample.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"candidates": len(cands), "counts": counts,
                      "chosen": {g: len(v) for g, v in groups.items()}}))


if __name__ == "__main__":
    import yaml
    cmd, cfg = sys.argv[1], yaml.safe_load(open(sys.argv[2], encoding="utf-8"))
    {"sample": sample, "pack": pack, "score": score}[cmd](cfg, Path(cfg["out_dir"]))
