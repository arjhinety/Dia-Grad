import json

import numpy as np

from data.mix.measure_mono import h64
from data.mix.quality_check import choose, gap_interval, pack, parse_answers, score


def _cands(texts):
    return {h64(t): {"text": t, "norm": t, "sources": ["fw2"], "rank": r} for r, t in enumerate(texts)}


def test_choose_splits_by_madlad_membership_and_length():
    texts = ["a b c d e", "f g h i j", "k l m n o", "p q r s t " * 40, "u v w x y"]
    cands = _cands(texts)
    clean = np.array([h64("a b c d e")])
    allm = np.unique(np.array([h64("a b c d e"), h64("f g h i j"), h64(texts[3])]))
    groups, counts = choose(cands, clean, allm, n=5, max_words=150)
    assert [p["text"] for p in groups["dropped"]] == ["a b c d e", "f g h i j"]
    assert [p["madlad"] for p in groups["dropped"]] == ["clean", "noisy_only"]
    assert [p["text"] for p in groups["kept"]] == ["k l m n o", "u v w x y"]
    assert counts["dropped"] == {"candidates": 3, "over_max_words": 1}


def test_gap_interval_mean_difference():
    gap, lo, hi = gap_interval([2, 2, 2, 2], [1, 1, 1, 1], 1000, 0)
    assert gap == 1.0 and lo == 1.0 and hi == 1.0


def _cfg(tmp_path, **kw):
    return {"seed": 7, "batches": 2, "hidden_repeats": 2, "bootstrap_resamples": 500, "out_dir": str(tmp_path),
            "decision_rule": {"min_gap": {"quality": 0.3, "naturalness": 0.3, "eligible": 0.1},
                              "max_repeat_disagreement": 0.2}, **kw}


def test_pack_hides_groups_and_puts_repeats_in_other_batch(tmp_path):
    groups = {g: [{"hash": i + (100 if g == "kept" else 0), "text": f"{g} {i} x y z", "sources": ["fw2"],
                   "madlad": "none"} for i in range(3)] for g in ("dropped", "kept")}
    (tmp_path / "sample.json").write_text(json.dumps({"groups": groups}))
    cfg = _cfg(tmp_path)
    pack(cfg, tmp_path)
    key = json.loads((tmp_path / "key.json").read_text())
    assert len(key) == 8
    where = {}
    for b in range(2):
        text = (tmp_path / f"batch-{b}.prompt.md").read_text()
        assert "dropped" not in text.split("items.")[0]          # rubric says nothing about groups
        for line in text.split("items.", 1)[1].splitlines():
            if line.startswith('{"item"'):
                where[json.loads(line)["item"]] = b
    for i, k in key.items():
        if "repeat_of" in k:
            assert where[i] != where[k["repeat_of"]]


def test_score_trips_rule_only_with_gap_and_interval(tmp_path):
    key = {f"d{i}": {"group": "dropped"} for i in range(4)} | {f"k{i}": {"group": "kept"} for i in range(4)}
    key["r0"] = {"group": "dropped", "repeat_of": "d0"}
    (tmp_path / "key.json").write_text(json.dumps(key))
    lab = {**{f"d{i}": 2 for i in range(4)}, **{f"k{i}": 1 for i in range(4)}, "r0": 2}
    lines = [json.dumps({"item": i, "language_status": "taglish", "quality": v, "naturalness": v})
             for i, v in lab.items()]
    (tmp_path / "batch-0.answer.md").write_text("\n".join(lines[:5]))
    (tmp_path / "batch-1.answer.md").write_text("```\n" + "\n".join(lines[5:]) + "\n```")
    res = score(_cfg(tmp_path), tmp_path)
    assert res["groups"]["dropped"]["n"] == 4 and res["gaps"]["quality"]["dropped_minus_kept"] == 1.0
    assert res["gaps"]["eligible"]["dropped_minus_kept"] == 0.0
    assert res["decision_rule"]["tripped"] and res["repeats"] == {"pairs": 1, "any_label_differs": 0,
                                                                  "judge_usable": True}


def test_parse_answers_ignores_fences():
    assert list(parse_answers('```json\n{"item": "a", "quality": 1}\n```')) == ["a"]


def test_other_language_counts_against_eligible_not_quality(tmp_path):
    key = {"d0": {"group": "dropped"}, "d1": {"group": "dropped"}, "k0": {"group": "kept"}, "k1": {"group": "kept"}}
    (tmp_path / "key.json").write_text(json.dumps(key))
    rows = [{"item": "d0", "language_status": "filipino_tagalog", "quality": 2, "naturalness": 2},
            {"item": "d1", "language_status": "filipino_tagalog", "quality": 2, "naturalness": 2},
            {"item": "k0", "language_status": "filipino_tagalog", "quality": 2, "naturalness": 2},
            {"item": "k1", "language_status": "other_language", "other_language": "Cebuano",
             "quality": None, "naturalness": None}]
    (tmp_path / "batch-0.answer.md").write_text("\n".join(json.dumps(r) for r in rows))
    (tmp_path / "batch-1.answer.md").write_text("")
    res = score(_cfg(tmp_path), tmp_path)
    assert res["groups"]["kept"]["quality"] == {"n": 1, "mean": 2.0, "zeros": 0}   # Cebuano item not scored as bad Tagalog
    assert res["gaps"]["quality"]["dropped_minus_kept"] == 0.0
    assert res["gaps"]["eligible"]["dropped_minus_kept"] == 0.5                     # 2/2 - 1/2
