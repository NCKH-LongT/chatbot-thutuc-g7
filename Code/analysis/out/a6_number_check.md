# A6 - number check of the earlier-draft Table 1 and p-value rounding

Source: per-question rows + results/paired_stats.json; script analysis/a6_number_check.py.

Table 1 mismatches (rounded to the printed precision): none

| Config | bal2 | ans recall | ref recall | refusals | E2E | precision % | behavior |
|---|---|---|---|---|---|---|---|
| t1 off | 0.6475 | 0.7627 | 0.5323 | 132 | 19 | 11.7 | 177/313 |
| t1 B | 0.6918 | 0.678 | 0.7056 | 175 | 21 | 17.9 | 215/313 |
| t1 C | 0.7854 | 0.7119 | 0.8589 | 213 | 25 | 30.9 | 256/313 |
| t1 R | 0.4893 | 0.5593 | 0.4194 | 104 | 28 | 43.8 | 138/313 |
| t1 L_nb | 0.7652 | 0.6271 | 0.9032 | 224 | 14 | 21.9 | 261/313 |
| t1 L_emb | 0.8011 | 0.6949 | 0.9073 | 225 | 17 | 25.4 | 266/313 |
| t1 gate_only | 0.77 | 0.661 | 0.879 | 218 | 15 | 20.8 | 257/313 |
| t1 A | 0.8144 | 0.7458 | 0.8831 | 219 | 35 | 45.5 | 263/313 |
| t1 AC | 0.8168 | 0.678 | 0.9556 | 237 | 32 | 58.2 | 278/313 |
| t1 ACname | 0.8338 | 0.7966 | 0.871 | 216 | 39 | 47.0 | 264/313 |
| t1 AB | 0.8229 | 0.7627 | 0.8831 | 219 | 36 | 46.2 | 264/313 |
| t2 off | 0.5707 | 0.619 | 0.5224 | 175 | 5 | 3.0 | 189/363 |
| t2 R | 0.4131 | 0.2381 | 0.5881 | 197 | 4 | 10.5 | 206/363 |
| t2 L_nb | 0.5787 | 0.2381 | 0.9194 | 308 | 2 | 6.9 | 314/363 |
| t2 L_emb | 0.5862 | 0.2381 | 0.9343 | 313 | 2 | 8.0 | 319/363 |
| t2 gate_only | 0.6665 | 0.4762 | 0.8567 | 287 | 5 | 9.1 | 298/363 |
| t2 A | 0.7052 | 0.5238 | 0.8866 | 297 | 9 | 19.6 | 309/363 |
| t2 AB | 0.6829 | 0.4762 | 0.8896 | 298 | 8 | 17.4 | 309/363 |
| t2 A2B | 0.729 | 0.5714 | 0.8866 | 297 | 10 | 20.0 | 309/363 |

| Pair | field | exact p | printed before | one rule |
|---|---|---|---|---|
| real_v2 off -> A | p_e2e | 0.00371917 | 0.004 (text) | 0.004 |
| real_v2 A -> C | p_behavior | 0.449963 | 0.45 (text) | 0.450 |
| real_v2 A -> C | p_e2e | 0.0639147 | 0.06 (text) / 0,064 (table md) | 0.064 |
| real_v2 A -> AC | p_behavior | 0.0166738 | 0.017 (text) | 0.017 |
| real_v2 A -> AC | p_e2e | 0.647606 | 0,65 (table md) | 0.648 |
| real_v2 A -> ACname | p_e2e | 0.387695 | 0.39 (text) | 0.388 |
| real_v2 A -> rag4b | p_e2e | 0.229523 | 0,23 (table md) | 0.230 |
| real_v4 off -> A | p_e2e | 0.125 | 0,12 (table md) | 0.125 |
| real_v4 AB -> R2final | p_e2e | 0.625 | 0.63 (text) / 0,62 (table md) | 0.625 |
| real_v4 off -> R2final | p_e2e | 0.179688 | 0,18 (table md) | 0.180 |
| real_v4 R2final -> rag4b | p_e2e | 0.0703125 | 0,07 (table md) | 0.070 |
| real_v4 abl_gate_only -> learned_gate | p_behavior | 0.0258961 | not reported | 0.026 |
| real_v4 abl_gate_only -> learned_gate_emb | p_behavior | 0.00308768 | not reported | 0.003 |
