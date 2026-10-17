"""Tests for tranche-1 code. Run in the diagrad:t1 container: `pytest -q tests` (HF_HOME=/hf mounted).

Tokenizer tests need the pinned MADLAD/mT5 tokenizers in the HF cache and are skipped without them.
"""
import glob
import random

import numpy as np
import pytest
import torch
from transformers import T5Config, T5ForConditionalGeneration

from diagrad.t1.data import Collator, infill_noise, lang_prefix_ids
from diagrad.t1.gate import (_balanced_accuracy, gap_ci, label_ay_inversion, label_po_opo,
                             probe_scores, retrieval_error)
from diagrad.t1.space import LossWeights, SentenceSpace, mean_pool


def tiny_space(seed=0):
    torch.manual_seed(seed)
    cfg = T5Config(vocab_size=64, d_model=16, d_kv=4, d_ff=32, num_layers=2, num_decoder_layers=2,
                   num_heads=2, decoder_start_token_id=0, pad_token_id=0, eos_token_id=1)
    return SentenceSpace(T5ForConditionalGeneration(cfg))


def tiny_batch():
    src = torch.tensor([[5, 6, 7, 1], [8, 9, 1, 0]])
    tgt = torch.tensor([[10, 11, 1], [12, 1, 0]])
    noisy = torch.tensor([[3, 1, 0], [3, 1, 0]])
    dec = torch.tensor([[40, 10, 11, 1], [40, 12, 1, 0]])          # 40 = language prefix
    lab = torch.tensor([[-100, 10, 11, 1], [-100, 12, 1, -100]])
    b = {"src_ids": src, "tgt_ids": tgt, "noisy_ids": noisy, "dec_ids": dec, "labels": lab}
    for k in ("src", "tgt", "noisy"):
        b[f"{k}_mask"] = (b[f"{k}_ids"] != 0).long()
    return b


def test_mean_pool_ignores_padding():
    h = torch.tensor([[[1.0, 2.0], [3.0, 4.0], [100.0, 100.0]]])
    assert torch.equal(mean_pool(h, torch.tensor([[1, 1, 0]])), torch.tensor([[2.0, 3.0]]))


def test_decoder_cross_attends_to_exactly_one_vector():
    sp = tiny_space()
    b = tiny_batch()
    vec = sp.encode(b["src_ids"], b["src_mask"])
    enc, mask = sp._bottleneck(vec)
    out = sp.model(encoder_outputs=enc, attention_mask=mask, decoder_input_ids=b["dec_ids"],
                   output_attentions=True)
    assert all(a.shape[-1] == 1 for a in out.cross_attentions)


def test_decoder_depends_on_source_only_through_the_vector():
    sp = tiny_space().eval()
    b = tiny_batch()
    v = sp.encode(b["src_ids"], b["src_mask"])
    # Same vector, different (padded-out) junk after the sentence: identical loss.
    src2 = b["src_ids"].clone(); src2[1, 3] = 50
    v2 = sp.encode(src2, b["src_mask"])
    assert torch.allclose(v, v2)
    assert torch.allclose(sp.decode_loss(v, b["dec_ids"], b["labels"]),
                          sp.decode_loss(v2, b["dec_ids"], b["labels"]))


def test_language_prefix_reaches_decoder_but_is_not_scored():
    sp = tiny_space().eval()
    b = tiny_batch()
    v = sp.encode(b["src_ids"], b["src_mask"])
    dec2 = b["dec_ids"].clone(); dec2[:, 0] = 41
    # Changing only the prefix token changes the loss on the scored tokens...
    assert not torch.allclose(sp.decode_loss(v, b["dec_ids"], b["labels"]),
                              sp.decode_loss(v, dec2, b["labels"]))
    # ...and 5 positions are scored: 3 + 2 (the prefix and padding are -100).
    assert int((b["labels"] != -100).sum()) == 5


def test_loss_weights_and_total():
    sp = tiny_space().eval()
    out = sp.losses(tiny_batch(), LossWeights(1.0, 0.1, 0.01))
    expected = out["mt"] + 0.1 * out["mse"] + 0.01 * out["dae"]
    assert torch.allclose(out["total"], expected)
    only_dae = sp.losses(tiny_batch(), LossWeights(0.0, 0.0, 1.0))
    assert set(only_dae) == {"dae", "total"}


def test_overfits_one_batch():
    sp = tiny_space().train()
    b = tiny_batch()
    opt = torch.optim.AdamW(sp.parameters(), lr=3e-3)
    first = None
    for _ in range(60):
        opt.zero_grad()
        loss = sp.losses(b, LossWeights())["total"]
        first = first if first is not None else loss.item()
        loss.backward(); opt.step()
    assert float(loss) < 0.5 * first


def test_generate_forces_prefix_and_returns_continuation():
    sp = tiny_space().eval()
    v = sp.encode(*[tiny_batch()[k] for k in ("src_ids", "src_mask")])
    out = sp.generate(v, [40], max_new_tokens=5, do_sample=False)
    assert out.shape[0] == 2 and out.shape[1] <= 5


def test_infill_noise_masks_about_35_percent_in_spans():
    rng = random.Random(0)
    ids = list(range(100, 200))
    out = infill_noise(ids, mask_id=7, rng=rng)
    kept = [t for t in out if t != 7]
    assert len(kept) == 100 - 35                     # exactly round(100 * 0.35) tokens masked
    assert kept == sorted(kept)                      # order preserved
    assert all(not (a == 7 and b == 7) for a, b in zip(out, out[1:]))  # one mask per span


def test_retrieval_error_worked_example():
    a = np.eye(4)
    b = np.eye(4)[[0, 1, 3, 2]]                       # rows 2 and 3 swapped -> 2 of 4 wrong
    assert retrieval_error(a, b) == 0.5
    assert retrieval_error(a, np.eye(4)) == 0.0


def test_balanced_accuracy_worked_example():
    y = np.array([0, 0, 0, 1])
    correct = np.array([True, True, False, True])
    assert _balanced_accuracy(y, correct) == pytest.approx((2 / 3 + 1) / 2)   # 0.8333


def test_probe_separable_and_random():
    rng = np.random.default_rng(0)
    y = np.array([0] * 300 + [1] * 300)
    x_sep = rng.normal(size=(600, 8)); x_sep[:, 0] += 4 * y
    x_rand = rng.normal(size=(600, 8))
    ba_sep, c_sep = probe_scores(x_sep, y)
    ba_rand, c_rand = probe_scores(x_rand, y)
    assert ba_sep > 0.95 and 0.4 < ba_rand < 0.6
    point, lo, hi = gap_ci(y, c_sep, c_rand, resamples=2000)
    assert lo > 0 and lo <= point <= hi
    assert gap_ci(y, c_sep, c_sep, resamples=200) == (0.0, 0.0, 0.0)


@pytest.mark.parametrize("s,po,ay", [
    ("Salamat po.", 1, 0),
    ("Opo, kumain na ako.", 1, 0),
    ("Ang bata ay kumain ng mangga.", 0, 1),
    ("Kumain ang bata ng mangga.", 0, 0),
    ("Ay, nakalimutan ko!", 0, 0),
    ("Si Maria po ay guro.", 1, 1),
    ("Pumunta siya sa Pook.", 0, 0),                 # 'Pook' is not 'po'
])
def test_labels(s, po, ay):
    assert label_po_opo(s) == po and label_ay_inversion(s) == ay


def _tok(name):
    from transformers import AutoTokenizer
    snaps = glob.glob(f"/hf/hub/models--google--{name}/snapshots/*")
    if not snaps:
        pytest.skip(f"{name} tokenizer not in HF cache")
    return AutoTokenizer.from_pretrained(snaps[0])


def test_madlad_prefix_is_single_language_token():
    tok = _tok("madlad400-3b-mt")
    assert lang_prefix_ids(tok, "fil") == [tok.convert_tokens_to_ids("<2fil>")]
    assert len(lang_prefix_ids(tok, "en")) == 1


def test_collator_shapes_and_no_language_tag_on_encoder():
    tok = _tok("madlad400-3b-mt")
    coll = Collator(tok, bidirectional=False)
    b = coll([{"src": "The child ate.", "tgt": "Kumain ang bata.", "src_lang": "en", "tgt_lang": "fil"}])
    fil = tok.convert_tokens_to_ids("<2fil>")
    assert fil not in b["src_ids"][0].tolist() and fil not in b["tgt_ids"][0].tolist()
    assert b["dec_ids"][0, 0].item() == fil and b["labels"][0, 0].item() == -100
    assert b["dec_ids"][0, 1:].tolist() == b["tgt_ids"][0].tolist()
    assert coll.mask_id == tok.convert_tokens_to_ids("<mask>")


def test_mt5_uses_sentinel_as_mask():
    tok = _tok("mt5-base")
    assert Collator(tok).mask_id == 250099      # mT5's <extra_id_0>, inside the trained embeddings
