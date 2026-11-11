"""Shared helpers for the analyses that recompute the paper's tables and statistics.

Reads ONLY committed per-question result files and label files under Code/.
Never runs a system. Outputs go to ./out/ next to this file.
Run each script with:  python -I -X utf8 <script>.py
"""
from __future__ import annotations

import json
import math
import os
import random
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Code/ = parent of analysis/
RES = os.path.join(ROOT, "eval", "hard", "results")
LABELS = os.path.join(ROOT, "labels")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

SEED, B = 20261027, 4000          # same seed / resamples as eval/hard/paired_stats.py

# configuration key -> result file (relative to RES)
T1 = {
    "off": "test/real_v2_off.json", "A": "test/real_v2_A.json", "B": "test/real_v2_B.json", "C": "test/real_v2_C.json",
    "AC": "test/real_v2_AC.json", "ACname": "test/real_v2_ACname.json", "AB": "test/real_v2_final.json",
    "R": "test/real_v2_rag4b.json", "L_nb": "test/real_v2_learned_gate.json", "L_emb": "test/real_v2_learned_gate_emb.json",
    "gate_only": "test/real_v2_abl_gate_only.json", "no_gate": "test/real_v2_abl_no_gate.json", "no_lex": "test/real_v2_abl_no_lex.json",
    "no_focus": "test/real_v2_abl_no_focus.json", "no_strip": "test/real_v2_abl_no_strip.json", "no_weak": "test/real_v2_abl_no_weak.json",
    "no_org": "test/real_v2_abl_no_org.json",
}
T2 = {
    "off": "test_v4/real_v4_off.json", "A": "test_v4/real_v4_A.json", "AB": "test_v4/real_v4_AB.json", "A2B": "test_v4/real_v4_R2final.json",
    "R": "test_v4/real_v4_rag4b.json", "L_nb": "test_v4/real_v4_learned_gate.json", "L_emb": "test_v4/real_v4_learned_gate_emb.json",
    "gate_only": "test_v4/real_v4_abl_gate_only.json", "no_gate": "test_v4/real_v4_abl_no_gate.json", "no_lex": "test_v4/real_v4_abl_no_lex.json",
    "no_focus": "test_v4/real_v4_abl_no_focus.json", "no_strip": "test_v4/real_v4_abl_no_strip.json", "no_weak": "test_v4/real_v4_abl_no_weak.json",
    "no_org": "test_v4/real_v4_abl_no_org.json",
}
DEV = {"off": "dev/dev_off.json", "A": "dev/dev_A.json"}
NAMES = {"off": "Base", "A": "A (rule layer)", "B": "B (reranker alone)", "C": "C (LLM reader alone)", "AC": "A + C (intent, name)",
         "ACname": "A + C (name only)", "AB": "A + B", "A2B": "A2 + B", "R": "R (RAG, LLM decides)", "L_nb": "L: naive Bayes gate",
         "L_emb": "L: embedding gate", "gate_only": "Gate only", "no_gate": "A without gate", "no_lex": "A without lexicon",
         "no_focus": "A without focus", "no_strip": "A without letter stripping", "no_weak": "A without weak-name filter",
         "no_org": "A without organization default"}
LABEL_FILES = {"dev": "dev_real_v1.jsonl", "t1": "test1_real_v2.jsonl", "t2": "test2_real_v4.jsonl"}
PORTAL = {"hf:doanhieung/vn-mps-public-service-qa": "MPS", "hf:hieunguyen1053/dichvucong_faqs/hoi-dap": "BinhDinh"}


def load_rows(rel: str) -> dict:
    d = json.load(open(os.path.join(RES, rel), encoding="utf-8"))
    rows = d["rows"] if isinstance(d, dict) else d
    return {r["id"]: r for r in rows}


def load_labels(which: str) -> dict:
    out = {}
    for line in open(os.path.join(LABELS, LABEL_FILES[which]), encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            r["portal"] = PORTAL[r["source"].split("#")[0]]
            out[r["id"]] = r
    return out


def correct(r) -> bool:                 # behavior correct (3-way)
    return r["got"] == r["beh"]


def e2e(r) -> bool:                     # answer question answered with a correct first procedure
    return r["beh"] == "answer" and r["got"] == "answer" and bool(r["top1"])


def bal(R: dict, w: dict):
    """Two-class balanced accuracy = (answer recall + refuse recall) / 2; w = multiplicity of each id (bootstrap)."""
    na = sum(k for i, k in w.items() if R[i]["beh"] == "answer")
    nr = sum(k for i, k in w.items() if R[i]["beh"] == "apologize")
    if not na or not nr:
        return None
    return (sum(k for i, k in w.items() if R[i]["beh"] == "answer" and R[i]["got"] == "answer") / na
            + sum(k for i, k in w.items() if R[i]["beh"] == "apologize" and R[i]["got"] == "apologize") / nr) / 2


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    return 1.0 if n == 0 else min(1.0, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)


def wilson(k: int, n: int, z: float = 1.959964):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def newcombe10(a: int, b: int, c: int, d: int, z: float = 1.959964):
    """Paired 2x2: a = both correct, b = X correct only, c = Y correct only, d = neither. Returns (delta, lo, hi) for p_Y - p_X.
    Newcombe RG (1998) Stat Med 17:2635-2650, method 10 (score-based, with phi correction)."""
    n = a + b + c + d
    p1 = (a + b) / n            # X
    p2 = (a + c) / n            # Y
    l1, u1 = wilson(a + b, n, z)
    l2, u2 = wilson(a + c, n, z)
    delta = p2 - p1
    # phi
    denom = (a + b) * (c + d) * (a + c) * (b + d)
    if denom == 0:
        phi = 0.0
    else:
        num = a * d - b * c
        # continuity-corrected phi as in Newcombe: max(|ad-bc| - n/2, 0) with sign
        if num > n / 2:
            num = num - n / 2
        elif num >= 0:
            num = 0.0
        phi = num / math.sqrt(denom)
    dl = math.sqrt(max(0.0, (p2 - l2) ** 2 - 2 * phi * (p2 - l2) * (u1 - p1) + (u1 - p1) ** 2))
    du = math.sqrt(max(0.0, (u2 - p2) ** 2 - 2 * phi * (u2 - p2) * (p1 - l1) + (p1 - l1) ** 2))
    return delta, delta - dl, delta + du


def cond_or_ci(b: int, c: int, alpha: float = 0.05):
    """Conditional (McNemar) odds ratio c/b (gains/losses) with exact Clopper-Pearson CI on c/(b+c)."""
    from scipy.stats import beta
    n = b + c
    if n == 0:
        return None, None, None
    k = c
    lo = 0.0 if k == 0 else beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - alpha / 2, k + 1, n - k)
    f = lambda p: (p / (1 - p)) if p < 1 else float("inf")
    est = (c / b) if b else float("inf")
    return est, f(lo), f(hi)


def boot_diffs(X: dict, Y: dict, stat=bal, seed=SEED, nboot=B):
    ids = sorted(X)
    rnd = random.Random(seed)
    ds = []
    for _ in range(nboot):
        w = {}
        for _ in ids:
            i = rnd.choice(ids)
            w[i] = w.get(i, 0) + 1
        u, v = stat(X, w), stat(Y, w)
        if u is not None and v is not None:
            ds.append(v - u)
    ds.sort()
    return ds


def pct(ds, q):
    """Same quantile convention as eval/hard/paired_stats.py (lower: int(q*n); upper: int(q*n)-1)."""
    n = len(ds)
    return ds[int(q * n)] if q < 0.5 else ds[int(q * n) - 1]


def fmt_p(p: float) -> str:
    """ONE rounding rule for every p-value in the paper (proposed): p >= 0.001 -> three decimals, half-up on the exact value;
    p < 0.001 -> one significant digit in scientific notation (e.g. 9e-19)."""
    if p >= 0.001:
        from decimal import Decimal, ROUND_HALF_UP
        return str(Decimal(repr(p)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))
    m, e = f"{p:.0e}".split("e")
    return f"{m}e{int(e)}"


def dump(name: str, obj) -> str:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return path
