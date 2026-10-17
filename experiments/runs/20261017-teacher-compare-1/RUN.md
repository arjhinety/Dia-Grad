# Run 20261017-teacher-compare-1

**Status: DONE 2026-10-17 (exploratory).** Decision basis: D25 and D26 (`decisions/DECISIONS.md` §D25, §D26).

## Before (fill in and commit before starting)

- **Type:** exploratory. It informs teacher choice for synthetic data (D22 Mix 4, D25); it supports no
  paper claim by itself.
- **Question / hypothesis:** do permissive teachers (MADLAD-400-7B/10B, Qwen3) translate en↔tl about
  as well as NLLB-200-3.3B, so that keeping NLLB/SONAR outputs out of training (D25) costs little? A
  second question: how fast does each generate on the GB10? Back-translation planning needs that
  number [unknown so far].
- **Research basis:**
  - MADLAD reports its model within 3.8 chrF of NLLB-54B on Flores-200 [paper: 2309.04662].
  - Teacher choice matters for synthetic data, with a Tagalog case study [paper: 2604.11290].
- **Expected result:**
  - MADLAD-10B within a few chrF++ of NLLB-3.3B, and Qwen3-32B weaker on fil→en than the MT models
    [inference].
  - MADLAD-3B is the slowest per quality point? [unknown].
- **Decision rule (D26, confirmed):** if NLLB-3.3B beats the best permissive model by more than
  5 chrF++ in both directions, with the 95% bootstrap interval of the gap above 0, bring a
  research-only deviation (D25 option 2) back as a new decision. Otherwise D25 stands.
- **Models (all pinned; list confirmed, D26)**, about 189 GB downloaded to `~/hf`:

  | Model | Revision | Size | Licence | Use |
  |---|---|---|---|---|
  | google/madlad400-3b-mt | fa184c675da0b5c9e1c8694fccd4e12e2d422094 | already local | Apache-2.0 | candidate |
  | google/madlad400-7b-mt | 1ff63ce7ddd571a69d45cad9672c553428419671 | 33.2 GB | Apache-2.0 | candidate |
  | google/madlad400-10b-mt | 9f2797629c31e69617186dbe5f0ca43bf662f36d | 42.9 GB | Apache-2.0 | candidate |
  | Qwen/Qwen3-14B | 40c069824f4251a91eefaf281ebe4c544efd3e18 | 29.5 GB | Apache-2.0 | candidate |
  | Qwen/Qwen3-32B | 9216db5781bf21249d130ec9da846c4624c16137 | 65.5 GB | Apache-2.0 | candidate |
  | facebook/nllb-200-3.3B | 1a07f7d195896b2114afcb79b7b57ab512e7b43e | 17.6 GB | CC-BY-NC-4.0 | **U6 only**: its outputs are never kept as training data (D25) |

- **Data:** 1,000 pairs sampled (seed 20261017) from `~/data/t1/heldout/dev_massive.jsonl`
  (registry `massive-1.1-tl-PH`, sha256 7f2597ba…), translated in both directions. Never SMOL (gate
  test, D19).
  - Caveat: MASSIVE is localised (entity swaps), so chrF++ against its references is low for every
    model. The comparison is relative, not absolute [inference].
- **Metrics:**
  - chrF++ (sacrebleu 2.6.0) per direction, with a 95% paired bootstrap interval (10,000 resamples);
  - sentences/s and tokens/s, and peak memory, per model.
  - No automatic metric is validated for Filipino (A6), so 50 outputs per model per direction get a
    blind check by Codex gpt-6.1-sol (D26): naturalness 0–2 and meaning 0–2, scored separately, with
    15 hidden repeats per direction to measure the judge's own consistency. Rubric: `RUBRIC` in
    `src/diagrad/t1/teacher_compare.py`, revised before any real output existed
    (Taglish and everyday register can score 2; *po* neutral; meaning-0 defined operationally).
    Advisory only: an LLM judge is not human evaluation (A6).
- **Decoding:**
  - MADLAD and NLLB: beam 4, max 256 new tokens; MADLAD with its `<2xx>` source tag.
  - Qwen3: greedy, thinking off, one fixed translation prompt (written in the config before running).
- **Contamination check:** MASSIVE dev was already checked against NLLB's *training bitext* (D20).
  Whether these models saw MASSIVE in their own training is [unknown], which matters for an absolute
  claim, not for this relative comparison.
- **Config:** `experiments/configs/20261017-teacher-compare-1.yaml` @ commit `1267beacc1d4bd46efc14a8d8b07c8952910dad2`
- **Code:** `src/diagrad/t1/teacher_compare.py` (`generate` / `score` / `pack`), tests
  `tests/test_teacher_compare.py`.
- **Kill criterion:** none needed (exploratory, no training). A model whose outputs hit the 256-token
  cap on more than 5% of sentences is reported as degenerate on this set, not re-decoded [judgement].
- **Seed(s):** 20261017 (sampling); decoding is deterministic.
- **Environment:** GB10 workstation, NVIDIA GB10, image `diagrad:t1` (pins in `env/requirements.lock`).
- **Planned compute:** smoke timing below; full estimate after MADLAD-3B's 1,000-sentence run.

## During

- 2026-10-17 06:39 UTC: **run started**, MADLAD-3B (container `tc-madlad-3b`), config @ 1267bea.
- 2026-10-17 06:45 UTC: MADLAD-3B done (log `artifacts/generate-log.jsonl`).
  - en→fil: 1,000 sentences in 37.0 s (27.0 sentences/s, 331 tokens/s), 0 hit the cap, peak 7.9 GB.
  - fil→en: 154.7 s (6.5 sentences/s, 65 tokens/s), 2 of 1,000 hit the cap (0.2%), peak 15.4 GB.
  - The other models wait for their downloads (Hugging Face, unauthenticated, 2–24 MB/s).
- 2026-10-17 07:46 UTC: downloads restarted with an authenticated Hugging Face token (kept outside the repository). The bottleneck was the workstation's network link (~17 MB/s total inbound), not rate limits.
- 2026-10-17 09:08 UTC: downloads done. Shards checked against each `*.index.json`: MADLAD-7B 7 shards
  33.2 GB, MADLAD-10B 9 / 42.9 GB, Qwen3-14B 8 / 29.5 GB, Qwen3-32B 17 / 65.5 GB, none missing.
  - NLLB-3.3B has no safetensors at the pinned revision, only `pytorch_model*.bin`, which the download
    had excluded. Fetched at the same revision (container `dl-nllb`); transformers loads `.bin` with
    torch's weights-only unpickler.
- 2026-10-17 09:10 UTC: MADLAD-7B, MADLAD-10B, Qwen3-14B, Qwen3-32B started in sequence.
- 2026-10-17 ~09:20 UTC: **interrupted.** The sequence ran as a child of an interactive terminal session, and the
  session ended during MADLAD-10B fil→en. Completed before that: MADLAD-7B both directions (en→fil
  14.6 sentences/s, fil→en 3.7, 2 hit the cap), MADLAD-10B en→fil (11.8 sentences/s, 0 hit the cap).
  NLLB `.bin` shards (3 of 3) arrived 10:22 UTC.
- 2026-10-17 13:39 UTC: relaunched detached (`setsid nohup`, script `~/hf/logs/run_teachers_2.sh`,
  log `~/hf/logs/run_teachers_2.log`): MADLAD-10B (both directions again), Qwen3-14B, Qwen3-32B,
  NLLB-3.3B. The first MADLAD-10B en→fil output's sha256 is kept to check that the rerun is identical
  (beam search should be deterministic).
- 2026-10-17 13:45 UTC: **code change, loading only.** `from_pretrained(...).cuda()` builds a CPU copy
  and then a GPU copy. On the GB10, CPU and GPU share 121 GB (80 GB available at the time; an unrelated
  process holds 3.5 GB of GPU memory), so Qwen3-32B (65.5 GB) would likely run out of memory.
  Changed to `device_map="cuda"` (weights straight to the GPU) before Qwen3 started. MADLAD-10B was
  already loaded the old way. Decoding is unchanged: MADLAD-3B on 8 pairs gives byte-identical outputs.
  Free memory and GPU use are logged every 30 s to `~/hf/logs/mem-20261017.log`.
- 2026-10-17 ~13:43 UTC: **out of memory, second interruption.** Free memory fell from 50 GB
  (13:41:55) to 10 GB (13:42:25); the kernel's OOM killer then took down every process of the run's account
  (kernel `oom_kill` counter 73 since boot, 13 in the account's user slice; its systemd manager
  restarted at 13:44:06 UTC; tmux died too). Running at the time: MADLAD-10B fil→en (loaded the old way,
  with a CPU copy), a MADLAD-3B smoke test started alongside it (a mistake: two GPU jobs on a shared
  121 GB pool), and an unrelated process (3.5 GB). Both interruptions happened during MADLAD-10B
  fil→en. The kernel log (which process was killed first) needs admin rights [unknown].
- 2026-10-17 13:47 UTC: **safeguards**, then MADLAD-10B relaunched alone:
  - `docker --memory` does not count GPU allocations on the GB10 (tested: 8 GB allocated under a
    4 GB cap). It is kept (40 GB) for host-side memory only.
  - `--gpu-mem-gb` (new, `torch.cuda.set_per_process_memory_fraction`): past the ceiling PyTorch raises
    `OutOfMemoryError` in that process instead of the kernel killing the session (tested on the GB10).
    MADLAD-10B runs with 70 GB. A ceiling cannot change outputs.
  - One GPU job at a time; free memory logged every 5 s (`~/hf/logs/mem-<model>-<time>.log`).

- 2026-10-17 06:24 UTC: weight downloads started (container `dl-teachers`, script
  `~/hf/logs/dl-teachers-20261017.sh`, pinned revisions, safetensors only).
- 2026-10-17 06:27 UTC, **smoke test (not the run; output in a temporary directory, discarded)**:
  MADLAD-3B, first 32 sampled pairs.
  - en→fil 15.9 sentences/s; fil→en 0.51 sentences/s.
  - The fil→en slowdown is one degenerate output: `huy huy` → "Whoa, whoa, …" to the 256-token cap.
    With length-sorted batching the whole batch waits for it.
  - Kept the decoding as written (no repetition penalty: changing decoding after seeing outputs would
    bias the comparison). The runner now logs `hit_max_new_tokens` per model and direction.
  - `score` and `pack` were exercised on copies of these outputs (gap 0.0 for identical systems, as
    expected). No chrF++ from the smoke test is a result.

## After

- End: 2026-10-17 14:41 UTC (last generation); scoring and the blind check the same day.
- **Results.** chrF++ on 1,000 MASSIVE-dev pairs per direction (`scores.json`; sacrebleu signature
  `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.6.0`); NLLB's lead is NLLB minus the model, with the 95% paired-bootstrap interval
  (10,000 resamples). Codex labels on 50 outputs per model and direction, 0–2, blind (`naturalness.json`);
  in brackets, the number of 0 labels.

| Direction | Model | chrF++ | NLLB's lead | Naturalness (0s) | Meaning (0s) |
|---|---|---:|---:|---:|---:|
| en-fil | madlad-3b | 57.51 | +5.62 [+4.56, +6.69] | 1.00 (12) | 1.50 (9) |
| en-fil | madlad-7b | 58.37 | +4.76 [+3.71, +5.84] | 1.14 (10) | 1.38 (11) |
| en-fil | madlad-10b | 58.02 | +5.12 [+4.05, +6.20] | 1.14 (10) | 1.46 (9) |
| en-fil | qwen3-14b | 51.44 | +11.69 [+10.48, +12.90] | 1.60 (1) | 1.28 (16) |
| en-fil | qwen3-32b | 52.52 | +10.62 [+9.35, +11.83] | 1.62 (1) | 1.42 (9) |
| en-fil | nllb-3.3b | 63.13 | reference | 1.58 (3) | 1.56 (6) |
| fil-en | madlad-3b | 63.53 | -2.60 [-3.73, -1.39] | 1.62 (2) | 1.62 (6) |
| fil-en | madlad-7b | 64.09 | -3.16 [-4.46, -1.72] | 1.64 (4) | 1.74 (4) |
| fil-en | madlad-10b | 63.39 | -2.45 [-3.82, -0.98] | 1.60 (4) | 1.62 (7) |
| fil-en | qwen3-14b | 60.45 | +0.49 [-0.65, +1.64] | 1.70 (0) | 1.68 (6) |
| fil-en | qwen3-32b | 61.33 | -0.40 [-1.50, +0.71] | 1.70 (0) | 1.62 (6) |
| fil-en | nllb-3.3b | 60.93 | reference | 1.70 (0) | 1.60 (5) |

- **Decision rule (D26): not tripped.** en→fil: NLLB leads the best permissive model (MADLAD-7B) by
  4.76 [3.71, 5.84], not more than 5. fil→en: every MADLAD model is ahead of NLLB. **D25 stands.**
- **Against expectation.**
  - Expected MADLAD-10B to be the best MADLAD; MADLAD-7B is ahead of it in both directions, within
    about one interval width [measured].
  - Expected Qwen3 to be weaker on fil→en; Qwen3-32B is level with NLLB there (−0.40 [−1.50, +0.71]).
  - **chrF++ and the blind check disagree on en→fil.** MADLAD has the highest chrF++ of the permissive
    models but the lowest naturalness (1.00–1.14, with 10–12 of 50 rated 0), while Qwen3 and NLLB score
    1.58–1.62 with 1–3 zeros. Codex's notes on the zeros: word-for-word calques of short lowercase
    commands ("who was in the beatles" → "na ay sa ang beatles"), entity names translated ("apple" →
    "mansanas"), and untranslated commands ("radio on") [measured]. chrF++ rewards their word overlap
    with the reference. This is the falsifier D26 names for the 5-point rule: chrF++ alone would have
    picked the less natural teacher [inference].
- **Caveats.**
  - The judge is an LLM, not a human; LLM judges may favour LLM-style fluent output, which would help
    Qwen3 [inference]. Human evaluation is still the evidence (A6).
  - The 15 hidden repeats per direction got identical labels (15/15). They were judged inside the same
    prompt, so this shows within-prompt consistency, not independent agreement [inference].
  - MASSIVE is voice-assistant commands: short, lowercase, unpunctuated and localised. Results may not
    hold for full sentences (e.g. ParaCrawl, Bible text) [inference].
  - One seed, one prompt, one decoding setting per model; exploratory.
- **What we learned.**
  1. Keeping NLLB/SONAR outputs out of training costs little on this set: in fil→en the permissive models
     are ahead, in en→fil Qwen3-32B matches NLLB on naturalness (1.62 vs 1.58) and is close on meaning
     (1.42 vs 1.56).
  2. For en→fil synthetic data, chrF++ against MASSIVE is not enough to choose a teacher; a naturalness
     check is needed.
  3. GB10 throughput: MADLAD-3B 27 / 6.5 sentences/s (en→fil / fil→en), Qwen3-32B 2.1 / 3.4, NLLB 30 / 34.
- **Artifacts** (not committed; sha256 in `metrics.jsonl`): `artifacts/<model>.<direction>.jsonl`, the
  naturalness prompts, answers and keys.
- **Follow-ups.** Repeat the naturalness check on a full-sentence set before choosing a back-translation
  teacher (D22 Mix 4); compare Codex's labels with the human labellers' on a shared sample.
