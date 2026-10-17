"""Validate the dataset registry and the source screening log (D24). Standard library only.

    python3 -m diagrad.registry.validate [--root REPO] [--json]

Checks every data/registry/*.json record against schema v2 (data/registry/schema/dataset_record.schema.json)
and data/registry/source_screening.json against its rules. Ported from OpenGrad's registry validator
(arjhinety/OpenGrad @ 76645059): a gate must show it examined something, so the result carries a census
that must add up (discovered == checked + skipped; checked == passed + failed), and an empty population
where records must exist is itself a failure. Exit 0 only when every record passed.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MOVING = re.compile(r"/(main|master|latest|HEAD)(/|$)|blob/main|tree/main|releases/latest")
TRAIN = {"TRAIN_PARALLEL", "TRAIN_MONOLINGUAL"}
HELDOUT = {"DEV", "GATE_TEST", "DIAGNOSTIC", "E1_EVALUATION"}
NC_LICENSE = re.compile(r"\bNC\b|non-?commercial|CC-BY-NC", re.I)

ENUMS = {
    "role": {"UPSTREAM_SOURCE", "DERIVED_CORPUS"},
    "lifecycle": {"ACTIVE", "HISTORICAL", "EXCLUDED"},
    "use_class": {"COMMERCIAL_OK", "COMMERCIAL_ATTRIBUTION", "SHARE_ALIKE", "RESEARCH_ONLY", "NOT_FOR_TRAINING"},
}
PURPOSES = TRAIN | HELDOUT | {"PROBE", "LABELLING_SAMPLE", "MEASUREMENT_ONLY"}
REQUIRED = ["schema_version", "id", "display_name", "role", "lifecycle", "purpose", "languages", "source_revision",
            "distribution", "license", "use_class", "text_origin", "redistribution", "attribution", "sample_count",
            "contamination", "forbidden_uses", "decisions", "retrieved"]
SUB = {
    "source_revision": (["kind", "value", "verified", "source"],
                        {"kind": {"GIT_COMMIT", "HF_REVISION", "VERSIONED_URL", "SERVER_FILE"}}),
    "license": (["spdx", "quote", "source"], {}),
    "text_origin": (["kind"], {"kind": {"HUMAN", "MINED", "MACHINE_TRANSLATED", "MIXED", "UNKNOWN"}}),
    "redistribution": (["status"], {"status": {"REDISTRIBUTION_WITH_ATTRIBUTION", "SHARE_ALIKE", "PER_SOURCE",
                                               "NOT_ASSESSED", "NOT_PERMITTED"}}),
    "attribution": (["required"], {}),
    "sample_count": (["published", "unit", "source"], {}),
    "contamination": (["status"], {"status": {"NOT_CHECKED", "CHECKED_CLEAN", "CHECKED_FLAGGED",
                                             "IS_HELDOUT_OR_EVALUATION"}}),
}
VERDICTS = {"PASS", "PARTIAL", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}
DECISIONS = {"SHORTLISTED", "EXCLUDED", "WATCHLIST"}


def check_record(rec, stem):
    """Return a list of error strings for one registry record (empty = passed)."""
    errs = [f"missing field '{k}'" for k in REQUIRED if k not in rec]
    if errs:
        return errs
    if rec["schema_version"] != 2:
        errs.append("schema_version must be 2")
    if rec["id"] != stem:
        errs.append(f"id '{rec['id']}' does not match file name '{stem}'")
    for k, allowed in ENUMS.items():
        if rec[k] not in allowed:
            errs.append(f"{k} '{rec[k]}' not in {sorted(allowed)}")
    for k, (req, enums) in SUB.items():
        v = rec[k]
        if not isinstance(v, dict):
            errs.append(f"{k} must be an object")
            continue
        errs += [f"{k}.{f} missing" for f in req if f not in v]
        errs += [f"{k}.{f} '{v[f]}' not in {sorted(a)}" for f, a in enums.items() if f in v and v[f] not in a]
    if errs:
        return errs

    purpose = set(rec["purpose"])
    if purpose - PURPOSES:
        errs.append(f"unknown purpose {sorted(purpose - PURPOSES)}")
    if purpose & TRAIN and purpose & HELDOUT:
        errs.append(f"held-out purpose {sorted(purpose & HELDOUT)} combined with training {sorted(purpose & TRAIN)}")
    if rec["lifecycle"] == "EXCLUDED" and purpose & TRAIN:
        errs.append("EXCLUDED record lists a training purpose")
    if purpose & TRAIN and rec["use_class"] == "NOT_FOR_TRAINING":
        errs.append("use_class NOT_FOR_TRAINING with a training purpose")
    if purpose & TRAIN and set(rec["forbidden_uses"]) & purpose:
        errs.append("a purpose is also listed in forbidden_uses")

    rev, dist = rec["source_revision"], rec["distribution"]
    if not isinstance(dist, list) or not dist:
        return errs + ["distribution must be a non-empty list"]
    if rev["kind"] in ("GIT_COMMIT", "HF_REVISION") and not HEX40.match(rev["value"]):
        errs.append(f"{rev['kind']} must be a full 40-hex id, got '{rev['value']}'")
    for d in dist:
        url = d.get("content_url", "")
        if MOVING.search(url):
            errs.append(f"content_url points at a moving target: {url}")
        if rev["kind"] in ("GIT_COMMIT", "HF_REVISION") and rev["value"] not in url:
            errs.append(f"content_url does not carry the pinned revision: {url}")
        if rev["kind"] == "VERSIONED_URL" and rev["value"] not in url:
            errs.append(f"content_url does not carry version '{rev['value']}': {url}")
        sha = d.get("sha256")
        if sha is not None and not HEX64.match(sha):
            errs.append(f"distribution '{d.get('name')}' sha256 is not 64-hex")
        if sha is None and (rev["kind"] == "SERVER_FILE" or d.get("local_path")):
            errs.append(f"distribution '{d.get('name')}' needs a sha256 (SERVER_FILE anchor or downloaded file)")

    red = rec["redistribution"]
    if red["status"] != "NOT_ASSESSED" and not red.get("basis"):
        errs.append("redistribution.basis required unless status is NOT_ASSESSED")
    if rec["attribution"]["required"] and not (rec["attribution"].get("text") or rec["attribution"].get("citation_target")):
        errs.append("attribution.required but neither attribution.text nor citation_target given")

    origin = rec["text_origin"]
    if origin["kind"] in ("MACHINE_TRANSLATED", "MIXED"):
        if not origin.get("generator_license"):
            errs.append("text_origin.generator_license required for machine-translated or mixed text")
        elif purpose & TRAIN and NC_LICENSE.search(origin["generator_license"]) and not rec.get("deviation"):
            errs.append("training text generated by a non-commercial model (licence rule, research/licenses/LICENSES.md) without a logged deviation")

    if purpose & HELDOUT and rec["contamination"]["status"] != "IS_HELDOUT_OR_EVALUATION":
        errs.append("held-out record must have contamination.status IS_HELDOUT_OR_EVALUATION")
    if rec["role"] == "DERIVED_CORPUS":
        if not rec.get("derived_from"):
            errs.append("DERIVED_CORPUS needs derived_from")
        if not HEX64.match(rec.get("processed_sha256", "")):
            errs.append("DERIVED_CORPUS needs a 64-hex processed_sha256")
    if not all(re.match(r"^D[0-9]+$", x) for x in rec["decisions"]):
        errs.append("decisions must be ids like D17")
    return errs


def check_screening(doc, registered):
    """Return a list of error strings for the screening log."""
    errs = []
    for s in doc.get("screenings", []):
        sid = s.get("id", "?")
        crit = {c["id"] for c in s.get("criteria", [])}
        if not crit:
            errs.append(f"{sid}: no criteria")
        for c in s.get("candidates", []):
            cid = f"{sid}/{c.get('id', '?')}"
            v = c.get("verdicts", {})
            if set(v) != crit:
                errs.append(f"{cid}: verdicts must cover exactly the criteria {sorted(crit)}")
            if set(v.values()) - VERDICTS:
                errs.append(f"{cid}: unknown verdict {sorted(set(v.values()) - VERDICTS)}")
            dec = c.get("decision")
            if dec not in DECISIONS:
                errs.append(f"{cid}: decision '{dec}' not in {sorted(DECISIONS)}")
            fails = {k for k, x in v.items() if x == "FAIL"}
            if dec == "SHORTLISTED" and fails:
                errs.append(f"{cid}: SHORTLISTED but fails {sorted(fails)}")
            if dec == "EXCLUDED" and (not c.get("failing_criteria") or not set(c["failing_criteria"]) <= fails):
                errs.append(f"{cid}: EXCLUDED must name failing_criteria that are FAIL verdicts")
            if dec == "WATCHLIST" and not c.get("watch_for"):
                errs.append(f"{cid}: WATCHLIST needs watch_for")
            if not c.get("evidence"):
                errs.append(f"{cid}: no evidence")
            if c.get("adopted"):
                if dec != "SHORTLISTED":
                    errs.append(f"{cid}: adopted but not SHORTLISTED")
                if c.get("registry_id") not in registered:
                    errs.append(f"{cid}: adopted but registry_id '{c.get('registry_id')}' has no record")
    return errs


def validate(root):
    reg = Path(root) / "data" / "registry"
    files = sorted(reg.glob("*.json"))
    records = [p for p in files if p.name != "source_screening.json"]
    census = {"discovered": len(records), "checked": 0, "skipped": 0, "passed": 0, "failed": 0}
    errors, registered = {}, set()
    for p in records:
        try:
            rec = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            errors[p.name] = [f"invalid JSON: {e}"]
            census["checked"] += 1
            census["failed"] += 1
            continue
        census["checked"] += 1
        e = check_record(rec, p.stem)
        if e:
            errors[p.name] = e
            census["failed"] += 1
        else:
            census["passed"] += 1
            registered.add(rec["id"])
    scr = reg / "source_screening.json"
    if scr.exists():
        e = check_screening(json.loads(scr.read_text()), registered)
        if e:
            errors["source_screening.json"] = e
    if census["discovered"] == 0:
        errors["<population>"] = ["no registry records found: discovery is broken (REQUIRED_NONEMPTY)"]
    ok_census = (census["discovered"] == census["checked"] + census["skipped"]
                 and census["checked"] == census["passed"] + census["failed"])
    if not ok_census:
        errors["<census>"] = [f"census does not add up: {census}"]
    return {"passed": not errors, "census": census, "errors": errors}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    r = validate(a.root)
    if a.json:
        print(json.dumps(r, indent=1))
    else:
        print("census:", r["census"])
        for f, es in r["errors"].items():
            for e in es:
                print(f"FAIL {f}: {e}")
        print("PASSED" if r["passed"] else "FAILED")
    return 0 if r["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
