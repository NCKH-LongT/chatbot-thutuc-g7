# 4. EMPIRICAL EVALUATION & TRANSPARENT RESULTS

All evaluation experiments were conducted on live runtime instances using the unified evaluation suite ([`eval/report.py`](file:///D:/dự%20án%20phase%202/merge_sys_3_4/eval/report.py)) under deterministic execution (`S3_USE_LLM=0`, rule planner), with LLM-assisted generation benchmarked on consumer edge hardware (**Intel Core i3-12100F 4C/8T @ 3.30–4.30 GHz, 32 GB DDR4 RAM, NVIDIA GeForce GTX 1660 SUPER 6 GB GDDR6**, local Ollama execution).

To ensure scientific integrity, **we strictly report Wilson 95% confidence intervals** for all binomial proportions and explicitly decouple the un-tuned **blind evaluation suites** from the developmental sets.

---

### 4.1. Strict Engine (System 3): Comprehensive Evaluation by Split Status

Table 1 summarizes system performance across 1,352 standardized administrative evaluation cases partitioned into blind, developmental, and holdout-used splits.

**Table 1: Strict Engine performance metrics across evaluation splits with Wilson 95% confidence intervals.**

| Split Status | Total Cases ($n$) | Behavioral Accuracy | Top-1 Accuracy | Top-3 Accuracy | MRR | nDCG@5 | Field Precision | Multi-Proc Complete | Clarify Recall | Refusal Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Blind (Official)** | **553** | **78%** (431/553) [74%–81%] | **73%** (295/406) [68%–77%] | **80%** (323/406) [75%–83%] | **0.759** | **0.752** | **51%** (199/388) [46%–56%] | **80%** (8/10) [49%–94%] | **47%** (40/86) [36%–57%] | **90%** (52/58) [79%–95%] |
| **DEV (Controlled)** | 641 | 98% (626/641) [96%–99%] | 98% (558/567) [97%–99%] | 99% (562/567) [98%–100%] | 0.987 | 0.976 | 99% (368/373) [97%–99%] | 89% (25/28) [73%–96%] | 88% (23/26) [71%–96%] | 91% (42/46) [80%–97%] |
| **Holdout-Used** | 158 | 85% (135/158) [79%–90%] | 87% (109/125) [80%–92%] | 90% (112/125) [83%–94%] | 0.876 | 0.885 | 76% (78/102) [67%–84%] | 76% (13/17) [53%–90%] | 30% (3/10) [11%–60%] | 80% (16/20) [58%–92%] |

On the un-tuned blind evaluation suite (553 cases), **Sys_3_4 maintains a robust 78% behavioral accuracy and 73% Top-1 accuracy**, with an MRR of 0.759. The primary performance bottleneck is identified in **Clarify Recall (47%)**, indicating that ambiguous citizen inquiries frequently default to single-procedure assumptions rather than triggering disambiguation cards. Conversely, **Safe Refusal reaches 90%**, confirming high resilience against out-of-scope inquiries.

---

### 4.2. Granular Breakdown Across Evaluation Benchmark Sources

Table 2 breaks down system performance across individual component benchmark datasets, including official blind suites, extended colloquial queries, multi-turn contexts, and municipal agency queries.

**Table 2: Breakdown of retrieval, ranking, and behavioral metrics across benchmark sources.**

| Benchmark Source | Nature & Scope | Cases ($n$) | Behavioral Acc. | Top-1 Retrieval | Top-3 Retrieval | MRR | nDCG@5 | Field Match | Clarify Recall | Safe Refusal |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `cases.jsonl` | Baseline & Core Suite | 590 | 98% (577/590) | 99% (503/510) | 99% (506/510) | 0.987 | 0.982 | 98% (362/369) | 83% (24/29) | 96% (45/47) |
| `cases_ctx.jsonl` | Multi-Turn Context Memory | 118 | 96% (113/118) | 97% (109/112) | 98% (110/112) | 0.978 | 0.947 | 98% (43/44) | — | 67% (4/6) |
| `cases_h2.jsonl` | Blind Holdout Phase 2 | 62 | 79% (49/62) | 81% (38/47) | 85% (40/47) | 0.812 | 0.825 | 64% (25/39) | 40% (2/5) | 67% (6/9) |
| `cases_h3.jsonl` | Blind Holdout Phase 3 | 88 | 85% (75/88) | 76% (51/67) | 84% (56/67) | 0.782 | 0.771 | 77% (44/57) | 33% (2/6) | 100% (12/12) |
| `cases_h4.json` | **Official Blind Holdout 4** | **106** | **85% (90/106)** | **78% (60/77)** | **87% (67/77)** | **0.824** | **0.805** | **45% (35/77)** | **62% (10/16)** | **100% (13/13)** |
| `cases_h5.json` | Blind Holdout Phase 5 | 111 | 77% (86/111) | 72% (58/81) | 77% (62/81) | 0.743 | 0.742 | 49% (40/81) | 60% (12/20) | 90% (9/10) |
| `cases_h6.json` | Blind Holdout Phase 6 | 126 | 74% (93/126) | 71% (62/87) | 80% (70/87) | 0.758 | 0.772 | 61% (53/87) | 39% (11/28) | 73% (8/11) |
| `cases_pseudo_real.json` | Colloquial Simulation 1 | 42 | 81% (34/42) | 73% (22/30) | 77% (23/30) | 0.753 | 0.706 | 43% (13/30) | 50% (3/6) | 100% (6/6) |
| `cases_pseudo_real2.json` | Colloquial Simulation 2 | 34 | 76% (26/34) | 79% (22/28) | 82% (23/28) | 0.804 | 0.795 | 18% (5/28) | 0% (0/3) | 67% (2/3) |
| `cases_pseudo_real3.json` | Stress Colloquial 3 | 36 | 47% (17/36) | 43% (12/28) | 50% (14/28) | 0.464 | 0.474 | 32% (9/28) | 17% (1/6) | 50% (1/2) |
| `cases_real_log_v1.json` | Handcrafted Citizen Logs | 29 | 76% (22/29) | 74% (17/23) | 78% (18/23) | 0.773 | 0.796 | 70% (16/23) | 0% (0/2) | 75% (3/4) |
| `cases_team.json` | High-Stakes Municipal Suite | 10 | 100% (10/10) | 100% (8/8) | 100% (8/8) | 1.000 | 0.952 | — | 100% (1/1) | 100% (1/1) |

---

### 4.3. Domain-Thematic Structural Evaluation (Template Benchmark)

To evaluate retrieval stability across specific statutory categories without the confounding noise of colloquial misspellings, we evaluated the system on the curated **Template Benchmark Suite** (12 thematic categories, $n=430$ cases).

**Table 3: Thematic evaluation across 12 statutory categories on the template benchmark ($n=430$).**

| Category / Intent Type | Test Cases ($n$) | Behavioral Acc. | Top-1 Retrieval | Top-3 Retrieval | MRR | nDCG@5 | Field Completeness | Multi-Intent Success |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `address` (Jurisdiction/Location) | 30 | 97% (29/30) | 100% (30/30) | 100% (30/30) | 1.000 | 1.000 | 50% (15/30) | — |
| `compare-khac-gi` (Distinction) | 20 | 100% (20/20) | 100% (20/20) | 100% (20/20) | 0.933 | 0.944 | — | 80% (16/20) |
| `compare-so-sanh` (Comparison) | 20 | 100% (20/20) | 100% (20/20) | 100% (20/20) | 1.000 | 1.000 | — | 100% (20/20) |
| `components` (Dossier Checklist) | 40 | 98% (39/40) | 95% (38/40) | 98% (39/40) | 0.963 | 0.966 | 98% (39/40) | — |
| `explain` (Procedural Guidance) | 40 | 98% (39/40) | 95% (38/40) | 98% (39/40) | 0.963 | 0.966 | 45% (18/40) | — |
| `fees` (Statutory Financial Costs) | 40 | 98% (39/40) | 100% (40/40) | 100% (40/40) | 1.000 | 1.000 | 90% (36/40) | — |
| `legal` (Governing Legal Decrees) | 40 | 98% (39/40) | 100% (40/40) | 100% (40/40) | 1.000 | 1.000 | 88% (35/40) | — |
| `list` (Domain-Wide Procedures) | 40 | 80% (32/40) | — | — | — | — | — | — |
| `multi_field` (Compound Field QA) | 40 | 98% (39/40) | 98% (39/40) | 100% (40/40) | 0.988 | 0.991 | 92% (37/40) | — |
| `online` (Digital Submission Portals) | 40 | 98% (39/40) | 98% (39/40) | 98% (39/40) | 0.975 | 0.975 | 82% (33/40) | — |
| `steps` (Execution Sequence) | 40 | 98% (39/40) | 100% (40/40) | 100% (40/40) | 1.000 | 1.000 | 90% (36/40) | — |
| `time` (Statutory Processing Deadlines)| 40 | 98% (39/40) | 100% (40/40) | 100% (40/40) | 1.000 | 1.000 | 88% (35/40) | — |

---

### 4.4. Friendly Engine (System 4): Multi-Domain & Document QA Evaluation

Table 4 reports empirical evaluation metrics for **System 4 (Friendly Mode)**, evaluating general dialogue, citizen document ingestion, tabular calculation, contextual behavior, and web search grounding.

**Table 4: Empirical evaluation metrics for the Friendly Engine (System 4).**

| Evaluation Scenario / Capability | Evaluated Scope & Query Nature | Empirical Result | Performance Assessment |
| :--- | :--- | :---: | :---: |
| **General Response Accuracy** | Unseen general inquiries and user prompts | **90.6% (29/32)** | High fidelity |
| **Resistance to Induced Hallucination** | Adversarial prompts with fake entities/costs | **83.3% (25/30 unhallucinated)** | Robust safe refusal |
| **Citizen Document QA (Word, Excel)** | Factual question answering over uploaded files | **100% (17/17 correct with citation)** | Perfect source grounding |
| **Tabular Counting & Aggregation** | Relational calculation (*"how many male students"*) | **100% (15/15, vs. 0% baseline)** | Zero aggregation errors |
| **Conversational Small Talk** | Natural greetings without spurious retrieval | **100% (25/25)** | Clean intent isolation |
| **Contextual Interaction Protocol** | 22 multi-turn scenarios (disambiguation, memory) | **95.5% (21/22 scenarios passed)** | High state stability |
| **DuckDuckGo Web Search Grounding** | Web retrieval over dynamic external topics | **87.5% (14/16 successful searches)** | Reliable real-time retrieval |
| **Web Numerical Hallucination Rate** | Fee/deadline figures against web snippets | **0/16 hallucinated figures (0.0%)** | 100% grounded in sources |

---

### 4.5. True Execution Latency & Hardware Profile

Table 5 details the true runtime latency profiles measured on local edge hardware (**Intel Core i3-12100F 4C/8T @ 3.30–4.30 GHz, 32 GB DDR4-3200 RAM, NVIDIA GeForce GTX 1660 SUPER 6 GB GDDR6**), distinguishing deterministic rule execution (CPU) from autoregressive SLM token generation (GPU and CPU).

**Table 5: Execution latency distribution across query archetypes and hardware modes.**

| Operational Pipeline | Underlying Execution Engine | p50 Latency | p95 Latency | Operational Notes |
| :--- | :--- | :---: | :---: | :--- |
| **Simple Queries (Strict)** | Deterministic Rules (CPU: i3-12100F) | **78 ms** | **122 ms** | Instant kiosk lookup |
| **Complex Queries (Strict)** | Deterministic Rules (CPU: i3-12100F) | **59 ms** | **122 ms** | Multi-field extraction |
| **Clarification Turns (Strict)**| State Machine FSM (CPU: i3-12100F) | **72 ms** | **143 ms** | Disambiguation card emission |
| **Out-of-Scope (Strict)** | Policy Guard (CPU: i3-12100F) | **52 ms** | **85 ms** | Safe refusal response |
| **Overall CPU Retrieval Range**| SQLite FTS5 + Rule Engine | **57–85 ms** | **85–122 ms** | **Pure algorithm latency** |
| **Generative Synthesis (SLM)** | Ollama `qwen3:4b` on GPU (GTX 1660S) | **3.19 s** | **6.27 s** | Fluid citizen explanation |
| **Generative Synthesis (CPU)** | Ollama `qwen3:4b` on CPU (i3-12100F) | **7.6–12.0 s** | **19.0–39.0 s** | 4–8x slower (GPU required) |


---

### 4.6. Safety, Privacy, and Injection Robustness (Tiers D1 & D2)

**Table 6: Empirical safety, PII protection, and prompt injection defense metrics.**

| Evaluation Tier | Metric / Test Suite Scope | Test Volume | Empirical Result | Target Compliance |
| :--- | :--- | :---: | :---: | :---: |
| **Tier D1 (Privacy)** | CCCD/National ID & Phone Redaction (Continuous digits) | 9 cases | **9/9 (100.0%)** | $\ge 99.0\%$ |
| **Tier D1 (Privacy)** | Separated Digits Redaction (Spaces, dashes, dots: `090 123 4567`) | 3 cases | **3/3 (100.0%)** | $100.0\%$ |
| **Tier D1 (Privacy)** | Non-PII Numerical False Positive Rate | 5 cases | **0/5 (0.0% FP)** | $0.0\%$ |
| **Tier D2 (Adversarial)**| Prompt Injection Detection (Direct override attacks) | 11 cases | **11/11 (100.0%)** | $\ge 95.0\%$ |
| **Tier D2 (Adversarial)**| Legitimate Administrative Query False Positive Rate | 6 cases | **0/6 (0.0% FP)** | $0.0\%$ |
| **Tier D2 (Adversarial)**| End-to-End System Safety Gate Execution | 17 cases | **17/17 (100.0%)** | $100.0\%$ |

Prior to the separator-aware regex patch in `server/policy/policy.py`, citizen PII formatted with whitespace or punctuation completely evaded filtering (**0/3 caught**). Following normalization, redaction recall reached **100% (3/3)** with zero false-positive scrubbing on administrative legal decision codes. Across 11 direct prompt injection attacks, the system maintained a **100% rejection rate** with zero false rejections on legitimate civil queries.
