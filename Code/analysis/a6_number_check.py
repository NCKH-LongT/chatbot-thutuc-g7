"""A6. Recompute every number of the earlier draft's Table 1 and the text p-values from the per-question rows, flag mismatches, and print
the p-values under ONE rounding rule (common.fmt_p: p >= 0.001 -> 3 decimals half-up; smaller -> 1 significant digit, scientific).
Also records the behavior accuracy and 3-class confusion that define 'balanced accuracy' unambiguously.
Inputs read-only. Outputs: out/a6_number_check.{json,md}.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RES, T1, T2, NAMES, correct, dump, e2e, fmt_p, load_rows  # noqa: E402

# Table 1 of the earlier draft (sections/results.tex): (bal, correct refusals, E2E, precision %)
PAPER = {
    "t1": {"off": (0.647, 132, 19, 11.7), "B": (0.692, 175, 21, 17.9), "C": (0.785, 213, 25, 30.9), "R": (0.489, 104, 28, 43.8),
           "L_nb": (0.765, 224, 14, 21.9), "L_emb": (0.801, 225, 17, 25.4), "gate_only": (0.770, 218, 15, 20.8), "A": (0.814, 219, 35, 45.5),
           "AC": (0.817, 237, 32, 58.2), "ACname": (0.834, 216, 39, 47.0), "AB": (0.823, 219, 36, 46.2)},
    "t2": {"off": (0.571, 175, 5, 3.0), "R": (0.413, 197, 4, 10.5), "L_nb": (0.579, 308, 2, 6.9), "L_emb": (0.586, 313, 2, 8.0),
           "gate_only": (0.666, 287, 5, 9.1), "A": (0.705, 297, 9, 19.6), "AB": (0.683, 298, 8, 17.4), "A2B": (0.729, 297, 10, 20.0)},
}
# p-values as printed in the earlier draft text / the Vietnamese paired_tests.md, against paired_stats.json
P_TEXT = [("real_v2 off -> A", "p_e2e", "0.004 (text)"), ("real_v2 A -> C", "p_behavior", "0.45 (text)"), ("real_v2 A -> C", "p_e2e", "0.06 (text) / 0,064 (table md)"),
          ("real_v2 A -> AC", "p_behavior", "0.017 (text)"), ("real_v2 A -> AC", "p_e2e", "0,65 (table md)"), ("real_v2 A -> ACname", "p_e2e", "0.39 (text)"),
          ("real_v2 A -> rag4b", "p_e2e", "0,23 (table md)"), ("real_v4 off -> A", "p_e2e", "0,12 (table md)"),
          ("real_v4 AB -> R2final", "p_e2e", "0.63 (text) / 0,62 (table md)"), ("real_v4 off -> R2final", "p_e2e", "0,18 (table md)"),
          ("real_v4 R2final -> rag4b", "p_e2e", "0,07 (table md)"), ("real_v4 abl_gate_only -> learned_gate", "p_behavior", "not reported"),
          ("real_v4 abl_gate_only -> learned_gate_emb", "p_behavior", "not reported")]


def main():
    out = {"table1": {}, "mismatches": [], "pvalues": []}
    for t, files in (("t1", T1), ("t2", T2)):
        for k, (pb, pr, pe, pp) in PAPER[t].items():
            R = load_rows(files[k])
            rows = list(R.values())
            na = sum(r["beh"] == "answer" for r in rows)
            nr = sum(r["beh"] == "apologize" for r in rows)
            ra = sum(r["beh"] == "answer" and r["got"] == "answer" for r in rows) / na
            rr = sum(r["beh"] == "apologize" and r["got"] == "apologize" for r in rows)
            balv = (ra + rr / nr) / 2
            ee = sum(e2e(r) for r in rows)
            ans = sum(r["got"] == "answer" for r in rows)
            prec = 100 * ee / ans if ans else None
            beh = sum(correct(r) for r in rows)
            rec = {"bal2": round(balv, 4), "refusals": rr, "e2e": ee, "precision_pct": round(prec, 1), "behavior": f"{beh}/{len(rows)}",
                   "answer_recall": round(ra, 4), "refuse_recall": round(rr / nr, 4)}
            out["table1"][f"{t} {k}"] = rec
            if round(balv, 3) != pb or rr != pr or ee != pe or round(prec, 1) != pp:
                out["mismatches"].append({"cfg": f"{t} {k}", "paper": [pb, pr, pe, pp], "recomputed": [round(balv, 3), rr, ee, round(prec, 1)]})
    ps = json.load(open(os.path.join(RES, "paired_stats.json"), encoding="utf-8"))
    for key, field, printed in P_TEXT:
        p = ps[key][field]
        out["pvalues"].append({"pair": key, "field": field, "exact": p, "printed_before": printed, "one_rule": fmt_p(p)})
    dump("a6_number_check.json", out)
    md = ["# A6 - number check of the earlier-draft Table 1 and p-value rounding", "",
          "Source: per-question rows + results/paired_stats.json; script analysis/a6_number_check.py.", "",
          f"Table 1 mismatches (rounded to the printed precision): {out['mismatches'] or 'none'}", "",
          "| Config | bal2 | ans recall | ref recall | refusals | E2E | precision % | behavior |", "|---|---|---|---|---|---|---|---|"]
    for k, v in out["table1"].items():
        md.append(f"| {k} | {v['bal2']} | {v['answer_recall']} | {v['refuse_recall']} | {v['refusals']} | {v['e2e']} | {v['precision_pct']} | {v['behavior']} |")
    md += ["", "| Pair | field | exact p | printed before | one rule |", "|---|---|---|---|---|"]
    for r in out["pvalues"]:
        md.append(f"| {r['pair']} | {r['field']} | {r['exact']:.6g} | {r['printed_before']} | {r['one_rule']} |")
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a6_number_check.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
