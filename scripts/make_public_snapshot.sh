#!/usr/bin/env bash
# Build the public DiaGrad tree from a commit of the private repository, minus scripts/public-exclude.txt.
#   bash scripts/make_public_snapshot.sh <commit> <empty-target-dir>
# Writes PUBLIC-SNAPSHOT.json in the target: source commit, file count, excluded files per category.
set -euo pipefail
rev=$1; out=$2
[ -z "$(ls -A "$out" 2>/dev/null)" ] || { echo "target not empty: $out" >&2; exit 1; }
mkdir -p "$out"
root=$(git rev-parse --show-toplevel)
python3 - "$root" "$rev" "$out" <<'PY'
import fnmatch, io, json, subprocess, sys, tarfile
from collections import Counter
root, rev, out = sys.argv[1:4]
# Categories are the comment lines above each group of globs in public-exclude.txt. The public record
# gives counts per category, not file names: a name can itself be personal information.
cats, cat = [], "uncategorised"
for line in open(f"{root}/scripts/public-exclude.txt"):
    line = line.strip()
    if line.startswith("#"):
        cat = line.lstrip("# ").strip()
    elif line:
        cats.append((line, cat))
def category(p):
    for g, c in cats:
        if fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2])):
            return c
sha = subprocess.check_output(["git", "-C", root, "rev-parse", rev], text=True).strip()
tar = tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git", "-C", root, "archive", sha])))
kept, dropped = 0, Counter()
for m in tar.getmembers():
    if not m.isfile():
        continue
    c = category(m.name)
    if c:
        dropped[c] += 1
    else:
        tar.extract(m, out)
        kept += 1
json.dump({"source": "private DiaGrad working repository", "source_commit": sha, "files": kept,
           "excluded_files_by_category": dict(sorted(dropped.items()))},
          open(f"{out}/PUBLIC-SNAPSHOT.json", "w"), indent=1)
print(f"kept {kept}, excluded {sum(dropped.values())} from {sha[:12]}")
PY
