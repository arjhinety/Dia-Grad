# License audit

Generated 2026-10-07 by `research/tools/license_audit.py` from `components.json`.
Licenses are read from each component's source (Hugging Face metadata or GitHub). This is an
engineering classification, not legal advice; read the license text before relying on it.

## permissive — Commercial use allowed; keep the license notice.

| Component | Kind | License | Why it's on the list | Note |
|---|---|---|---|---|
| [google/madlad400-3b-mt](https://huggingface.co/api/models/google/madlad400-3b-mt) | hf-model | apache-2.0 | Path A base for our own sentence space |  |
| [google/madlad400-7b-mt](https://huggingface.co/api/models/google/madlad400-7b-mt) | hf-model | apache-2.0 | Path A, larger |  |
| [google/madlad400-10b-mt](https://huggingface.co/api/models/google/madlad400-10b-mt) | hf-model | apache-2.0 | Path A, largest |  |
| [google/mt5-base](https://huggingface.co/api/models/google/mt5-base) | hf-model | apache-2.0 | Path B cheap prototype |  |
| [google/byt5-base](https://huggingface.co/api/models/google/byt5-base) | hf-model | apache-2.0 | Path B, byte-level (no tokenizer bias against PH languages) |  |
| [sentence-transformers/LaBSE](https://huggingface.co/api/models/sentence-transformers/LaBSE) | hf-model | apache-2.0 | Path C encoder |  |
| [intfloat/multilingual-e5-large](https://huggingface.co/api/models/intfloat/multilingual-e5-large) | hf-model | mit | Path C encoder |  |
| [BAAI/bge-m3](https://huggingface.co/api/models/BAAI/bge-m3) | hf-model | mit | Path C encoder |  |
| [Alibaba-NLP/gte-multilingual-base](https://huggingface.co/api/models/Alibaba-NLP/gte-multilingual-base) | hf-model | apache-2.0 | Path C encoder |  |
| [facebook/mbart-large-50](https://huggingface.co/api/models/facebook/mbart-large-50) | hf-model | mit | alternative encoder-decoder |  |
| [deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4.1-Flash) | hf-model | mit | architecture reference with built-in Engram |  |
| [deepseek-ai/DeepSeek-V4-Flash](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Flash) | hf-model | mit | architecture reference |  |
| [allenai/OLMo-2-0425-1B](https://huggingface.co/api/models/allenai/OLMo-2-0425-1B) | hf-model | apache-2.0 | fully open small base model (used by Encode-Think-Decode) |  |
| [Qwen/Qwen3-0.6B](https://huggingface.co/api/models/Qwen/Qwen3-0.6B) | hf-model | apache-2.0 | small open base model for quick experiments |  |
| [ByteDance/Ouro-1.4B](https://huggingface.co/api/models/ByteDance/Ouro-1.4B) | hf-model | apache-2.0 | looped model studied by the halting-gate paper |  |
| [tomg-group-umd/huginn-0125](https://huggingface.co/api/models/tomg-group-umd/huginn-0125) | hf-model | apache-2.0 | recurrent-depth model (2502.05171) |  |
| [Unbabel/wmt22-comet-da](https://huggingface.co/api/models/Unbabel/wmt22-comet-da) | hf-model | apache-2.0 | evaluation metric |  |
| [google/metricx-24-hybrid-large-v2p6](https://huggingface.co/api/models/google/metricx-24-hybrid-large-v2p6) | hf-model | apache-2.0 | evaluation metric |  |
| [deepseek-ai/Engram](https://github.com/deepseek-ai/Engram) | github | apache-2.0 | Engram reference implementation |  |
| [facebookresearch/large_concept_model](https://github.com/facebookresearch/large_concept_model) | github | mit | LCM code (sentence-space modelling) |  |
| [alexiglad/EBT](https://github.com/alexiglad/EBT) | github | apache-2.0 | Energy-Based Transformers code |  |
| [seal-rg/recurrent-pretraining](https://github.com/seal-rg/recurrent-pretraining) | github | apache-2.0 | recurrent-depth training code |  |
| [facebookresearch/coconut](https://github.com/facebookresearch/coconut) | github | mit | continuous latent reasoning code |  |
| [google-research/metricx](https://github.com/google-research/metricx) | github | apache-2.0 | MetricX code |  |
| [Unbabel/COMET](https://github.com/Unbabel/COMET) | github | apache-2.0 | COMET code |  |
| [HPLT/HPLT2.0_cleaned](https://huggingface.co/api/datasets/HPLT/HPLT2.0_cleaned) | hf-dataset | cc0-1.0 | Filipino monolingual text (tgl_Latn) for the target encoder's denoising loss (data survey 2026-10-07) |  |
| [google/wmt24pp](https://huggingface.co/api/datasets/google/wmt24pp) | hf-dataset | apache-2.0 | E1 evaluation data (en-fil_PH); must stay out of every training and held-out set |  |

## permissive-attribution — Commercial use allowed; attribution required.

| Component | Kind | License | Why it's on the list | Note |
|---|---|---|---|---|
| [allenai/MADLAD-400](https://huggingface.co/api/datasets/allenai/MADLAD-400) | hf-dataset | odc-by | monolingual pretraining data incl. PH languages |  |
| [HuggingFaceFW/fineweb-2](https://huggingface.co/api/datasets/HuggingFaceFW/fineweb-2) | hf-dataset | odc-by | monolingual pretraining data |  |
| [aisingapore/kalahi](https://huggingface.co/api/datasets/aisingapore/kalahi) | hf-dataset | cc-by-4.0 | evaluation (Kalahi) — id to verify |  |
| [google/smol](https://huggingface.co/api/datasets/google/smol) | hf-dataset | cc-by-4.0 | en-fil parallel (SmolSent 754 sentences, SmolDoc 60 docs; human translation): tranche-1 held-out candidate (data survey 2026-10-07) |  |
| [AmazonScience/massive](https://huggingface.co/api/datasets/AmazonScience/massive) | hf-dataset | cc-by-4.0 | en-US/tl-PH parallel utterances (16,521; human localisation, card names MTurk worker ids): tranche-1 held-out candidate (data survey 2026-10-07) |  |
| [mutiyama/alt](https://huggingface.co/api/datasets/mutiyama/alt) | hf-dataset | cc-by-4.0 | ALT en-fil parallel (18,088 in OPUS; Wikinews, human translation): tranche-1 candidate (data survey 2026-10-07) |  |

## share-alike — Commercial use allowed, but derived data/works must carry the same license.

| Component | Kind | License | Why it's on the list | Note |
|---|---|---|---|---|
| [openlanguagedata/flores_plus](https://huggingface.co/api/datasets/openlanguagedata/flores_plus) | hf-dataset | cc-by-sa-4.0 | evaluation (must stay out of training) | gated: auto |
| [facebook/belebele](https://huggingface.co/api/datasets/facebook/belebele) | hf-dataset | cc-by-sa-4.0 | evaluation (reading comprehension) |  |

## non-commercial — Research only. Must not end up inside a commercially used DiaGrad model.

| Component | Kind | License | Why it's on the list | Note |
|---|---|---|---|---|
| [facebook/SONAR](https://huggingface.co/api/models/facebook/SONAR) | hf-model | cc-by-nc-4.0 | excluded reference (non-commercial) |  |
| [facebook/nllb-200-distilled-600M](https://huggingface.co/api/models/facebook/nllb-200-distilled-600M) | hf-model | cc-by-nc-4.0 | excluded reference (non-commercial); must not be used to make training data |  |
| [Unbabel/wmt22-cometkiwi-da](https://huggingface.co/api/models/Unbabel/wmt22-cometkiwi-da) | hf-model | cc-by-nc-sa-4.0 | evaluation metric (reference-free) | gated: auto |
| [Unbabel/XCOMET-XL](https://huggingface.co/api/models/Unbabel/XCOMET-XL) | hf-model | cc-by-nc-sa-4.0 | evaluation metric with error spans | gated: auto |

## unknown — No license found at the source. Treat as all rights reserved until clarified.

| Component | Kind | License | Why it's on the list | Note |
|---|---|---|---|---|
| [facebookresearch/SONAR](https://github.com/facebookresearch/SONAR) | github | — | SONAR code (MIT) vs weights (NC) | GitHub could not identify the license file (NOASSERTION) |
| [jxmorris12/vec2text](https://github.com/jxmorris12/vec2text) | github | — | embedding inversion code (Path C) |  |
| [uonlp/CulturaX](https://huggingface.co/api/datasets/uonlp/CulturaX) | hf-dataset | — | monolingual pretraining data | gated: auto |
| [allenai/nllb](https://huggingface.co/api/datasets/allenai/nllb) | hf-dataset | — | mined parallel data (check terms carefully) |  |
| [UD-Filipino/filbench](https://huggingface.co/api/datasets/UD-Filipino/filbench) | hf-dataset | — | evaluation (FilBench) — id to verify | HTTP 401 |
