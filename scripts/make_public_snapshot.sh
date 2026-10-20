#!/usr/bin/env bash
# Build the public DiaGrad tree from a commit of the private repository, minus scripts/public-exclude.txt,
# with the wording in scripts/public-rewrites.yaml replaced. Both lists are read from the working tree,
# so older commits are built with the current rules.
#   bash scripts/make_public_snapshot.sh <commit> <empty-target-dir>
# Writes PUBLIC-SNAPSHOT.json in the target: source commit, file count, excluded files per category,
# rewrites per file.
set -euo pipefail
rev=$1; out=$2
[ -z "$(ls -A "$out" 2>/dev/null)" ] || { echo "target not empty: $out" >&2; exit 1; }
mkdir -p "$out"
root=$(git rev-parse --show-toplevel)
python3 - "$root" "$rev" "$out" <<'PY'
import fnmatch, io, json, re, subprocess, sys, tarfile
from pathlib import Path
import yaml
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
# Rewrites: `old` may occur at most once (zero where the commit predates the text); afterwards no
# forbidden pattern may match anywhere in the tree.
rules = yaml.safe_load(open(f"{root}/scripts/public-rewrites.yaml", encoding="utf-8"))
rewritten = Counter()
def texts():
    for f in sorted(Path(out).rglob("*")):
        if f.is_file():
            try:
                yield f, f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pass
# Pattern rewrites: every match in every text file (optionally limited to `paths` globs).
for r in rules.get("patterns", []):
    pat = re.compile(r["pattern"], re.M)
    for f, text in texts():
        rel = str(f.relative_to(out))
        if r.get("paths") and not any(fnmatch.fnmatchcase(rel, g) for g in r["paths"]):
            continue
        new, n = pat.subn(r["replace"], text)
        if n:
            f.write_text(new, encoding="utf-8")
            rewritten[rel] += n
for r in rules["rewrites"]:
    f = Path(out, r["path"])
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    n = text.count(r["old"])
    if n > 1:
        sys.exit(f"rewrite matches {n} times in {r['path']}: {r['old'][:60]!r}")
    if n:
        f.write_text(text.replace(r["old"], r["new"]), encoding="utf-8")
        rewritten[r["path"]] += 1
bad = []
for f, text in texts():
    for pat in rules["forbidden"]:
        for m in re.finditer(pat, text, re.M):
            line = text[:m.start()].count("\n") + 1
            bad.append(f"{f.relative_to(out)}:{line}: {pat}")
if bad:
    sys.exit("forbidden wording left in the public tree:\n" + "\n".join(bad))
json.dump({"source": "private DiaGrad working repository", "source_commit": sha, "files": kept,
           "excluded_files_by_category": dict(sorted(dropped.items())),
           "rewrites_by_file": dict(sorted(rewritten.items()))},
          open(f"{out}/PUBLIC-SNAPSHOT.json", "w"), indent=1)
print(f"kept {kept}, excluded {sum(dropped.values())}, rewrites {sum(rewritten.values())} from {sha[:12]}")
PY
