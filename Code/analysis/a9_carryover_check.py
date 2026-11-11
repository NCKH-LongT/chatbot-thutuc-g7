"""A9 - re-derive the earlier-draft numbers that the paper carries over but that A1-A8 do not cover.

Reads ONLY committed per-question result files under Code/, like common.py.
Run:  python -I -X utf8 a9_carryover_check.py   -> out/a9_carryover_check.json / .md

Checks:
 1. Test 1: BA2 of base and A on the 302 questions without the 11 near-duplicates (ids from Code/eval/real_v2/README.md, Limitation 2)
    and on the random stratum (earlier draft: 0.651 -> 0.810; 0.512 -> 0.859).
 2. Team-written blind set (518): BA2 of base and A (earlier draft: 0.852 for base).
 3. Round 2 on development (dev595 = real_v1 + real_v2): A -> A2+B behavior +/- (earlier draft / RUN_PLAN: +25/-0) and the
    "strict" gains/losses (decision correct AND, for answer, correct first procedure; earlier draft: 30/0 on dev vs 4/4 on test 2), and
    the share of questions whose decision or first procedure changes (earlier draft: 6.2% dev, 5.2% test 2).
 4. Test 1: the 24 answer questions that A misses - how they fail; refusals by the gate where the base had the correct
    procedure first; misses whose correct code is outside A's ranked top-5 (earlier draft: 12 refused, 4 of them by the gate with base
    top-1 correct; of the other 12, 7 with the correct code outside the top five).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RES, OUT, load_rows, bal, mcnemar_exact, fmt_p  # noqa: F401

NEAR_DUP = {f"real_v2-{n:03d}" for n in (13, 133, 152, 154, 164, 188, 212, 263, 268, 288, 297)}


def ba(R: dict, ids) -> float:
    return bal(R, {i: 1 for i in ids})


def strict(r) -> bool:
    if r["got"] != r["beh"]:
        return False
    return bool(r["top1"]) if r["beh"] == "answer" else True


def first_proc(r):
    t = r.get("tops") or []
    return t[0] if t else None


def main():
    out = {}
    # 1. test 1 clean subset and random stratum
    off, A = load_rows("test/real_v2_off.json"), load_rows("test/real_v2_A.json")
    clean = [i for i in off if i not in NEAR_DUP]
    rnd = [i for i in off if off[i]["stratum"] == "random"]
    out["t1_clean302"] = {"n": len(clean), "ba_off": round(ba(off, clean), 4), "ba_A": round(ba(A, clean), 4)}
    out["t1_random"] = {"n": len(rnd), "ba_off": round(ba(off, rnd), 4), "ba_A": round(ba(A, rnd), 4)}

    # 2. team-written blind
    gres = {}
    for k, f in (("off", "regress/golden_off_frozen.json"), ("A", "regress/golden_A_frozen.json")):
        rows = [r for r in json.load(open(os.path.join(RES, f), encoding="utf-8"))["rows"] if r["status"] == "blind"]
        R = {r["id"]: r for r in rows}
        gres[k] = {"n": len(R), "ba2": round(ba(R, list(R)), 4),
                   "ans_recall": round(sum(r["got"] == "answer" for r in rows if r["beh"] == "answer")
                                       / sum(r["beh"] == "answer" for r in rows), 4)}
    out["team_written_blind"] = gres

    # 3. round 2: development (dev595) and test 2
    def r2(fa, fb):
        Ra, Rb = load_rows(fa), load_rows(fb)
        ids = list(Ra)
        beh_plus = sum((not (Ra[i]["got"] == Ra[i]["beh"])) and Rb[i]["got"] == Rb[i]["beh"] for i in ids)
        beh_minus = sum(Ra[i]["got"] == Ra[i]["beh"] and Rb[i]["got"] != Rb[i]["beh"] for i in ids)
        s_plus = sum((not strict(Ra[i])) and strict(Rb[i]) for i in ids)
        s_minus = sum(strict(Ra[i]) and not strict(Rb[i]) for i in ids)
        changed = sum(Ra[i]["got"] != Rb[i]["got"] or (Ra[i]["got"] == "answer" and first_proc(Ra[i]) != first_proc(Rb[i]))
                      for i in ids)
        return {"n": len(ids), "behavior_plus": beh_plus, "behavior_minus": beh_minus,
                "behavior_p": fmt_p(mcnemar_exact(beh_plus, beh_minus)),
                "strict_plus": s_plus, "strict_minus": s_minus,
                "changed_decision_or_first_procedure": changed, "changed_share": round(changed / len(ids), 4)}
    out["round2_dev595_A_to_A2B"] = r2("dev/d2_A.json", "dev/d2_AR2B.json")
    out["round2_t2_A_to_A2B"] = r2("test_v4/real_v4_A.json", "test_v4/real_v4_R2final.json")

    # 4. test 1: answer questions A misses
    miss = [i for i in A if A[i]["beh"] == "answer" and not (A[i]["got"] == "answer" and A[i]["top1"])]
    by_got = {}
    for i in miss:
        by_got[A[i]["got"]] = by_got.get(A[i]["got"], 0) + 1

    def route(r):
        rs = r.get("routes") or []
        return rs[-1][1] if rs else ""
    refused = [i for i in miss if A[i]["got"] == "apologize"]
    gate_refused = [i for i in refused if route(A[i]) != "not_found"]
    gate_refused_base_top1 = [i for i in gate_refused if off[i]["top1"]]
    others = [i for i in miss if A[i]["got"] != "apologize"]
    outside_top5 = [i for i in others if not (set(A[i]["exp"]) & set((A[i].get("ranked") or [])[:5]))]
    out["t1_A_answer_misses"] = {"n": len(miss), "by_decision": by_got, "refused": len(refused),
                                 "refused_by_gate": len(gate_refused),
                                 "refused_by_gate_with_base_top1_correct": len(gate_refused_base_top1),
                                 "not_refused": len(others), "not_refused_correct_code_outside_ranked_top5": len(outside_top5)}

    json.dump(out, open(os.path.join(OUT, "a9_carryover_check.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    md = ["# A9 - re-derivation of earlier-draft numbers carried into the paper", "",
          "Source: per-question rows in Code/eval/hard/results; script analysis/a9_carryover_check.py.", ""]
    for k, v in out.items():
        md.append(f"- **{k}**: {json.dumps(v, ensure_ascii=False)}")
    open(os.path.join(OUT, "a9_carryover_check.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
