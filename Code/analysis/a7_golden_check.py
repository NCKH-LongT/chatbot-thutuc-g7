"""A7. Facts about the team-written (golden) blind set runs.

Reads (read-only) Code/eval/hard/results/regress/golden_{off,A2,off_frozen,A_frozen}.json: code stamps, the number of
blind cases excluded because their gold procedure code is absent from the 13 Oct 2026 snapshot (excluded_unmapped), class counts,
decision identity between the original and the rerun, and the base->A change. Commit dates are NOT in these files; they come from
`git log` of the product repository (not part of this repository). Outputs: out/a7_golden_check.{json,md}.
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RES, dump, mcnemar_exact  # noqa: E402

FILES = {"off_original": "golden_off.json", "A_original": "golden_A2.json", "off_rerun": "golden_off_frozen.json", "A_rerun": "golden_A_frozen.json"}


def main():
    D = {k: json.load(open(os.path.join(RES, "regress", f), encoding="utf-8")) for k, f in FILES.items()}
    out = {}
    blind = {}
    for k, d in D.items():
        rows = [r for r in d["rows"] if r["status"] == "blind"]
        blind[k] = {r["id"]: r for r in rows}
        st = d.get("stamp") or {}
        out[k] = {"stamp_git": st.get("git"), "settings": st.get("settings"), "excluded_unmapped": d.get("excluded_unmapped"),
                  "blind_scored_n": len(rows), "blind_classes": dict(Counter(r["beh"] for r in rows)),
                  "answer_rows_with_gold_code_for_top1": sum(r["beh"] == "answer" and r["scored"] for r in rows),
                  "behavior_correct": sum(r["beh_ok"] for r in rows), "top1": sum(bool(r["top1"]) for r in rows),
                  "refuse_correct": sum(r["beh"] == "apologize" and r["got"] == "apologize" for r in rows)}
    out["blind_total_before_exclusion"] = out["off_rerun"]["blind_scored_n"] + out["off_rerun"]["excluded_unmapped"]["blind"]
    out["identical_decisions_off"] = sum(blind["off_original"][i]["got"] == blind["off_rerun"][i]["got"] for i in blind["off_original"])
    out["identical_decisions_A"] = sum(blind["A_original"][i]["got"] == blind["A_rerun"][i]["got"] for i in blind["A_original"])
    g = sum(blind["A_rerun"][i]["beh_ok"] and not blind["off_rerun"][i]["beh_ok"] for i in blind["off_rerun"])
    l = sum(blind["off_rerun"][i]["beh_ok"] and not blind["A_rerun"][i]["beh_ok"] for i in blind["off_rerun"])
    out["off_to_A_behavior"] = {"gain": g, "loss": l, "p": mcnemar_exact(g, l)}
    out["refuse_share"] = {"of_518": round(out["off_rerun"]["blind_classes"]["apologize"] / 518, 4),
                           "of_553_if_no_exclusion": round(out["off_rerun"]["blind_classes"]["apologize"] / out["blind_total_before_exclusion"], 4)}
    dump("a7_golden_check.json", out)
    md = ["# A7 - team-written (golden) blind set: runs, exclusions, identity", "",
          "Source: Code/eval/hard/results/regress/golden_*.json; script analysis/a7_golden_check.py.", ""]
    for k in FILES:
        md.append(f"- {k}: stamp {out[k]['stamp_git']}, excluded {out[k]['excluded_unmapped']}, scored blind {out[k]['blind_scored_n']} "
                  f"{out[k]['blind_classes']}, answer rows with a gold code {out[k]['answer_rows_with_gold_code_for_top1']}, behavior {out[k]['behavior_correct']}, "
                  f"top-1 {out[k]['top1']}, correct refusals {out[k]['refuse_correct']}")
    md += [f"- blind questions before exclusion: {out['blind_total_before_exclusion']}",
           f"- identical decisions original vs rerun: off {out['identical_decisions_off']}/518, A {out['identical_decisions_A']}/518",
           f"- base -> A on the 518: +{g}/-{l} (p {mcnemar_exact(g, l):.3f})", f"- refuse share: {out['refuse_share']}", ""]
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a7_golden_check.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
