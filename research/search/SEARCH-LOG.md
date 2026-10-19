# Search log

Generated 2026-10-19 by `research/tools/search_log.py report` from `log.jsonl`.
Do not edit by hand: add queries to `queries.json`, decisions to `screening.json`, re-run.

Screening status: **included** (in `research/papers/seed.json`) · **excluded** (reason given)
· **title-screened** (seen in results, not yet assessed).
Unique papers seen: 951 — included 58, excluded 104, title-screened 751.


## S01: iterative refinement of latent sentence plan before decoding

Serves item(s) 1. Purpose: latent whole-sentence draft refined before writing

Runs: 1 (latest 2026-09-24T07:07:37+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1808.08762 | Sentence Embeddings in NLI with Iterative Refinement Encoders | 2018 | title-screened |
| 2 | 2405.18400 | Superposed Decoding: Multiple Generations from a Single Autoregressive Inference Pass | 2024 | title-screened |
| 3 | 2510.11052 | Latent Refinement Decoding: Enhancing Diffusion-Based Language Models by Refining Belief States | 2025 | included |
| 4 | 1906.05275 | Keeping Notes: Conditional Natural Language Generation with a Scratchpad Mechanism | 2019 | title-screened |
| 5 | 2506.19830 | Scaling Speculative Decoding with Lookahead Reasoning | 2025 | title-screened |
| 6 | 2502.11517 | Learning to Keep a Promise: Scaling Language Model Decoding Parallelism with Learned Asynchronous Decoding | 2025 | title-screened |
| 7 | 1805.01035 | Split and Rephrase: Better Evaluation and a Stronger Baseline | 2018 | title-screened |
| 8 | 2508.19982 | Diffusion Language Models Know the Answer Before Decoding | 2025 | title-screened |

## S02: verifier critic in latent space halting additional computation

Serves item(s) 1, 3. Purpose: critic/verifier that decides whether to spend more compute

Runs: 1 (latest 2026-09-24T07:07:39+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2509.23152 | Critique to Verify: Accurate and Honest Test-Time Scaling with RL-Trained Verifiers | 2025 | title-screened |
| 2 | 2508.16665 | Trust but Verify! A Survey on Verification Design for Test-time Scaling | 2025 | title-screened |
| 3 | 2510.18982 | Test-time Verification via Optimal Transport: Coverage, ROC, & Sub-optimality | 2025 | title-screened |
| 4 | 2502.12118 | Scaling Test-Time Compute Without Verification or RL is Suboptimal | 2025 | title-screened |
| 5 | 2502.01989 | VFScale: Intrinsic Reasoning through Verifier-Free Test-time Scalable Diffusion Model | 2025 | title-screened |
| 6 | 2505.11824 | Latent Veracity Inference for Identifying Errors in Stepwise Reasoning | 2025 | title-screened |
| 7 | 2602.01070 | What If We Allocate Test-Time Compute Adaptively? | 2026 | title-screened |
| 8 | 2606.19808 | Think Again or Think Longer? Selective Verification for Budget-Aware Reasoning | 2026 | title-screened |

## S03: energy-based transformer verify and refine predictions

Serves item(s) 1, 3. Purpose: learned verifier driving refinement

Runs: 1 (latest 2026-09-24T07:07:40+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2507.02092 | Energy-Based Transformers are Scalable Learners and Thinkers | 2025 | included |
| 2 | 2311.08362 | Transformers can optimally learn regression mixture models | 2023 | excluded (off-topic (in-context regression theory)) |
| 3 | 2205.13401 | Your Transformer May Not be as Powerful as You Expect | 2022 | title-screened |
| 4 | 2106.13638 | Transient Stability Analysis with Physics-Informed Neural Networks | 2023 | excluded (off-topic (power systems)) |
| 5 | 2505.03188 | Transformers Applied to Short-term Solar PV Power Output Forecasting | 2025 | excluded (off-topic (solar forecasting)) |
| 6 | 2410.16699 | Graph Transformers Dream of Electric Flow | 2024 | excluded (off-topic (graph transformers, electric flow)) |
| 7 | 2410.01265 | Transformers Handle Endogeneity in In-Context Linear Regression | 2024 | excluded (off-topic (econometrics in-context)) |
| 8 | 2509.19702 | Linear Transformers Implicitly Discover Unified Numerical Algorithms | 2025 | excluded (off-topic (numerical algorithms)) |

## S04: adaptive computation time learned halting transformer

Serves item(s) 1, 4. Purpose: learned halting

Runs: 1 (latest 2026-09-24T07:07:40+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2507.13569 | Change of Thought: Adaptive Test-Time Computation | 2025 | title-screened |
| 2 | 2607.20519 | Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts | 2026 | included |
| 3 | 2312.10193 | Adaptive Computation Modules: Granular Conditional Computation For Efficient Inference | 2023 | excluded (screened 2026-10-07 (S103): per-token learner gating under user budgets; no per-action cost heterogeneity or RL cost penalty, not cited) |
| 4 | 2602.08864 | Understanding Dynamic Compute Allocation in Recurrent Transformers | 2026 | excluded (screened 2026-10-07 (S103): token-level halting analysis; no per-stage cost penalty, not cited) |
| 5 | 1603.08983 | Adaptive Computation Time for Recurrent Neural Networks | 2016 | included |
| 6 | 2505.18948 | Exact Expressive Power of Transformers with Padding | 2025 | title-screened |
| 7 | 2406.03136 | Computational Limits of Low-Rank Adaptation (LoRA) Fine-Tuning for Transformer Models | 2024 | excluded (off-topic (LoRA theory)) |
| 8 | 2303.07109 | Transformer-based World Models Are Happy With 100k Interactions | 2023 | excluded (off-topic (world models for RL)) |

## S05: recurrent depth latent reasoning test-time compute

Serves item(s) 1, 4. Purpose: internal repasses without text

Runs: 1 (latest 2026-09-24T07:07:42+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.05171 | Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach | 2025 | included |
| 2 | 2602.07845 | Recurrent-Depth VLA: Implicit Test-Time Compute Scaling of Vision-Language-Action Models via Latent Iterative Reasoning | 2026 | title-screened |
| 3 | 2510.07358 | Encode, Think, Decode: Scaling test-time reasoning with recursive latent thoughts | 2025 | included |
| 4 | 2507.02199 | Latent Chain-of-Thought? Decoding the Depth-Recurrent Transformer | 2025 | title-screened |
| 5 | 2605.11011 | LoopUS: Recasting Pretrained LLMs into Looped Latent Refinement Models | 2026 | title-screened |
| 6 | 2503.07572 | Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning | 2025 | title-screened |
| 7 | 2502.10428 | Dynamic Chain-of-Thought: Towards Adaptive Deep Reasoning | 2025 | title-screened |
| 8 | 2507.16784 | Beyond Context Limits: Subconscious Threads for Long-Horizon Reasoning | 2025 | title-screened |

## S06: continuous latent thought reasoning

Serves item(s) 1, 6. Purpose: thinking in hidden states instead of text

Runs: 1 (latest 2026-09-24T07:07:43+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2604.06374 | The Illusion of Superposition? A Principled Analysis of Latent Thinking in Language Models | 2026 | title-screened |
| 2 | 2412.06769 | Training Large Language Models to Reason in a Continuous Latent Space | 2024 | included |
| 3 | 2606.12689 | Observable Patterns Are Not Explanations: A Causal-Geometric Analysis of Latent Reasoning Models | 2026 | included |
| 4 | 2509.25239 | A Formal Comparison Between Chain of Thought and Latent Thought | 2025 | title-screened |
| 5 | 2602.10229 | Latent Thoughts Tuning: Bridging Context and Reasoning with Fused Information in Latent Tokens | 2026 | title-screened |
| 6 | 2606.20075 | What Makes Effective Supervision in Latent Chain-of-Thought: An Information-Theoretic Analysis | 2026 | title-screened |
| 7 | 2512.21711 | Do Latent Tokens Think? A Causal and Adversarial Analysis of Chain-of-Continuous-Thought | 2025 | title-screened |
| 8 | 2604.22709 | Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought | 2026 | title-screened |

## S07: sentence-level concept model latent space

Serves item(s) 1. Purpose: sentence-level latent representations

Runs: 1 (latest 2026-09-24T07:07:44+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2512.23988 | Fantastic Reasoning Behaviors and Where to Find Them: Unsupervised Discovery of the Reasoning Process | 2025 | title-screened |
| 2 | 2603.01227 | The Lattice Representation Hypothesis of Large Language Models | 2026 | title-screened |
| 3 | 2403.03867 | On the Origins of Linear Representations in Large Language Models | 2024 | title-screened |
| 4 | 2604.02029 | The Latent Space: Foundation, Evolution, Mechanism, Ability, and Outlook | 2026 | title-screened |
| 5 | 2311.08968 | Identifying Linear Relational Concepts in Large Language Models | 2023 | title-screened |
| 6 | 2506.16975 | Latent Concept Disentanglement in Transformer-based Language Models | 2025 | title-screened |
| 7 | 2412.08821 | Large Concept Models: Language Modeling in a Sentence Representation Space | 2024 | included |
| 8 | 2406.01506 | The Geometry of Categorical and Hierarchical Concepts in Large Language Models | 2024 | title-screened |

## S08: diffusion language model iterative refinement whole sequence

Serves item(s) 1. Purpose: whole-sequence refinement

Runs: 1 (latest 2026-09-24T07:07:45+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.16813 | One-step Language Modeling via Continuous Denoising | 2026 | title-screened |
| 2 | 2510.11052 | Latent Refinement Decoding: Enhancing Diffusion-Based Language Models by Refining Belief States | 2025 | included |
| 3 | 2605.09603 | Edit-Based Refinement for Parallel Masked Diffusion Language Models | 2026 | title-screened |
| 4 | 2509.24007 | Sequential Diffusion Language Models | 2025 | title-screened |
| 5 | 2601.07351 | Beyond Hard Masks: Progressive Token Evolution for Diffusion Language Models | 2026 | title-screened |
| 6 | 2604.11748 | LangFlow: Continuous Diffusion Rivals Discrete in Language Modeling | 2026 | title-screened |
| 7 | 2509.20624 | FS-DFM: Fast and Accurate Long Text Generation with Few-Step Diffusion Language Models | 2025 | title-screened |
| 8 | 2503.04482 | Generalized Interpolating Discrete Diffusion | 2025 | title-screened |

## S09: non-autoregressive machine translation iterative refinement

Serves item(s) 1. Purpose: refinement in translation specifically

Runs: 1 (latest 2026-09-24T07:07:46+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2104.11897 | Modeling Coverage for Non-Autoregressive Neural Machine Translation | 2021 | title-screened |
| 2 | 1811.04719 | End-to-End Non-Autoregressive Neural Machine Translation with Connectionist Temporal Classification | 2018 | title-screened |
| 3 | 1711.02281 | Non-Autoregressive Neural Machine Translation | 2017 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 4 | 2302.07863 | Speculative Decoding with Big Little Decoder | 2023 | title-screened |
| 5 | 2004.03227 | Improving Fluency of Non-Autoregressive Machine Translation | 2020 | title-screened |
| 6 | 2006.10369 | Deep Encoder, Shallow Decoder: Reevaluating Non-autoregressive Machine Translation | 2020 | title-screened |
| 7 | 2204.09269 | A Survey on Non-Autoregressive Generation for Neural Machine Translation and Beyond | 2022 | title-screened |
| 8 | 2210.03953 | Non-Monotonic Latent Alignments for CTC-Based Non-Autoregressive Machine Translation | 2022 | title-screened |

## S10: deliberation network two-pass decoding translation

Serves item(s) 1. Purpose: two-pass translation

Runs: 1 (latest 2026-09-24T07:07:47+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.08561 | Quality-Aware Decoding: Unifying Quality Estimation and Decoding | 2025 | included |
| 2 | 1409.1259 | On the Properties of Neural Machine Translation: Encoder-Decoder Approaches | 2014 | title-screened |
| 3 | 1610.10099 | Neural Machine Translation in Linear Time | 2016 | title-screened |
| 4 | 1406.1078 | Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation | 2014 | title-screened |
| 5 | 2205.00978 | Quality-Aware Decoding for Neural Machine Translation | 2022 | included |
| 6 | 1702.01806 | Beam Search Strategies for Neural Machine Translation | 2017 | title-screened |
| 7 | 1409.0473 | Neural Machine Translation by Jointly Learning to Align and Translate | 2014 | title-screened |
| 8 | 2309.10966 | MBR and QE Finetuning: Training-time Distillation of the Best and Most Expensive Decoding Methods | 2023 | title-screened |

## S11: mixture of experts router reinforcement learning

Serves item(s) 2. Purpose: RL-trained routing

Runs: 1 (latest 2026-09-24T07:07:48+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.17038 | Phase-Aware Mixture of Experts for Agentic Reinforcement Learning | 2026 | excluded (agentic RL MoE, not routing by critique) |
| 2 | 2510.23027 | Towards Stable and Effective Reinforcement Learning for Mixture-of-Experts | 2025 | title-screened |
| 3 | 2609.13058 | Expert-Space Exploration in MoE Reinforcement Learning | 2026 | title-screened |
| 4 | 2412.13053 | SMOSE: Sparse Mixture of Shallow Experts for Interpretable Reinforcement Learning in Continuous Control Tasks | 2024 | excluded (off-topic (continuous-control RL)) |
| 5 | 2510.11370 | Stabilizing MoE Reinforcement Learning by Aligning Training and Inference Routers | 2025 | included |
| 6 | 2510.02850 | Reward Model Routing in Alignment | 2025 | title-screened |
| 7 | 2509.21823 | ProRe: A Proactive Reward System for GUI Agents via Reasoner-Actor Collaboration | 2025 | excluded (GUI-agent reward system, not MoE) |
| 8 | 2311.08692 | Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models | 2023 | included |

## S12: conditional memory lookup n-gram embedding sparsity

Serves item(s) 5. Purpose: Engram and lookup memory

Runs: 1 (latest 2026-09-24T07:07:50+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2601.07372 | Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models | 2026 | included |
| 2 | 2609.15126 | MoME: Mixture-of-Memory Embeddings for Context-Aware Sparse Lookup | 2026 | title-screened |
| 3 | 1412.1454 | Skip-gram Language Modeling Using Sparse Non-negative Matrix Probability Estimation | 2014 | title-screened |
| 4 | 2601.15205 | Beyond the Geometric Curse: High-Dimensional N-Gram Hashing for Dense Retrieval | 2026 | title-screened |
| 5 | 2601.21461 | $L^3$: Large Lookup Layers | 2026 | title-screened |
| 6 | 2605.16893 | NGM: A Plug-and-Play Training-Free Memory Module for LLMs | 2026 | title-screened |
| 7 | 2203.12171 | An Empirical Study of Memorization in NLP | 2022 | title-screened |
| 8 | 2603.15923 | Learning to Recall with Transformers Beyond Orthogonal Embeddings | 2026 | title-screened |

## S13: critic network decides whether to refine latent representation

Serves item(s) 1, 3. Purpose: critic deciding refinement

Runs: 1 (latest 2026-09-24T07:07:51+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2507.15024 | RefCritic: Training Long Chain-of-Thought Critic Models with Refinement Feedback | 2025 | title-screened |
| 2 | 2605.14641 | How to Evaluate and Refine your CAM | 2026 | title-screened |
| 3 | 2505.11628 | Critique-Guided Distillation for Robust Reasoning via Refinement | 2025 | title-screened |
| 4 | 2512.13979 | ReflCtrl: Controlling LLM Reflection via Representation Engineering | 2025 | title-screened |
| 5 | 2410.05495 | Self-rationalization improves LLM as a fine-grained judge | 2024 | title-screened |
| 6 | 2412.13171 | Compressed Chain of Thought: Efficient Reasoning Through Dense Representations | 2024 | title-screened |
| 7 | 2604.06374 | The Illusion of Superposition? A Principled Analysis of Latent Thinking in Language Models | 2026 | title-screened |
| 8 | 2506.10128 | ViCrit: A Verifiable Reinforcement Learning Proxy Task for Visual Perception in VLMs | 2025 | title-screened |

## S14: discriminator on hidden states of language model adversarial training text

Serves item(s) 3. Purpose: GAN-style discriminator on hidden states

Runs: 1 (latest 2026-09-24T07:07:53+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2604.15163 | DPC: Training-Free Text-to-SQL Candidate Selection via Dual-Paradigm Consistency | 2026 | excluded (text-to-SQL selection) |
| 2 | 2607.01208 | Distill to Detect: Exposing Stealth Biases in LLMs through Cartridge Distillation | 2026 | excluded (bias detection) |
| 3 | 2512.08123 | Universal Adversarial Suffixes Using Calibrated Gumbel-Softmax Relaxation | 2025 | excluded (adversarial suffixes) |
| 4 | 2510.04347 | Unmasking Backdoors: An Explainable Defense via Gradient-Attention Anomaly Scoring for Pre-trained Language Models | 2025 | excluded (backdoor defense) |
| 5 | 2509.23886 | Towards Understanding Subliminal Learning: When and How Hidden Biases Transfer | 2025 | excluded (subliminal learning) |
| 6 | 2607.28319 | Fairness Pruning: Locating Demographic Bias in GLU-MLP Layers via Differential Activations | 2026 | excluded (fairness pruning) |
| 7 | 2312.02780 | Scaling Laws for Adversarial Attacks on Language Model Activations | 2023 | excluded (adversarial attacks) |
| 8 | 2204.04636 | "That Is a Suspicious Reaction!": Interpreting Logits Variation to Detect NLP Adversarial Attacks | 2022 | excluded (adversarial detection) |

## S15: predict translation errors from model internal hidden states quality estimation

Serves item(s) 3, 7. Purpose: predicting translation errors from internals

Runs: 1 (latest 2026-09-24T07:07:54+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2505.23183 | Unsupervised Word-level Quality Estimation for Machine Translation Through the Lens of Annotators (Dis)agreement | 2025 | title-screened |
| 2 | 1610.04841 | Translation Quality Estimation using Recurrent Neural Network | 2016 | title-screened |
| 3 | 2305.12535 | Explaining How Transformers Use Context to Build Predictions | 2023 | title-screened |
| 4 | 2310.13988 | GEMBA-MQM: Detecting Translation Quality Error Spans with GPT-4 | 2023 | included |
| 5 | 2308.07286 | The Devil is in the Errors: Leveraging Large Language Models for Fine-grained Machine Translation Evaluation | 2023 | included |
| 6 | 2601.00680 | Sigmoid Head for Quality Estimation under Language Ambiguity | 2026 | title-screened |
| 7 | 2406.19384 | The Remarkable Robustness of LLMs: Stages of Inference? | 2024 | title-screened |
| 8 | 2410.06338 | Are Large Language Models State-of-the-art Quality Estimators for Machine Translation of User-generated Content? | 2024 | title-screened |

## S16: plan then write latent sentence plan language model

Serves item(s) 1. Purpose: plan-then-write

Runs: 1 (latest 2026-09-24T07:07:55+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1907.04944 | Can Unconditional Language Models Recover Arbitrary Sentences? | 2019 | title-screened |
| 2 | 2412.09879 | On the Limit of Language Models as Planning Formalizers | 2024 | title-screened |
| 3 | 2604.12493 | Latent Planning Emerges with Scale | 2026 | included |
| 4 | 2306.15926 | Most Language Models can be Poets too: An AI Writing Assistant and Constrained Text Generation Studio | 2023 | title-screened |
| 5 | 1708.00781 | Dynamic Entity Representations in Neural Language Models | 2017 | title-screened |
| 6 | 2205.05124 | Extracting Latent Steering Vectors from Pretrained Language Models | 2022 | title-screened |
| 7 | 2601.20164 | What's the plan? Metrics for implicit planning in LLMs and their application to rhyme generation and question answering | 2026 | title-screened |
| 8 | 2502.06258 | Emergent Response Planning in LLMs | 2025 | title-screened |

## S17: looped transformer learned halting gate

Serves item(s) 1, 4. Purpose: halting gates in looped models

Runs: 1 (latest 2026-09-24T07:07:56+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2607.20519 | Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts | 2026 | included |
| 2 | 2603.08391 | Adaptive Loops and Memory in Transformers: Think Harder or Know More? | 2026 | included |
| 3 | 2410.01405 | On Expressive Power of Looped Transformers: Theoretical Analysis and Enhancement via Timestep Encoding | 2024 | title-screened |
| 4 | 2605.23872 | Training-Free Looped Transformers | 2026 | title-screened |
| 5 | 2502.17416 | Reasoning with Latent Thoughts: On the Power of Looped Transformers | 2025 | included |
| 6 | 2606.18206 | Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers | 2026 | title-screened |
| 7 | 2607.13491 | DeepLoop: Depth Scaling for Looped Transformers | 2026 | title-screened |
| 8 | 2607.16051 | Loop the Loopies! | 2026 | title-screened |

## S18: self-correction in latent space without generating text

Serves item(s) 1, 6. Purpose: self-correction without text

Runs: 1 (latest 2026-09-24T07:07:57+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2511.12742 | Stabilizing Self-Consuming Diffusion Models with Latent Space Filtering | 2025 | title-screened |
| 2 | 2605.06548 | Continuous Latent Diffusion Language Model | 2026 | included |
| 3 | 2510.01384 | Fine-Tuning Masked Diffusion for Provable Self-Correction | 2025 | title-screened |
| 4 | 2602.11590 | Learn from Your Mistakes: Self-Correcting Masked Diffusion Models | 2026 | included |
| 5 | — | Contrastive-Guided Self-Supervised Latent Visual Reasoning for Hallucination Mitigation |  | title-screened |
| 6 | 2406.15673 | Large Language Models have Intrinsic Self-Correction Ability | 2024 | title-screened |
| 7 | 2603.12261 | The Latent Color Subspace: Emergent Order in High-Dimensional Chaos | 2026 | title-screened |
| 8 | 2603.02230 | Generalized Discrete Diffusion with Self-Correction | 2026 | title-screened |

## S19: Filipino Tagalog machine translation evaluation

Serves item(s) 7. Purpose: Filipino MT evaluation

Runs: 1 (latest 2026-09-24T07:07:58+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2508.18549 | COMET-poly: Machine Translation Metric Grounded in Other Candidates | 2025 | title-screened |
| 2 | 2403.03521 | BiVert: Bidirectional Vocabulary Evaluation using Relations for Machine Translation | 2024 | title-screened |
| 3 | 2601.03790 | NeoAMT: Neologism-Aware Agentic Machine Translation with Reinforcement Learning | 2026 | title-screened |
| 4 | 2505.20428 | The UD-NewsCrawl Treebank: Reflections and Challenges from a Large-scale Tagalog Syntactic Annotation Project | 2025 | included |
| 5 | 2601.00223 | JP-TL-Bench: Anchored Pairwise LLM Evaluation for Bidirectional Japanese-English Translation | 2026 | title-screened |
| 6 | 2401.01283 | Quality and Quantity of Machine Translation References for Automatic Metrics | 2024 | title-screened |
| 7 | 1710.02095 | Machine Translation Evaluation with Neural Networks | 2017 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2508.20511 | Languages Still Left Behind: Toward a Better Multilingual Machine Translation Benchmark |  | included |

## S20: Philippine languages benchmark large language models

Serves item(s) 7. Purpose: Philippine benchmarks

Runs: 1 (latest 2026-09-24T07:07:59+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2508.03523 | FilBench: Can LLMs Understand and Generate Filipino? | 2025 | included |
| 2 | 2409.15380 | Kalahi: A handcrafted, grassroots cultural LLM evaluation suite for Filipino | 2024 | included |
| 3 | 2111.06053 | Improving Large-scale Language Models and Resources for Filipino | 2021 | title-screened |
| 4 | — | Wiki-40B: Multilingual Language Model Dataset | 2020 | title-screened |
| 5 | 1907.00409 | Evaluating Language Model Finetuning Techniques for Low-resource Languages | 2019 | title-screened |
| 6 | 2410.21200 | BongLLaMA: LLaMA for Bangla Language | 2024 | title-screened |
| 7 | 2502.14301 | SEA-HELM: Southeast Asian Holistic Evaluation of Language Models | 2025 | included |
| 8 | 2411.10083 | Xmodel-1.5: An 1B-scale Multilingual LLM | 2024 | title-screened |

## S21: Cebuano Ilocano low-resource translation

Serves item(s) 7. Purpose: other Philippine languages

Runs: 1 (latest 2026-09-24T07:07:59+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2203.17225 | A Baseline Readability Model for Cebuano | 2022 | title-screened |
| 2 | 2310.00679 | CebuaNER: A New Baseline Cebuano Named Entity Recognition Model | 2023 | title-screened |
| 3 | 2412.05184 | QueEn: A Large Language Model for Quechua-English Translation | 2024 | title-screened |
| 4 | 2310.15612 | Machine Translation for Nko: Tools, Corpora and Baseline Results | 2023 | title-screened |
| 5 | 2304.09919 | The eBible Corpus: Data and Model Benchmarks for Bible Translation for Low-Resource Languages | 2023 | title-screened |
| 6 | 2111.06053 | Improving Large-scale Language Models and Resources for Filipino | 2021 | title-screened |
| 7 | 2410.07830 | NusaMT-7B: Machine Translation for Low-Resource Indonesian Languages with Large Language Models | 2024 | title-screened |
| 8 | 2304.08865 | Romanization-based Large-scale Adaptation of Multilingual Language Models | 2023 | title-screened |

## S22: MQM error annotation machine translation low-resource

Serves item(s) 7. Purpose: error annotation

Runs: 1 (latest 2026-09-24T07:08:00+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2510.24664 | MQM Re-Annotation: A Technique for Collaborative Evaluation of Machine Translation | 2025 | title-screened |
| 2 | 2308.07286 | The Devil is in the Errors: Leveraging Large Language Models for Fine-grained Machine Translation Evaluation | 2023 | included |
| 3 | 2405.16969 | The Multi-Range Theory of Translation Quality Measurement: MQM scoring models and Statistical Quality Control | 2024 | title-screened |
| 4 | 1905.11901 | Revisiting Low-Resource Neural Machine Translation: A Case Study | 2019 | title-screened |
| 5 | 2502.11862 | Understanding In-Context Machine Translation for Low-Resource Languages: A Case Study on Manchu | 2025 | title-screened |
| 6 | 2409.13949 | Mufu: Multilingual Fused Learning for Low-Resource Translation with LLM | 2024 | title-screened |
| 7 | 2603.25222 | Translation or Recitation? Calibrating Evaluation Scores for Machine Translation of Extremely Low-Resource Languages | 2026 | included |
| 8 | 2408.11457 | Expanding FLORES+ Benchmark for more Low-Resource Settings: Portuguese-Emakhuwa Machine Translation Evaluation | 2024 | title-screened |

## S23: DeepSeek V4

Serves item(s) 1, 5. Purpose: confirm DeepSeek V4/V4.1 architecture

Runs: 1 (latest 2026-09-24T07:08:01+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2501.12948 | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning | 2025 | title-screened |
| 2 | 2505.09388 | Qwen3 Technical Report | 2025 | title-screened |
| 3 | 2303.18223 | A Survey of Large Language Models | 2023 | title-screened |
| 4 | 2503.14476 | DAPO: An Open-Source LLM Reinforcement Learning System at Scale | 2025 | title-screened |
| 5 | 2503.09516 | Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning | 2025 | title-screened |
| 6 | 2606.19348 | DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence | 2026 | included |
| 7 | 2609.19969 | DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression | 2026 | included |
| 8 | 2607.20145 | SLAI T-Rex: Full-Parameter Post-training of the DeepSeek-V4 Family on Ascend SuperPOD | 2026 | title-screened |

## S24: DSpark speculative decoding semi-autoregressive draft confidence-scheduled verification

Serves item(s) 1. Purpose: DSpark, used by V4.1-Flash

Runs: 1 (latest 2026-09-24T07:08:02+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2607.05147 | DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation | 2026 | included |
| 2 | 2603.27027 | TAPS: Task Aware Proposal Distributions for Speculative Sampling | 2026 | title-screened |
| 3 | 2603.03251 | Speculative Speculative Decoding | 2026 | title-screened |
| 4 | 2408.11850 | Parallel Speculative Decoding with Adaptive Draft Length | 2024 | title-screened |
| 5 | 2606.24957 | Dustin: Draft-Augmented Sparse Verification for Efficient Long-Context Generation with Speculative Decoding | 2026 | title-screened |
| 6 | 2512.20573 | Fail Fast, Win Big: Rethinking the Drafting Strategy in Speculative Decoding via Diffusion LLMs | 2025 | title-screened |
| 7 | 2601.05724 | Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding | 2026 | title-screened |
| 8 | 2502.04557 | Speeding up Speculative Decoding via Sequential Approximate Verification | 2025 | title-screened |

## S25: You Only Cache Once decoder-decoder architecture

Serves item(s) 1. Purpose: YOCO, basis of V4.1-Flash's encoder-decoder

Runs: 1 (latest 2026-09-24T07:08:03+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2405.05254 | You Only Cache Once: Decoder-Decoder Architectures for Language Models | 2024 | included |
| 2 | 2604.01220 | Universal YOCO for Efficient Depth Scaling | 2026 | title-screened |
| 3 | 2603.03251 | Speculative Speculative Decoding | 2026 | title-screened |
| 4 | 2406.17276 | OPT-Tree: Speculative Decoding with Adaptive Draft Tree Structure | 2024 | title-screened |
| 5 | 2509.04185 | Set Block Decoding is a Language Model Inference Accelerator | 2025 | title-screened |
| 6 | 2602.01519 | You Need an Encoder for Native Position-Independent Caching | 2026 | title-screened |
| 7 | 2507.06607 | Decoder-Hybrid-Decoder Architecture for Efficient Reasoning with Long Generation | 2025 | title-screened |
| 8 | 2609.17652 | Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches | 2026 | title-screened |

## S26: SONAR sentence-level multimodal language-agnostic representations

Serves item(s) 1. Purpose: SONAR and successors

Runs: 1 (latest 2026-09-24T07:08:03+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2308.11466 | SONAR: Sentence-Level Multimodal and Language-Agnostic Representations | 2023 | included |
| 2 | 2603.16606 | Omnilingual SONAR: Cross-Lingual and Cross-Modal Sentence Embeddings Bridging Massively Multilingual Text and Speech | 2026 | included |
| 3 | 2411.17666 | How do Multimodal Foundation Models Encode Text and Speech? An Analysis of Cross-Lingual and Cross-Modal Representations | 2024 | title-screened |
| 4 | 2510.19398 | SONAR-SLT: Multilingual Sign Language Translation via Language-Agnostic Sentence Embedding Supervision | 2025 | title-screened |
| 5 | 2407.11351 | Learning Modality-agnostic Representation for Semantic Segmentation from Any Modalities | 2024 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | 1707.07250 | Tensor Fusion Network for Multimodal Sentiment Analysis | 2017 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 7 | 2505.13777 | Sat2Sound: A Unified Framework for Zero-Shot Soundscape Mapping | 2026 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2205.08180 | SAMU-XLSR: Semantically-Aligned Multimodal Utterance-level Cross-Lingual Speech Representation | 2022 | title-screened |

## S27: text embeddings reveal almost as much as text inversion

Serves item(s) 1. Purpose: decoding text back from embeddings

Runs: 1 (latest 2026-09-24T07:08:04+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2310.06816 | Text Embeddings Reveal (Almost) As Much As Text | 2023 | included |
| 2 | 2502.14862 | Interpretable Text Embeddings and Text Similarity Explanation: A Survey |  | title-screened |
| 3 | 2602.04105 | Expert Selections In MoE Models Reveal (Almost) As Much As Text | 2026 | title-screened |
| 4 | 2603.21437 | Semantic Shift: the Fundamental Challenge in Text Embedding and Retrieval | 2026 | title-screened |
| 5 | 2501.09749 | Enhancing Lexicon-Based Text Embeddings with Large Language Models | 2025 | title-screened |
| 6 | 2504.00147 | Universal Zero-shot Embedding Inversion | 2025 | title-screened |
| 7 | 2509.03020 | Training LLMs to be Better Text Embedders through Bidirectional Reconstruction | 2025 | title-screened |
| 8 | 2412.09165 | When Text Embedding Meets Large Language Model: A Comprehensive Survey | 2024 | title-screened |

## S28: critic model evaluates sentence embedding before decoding

Serves item(s) 1, 3. Purpose: critic operating on sentence embeddings (gap check for option c)

Runs: 1 (latest 2026-09-24T07:08:05+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1806.06259 | Evaluation of sentence embeddings in downstream and linguistic probing tasks | 2018 | excluded (embedding probing benchmark (old)) |
| 2 | 1909.00142 | Evaluation Benchmarks and Learning Criteria for Discourse-Aware Sentence Representations | 2019 | excluded (discourse benchmarks) |
| 3 | 2008.09049 | Discovering Useful Sentence Representations from Large Pretrained Language Models | 2020 | title-screened |
| 4 | 1808.08762 | Sentence Embeddings in NLI with Iterative Refinement Encoders | 2018 | title-screened |
| 5 | 2605.19908 | Where Does Authorship Signal Emerge in Encoder-Based Language Models? | 2026 | excluded (authorship attribution) |
| 6 | 2305.10786 | Ditto: A Simple and Efficient Approach to Improve Sentence Embeddings | 2023 | title-screened |
| 7 | 2310.05703 | An Attribution Method for Siamese Encoders | 2023 | excluded (attribution for Siamese encoders) |
| 8 | 2505.17282 | Attention with Trained Embeddings Provably Selects Important Tokens | 2025 | title-screened |

## S29: generative adversarial network latent space text generation autoencoder

Serves item(s) 1, 3. Purpose: GAN in a continuous latent space for text (the author's analogy)

Runs: 1 (latest 2026-09-24T07:08:06+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1905.12777 | Educating Text Autoencoders: Latent Representation Guidance via Denoising | 2019 | title-screened |
| 2 | 2412.08117 | LatentSpeech: Latent Diffusion for Text-To-Speech Generation | 2024 | excluded (speech synthesis) |
| 3 | 2506.09644 | DGAE: Diffusion-Guided Autoencoder for Efficient Latent Representation Learning | 2025 | excluded (image autoencoders) |
| 4 | 2007.02798 | Gradient Origin Networks | 2020 | excluded (generic generative method, not text) |
| 5 | 2601.16208 | Scaling Text-to-Image Diffusion Transformers with Representation Autoencoders | 2026 | excluded (text-to-image) |
| 6 | 2605.18324 | Improved Baselines with Representation Autoencoders | 2026 | excluded (image autoencoders) |
| 7 | 2502.03444 | Masked Autoencoders Are Effective Tokenizers for Diffusion Models | 2025 | excluded (image tokenizers) |
| 8 | 2112.06749 | Step-unrolled Denoising Autoencoders for Text Generation | 2021 | title-screened |

## S30: mixture of experts expert selection based on output quality critique

Serves item(s) 1, 2. Purpose: critique-driven expert selection in MoE (gap check for the router-level claim)

Runs: 1 (latest 2026-09-24T07:08:08+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.19279 | CritiQ: Mining Data Quality Criteria from Human Preferences | 2025 | excluded (data-quality criteria, not MoE) |
| 2 | 2506.01241 | ExpertLongBench: Benchmarking Language Models on Expert-Level Long-Form Generation Tasks with Structured Checklists | 2025 | excluded (benchmark, not architecture) |
| 3 | 2511.11562 | PRBench: Large-Scale Expert Rubrics for Evaluating High-Stakes Professional Reasoning | 2025 | excluded (benchmark) |
| 4 | 2604.02368 | Xpertbench: Expert Level Tasks with Rubrics-Based Evaluation | 2026 | excluded (benchmark) |
| 5 | 2510.18941 | ProfBench: Multi-Domain Rubrics requiring Professional Knowledge to Answer and Judge | 2025 | excluded (benchmark) |
| 6 | 2512.17776 | DEER: A Benchmark for Evaluating Deep Research Agents on Expert Report Generation | 2025 | excluded (benchmark) |
| 7 | 2604.00477 | Logarithmic Scores, Power-Law Discoveries: Disentangling Measurement from Coverage in Agent-Based Evaluation | 2026 | excluded (agent evaluation measurement) |
| 8 | 2402.18191 | Clustering and Ranking: Diversity-preserved Instruction Selection through Expert-aligned Quality Estimation | 2024 | excluded (instruction data selection) |

## S31: human translation process revision multi-pass cognitive model machine translation

Serves item(s) 1, 6. Purpose: human multi-pass translation as model inspiration

Runs: 1 (latest 2026-09-24T07:08:09+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2306.03856 | Iterative Translation Refinement with Large Language Models | 2023 | included |
| 2 | 2409.06790 | Translating Step-by-Step: Decomposing the Translation Process for Improved Translation Quality of Long-Form Texts | 2024 | title-screened |
| 3 | 2506.08403 | TACTIC: Translation Agents with Cognitive-Theoretic Interactive Collaboration | 2025 | included |
| 4 | 1409.0473 | Neural Machine Translation by Jointly Learning to Align and Translate | 2014 | title-screened |
| 5 | 2503.10351 | New Trends for Modern Machine Translation with Large Reasoning Models | 2025 | title-screened |
| 6 | 2510.11919 | LLM Reasoning for Machine Translation: Synthetic Data Generation over Thinking Tokens | 2025 | title-screened |
| 7 | 2009.09025 | COMET: A Neural Framework for MT Evaluation | 2020 | title-screened |
| 8 | 2508.18549 | COMET-poly: Machine Translation Metric Grounded in Other Candidates | 2025 | title-screened |

## S32: language model knows when it is wrong hidden state probe self-evaluation

Serves item(s) 1, 3. Purpose: self-evaluation from hidden states

Runs: 1 (latest 2026-09-24T07:08:10+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2512.20578 | Can LLMs Predict Their Own Failures? Self-Awareness via Internal Circuits | 2025 | included |
| 2 | 2207.05221 | Language Models (Mostly) Know What They Know | 2022 | included |
| 3 | 2602.01897 | Internal Flow Signatures for Self-Checking and Refinement in LLMs | 2026 | included |
| 4 | 2505.23836 | Large Language Models Often Know When They Are Being Evaluated | 2025 | excluded (evaluation awareness, not error detection) |
| 5 | 2406.19501 | Monitoring Latent World States in Language Models with Propositional Probes | 2024 | title-screened |
| 6 | 2601.01828 | Emergent Introspective Awareness in Large Language Models | 2026 | title-screened |
| 7 | 2603.16331 | Decoding the Critique Mechanism in Large Reasoning Models | 2026 | included |
| 8 | 2602.02416 | Structure Enables Effective Self-Localization of Errors in LLMs | 2026 | title-screened |

## S33: large concept model sentence embedding diffusion follow-up

Serves item(s) 1. Purpose: large concept model follow-ups

Runs: 1 (latest 2026-09-24T07:08:11+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2412.08821 | Large Concept Models: Language Modeling in a Sentence Representation Space | 2024 | included |
| 2 | 2412.02542 | Unveiling Concept Attribution in Diffusion Models | 2024 | excluded (text-to-image concept attribution) |
| 3 | 2603.29239 | Diffusion Mental Averages | 2026 | excluded (image diffusion) |
| 4 | 2505.15045 | Diffusion vs. Autoregressive Language Models: A Text Embedding Perspective | 2025 | title-screened |
| 5 | 2403.13807 | Editing Massive Concepts in Text-to-Image Diffusion Models | 2024 | excluded (text-to-image editing) |
| 6 | 2405.07288 | Erasing Concepts from Text-to-Image Diffusion Models with Few-shot Unlearning | 2024 | excluded (text-to-image unlearning) |
| 7 | 2602.11047 | Embedding Inversion via Conditional Masked Diffusion Language Models | 2026 | included |
| 8 | 2510.03206 | Coevolutionary Continuous Discrete Diffusion: Make Your Diffusion Language Model a Latent Reasoner | 2025 | title-screened |

## S34: adaptive computation per sentence segment level early exit

Serves item(s) 1, 4. Purpose: dynamic compute per sentence rather than per token

Runs: 1 (latest 2026-09-24T07:08:12+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1603.08983 | Adaptive Computation Time for Recurrent Neural Networks | 2016 | included |
| 2 | 2310.05424 | Fast and Robust Early-Exiting Framework for Autoregressive Language Models with Synchronized Parallel Decoding | 2023 | title-screened |
| 3 | 2509.23666 | Beyond Greedy Exits: Improved Early Exit Decisions for Risk Control and Reliability | 2025 | title-screened |
| 4 | 2309.09546 | Training dynamic models using early exits for automatic speech recognition on resource-constrained devices | 2023 | excluded (speech early-exit (per-frame), not text) |
| 5 | 2405.15198 | RAEE: A Robust Retrieval-Augmented Early Exit Framework for Efficient Inference | 2024 | excluded (retrieval early-exit, not critique) |
| 6 | 2502.00745 | BEEM: Boosting Performance of Early Exit DNNs using Multi-Exit Classifiers as Experts | 2025 | excluded (vision early-exit) |
| 7 | 2312.10193 | Adaptive Computation Modules: Granular Conditional Computation For Efficient Inference | 2023 | excluded (screened 2026-10-07 (S103): per-token learner gating under user budgets; no per-action cost heterogeneity or RL cost penalty, not cited) |
| 8 | 2506.18035 | Splitformer: An improved early-exit architecture for automatic speech recognition on edge devices | 2025 | excluded (speech early-exit) |

## S35: unsupervised verifier learned from pretraining without reward labels

Serves item(s) 3. Purpose: critic trained without human labels

Runs: 1 (latest 2026-09-24T07:08:13+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2604.18547 | FUSE: Ensembling Verifiers with Zero Labeled Data | 2026 | title-screened |
| 2 | 2503.12917 | Verification Learning: Make Unsupervised Neuro-Symbolic System Feasible | 2025 | title-screened |
| 3 | 2604.12002 | Self-Distillation Zero: Self-Revision Turns Binary Rewards into Dense Supervision | 2026 | title-screened |
| 4 | 2505.16022 | NOVER: Incentive Training for Language Models via Verifier-Free Reinforcement Learning | 2025 | title-screened |
| 5 | 2605.10158 | Unsupervised Process Reward Models | 2026 | title-screened |
| 6 | 2605.28805 | OmniVerifier-M1: Multimodal Meta-Verifier with Explicit Structured Recalibration | 2026 | title-screened |
| 7 | 2408.02666 | Self-Taught Evaluators | 2024 | title-screened |
| 8 | 2411.11504 | Search, Verify and Feedback: Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering | 2024 | title-screened |

## S36: sparsely-gated mixture of experts layer router

Serves item(s) 2. Purpose: foundational MoE router papers to define 'prior routing' (write-up)

Runs: 1 (latest 2026-09-24T08:28:11+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2209.08326 | Parameter-Efficient Conformers via Sharing Sparsely-Gated Experts for End-to-End Speech Recognition | 2022 | title-screened |
| 2 | 2604.14419 | Equifinality in Mixture of Experts: Routing Topology Does Not Determine Language Modeling Quality | 2026 | title-screened |
| 3 | 2411.19402 | On the effectiveness of discrete representations in sparse mixture of experts | 2024 | title-screened |
| 4 | 2607.28308 | Beyond Geometric Complementarity: Coherent Overlap in Sparse Mixture-of-Experts Routing | 2026 | title-screened |
| 5 | 2606.12397 | Redesign Mixture-of-Experts Routers with Manifold Power Iteration | 2026 | title-screened |
| 6 | 2312.07035 | HyperRouter: Towards Efficient Training and Inference of Sparse Mixture of Experts | 2023 | title-screened |
| 7 | 2110.07431 | Towards More Effective and Economic Sparsely-Activated Model | 2021 | title-screened |
| 8 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |

## S37: group relative policy optimization reinforcement learning language model

Serves item(s) 2. Purpose: RL algorithms to name for the critique router (write-up)

Runs: 1 (latest 2026-09-24T08:28:12+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.03143 | Self-Hinting Language Models Enhance Reinforcement Learning | 2026 | title-screened |
| 2 | 2601.12730 | Distribution-Centric Policy Optimization Dominates Exploration-Exploitation Trade-off | 2026 | title-screened |
| 3 | 2506.09340 | RePO: Replay-Enhanced Policy Optimization | 2025 | title-screened |
| 4 | 2511.00066 | Sharpness-Guided Group Relative Policy Optimization via Probability Shaping | 2025 | title-screened |
| 5 | 2604.02288 | Unifying Group-Relative and Self-Distillation Policy Optimization via Sample Routing | 2026 | title-screened |
| 6 | 2601.22582 | MC-GRPO: Median-Centered Group Relative Policy Optimization for Small-Rollout Reinforcement Learning | 2026 | title-screened |
| 7 | 2505.09655 | DRA-GRPO: Exploring Diversity-Aware Reward Adjustment for R1-Zero-Like Training of Large Language Models | 2025 | title-screened |
| 8 | 2509.21792 | FastGRPO: Accelerating Policy Optimization via Concurrency-aware Speculative Decoding and Online Draft Learning | 2025 | title-screened |

## S38: proximal policy optimization algorithms

Serves item(s) 2. Purpose: PPO reference (write-up)

Runs: 1 (latest 2026-09-24T08:28:13+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1707.06347 | Proximal Policy Optimization Algorithms | 2017 | included |
| 2 | 2602.01156 | PolicyFlow: Policy Optimization with Continuous Normalizing Flow in Reinforcement Learning | 2026 | title-screened |
| 3 | 2205.09123 | A2C is a special case of PPO | 2022 | title-screened |
| 4 | 2302.11312 | Behavior Proximal Policy Optimization | 2023 | title-screened |
| 5 | 2604.18578 | Bounded Ratio Reinforcement Learning | 2026 | title-screened |
| 6 | 2103.01955 | The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games | 2021 | title-screened |
| 7 | 2411.01798 | SALSA: Soup-based Alignment Learning for Stronger Adaptation in RLHF | 2024 | title-screened |
| 8 | 2305.09655 | RAMario: Experimental Approach to Reptile Algorithm -- Reinforcement Learning for Mario | 2023 | title-screened |

## S39: DeepSeekMoE expert specialization fine-grained experts

Serves item(s) 2. Purpose: fine-grained expert routing as used by DeepSeek (write-up)

Runs: 1 (latest 2026-09-24T08:28:14+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.05711 | OmniMoE: An Efficient MoE by Orchestrating Atomic Experts at Scale | 2026 | title-screened |
| 2 | 2401.06066 | DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models | 2024 | included |
| 3 | 2505.10860 | On DeepSeekMoE: Statistical Benefits of Shared Experts and Normalized Sigmoid Gating | 2025 | title-screened |
| 4 | 2602.12556 | SD-MoE: Spectral Decomposition for Effective Expert Specialization | 2026 | title-screened |
| 5 | 2504.06792 | Domain-Specific Pruning of Large Mixture-of-Experts Models with Few-shot Demonstrations | 2025 | title-screened |
| 6 | 2505.06839 | The power of fine-grained experts: Granularity boosts expressivity in Mixture of Experts | 2025 | title-screened |
| 7 | 2506.23266 | Sub-MoE: Efficient Mixture-of-Expert LLMs Compression via Subspace Expert Merging | 2025 | title-screened |
| 8 | 2405.04434 | DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model | 2024 | title-screened |

## S40: Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer

Serves item(s) 2. Purpose: original sparsely-gated MoE paper (title search)

Runs: 1 (latest 2026-09-24T08:28:24+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1701.06538 | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | 2017 | included |
| 2 | 2410.08003 | More Experts Than Galaxies: Conditionally-Overlapping Experts with Biologically-Inspired Fixed Routing | 2024 | title-screened |
| 3 | 1312.4314 | Learning Factored Representations in a Deep Mixture of Experts | 2013 | title-screened |
| 4 | 2403.08245 | Scattered Mixture-of-Experts Implementation | 2024 | title-screened |
| 5 | 2208.02813 | Towards Understanding Mixture of Experts in Deep Learning | 2022 | title-screened |
| 6 | 2105.15082 | M6-T: Exploring Sparse Expert Models and Beyond | 2021 | title-screened |
| 7 | 2505.06839 | The power of fine-grained experts: Granularity boosts expressivity in Mixture of Experts | 2025 | title-screened |
| 8 | 2504.12463 | Dense Backpropagation Improves Training for Sparse Mixture-of-Experts | 2025 | title-screened |

## S41: DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models

Serves item(s) 2. Purpose: paper that introduced GRPO (title search)

Runs: 1 (latest 2026-09-24T08:28:35+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2402.03300 | DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models | 2024 | included |
| 2 | 2511.22570 | DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning | 2025 | title-screened |
| 3 | 2511.19333 | Learning to Reason: Training LLMs with GPT-OSS or DeepSeek R1 Reasoning Traces | 2025 | title-screened |
| 4 | 2502.06772 | ReasonFlux: Hierarchical LLM Reasoning via Scaling Thought Templates | 2025 | title-screened |
| 5 | 2605.29247 | DenseSteer: Steering Small Language Models towards Dense Math Reasoning | 2026 | title-screened |
| 6 | 2505.08311 | AM-Thinking-v1: Advancing the Frontier of Reasoning at 32B Scale | 2025 | title-screened |
| 7 | 2503.12524 | EXAONE Deep: Reasoning Enhanced Language Models | 2025 | title-screened |
| 8 | 2501.04519 | rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking | 2025 | title-screened |

## S42: Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity

Serves item(s) 2. Purpose: Switch Transformer top-1 routing (title search)

Runs: 1 (latest 2026-09-24T08:28:47+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2101.03961 | Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity | 2021 | included |
| 2 | 2309.08520 | Scaling Laws for Sparsely-Connected Foundation Models | 2023 | title-screened |
| 3 | 2404.01847 | Accelerating Transformer Pre-training with 2:4 Sparsity | 2024 | title-screened |
| 4 | 2410.23168 | TokenFormer: Rethinking Transformer Scaling with Tokenized Model Parameters | 2024 | title-screened |
| 5 | 2505.23949 | TSENOR: Highly-Efficient Algorithm for Finding Transposable N:M Sparse Masks | 2025 | title-screened |
| 6 | 2210.06313 | The Lazy Neuron Phenomenon: On Emergence of Activation Sparsity in Transformers | 2022 | title-screened |
| 7 | 2211.13184 | TorchScale: Transformers at Scale | 2022 | title-screened |
| 8 | 2503.11272 | When Do Transformers Outperform Feedforward and Recurrent Networks? A Statistical Perspective | 2025 | title-screened |

## S43: Deliberation Networks: Sequence Generation Beyond One-Pass Decoding

Serves item(s) 1. Purpose: Deliberation Networks (NIPS 2017) title search; review M4 (2026-09-24). Checks whether the catalogue holds this non-arXiv paper

Runs: 1 (latest 2026-09-24T11:07:18+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2203.16487 | Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation | 2022 | title-screened |
| 2 | 1811.03115 | Blockwise Parallel Decoding for Deep Autoregressive Models | 2018 | title-screened |
| 3 | 1906.05275 | Keeping Notes: Conditional Natural Language Generation with a Scratchpad Mechanism | 2019 | title-screened |
| 4 | 2602.10603 | dnaHNet: A Scalable and Hierarchical Foundation Model for Genomic Sequence Learning | 2026 | title-screened |
| 5 | 2410.18234 | Multi-Draft Speculative Sampling: Canonical Decomposition and Theoretical Limits | 2024 | title-screened |
| 6 | 2510.08169 | Bidirectional Representations Augmented Autoregressive Biological Sequence Generation:Application in De Novo Peptide Sequencing | 2025 | title-screened |
| 7 | 2404.09221 | Exploring and Improving Drafts in Blockwise Parallel Decoding | 2024 | title-screened |
| 8 | 1906.09601 | Sequence Generation: From Both Sides to the Middle | 2019 | title-screened |

## S44: deliberation networks

Serves item(s) 1. Purpose: Deliberation Networks, keyword search (same purpose as S43)

Runs: 1 (latest 2026-09-24T11:07:19+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2601.16863 | Mixture-of-Models: Unifying Heterogeneous Agents via N-Way Self-Evaluating Deliberation | 2026 | title-screened |
| 2 | 2503.18962 | Representative Ranking for Deliberation in the Public Sphere | 2025 | title-screened |
| 3 | 2510.05154 | Can AI Truly Represent Your Voice in Deliberations? A Comprehensive Study of Large-Scale Opinion Aggregation with LLMs | 2025 | title-screened |
| 4 | 2405.09463 | Gaze-DETR: Using Expert Gaze to Reduce False Positives in Vulvovaginal Candidiasis Screening |  | title-screened |
| 5 | 2301.12530 | G-Rank: Unsupervised Continuous Learn-to-Rank for Edge Devices in a P2P Network | 2023 | title-screened |
| 6 | 2403.16812 | Towards Human-AI Deliberation: Design and Evaluation of LLM-Empowered Deliberative AI for AI-Assisted Decision-Making | 2024 | title-screened |
| 7 | 2506.20877 | THIRDEYE: Cue-Aware Monocular Depth Estimation via Brain-Inspired Multi-Stage Fusion | 2025 | title-screened |
| 8 | 2502.12973 | Optimizing Social Network Interventions via Hypergradient-Based Recommender System Design | 2025 | title-screened |

## S45: mixture of experts sparsely gated routing survey

Serves item(s) 1, 2. Purpose: MoE survey (explainer foundations) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:16+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2607.28308 | Beyond Geometric Complementarity: Coherent Overlap in Sparse Mixture-of-Experts Routing | 2026 | title-screened |
| 2 | 2604.14419 | Equifinality in Mixture of Experts: Routing Topology Does Not Determine Language Modeling Quality | 2026 | title-screened |
| 3 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 4 | 2601.03425 | The Illusion of Specialization: Unveiling the Domain-Invariant "Standing Committee" in Mixture-of-Experts Models | 2026 | title-screened |
| 5 | 2405.14131 | Statistical Advantages of Perturbing Cosine Router in Mixture of Experts | 2024 | title-screened |
| 6 | 2110.07431 | Towards More Effective and Economic Sparsely-Activated Model | 2021 | title-screened |
| 7 | 2306.03745 | Soft Merging of Experts with Adaptive Routing | 2023 | title-screened |
| 8 | 2411.19402 | On the effectiveness of discrete representations in sparse mixture of experts | 2024 | title-screened |
| 9 | 2312.07035 | HyperRouter: Towards Efficient Training and Inference of Sparse Mixture of Experts | 2023 | title-screened |
| 10 | 2505.10860 | On DeepSeekMoE: Statistical Benefits of Shared Experts and Normalized Sigmoid Gating | 2025 | title-screened |

## S46: GShard scaling giant models conditional computation automatic sharding

Serves item(s) 1, 2. Purpose: GShard: first large MoE transformer for multilingual MT (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:17+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2006.16668 | GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding | 2020 | title-screened |
| 2 | 2605.05664 | Sparse-to-Complete: From Sparse Image Captures to Complete 3D Scenes | 2026 | title-screened |
| 3 | — | RaPTGS: Render-Agnostic Post-Training Compression of 3D Gaussian Splatting |  | title-screened |
| 4 | 2605.20150 | TideGS: Scalable Training of Over One Billion 3D Gaussian Splatting Primitives via Out-of-Core Optimization | 2026 | title-screened |
| 5 | 2512.18692 | EcoSplat: Efficiency-controllable Feed-forward 3D Gaussian Splatting from Multi-view Images | 2025 | title-screened |

## S47: router z-loss stable transferable sparse expert models

Serves item(s) 1, 2. Purpose: ST-MoE: training stability, router z-loss (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:18+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2312.07035 | HyperRouter: Towards Efficient Training and Inference of Sparse Mixture of Experts | 2023 | title-screened |
| 2 | 2411.19402 | On the effectiveness of discrete representations in sparse mixture of experts | 2024 | title-screened |
| 3 | 2202.08906 | ST-MoE: Designing Stable and Transferable Sparse Expert Models | 2022 | title-screened |
| 4 | 2602.08621 | Sparse Models, Sparse Safety: Unsafe Routes in Mixture-of-Experts LLMs | 2026 | title-screened |
| 5 | 2504.12463 | Dense Backpropagation Improves Training for Sparse Mixture-of-Experts | 2025 | title-screened |

## S48: expert choice routing mixture of experts

Serves item(s) 1, 2. Purpose: Expert-choice routing (experts pick tokens) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:19+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2202.09368 | Mixture-of-Experts with Expert Choice Routing | 2022 | title-screened |
| 2 | 2603.11535 | Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing | 2026 | title-screened |
| 3 | 2605.11689 | Slicing and Dicing: Configuring Optimal Mixtures of Experts | 2026 | title-screened |
| 4 | 2604.01622 | Expert-Choice Routing Enables Adaptive Computation in Diffusion Language Models | 2026 | title-screened |
| 5 | — | Deterministic multi-hash routing supports long-horizon training in a compact language model | 2026 | title-screened |

## S49: hash layers large sparse models

Serves item(s) 1, 2. Purpose: Hash routing (no learned router) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:19+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2106.04426 | Hash Layers For Large Sparse Models | 2021 | title-screened |
| 2 | 2112.14397 | EvoMoE: An Evolutional Mixture-of-Experts Training Framework via Dense-To-Sparse Gate | 2021 | title-screened |
| 3 | 2601.21461 | $L^3$: Large Lookup Layers | 2026 | title-screened |
| 4 | 2502.14770 | Determining Layer-wise Sparsity for Large Language Models Through a Theoretical Perspective | 2025 | title-screened |
| 5 | 2606.26519 | Boundary-Aware Context Grounding for A Low-Channel EEG Agent | 2026 | title-screened |

## S50: BASE layers balanced assignment of experts

Serves item(s) 1, 2. Purpose: BASE layers: routing as balanced assignment (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:20+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2103.16716 | BASE Layers: Simplifying Training of Large, Sparse Models | 2021 | title-screened |
| 2 | 2106.04426 | Hash Layers For Large Sparse Models | 2021 | title-screened |
| 3 | 2502.15451 | Binary-Integer-Programming Based Algorithm for Expert Load Balancing in Mixture-of-Experts Models | 2025 | title-screened |
| 4 | 2512.03915 | A Theoretical Framework for Auxiliary-Loss-Free Load Balancing of Sparse Mixture-of-Experts in Large-Scale AI Models | 2025 | title-screened |
| 5 | — | OneSparse: A Unified Framework for Sparse Activation Layers in Vision Models |  | title-screened |

## S51: soft mixture of experts

Serves item(s) 1, 2. Purpose: Soft MoE (weighted token mixtures) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:20+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2410.01930 | Don't flatten, tokenize! Unlocking the key to SoftMoE's efficacy in deep RL | 2024 | title-screened |
| 2 | 2507.06363 | Mamba Goes HoME: Hierarchical Soft Mixture-of-Experts for 3D Medical Image Segmentation | 2025 | title-screened |
| 3 | 2510.16138 | Expert Merging in Sparse Mixture of Experts with Nash Bargaining | 2025 | title-screened |
| 4 | 2308.00951 | From Sparse to Soft Mixtures of Experts | 2023 | title-screened |
| 5 | 2408.17280 | Flexible and Effective Mixing of Large Language Models into a Mixture of Domain Experts | 2024 | title-screened |

## S52: auxiliary-loss-free load balancing mixture of experts

Serves item(s) 1, 2. Purpose: Load balancing without auxiliary loss (DeepSeek) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:21+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2408.15664 | Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts | 2024 | title-screened |
| 2 | 2512.03915 | A Theoretical Framework for Auxiliary-Loss-Free Load Balancing of Sparse Mixture-of-Experts in Large-Scale AI Models | 2025 | title-screened |
| 3 | 2604.23036 | Preserving Long-Tailed Expert Information in Mixture-of-Experts Tuning | 2026 | title-screened |
| 4 | 2412.19437 | DeepSeek-V3 Technical Report | 2024 | included |
| 5 | 2501.11873 | Demons in the Detail: On Implementing Load Balancing Loss for Training Specialized Mixture-of-Expert Models | 2025 | title-screened |
| 6 | 2502.15451 | Binary-Integer-Programming Based Algorithm for Expert Load Balancing in Mixture-of-Experts Models | 2025 | title-screened |

## S53: sparse upcycling dense checkpoint mixture of experts

Serves item(s) 1, 2. Purpose: Sparse upcycling: MoE from dense checkpoints (relevant to our encoder) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:22+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2212.05055 | Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints | 2022 | title-screened |
| 2 | 2502.19261 | Drop-Upcycling: Training Sparse Mixture of Experts with Partial Re-initialization | 2025 | title-screened |
| 3 | 2510.08008 | Recycling Pretrained Checkpoints: Orthogonal Growth of Mixture-of-Experts for Efficient Large Language Model Pre-Training | 2025 | title-screened |
| 4 | 2602.11543 | Pretraining A Large Language Model using Distributed GPUs: A Memory-Efficient Decentralized Paradigm | 2026 | title-screened |
| 5 | 2409.19291 | CLIP-MoE: Towards Building Mixture of Experts for CLIP with Diversified Multiplet Upcycling | 2024 | title-screened |

## S54: MegaBlocks efficient sparse training mixture of experts

Serves item(s) 1, 2. Purpose: MoE systems: dropless training kernels (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:23+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2211.15841 | MegaBlocks: Efficient Sparse Training with Mixture-of-Experts | 2022 | title-screened |
| 2 | 2105.15082 | M6-T: Exploring Sparse Expert Models and Beyond | 2021 | title-screened |
| 3 | 2403.08245 | Scattered Mixture-of-Experts Implementation | 2024 | title-screened |
| 4 | 2504.12463 | Dense Backpropagation Improves Training for Sparse Mixture-of-Experts | 2025 | title-screened |
| 5 | 2609.21346 | IntBMoE: Integrating Block-Level Conditioning into Expert Composition for Full-Participation Mixture-of-Experts | 2026 | title-screened |

## S55: Mixtral of experts

Serves item(s) 1, 2. Purpose: Mixtral: open MoE model (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:24+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2401.04088 | Mixtral of Experts | 2024 | title-screened |
| 2 | 2506.23266 | Sub-MoE: Efficient Mixture-of-Expert LLMs Compression via Subspace Expert Merging | 2025 | title-screened |
| 3 | 2604.06515 | Efficient Quantization of Mixture-of-Experts with Theoretical Generalization Guarantees | 2026 | title-screened |
| 4 | 2508.18376 | Mining Tensor/Neuron-Level Sparsity to Maximize Mixture-of-Experts Potential in Post-Training and Inference | 2025 | title-screened |
| 5 | 1312.4314 | Learning Factored Representations in a Deep Mixture of Experts | 2013 | title-screened |

## S56: OLMoE open mixture of experts language models

Serves item(s) 1, 2. Purpose: OLMoE: fully open MoE with specialisation analysis (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:25+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2409.02060 | OLMoE: Open Mixture-of-Experts Language Models | 2024 | title-screened |
| 2 | 2402.01739 | OpenMoE: An Early Effort on Open Mixture-of-Experts Language Models | 2024 | title-screened |
| 3 | 2607.09424 | A Sovereign, Open-Source Foundation Model for German and English | 2026 | title-screened |
| 4 | 2411.00918 | LIBMoE: A Library for comprehensive benchmarking Mixture of Experts in Large Language Models | 2024 | title-screened |
| 5 | 2509.22745 | SafeMoE: Safe Fine-Tuning for MoE LLMs by Aligning Harmful Input Routing | 2025 | title-screened |

## S57: scaling laws fine-grained mixture of experts

Serves item(s) 1, 2. Purpose: MoE scaling laws / granularity (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:25+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2402.07871 | Scaling Laws for Fine-Grained Mixture of Experts | 2024 | title-screened |
| 2 | 2509.24244 | Model Merging Scaling Laws in Large Language Models | 2026 | title-screened |
| 3 | 2407.04153 | Mixture of A Million Experts | 2024 | title-screened |
| 4 | 2512.05564 | ProPhy: Progressive Physical Alignment for Dynamic World Simulation | 2025 | title-screened |
| 5 | 2507.17702 | Towards Greater Leverage: Scaling Laws for Efficient Mixture-of-Experts Language Models | 2025 | title-screened |
| 6 | 2507.09404 | Scaling Laws for Optimal Data Mixtures | 2025 | title-screened |

## S58: unified scaling laws routed language models

Serves item(s) 1, 2. Purpose: Scaling laws for routed LMs (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:26+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2202.01169 | Unified Scaling Laws for Routed Language Models | 2022 | title-screened |
| 2 | 2405.10938 | Observational Scaling Laws and the Predictability of Language Model Performance | 2024 | title-screened |
| 3 | 2505.23926 | Point-MoE: Towards Cross-Domain Generalization in 3D Semantic Segmentation via Mixture-of-Experts | 2025 | title-screened |
| 4 | 2210.11399 | Transcending Scaling Laws with 0.1% Extra Compute | 2022 | title-screened |
| 5 | 2301.03728 | Scaling Laws for Generative Mixed-Modal Language Models | 2023 | title-screened |

## S59: what do experts learn mixture of experts specialization analysis

Serves item(s) 1, 2. Purpose: Expert specialisation evidence (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:27+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 2 | 2601.03425 | The Illusion of Specialization: Unveiling the Domain-Invariant "Standing Committee" in Mixture-of-Experts Models | 2026 | title-screened |
| 3 | 2405.14124 | Mixture of Experts Meets Prompt-Based Continual Learning | 2024 | title-screened |
| 4 | 2208.03306 | Branch-Train-Merge: Embarrassingly Parallel Training of Expert Language Models | 2022 | title-screened |
| 5 | 1110.2058 | Convergence Rates for Mixture-of-Experts | 2011 | title-screened |
| 6 | 1312.4314 | Learning Factored Representations in a Deep Mixture of Experts | 2013 | title-screened |
| 7 | 2509.25278 | MAESTRO : Adaptive Sparse Attention and Robust Learning for Multimodal Dynamic Time Series | 2025 | title-screened |
| 8 | 2602.10585 | Neural Additive Experts: Context-Gated Experts for Controllable Model Additivity | 2026 | title-screened |

## S60: mixture of experts routing

Serves item(s) 1, 2. Purpose: Recent MoE routing work (2025+) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:27+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2607.28308 | Beyond Geometric Complementarity: Coherent Overlap in Sparse Mixture-of-Experts Routing | 2026 | title-screened |
| 2 | 2604.14419 | Equifinality in Mixture of Experts: Routing Topology Does Not Determine Language Modeling Quality | 2026 | title-screened |
| 3 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 4 | 2602.09001 | DirMoE: Dirichlet-Routed Mixture of Experts | 2026 | title-screened |
| 5 | 2505.16056 | Not All Models Suit Expert Offloading: On Local Routing Consistency of Mixture-of-Expert Models | 2025 | title-screened |
| 6 | 2606.01509 | ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts | 2026 | title-screened |
| 7 | 2509.25684 | LD-MoLE: Learnable Dynamic Routing for Mixture of LoRA Experts | 2025 | title-screened |
| 8 | 2510.04694 | Multilingual Routing in Mixture-of-Experts | 2025 | title-screened |
| 9 | 2603.11535 | Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing | 2026 | title-screened |
| 10 | 2512.23447 | Coupling Experts and Routers in Mixture-of-Experts via an Auxiliary Loss | 2025 | title-screened |
| 11 | 2510.13462 | Who Speaks for the Trigger? Dynamic Expert Routing in Backdoored Mixture-of-Experts Transformers | 2025 | title-screened |
| 12 | 2601.04416 | Transitive Expert Error and Routing Problems in Complex AI Systems | 2026 | title-screened |
| 13 | 2511.13344 | YOLO Meets Mixture-of-Experts: Adaptive Expert Routing for Robust Object Detection | 2025 | title-screened |
| 14 | 2601.03425 | The Illusion of Specialization: Unveiling the Domain-Invariant "Standing Committee" in Mixture-of-Experts Models | 2026 | title-screened |
| 15 | 2512.22741 | A Text-Routed Sparse Mixture-of-Experts Model with Explanation and Temporal Alignment for Multi-Modal Sentiment Analysis | 2025 | title-screened |

## S61: mixture of experts expert specialization

Serves item(s) 1, 2. Purpose: Recent expert specialisation work (2025+) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:28+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2601.03425 | The Illusion of Specialization: Unveiling the Domain-Invariant "Standing Committee" in Mixture-of-Experts Models | 2026 | title-screened |
| 2 | 2512.19765 | How Many Experts Are Enough? Towards Optimal Semantic Specialization for Mixture-of-Experts | 2025 | title-screened |
| 3 | 2602.12556 | SD-MoE: Spectral Decomposition for Effective Expert Specialization | 2026 | title-screened |
| 4 | 2505.22323 | Advancing Expert Specialization for Better MoE | 2025 | title-screened |
| 5 | 2604.13508 | Enhancing Mixture-of-Experts Specialization via Cluster-Aware Upcycling | 2026 | title-screened |
| 6 | 2508.19594 | Understanding and Leveraging the Expert Specialization of Context Faithfulness in Mixture-of-Experts LLMs | 2025 | title-screened |
| 7 | 2507.23279 | Unveiling Super Experts in Mixture-of-Experts Large Language Models | 2025 | title-screened |
| 8 | 2510.13079 | GatePro: Parameter-Free Expert Selection Optimization for Mixture-of-Experts Models | 2025 | title-screened |
| 9 | 2502.17187 | Evaluating Expert Contributions in a MoE LLM for Quiz-Based Tasks | 2025 | title-screened |
| 10 | 2506.08356 | MedMoE: Modality-Specialized Mixture of Experts for Medical Vision-Language Understanding | 2025 | title-screened |

## S62: mixture of experts load balancing

Serves item(s) 1, 2. Purpose: Recent load-balancing work (2025+) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:29+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.15451 | Binary-Integer-Programming Based Algorithm for Expert Load Balancing in Mixture-of-Experts Models | 2025 | title-screened |
| 2 | 2512.03915 | A Theoretical Framework for Auxiliary-Loss-Free Load Balancing of Sparse Mixture-of-Experts in Large-Scale AI Models | 2025 | title-screened |
| 3 | 2501.11873 | Demons in the Detail: On Implementing Load Balancing Loss for Training Specialized Mixture-of-Expert Models | 2025 | title-screened |
| 4 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 5 | 2601.17111 | Least-Loaded Expert Parallelism: Load Balancing An Imbalanced Mixture-of-Experts | 2026 | title-screened |
| 6 | 2605.15403 | $\phi$-Balancing for Mixture-of-Experts Training | 2026 | title-screened |
| 7 | 2605.11689 | Slicing and Dicing: Configuring Optimal Mixtures of Experts | 2026 | title-screened |
| 8 | 2601.03425 | The Illusion of Specialization: Unveiling the Domain-Invariant "Standing Committee" in Mixture-of-Experts Models | 2026 | title-screened |
| 9 | 2505.22323 | Advancing Expert Specialization for Better MoE | 2025 | title-screened |
| 10 | 2505.21411 | Pangu Pro MoE: Mixture of Grouped Experts for Efficient Sparsity | 2025 | title-screened |

## S63: mixture of experts machine translation multilingual

Serves item(s) 1, 2. Purpose: MoE for multilingual MT (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:30+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2605.24681 | Mix-MoE: Improving Multilingual Machine Translation of Large Language Models through Mixed MoEs | 2026 | title-screened |
| 2 | 1806.02525 | Multi-Source Neural Machine Translation with Missing Data | 2018 | title-screened |
| 3 | 2310.12236 | Direct Neural Machine Translation with Task-level Mixture of Experts models | 2023 | title-screened |
| 4 | 2212.07571 | Fixing MoE Over-Fitting on Low-Resource Languages in Multilingual Machine Translation | 2022 | title-screened |
| 5 | 2603.16309 | Omnilingual MT: Machine Translation for 1,600 Languages | 2026 | included |
| 6 | 2212.09811 | Memory-efficient NLLB-200: Language-specific Expert Pruning of a Massively Multilingual Machine Translation Model | 2022 | title-screened |
| 7 | 2401.10440 | Breaking the Curse of Multilinguality with Cross-lingual Expert Language Models | 2024 | title-screened |
| 8 | 2411.01474 | MoCE: Adaptive Mixture of Contextualization Experts for Byte-based Neural Machine Translation | 2024 | title-screened |

## S64: mixture-of-depths dynamically allocating compute transformer

Serves item(s) 1, 2. Purpose: Mixture-of-Depths: token-level compute routing (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:31+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2404.02258 | Mixture-of-Depths: Dynamically allocating compute in transformer-based language models | 2024 | title-screened |
| 2 | 2410.13184 | Router-Tuning: A Simple and Effective Approach for Enabling Dynamic-Depth in Transformers | 2024 | title-screened |
| 3 | 2602.08864 | Understanding Dynamic Compute Allocation in Recurrent Transformers | 2026 | excluded (screened 2026-10-07 (S103): token-level halting analysis; no per-stage cost penalty, not cited) |
| 4 | 2307.16375 | UniAP: Unifying Inter- and Intra-Layer Automatic Parallelism by Mixed Integer Quadratic Programming |  | title-screened |
| 5 | 2301.13310 | Alternating Updates for Efficient Transformers | 2023 | title-screened |

## S65: PonderNet learning to ponder

Serves item(s) 1, 2. Purpose: PonderNet: learned halting (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:31+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2107.05407 | PonderNet: Learning to Ponder | 2021 | title-screened |
| 2 | 2402.17896 | Researchy Questions: A Dataset of Multi-Perspective, Decompositional Questions for LLM Web Agents | 2024 | title-screened |
| 3 | 1602.02261 | End-to-End Goal-Driven Web Navigation | 2016 | title-screened |
| 4 | 2109.04832 | Asking It All: Generating Contextualized Questions for any Semantic Role | 2021 | title-screened |
| 5 | 2112.08656 | DREAM: Improving Situational QA by First Elaborating the Situation | 2021 | title-screened |

## S66: universal transformers

Serves item(s) 1, 2. Purpose: Universal Transformers: recurrent depth with ACT (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:32+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1807.03819 | Universal Transformers | 2018 | title-screened |
| 2 | 2405.16039 | MoEUT: Mixture-of-Experts Universal Transformers | 2024 | title-screened |
| 3 | 2310.07096 | Sparse Universal Transformer | 2023 | title-screened |
| 4 | 2405.07905 | PLUTO: Pathology-Universal Transformer | 2024 | title-screened |
| 5 | 2303.13072 | Beyond Universal Transformer: block reusing with adaptor in Transformer for automatic speech recognition | 2023 | title-screened |

## S67: confident adaptive language modeling early exit

Serves item(s) 1, 2. Purpose: CALM: early exit per token (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:33+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2207.07061 | Confident Adaptive Language Modeling | 2022 | title-screened |
| 2 | 2310.05424 | Fast and Robust Early-Exiting Framework for Autoregressive Language Models with Synchronized Parallel Decoding | 2023 | title-screened |
| 3 | 2211.11152 | You Need Multiple Exiting: Dynamic Early Exiting for Accelerating Unified Vision Language Model | 2022 | title-screened |
| 4 | 2310.18239 | Fine-Tuning Language Models Using Formal Methods Feedback | 2023 | title-screened |
| 5 | 2605.31170 | Emergent Languages in Populations of Language Model Agents: From Token Efficiency to Oversight Evasion | 2026 | title-screened |

## S68: scaling laws reward model overoptimization

Serves item(s) 1, 2. Purpose: Reward over-optimisation (Goodhart) evidence (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:34+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2210.10760 | Scaling Laws for Reward Model Overoptimization | 2022 | title-screened |
| 2 | 2502.18969 | (Mis)Fitting: A Survey of Scaling Laws | 2025 | title-screened |
| 3 | 2406.02900 | Scaling Laws for Reward Model Overoptimization in Direct Alignment Algorithms | 2024 | title-screened |
| 4 | 2605.01640 | Prescriptive Scaling Laws for Data Constrained Training | 2026 | title-screened |
| 5 | 2608.07222 | Skaling: Chinchilla's Exponents Meet Kaplan's Coupling | 2026 | title-screened |

## S69: attention is all you need transformer

Serves item(s) 1, 2. Purpose: Transformer foundations (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:34+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2308.07661 | Attention Is Not All You Need Anymore | 2023 | title-screened |
| 2 | 2310.01082 | Linear attention is (maybe) all you need (to understand transformer optimization) | 2023 | title-screened |
| 3 | 2505.06633 | Attention Is Not All You Need: The Importance of Feedforward Networks in Transformer Models | 2025 | title-screened |

## S70: exploring the limits of transfer learning unified text-to-text transformer

Serves item(s) 1, 2. Purpose: T5: encoder-decoder foundations (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:35+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1910.10683 | Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer | 2019 | title-screened |
| 2 | 2005.10433 | Text-to-Text Pre-Training for Data-to-Text Tasks | 2020 | title-screened |
| 3 | 2305.12567 | Model-Generated Pretraining Signals Improves Zero-Shot Generalization of Text-to-Text Transformers | 2023 | title-screened |

## S71: estimating or propagating gradients through stochastic neurons

Serves item(s) 1, 2. Purpose: Straight-through estimator for discrete choices (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:36+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1308.3432 | Estimating or Propagating Gradients Through Stochastic Neurons for Conditional Computation | 2013 | title-screened |
| 2 | 2509.25536 | Optimal Nuisance Function Tuning for Doubly Robust Functional Estimation under Proportional Asymptotics | 2025 | title-screened |
| 3 | 2308.06689 | Estimator Meets Equilibrium Perspective: A Rectified Straight Through Estimator for Binary Neural Networks Training | 2023 | title-screened |

## S72: training compute-optimal large language models

Serves item(s) 1, 2. Purpose: Chinchilla compute accounting (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:43:37+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2203.15556 | Training Compute-Optimal Large Language Models | 2022 | title-screened |
| 2 | 2304.03208 | Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster | 2023 | title-screened |
| 3 | 2404.19484 | More Compute Is What You Need | 2024 | title-screened |

## S73: a survey on mixture of experts in large language models

Serves item(s) 1, 2. Purpose: MoE survey (explainer) (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:44:00+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2407.06204 | A Survey on Mixture of Experts | 2024 | title-screened |
| 2 | 2508.09834 | Speed Always Wins: A Survey on Efficient Architectures for Large Language Models | 2025 | title-screened |
| 3 | 2509.21164 | Mixture of Thoughts: Learning to Aggregate What Experts Think, Not Just What They Say | 2025 | title-screened |
| 4 | 2603.04445 | Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey | 2026 | title-screened |
| 5 | 2507.23279 | Unveiling Super Experts in Mixture-of-Experts Large Language Models | 2025 | title-screened |
| 6 | 2402.16363 | LLM Inference Unveiled: Survey and Roofline Model Insights | 2024 | title-screened |

## S74: Attention Is All You Need

Serves item(s) 1, 2. Purpose: Transformer paper, keyword mode (explainer extension, 2026-09-24)

Runs: 1 (latest 2026-09-24T11:44:01+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1706.03762 | Attention Is All You Need | 2017 | title-screened |
| 2 | 2407.02328 | Efficient Sparse Attention needs Adaptive Token Release | 2024 | title-screened |
| 3 | 2507.23267 | Your Spending Needs Attention: Modeling Financial Habits with Transformers | 2025 | title-screened |
| 4 | 2411.15236 | Text Embedding is Not All You Need: Attention Control for Text-to-Image Semantic Alignment with Text Self-Attention Maps | 2024 | title-screened |
| 5 | 2507.15807 | True Multimodal In-Context Learning Needs Attention to the Visual Context | 2025 | title-screened |
| 6 | 2507.03916 | Animation Needs Attention: A Holistic Approach to Slides Animation Comprehension with Visual-Language Models | 2025 | title-screened |

## S75: test-time expert re-routing mixture of experts

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:23+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.20395 | R2-T2: Re-Routing in Test-Time for Multimodal Mixture-of-Experts | 2025 | title-screened |
| 2 | 2505.14136 | Local Mixtures of Experts: Essentially Free Test-Time Training via Model Merging | 2025 | title-screened |
| 3 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 4 | 2202.09368 | Mixture-of-Experts with Expert Choice Routing | 2022 | title-screened |
| 5 | 2504.07964 | C3PO: Critical-Layer, Core-Expert, Collaborative Pathway Optimization for Test-Time Expert Re-Mixing | 2025 | title-screened |
| 6 | 2601.03425 | The Illusion of Specialization: Unveiling the Domain-Invariant "Standing Committee" in Mixture-of-Experts Models | 2026 | title-screened |
| 7 | 2306.02628 | Active Ranking of Experts Based on their Performances in Many Tasks | 2023 | title-screened |
| 8 | 2509.22572 | Dynamic Experts Search: Enhancing Reasoning in Mixture-of-Experts LLMs at Test Time | 2025 | title-screened |

## S76: test-time optimization of expert routing weights in MoE language models

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:24+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.20395 | R2-T2: Re-Routing in Test-Time for Multimodal Mixture-of-Experts | 2025 | title-screened |
| 2 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 3 | 2401.13920 | LocMoE: A Low-Overhead MoE for Large Language Model Training | 2024 | title-screened |
| 4 | 2606.01509 | ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts | 2026 | title-screened |
| 5 | 2603.11535 | Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing | 2026 | title-screened |
| 6 | 2204.08396 | StableMoE: Stable Routing Strategy for Mixture of Experts | 2022 | title-screened |
| 7 | 2511.02237 | Opportunistic Expert Activation: Batch-Aware Expert Routing for Faster Decode Without Retraining | 2025 | title-screened |
| 8 | 2406.13233 | AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models | 2024 | title-screened |

## S77: re-route tokens to different experts after verification failure

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:26+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2606.19808 | Think Again or Think Longer? Selective Verification for Budget-Aware Reasoning | 2026 | title-screened |
| 2 | 2609.32821 | Routing Drift Alone Does Not Diagnose Failure in Merged MoE LLMs | 2026 | title-screened |
| 3 | 2604.14246 | Awakening Dormant Experts:Counterfactual Routing to Mitigate MoE Hallucinations | 2026 | title-screened |
| 4 | 2606.12243 | VIA-SD: Verification via Intra-Model Routing for Speculative Decoding | 2026 | title-screened |
| 5 | 2512.10756 | OPV: Outcome-based Process Verifier for Efficient Long Chain-of-Thought Verification | 2025 | title-screened |
| 6 | 2608.30135 | Verification-Aware Training for Speculative Decoding | 2026 | title-screened |
| 7 | 2602.16994 | Dynamic Delayed Tree Expansion For Improved Multi-Path Speculative Decoding | 2026 | title-screened |
| 8 | 2607.20379 | Train the Model, Not the Reader: Decodability Supervision for Verifiable Activation Explanations | 2026 | title-screened |

## S78: feedback-driven expert selection mixture of experts self-correction

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:27+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2608.24794 | CAFE: Self-Improving Search Agents Need Co-Evolving Feedback | 2026 | title-screened |
| 2 | 2506.03332 | Helpful Agent Meets Deceptive Judge: Understanding Vulnerabilities in Agentic Workflows | 2025 | title-screened |
| 3 | 2512.06751 | Becoming Experienced Judges: Selective Test-Time Learning for Evaluators | 2025 | title-screened |
| 4 | 2606.11173 | The Role of Feedback Alignment in Self-Distillation | 2026 | title-screened |
| 5 | 2409.00935 | Self-Judge: Selective Instruction Following with Alignment Self-Evaluation | 2024 | title-screened |
| 6 | 2609.38792 | Training LLM Judges from Language Feedback via Position-Selective Self-Distillation | 2026 | title-screened |
| 7 | 2504.13145 | Exploring Expert Failures Improves LLM Agent Tuning | 2025 | title-screened |
| 8 | 2601.05960 | Distilling Feedback into Memory-as-a-Tool | 2026 | title-screened |

## S79: dynamic number of experts per token confidence based routing

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:28+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2603.11535 | Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing | 2026 | title-screened |
| 2 | 2511.06494 | Route Experts by Sequence, not by Token | 2025 | title-screened |
| 3 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 4 | 2607.28308 | Beyond Geometric Complementarity: Coherent Overlap in Sparse Mixture-of-Experts Routing | 2026 | title-screened |
| 5 | 2604.14419 | Equifinality in Mixture of Experts: Routing Topology Does Not Determine Language Modeling Quality | 2026 | title-screened |
| 6 | 2606.01509 | ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts | 2026 | title-screened |
| 7 | — | Deterministic multi-hash routing supports long-horizon training in a compact language model | 2026 | title-screened |
| 8 | 2602.09001 | DirMoE: Dirichlet-Routed Mixture of Experts | 2026 | title-screened |

## S80: critic guided refinement of latent representation before decoding

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:29+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2606.01243 | Unlocking the Black Box of Latent Reasoning: An Interpretability-Guided Approach to Intervention | 2026 | title-screened |
| 2 | 2607.01774 | Subliminal Clocks: Latent Time Modelling in Diffusion Language Models | 2026 | title-screened |
| 3 | 2604.17362 | FARM: Foundational Aerial Radio Map for Intelligent Low-Altitude Networking | 2026 | title-screened |
| 4 | 2602.14759 | Inner Loop Inference for Pretrained Transformers: Unlocking Latent Capabilities Without Training | 2026 | title-screened |
| 5 | 2310.03686 | DecoderLens: Layerwise Interpretation of Encoder-Decoder Transformers | 2023 | title-screened |
| 6 | 2312.06738 | InstructAny2Pix: Flexible Visual Editing via Multimodal Instruction Following | 2023 | title-screened |
| 7 | 2605.22939 | Learnability-Informed Fine-Tuning of Diffusion Language Models | 2026 | title-screened |
| 8 | 2603.00602 | Learning to Explore: Policy-Guided Outlier Synthesis for Graph Out-of-Distribution Detection | 2026 | title-screened |

## S81: sentence embedding bottleneck decoder machine translation single vector

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:31+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2409.15051 | Scaling Laws of Decoder-Only Models on the Multilingual Machine Translation Task | 2024 | title-screened |
| 2 | 1804.06609 | Fast Lexically Constrained Decoding with Dynamic Beam Allocation for Neural Machine Translation | 2018 | title-screened |
| 3 | 2108.08877 | Sentence-T5: Scalable Sentence Encoders from Pre-trained Text-to-Text Models | 2021 | title-screened |
| 4 | 1911.02150 | Fast Transformer Decoding: One Write-Head is All You Need | 2019 | title-screened |
| 5 | 2008.09396 | Neural Machine Translation without Embeddings | 2020 | title-screened |
| 6 | 2503.06594 | Beyond Decoder-only: Large Language Models Can be Good Encoders for Machine Translation | 2025 | title-screened |
| 7 | 2202.08904 | SGPT: GPT Sentence Embeddings for Semantic Search | 2022 | title-screened |
| 8 | 1803.11175 | Universal Sentence Encoder | 2018 | title-screened |

## S82: quality estimation feedback loop iterative machine translation refinement

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:32+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.14429 | Early-Exit and Instant Confidence Translation Quality Estimation | 2025 | title-screened |
| 2 | 2306.03856 | Iterative Translation Refinement with Large Language Models | 2023 | included |
| 3 | 1610.04841 | Translation Quality Estimation using Recurrent Neural Network | 2016 | title-screened |
| 4 | 2311.09132 | Aligning Neural Machine Translation Models: Human Feedback in Training and Inference | 2023 | title-screened |
| 5 | 2505.24683 | Should I Share this Translation? Evaluating Quality Feedback for User Reliance on Machine Translation |  | title-screened |
| 6 | 2404.18031 | Quality Estimation with k-nearest Neighbors and Automatic Evaluation for Model-specific Quality Estimation | 2024 | title-screened |
| 7 | 2306.01549 | Evaluating Machine Translation Quality with Conformal Predictive Distributions | 2023 | title-screened |
| 8 | 2503.03044 | QE4PE: Word-level Quality Estimation for Human Post-Editing | 2025 | title-screened |

## S83: mixture of experts routing reinforcement learning router policy

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:33+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.17038 | Phase-Aware Mixture of Experts for Agentic Reinforcement Learning | 2026 | excluded (agentic RL MoE, not routing by critique) |
| 2 | 2609.13058 | Expert-Space Exploration in MoE Reinforcement Learning | 2026 | title-screened |
| 3 | 2506.09033 | Router-R1: Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning | 2025 | title-screened |
| 4 | 2510.11370 | Stabilizing MoE Reinforcement Learning by Aligning Training and Inference Routers | 2025 | included |
| 5 | 2510.02850 | Reward Model Routing in Alignment | 2025 | title-screened |
| 6 | 2603.24984 | MoE-GRPO: Optimizing Mixture-of-Experts via Reinforcement Learning in Vision-Language Models | 2026 | title-screened |
| 7 | 2510.08439 | xRouter: Training Cost-Aware LLMs Orchestration System via Reinforcement Learning | 2025 | title-screened |
| 8 | 2602.09001 | DirMoE: Dirichlet-Routed Mixture of Experts | 2026 | title-screened |

## S84: Filipino Tagalog machine translation human evaluation error analysis

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:34+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2508.18549 | COMET-poly: Machine Translation Metric Grounded in Other Candidates | 2025 | title-screened |
| 2 | 2308.07286 | The Devil is in the Errors: Leveraging Large Language Models for Fine-grained Machine Translation Evaluation | 2023 | included |
| 3 | 2310.10482 | xCOMET: Transparent Machine Translation Evaluation through Fine-grained Error Detection | 2023 | included |
| 4 | 2401.01283 | Quality and Quantity of Machine Translation References for Automatic Metrics | 2024 | title-screened |
| 5 | 2401.16313 | Machine Translation Meta Evaluation through Translation Accuracy Challenge Sets | 2024 | title-screened |
| 6 | 2305.19144 | BLEU Meets COMET: Combining Lexical and Neural Metrics Towards Robust Machine Translation Evaluation | 2023 | title-screened |
| 7 | 2609.04173 | Last Translation Benchmark | 2026 | included |
| 8 | 2403.03521 | BiVert: Bidirectional Vocabulary Evaluation using Relations for Machine Translation | 2024 | title-screened |

## S85: mixture of experts routing critique verifier

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:35+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2606.03031 | AUDITFLOW: Executable Symbolic Environments for Structured Financial Reporting Verification | 2026 | title-screened |
| 2 | 2607.24117 | Grading the Narrators: An Isnad-Rijal Framework for Claim-Level Provenance in Multi-Agent Knowledge Systems | 2026 | title-screened |

## S86: latent self-correction before generation hidden state draft

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:36+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2607.01774 | Subliminal Clocks: Latent Time Modelling in Diffusion Language Models | 2026 | title-screened |

## S87: adaptive computation mixture of experts revisit routing decision

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:37+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2604.14419 | Equifinality in Mixture of Experts: Routing Topology Does Not Determine Language Modeling Quality | 2026 | title-screened |
| 2 | 2603.11535 | Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing | 2026 | title-screened |
| 3 | 2604.01622 | Expert-Choice Routing Enables Adaptive Computation in Diffusion Language Models | 2026 | title-screened |
| 4 | 2606.01509 | ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts | 2026 | title-screened |
| 5 | 2604.04230 | Three Phases of Expert Routing: How Load Balance Evolves During Mixture-of-Experts Training | 2026 | title-screened |
| 6 | 2607.28308 | Beyond Geometric Complementarity: Coherent Overlap in Sparse Mixture-of-Experts Routing | 2026 | title-screened |
| 7 | 2602.09001 | DirMoE: Dirichlet-Routed Mixture of Experts | 2026 | title-screened |
| 8 | 2603.18297 | Path-Constrained Mixture-of-Experts | 2026 | title-screened |

## S88: machine translation low-resource Philippine languages

Serves item(s) 1, 3. Purpose: prior-work audit, novelty gap check (2026-10-02)

Runs: 1 (latest 2026-10-02T03:20:38+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2606.11786 | Lius: Translation Model Based Instructional Lingustic Using Continual Instruction Tuning In Kupang Malay | 2026 | title-screened |
| 2 | 2603.25222 | Translation or Recitation? Calibrating Evaluation Scores for Machine Translation of Extremely Low-Resource Languages | 2026 | included |
| 3 | 2604.19778 | Towards High-Quality Machine Translation for Kokborok: A Low-Resource Tibeto-Burman Language of Northeast India | 2026 | title-screened |
| 4 | 2603.25489 | Translation Asymmetry in LLMs as a Data Augmentation Factor: A Case Study for 6 Romansh Language Varieties | 2026 | candidate |

## S89: reuse cached early layer activations recompute later layers transformer

Serves item(s) 1, 4. Purpose: layer-caching idea for repass (2026-10-05): prior work on reusing early-layer computation

Runs: 1 (latest 2026-10-05T06:26:10+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2608.18486 | WhiteMatter: All-to-All Cross-Layer Connections via KV Source Mixing | 2026 | title-screened |
| 2 | 2205.05198 | Reducing Activation Recomputation in Large Transformer Models | 2022 | title-screened |
| 3 | 2505.01855 | Intra-Layer Recurrence in Transformers for Language Modeling | 2025 | title-screened |
| 4 | 2407.09298 | Transformer Layers as Painters | 2024 | title-screened |
| 5 | 2312.12742 | Cached Transformers: Improving Transformers with Differentiable Memory Cache | 2023 | title-screened |
| 6 | 2505.16950 | Bottlenecked Transformers: Periodic KV Cache Consolidation for Generalised Reasoning | 2025 | title-screened |
| 7 | 2405.10637 | Layer-Condensed KV Cache for Efficient Inference of Large Language Models | 2024 | title-screened |
| 8 | 2410.17897 | Value Residual Learning For Alleviating Attention Concentration In Transformers | 2024 | title-screened |

## S90: iterate middle layers recurrent depth encode think decode latent reasoning

Serves item(s) 1, 4. Purpose: layer-caching idea for repass (2026-10-05): prior work on reusing early-layer computation

Runs: 1 (latest 2026-10-05T06:26:12+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2510.07358 | Encode, Think, Decode: Scaling test-time reasoning with recursive latent thoughts | 2025 | included |
| 2 | 2507.02199 | Latent Chain-of-Thought? Decoding the Depth-Recurrent Transformer | 2025 | title-screened |
| 3 | 2601.21582 | Depth-Recurrent Attention Mixtures: Giving Latent Reasoning the Attention it Deserves | 2026 | title-screened |
| 4 | 2602.00449 | Do Latent-CoT Models Think Step-by-Step? A Mechanistic Study on Sequential Reasoning Tasks | 2026 | title-screened |
| 5 | 2510.26745 | Deep sequence models tend to memorize geometrically; it is unclear why | 2025 | title-screened |
| 6 | 2603.21676 | Thinking Deeper, Not Longer: Depth-Recurrent Transformers for Compositional Generalization | 2026 | title-screened |
| 7 | 2606.31779 | Bridging the Gap Between Latent and Explicit Reasoning with Looped Transformers | 2026 | title-screened |
| 8 | 2604.07822 | Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers | 2026 | title-screened |

## S91: KV cache sharing across recursion steps recursive transformer

Serves item(s) 1, 4. Purpose: layer-caching idea for repass (2026-10-05): prior work on reusing early-layer computation

Runs: 1 (latest 2026-10-05T06:26:13+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2507.10524 | Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation | 2025 | title-screened |
| 2 | 2512.03870 | Reconstructing KV Caches with Cross-Layer Fusion for Enhanced Transformers | 2025 | title-screened |
| 3 | 2406.09297 | MLKV: Multi-Layer Key-Value Heads for Memory Efficient Transformer Decoding | 2024 | title-screened |
| 4 | 2603.19664 | The Residual Stream Is All You Need: On the Redundancy of the KV Cache in Transformer Inference | 2026 | title-screened |
| 5 | 2601.19178 | CollectiveKV: Decoupling and Sharing Collaborative Information in Sequential Recommendation | 2026 | title-screened |
| 6 | 2608.01247 | RestoreKV: Recovering Full-Cache Behavior Under Aggressive Query-Agnostic KV Cache Eviction | 2026 | title-screened |
| 7 | — | EVOKE: Reversible KV-Cache Eviction as Agent Working Memory | 2026 | title-screened |
| 8 | 2511.01815 | KV Cache Transform Coding for Compact Storage in LLM Inference | 2025 | title-screened |

## S92: prefix caching LLM serving reuse KV cache shared prefix

Serves item(s) 1, 4. Purpose: layer-caching idea for repass (2026-10-05): prior work on reusing early-layer computation

Runs: 1 (latest 2026-10-05T06:26:14+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2503.16525 | KVShare: An LLM Service System with Efficient and Effective Multi-Tenant KV Cache Reuse | 2025 | title-screened |
| 2 | 2507.07400 | KVFlow: Efficient Prefix Caching for Accelerating LLM-based Multi-Agent Workflows | 2025 | title-screened |
| 3 | 2601.18999 | Randomization Boosts KV Caching, Learning Balances Query Load: A Joint Perspective | 2026 | title-screened |
| 4 | 2511.01815 | KV Cache Transform Coding for Compact Storage in LLM Inference | 2025 | title-screened |
| 5 | 2510.09665 | LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference | 2025 | title-screened |
| 6 | 2603.13281 | ICaRus: Identical Cache Reuse for Efficient Multi-Model Inference | 2026 | title-screened |
| 7 | 2604.13226 | KV Packet: Recomputation-Free Context-Independent KV Caching for LLMs | 2026 | title-screened |
| 8 | 2602.06502 | DualMap: Enabling Both Cache Affinity and Load Balancing for Distributed LLM Serving | 2026 | title-screened |

## S93: inject feedback at intermediate layer transformer self-correction hidden states

Serves item(s) 1, 4. Purpose: layer-caching idea for repass (2026-10-05): prior work on reusing early-layer computation

Runs: 1 (latest 2026-10-05T06:26:15+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2303.09435 | Jump to Conclusions: Short-Cutting Transformers With Linear Transformations | 2023 | title-screened |
| 2 | 2602.14759 | Inner Loop Inference for Pretrained Transformers: Unlocking Latent Capabilities Without Training | 2026 | title-screened |
| 3 | 2412.05768 | Uncovering Uncertainty in Transformer Inference | 2024 | title-screened |
| 4 | 2002.09402 | Addressing Some Limitations of Transformers with Feedback Memory | 2020 | title-screened |
| 5 | 2406.09519 | Talking Heads: Understanding Inter-layer Communication in Transformer Language Models | 2024 | title-screened |
| 6 | 2302.00456 | Analyzing Feed-Forward Blocks in Transformers through the Lens of Attention Maps | 2023 | title-screened |
| 7 | 2203.14680 | Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space | 2022 | title-screened |
| 8 | 2408.15138 | How transformers learn structured data: insights from hierarchical filtering | 2024 | title-screened |

## S94: partial recomputation iterative refinement neural machine translation reuse encoder states

Serves item(s) 1, 4. Purpose: layer-caching idea for repass (2026-10-05): prior work on reusing early-layer computation

Runs: 1 (latest 2026-10-05T06:26:16+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1406.1078 | Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation | 2014 | title-screened |
| 2 | 1807.05353 | Recurrent Stacking of Layers for Compact Neural Machine Translation Models | 2018 | title-screened |
| 3 | 2510.07739 | MeSH: Memory-as-State-Highways for Recursive Transformers | 2025 | title-screened |
| 4 | 2410.11135 | Mimetic Initialization Helps State Space Models Learn to Recall | 2024 | title-screened |
| 5 | 2308.03421 | RecycleGPT: An Autoregressive Language Model with Recyclable Module | 2023 | title-screened |
| 6 | 2509.22630 | StateX: Enhancing RNN Recall via Post-training State Expansion | 2025 | title-screened |
| 7 | — | Vector Position States: Content-Conditioned Structural Addressing for Transformers | 2026 | title-screened |
| 8 | 1409.1259 | On the Properties of Neural Machine Translation: Encoder-Decoder Approaches | 2014 | title-screened |

## S95: layer reuse adaptive depth looping pretrained transformer inference

Serves item(s) 1, 4. Purpose: layer-caching idea for repass (2026-10-05): prior work on reusing early-layer computation

Runs: 1 (latest 2026-10-05T06:26:17+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.14759 | Inner Loop Inference for Pretrained Transformers: Unlocking Latent Capabilities Without Training | 2026 | title-screened |
| 2 | 2607.13491 | DeepLoop: Depth Scaling for Looped Transformers | 2026 | title-screened |
| 3 | 2511.18105 | AdaPerceiver: Transformers with Adaptive Width, Depth, and Tokens | 2025 | title-screened |
| 4 | 2610.02185 | Decoding Looped Transformers Better for (Almost) Free | 2026 | title-screened |
| 5 | 2605.23872 | Training-Free Looped Transformers | 2026 | title-screened |
| 6 | 2608.09444 | Depth-adaptive Inference of Looped Language Models via Continuous Depth Batching | 2026 | title-screened |
| 7 | 2507.07996 | Skip a Layer or Loop it? Test-Time Depth Adaptation of Pretrained LLMs | 2025 | title-screened |
| 8 | 2604.19254 | ShadowPEFT: Shadow Network for Parameter-Efficient Fine-Tuning | 2026 | title-screened |

## S96: compute penalty reward adaptive computation policy cost sensitivity

Serves item(s) 1, 4. Purpose: lambda coupling under layer caching (2026-10-05): compute cost terms biasing policies

Runs: 1 (latest 2026-10-05T06:28:16+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2305.15193 | Adaptive Policy Learning to Additional Tasks | 2023 | title-screened |
| 2 | 2606.21795 | Discretizing Reward Models | 2026 | title-screened |
| 3 | 2502.02516 | Adaptive Exploration for Multi-Reward Multi-Policy Evaluation | 2025 | title-screened |
| 4 | 2302.01399 | Accelerating Policy Gradient by Estimating Value Function from Prior Computation in Deep Reinforcement Learning | 2023 | title-screened |
| 5 | 2502.07764 | Polynomial-Time Approximability of Constrained Reinforcement Learning | 2025 | title-screened |
| 6 | 2301.13087 | Improved Regret for Efficient Online Reinforcement Learning with Linear Function Approximation | 2023 | title-screened |
| 7 | 2602.05999 | On the Role of Computation in Reinforcement Learning | 2026 | title-screened |
| 8 | 2406.01423 | Value Improved Actor Critic Algorithms | 2024 | title-screened |

## S97: cost-aware routing reinforcement learning cost penalty trade-off quality

Serves item(s) 1, 4. Purpose: lambda coupling under layer caching (2026-10-05): compute cost terms biasing policies

Runs: 1 (latest 2026-10-05T06:28:17+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2510.08439 | xRouter: Training Cost-Aware LLMs Orchestration System via Reinforcement Learning | 2025 | title-screened |
| 2 | 2603.23889 | Off-Policy Safe Reinforcement Learning with Cost-Constrained Optimistic Exploration | 2026 | title-screened |
| 3 | 2505.16037 | Causal LLM Routing: End-to-End Regret Minimization from Observational Data | 2025 | title-screened |
| 4 | 2406.18665 | RouteLLM: Learning to Route LLMs with Preference Data | 2024 | title-screened |
| 5 | 2508.12491 | Cost-Aware Contrastive Routing for LLMs | 2025 | title-screened |
| 6 | 2502.03261 | CARROT: A Cost Aware Rate Optimal Router | 2025 | title-screened |
| 7 | 2602.21227 | Budget-Aware Agentic Routing via Boundary-Guided Training | 2026 | title-screened |
| 8 | 2605.11975 | Stochastic Minimum-Cost Reach-Avoid Reinforcement Learning | 2026 | title-screened |

## S98: compare adaptive computation methods at matched compute quality compute trade-off curve

Serves item(s) 3, 4. Purpose: matched-compute comparison of the MetricX-24 and chrF++ routers along lambda sweeps (2026-10-05)

Runs: 1 (latest 2026-10-05T07:15:06+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.01070 | What If We Allocate Test-Time Compute Adaptively? | 2026 | title-screened |
| 2 | 2603.22339 | Problems with Chinchilla Approach 2: Systematic Biases in IsoFLOP Parabola Fits | 2026 | title-screened |
| 3 | 2311.03233 | Navigating Scaling Laws: Compute Optimality in Adaptive Model Training | 2023 | title-screened |
| 4 | 2506.12721 | Strategic Scaling of Test-Time Compute: A Bandit Learning Approach | 2025 | title-screened |
| 5 | 2107.05407 | PonderNet: Learning to Ponder | 2021 | title-screened |
| 6 | 2312.10193 | Adaptive Computation Modules: Granular Conditional Computation For Efficient Inference | 2023 | excluded (screened 2026-10-07 (S103): per-token learner gating under user budgets; no per-action cost heterogeneity or RL cost penalty, not cited) |
| 7 | 2507.02076 | Reasoning on a Budget: A Survey of Adaptive and Controllable Test-Time Compute in LLMs | 2025 | title-screened |
| 8 | 2605.17234 | Active Budget Allocation for Efficient Scaling Law Estimation via Surrogate-Guided Pruning | 2026 | title-screened |

## S99: reward scale sensitivity penalty coefficient different reward metrics reinforcement learning comparison

Serves item(s) 3, 4. Purpose: matched-compute comparison of the MetricX-24 and chrF++ routers along lambda sweeps (2026-10-05)

Runs: 1 (latest 2026-10-05T07:15:06+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2606.21795 | Discretizing Reward Models | 2026 | title-screened |
| 2 | 2410.11348 | RATE: Causal Explainability of Reward Models with Imperfect Counterfactuals | 2024 | title-screened |
| 3 | 2602.18037 | Gradient Regularization Mitigates Reward Hacking in Reinforcement Learning from Human Feedback and Verifiable Rewards | 2026 | title-screened |
| 4 | 2403.03185 | Correlated Proxies: A New Definition and Improved Mitigation for Reward Hacking | 2024 | title-screened |
| 5 | 2210.10760 | Scaling Laws for Reward Model Overoptimization | 2022 | title-screened |
| 6 | 2610.00574 | Make Sparse Rewards Count: Density-Aware Reward Aggregation for Multi-Reward RL | 2026 | title-screened |
| 7 | 2604.10062 | When Can You Poison Rewards? A Tight Characterization of Reward Poisoning in Linear MDPs | 2026 | title-screened |
| 8 | 2510.08977 | Breaking the Self-Confirming Loop: Diagnosing and Mitigating Systemic Reward Bias in Self-Rewarding RL | 2025 | title-screened |

## S100: compute-matched evaluation test-time compute Pareto frontier comparison methods

Serves item(s) 3, 4. Purpose: matched-compute comparison of the MetricX-24 and chrF++ routers along lambda sweeps (2026-10-05)

Runs: 1 (latest 2026-10-05T07:15:08+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2512.04558 | On the Limits of Test-Time Compute: Sequential Reward Filtering for Better Inference | 2025 | title-screened |
| 2 | 2605.07248 | PaT: Planning-after-Trial for Efficient Test-Time Code Generation | 2026 | title-screened |
| 3 | 2602.01070 | What If We Allocate Test-Time Compute Adaptively? | 2026 | title-screened |
| 4 | 2503.19877 | Scaling Evaluation-time Compute with Reasoning Models as Process Evaluators | 2025 | title-screened |
| 5 | 2406.07529 | MAP: Low-compute Model Merging with Amortized Pareto Fronts via Quadratic Approximation | 2024 | title-screened |
| 6 | 2602.07670 | Surprisal-Guided Selection: Compute-Optimal Test-Time Strategies for Execution-Grounded Code Generation | 2026 | title-screened |
| 7 | 2507.05195 | Train-before-Test Harmonizes Language Model Rankings | 2025 | title-screened |
| 8 | 2501.02497 | Test-time Computing: from System-1 Thinking to System-2 Thinking | 2025 | title-screened |

## S101: calibrate threshold on held-out calibration set to target compute budget adaptive computation

Serves item(s) 3, 4. Purpose: D14 amendment: choosing lambda on a pilot to hit target compute levels (2026-10-07)

Runs: 1 (latest 2026-10-07T09:32:33+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2605.17234 | Active Budget Allocation for Efficient Scaling Law Estimation via Surrogate-Guided Pruning | 2026 | title-screened |
| 2 | 2606.21749 | Quantile‑Adaptive Temperature Scaling for Confidence Calibration |  | title-screened |
| 3 | 2609.01072 | Let Confidence Change, Not the Prediction: Prediction-Preserving Repair for Post-hoc Calibration | 2026 | title-screened |
| 4 | 2508.21495 | Rethinking Calibration for Early-Exit Neural Networks | 2025 | title-screened |
| 5 | 2306.14343 | TCE: A Test-Based Approach to Measuring Calibration Error | 2023 | title-screened |
| 6 | 2603.22339 | Problems with Chinchilla Approach 2: Systematic Biases in IsoFLOP Parabola Fits | 2026 | title-screened |
| 7 | — | Rethinking Detection Calibration: A Coordinate Perspective |  | title-screened |
| 8 | 2506.23492 | Sample Margin-Aware Recalibration of Temperature Scaling | 2025 | title-screened |

## S102: tune cost penalty to meet target compute budget reinforcement learning router

Serves item(s) 3, 4. Purpose: D14 amendment: choosing lambda on a pilot to hit target compute levels (2026-10-07)

Runs: 1 (latest 2026-10-07T09:32:33+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2207.07790 | BCRLSP: An Offline Reinforcement Learning Framework for Sequential Targeted Promotion | 2022 | title-screened |
| 2 | 2505.20583 | Balancing Performance and Costs in Best Arm Identification | 2025 | title-screened |
| 3 | 2510.08439 | xRouter: Training Cost-Aware LLMs Orchestration System via Reinforcement Learning | 2025 | title-screened |
| 4 | 2602.05999 | On the Role of Computation in Reinforcement Learning | 2026 | title-screened |
| 5 | 2306.00603 | Safe Offline Reinforcement Learning with Real-Time Budget Constraints | 2023 | title-screened |
| 6 | 2506.05256 | Just Enough Thinking: Efficient Reasoning with Adaptive Length Penalties Reinforcement Learning | 2025 | title-screened |
| 7 | 2602.03814 | Conformal Thinking: Risk Control for Reasoning on a Compute Budget | 2026 | title-screened |
| 8 | 2302.03201 | Near-Minimax-Optimal Risk-Sensitive Reinforcement Learning with CVaR | 2023 | title-screened |

## S103: separate compute penalty per stage heterogeneous action cost adaptive computation reinforcement learning

Serves item(s) 3, 4. Purpose: D14 units amendment: per-stage compute penalty when actions differ ~50x in FLOP cost (2026-10-07)

Runs: 1 (latest 2026-10-07T09:38:31+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.05999 | On the Role of Computation in Reinforcement Learning | 2026 | title-screened |
| 2 | 2512.01457 | Zero-Overhead Introspection for Adaptive Test-Time Compute | 2025 | title-screened |
| 3 | 2505.12611 | Action-Dependent Optimality-Preserving Reward Shaping | 2025 | title-screened |
| 4 | 2502.04327 | Value-Based Deep RL Scales Predictably | 2025 | title-screened |
| 5 | 2406.01423 | Value Improved Actor Critic Algorithms | 2024 | title-screened |
| 6 | 2301.12083 | Beyond Exponentially Fast Mixing in Average-Reward Reinforcement Learning via Multi-Level Monte Carlo Actor-Critic | 2023 | title-screened |
| 7 | 2312.10193 | Adaptive Computation Modules: Granular Conditional Computation For Efficient Inference | 2023 | excluded (screened 2026-10-07 (S103): per-token learner gating under user budgets; no per-action cost heterogeneity or RL cost penalty, not cited) |
| 8 | 2602.08864 | Understanding Dynamic Compute Allocation in Recurrent Transformers | 2026 | excluded (screened 2026-10-07 (S103): token-level halting analysis; no per-stage cost penalty, not cited) |

## S104: per-step cost penalty multi-stage cascade early exit reinforcement learning budget constraint lagrangian

Serves item(s) 3, 4. Purpose: D14 units amendment: per-stage compute penalty when actions differ ~50x in FLOP cost (2026-10-07)

Runs: 1 (latest 2026-10-07T09:38:32+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | — | POCE: Primal Policy Optimization with Conservative Estimation for Multi-constraint Offline Reinforcement Learning |  | title-screened |
| 2 | 2506.16016 | Dual-Objective Reinforcement Learning with Novel Hamilton-Jacobi-Bellman Formulations | 2025 | title-screened |
| 3 | 2301.13087 | Improved Regret for Efficient Online Reinforcement Learning with Linear Function Approximation | 2023 | title-screened |
| 4 | 2303.02135 | Eventual Discounting Temporal Logic Counterfactual Experience Replay | 2023 | title-screened |
| 5 | 2504.12557 | TraCeS: Learning Per-Timestep Constraint-Violation Credit from Sparse Trajectory-Level Labels | 2025 | title-screened |
| 6 | 2506.13672 | The Courage to Stop: Overcoming Sunk Cost Fallacy in Deep Reinforcement Learning | 2025 | title-screened |
| 7 | 2605.11975 | Stochastic Minimum-Cost Reach-Avoid Reinforcement Learning | 2026 | title-screened |
| 8 | 2603.03480 | Minimax Optimal Strategy for Delayed Observations in Online Reinforcement Learning | 2026 | title-screened |

## S105: ponder cost halting policy collapse always halt never halt adaptive computation time

Serves item(s) 3, 4. Purpose: D14 units amendment: per-stage compute penalty when actions differ ~50x in FLOP cost (2026-10-07)

Runs: 1 (latest 2026-10-07T09:38:33+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2506.13672 | The Courage to Stop: Overcoming Sunk Cost Fallacy in Deep Reinforcement Learning | 2025 | title-screened |
| 2 | 2510.10103 | Stop When Enough: Adaptive Early-Stopping for Chain-of-Thought Reasoning | 2025 | title-screened |
| 3 | 2306.00338 | Last Switch Dependent Bandits with Monotone Payoff Functions | 2023 | title-screened |
| 4 | 2605.29860 | ESPO: Early-Stopping Proximal Policy Optimization | 2026 | title-screened |
| 5 | 2509.13637 | Delta Matters: An Analytically Tractable Model for beta–delta Discounting Agents | 2025 | title-screened |
| 6 | 2303.02135 | Eventual Discounting Temporal Logic Counterfactual Experience Replay | 2023 | title-screened |
| 7 | 2301.02389 | Provable Reset-free Reinforcement Learning by No-Regret Reduction | 2023 | title-screened |
| 8 | 2507.12453 | Cost-aware Stopping for Bayesian Optimization | 2025 | title-screened |

## S106: random halting baseline matched compute rate adaptive computation learned policy versus random

Serves item(s) 3, 4. Purpose: D14 per-stage: replacement test when lambda is tuned to a fixed redo rate (random-at-matched-rate and fixed-iteration baselines) (2026-10-07)

Runs: 1 (latest 2026-10-07T09:42:43+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2305.15193 | Adaptive Policy Learning to Additional Tasks | 2023 | title-screened |
| 2 | 1803.07055 | Simple random search provides a competitive approach to reinforcement learning | 2018 | title-screened |
| 3 | 2406.11810 | Computationally Efficient RL under Linear Bellman Completeness for Deterministic Dynamics | 2024 | title-screened |
| 4 | 2602.05999 | On the Role of Computation in Reinforcement Learning | 2026 | title-screened |
| 5 | 2006.06294 | Adaptive Reward-Free Exploration | 2020 | title-screened |
| 6 | 2402.14528 | ACE : Off-Policy Actor-Critic with Causality-Aware Entropy Regularization | 2024 | title-screened |
| 7 | 2111.00765 | Validate on Sim, Detect on Real -- Model Selection for Domain Randomization | 2021 | title-screened |
| 8 | 2411.15370 | Deep Policy Gradient Methods Without Batch Updates, Target Networks, or Replay Buffers | 2024 | title-screened |

## S107: learned refinement decision versus fixed number of refinement iterations matched rate baseline translation

Serves item(s) 3, 4. Purpose: D14 per-stage: replacement test when lambda is tuned to a fixed redo rate (random-at-matched-rate and fixed-iteration baselines) (2026-10-07)

Runs: 1 (latest 2026-10-07T09:42:43+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2605.13368 | What Does LLM Refinement Actually Improve? A Systematic Study on Document-Level Literary Translation | 2026 | candidate |
| 2 | 2306.03856 | Iterative Translation Refinement with Large Language Models | 2023 | included |
| 3 | 2511.22173 | RefineBench: Evaluating Refinement Capability of Language Models via Checklists | 2025 | title-screened |
| 4 | 2502.12701 | Translate Smart, not Hard: Cascaded Translation Systems with Quality-Aware Deferral |  | candidate |
| 5 | 2402.10963 | GLoRe: When, Where, and How to Improve LLM Reasoning via Global and Local Refinements | 2024 | title-screened |
| 6 | 2401.01283 | Quality and Quantity of Machine Translation References for Automatic Metrics | 2024 | title-screened |
| 7 | 2602.08948 | CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute | 2026 | excluded (screened 2026-10-07 (S107): confidence-guided refinement controller for LLM reasoning; no matched-rate random baseline found in abstract) |
| 8 | 2004.03672 | Dynamic Data Selection and Weighting for Iterative Back-Translation | 2020 | candidate |

## S108: budget-constrained policy fixed action rate Lagrangian degenerate policy evaluation random baseline same rate

Serves item(s) 3, 4. Purpose: D14 per-stage: replacement test when lambda is tuned to a fixed redo rate (random-at-matched-rate and fixed-iteration baselines) (2026-10-07)

Runs: 1 (latest 2026-10-07T09:42:44+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.07764 | Polynomial-Time Approximability of Constrained Reinforcement Learning | 2025 | title-screened |
| 2 | 2506.16016 | Dual-Objective Reinforcement Learning with Novel Hamilton-Jacobi-Bellman Formulations | 2025 | title-screened |
| 3 | 2108.06655 | Policy Evaluation and Temporal-Difference Learning in Continuous Time and Space: A Martingale Approach | 2021 | title-screened |
| 4 | 2505.12049 | Beyond Scalar Rewards: An Axiomatic Framework for Lexicographic MDPs | 2025 | title-screened |
| 5 | 2505.19238 | Efficient Policy Optimization in Robust Constrained MDPs with Iteration Complexity Guarantees | 2025 | title-screened |
| 6 | 2605.18591 | Randomized Advantage Transformation (RAT): Computing Natural Policy Gradients via Direct Backpropagation | 2026 | title-screened |
| 7 | 2505.21391 | Finite Sample Analysis of Linear Temporal Difference Learning with Arbitrary Features | 2025 | title-screened |
| 8 | 2106.06170 | Taylor Expansion of Discount Factors | 2021 | title-screened |

## S109: adaptive computation compared with fixed depth at the same average number of steps

Serves item(s) 3, 4. Purpose: D14 per-stage: matching the fixed-redo baseline (B4) to a non-integer average redo rate (2026-10-07)

Runs: 1 (latest 2026-10-07T09:45:19+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2107.05407 | PonderNet: Learning to Ponder | 2021 | title-screened |
| 2 | 2312.10193 | Adaptive Computation Modules: Granular Conditional Computation For Efficient Inference | 2023 | excluded (screened 2026-10-07 (S103): per-token learner gating under user budgets; no per-action cost heterogeneity or RL cost penalty, not cited) |
| 3 | 2311.03233 | Navigating Scaling Laws: Compute Optimality in Adaptive Model Training | 2023 | title-screened |
| 4 | 2607.20519 | Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts | 2026 | included |
| 5 | 1603.08983 | Adaptive Computation Time for Recurrent Neural Networks | 2016 | included |
| 6 | 1910.10073 | Depth-Adaptive Transformer | 2019 | excluded (title-screened 2026-10-07 (S109): depth-adaptive MT decoder (2019); abstract not read; popescu2026adaptive already covers the fixed-depth comparison) |
| 7 | 2511.04981 | Scaling depth capacity via zero/one-layer model expansion | 2025 | title-screened |
| 8 | 2602.16490 | From Growing to Looping: A Unified View of Iterative Computation in LLMs | 2026 | title-screened |

## S110: adaptive halting versus static fixed iterations matched average compute interpolation baseline

Serves item(s) 3, 4. Purpose: D14 per-stage: matching the fixed-redo baseline (B4) to a non-integer average redo rate (2026-10-07)

Runs: 1 (latest 2026-10-07T09:45:19+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.03787 | Iterate to Accelerate: A Unified Framework for Iterative Reasoning and Feedback Convergence | 2025 | title-screened |
| 2 | 2501.18962 | Spend Wisely: Maximizing Post-Training Gains in Iterative Synthetic Data Bootstrapping | 2025 | title-screened |
| 3 | 2602.01476 | Conformal Prediction for Early Stopping in Mixed Integer Optimization | 2026 | title-screened |
| 4 | 2505.24452 | Stepsize anything: A unified learning rate schedule for budgeted-iteration training | 2025 | title-screened |
| 5 | 2506.03464 | From Average-Iterate to Last-Iterate Convergence in Games: A Reduction and Its Applications | 2025 | title-screened |
| 6 | 2310.07831 | Optimal Linear Decay Learning Rate Schedules and Further Refinements | 2023 | title-screened |
| 7 | 2504.11997 | A Computationally Efficient Algorithm for Infinite-Horizon Average-Reward Linear MDPs | 2025 | title-screened |
| 8 | 2408.13150 | Adaptive backtracking for faster optimization | 2024 | title-screened |

## S111: statistical power sample size human evaluation machine translation system comparison

Serves item(s) 3, 4. Purpose: D14 per-stage tests: statistical power / sample size for human-label comparisons (2026-10-07)

Runs: 1 (latest 2026-10-07T09:49:38+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2204.06546 | Disentangling Uncertainty in Machine Translation Evaluation | 2022 | title-screened |
| 2 | 2209.07351 | Rethinking Round-Trip Translation for Machine Translation Evaluation | 2022 | candidate |
| 3 | 2401.06568 | Lost in the Source Language: How Large Language Models Evaluate the Quality of Machine Translation | 2024 | title-screened |
| 4 | 2510.20780 | Are Large Reasoning Models Good Translation Evaluators? Analysis and Performance Boost | 2025 | title-screened |
| 5 | 2401.01283 | Quality and Quantity of Machine Translation References for Automatic Metrics | 2024 | title-screened |
| 6 | 2502.14429 | Early-Exit and Instant Confidence Translation Quality Estimation | 2025 | title-screened |
| 7 | 2109.06352 | Uncertainty-Aware Machine Translation Evaluation | 2021 | title-screened |
| 8 | 2509.19020 | Investigating Test-Time Scaling with Reranking for Machine Translation | 2025 | title-screened |

## S112: underpowered NLP experiments statistical power analysis minimum detectable effect

Serves item(s) 3, 4. Purpose: D14 per-stage tests: statistical power / sample size for human-label comparisons (2026-10-07)

Runs: 1 (latest 2026-10-07T09:49:39+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2010.06595 | With Little Power Comes Great Responsibility | 2020 | title-screened |
| 2 | 2406.13122 | Testing for Underpowered Literatures | 2025 | title-screened |
| 3 | 2205.11134 | Please, Don't Forget the Difference and the Confidence Interval when Seeking for the State-of-the-Art Status | 2022 | title-screened |
| 4 | 2603.12997 | Deconstructing the Failure of Ideal Noise Correction: A Three-Pillar Diagnosis | 2026 | title-screened |
| 5 | 2004.13705 | Showing Your Work Doesn't Always Work | 2020 | title-screened |
| 6 | 2103.11795 | Simpson's Bias in NLP Training | 2021 | title-screened |
| 7 | 2005.04118 | Beyond Accuracy: Behavioral Testing of NLP models with CheckList | 2020 | title-screened |
| 8 | 2406.12150 | ChaosMining: A Benchmark to Evaluate Post-Hoc Local Attribution Methods in Low SNR Environments | 2024 | excluded (screened 2026-10-07 (data survey), S126: attribution benchmark, off-topic) |

## S113: random baseline matched compute stratified by input length adaptive computation sentence length cost

Serves item(s) 3, 4. Purpose: D14 stage-1 B5: matching a random baseline in FLOPs when redo cost scales with sentence length (2026-10-07)

Runs: 1 (latest 2026-10-07T09:52:51+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2410.04707 | Learning How Hard to Think: Input-Adaptive Allocation of LM Computation | 2024 | title-screened |
| 2 | 2606.07726 | Cutting LLM Evaluation Costs with SySRs: A Bandit Algorithm That Provably Exploits Model Similarity | 2026 | title-screened |
| 3 | 2605.10875 | Compute Where it Counts: Self Optimizing Language Models | 2026 | title-screened |
| 4 | 2603.22339 | Problems with Chinchilla Approach 2: Systematic Biases in IsoFLOP Parabola Fits | 2026 | title-screened |
| 5 | 2305.10713 | Flatness-Aware Prompt Selection Improves Accuracy and Sample Efficiency | 2023 | title-screened |
| 6 | 2606.23670 | Tapered Language Models | 2026 | title-screened |
| 7 | 2506.15553 | Approximating Language Model Training Data from Weights | 2025 | title-screened |
| 8 | 2407.06172 | On Speeding Up Language Model Evaluation | 2024 | title-screened |

## S114: FLOPs-matched comparison input length dependent compute early exit translation length bias

Serves item(s) 3, 4. Purpose: D14 stage-1 B5: matching a random baseline in FLOPs when redo cost scales with sentence length (2026-10-07)

Runs: 1 (latest 2026-10-07T09:52:52+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2604.21106 | How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models | 2026 | title-screened |
| 2 | 2311.15436 | Learning to Skip for Language Modeling | 2023 | title-screened |
| 3 | 2601.08490 | BenchOverflow: Measuring Overflow in Large Language Models via Plain-Text Prompts | 2026 | title-screened |
| 4 | 2511.21086 | Orthographic Constraint Satisfaction and Human Difficulty Alignment in Large Language Models | 2025 | title-screened |
| 5 | 2606.23670 | Tapered Language Models | 2026 | title-screened |
| 6 | 2404.06954 | Accelerating Inference in Large Language Models with a Unified Layer Skipping Strategy | 2024 | title-screened |
| 7 | 2404.02258 | Mixture-of-Depths: Dynamically allocating compute in transformer-based language models | 2024 | title-screened |
| 8 | 2603.14785 | SkipOPU: An FPGA-based Overlay Processor for Large Language Models with Dynamically Allocated Computation | 2026 | title-screened |

## S115: average FLOPs per token versus per example compute accounting adaptive computation variable length inputs

Serves item(s) 3, 4. Purpose: D14 compute unit: ratio of sums vs mean of per-example ratios for average compute (2026-10-07)

Runs: 1 (latest 2026-10-07T09:54:36+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2404.02258 | Mixture-of-Depths: Dynamically allocating compute in transformer-based language models | 2024 | title-screened |
| 2 | 2601.23278 | FOCUS: DLLMs Know How to Tame Their Compute Bound | 2026 | title-screened |
| 3 | 2512.10656 | Token Sample Complexity of Attention | 2025 | title-screened |
| 4 | 2603.14785 | SkipOPU: An FPGA-based Overlay Processor for Large Language Models with Dynamically Allocated Computation | 2026 | title-screened |
| 5 | 2312.10193 | Adaptive Computation Modules: Granular Conditional Computation For Efficient Inference | 2023 | excluded (screened 2026-10-07 (S103): per-token learner gating under user budgets; no per-action cost heterogeneity or RL cost penalty, not cited) |
| 6 | 2504.06949 | Adaptive Computation Pruning for the Forgetting Transformer | 2025 | title-screened |
| 7 | 2402.17227 | Efficient Backpropagation with Variance-Controlled Adaptive Sampling | 2024 | title-screened |
| 8 | 2506.01084 | zip2zip: Inference-Time Adaptive Vocabularies for Language Models via Token Compression | 2025 | title-screened |

## S116: ratio of sums versus mean of ratios efficiency metric aggregation bias

Serves item(s) 3, 4. Purpose: D14 compute unit: ratio of sums vs mean of per-example ratios for average compute (2026-10-07)

Runs: 1 (latest 2026-10-07T09:54:37+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2304.08859 | Unveiling and unraveling aggregation and dispersion fallacies in group MCDM | 2023 | title-screened |
| 2 | 1702.05222 | Direct Estimation of Information Divergence Using Nearest Neighbor Ratios | 2017 | title-screened |
| 3 | 2509.25671 | The Flaw of Averages: Quantifying Uniformity of Performance on Benchmarks | 2025 | title-screened |
| 4 | 2605.08485 | Sinkhorn Treatment Effects: A Causal Optimal Transport Measure | 2026 | title-screened |
| 5 | 2506.09627 | Benchmarking Debiasing Methods for LLM-based Parameter Estimates | 2025 | title-screened |
| 6 | 2603.11907 | Causal Representation Learning with Optimal Compression and Complex Treatments | 2026 | title-screened |
| 7 | 2305.13715 | Covariate balancing using the integral probability metric for causal inference | 2023 | title-screened |
| 8 | 2509.23074 | Beyond Model Ranking: Predictability-Aligned Evaluation for Time Series Forecasting | 2025 | title-screened |

## S117: tokenizer length disparity across languages unfairness token premium

Serves item(s) 3, 4. Purpose: D14 per-language compute matching: tokenizer length disparity across languages (2026-10-07)

Runs: 1 (latest 2026-10-07T09:59:08+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2510.21909 | Explaining and Mitigating Crosslingual Tokenizer Inequities | 2025 | candidate |
| 2 | 2305.15425 | Language Model Tokenizers Introduce Unfairness Between Languages | 2023 | included |
| 3 | 2508.04796 | Parity-Aware Byte-Pair Encoding: Improving Cross-lingual Fairness in Tokenization | 2025 | title-screened |
| 4 | 2305.13707 | Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models | 2023 | candidate |
| 5 | 2601.11518 | How Long Is a Piece of String? A Brief Empirical Analysis of Tokenizers | 2026 | title-screened |
| 6 | 2410.11985 | The Fair Language Model Paradox | 2024 | title-screened |
| 7 | 2502.15343 | Tokenization is Sensitive to Language Variation | 2025 | title-screened |
| 8 | 2406.16829 | Understanding and Mitigating Tokenization Bias in Language Models | 2024 | title-screened |

## S118: tokenization parity multilingual number of tokens per sentence differs by language cost

Serves item(s) 3, 4. Purpose: D14 per-language compute matching: tokenizer length disparity across languages (2026-10-07)

Runs: 1 (latest 2026-10-07T09:59:09+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2510.21909 | Explaining and Mitigating Crosslingual Tokenizer Inequities | 2025 | candidate |
| 2 | 2305.15425 | Language Model Tokenizers Introduce Unfairness Between Languages | 2023 | included |
| 3 | 2305.17179 | Tokenization Impacts Multilingual Language Modeling: Assessing Vocabulary Allocation and Overlap Across Languages | 2023 | title-screened |
| 4 | 2508.04796 | Parity-Aware Byte-Pair Encoding: Improving Cross-lingual Fairness in Tokenization | 2025 | title-screened |
| 5 | 2402.18376 | Tokenization Is More Than Compression | 2024 | title-screened |
| 6 | 2601.11518 | How Long Is a Piece of String? A Brief Empirical Analysis of Tokenizers | 2026 | title-screened |
| 7 | 2403.13754 | Different Tokenization Schemes Lead to Comparable Performance in Spanish Number Agreement | 2024 | title-screened |
| 8 | 2305.13707 | Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models | 2023 | candidate |

## S119: tokenizer fertility low-resource languages Tagalog Filipino Austronesian

Serves item(s) 3, 4. Purpose: D14 per-language compute matching: tokenizer length disparity across languages (2026-10-07)

Runs: 1 (latest 2026-10-07T09:59:09+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2311.07161 | Developing a Named Entity Recognition Dataset for Tagalog | 2023 | title-screened |
| 2 | 2205.15960 | NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages | 2022 | title-screened |
| 3 | 1907.00409 | Evaluating Language Model Finetuning Techniques for Low-resource Languages | 2019 | title-screened |
| 4 | 2505.20428 | The UD-NewsCrawl Treebank: Reflections and Challenges from a Large-scale Tagalog Syntactic Annotation Project | 2025 | included |
| 5 | 2602.17655 | What Language is This? Ask Your Tokenizer. | 2026 | title-screened |
| 6 | 2601.10161 | AWED-FiNER: Agents, Web applications, and Expert Detectors for Fine-grained Named Entity Recognition across 36 Languages for 6.6 Billion Speakers | 2026 | title-screened |
| 7 | 2111.06053 | Improving Large-scale Language Models and Resources for Filipino | 2021 | title-screened |
| 8 | 2508.14586 | Filling the Gap for Uzbek: Creating Translation Resources for Southern Uzbek | 2025 | title-screened |

## S120: compute budget drift between pilot calibration and full reinforcement learning training penalty coefficient

Serves item(s) 3, 4. Purpose: D14 full-run tolerance: RL policy compute drift between short calibration runs and full training (2026-10-07)

Runs: 1 (latest 2026-10-07T10:04:13+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2511.03710 | Shrinking the Variance: Shrinkage Baselines for Reinforcement Learning with Verifiable Rewards | 2025 | title-screened |
| 2 | 2601.19624 | Tracking Drift: Variation-Aware Entropy Scheduling for Non-Stationary Reinforcement Learning | 2026 | title-screened |
| 3 | 2505.19247 | Improving Value Estimation Critically Enhances Vanilla Policy Gradient | 2025 | title-screened |
| 4 | 2507.08761 | Penalizing Infeasible Actions and Reward Scaling in Reinforcement Learning with Offline Data | 2025 | title-screened |
| 5 | 2504.20887 | Return Capping: Sample Efficient CVaR Policy Gradient Optimisation | 2025 | title-screened |
| 6 | 2603.09117 | Decoupling Reasoning and Confidence: Resurrecting Calibration in Reinforcement Learning from Verifiable Rewards | 2026 | title-screened |
| 7 | 2607.10848 | Predictive Divergence Masks for LLM RL | 2026 | title-screened |
| 8 | 2609.32444 | Rethinking Training-Inference Mismatch in LLM Reinforcement Learning: Where It Arises and How to Correct It | 2026 | title-screened |

## S121: Lagrangian multiplier adaptive cost constraint satisfied at convergence reinforcement learning target rate

Serves item(s) 3, 4. Purpose: D14 full-run tolerance: RL policy compute drift between short calibration runs and full training (2026-10-07)

Runs: 1 (latest 2026-10-07T10:04:13+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2503.12932 | Efficient Action-Constrained Reinforcement Learning via Acceptance-Rejection Method and Augmented MDPs | 2025 | title-screened |
| 2 | 2202.06828 | On the Convergence of SARSA with Linear Function Approximation | 2022 | title-screened |
| 3 | 2302.01275 | ReLOAD: Reinforcement Learning with Optimistic Ascent-Descent for Last-Iterate Convergence in Constrained MDPs | 2023 | title-screened |
| 4 | 2505.21391 | Finite Sample Analysis of Linear Temporal Difference Learning with Arbitrary Features | 2025 | title-screened |
| 5 | 2506.16016 | Dual-Objective Reinforcement Learning with Novel Hamilton-Jacobi-Bellman Formulations | 2025 | title-screened |
| 6 | 2605.11975 | Stochastic Minimum-Cost Reach-Avoid Reinforcement Learning | 2026 | title-screened |
| 7 | 2606.18531 | When Does Trajectory-Level Supervision Permit Efficient Offline Reinforcement Learning? | 2026 | title-screened |
| 8 | 2301.13087 | Improved Regret for Efficient Online Reinforcement Learning with Linear Function Approximation | 2023 | title-screened |

## S122: error span annotation time per segment machine translation human evaluation cost MQM ESA

Serves item(s) 3, 4. Purpose: D14 annotation recount: human MT error-span annotation time and number of systems (2026-10-07)

Runs: 1 (latest 2026-10-07T10:14:11+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2510.24664 | MQM Re-Annotation: A Technique for Collaborative Evaluation of Machine Translation | 2025 | title-screened |
| 2 | 2401.01283 | Quality and Quantity of Machine Translation References for Automatic Metrics | 2024 | title-screened |
| 3 | 2308.07286 | The Devil is in the Errors: Leveraging Large Language Models for Fine-grained Machine Translation Evaluation | 2023 | included |
| 4 | 2503.03044 | QE4PE: Word-level Quality Estimation for Human Post-Editing | 2025 | title-screened |
| 5 | 1311.3961 | HEVAL: Yet Another Human Evaluation Metric | 2013 | title-screened |
| 6 | 2410.11127 | IsoChronoMeter: A simple and effective isochronic translation evaluation metric | 2024 | title-screened |
| 7 | 2405.16969 | The Multi-Range Theory of Translation Quality Measurement: MQM scoring models and Statistical Quality Control | 2024 | title-screened |
| 8 | 2210.15615 | ACES: Translation Accuracy Challenge Sets for Evaluating Machine Translation Metrics | 2022 | title-screened |

## S123: sentence-level versus document-level human evaluation machine translation context annotation time

Serves item(s) 3, 4. Purpose: D14 annotation unit: sentence-level vs paragraph/document-level human MT evaluation, time and context (2026-10-07)

Runs: 1 (latest 2026-10-07T10:22:25+00:00, `pwc 0.4.2	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2305.11142 | Discourse Centric Evaluation of Machine Translation with a Densely Annotated Parallel Corpus | 2023 | title-screened |
| 2 | 2012.06143 | Document-aligned Japanese-English Conversation Parallel Corpus | 2020 | title-screened |
| 3 | 2406.03869 | Recovering document annotations for sentence-level bitext | 2024 | title-screened |
| 4 | 2509.17249 | Extending Automatic Machine Translation Evaluation to Book-Length Documents | 2025 | title-screened |
| 5 | 2510.24664 | MQM Re-Annotation: A Technique for Collaborative Evaluation of Machine Translation | 2025 | title-screened |
| 6 | 2406.11049 | Reconsidering Sentence-Level Sign Language Translation | 2024 | title-screened |
| 7 | 1311.3961 | HEVAL: Yet Another Human Evaluation Metric | 2013 | title-screened |
| 8 | 2301.06825 | HanoiT: Enhancing Context-aware Translation via Selective Context | 2023 | title-screened |

## S124: English Tagalog Filipino parallel corpus machine translation low-resource dataset

Serves item(s) 1, 7. Purpose: Tranche-1 data survey: English-Filipino parallel corpora and their sizes (2026-10-07)

Runs: 1 (latest 2026-10-07T14:20:54+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2007.03541 | scb-mt-en-th-2020: A Large English-Thai Parallel Corpus | 2020 | excluded (screened 2026-10-07 (data survey), S124: English-Thai corpus, not Filipino) |
| 2 | 2009.09359 | Not Low-Resource Anymore: Aligner Ensembling, Batch Filtering, and New Datasets for Bengali-English Machine Translation | 2020 | excluded (screened 2026-10-07 (data survey), S124: Bengali-English, not Filipino) |
| 3 | 1902.01382 | The FLoRes Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English | 2019 | title-screened |
| 4 | 2007.07691 | A Multilingual Parallel Corpora Collection Effort for Indian Languages | 2020 | excluded (screened 2026-10-07 (data survey), S124: Indian languages, not Filipino) |
| 5 | 2301.02773 | Building a Parallel Corpus and Training Translation Models Between Luganda and English | 2023 | excluded (screened 2026-10-07 (data survey), S124: Luganda-English, not Filipino) |
| 6 | 2205.15960 | NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages | 2022 | title-screened |
| 7 | 2103.15625 | English-Twi Parallel Corpus for Machine Translation | 2021 | excluded (screened 2026-10-07 (data survey), S124: English-Twi, not Filipino) |
| 8 | 2511.00486 | Leveraging the Cross-Domain & Cross-Linguistic Corpus for Low Resource NMT: A Case Study On Bhili-Hindi-English Parallel Corpus | 2025 | excluded (screened 2026-10-07 (data survey), S124: Bhili-Hindi-English, not Filipino) |

## S125: quality audit of web-mined multilingual parallel corpora CCAligned WikiMatrix ParaCrawl low-resource languages

Serves item(s) 1, 7. Purpose: Tranche-1 data survey: known quality issues of web-mined en-tl bitext (2026-10-07)

Runs: 1 (latest 2026-10-07T14:20:55+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2103.12028 | Quality at a Glance: An Audit of Web-Crawled Multilingual Datasets | 2021 | candidate |
| 2 | 1907.05791 | WikiMatrix: Mining 135M Parallel Sentences in 1620 Language Pairs from Wikipedia | 2019 | candidate |
| 3 | 2403.08693 | Do Language Models Care About Text Quality? Evaluating Web-Crawled Corpora Across 11 Languages | 2024 | title-screened |
| 4 | 2502.19074 | Improving the Quality of Web-mined Parallel Corpora of Low-Resource Languages using Debiasing Heuristics |  | candidate |
| 5 | 2512.18834 | Mix, MinHash, and Match: Cross-Source Agreement for Multilingual Pretraining Datasets | 2025 | title-screened |
| 6 | 2203.08111 | Does Corpus Quality Really Matter for Low-Resource Languages? | 2022 | candidate |
| 7 | 2605.31136 | Multilingual and Cross-Lingual Citation Needed Detection on Wikipedia for Lower-Resource Languages | 2026 | title-screened |
| 8 | 2411.05527 | How Good is Your Wikipedia? Auditing Data Quality for Low-resource and Multilingual NLP | 2024 | title-screened |

## S126: LASER margin-based bitext mining CCMatrix NLLB mined data noise filtering

Serves item(s) 1, 7. Purpose: Tranche-1 data survey: how mined corpora (CCMatrix, NLLB) were made and filtered (2026-10-07)

Runs: 1 (latest 2026-10-07T14:20:55+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2207.04452 | NGAME: Negative Mining-aware Mini-batching for Extreme Classification | 2022 | excluded (screened 2026-10-07 (data survey), S126: extreme classification, off-topic) |
| 2 | 2509.18577 | Prior-based Noisy Text Data Filtering: Fast and Strong Alternative For Perplexity | 2026 | title-screened |
| 3 | 2603.24917 | Estimating near-verbatim extraction risk in language models with decoding-constrained beam search | 2026 | excluded (screened 2026-10-07 (data survey), S126: extraction risk in LMs, off-topic for bitext mining) |
| 4 | 2203.13920 | Canary Extraction in Natural Language Understanding Models | 2022 | excluded (screened 2026-10-07 (data survey), S126: canary extraction in NLU, off-topic) |
| 5 | 2210.11773 | SimANS: Simple Ambiguous Negatives Sampling for Dense Text Retrieval | 2022 | excluded (screened 2026-10-07 (data survey), S126: dense retrieval negatives, off-topic) |
| 6 | 2406.12150 | ChaosMining: A Benchmark to Evaluate Post-Hoc Local Attribution Methods in Low SNR Environments | 2024 | excluded (screened 2026-10-07 (data survey), S126: attribution benchmark, off-topic) |
| 7 | 2310.02110 | Sieve: Multimodal Dataset Pruning using Image Captioning Models |  | title-screened |
| 8 | 2402.14029 | Partial Search in a Frozen Network is Enough to Find a Strong Lottery Ticket | 2024 | excluded (screened 2026-10-07 (data survey), S126: lottery tickets, off-topic) |

## S127: Philippine languages NLP resources survey datasets Tagalog Cebuano

Serves item(s) 1, 7. Purpose: Tranche-1 data survey: Philippine-language resource catalogues (SEACrowd and others) (2026-10-07)

Runs: 1 (latest 2026-10-07T14:20:56+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2311.07161 | Developing a Named Entity Recognition Dataset for Tagalog | 2023 | title-screened |
| 2 | 2203.05437 | IndicNLG Benchmark: Multilingual Datasets for Diverse NLG Tasks in Indic Languages | 2022 | excluded (screened 2026-10-07 (data survey), S127: Indic NLG datasets, not Filipino) |
| 3 | 2604.18423 | BhashaSutra: A Task-Centric Unified Survey of Indian NLP Datasets, Corpora, and Resources | 2026 | excluded (screened 2026-10-07 (data survey), S127: Indian NLP survey, not Filipino) |
| 4 | 2205.15960 | NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages | 2022 | title-screened |
| 5 | 2311.07171 | calamanCy: A Tagalog Natural Language Processing Toolkit | 2023 | candidate |
| 6 | 2203.17225 | A Baseline Readability Model for Cebuano | 2022 | title-screened |
| 7 | — | Wiki-40B: Multilingual Language Model Dataset | 2020 | title-screened |
| 8 | 2404.06976 | Quati: A Brazilian Portuguese Information Retrieval Dataset from Native Speakers | 2024 | excluded (screened 2026-10-07 (data survey), S127: Portuguese IR dataset, off-topic) |

## S128: back-translation of monolingual target data for low-resource neural machine translation at scale

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): back-translation

Runs: 1 (latest 2026-10-17T03:46:04+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1808.09381 | Understanding Back-Translation at Scale | 2018 | candidate |
| 2 | 2305.14124 | When Does Monolingual Data Help Multilingual Translation: The Role of Domain and Model Scale | 2023 | candidate |
| 3 | 1805.11213 | Bi-Directional Neural Machine Translation with Synthetic Parallel Data | 2018 | title-screened |
| 4 | 2404.08259 | Investigating Neural Machine Translation for Low-Resource Languages: Using Bavarian as a Case Study | 2024 | title-screened |
| 5 | 2207.04672 | No Language Left Behind: Scaling Human-Centered Machine Translation | 2022 | included |
| 6 | 2004.14928 | Language Model Prior for Low-Resource Neural Machine Translation | 2020 | title-screened |
| 7 | 2501.19314 | An Efficient Approach for Machine Translation on Low-resource Languages: A Case Study in Vietnamese-Chinese | 2025 | title-screened |
| 8 | 2004.03672 | Dynamic Data Selection and Weighting for Iterative Back-Translation | 2020 | candidate |

## S129: iterative back-translation self-training forward translation low-resource machine translation

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): forward translation / self-training

Runs: 1 (latest 2026-10-17T03:46:05+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2004.03672 | Dynamic Data Selection and Weighting for Iterative Back-Translation | 2020 | candidate |
| 2 | 1805.11213 | Bi-Directional Neural Machine Translation with Synthetic Parallel Data | 2018 | title-screened |
| 3 | 2306.03856 | Iterative Translation Refinement with Large Language Models | 2023 | included |
| 4 | 1909.07342 | Multilingual Neural Machine Translation for Zero-Resource Languages | 2019 | title-screened |
| 5 | 2603.25489 | Translation Asymmetry in LLMs as a Data Augmentation Factor: A Case Study for 6 Romansh Language Varieties | 2026 | candidate |
| 6 | 1808.09381 | Understanding Back-Translation at Scale | 2018 | candidate |
| 7 | 2606.03782 | Reasoning over Grammar: Can Synthetic Linguistic Reasoning Traces Enhance Low-Resource Machine Translation? | 2026 | title-screened |
| 8 | 2509.20209 | Low-Resource English-Tigrinya MT: Leveraging Multilingual Models, Custom Tokenizers, and Clean Evaluation Benchmarks | 2025 | title-screened |

## S130: sequence-level knowledge distillation teacher student neural machine translation

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): sequence-level KD

Runs: 1 (latest 2026-10-17T03:46:05+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1606.07947 | Sequence-Level Knowledge Distillation | 2016 | candidate |
| 2 | 2412.15303 | Self-Evolution Knowledge Distillation for LLM-based Machine Translation | 2024 | title-screened |
| 3 | 2605.01374 | MTA: Multi-Granular Trajectory Alignment for Large Language Model Distillation | 2026 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 4 | 2403.01479 | Align-to-Distill: Trainable Attention Alignment for Knowledge Distillation in Neural Machine Translation | 2024 | title-screened |
| 5 | 2604.07466 | Cross-Tokenizer LLM Distillation through a Byte-Level Interface | 2026 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | — | Aggregating Cross-Domain Knowledge via Learnable Tokens for Multi-Teacher Distillation |  | title-screened |
| 7 | 2511.02833 | In Good GRACES: Principled Teacher Selection for Knowledge Distillation | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2310.03188 | Talking Models: Distill Pre-trained Knowledge to Downstream Models via Interactive Communication | 2023 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |

## S131: large language model generated synthetic parallel data for low-resource machine translation

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): LLM-generated parallel data

Runs: 1 (latest 2026-10-17T03:46:06+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.11862 | Understanding In-Context Machine Translation for Low-Resource Languages: A Case Study on Manchu | 2025 | title-screened |
| 2 | 2505.14423 | Scaling Low-Resource MT via Synthetic Data Generation with LLMs | 2025 | candidate |
| 3 | 2504.00339 | VNJPTranslate: A comprehensive pipeline for Vietnamese-Japanese translation | 2025 | title-screened |
| 4 | 2508.08680 | TopXGen: Topic-Diverse Parallel Data Generation for Low-Resource Machine Translation | 2025 | candidate |
| 5 | 2504.01919 | Bridging the Linguistic Divide: A Survey on Leveraging Large Language Models for Machine Translation | 2025 | title-screened |
| 6 | 2311.00998 | Replicable Benchmarking of Neural Machine Translation (NMT) on Low-Resource Local Languages in Indonesia | 2023 | title-screened |
| 7 | 2403.13638 | Do Not Worry if You Do Not Have Data: Building Pretrained Language Models Using Translationese | 2024 | title-screened |
| 8 | 2402.01939 | A Morphologically-Aware Dictionary-based Data Augmentation Technique for Machine Translation of Under-Represented Languages | 2024 | candidate |

## S132: pivot language triangulation synthetic parallel corpus zero-resource translation

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): pivot / triangulation

Runs: 1 (latest 2026-10-17T03:46:06+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2205.04651 | ParaCotta: Synthetic Multilingual Paraphrase Corpora from the Most Diverse Translation Sample Pair | 2022 | candidate |
| 2 | 2505.14423 | Scaling Low-Resource MT via Synthetic Data Generation with LLMs | 2025 | candidate |
| 3 | 2205.15960 | NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages | 2022 | title-screened |
| 4 | 2403.13638 | Do Not Worry if You Do Not Have Data: Building Pretrained Language Models Using Translationese | 2024 | title-screened |
| 5 | 2209.03316 | On the Complementarity between Pre-Training and Random-Initialization for Resource-Rich Machine Translation | 2022 | title-screened |
| 6 | 2502.19074 | Improving the Quality of Web-mined Parallel Corpora of Low-Resource Languages using Debiasing Heuristics |  | candidate |
| 7 | 1805.11213 | Bi-Directional Neural Machine Translation with Synthetic Parallel Data | 2018 | title-screened |
| 8 | 1911.10668 | JParaCrawl: A Large Scale Web-Based English-Japanese Parallel Corpus | 2019 | title-screened |

## S133: multilingual sentence embedding distillation teacher student LASER3 low-resource languages

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): sentence-encoder distillation (LASER3 / SONAR / Reimers)

Runs: 1 (latest 2026-10-17T03:46:06+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1812.10464 | Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond | 2018 | candidate |
| 2 | 2004.09813 | Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation | 2020 | candidate |
| 3 | 2302.08387 | LEALLA: Learning Lightweight Language-agnostic Sentence Embeddings with Knowledge Distillation | 2023 | candidate |
| 4 | 2205.12654 | Bitext Mining Using Distilled Sentence Representations for Low-Resource Languages | 2022 | candidate |
| 5 | 2509.11414 | Continually Adding New Languages to Multilingual Language Models | 2025 | title-screened |
| 6 | 2305.16302 | Cross-Lingual Knowledge Distillation for Answer Sentence Selection in Low-Resource Languages | 2023 | title-screened |
| 7 | 2603.01732 | Bootstrapping Embeddings for Low Resource Languages | 2026 | title-screened |
| 8 | 2504.06036 | Multi-Sense Embeddings for Language Models and Knowledge Distillation | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |

## S134: making monolingual sentence embeddings multilingual using knowledge distillation

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): sentence-encoder distillation (Reimers & Gurevych)

Runs: 1 (latest 2026-10-17T03:46:07+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2004.09813 | Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation | 2020 | candidate |
| 2 | 2504.06036 | Multi-Sense Embeddings for Language Models and Knowledge Distillation | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 3 | 2302.08387 | LEALLA: Learning Lightweight Language-agnostic Sentence Embeddings with Knowledge Distillation | 2023 | candidate |
| 4 | 1812.10464 | Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond | 2018 | candidate |
| 5 | 2412.14964 | Knowledge Injection via Prompt Distillation | 2024 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | 2306.01709 | Distilling Efficient Language-Specific Models for Cross-Lingual Transfer | 2023 | title-screened |
| 7 | 2007.01852 | Language-agnostic BERT Sentence Embedding | 2020 | candidate |
| 8 | 2103.06418 | LightMBERT: A Simple Yet Effective Method for Multilingual BERT Distillation | 2021 | title-screened |

## S135: bitext mining from monolingual web crawl LaBSE margin scoring new language pairs

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): own bitext mining

Runs: 1 (latest 2026-10-17T03:46:07+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2306.12907 | xSIM++: An Improved Proxy to Bitext Mining Performance for Low-Resource Languages | 2023 | candidate |
| 2 | 1911.04944 | CCMatrix: Mining Billions of High-Quality Parallel Sentences on the WEB | 2019 | candidate |
| 3 | 1907.05791 | WikiMatrix: Mining 135M Parallel Sentences in 1620 Language Pairs from Wikipedia | 2019 | candidate |
| 4 | 2205.12654 | Bitext Mining Using Distilled Sentence Representations for Low-Resource Languages | 2022 | candidate |
| 5 | 2504.02768 | MultiBLiMP 1.0: A Massively Multilingual Benchmark of Linguistic Minimal Pairs | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | 2406.07424 | MINERS: Multilingual Language Models as Semantic Retrievers | 2024 | title-screened |
| 7 | 2406.19892 | Automatic register identification for the open web using multilingual deep learning | 2024 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 1912.00582 | BLiMP: The Benchmark of Linguistic Minimal Pairs for English | 2019 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |

## S136: comparable corpora document alignment Wikipedia parallel sentence extraction

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): comparable corpora / document alignment

Runs: 1 (latest 2026-10-17T03:46:08+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2005.02324 | Neural CRF Model for Sentence Alignment in Text Simplification | 2020 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 2 | 1907.05791 | WikiMatrix: Mining 135M Parallel Sentences in 1620 Language Pairs from Wikipedia | 2019 | candidate |
| 3 | 2007.07691 | A Multilingual Parallel Corpora Collection Effort for Indian Languages | 2020 | excluded (screened 2026-10-07 (data survey), S124: Indian languages, not Filipino) |
| 4 | 2311.03696 | Bilingual Corpus Mining and Multistage Fine-Tuning for Improving Machine Translation of Lecture Transcripts | 2023 | title-screened |
| 5 | 1905.01715 | A Parallel Corpus of Theses and Dissertations Abstracts | 2019 | title-screened |
| 6 | 2108.05289 | Icelandic Parallel Abstracts Corpus | 2021 | title-screened |
| 7 | 1905.01852 | A Large Parallel Corpus of Full-Text Scientific Articles | 2019 | title-screened |
| 8 | 2010.02810 | Swiss Parliaments Corpus, an Automatically Aligned Swiss German Speech to Standard German Text Corpus | 2020 | title-screened |

## S137: code-switching data augmentation bilingual dictionary substitution machine translation

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): dictionary / code-switching augmentation

Runs: 1 (latest 2026-10-17T03:46:08+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2210.12214 | Optimizing Bilingual Neural Transducer with Synthetic Code-switching Text Generation | 2022 | title-screened |
| 2 | 2402.01939 | A Morphologically-Aware Dictionary-based Data Augmentation Technique for Machine Translation of Under-Represented Languages | 2024 | candidate |
| 3 | 2107.01573 | Arabic Code-Switching Speech Recognition using Monolingual Data | 2021 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 4 | 2010.05549 | Improving Low Resource Code-switched ASR using Augmented Code-switched TTS | 2020 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 5 | 2004.14200 | Syntax-aware Data Augmentation for Neural Machine Translation | 2020 | title-screened |
| 6 | 2406.02517 | Deterministic Reversible Data Augmentation for Neural Machine Translation | 2024 | title-screened |
| 7 | 2310.07423 | Adapting the adapters for code-switching in multilingual ASR | 2023 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2305.16724 | Code-Switched Text Synthesis in Unseen Language Pairs | 2023 | candidate |

## S138: human post-editing of machine translation to create low-resource parallel data SMOL

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): human post-editing

Runs: 1 (latest 2026-10-17T03:46:08+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2502.12301 | SMOL: Professionally translated parallel data for 115 under-represented languages | 2025 | candidate |
| 2 | 2511.18411 | SmolKalam: Ensemble Quality-Filtered Translation at Scale for High Quality Arabic Post-Training Data | 2025 | candidate |
| 3 | 2505.14423 | Scaling Low-Resource MT via Synthetic Data Generation with LLMs | 2025 | candidate |
| 4 | 2502.19074 | Improving the Quality of Web-mined Parallel Corpora of Low-Resource Languages using Debiasing Heuristics |  | candidate |
| 5 | 2402.01939 | A Morphologically-Aware Dictionary-based Data Augmentation Technique for Machine Translation of Under-Represented Languages | 2024 | candidate |
| 6 | 1905.01852 | A Large Parallel Corpus of Full-Text Scientific Articles | 2019 | title-screened |
| 7 | 2502.11862 | Understanding In-Context Machine Translation for Low-Resource Languages: A Case Study on Manchu | 2025 | title-screened |
| 8 | 2012.06143 | Document-aligned Japanese-English Conversation Parallel Corpus | 2020 | title-screened |

## S139: quality estimation filtering of synthetic back-translated data round-trip consistency

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): QE / round-trip filtering of synthetic data

Runs: 1 (latest 2026-10-17T03:46:09+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2408.04614 | Better Alignment with Instruction Back-and-Forth Translation | 2024 | title-screened |
| 2 | 1808.09381 | Understanding Back-Translation at Scale | 2018 | candidate |
| 3 | 2502.19941 | Alleviating Distribution Shift in Synthetic Data for Machine Translation Quality Estimation | 2025 | candidate |
| 4 | 2209.07351 | Rethinking Round-Trip Translation for Machine Translation Evaluation | 2022 | candidate |
| 5 | 1610.04841 | Translation Quality Estimation using Recurrent Neural Network | 2016 | title-screened |
| 6 | 2306.01549 | Evaluating Machine Translation Quality with Conformal Predictive Distributions | 2023 | title-screened |
| 7 | 2504.01908 | Benchmarking Synthetic Tabular Data: A Multi-Dimensional Evaluation Framework | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2502.14429 | Early-Exit and Instant Confidence Translation Quality Estimation | 2025 | title-screened |

## S140: NLLB distilled synthetic data translation dataset created with NLLB-200 outputs

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): use of NLLB outputs as training data

Runs: 1 (latest 2026-10-17T03:46:09+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2512.13884 | FiNERweb: Datasets and Artifacts for Scalable Multilingual Named Entity Recognition | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 2 | 2101.05716 | SICKNL: A Dataset for Dutch Natural Language Inference | 2021 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 3 | 1809.02922 | Transforming Question Answering Datasets Into Natural Language Inference Datasets | 2018 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 4 | 2408.06537 | Introducing the NewsPaLM MBR and QE Dataset: LLM-Generated High-Quality Parallel Data Outperforms Traditional Web-Crawled Data | 2024 | candidate |
| 5 | 2109.02846 | Datasets: A Community Library for Natural Language Processing | 2021 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | 2404.06996 | XNLIeu: a dataset for cross-lingual NLI in Basque | 2024 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 7 | 2503.10267 | An Expanded Massive Multilingual Dataset for High-Performance Language Technologies | 2025 | included |
| 8 | 2403.13638 | Do Not Worry if You Do Not Have Data: Building Pretrained Language Models Using Translationese | 2024 | title-screened |

## S141: translationese in back-translated training data evaluation original source test sets

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): testing synthetic data / translationese

Runs: 1 (latest 2026-10-17T03:46:10+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1808.09381 | Understanding Back-Translation at Scale | 2018 | candidate |
| 2 | 2401.06568 | Lost in the Source Language: How Large Language Models Evaluate the Quality of Machine Translation | 2024 | title-screened |
| 3 | 2509.14031 | You Are What You Train: Effects of Data Composition on Training Context-aware Machine Translation Models |  | title-screened |
| 4 | 2408.04614 | Better Alignment with Instruction Back-and-Forth Translation | 2024 | title-screened |
| 5 | 2608.10812 | Reference-Free Post-Training of Open Large Language Models for Multilingual Machine Translation | 2026 | title-screened |
| 6 | 2609.04173 | Last Translation Benchmark | 2026 | included |
| 7 | 1610.04841 | Translation Quality Estimation using Recurrent Neural Network | 2016 | title-screened |
| 8 | 2004.03672 | Dynamic Data Selection and Weighting for Iterative Back-Translation | 2020 | candidate |

## S142: Improving neural machine translation models with monolingual data back-translation Sennrich

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): back-translation (origin paper)

Runs: 1 (latest 2026-10-17T03:46:34+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1808.09381 | Understanding Back-Translation at Scale | 2018 | candidate |
| 2 | 2004.03672 | Dynamic Data Selection and Weighting for Iterative Back-Translation | 2020 | candidate |
| 3 | 2109.07780 | Improving Neural Machine Translation by Bidirectional Training | 2021 | title-screened |
| 4 | 1805.11213 | Bi-Directional Neural Machine Translation with Synthetic Parallel Data | 2018 | title-screened |
| 5 | 2110.01811 | On the Complementarity between Pre-Training and Back-Translation for Neural Machine Translation | 2021 | candidate |
| 6 | 2209.13940 | Revamping Multilingual Agreement Bidirectionally via Switched Back-translation for Multilingual Neural Machine Translation | 2022 | title-screened |
| 7 | 2004.14928 | Language Model Prior for Low-Resource Neural Machine Translation | 2020 | title-screened |
| 8 | 2204.06812 | Learning to Generalize to More: Continuous Semantic Augmentation for Neural Machine Translation | 2022 | title-screened |

## S143: revisiting self-training for neural sequence generation noise

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): forward translation / self-training

Runs: 1 (latest 2026-10-17T03:46:35+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | — | Test Time Training for Long Videos via Frame Forgetting Network |  | title-screened |
| 2 | 2306.05426 | SequenceMatch: Imitation Learning for Autoregressive Sequence Modelling with Backtracking | 2023 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 3 | 2501.12352 | Test-time regression: a unifying framework for designing sequence models with associative memory | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 4 | — | NICE: Neurogenesis Inspired Contextual Encoding for Replay-free Class Incremental Learning |  | title-screened |
| 5 | 2106.15078 | Don't Take It Literally: An Edit-Invariant Sequence Loss for Text Generation | 2021 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | 2503.18371 | Do Your Best and Get Enough Rest for Continual Learning | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 7 | 2411.18447 | Continuous Autoregressive Models with Noise Augmentation Avoid Error Accumulation | 2024 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2506.03164 | Test-Time Scaling of Diffusion Models via Noise Trajectory Search | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |

## S144: Aya dataset collection translated with NLLB multilingual instruction data

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): use of NLLB outputs as training data

Runs: 1 (latest 2026-10-17T03:46:35+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2402.06619 | Aya Dataset: An Open-Access Collection for Multilingual Instruction Tuning | 2024 | candidate |
| 2 | 2402.07827 | Aya Model: An Instruction Finetuned Open-Access Multilingual Language Model | 2024 | title-screened |
| 3 | 2601.03136 | Limited Linguistic Diversity in Embodied AI Datasets | 2026 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 4 | 2305.11527 | InstructIE: A Bilingual Instruction-based Information Extraction Dataset | 2023 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 5 | 2405.15032 | Aya 23: Open Weight Releases to Further Multilingual Progress | 2024 | title-screened |
| 6 | — | Wiki-40B: Multilingual Language Model Dataset | 2020 | title-screened |
| 7 | 2407.09855 | Building pre-train LLM Dataset for the INDIC Languages: a case study on Hindi | 2024 | title-screened |
| 8 | 2312.12624 | Building a Llama2-finetuned LLM for Odia Language Utilizing Domain Knowledge Instruction Set | 2023 | title-screened |

## S145: SONAR sentence-level multimodal and language-agnostic representations

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): sentence-encoder distillation (SONAR)

Runs: 1 (latest 2026-10-17T03:46:36+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2308.11466 | SONAR: Sentence-Level Multimodal and Language-Agnostic Representations | 2023 | included |
| 2 | 2603.16606 | Omnilingual SONAR: Cross-Lingual and Cross-Modal Sentence Embeddings Bridging Massively Multilingual Text and Speech | 2026 | included |
| 3 | 2411.17666 | How do Multimodal Foundation Models Encode Text and Speech? An Analysis of Cross-Lingual and Cross-Modal Representations | 2024 | title-screened |
| 4 | 1707.07250 | Tensor Fusion Network for Multimodal Sentiment Analysis | 2017 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 5 | 2407.11351 | Learning Modality-agnostic Representation for Semantic Segmentation from Any Modalities | 2024 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | 2510.19398 | SONAR-SLT: Multilingual Sign Language Translation via Language-Agnostic Sentence Embedding Supervision | 2025 | title-screened |
| 7 | 2505.13777 | Sat2Sound: A Unified Framework for Zero-Shot Soundscape Mapping | 2026 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 1906.01815 | Towards Multimodal Sarcasm Detection (An _Obviously_ Perfect Paper) | 2019 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |

## S146: Tagalog Filipino English machine translation low-resource

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): Filipino-specific data techniques

Runs: 1 (latest 2026-10-17T03:46:36+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1902.01382 | The FLoRes Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English | 2019 | title-screened |
| 2 | 2509.20209 | Low-Resource English-Tigrinya MT: Leveraging Multilingual Models, Custom Tokenizers, and Clean Evaluation Benchmarks | 2025 | title-screened |
| 3 | 2410.07830 | NusaMT-7B: Machine Translation for Low-Resource Indonesian Languages with Large Language Models | 2024 | title-screened |
| 4 | 2301.02773 | Building a Parallel Corpus and Training Translation Models Between Luganda and English | 2023 | excluded (screened 2026-10-07 (data survey), S124: Luganda-English, not Filipino) |
| 5 | 2106.03193 | The FLORES-101 Evaluation Benchmark for Low-Resource and Multilingual Machine Translation | 2021 | included |
| 6 | 2004.00648 | Igbo-English Machine Translation: An Evaluation Benchmark | 2020 | title-screened |
| 7 | 2009.09359 | Not Low-Resource Anymore: Aligner Ensembling, Batch Filtering, and New Datasets for Bengali-English Machine Translation | 2020 | excluded (screened 2026-10-07 (data survey), S124: Bengali-English, not Filipino) |
| 8 | 2309.16575 | A Benchmark for Learning to Translate a New Language from One Grammar Book | 2023 | title-screened |

## S147: Taglish code-switched Tagalog English corpus

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): Taglish code-switching

Runs: 1 (latest 2026-10-17T03:46:36+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2505.20428 | The UD-NewsCrawl Treebank: Reflections and Challenges from a Large-scale Tagalog Syntactic Annotation Project | 2025 | included |
| 2 | 2311.07161 | Developing a Named Entity Recognition Dataset for Tagalog | 2023 | title-screened |
| 3 | 2112.06223 | ASCEND: A Spontaneous Chinese-English Dataset for Code-switching in Multi-turn Conversation | 2021 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 4 | 2502.18913 | CS-Dialogue: A 104-Hour Dataset of Spontaneous Mandarin-English Code-Switching Dialogues for Speech Recognition | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 5 | 2601.17277 | PingPong: A Natural Benchmark for Multi-Turn Code-Switching Dialogues | 2026 | title-screened |
| 6 | 2603.29221 | SiPaKosa: A Comprehensive Corpus of Canonical and Classical Buddhist Texts in Sinhala and Pali | 2026 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 7 | 2305.13989 | MasakhaPOS: Part-of-Speech Tagging for Typologically Diverse African Languages | 2023 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2603.16601 | Tarab: A Multi-Dialect Corpus of Arabic Lyrics and Poetry | 2026 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |

## S148: synthetic data for training multilingual sentence embeddings translated pairs

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): synthetic data for sentence embeddings

Runs: 1 (latest 2026-10-17T03:46:37+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2004.09813 | Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation | 2020 | candidate |
| 2 | 2403.13638 | Do Not Worry if You Do Not Have Data: Building Pretrained Language Models Using Translationese | 2024 | title-screened |
| 3 | 2502.08468 | mmE5: Improving Multimodal Multilingual Embeddings via High-quality Synthetic Data | 2025 | candidate |
| 4 | 2205.04651 | ParaCotta: Synthetic Multilingual Paraphrase Corpora from the Most Diverse Translation Sample Pair | 2022 | candidate |
| 5 | 2401.00368 | Improving Text Embeddings with Large Language Models | 2023 | candidate |
| 6 | 2604.11290 | Polyglot Teachers: Evaluating Language Models for Multilingual Synthetic Data Generation | 2026 | candidate |
| 7 | 2503.22973 | XL-Instruct: Synthetic Data for Cross-Lingual Open-Ended Generation | 2025 | title-screened |
| 8 | 2207.12759 | Training Effective Neural Sentence Encoders from Automatically Mined Paraphrases | 2022 | candidate |

## S149: pivot-based transfer learning neural machine translation non-English language pairs

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): pivot / triangulation

Runs: 1 (latest 2026-10-17T03:46:37+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 1711.02281 | Non-Autoregressive Neural Machine Translation | 2017 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 2 | 2110.01811 | On the Complementarity between Pre-Training and Back-Translation for Neural Machine Translation | 2021 | candidate |
| 3 | 2310.12236 | Direct Neural Machine Translation with Task-level Mixture of Experts models | 2023 | title-screened |
| 4 | 1611.04558 | Google's Multilingual Neural Machine Translation System: Enabling Zero-Shot Translation | 2016 | title-screened |
| 5 | 2405.09913 | TransMI: A Framework to Create Strong Baselines from Multilingual Pretrained Language Models for Transliterated Data | 2024 | title-screened |
| 6 | 2109.07780 | Improving Neural Machine Translation by Bidirectional Training | 2021 | title-screened |
| 7 | 1710.02095 | Machine Translation Evaluation with Neural Networks | 2017 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 8 | 2212.00138 | Word Alignment in the Era of Deep Learning: A Tutorial | 2022 | title-screened |

## S150: data augmentation for low-resource neural machine translation rare word substitution

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): dictionary augmentation

Runs: 1 (latest 2026-10-17T03:46:38+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2406.02517 | Deterministic Reversible Data Augmentation for Neural Machine Translation | 2024 | title-screened |
| 2 | 2402.05584 | AutoAugment Is What You Need: Enhancing Rule-based Augmentation Methods in Low-resource Regimes | 2024 | title-screened |
| 3 | 2603.25489 | Translation Asymmetry in LLMs as a Data Augmentation Factor: A Case Study for 6 Romansh Language Varieties | 2026 | candidate |
| 4 | 2309.04862 | Distributional Data Augmentation Methods for Low Resource Language | 2023 | title-screened |
| 5 | 2208.06957 | Syntax-driven Data Augmentation for Named Entity Recognition | 2022 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |
| 6 | 2402.01939 | A Morphologically-Aware Dictionary-based Data Augmentation Technique for Machine Translation of Under-Represented Languages | 2024 | candidate |
| 7 | 2309.12763 | Reduce, Reuse, Recycle: Is Perturbed Data better than Other Language augmentation for Low Resource Self-Supervised Speech Models | 2023 | title-screened |
| 8 | 2404.00415 | CoDa: Constrained Generation based Data Augmentation for Low-Resource NLP | 2024 | title-screened |

## S151: multilingual LLM translation fine-tuning with synthetic data from larger teacher distillation low-resource languages

Serves item(s) 1, 7. Purpose: Data-gathering techniques survey (2026-10-17): LLM teacher distillation for MT

Runs: 1 (latest 2026-10-17T03:46:38+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2601.16278 | Better as Generators Than Classifiers: Leveraging LLMs and Synthetic Data for Low-Resource Multilingual Classification | 2026 | title-screened |
| 2 | 2410.14815 | Adapting Multilingual LLMs to Low-Resource Languages using Continued Pre-training and Synthetic Corpus | 2024 | candidate |
| 3 | 2604.11290 | Polyglot Teachers: Evaluating Language Models for Multilingual Synthetic Data Generation | 2026 | candidate |
| 4 | 2311.10797 | TaCo: Enhancing Cross-Lingual Transfer for Low-Resource Languages in LLMs through Translation-Assisted Chain-of-Thought Processes | 2023 | title-screened |
| 5 | 2505.14423 | Scaling Low-Resource MT via Synthetic Data Generation with LLMs | 2025 | candidate |
| 6 | 2407.09879 | sPhinX: Sample Efficient Multilingual Instruction Fine-Tuning Through N-shot Guided Prompting | 2024 | title-screened |
| 7 | 2305.13627 | InstructAlign: High-and-Low Resource Language Alignment via Continual Crosslingual Instruction Tuning | 2023 | title-screened |
| 8 | 2311.05741 | Efficiently Adapting Pretrained Language Models To New Languages | 2023 | title-screened |

## S152: FineWeb-2 multilingual pretraining data per language

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): FineWeb-2 pipeline and per-language data

Runs: 1 (latest 2026-10-17T17:48:06+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2506.20920 | FineWeb2: One Pipeline to Scale Them All -- Adapting Pre-Training Data Processing to Every Language | 2025 | included |
| 2 | 2502.13252 | Multilingual Language Model Pretraining using Machine-translated Data | 2025 | title-screened |
| 3 | 2411.06402 | Fineweb-Edu-Ar: Machine-translated Corpus to Support Arabic Small Language Models | 2024 | title-screened |
| 4 | 2410.23956 | Multilingual Pretraining Using a Large Corpus Machine-Translated from a Single Source Language | 2024 | title-screened |
| 5 | 2408.08003 | Leveraging Web-Crawled Data for High-Quality Fine-Tuning | 2024 | title-screened |
| 6 | 2512.18834 | Mix, MinHash, and Match: Cross-Source Agreement for Multilingual Pretraining Datasets | 2025 | title-screened |
| 7 | 2406.17557 | The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale | 2024 | title-screened |
| 8 | 2512.13884 | FiNERweb: Datasets and Artifacts for Scalable Multilingual Named Entity Recognition | 2025 | excluded (screened 2026-10-17 (data-gathering techniques survey), title-screened off-topic for data gathering) |

## S153: HPLT 2.0 multilingual web corpus

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): HPLT 2.0 corpus

Runs: 1 (latest 2026-10-17T17:48:06+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2602.11968 | DHPLT: large-scale multilingual diachronic corpora and word representations for semantic change modelling | 2026 | title-screened |
| 2 | 2503.10267 | An Expanded Massive Multilingual Dataset for High-Performance Language Technologies | 2025 | included |
| 3 | 2403.14009 | A New Massive Multilingual Dataset for High-Performance Language Technologies | 2024 | title-screened |
| 4 | 2508.13079 | DocHPLT: A Massively Multilingual Document-Level Translation Dataset | 2025 | title-screened |
| 5 | 2008.05055 | The Annotation Guideline of LST20 Corpus | 2020 | title-screened |
| 6 | 1905.01715 | A Parallel Corpus of Theses and Dissertations Abstracts | 2019 | title-screened |
| 7 | 2511.01066 | HPLT 3.0: Very Large-Scale Multilingual Resources for LLM and MT. Mono- and Bi-lingual Data, Multilingual Evaluation, and Pre-Trained Models | 2025 | title-screened |
| 8 | 2103.12028 | Quality at a Glance: An Audit of Web-Crawled Multilingual Datasets | 2021 | candidate |

## S154: CulturaX cleaned multilingual dataset

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): CulturaX

Runs: 1 (latest 2026-10-17T17:48:07+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2309.09400 | CulturaX: A Cleaned, Enormous, and Multilingual Dataset for Large Language Models in 167 Languages | 2023 | included |
| 2 | — | Wiki-40B: Multilingual Language Model Dataset | 2020 | title-screened |
| 3 | 2502.11546 | DCAD-2000: A Multilingual Dataset across 2000+ Languages with Data Cleaning as Anomaly Detection | 2025 | title-screened |
| 4 | 2504.05154 | CARE: Aligning Language Models for Regional Cultural Awareness | 2025 | title-screened |
| 5 | 2504.08820 | CAReDiO: Enhancing Cultural Alignment of LLM via Representativeness and Distinctiveness Guided Data Optimization | 2025 | title-screened |
| 6 | 2509.17399 | DIWALI - Diversity and Inclusivity aWare cuLture specific Items for India: Dataset and Assessment of LLMs for Cultural Text Adaptation in Indian Context | 2025 | title-screened |
| 7 | 2604.19016 | AlignCultura: Towards Culturally Aligned Large Language Models? | 2026 | title-screened |
| 8 | 2407.12336 | M2DS: Multilingual Dataset for Multi-document Summarisation | 2024 | title-screened |

## S155: quality audit of multilingual web-crawled datasets low-resource languages

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): audits of web corpora for low-resource languages

Runs: 1 (latest 2026-10-17T17:48:07+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2103.12028 | Quality at a Glance: An Audit of Web-Crawled Multilingual Datasets | 2021 | candidate |
| 2 | 2203.08111 | Does Corpus Quality Really Matter for Low-Resource Languages? | 2022 | candidate |
| 3 | 2501.14506 | WanJuanSiLu: A High-Quality Open-Source Webtext Dataset for Low-Resource Languages | 2025 | title-screened |
| 4 | 2411.05527 | How Good is Your Wikipedia? Auditing Data Quality for Low-resource and Multilingual NLP | 2024 | title-screened |
| 5 | 2605.12623 | DocAtlas: Multilingual Document Understanding Across 80+ Languages | 2026 | title-screened |
| 6 | 2603.29244 | The Thiomi Dataset: A Large-Scale Multimodal Corpus for Low-Resource African Languages | 2026 | title-screened |
| 7 | 2605.31136 | Multilingual and Cross-Lingual Citation Needed Detection on Wikipedia for Lower-Resource Languages | 2026 | title-screened |
| 8 | 2404.17342 | From Multiple-Choice to Extractive QA: A Case Study for English and Arabic | 2024 | title-screened |

## S156: Tagalog Filipino monolingual corpus language model pretraining

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): existing Filipino monolingual corpora

Runs: 1 (latest 2026-10-17T17:48:08+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2111.06053 | Improving Large-scale Language Models and Resources for Filipino | 2021 | title-screened |
| 2 | 2404.01856 | Poro 34B and the Blessing of Multilinguality | 2024 | title-screened |
| 3 | 2407.13657 | FuLG: 150B Romanian Corpus for Language Model Pretraining | 2024 | title-screened |
| 4 | 2507.14664 | Mangosteen: An Open Thai Corpus for Language Model Pretraining | 2025 | title-screened |
| 5 | 2304.07880 | Sabiá: Portuguese Large Language Models | 2023 | title-screened |
| 6 | 2311.07171 | calamanCy: A Tagalog Natural Language Processing Toolkit | 2023 | candidate |
| 7 | 2205.06266 | Lifting the Curse of Multilinguality by Pre-training Modular Transformers | 2022 | title-screened |
| 8 | 2311.07161 | Developing a Named Entity Recognition Dataset for Tagalog | 2023 | title-screened |

## S157: MADLAD-400 multilingual document-level audited dataset

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): MADLAD-400 data audit

Runs: 1 (latest 2026-10-17T17:48:08+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2309.04662 | MADLAD-400: A Multilingual And Document-Level Large Audited Dataset | 2023 | included |
| 2 | 2210.09984 | Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | title-screened |
| 3 | — | Wiki-40B: Multilingual Language Model Dataset | 2020 | title-screened |
| 4 | 2103.12028 | Quality at a Glance: An Audit of Web-Crawled Multilingual Datasets | 2021 | candidate |
| 5 | 2110.06744 | Masader: Metadata Sourcing for Arabic Text and Speech Data Resources | 2021 | title-screened |
| 6 | 2502.11546 | DCAD-2000: A Multilingual Dataset across 2000+ Languages with Data Cleaning as Anomaly Detection | 2025 | title-screened |
| 7 | 2012.03411 | MLS: A Large-Scale Multilingual Dataset for Speech Research | 2020 | title-screened |
| 8 | 2308.16884 | The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | included |

## S158: cross-source agreement multilingual pretraining datasets deduplication

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): cross-corpus agreement for multilingual pretraining data

Runs: 1 (latest 2026-10-17T17:48:09+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2512.18834 | Mix, MinHash, and Match: Cross-Source Agreement for Multilingual Pretraining Datasets | 2025 | title-screened |
| 2 | 2506.20920 | FineWeb2: One Pipeline to Scale Them All -- Adapting Pre-Training Data Processing to Every Language | 2025 | included |
| 3 | 2505.22232 | Judging Quality Across Languages: A Multilingual Approach to Pretraining Data Filtering with Language Models | 2025 | title-screened |
| 4 | 2502.10361 | Enhancing Multilingual LLM Pretraining with Model-Based Data Selection | 2025 | title-screened |
| 5 | 2202.09583 | Models and Datasets for Cross-Lingual Summarisation | 2022 | title-screened |
| 6 | 2107.06499 | Deduplicating Training Data Makes Language Models Better | 2021 | title-screened |
| 7 | 2502.11546 | DCAD-2000: A Multilingual Dataset across 2000+ Languages with Data Cleaning as Anomaly Detection | 2025 | title-screened |
| 8 | 2406.13236 | Data Contamination Can Cross Language Barriers | 2024 | title-screened |

## S159: multilingual denoising pretraining sequence-to-sequence machine translation

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): denoising pretraining for MT sentence encoders

Runs: 1 (latest 2026-10-17T17:48:09+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2001.08210 | Multilingual Denoising Pre-training for Neural Machine Translation | 2020 | title-screened |
| 2 | 2110.08547 | Towards Making the Most of Multilingual Pretraining for Zero-Shot Neural Machine Translation | 2021 | title-screened |
| 3 | 2201.07365 | Improving Neural Machine Translation by Denoising Training | 2022 | title-screened |
| 4 | 2407.16222 | PreAlign: Boosting Cross-Lingual Transfer by Early Establishment of Multilingual Alignment | 2024 | title-screened |
| 5 | 2008.00401 | Multilingual Translation with Extensible Multilingual Pretraining and Finetuning | 2020 | title-screened |
| 6 | 2408.01394 | Improving Multilingual Neural Machine Translation by Utilizing Semantic and Linguistic Features | 2024 | title-screened |
| 7 | 2106.06381 | Improving Pretrained Cross-Lingual Language Models via Self-Labeled Word Alignment | 2021 | title-screened |
| 8 | 2204.07834 | Bridging Cross-Lingual Gaps During Leveraging the Multilingual Sequence-to-Sequence Pretraining for Text Generation and Understanding | 2022 | title-screened |

## S160: Wikipedia data quality low-resource languages audit

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): Wikipedia quality for low-resource languages

Runs: 1 (latest 2026-10-17T17:48:09+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2411.05527 | How Good is Your Wikipedia? Auditing Data Quality for Low-resource and Multilingual NLP | 2024 | title-screened |
| 2 | 2605.31136 | Multilingual and Cross-Lingual Citation Needed Detection on Wikipedia for Lower-Resource Languages | 2026 | title-screened |
| 3 | 2103.12028 | Quality at a Glance: An Audit of Web-Crawled Multilingual Datasets | 2021 | candidate |
| 4 | 2505.16506 | Utilizing citation index and synthetic quality measure to compare Wikipedia languages across various topics | 2025 | title-screened |
| 5 | 2203.08111 | Does Corpus Quality Really Matter for Low-Resource Languages? | 2022 | candidate |
| 6 | 2404.00565 | Leveraging Corpus Metadata to Detect Template-based Translation: An Exploratory Case Study of the Egyptian Arabic Wikipedia Edition | 2024 | title-screened |
| 7 | 2305.05928 | WikiSQE: A Large-Scale Dataset for Sentence Quality Estimation in Wikipedia | 2023 | title-screened |
| 8 | 2412.00948 | Uhura: A Benchmark for Evaluating Scientific Question Answering and Truthfulness in Low-Resource African Languages | 2024 | title-screened |

## S161: massively multilingual corpus 500 languages continued pretraining

Serves item(s) 7. Purpose: Monolingual Filipino text screening (2026-10-17, D4): Glot500 / MaLA corpora for Tagalog

Runs: 1 (latest 2026-10-17T17:48:10+00:00, `pwc 0.4.3	api v1`)

| # | arXiv | Title | Year | Status |
|---|---|---|---|---|
| 1 | 2305.12182 | Glot500: Scaling Multilingual Corpora and Language Models to 500 Languages | 2023 | title-screened |
| 2 | 2409.17892 | EMMA-500: Enhancing Massively Multilingual Adaptation of Large Language Models | 2024 | title-screened |
| 3 | 2506.20920 | FineWeb2: One Pipeline to Scale Them All -- Adapting Pre-Training Data Processing to Every Language | 2025 | included |
| 4 | 2410.23956 | Multilingual Pretraining Using a Large Corpus Machine-Translated from a Single Source Language | 2024 | title-screened |
| 5 | 2410.23825 | GlotCC: An Open Broad-Coverage CommonCrawl Corpus and Pipeline for Minority Languages | 2024 | title-screened |
| 6 | 2404.01856 | Poro 34B and the Blessing of Multilinguality | 2024 | title-screened |
| 7 | 2506.00469 | Massively Multilingual Adaptation of Large Language Models Using Bilingual Translation Data | 2025 | title-screened |
| 8 | 2304.09151 | UniMax: Fairer and more Effective Language Sampling for Large-Scale Multilingual Pretraining | 2023 | title-screened |

## Searches recorded elsewhere

Searches run with other tools (web, Hugging Face) are logged in the
appendix of their reports; they count as part of this protocol.

| Record | Section | Tools | Date | By |
|---|---|---|---|---|
| `research/diligence/A5-contamination.md` | search appendix | pwc, web search/fetch, gh, Hugging Face API | 2026-09-24 | A5 review |
| `research/diligence/A6-metric-validity.md` | Appendix A | pwc, web search/fetch, Hugging Face API | 2026-09-24 | A6 review |
| `research/diligence/A7-venues.md` | 6. Search appendix | web search/fetch, pwc | 2026-09-24 | A7 review |
| `research/data-survey/en-fil-parallel-2026-10-07.md` | Appendix A. Retrieval log | OPUS API (curl), Helsinki-NLP/OPUS GitHub corpus metadata, Hugging Face API, SEACrowd HF org listing | 2026-10-07 | data survey |
