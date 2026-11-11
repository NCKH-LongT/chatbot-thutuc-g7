"""A1. Paired effect sizes, intervals and minimum detectable effects for EVERY comparison the revised paper mentions.

Inputs (read-only): Code/eval/hard/results/{test,test_v4}/*.json (per-question rows), results/paired_stats.json (for a
reproduction check). Nothing is rerun. Output: out/a1_paired_all.json and out/a1_paired_all.md.

Per comparison X -> Y on the same questions:
  * balanced accuracy (2-class: mean of answer recall and refuse recall) difference, paired bootstrap 95% and 90% percentile intervals
    (4,000 resamples of questions, SEED 20261027, same resampling stream and quantile convention as eval/hard/paired_stats.py, so the
    95% intervals reproduce paired_stats.json exactly where the pair exists there);
  * behavior accuracy (3-way) difference, E2E accuracy difference (on answer questions), answer-recall and refuse-recall differences,
    each with paired bootstrap 95% intervals from the same resamples;
  * exact two-sided McNemar p on behavior and on E2E, and the conditional odds ratio gains/losses with exact (Clopper-Pearson) 95% CI;
  * MDE (80% power, two-sided alpha 0.05): balanced accuracy ~ 2.8 x bootstrap SD of the difference; E2E proportion via Connor (1987)
    formula using the observed discordant proportion among answer questions;
  * equivalence-style reading: the smallest symmetric margin m such that the 90% bootstrap interval lies inside (-m, +m)
    (TOST at alpha 0.05 would declare equivalence for any margin >= m).
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (B, RES, SEED, T1, T2, NAMES, bal, cond_or_ci, correct, dump, e2e, fmt_p, load_rows, mcnemar_exact, pct)  # noqa: E402

Z975, Z80 = 1.959964, 0.841621


def always_refuse(R):
    return {i: {**r, "got": "apologize", "top1": False} for i, r in R.items()}


def clar_to_refuse(R):
    return {i: ({**r, "got": "apologize"} if r["got"] == "clarify" else r) for i, r in R.items()}


def wstats(R, w):
    """All weighted statistics for one configuration under bootstrap weights w."""
    na = sum(k for i, k in w.items() if R[i]["beh"] == "answer")
    nr = sum(k for i, k in w.items() if R[i]["beh"] == "apologize")
    n = sum(w.values())
    ra = sum(k for i, k in w.items() if R[i]["beh"] == "answer" and R[i]["got"] == "answer") / na if na else None
    rr = sum(k for i, k in w.items() if R[i]["beh"] == "apologize" and R[i]["got"] == "apologize") / nr if nr else None
    return {"bal": (ra + rr) / 2 if na and nr else None, "beh": sum(k for i, k in w.items() if correct(R[i])) / n,
            "e2e": sum(k for i, k in w.items() if e2e(R[i])) / na if na else None, "rec_answer": ra, "rec_refuse": rr}


def connor_mde(n, psi):
    """Smallest |delta| detectable with 80% power by McNemar (Connor 1987): n = (z_a sqrt(psi) + z_b sqrt(psi - d^2))^2 / d^2."""
    if psi <= 0:
        return None
    lo, hi = 1e-6, psi
    f = lambda d: (Z975 * math.sqrt(psi) + Z80 * math.sqrt(max(psi - d * d, 0))) ** 2 / (d * d) - n
    if f(hi) > 0:
        return None            # not detectable at any delta <= psi
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return hi


_WCACHE = {}


def weights(ids):
    """B x n multiplicity matrix, drawn with the SAME Python RNG stream as paired_stats.py (rnd.choice(ids) n times per resample)."""
    import numpy as np
    key = tuple(ids)
    if key not in _WCACHE:
        rnd = random.Random(SEED)
        pos = {i: j for j, i in enumerate(ids)}
        W = np.zeros((B, len(ids)), dtype=np.int32)
        for b in range(B):
            for _ in ids:
                W[b, pos[rnd.choice(ids)]] += 1
        _WCACHE[key] = W
    return _WCACHE[key]


def vecstats(R, ids, W):
    import numpy as np
    isA = np.array([R[i]["beh"] == "answer" for i in ids], float)
    isR = np.array([R[i]["beh"] == "apologize" for i in ids], float)
    okA = np.array([R[i]["beh"] == "answer" and R[i]["got"] == "answer" for i in ids], float)
    okR = np.array([R[i]["beh"] == "apologize" and R[i]["got"] == "apologize" for i in ids], float)
    ok = np.array([correct(R[i]) for i in ids], float)
    ee = np.array([e2e(R[i]) for i in ids], float)
    na, nr, n = W @ isA, W @ isR, W.sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        ra, rr = (W @ okA) / na, (W @ okR) / nr
        return {"bal": (ra + rr) / 2, "beh": (W @ ok) / n, "e2e": (W @ ee) / na, "rec_answer": ra, "rec_refuse": rr}, (na > 0) & (nr > 0)


def compare(X, Y):
    import numpy as np
    ids = sorted(X)
    one = {i: 1 for i in ids}
    sx, sy = wstats(X, one), wstats(Y, one)
    W = weights(ids)
    keys = ("bal", "beh", "e2e", "rec_answer", "rec_refuse")
    u, okx = vecstats(X, ids, W)
    v, oky = vecstats(Y, ids, W)
    m = okx & oky
    ds = {k: list((v[k] - u[k])[m]) for k in keys}
    out = {}
    for k in keys:
        d = sorted(ds[k])
        m = sum(d) / len(d)
        sd = math.sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        lo90, hi90 = pct(d, 0.05), pct(d, 0.95)
        out[k] = {"x": round(sx[k], 4), "y": round(sy[k], 4), "diff": round(sy[k] - sx[k], 4),
                  "ci95": [round(pct(d, 0.025), 3), round(pct(d, 0.975), 3)], "ci90": [round(lo90, 3), round(hi90, 3)],
                  "boot_sd": round(sd, 4), "equiv_margin_90": round(max(abs(lo90), abs(hi90)), 3)}
    out["bal"]["mde80_approx"] = round(2.8 * out["bal"]["boot_sd"], 3)
    bx = {i: correct(X[i]) for i in ids}
    by = {i: correct(Y[i]) for i in ids}
    g = sum(by[i] and not bx[i] for i in ids)
    l = sum(bx[i] and not by[i] for i in ids)
    eg = sum(e2e(Y[i]) and not e2e(X[i]) for i in ids)
    el = sum(e2e(X[i]) and not e2e(Y[i]) for i in ids)
    na = sum(X[i]["beh"] == "answer" for i in ids)
    orb = cond_or_ci(l, g)
    ore = cond_or_ci(el, eg)
    out["behavior_mcnemar"] = {"gain": g, "loss": l, "p": mcnemar_exact(g, l), "p_fmt": fmt_p(mcnemar_exact(g, l)),
                               "or_gain_loss": None if orb[0] is None else [round(orb[0], 2), round(orb[1], 2), round(orb[2], 2)],
                               "mde80_prop": (lambda v: None if v is None else round(v, 3))(connor_mde(len(ids), (g + l) / len(ids)))}
    out["e2e_mcnemar"] = {"x": sum(e2e(X[i]) for i in ids), "y": sum(e2e(Y[i]) for i in ids), "n_answer": na, "gain": eg, "loss": el,
                          "p": mcnemar_exact(eg, el), "p_fmt": fmt_p(mcnemar_exact(eg, el)),
                          "or_gain_loss": None if ore[0] is None else [round(ore[0], 2), round(ore[1], 2), round(ore[2], 2)],
                          "mde80_prop": (lambda v: None if v is None else round(v, 3))(connor_mde(na, (eg + el) / na)) if (eg + el) else None}
    out["n"] = len(ids)
    return out


PAIRS = {
    "t1": [("off", "A"), ("A", "AB"), ("A", "C"), ("A", "AC"), ("A", "ACname"), ("A", "R"), ("A", "R_c2r"), ("AR", "R"), ("AR", "R_c2r"),
           ("off", "B"), ("off", "C"), ("off", "gate_only"), ("gate_only", "A"), ("gate_only", "L_nb"), ("gate_only", "L_emb"),
           ("A", "L_nb"), ("A", "L_emb"), ("off", "L_nb"), ("off", "L_emb"),
           ("A", "no_gate"), ("A", "no_lex"), ("A", "no_focus"), ("A", "no_strip"), ("A", "no_weak"), ("A", "no_org"), ("AR", "off")],
    "t2": [("off", "A"), ("A", "A2B"), ("AB", "A2B"), ("off", "A2B"), ("A", "AB"), ("A2B", "R"), ("A", "R"), ("A2B", "R_c2r"), ("AR", "R"),
           ("AR", "R_c2r"), ("off", "gate_only"), ("gate_only", "A"), ("gate_only", "L_nb"), ("gate_only", "L_emb"), ("A", "L_nb"),
           ("A", "L_emb"), ("off", "L_nb"), ("off", "L_emb"),
           ("A", "no_gate"), ("A", "no_lex"), ("A", "no_focus"), ("A", "no_strip"), ("A", "no_weak"), ("A", "no_org"), ("AR", "off")],
}


def configs(files):
    C = {k: load_rows(v) for k, v in files.items()}
    C["AR"] = always_refuse(C["off"])
    C["R_c2r"] = clar_to_refuse(C["R"])
    return C


def main():
    res = {}
    check = json.load(open(os.path.join(RES, "paired_stats.json"), encoding="utf-8"))
    pmap = {"t1": "real_v2", "t2": "real_v4"}
    fmap = {"AB": {"t1": "final", "t2": "AB"}, "A2B": {"t2": "R2final"}, "R": {"t1": "rag4b", "t2": "rag4b"},
            "L_nb": {"t1": "learned_gate", "t2": "learned_gate"}, "L_emb": {"t1": "learned_gate_emb", "t2": "learned_gate_emb"},
            "gate_only": {"t1": "abl_gate_only", "t2": "abl_gate_only"}}
    repro = []
    for t, files in (("t1", T1), ("t2", T2)):
        C = configs(files)
        for x, y in PAIRS[t]:
            r = compare(C[x], C[y])
            key = f"{t} {x} -> {y}"
            res[key] = r
            # reproduction check against paired_stats.json
            fx, fy = fmap.get(x, {}).get(t, x), fmap.get(y, {}).get(t, y)
            ck = f"{pmap[t]} {fx} -> {fy}"
            if ck in check:
                c = check[ck]
                ok = (tuple(c["ci95"]) == tuple(r["bal"]["ci95"]) and c["behavior"] == f"+{r['behavior_mcnemar']['gain']}/-{r['behavior_mcnemar']['loss']}"
                      and c["e2e_change"] == f"+{r['e2e_mcnemar']['gain']}/-{r['e2e_mcnemar']['loss']}")
                repro.append({"pair": ck, "reproduced": ok, "paired_stats_ci95": c["ci95"], "a1_ci95": r["bal"]["ci95"]})
    res["_reproduction_check_vs_paired_stats_json"] = repro
    dump("a1_paired_all.json", res)

    L = ["# A1 - paired comparisons (all comparisons mentioned in the revised text)", "",
         "Source: per-question rows in Code/eval/hard/results/{test,test_v4}; script analysis/a1_paired_all.py. "
         "AR = always refuse (constructed from the labels); R_c2r = R with its clarifications counted as refusals. "
         "Bal = 2-class balanced accuracy. Intervals: paired bootstrap percentile, 4,000 resamples, seed 20261027. "
         "Equiv. margin = smallest m with the 90% interval inside (-m, m). MDE80 = minimum detectable effect at 80% power.", "",
         f"Reproduction of paired_stats.json: {sum(r['reproduced'] for r in repro)}/{len(repro)} pairs identical.", "",
         "| Set | X -> Y | Bal X->Y | dBal [95%] | dBal 90% | equiv. m | MDE80 bal | Beh +/- (p) | dBeh [95%] | E2E X->Y /n (+/-, p) | dE2E [95%] | MDE80 E2E | dAnsRec [95%] | dRefRec [95%] |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, r in res.items():
        if k.startswith("_"):
            continue
        t, rest = k.split(" ", 1)
        b, m, e = r["bal"], r["behavior_mcnemar"], r["e2e_mcnemar"]
        L.append(f"| {t.upper()} | {rest} | {b['x']:.3f}->{b['y']:.3f} | {b['diff']:+.3f} [{b['ci95'][0]:+.3f}, {b['ci95'][1]:+.3f}] | "
                 f"[{b['ci90'][0]:+.3f}, {b['ci90'][1]:+.3f}] | {b['equiv_margin_90']:.3f} | {b['mde80_approx']:.3f} | "
                 f"+{m['gain']}/-{m['loss']} ({m['p_fmt']}) | {r['beh']['diff']:+.3f} [{r['beh']['ci95'][0]:+.3f}, {r['beh']['ci95'][1]:+.3f}] | "
                 f"{e['x']}->{e['y']}/{e['n_answer']} (+{e['gain']}/-{e['loss']}, {e['p_fmt']}) | {r['e2e']['diff']:+.3f} [{r['e2e']['ci95'][0]:+.3f}, {r['e2e']['ci95'][1]:+.3f}] | "
                 f"{e['mde80_prop'] if e['mde80_prop'] is not None else 'n/a'} | "
                 f"{r['rec_answer']['diff']:+.3f} [{r['rec_answer']['ci95'][0]:+.3f}, {r['rec_answer']['ci95'][1]:+.3f}] | "
                 f"{r['rec_refuse']['diff']:+.3f} [{r['rec_refuse']['ci95'][0]:+.3f}, {r['rec_refuse']['ci95'][1]:+.3f}] |")
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "a1_paired_all.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[:8]))
    for r in repro:
        print(r)


if __name__ == "__main__":
    main()
