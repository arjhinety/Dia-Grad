# DiaGrad roadmap

DiaGrad proceeds in tranches, each behind a gate. A later tranche starts only if the earlier gate
passes; every gate has a pre-stated consequence if it fails.

## Done

- Idea refinement: the critic judges an internal whole-sentence draft (D1–D2); posterior routing with
  accept / repass / reroute, the reroute strength learned by RL (D5, D9, D9a, D13).
- Proposal, one-page brief and study guides; two rounds of pre-circulation review (D7, D8, D10).
- Paper library with provenance (171 papers: version, licence, hash) and a logged literature search
  (151 queries).
- Licence audit of candidate models, code and datasets; diligence reports A4–A7.
- Tranche-1 setup on the GB10: pinned container, sentence-space code and tests (D16).
- Held-out sets chosen and contamination-checked: SMOL gate test, MASSIVE dev (D19, D20).
- Training data: 12 sources registered, Mix 3 chosen and measured, about 305M raw MADLAD tokens before
  filtering (D17, D22–D24).

## Tranche 1 — feasibility gate (in progress)

Can a permissive, SONAR-style single-vector sentence space on MADLAD-400-3B carry what the design
needs? Pass rule in the [README](README.md#tranche-1-the-feasibility-gate).

- [x] Teacher comparison: permissive teachers against NLLB-3.3B (D25, D26): NLLB not ahead by more than 5 chrF++; D25 stands
- [ ] Filter calibration on the hand-labelled NLLB sample (D18; waits for labellers)
- [ ] Probe data for *po/opo* and *ay*-inversion, with hand labels
- [x] Monolingual text for the denoising term (D28): slice `t1-mono-slice-v1`, 507M tokens; SMOL 0/754 flagged
- [ ] Freeze the preregistration
- [ ] Train the sentence space; run the gate

## E1 — English→Filipino MT error study

Measure how many errors are about meaning and how many about surface form. It decides which critic
is built first (D2, D3).

- [x] Protocol drafted; WMT24++ en-fil_PH registered
- [ ] Native-speaker annotators recruited; 60-segment pilot; about 2,400 error-span annotations

## Later, only if each gate passes

- **Tranche 2** (about 800–1,600 H100-hours): small prototypes and every baseline. Stop or narrow the
  claim if the critic does not beat a confidence-triggered repass and an iso-FLOP MoE; drop the
  MoE-specific claim if reroute does not beat both a plain repass and a random-direction reroute.
- **Tranche 3** (about 500–1,000 H100-hours): one scale check.
- Japanese after Filipino; other Philippine languages as data allows.
