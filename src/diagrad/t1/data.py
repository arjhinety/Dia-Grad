"""Batches for the tranche-1 sentence space: tokenised pairs, decoder language prefix, DAE noise.

Input files are JSONL with one pair per line: {"src": ..., "tgt": ..., "src_lang": ..., "tgt_lang": ...}
(lang codes as MADLAD tags without brackets, e.g. "en", "fil"). With `bidirectional`, each pair is
used in a random direction, so the space is trained en->fil and fil->en.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

import torch


def read_pairs(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def lang_prefix_ids(tokenizer, lang: str) -> list[int]:
    """Decoder prefix for a target language: MADLAD's single `<2xx>` token if the vocabulary has it,
    otherwise the tag's sub-word pieces (mT5 has no language tokens)."""
    tag = f"<2{lang}>"
    tid = tokenizer.convert_tokens_to_ids(tag)
    if tid is not None and tid != tokenizer.unk_token_id:
        return [tid]
    return tokenizer(tag, add_special_tokens=False).input_ids


def infill_noise(ids: list[int], mask_id: int, rng: random.Random,
                 mask_ratio: float = 0.35, mean_span: float = 3.5) -> list[int]:
    """mBART-style text infilling (Liu et al. 2020, cited by SONAR for its DAE loss): replace spans
    covering about `mask_ratio` of the tokens, span lengths ~ Poisson(mean_span), each by ONE mask
    token. SONAR does not state its exact noise settings [verify]; these are mBART's defaults."""
    n = len(ids)
    if n == 0:
        return list(ids)
    budget = max(1, round(n * mask_ratio))
    masked = [False] * n
    while budget > 0:
        span = min(budget, max(1, _poisson(rng, mean_span)), n)
        start = rng.randrange(0, n - span + 1)
        for i in range(start, start + span):
            if not masked[i]:
                masked[i] = True
                budget -= 1
        if all(masked):
            break
    out: list[int] = []
    for i, tok in enumerate(ids):
        if not masked[i]:
            out.append(tok)
        elif i == 0 or not masked[i - 1]:
            out.append(mask_id)
    return out


def _poisson(rng: random.Random, lam: float) -> int:
    # Knuth's method; lam is small.
    import math
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= L:
            return k
        k += 1


@dataclass
class Collator:
    tokenizer: object
    max_len: int = 128
    bidirectional: bool = True
    mask_ratio: float = 0.35
    mean_span: float = 3.5
    seed: int = 0

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        tok = self.tokenizer
        self.pad = tok.pad_token_id
        self.eos = tok.eos_token_id
        # Mask token for infilling. mT5: its pretraining sentinel, stored in the transformers 5.x
        # tokenizer as the piece "▁<extra_id_0>" (id 250099). MADLAD: "<mask>" (id 494).
        self.mask_id = None
        for cand in ("<extra_id_0>", "▁<extra_id_0>", "<mask>"):
            tid = tok.convert_tokens_to_ids(cand)
            if tid is not None and tid != tok.unk_token_id:
                self.mask_id = tid
                break
        if self.mask_id is None:
            raise ValueError("tokenizer has neither <extra_id_0> nor <mask> to use as the DAE mask token")

    def _ids(self, text: str) -> list[int]:
        # Plain sentence + EOS, no language tag on the encoder side.
        ids = self.tokenizer(text, add_special_tokens=False).input_ids[: self.max_len - 1]
        return ids + [self.eos]

    def _pad(self, seqs: list[list[int]], value: int) -> torch.Tensor:
        width = max(len(s) for s in seqs)
        return torch.tensor([s + [value] * (width - len(s)) for s in seqs])

    def __call__(self, rows: list[dict]) -> dict[str, torch.Tensor]:
        src, tgt, noisy, dec, lab = [], [], [], [], []
        for r in rows:
            s, t, tl = r["src"], r["tgt"], r["tgt_lang"]
            if self.bidirectional and self.rng.random() < 0.5:
                s, t, tl = r["tgt"], r["src"], r["src_lang"]
            s_ids, t_ids = self._ids(s), self._ids(t)
            prefix = lang_prefix_ids(self.tokenizer, tl)
            src.append(s_ids)
            tgt.append(t_ids)
            noisy.append(infill_noise(t_ids[:-1], self.mask_id, self.rng,
                                      self.mask_ratio, self.mean_span) + [self.eos])
            dec.append(prefix + t_ids)
            lab.append([-100] * len(prefix) + t_ids)
        out = {
            "src_ids": self._pad(src, self.pad), "tgt_ids": self._pad(tgt, self.pad),
            "noisy_ids": self._pad(noisy, self.pad), "dec_ids": self._pad(dec, self.pad),
            "labels": self._pad(lab, -100),
        }
        for k in ("src", "tgt", "noisy"):
            out[f"{k}_mask"] = (out[f"{k}_ids"] != self.pad).long()
        return out
