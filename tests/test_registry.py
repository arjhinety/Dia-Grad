"""Tests for the dataset registry validator (D24). Standard library only."""
import copy
import json
from pathlib import Path

from diagrad.registry.validate import check_record, check_screening, validate

REPO = Path(__file__).resolve().parents[1]
REV = "a" * 40
GOOD = {
    "schema_version": 2, "id": "toy", "display_name": "Toy pairs", "role": "UPSTREAM_SOURCE", "lifecycle": "ACTIVE",
    "purpose": ["TRAIN_PARALLEL"], "languages": ["eng_Latn", "tgl_Latn"],
    "source_revision": {"kind": "HF_REVISION", "value": REV, "verified": True, "source": "HF API"},
    "distribution": [{"name": "a.parquet", "content_url": f"https://huggingface.co/datasets/x/y/resolve/{REV}/a.parquet",
                      "local_path": "~/data/raw/x/a.parquet", "sha256": "b" * 64, "bytes": 10}],
    "license": {"spdx": "CC0-1.0", "quote": "CC0", "source": "card"}, "use_class": "COMMERCIAL_OK",
    "text_origin": {"kind": "HUMAN"}, "redistribution": {"status": "NOT_ASSESSED"},
    "attribution": {"required": False}, "sample_count": {"published": 3, "unit": "pairs", "source": "card"},
    "contamination": {"status": "NOT_CHECKED"}, "forbidden_uses": [], "decisions": ["D22"], "retrieved": "2026-10-17",
}


def bad(path, value):
    """Errors for GOOD with one field replaced; path is a tuple of keys."""
    rec = copy.deepcopy(GOOD)
    target = rec
    for k in path[:-1]:
        target = target[k]
    target[path[-1]] = value
    return check_record(rec, "toy")


def test_good_record_passes():
    assert check_record(GOOD, "toy") == []


def test_moving_revision_and_short_ids_are_rejected():
    assert any("40-hex" in e for e in bad(("source_revision", "value"), "main"))
    rec = copy.deepcopy(GOOD)
    rec["distribution"][0]["content_url"] = "https://huggingface.co/datasets/x/y/resolve/main/a.parquet"
    errs = check_record(rec, "toy")
    assert any("moving target" in e for e in errs) and any("pinned revision" in e for e in errs)


def test_downloaded_file_needs_a_digest():
    rec = copy.deepcopy(GOOD)
    rec["distribution"][0]["sha256"] = None
    assert any("needs a sha256" in e for e in check_record(rec, "toy"))


def test_heldout_never_combines_with_training():
    errs = bad(("purpose",), ["TRAIN_PARALLEL", "GATE_TEST"])
    assert any("held-out purpose" in e for e in errs)


def test_noncommercial_generator_blocked_for_training_unless_deviation():
    rec = copy.deepcopy(GOOD)
    rec["text_origin"] = {"kind": "MACHINE_TRANSLATED", "generator_model": "facebook/nllb-200-3.3B",
                          "generator_license": "CC-BY-NC-4.0"}
    assert any("non-commercial model" in e for e in check_record(rec, "toy"))
    rec["deviation"] = "D99"
    assert check_record(rec, "toy") == []
    rec["text_origin"]["generator_license"] = "Apache-2.0"
    del rec["deviation"]
    assert check_record(rec, "toy") == []


def test_redistribution_basis_required_once_assessed():
    assert any("basis" in e for e in bad(("redistribution",), {"status": "SHARE_ALIKE"}))


def test_screening_rules():
    crit = [{"id": "C1", "text": "pairs"}, {"id": "C2", "text": "terms"}]
    def doc(c):
        return {"screenings": [{"id": "S", "criteria": crit, "candidates": [c]}]}
    ok = {"id": "x", "verdicts": {"C1": "PASS", "C2": "PASS"}, "decision": "SHORTLISTED", "evidence": ["url"],
          "adopted": True, "registry_id": "toy"}
    assert check_screening(doc(ok), {"toy"}) == []
    assert any("has no record" in e for e in check_screening(doc(ok), set()))
    fails = dict(ok, verdicts={"C1": "PASS", "C2": "FAIL"})
    assert any("SHORTLISTED but fails" in e for e in check_screening(doc(fails), {"toy"}))
    excl = {"id": "y", "verdicts": {"C1": "PASS", "C2": "PARTIAL"}, "decision": "EXCLUDED",
            "failing_criteria": ["C2"], "evidence": ["url"]}
    assert any("FAIL verdicts" in e for e in check_screening(doc(excl), set()))


def test_census_adds_up_on_a_worked_example(tmp_path):
    reg = tmp_path / "data" / "registry"
    reg.mkdir(parents=True)
    (reg / "toy.json").write_text(json.dumps(GOOD))
    broken = dict(GOOD, id="other")                       # id does not match its file name
    (reg / "wrong.json").write_text(json.dumps(broken))
    (reg / "junk.json").write_text("{not json")
    r = validate(tmp_path)
    # 3 records discovered: 1 passes, 2 fail -> 3 == 3 + 0 and 3 == 1 + 2
    assert r["census"] == {"discovered": 3, "checked": 3, "skipped": 0, "passed": 1, "failed": 2}
    assert not r["passed"] and set(r["errors"]) == {"wrong.json", "junk.json"}


def test_empty_registry_is_a_failure_not_a_pass(tmp_path):
    (tmp_path / "data" / "registry").mkdir(parents=True)
    r = validate(tmp_path)
    assert not r["passed"] and "<population>" in r["errors"]


def test_repository_registry_passes():
    r = validate(REPO)
    assert r["passed"], r["errors"]
    assert r["census"]["discovered"] == r["census"]["passed"] >= 6
