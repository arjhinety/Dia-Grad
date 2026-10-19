from data.mix.measure_probe_sources import band, count


def test_count_unit_is_unique_probeable_sides():
    pairs = [("Thank you.", "Salamat po sa inyo.", "all"),
             ("Thank you!", "Salamat po sa inyo!", "all"),          # same side after norm: counted once
             ("Yes.", "Opo.", "all"),                                # 1 word: outside 3-40
             ("The child ate.", "Ang bata ay kumain.", "all"),
             ("I went home.", "Umuwi na ako kahapon.", "all")]
    c, sample = count(pairs)
    assert c["all"]["sides"] == 3 and c["all"]["po_opo"] == 1 and c["all"]["ay"] == 1
    assert c["all"]["po_rate"] == 1 / 3
    assert [s["fil"] for s in sample] == ["Salamat po sa inyo."]


def test_nllb_bands():
    assert [band(s) for s in (1.25, 1.2, 1.15, 1.07, 1.0)] == [">=1.2", ">=1.2", ">=1.1", ">=1.06", "<1.06"]
