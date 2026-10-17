"""Contamination check: A5 §3.2 as adopted for tranche 1 (D20). Standard library only.

Unit: one test item = one sentence pair. Every rate is flagged items / total items (A5 §3.2).

For each item side (English, Filipino) the check finds the longest contiguous run of words that also
occurs in any training sentence (either column). An item is flagged at n = 8 if either side has a
matching run of at least 8 words, or, for a side shorter than 8 words, if the whole side occurs inside
a training sentence (ConTAM longest-match, skip budget 0). The 13-word flag (GPT-3) is reported too.
Exact matches of the whole source, target and pair are counted separately. A side's reported
"longest" is exact when it reaches min(8, side length); 0 means the longest match is shorter.

Text is normalised twice: "plain" (NFKC, lowercase, punctuation to spaces, whitespace collapsed; the
same as data/heldout/build_heldout.py) and "fold" (plain, then diacritics removed). Fold can only add
matches, so it is the primary flag; plain is reported beside it.

Run (training lines on stdin as tab-separated English and Filipino; other columns are ignored):
    zcat nllb.gz | cut -f1,2 | python -m diagrad.t1.contamination --out report.json \
        --summary summary.json --train-name NAME test1.jsonl test2.jsonl
"""
import argparse
import hashlib
import json
import multiprocessing as mp
import platform
import re
import sys
import unicodedata
from itertools import islice
from pathlib import Path

N_FLAG, N_GPT3 = 8, 13
VARIANTS = ("plain", "fold")
_PUNCT = re.compile(r"[^\w\s]")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    return " ".join(_PUNCT.sub(" ", s).split())


def fold(s: str) -> str:
    """Remove diacritics from already-normalised text (e.g. 'ñ' -> 'n', 'â' -> 'a')."""
    if s.isascii():
        return s
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def flag_rate(flagged: int, total: int) -> float:
    """Flagged items / total items. Both counts are items, never spans or sides."""
    if total <= 0 or not 0 <= flagged <= total:
        raise ValueError(f"need 0 <= flagged <= total, total > 0; got {flagged}/{total}")
    return flagged / total


def is_flagged(longest: int, length: int, n: int) -> bool:
    """A side is flagged if its longest training match is >= n words, or covers it when shorter."""
    return length > 0 and longest >= min(n, length)


class Index:
    """Anchors built from the test items; matched against training sentences."""

    def __init__(self, items):
        self.items = items
        self.words = {v: [] for v in VARIANTS}             # [variant][sid] -> list of words
        self.anchor = {v: {} for v in VARIANTS}            # [variant][n][key] -> [(sid, pos)]
        self.first = {v: {} for v in VARIANTS}             # [variant][n][first word] -> {last words}
        self.exact = {v: {} for v in VARIANTS}             # [variant][side text] -> [sid]
        self.pair = {v: {} for v in VARIANTS}              # [variant][(en, fil)] -> [item index]
        for k, it in enumerate(items):
            texts = {"plain": [norm(it["src"]), norm(it["tgt"])]}
            texts["fold"] = [fold(t) for t in texts["plain"]]
            for v in VARIANTS:
                self.pair[v].setdefault(tuple(texts[v]), []).append(k)
                for s, t in enumerate(texts[v]):
                    sid = 2 * k + s
                    w = t.split()
                    self.words[v].append(w)
                    if not w:
                        continue
                    self.exact[v].setdefault(t, []).append(sid)
                    n = min(N_FLAG, len(w))
                    for p in range(len(w) - n + 1):
                        self.anchor[v].setdefault(n, {}).setdefault(" ".join(w[p:p + n]), []).append((sid, p))
                        self.first[v].setdefault(n, {}).setdefault(w[p], set()).add(w[p + n - 1])

    def scan_words(self, v, w, best):
        """Update best[sid] = (length, span) with the longest run each item side shares with w."""
        words = self.words[v]
        for n, firsts in self.first[v].items():
            table = self.anchor[v][n]
            for i in range(len(w) - n + 1):
                lasts = firsts.get(w[i])
                if lasts is None or w[i + n - 1] not in lasts:
                    continue
                for sid, p in table.get(" ".join(w[i:i + n]), ()):
                    a = words[sid]
                    if best.get(sid, (0,))[0] == len(a):
                        continue
                    lo = 0
                    while i - lo > 0 and p - lo > 0 and w[i - lo - 1] == a[p - lo - 1]:
                        lo += 1
                    hi = n
                    while i + hi < len(w) and p + hi < len(a) and w[i + hi] == a[p + hi]:
                        hi += 1
                    length = lo + hi
                    if length > best.get(sid, (0,))[0]:
                        best[sid] = (length, " ".join(a[p - lo:p + hi]))


_INDEX = None


def _work(lines):
    best = {v: {} for v in VARIANTS}
    exact = {v: set() for v in VARIANTS}
    pairs = {v: set() for v in VARIANTS}
    count = 0
    for line in lines:
        f = line.rstrip("\n").split("\t", 2)
        if len(f) < 2:
            continue
        count += 1
        plain = [norm(f[0]), norm(f[1])]
        for v in VARIANTS:
            cols = plain if v == "plain" else [fold(t) for t in plain]
            for k in _INDEX.pair[v].get(tuple(cols), ()):
                pairs[v].add(k)
            for t in cols:
                exact[v].update(_INDEX.exact[v].get(t, ()))
                _INDEX.scan_words(v, t.split(), best[v])
    return count, best, exact, pairs


def scan(index, lines, workers=1, chunk=20000):
    """Scan training lines; returns (line count, best, exact sids, pair hits) merged over chunks."""
    global _INDEX
    _INDEX = index
    best = {v: {} for v in VARIANTS}
    exact = {v: set() for v in VARIANTS}
    pairs = {v: set() for v in VARIANTS}
    total = 0
    it = iter(lines)
    chunks = iter(lambda: list(islice(it, chunk)), [])
    if workers > 1:
        pool = mp.get_context("fork").Pool(workers)
        results = pool.imap_unordered(_work, chunks, chunksize=1)
    else:
        pool, results = None, map(_work, chunks)
    for count, b, e, p in results:
        total += count
        for v in VARIANTS:
            for sid, val in b[v].items():
                if val[0] > best[v].get(sid, (0,))[0]:
                    best[v][sid] = val
            exact[v] |= e[v]
            pairs[v] |= p[v]
    if pool:
        pool.close()
        pool.join()
    return total, best, exact, pairs


def item_results(index, best, exact, pairs):
    """Per item and variant: longest match per side, flags at 8 and 13, exact hits."""
    out = []
    for k, it in enumerate(index.items):
        r = {"id": it["id"]}
        for v in VARIANTS:
            sides = []
            for s in (0, 1):
                sid = 2 * k + s
                length = len(index.words[v][sid])
                longest, span = best[v].get(sid, (0, ""))
                sides.append({"words": length, "longest": longest, "span": span,
                              "flag8": is_flagged(longest, length, N_FLAG),
                              "flag13": is_flagged(longest, length, N_GPT3),
                              "exact": sid in exact[v]})
            r[v] = {"src": sides[0], "tgt": sides[1], "pair_exact": k in pairs[v],
                    "flag8": sides[0]["flag8"] or sides[1]["flag8"],
                    "flag13": sides[0]["flag13"] or sides[1]["flag13"]}
        out.append(r)
    return out


def summarise(results):
    """Counts and rates per variant. Every rate is flagged items / total items."""
    total = len(results)
    s = {"items": total}
    for v in VARIANTS:
        c = {
            "flag8": sum(r[v]["flag8"] for r in results),
            "flag13": sum(r[v]["flag13"] for r in results),
            "src_flag8": sum(r[v]["src"]["flag8"] for r in results),
            "tgt_flag8": sum(r[v]["tgt"]["flag8"] for r in results),
            "src_exact": sum(r[v]["src"]["exact"] for r in results),
            "tgt_exact": sum(r[v]["tgt"]["exact"] for r in results),
            "pair_exact": sum(r[v]["pair_exact"] for r in results),
        }
        c["rate8"] = flag_rate(c["flag8"], total)
        c["rate13"] = flag_rate(c["flag13"], total)
        c["clean_items"] = total - c["flag8"]
        c["flagged_ids"] = [r["id"] for r in results if r[v]["flag8"]]
        s[v] = c
    return s


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tests", nargs="+", help="test sets as JSONL with src, tgt, id")
    ap.add_argument("--out", required=True, help="full report, with matched spans (keep outside the repo)")
    ap.add_argument("--summary", required=True, help="counts, rates and flagged ids only, no text")
    ap.add_argument("--train-name", required=True, help="what stdin holds, e.g. a registry record and sha256")
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args(argv)

    sets = {}
    for p in a.tests:
        with open(p, encoding="utf-8") as f:
            sets[Path(p).stem] = [json.loads(line) for line in f if line.strip()]
    items = [it for rows in sets.values() for it in rows]
    index = Index(items)
    lines, best, exact, pairs = scan(index, sys.stdin, workers=a.workers)
    results = item_results(index, best, exact, pairs)

    meta = {"procedure": "A5 §3.2 as adopted for tranche 1 (D20)", "train": a.train_name,
            "train_lines": lines, "n_flag": N_FLAG, "n_gpt3": N_GPT3,
            "checker_sha256": _sha256(__file__), "python": platform.python_version(),
            "tests": {name: {"file": p, "sha256": _sha256(p)} for name, p in zip(sets, a.tests)}}
    full, summary, start = dict(meta, sets={}), dict(meta, sets={}), 0
    for name, rows in sets.items():
        part = results[start:start + len(rows)]
        start += len(rows)
        summary["sets"][name] = summarise(part)
        full["sets"][name] = {"summary": summary["sets"][name], "items": part}
    Path(a.out).write_text(json.dumps(full, ensure_ascii=False, indent=1))
    Path(a.summary).write_text(json.dumps(summary, indent=1) + "\n")
    for name, s in summary["sets"].items():
        print(name, s["items"], {v: (s[v]["flag8"], round(s[v]["rate8"], 4), s[v]["flag13"]) for v in VARIANTS})


if __name__ == "__main__":
    main()
