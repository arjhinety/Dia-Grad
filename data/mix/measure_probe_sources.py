"""Count probe candidates in the parallel corpora (D3): Filipino sides with po/opo and with ay-inversion.

Run in diagrad:t1:
    python -m data.mix.measure_probe_sources OUT_DIR name=kind:path ...
kinds: moses (OPUS txt.zip), ebible (folder), parquet (HF opus_paracrawl), nllb (allenai/nllb tsv.gz,
binned by its LASER score column).

Unit: unique Filipino sides (diagrad.t1.contamination.norm) of 3-40 words, the probe-able length. Rates
= sides with the label / unique sides. Labels: diagrad.t1.gate.label_po_opo and label_ay_inversion (the
ay rule is provisional). For each corpus a seeded sample of up to 200 po/opo pairs is saved beside the
counts (OUT_DIR/<name>.po-sample.jsonl, not committed) for an alignment check.
"""
import gzip
import json
import random
import sys
from pathlib import Path

from data.mix.measure_mono import h64
from data.mix.measure_sources import READERS
from diagrad.t1.contamination import norm
from diagrad.t1.gate import label_ay_inversion, label_po_opo

MIN_W, MAX_W = 3, 40
NLLB_BANDS = (1.2, 1.1, 1.06)                 # LASER score lower bounds; the last band is below 1.06


def read_nllb(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            c = line.split("\t", 3)
            yield c[0], c[1], float(c[2])


def band(score):
    for lo in NLLB_BANDS:
        if score >= lo:
            return f">={lo}"
    return f"<{NLLB_BANDS[-1]}"


def count(pairs, seed=20261019, keep=200):
    """pairs: (en, fil, band). Returns {band: counts} and a reservoir sample of po/opo pairs."""
    seen, out, sample, n_po = set(), {}, [], 0
    rng = random.Random(seed)
    for en, fil, b in pairs:
        n = norm(fil)
        w = n.count(" ") + 1 if n else 0
        if not MIN_W <= w <= MAX_W:
            continue
        h = h64(n)
        if h in seen:
            continue
        seen.add(h)
        c = out.setdefault(b, {"sides": 0, "po_opo": 0, "ay": 0, "both": 0})
        po, ay = label_po_opo(fil), label_ay_inversion(fil)
        c["sides"] += 1
        c["po_opo"] += po
        c["ay"] += ay
        c["both"] += po and ay
        if po:
            n_po += 1
            if len(sample) < keep:
                sample.append({"en": en, "fil": fil, "band": b})
            elif rng.random() < keep / n_po:
                sample[rng.randrange(keep)] = {"en": en, "fil": fil, "band": b}
    for c in out.values():
        c["po_rate"] = c["po_opo"] / c["sides"] if c["sides"] else None
        c["ay_rate"] = c["ay"] / c["sides"] if c["sides"] else None
    return out, sample


def main(out_dir, specs):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        name, rest = spec.split("=", 1)
        kind, path = rest.split(":", 1)
        if kind == "nllb":
            pairs = ((e, f, band(s)) for e, f, s in read_nllb(path))
        else:
            pairs = ((e, f, "all") for e, f in READERS[kind](path))
        counts, sample = count(pairs)
        (out / f"{name}.probe-counts.json").write_text(json.dumps(counts, indent=1) + "\n")
        with open(out / f"{name}.po-sample.jsonl", "w", encoding="utf-8") as f:
            for s in sample:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        print(name, json.dumps(counts), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
