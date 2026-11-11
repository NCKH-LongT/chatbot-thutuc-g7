# analysis/ - recompute the paper's tables and statistics from the committed rows

These scripts read only files that are in this repository: the per-question result rows in `eval/hard/results/`,
the label files in `labels/` and the second-pass files in `eval/real_v2/relabel/`. They run no system, call no model
and need no question texts or procedure DB. Outputs are written to `analysis/out/` (committed, so a re-run can be compared with `git diff`).

```
cd Code/analysis
python -I -X utf8 a1_paired_all.py      # then a2 ... a10, see the notes below
```

Python 3.10+. The standard library is enough, except that `a1_paired_all.py` imports `scipy` (one conditional odds-ratio
interval, `common.cond_or_ci`; `pip install scipy`). `common.py` resolves `Code/` from its own location, so the scripts can be
run from any directory. Run `a1` before `a8` and `a10` (they read or import a1), and `a4` once per run (its `__main__` appends a section to its `.md`).

| Script | What it recomputes | Paper item |
|---|---|---|
| `a6_number_check.py` | Per configuration and test set: balanced accuracy, correct refusals, E2E, answer precision, behavior accuracy; the p-values under one rounding rule | Table 3 (`tab:main`) |
| `a1_paired_all.py` | Every paired comparison X -> Y: delta balanced accuracy with paired bootstrap 95% / 90% intervals (4,000 resamples, seed 20261027), gains and losses, exact McNemar p, MDE; checks against `eval/hard/results/paired_stats.json` | Table 3 (with a6) and Table 4 (`tab:paired`) |
| `a10_declared_round1.py` | The round-1 declared comparisons (base vs each variant and vs A+B on test 1) with Wilson intervals, using the same code as a1 | Table 4 (rows marked D) |
| `a2_confusion_risk.py` | Per-class confusion matrices, answer precision, break-even cost c*, utility per 100 questions | `tab:confusion` |
| `a8_power.py` | Fewest one-sided discordant questions with McNemar p < 0.05; ranges of the minimum detectable effects per test set (from a1) | Power / MDE statements |
| `a3_portal.py` | Label mix and effect of the rule layer and the gate per source portal; the gate categories behind the refusals | Portal (source/target mismatch) analysis |
| `a4_devtest_gap.py` | Development vs test 1 top-1 gap of the base system, by stratum and portal; multi-code label check | Development-test gap |
| `a5_agreement_refuse.py` | Agreement and Cohen's kappa for refuse vs non-refuse between the two labeling passes (100-question sample), with a bootstrap interval | Label agreement (kappa) |
| `a7_golden_check.py` | Team-written blind set: runs, exclusions, identity of the original run and the re-run | Team-written set |
| `a9_carryover_check.py` | Team-written set balanced accuracy; near-duplicate and random-stratum checks on test 1; round-2 development gains and losses; share of changed decisions; how the 24 answerable test-1 questions missed by A fail | Team-written set; numbers quoted in the text |

`common.py` holds the shared helpers (paths, the result-file map per configuration, balanced accuracy, McNemar, Wilson, Newcombe,
bootstrap). The bootstrap is the one in `eval/hard/paired_stats.py`, so the 95% intervals reproduce `paired_stats.json`.
