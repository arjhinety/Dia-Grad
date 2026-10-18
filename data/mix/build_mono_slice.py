"""Build the tranche-1 monolingual slice for the target encoder's denoising term (D28, roadmap A6).

Run in the diagrad:t1 container (record: data/registry/t1-mono-slice-v1.json):
    python -m data.mix.build_mono_slice pool CONFIG     # filter, dedup, held-out removal -> pool + stats
    python -m data.mix.build_mono_slice select CONFIG   # token budget, sentence segments -> slice + stats

pool, per paragraph (newline-separated, >= 5 words after diagrad.t1.contamination.norm, the unit of
data/mix/measure_mono.py), sources in config order so earlier sources win duplicates:
  1. drop it if its hash is in any MADLAD-400 fil split (clean or noisy; D28 option A);
  2. drop it if an earlier paragraph had the same normalised text (exact dedup across all sources);
  3. drop it if it shares an 8-word run with any held-out item side (fold normalisation, as D20), or
     contains a whole side shorter than 8 words of a `full_rule` set (the gate test set; D28 item 6).
Kept paragraphs go to POOL/pool-*.jsonl.gz with their seeded rank (quality_check.seeded).

select: sources marked `whole` are taken entirely; the rest by ascending rank until the estimated
token budget is met (estimate: words x the source's tokens-per-word from the stats run). Each chosen
paragraph is split into sentences and consecutive sentences are packed into segments of at most
`max_segment_tokens` MADLAD tokens; a single longer sentence is cut at that length. Every segment is
tokenised, so the reported token count is exact (no EOS counted). Each segment is one row with the
columns of data/ROW-PROVENANCE.md adapted to monolingual text (text, lang; no tgt side).
"""
import gzip
import hashlib
import json
import os
import multiprocessing as mp
import re
import sys
from pathlib import Path

from data.mix.measure_mono import MIN_WORDS, h64
from data.mix.quality_check import seeded
from diagrad.t1.contamination import N_FLAG, Index, fold, is_flagged, norm

_INDEX = None
_SENT = re.compile(r"(?<=[.!?])\s+")


def heldout_hit(index, text_norm, whole_short_sides=True):
    """True if the paragraph matches a held-out side under the D20 rule (fold variant). With
    whole_short_sides=False only a run of >= 8 words counts (D28 item 6: MASSIVE sets, whose one- and
    two-word sides such as "wala" would otherwise remove every paragraph containing that word)."""
    best = {}
    index.scan_words("fold", fold(text_norm).split(), best)
    words = index.words["fold"]
    if not whole_short_sides:
        return any(length >= N_FLAG for length, _ in best.values())
    return any(is_flagged(length, len(words[sid]), N_FLAG) for sid, (length, _) in best.items())


def _init_index(items):
    """items = (full-rule items, 8-word-only items)."""
    global _INDEX
    _INDEX = (Index(items[0]), Index(items[1]) if items[1] else None)


def _check(batch):
    full, run8 = _INDEX
    return [heldout_hit(full, n) or (run8 is not None and heldout_hit(run8, n, whole_short_sides=False))
            for _, n in batch]


def _pool(cfg, init, arg):
    # forkserver: the parent has pyarrow threads, and fork() after threads can deadlock a child
    return mp.get_context("forkserver").Pool(cfg["workers"], initializer=init, initargs=(arg,))


def read_docs(src):
    """(text, doc_id, url) for every row of every *.parquet under src["path"] (sorted); column names
    from src["columns"] (keys text, id, url)."""
    import pyarrow.parquet as pq
    col = src["columns"]
    p = Path(src["path"])
    for f in (sorted(p.rglob("*.parquet")) if p.is_dir() else [p]):
        for b in pq.ParquetFile(f).iter_batches(columns=[col["text"], col["id"], col["url"]], batch_size=4096):
            d = b.to_pydict()
            for text, i, u in zip(d[col["text"]], d[col["id"]], d[col["url"]]):
                if text:
                    yield text, i, u


def paragraphs(text):
    for raw in text.split("\n"):
        n = norm(raw)
        if n.count(" ") + 1 >= MIN_WORDS:
            yield raw.strip(), n


def pool(cfg):
    import numpy as np
    out = Path(cfg["pool_dir"])
    out.mkdir(parents=True, exist_ok=True)
    def load(files):
        return [json.loads(l) for f in files for l in open(f, encoding="utf-8") if l.strip()]
    items = (load(cfg["heldout"]["full_rule"]), load(cfg["heldout"].get("eight_word_runs_only", [])))
    ldir = Path(cfg["lines_dir"])
    madlad = np.unique(np.concatenate([np.load(ldir / f) for f in cfg["madlad_lines"]]))
    seen = set()
    stats = {}
    with _pool(cfg, _init_index, items) as workers:
        for src in cfg["sources"]:
            name, docs = src["name"], read_docs(src)
            c = dict(documents=0, paragraphs=0, in_madlad=0, duplicate=0, heldout=0, kept=0, kept_words=0)
            fh = gzip.open(out / f"pool-{name}.jsonl.gz", "wt", encoding="utf-8")
            buf = []

            def flush():
                if not buf:
                    return
                hs = np.array([b[0] for b in buf], dtype=np.int64)
                in_m = np.isin(hs, madlad)
                cand = []
                for b, m in zip(buf, in_m):
                    h = b[0]
                    if m:
                        c["in_madlad"] += 1
                    elif h in seen:
                        c["duplicate"] += 1
                    else:
                        seen.add(h)
                        cand.append(b)
                chunks = [cand[i:i + 2000] for i in range(0, len(cand), 2000)]
                flags = [x for part in workers.map(_check, [[(b[0], b[2]) for b in ch] for ch in chunks]) for x in part]
                for (h, raw, n, doc, url, k), hit in zip(cand, flags):
                    if hit:
                        c["heldout"] += 1
                        continue
                    w = len(raw.split())
                    c["kept"] += 1
                    c["kept_words"] += w
                    fh.write(json.dumps({"id": h, "src": name, "doc": doc, "url": url, "para_index": k,
                                         "rank": seeded(cfg["seed"], n), "words": w, "text": raw},
                                        ensure_ascii=False) + "\n")
                buf.clear()

            for text, doc, url in docs:
                c["documents"] += 1
                for k, (raw, n) in enumerate(paragraphs(text)):
                    c["paragraphs"] += 1
                    buf.append((h64(n), raw, n, doc, url, k))
                if len(buf) >= 200000:
                    flush()
            flush()
            fh.close()
            stats[name] = c
            print(name, json.dumps(c), flush=True)
    (out / "pool-stats.json").write_text(json.dumps(stats, indent=1) + "\n")


def segments(text, tok, max_tokens):
    """Pack consecutive sentences into segments of <= max_tokens tokens; cut a longer sentence."""
    segs, cur, cur_n = [], [], 0
    for s in _SENT.split(text):
        s = s.strip()
        if not s:
            continue
        n = len(tok(s, add_special_tokens=False).input_ids)
        if n > max_tokens:
            if cur:
                segs.append(" ".join(cur))
                cur, cur_n = [], 0
            ids = tok(s, add_special_tokens=False).input_ids
            for i in range(0, len(ids), max_tokens):
                segs.append(tok.decode(ids[i:i + max_tokens]).strip())
            continue
        if cur and cur_n + n > max_tokens:
            segs.append(" ".join(cur))
            cur, cur_n = [], 0
        cur.append(s)
        cur_n += n
    if cur:
        segs.append(" ".join(cur))
    return segs


_TOK = None


def _init_tok(spec):
    global _TOK
    from transformers import AutoTokenizer
    _TOK = AutoTokenizer.from_pretrained(spec[0], revision=spec[1])


FILTERS = ["madlad400_fil_absent", "exact_paragraph_dedup", "heldout_d20_paragraph_clear"]


def row_meta(registry_dir, registry_id, version):
    """Per-source columns of data/ROW-PROVENANCE.md, adapted to monolingual rows, from the record."""
    r = json.loads((Path(registry_dir) / f"{registry_id}.json").read_text(encoding="utf-8"))
    return {"source_dataset": r["id"], "source_revision": r["source_revision"]["value"], "lang": r["languages"][0],
            "source_license": r["license"]["spdx"], "use_class": r["use_class"],
            "redistribution_status": r["redistribution"]["status"], "text_origin": r["text_origin"]["kind"],
            "synthetic_tag": "", "normaliser_version": version, "filters_passed": FILTERS,
            "contamination_status": "PARAGRAPH_D20_CLEAR"}


def _seg_work(args):
    rows, max_tokens, meta = args
    out = []
    for r in rows:
        for k, s in enumerate(segments(r["text"], _TOK, max_tokens)):
            out.append({"diagrad_id": f"{meta['source_dataset']}:{r['doc']}:{r['para_index']}:{k}", "text": s,
                        **meta, "source_record_id": r["doc"], "source_url": r["url"] or "",
                        "tokens": len(_TOK(s, add_special_tokens=False).input_ids),
                        "row_sha256": hashlib.sha256(s.encode("utf-8")).hexdigest()})
    return out


def select(cfg):
    pdir, out = Path(cfg["pool_dir"]), Path(cfg["slice_dir"])
    out.mkdir(parents=True, exist_ok=True)
    tpw = cfg["tokens_per_word"]
    whole = [s["name"] for s in cfg["sources"] if s.get("whole")]
    rest = [s["name"] for s in cfg["sources"] if not s.get("whole")]

    def rows(name):
        with gzip.open(pdir / f"pool-{name}.jsonl.gz", "rt", encoding="utf-8") as f:
            for line in f:
                yield json.loads(line)

    budget = cfg["token_budget"] - sum(r["words"] * tpw[n] for n in whole for r in rows(n))
    ranked = sorted(((r["rank"], r["words"] * tpw[n]) for n in rest for r in rows(n)))
    total, cut = 0.0, None
    for rank, est in ranked:
        if total >= budget:
            cut = rank
            break
        total += est
    stats = {"rank_cut": cut, "estimated_tokens_rest": total, "sources": {}}
    version = os.environ.get("DIAGRAD_COMMIT", "unknown")
    digests = []
    with _pool(cfg, _init_tok, cfg["tokenizer"]) as workers, gzip.open(out / "slice.jsonl.gz", "wt", encoding="utf-8") as fh:
        for s in cfg["sources"]:
            n = s["name"]
            c = dict(paragraphs=0, segments=0, tokens=0)
            batch, jobs = [], []
            meta = row_meta(cfg["registry_dir"], s["registry_id"], version)

            def run():
                for part in workers.imap(_seg_work, [(b, cfg["max_segment_tokens"], meta) for b in jobs]):
                    for seg in part:
                        c["segments"] += 1
                        c["tokens"] += seg["tokens"]
                        digests.append(seg["row_sha256"])
                        fh.write(json.dumps(seg, ensure_ascii=False) + "\n")
                jobs.clear()

            for r in rows(n):
                if not s.get("whole") and cut is not None and r["rank"] >= cut:
                    continue
                c["paragraphs"] += 1
                batch.append(r)
                if len(batch) == 5000:
                    jobs.append(batch)
                    batch = []
                if len(jobs) == 4 * cfg["workers"]:
                    run()
            if batch:
                jobs.append(batch)
            run()
            stats["sources"][n] = c
            print(n, json.dumps(c), flush=True)
    stats["tokens"] = sum(c["tokens"] for c in stats["sources"].values())
    stats["normaliser_version"] = version
    # processed_sha256 (data/ROW-PROVENANCE.md): sha256 over the sorted row_sha256 values
    stats["processed_sha256"] = hashlib.sha256("\n".join(sorted(digests)).encode()).hexdigest()
    (out / "slice-stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    print(json.dumps(stats))


if __name__ == "__main__":
    import yaml
    cmd, cfg = sys.argv[1], yaml.safe_load(open(sys.argv[2], encoding="utf-8"))
    {"pool": pool, "select": select}[cmd](cfg)
