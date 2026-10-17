# E1 · Filipino machine-translation error study: protocol

> **DRAFT, not yet frozen.** Written 2026-09-24. Sections marked **[ARJHINE]** need a decision.
> Once frozen, record the commit SHA here; afterwards, changes go only in the deviation log (§10).
> Why this study exists: decision D2 (`decisions/DECISIONS.md`). CAMOE is designed with two
> critics (meaning and target-language). Which to build first, and whether both are needed, must rest
> on measured error statistics, not assumption.

## 1. Research questions

- **RQ1 (the deciding question):** In machine translation from English into Philippine languages, what
  share of errors are **meaning errors** (visible in a language-neutral meaning draft) versus **surface
  errors** (only visible in the target-language draft)? Measured per language and per system.
  *Note (D8, 2026-09-24):* annotators judge an error's **effect** (did the meaning change?), while
  the critics are split by **where** an error can be seen (the language-neutral draft or the
  target draft). The two overlap but are not identical: a voice affix that disagrees with its
  markers changes the meaning yet only exists in the target form. The boundary categories and the
  per-error "meaning changed" tick measure how far the two splits diverge.
- **RQ2:** Which error categories dominate? This sizes the critics' named categories.
- **RQ3:** Does the split differ between dedicated translation models and general LLMs?
- **RQ4 (method check):** How well do annotators agree on the meaning/surface family and on categories?
  Can an LLM annotator stand in for humans on this task?

This is a **descriptive** study: it measures, it doesn't test CAMOE. Its output feeds D2's build order
and the paper's motivation section.

## 2. What already exists (phase 0)

No published statistic answers RQ1 (see `phase0-existing-evidence.md`). The closest figures:
- FilBench: GPT-4o failure *modes* (overgeneration, instruction failures, hallucination) among 100
  failures (FilBench says "a sample of 100 failure cases"; how it was sampled is not stated).
- Batayan: qualitative evidence of *ay*-inversion and awkward word choice, with no counts.

## 3. Materials

**Source segments.**
- Language: English → Filipino/Tagalog.
- Data: WMT24++ `en-fil_PH` (`data/registry/wmt24pp-en-fil_PH.json`). 998 rows; 960 usable after
  removing the 38 `is_bad_source` rows (the canary row is one of them).
- Unit: segments are **paragraph-level** (mean 33.6 words and about 2.5 sentences; about half are a
  single sentence, 46–52% depending on the sentence splitter). DiaGrad drafts single sentences, so
  annotators also mark which sentence each error span falls in, and RQ1 is reported both per segment
  and per sentence.
- Domains: news, social, speech, literary.
- The professional post-edit (`target`) serves as the reference.
- Why this set: professional references, permissive license (Apache-2.0), 4 domains, and released in
  2025, which lowers contamination risk for older models (A5).

**Other languages (decided D3: wave 1 is Filipino only).**
- Cebuano and Ilocano need a source set with references. Candidates:
  - FLORES+ devtest (CC-BY-SA; audit-tier per A5);
  - NTREX;
  - a small set we translate ourselves.
- Wave 1 could be Filipino only, with Cebuano added once annotators are found.

**Systems (D3: paid APIs allowed,; final list confirmed at pilot).** Proposed, chosen to cover RQ3 and to include CAMOE's likely base:

| System | Type | Why | Runs where |
|---|---|---|---|
| MADLAD-400-3B-MT | dedicated MT, Apache-2.0 | Proposed Path A base; the errors CAMOE would inherit | locally (RTX 4050, 6 GB, 8-bit) |
| An open LLM with Filipino support (e.g. Qwen3 or SEA-LION) | general LLM | RQ3 contrast | locally if ≤ ~4B, else API |
| DeepSeek-V4.1-Flash | frontier open-weights LLM | Architecture reference with Engram; strong baseline | API (cost) |

Outputs of any model may be *analysed*. Only permissively licensed ones may later become *training*
data (research/licenses/LICENSES.md).

## 4. Sampling

- **Pilot:** 60 segments × all systems. Purposes: test the guidelines and category definitions,
  measure agreement, and time per item.
- **Main:** stratified by domain, **[ARJHINE]** e.g. 300 segments × 3 systems = 900 outputs.
  - Why about 300: if about 50% of errors are meaning errors and there are about 300 errors, the 95%
    interval on that share is about ±6 points (normal approximation: 1.96·√(0.25/300)).
  - Final precision comes from a cluster bootstrap over segments, because errors in one segment aren't
    independent.
- Segment order and system order are randomised per annotator, and system identity is hidden (blind).

## 5. Annotation scheme

Per output:
- **error spans**, each with a **category** and a **severity** (minor / major / critical: MQM weights
  1 / 5 / 25);
- plus a 0–100 overall score (ESA-style; 2406.11580).

Categories come from the A6 proposal (`research/diligence/A6-metric-validity.md` §7). Each is assigned a
**family**, which is what RQ1 measures:

| # | Category | Family | Note |
|---|---|---|---|
| 1 | Mistranslation | meaning | |
| 2 | Omission / Addition (incl. hallucination, overgeneration) | meaning | |
| 3 | Voice/focus error | **boundary** | Philippine-specific. Affix and *ang/ng/sa* marking disagree, so who did what changes = meaning; a different but consistent voice (UD Tagalog paper, 2505.20428 §3.1: variants are "pragmatically equivalent") = surface/discourse |
| 11 | Untranslated | meaning | |
| 12 | Terminology | **boundary** | wrong concept = meaning; wrong term for right concept = surface |
| 4 | Aspect/affix morphology | **boundary** | wrong aspect changes meaning; malformed affix is surface |
| 5 | Spelling / orthography | surface | accepted variants are not errors |
| 6 | Unnatural word order / *ay*-inversion / translationese | surface | Philippine-specific |
| 7 | Pragmatically awkward word choice | surface | |
| 8 | Politeness / respect marking (*po/opo*, respect plurals) | surface | needs a linguist source before guidelines are final (A6) |
| 9 | Code-switching / register mismatch (Taglish) | surface | judged against a declared target register |
| 10 | Wrong language / variety drift | surface | |
| 13 | Culture-specific reference | **boundary** | |
| 14 | Other / source error | excluded from RQ1 | |

- **Boundary categories:** annotators also tick "meaning changed: yes/no" for each error in them.
- RQ1 is reported **three ways**, so the conclusion can't hinge on how we sorted the boundary cases:
  - boundary errors counted as meaning;
  - boundary errors counted as surface;
  - using the tick.
- **Target register:** each segment gets a declared register (the WMT24++ domain gives a default, e.g.
  social = colloquial with Taglish allowed). This lets category 9 be judged consistently.

## 6. Annotators

- **[ARJHINE]** who:
  - native Filipino speakers, at least 2 per output, and 3 on a 25% overlap subset;
  - The author may annotate, but then not on the overlap subset used to measure agreement (to avoid
    designer bias);
  - pay and consent per `data/DATA-PLAN.md`.
- Training: guidelines plus about 20 worked examples; a calibration round on pilot items, then
  discussion, then a guideline revision (logged).
- **LLM annotator (RQ4):**
  - an LLM annotates the same items with the same guidelines, *after* the humans and independently;
  - it is scored against human agreement;
  - it never replaces human labels in the RQ1 estimate.

## 7. Analysis plan (preregistered)

1. Meaning share = meaning errors ÷ (meaning + surface errors). Reported per language × system ×
   domain, and pooled; weighted by severity and unweighted; three ways for boundary categories.
2. 95% confidence intervals by cluster bootstrap over segments (10,000 resamples).
3. Category distribution (RQ2): counts and severity-weighted shares.
4. RQ3: difference in meaning share between system types, with bootstrap CI.
5. Agreement (RQ4):
   - Krippendorff's α on the family label for matched spans;
   - span-overlap F1;
   - category agreement;
   - LLM-vs-human compared with human-vs-human.
6. **Decision rule for D2 build order [ARJHINE: confirm thresholds].** Proposed:
   - if the surface share's CI lower bound ≥ 30%, the target-language critic is built in the first
     round alongside the meaning critic;
   - if the meaning share's CI lower bound ≥ 70%, the meaning critic goes first, as originally
     suggested;
   - otherwise both are built, and order is chosen by engineering cost.

## 8. Outputs and provenance

- MT outputs: `data/outputs/<system>/`, each with its generation config, model revision and seed, per
  `experiments/` conventions (one run record per system).
- Annotations: `data/annotations/`. Raw files are kept unchanged; any cleaning happens in scripts.
- Every figure used in the paper is regenerated by a script in `analysis/`, from committed data.

## 9. Ethics and licensing

- Sources: WMT24++ is Apache-2.0.
- Annotators: consent, fair pay, credit in the acknowledgements.
- No personal data is involved in the source text beyond what WMT24++ already publishes.

## 10. Deviation log

(empty; record any change after freezing: date, what, why, whether results were known)
