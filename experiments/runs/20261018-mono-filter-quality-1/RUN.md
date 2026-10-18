# Run 20261018-mono-filter-quality-1

**Status: DONE 2026-10-18 (exploratory).** Decision basis: D28 (`decisions/DECISIONS.md` §D28).

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
- **Config:** `experiments/configs/20261018-mono-filter-quality-1.yaml` @ commit `15ecf9599e60cf9319281f924250f7b2f6f726a7`.
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

- 2026-10-18 12:28-12:30 UTC: rating, 4 Codex gpt-6.1-sol calls in parallel (config @ 15ecf95); 220 of 220
  items answered. Hashes:
  - `key.json` 9f5463ac15942336f2f4fae06128cff91b9dca38bf510a5b62ebd08e88ac9ddd
  - `batch-0.answer.md` b7428a3ac5c738697121737d77897ab1bb161d18956f41a0a4aeca635bdae946
  - `batch-1.answer.md` 09013a3f40f5a6723c56a14a1081cf3b138b21cc0c49b60f065d6f8d1bb5831f
  - `batch-2.answer.md` b480e57bf663b78880df47984566f5ee5646d53ba4ddecf7612f3c1871095d7a
  - `batch-3.answer.md` bd227bebc005142180a925d2b36b23b488639ce2ff9162729654c81501e1d3df
## After

- **Outcome: option A stands** (`scores.json`). The rule did not trip, and the gaps point the other way:
  paragraphs the MADLAD filter drops score clearly *lower*.

  | Score | Dropped | Kept | Dropped - kept [95% interval] |
  |---|---|---|---|
  | quality (0-2, Filipino/Taglish only) | 1.17 (n 90, 31 zeros) | 1.81 (n 91, 4 zeros) | -0.65 [-0.86, -0.44] |
  | naturalness (0-2, Filipino/Taglish only) | 1.11 (30 zeros) | 1.63 (2 zeros) | -0.52 [-0.73, -0.30] |
  | eligible (share Filipino/Taglish) | 0.90 | 0.91 | -0.01 [-0.09, 0.07] |
  | translation artifacts "present" | 39 of 100 | 16 of 100 | not part of the rule |

- **Judge consistency:** 4 of 20 hidden-repeat pairs differ on at least one label (20%), exactly at the
  limit, so the judge counts as usable, but only just. Two of the four are language_status only
  (filipino_tagalog vs taglish, mixed_uncertain vs filipino_tagalog); one is a quality 2 vs 0 on a kept
  paragraph. Repeats were judged in separate calls, so this is a stricter test than D26's 15/15.
- **Checks [measured]:** group labels re-derived from the MADLAD hash sets: 0 mismatches
  (`artifacts/breakdown.py`).
- **Where the gap comes from [measured, small cells]** (quality means, Filipino/Taglish items):
  - by MADLAD split: in MADLAD clean 0.77 (n 53); in MADLAD noisy only 1.73 (n 37); in neither 1.81 (n 91);
  - by source: dropped FineWeb-2 only 0.88 (n 50), dropped in both FineWeb-2 and HPLT 1.40 (n 25),
    dropped HPLT only 1.73 (n 15); kept 1.64-1.98 in every source cell.
- **Interpretation:**
  - The low scores sit in paragraphs that FineWeb-2 and MADLAD-400 *clean* share. A plausible reason is
    that templated or machine-translated pages (SEO, product spam) repeat across many sites and so
    survive in several crawls [inference; repetition per paragraph was not measured].
  - This contradicts, for this pool, the cross-source agreement signal of alrashed2025mix (2512.18834).
    Their agreement is between independent pipelines at document level after MinHash; ours is exact
    paragraph match against the base model's own corpus, and one judge on 200 paragraphs [inference].
  - Side finding: MADLAD-400 clean, the base model's pre-training text, contains this low-scoring material
    [inference from 53 items; not a measurement of MADLAD-400 as a whole].
  - Advisory only: one LLM judge, no human labels (A6).
- **Follow-ups.**
  - The kept group still has 4 of 91 quality zeros and 16 translation-artifact flags; the slice build
    should still filter (D28 step 5) [judgement].
  - Measuring per-paragraph repetition would test the inference above cheaply.
