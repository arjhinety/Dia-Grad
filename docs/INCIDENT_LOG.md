# Incident log

DiaGrad publishes its mistakes along with its results. An incident that cost work, changed a run or
weakens a claim is part of the research record. Each entry states what happened, what was lost, what
survived, what it does to any claim, and what changed. Entries are never edited to look better; a
later entry can supersede an earlier one, and both stay. (Format adopted from OpenGrad.)

| ID | Date | Summary | State |
|---|---|---|---|
| INC-0001 | 2026-10-17 | Out of memory on the shared GB10 killed the whole user session during the teacher comparison | Closed — safeguards in place; no outputs lost |
| INC-0002 | 2026-10-17 | Qwen3-32B could not load: the loader held a full CPU copy of the weights | Closed — shard-by-shard loader, weights verified identical |

---

## INC-0001 — Out of memory killed the user session

**Date:** 2026-10-17 · **Run:** [`20261017-teacher-compare-1`](../experiments/runs/20261017-teacher-compare-1/RUN.md)
· **Severity:** low for results, high for working time.

### What happened

The GB10 has 121 GB of memory shared by CPU and GPU. While MADLAD-400-10B translated fil→en (its
peak is 38.7 GB, because a few degenerate outputs run to the 256-token cap with beam 4), a second GPU
job, a smoke test, was started alongside it, and an unrelated service held 3.5 GB. Free memory
fell from 50 GB to 10 GB in 30 seconds. The kernel's OOM killer then killed every process of the user,
including the terminal multiplexer and the run itself (the kernel's `oom_kill` counter showed 13 kills
in the user's slice; the user's systemd manager restarted). An earlier interruption the same day, at
the same step, was most likely the same cause [inference; the kernel log needs admin rights].

### What was lost, what survived

Lost: about 5 hours of wall time. Survived: every completed output, because each model and direction
is written to its own file and logged with its sha256 as soon as it finishes. The rerun of
MADLAD-400-10B en→fil was byte-identical to the first run, so beam search on this setup is
deterministic.

### Effect on claims

None on outputs. Timings are per model and direction, measured with one job on the GPU.

### What changed

- One GPU job at a time; free memory is logged every 5 seconds during runs.
- `--gpu-mem-gb`: a per-process GPU ceiling (`torch.cuda.set_per_process_memory_fraction`), so a model
  that overflows raises `OutOfMemoryError` in its own process instead of the kernel killing the session.
- `docker --memory` caps host memory only; tested: it does not count GPU allocations on the GB10.
- Models load straight to the GPU (`device_map="cuda"`).

## INC-0002 — Qwen3-32B could not load

**Date:** 2026-10-17 · **Run:** the same.

### What happened

With the INC-0001 safeguards in place, Qwen3-32B (65.5 GB) was killed by its container's 40 GB host
memory cap during loading; the user session survived. A load-only test on Qwen3-14B showed why:
`from_pretrained(..., device_map="cuda")` held a full CPU copy of the weights while loading (27.9 GB
anonymous memory at peak for a 27.5 GB model). For Qwen3-32B that is about 131 GB in a 121 GB machine.

### What changed

`load_causal_by_shard` in [`src/diagrad/t1/teacher_compare.py`](../src/diagrad/t1/teacher_compare.py)
builds the model on the GPU and copies the weights in one shard at a time (peak CPU memory 0.6 GB). On
Qwen3-14B it gives the same weights as `from_pretrained`: all 443 tensors equal. Qwen3-32B uses it
(`loader: by_shard` in the run config); the other models keep `from_pretrained`.
