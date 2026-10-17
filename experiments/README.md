# Experiments: conventions

These conventions were written *before* the first run so that every run, including failures, is
recorded the same way (DILIGENCE T1 #9). Runs so far: [`runs/INDEX.md`](runs/INDEX.md).

## Layout

```
experiments/
  configs/            one YAML/JSON file per run configuration (committed)
  runs/
    INDEX.md          one line per run, successes and failures alike (committed)
    <RUN_ID>/
      RUN.md          the run record, from templates/run-record.md (committed)
      metrics.jsonl   small metric logs (committed)
      artifacts/      checkpoints, large outputs (NOT committed; hashes go in RUN.md)
  templates/
    run-record.md
```

## Rules

1. **Run ID:** `YYYYMMDD-<short-slug>-<n>`, e.g. `20261015-pathB-bottleneck-1`.
2. **Before starting a run:**
   - commit its config;
   - write RUN.md's "Before" section: hypothesis, preregistration section, expected result, kill criterion;
   - record the commit SHA in the run record.
3. **Seeds:**
   - every run has an explicit seed;
   - confirmatory runs use the seed list fixed in the preregistration, never seeds chosen after seeing results.
4. **Data:**
   - record the dataset registry ID and sha256 of every input file;
   - evaluation data passes the contamination check (see `research/diligence/A5-contamination.md`) before use.
5. **Environment:** record library versions (`pip freeze` or equivalent), GPU type and count, and the driver version.
6. **Compute:**
   - record GPU-hours and total FLOPs where they can be estimated;
   - for CAMOE runs with variable repasses, record both the average and the worst-case compute per input.
7. **Failures are records, not deletions.** A crashed, diverged or disappointing run keeps its RUN.md, with what happened and what was learned.
8. **Exploratory vs confirmatory:** mark every run as one or the other. Only confirmatory runs, planned in the preregistration, support claims in the paper.
9. **Deviations:** any change to a preregistered plan is logged in the preregistration's deviation section *before* the result is known, or flagged as post-hoc if not.
