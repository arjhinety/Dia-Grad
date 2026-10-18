# Run 20261018-mono-filter-quality-1

**Status: PLANNED (exploratory).** Decision basis: D28 (`decisions/DECISIONS.md` §D28).

## Before (fill in and commit before starting)

- **Type:** exploratory. It decides whether D28 option A (drop every paragraph also in MADLAD-400)
  stands or is revisited as option B; it supports no paper claim by itself.
- **Question / hypothesis:** the paragraphs that the MADLAD filter removes from the option A pool are not
  clearly better than the paragraphs it keeps (D28 hypothesis 3).
- **Research basis:**
  - Against: text kept by several independent pipelines tends to be higher quality
    [paper: alrashed2025mix, 2512.18834, abstract and §7.1]. The dropped group is, by construction,
    text that FineWeb-2 or HPLT 2.0 *and* MADLAD-400 all kept.
  - For: a much cleaner Basque corpus gave similar downstream NLU results [paper: artetxe2022does,
    2203.08111, abstract].
- **Expected result:** dropped paragraphs score a little higher, by less than 0.3 [inference from the
  agreement paper; size unknown].
- **Decision rule (fixed before any rating, D28; the third score added after a rubric review, still
  before any rating):** the choice is revisited as option B if, on any one score, mean(dropped) -
  mean(kept) reaches the threshold and its 95% bootstrap interval lies above 0:
  - quality, 0-2, Filipino/Taglish paragraphs only: 0.3;
  - naturalness, 0-2, Filipino/Taglish paragraphs only: 0.3;
  - eligible, the share of paragraphs labelled Filipino/Tagalog or Taglish: 0.10 [judgement threshold].
  Otherwise option A stands. If more than 20% of hidden-repeat pairs get a different label,
  the judge is not consistent enough and there is no verdict.
- **Data:**
  - Pool: FineWeb-2 fil_Latn train (registry `hf-fineweb-2-fil_Latn`, sha256 14948c3e…) and HPLT 2.0
    cleaned tgl_Latn (registry `hf-hplt2.0-cleaned-tgl_Latn`, 20 files, sha256 in the record).
  - Membership: unique-paragraph hashes of MADLAD-400 fil clean and noisy (all three files), from
    `data/mix/measure_mono.py stats` (`data/mix/measure-mono-2026-10-17.json`).
  - Unit: unique normalised paragraphs of at least 5 words. A paragraph is a candidate when a seeded
    hash of its text falls in a 1-in-4,000 subset, so selection cannot depend on content; the first 100
    per group by that hash are taken; paragraphs over 150 words are left out of both groups.
  - No held-out or evaluation text is involved.
- **Judge:** Codex gpt-6.1-sol, blind: shuffled, random item ids, group held only in `key.json`; 4
  batches (4 separate calls) of about 55 items; 20 hidden repeats, each in a different batch from its
  original, so a repeat is judged in a separate call (in D26 all repeats shared one prompt). Labels:
  language_status, quality 0-2 and naturalness 0-2 (Filipino/Taglish only), translation_artifacts.
  Rubric: `RUBRIC` in `data/mix/quality_check.py`. Advisory only: an LLM judge is not human evaluation (A6).
- **Metrics:** mean per group and score, count of 0s, mt_suspect count; gap with a 95% percentile
  bootstrap interval (10,000 resamples, each group resampled on its own); repeat-pair disagreement.
- **Config:** `experiments/configs/20261018-mono-filter-quality-1.yaml` @ commit (filled in at commit).
- **Code:** `data/mix/quality_check.py` (`sample` / `pack` / `score`), tests `tests/test_quality_check.py`.
- **Kill criterion:** none needed (no training).
- **Seed(s):** 20261018 (selection and packing; bootstrap uses the same seed).
- **Environment:** GB10 workstation, image `diagrad:t1` (sampling and scoring); Codex CLI on the host.
- **Planned compute:** CPU only; sampling about 20 minutes; 4 Codex calls.

## During

- 2026-10-18: `sample` run (deterministic from the config; no ratings exist yet).
  - 11,890 candidates: 5,895 dropped, 5,995 kept (49.6% dropped; the full pool is 49.5%, 23.2M of
    46.9M unique paragraphs [measured]). Over 150 words: 67 dropped, 70 kept candidates (1.1%, 1.2%).
  - Chosen: 100 per group. Dropped: 58 in MADLAD clean, 42 in noisy only; sources 56 FineWeb-2,
    17 HPLT, 27 both. Kept: 45 FineWeb-2, 46 HPLT, 9 both. Mean length 35.2 and 29.8 words.
  - The groups differ in source mix and in cross-source agreement by construction; that is part of
    the question, not a defect of the sample.
  - `artifacts/sample.json` sha256 76b2efe79ce3e999768bdb7e0b1dcf2590c7a4cc136317ee3f8411c4b00b6108.
- 2026-10-18 13:26: rubric revised before any rating:
  - a separate language_status label, so Cebuano, Ilokano or English text is counted as not
    Filipino rather than as bad Tagalog; quality and naturalness are scored only for Filipino/Taglish
    paragraphs, and the share of those becomes a third score ("eligible");
  - quality and naturalness are independent; useful lists, ads, legal text and FAQs are not downgraded
    for genre; boundary clipping alone is not penalised;
  - Taglish with long English stretches can score 2; regional, historical, religious and online usage
    and non-KWF spellings (sya, di, pwede) are accepted;
  - mt_suspect replaced by translation_artifacts (present/absent/uncertain), described as perceived
    artifacts, not machine origin;
  - confidence refers to quality and naturalness only.
  Not adopted: a separate calibration set before rating. It would need constructed
  Filipino examples; the hidden repeats measure consistency instead [judgement].

## After

(to be filled in)
