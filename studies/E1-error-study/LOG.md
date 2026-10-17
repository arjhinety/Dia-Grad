# E1 study log

Append-only, dated. Everything that happens in this study is logged here: decisions, data
retrieved, findings, problems, changes of plan. Newest at the bottom.

## 2026-09-24

- **Why the study exists:** decision D2. CAMOE will have two critics (meaning, target-language).
  The build order, and whether both are needed, must rest on real Filipino error statistics, since
  the paper depends on it.
- **Phase 0 (existing evidence):** no published statistic answers RQ1. FilBench gives failure modes
  among 100 hand-picked GPT-4o failures (47/34/19%); Batayan gives qualitative evidence of *ay*-inversion
  and awkward word choice. Details: `phase0-existing-evidence.md`.
- **Source data retrieved:** WMT24++ `en-fil_PH` at revision `fd7405c06494bc66a57b25f55d217a72f96e60dc`,
  sha256 `357a443d…`. 998 rows (1 canary, 38 bad-source), so 959 usable. Domains: social 531,
  literary 206, news 149, speech 111. Registered in `data/registry/wmt24pp-en-fil_PH.json`.
- **Checked in the paper:** `original_target` is a professional human reference and `target` is a
  professional post-edit (sometimes a full rewrite; 2502.12404 §2.1). The dataset has **no MT output**,
  so E1 must generate it. Post-edits differ from references in 202/998 rows (20%).
- **Example seen while inspecting (row 1):**
  - source: "Siso's depictions of land, water center new gallery exhibition";
  - reference: "Mga pagpapahiwatig ni Siso ng bagong eksibisyon sa galeriya ng sentro ng lupa, tubig";
  - post-edit: "Mga depiction ni Siso ng lupa, tubig sentro ng bagong gallery exhibition".
  The reference misreads "center" as a noun (meaning error), and the post-editor chose English
  loanwords (a register choice). Human references themselves contain both error families.
- **Hardware available:** NVIDIA RTX 4050 Laptop GPU, 6 GB; PyTorch 2.10 with CUDA. Enough for
  MADLAD-400-3B in 8-bit and small LLMs.
- **Protocol drafted:** `PROTOCOL.md` (not frozen; [ARJHINE] decisions open: languages, systems,
  sample size, annotators, decision thresholds).
- **Decisions (D3):** wave 1 is Filipino only; paid APIs allowed; annotators to be
  recruited after the research proposal.

## 2026-09-24 (later): corrections from the pre-circulation review

- **Usable count corrected: 960, not 959.** The canary row is itself one of the 38 `is_bad_source`
  rows, so 998 − 38 = 960. The earlier entry above ("so 959 usable") counted the canary twice.
  Found in a pre-circulation review (M6), rechecked on the
  data file. Corrected in PROTOCOL.md §3, the dataset registry notes, the write-up, the study guide
  and the slides.
- **Unit of analysis.** WMT24++ segments are paragraph-level (the paper, 2502.12404 §2.1). Usable
  sources average 33.6 words and 2.51 sentences; 45.9% are one sentence with a rule-based splitter
  (split after `.`, `!` or `?` followed by a capital or digit). An earlier quick count with a looser
  splitter gave about 52% and 2.3. DiaGrad drafts single sentences, so PROTOCOL.md §3 now asks
  annotators to mark the sentence each error span falls in, and RQ1 is reported per segment and per
  sentence.
- **FilBench wording corrected.** The earlier entry says "100 hand-picked GPT-4o failures". FilBench
  says "a sample of 100 failure cases" and does not say how the sample was drawn. Corrected in
  PROTOCOL.md §2 and `phase0-existing-evidence.md`.
- **Voice/focus is a boundary category.** The UD Tagalog paper (2505.20428, §3.1) calls the three
  voice variants of one sentence "pragmatically equivalent". A voice choice consistent with the
  *ang/ng/sa* marking keeps who-did-what (surface/discourse); only affix–marker disagreement changes
  the roles (meaning). E1 already reports boundary categories both ways; the write-up now says so.

## 2026-09-24 (round-2 review)

- **Effect vs visibility.** A round-2 review (N4) noted that RQ1 defines meaning errors as
  "visible in a language-neutral meaning draft" while annotators judge an error's *effect*. A
  voice/marker mismatch changes the meaning but only exists in the Filipino form. Added a note under
  RQ1 in PROTOCOL.md (not yet frozen); the write-up now assigns such errors to the target critic
  (decision D8).
