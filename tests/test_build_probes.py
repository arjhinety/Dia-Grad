import json

from data.probes.build_probes import length_bin, matched_negatives, pool, select, threshold
from diagrad.t1.contamination import Index


def _idx(items=()):
    return Index(list(items))


def test_pool_dedups_filipino_sides_drops_heldout_and_labels():
    pairs = [("Yes, sir.", "Opo, sir, nandito na ako."),
             ("Yes sir!", "Opo, sir, nandito na ako!"),                       # same side after norm
             ("The boy ate rice.", "Ang bata ay kumain ng kanin."),
             ("Turn on the light", "Buksan mo ang ilaw ngayon"),               # held-out (SMOL, full rule)
             ("Ok.", "Sige.")]                                                # 1 word: too short
    full = _idx([{"src": "turn on the light", "tgt": "buksan mo ang ilaw"}])
    rows, removed = pool(pairs, full, _idx())
    assert removed == 1 and [r["fil"] for r in rows] == ["Opo, sir, nandito na ako.", "Ang bata ay kumain ng kanin."]
    assert [(r["po_opo"], r["ay"], r["cue"]) for r in rows] == [(1, 0, 1), (0, 1, 0)]


def test_matched_negatives_follow_positive_length_bins():
    rows = [{"fil": f"p{i}", "words": 4, "po_opo": 1} for i in range(2)] + \
           [{"fil": f"n{i}", "words": 4, "po_opo": 0} for i in range(5)] + \
           [{"fil": f"m{i}", "words": 30, "po_opo": 0} for i in range(5)]
    pos, neg = matched_negatives(rows, "po_opo", 1, 2)
    assert len(pos) == 2 and len(neg) == 4 and all(r["words"] == 4 for r in neg)
    assert length_bin(4) == 0 and length_bin(30) == 5


def test_threshold_lowest_with_required_precision():
    pts = [(90, 1), (80, 1), (70, 0), (60, 1), (50, 0), (40, 0)]
    # at t=60: 3 of 4 aligned (0.75); at t=50: 3/5 = 0.6
    assert threshold(pts, 0.75) == 60
    assert threshold(pts, 0.9) == 80
    assert threshold([(10, 0)], 0.5) is None


def test_select_pairs_each_positive_with_a_same_bin_negative(tmp_path, monkeypatch):
    import data.probes.build_probes as b
    rows = [{"id": i, "en": f"e{i}", "fil": f"f {i} a b", "words": 4 if i < 6 else 30, "po_opo": int(i < 2),
             "ay": int(i in (2, 3)), "cue": int(i == 0), "chrf": 50.0 if i != 5 else 10.0} for i in range(8)]
    monkeypatch.setattr(b, "with_chrf", lambda cfg: [dict(r) for r in rows])
    monkeypatch.setattr(b, "excluded_by_slice", lambda cfg: {4})
    (tmp_path / "calibration").mkdir()
    (tmp_path / "calibration" / "threshold.json").write_text(json.dumps({"threshold_chrf": 40.0}))
    select({"out_dir": str(tmp_path), "seed": 1, "per_class": 10})
    po = [json.loads(l) for l in open(tmp_path / "probe-po_opo.jsonl")]
    # ids 0,1 positive (4 words); 4-word negatives left after chrF (5 out) and slice (4 out): 2, 3
    assert sorted(r["id"] for r in po if r["label"]) == [0, 1]
    assert sorted(r["id"] for r in po if not r["label"]) == [2, 3]
    stats = json.loads((tmp_path / "select-stats.json").read_text())
    assert stats["features"]["po_opo"]["positives_with_cue"] == 1 and stats["passed_screen"] == 6
