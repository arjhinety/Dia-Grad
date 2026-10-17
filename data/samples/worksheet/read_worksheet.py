"""Read a returned (filled) worksheet PDF (v2: meaning + filipino per item) into a TSV of labels, mapped back to NLLB line numbers.

Run: uv run --no-project --with pypdf python data/samples/worksheet/read_worksheet.py <filled.pdf> <out.tsv>
Paper returns (scans) are typed in by hand into the same TSV columns instead.
"""
import csv
import sys
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent


def clean(v):
    v = "" if v is None else str(v)
    return "" if v in ("/Off", "Off") else v.lstrip("/")


def main(pdf, out):
    fields = {k: clean(v.get("/V")) for k, v in PdfReader(pdf).get_fields().items()}
    item_map = {r["item"]: r["nllb_line"] for r in csv.DictReader(open(HERE / "item-map.tsv"), delimiter="\t")}
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["item", "nllb_line", "meaning", "filipino", "unsure", "note"])
        for item, line in item_map.items():
            k = f"item{int(item):03d}"
            w.writerow([item, line, fields.get(f"{k}_meaning", ""), fields.get(f"{k}_filipino", ""),
                        "yes" if fields.get(f"{k}_unsure") else "", fields.get(f"{k}_note", "")])
    meta = {k: v for k, v in fields.items() if k.startswith("labeller_")}
    missing = [i for i in item_map
               if not fields.get(f"item{int(i):03d}_meaning") or not fields.get(f"item{int(i):03d}_filipino")]
    print("labeller:", meta)
    print("unlabelled items:", missing or "none")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
