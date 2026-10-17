# Folder map

Every tracked folder and its key files. The landing page is the [README](../README.md).

| Path | What it holds |
|---|---|
| [`decisions/DECISIONS.md`](../decisions/DECISIONS.md) | The project's design decisions: what was decided, why, and the evidence |
| [`data/DATA-PLAN.md`](../data/DATA-PLAN.md) | Which datasets we need and **why**, plus the diligence checklist (rights, consent, provenance, contamination) |
| [`research/papers/`](../research/papers/) | Reference library: `REFERENCES.md`, `references.bib`, `registry.json`, version-pinned PDFs, full text in `txt/` (search this), catalog copies in `md/` (may be truncated) |
| [`studies/E1-error-study/`](../studies/E1-error-study/) | Filipino MT error study: `PROTOCOL.md`, append-only `LOG.md`, phase-0 evidence, data |
| [`data/registry/`](../data/registry/) | One provenance record per dataset (source, revision, sha256, license) |
| [`research/tools/build_provenance.py`](../research/tools/build_provenance.py) | Rebuilds reference records from `research/papers/seed.json` |
| [`research/search/`](../research/search/) | Recorded search protocol: `queries.json`, `screening.json`, append-only `log.jsonl`, `SEARCH-LOG.md` (tool: `research/tools/search_log.py`) |
| [`research/licenses/`](../research/licenses/) | License audit of every candidate model, code base and dataset (tool: `research/tools/license_audit.py`) |
| [`research/diligence/`](../research/diligence/) | A4 baselines/ablations, A5 contamination, A6 metric validity |
| [`prereg/PREREGISTRATION.md`](../prereg/PREREGISTRATION.md) | Preregistration draft, with **[ARJHINE]** blanks |
| [`experiments/`](../experiments/) | Run conventions, run-record template, run index (runs listed in `experiments/runs/INDEX.md`) |
| [`src/diagrad/`](../src/diagrad/) | Tranche-1 code: sentence space, gate probes, contamination check, teacher comparison, dataset-registry validator |
| [`tests/`](../tests/) | Tests for `src/` (CPU tests run in CI; GPU and tokenizer tests need the container) |
| [`env/`](../env/) | Pinned container for the GB10 (`Dockerfile`, `requirements.lock`) |
| [`data/mix/`](../data/mix/) | Training-mix measurements (tokens, overlap with NLLB) and their scripts |
| [`data/heldout/`](../data/heldout/) | Text-free summaries of the held-out sets and their contamination check |
| [`scripts/`](../scripts/) | Repository checks (publication hygiene) |
| [`docs/INCIDENT_LOG.md`](INCIDENT_LOG.md) | Incidents that affected runs or claims |
