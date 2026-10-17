"""Single-vector sentence space on a T5-family encoder-decoder (tranche 1).

Recipe from SONAR (Duquenne et al., arXiv 2308.11466, sections 3 and 5):
- the encoder's token outputs are mean-pooled into one fixed-size vector (5.1: mean-pooling was
  chosen over max- and EOS-pooling);
- the decoder cross-attends only to that single vector;
- loss L = L_MT + 0.1 * L_MSE + 0.01 * L_DAE (Table 1, final SONAR row).

Design choices not taken from the paper (pending confirmation, see experiments/T1-SETUP.md):
- the target language is given to the DECODER as a forced prefix (e.g. MADLAD's `<2fil>`), never to
  the encoder, so the pooled vector is not told which language it will be decoded into;
- the MSE term compares the two sides' pooled vectors with gradients through both (no frozen
  teacher); SONAR relies on the MT and DAE terms to prevent collapse (section 3).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import nn
from transformers.modeling_outputs import BaseModelOutput


def mean_pool(hidden: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """Average token vectors over real (unpadded) positions. hidden [B,T,D], mask [B,T] -> [B,D]."""
    m = mask.to(hidden.dtype).unsqueeze(-1)
    return (hidden * m).sum(1) / m.sum(1).clamp_min(1.0)


@dataclass
class LossWeights:
    mt: float = 1.0
    mse: float = 0.1
    dae: float = 0.01


class SentenceSpace(nn.Module):
    def __init__(self, seq2seq: nn.Module):
        super().__init__()
        self.model = seq2seq

    def encode(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        enc = self.model.get_encoder()(input_ids=input_ids, attention_mask=attention_mask)
        return mean_pool(enc.last_hidden_state, attention_mask)

    def _bottleneck(self, vec: torch.Tensor):
        """The decoder sees a length-1 'encoder output': the pooled vector and nothing else."""
        hidden = vec.unsqueeze(1)
        mask = torch.ones(hidden.shape[:2], dtype=torch.long, device=hidden.device)
        return BaseModelOutput(last_hidden_state=hidden), mask

    def decode_loss(self, vec: torch.Tensor, dec_ids: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """Teacher-forced cross-entropy of the target given only `vec`.

        `dec_ids` = forced language prefix + sentence + EOS, right-padded. `labels` is the same with
        prefix and padding set to -100, so the prefix conditions the decoder without being scored.
        The decoder input is built from `dec_ids` (not from `labels`, whose -100 would become padding).
        """
        enc, mask = self._bottleneck(vec)
        cfg = self.model.config
        dec_in = torch.full_like(dec_ids, cfg.pad_token_id)
        dec_in[:, 0] = cfg.decoder_start_token_id
        dec_in[:, 1:] = dec_ids[:, :-1]
        out = self.model(encoder_outputs=enc, attention_mask=mask, decoder_input_ids=dec_in)
        logits = out.logits.float()
        return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), labels.reshape(-1), ignore_index=-100)

    @torch.no_grad()
    def generate(self, vec: torch.Tensor, prefix_ids: list[int], **gen_kwargs) -> torch.Tensor:
        enc, mask = self._bottleneck(vec)
        start = self.model.config.decoder_start_token_id
        dec = torch.tensor([[start, *prefix_ids]] * vec.shape[0], device=vec.device)
        out = self.model.generate(encoder_outputs=enc, attention_mask=mask,
                                  decoder_input_ids=dec, **gen_kwargs)
        return out[:, dec.shape[1]:]

    def losses(self, batch: dict[str, torch.Tensor], w: LossWeights) -> dict[str, torch.Tensor]:
        """batch keys: src_ids/src_mask (source), tgt_ids/tgt_mask (target as encoder input),
        noisy_ids/noisy_mask (noised target), dec_ids and labels (see decode_loss)."""
        out: dict[str, torch.Tensor] = {}
        total = torch.zeros((), device=batch["labels"].device)
        need_src = w.mt > 0 or w.mse > 0
        v_src = self.encode(batch["src_ids"], batch["src_mask"]) if need_src else None
        if w.mt > 0:
            out["mt"] = self.decode_loss(v_src, batch["dec_ids"], batch["labels"])
            total = total + w.mt * out["mt"]
        if w.mse > 0:
            v_tgt = self.encode(batch["tgt_ids"], batch["tgt_mask"])
            out["mse"] = F.mse_loss(v_src.float(), v_tgt.float())
            total = total + w.mse * out["mse"]
        if w.dae > 0:
            v_noisy = self.encode(batch["noisy_ids"], batch["noisy_mask"])
            out["dae"] = self.decode_loss(v_noisy, batch["dec_ids"], batch["labels"])
            total = total + w.dae * out["dae"]
        out["total"] = total
        return out
