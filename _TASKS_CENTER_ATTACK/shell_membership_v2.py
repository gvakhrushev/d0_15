#!/usr/bin/env python3
"""shell_membership_v2 - executes SHELL_MEMBERSHIP_PREREG_V2.md Q2 (+ null gate). DRAFT companion.

EXACT structure-matched null (prereg Q2a): excluded set fixed {6,7}; shared pair S in C(11,2);
A = S + 3 of remaining 9; C = S + 2 of remaining 6; B = last 4  ->  55*84*15 = 69300 assignments,
enumerated EXACTLY (no sampling). Frozen defs A={1,2,3,10,11} B={4,5,8,9} C={2,3,12,13} is one of
them (S={2,3}).
Implementation choices frozen here: mass-scramble gate (prereg "Null gate") uses per-draw
MC percentile with 500 null samples (exact 69300x200 would be ~42M fits); LOO uses the full exact
null per fold. Metric = mean over shells of circle-fit radial RMS (v1 metric, unchanged).
Line control: same enumerations with best-fit LINE residual RMS (np.polyfit deg=1).
"""
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PHI = (1 + 5 ** 0.5) / 2
DELTA0 = PHI - 1.5
LOG10_ME = math.log10(0.51099895)
FROZEN = {"A": [1, 2, 3, 10, 11], "B": [4, 5, 8, 9], "C": [2, 3, 12, 13]}
EXCLUDED = (6, 7)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


FIB_C = sorted({fib(n) for n in range(1, 13)})
BASIS = []
for n in range(-16, 17):
    for k in range(-16, 17):
        for rank, kappa in enumerate(FIB_C, start=1):
            BASIS.append((abs(n) + abs(k) + rank, abs(n), abs(k), kappa, n,
                          n * math.log10(2.0) + k * math.log10(PHI) + math.log10(kappa)))


def fit_n(l10):
    best = None
    for cplx, an, ak, kappa, n, pred in BASIS:
        key = (abs(l10 - pred), cplx, an, ak, kappa, n)
        if best is None or key < best[0]:
            best = (key, n)
    return best[1]


def load_masses():
    masses = {}
    for line in (ROOT / "08_PASSPORTS/PDG/data/mass_width_2025.mcd").read_text(
            encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("*"):
            continue
        toks = line.split()
        ids, m = [], None
        for t in toks:
            if m is None:
                try:
                    ids.append(abs(int(t)))
                    continue
                except ValueError:
                    pass
                try:
                    m = float(t)
                except ValueError:
                    break
        if m and m > 0:
            for pid in ids:
                masses.setdefault(pid, m * 1000.0)
    return masses


def build_nodes(mass_of_slot):
    """mass_of_slot: dict slot->mass(MeV) for slots 2..13 (+ slot1 gamma-node fixed)."""
    K_E = 2 ** 23 * (2 * math.pi) ** 3 * PHI ** (233 / 4.0)
    H_E = math.log10(K_E) / DELTA0
    nodes = {1: (0.0, 0.0)}
    for slot, m in mass_of_slot.items():
        l10 = math.log10(m)
        Hp = H_E + (l10 - LOG10_ME) / DELTA0
        nodes[slot] = (abs(float(fit_n(l10))), Hp % 13.0)
    ref = nodes[7][1]
    out = {}
    for slot, (na, h) in nodes.items():
        hu = h
        while hu - ref > 6.5:
            hu -= 13
        while hu - ref < -6.5:
            hu += 13
        out[slot] = (na, hu)
    return out


def circle_rms(P):
    x = P[:, 0]; y = P[:, 1]
    A = np.column_stack([2 * x, 2 * y, np.ones_like(x)])
    cx, cy, c = np.linalg.lstsq(A, x * x + y * y, rcond=None)[0]
    r = math.sqrt(max(0.0, cx * cx + cy * cy + c))
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    return float(np.sqrt(np.mean((d - r) ** 2)))


def line_rms(P):
    x = P[:, 0]; y = P[:, 1]
    if np.ptp(x) < 1e-12:
        return float(np.sqrt(np.mean((x - x.mean()) ** 2)))
    a, b = np.polyfit(x, y, 1)
    return float(np.sqrt(np.mean((y - (a * x + b)) ** 2) / (1 + a * a)))


def score(defs, nodes, fitfn, drop=None):
    tot = []
    for sids in defs:
        pts = np.array([nodes[s] for s in sids if s in nodes and s != drop])
        if len(pts) < 3:
            return None  # fold degenerate for this assignment
        tot.append(fitfn(pts))
    return float(np.mean(tot))


def all_assignments():
    pool = [s for s in range(1, 14) if s not in EXCLUDED]
    out = []
    for S in itertools.combinations(pool, 2):
        rest = [s for s in pool if s not in S]
        for Aex in itertools.combinations(rest, 3):
            rem = [s for s in rest if s not in Aex]
            for Cex in itertools.combinations(rem, 2):
                B = tuple(s for s in rem if s not in Cex)
                out.append((tuple(sorted(S + Aex)), B, tuple(sorted(S + Cex))))
    return out


def main() -> int:
    print("=== shell_membership_v2 — executing SHELL_MEMBERSHIP_PREREG_V2.md Q2 ===")
    masses = load_masses()
    core = [12, 5, 1, 15, 24, 13, 3, 4, 23, 11, 2, 6, 25]
    slot_mass = {i + 1: masses[p] for i, p in enumerate(core) if p in masses}
    slot_mass.pop(1, None)  # slot 1 = gamma node fixed at origin
    nodes = build_nodes(slot_mass)
    assigns = all_assignments()
    frozen = (tuple(sorted(FROZEN["A"])), tuple(FROZEN["B"]), tuple(sorted(FROZEN["C"])))
    assert frozen in assigns, "frozen defs must be in the enumerated null family"
    print(f"[null-family] exact enumeration: {len(assigns)} assignments (expected 69300)")

    # Q2a exact test (circles)
    sc = np.array([score(a, nodes, circle_rms) for a in assigns])
    s_frozen = score(frozen, nodes, circle_rms)
    p_exact = float(np.mean(sc <= s_frozen + 1e-15))
    print(f"[Q2a] frozen mean-RMS={s_frozen:.5f}; EXACT p = {p_exact:.6f} "
          f"({int(round(p_exact*len(assigns)))}/{len(assigns)} assignments <= frozen)")

    # Q2c line control
    sl = np.array([score(a, nodes, line_rms) for a in assigns])
    s_frozen_l = score(frozen, nodes, line_rms)
    p_line = float(np.mean(sl <= s_frozen_l + 1e-15))
    print(f"[Q2c] LINE control: frozen={s_frozen_l:.5f}; exact p = {p_line:.6f} "
          f"(if similar to Q2a, circle-ness carries no extra content)")

    # Q2b LOO stability (drop each slot; degenerate folds -> assignment skipped)
    loo_pass = 0
    for drop in range(1, 14):
        svals = []
        for a in assigns:
            v = score(a, nodes, circle_rms, drop=drop)
            if v is not None:
                svals.append(v)
        v_f = score(frozen, nodes, circle_rms, drop=drop)
        if v_f is None:
            continue
        pct = float(np.mean(np.array(svals) <= v_f + 1e-15))
        ok = pct <= 0.05
        loo_pass += ok
        print(f"[Q2b] LOO drop slot {drop:2d}: frozen percentile p={pct:.4f} {'OK' if ok else 'FAIL'}")
    print(f"[Q2b] LOO: {loo_pass}/13 folds keep frozen at p<=0.05 (criterion >= 11)")

    # Null gate: mass-scramble (labels permuted among slots 2..13), 200 draws, 500-sample MC each
    rng = np.random.default_rng(20260704)
    slots = sorted(slot_mass)
    vals = [slot_mass[s] for s in slots]
    fired = 0
    idx_pool = np.arange(len(assigns))
    for _ in range(200):
        perm = rng.permutation(vals)
        nod = build_nodes(dict(zip(slots, perm)))
        s_f = score(frozen, nod, circle_rms)
        sample = [score(assigns[i], nod, circle_rms) for i in rng.choice(idx_pool, 500, replace=False)]
        if np.mean(np.array(sample) <= s_f + 1e-15) <= 0.01:
            fired += 1
    gate_ok = fired <= 10
    print(f"[gate] mass-scramble: frozen 'won' (p<=0.01) on {fired}/200 label-permuted draws "
          f"(must be <=5%: {'PASS' if gate_ok else 'FAIL'})")

    confirmed = (p_exact <= 0.01) and (loo_pass >= 11) and gate_ok
    verdict = {"p_exact": p_exact, "p_line": p_line, "loo_pass": loo_pass,
               "gate_fired": fired, "gate_ok": gate_ok,
               "verdict": "membership-signal-confirmed (pre-registered)" if confirmed else "not-confirmed"}
    (ROOT / "_TASKS_CENTER_ATTACK" / "shell_membership_v2.results.json").write_text(
        json.dumps(verdict, indent=1))
    print("verdict:", json.dumps(verdict))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
