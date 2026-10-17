# Data plan: what datasets DiaGrad needs, and why

Created 2026-09-24 so the reasons are on record. **Status: draft.** The final list gets
fixed once items 1–3 of `ideas/01-question-log.md` are refined; until then every entry says *why*
it exists and which question it serves, so an entry can be dropped if that reason disappears.

Labels: **[decided]** follows from a decision already logged · **[inferred]** an AI-assisted reading of
the current design, to be confirmed · **[open]** depends on a question not yet answered.

## Context

- Filipino languages first, Japanese later; coding and other domains possible (item 8).
- Start with languages existing resources already support (e.g. SONAR text: Tagalog, Cebuano,
  Ilocano, Pangasinan, Waray). Gather data for the others over time with project partners (item 7).
- Multi-year project: datasets arrive in waves, and each wave must be recorded well enough that
  results stay comparable across years.

## Dataset types and the reason for each

| # | Dataset | Why we need it | Serves | Status |
|---|---|---|---|---|
| D1 | **Error study set**: outputs of existing models translating Philippine languages, with errors labelled by category (meaning, grammar/focus, politeness/register, dialect drift, …) | We don't yet know which errors matter most. This study decides what the critic should target, and it motivates the paper | Item 1 (open question), item 7 | [decided]: agreed to research errors first |
| D2 | **Monolingual text per language** | Pretraining the base model. Engram-style memory learns from the N-gram statistics of each language, so thin data means a weak memory for that language | Items 5, 8 | [inferred] |
| D3 | **Parallel text** (Philippine language ↔ English / Tagalog; later ↔ Japanese) | Translation is the first test task, and pairs are needed to train and measure it | Items 7, 8 | [inferred] |
| D4 | **Critic training data**: translations judged good/bad, ideally with named error categories and corrected versions | The critic needs a source for "bad" (item 3). Named categories make its judgments readable, not black magic (D1 constraint 4) | Items 1, 3 | [open]: depends on how the critic is trained |
| D5 | **Held-out evaluation sets**, verified by native speakers, per language | Tests whether CAMOE works. Must never touch training, or results are meaningless | Item 7 | [decided]: evaluation is required |
| D6 | **Variety and register metadata**: language/dialect label, region, register (e.g. *po*/*opo*), code-switching (Taglish, Bislish) | Needed to check whether the critic catches dialect drift and register errors, and to report results per variety rather than as one blended number | Items 1, 7 | [inferred] |
| D7 | **Coding data** (later) | Tests whether critique generalises beyond translation | Item 8 | [open] |

## Diligence checklist (applies to every dataset)

**Provenance.** Same standard as papers (`research/papers/REFERENCES.md`):
- source, collector, collection date, version, license, file hashes, and every transformation applied;
- one record per dataset, kept in `data/registry/` (to create when the first dataset arrives).

**Rights and consent.**
- Confirm the license allows training *and* publishing results.
- For data from people: informed consent covering AI training.
- Philippine Data Privacy Act (RA 10173) for any personal information.
- For indigenous-community languages: the Indigenous Peoples' Rights Act (RA 8371) and free, prior and informed consent may apply.
- Get these checked by someone qualified; don't assume.

**Community and fairness.**
- Native-speaker involvement in collection and review.
- Fair pay for annotators.
- Credit to contributing communities.
- A plan for giving value back, such as releasing datasets or models to those communities where the terms allow.

**Quality.**
- Language-ID accuracy.
- Spelling and orthography variants (many Philippine languages have competing spellings).
- Deduplication.
- Agreement between annotators on error labels, measured and reported, not assumed.

**Separation.**
- Evaluation data (D5, and public benchmarks such as FilBench) is checked for overlap with training data before every run. This is called a **contamination check**.
- A test the model has already seen measures memory, not ability.

**Balance and reporting.**
- Record how much data each language and variety has.
- Report results per language, so strong Tagalog numbers don't hide weak Waray ones.

**Documentation.** A datasheet per dataset: what it is, why it was collected, who is in it, known gaps.

## To decide once the idea is refined

- [ ] Which of D1–D7 are actually required for the first paper, and which wait for the model phase
- [ ] Minimum size per dataset for the first experiment
- [ ] Which languages are in wave 1
- [ ] Who reviews rights/consent, and whether a university ethics review applies
