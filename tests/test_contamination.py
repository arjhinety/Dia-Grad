"""Tests for the contamination check (D20). Standard library only; runs anywhere."""
import pytest

from diagrad.t1.contamination import Index, flag_rate, fold, item_results, norm, scan, summarise

ITEMS = [
    # a: 10-word English side shares an 8-word run with a training line -> flagged at 8, not at 13
    {"id": "a", "src": "one two three four five six seven eight nine ten", "tgt": "isa dalawa tatlo"},
    # b: 4-word side found whole inside a training sentence -> flagged (short item rule)
    {"id": "b", "src": "Thank you, very much!", "tgt": "salamat po nang marami"},
    # c: 5-word side of which only 4 words are found -> not flagged
    {"id": "c", "src": "good morning to you all", "tgt": "magandang hapon po sa lahat"},
    # d: matches only once diacritics are removed (pô vs po)
    {"id": "d", "src": "have you eaten", "tgt": "Kumain na pô kayo"},
    # e: exact pair, also inside a second line; still counts as one item
    {"id": "e", "src": "The cat sat on the mat today", "tgt": "umupo ang pusa"},
]
TRAIN = [
    "zero two three four five six seven eight nine eleven\twala\n",
    "Well, thank you very much indeed.\tsalamat\n",
    "Good morning to you.\tMagandang umaga sa iyo.\n",
    "Did you eat?\tKumain na po kayo ba?\n",
    "The cat sat on the mat today.\tUmupo ang pusa.\n",
    "I saw the cat sat on the mat today again\tnakita ko\n",
    "a line without a tab\n",
]


def run(workers=1):
    index = Index(ITEMS)
    lines, best, exact, pairs = scan(index, TRAIN, workers=workers, chunk=2)
    res = item_results(index, best, exact, pairs)
    return lines, {r["id"]: r for r in res}, summarise(res)


def test_flag_rate_worked_example_from_a5():
    assert flag_rate(253, 1012) == 0.25          # A5 §3.2: 253 flagged of 1,012 items
    with pytest.raises(ValueError):
        flag_rate(5, 4)
    with pytest.raises(ValueError):
        flag_rate(0, 0)


def test_normalisation_matches_build_heldout_and_folds_diacritics():
    assert norm("  Thank you,  VERY much! ") == "thank you very much"
    assert fold(norm("Kumain na pô kayo")) == "kumain na po kayo"
    assert fold(norm("Niño")) == "nino"


def test_longest_match_and_flags_per_side():
    lines, r, _ = run()
    assert lines == 6                            # the line without a tab is not counted
    a = r["a"]["plain"]["src"]
    assert (a["words"], a["longest"], a["span"]) == (10, 8, "two three four five six seven eight nine")
    assert a["flag8"] and not a["flag13"]
    assert r["b"]["plain"]["src"]["flag8"] and r["b"]["plain"]["src"]["flag13"]
    assert r["c"]["plain"]["src"]["longest"] == 0 and not r["c"]["fold"]["flag8"]
    assert not r["d"]["plain"]["flag8"] and r["d"]["fold"]["tgt"]["flag8"]
    e = r["e"]["plain"]
    assert e["pair_exact"] and e["src"]["exact"] and e["tgt"]["exact"]


def test_summary_counts_items_not_sides_or_lines():
    _, _, s = run()
    assert s["items"] == 5
    # fold: a, b, d, e flagged -> 4/5; plain: a, b, e -> 3/5. Item e matches on both sides and in two
    # lines but counts once.
    assert (s["fold"]["flag8"], s["fold"]["rate8"]) == (4, 0.8)
    assert (s["plain"]["flag8"], s["plain"]["rate8"]) == (3, 0.6)
    assert s["fold"]["flagged_ids"] == ["a", "b", "d", "e"]
    assert (s["fold"]["flag13"], s["plain"]["flag13"]) == (3, 2)
    assert s["plain"]["clean_items"] == 2
    assert (s["plain"]["src_exact"], s["plain"]["tgt_exact"], s["plain"]["pair_exact"]) == (1, 1, 1)


def test_parallel_scan_gives_the_same_result():
    assert run(workers=1) == run(workers=2)
