# Publication records (D21, D24)

Adapted from OpenGrad's `reports/releases/`. Publishing a dataset on Hugging Face is an outward-facing
step that needs the author's explicit approval at the time (D21). Each publication gets one append-only JSON
record here, written at the time of the event. Nothing has been published yet.

A record holds:
- `repository`, `hub_revision` (full 40-hex), and `superseded_hub_revision` if it replaces one;
- `event_occurred_at` and `entry_recorded_at`. If the entry is written after the event,
  `recorded_retroactively: true` plus the immutable evidence it was reconstructed from;
- the derived corpus's registry id and `processed_sha256` (the payload identity), the record count,
  and the files published;
- for a correction (a licence file or card fixed, payload unchanged): what changed and why. A
  correction is a new publication event, not a new version of the corpus.

Two identities, kept separate:
- **release identity**: the payload (rows and their fingerprint). It is immutable, a rebuild must
  reproduce it, and experiments pin it;
- **publication identity**: the set of files at a Hub revision. It moves whenever anything published
  changes, including the card or the licence file.

Before any upload: run the A5 §3.2 check against held-out and evaluation sets, add the canary string,
leave out rows whose source is `NOT_PERMITTED`, keep share-alike sources in their own config, and
write the card's attribution section from the registry records.
