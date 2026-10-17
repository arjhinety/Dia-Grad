"""Recorded search protocol: run literature searches and keep an auditable record of them.

Inputs (research/search/):
  queries.json    the searches, each with an id, the question it serves, and the query text
  screening.json  include/exclude decisions per paper, each with a reason

Outputs (research/search/):
  log.jsonl       append-only: every executed search with timestamp, tool version and full hit list
  SEARCH-LOG.md   human-readable summary: per query, the hits and their screening status

Usage:
  python research/tools/search_log.py run [QUERY_ID ...]   # execute queries (all if none given)
  python research/tools/search_log.py report               # rebuild SEARCH-LOG.md from the log

Re-running a query appends a new dated entry rather than overwriting, so the record shows how
the literature changed between searches.
"""
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "search"))
LOG = os.path.join(ROOT, "log.jsonl")
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def load(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return json.load(f)


def pwc(*args):
    r = subprocess.run(["pwc", *args], capture_output=True, env=ENV)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "replace"))
    return r.stdout.decode("utf-8")


def run(ids):
    version = pwc("version").strip()
    queries = [q for q in load("queries.json")["queries"] if not ids or q["id"] in ids]
    with open(LOG, "a", encoding="utf-8") as log:
        for q in queries:
            args = ["search", q["query"], "--limit", str(q.get("limit", 8)), "--json"]
            if q.get("mode"):
                args += ["--mode", q["mode"]]
            if q.get("start_date"):  # recency filter, e.g. "2025-01-01", to surface current work
                args += ["--start-date", q["start_date"]]
            data = json.loads(pwc(*args))["data"]["results"]
            hits = [{"rank": i + 1, "arxiv": h.get("arxiv_id"), "catalog_id": h.get("id"),
                     "title": " ".join(h["title"].split()), "published": h.get("published"),
                     "citations": h.get("citation_count")} for i, h in enumerate(data)]
            log.write(json.dumps({"time": now(), "tool": version, "query_id": q["id"],
                                  "query": q["query"], "args": args, "hits": hits},
                                 ensure_ascii=False) + "\n")
            print(f"{q['id']}: {len(hits)} hits")


def report():
    queries = {q["id"]: q for q in load("queries.json")["queries"]}
    screening = load("screening.json")["decisions"]
    runs = {}
    with open(LOG, encoding="utf-8") as f:
        for entry in map(json.loads, f):
            runs.setdefault(entry["query_id"], []).append(entry)
    lines = [
        "# Search log",
        "",
        f"Generated {now()[:10]} by `research/tools/search_log.py report` from `log.jsonl`.",
        "Do not edit by hand: add queries to `queries.json`, decisions to `screening.json`, re-run.",
        "",
        "Screening status: **included** (in `research/papers/seed.json`) · **excluded** (reason given)",
        "· **title-screened** (seen in results, not yet assessed).",
        "",
    ]
    counts = {"included": 0, "excluded": 0, "title-screened": 0}
    seen = set()
    for qid, q in queries.items():
        entries = runs.get(qid, [])
        lines += [f"## {qid}: {q['query']}", "",
                  f"Serves item(s) {', '.join(map(str, q['items']))}. Purpose: {q['purpose']}", ""]
        if not entries:
            lines += ["_Not yet run._", ""]
            continue
        last = entries[-1]
        lines += [f"Runs: {len(entries)} (latest {last['time']}, `{last['tool']}`)", "",
                  "| # | arXiv | Title | Year | Status |", "|---|---|---|---|---|"]
        for h in last["hits"]:
            key = h["arxiv"] or f"catalog:{h['catalog_id']}"
            d = screening.get(key, {})
            status = d.get("status", "title-screened")
            note = f" ({d['reason']})" if d.get("reason") and status == "excluded" else ""
            if key not in seen:
                counts[status] = counts.get(status, 0) + 1
                seen.add(key)
            lines.append(f"| {h['rank']} | {h['arxiv'] or '—'} | {h['title']} | "
                         f"{(h['published'] or '')[:4]} | {status}{note} |")
        lines.append("")
    lines[7:7] = [f"Unique papers seen: {len(seen)} — included {counts['included']}, "
                  f"excluded {counts['excluded']}, title-screened {counts['title-screened']}.", ""]
    external = load("queries.json").get("_external", [])
    if external:
        lines += ["## Searches recorded elsewhere", "",
                  "Searches run with other tools (web, Hugging Face) are logged in the",
                  "appendix of their reports; they count as part of this protocol.", "",
                  "| Record | Section | Tools | Date | By |", "|---|---|---|---|---|"]
        lines += [f"| `{e['record']}` | {e['section']} | {e['tools']} | {e['date']} | {e['by']} |" for e in external]
        lines.append("")
    with open(os.path.join(ROOT, "SEARCH-LOG.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"SEARCH-LOG.md written: {len(seen)} unique papers")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("run", "report"):
        sys.exit(__doc__)
    run(sys.argv[2:]) if sys.argv[1] == "run" else report()
