# A8 - power and minimum detectable effects

Source: out/a1_paired_all.json; script analysis/a8_power.py.

- Exact two-sided McNemar needs at least 6 discordant questions all in one direction for p < 0.05 (p = 0.0312; with 5: p = 0.0625).
- Test 1 (59 answer questions): balanced-accuracy MDE80 [0.024, 0.127]; E2E MDE80 [0.161, 0.246] (= [9.5, 14.5] questions).
- Test 2 (21 answer questions): balanced-accuracy MDE80 [0.133, 0.208]; E2E MDE80 [0.357, 0.378] (n/a = not reachable with the observed discordance).

| Set | pair | bal MDE80 | E2E MDE80 (prop.) | equivalence margin (90%) |
|---|---|---|---|---|
| T1 | off -> A | 0.104 | 0.246 | 0.227 |
| T1 | A -> AB | 0.024 | None | 0.025 |
| T1 | A -> C | 0.097 | 0.228 | 0.087 |
| T1 | A -> AC | 0.079 | 0.203 | 0.049 |
| T1 | A -> ACname | 0.041 | 0.161 | 0.046 |
| T1 | A -> R | 0.127 | 0.233 | 0.401 |
| T1 | gate_only -> L_nb | 0.073 | None | 0.048 |
| T1 | gate_only -> L_emb | 0.057 | None | 0.065 |
| T2 | off -> A | 0.138 | None | 0.214 |
| T2 | AB -> A2B | 0.133 | None | 0.125 |
| T2 | off -> A2B | 0.208 | 0.378 | 0.282 |
| T2 | A2B -> R | 0.153 | 0.357 | 0.411 |
| T2 | A -> A2B | 0.152 | None | 0.114 |
| T2 | gate_only -> L_nb | 0.169 | None | 0.187 |
| T2 | gate_only -> L_emb | 0.168 | None | 0.178 |
