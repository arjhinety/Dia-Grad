import gzip
import json

import numpy as np

from data.mix.build_mono_slice import heldout_hit, pool, segments
from data.mix.measure_mono import h64
from diagrad.t1.contamination import Index, norm


class WordTok:
    """Stand-in tokenizer: one token per word."""
    def __call__(self, s, add_special_tokens=False):
        return type("T", (), {"input_ids": s.split()})()

    def decode(self, ids):
        return " ".join(ids)


def test_heldout_hit_uses_8_words_and_whole_short_sides():
    idx = Index([{"src": "Turn on the lights in the kitchen now please", "tgt": "Buksan mo ang ilaw"}])
    assert heldout_hit(idx, norm("Sabi niya: turn on the lights in the kitchen now, tapos umalis."))
    assert not heldout_hit(idx, norm("turn on the lights in the garden now please"))     # 4-word run only
    assert heldout_hit(idx, norm("Kaya buksan mo ang ilaw sa sala bago matulog."))        # whole 4-word side
    assert heldout_hit(idx, norm("Kaya bukşan mo ang ilaw sa sala."))                     # fold: diacritics
    assert not heldout_hit(idx, norm("Kaya buksan mo ang ilaw sa sala."), whole_short_sides=False)
    assert heldout_hit(idx, norm("turn on the lights in the kitchen now"), whole_short_sides=False)


def test_segments_pack_sentences_and_cut_long_ones():
    tok = WordTok()
    text = "Isa dalawa tatlo. Apat lima anim. Pito walo siyam sampu labing-isa labindalawa."
    assert segments(text, tok, 6) == ["Isa dalawa tatlo. Apat lima anim.", "Pito walo siyam sampu labing-isa labindalawa."]
    assert segments(text, tok, 4) == ["Isa dalawa tatlo.", "Apat lima anim.", "Pito walo siyam sampu",
                                      "labing-isa labindalawa."]


def test_pool_filters_madlad_duplicates_and_heldout(tmp_path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    docs = ["Ang unang talata ay bago at malinis.\nAng talatang ito ay nasa MADLAD na dati.",
            "Ang unang talata ay bago at malinis.\nBuksan mo ang ilaw sa kusina ngayon din.\nMaikli."]
    pq.write_table(pa.table({"text": docs, "id": ["d0", "d1"], "url": ["u0", "u1"]}), tmp_path / "a.parquet")
    np.save(tmp_path / "m.lines.npy", np.array([h64(norm("Ang talatang ito ay nasa MADLAD na dati."))]))
    held = tmp_path / "h.jsonl"
    held.write_text(json.dumps({"id": "x", "src": "Turn on the light", "tgt": "Buksan mo ang ilaw"}) + "\n")
    cfg = {"pool_dir": str(tmp_path / "pool"), "heldout": {"full_rule": [str(held)]}, "lines_dir": str(tmp_path),
           "madlad_lines": ["m.lines.npy"], "seed": 1, "workers": 1,
           "sources": [{"name": "a", "path": str(tmp_path / "a.parquet"),
                        "columns": {"text": "text", "id": "id", "url": "url"}}]}
    pool(cfg)
    stats = json.loads((tmp_path / "pool" / "pool-stats.json").read_text())["a"]
    assert stats == {"documents": 2, "paragraphs": 4, "in_madlad": 1, "duplicate": 1, "heldout": 1,
                     "kept": 1, "kept_words": 7}
    rows = [json.loads(l) for l in gzip.open(tmp_path / "pool" / "pool-a.jsonl.gz", "rt")]
    assert [(r["text"], r["doc"], r["url"], r["para_index"]) for r in rows] == \
        [("Ang unang talata ay bago at malinis.", "d0", "u0", 0)]


def test_select_budget_segments_and_provenance(tmp_path):
    import data.mix.build_mono_slice as b
    pdir = tmp_path / "pool"
    pdir.mkdir()
    def write(name, rows):
        with gzip.open(pdir / f"pool-{name}.jsonl.gz", "wt") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
    para = lambda i, rank, text: {"id": i, "src": "x", "doc": f"d{i}", "url": "", "para_index": 0, "rank": rank,
                                  "words": len(text.split()), "text": text}
    write("w", [para(1, 9, "Buong talata ng una.")])
    write("r", [para(2, 5, "Ikalawa ito. Tatlo na salita."), para(3, 1, "Una sa ranggo ito."), para(4, 7, "Hindi kasama ito.")])
    reg = tmp_path / "reg"
    reg.mkdir()
    for rid in ("rw", "rr"):
        (reg / f"{rid}.json").write_text(json.dumps({"id": rid, "source_revision": {"value": "abc"}, "languages": ["fil_Latn"],
            "license": {"spdx": "ODC-By-1.0"}, "use_class": "RESEARCH_ONLY", "redistribution": {"status": "NOT_ASSESSED"},
            "text_origin": {"kind": "MINED"}}))
    cfg = {"pool_dir": str(pdir), "slice_dir": str(tmp_path / "slice"), "registry_dir": str(reg), "workers": 1,
           "token_budget": 12, "tokens_per_word": {"w": 1.0, "r": 1.0}, "max_segment_tokens": 3,
           "tokenizer": None, "sources": [{"name": "w", "registry_id": "rw", "whole": True},
                                          {"name": "r", "registry_id": "rr"}]}
    b._init_tok = lambda spec: setattr(b, "_TOK", WordTok())
    b._pool = lambda cfg, init, arg: __import__("multiprocessing.dummy", fromlist=["Pool"]).Pool(1, init, (arg,))
    b.select(cfg)
    rows = [json.loads(l) for l in gzip.open(tmp_path / "slice" / "slice.jsonl.gz", "rt")]
    # whole source: 4 words; budget 12 - 4 = 8 -> ranks 1 (4 words) and 5 (5 words) taken, rank 7 not.
    # Segments of <= 3 tokens: a 4-word sentence is cut 3 + 1; "Ikalawa ito." (2) + "Tatlo na salita." (3) > 3.
    assert [r["source_record_id"] for r in rows] == ["d1", "d1", "d2", "d2", "d3", "d3"]
    assert [r["text"] for r in rows if r["source_record_id"] == "d2"] == ["Ikalawa ito.", "Tatlo na salita."]
    assert rows[0]["diagrad_id"] == "rw:d1:0:0" and rows[0]["source_dataset"] == "rw" and rows[0]["tokens"] == 3
    stats = json.loads((tmp_path / "slice" / "slice-stats.json").read_text())
    assert stats["tokens"] == sum(r["tokens"] for r in rows)
