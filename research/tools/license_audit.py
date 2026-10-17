"""License audit: check every component in research/licenses/components.json at its source.

Sources: Hugging Face model/dataset metadata (cardData.license, license:* tags) and the GitHub
repository license API. A missing or unrecognised license is reported as such, never guessed.

Outputs (research/licenses/):
  audit.json   machine-readable result with retrieval timestamps
  LICENSES.md  human-readable table grouped by what the license allows

Usage:  python research/tools/license_audit.py
"""
import datetime as dt
import json
import os
import subprocess
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "licenses"))

# How each license affects a model DiaGrad may eventually use commercially.
# This is a coarse engineering classification, not legal advice.
CLASS = {
    "apache-2.0": "permissive", "mit": "permissive", "bsd-3-clause": "permissive",
    "bsd-2-clause": "permissive", "cc-by-4.0": "permissive-attribution", "odc-by": "permissive-attribution",
    "cc0-1.0": "permissive", "cc-by-sa-4.0": "share-alike", "odbl": "share-alike",
    "cc-by-nc-4.0": "non-commercial", "cc-by-nc-sa-4.0": "non-commercial", "cc-by-nc-nd-4.0": "non-commercial",
    "llama3.2": "custom", "llama3.1": "custom", "gemma": "custom", "other": "custom",
}
MEANING = {
    "permissive": "Commercial use allowed; keep the license notice.",
    "permissive-attribution": "Commercial use allowed; attribution required.",
    "share-alike": "Commercial use allowed, but derived data/works must carry the same license.",
    "non-commercial": "Research only. Must not end up inside a commercially used DiaGrad model.",
    "custom": "Own terms; read the license text before use.",
    "unknown": "No license found at the source. Treat as all rights reserved until clarified.",
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "DiaGrad-license-audit/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"


def check(c):
    if c["kind"] in ("hf-model", "hf-dataset"):
        base = "models" if c["kind"] == "hf-model" else "datasets"
        url = f"https://huggingface.co/api/{base}/{c['id']}"
        d, err = get_json(url)
        if d is None:
            return {"license": None, "source": url, "error": err}
        lic = (d.get("cardData") or {}).get("license")
        if isinstance(lic, list):
            lic = ",".join(lic)
        tags = [t.split(":", 1)[1] for t in d.get("tags", []) if t.startswith("license:")]
        extra = {"gated": d.get("gated")} if d.get("gated") else {}
        return {"license": lic or (",".join(tags) if tags else None), "source": url, **extra}
    if c["kind"] == "github":
        r = subprocess.run(["gh", "api", f"repos/{c['id']}"], capture_output=True)
        src = f"https://github.com/{c['id']}"
        if r.returncode != 0:
            return {"license": None, "source": src, "error": "repo not found or inaccessible"}
        lic = (json.loads(r.stdout).get("license") or {}).get("spdx_id")
        return {"license": None if lic in (None, "NOASSERTION") else lic.lower(), "source": src,
                **({"note": "GitHub could not identify the license file (NOASSERTION)"} if lic == "NOASSERTION" else {})}
    raise ValueError(c["kind"])


def classify(lic):
    if not lic:
        return "unknown"
    classes = {CLASS.get(part.strip().lower(), "custom") for part in lic.split(",")}
    for worst in ("non-commercial", "custom", "share-alike", "permissive-attribution", "permissive"):
        if worst in classes:
            return worst
    return "custom"


def main():
    with open(os.path.join(ROOT, "components.json"), encoding="utf-8") as f:
        comps = json.load(f)["components"]
    results = []
    for c in comps:
        r = {**c, **check(c), "checked": now()}
        r["class"] = classify(r["license"])
        results.append(r)
        print(f"{r['class']:<24} {r['license'] or '-':<22} {c['id']}")
    with open(os.path.join(ROOT, "audit.json"), "w", encoding="utf-8") as f:
        json.dump({"generated": now(), "results": results}, f, indent=2, ensure_ascii=False)
    lines = ["# License audit", "",
             f"Generated {now()[:10]} by `research/tools/license_audit.py` from `components.json`.",
             "Licenses are read from each component's source (Hugging Face metadata or GitHub). This is an",
             "engineering classification, not legal advice; read the license text before relying on it.", ""]
    for cls in ("permissive", "permissive-attribution", "share-alike", "custom", "non-commercial", "unknown"):
        group = [r for r in results if r["class"] == cls]
        if not group:
            continue
        lines += [f"## {cls} — {MEANING[cls]}", "", "| Component | Kind | License | Why it's on the list | Note |",
                  "|---|---|---|---|---|"]
        for r in group:
            note = r.get("error") or r.get("note") or ("gated: " + str(r["gated"]) if r.get("gated") else "")
            lines.append(f"| [{r['id']}]({r['source']}) | {r['kind']} | {r['license'] or '—'} | {r['role']} | {note} |")
        lines.append("")
    with open(os.path.join(ROOT, "LICENSES.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
