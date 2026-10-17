"""Train a tranche-1 sentence space (or the target encoder, with weights mt=0, mse=0, dae=1).

Usage (inside the diagrad:t1 container, repo mounted at /repo):
    python -m diagrad.t1.train_space experiments/configs/<config>.yaml --out experiments/runs/<RUN_ID>

Writes <out>/metrics.jsonl (small, committed) and <out>/artifacts/ (checkpoints, git-ignored).
Write RUN.md's "Before" section first (experiments/README.md).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path

import numpy as np
import torch
import yaml
from torch.utils.data import DataLoader
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from diagrad.t1.data import Collator, read_pairs
from diagrad.t1.space import LossWeights, SentenceSpace


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    out = Path(args.out)
    (out / "artifacts").mkdir(parents=True, exist_ok=True)
    set_seed(cfg["seed"])
    dev = "cuda" if torch.cuda.is_available() else "cpu"

    tok = AutoTokenizer.from_pretrained(cfg["model"], revision=cfg.get("revision"))
    base = AutoModelForSeq2SeqLM.from_pretrained(cfg["model"], revision=cfg.get("revision"),
                                                 dtype=torch.float32)
    if cfg.get("gradient_checkpointing"):
        base.gradient_checkpointing_enable()
    space = SentenceSpace(base).to(dev).train()
    w = LossWeights(**cfg.get("loss_weights", {}))

    coll = Collator(tok, max_len=cfg.get("max_len", 128), bidirectional=cfg.get("bidirectional", True),
                    seed=cfg["seed"])
    rows = read_pairs(cfg["train_file"])
    loader = DataLoader(rows, batch_size=cfg["batch_size"], shuffle=True, collate_fn=coll,
                        generator=torch.Generator().manual_seed(cfg["seed"]), drop_last=True)

    steps, accum = cfg["steps"], cfg.get("grad_accum", 1)
    opt = torch.optim.AdamW(space.parameters(), lr=cfg["lr"], weight_decay=cfg.get("weight_decay", 0.0))
    warm = cfg.get("warmup", 0)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: min(1.0, (s + 1) / max(1, warm)) * 0.5 * (1 + math.cos(math.pi * min(1.0, s / steps))))

    log = open(out / "metrics.jsonl", "a")
    step, t0, tokens = 0, time.time(), 0
    it = iter(loader)
    while step < steps:
        opt.zero_grad(set_to_none=True)
        agg: dict[str, float] = {}
        for _ in range(accum):
            try:
                batch = next(it)
            except StopIteration:
                it = iter(loader)
                batch = next(it)
            batch = {k: v.to(dev) for k, v in batch.items()}
            tokens += int(batch["src_mask"].sum() + batch["tgt_mask"].sum())
            with torch.autocast(dev, dtype=torch.bfloat16, enabled=cfg.get("bf16", True)):
                losses = space.losses(batch, w)
            (losses["total"] / accum).backward()
            for k, v in losses.items():
                agg[k] = agg.get(k, 0.0) + v.item() / accum
        gn = torch.nn.utils.clip_grad_norm_(space.parameters(), cfg.get("clip", 1.0))
        opt.step()
        sched.step()
        step += 1
        if step % cfg.get("log_every", 10) == 0 or step == steps:
            rec = {"step": step, **{f"loss_{k}": round(v, 5) for k, v in agg.items()},
                   "grad_norm": round(float(gn), 4), "lr": sched.get_last_lr()[0],
                   "tokens": tokens, "elapsed_s": round(time.time() - t0, 1)}
            if dev == "cuda":
                rec["max_mem_gb"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
            if not all(math.isfinite(v) for v in agg.values()):
                rec["error"] = "non-finite loss"
                log.write(json.dumps(rec) + "\n")
                raise SystemExit(f"non-finite loss at step {step}: {agg}")
            log.write(json.dumps(rec) + "\n")
            log.flush()
            print(rec, flush=True)
        if cfg.get("save_every") and step % cfg["save_every"] == 0:
            base.save_pretrained(out / "artifacts" / f"step{step}")
    if cfg.get("save_final", True):
        base.save_pretrained(out / "artifacts" / "final")
        tok.save_pretrained(out / "artifacts" / "final")


if __name__ == "__main__":
    main()
