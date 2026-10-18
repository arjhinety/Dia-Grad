"""Measure candidate monolingual Filipino corpora for the target encoder (D4).

Run in the diagrad:t1 container (needs the pinned MADLAD tokenizer in HF_HOME):
    python -m data.mix.measure_mono stats OUT_DIR fineweb2=parquet:/raw/fineweb2-.../data/fil_Latn/train \
        madlad=madlad:/raw/madlad400-fil-.../data/fil/fil_clean_0000.jsonl.gz ...
    python -m data.mix.measure_mono overlap OUT_DIR            # after stats, for every pair of corpora
    python -m data.mix.measure_mono lines SPEC | python -m diagrad.t1.contamination ...   # D20 check
    python -m data.mix.measure_mono features OUT_DIR SPEC ...  # po/opo and ay rates on the sample

stats, per corpus: documents, lines, words (whitespace), MADLAD tokens, exact duplicate documents, and
the unique "lines" (newline-separated paragraphs of >= 5 words after diagrad.t1.contamination.norm),
hashed to 64 bits and saved as OUT_DIR/<name>.lines.npy. MADLAD tokens are measured on the documents
whose hash falls in a fixed 1-in-SAMPLE subset and scaled by words: tokens = words x (sample tokens /
sample words). No EOS is counted.

overlap: for each ordered pair (A, B), the share of A's unique lines that also occur in B.
Unit: unique normalised lines of >= 5 words; rate = A's lines found in B / A's unique lines. A 64-bit
hash collision can only add matches; at 1e8 lines the expected number of false matches is below 1e-3.

features, on the same 1-in-SAMPLE documents: sentences (split after . ! ? followed by space, >= 3
words) and how many carry po/opo and ay-inversion by the gate's labellers (diagrad.t1.gate; the ay
rule is provisional). Unit: sentences of the sample; rate = labelled sentences / sample sentences.
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path

from diagrad.t1.contamination import norm

MADLAD = ("google/madlad400-3b-mt", "fa184c675da0b5c9e1c8694fccd4e12e2d422094")
MIN_WORDS = 5
SAMPLE = 200


def h64(s):
    return int.from_bytes(hashlib.blake2b(s.encode("utf-8"), digest_size=8).digest(), "little", signed=True)


def read_parquet(path, column="text"):
    """Every *.parquet under path (sorted), or the one file; column 'text' unless given as path#col."""
    import pyarrow.parquet as pq
    p = Path(path)
    files = sorted(p.rglob("*.parquet")) if p.is_dir() else [p]
    for f in files:
        pf = pq.ParquetFile(f)
        for batch in pf.iter_batches(columns=[column], batch_size=4096):
            for t in batch.column(0).to_pylist():
                if t:
                    yield t


def read_jsonlgz(path, field="text", literal_newlines=False):
    p = Path(path)
    for f in (sorted(p.rglob("*.jsonl.gz")) if p.is_dir() else [p]):
        with gzip.open(f, "rt", encoding="utf-8") as fh:
            for line in fh:
                t = json.loads(line).get(field)
                if t:
                    yield t.replace("\\n", "\n") if literal_newlines else t


def read_madlad(path):
    """MADLAD-400 jsonl.gz: line breaks inside 'text' are stored as the two characters backslash, n."""
    return read_jsonlgz(path, literal_newlines=True)


READERS = {"parquet": read_parquet, "jsonlgz": read_jsonlgz, "madlad": read_madlad}


def open_spec(spec):
    """name=kind:path[#column]"""
    name, rest = spec.split("=", 1)
    kind, path = rest.split(":", 1)
    path, _, col = path.partition("#")
    return name, (READERS[kind](path, col) if col else READERS[kind](path))


def doc_lines(text):
    """Normalised lines of >= MIN_WORDS words."""
    for raw in text.split("\n"):
        n = norm(raw)
        if n.count(" ") + 1 >= MIN_WORDS:
            yield n


def stats(out_dir, specs):
    import numpy as np
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MADLAD[0], revision=MADLAD[1])
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    report = {}
    for spec in specs:
        name, docs = open_spec(spec)
        c = dict(documents=0, lines_total=0, lines_kept=0, words=0, chars=0, sample_docs=0,
                 sample_words=0, sample_tokens=0)
        hashes, doc_hashes = [], set()
        dup_docs = 0
        for text in docs:
            c["documents"] += 1
            c["chars"] += len(text)
            w = len(text.split())
            c["words"] += w
            dh = h64(norm(text))
            if dh in doc_hashes:
                dup_docs += 1
            doc_hashes.add(dh)
            if dh % SAMPLE == 0:
                c["sample_docs"] += 1
                c["sample_words"] += w
                c["sample_tokens"] += len(tok(text, add_special_tokens=False)["input_ids"])
            c["lines_total"] += text.count("\n") + 1
            for line in doc_lines(text):
                c["lines_kept"] += 1
                hashes.append(h64(line))
        u = np.unique(np.array(hashes, dtype=np.int64))
        np.save(out / f"{name}.lines.npy", u)
        c["unique_lines"] = int(u.size)
        c["duplicate_documents"] = dup_docs
        c["tokens_per_word"] = c["sample_tokens"] / c["sample_words"] if c["sample_words"] else None
        c["madlad_tokens_est"] = round(c["words"] * c["tokens_per_word"]) if c["sample_words"] else None
        c["spec"] = spec
        report[name] = c
        print(name, json.dumps(c), flush=True)
        (out / f"{name}.stats.json").write_text(json.dumps(c, indent=1) + "\n")
    return report


def overlap(out_dir):
    import numpy as np
    out = Path(out_dir)
    sets = {p.name[:-len(".lines.npy")]: np.load(p) for p in sorted(out.glob("*.lines.npy"))}
    m = {}
    for a, ua in sets.items():
        m[a] = {}
        for b, ub in sets.items():
            if a != b:
                found = int(np.isin(ua, ub, assume_unique=True).sum())
                m[a][b] = {"found": found, "of": int(ua.size), "rate": found / ua.size if ua.size else None}
    rep = {"unit": f"unique normalised lines of >= {MIN_WORDS} words; rate = lines of row found in column / "
                   "unique lines of row", "normalisation": "diagrad.t1.contamination.norm", "matrix": m}
    (out / "overlap.json").write_text(json.dumps(rep, indent=1) + "\n")
    names = list(sets)
    print("row in column".ljust(14) + "".join(n[:10].rjust(11) for n in names))
    for a in names:
        print(a[:14].ljust(14) + "".join(("-" if a == b else f"{m[a][b]['rate']:.3f}").rjust(11) for b in names))


def sentences(text):
    import re
    for line in text.split("\n"):
        for s in re.split(r"(?<=[.!?])\s+", line):
            if len(s.split()) >= 3:
                yield s


def features(out_dir, specs):
    from diagrad.t1.gate import label_ay_inversion, label_po_opo
    out = Path(out_dir)
    for spec in specs:
        name, docs = open_spec(spec)
        c = dict(sample_docs=0, sentences=0, po_opo=0, ay=0)
        for text in docs:
            if h64(norm(text)) % SAMPLE:
                continue
            c["sample_docs"] += 1
            for s in sentences(text):
                c["sentences"] += 1
                c["po_opo"] += label_po_opo(s)
                c["ay"] += label_ay_inversion(s)
        n = c["sentences"]
        c["po_opo_rate"] = c["po_opo"] / n if n else None
        c["ay_rate"] = c["ay"] / n if n else None
        print(name, json.dumps(c), flush=True)
        (out / f"{name}.features.json").write_text(json.dumps(c, indent=1) + "\n")


def lines(spec):
    """Each raw line (paragraph) of the corpus as a training 'sentence' for the D20 checker."""
    _, docs = open_spec(spec)
    w = sys.stdout.write
    for text in docs:
        for raw in text.split("\n"):
            if raw.strip():
                w(raw.replace("\t", " ") + "\t\n")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "stats":
        stats(args[0], args[1:])
    elif cmd == "overlap":
        overlap(args[0])
    elif cmd == "features":
        features(args[0], args[1:])
    elif cmd == "lines":
        lines(args[0])
    else:
        sys.exit(f"unknown command {cmd}")
