import sys, random, csv
# Uniform random sample of 100 lines from the first 1,000,000 (seed 20261008). Untrusted text, parsed only.
rng = random.Random(20261008)
pick = set(rng.sample(range(1_000_000), 100))
w = csv.writer(open(sys.argv[1], "w", newline="", encoding="utf-8"), delimiter="\t", lineterminator="\n")
w.writerow(["line", "laser_score", "english", "tagalog", "label", "note"])
for i, line in enumerate(sys.stdin):
    if i in pick:
        f = line.rstrip("\n").split("\t")
        w.writerow([i + 1, f[2], f[0].replace("\t", " "), f[1].replace("\t", " "), "", ""])
