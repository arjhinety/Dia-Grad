# Run <RUN_ID>

## Before (fill in and commit before starting)

- **Type:** exploratory / confirmatory
- **Question / hypothesis:** (link the preregistration section, e.g. `prereg/PREREGISTRATION.md#H1`)
- **Expected result:**
- **Kill criterion for this run:**
- **Config:** `experiments/configs/<file>` @ commit `<sha>`
- **Seed(s):**
- **Data:** dataset registry ID(s), split, sha256 of input files
- **Contamination check:** passed / not applicable (reason)
- **Base model / checkpoint:** name, version, license (see `research/licenses/LICENSES.md`)
- **Environment:** GPU type × count, driver, key library versions
- **Planned compute:** GPU-hours; FLOPs estimate

## During

- Start time (UTC):
- Notable events (divergence, restarts, config changes with reasons):
- Collapse monitoring (critic accept/reject rate, repass distribution), for CAMOE runs:

## After

- End time (UTC), actual GPU-hours:
- Compute used per input: average / worst case
- **Results:** metrics with confidence intervals; link `metrics.jsonl`
- **Against expectation:** matched / differed / inconclusive, and how
- **What we learned:**
- **Artifacts:** paths and sha256 (not committed)
- **Follow-ups:**
