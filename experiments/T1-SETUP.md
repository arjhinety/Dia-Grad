# Tranche-1 setup on the GB10 workstation (2026-10-07)

Engineering setup only. No tranche-1 run has been made, and nothing here is a result. Smoke tests used
hand-written toy pairs, kept outside the repo and not counted as data.

## Environment

- Machine: GB10 workstation, NVIDIA GB10, driver 580.173.02, CUDA 13.0, 121 GiB unified memory, aarch64.
  The machine is shared: an unrelated process held 3.5 GB of GPU memory during the smoke runs.
- Image `diagrad:t1` (id `sha256:314f9ae1…81e9df`), built from `env/Dockerfile`:
  - base `nvcr.io/nvidia/pytorch@sha256:42263b24…01edee` (NGC 25.10; torch 2.9.0a0+145a3a7bda.nv25.10);
  - Python dependencies pinned in `env/requirements.lock` (transformers 5.19.0, datasets 5.1.0,
    sacrebleu 2.6.0, scikit-learn 1.7.2, …).
- Build: `docker build -t diagrad:t1 env/`.
- Run (repo at /repo, HF cache at /hf, offline):

  ```
  docker run --rm --gpus all --ipc=host -u $(id -u):$(id -g) -e HOME=/tmp -e HF_HUB_OFFLINE=1 \
    -e PYTHONPATH=/repo/src -v ~/hf:/hf:ro -v $PWD:/repo diagrad:t1 <command>
  ```

- Tests: `python -m pytest -q -p no:cacheprovider tests` (21 passing on 2026-10-07; 26 with the
  contamination tests on 2026-10-08, of which 3 need the HF cache mounted).

## Base models (Apache-2.0; HF cache `~/hf`, outside the repo)

| Model | Revision | Weights file | sha256 | Bytes |
|---|---|---|---|---|
| google/madlad400-3b-mt | fa184c675da0b5c9e1c8694fccd4e12e2d422094 | model.safetensors | 66ff5f8fcaf92291da486fdfbd4d5233cec90e1359348a56e3172c978b3a76d4 | 11,761,587,872 |
| google/mt5-base | 2eb15465c5dd7f72a8f7984306ad05ebc3dd1e1f | pytorch_model.bin | 180573b534144580f04af026da62bf71bc976ee1b7eb311b8945e2fefde8d614 | 2,329,735,129 |

mt5-base ships only a pickled `.bin` (no safetensors). The MADLAD hash is the hub's LFS blob name; the
mT5 hash was recomputed locally and matches its blob name.

## Code (`src/diagrad/t1/`)

- `space.py`: SONAR recipe (arXiv 2308.11466). The decoder sees one mean-pooled vector, and the loss
  is MT + 0.1·MSE + 0.01·DAE. A test checks that the decoder's cross-attention has length 1.
- `data.py`: pairs as JSONL; decoder language prefix; mBART-style infilling noise.
- `gate.py`: retrieval error; linear probes (balanced accuracy, 5-fold); bootstrap gap interval;
  *po/opo* and provisional *ay*-inversion labels.
- `train_space.py`: training loop. Weights `mt=0, mse=0, dae=1` give the target encoder.
- `contamination.py` (added 2026-10-08, D20): A5 §3.2 check (exact match, 8/13-word longest match,
  flag rate per item); standard library only. FRED R-score not written yet (needs the training slice, D6).
- Not written yet:
  - the drafter (z_m → z_t);
  - the gate evaluation script, which encodes held-out sets, runs probes and compares chrF++ with
    MADLAD as released;
  - data preparation from the chosen corpora.

## Design choices to be confirmed (not decided)

1. **The language tag goes to the decoder, not the encoder.** MADLAD normally reads `<2fil>` at the
   start of the source. Here the decoder gets it as a forced first token instead.
   - Why: if the encoder saw the target language, the single vector would encode it, which works
     against a language-neutral meaning vector.
   - The SONAR excerpt we read does not describe how its decoder is told the language [verify].
   - mT5 has no language tokens. It gets the tag's sub-word pieces (`<2fil>` spelled out).
2. **Denoising noise follows mBART:** about 35% of tokens masked in spans of mean length 3.5, each
   span replaced by one mask token. SONAR cites mBART but states no settings [verify].
   - MADLAD uses its `<mask>` token (id 494).
   - mT5 uses its pretraining sentinel `▁<extra_id_0>` (id 250099).
3. **Both sides of the MSE term receive gradients** (no frozen teacher), as SONAR describes. SONAR
   relies on the translation and denoising terms to prevent collapse.
4. **Each pair is used in a random direction** (en→fil or fil→en).

## Observations from the smoke runs (toy data; engineering signals, not results)

- **The MSE term may be too small to matter at SONAR's weight [inference].** In the 3B smoke runs,
  the raw MSE between the two pooled vectors was 1e-4 to 4e-4. At weight 0.1 it adds about 1e-5 to a
  loss of about 1.5. MSE depends on the vectors' scale, and NLLB's vectors (SONAR's base) may sit at a
  different scale from MADLAD's. Watch retrieval error in the first real run. If the space does not
  align, the weight or a normalisation of the vectors needs revisiting (a design change, logged
  before use).
- **Throughput of MADLAD-400-3B on the GB10, untuned:**
  - batch 64, about 38 tokens per side, gradient checkpointing, fp32 weights with bf16 autocast;
  - 10.5 s per step, about 470 source+target tokens per second, 55 GB peak memory.
  - By the compute plan's formula (6 × N × tokens), that is about 8.5 TFLOP/s. A plain bf16 matrix
    multiply measured 98 TFLOP/s on the same GPU.
  - At this rate, the plan's 1B-token MADLAD sentence-space run would take about 25 days
    [inference: plan tokens counted as source+target tokens].
  - Tuning (no checkpointing, since memory allows it; bf16 weights; fused optimizer; torch.compile)
    may give 2–3× [unknown until measured].
- mT5-base on short toy pairs: about 1,000 tokens per second, 11 GB peak.
- **Added 2026-10-08 (for the tranche-1 roadmap):**
  - mT5-base, full recipe, batch 64, about 38 tokens per side, no checkpointing: steps 10–20 gave
    39,039 tokens in 12.2 s, about 3,200 tokens per second; 26.9 GB peak.
  - MADLAD-3B, denoising only (the target-encoder recipe), same batch: 4.8 s per step against
    10.5 s for the full recipe, i.e. 2.19× faster per step; 54.8 GB peak.
  - Tokens per NLLB pair, from 20,000 pairs (every 50th of the top million): 50.4 MADLAD tokens per
    pair (22.7 English + 27.7 Filipino, with end-of-sentence tokens); 56.9 with mT5's tokenizer. So
    1M pairs hold about 50M tokens, and the plan's 1B tokens is about 20 passes over them.
  - These feed the compute roadmap (`pitch/roadmap/plan.py`).

## Data

See the survey `research/data-survey/en-fil-parallel-2026-10-07.md` and decision D15 (research-only
datasets allowed for initial work; non-commercial models still excluded).
