# A5 - agreement on refuse vs non-refuse (second-pass sample, test 1)

Source: eval/real_v2/relabel/{relabel_ids.json, agreement.txt}, labels/test1_real_v2.jsonl; script analysis/a5_agreement_refuse.py.

- 3-class matrix reproduced (rows A, cols B): {'answer': {'answer': 13, 'clarify': 7, 'apologize': 2}, 'clarify': {'answer': 1, 'clarify': 1, 'apologize': 0}, 'apologize': {'answer': 0, 'clarify': 2, 'apologize': 65}}; kappa 0.685 (agreement.txt: 0.685).
- Refuse vs non-refuse on the 91 items both kept: agree 87/91 (95.6%), kappa 0.887 (95% bootstrap [0.767, 0.974]); disagreements: A refuse/B not 2, B refuse/A not 2.
- Sensitivity, all 100 items with B's 9 'skip' counted as non-refuse: kappa 0.684 (87/100).
- Caveat: Both passes LLM-assisted; B's checker (project lead) had seen aggregate class proportions. Not human-human agreement.

