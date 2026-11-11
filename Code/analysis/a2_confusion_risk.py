"""A2. Per-class confusion matrices, answer precision, risk-coverage operating points and cost-weighted utility.

Inputs (read-only): per-question rows in Code/eval/hard/results/{test,test_v4}; strata from the result rows / label files.
Nothing is rerun. Outputs: out/a2_confusion_risk.json, out/a2_confusion_risk.md.

Confusion matrix columns: answer with a correct first procedure (ans_ok), answer with a wrong procedure (ans_wrong), clarify, refuse.
For non-answer gold rows every "answer" output is ans_wrong (there is no correct procedure to give).

Risk-coverage: coverage = answered / n; selective risk = wrong answers / answered = 1 - answer precision (Wilson 95% CI).
No configuration stores a continuous confidence score (rule outputs are discrete; the reranker and learned-gate scores were not saved),
so only one operating point per configuration exists; a threshold sweep would require rerunning systems and is NOT done here.

Utility per 100 questions, U(c, r) = 100 * (correct answers - c * wrong answers - r * missed answerable) / n, with refusals and
clarifications otherwise worth 0; c = cost of a wrong answer relative to the benefit of a correct one; r = cost of not answering an
answerable question (refusing or clarifying it). Always refusing scores U = -100 * r * n_answer / n.
Break-even c* = correct / wrong (with r = 0): a configuration beats always-refusing only if a wrong answer costs less than c* correct ones.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import T1, T2, NAMES, dump, e2e, load_labels, load_rows, wilson  # noqa: E402

MAIN = {"t1": ["off", "B", "C", "R", "L_nb", "L_emb", "gate_only", "A", "AC", "ACname", "AB"],
        "t2": ["off", "R", "L_nb", "L_emb", "gate_only", "A", "AB", "A2B"]}
CS, RS = (1, 2, 3, 5, 10), (0.0, 0.5)


def confusion(R, ids):
    M = {g: {"ans_ok": 0, "ans_wrong": 0, "clarify": 0, "refuse": 0} for g in ("answer", "clarify", "apologize")}
    for i in ids:
        r = R[i]
        if r["got"] == "answer":
            M[r["beh"]]["ans_ok" if e2e(r) else "ans_wrong"] += 1
        elif r["got"] == "clarify":
            M[r["beh"]]["clarify"] += 1
        else:
            M[r["beh"]]["refuse"] += 1
    return M


def risk(R, ids):
    n = len(ids)
    answered = sum(R[i]["got"] == "answer" for i in ids)
    ok = sum(e2e(R[i]) for i in ids)
    wrong = answered - ok
    wrong_to = {g: sum(R[i]["got"] == "answer" and not e2e(R[i]) and R[i]["beh"] == g for i in ids) for g in ("answer", "clarify", "apologize")}
    na = sum(R[i]["beh"] == "answer" for i in ids)
    missed = sum(R[i]["beh"] == "answer" and R[i]["got"] != "answer" for i in ids)
    lo, hi = wilson(ok, answered) if answered else (None, None)
    out = {"n": n, "n_answer": na, "answered": answered, "coverage": round(answered / n, 4), "correct_answers": ok, "wrong_answers": wrong,
           "wrong_answers_by_gold": wrong_to, "missed_answerable": missed,
           "precision": round(ok / answered, 4) if answered else None, "precision_ci95": [round(lo, 3), round(hi, 3)] if answered else None,
           "selective_risk": round(wrong / answered, 4) if answered else None,
           "break_even_cost_c_star": round(ok / wrong, 3) if wrong else None, "utility_per_100": {}}
    for r_ in RS:
        for c in CS:
            out["utility_per_100"][f"c={c},r={r_}"] = round(100 * (ok - c * wrong - r_ * missed) / n, 2)
    out["always_refuse_utility_per_100"] = {f"r={r_}": round(-100 * r_ * na / n, 2) for r_ in RS}
    return out


def main():
    res = {}
    md = ["# A2 - confusion matrices, answer precision, risk-coverage points, cost-weighted utility", "",
          "Source: per-question rows, Code/eval/hard/results/{test,test_v4}; script analysis/a2_confusion_risk.py.", ""]
    for t, files in (("t1", T1), ("t2", T2)):
        C = {k: load_rows(files[k]) for k in MAIN[t]}
        lab = load_labels(t)
        ids_all = sorted(C["off"])
        subsets = {"all": ids_all}
        if t == "t1":
            subsets["random_stratum"] = [i for i in ids_all if lab[i]["stratum"] == "random"]
            subsets["topical_stratum"] = [i for i in ids_all if lab[i]["stratum"] != "random"]
        for sname, ids in subsets.items():
            for k in MAIN[t]:
                res[f"{t} {sname} {k}"] = {"confusion": confusion(C[k], ids), "risk": risk(C[k], ids)}
            md += [f"## {t.upper()} - {sname} ({len(ids)} questions)", "",
                   "| Configuration | answered | coverage | correct | wrong (to refuse / to answer / to clarify gold) | precision [95%] | c* | U c=1 | U c=2 | U c=5 | U c=10 | U c=2,r=0.5 |",
                   "|---|---|---|---|---|---|---|---|---|---|---|---|"]
            for k in MAIN[t]:
                r = res[f"{t} {sname} {k}"]["risk"]
                w = r["wrong_answers_by_gold"]
                u = r["utility_per_100"]
                pr = "-" if r["precision"] is None else f"{100 * r['precision']:.1f}% [{100 * r['precision_ci95'][0]:.0f}, {100 * r['precision_ci95'][1]:.0f}]"
                md.append(f"| {NAMES[k]} | {r['answered']} | {r['coverage']:.3f} | {r['correct_answers']} | {r['wrong_answers']} ({w['apologize']} / {w['answer']} / {w['clarify']}) | "
                          f"{pr} | {r['break_even_cost_c_star']} | {u['c=1,r=0.0']} | {u['c=2,r=0.0']} | {u['c=5,r=0.0']} | {u['c=10,r=0.0']} | {u['c=2,r=0.5']} |")
            ar = res[f"{t} {sname} off"]["risk"]["always_refuse_utility_per_100"]
            md += ["", f"Always refuse: U = 0 (r = 0); U = {ar['r=0.5']} (r = 0.5).", ""]
            if sname == "all":
                md += ["Confusion matrices (rows = gold; columns = answer-correct-procedure / answer-wrong-procedure / clarify / refuse):", ""]
                for k in MAIN[t]:
                    M = res[f"{t} {sname} {k}"]["confusion"]
                    md.append(f"- **{NAMES[k]}**: answer [{M['answer']['ans_ok']}, {M['answer']['ans_wrong']}, {M['answer']['clarify']}, {M['answer']['refuse']}]; "
                              f"clarify [-, {M['clarify']['ans_wrong']}, {M['clarify']['clarify']}, {M['clarify']['refuse']}]; "
                              f"refuse [-, {M['apologize']['ans_wrong']}, {M['apologize']['clarify']}, {M['apologize']['refuse']}]")
                md.append("")
    dump("a2_confusion_risk.json", res)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a2_confusion_risk.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
