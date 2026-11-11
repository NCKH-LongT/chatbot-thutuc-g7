"""A5. Label agreement for the REFUSE vs NON-REFUSE decision .

The second-pass labels B are not released as a file, but they are fully determined by released files:
  relabel_ids.json (the 100 ids), labels/test1_real_v2.jsonl (pass A labels) and agreement.txt, which lists EVERY item where the two
  passes differ (22 items, including the 9 that B set aside as 'skip'). For all other ids B == A.
The script reconstructs B, checks that it reproduces the 3x3 matrix and kappa printed in agreement.txt, then computes the binary
(refuse vs non-refuse) agreement and kappa with a 2,000-resample bootstrap interval (seed 20261025, as the relabel scripts).
Both passes are LLM-assisted (A: Claude; B: Gemini 4 Argon proposals checked by the project lead) - this is NOT human-human agreement.
Outputs: out/a5_agreement_refuse.{json,md}.
"""
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, dump, load_labels  # noqa: E402

REL = os.path.join(ROOT, "eval", "real_v2", "relabel")


def kappa(pairs, cats):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    ids = json.load(open(os.path.join(REL, "relabel_ids.json"), encoding="utf-8"))["ids"]
    A = load_labels("t1")
    B = {i: A[i]["beh"] for i in ids}
    txt = open(os.path.join(REL, "agreement.txt"), encoding="utf-8").read()
    for m in re.finditer(r"(real_v2-\d{3}) \| A: (\w+)[^|]*\| B: (\w+)", txt):
        i, a, b = m.groups()
        assert A[i]["beh"] == a, (i, a, A[i]["beh"])
        B[i] = b
    keep = [i for i in ids if B[i] != "skip"]
    cats3 = ("answer", "clarify", "apologize")
    pairs3 = [(A[i]["beh"], B[i]) for i in keep]
    mat = {a: {b: sum(1 for x, y in pairs3 if x == a and y == b) for b in cats3} for a in cats3}
    k3 = kappa(pairs3, cats3)
    pairs2 = [(a == "apologize", b == "apologize") for a, b in pairs3]
    k2 = kappa(pairs2, (True, False))
    agree2 = sum(a == b for a, b in pairs2)
    rnd = random.Random(20261025)
    ks = []
    for _ in range(2000):
        s = [pairs2[rnd.randrange(len(pairs2))] for _ in pairs2]
        ks.append(kappa(s, (True, False)))
    ks.sort()
    # with the 9 skips counted as non-refuse (B) - sensitivity: B set them aside as non-questions, A refused them
    pairs2s = [(A[i]["beh"] == "apologize", B[i] == "apologize") for i in ids]
    out = {"n_sample": len(ids), "n_both_kept": len(keep), "matrix_rows_A_cols_B": mat,
           "kappa3_reproduced": round(k3, 3), "kappa3_reported_in_agreement_txt": 0.685,
           "refuse_vs_nonrefuse": {"agree": agree2, "n": len(pairs2), "pct": round(agree2 / len(pairs2), 3),
                                   "both_refuse": sum(a and b for a, b in pairs2), "A_refuse_B_not": sum(a and not b for a, b in pairs2),
                                   "B_refuse_A_not": sum(b and not a for a, b in pairs2), "both_nonrefuse": sum((not a) and (not b) for a, b in pairs2),
                                   "kappa": round(k2, 3), "kappa_ci95_boot2000": [round(ks[int(0.025 * 2000)], 3), round(ks[int(0.975 * 2000) - 1], 3)]},
           "sensitivity_skips_as_nonrefuse_100_items": {"agree": sum(a == b for a, b in pairs2s), "n": len(pairs2s),
                                                        "kappa": round(kappa(pairs2s, (True, False)), 3)},
           "caveat": "Both passes LLM-assisted; B's checker (project lead) had seen aggregate class proportions. Not human-human agreement."}
    dump("a5_agreement_refuse.json", out)
    md = ["# A5 - agreement on refuse vs non-refuse (second-pass sample, test 1)", "",
          "Source: eval/real_v2/relabel/{relabel_ids.json, agreement.txt}, labels/test1_real_v2.jsonl; script analysis/a5_agreement_refuse.py.", "",
          f"- 3-class matrix reproduced (rows A, cols B): {mat}; kappa {out['kappa3_reproduced']} (agreement.txt: 0.685).",
          f"- Refuse vs non-refuse on the {len(pairs2)} items both kept: agree {agree2}/{len(pairs2)} ({100 * agree2 / len(pairs2):.1f}%), "
          f"kappa {out['refuse_vs_nonrefuse']['kappa']} (95% bootstrap {out['refuse_vs_nonrefuse']['kappa_ci95_boot2000']}); "
          f"disagreements: A refuse/B not {out['refuse_vs_nonrefuse']['A_refuse_B_not']}, B refuse/A not {out['refuse_vs_nonrefuse']['B_refuse_A_not']}.",
          f"- Sensitivity, all 100 items with B's 9 'skip' counted as non-refuse: kappa {out['sensitivity_skips_as_nonrefuse_100_items']['kappa']} "
          f"({out['sensitivity_skips_as_nonrefuse_100_items']['agree']}/100).",
          f"- Caveat: {out['caveat']}", ""]
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a5_agreement_refuse.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
