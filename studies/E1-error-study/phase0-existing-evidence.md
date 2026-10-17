# E1 phase 0 · What published work already says about Filipino MT errors

Compiled 2026-09-24 from the full texts in `research/papers/txt/`. Quotes are from the PDFs.

| Source | What was measured | Numbers | Can it answer RQ1 (meaning vs surface share)? |
|---|---|---|---|
| FilBench (2508.03523, §5 "Failure modes") | Authors manually inspected **100 failure cases from GPT-4o** on generation tasks (incl. translation) | overgeneration **47%**, poor instruction-following (incl. "translations in an incorrect target language") **34%**, hallucination **19%** | **No.** Failures only, "a sample of 100 failure cases" (sampling method not stated, so not known to be random); coarse failure modes, not error categories; mixes families (wrong target language = surface, hallucination = meaning, overgeneration = addition) |
| Batayan (2502.14911, §3.3 and §4) | Qualitative review of machine- and expert-translated Filipino datasets | No counts. MT showed "an unusual preference with using ay-inversion" and used "terms that were synonymous to their English counterparts but pragmatically-awkward"; earlier datasets had "inaccuracies and translationese" | **No.** Qualitative, but confirms that surface errors (*ay*-inversion, awkward word choice) are common enough to be noticed |
| WMT24++ (2502.12404, §2–3, App. B) | Professional references, then professional post-edits; systems ranked by automatic metrics only | Of 998 en-fil_PH rows, **202 (20%)** post-edits differ from the reference (computed by us from the data file, 2026-09-24). No MT error analysis | **No.** No human evaluation of MT output; the authors defer it to "future work" |
| SEA-HELM (2502.14301) | Filipino translation scored with MetricX-24 | Scores only | **No** |

**Conclusion:** no published work measures the meaning/surface split for MT into any Philippine
language. E1 fills this gap. The gap itself is a finding worth reporting in the paper's motivation.

**Caveat on our own inference:** "surface errors are common" rests on Batayan's qualitative
observation plus FilBench's wrong-target-language share. Neither is a random sample of MT output, so
neither tells us the proportion.
