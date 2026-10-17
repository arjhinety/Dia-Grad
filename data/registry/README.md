# Dataset registry (D24)

Adapted from OpenGrad's scheme (`arjhinety/OpenGrad` @ `76645059`: `docs/datasets/ADDING_A_SOURCE.md`,
`docs/PROVENANCE.md`). Anyone reading a DiaGrad result should be able to answer, without asking us:
which bytes were used, under what terms, what else they overlap, and which sources were considered
and rejected.

## Files

| File | Holds |
|---|---|
| `<id>.json` | One record per dataset we use, schema v2 (`schema/dataset_record.schema.json`) |
| `source_screening.json` | Every candidate screened for a purpose, with a verdict per criterion, **including the rejected ones** |
| `../ROW-PROVENANCE.md` | The provenance columns every row of a normalised DiaGrad dataset carries (D21) |
| `../releases/` | Append-only records of each Hugging Face publication |

The data itself never goes into git (licences, size). Raw files live under `~/data/raw/<id-or-version>/`
on the GB10 workstation, each in its own folder; the record pins their sha256.

Check everything with:

```bash
PYTHONPATH=src python3 -m diagrad.registry.validate      # or the full test suite: tests/test_registry.py
```

The validator prints a census (`discovered == checked + skipped`, `checked == passed + failed`). An
empty registry is a failure, not a pass.

## Adding a source, in order

0. **Screen first.** Add the candidate to `source_screening.json` under the purpose's screening, with a
   verdict per criterion (PASS / PARTIAL / FAIL / UNKNOWN / NOT_APPLICABLE), a count and its basis,
   evidence, and a decision: SHORTLISTED (fails nothing), EXCLUDED (names the FAIL criteria) or
   WATCHLIST (names what would change the verdict). Rejected candidates stay in the log. Adopting is
   the author's decision; an adopted candidate must point at a registry record.
1. **Pin the bytes.** Use an immutable revision: a full git commit, a Hugging Face revision, or a
   version that is part of the URL (OPUS `.../v9/...`). Never `main`, `master` or `latest`. A file with
   no version (`SERVER_FILE`) is anchored by its own sha256. List each file in `distribution` with its
   URL, local path, sha256 and size, and say in `verified_from` how you know they are the pinned bytes
   (the Hub's LFS sha256, `git hash-object` equal to the pinned tree's blob id, the server's hash).
2. **Record the terms.** Quote the licence as read at the pinned revision (not a metadata tag alone),
   with its SPDX id. Set `use_class`, `redistribution.status` with its `basis`, and the attribution
   fields. D21: this is what the published dataset card and the per-row `source_license` use.
3. **Record what the text is.** `text_origin.kind`: HUMAN, MINED, MACHINE_TRANSLATED or MIXED. For
   machine-translated text, name the generator and its licence: the validator blocks training text
   from a non-commercial model unless a logged deviation (`"deviation": "D<n>"`) allows it.
4. **Record overlap and contamination.** `contamination.status` comes from the A5 §3.2 check (D20).
   Held-out and evaluation sets are `IS_HELDOUT_OR_EVALUATION` and can never list a training purpose.
5. **Uses.** `purpose` lists what the data may be used for; `forbidden_uses` what it may not
   (e.g. `PUBLISH_IN_TRAINING_DATASET` for held-out sets).
6. **Validate**, then commit the record together with the code that uses it.

Paper references in `attribution.citation_target` follow the project's citation rule: if the paper is not yet in
`research/papers/references.bib`, mark it `[verify]`.
