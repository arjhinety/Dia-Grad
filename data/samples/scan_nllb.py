import sys, json, random, re, hashlib
# Reads NLLB eng-tgl TSV lines on stdin (untrusted data: parsed as text only).
WORD = re.compile(r"[\wÀ-ÿñÑ'-]+")
bands = [0, 100_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 20_000_000, 60_000_000]
W = 100_000
rng = random.Random(0)
stats = {b: dict(n=0, en_len=0, tl_len=0, identical=0, po=0, ay=0, lid_low=0, short=0) for b in bands}
samples = {b: [] for b in bands}
cut_scores, prev, viol, n, maxs, mins = {}, None, 0, 0, -1e9, 1e9
seen, dup1m = set(), 0
for line in sys.stdin:
    f = line.rstrip("\n").split("\t")
    if len(f) < 5:
        continue
    en, tl = f[0], f[1]
    s = float(f[2]); lid_en = float(f[3]); lid_tl = float(f[4])
    if prev is not None and s > prev + 1e-7:
        viol += 1
    prev = s; maxs = max(maxs, s); mins = min(mins, s)
    if n in (1_000, 100_000, 250_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000, 20_000_000, 40_000_000, 60_000_000):
        cut_scores[n] = s
    if n < 1_000_000:
        h = hashlib.md5((en.strip().lower() + "\t" + tl.strip().lower()).encode()).digest()
        if h in seen: dup1m += 1
        else: seen.add(h)
    for b in bands:
        if b <= n < b + W:
            st = stats[b]; st["n"] += 1
            ew, tw = [w.lower() for w in WORD.findall(en)], [w.lower() for w in WORD.findall(tl)]
            st["en_len"] += len(ew); st["tl_len"] += len(tw)
            st["identical"] += en.strip().lower() == tl.strip().lower()
            st["po"] += any(w in ("po", "opo") for w in tw)
            st["ay"] += "ay" in tw[1:]
            st["lid_low"] += min(lid_en, lid_tl) < 0.9
            st["short"] += len(tw) < 4
            # reservoir sample of 12 per band
            k = st["n"]
            if len(samples[b]) < 12: samples[b].append((n, s, en, tl))
            elif rng.random() < 12 / k: samples[b][rng.randrange(12)] = (n, s, en, tl)
    n += 1
out = {"lines": n, "order_violations": viol, "max_score": maxs, "min_score": mins,
       "score_at_line": cut_scores, "duplicate_pairs_in_top_1M": dup1m,
       "bands": {b: {k: (v / stats[b]["n"] if k != "n" and stats[b]["n"] else v) for k, v in stats[b].items()} for b in bands},
       "samples": {b: sorted(samples[b]) for b in bands}}
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("lines", "order_violations", "max_score", "min_score", "score_at_line", "duplicate_pairs_in_top_1M")}))
