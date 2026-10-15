# 5. DISCUSSION & SCIENTIFIC AUDIT OF EVALUATION METHODOLOGY

### 5.1. The Empirical Fallacy of LLM-as-a-Judge for Statutory RAG
Recent literature in retrieval-augmented generation relies heavily on synthetic LLM-as-a-judge frameworks such as RAGAS (Es et al., 2024). While the original RAGAS study demonstrated high human correlation when evaluated on general-knowledge Wikipedia queries (**WikiEval**), its validity when deployed with lightweight on-premise models in public administration has remained unverified.

We conducted an empirical calibration study (`eval/ragas_calib.py`) utilizing local SLMs (Qwen3-4B and Qwen2.5-7B) to evaluate 92 administrative question-answering pairs against negative controls:
1. **Planted Hallucinations:** When an explicit factual fabrication (*"This procedure is completely free and completed within 1 hour at any municipal agency"*) was injected into legitimate answers, **Qwen2.5-7B identified the hallucination in only 51% of cases (47/92)**, while Qwen3-4B caught only 30% (9/30).
2. **Inter-Judge Agreement:** When calibrated against an authoritative model baseline across 30 identical cases, Qwen2.5-7B achieved an inter-annotator agreement of **$\kappa = 0.02$ on Faithfulness** and **$\kappa = 0.20$ on Relevancy**, falling drastically short of acceptable scientific reliability ($\kappa \ge 0.60$).

These findings demonstrate that **relying uncritically on LLM-as-a-judge scores creates a false sense of factual safety**. Consequently, **Sys_3_4 establishes a strict architectural paradigm**: administrative factuality is enforced via deterministic database anchoring and rule-based verification, rather than generative post-hoc grading.

### 5.2. Analysis of the Generalization Gap in Public Administration
A comparison of the controlled developmental suite (DEV, 98% Top-1) and the unseen blind evaluation suite (553 cases, 73% Top-1) highlights the primary challenges of real-world deployment:
- **Lexical Divergence:** Colloquial queries frequently employ dialectal verbs (*"xin giấy chứng sinh"*, *"nhập khẩu cho vợ"*) that exhibit low lexical overlap with codified procedure titles (*"Đăng ký khai sinh"*, *"Đăng ký thường trú"*).
- **Brother Procedure Ambiguity:** In civil status registration, closely related procedures (e.g., *Đăng ký kết hôn có yếu tố nước ngoài* vs. *Đăng ký kết hôn trong nước*) share over 80% of vocabulary. Without explicit clarification dialogue, single-turn search defaults to the domestic procedure, depressing Top-1 retrieval while maintaining high Top-3 recall (80%–87%).

### 5.3. Known System & Data Limitations
1. **Clarification Recall Bottleneck:** In the blind evaluation suite, only 47% of ambiguous inquiries successfully triggered clarification cards, with the remainder resolving to an assumed top candidate.
2. **National Portal Snapshot Omissions:** In the national database snapshot, standardized fees are published for only 467 of 1,350 procedures (34.6%). For the remaining 883 procedures, the portal records no explicit fee schedule; Sys_3_4 strictly outputs a refusal (*"Phí chưa được công bố chính thức"*) to avoid hallucination.
3. **Database String Parsing Anomalies:** Database audits revealed approximately 31 records where currency punctuation was truncated during scraper ingestion (e.g., `"20.000"` parsed as 20 VND instead of 20,000 VND). The strict engine implements regex-level currency sanitization to prevent misleading cost outputs.
4. **Data Provenance Verification (In Progress):** To quantify the fidelity of the scraped gazetteer against the authoritative National Public Service Portal, we are conducting a manual provenance audit over a random sample of 50 procedure records, cross-checking fees, processing times, and dossier components against the live portal pages. a manual provenance audit over 50 procedure records yielded a source-faithful rate of 84.4% (211/250 fields; 95% CI: 79%–88%), rising to 93.5% (187/200; CI: 89%–96%) when restricted to the four core numerical/legal fields (fees, processing time, legal basis, decision number).
