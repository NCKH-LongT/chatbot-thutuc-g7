"""A4. The development-test top-1 gap of the base system (paper: 7/55 on dev vs 20/59 on test 1; topical stratum 5/42 vs 17/48).

What can be checked from released files (no question texts are released, so length / wording cannot be compared):
  * top-1, top-3, MRR@5 and 'correct procedure anywhere in the base's ranked list' by stratum and portal;
  * what the base system DID with the answer questions (answered, clarified, refused);
  * label shape: how many answer questions accept more than one procedure code (expect_ids), by set and stratum;
  * which procedures the answer questions point to (overlap of gold codes between dev and test, and concentration).
Inputs read-only: results/dev/dev_off.json, results/test/real_v2_off.json, labels/*.jsonl. Outputs: out/a4_devtest_gap.{json,md}.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import dump, load_labels, load_rows, wilson  # noqa: E402


def block(R, lab, ids):
    A = [i for i in ids if lab[i]["beh"] == "answer"]
    n = len(A)
    t1 = sum(bool(R[i]["top1"]) for i in A)
    t3 = sum(bool(R[i].get("top3")) for i in A)
    inlist = sum(any(p in set(lab[i]["expect_ids"]) for p in (R[i].get("ranked") or [])) for i in A)
    mrr = sum(R[i].get("rr", 0.0) for i in A) / n if n else None
    did = Counter(R[i]["got"] for i in A)
    multi = sum(len(lab[i]["expect_ids"]) > 1 for i in A)
    lo, hi = wilson(t1, n) if n else (None, None)
    return {"n_answer": n, "top1": t1, "top1_ci95": [round(lo, 3), round(hi, 3)] if n else None, "top3": t3,
            "correct_in_ranked_list_top5": inlist, "mrr5": round(mrr, 3) if mrr is not None else None,
            "base_decision_on_answer_qs": dict(did), "answer_qs_accepting_multiple_codes": multi,
            "portal_mix": dict(Counter(lab[i]["portal"] for i in A))}


def main():
    res = {}
    sets = {"dev": ("dev/dev_off.json", "dev"), "t1": ("test/real_v2_off.json", "t1")}
    gold_codes = {}
    for s, (f, lf) in sets.items():
        R, lab = load_rows(f), load_labels(lf)
        ids = sorted(R)
        for st in ("random", "chude", "all"):
            sub = [i for i in ids if st == "all" or lab[i]["stratum"] == st]
            res[f"{s} {st}"] = block(R, lab, sub)
        gold_codes[s] = Counter(c for i in ids if lab[i]["beh"] == "answer" for c in lab[i]["expect_ids"][:1])
    # concentration / overlap of the (first) gold procedure codes
    d, t = gold_codes["dev"], gold_codes["t1"]
    res["gold_first_code_overlap"] = {"dev_distinct": len(d), "t1_distinct": len(t), "shared_distinct": len(set(d) & set(t)),
                                      "t1_answer_qs_whose_first_code_also_in_dev": sum(v for k, v in t.items() if k in d),
                                      "dev_top5_codes": d.most_common(5), "t1_top5_codes": t.most_common(5)}
    dump("a4_devtest_gap.json", res)
    md = ["# A4 - development vs test-1 top-1 gap of the base system", "",
          "Source: results/dev/dev_off.json, results/test/real_v2_off.json, labels/*.jsonl; script analysis/a4_devtest_gap.py.", "",
          "| Set / stratum | answer qs | top-1 [95%] | top-3 | correct code in ranked top-5 | MRR@5 | base decision on answer qs | >1 accepted code | portal mix |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, v in res.items():
        if k.startswith("gold"):
            continue
        md.append(f"| {k} | {v['n_answer']} | {v['top1']} {v['top1_ci95']} | {v['top3']} | {v['correct_in_ranked_list_top5']} | {v['mrr5']} | "
                  f"{v['base_decision_on_answer_qs']} | {v['answer_qs_accepting_multiple_codes']} | {v['portal_mix']} |")
    md += ["", f"Gold-code overlap: {res['gold_first_code_overlap']}", ""]
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a4_devtest_gap.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()


def multi_code_check():
    """How many base top-1 hits on each set rely on an answer question that accepts several codes, and how many hit a code other
    than the first listed one (a 'strict' single-code reading of the label)."""
    out = {}
    for s, (f, lf) in {"dev": ("dev/dev_off.json", "dev"), "t1": ("test/real_v2_off.json", "t1")}.items():
        R, lab = load_rows(f), load_labels(lf)
        for st in ("chude", "random", "all"):
            A = [i for i in sorted(R) if lab[i]["beh"] == "answer" and (st == "all" or lab[i]["stratum"] == st)]
            hits = [i for i in A if R[i]["top1"]]
            multi_hits = [i for i in hits if len(lab[i]["expect_ids"]) > 1]
            strict = sum(1 for i in hits if R[i]["tops"] and R[i]["tops"][0] == lab[i]["expect_ids"][0])
            out[f"{s} {st}"] = {"n_answer": len(A), "top1_hits": len(hits), "hits_on_multi_code_questions": len(multi_hits),
                                "top1_if_only_first_listed_code_counted": strict}
    return out


if __name__ == "__main__":
    import json
    mc = multi_code_check()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a4_devtest_gap.json")
    d = json.load(open(path, encoding="utf-8"))
    d["multi_code_check"] = mc
    dump("a4_devtest_gap.json", d)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a4_devtest_gap.md"), "a", encoding="utf-8") as fh:
        fh.write("## Multi-code check\n\n" + "\n".join(f"- {k}: {v}" for k, v in mc.items()) + "\n")
    print(mc)
