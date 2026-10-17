# A6 · Metric-validity review: which translation metrics can DiaGrad trust for Philippine languages?

Diligence item #12 (`research/DILIGENCE.md`, T2 "Evaluation validity for Philippine languages").
Desk research only. Every source was retrieved on **2026-09-24**, unless a line says otherwise.
Language codes used below: Tagalog/Filipino (tl / fil / tgl), Cebuano (ceb), Ilocano (ilo),
Hiligaynon (hil), Waray (war), Bikol (bcl), Kapampangan (pam), Pangasinan (pag).

Labels used throughout:
- **[source-stated]**: the cited source says this directly (arXiv ID + section, or URL).
- **[inference]**: my reasoning from sourced facts. It is not stated anywhere as such.
- **[unknown]**: I could not verify this. The report does not guess.
- **[proposal]**: a design suggestion for DiaGrad. It needs a decision before use.

---

## 1. Plain-language summary

### Findings

1. **No published study has checked any automatic translation metric against human judgments for any
   Philippine language.** I searched Papers with Code, the web and Hugging Face (Appendix A). I found no
   dataset in which native speakers score machine translations for Tagalog, Cebuano, Ilocano or the others,
   and no paper that reports how BLEU, chrF, COMET, MetricX or an LLM judge agrees with such scores
   [unknown → negative search result]. The nearest things that do exist:
   - **WMT24++** gives English→Filipino (`en-fil_PH`) references and post-edits (Apache-2.0). Its authors
     rank systems with automatic metrics only and say "These results should be confirmed using a
     human-based evaluation, which we leave for future work" (arXiv 2502.12404, Abstract) [source-stated].
   - The **WMT 2021 large-scale multilingual task** included Tagalog, but scored it with spBLEU on
     FLORES-101 (Findings of WMT21 LSMT, aclanthology.org/2021.wmt-1.2, §2 and §5.3). I found no human
     evaluation of Tagalog in the extracted text [source-stated for spBLEU; inference for "no human
     evaluation"].
   - **WMT25** has no Philippine language in any track (statmt.org/wmt25/translation-task.html)
     [source-stated].
   - The Filipino benchmarks **Batayan** (2502.14911, §5.1) and **SEA-HELM** (2502.14301, Table 1) score
     Filipino translation with MetricX-24 (Batayan also uses chrF++). **FilBench** uses ROUGE-L
     (2508.03523, §3.3). None of the three shows that its metric agrees with Filipino speakers' judgments of
     translation quality [inference from reading their metric sections].

2. **Most learned metrics were never pretrained on most Philippine languages.** A learned metric such as
   COMET is a neural network built on a multilingual "encoder" (a model pretrained to read text in many
   languages). The metric is then taught to predict human quality scores. If the encoder never saw a
   language during pretraining, the metric is guessing about text it cannot really read. COMET's own
   documentation says: "results for language pairs containing uncovered languages are unreliable!"
   (github.com/Unbabel/COMET README, "Languages Covered") [source-stated]. Coverage by encoder:
   - Encoders behind COMET-22, xCOMET and CometKiwi: **Tagalog only**.
   - Encoder behind MetricX: **Filipino and Cebuano**.
   - Encoder behind BLEURT-20: **Filipino and Cebuano**.
   - None of these encoders covers **Ilocano, Hiligaynon, Waray, Bikol, Kapampangan or Pangasinan**.

   Details and sources are in §3.

3. **The closest comparable evidence comes from African and Indian low-resource languages, and it is
   sobering.**
   - **AfriCOMET** (2311.09828, §3.2.1, Table 2): average sentence-level Spearman correlation with human
     scores across 13 African language pairs.

     | Metric | Average Spearman |
     |---|---|
     | BLEU | 0.237 |
     | chrF++ | 0.277 |
     | COMET-22 | 0.328 |
     | GPT-4 | 0.383 |
     | AfriCOMET (best) | 0.441 |

     [source-stated]
   - **SSA-COMET** (2506.04557, §5.3, Table 3): 14 African language pairs, average Spearman.

     | Metric | Average Spearman |
     |---|---|
     | BLEU | 0.387 |
     | chrF++ | 0.498 |
     | COMET-22 | 0.366 |
     | MetricX-24 | 0.567 |
     | Gemini-2.5-Pro, 5-shot | 0.633 |
     | SSA-COMET-MTL | 0.639 |

     [source-stated]. **Here chrF++ beat COMET-22.** A plain character-overlap metric can do better than a
     learned metric whose encoder does not know the language [inference].
   - **Four low-resource Indian languages** (Assamese, Maithili, Kannada, Punjabi; 2406.03893, Abstract and
     Table 1): the best learned metrics reach only Kendall τ ≈ 0.32 and Pearson ≈ 0.45 at segment level.
     GEMBA-MQM, an LLM-judge method, averaged Kendall τ 0.178, well below CometKiwi-XL at 0.309
     [source-stated].

   **Practical meaning:** even the best metrics in these settings agree only weakly to moderately with
   native speakers on individual sentences. Agreement also varies widely from language to language
   [inference].

4. **LLM judges are promising but cannot yet stand in for native speakers here.**
   - GEMBA-MQM's authors "advise caution when using it in academic works to demonstrate improvements"
     (2310.13988, Abstract, §5). They also say they "cannot conclude if the method will perform well on
     low-resource languages" (Limitations) [source-stated].
   - SSA-COMET found that LLM judges did much worse without five in-context examples. Asking the LLM to mark
     error spans before scoring *lowered* its correlation: Gemini-2.5-Pro's Spearman fell from 0.633 to
     0.595 (2506.04557, §5.3 "Impact of Error Span Prediction on LLMs") [source-stated].
   - GPT-4 judges were biased toward high scores (2309.07462, Abstract). That study covered 8 mostly
     high-resource languages, not truly low-resource ones [source-stated].

5. **Human error labels themselves are noisy, and this matters directly for the critic's named
   categories.** In the ESA paper, the *same* MQM annotator re-annotating the same documents two months
   later marked an overlapping error only 30% of the time. When the same severity and category were also
   required, this fell to **8.4%** (2406.11580, §6.4, Table 6) [source-stated]. So when a critic is scored
   against human category labels, its measured accuracy is limited by how consistent the humans
   themselves are [inference].

6. **A metric the model was optimised for stops being a fair judge of that model.**
   - In quality-aware decoding, systems explicitly optimised for a learned metric scored well on that
     metric. But "their correlation with human judgments decreases and they are no longer reliable
     indicators of system-level ranking" (2205.00978, §4.2.4) [source-stated].
   - For CAMOE, if the critic is trained on, distilled from, or selected with metric X, then metric X cannot
     be the evidence that CAMOE is better [inference].

### Why this matters for DiaGrad

A paper that says "CAMOE improves Philippine-language translation" must show three things:

1. The improvement is real, not a side effect of a metric's blind spots.
2. It holds for each language, not only for Tagalog.
3. The critic's named error categories mean what they say.

**What automatic metrics can support:**
- For **Tagalog/Filipino**: supporting evidence from chrF++ plus MetricX-24 and COMET-22, but only after
  we check them against our own native-speaker scores.
- For **Cebuano**: chrF++ plus MetricX-24, with the same check.
- For **Ilocano, Hiligaynon, Waray, Bikol, Kapampangan and Pangasinan**: only chrF++ as a rough signal.
  **Human evaluation is the only real evidence** for these languages.

**What we still need:**
- **The human evaluation is the main evidence, not an optional extra.** It must also produce error
  *categories*, because the critic has to be judged on its named categories (DILIGENCE #6).
- **A small "metric validation" study on DiaGrad's own held-out set (D5).** Before trusting any automatic
  metric for a language, measure how well it agrees with native speakers on that language, and put that
  next to how well the speakers agree with each other (2604.17393, Abstract, recommends this comparison)
  [inference + source-stated].

### What we know vs. what we don't know

| Status | Statement |
|---|---|
| **Directly verified** | Which languages each encoder covers (paper tables and Hugging Face model cards, §3). The metric licences on the model cards. The correlation numbers quoted for African and Indian languages. That WMT24++, SEA-HELM and Batayan use MetricX-24 for Filipino. That WMT25 has no Philippine language |
| **Strongly suggested** | Learned metrics are unreliable for Ilocano, Hiligaynon, Waray, Bikol, Kapampangan and Pangasinan, because their encoders never saw those languages and their developers call such results unreliable. chrF++ is the safest common automatic metric across all Philippine languages, because it depends on no encoder and it did as well as or better than BLEU in every comparable study found |
| **Hypothesis** | That MetricX-24 and COMET-22 track human judgment reasonably well for Tagalog, as they do for other covered mid-resource languages. Plausible, but untested |
| **Unknown** | The actual correlation of any metric with human judgment for any Philippine language. Whether LLM judges understand Waray, Pangasinan and the other smaller languages. How well humans agree with each other on Philippine-specific categories such as verb voice ("focus") and politeness markers |

**One correction to our own records.** `seed.json` summarises FRED (2603.25222) as "much of the variation
in low-resource MT scores comes from train-test overlap and pretraining exposure". The abstract does say
this. But the paper's own regression (§3.3, Table 3) finds that the pretraining-exposure score explains
almost nothing (R² = 0.0142), while train–test similarity explains most (R² = 0.582). The paper concludes
"pre-training data contamination is not the most significant issue" in its setting [source-stated]. The
registry note should say "train–test overlap (R-score)", not "pretraining exposure". I have not edited
`seed.json`, as instructed.

---

## 2. Concepts in one place (read once, then skip)

- **Reference-based vs. reference-free metrics.**
  - A *reference-based* metric compares the system's translation with a human "reference" translation:
    BLEU, chrF, COMET-22, MetricX-24 (hybrid mode), BLEURT.
  - A *reference-free* metric, also called **quality estimation (QE)**, looks only at the source and the
    translation: CometKiwi, xCOMET-QE, MetricX-24-QE, GEMBA-MQM.
  - QE does not depend on reference quality. But it depends even more on the model understanding *both*
    languages [inference].
- **Correlation with human judgment.** Humans score many translations, the metric scores the same ones,
  and we measure how well the two lists agree.
  - *Segment level* asks whether the metric picks the better sentence (Kendall τ, Spearman ρ, Pearson r).
  - *System level* asks whether the metric ranks whole systems in the right order. **Pairwise accuracy**
    is the share of system pairs ordered the same way as by humans (2310.13988, §3.2).
  - Pearson on few systems is fragile: in MQM23 it rests on "as little as 12 systems" (2310.13988, §3.2)
    [source-stated].
- **Human evaluation protocols.**
  - **DA (Direct Assessment):** a 0–100 score per translation. Cheap, but noisy.
  - **MQM (Multidimensional Quality Metrics):** trained annotators mark each error span and give it a
    category (accuracy/mistranslation, fluency/grammar, …) and a severity (minor/major/critical). An
    error-weighted score follows. WMT weights are 1/5/25 (2310.13988, §1).
  - **ESA (Error Span Annotation):** annotators mark error spans with severity only (no category), then
    give a 0–100 score (2406.11580, §4).
- **Inter-annotator agreement (IAA).** How much two people agree on the same items. It sets the ceiling:
  no metric or critic can be shown to agree with "humans" better than humans agree with each other
  (2604.17393, Abstract, recommends reporting metric agreement *relative to* IAA) [source-stated + inference].

---

## 3. Which Philippine languages each metric's encoder covers

| Metric | Underlying pretrained model | Evidence of coverage | tl/fil | ceb | ilo | hil | war | bcl | pam | pag |
|---|---|---|---|---|---|---|---|---|---|---|
| COMET-22 (`Unbabel/wmt22-comet-da`) | XLM-R large | XLM-R paper 1911.02116, App. A, Table 6: "tl Filipino", 556M tokens / 3.1 GiB, the only Philippine language among its 100. Hugging Face card language list contains `tl` only | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| xCOMET-XL/XXL | XLM-R XL / XXL (2310.10482, §4.1) | Same CC-100 languages as XLM-R [inference]. Hugging Face card lists `tl` | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| CometKiwi-22 | InfoXLM large (COMET README) | InfoXLM uses CC-100 filtered to 94 languages above 0.1 GB (2007.07834, §4 "Corpus"). Filipino has 3.1 GiB, so it is kept [inference]. Card lists `tl` | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| CometKiwi-23 XL/XXL | XLM-R XL / XXL (COMET README) | Card lists `tl` | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| MetricX-23 / MetricX-24 | mT5 (github.com/google-research/metricx README) | mT5 paper 2010.11934, Table 6 (mC4): `fil` Filipino 2.1B tokens, 0.62% of mT5 training data; `ceb` Cebuano 0.2B tokens, 0.36%. No other Philippine language | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| BLEURT-20 | RemBERT (github.com/google-research/bleurt checkpoints.md) | `google/rembert` card language list includes `fil`, `ceb` (104 codes). RemBERT is pretrained on 110 languages (2010.12821, App.) | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| BLASER 2.0 (SONAR-based) | SONAR encoders | SONAR text covers tgl, ceb, ilo, pag, war (`data/DATA-PLAN.md` context line; not re-verified here) [unknown / to verify]. Licence CC-BY-NC-4.0 (HF card) | ✓? | ✓? | ✓? | ✗? | ✓? | ✗? | ✗? | ✓? |
| BLEU / chrF / chrF++ | none (string matching) | Works on any Latin-script text. Quality then depends on the reference and on spelling variation [inference] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| spBLEU (FLORES-200 SentencePiece) | shared subword tokenizer | FLORES+ (HF `openlanguagedata/flores_plus`, CC-BY-SA-4.0, gated) has configs `fil_Latn`, `ceb_Latn`, `ilo_Latn`, `pag_Latn`, `war_Latn`. No hil, bcl, pam [source-stated]. The tokenizer is presumably trained on those languages [inference] | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✓ |
| LLM judges (GEMBA-MQM, AutoMQM, others) | the LLM used | Coverage depends on the LLM's undisclosed training data | ? | ? | ? | ? | ? | ? | ? | ? |

Notes.
- **"Covered" does not mean "validated".** None of these metrics was *trained on human quality scores*
  for any Philippine language.
  - COMET-22 and CometKiwi-22 were trained on WMT direct assessments from 2017–2020 (COMET README).
  - MetricX-24 was trained on WMT DA and MQM data from 2015–2022 (MetricX README, "Changes to the WMT'24
    Submission").
  - WMT news tasks in those years had no Philippine language pairs [inference; I did not audit every WMT
    year's language list].
  - So even for Tagalog, these metrics score the language "zero-shot": they were never trained on its
    quality scores [inference].
- **Coverage is thin even where it exists.** Cebuano is 0.36% of mT5's pretraining mix, Filipino 0.62%
  (2010.11934, Table 6) [source-stated].
- **Licences matter for DiaGrad's own use** (see A2 licence audit).
  - COMET-22: Apache-2.0.
  - MetricX-24: Apache-2.0.
  - RemBERT: Apache-2.0.
  - xCOMET-XL, CometKiwi-22 and CometKiwi-23-XL: CC-BY-NC-SA-4.0 and gated.
  - BLASER 2.0: CC-BY-NC-4.0.

  All from Hugging Face API model cards [source-stated]. the licence rules in `research/licenses/LICENSES.md` already forbids
  non-commercial components inside the model and names CometKiwi and xCOMET as excluded *training
  signals*. They may still serve as research-only *evaluation* cross-checks, subject to the A2 audit
  [inference from the rule's wording].

---

## 4. Metric × evidence table

"PH evidence" = evidence specific to Philippine languages. "Comparable evidence" = low-resource languages
elsewhere.

| Metric | What it measures | PH evidence | Comparable low-resource evidence | Known failure modes | Verdict for DiaGrad |
|---|---|---|---|---|---|
| **BLEU / SacreBLEU** | Word n-gram overlap with a reference | Used for Cebuano→Tagalog NMT (arXiv 1902.07250, BLEU 20.01; search snippet only) [source-stated, secondary]. No human validation | Lowest correlation of all metrics in AfriCOMET (avg Spearman 0.237) and SSA-COMET (0.387). In the Indic zero-shot study, SacreBLEU averaged Kendall 0.119 (2406.03893, Table 1) [source-stated]. WMT22 findings are titled "Stop using BLEU" (cited in 2310.13988 refs) | Penalises valid paraphrases. Rewards copying named entities: "simple heuristics, such as copying named entities, can yield non-trivial BLEU" on FLORES+ (2508.20511, Abstract) [source-stated]. Sole use "impeded the development of improved models" (2107.10821, Abstract) | Report only for comparison with older Philippine MT papers. **Never as evidence** |
| **spBLEU** | BLEU after a shared multilingual subword tokenizer (introduced with FLORES-101, 2106.03193) | WMT21 LSMT ranked Tagalog systems with spBLEU (2021.wmt-1.2, §2.2 and §5.3) [source-stated] | "often achieve worse correlation to human judgements" than embedding and learned metrics (2311.09828, §1, citing WMT22) [source-stated] | Same as BLEU | Comparison only |
| **chrF / chrF++** | Character n-gram F-score (++ adds word bigrams) | Batayan reports chrF++ for eng↔fil (2502.14911, §5.1) without validation | Better than BLEU in every comparable study: AfriCOMET 0.277 vs 0.237; SSA-COMET 0.498 vs 0.387. SSA-COMET: above COMET-22 (0.498 vs 0.366). Indic: Kendall 0.180 vs SacreBLEU 0.119, but below learned metrics [source-stated]. FRED: variability also shows up in chrF, and scores depend on train–test overlap (2603.25222, §1, §3.3) | Still lexical. Cannot tell a wrong-meaning sentence that shares characters from a correct one [inference]. Closely related Philippine languages share many character n-grams, so output in the **wrong** Philippine language may still get partial credit [inference, untested] | **Primary automatic metric for all eight languages**, always with human evaluation. Report the sacreBLEU signature |
| **COMET-22** | XLM-R regression on (source, translation, reference), trained on WMT DA | Encoder covers Tagalog only | AfriCOMET avg Spearman 0.328; SSA-COMET 0.366 (below chrF++) [source-stated]. Indic zero-shot: COMET-DA Kendall 0.245 (Table 1) | "results for language pairs containing uncovered languages are unreliable!" (COMET README). "not sensitive enough to discrepancies in numbers and named entities" (2202.05148, Abstract). Optimising for it makes it unreliable (2205.00978, §4.2.4) [source-stated] | Secondary metric for **Tagalog only**, after validation on D5. Do not report for other Philippine languages |
| **CometKiwi-22 / -23 (QE)** | Reference-free regression (InfoXLM / XLM-R XL) | Covers Tagalog only | AfriCOMET QE table: CometKiwi weak for several African pairs (e.g. eng-ibo Spearman 0.188) (2311.09828, §4 table) [source-stated]. Indic: CometKiwi-XL was the best off-the-shelf metric (Kendall 0.309) | Scale compression: "Comet QE 22 ranges from 60% to 80% across most translations" (2609.04173, related-work paragraph "Translation evaluation") [source-stated]. QE metrics are "biased against human translations" (2502.12404, §3.1, App. D) [source-stated] | Evaluation-only cross-check for Tagalog. **Never a training, reranking or critic signal**: non-commercial licence (CC-BY-NC-SA-4.0, gated), and the licence rules in `research/licenses/LICENSES.md` excludes CometKiwi and xCOMET as training signals |
| **xCOMET-XL/XXL** | Score plus error spans with severity (minor/major/critical); no error categories (2310.10482, §4) | Covers Tagalog only | No low-resource correlation study found. The authors say it would be "interesting to explore whether these trends hold for … low-resource ones" (2310.10482, §7) [source-stated] | Spans have severity but no *category*, so it cannot directly check the critic's named categories [inference]. CC-BY-NC-SA | Optional, for Tagalog, **evaluation only** (same licence rule as CometKiwi). A useful baseline span detector against which to compare the critic's spans |
| **MetricX-23 / -24** | mT5 regression to MQM-like 0–25 error score. Hybrid mode works with or without a reference | Used by SEA-HELM and Batayan for Filipino; WMT24++ for `fil_PH` (all without human validation) [source-stated] | SSA-COMET: MetricX-24 avg Spearman 0.567, the best regression metric not trained on African data (Table 3) [source-stated] | Its README lists failure modes it had to add synthetic data for: "Undertranslation", "Overtranslation", "Fluent but unrelated translation", "Gibberish", missing punctuation (MetricX README, "Synthetic Data") [source-stated]. So models without that data miss these cases [inference]. Biased against human translations (WMT24++ §3.1) | **Best candidate secondary metric for Tagalog and Cebuano** (Apache-2.0; mT5 covers both). Validate on D5 first |
| **BLEURT-20** | RemBERT regression, fine-tuned on WMT 2015–19 ratings plus synthetic data (checkpoints.md) | Kalahi (2409.15380, §4.2) uses BLEURT on Filipino cultural *generation*, not translation | Indic zero-shot: Kendall 0.250, Pearson 0.366 (2406.03893, Table 1) [source-stated] | Same zero-shot concern | Optional alternative for Tagalog/Cebuano. Low priority |
| **BLASER 2.0** | SONAR-embedding metric (ref / QE) | None found | None found in this search [unknown] | Non-commercial licence | Not recommended as evidence. Its SONAR language coverage is worth a later check [unknown] |
| **GEMBA-MQM** | GPT-4 prompted with 3 fixed examples to list MQM errors | None | System-level SOTA on WMT23 high-resource pairs (96.5% pairwise accuracy, Table 1). Indic low-resource: Kendall 0.178, below learned metrics (2406.03893, Table 1) [source-stated] | Proprietary drift and possible test-set contamination (2310.13988, §5). Misused an error class: "locale convention" took 32% of all errors until removed (§4.3, Table 5) [source-stated] | Do not use as evidence. Its prompt (Fig. 1) is a useful template for the critic's output format |
| **AutoMQM** | PaLM-2 prompted to produce MQM spans + categories | None | First LLM-judge test on low-resource pairs (en↔gu, en↔kk, WMT19 DA): "promising, but lags behind state-of-the-art learned metrics" (2308.07286, §1 contributions, §6.3) [source-stated] | "over-predict errors … ~5 words per span vs ~2 words in the ground truth" and low span precision (§6.3/Table 6) [source-stated] | Method reference for evaluating span-level critics: span precision, major recall, MCC (§6.1) |
| **LLM judges in general** | Any LLM asked for a score or error list | None | SSA-COMET: Gemini-2.5-Pro 5-shot is the best judge (0.633), much worse zero-shot (App. H), and worse when asked for spans first (0.595) [source-stated]. ITEM (6 Indian languages): LLM evaluators align best with humans (2510.07061, Abstract) [source-stated] | Bias toward high scores; needs calibration "with a set of human-labeled judgments in each language before deployment" (2309.07462, §5) [source-stated]. Tested languages in that study were not low-resource | Third opinion only: open weights, pinned version, few-shot with Philippine examples, calibrated on D5 |
| **FilBench ROUGE-L** | Longest-common-subsequence overlap | FilBench generation score (2508.03523, §3.3) | none | Lexical; similar limits to BLEU [inference] | Not recommended for MT claims |

---

## 5. Known failure modes to design against

Each item says what goes wrong, why DiaGrad should care, and the source.

1. **Fluent but wrong output scores too well.**
   - COMET misses number and named-entity errors (2202.05148, Abstract).
   - MetricX needed synthetic training data to catch "fluent but unrelated" translations (MetricX README).
   - Consequence for CAMOE: a critic trained against such a metric inherits its blind spots [inference].
2. **Optimising for the metric breaks the metric.** Explicit optimisation lowers the metric's agreement
   with humans (2205.00978, §4.2.4) [source-stated]. CAMOE's critic may itself act as a learned quality
   signal. So **the evaluation metric must be independent of anything used in training, reranking or
   critic distillation** [inference / proposal].
3. **Language not covered by the encoder.** Reported by COMET's own README. AfriCOMET: "the performance of
   these approaches is often unpredictable for languages that were not included in the pre-training
   phase" (2311.09828, §1) [source-stated].
4. **Test data seen during training.**
   - Proprietary LLM judges may have seen any published test set (2310.13988, §5) [source-stated].
   - FRED shows that train–test similarity (R-score) explains 58% of score variance in extremely
     low-resource MT (2603.25222, §3.3). A nearest-neighbour "retrieval" baseline sometimes beats the
     neural systems (§3.4) [source-stated].
   - Links to A5 (contamination check).
5. **Weak references and "translationese".**
   - Batayan re-translated the Filipino FLORES-200 set. The reason: earlier translations "were unnatural,
     disfluent, and showed characteristics of translationese" and overused *ay*-inversion (2502.14911,
     §2.2, §4.1, Table 1) [source-stated].
   - Human checks of FLORES+ in four other languages found many translations below the claimed quality
     bar (2508.20511, Abstract) [source-stated].
   - Consequence: a reference-based metric scored against a stiff reference rewards stiff output
     [inference].
6. **Wrong target language.**
   - FilBench found models "generate translations in an incorrect target language". In 100 GPT-4o
     failures, poor instruction-following was 34%, overgeneration 47% and hallucination 19% (2508.03523,
     §5.2, Table 4) [source-stated].
   - For eight related Philippine languages, *which* language comes out needs a separate check: a
     language-ID test plus a named error category [proposal].
7. **Bias against human translations.** QE metrics score human translations lower than human evaluators
   do (2502.12404, §3.1, App. D) [source-stated]. Do not claim "super-human" from metrics.
8. **Domain shift.** Metric–human agreement drops on unseen domains once human label variation is taken
   into account. There, human–human agreement was 0.96 against metric–human 0.78–0.83 (2604.17393,
   Abstract) [source-stated].
9. **Too few systems or segments.**
   - System-level Pearson with a dozen systems is fragile (2310.13988, §3.2) [source-stated].
   - A Hausa/Fongbe study reports ρ = 1.0 for Fongbe and 0.5 for Hausa at system level, with humans
     preferring a different system than all metrics chose for Hausa (2606.22269, Abstract via arXiv page)
     [source-stated]. With only a handful of systems, ρ = 1.0 carries little information [inference].
10. **Embedding collapse.** BERTScore gave within-language similarity above 0.99 for Hausa/Fongbe, so it
    could not separate good from bad (2606.22269, Abstract) [source-stated].
11. **LLM judges misuse categories.** GEMBA's "locale convention" class was applied to correct
    translations and took 32% of all errors (2310.13988, §4.3) [source-stated]. **Every error category
    the critic uses must be tested for whether annotators, and the critic, apply it consistently**
    [inference].

---

## 6. Recommended evaluation protocol

### 6.1 Automatic metrics [proposal]

| Tier | What | For which languages | Why |
|---|---|---|---|
| Always report | **chrF++** (sacreBLEU, signature published) | All | Needs no encoder; as good as or better than BLEU in every comparable study; cheap |
| Secondary, after validation | **MetricX-24 hybrid** (Apache-2.0) | tl/fil, ceb | mT5 covers both; strongest non-adapted regression metric in SSA-COMET |
| Secondary, after validation | **COMET-22** (Apache-2.0) | tl/fil only | Most widely reported; XLM-R covers Tagalog only |
| Comparability only | BLEU / spBLEU | Where prior Philippine work reports them | Older papers (WMT21 LSMT, Cebuano→Tagalog NMT) use them |
| Third opinion | Open-weight LLM judge, pinned version, few-shot with Philippine examples | Any, flagged as unvalidated | Only after calibration against D5 (2309.07462, §5) |
| Test-set difficulty | **FRED R-score and token fertility** per test set | All | Shows whether a high score reflects train–test overlap (2603.25222, §2.2) |
| Language check | Language-ID on outputs | All | Catches wrong-target-language outputs (FilBench §5.2) |

**Rules** [proposal]:
- No metric used in training, reranking, early stopping or critic distillation is used as evaluation
  evidence (2205.00978, §4.2.4).
- Report per language, never only a pooled number (`data/DATA-PLAN.md`, "Balance and reporting").
- Learned-metric numbers for languages outside the encoder are either not reported or clearly marked
  "unvalidated".
- **Metric validation study.** On a D5 subset per language, collect human scores (§6.2). Compute per
  metric:
  - segment-level Kendall τ (the tie-aware variants used in WMT; 2310.13988 cites Deutsch et al. 2023);
  - system-level pairwise accuracy (2310.13988, §3.2).

  Place each value next to the human–human agreement (2604.17393). A metric counts as "validated for
  language L" only above a threshold fixed *before* seeing results [proposal; threshold value
  deliberately left blank for the preregistration, DILIGENCE #1].
- For score-difference thresholds, Kocmi et al. 2024 (2401.06760, Abstract) estimate how big a metric
  difference must be before humans notice it. Their data are high-resource, so their numbers should not
  be transferred to Philippine languages [inference].

### 6.2 Human evaluation [proposal, grounded in the practice cited]

**Protocol: ESA scores plus category labels ("ESA + categories").**
- ESA gives a 0–100 score plus error spans with severity. It is faster than MQM: median 29 s vs 38 s
  per paragraph (2406.11580, §6.5). It had higher intra- and inter-annotator agreement than MQM (§6.4,
  Table 5). It works with bilingual speakers or translators rather than trained MQM experts (§5)
  [source-stated].
- ESA "does not provide breakdown of error types" (2406.11580, Limitations) [source-stated]. The critic
  needs named categories. So annotators also label each span with a category from the small taxonomy in
  §7. AfriMTE did something similar for non-experts: 4 adequacy categories plus 4 fluency categories,
  combined with a DA-style score (2311.09828, §2.2.1) [source-stated].
- If categories prove too unreliable (see the 8.4% figure above), fall back to ESA-only for *system*
  claims. Keep categories only for the critic study (D1/D4) [proposal].
- Options to consider:
  - **Contrastive ESA**: several translations of one source shown side by side. It reduced annotation
    time and noise for English→Japanese (2607.26640, arXiv abstract) [source-stated].
  - **MQM re-annotation**, a second pass over earlier annotations. It finds errors missed the first time
    (2510.24664, Abstract) [source-stated].
  - Tooling: **Pearmut** supports DA/ESA/MQM, attention checks and document context (2601.02933,
    Abstract) [source-stated].

**Who and how many.**

| Practice in comparable work | Source |
|---|---|
| ≥2 bilingual native speakers per item, each with a Bachelor's degree or higher; a 20-item calibration round with discussion | AfriMTE, 2311.09828, §2.3 |
| 2 bilingual native evaluators per language pair; 300 overlapping items per language for agreement; 6,600 items per language pair | SSA-MTE, 2506.04557, §3.3–3.4 |
| 50 common segments to calibrate; annotator replaced if Pearson < 0.5; 250 MQM items per language | Indic zero-shot, 2406.03893, §3 |
| 3 native-speaker annotators for agreement subsets | FilBench (150 items, §5.3, Table 5); Batayan sentiment task |

[all source-stated]

**Proposed minimum for a credible CAMOE paper** [proposal; to be sized by a power analysis in the
preregistration]:
- **Per language where a claim is made:**
  - ≥2 native-speaker annotators per item, from different regions where varieties differ;
  - ≥3 annotators on an overlap subset of at least ~200–300 segments (the SSA-MTE scale) to measure
    agreement;
  - a calibration round before real annotation.
- **Systems:**
  - CAMOE;
  - the compute-matched baselines (DILIGENCE #3);
  - the confidence baseline (#4);
  - the **human reference** as a hidden "system", to check annotator attention and metric bias.
- **Blinding:** annotators never see system names; system order is randomised per document.
- **Attention checks:** deliberately damaged translations, as ESA did (2406.11580, §6.4 "Quality
  control"). In ESA, the original outscored the damaged version 86% of the time [source-stated].
- **Normalisation:** z-score each annotator's scores before averaging (AfriMTE §2.3; SSA-MTE §5)
  [source-stated].
- **Agreement to report:**
  - scores: Kendall τ-c and Pearson between annotators, as in ESA §6.4, and ICC(3,k), as in SSA-MTE
    Table 1;
  - categories: Cohen's or Fleiss' κ and Krippendorff's α. Batayan reports both, and also joint
    agreement, because chance-corrected measures behave badly on skewed labels (2502.14911, §3.3)
    [source-stated];
  - spans: overlap rate, as in ESA §6.4, Table 6.
- **Budget reduction:** prediction-powered inference combines a small human sample with metric scores
  and still gives unbiased system comparisons (2608.26638, arXiv abstract, EMNLP 2026) [source-stated].
  This is worth considering once a metric is validated for a language [inference].
- **Fair pay and consent** as in `data/DATA-PLAN.md`. For scale: SSA-MTE paid about US$590 per annotator
  for 3,300 annotations (2506.04557, Ethical Considerations) [source-stated; Philippine rates unknown].

### 6.3 Evaluating the critic itself (DILIGENCE #6)

Treat the critic as an automatic error annotator and score it the way AutoMQM was scored (2308.07286,
§6.1 "Span Meta-Evaluation") [source-stated method; application is a proposal]:
- **span precision** (predicted spans that humans also marked);
- **major recall** (human-marked major errors that the critic caught);
- **MCC**;
- **category agreement** (κ against the human majority label), always shown next to human–human κ;
- comparison against **xCOMET's spans** (Tagalog) and a **confidence baseline** (DILIGENCE #4).

---

## 7. Proposed error taxonomy for the critic's named categories  **[PROPOSAL]**

**Why start from MQM.**
- It is the standard behind WMT human evaluation.
- LLM judges already use it: the GEMBA-MQM prompt lists accuracy (addition, mistranslation, omission,
  untranslated), fluency (character encoding, grammar, inconsistency, punctuation, register, spelling),
  style (awkward), terminology, non-translation and other, with critical/major/minor severities
  (2310.13988, Fig. 1).
- The official MQM Core has 7 dimensions: Terminology, Accuracy, Linguistic conventions, Style, Locale
  conventions, Audience appropriateness, Design and markup. It tells implementers to "choose error types
  with the granularity that makes sense" (themqm.org/error-types-2/typology/) [source-stated].

**Why keep it small.**
- Agreement on fine categories is low. MQM same-annotator repeat agreement with matching category and
  severity was 8.4% (2406.11580, §6.4).
- AfriMTE used only 8 categories for non-expert annotators (2311.09828, §2.2.1) [source-stated].
- A category nobody applies consistently teaches the critic noise [inference].

| # | Category (parent → child) | Definition for annotators | Philippine-specific? | Grounding |
|---|---|---|---|---|
| 1 | Accuracy → Mistranslation | Meaning differs from the source | no | MQM (GEMBA Fig. 1) |
| 2 | Accuracy → Omission / Addition (incl. hallucination and overgeneration) | Content missing, or content added that is not in the source | no, but frequent | MQM. FilBench: overgeneration 47% of GPT-4o translation failures (2508.03523, §5.2) |
| 3 | Accuracy → **Voice/focus role error** | The verb's voice affix or the *ang/ng/sa* marking makes the wrong participant the subject, so *who did what to whom* changes | **yes** | Tagalog voice: "each sentence has a different subject (preceded by the *ang* marker) and a different verbal affix denoting the thematic role" (2505.20428, §3.1, Fig. 1) [source-stated]. Treating a meaning-changing voice error as an accuracy error is [inference] |
| 4 | Fluency → Grammar → **Aspect/affix morphology** | Wrong aspect (completed / ongoing / not yet begun) or malformed affixation that does not change who did what | **yes** | Filipino affixes mark "tense, focus, and mood" (2502.14911, §1) [source-stated]. A 2026 Filipino/Cebuano LLM-MT human study reports errors in "tense or aspect" (Springer ch. 10.1007/978-3-032-20897-2_3, via search snippet only; full text not accessed) [source-stated, secondary] |
| 5 | Fluency → Spelling / Orthography | Misspelling. **Accepted spelling variants are not errors**; the style guide lists them | partly | `data/DATA-PLAN.md` notes competing spellings [inference for the rule] |
| 6 | Style → **Unnatural word order / translationese** | Grammatical but stiff, e.g. unnecessary *ay*-inversion where normal predicate-first order is expected | **yes** | Machine translations showed "an unusual preference" for *ay*-inversion, which is common in formal settings (2502.14911, §2.2, §4.1) [source-stated] |
| 7 | Style → **Pragmatically awkward word choice** | A dictionary-correct word that a native speaker would not use in this sense | **yes** (frequent) | Batayan example: *magpapadala* / *hudyat* for "send a strong signal" (2502.14911, §4.1) [source-stated] |
| 8 | Register → **Politeness / respect marking** | Missing, extra or misplaced *po/opo* (and other respect forms, such as plural-of-respect pronouns) for the target register | **yes** | Target-register metadata already planned (D6 in `data/DATA-PLAN.md`). Linguistic sourcing is weak in this search: only non-academic web pages and a ResearchGate title on *po* in campaign ads were found [unknown → needs a linguist-authored source, e.g. a reference grammar, before annotator guidelines are written] |
| 9 | Register → **Code-switching mismatch (Taglish and similar)** | English insertions where the target register calls for Filipino, or forced "pure" Filipino where natural usage keeps the English word. Judged against a *declared* target register | **yes** | Batayan: Taglish is argued to be the de facto lingua franca; the benchmark prioritised colloquial usage and common loanwords (2502.14911, §2.1–2.2) [source-stated]. Needs D6 register labels [inference] |
| 10 | Accuracy → **Wrong language / variety drift** | Output (or part of it) is in a different Philippine language or variety than requested, e.g. Tagalog words in a Cebuano target. Distinct from "untranslated" (left in the source language) | **yes** | FilBench: translations "in an incorrect target language" (2508.03523, §5.2) [source-stated]. Separating drift from untranslated text is [proposal] |
| 11 | Accuracy → Untranslated | Source-language text left in the output (not deliberate code-switching) | no | MQM |
| 12 | Terminology | Wrong or inconsistent domain term | no | MQM |
| 13 | Audience appropriateness → Culture-specific reference | A reference that does not fit the target culture | partly | MQM Core dimension (themqm.org) |
| 14 | Other / Source error | Anything else, and problems already in the source | no | MQM |

**Severity:** minor / major / critical, with the WMT weights 1 / 5 / 25 (2310.13988, §1) [source-stated].
Keep "Non-translation" (the whole output is unusable) as an automatic critical error.

**Before this taxonomy trains anything** [proposal]:
1. Pilot it on the D1 error-study set with ≥3 annotators per language.
2. Merge or drop any category whose κ stays low after one guideline revision. Record the threshold in the
   preregistration.
3. Check that the categories an LLM or the critic uses are applied as defined, not as a catch-all. This
   is the GEMBA "locale convention" lesson (2310.13988, §4.3).
4. For languages other than Tagalog, get native speakers to review categories 3, 4, 8 and 9. Voice
   systems and politeness marking differ across Philippine languages (e.g. *po* use is described for
   Tagalog-, Bikol- and Kapampangan-speaking areas in the web sources found). How far each applies per
   language is [unknown].

---

## 8. Papers worth adding to the reference registry (do NOT edit `seed.json` from here)

| arXiv ID | One-line reason |
|---|---|
| 2311.09828 | AfriMTE/AfriCOMET: simplified-MQM protocol for non-expert native speakers, plus a regional-encoder COMET. Template for a Philippine COMET |
| 2506.04557 | SSA-COMET: 73k annotations; chrF++ beats COMET-22 when the encoder lacks the language; LLM judges need few-shot examples; asking for spans hurts |
| 2406.03893 | Zero-shot MT evaluation for four low-resource Indian languages: learned metrics reach only τ ≈ 0.32; GEMBA-MQM weak |
| 2212.10180 | IndicMT Eval (ACL 2023): 7k MQM annotations; metrics miss fluency errors in non-English languages |
| 2510.07061 | ITEM: 26 metrics × 6 Indian languages; LLM judges best aligned; outlier sensitivity |
| 2502.12404 | WMT24++: the only large public English→Filipino MT reference set with post-edits (Apache-2.0); metric bias against human translations |
| 2406.11580 | ESA protocol: cheaper than MQM with comparable quality; the MQM category-agreement figures (8.4%) |
| 2607.26640 | Contrastive ESA: several outputs side by side; less time and noise |
| 2601.02933 | Pearmut: open human-evaluation platform (DA/ESA/MQM, attention checks) |
| 2510.24664 | MQM re-annotation: a second pass improves annotation quality |
| 2604.17393 | Compare metric–human agreement with human–human agreement; domain-shift weakness |
| 2608.26638 | Prediction-powered evaluation: fewer human labels for unbiased system comparison |
| 2609.04173 | Last Translation Benchmark: rule-verified hard cases, including 36 Filipino items; model for a Philippine challenge set |
| 2508.20511 | FLORES+ quality problems; named-entity copying inflates BLEU |
| 2309.07462 | LLM evaluators biased high; calibrate per language with native judgments |
| 2310.10482 | xCOMET: open span-level metric (severity only), a baseline for the critic's spans |
| 2309.11925 | CometKiwi-23: XL/XXL QE models used in WMT24++ |
| 2104.14478 | Freitag et al.: MQM with professional translators beats crowd DA; the basis of modern MQM |
| 2107.10821 | "To ship or not to ship": BLEU-only evaluation led to bad decisions; pairwise-accuracy method |
| 2401.06760 | Metric deltas humans actually notice (high-resource calibration) |
| 2202.05148 | COMET blind to number and named-entity errors, found via MBR decoding |
| 2502.14911 | Batayan: Filipino/Taglish benchmark; FLORES Filipino re-translated for translationese; *ay*-inversion evidence |
| 2505.20428 | UD-NewsCrawl Tagalog treebank: describes the voice/focus system used in taxonomy item 3 |
| 1911.02116 | XLM-R: CC-100 language table (Filipino is the only Philippine language), which fixes COMET coverage |
| 2010.11934 | mT5: mC4 table (fil, ceb), which fixes MetricX coverage |
| 2106.03193 | FLORES-101: origin of spBLEU and the WMT21 Tagalog evaluation set |
| 2603.16309 | Omnilingual MT: BLASER 3, Met-BOUQuET and the XSTS+R+P human protocol for long-tail languages. Philippine coverage not checked [unknown] |
| 2606.22269 | Hausa/Fongbe: metrics disagree with native preference; BERTScore embedding collapse |

Already in the registry and used here: 2310.13988 (GEMBA-MQM), 2308.07286 (AutoMQM), 2603.25222 (FRED;
see the correction in §1), 2205.00978 (quality-aware decoding, overfitting to metrics), 2508.03523
(FilBench), 2502.14301 (SEA-HELM), 2409.15380 (Kalahi).

---

## 9. Sources (all retrieved 2026-09-24)

Local markdown in `research/papers/md/`:
- 2310.13988 (GEMBA-MQM)
- 2308.07286 (AutoMQM)
- 2205.00978 (quality-aware decoding)
- 2502.08561 (quality-aware decoding with QE)
- 2508.03523 (FilBench)
- 2502.14301 (SEA-HELM)
- 2409.15380 (Kalahi)

Full text via `pwc paper read` (Papers with Code markdown of the arXiv HTML):
- 2603.25222 (FRED; *not* present locally despite the task note)
- 2311.09828, 2506.04557, 2502.12404, 2309.07462, 2604.17393, 2609.04173, 2508.20511, 2310.10482
- 2406.03893, 2510.07061, 2603.16309 (truncated rendition; metric sections not in the retrieved text)
- 1911.02116, 2010.11934, 2010.12821, 2007.07834, 2406.11580, 2309.11925, 2505.20428

Abstract pages / metadata:
- arxiv.org/abs/2212.10180, /2104.14478, /2202.05148, /2401.06760, /2107.10821, /2602.17425,
  /2606.22269, /2608.26638, /2607.26640
- `pwc paper info` for 2106.03193, 2601.02933, 2510.24664

PDFs (text extracted locally):
- arxiv.org/pdf/2502.14911 (Batayan)
- aclanthology.org/2021.wmt-1.2.pdf (WMT21 LSMT findings)

Web pages:
- github.com/Unbabel/COMET README ("Languages Covered")
- huggingface.co/Unbabel/wmt22-comet-da README
- github.com/google-research/metricx README ("Changes to the WMT'24 Submission", "Synthetic Data")
- github.com/google-research/bleurt checkpoints.md
- themqm.org/error-types-2/typology/
- www2.statmt.org/wmt25/translation-task.html

Hugging Face API (`/api/models`, `/api/datasets`):
- google/rembert
- Unbabel/wmt22-comet-da, Unbabel/XCOMET-XL, Unbabel/wmt22-cometkiwi-da, Unbabel/wmt23-cometkiwi-da-xl
- google/metricx-24-hybrid-xl-v2p6, google/metricx-24-hybrid-xxl-v2p6
- McGill-NLP/ssa-comet-mtl
- facebook/blaser-2.0-ref, facebook/blaser-2.0-qe
- datasets google/wmt24pp, openlanguagedata/flores_plus

Secondary only (search-result snippets, full text not read):
- Springer chapter "Evaluating the Performance of Large Language Models for Filipino and Cebuano Machine
  Translation" (doi 10.1007/978-3-032-20897-2_3; the publisher page redirected to a login, and the
  university news page failed DNS)
- arXiv 1902.07250 (Cebuano→Tagalog NMT, BLEU 20.01)
- ResearchGate "The use of politeness marker 'po' in Television-mediated political campaign
  advertisements in the Philippines" (title only)

Not verified (named but not opened): WMT24 metrics findings "Are LLMs Breaking MT Metrics?" (the fetch
timed out); MetricX-24 paper 2410.03983 (`pwc` returned no data).

---

## Appendix A · Search log (all 2026-09-24)

| Tool | Query / target | Useful result |
|---|---|---|
| pwc search | machine translation metrics low-resource languages correlation human judgment | 2603.25222, 2604.17393, 2210.15615, 2401.16313 |
| pwc search | AfriCOMET African languages MT evaluation | 2311.09828, 2506.04557 |
| pwc search | IndicMT Eval metrics Indian languages | 2406.03893, 2510.07061 |
| pwc search | Tagalog machine translation evaluation | nothing Tagalog-specific; 2609.04173 |
| pwc search | Filipino machine translation human evaluation | 2601.02933, 2508.20511; nothing Filipino-specific |
| pwc search | Cebuano machine translation | nothing relevant |
| pwc search | Philippine languages machine translation | 2111.06053 (Filipino LMs); nothing on evaluation |
| pwc search | error span annotation ESA human evaluation machine translation | 2510.24664, 2604.17393 |
| pwc search | Error Span Annotation: A Balanced Approach for Human Evaluation of Machine Translation | 2310.10482; ESA itself fetched as 2406.11580 |
| pwc search | MetricX-24 metrics shared task | 2509.25546; MetricX-24 paper not indexed |
| pwc search | xCOMET transparent machine translation evaluation error span | 2310.10482, 2406.14553 |
| pwc search | CometKiwi quality estimation | 2309.11925, 2209.06243 |
| pwc search | WMT24++ expanding language coverage 55 languages | 2502.12404, 2603.16309 |
| pwc search | LLM-based evaluators multilingual evaluation low-resource bias | 2309.07462, 2410.17578 |
| pwc search | COMET weaknesses minimum Bayes risk decoding empty translation | 2411.03524, 2205.00978 |
| pwc search | pitfalls COMET metric | 2305.11806, 2305.19144 |
| pwc search | code-switching machine translation evaluation Taglish | 2505.20428 (only Tagalog hit) |
| pwc search | Southeast Asian languages machine translation metric evaluation | 2502.14301 |
| pwc search | Tagalog voice focus system verb morphology NLP | 2311.07171 (calamanCy) |
| pwc search | Tagalog politeness po opo honorific | none Tagalog-specific (2502.20864 Javanese honorifics) |
| pwc search | Cebuano Ilocano Hiligaynon Waray NLP resources benchmark | 2508.03523, 2203.17225, 2310.00679; no MT evaluation |
| pwc paper read | 2603.25222, 2311.09828, 2506.04557, 2502.12404, 2309.07462, 2604.17393, 2609.04173, 2508.20511, 2310.10482, 2406.03893, 2510.07061, 2603.16309, 1911.02116, 2010.11934, 2010.12821, 2007.07834, 2406.11580, 2309.11925, 2505.20428 | full text read / grepped |
| pwc paper read | 2401.06760, 2212.10180, 2104.14478, 2202.05148, 2502.14911 | "Paper Markdown was not found" → used arXiv abs / PDF instead |
| pwc paper info | 2106.03193, 2601.02933, 2510.24664 | abstracts |
| pwc paper info | 2608.26638, 2607.26640, 2602.17425, 2606.22269, 2410.03983 | no data → arXiv abs via WebFetch (except 2410.03983) |
| WebSearch | WMT 2025 general machine translation human evaluation ESA languages Filipino | WMT25 findings, 2607.26640, 2608.26638 |
| WebSearch | Tagalog Cebuano machine translation human evaluation metric correlation BLEU chrF COMET | 1902.07250, 2602.17425, 2606.22269; no Philippine correlation study |
| WebSearch | XLM-RoBERTa CC-100 language list Tagalog Cebuano Ilocano coverage | pointed to 1911.02116 App. A |
| WebSearch | Batayan Filipino NLP benchmark translation evaluation native speakers | 2502.14911 |
| WebSearch | Filipino English machine translation LLM evaluation native speaker MQM study 2025 | Springer Filipino/Cebuano chapter; KatotohananQA |
| WebSearch | "Evaluating the Performance of Large Language Models for Filipino and Cebuano Machine Translation" | chapter snippet (human syntactic/semantic analysis; tense/aspect errors) |
| WebSearch | WMT24++ human evaluation MQM ESA 55 languages follow-up fil_PH results metrics correlation | no follow-up with Filipino human scores found |
| WebSearch | Findings of the WMT 2021 Shared Task on Large-Scale Multilingual Machine Translation small task 2 Tagalog Javanese human evaluation spBLEU | 2021.wmt-1.2 |
| WebSearch | Tagalog politeness particles "po" "opo" respect markers linguistics paper | only non-academic pages plus one ResearchGate title |
| WebFetch | arxiv.org/abs/2212.10180, 2104.14478, 2202.05148, 2401.06760, 2107.10821, 2602.17425, 2606.22269, 2608.26638, 2607.26640 | abstracts |
| WebFetch | github.com/google-research/bleurt checkpoints.md (blob + raw) | BLEURT-20 = RemBERT + WMT 2015–19 ratings |
| WebFetch | themqm.org/error-types-2/typology/ (×2) | MQM Core 7 dimensions |
| WebFetch | www2.statmt.org/wmt25/translation-task.html | no Philippine languages in WMT25 |
| WebFetch | arxiv.org/pdf/2502.14911; aclanthology.org/2021.wmt-1.2.pdf | PDFs saved, text extracted with pypdf |
| WebFetch (failed) | link.springer.com chapter (login redirect); uic.edu.ph news (DNS failure); statmt WMT24 metrics PDF (timeout) | — |
| curl (HF API) | models: google/rembert, Unbabel/wmt22-comet-da, Unbabel/XCOMET-XL, Unbabel/wmt22-cometkiwi-da, Unbabel/wmt23-cometkiwi-da-xl, google/metricx-24-hybrid-xl-v2p6, google/metricx-24-hybrid-xxl-v2p6, McGill-NLP/ssa-comet-mtl, facebook/blaser-2.0-ref, facebook/blaser-2.0-qe | licences and language metadata |
| curl (HF API) | datasets: google/wmt24pp, openlanguagedata/flores_plus | `en-fil_PH` config; FLORES+ Philippine configs |
| curl (HF API) | dataset search: "tagalog mqm", "filipino mqm", "tagalog translation quality", "filipino translation human", "cebuano translation", "tagalog direct assessment", "mt human evaluation tagalog", "wmt mqm" | **no Philippine human-judgment MT dataset found** (only parallel text and the WMT MQM sets) |
| curl (raw READMEs) | Unbabel/COMET, Unbabel/wmt22-comet-da, google-research/metricx | coverage warning; MetricX failure-mode list |

**Limits of this search.** I did not search Google Scholar, the ACL Anthology full-text index or
Philippine university repositories (e.g. PCSC or LREC-COLING workshop proceedings), which are behind
tools this task excluded or that timed out. A Philippine-language metric-validation study published only
in a local venue could exist and would not have been found [unknown].
