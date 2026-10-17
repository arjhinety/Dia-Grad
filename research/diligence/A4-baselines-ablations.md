# A4 · Candidate baselines and ablations (draft, 2026-09-24)

**Status: candidates only.** The final set is fixed in the preregistration once item 1 is refined.
Each entry states the question it answers, because a comparison without a question is just a number.
Paper IDs refer to `research/papers/REFERENCES.md`.

## Why these exist, in one paragraph

CAMOE adds a critic, repasses, and extra compute at the same time. If CAMOE beats a plain model, any
of those three could be the reason. Baselines hold two of them fixed and vary the third, so that the
improvement can be attributed to the **critic's judgment**, which is the paper's claim.

## Baselines

| ID | Baseline | Question it answers | Motivated by |
|---|---|---|---|
| B0 | Same architecture, critic removed | Does anything we added help at all? | — |
| B1 | Plain MoE given CAMOE's **average** extra compute (more active experts or layers) | Is the gain just extra compute? (iso-FLOP) | Engram (2601.07372) and adaptive loops (2603.08391) report iso-FLOP / iso-parameter comparisons |
| B2 | Plain MoE given CAMOE's **worst-case** compute | Same, at the least favourable accounting | DILIGENCE T3 (variable compute) |
| B3 | **Confidence-triggered repass**: same repass mechanism, decided by the model's own confidence instead of the critic | Is the critic better than "am I confident?" **The critic must beat this.** | Halting gates (2607.20519); P(IK) calibration (2207.05221) |
| B4 | **Fixed repasses**: always N passes, no decision | Does *deciding* when to repass matter? | Encode-Think-Decode (2510.07358); recurrent depth (2502.05171) |
| B5 | **Random repasses** at the critic's observed rate | Do the critic's *choices* matter, or only how often it repasses? | — |
| B6 | **Output-level critique**: write the full translation, then refine or rerank it with a quality model | Does internal critique beat critique of written text? (option b vs c, item 6) | Quality-aware decoding (2205.00978); iterative refinement (2306.03856) |
| B7 | QE-guided decoding at matched compute | Same question, token-level external critic | 2502.08561 |
| B8 | Energy-based refinement without named categories | Does the critic need to be separate, or is an energy score enough? | EBT (2507.02092) |
| B9 | Post-hoc hidden-state failure predictor used as the critic | Does an *architectural*, trained-in critic beat a probe attached afterwards? | Gnosis (2512.20578) |
| B10 | Sentence-space model with no critic | Isolates the critic from the sentence-space substrate | Large Concept Models (2412.08821) |
| B11 | **Random-direction reroute, effect-matched** (D10, D12): same critic, same policy decisions and layers, but zero-mean Gaussian noise on the router's selection scores instead of the push away from the failed experts, scaled per layer (calibrated on held-out sentences) so the same share of tokens get a different expert set as under REROUTE | Does REROUTE help because the critique *directs* the change of experts, or only because any routing change adds diversity? REROUTE must beat this as well as REPASS | ESRL (2609.13058): perturbing routing alters outputs much like raising temperature; test-time re-routing R2-T2 (2502.20395), C3PO (2504.07964) |
| R1 | MADLAD-400 MT as released; a strong open LLM | Reference points for absolute quality (not compute-matched; reported as context only) | MADLAD-400 (2309.04662) |

**Note on B1/B2 if layer caching is used** (an idea under consideration, not a decision). Caching early layers would make a repass cost less than a full pass.
If DiaGrad uses it, the iso-FLOP baselines' **average and worst-case extra compute must be computed
from the cached implementation's actual FLOPs and its measured latency**, not from the full-pass
figure (+30%) in `pitch/compute/estimate.py`. Otherwise the baselines would get the wrong budget,
and the comparison would no longer be at equal compute.

## Ablations (remove or change one part at a time)

| ID | Change | Question | Links |
|---|---|---|---|
| X1 | Critic scores but never triggers a repass | Does training the critic help as an auxiliary signal on its own? | item 3 |
| X2 | Single score vs named error categories | Do named categories cost quality? Do they help? | "not black magic" |
| X3 | Critic trained jointly vs trained after the base model | Does joint training distort the model? | 2607.20519 warning |
| X4 | Critic sees draft only vs draft + source | Is the critic judging faithfulness or just fluency? | A6 metric review |
| X5 | On rejection: refine draft / redraft / consult another expert | Which recovery action works? | item 1.4, item 2 |
| X6 | Max repasses 1 / 2 / 4 | Where do returns stop? | item 4 |
| X7 | With vs without Engram memory | Do memory and critique interact? | 2601.07372, 2603.08391 |
| X8 | Critic training signal: reference-based / QE model / MQM labels | Which signal teaches "bad" best? | item 3; licensing constraint below |

## Measuring the critic itself (not a baseline, but required)

- Agreement with human error labels: precision, recall, and per-category agreement (data plan D1/D4).
- Calibration: does a confident rejection actually mean a worse draft?
- Collapse monitoring: accept/reject rates and repass distribution over training.

## Licensing constraint on critic training signals

The license audit (`research/licenses/LICENSES.md`) found:
- **CometKiwi and xCOMET are CC-BY-NC-SA** (non-commercial). Using them to *evaluate* is fine. Using
  them to *train the critic* (X8) could carry non-commercial terms into the model.
- COMET-22 (wmt22-comet-da) and MetricX-24 are **Apache-2.0**: safe as training signals.
