# 2. RELATED WORKS: QUANTITATIVE ANALYSIS AND TECHNICAL METHODS

### 2.1. E-Government Chatbots and Public Administration AI
- **GuidaPA (Jimenez-Gutierrez et al., 2026) [1]:** Applied Federated Learning to train municipal chatbots across Italian administrative platforms (SIGESON and SIDFORS) using 4-bit QLoRA over 15 federated communication rounds. Reported ROUGE-1 of 61.10% (vs. 62.18% centralized, 41.45% untuned), BLEU-4 of 45.02% (vs. 26.97% untuned), and METEOR of 63.94%, demonstrating that on-premise execution preserves municipal data privacy without losing generation fidelity.
- **GovAI-Pipe (Kaplan, 2026) [2]:** Implemented a layered AI governance pipeline for Turkey's e-Government Gateway across 1,500 citizen services with pre-retrieval scope filtering and post-generation compliance validators, achieving 94.6% regulatory compliance.
- **Grip-on-LLMs (Samson et al., 2026) [3]:** Benchmarked 6 LLMs across 1,200 administrative prompts in the City of Amsterdam, revealing that standard models fail on municipal-specific rules in 38.2% of scenarios.
- **COPAL (Liu et al., 2026) [4]:** Evaluated composed organization-specific policy alignment across 3 public service datasets (85 policies), showing that standard prompting experiences a 42.1% performance drop under conflicting multi-tiered regulations.

### 2.2. Legal RAG, Hallucination Verification, and Statutory QA
- **LegalCheck (van der Meer & Rossi, ICAIL 2026) [5]:** Evaluated municipal legal advice generation in Amsterdam across 184 municipal cases, achieving 81.3% clause retrieval precision and 84.1% factual consistency.
- **LegalBench-RAG (Pipitone & Alami, 2024) [6]:** Benchmarked 162 legal tasks, demonstrating that standard RAG without structural indexing attains only 64.2% accuracy on clause extraction.
- **CanLegalRAGBench (Zhao et al., 2026) [7]:** Evaluated 2,500 Canadian precedents, proving that hybrid sparse-dense indexes lift MRR@5 by 27.4% over pure dense embeddings.
- **HyPA-RAG (Kalra et al., 2024) [8]:** Parameter-adaptive RAG tuning top-$k$ (3 to 15), lifting statutory QA F1 by 14.8%.
- **Large Legal Fictions (Dahl et al., 2024) [9]:** Investigated hallucination prevalence in legal generative AI across multiple legal jurisdictions, documenting error rates ranging from 69% to 88% on specific legal inquiries, reinforcing the need for strict factual citation.
- **Hallucination-Free RAG (Cao et al., 2024) [10]:** Established constraint-governed retrieval frameworks guaranteeing strict grounding on domain gazetteers.
- **Chain-of-Verification (CoVe - Dhuliawala et al., 2023) [11]:** 4-stage pipeline that factorizes queries into independent verification steps, reducing hallucinations by 38.0% to 56.0% on factual QA tasks.
- **Self-RAG (Asai et al., ICLR 2024) [12]:** Reflection token generation where a 7B model outperformed ChatGPT by 12.8% on PopQA with 81.2% FactCheck precision.
- **CRITIC (Gou et al., ICLR 2024) [13]:** Tool-interactive self-correction improving answer factuality from 42.1% to 71.4% and removing 64.0% of calculation errors.
- **GASP Grounding (Bouke et al., IPM 2026) [14]:** Perturbation-based sensitivity checking for public administration RAG, achieving 0.892 AUROC in detecting fabricated requirements.
- **Patel et al. (2025) [15]:** Multi-modal fact-verification framework reducing document form errors by 44.5%.
- **STARD (Statutory Reasoning Consortium, 2024) [28]:** A benchmark for statutory interpretation and administrative-procedure reasoning, establishing that rule-grounded evaluation of statutory QA exposes failure modes that open-domain factuality metrics miss — motivating the deterministic, database-anchored verification adopted in this work.

### 2.3. Hybrid Retrieval, Reranking, and Table Understanding
- **Corrective RAG (CRAG - Yan et al., 2024) [16]:** Retrieval evaluator raising PopQA accuracy from 48.7% (standard RAG) to 63.5%.
- **Akarsu et al. (2026) [17]:** Text-and-table legal documents benchmark, lifting table recall from 43.1% to 88.5% on fee/deadline schedules.
- **Baban et al. (KDD 2025) [18]:** Multi-agent hybrid retrieval achieving 19.3% NDCG@10 improvement.
- **LQ-RAG (2025) [19]:** Interactive query feedback lifting top-3 retrieval precision to 87.2%.
- **LegalMALR (Li et al., 2026) [20]:** Multi-agent statute retrieval achieving 85.6% accuracy on complex legal queries.

### 2.4. Local SLMs and Edge Computing
- **Shakti SLM (Aralimatti et al., 2025) [21]:** LoRA domain adaptation for 1.5B–3B models, delivering 86.4% task accuracy with <3.8GB VRAM at 24 tokens/s.
- **Qwen2.5 / Qwen3 (Qwen Team, 2024–2025) [22]:** Open foundation models delivering competitive reasoning and strong Vietnamese semantic preservation with low VRAM footprint.
- **Pareja et al. (2024) [23]:** SFT recipe showing 5,000 clean pairs beat 100,000 noisy samples, lifting instruction following from 52.3% to 81.7%.

### 2.5. Vietnamese Legal & Public Administration AI
- **ViGPTQA (Nguyen et al., 2023) [24]:** Dedicated Vietnamese legal QA benchmark of 15,000 pairs, reporting baseline GPT-3.5 performance of 68.5% Exact Match and 74.2% F1 score.
- **Hien et al. (IC3K 2025) [25]:** Proposed an integrated IR and LLM framework over 45,000 legal documents and 350,000 legal QA pairs, achieving 89.0% statutory retrieval accuracy, reducing latency by 58.0%, and obtaining a 4.23/5 user satisfaction score.
- **Ngo et al. (ICT 2025) [26]:** Built a Vietnamese statutory query assistant using Sentence Transformers, reporting 82.4% Top-1 precision, 88.6% Top-3 precision, and 1.12s average latency across 500 legal queries.
- **LawPal (Kumar et al., 2025) [27]:** Evaluated legal accessibility RAG on 1,000 civil queries, achieving 86.4% precision while reducing legal phrasing complexity by 68.0%.

### 2.6. Benchmarking Frameworks and Automated Judges
- **RAGAS (Es et al., EACL 2024) [29]:** Automated evaluation framework defining Faithfulness, Answer Relevance, Context Precision, and Context Recall, validated originally on the open-domain **WikiEval** benchmark (reporting 0.82 Pearson correlation on Faithfulness and 0.86 on Context Relevance with human annotators on Wikipedia-derived queries).
- **Constitutional AI (Bai et al., Anthropic 2022) [34]:** RLAIF with constitutional constraints, suppressing off-policy responses by 74.0%.
- **DSPy (Khattab et al., Stanford, ICLR 2024) [35]:** Declarative LM compiler lifting multi-hop pipeline accuracy from 46.2% to 70.8% (+24.6%).
- **ToolLLM (Qin et al., Tsinghua, ICLR 2024) [33]:** ToolBench API orchestration with DFSDT, lifting tool success rate from 34.2% to 72.5%.
