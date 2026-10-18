import json

import numpy as np

from data.mix.measure_mono import doc_lines, h64, overlap


def test_doc_lines_keeps_five_word_lines_normalised():
    text = "Kumain na ba kayo, po?\nOo.\n\nSi Ana ay pumunta sa palengke kahapon."
    assert list(doc_lines(text)) == ["kumain na ba kayo po", "si ana ay pumunta sa palengke kahapon"]


def test_overlap_rate_is_found_lines_over_row_lines(tmp_path):
    a = np.unique(np.array([h64(s) for s in ["w x y z v", "a b c d e", "f g h i j", "k l m n o"]]))
    b = np.unique(np.array([h64(s) for s in ["a b c d e", "f g h i j"]]))
    np.save(tmp_path / "a.lines.npy", a)
    np.save(tmp_path / "b.lines.npy", b)
    overlap(tmp_path)
    m = json.loads((tmp_path / "overlap.json").read_text())["matrix"]
    assert m["a"]["b"] == {"found": 2, "of": 4, "rate": 0.5}     # 2 of A's 4 lines are in B
    assert m["b"]["a"] == {"found": 2, "of": 2, "rate": 1.0}     # all of B is in A


def test_madlad_reader_restores_line_breaks(tmp_path):
    import gzip
    from data.mix.measure_mono import read_madlad
    f = tmp_path / "x.jsonl.gz"
    with gzip.open(f, "wt", encoding="utf-8") as h:
        h.write(json.dumps({"text": "Unang talata dito ay mahaba.\\nIkalawang talata dito ay mahaba rin."}) + "\n")
    (text,) = read_madlad(f)
    assert len(list(doc_lines(text))) == 2


def test_sentences_split_and_drop_short():
    from data.mix.measure_mono import sentences
    text = "Opo, kumain na po ako. Salamat!\nSi Ana ay umalis kanina. Oo."
    assert list(sentences(text)) == ["Opo, kumain na po ako.", "Si Ana ay umalis kanina."]
