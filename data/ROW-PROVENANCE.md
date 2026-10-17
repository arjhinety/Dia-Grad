# Row provenance for normalised DiaGrad datasets (D21, D24)

Every row of a normalised dataset we build (the tranche-1 training mix, and anything later published
on Hugging Face) carries its own provenance, so a single row can be traced to its source and terms.
Adapted from OpenGrad's release rows (`src/opengrad/data/release.py`, `_parquet_row`).

| Column | Meaning |
|---|---|
| `diagrad_id` | Stable id: `<source id>:<source record id>` |
| `src_text`, `tgt_text` | The pair after normalisation |
| `src_lang`, `tgt_lang` | e.g. `eng_Latn`, `tgl_Latn` |
| `source_dataset` | Registry id (`data/registry/<id>.json`) |
| `source_revision` | The record's pinned revision or version |
| `source_record_id` | The upstream row id or line number in the pinned file |
| `source_url` | The upstream page URL where the source has one (NLLB `eng_url`/`tgl_url`), else empty |
| `source_license` | SPDX id from the record |
| `use_class` | From the record (e.g. `RESEARCH_ONLY`, `SHARE_ALIKE`) |
| `redistribution_status` | From the record; rows that are `NOT_PERMITTED` never enter a published copy |
| `text_origin` | HUMAN / MINED / MACHINE_TRANSLATED (+ generator) |
| `synthetic_tag` | Empty for real pairs; e.g. `<BT>` for back-translated pairs (D22 Mix 4) |
| `normaliser_version` | Version of the normalisation code (git commit) |
| `filters_passed` | Which filters the row passed, with scores (LID, length, LASER/LaBSE) |
| `contamination_status` | Result of the A5 §3.2 check for this row |
| `row_sha256` | sha256 of the normalised (`src_text`, `tgt_text`) pair |

A dataset built from these rows has its own registry record (`role: DERIVED_CORPUS`) with
`derived_from` (each source id and revision) and `processed_sha256`, an order-independent fingerprint:
sha256 over the sorted `row_sha256` values.

Not implemented yet: the normaliser is written when the D22 mix is built.
