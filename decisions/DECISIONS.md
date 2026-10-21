# Design decisions

This document records the design decisions of DiaGrad, made by Arjhine Ty as project lead. Each entry
states what was decided, the reasoning, the evidence it rests on, and what would lead to it being
revisited. Numbers follow the project's internal record, so references such as "D22" elsewhere in the
repository resolve here. Administrative decisions (D3 work priorities, D4 naming and framing, D11 GPU
pricing, D27 publication of this repository) are not reproduced.

Evidence labels: **[paper]** stated in the cited work (arXiv identifier; entries are in
`research/papers/references.bib` unless marked); **[measured]** our own measurement, with the file
that holds it; **[source-stated]** a dataset card, licence or API; **[inference]** reasoning from the
evidence; **[judgement]** a choice that no cited work settles. Decisions D1–D14 predate the rule that
every decision carries an evidence entry; their reasoning is summarised from the design record.

---

## Part I. The method

### D1. The critic judges an internal draft of the whole sentence

**Decision (2026-09-24).** The critic judges a latent, not-yet-written draft of a whole sentence, once
the draft is complete. Two alternatives were considered and set aside: judging a single token's hidden
state inside the layers (kept as a possible ablation), and judging the fully generated output (kept as
a baseline). Critique written out as visible reasoning text is excluded.

**Requirements.** The critic decides *whether* another internal pass is needed rather than forcing
one every time; its judgements must be inspectable; and it is a first-class component alongside the
router, intended as the core contribution.

**Revisit if** prior work shows that internal whole-sentence drafting is impractical at small scale.

### D2. Two drafts and two critics, in stages

**Decision (2026-09-24).** The model forms two internal drafts: a language-neutral meaning draft
z_m, judged by a meaning critic, and, once that is accepted, a target-language draft z_t, judged by a
target critic, before any text is written.

**Rationale.** A meaning vector trained to pull translations together (SONAR's MSE term) can expose
meaning errors (mistranslation, omission, addition, role errors) but probably not choices made while
writing the target sentence: *po/opo* politeness, *ay*-inversion, Taglish register, spelling, dialect
drift [inference from the training objective of 2308.11466; not yet measured]. The tranche-1 gate
measures it.

**Order of work.** Which critic is built first is decided by a Filipino MT error study (E1,
`studies/E1-error-study/`), so that the choice rests on measured error statistics. If one error family
proves negligible, the design drops to a single critic.

### D5. The critique router is trained by reinforcement learning

**Decision (2026-09-24).** The critique router, which decides what to do after the critic's judgement,
is trained by reinforcement learning, with a small imitation-learning subset (oracle distillation:
each action tried offline, the policy trained to copy the best) as a comparison and fallback. Critics
(judges) and router (decider) remain separate modules. The action space is ACCEPT, REPASS and REROUTE
(D7); BLEND is deferred.

### D6. Posterior routing

**Decision (2026-09-24).** The contribution is framed as *posterior routing*. A standard MoE router is
*prior*: it assigns experts before any output exists. The critique router is *posterior*: it acts
after an internal draft exists and has been judged, choosing to accept it, send it back for another
internal pass, or reroute it to other experts. The claim to be tested is that posterior routing beats
spending the same extra compute and beats the model's own confidence, with Filipino translation as the
first testbed. The term was not found in our literature searches; this is not a novelty claim.

### D7. REROUTE belongs in the first paper; compute is requested in gated tranches

**Decision (2026-09-24).**
1. REROUTE is part of the first paper. Without it the method reduces to critic-gated halting; the
   MoE-specific claim is that REROUTE beats REPASS at equal compute.
2. Compute is requested as a small first tranche (build the sentence space; test cheaply whether the
   meaning draft drops surface detail), with later tranches each gated on the previous result.
3. An Engram-style memory component stays in the architecture; its role is an open design question,
   tested by ablation.
4. Critic-training recipes based on frontier-LLM teacher labels or CCAligned are not adopted until
   each source passes the licence audit.

### D8. The target drafter is a small MoE; the reward and the training of critique inputs

**Decision (2026-09-24).**
1. The target drafter is a small MoE with its own prior router, so that REROUTE is defined in both
   stages and the MoE-specific test also covers surface errors. From tranche 2 (D32); the tranche-1 gate uses a dense drafter.
2. The router's reward uses Q = −MetricX-24 (D14), with a human-label check, plus a comparison router
   rewarded by chrF++. A composite of chrF++ minus the critics' own penalties was rejected: the router
   would be graded by the critics it acts on.
3. Modules that consume the critique are trained only with the second pass's translation loss, with
   the first pass detached, and never on the reward; reinforcement-learning rollouts are therefore
   forward-only for them. The risk that a regression drafter averages alternatives is stated and
   tested in tranche 1 (D30).

### D9. The REROUTE bias changes which experts are selected, not how outputs are weighted

**Decision (2026-09-24).** As in DeepSeek's auxiliary-loss-free balancing, where "the bias term is
only used for routing" [paper: deepseekai2024deepseeka, §2.1.2], gating weights come from the
unbiased router scores. In router steering, larger pushes hurt, which the authors attribute to
disrupting the aggregation weights [paper: bandarkar2025multilingual, §6]; a selection-only bias
avoids that. Biasing both selection and weights is kept as an ablation.

### D9a. The REROUTE push strength is learned by reinforcement learning

**Decision (2026-09-24).** A selection-only bias acts through the top-k choice, which has no gradient,
so the push strength cannot be trained by the translation loss. Of three options (a fixed rule, a
straight-through gradient, reinforcement learning), the strength is learned by reinforcement learning
as part of the router's action.
1. Expert e in MoE layer l receives bias −β_l · u_le, where u_le is the share of the failed pass's
   tokens routed to e at l. The per-layer strengths β_l ∈ [0, β_max] are sampled from a squashed
   Gaussian whose mean is a learned projection of the critic output and the draft state, a
   continuous-action policy of the kind PPO uses [paper: schulman2017proximal].
2. No module that produces the first draft is trained on the reward, so the incentive argument holds:
   the push acts only after the first draft exists.
3. Ablations: learned against fixed strength; selection-only against selection-and-weights bias.

**Known costs [inference].** A continuous action adds variance to the policy gradient, and the MoE
routing mismatch between rollout and training now touches the router's own action, so both must use
the same routing implementation [paper: ma2025stabilizing].

### D10. Test-time re-routing as related work; provisional tranche-1 thresholds

**Decision (2026-10-02).**
1. Test-time re-routing methods are cited and compared: R2-T2 (2502.20395), C3PO (2504.07964),
   Dynamic Experts Search (2509.22572), Counterfactual Routing (2604.14246) and ESRL (2609.13058).
   Their signal is neighbour success, expert counts or causal impact, not a critic's judgement of the
   model's own unwritten draft, and none learns an accept/redo/reroute policy.
2. A random-direction reroute baseline is added, answering ESRL's confound: does REROUTE help because
   the critique directs the change, or because any routing change adds diversity? Its mechanism was
   revised in D12.
3. Provisional numeric thresholds for the tranche-1 feasibility gate are stated in advance
   (`prereg/PREREGISTRATION.md` §7a). They may be revised before tranche 1 starts, never after.

### D12. The random-direction reroute is matched on effect, not on strength

**Decision (2026-10-02).** Applying the same strengths to a random permutation of the failed pass's
expert usage rarely changes the selected experts: the bias only pushes experts down, and a shuffle
puts most of the push on experts that were not selected (in a four-expert example, 7 of 24 shuffles
changed the selection) [arithmetic]. Such a control behaves like REPASS, and REROUTE would beat it for
the wrong reason. The control therefore adds zero-mean Gaussian noise to the selection scores, with
the per-layer scale calibrated on held-out sentences so that the share of tokens whose selected expert
set changes equals the directed REROUTE's share. The question becomes: at the same amount of expert
change, does changing away from the failed experts, with critique-chosen strengths, beat changing at
random? Both change rates are reported.

### D13. Shared stage weights learn from both passes; the first draft is detached

**Decision (2026-10-04).** A stage with a repass is trained on the translation loss of its first-draft
output plus that of its second-pass output, and both reach the shared weights. In the second pass the
first pass's output, and the critic output computed from it, are constants. The same structure appears
in SimSiam [paper: 2011.10566]: a shared encoder with a stop-gradient on one branch still trains through
the other.

The detach removes the *direct* incentive to write first drafts that are easy to fix, not indirect
effects through the shared weights. First-draft quality is therefore tracked during training; a decline
would reopen the choice (training the shared weights on the first pass only, or a separate first-pass
loss weight). Only the critique router is trained on the reward.

### D14. Comparing the two reward variants at matched extra compute

**Decision (2026-10-07).** MetricX-24 is an error score on 0–25 [paper: 2410.03983] and chrF++ runs
0–100, so one shared compute penalty λ would price compute differently for the two routers, and a
quality difference would mix "which reward is better" with "which router spent more" [inference].
1. Q = −MetricX-24, so that higher is better.
2. One λ per stage and translation direction, each set on a pilot of held-out *training-side*
   sentences so that both routers reach the same compute targets: stage 1 at 0.05, 0.15 and 0.30 of a
   full pass's FLOPs; stage 2 at 1.0 redo per sentence. λ is never negative; at most 2 extra passes
   per stage. Calibrating exit thresholds on a held-apart set follows CALM [paper: 2207.07061]; that
   a penalty weight can be searched the same way is our inference.
3. "Extra compute" is average extra FLOPs per sentence relative to one full pass, computed as a ratio
   of sums per stage and direction; worst case and latency are reported beside it.
4. The routers are compared only on evidence neither was rewarded on: native speakers' error-span
   labels, and language identification for drift. Each router's own metric is diagnostic.
5. A full run that misses its compute target is recalibrated and rerun once; if it misses again, the
   comparison is made at the measured levels and the mismatch reported.
6. Human evaluation labels sentences shown in their paragraph. Baselines are compared on native
   speakers' labels at the middle compute level (C₁ ≈ 0.15); the router's curve across all three
   levels is reported, with automatic scores for baselines at the other levels as diagnostics only.

**Supporting practice.** Comparing adaptive-compute methods along quality–compute curves is standard
[paper: 2207.07061]; halting behaviour is sensitive to the compute penalty [paper: 1603.08983].

---

## Part II. Tranche 1: data, evaluation and infrastructure

### D15. Initial research may train on non-commercially licensed datasets

**Decision (2026-10-07).** Tranche-1 and other initial research runs may train on datasets licensed for
research but not commercial use. Licences are recorded for every dataset, and terms that forbid
research use, limit redistribution or gate access are followed. Non-commercial *models* (SONAR, NLLB
weights) and non-commercial metrics as *training signals* (CometKiwi, xCOMET) remain excluded,
including as generators of training data. Every artefact trained on such data is labelled
`research-only` and is never distilled into a commercially used model; a permissive retrain is a
separate step.

**Rationale.** The tranche-1 question does not depend on commercial rights to the data, while the
largest English–Tagalog source (NLLB's mined bitext) is ODC-By packaging over unlicensed web text
[source-stated: allenai/nllb card]. **Revisit if** the tranche-1 result can be reproduced only with
non-commercial data, in which case a permissive encoder would not follow.

### D16. Tranche-1 work runs on one GB10 workstation

**Decision (2026-10-08).** All tranche-1 work runs on an NVIDIA GB10 workstation; whether the
full-size MADLAD-400-3B run moves to H100s is decided before that run. Measured throughput: MADLAD-3B
full recipe about 470 tokens/s untuned (55 GB peak), mT5-base about 3,200 tokens/s, bf16 matrix multiply
98 TFLOP/s [measured: `experiments/T1-SETUP.md`].

### D17. First training pairs: the top-ranked NLLB en-tl pairs

**Decision (2026-10-08).** The first learning runs use NLLB en-tl, sorted by LASER3 score, top slice of
about 1M pairs; web text without a licence may be used for research runs, labelled `research-only`.

**Evidence.** NLLB mined about 33M en-tl pairs and adding them raised tl→en BLEU [paper: 2207.04672,
Table 13]; top-ranked slices of web-mined corpora train better models than random or bottom slices
[paper: 2402.07446, §6]. Against: LASER favours machine-translated and multi-way-parallel text
[paper: 2401.05749, §4–5], and a 100-pair sample showed machine-like pairs near the top [measured].
**Revisit if** the labelled sample (D18) shows the top slice is mostly misaligned or not Filipino.

### D18. The training sample is labelled on two questions by two labellers

**Decision (2026-10-08).** Each sampled pair is labelled on two questions rather than one quality
label: meaning against the English (same / slightly off / different) and the Filipino on its own
(natural / stiff / broken / not Filipino). The same 100 pairs are labelled independently by two fluent
speakers.

**Rationale.** A wrong meaning and machine-sounding Filipino are different defects with different
remedies (stricter alignment filtering against adding human-written sources); one label would hide
which is needed. The only en-tl audit likewise separates wrong translation, wrong language and
non-language [paper: 2103.12028, Table 11]. Two labellers make agreement measurable. **Revisit if**
agreement is low on either question.

### D19. Held-out sets: SMOL is the gate test, MASSIVE dev the development set

**Decision (2026-10-08).**
1. Gate test: all 754 SMOL SmolSent en–fil pairs (professional translation, CC-BY-4.0, released 2025)
   [source-stated; paper: 2502.12301], opened only for the MADLAD baseline and the gate evaluation.
2. Development set: MASSIVE 1.1 tl-PH dev, minus pairs found in NLLB; the MASSIVE test split is a
   labelled diagnostic.

**Rationale.** MASSIVE is localised rather than translated (entities are swapped, e.g. "California"
becomes "Pangasinan"), which breaks meaning equivalence for retrieval [measured: inspection]. An
exact-match scan found 0 of 754 SMOL sentences in NLLB [measured: `data/heldout/manifest.json`].
Precision at a 5% retrieval error is about ±1.6 points with 754 pairs [arithmetic].

### D20. Contamination check; the gate is judged on SMOL's clean subset

**Decision (2026-10-08).** Every held-out item is checked against all tranche-1 training data
following the procedure in `research/diligence/A5-contamination.md` §3.2: exact match, and the
longest-match rule flagging an 8-word run (or a whole side shorter than 8 words), after normalisation
with and without diacritics; the 13-word rule is reported for comparison. The gate is judged on the
unflagged subset of SMOL, fixed before the baseline is run, with the full-set score beside it. If more
than 10% of SMOL is flagged, tranche 1 stops for a decision.

**Evidence.** Longest-match gives the best contamination signal and thresholds above 8 cause false
negatives [paper: 2411.03923, §1, §5]; GPT-3 introduced 13-gram clean-subset reporting [paper:
2005.14165, App. C]; a nearest-neighbour retrieval proxy explains much of the variance in extremely
low-resource MT scores [paper: 2603.25222, §3.3]. **Measured** against all of NLLB en-tl: SMOL 15/754
flagged (2.0%), MASSIVE dev 246/1,963, MASSIVE test 354/2,862, mostly through short commands
[measured: `data/heldout/contamination-nllb-2026-10-08.json`].

### D21. Provenance and attribution carry over to any published dataset

**Decision (2026-10-17).** If the normalised training data is published, every row keeps its
provenance (source corpus, version, original identifier or URL, licence), and every source's
attribution terms are honoured. Which sources may be redistributed at all, and how held-out text is
kept out, is settled before any publication. ODC-By requires attribution and CC BY-SA share-alike
[source-stated]; a row that cannot be traced cannot meet either.

### D22. Tranche-1 training mix: NLLB core plus OPUS corpora

**Decision (2026-10-17).** NLLB en-tl top ≈3.5M pairs, plus CCMatrix v1, OpenSubtitles v2024,
ParaCrawl v9, WikiMatrix v1, bible-uedin v1, eBible `tglulb`, QED v2.0a (research-only) and Global
Voices v2018q4, deduplicated against NLLB and each other, targeting 200–250M tokens. A second-opinion
similarity filter (LaBSE or Bicleaner AI) is applied to the NLLB part, calibrated on the labelled
sample. Excluded: CCAligned, MaLA copies (lost provenance), JW300 (rights holder refused) and
evaluation sets. Back-translation with MADLAD is held in reserve.

**Evidence, for filtering hard.** Re-filtering the same NLLB release with LaBSE ≥ 0.80 dropped 76% of
pairs and improved chrF++ [paper: 2305.16307, §4.3]; strict classifier filtering won for African
languages [paper: 2210.10692, §6.2]. **Against filtering too hard:** dropping a low-score band hurt when
pools were small [paper: 2111.06787, Table 2]; pretrained models are more robust to noise [paper:
2402.07446, §7]. **Why the extra corpora:** subtitles add conversational Filipino and *po/opo*, rare
at the top of NLLB (0.3–0.5%) [measured]; CCAligned was 13% correct in the only en-tl audit [paper:
2103.12028, Table 11]. **Revisit if** the OPUS corpora prove mostly duplicates of NLLB, or the filter
removes most pairs the labellers judge good.

### D23. Corpus sizes are measured on the files themselves

**Decision (2026-10-17).** Token yield and overlap are measured on the downloaded corpora, not inferred
from OPUS word counts, since OPUS reports whitespace tokens and our MADLAD tokens per pair differ by
source (NLLB 50, ParaCrawl 83, eBible 75) [measured]. Corpora not reachable from the workstation are
downloaded on a separate machine and checked against sha256 and pair counts on arrival.

### D24. A schema-checked record for every dataset

**Decision (2026-10-17).** Every source has one record (`data/registry/`) with an immutable revision,
per-file sha256, the quoted licence, redistribution status with its basis, attribution fields, text
origin (human, mined, machine-translated and by which model), and allowed and forbidden uses. A
screening log keeps rejected candidates with their reasons, in the manner of a PRISMA flow; normalised
datasets carry per-row provenance columns (`data/ROW-PROVENANCE.md`); a validator reports what it
examined. The scheme is adapted from the OpenGrad project. Decisions about data can only be checked
later if each source is pinned to exact bytes and terms [inference].

### D25. No SONAR or NLLB outputs in training data

**Decision (2026-10-17).** No text or embeddings generated by SONAR or NLLB (CC-BY-NC) enter any
training data, including research-only runs. They are allowed for evaluation and analysis only:
comparison rows, neighbour comparisons with SONAR's space, and reference translations of development
sentences. Selecting NLLB pairs by their LASER3 score is not generation and remains allowed.

**Rationale.** Training on these outputs would make a tranche-1 success partly a copy of the baseline
it is compared against [inference]. Published work does use NLLB outputs for synthetic data [paper:
2402.06619; 2508.08680; 2603.16606], but none argues for training on non-commercial outputs. MADLAD
reports its 10.7B model within 3.8 chrF of NLLB-54B on Flores-200 [paper: 2309.04662], so permissive
teachers may be close enough that the rule costs little. **Revisit if** NLLB-3.3B is far ahead of
every permissive teacher (D26).

### D26. Teacher comparison against NLLB-3.3B

**Decision (2026-10-17).** MADLAD-400 3B / 7B / 10B and Qwen3-14B / 32B (Apache-2.0) are compared with
NLLB-200-3.3B (evaluation only) on MASSIVE dev, never SMOL. If NLLB beats the best permissive model by
more than 5 chrF++ in both directions, with the 95% paired-bootstrap interval of the gap above 0, a
research-only exception is reconsidered; otherwise D25 stands. Naturalness and meaning are rated 0–2
by a blind LLM judge (gpt-6.1-sol), with hidden repeats; this is advisory, since no automatic judge is
validated for Filipino (`research/diligence/A6-metric-validity.md`).

**Rationale.** The three MADLAD sizes share training data, so they isolate scale [paper: 2309.04662,
§4.1]. The 5-point threshold sits between the gaps MADLAD's authors describe as "within" and "behind"
NLLB [inference]; no paper sets it [judgement]. Teacher choice changes the value of synthetic data,
with a Tagalog case study [paper: 2604.11290].

**Result (2026-10-17) [measured]** (`experiments/runs/20261017-teacher-compare-1/RUN.md`). The rule did
not trip: en→fil, NLLB leads MADLAD-7B by 4.76 [3.71, 5.84] chrF++; fil→en, every MADLAD model leads
NLLB. D25 stands. On en→fil, however, MADLAD is within 5 chrF++ of NLLB but rated clearly less natural
(1.00–1.14 against 1.58), so chrF++ alone does not choose an en→fil teacher; a naturalness check stays
part of teacher choice.

### D28. Monolingual text for the target encoder: text the base model has not seen

**Decision (2026-10-18).** The target encoder's denoising text comes from FineWeb-2 fil_Latn and
HPLT 2.0 cleaned tgl_Latn, merged and deduplicated by normalised paragraph, with every paragraph that
also occurs in MADLAD-400 fil (clean or noisy split) removed; FinePDFs fil_Latn is added whole. About
0.5B MADLAD tokens are sampled. A paragraph is removed if it shares an 8-word run with any held-out
item or contains a whole side of a SMOL test item; whole short MASSIVE sides do not remove paragraphs.

**Rationale.** The MADLAD MT models were trained partly on MADLAD-400 with a MASS-style denoising
objective [paper: 2309.04662, §4.1], close to the target encoder's mBART-style term [paper:
2001.08210]. Denoising text the base has already denoised would make part of what the encoder learns a
replay [inference]. Deduplication reduces verbatim memorisation about tenfold with equal or better
accuracy [paper: 2107.06499]. Against the filter: content kept by several independent pipelines tends
to be of higher quality [paper: 2512.18834]; for Basque, size and coverage mattered more than
cleanliness [paper: 2203.08111].

**Measurements [measured]** (`data/mix/measure-mono-2026-10-17.json`). FineWeb-2 and HPLT 2.0 hold
46.9M unique paragraphs, 23.7M of them in no MADLAD-400 split. A blind check of 100 removed against
100 kept paragraphs found the removed ones *lower* in quality (−0.65 [−0.86, −0.44] on 0–2) and
naturalness (−0.52 [−0.73, −0.30]), with the same Filipino share
(`experiments/runs/20261018-mono-filter-quality-1/RUN.md`). One- and two-word MASSIVE sides (e.g.
"wala") would have removed 11% of FinePDFs paragraphs with 3 genuine 8-word matches among 21,866
flags, hence the narrower removal rule.

**Result.** Slice `t1-mono-slice-v1`: 507,331,139 MADLAD tokens in 10,792,835 segments; SMOL 0/754
flagged (`data/heldout/contamination-t1-mono-slice-v1-2026-10-18.json`).

### D29. Probe data: held-back subtitle pairs, both classes from one source

**Decision (2026-10-19).** The *po/opo* and *ay*-inversion probe sets are drawn from OpenSubtitles
v2024 en-tl, positives and negatives alike, with negatives matched to positives by length, so that the
classes differ in the feature rather than in source. A pair is kept if MADLAD-400-3B's fil→en
translation of the Filipino side reaches a sentence-chrF threshold against the subtitle English; the
threshold was calibrated on 200 alignment labels (blind LLM judge) before any probe was run. Probe
pairs, and any training pair sharing a normalised side with one, are excluded from the training mix.
Whether the English carries a respect or address cue is recorded per pair.

**Rationale.** The drafter probe starts from the English, so each probe pair must be a translation.
Mined corpora contain many misaligned pairs [paper: 2103.12028, Table 11], and a blind alignment check
of 40 *po* pairs per source rated OpenSubtitles highest (1.60 of 2) and CCMatrix and NLLB lowest
(0.12, 0.30) [measured: `data/mix/measure-probe-sources-2026-10-19.json`].

**Result (2026-10-19) [measured]** (`data/probes/probes-v1-stats.json`). 1,000 pairs per class for
both features; threshold chrF 54.88; a blind check of 120 kept pairs found none unrelated. *po*
positives carry an English respect cue 4.8 times as often as negatives (247 against 51), leaving 753
cue-free positives for the meaning-draft comparison.

### D30. The drafter is scored on what it writes and on whether the register setting controls it

**Decision (2026-10-20).** The tranche-1 check that the target drafter delivers surface form no longer
scores a probe on the drafter's z_t against the *reference translation's* labels.

**Rationale.** The drafter sees only the English source (as z_m), the target language and the
register setting ρ. By the data-processing inequality, its output carries no more information about
the reference translator's choice than those inputs do. *ay*-inversion is largely a stylistic choice,
and 753 of 1,000 *po* positives carry no English cue, so a probe against reference labels would be
capped near chance for a good drafter and an averaging one alike [inference; the cap is to be measured
by a probe on encodings of the English sides].

**Replacement.** For *po*, each source is drafted with ρ = polite and ρ = plain, decoded and labelled;
ρ must switch *po* on and off. For *ay*, the decoded output must be well-formed and committed to one
order, and z_t must carry the form its own decoded text shows. Averaging is the failure the check
exists to catch: a regression model "generates their average in SONAR space … which may not correspond
to any relevant point" [paper: 2412.08821, §2.4.1], and the same work measures it by the distance a
vector moves when decoded and re-encoded. The reference-label probe is still reported as a diagnostic.

**Pass rule (2026-10-20).** Each measurement is also taken on reference z_t over the same sentences,
and each check uses the conservative end of a 95% bootstrap interval that resamples source sentences:
1. *Meaning*: decoded chrF++ under each register setting is at least 90% of that of decoded
   reference z_t, so a drafter cannot pass by producing a few fluent but unrelated sentences.
2. *No averaging*: the median and 90th-percentile distance a vector moves when decoded and re-encoded
   are at most 1.5 times those of reference z_t. Synthetic averages serve as a positive control; if
   they do not move clearly more than real vectors, the check is reported as inconclusive.
3. *Register control*: *po* appears in at least 70% of drafts with ρ = polite and at most 10% with
   ρ = plain, with a paired difference of at least 0.60. Because *po* is a clitic whose placement is
   constrained, a blind sample is also checked for grammatical placement and preserved meaning.
4. *Readable form*: a linear probe trained on reference z_t, applied to the drafter's z_t, reaches
   balanced accuracy of at least 0.75 against the labels of the drafter's own decoded text. Training
   the probe on reference vectors keeps it from simply reading the register setting.

A leg is inconclusive, never passed, if its yardstick is weak (decoded reference z_t keeps *po* in
fewer than 80% of *po* sentences) or if the drafter writes fewer than 500 sentences of either *ay*
form. *ay*-inversion is associated with formal or careful style rather than politeness, so a
politeness setting is not expected to steer it. The thresholds are a judgement; the round-trip
metric follows 2412.08821. The full rule is in `prereg/PREREGISTRATION.md` §7a.

### D31. The register setting in tranche 1: politeness and word order, derived from the reference

**Decision (2026-10-20).** During tranche-1 training, ρ has two settings, each derived automatically
from the Filipino reference of a training pair: politeness (polite when *po/opo/ho/oho* is present,
plain for second-person address without them, otherwise neutral) and word order (inverted when
*ay*-inversion is detected, otherwise predicate-first). A labelled pair carries its setting with
probability 0.5; a neutral pair carries a random setting with the same probability; marks are redrawn
each epoch.

**Rationale.** Target-side labels attached as side constraints to part of the training data controlled
German politeness in subtitle translation: with the constraint "polite", 1,728 of 2,000 outputs were
polite and 64 informal [paper: sennrich2016controlling, Table 2]. Marking only part of the data, and
marking neutral sentences at random, lets the model translate without a setting and ignore one that
does not apply; classifier-free guidance uses the same device of dropping the condition during
training [paper: 2207.12598, Algorithm 1]. *ay*-inversion is associated with formal or careful style
rather than politeness, so a politeness setting alone would not steer it, and inversion is rare
(3.1% of the subtitle pool). Without a word-order setting the drafter would seldom write inverted
sentences, and the *ay* leg of the drafter checks (D30) would likely be inconclusive.

**Alternatives considered.** A politeness setting only, which leaves the *ay* question unanswerable in
tranche 1. A formality setting taken from the source corpus, in the manner of domain tags
[paper: 1612.06140]; it would encode the corpus as well as formality, and the *ay* probe sentences are
all from subtitles, so a weak result could not be attributed to the drafter.

**Use in the checks.** Each *ay* probe source is drafted under both order settings. The inversion rate
under each setting is reported; it is not a pass condition, but if the setting does not take, the *ay*
leg remains inconclusive.

**Scope.** The order setting is a measurement device for tranche 1, not a register a user would
declare. The full system's register setting (formality and English–Filipino mix) is unchanged. The
label rules are checked by a language review before use [judgement for the extension to word order;
no published work controls word order this way].

### D32. A dense drafter for the tranche-1 gate, with an upcycled MoE reported beside it

**Decision (2026-10-21).** The drafter judged by the tranche-1 gate is a dense transformer. After
training, it is converted into a small MoE by sparse upcycling, in which each expert is initialised
from the trained dense feed-forward layer; the MoE is trained further and run through the same four
drafter checks, and its results are reported beside the gate rather than counted in it. The MoE
drafter of D8 applies from tranche 2 and starts from the upcycled model.

**Rationale.** The MoE drafter exists so that REROUTE is defined at the target stage, which is tested
in tranche 2; tranche 1 tests the representation. A dense drafter answers whether a drafted vector
carries surface form with fewer possible causes of failure, and matches the closest precedent: the
Base-LCM sentence-vector model is "a standard decoder-only Transformer surrounded with a PreNet and a
PostNet" [paper: 2412.08821, Fig. 4]. Sparse upcycling improved T5-Base and T5-Large over their dense
versions with about half of the original training cost [paper: 2212.05055], and its authors propose
it for the case where it is not known whether a dense or an MoE model is better. Small sparse models
are rarely unstable [paper: 2202.08906, §3]. An MoE does not by itself remove the averaging risk,
since the same inputs reach the same experts and yield the same vector; that risk is addressed by the
training loss.

**Alternatives considered.** A dense drafter alone, which defers the question of whether the gate
result transfers to the MoE drafter; and an MoE drafter as the gate, which adds routing settings and
failure causes that tranche 1 is not designed to measure.

**What would revise it.** The upcycled MoE failing a check that the dense drafter passes (the result
does not transfer), or clearly outperforming it on meaning or averaging (routing matters for the
representation question).
