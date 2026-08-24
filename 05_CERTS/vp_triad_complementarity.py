#!/usr/bin/env python3
"""D0-TRIAD-COMPLEMENTARITY-001 — the trinary law invisible to pairwise checks.

STRUCTURE (THE, Lean D0.Core.TriadComplementarity, TRIAD CONSTRAINT):
  admissible triad record: r11+r22+r33 = 1 and
    det ≡ r11*r22*r33 + 2*r12*r23*r13 − r11*r23² − r22*r13² − r33*r12² ≥ 0.
  With ti = |pair opposite branch i|:
    THEOREM: a*b*c + 2*t1*t2*t3 ≥ a*t1² + b*t2² + c*t3²        (determinant face)
  Tightness: balanced coherent record (all entries 1/3) saturates exactly (det=0, pure).
  Pairwise collapse: summing the three 2×2 principal bounds yields only tr(rho²)≤1 —
  trivial. The cubic term is where genuine trinary content lives.

OPEN-GAP POSITION: for N≥3 paths the mainstream has no consensus tight trivariate
complementarity law; this derived necessary condition is a candidate answer, checkable on
existing multi-arm interferometry data (apparatus bridge as in DYAD-FRINGE-BRIDGE-001).

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 non-PSD triad violates the constraint (non-vacuity of the determinant face);
  C2 IRREDUCIBILITY TO PAIRS: a magnitude triple that passes ALL THREE 2×2 principal tests
     yet violates the trinary constraint — pairwise audits cannot replace the determinant;
  C3 balanced coherent must SATURATE (wave extremum sits on the face, not inside).
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-9


def det3(a, b, c, x12, x13, x23):
    return a * b * c + 2 * x12 * x23 * x13 - a * x23**2 - b * x13**2 - c * x12**2


def gap(a, b, c, t1, t2, t3):
    """lhs - rhs of the trinary constraint."""
    return a * b * c + 2 * t1 * t2 * t3 - a * t1**2 - b * t2**2 - c * t3**2


def random_psd3(rng, n):
    out = []
    while len(out) < n:
        X = rng.normal(size=(3, 7)) + 1j * rng.normal(size=(3, 7))
        rho = X @ X.conj().T
        tr = rho.trace().real
        if tr < 1e-12:
            continue
        out.append(rho / tr)
        if len(out) >= n:
            break
    return out


def main() -> int:
    print("=== D0-TRIAD-COMPLEMENTARITY-001  abc + 2·t1t2t3 ≥ a·t1²+b·t2²+c·t3² ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: unit closure + 3x3 determinant positivity; "
          "ti = coherence of pair OPPOSITE branch i; no quantum postulates")

    # ---- GATE 1: zero violations over dense random PSD ensemble --------------------------
    rng = np.random.default_rng(31)
    states = random_psd3(rng, 120_000)
    viol = 0
    worst = float("inf")
    for rho in states:
        a, b, c = rho[0, 0].real, rho[1, 1].real, rho[2, 2].real
        g = gap(a, b, c, abs(rho[1, 2]), abs(rho[0, 2]), abs(rho[0, 1]))
        worst = min(worst, g)
        if g < -1e-10:
            viol += 1
    assert viol == 0, f"{viol} violations found, worst gap {worst}"
    print(f"PASS_TRIAD_CONSTRAINT  {len(states)} PSD states: zero violations "
          f"(min gap {worst:.3e} ≥ 0)")

    # ---- GATE 2: saturation by the balanced coherent record -------------------------------
    a = b = c = 1 / 3
    t = 1 / 3
    assert abs(det3(a, b, c, t, t, t)) < TOL, "balanced coherent must be pure (det=0)"
    assert abs(gap(a, b, c, t, t, t)) < TOL, "balanced coherent must SATURATE the law"
    print(f"PASS_SATURATION  balanced coherent (all 1/3): det=0, gap=0 — wave extremum "
          f"sits exactly on the determinant face")

    # ---- CONTROL C1 (must fail): non-PSD triad breaks the constraint ----------------------
    # NOTE: for 3x3, det>=0 alone is NOT positivity (Sylvester needs all principal minors).
    # C1 uses a record failing BOTH a 2x2 minor and the trinary law:
    # diag(0.1,0.1,0.1) with t1=t2=0.3, t3=0:
    #   minor23: 0.01-0.09 < 0;  det = 0.001 - 0.009 - 0.009 < 0;  gap = 0.001 - 0.018 < 0.
    bad = dict(a=0.1, b=0.1, c=0.1, t1=0.3, t2=0.3, t3=0.0)
    d_bad = det3(bad["a"], bad["b"], bad["c"], bad["t3"], bad["t2"], bad["t1"])
    g_bad = gap(**bad)
    assert d_bad < -TOL, f"control matrix must be non-PSD: det={d_bad}"
    assert g_bad < -TOL, f"non-PSD must violate the constraint: gap={g_bad}"
    print(f"FAIL_NONPSD_TRIAD  diag(0.1,0.1,0.1), (t1,t2,t3)=(0.3,0.3,0): "
          f"minor23<0, det={d_bad:.4f}<0, gap={g_bad:.4f}<0 "
          f"(NB: det>=0 alone is not positivity — Sylvester is load-bearing)")

    # ---- CONTROL C2 (must fail): pairs pass, trinary law cuts -----------------------------
    # a=b=0.45, c=0.1; t1 and t2 sit AT their pairwise caps sqrt(b*c)=sqrt(a*c)=sqrt(0.045),
    # t3 = 0: every 2x2 principal test passes (two at the boundary), yet det < 0.
    a, b, c = 0.45, 0.45, 0.1
    cap1, cap2, cap3 = (b * c) ** 0.5, (a * c) ** 0.5, (a * b) ** 0.5
    t1 = cap1
    t2 = cap2
    t3 = 0.0
    assert t1 <= cap1 + TOL and t2 <= cap2 + TOL and t3 <= cap3 + TOL, \
        f"witness must respect every pairwise cap: ({cap1:.3f},{cap2:.3f},{cap3:.3f})"
    g_pair_ok = gap(a, b, c, t1, t2, t3)
    d_wit = det3(a, b, c, t3, t2, t1)
    assert d_wit < -TOL, f"C2 witness must be non-PSD: det={d_wit}"
    assert g_pair_ok < -TOL, f"C2 witness must violate the trinary law: gap={g_pair_ok}"
    print(f"FAIL_PAIRWISE_INSUFFICIENT  a={a},b={b},c={c} with "
          f"(t1,t2,t3)=({t1:.4f},{t2:.4f},{t3}): all 2×2 principal tests pass "
          f"(two AT the caps {cap1:.4f}/{cap2:.4f}), but det={d_wit:.6f}<0, "
          f"gap={g_pair_ok:.6f}<0 — trinary content is irreducible to pairs")

    # ---- M1/open-gap note ------------------------------------------------------------------
    print("OPEN_GAP_POSITION  N≥3-path complementarity has no consensus tight form in the "
          "mainstream; this derived determinant face is a candidate law, testable on "
          "multi-arm data via the apparatus bridge")
    print("HONEST_BOUNDARY  necessity = THE (Lean rc=0, 0 sorry); sufficiency-with-phases "
          "and possible experimentally tighter forms stay open targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
