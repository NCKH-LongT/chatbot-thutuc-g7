# Evaluating Three-Way scope decisions on questions from Vietnamese citizens under a Locked Protocol

Code, labels, per-question results and analysis scripts that accompany the paper.

**Authors:** Hoang Nhan Trinh, Viet Hung Nguyen, Le Thien Dan Pham (Department of Artificial Intelligence, FPT University, Ho Chi Minh City, Vietnam) and Long Truong (corresponding author), Anh Duy Bui, Ngoc Minh Chau Hoang (Faculty of Software Engineering, FPT University, Ho Chi Minh City, Vietnam).

## For reviewers (English)

### What this repository contains

The paper studies an assistant for commune/ward-level administrative procedures in Vietnam and asks when it should answer, clarify or refuse. The evaluation is locked and run once: the test sets (313 and 363 questions) were labeled and hashed before the code they test, and each configuration was run once.

Everything needed to check the reported numbers is in [`Code/`](Code/):

| Path | Content |
|---|---|
| [`Code/`](Code/) | The system (rules, ranking, optional reranker and LLM reader), the evaluation scripts, the procedure database, labels and per-question results. [`Code/README.md`](Code/README.md) maps each paper component to files (in Vietnamese). |
| [`Code/analysis/`](Code/analysis/) | Scripts that recompute the paper's tables and statistics from the committed per-question rows, with their outputs in `Code/analysis/out/`. [`Code/analysis/README.md`](Code/analysis/README.md) maps each script to the table or statement it reproduces. |
| `Code/labels/` | Labels for 958 questions: IDs and source pointers (dataset and row), no question texts. |
| `Code/eval/hard/results/` | Per-question decisions of every run (development, test 1, test 2), without question texts. |
| `Code/eval/real_v1/LOCK.md`, `Code/eval/real_v2/LOCK.md`, `Code/eval/real_v4/README.md` | SHA-256 hashes and commits at which the label sets (development, test 1, test 2) were locked. |
| `Code/data/runtime/knowledge/3-423eff02f8.db` | The procedure database used by all runs (public portal data, no personal data). |
| `07_paper_draft/latex/` | LaTeX source of the paper as submitted to ICCIES 2027 (Springer LNCS class). Build with pdflatex + bibtex. |

### What is not here

- **Question texts.** The questions come from two public Hugging Face datasets that state no license, so they are not redistributed. `Code/labels/` holds only IDs and row positions; `python run_server.py eval/rebuild_questions.py` (from `Code/`) re-fetches the texts from the datasets.

### How to reproduce

Three levels, from cheapest to most demanding. Run commands from `Code/` unless noted.

1. **Recompute the tables from the committed rows** (Python 3.10+, standard library; `scipy` for `a1_paired_all.py`; no database, no models, no question texts):

   ```
   cd Code/analysis
   python -I -X utf8 a1_paired_all.py      # then a2 ... a10, see analysis/README.md
   python ../eval/hard/paired_stats.py     # McNemar and bootstrap intervals -> eval/hard/results/paired_stats.json
   ```

   The regenerated files in `analysis/out/` and `paired_stats.json` are identical to the committed ones.

2. **Re-run the rules-only configurations** (Base, rule layer A, round 2): needs Python 3.10+ with `numpy`, the shipped database, and the question texts rebuilt as described above (network access to Hugging Face). No model is called. On the development set:

   ```
   python run_server.py eval/rebuild_questions.py
   python run_server.py eval/hard/dev.py                      # rule layer on (default)
   S3_SCOPE_GATE=0 S3_LEXICON2=0 S3_LETTER_STRIP=0 S3_WEAK_NAME=0 S3_FOCUS=0 S3_ORG_DEFAULT=0 \
       python run_server.py eval/hard/dev.py                  # Base (all rule switches off)
   ```

   The per-question decisions can be compared with `eval/hard/results/dev/`. The two locked test sets are read only with `--final real_v2|real_v4`; the paper's runs were made once, so re-running them is for verification only. The scripts `final_runs.sh`, `final_runs_v4.sh`, `ablation_runs.sh` and `regress.sh` in `eval/hard/` write to the git-ignored `.bench/` and `.tmp/`, never over the committed results.

3. **Configurations that need models** (reranker B, LLM reader C, A+C, the RAG baseline R, learned gates L): in addition to the above, install `requirements.txt`, then run a local [Ollama](https://ollama.com) with `qwen3:4b-instruct-2507-q4_K_M` and `bge-m3`; the reranker `BAAI/bge-reranker-v2-m3` runs through `transformers` (GPU recommended). Flags are listed in `eval/hard/README.md`; the exact settings of the paper's runs are in `eval/hard/final_runs.sh` and `eval/hard/final_runs_v4.sh`. Model outputs are not deterministic across hardware, so only the committed per-question rows are the reference.

### Data and privacy

Procedure records come from a public national portal and contain no personal data. Personal data in the questions was masked before labeling. See `Code/README.md` for the sources and the collection procedure.

### License

Apache License 2.0, see [`LICENSE`](LICENSE).

---

## Phần theo khuôn repo môn học (tiếng Việt)

Repo này là repo của nhóm 7 trong môn thực tập, dựng theo khuôn thư mục của môn. Bài báo 1 (System 3) là **thủ tục hành chính cấp xã/phường**: trợ lý chỉ phục vụ thủ tục do cấp xã/phường giải quyết, không phải mọi thủ tục.

- **Nhóm:** Nhóm 7 (thực tập).
- **Thành viên:** Trịnh Hoàng Nhân, Nguyễn Viết Hưng, Phạm Lê Thiên Dấn, Trương Long.
- **Đơn vị:** Trường Đại học FPT, TP. Hồ Chí Minh.

### Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `01_topic_proposal/` | Đề xuất đề tài, nhật ký đổi đề tài |
| `02_related_work/` | Từ khoá tìm kiếm, danh sách tài liệu đã kiểm, ma trận tổng quan, các tệp tóm tắt (`paper_summaries/`) |
| `03_problem_and_gap/` | Phát biểu vấn đề, khoảng trống nghiên cứu, câu hỏi nghiên cứu, phân tích đóng góp |
| `04_proposed_system/` | Tổng quan, kiến trúc, tích hợp model, luồng dữ liệu, sơ đồ (`diagrams/`) |
| `05_methodology/` | Phương pháp, dữ liệu, baseline, chỉ số |
| `06_experiment_results/` | Cài đặt thí nghiệm, kết quả, bảng (`tables/`), hình (`figures/`) |
| `07_paper_draft/` | Nguồn LaTeX của bài, bản nộp ICCIES 2027 (`latex/`) |
| `08_final_submission/` | Chỉ có `README.md`: PDF bản cuối sẽ được đưa lên sau khi có bản camera-ready |
| `weekly_reports/` | Báo cáo tuần |
| `Code/` | Code công khai đi kèm bài: System 3, script đánh giá, DB thủ tục, nhãn, kết quả từng câu (không có văn bản câu hỏi) |
| `Code/analysis/` | Script tính lại các bảng và thống kê của bài từ kết quả từng câu, kèm kết quả (`out/`) |

Các thư mục `01_` đến `06_` và `weekly_reports/` là tài liệu quá trình làm việc, giữ nguyên như đã nộp cho môn học; chúng có thể nhắc tới các bản nháp hoặc đường dẫn cũ không còn trong cây thư mục hiện tại.

### Đọc nhanh

- Tái lập: phần "How to reproduce" ở trên, rồi `Code/README.md` (tiếng Việt, ánh xạ giữa bài báo và tệp) và `Code/analysis/README.md`.
- Kết quả của bài: tính lại bằng `Code/analysis/`; bản tóm tắt của môn học ở `06_experiment_results/`.

### Dữ liệu và quyền riêng tư

- **Câu hỏi:** lấy từ hai bộ dữ liệu công khai trên Hugging Face. Hai bộ này không ghi giấy phép, nên văn bản câu hỏi không được phát hành lại; repo chỉ có mã câu và nhãn. Thông tin cá nhân đã được che trước khi gán nhãn.
- **Dữ liệu thủ tục:** thu từ Cổng Dịch vụ công Quốc gia, không chứa dữ liệu cá nhân; DB nằm trong `Code/data/runtime/knowledge/`.
- **Lịch sử repo:** các commit cũ (trước `e779b80`) là lịch sử của môn học và không được viết lại.
