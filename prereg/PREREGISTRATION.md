# Preregistration: CAMOE (DiaGrad)

> **UNREGISTERED DRAFT.** Prepared on 2026-09-24 from the recorded decisions. Sections marked
> **[ARJHINE]** are still to be decided by the author. Nothing here is a finding. Structure follows a standard
> preregistration scaffold, adapted to an ML architecture study.
> Once frozen, commit it and record the commit SHA below; after that, changes go only in §15.

## 1. Administrative record

- Project: DiaGrad (placeholder name) · CAMOE, Critique-Augmented Mixture of Experts
- Accountable owner: Arjhine Ty (Experimental Intelligence)
- Collaborators and roles: **[ARJHINE]** (Tim Santos: infrastructure and compute resources)
- Record status: draft · Freeze commit SHA: **[on freeze]** · Public registration (e.g. OSF), if any: **[ARJHINE]**
- Funding and compute sources: **[ARJHINE]**
- Prior access to evaluation data: none yet

## 2. Oversight gates

- Data rights and consent review: see `data/DATA-PLAN.md`. Reviewer: **[ARJHINE]**
- Human evaluation with native speakers: needs consent and a pay plan; ethics review needed? **[ARJHINE]**
- No experiment on human-derived data starts until these are cleared.

## 3. Search boundary and evidence

- Search protocol and log: `research/search/` (35 queries on 2026-09-24; re-run before freezing).
- Reference library with provenance: `research/papers/REFERENCES.md`.
- "Not found within this boundary" does **not** establish novelty.

## 4. Starting observation

The author's observation from Japanese translation work:
- LLMs write a translation in one left-to-right pass.
- Humans translate in several mental passes and revise before committing.
- Visible self-critique in reasoning text ("pseudo-critique") is not the same thing.
(Source: `ideas/00-origin.md`.)

## 5. Research question

**Draft:** Does a critic that judges an internal whole-sentence draft, and decides whether another
internal pass is needed, improve translation quality for Philippine languages beyond what the same
extra compute achieves without the critic?

**[ARJHINE]:** confirm or rewrite this question.

## 6. Candidate hypotheses (all remain candidates)

- **H1** (single worker + critic): one worker expert produces the draft, and one or more critics accept it or trigger a repass.
- **H2** (parallel candidates): several experts draft in parallel, and the critic weights them.
- **H3** (many workers, many critics): multiple experts and multiple specialised critics.
- **W1–W5** (why critique must be architectural): **[ARJHINE]**, to be drafted together (`hypotheses/why-architectural.md`).

## 7. Predictions, rivals and falsification

Rival explanations each hypothesis must beat (from `research/diligence/A4-baselines-ablations.md`):
- **R-compute:** gains come from extra compute. Tested by B1 and B2.
- **R-confidence:** the model's own confidence decides repasses as well as the critic does. Tested by B3.
- **R-random:** any repass helps, and the critic's choice doesn't matter. Tested by B4 and B5.
- **R-external:** critiquing written output is as good. Tested by B6 and B7.
- **R-diversity:** REROUTE helps only because any change of experts adds diversity, not because the
  critique directs it. Tested by B11 (random-direction reroute, effect-matched: same share of tokens
  with a changed expert set as REROUTE, random direction; D10, D12). Both change rates are reported.
- **R-metric:** the router's gains are an artefact of its reward metric. Tested by a router rewarded
  with chrF++, compared with the router rewarded with Q = −MetricX-24 at matched compute per stage,
  separately in each translation direction (pooled figures alongside only): C₁ ≈ 0.05, 0.15 and
  0.30 and one stage-2 redo per sentence. Extra compute is a ratio of sums: total extra FLOPs over the
  evaluated sentences ÷ their total first-pass FLOPs, measured from the implementation. Each stage
  and direction has its own λ ≥ 0, chosen on a small pilot of held-out training sentences; at most
  two extra passes per stage. Evidence is only what neither router was rewarded on: native speakers'
  error-span labels on the held-out subset, and language-ID of the outputs (drift claims only).
  chrF++ for the chrF++ router and MetricX-24 for the MetricX-24 router are diagnostic only. The
  held-out human-labelled subset is never used to choose λ, checkpoints or a router. Per stage and
  direction: action rates, redos per sentence, share at the cap, C₁ and C₂, latency. (D14)

Kill criteria (D14). Thresholds marked **[ARJHINE]** are fixed before any tranche-2 data are seen.
- **Compute unit.** Extra compute is total extra FLOPs over the evaluated sentences ÷ their total
  first-pass FLOPs (a ratio of sums, not a mean of per-sentence ratios), per stage (C₁, C₂),
  computed and matched separately for each translation direction, because tokenizers split languages
  into very different numbers of tokens (petrov2023language). All targets (λ1, and λ2's redo rate),
  all compute matching (B1's average, B3, B5 at both stages) and the source-length bins are per
  direction. Pooled figures are reported alongside only. B1's worst case is a per-sentence maximum.
- **Sample size first.** n labelled sentences per language = **[ARJHINE]**, from a simulation-based
  power analysis (item and rater variance from E1 or a labelled pilot; 80% power for δ at two-sided
  5%, all required comparisons jointly; card2020with). If that n is unaffordable, the per-stage tests
  are declared underpowered here, before data, and stage-level claims are exploratory.
- **Calibration failure (either stage).** On the pilot, no λ ≥ 0 brings the dev-set compute level
  (stage 1) or redo rate (stage 2) within **[ARJHINE]**% of target, because the rate jumps past it.
  That stage fails. If the rate stays below target even at λ = 0, λ = 0 is used and the rate is
  reported: a finding, not a failure.
- **Full-run tolerance.** After each full RL run, its dev-set C₁ (ratio of sums) and stage-2 redo
  rate, per translation direction, must be within **[ARJHINE]**% of target. If not, λ is recalibrated
  with one extra probe and the full run is rerun once. If it is still outside, the comparison is made
  at the measured levels and the mismatch is reported. Baselines are matched to the router's measured
  levels in all cases. Every miss is recorded in the run record.
- **Stage-2 test.** Backbone and stage-1 router fixed; compute level(s) **[ARJHINE; suggested
  f₁ = 0.15]**; stage-2 target 1.0 redo per sentence. On the severity-weighted error-span score
  (native speakers, held-out subset, protocol **[ARJHINE, after A6]**), the stage-2 router must:
  - beat B5 at stage 2 (random redos at its observed 0/1/2 distribution and repass/reroute mix) by
    ≥ **[ARJHINE] δ₅⁽²⁾**;
  - and beat B4 at stage 2 with N = 1 by ≥ **[ARJHINE] δ₄** (superiority) or stay within
    **[ARJHINE]** (non-inferiority; **[ARJHINE: choose]**);
  - B4 at N = 0 is reported (does stage 2 help at all?), not required.
- **Stage-1 test.** Backbone fixed, stage-2 policy unchanged, same compute level(s). The stage-1
  router must beat B5 at stage 1 by ≥ **[ARJHINE] δ₅⁽¹⁾**.
  - B5 is **matched in stage-1 FLOPs, not just redo count**: within source-length bins defined per
    direction (edges **[ARJHINE]**, fixed on the dev set before test data), random stage-1 redos at
    the router's observed per-bin 0/1/2 distribution and repass/reroute mix.
  - B5's measured stage-1 extra FLOPs must be within **[ARJHINE]**% of the router's, or the bins are
    narrowed.
  - "Deciding matters" at stage 1 is tested by B3 (also matched in FLOPs) and B1 at equal compute.
- **Both tests:**
  - Each comparison passes if the lower bound of a two-sided 95% paired bootstrap interval (10,000
    resamples of sentences across arms) is above zero (above −margin for non-inferiority), on
    ≥ **[ARJHINE]** of the languages tested. No automatic metric counts.
  - A stage that fails is reported as fixed or random computation, and its posterior-routing claim
    is dropped.
  - An underpowered result is inconclusive, and the claim is not made.
  - **Both stages fail:** stop or redirect.
- The other stop conditions in the write-up's §7 (tranche-1 gate, §7a; beat B3; beat B1; REROUTE
  beats REPASS and B11; annotator agreement), with thresholds **[ARJHINE]**. Beat B3 (both
  versions), beat B1 (average- and worst-case-matched) and REROUTE vs REPASS and B11 are judged on
  the same native speakers' error-span labels, at C₁ = 0.15.
- **Annotation unit.** Tranche-2 human evaluation labels single sentences, each shown in its source
  paragraph; n counts sentences. 16 systems per direction share the same n sentences: the MetricX-24
  and chrF++ routers at the three C₁ levels (the MetricX-24 router at 0.15 also serves both per-stage
  tests), B5 at each stage, B4 at N = 0 and N = 1, B3 ×2, B1 ×2, the REPASS-only router and B11. Each
  output gets 2 annotators plus a third on 25%.
- Reported per stage, per direction and per arm as diagnostics, not tests: action rates, stage-1 and
  stage-2 redos per sentence, the share at the cap, C₁ and C₂, latency.

## 7a. Tranche-1 feasibility gate (provisional, D10; stated in the research proposal)

Proposed on 2026-10-02 and stated in the research proposal. **[ARJHINE]**:
confirm or change the numbers before tranche 1 starts. They may not change after tranche-1 data exist.

Tranche 1 tests the representation, not posterior routing. Held-out text is disjoint from training,
E1 and all evaluation sets.
Held-out sets (D19, 2026-10-08, before any tranche-1 data): the gate test set is SMOL SmolSent
en–fil (754 pairs), opened only for the MADLAD baseline and the gate evaluation; the dev set for
watching training is MASSIVE 1.1 tl-PH dev (minus pairs found in NLLB). Changed from "1,000 held-out
pairs" before data existed.
Contamination (D20, 2026-10-08, before any tranche-1 data): the A5 §3.2 check runs against all
tranche-1 training data (all of NLLB en-tl, and the target encoder's monolingual text). The gate is
judged on the clean subset of SMOL (pairs with no 8-word match, or no whole-side match for sides
shorter than 8 words), fixed before the MADLAD baseline is run; the full-set score is reported beside
it. If more than 10% of SMOL is flagged, tranche 1 stops for the author's decision. Every chrF++ is
reported with the FRED R-score against the parallel training slice.

Probes are linear, scored by balanced accuracy (chance 0.5) with 5-fold
cross-validation and at least 500 sentences per class. Labels are automatic: a token match for
*po/opo*, and a rule-based *ay*-inversion detector checked against 200 hand-labelled sentences.

| Check | Pass if |
|---|---|
| Sentence space works | cross-lingual retrieval error ≤ 5% (en↔fil, the clean subset of the 754 SMOL SmolSent pairs; D19, D20), and en→fil translation decoded from the single vector reaches ≥ 80% of MADLAD-400-3B's chrF++ (as released) on the same pairs |
| z_m lacks surface form | probe on z_m (meaning encoding of the Filipino reference) ≤ 0.65 for *po/opo* and for *ay*-inversion |
| z_t can carry it | probe on the reference z_t (target encoder) ≥ 0.85 on both |
| The drafter delivers it | the four drafter checks below (D30) all pass |

**Drafter checks (D30, decided 2026-10-20, before any tranche-1 result).** The drafter sees only the
English source (as z_m), the target language and the register setting ρ, so it cannot carry the
reference translator's free choices beyond what the English carries. It is therefore scored on what it
writes, each measurement also taken on reference z_t over the same sentences as the yardstick. Every
check uses the conservative end of a two-sided 95% bootstrap interval (10,000 resamples) that resamples
source sentences, keeping a source's polite and plain drafts together; probe folds are grouped by
source. Decoding settings, distance and normalisation are fixed before the run; vectors are re-encoded
with the target encoder.
- **Yardstick (precondition for the *po* legs):** decoded reference z_t keeps *po* in ≥ 80% of *po*
  sentences and adds it to ≤ 5% of the others. Otherwise the *po* legs are inconclusive.
- **(i) Meaning:** under each ρ, the drafter's decoded chrF++ against the reference is ≥ 90% of that of
  decoded reference z_t. A blind LLM-judge check of 200 polite/plain pairs (meaning kept, *po* placed
  grammatically) is reported beside it.
- **(ii) No averaging (round-trip consistency):** the median and the 90th percentile of the distance
  a vector moves when decoded and re-encoded are each ≤ 1.5× those of reference z_t. Positive control:
  synthetic averages (the mean of a sentence's reference z_t and that of the same sentence with *po*
  removed) must move clearly more than reference vectors; if not, the check is uninformative and
  reported as inconclusive.
- **(iii) Register control:** each *po*-set source is drafted with ρ = polite and with ρ = plain;
  *po* appears in ≥ 70% of polite drafts and ≤ 10% of plain drafts, and the paired difference is
  ≥ 0.60.
- **(iv) Readable form:** a linear probe trained on reference z_t with reference labels, applied to
  the drafter's z_t, reaches balanced accuracy ≥ 0.75 against the labels of the drafter's own decoded
  text. For *ay* this needs ≥ 500 drafts of each form; otherwise the *ay* leg is inconclusive, not
  passed. Each *ay*-set source is drafted under both word-order settings of ρ (D31), and the
  inversion rate under each setting is reported.
- **ρ in training (D31):** politeness (polite / plain / neutral) and word order (inverted /
  predicate-first), both labelled automatically from the reference; a labelled pair is marked with
  probability 0.5, a neutral pair with a random setting at the same probability, redrawn each epoch.
- **Drafter architecture (D32):** the checks above judge a dense drafter. The same checks are then
  run on a small MoE sparse-upcycled from it and reported beside the gate, not counted in it.
- **Diagnostics, not pass conditions:** the probe on the drafter's z_t against reference labels; the
  drafter-minus-z_m gap; a probe on encodings of the English sides (how much the English predicts each
  choice).
- **Labels for decoded drafts:** the automatic labellers are extended before the run to *ho/oho* and
  to contracted *'y* forms (*siya'y*, *ito'y*); *Opo* used as "yes" becomes *Oo* in a plain draft. The
  probe sets `t1-probes-v1` keep their original labels (about 0.5% noise from contracted forms,
  documented).

Outcomes:
- all pass: proceed to tranche 2;
- z_m > 0.65: a single draft may suffice, so simplify the design (the z_m check measures linear
  readability of the form, not its absence);
- reference z_t passes but drafter check (ii) fails: regression averaging (LCM) has materialised, so
  revise the drafter (diffusion or quantised) before tranche 2; (iii) alone fails: revise the
  conditioning on ρ; (i) or (iv) fails: diagnose before any architecture change;
- a leg is inconclusive (weak yardstick, too few drafts, failed positive control): it is not counted as
  passed; one retest of a revised drafter is allowed on this probe set, a second needs fresh probe data
  (QED is the reserve);
- sentence space fails: stop and rethink the substrate (e.g. few-vector drafts);
- a confidence interval straddles a threshold: the tranche margin buys one more seed or a larger
  probe set, and tranche 2 does not start until it is resolved.

Rationale for these numbers (to be confirmed by Arjhine Ty):
- **5% retrieval error.** It leaves room above the low single-digit error rates SONAR-class spaces
  reach on high-resource pairs, while catching a space that has failed to align. [inference; we have
  not measured en–fil]
- **80% of MADLAD's chrF++.** The bottleneck is expected to cost quality; 80% is the floor below
  which critique gains on top would not be worth reporting. [judgement]
- **The 0.65 / 0.75 / 0.85 ladder.** It separates "mostly absent" from "reliably present" by at least
  10 points at every step, so the gap test is not decided by noise. [judgement]

## 8. Nulls and controls

- **Null:** CAMOE = B1 (iso-FLOP MoE) on the primary metric.
- **Negative controls:** random critic (B5); critic that never triggers repasses (X1); random-direction reroute (B11).

## 9. Measurement

- Metrics and their validity for Philippine languages: pending `research/diligence/A6-metric-validity.md`.
- Critic-only measurement: agreement with human error labels, calibration, and collapse monitoring (A4).
- Primary metric: **[ARJHINE, after A6]** · Secondary metrics: **[after A6]**

## 10. Design

- **Substrate:** **[ARJHINE, item 1.1]**. Proposed:
  - Path B (mT5/ByT5) for pipeline debugging;
  - Path A (MADLAD-400 + SONAR recipe) for main runs.
  - See `ideas/03-sentence-space-substrate.md`.
- **Unit of "the painting":** **[ARJHINE, item 1.2]**
- **Languages, wave 1:** **[ARJHINE]**. Candidates are those with data and model support, e.g. Tagalog, Cebuano, Ilocano.
- **Scales:** at least two model sizes, to check that the trend holds. **[after compute estimate]**
- **Seeds:** **[fix number, e.g. 3–5 per configuration]**
- **Data splits and contamination check:** pending `research/diligence/A5-contamination.md`.

## 11. Analysis plan

- Report per language, never only a pooled average.
- Report confidence intervals via bootstrap over test sentences, and across seeds.
- Paired significance tests against each baseline, with multiple-comparison correction across languages and baselines.
- Label every analysis confirmatory (planned here) or exploratory (everything else).

## 12. Compute accounting

- Report FLOPs per input for CAMOE: average and worst case. The average is a ratio of sums per
  stage and per translation direction (D14, kill criteria in §7).
- Report GPU-hours per run.
- The compute estimate for the research proposal is in `pitch/compute/ESTIMATE.md`.

## 13. Data, code, provenance

- Papers: `research/papers/`.
- Licenses: `research/licenses/`.
- Runs: `experiments/` conventions.
- Datasets: `data/` (registry to be created with the first dataset).

## 14. AI and tool assistance

- Much of the code and documentation was written with AI assistance (Anthropic's Claude).
- Literature search: Papers with Code CLI.
- Disclosure must follow the target venue's policy.
- Every AI-drafted claim is verified against primary sources before it goes in the paper.

## 15. Deviations and amendments

For each: date · section · original plan · change and reason · who decided · whether results were
already known · expected impact · whether the original analysis is still reported.

## 16. Sign-off

- Accountable investigator: Arjhine Ty · date: **[on freeze]**
- Domain review (Philippine languages): **[name]**
- Methods review: **[name]**
