# A3 - portal (source) analysis

Source: labels in Code/labels/*.jsonl (source -> portal) and per-question rows of eval/hard/results; script analysis/a3_portal.py. Gate categories are the system's own refusal routes in configuration A, not gold labels.

## dev MPS
- n = 140; labels {'apologize': 106, 'clarify': 1, 'answer': 33}; refuse share 0.757; strata {'random': 57, 'chude': 83}; random stratum n = 57, labels {'apologize': 49, 'clarify': 1, 'answer': 7}, refuse share 0.86
- base -> A: balanced 0.604 -> 0.858 (diff 95% [0.161, 0.348]), behavior +60/-4 (p 7.4e-14), correct refusals 35 -> 92, E2E 5 -> 15 of 33

## dev BinhDinh
- n = 142; labels {'apologize': 114, 'answer': 22, 'clarify': 6}; refuse share 0.803; strata {'random': 54, 'chude': 88}; random stratum n = 54, labels {'apologize': 48, 'answer': 6}, refuse share 0.889
- base -> A: balanced 0.628 -> 0.784 (diff 95% [0.056, 0.262]), behavior +24/-1 (p 1.5e-06), correct refusals 81 -> 101, E2E 1 -> 6 of 22

## dev all
- n = 282; labels {'apologize': 220, 'clarify': 7, 'answer': 55}; refuse share 0.78; strata {'random': 111, 'chude': 171}; random stratum n = 111, labels {'apologize': 97, 'clarify': 1, 'answer': 13}, refuse share 0.874
- base -> A: balanced 0.636 -> 0.83 (diff 95% [0.124, 0.264]), behavior +84/-5 (p 1.4e-19), correct refusals 116 -> 193, E2E 6 -> 21 of 55

## t1 MPS
- n = 144; labels {'apologize': 113, 'answer': 31}; refuse share 0.785; strata {'random': 62, 'chude': 82}; random stratum n = 62, labels {'apologize': 56, 'answer': 6}, refuse share 0.903
- base -> A: balanced 0.618 -> 0.875 (diff 95% [0.159, 0.35]), behavior +71/-5 (p 5.2e-16), correct refusals 34 -> 103, E2E 13 -> 20 of 31
- base -> gate only: balanced 0.618 -> 0.834 (diff 95% [0.132, 0.292]), behavior +67/-5 (p 6.4e-15)
- A_correct_refusals_by_category: {'petition': 31, 'internal': 19, 'not_in_db': 18, 'legal': 18, 'complaint': 8, 'not_found': 6, 'info': 2, 'status': 1}
- A_new_correct_refusals_vs_base_by_category: {'not_in_db': 17, 'legal': 15, 'petition': 15, 'internal': 12, 'complaint': 6, 'not_found': 2, 'status': 1, 'info': 1}
- A_refusals_of_answer_questions_by_category: {'info': 2, 'not_in_db': 2, 'legal': 1}

## t1 BinhDinh
- n = 169; labels {'apologize': 135, 'clarify': 6, 'answer': 28}; refuse share 0.799; strata {'random': 40, 'chude': 129}; random stratum n = 40, labels {'apologize': 34, 'clarify': 1, 'answer': 5}, refuse share 0.85
- base -> A: balanced 0.649 -> 0.751 (diff 95% [-0.001, 0.206]), behavior +25/-5 (p 0.00032), correct refusals 98 -> 116, E2E 6 -> 15 of 28
- base -> gate only: balanced 0.649 -> 0.701 (diff 95% [0.0, 0.094]), behavior +19/-1 (p 4e-05)
- A_correct_refusals_by_category: {'not_in_db': 65, 'not_found': 23, 'complaint': 18, 'status': 6, 'legal': 2, 'info': 1, 'internal': 1}
- A_new_correct_refusals_vs_base_by_category: {'not_in_db': 11, 'complaint': 4, 'status': 3, 'legal': 1, 'not_found': 1}
- A_refusals_of_answer_questions_by_category: {'not_found': 4, 'complaint': 2, 'info': 1}

## t1 all
- n = 313; labels {'apologize': 248, 'clarify': 6, 'answer': 59}; refuse share 0.792; strata {'random': 102, 'chude': 211}; random stratum n = 102, labels {'apologize': 90, 'clarify': 1, 'answer': 11}, refuse share 0.882
- base -> A: balanced 0.647 -> 0.814 (diff 95% [0.095, 0.24]), behavior +96/-10 (p 8.7e-19), correct refusals 132 -> 219, E2E 19 -> 35 of 59
- base -> gate only: balanced 0.647 -> 0.77 (diff 95% [0.072, 0.17]), behavior +86/-6 (p 3.1e-19)
- A_correct_refusals_by_category: {'not_in_db': 83, 'petition': 31, 'not_found': 29, 'complaint': 26, 'legal': 20, 'internal': 20, 'status': 7, 'info': 3}
- A_new_correct_refusals_vs_base_by_category: {'not_in_db': 28, 'legal': 16, 'petition': 15, 'internal': 12, 'complaint': 10, 'status': 4, 'not_found': 3, 'info': 1}
- A_refusals_of_answer_questions_by_category: {'not_found': 4, 'info': 3, 'complaint': 2, 'not_in_db': 2, 'legal': 1}

## t2 MPS
- n = 227; labels {'apologize': 215, 'answer': 10, 'clarify': 2}; refuse share 0.947; strata {'random': 227}; random stratum n = 227, labels {'apologize': 215, 'answer': 10, 'clarify': 2}, refuse share 0.947
- base -> A: balanced 0.614 -> 0.753 (diff 95% [-0.058, 0.339]), behavior +105/-4 (p 1.8e-26), correct refusals 92 -> 195, E2E 4 -> 6 of 10
- base -> gate only: balanced 0.614 -> 0.68 (diff 95% [-0.095, 0.217]), behavior +93/-3 (p 3.7e-24)
- A_correct_refusals_by_category: {'legal': 58, 'petition': 42, 'not_in_db': 32, 'internal': 25, 'not_found': 22, 'complaint': 16}
- A_new_correct_refusals_vs_base_by_category: {'legal': 36, 'not_in_db': 22, 'internal': 16, 'petition': 11, 'not_found': 11, 'complaint': 8}
- A_refusals_of_answer_questions_by_category: {'complaint': 1, 'not_in_db': 1, 'internal': 1, 'legal': 1}

## t2 BinhDinh
- n = 136; labels {'apologize': 120, 'answer': 11, 'clarify': 5}; refuse share 0.882; strata {'random': 136}; random stratum n = 136, labels {'apologize': 120, 'answer': 11, 'clarify': 5}, refuse share 0.882
- base -> A: balanced 0.573 -> 0.652 (diff 95% [0.046, 0.116]), behavior +20/-1 (p 2.1e-05), correct refusals 83 -> 102, E2E 1 -> 3 of 11
- base -> gate only: balanced 0.573 -> 0.652 (diff 95% [0.048, 0.114]), behavior +19/-0 (p 3.8e-06)
- A_correct_refusals_by_category: {'not_in_db': 54, 'not_found': 25, 'status': 14, 'complaint': 7, 'legal': 2}
- A_new_correct_refusals_vs_base_by_category: {'not_in_db': 14, 'status': 3, 'complaint': 2, 'not_found': 1}
- A_refusals_of_answer_questions_by_category: {'not_found': 4}

## t2 all
- n = 363; labels {'apologize': 335, 'answer': 21, 'clarify': 7}; refuse share 0.923; strata {'random': 363}; random stratum n = 363, labels {'apologize': 335, 'answer': 21, 'clarify': 7}, refuse share 0.923
- base -> A: balanced 0.571 -> 0.705 (diff 95% [0.033, 0.228]), behavior +125/-5 (p 4.4e-31), correct refusals 175 -> 297, E2E 5 -> 9 of 21
- base -> gate only: balanced 0.571 -> 0.666 (diff 95% [0.007, 0.168]), behavior +112/-3 (p 1.2e-29)
- A_correct_refusals_by_category: {'not_in_db': 86, 'legal': 60, 'not_found': 47, 'petition': 42, 'internal': 25, 'complaint': 23, 'status': 14}
- A_new_correct_refusals_vs_base_by_category: {'legal': 36, 'not_in_db': 36, 'internal': 16, 'not_found': 12, 'petition': 11, 'complaint': 10, 'status': 3}
- A_refusals_of_answer_questions_by_category: {'not_found': 4, 'complaint': 1, 'not_in_db': 1, 'internal': 1, 'legal': 1}

