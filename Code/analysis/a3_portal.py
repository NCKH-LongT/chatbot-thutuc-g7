"""A3. Source/target mismatch facts: per-portal label mix, per-portal effect of the rule layer and of the gate, and which gate
categories produce the refusals (and the base->A gains) on each portal.

Portal of each question = the Hugging Face dataset in the label file's `source` field (Code/labels/*.jsonl):
  hf:doanhieung/vn-mps-public-service-qa -> MPS (Ministry of Public Security portal); hf:hieunguyen1053/dichvucong_faqs/hoi-dap -> BinhDinh.
Gate category of a refusal = the `routes` field the system itself wrote in each per-question row of configuration A (e.g. ["apologize",
"internal"]); this is the SYSTEM's reason, not a gold label (gold labels carry no refusal category in the released files).
Inputs read-only; nothing rerun. Outputs: out/a3_portal.json, out/a3_portal.md.
"""
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import B, SEED, DEV, T1, T2, bal, correct, dump, e2e, load_labels, load_rows, mcnemar_exact, pct  # noqa: E402


def bal_ci(X, Y, ids):
    X = {i: X[i] for i in ids}
    Y = {i: Y[i] for i in ids}
    one = {i: 1 for i in ids}
    rnd = random.Random(SEED)
    ds = []
    for _ in range(B):
        w = {}
        for _ in ids:
            i = rnd.choice(ids)
            w[i] = w.get(i, 0) + 1
        u, v = bal(X, w), bal(Y, w)
        if u is not None and v is not None:
            ds.append(v - u)
    ds.sort()
    return round(bal(X, one), 3), round(bal(Y, one), 3), [round(pct(ds, 0.025), 3), round(pct(ds, 0.975), 3)]


def refusal_reason(r):
    """First refusal category in the system's own routes (None if the question was not refused by a route)."""
    for step in (r.get("routes") or []):
        if step and step[0] == "apologize":
            return step[1] or "unspecified"
    return None


def main():
    res, md = {}, ["# A3 - portal (source) analysis", "",
                   "Source: labels in Code/labels/*.jsonl (source -> portal) and per-question rows of eval/hard/results; "
                   "script analysis/a3_portal.py. Gate categories are the system's own refusal routes in configuration A, not gold labels.", ""]
    for t, files, labf in (("dev", DEV, "dev"), ("t1", T1, "t1"), ("t2", T2, "t2")):
        lab = load_labels(labf)
        off, A = load_rows(files["off"]), load_rows(files["A"])
        go = load_rows(files["gate_only"]) if "gate_only" in files else None
        for portal in ("MPS", "BinhDinh", "all"):
            ids = sorted(i for i in lab if portal == "all" or lab[i]["portal"] == portal)
            mix = Counter(lab[i]["beh"] for i in ids)
            strat = Counter(lab[i]["stratum"] for i in ids)
            rnd_ids = [i for i in ids if lab[i]["stratum"] == "random"]
            rmix = Counter(lab[i]["beh"] for i in rnd_ids)
            entry = {"n": len(ids), "label_mix": dict(mix), "refuse_share": round(mix["apologize"] / len(ids), 3),
                     "strata": dict(strat), "random_stratum_n": len(rnd_ids), "random_stratum_label_mix": dict(rmix),
                     "random_stratum_refuse_share": round(rmix["apologize"] / len(rnd_ids), 3) if rnd_ids else None}
            if mix["answer"] and mix["apologize"]:
                bx, by, ci = bal_ci(off, A, ids)
                g = sum(correct(A[i]) and not correct(off[i]) for i in ids)
                l = sum(correct(off[i]) and not correct(A[i]) for i in ids)
                entry["base_to_A"] = {"bal_base": bx, "bal_A": by, "diff_ci95": ci, "behavior": f"+{g}/-{l}", "p": mcnemar_exact(g, l),
                                      "refusals_base": sum(lab[i]["beh"] == "apologize" and off[i]["got"] == "apologize" for i in ids),
                                      "refusals_A": sum(lab[i]["beh"] == "apologize" and A[i]["got"] == "apologize" for i in ids),
                                      "e2e_base": sum(e2e(off[i]) for i in ids), "e2e_A": sum(e2e(A[i]) for i in ids), "n_answer": mix["answer"]}
                if go:
                    gg = sum(correct(go[i]) and not correct(off[i]) for i in ids)
                    gl = sum(correct(off[i]) and not correct(go[i]) for i in ids)
                    gbx, gby, gci = bal_ci(off, go, ids)
                    entry["base_to_gate_only"] = {"bal_base": gbx, "bal_gate_only": gby, "diff_ci95": gci, "behavior": f"+{gg}/-{gl}",
                                                  "p": mcnemar_exact(gg, gl)}
            if t != "dev":
                # refusal categories of A on gold-refuse questions, and categories of the base->A gains
                cats = Counter(refusal_reason(A[i]) for i in ids if lab[i]["beh"] == "apologize" and A[i]["got"] == "apologize")
                gains = Counter(refusal_reason(A[i]) for i in ids
                                if lab[i]["beh"] == "apologize" and A[i]["got"] == "apologize" and off[i]["got"] != "apologize")
                wrong_ref = Counter(refusal_reason(A[i]) for i in ids if lab[i]["beh"] == "answer" and A[i]["got"] == "apologize")
                entry["A_correct_refusals_by_category"] = dict(cats.most_common())
                entry["A_new_correct_refusals_vs_base_by_category"] = dict(gains.most_common())
                entry["A_refusals_of_answer_questions_by_category"] = dict(wrong_ref.most_common())
            res[f"{t} {portal}"] = entry
    dump("a3_portal.json", res)
    for k, e in res.items():
        md.append(f"## {k}")
        md.append(f"- n = {e['n']}; labels {e['label_mix']}; refuse share {e['refuse_share']}; strata {e['strata']}; random stratum n = "
                  f"{e['random_stratum_n']}, labels {e['random_stratum_label_mix']}, refuse share {e['random_stratum_refuse_share']}")
        if "base_to_A" in e:
            b = e["base_to_A"]
            md.append(f"- base -> A: balanced {b['bal_base']} -> {b['bal_A']} (diff 95% {b['diff_ci95']}), behavior {b['behavior']} (p {b['p']:.2g}), "
                      f"correct refusals {b['refusals_base']} -> {b['refusals_A']}, E2E {b['e2e_base']} -> {b['e2e_A']} of {b['n_answer']}")
        if "base_to_gate_only" in e:
            b = e["base_to_gate_only"]
            md.append(f"- base -> gate only: balanced {b['bal_base']} -> {b['bal_gate_only']} (diff 95% {b['diff_ci95']}), behavior {b['behavior']} (p {b['p']:.2g})")
        for f in ("A_correct_refusals_by_category", "A_new_correct_refusals_vs_base_by_category", "A_refusals_of_answer_questions_by_category"):
            if f in e:
                md.append(f"- {f}: {e[f]}")
        md.append("")
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a3_portal.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
