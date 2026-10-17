"""Measure MADLAD tokens and overlap with NLLB en-tl for candidate D22 sources (D23).

Run in the diagrad:t1 container (needs the pinned MADLAD tokenizer in HF_HOME), NLLB on stdin:
    zcat eng_Latn-tgl_Latn.gz | cut -f1,2 | python -m data.mix.measure_sources OUT.json \
        paracrawl=parquet:/raw/pc/train-00000-of-00001.parquet ebible=ebible:/raw/ebible \
        ccmatrix=moses:/raw/opus-CCMatrix-v1-en-tl/OPUS-CCMatrix.en-tl.txt.zip

For each source: pairs, MADLAD tokens (English + Filipino, with EOS each side), and how many pairs
already appear in NLLB, after the normalisation of the D20 check (diagrad.t1.contamination.norm):
whole pair, English side, Filipino side. Unit: pairs of the source; rate = found pairs / source pairs.
"""
import json
import sys
from pathlib import Path

from diagrad.t1.contamination import norm

MADLAD = ("google/madlad400-3b-mt", "fa184c675da0b5c9e1c8694fccd4e12e2d422094")


def read_parquet(path):
    import pyarrow.parquet as pq
    for row in pq.read_table(path).column("translation").to_pylist():
        yield row["en"], row["tl"]


def read_ebible(folder):
    d = Path(folder)
    en = (d / "eng-engwebp.txt").read_text(encoding="utf-8").split("\n")
    tl = (d / "tgl-tglulb.txt").read_text(encoding="utf-8").split("\n")
    for a, b in zip(en, tl):
        if a.strip() and b.strip() and a.strip() != "<range>" and b.strip() != "<range>":
            yield a, b


def read_moses(path):
    """An OPUS `moses/<pair>.txt.zip`: `<Corpus>.<pair>.en` plus the other side (`.tl` or `.fil`),
    line-aligned. Read inside the zip, never extracted."""
    import io
    import zipfile
    z = zipfile.ZipFile(path)
    names = z.namelist()
    en = next(n for n in names if n.endswith(".en"))
    other = next(n for n in names if n.endswith((".tl", ".fil")))
    with z.open(en) as fa, z.open(other) as fb:
        for a, b in zip(io.TextIOWrapper(fa, encoding="utf-8"), io.TextIOWrapper(fb, encoding="utf-8")):
            a, b = a.rstrip("\n"), b.rstrip("\n")
            if a.strip() and b.strip():
                yield a, b


READERS = {"parquet": read_parquet, "ebible": read_ebible, "moses": read_moses}


def main(out, specs):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MADLAD[0], revision=MADLAD[1])
    sources = {}
    for spec in specs:
        name, rest = spec.split("=", 1)
        kind, path = rest.split(":", 1)
        sources[name] = list(READERS[kind](path))
    stats, keys, pair_tokens = {}, {}, {}
    for name, pairs in sources.items():
        n_tok = 0
        normed = [(norm(a), norm(b)) for a, b in pairs]
        for i in range(0, len(pairs), 4000):
            a = tok([p[0] for p in pairs[i:i + 4000]])["input_ids"]
            b = tok([p[1] for p in pairs[i:i + 4000]])["input_ids"]
            for k, x, y in zip(normed[i:i + 4000], a, b):
                n_tok += len(x) + len(y)
                pair_tokens.setdefault(k, len(x) + len(y))   # first occurrence across sources
        keys[name] = normed
        stats[name] = {"pairs": len(pairs), "madlad_tokens": n_tok,
                       "tokens_per_pair": round(n_tok / max(len(pairs), 1), 2),
                       "duplicate_pairs_within": len(normed) - len(set(normed))}
    all_pairs = {p for v in keys.values() for p in v}
    all_en = {p[0] for p in all_pairs}
    all_tl = {p[1] for p in all_pairs}
    seen_pair, seen_en, seen_tl, lines = set(), set(), set(), 0
    for line in sys.stdin:
        f = line.rstrip("\n").split("\t")
        if len(f) < 2:
            continue
        lines += 1
        a, b = norm(f[0]), norm(f[1])
        if a in all_en:
            seen_en.add(a)
        if b in all_tl:
            seen_tl.add(b)
        if (a, b) in all_pairs:
            seen_pair.add((a, b))
    for name, normed in keys.items():
        n = len(normed)
        s = stats[name]
        s["in_nllb_pair"] = sum(p in seen_pair for p in normed)
        s["in_nllb_en_side"] = sum(p[0] in seen_en for p in normed)
        s["in_nllb_tl_side"] = sum(p[1] in seen_tl for p in normed)
        s["rate_pair_in_nllb"] = round(s["in_nllb_pair"] / n, 4) if n else None
        new = [p for p in normed if p not in seen_pair]
        s["new_pairs_after_dedup"] = len(set(new))
    # Across sources: a pair counted once even if two corpora contain it (e.g. the two Bibles).
    union_new = {p for v in keys.values() for p in v if p not in seen_pair}
    union = {"distinct_pairs_all_sources": len(all_pairs), "new_pairs_not_in_nllb": len(union_new),
             "new_pairs_madlad_tokens": sum(pair_tokens[p] for p in union_new),
             "note": "dedup across all listed sources and against NLLB; tokens of the first occurrence"}
    report = {"nllb_lines_scanned": lines, "union": union, "tokenizer": MADLAD, "normalisation": "diagrad.t1.contamination.norm",
              "sources": stats}
    Path(out).write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
