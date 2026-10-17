import json

import numpy as np
from sacrebleu.metrics import CHRF

from diagrad.t1.teacher_compare import (chrf_stats, corpus_from_stats, decision_rule, direction_items,
                                        paired_bootstrap_gap, sample_pairs)


def test_decision_rule_needs_both_directions():
    a = {"en-fil": {"gap": 6.0, "ci_low": 1.0}, "fil-en": {"gap": 5.5, "ci_low": 0.2}}
    assert decision_rule(a, 5.0) == {"per_direction": {"en-fil": True, "fil-en": True}, "tripped": True}
    b = {"en-fil": {"gap": 6.0, "ci_low": 1.0}, "fil-en": {"gap": 7.0, "ci_low": -0.5}}
    assert decision_rule(b, 5.0)["tripped"] is False          # interval crosses 0
    c = {"en-fil": {"gap": 5.0, "ci_low": 2.0}, "fil-en": {"gap": 9.0, "ci_low": 3.0}}
    assert decision_rule(c, 5.0)["per_direction"]["en-fil"] is False   # "more than 5": 5.0 is not
    assert decision_rule({}, 5.0)["tripped"] is False


def test_stats_sum_to_corpus_chrf():
    m = CHRF(word_order=2)
    hyps, refs = ["ang aso ay tumakbo", "kumain siya"], ["tumakbo ang aso", "kumain siya ng kanin"]
    assert abs(corpus_from_stats(m, chrf_stats(m, hyps, refs)) - m.corpus_score(hyps, [refs]).score) < 1e-9


def test_bootstrap_identical_systems_gap_zero():
    m = CHRF(word_order=2)
    s = chrf_stats(m, ["a b c", "d e", "f g h"], ["a b c", "d x", "f g"])
    g = paired_bootstrap_gap(m, s, s, resamples=200, seed=1)
    assert g == {"gap": 0.0, "ci_low": 0.0, "ci_high": 0.0}


def test_bootstrap_sign_better_reference_positive():
    m = CHRF(word_order=2)
    refs = ["ang bahay ay malaki", "maganda ang araw", "umuulan ngayon"]
    good = chrf_stats(m, refs, refs)
    bad = chrf_stats(m, ["bahay", "araw", "ngayon"], refs)
    g = paired_bootstrap_gap(m, good, bad, resamples=200, seed=1)
    assert g["gap"] > 0 and g["ci_low"] > 0


def test_sampling_is_seeded_and_in_file_order(tmp_path):
    p = tmp_path / "d.jsonl"
    p.write_text("".join(json.dumps({"id": i, "src": f"e{i}", "tgt": f"f{i}"}) + "\n" for i in range(20)))
    a, b = sample_pairs(p, 5, 7), sample_pairs(p, 5, 7)
    assert a == b and len(a) == 5 and [r["id"] for r in a] == sorted(r["id"] for r in a)
    fe = direction_items(a, "fil-en")[0]
    assert fe["src"] == a[0]["tgt"] and fe["ref"] == a[0]["src"]
