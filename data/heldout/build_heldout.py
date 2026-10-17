"""Build the tranche-1 held-out sets (D19) from the raw downloads.

Run (host Python, no dependencies; reads untrusted text, so run with -I):
    zcat ~/data/raw/nllb-eng_Latn-tgl_Latn/eng_Latn-tgl_Latn.gz | \
      python3 -I data/heldout/build_heldout.py ~/data/raw/massive-1.1/x/1.1/data \
        ~/data/raw/smol-en_fil ~/data/t1/heldout

Outputs (JSONL, one pair per line, the format diagrad.t1.data reads):
    test_smol.jsonl          gate test set: all SMOL SmolSent en-fil pairs (opened only at G1 and G6)
    dev_massive.jsonl        dev set: MASSIVE 1.1 tl-PH dev, minus pairs with either side in NLLB
    diag_massive_test.jsonl  diagnostic: MASSIVE tl-PH test, minus pairs with either side in NLLB
    manifest.json            counts, removed ids, sha256 of every output
NLLB lines are read from stdin and compared after the same normalisation used in D19's check
(NFKC, lowercase, punctuation to spaces, whitespace collapsed).
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return " ".join(s.split())


def load(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main(massive_dir, smol_dir, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    en = {r["id"]: r for r in load(f"{massive_dir}/en-US.jsonl")}
    tl = load(f"{massive_dir}/tl-PH.jsonl")

    def massive(split):
        return [{"src": en[r["id"]]["utt"], "tgt": r["utt"], "src_lang": "en", "tgt_lang": "fil",
                 "id": f"massive-1.1:{r['id']}", "source": f"MASSIVE 1.1 tl-PH {split}"}
                for r in tl if r["partition"] == split and r["id"] in en]

    smol = [{"src": r["src"], "tgt": r["trg"], "src_lang": "en", "tgt_lang": "fil",
             "id": f"smol-smolsent:{r['id']}", "source": "SMOL SmolSent en_fil"}
            for r in load(f"{smol_dir}/smolsent_en_fil.jsonl")]
    sets = {"test_smol": smol, "dev_massive": massive("dev"), "diag_massive_test": massive("test")}

    en_keys = {norm(r["src"]) for rows in sets.values() for r in rows}
    tl_keys = {norm(r["tgt"]) for rows in sets.values() for r in rows}
    seen_en, seen_tl, lines = set(), set(), 0
    for line in sys.stdin:
        f = line.split("\t", 2)
        if len(f) < 2:
            continue
        lines += 1
        a, b = norm(f[0]), norm(f[1])
        if a in en_keys:
            seen_en.add(a)
        if b in tl_keys:
            seen_tl.add(b)

    manifest = {"nllb_lines_scanned": lines, "normalisation": "NFKC, lowercase, punctuation->space, collapse",
                "sets": {}}
    for name, rows in sets.items():
        hit = [r for r in rows if norm(r["src"]) in seen_en or norm(r["tgt"]) in seen_tl]
        keep = rows if name == "test_smol" else [r for r in rows if r not in hit]
        path = out / f"{name}.jsonl"
        with open(path, "w", encoding="utf-8") as fh:
            for r in keep:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        manifest["sets"][name] = {
            "file": path.name, "pairs_in": len(rows), "found_in_nllb": len(hit),
            "removed_ids": [r["id"] for r in hit] if name != "test_smol" else [],
            "pairs_out": len(keep), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        if name == "test_smol" and hit:
            manifest["sets"][name]["WARNING"] = "test pairs found in NLLB; D19 assumed none"
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps({k: {x: v[x] for x in ("pairs_in", "found_in_nllb", "pairs_out", "sha256")}
                      for k, v in manifest["sets"].items()}, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
