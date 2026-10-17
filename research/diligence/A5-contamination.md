# A5 · Contamination check: which Philippine-language benchmarks can DiaGrad trust?

Created 2026-09-24 (desk research only; no models trained or run). Task A5 in `research/DILIGENCE.md` (item #13).
All sources retrieved **2026-09-24** unless noted.

**Labels.** **[source-stated]**: a paper, dataset card, script or API response says it. **[inference]**: my reasoning from stated facts, mostly from dates. **[unknown]**: I could not verify it.

**Verdict scale used in the table.**
- **Known**: a source states that the benchmark's items are in the training source, or the training source's own listing shows it.
- **Likely**: the benchmark text (or its source text) was public on the open web before the crawl window closed, and nothing removed it.
- **Possible**: public before the crawl window closed, but no positive evidence of inclusion. My spot check of Common Crawl found few direct captures (see §1.4).
- **Ruled out by date**: the benchmark was released after the corpus's last crawl or snapshot, so the corpus cannot contain it. The *source text* a benchmark was built from may still be older.
- **No evidence / Unknown**: nothing stated, and the dates don't settle it.

---

## 1. Plain-language summary

### 1.1 What we found

1. **Two public test sets are already inside common training corpora (Known):**
   - **TICO-19 Tagalog.** FilBench uses it as its "domain-specific translation" task.
     - OPUS distributes TICO-19 en-tl as a training corpus of 3,071 pairs. That equals TICO-19's validation (971) plus test (2,100) splits [source-stated: OPUS API; HF `gmnlp/tico19` split sizes].
     - NLLB's public-bitext download script fetches TICO-19 including Tagalog [source-stated: fairseq `nllb` branch, `download_parallel_corpora.py`].
     - FilBench's TICO-19 TGL set has 971 items, the same size as the validation split [source-stated: 2508.03523 Table 1].
     - **Any model trained on "all of OPUS" or NLLB's bitext has very likely seen FilBench's TICO items** [inference].
   - **Tatoeba.** FilBench uses Tatoeba CEB and TGL.
     - OPUS ships a `Tatoeba` corpus for every Philippine pair we care about, for example en-tl 10,450 pairs and en-ilo 2,093 [source-stated: OPUS API].
     - The Tatoeba Translation Challenge takes its test sets from that same Tatoeba database. Its authors show that some test pairs also occur in other OPUS training data [source-stated: 2010.06354 §1, Fig. 3].
2. **FLORES is the benchmark most often found contaminated in *other* models.**
   - The CONDA 2024 contamination database lists FLORES inside the xP3 instruction mixture, and flags BLOOMZ, mT0 and Claude 3 Opus [source-stated: 2407.21530 Tables 1–2].
   - FLORES-101 (June 2021) already covered Tagalog and Cebuano. FLORES-200 (July 2022) added Ilocano, Waray and Pangasinan. The dev and devtest splits are public; only the test split is hidden behind a server [source-stated: 2106.03193 language table; 2207.04672 §4.1.3].
   - **Belebele reuses FLORES dev/devtest passages** [source-stated: 2308.16884 §3.5]. Any FLORES leak therefore also leaks Belebele's passages, though not its questions.
3. **MADLAD-400 (the proposed permissive replacement for SONAR) comes out fairly clean on paper:**
   - Its crawl stops at 2022-08-20 [source-stated: 2309.04662 §2].
   - Its parallel-data source list (Appendix A.5, Table 11) contains no Tatoeba, TICO-19, FLORES or ALT [source-stated].
   - OPUS-100, one of its sources, has no Philippine pairs [source-stated: HF `Helsinki-NLP/opus-100` configs].
   - **But:**
     - The paper says nothing at all about decontamination. I searched the full v1 text.
     - Tagalog and Cebuano FLORES were public a year before its crawl ended (**Possible**).
     - It reports results on FLORES-200 for ceb, fil, ilo, pag and war, and on NTREX for fil [source-stated: Table 14].
4. **The newer Filipino suites were released after most corpora were built:** Kalahi (Sept 2024), SEA-HELM and Batayan (Feb 2025), FilBench (Aug 2025).
   - They are **Ruled out by date** for mC4, MADLAD-400, HPLT v2, CulturaX and FineWeb-2 (FineWeb-2's crawl ends April 2024).
   - They are **not** ruled out for DeepSeek-V4 or V4.1, which appeared in 2026.
   - Two caveats:
     - FilBench is a *bundle of older datasets*, so its parts inherit their own older contamination risks.
     - Batayan re-translated its Filipino FLORES and Belebele items with native speakers, so SEA-HELM's Filipino references differ from public FLORES [source-stated: 2502.14911 §2–3].
5. **DeepSeek-V4 and V4.1 state nothing usable.**
   - The reports give no language list, no data cutoff date and no decontamination statement. Both full PDFs were searched.
   - V4 says only that it builds "a larger corpus" for multilingual data on top of V3's data. V4.1 says it filters "low-quality machine-translated text" [source-stated: 2606.19348 §4.1; 2609.19969 §4.1].
   - Contamination for DeepSeek is therefore **Unknown and uncheckable**, since the training data is closed.

### 1.2 What it means for DiaGrad

- **Do not make headline claims on TICO-19 or Tatoeba** if any training data comes from OPUS or NLLB. That covers most Philippine parallel data. Treat them as diagnostics only [inference].
- **FLORES devtest and Belebele may be reported, but only with a contamination audit attached**, run against our own training data using the procedure in §3. For closed-data bases (DeepSeek), treat those scores as upper bounds [inference].
- **DiaGrad's own native-speaker held-out sets (DATA-PLAN D5) are the only fully trustworthy evaluation.**
  - Keep them off the public web.
  - Hash them.
  - Write them *after* the base model's release date.

  This matches the DATA-PLAN "Separation" rule [inference].
- **Low-contamination external options for Tagalog:**
  - BOUQuET: hand-written, not crawled, includes Tagalog, with an evaluation split "intended to be kept hidden" [source-stated: 2502.04314 §3].
  - The hidden FLORES-200 test split, via its server [source-stated: 2207.04672 §4.1.3].
- **What contamination does to scores in MT:**
  - Contamination with *both* source and target inflates BLEU by up to 30 points at 8B scale, 2.5× the effect at 1B.
  - Source-only or target-only contamination inflates less and less consistently.
  - Languages with no representation in pre-training showed no measurable inflation. Above some threshold of representation, pairs with lower baseline scores were hit harder [source-stated: 2501.18771 abstract, §1, §5.5–5.6].
  - Tagalog and Cebuano are well represented in web corpora, so full-pair leaks of FLORES or TICO would matter [inference].

### 1.3 What is still unknown

- Whether MADLAD-400, FineWeb-2, CulturaX or HPLT v2 actually contain FLORES Tagalog/Cebuano text. Nobody has published an n-gram check, and I could not run one [unknown].
- The exact list of Philippine pairs in MADLAD's parallel data. It is published with the checkpoints; I did not download it [unknown].
- Whether NLLB's *mined* data contains FLORES dev/devtest. The NLLB paper (v3) has no explicit decontamination statement that I could find. The `allenai/nllb` card warns: "The data includes some development and test sets from other datasets, such as xlsum. In addition, sourcing data from multiple web crawls is likely to produce incidental overlap with other test sets." [source-stated; specific FLORES status unknown].
- Everything about DeepSeek-V4/V4.1 pre-training data composition [unknown].
- Whether MultiLoKo, which DeepSeek evaluates on, covers Tagalog. Not checked [unknown].

### 1.4 A spot check of Common Crawl, and what it does and doesn't show

I queried the Common Crawl URL index for two snapshots:
- CC-MAIN-2022-33, around the MADLAD cutoff;
- CC-MAIN-2024-10, inside FineWeb-2's window.

The URL patterns were the FLORES GitHub, the FLORES/Belebele/TICO/NTREX Hugging Face mirrors, NTREX GitHub and raw files, tico-19.github.io, and tatoeba.org sentence pages.

Results [source-stated: index.commoncrawl.org responses, 2026-09-24]:
- The only status-200 benchmark page found was `huggingface.co/datasets/gsarti/flores_101/viewer/eng/devtest` in 2024-10.
- tico-19.github.io landing pages were captured, but no data files.
- Tatoeba sentence pages appeared only as redirects (302), with no status-200 captures in the pages sampled.

**Interpretation [inference]:**
- Raw crawls of the benchmark files themselves look sparse, so the main contamination routes are *curated* corpora: OPUS, NLLB bitext, and instruction mixtures such as xP3.
- In addition, the *source text* of a benchmark may itself be on the web. That covers news for NTREX, NewsPH-NLI and BalitaNLP, and Wikimedia for the FLORES English side.
- This covers 2 of 128 snapshots with prefix queries only, so it is **weak negative evidence, not a clearance**.

---

## 2. Benchmark × source table

Abbreviations:

| Short name | What it is |
|---|---|
| MADLAD-mono | MADLAD-400 monolingual crawl (CC through 2022-08-20) |
| MADLAD-MT | MADLAD-400 MT models (parallel data from Table 11, plus MASS on MADLAD-mono) |
| mC4 | mT5's corpus (71 CC snapshots available by Oct 2020) |
| FW2 | FineWeb-2 (96 CC snapshots, summer 2013 to April 2024) |
| CulturaX | mC4 3.1.0 plus OSCAR 20.19/21.09/22.01/23.01 |
| HPLT2 | HPLT v2 (Internet Archive crawls mostly 2012–2020; CC crawls mostly 2014–2022) |
| OPUS | OPUS, as used in bulk |
| NLLB | NLLB public bitext recipe plus mined data |
| DS-V4 | DeepSeek-V4 / V4.1 pre-training |

### 2.1 Benchmark facts (used by the verdicts below)

| Benchmark | PH languages | Public since | Where it lives now | Source text origin |
|---|---|---|---|---|
| FLORES-101 → FLORES-200 → FLORES+ | FLORES-101: ceb, tgl. FLORES-200 adds ilo, war, pag. FLORES+ configs: ceb_Latn, fil_Latn, ilo_Latn, pag_Latn, war_Latn | FLORES-101 June 2021 (2106.03193); FLORES-200 July 2022 (2207.04672) | `facebook/flores` and `openlanguagedata/flores_plus` are **now gated**, with terms against crawler-reachable re-hosting. Ungated mirrors exist: `Muennighoff/flores200` (created 2022-07-17) and `gsarti/flores_101` [source-stated: HF API] | English Wikinews, Wikijunior and Wikivoyage, professionally translated. 3,001 sentences. Test split hidden [source-stated: 2207.04672 §4.1.1, §4.1.3] |
| Belebele | ceb_Latn, tgl_Latn, ilo_Latn, war_Latn [source-stated: HF configs] | Aug 2023 (2308.16884); HF `facebook/belebele` ungated, created 2023-09-01 | Ungated HF | Passages from FLORES dev/devtest ("none belonging to the hidden FLORES test set"). Questions newly written. Authors warn that open-sourcing may let samples "get collected into large pretraining corpora" [source-stated: §3.5, Ethics] |
| NTREX-128 | fil only (`newstest2019-ref.fil.txt`) [source-stated: GitHub tree] | GitHub repo created 2022-10-31 [source-stated: gh API] | GitHub, plus ungated HF mirrors (`mteb/NTREX`, `davidstap/NTREX`, `SEACrowd/ntrex_128`, …) | English WMT19 newstest (news), human-translated [source-stated: 2508.03523 Table 7] |
| Tatoeba (Challenge test sets) | tgl, ceb (FilBench). OPUS Tatoeba pairs: en-tl 10,450; ceb-en 424; en-ilo 2,093; en-war 1,569; en-pam 1,497; en-pag 50; en-hil 22; bcl-en 2 [source-stated: OPUS API] | Tatoeba site is long-running; Challenge 2020 (2010.06354) | tatoeba.org; OPUS; HF `Helsinki-NLP/tatoeba_mt` | Crowd-sourced short sentences, average 5.90 tokens in FilBench [source-stated: 2508.03523 App. I] |
| TICO-19 | tl (Tagalog) | 2020 | tico-19.github.io; OPUS `tico-19`; HF `gmnlp/tico19` (en-tl validation 971, test 2,100) | News, Wikipedia, PubMed [source-stated: 2508.03523 Table 7] |
| Kalahi | Filipino (150 prompts) | arXiv Sept 2024; HF `aisingapore/kalahi` **ungated**, created 2024-10-20. SEA-HELM copy `aisingapore/Cultural-Evaluation-Kalahi` gated | Ungated HF | Hand-written with native speakers through focus-group discussions [source-stated: 2409.15380 §3] |
| SEA-HELM Filipino (= Batayan) | Filipino | Feb 2025 (2502.14301, 2502.14911) | HF `aisingapore/NLG-Machine-Translation` (en_to_tl, tl_to_en), NLR-NLI, NLR-Causal-Reasoning, NLU-Sentiment-Analysis, NLG-Abstractive-Summarization. All `gated: auto`, created 2024-12-11. PAWS-tl and Global-MMLU-lite-tl are **plain JSONL in the public MIT GitHub repo** `aisingapore/SEA-HELM` [source-stated: HF API, gh API] | FLORES FIL (1,012) and Belebele (900) natively **re-translated**. PAWS, COPA, XNLI and XL-Sum natively translated. PH Elections tweets native [source-stated: 2502.14911 Table 1, §2] |
| FilBench | Filipino, Tagalog, Cebuano | Aug 2025 (2508.03523; EMNLP 2025) | Bundle of 12 sub-tasks. Instruction-format copies are ungated on HF org `filbench` (e.g. `filbench/cebuano-readability`, `filbench/UD_Tagalog-NewsCrawl`) | Components: SIB-200, CebuaNER, TLUnified-NER, Universal NER, FiReCS, BalitaNLP, Dengue, INCLUDE, Global-MMLU, Kalahi, StingrayBench, Cebuano Readability, Belebele, NewsPH-NLI, NTREX, Tatoeba, TICO-19 [source-stated: Tables 1, 7] |
| Other PH sets found | — | — | — | NewsPH-NLI (scraped "from all major Philippine news sites" [source-stated: 2010.11574 §3]); BalitaNLP and TLUnified-NER (news); ALT en-fil in OPUS, 18,088 pairs [source-stated: OPUS API]; BOUQuET tgl (hand-written, hidden eval split) [source-stated: 2502.04314 §3, language table] |

### 2.2 Verdicts per pair

| Benchmark | Source | Verdict | Evidence and reasoning |
|---|---|---|---|
| **FLORES tgl/ceb** (dev/devtest) | MADLAD-mono / MADLAD-MT | **Possible** | Public June 2021, crawl ends 2022-08-20 [source-stated]. No decontamination statement in 2309.04662 v1 [source-stated by absence, full-text search]. FLORES is not in the parallel sources, Table 11 [source-stated]. CC-MAIN-2022-33 had no captures of the FLORES GitHub or HF mirror pages [source-stated, spot check]. For xx→en, the English reference text (Wikimedia) was certainly on the web: target-side-only exposure, which 2501.18771 finds inflates scores little and inconsistently [source-stated + inference] |
| FLORES ilo/war/pag | MADLAD-mono / MT | **Possible but unlikely** | FLORES-200 appeared July 2022, about 5 weeks before the crawl cutoff [inference from dates] |
| FLORES (any PH) | mC4 / mT5 | **Ruled out by date** for the translations | mC4 used the 71 CC snapshots available at writing time, Oct 2020 [source-stated: 2010.11934 §2]; FLORES-101 is 2021 [inference]. The English source sentences are older Wikimedia text [inference] |
| FLORES (any PH) | FW2 | **Possible** | Crawl window reaches April 2024 [source-stated: 2506.20920]. Its "contamination" analysis concerns language-ID noise, not benchmarks; I found no benchmark decontamination statement [source-stated by absence]. CC-MAIN-2024-10 contains the `gsarti/flores_101` viewer page for eng/devtest [source-stated, spot check]. PH-language viewer pages were not checked [unknown] |
| FLORES (any PH) | CulturaX | **Possible** | OSCAR 21.09–23.01 postdate FLORES-101 [source-stated: 2309.09400 §1; inference]. No benchmark decontamination statement found [source-stated by absence] |
| FLORES (any PH) | HPLT2 | **Possible** | CC crawls mostly 2014–2022 [source-stated: 2503.10267 §4.1]. Authors: "It is possible that some of the test data we use for evaluation is contained within HPLT v2" (their own evaluation sets, which include FLORES-200) [source-stated: §6] |
| FLORES (any PH) | OPUS | **No evidence** (direct) | No `flores` corpus in the OPUS listings for en-tl or ceb-en [source-stated: OPUS API]. OPUS also hosts the `NLLB` mined corpus (en-tl 63.6M pairs); see the NLLB row [source-stated] |
| FLORES (any PH) | NLLB | **Unknown** | The NLLB team built FLORES-200 and hid the test split. I found no statement that dev/devtest were filtered from the mined data. The card warns of "incidental overlap with other test sets" [source-stated: 2207.04672; `allenai/nllb` README] |
| FLORES (any PH) | xP3 → BLOOMZ, mT0 (not DiaGrad candidates) | **Known** | CONDA database [source-stated: 2407.21530 Tables 1–2]. Also, BLOOMZ was "fine-tuned for translation on FLORES-200" [source-stated: 2308.16884 Limitations] |
| FLORES (any PH) | DS-V4 | **Unknown / uncheckable** | No data list, cutoff or decontamination statement [source-stated by absence: 2606.19348, 2609.19969 full PDFs]. Public since 2021–22 [inference: plausible] |
| SEA-HELM FIL FLORES (re-translated) | all pre-2025 corpora | **Ruled out by date** for the new Filipino references | Re-translated for Batayan, released Feb 2025. English side = FLORES English [source-stated: 2502.14911; inference] |
| SEA-HELM FIL FLORES | DS-V4 | **Unknown** | HF copies are gated, so crawler exposure is reduced [source-stated: HF API]. Status before gating is unknown [unknown] |
| **Belebele** (ceb/tgl/ilo/war) | mC4, MADLAD, HPLT2 | **Questions ruled out by date; passages = FLORES rows above** | Released Aug 2023 [source-stated] |
| Belebele | FW2 | **Possible** | Window reaches Apr 2024. `facebook/belebele` HF pages had no captures in CC-MAIN-2024-10 [source-stated, spot check] |
| Belebele | CulturaX | **Unknown** | Depends on OSCAR 23.01's crawl date, not verified [unknown] |
| Belebele | DS-V4 | **Unknown / possible** | Ungated since 2023; authors warn of crawl pickup [source-stated] |
| **NTREX fil** | MADLAD-mono | **Ruled out by date** for the Filipino references | GitHub repo created 2022-10-31, after the 2022-08-20 cutoff [source-stated; inference]. The English source (WMT19 news) predates it: target-side exposure for fil→en only [inference] |
| NTREX fil | FW2, DS-V4 | **Possible** | Many ungated HF mirrors since 2024 [source-stated: HF search]. No CC captures of the NTREX GitHub or raw files in 2022-33 or 2024-10 [source-stated, spot check] |
| NTREX fil | NLLB, OPUS | **No evidence** | Not in OPUS en-fil listing (ALT, GlobalVoices, QED, TED2020, Ubuntu) [source-stated] |
| **Tatoeba tgl/ceb** | OPUS | **Known** | OPUS `Tatoeba` corpus exists for all PH pairs [source-stated: OPUS API]. Challenge test data is drawn from Tatoeba [source-stated: 2010.06354 §1]. Even the Challenge's Tatoeba-free training data overlaps with some test pairs [source-stated: Fig. 3] |
| Tatoeba | NLLB | **Possible** | The public bitext script has no Tatoeba downloader [source-stated: `download_parallel_corpora.py`]. Mined data "likely to produce incidental overlap" [source-stated: README] |
| Tatoeba | MADLAD-MT | **No evidence** | Not in Table 11 [source-stated] |
| Tatoeba | mC4 / MADLAD-mono | **Unlikely** | Both drop pages without at least 3 lines of 200+ characters [source-stated: 2309.04662 §2.1; 2010.11934 §2]. Tatoeba sentence pages are short-sentence pages [inference] |
| Tatoeba | FW2, CulturaX, HPLT2, DS-V4 | **Possible** | Web-public; filters not checked against Tatoeba pages [unknown] |
| **TICO-19 tl** | OPUS | **Known** | OPUS `tico-19` en-tl has 3,071 pairs = validation 971 + test 2,100 [source-stated counts; inference that it holds both splits]. FilBench uses 971 items [source-stated] |
| TICO-19 tl | NLLB | **Known** | NLLB's public bitext script downloads TICO-19 translation memories with `"tl": "tgl"` among target languages [source-stated] |
| TICO-19 tl | MADLAD-MT | **No evidence** | Not in Table 11 [source-stated] |
| TICO-19 tl | web corpora, DS-V4 | **Possible** | Released 2020 as zip files; the site's landing pages are crawled but no data files were seen [source-stated, spot check] |
| **Kalahi** | mC4, MADLAD, HPLT2, CulturaX, FW2 | **Ruled out by date** | arXiv Sept 2024; HF 2024-10-20. All these corpora close earlier (FW2: April 2024) [source-stated dates; inference] |
| Kalahi | DS-V4 | **Unknown / possible** | Ungated on HF since Oct 2024 [source-stated] |
| **FilBench (as a bundle)** | all | **Inherits per component** | Its TICO-19 and Tatoeba parts are Known-contaminated for OPUS/NLLB-trained models. Its Belebele part = FLORES risk. Global-MMLU TGL is a translation of MMLU, and MMLU is reported contaminated in CommonCrawl [source-stated: 2407.21530 Table 1]. Translated copies can transfer contamination across languages and evade n-gram checks [source-stated: 2406.13236 abstract, §3]. NewsPH-NLI, BalitaNLP and TLUnified-NER are built from news websites, so their source text is **Likely** in any CC-derived corpus [inference from 2010.11574 §3] |
| FilBench | DS-V4 | **Unknown** | Released Aug 2025, before V4 (June 2026) [source-stated dates] |
| ALT en-fil (if used) | OPUS | **Known (whole corpus)** | OPUS lists ALT en-fil, 18,088 pairs [source-stated]. Whether that includes ALT's standard test split: [unknown] |
| BOUQuET tgl | all | **Ruled out for the hidden eval split** | Hand-written, "not crawled"; evaluation split intended to be hidden [source-stated: 2502.04314 §3] |

---

## 3. Recommended contamination-check procedure (run before every evaluation)

### 3.1 How researchers usually check
- **13-gram overlap (GPT-3).**
  - Flag any test example with a 13-gram overlap with the pre-training set, "or that overlap with the whole example when it is shorter than 13-grams".
  - Report scores on a "clean" subset alongside the full set.
  - Their check flagged 25% of WMT16 German–English test examples [source-stated: 2005.14165 §4, App. C].
- **ConTAM (2411.03923).**
  - Compares four n-gram metrics.
  - "Longest-match" gives the best signal.
  - Smaller n is better, and "even one occurrence in the pre-training data matters". Setting n above 8 or requiring a count above 1 causes false negatives.
  - Thresholds should be chosen per model [source-stated: 2411.03923 §1, §5].
- **FRED (2603.25222, ACL 2026).**
  - *E* (pre-training exposure): the mean pre-training-corpus count of the test set's unique target 4-grams, computed with infini-gram.
  - *R* (retrieval proxy): the score a nearest-neighbour lookup of the *training* set would get, i.e. a ceiling for pure memorisation.
  - *D* (corpus diversity) and *F* (token fertility) complete the set.
  - In their extremely-low-resource regression, *R* explained the most variance (R² = 0.582) and *E* almost none (R² = 0.0142) [source-stated: 2603.25222 §2.2, §3.3, App. E.1].
  - *E* is a raw mean count, so it scales with corpus size. Compare it only across test sets scored against the *same* corpus [inference].
  - The expected local copy (`research/papers/md/2603.25222.md`) does not exist. I read the paper through `pwc paper read`.
- **Cross-lingual contamination.** A model trained on a *translated* benchmark gains on the original while text-overlap checks miss it. The authors propose generalisation-based detection instead [source-stated: 2406.13236].
- **Black-box checks for closed-data models.** Examples are guided-instruction completion tests (Golchin & Surdeanu) and membership-inference methods, as catalogued in the CONDA report [source-stated: 2407.21530 §2]. I did not verify their reliability for Philippine languages [unknown].

### 3.2 DiaGrad procedure (proposed in this review)

> **Adopted for tranche 1 on 2026-10-08 (D20).** Steps 1–5, 9, 11 and 12 apply; steps 6–8 and 10
> concern benchmarks and base models not used in tranche 1. Checker: `src/diagrad/t1/contamination.py`.

**Unit pinned:** one test **item** = one sentence pair, or one multiple-choice question including its passage. Every rate below is *flagged items ÷ total items*, with both counts reported. Worked example: a 1,012-item FLORES devtest with 253 flagged items → 253 / 1012 = **0.25**. Put this literal case in the checker's unit test.

**Steps:**

1. **Freeze and hash.**
   - Record URL, version or commit, retrieval date and SHA-256 for each test file, in `data/registry/` per DATA-PLAN.
   - Record which split is used (FLORES dev vs devtest).
2. **Normalise both sides identically.**
   - Unicode NFKC, lowercase, collapse whitespace, strip punctuation.
   - Also strip diacritics as a second pass, because Filipino orthography varies.
   - Tokenise on *whitespace words*, not a model tokenizer, so results compare across base models.
3. **Exact match.**
   - Hash the normalised source, the target, and the (source, target) pair.
   - Look up each against every file DiaGrad trains on: D2 monolingual, D3 parallel, D4 critic data, any SFT or instruction mixture, and back-translation outputs.
   - Report source-only, target-only and pair hits separately. Pair hits are the ones that inflate scores most [source-stated: 2501.18771].
4. **N-gram overlap (ConTAM longest-match).**
   - For every item, compute the longest contiguous word span found in the training data. Allow a skip budget of 0 as the default.
   - Flag the item if it contains any 8-gram match. If the item is shorter than 8 words, flag it only on a whole-item match; this matters for Tatoeba, whose items average 5.9 tokens.
   - Also report the GPT-3-style 13-gram flag, for comparability with published work.
   - For corpora too large to scan directly (MADLAD-400, FineWeb-2), build an infini-gram index over **only the PH-language subsets we actually use**, as FRED did for a ~30 GB bitext subset in about 3 hours on CPU [source-stated: 2603.25222 App. G].
5. **FRED R-score against our own parallel training data.**
   - Nearest-neighbour chrF against D3.
   - Report it next to every MT score. A system that does not beat *R* has not shown translation ability [source-stated reasoning: 2603.25222 §3.4].
6. **FRED E-score** against each indexed corpus, as a secondary exposure indicator only.
7. **Translated-benchmark check.**
   - For Global-MMLU TGL and Batayan's COPA, XNLI and PAWS, also run steps 3–4 on the *English originals* against the English parts of our training data.
   - Flag the whole benchmark if the original is contaminated [inference from 2406.13236].
8. **Closed-data base models (DeepSeek).**
   - The training data cannot be checked, so:
     - (a) State that scores are upper bounds.
     - (b) Run a completion probe: give the first half of FLORES or Belebele items and measure verbatim continuation.
     - (c) Compare against a time-split set: DiaGrad D5 items written **after** the model's release date.
   - A large gap between public-benchmark and time-split performance is a contamination signal, not proof [inference].
9. **Report both scores.** Give the full-set score and the clean-subset score (flagged items removed), plus the flag rate, per language. If the clean subset has fewer than about 200 items, say so rather than reporting it alone [inference].
10. **Decide using tiers:**
    - **Tier A (headline claims):** DiaGrad D5 held-out sets; hidden splits (FLORES-200 test via server, BOUQuET eval).
    - **Tier B (report with audit):** FLORES devtest, Belebele, NTREX fil, Kalahi, SEA-HELM Filipino.
    - **Tier C (diagnostic only when OPUS or NLLB data is used):** TICO-19 tl, Tatoeba, ALT.
11. **Re-run and log.** Re-run the check whenever training data changes. Store a JSON report (counts, flag lists, hashes, tool versions) in the run log (DILIGENCE #9).
12. **Protect our own eval data.** Never upload D5 to crawlable locations. Use gated or encrypted storage, following FLORES+'s gating terms ("I agree not to re-host FLORES+ in places where it could be picked up by web crawlers") [source-stated: HF card metadata]. Add a canary string [inference; practice described in the CONDA literature, not verified here].

---

## 4. Sources (all retrieved 2026-09-24)

**Papers (arXiv IDs; local copy in `research/papers/md/` where noted):**
- 2309.04662 MADLAD-400. §2 (CC snapshots to 2022-08-20), §2.1 filters, §3, App. A.5 Table 11 (parallel sources), App. A.9 Table 14 (languages evaluated), §5 memorisation. v1 PDF fully searched.
  - Note: the local md is truncated after App. A.4, and its table shows "tl Tetela" where the PDF has "tll".
- 2508.03523 FilBench (local): Table 1, Table 7, Limitations, App. I.
- 2409.15380 Kalahi (local): §3.
- 2502.14301 SEA-HELM (local): Table 1, App. I Table I.19.
- 2502.14911 Batayan: Table 1, §2–3 (native re-translation of FLORES/Belebele), App. (MT uses the FLORES-200 Filipino subset).
- 2606.19348 DeepSeek-V4 (local plus full PDF): §4.1. 2609.19969 DeepSeek-V4.1-Flash (local md truncated at 30/51 pages; full PDF searched): §4.1.
- 2412.19437 DeepSeek-V3: §4.1 ("expanding multilingual coverage beyond English and Chinese"; no decontamination statement found).
- 2603.25222 FRED (via `pwc paper read`): §2.2, §3.2–3.4, App. E.1, App. G.
- 2207.04672 NLLB (v3 PDF): §4.1.1, §4.1.3.
- 2106.03193 FLORES-101: language table (ceb, tgl).
- 2308.16884 Belebele: §3.5, Limitations, Ethics.
- 2010.06354 Tatoeba Translation Challenge: §1, Fig. 3, participation rules.
- 2010.11934 mT5: §2. 2506.20920 FineWeb2: §1, §5. 2309.09400 CulturaX: §1. 2503.10267 HPLT v2: §4.1, §6.
- 2005.14165 GPT-3: §4, App. C. 2411.03923 ConTAM: §1, §3.1, §5. 2406.13236 cross-lingual contamination. 2407.21530 CONDA 2024 report: Tables 1–2.
- 2501.18771 Kocyigit et al.: abstract, §1, §5.5.
- 2502.04314 BOUQuET: §3, language table. 2010.11574 NewsPH-NLI: §3. 2508.20511 FLORES+ quality re-evaluation. 2608.09766 Cultivar (FLORES overfitting via localisation).

**Web / API:**
- HF dataset API `https://huggingface.co/api/datasets/{name}` for: openlanguagedata/flores_plus, facebook/flores, facebook/belebele, mteb/NTREX, Helsinki-NLP/tatoeba_mt, Helsinki-NLP/opus-100, aisingapore/kalahi, aisingapore/{NLG-Machine-Translation, Cultural-Evaluation-Kalahi, NLU-Question-Answering, NLR-NLI, NLR-Causal-Reasoning, NLU-Sentiment-Analysis, NLG-Abstractive-Summarization}, allenai/MADLAD-400, HuggingFaceFW/fineweb-2, uonlp/CulturaX, HPLT/HPLT2.0_cleaned, allenai/nllb, allenai/c4, gsarti/flores_101, Muennighoff/flores200, gmnlp/tico19, davidstap/NTREX.
- `https://huggingface.co/datasets/allenai/nllb/raw/main/README.md`
- `https://datasets-server.huggingface.co/size?dataset=gmnlp/tico19`
- OPUS API `https://opus.nlpl.eu/opusapi?source=..&target=..&preprocessing=moses&version=latest`
- `https://raw.githubusercontent.com/facebookresearch/fairseq/nllb/examples/nllb/data/download_parallel_corpora.py`
- GitHub API: `repos/MicrosoftTranslator/NTREX`, `repos/aisingapore/SEA-HELM` (tree, translation and Kalahi configs).
- Common Crawl index `https://index.commoncrawl.org/CC-MAIN-2022-33-index`, `…/CC-MAIN-2024-10-index`, `collinfo.json`.
- `https://tico-19.github.io/index.html`

---

## 5. Papers worth adding to the reference registry (not added; `seed.json` untouched)

- **2207.04672**: NLLB. Defines FLORES-200 splits, with the test split hidden.
- **2106.03193**: FLORES-101. Tagalog/Cebuano FLORES public since 2021.
- **2308.16884**: Belebele. Passages reuse FLORES dev/devtest; authors warn about crawl contamination.
- **2010.06354**: Tatoeba Challenge. Documents test–train overlap in OPUS.
- **2502.14911**: Batayan. The SEA-HELM Filipino data, natively re-translated.
- **2603.25222**: FRED metrics. The task assumed a local copy; none exists.
- **2501.18771**: Controlled study of contamination in MT (the 30-BLEU inflation; the language-representation threshold).
- **2411.03923**: ConTAM. Longest-match n-gram, small n.
- **2406.13236**: Cross-lingual contamination. Relevant to translated Filipino benchmarks.
- **2407.21530**: CONDA 2024 contamination database. FLORES in xP3 and several models.
- **2005.14165**: GPT-3. The 13-gram clean-subset convention.
- **2502.04314**: BOUQuET. Hand-written, hidden-eval MT benchmark including Tagalog.
- **2506.20920 / 2309.09400 / 2503.10267 / 2010.11934**: FineWeb2 / CulturaX / HPLT v2 / mT5. Crawl windows of candidate corpora.
- **2412.19437**: DeepSeek-V3. V4 inherits its data preprocessing.
- **2406.10118**: SEACrowd. A catalogue of SEA and PH datasets for finding further eval sets.
- **2010.11574**: NewsPH-NLI. A news-scraped FilBench component.
- **2608.09766**: Cultivar. Evidence of FLORES overfitting.

---

## 6. Search appendix (search protocol record, DILIGENCE #2)

All searches were run 2026-09-24. Tools: `pwc` = Papers with Code CLI; WS = WebSearch; WF = WebFetch; curl; gh; grep = local text search.

| # | Tool | Query / target | Result used? |
|---|---|---|---|
| 1 | grep (local md) | `contamina\|13-gram\|leak\|memoriz` in 2309.04662, 2508.03523, 2409.15380, 2502.14301, 2606.19348, 2609.19969, 2601.07372 | Yes (MADLAD §5; no statements elsewhere) |
| 2 | grep (local md) | FLORES/NTREX/Tatoeba/OPUS/crawl terms in 2309.04662 | Yes |
| 3 | grep (local md) | FilBench, Kalahi, SEA-HELM dataset tables and licences | Yes |
| 4 | grep (local md) | DeepSeek V4/V4.1 data-construction sections | Yes |
| 5 | pwc | `paper info 2603.25222 --json`; `paper read 2603.25222` | Yes (FRED) |
| 6 | curl | HF API for 16 dataset IDs (FLORES, Belebele, NTREX, Tatoeba, Kalahi, MADLAD, FW2, CulturaX, HPLT, NLLB, C4) | Yes |
| 7 | curl | HF card metadata (gating terms) for flores_plus, facebook/flores, tatoeba_mt, CulturaX; Belebele configs | Yes |
| 8 | WF | arxiv.org/pdf/2309.04662v2 | Failed (404; only v1 exists) |
| 9 | curl + pdftotext | arXiv PDF 2309.04662 (v1) | Yes (App. A.5, A.9) |
| 10 | WS | `NLLB "No Language Left Behind" training data remove sentences FLORES-200 dev devtest overlap filtering` | Pointed to the allenai/nllb README; no explicit decontamination found |
| 11 | curl + pdftotext | allenai/nllb README; arXiv 2207.04672v3 PDF | Yes |
| 12 | curl + pdftotext | arXiv 2506.20920, 2309.09400, 2503.10267, 2010.11934 | Yes |
| 13 | curl + pdftotext | arXiv 2308.16884, 2502.14911, 2010.06354 | Yes |
| 14 | curl | OPUS API (first attempt; redirect error), then corpus listings for en-tl, ceb-en, en-ilo, en-war, en-fil, en-hil, en-pag, en-pam, bcl-en | Yes |
| 15 | gh | `repos/aisingapore/SEA-HELM` (metadata, tree, translation and Kalahi config.yaml) | Yes |
| 16 | curl | HF API for aisingapore SEA-HELM datasets; HF search `filbench, batayan, kalahi, tico, tatoeba_mt, ntrex` | Yes |
| 17 | gh | `repos/MicrosoftTranslator/NTREX` (metadata, tree) | Yes |
| 18 | curl | HF card `0x22almostEvil/tatoeba-mt-qna-oa` | Noted only: Tatoeba repackaged as instruction data; PH coverage unknown; not used in verdicts |
| 19 | pwc | `data contamination machine translation FLORES` | Yes (2608.09766, 2508.20511) |
| 20 | pwc | `benchmark contamination detection n-gram overlap pretraining` | Yes (2310.18018, 2411.03923, 2406.13236, 2311.04850) |
| 21 | pwc | `cross-lingual data contamination translated benchmark` | Yes (2406.13236) |
| 22 | pwc | `contamination metrics evaluation data how to measure ConTAM` | Yes (2411.03923, 2407.21530) |
| 23 | pwc | `Filipino Tagalog benchmark evaluation` | Yes (confirms FilBench; 2203.17225 noted) |
| 24 | pwc | `Philippine languages machine translation test set` | Nothing new PH-specific |
| 25 | pwc | `Cebuano Ilocano Hiligaynon dataset` | Noted 2311.07161, 2310.00679 (NER; not MT eval) |
| 26 | pwc | `paper read` 2508.20511, 2608.09766, 2407.21530, 2411.03923, 2406.13236 | Yes |
| 27 | WS | `Overestimation in LLM Evaluation controlled large-scale study data contamination impact on machine translation arXiv` | Yes (2501.18771) |
| 28 | pwc / WF / curl | 2501.18771: pwc read (empty), WF of HTML (summary partly garbled: model sizes misreported), PDF via curl (verified) | Yes (from PDF only) |
| 29 | curl + pdftotext | arXiv 2005.14165 (GPT-3), 2412.19437 (DeepSeek-V3), 2106.03193 (FLORES-101) | Yes |
| 30 | curl | HF API: gsarti/flores_101, Muennighoff/flores200, gmnlp/tico19, davidstap/NTREX; CC collinfo | Yes |
| 31 | curl | CC index (CC-MAIN-2022-33, CC-MAIN-2024-10): flores GitHub, HF mirrors, NTREX GitHub/raw, tico-19.github.io, tatoeba.org. First run URL-encoded wrongly (all 0); re-run correctly | Yes (§1.4) |
| 32 | curl | CC index tatoeba.org sentence pages, pages 0–5, both snapshots | Yes (0 status-200) |
| 33 | WS | `Philippine languages benchmark LLM evaluation Cebuano Ilocano Hiligaynon Bikol Kapampangan test set 2025 2026 arXiv` | Only FilBench/Batayan found |
| 34 | pwc | `Tagalog English machine translation evaluation dataset` | Yes (2502.04314 BOUQuET) |
| 35 | pwc | `Filipino natural language inference dataset` | Yes (2010.11574) |
| 36 | pwc | `Southeast Asian languages benchmark SEACrowd` | Yes (2406.10118 for registry) |
| 37 | pwc | `Philippine languages large language model` | Noted 2111.06053, 2509.02160; not used |
| 38 | pwc | `paper read 2502.04314`, `paper read 2010.11574` | Yes |
| 39 | curl | HF API Helsinki-NLP/opus-100 configs; OPUS WikiMatrix en-war | Yes (no PH pairs in OPUS-100) |
| 40 | curl | fairseq nllb `download_parallel_corpora.py` | Yes (TICO-19 tl downloaded; no Tatoeba) |
| 41 | curl | datasets-server size for gmnlp/tico19; tico-19.github.io | Yes (971 / 2,100) |
| 42 | curl + pdftotext | arXiv 2609.19969 and 2606.19348 full PDFs | Yes (no contamination statements) |
| 43 | pwc | `MultiLoKo multilingual local knowledge benchmark` | Failed (SSL timeout); Tagalog coverage left unknown |
