# A4 - development vs test-1 top-1 gap of the base system

Source: results/dev/dev_off.json, results/test/real_v2_off.json, labels/*.jsonl; script analysis/a4_devtest_gap.py.

| Set / stratum | answer qs | top-1 [95%] | top-3 | correct code in ranked top-5 | MRR@5 | base decision on answer qs | >1 accepted code | portal mix |
|---|---|---|---|---|---|---|---|---|
| dev random | 13 | 2 [0.043, 0.422] | 3 | 3 | 0.192 | {'answer': 11, 'apologize': 2} | 0 | {'MPS': 7, 'BinhDinh': 6} |
| dev chude | 42 | 5 [0.052, 0.25] | 9 | 9 | 0.163 | {'clarify': 1, 'answer': 30, 'apologize': 11} | 5 | {'BinhDinh': 16, 'MPS': 26} |
| dev all | 55 | 7 [0.063, 0.24] | 12 | 12 | 0.17 | {'answer': 41, 'apologize': 13, 'clarify': 1} | 5 | {'MPS': 33, 'BinhDinh': 22} |
| t1 random | 11 | 3 [0.097, 0.566] | 3 | 3 | 0.273 | {'answer': 6, 'clarify': 2, 'apologize': 3} | 1 | {'MPS': 6, 'BinhDinh': 5} |
| t1 chude | 48 | 17 [0.234, 0.496] | 20 | 21 | 0.386 | {'answer': 39, 'apologize': 8, 'clarify': 1} | 18 | {'MPS': 25, 'BinhDinh': 23} |
| t1 all | 59 | 20 [0.231, 0.466] | 23 | 24 | 0.365 | {'answer': 45, 'clarify': 3, 'apologize': 11} | 19 | {'MPS': 31, 'BinhDinh': 28} |

Gold-code overlap: {'dev_distinct': 21, 't1_distinct': 24, 'shared_distinct': 16, 't1_answer_qs_whose_first_code_also_in_dev': 48, 'dev_top5_codes': [('1.116410', 13), ('1.116788', 10), ('1.012566', 5), ('1.013978', 4), ('1.115970', 3)], 't1_top5_codes': [('1.116410', 11), ('1.116788', 9), ('1.115970', 5), ('2.000635', 3), ('1.012566', 3)]}

## Multi-code check

- dev chude: {'n_answer': 42, 'top1_hits': 5, 'hits_on_multi_code_questions': 0, 'top1_if_only_first_listed_code_counted': 5}
- dev random: {'n_answer': 13, 'top1_hits': 2, 'hits_on_multi_code_questions': 0, 'top1_if_only_first_listed_code_counted': 2}
- dev all: {'n_answer': 55, 'top1_hits': 7, 'hits_on_multi_code_questions': 0, 'top1_if_only_first_listed_code_counted': 7}
- t1 chude: {'n_answer': 48, 'top1_hits': 17, 'hits_on_multi_code_questions': 5, 'top1_if_only_first_listed_code_counted': 16}
- t1 random: {'n_answer': 11, 'top1_hits': 3, 'hits_on_multi_code_questions': 0, 'top1_if_only_first_listed_code_counted': 3}
- t1 all: {'n_answer': 59, 'top1_hits': 20, 'hits_on_multi_code_questions': 5, 'top1_if_only_first_listed_code_counted': 19}
