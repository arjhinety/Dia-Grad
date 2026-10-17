"""Teacher comparison for tranche 1 (run 20261017-teacher-compare-1; D25, D26).

Translates the same 1,000 MASSIVE-dev pairs in both directions with each pinned model, then scores
chrF++ with a paired bootstrap against the reference model (NLLB-3.3B, evaluation only: D25 U6).

  generate  --config C --model NAME [--limit N --out DIR]   one model, both directions
  score     --config C [--out DIR]                          chrF++, gaps, decision rule -> scores.json
  pack      --config C [--out DIR]                          blind naturalness items for Codex (D26)

Outputs (`<out>/<model>.<direction>.jsonl`) are run artifacts and are not committed; their sha256 and
the timing go to `metrics.jsonl` next to RUN.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import time
from pathlib import Path

import numpy as np
import yaml
from sacrebleu.metrics import CHRF

THINK = re.compile(r"<think>.*?</think>", re.S)


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sample_pairs(path, n: int, seed: int) -> list[dict]:
    """`n` rows drawn without replacement with `random.Random(seed)`, kept in file order."""
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    keep = sorted(random.Random(seed).sample(range(len(rows)), n))
    return [rows[i] for i in keep]


def direction_items(rows: list[dict], direction: str) -> list[dict]:
    """en-fil keeps the file's orientation (src English); fil-en swaps it."""
    if direction == "en-fil":
        return [{"id": r["id"], "src": r["src"], "ref": r["tgt"]} for r in rows]
    if direction == "fil-en":
        return [{"id": r["id"], "src": r["tgt"], "ref": r["src"]} for r in rows]
    raise ValueError(direction)


# ---------------------------------------------------------------- scoring

def chrf_stats(metric: CHRF, hyps: list[str], refs: list[str]) -> np.ndarray:
    """Per-sentence chrF++ sufficient statistics, shape [n, k]; their column sums give corpus chrF++."""
    return np.asarray(metric._extract_corpus_statistics(hyps, [refs]), dtype=np.float64)


def corpus_from_stats(metric: CHRF, stats: np.ndarray) -> float:
    return float(metric._compute_score_from_stats(list(stats.sum(0))).score)


def paired_bootstrap_gap(metric: CHRF, ref_stats, cand_stats, resamples: int, seed: int,
                         ci: float = 0.95, chunk: int = 500) -> dict:
    """Corpus chrF++ of the reference system minus the candidate, on the same resampled sentence sets.

    Returns the point gap and the percentile interval of the resampled gaps.
    """
    n = ref_stats.shape[0]
    rng = np.random.default_rng(seed)
    gaps = []
    for start in range(0, resamples, chunk):
        idx = rng.integers(0, n, size=(min(chunk, resamples - start), n))
        r, c = ref_stats[idx].sum(1), cand_stats[idx].sum(1)
        gaps.extend(metric._compute_score_from_stats(list(a)).score - metric._compute_score_from_stats(list(b)).score
                    for a, b in zip(r, c))
    lo, hi = np.percentile(gaps, [100 * (1 - ci) / 2, 100 * (1 + ci) / 2])
    point = corpus_from_stats(metric, ref_stats) - corpus_from_stats(metric, cand_stats)
    return {"gap": float(point), "ci_low": float(lo), "ci_high": float(hi)}


def decision_rule(per_direction: dict, gap_chrf: float) -> dict:
    """D26: trips only if, in EVERY direction, the reference beats the best candidate by more than
    `gap_chrf` and the interval of that gap lies above 0.

    per_direction: {direction: {"best": name, "gap": g, "ci_low": lo, ...}}
    """
    each = {d: bool(v["gap"] > gap_chrf and v["ci_low"] > 0) for d, v in per_direction.items()}
    return {"per_direction": each, "tripped": bool(each) and all(each.values())}


# ---------------------------------------------------------------- generation

def _batches(items, size):
    order = sorted(range(len(items)), key=lambda i: len(items[i]["src"]))
    for s in range(0, len(order), size):
        yield order[s:s + size]


def load_causal_by_shard(repo: str, revision: str):
    """Build the model on the GPU, then copy weights in one shard at a time.

    `from_pretrained(..., device_map="cuda")` holds a full CPU copy of the weights while loading
    (measured on Qwen3-14B: 27.9 GB anonymous memory at peak for a 27.5 GB model). On the GB10, CPU and
    GPU share 121 GB, so Qwen3-32B (65.5 GB) cannot load that way. Here CPU memory stays at about one
    tensor. Every checkpoint key must match a model parameter, and every parameter must be filled.
    """
    import glob
    import os

    import torch
    from huggingface_hub import snapshot_download
    from safetensors import safe_open
    from transformers import AutoConfig, AutoModelForCausalLM

    path = snapshot_download(repo, revision=revision, allow_patterns=["*.safetensors", "*.json"])
    config = AutoConfig.from_pretrained(repo, revision=revision)
    with torch.device("cuda"):
        model = AutoModelForCausalLM.from_config(config, dtype=torch.bfloat16)
    params = dict(model.named_parameters())
    filled = set()
    with torch.no_grad():
        for shard in sorted(glob.glob(os.path.join(path, "*.safetensors"))):
            with safe_open(shard, framework="pt", device="cuda") as f:
                for key in f.keys():
                    params[key].copy_(f.get_tensor(key))
                    filled.add(key)
    missing = set(params) - filled
    if getattr(config, "tie_word_embeddings", False):
        missing.discard("lm_head.weight")
    assert not missing, f"parameters not in the checkpoint: {sorted(missing)[:5]}"
    return model


def generate(cfg: dict, name: str, limit: int | None, out: Path, gpu_mem_gb: float | None = None) -> None:
    import torch
    import transformers
    from transformers import (AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer)

    if gpu_mem_gb:
        # A ceiling for this process: past it PyTorch raises OutOfMemoryError here, instead of the
        # kernel's OOM killer taking down the whole user session (2026-10-17, run 20261017-teacher-
        # compare-1). docker --memory does not cover GPU allocations on the GB10 (tested).
        torch.cuda.set_per_process_memory_fraction(gpu_mem_gb * 2**30 / torch.cuda.mem_get_info()[1])
    spec = next(m for m in cfg["models"] if m["name"] == name)
    data = cfg["data"]
    digest = sha256(data["path"])
    assert digest.startswith(data["sha256_prefix"]), f"input sha256 {digest} != {data['sha256_prefix']}…"
    rows = sample_pairs(data["path"], data["n"], cfg["seed"])[:limit]
    kind = spec["kind"]
    tok = AutoTokenizer.from_pretrained(spec["repo"], revision=spec["revision"])
    # Straight to the GPU: on the GB10 (CPU and GPU share 121 GB) a CPU copy plus a .cuda() copy of
    # Qwen3-32B (65.5 GB) would not fit.
    load = dict(revision=spec["revision"], dtype=torch.bfloat16)
    if kind == "causal":
        tok.padding_side = "left"
        # Qwen3-14B ran with from_pretrained; Qwen3-32B needs the shard loader (identical weights,
        # checked on Qwen3-14B: RUN.md 2026-10-17).
        if spec.get("loader") == "by_shard":
            model = load_causal_by_shard(spec["repo"], spec["revision"]).eval()
        else:
            model = AutoModelForCausalLM.from_pretrained(spec["repo"], **load, device_map="cuda").eval()
        dec = cfg["decoding"]["causal"]
    else:
        model = AutoModelForSeq2SeqLM.from_pretrained(spec["repo"], **load, device_map="cuda").eval()
        dec = cfg["decoding"]["seq2seq"]
    out.mkdir(parents=True, exist_ok=True)

    for direction in data["directions"]:
        src_l, tgt_l = direction.split("-")
        items = direction_items(rows, direction)
        hyps, new_tokens, hit_cap = [None] * len(items), 0, 0
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        for idx in _batches(items, dec["batch_size"]):
            srcs = [items[i]["src"] for i in idx]
            gen_kw = dict(max_new_tokens=dec["max_new_tokens"])
            if kind == "madlad":
                tag = cfg["lang_codes"]["madlad"][tgt_l]
                enc = tok([f"{tag} {s}" for s in srcs], return_tensors="pt", padding=True)
                gen_kw["num_beams"] = dec["num_beams"]
            elif kind == "nllb":
                codes = cfg["lang_codes"]["nllb"]
                tok.src_lang = codes[src_l]
                enc = tok(srcs, return_tensors="pt", padding=True)
                gen_kw.update(num_beams=dec["num_beams"],
                              forced_bos_token_id=tok.convert_tokens_to_ids(codes[tgt_l]))
            else:
                prompts = [tok.apply_chat_template(
                    [{"role": "user", "content": cfg["prompt"][direction].format(src=s)}],
                    tokenize=False, add_generation_prompt=True,
                    enable_thinking=dec["enable_thinking"]) for s in srcs]
                enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False)
                gen_kw.update(do_sample=False, temperature=None, top_p=None, top_k=None)
            enc = {k: v.cuda() for k, v in enc.items()}
            with torch.inference_mode():
                seq = model.generate(**enc, **gen_kw)
            if kind == "causal":
                seq = seq[:, enc["input_ids"].shape[1]:]
            start = getattr(model.config, "decoder_start_token_id", None)
            real = (seq != tok.pad_token_id) & (seq != (-1 if start is None else start))
            lens = real.sum(1)
            new_tokens += int(lens.sum())
            hit_cap += int((lens >= dec["max_new_tokens"]).sum())   # ran to the cap: no EOS (degenerate)
            for i, text in zip(idx, tok.batch_decode(seq, skip_special_tokens=True)):
                hyps[i] = THINK.sub("", text).strip()
        torch.cuda.synchronize()
        secs = time.perf_counter() - t0

        path = out / f"{name}.{direction}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for it, h in zip(items, hyps):
                f.write(json.dumps({**it, "hyp": h}, ensure_ascii=False) + "\n")
        rec = {"event": "generate", "model": name, "repo": spec["repo"], "revision": spec["revision"],
               "use": spec["use"], "direction": direction, "n": len(items), "seconds": round(secs, 2),
               "sentences_per_s": round(len(items) / secs, 3), "new_tokens": new_tokens,
               "tokens_per_s": round(new_tokens / secs, 1), "hit_max_new_tokens": hit_cap,
               "peak_mem_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2),
               "output": path.name, "output_sha256": sha256(path), "input_sha256": digest,
               "torch": torch.__version__, "transformers": transformers.__version__,
               "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        with open(out / "generate-log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec))


# ---------------------------------------------------------------- score, pack

def load_outputs(out: Path, name: str, direction: str) -> list[dict]:
    return [json.loads(l) for l in open(out / f"{name}.{direction}.jsonl", encoding="utf-8")]


def score(cfg: dict, out: Path) -> dict:
    m = cfg["metrics"]
    metric = CHRF(word_order=m["chrf_word_order"])
    ref_name = m["reference_model"]
    names = [s["name"] for s in cfg["models"]]
    result = {"metric": f"chrF++ (sacrebleu CHRF word_order={m['chrf_word_order']})",
              "reference_model": ref_name, "scores": {}, "gaps": {}, "best": {}}
    for direction in cfg["data"]["directions"]:
        stats, ids = {}, None
        for name in names:
            rows = load_outputs(out, name, direction)
            row_ids = [r["id"] for r in rows]
            assert ids is None or row_ids == ids, f"{name} {direction}: rows not aligned"
            ids = row_ids
            stats[name] = chrf_stats(metric, [r["hyp"] for r in rows], [r["ref"] for r in rows])
        result["scores"][direction] = {n: corpus_from_stats(metric, s) for n, s in stats.items()}
        result["gaps"][direction] = {
            n: paired_bootstrap_gap(metric, stats[ref_name], stats[n], m["bootstrap_resamples"],
                                    cfg["seed"], cfg["decision_rule"]["ci"])
            for n in names if n != ref_name}
        cands = {n: v for n, v in result["scores"][direction].items() if n != ref_name}
        best = max(cands, key=cands.get)
        result["best"][direction] = {"best": best, **result["gaps"][direction][best]}
        metric.corpus_score([r["hyp"] for r in rows], [[r["ref"] for r in rows]])  # sets the signature
    result["signature"] = str(metric.get_signature())
    result["decision_rule"] = {**cfg["decision_rule"],
                               **decision_rule(result["best"], cfg["decision_rule"]["gap_chrf"])}
    return result


RUBRIC = """You are judging machine translations between English and Filipino (Tagalog) of short
voice-assistant commands. For each item, give two separate labels for the TRANSLATION, judged against
the supplied source (never an imagined original). A fluent mistranslation can get naturalness 2 and
meaning 0.

- naturalness: 2 = something a fluent speaker would naturally say or type to a voice assistant;
  1 = understandable but unnatural (word order, calques, odd word choice, awkwardly formal);
  0 = substantially unintelligible, or not in the target language (an untranslated sentence is 0).
  Everyday Tagalog and idiomatic Taglish ("i-off", "takeaways") can be 2; formal or KWF Filipino can
  also be 2 where it fits. Formality is neither a bonus nor a defect. Adding or omitting "po" does not
  by itself change the label; awkward placement does. Natural fragments, contractions and Philippine
  English are fine. Ignore punctuation and capitalisation.
- meaning: 2 = intent and necessary details preserved; 1 = a limited discrepancy; 0 = changes the
  requested action or polarity, or an essential detail (recipient, time, quantity, place). Local
  entities in the source (e.g. Divisoria) should be kept. Routine politeness differences do not count.

If a source is ambiguous or malformed, say so in the note; do not repair it. Confidence is your
certainty in BOTH labels (use the lower): [certain]/[likely]/[unsure]. Some items may repeat; judge
each on its own. Reply as JSON lines only, one per item:
{"item": "<id>", "naturalness": 0|1|2, "meaning": 0|1|2, "confidence": "...", "note": "<short>"}
"""


def pack(cfg: dict, out: Path) -> None:
    """Blind items: the same `per_model_per_direction` source sentences for every model, item ids
    random, model names held only in the key file."""
    k = cfg["naturalness"]["per_model_per_direction"]
    rng = random.Random(cfg["seed"] + 1)
    names = [s["name"] for s in cfg["models"]]
    for direction in cfg["data"]["directions"]:
        base = load_outputs(out, names[0], direction)
        chosen = set(rng.sample([r["id"] for r in base], k))
        items, key = [], {}
        for name in names:
            for r in load_outputs(out, name, direction):
                if r["id"] in chosen:
                    iid = f"{rng.getrandbits(40):010x}"
                    key[iid] = {"model": name, "id": r["id"]}
                    items.append({"item": iid, "source": r["src"], "translation": r["hyp"]})
        # Hidden repeats measure the judge's own consistency (rubric review, 2026-10-17).
        for orig in rng.sample(items, cfg["naturalness"]["hidden_repeats"]):
            iid = f"{rng.getrandbits(40):010x}"
            key[iid] = {**key[orig["item"]], "repeat_of": orig["item"]}
            items.append({**orig, "item": iid})
        rng.shuffle(items)
        body = "\n".join(json.dumps(i, ensure_ascii=False) for i in items)
        (out / f"naturalness-{direction}.prompt.md").write_text(
            f"{RUBRIC}\nDirection: {direction}. {len(items)} items.\n\n{body}\n", encoding="utf-8")
        (out / f"naturalness-{direction}.key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["generate", "score", "pack"])
    ap.add_argument("--config", required=True)
    ap.add_argument("--model")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--out")
    ap.add_argument("--gpu-mem-gb", type=float, help="per-process GPU memory ceiling (GB)")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    out = Path(a.out or cfg["out_dir"])
    if a.command == "generate":
        generate(cfg, a.model, a.limit, out, a.gpu_mem_gb)
    elif a.command == "score":
        res = score(cfg, out)
        (out / "scores.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(json.dumps(res["best"], indent=1), json.dumps(res["decision_rule"]))
    else:
        pack(cfg, out)


if __name__ == "__main__":
    main()
