"""A10 - paired statistics for the round-1 DECLARED comparisons that a1 did not compute.

The round-1 plan (Code/eval/real_v2/README.md, "Ke hoach do", locked before the code change) declared:
base vs each variant (A, B, C, A+C, A+C name) and base vs the final combination (A+B), with Wilson 95% intervals per metric.
It did NOT declare McNemar or bootstrap; those are computed here with exactly the same code as a1 (a1_paired_all.compare: same
bootstrap stream, seed 20261027, 4,000 resamples) so the numbers are comparable to Table 4. Reads only committed per-question files.
Run:  python -I -X utf8 a10_declared_round1.py   -> out/a10_declared_round1.{json,md}
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import T1, dump  # noqa: E402
import a1_paired_all  # noqa: E402
from a1_paired_all import compare, configs  # noqa: E402

# scipy is not needed here; it is only used by a1 for the conditional odds-ratio CI, which is not reported here.
a1_paired_all.cond_or_ci = lambda a, b: (None, None, None)

PAIRS = [("off", "A"), ("off", "B"), ("off", "C"), ("off", "AC"), ("off", "ACname"), ("off", "AB"), ("A", "AB")]


def main():
    C = configs(T1)
    res = {}
    L = ["# A10 - round-1 declared comparisons (base vs each variant and vs the selection A+B), test 1", "",
         "Script analysis/a10_declared_round1.py (same compare() as a1). Declared metric: Wilson intervals per configuration; the paired "
         "McNemar p and bootstrap intervals below were computed after the runs.", "",
         "| X -> Y | Bal X->Y | dBal [95%] | equiv m (90%) | MDE80 bal | Beh +/- (p) | E2E X->Y (+/-, p) |", "|---|---|---|---|---|---|---|"]
    for x, y in PAIRS:
        r = compare(C[x], C[y])
        res[f"t1 {x} -> {y}"] = r
        b, m, e = r["bal"], r["behavior_mcnemar"], r["e2e_mcnemar"]
        L.append(f"| {x} -> {y} | {b['x']:.3f}->{b['y']:.3f} | {b['diff']:+.3f} [{b['ci95'][0]:+.3f}, {b['ci95'][1]:+.3f}] | "
                 f"{b['equiv_margin_90']:.3f} | {b['mde80_approx']:.3f} | +{m['gain']}/-{m['loss']} ({m['p_fmt']}) | "
                 f"{e['x']}->{e['y']}/{e['n_answer']} (+{e['gain']}/-{e['loss']}, {e['p_fmt']}) |")
    dump("a10_declared_round1.json", res)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a10_declared_round1.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
