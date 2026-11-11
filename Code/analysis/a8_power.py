"""A8. Power / minimum-detectable-effect summary for the paper's power statement.

Reads out/a1_paired_all.json (produced by a1_paired_all.py from committed per-question rows) and adds exact facts:
  * the smallest number of discordant questions, all in one direction, for which the exact two-sided McNemar test gives p < 0.05;
  * per test set, the range of the approximate MDE (80% power, alpha 0.05) of the balanced-accuracy difference and of the E2E proportion.
Outputs: out/a8_power.{json,md}.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, dump, mcnemar_exact  # noqa: E402

DECLARED_OR_DISCUSSED = {
    "t1": ["off -> A", "A -> AB", "A -> C", "A -> AC", "A -> ACname", "A -> R", "gate_only -> L_nb", "gate_only -> L_emb"],
    "t2": ["off -> A", "AB -> A2B", "off -> A2B", "A2B -> R", "A -> A2B", "gate_only -> L_nb", "gate_only -> L_emb"],
}


def main():
    a1 = json.load(open(os.path.join(OUT, "a1_paired_all.json"), encoding="utf-8"))
    kmin = next(k for k in range(1, 50) if mcnemar_exact(k, 0) < 0.05)
    out = {"min_one_direction_discordant_for_p_lt_0.05": kmin, "p_at_kmin": mcnemar_exact(kmin, 0), "p_at_kmin_minus_1": mcnemar_exact(kmin - 1, 0)}
    for t, pairs in DECLARED_OR_DISCUSSED.items():
        rows = {p: a1[f"{t} {p}"] for p in pairs}
        mb = [r["bal"]["mde80_approx"] for r in rows.values() if r["bal"]["mde80_approx"] > 0]
        me = [r["e2e_mcnemar"]["mde80_prop"] for r in rows.values() if r["e2e_mcnemar"]["mde80_prop"]]
        na = next(iter(rows.values()))["e2e_mcnemar"]["n_answer"]
        out[t] = {"n_answer": na, "bal_mde80_range": [min(mb), max(mb)], "e2e_mde80_prop_range": [min(me), max(me)] if me else None,
                  "e2e_mde80_questions_range": [round(min(me) * na, 1), round(max(me) * na, 1)] if me else None,
                  "per_pair": {p: {"bal_mde80": r["bal"]["mde80_approx"], "e2e_mde80_prop": r["e2e_mcnemar"]["mde80_prop"],
                                   "equiv_margin_90": r["bal"]["equiv_margin_90"]} for p, r in rows.items()}}
    dump("a8_power.json", out)
    md = ["# A8 - power and minimum detectable effects", "", "Source: out/a1_paired_all.json; script analysis/a8_power.py.", "",
          f"- Exact two-sided McNemar needs at least {kmin} discordant questions all in one direction for p < 0.05 "
          f"(p = {out['p_at_kmin']:.4f}; with {kmin - 1}: p = {out['p_at_kmin_minus_1']:.4f}).",
          f"- Test 1 ({out['t1']['n_answer']} answer questions): balanced-accuracy MDE80 {out['t1']['bal_mde80_range']}; E2E MDE80 "
          f"{out['t1']['e2e_mde80_prop_range']} (= {out['t1']['e2e_mde80_questions_range']} questions).",
          f"- Test 2 ({out['t2']['n_answer']} answer questions): balanced-accuracy MDE80 {out['t2']['bal_mde80_range']}; E2E MDE80 "
          f"{out['t2']['e2e_mde80_prop_range']} (n/a = not reachable with the observed discordance).", "",
          "| Set | pair | bal MDE80 | E2E MDE80 (prop.) | equivalence margin (90%) |", "|---|---|---|---|---|"]
    for t in ("t1", "t2"):
        for p, v in out[t]["per_pair"].items():
            md.append(f"| {t.upper()} | {p} | {v['bal_mde80']} | {v['e2e_mde80_prop']} | {v['equiv_margin_90']} |")
    open(os.path.join(OUT, "a8_power.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
