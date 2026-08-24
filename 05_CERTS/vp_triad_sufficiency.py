#!/usr/bin/env python3
"""D0-TRIAD-SUFFICIENCY-001 — the magnitude region is EXACTLY (caps ∧ determinant face).

STRUCTURE (THE, Lean D0.Core.TriadSufficiency, TRIAD_MAGNITUDE_CHARACTERIZATION_PROVED):
  * SUFFICIENCY (constructive): magnitudes (a,b,c;t1,t2,t3) with unit closure, pairwise caps
    t1²≤bc, t2²≤ac, t3²≤ab, and the trinary law abc+2·t1t2t3 ≥ a·t1²+b·t2²+c·t3² are
    REALIZED by the aligned-phase record (r12,t3),(r13,t2),(r23,t1): every principal minor
    is a cap, and the determinant IS the face gap.
  * NECESSITY: every admissible record yields caps (Sylvester minors) and the face
    (triad_constraint).
  => CAPSTONE: realizability ⟺ caps ∧ face. The admissible magnitude region of the triad is
     completely described — pairwise caps + one trinary law, nothing hidden.

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 face-failing but cap-passing witness must realize NON-PSD — face is load-bearing;
  C2 cap-failing but face-passing witness must realize NON-PSD — caps are load-bearing.
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-9


def face_gap(a, b, c, t1, t2, t3):
    return a * b * c + 2 * t1 * t2 * t3 - a * t1**2 - b * t2**2 - c * t3**2


def aligned_matrix(a, b, c, t1, t2, t3):
    return np.array([[a, t3, t2], [t3, b, t1], [t2, t1, c]], dtype=float)


def min_eig(M):
    return float(np.linalg.eigvalsh(M).min())


def main() -> int:
    print("=== D0-TRIAD-SUFFICIENCY-001  realizability ⟺ caps ∧ face ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: unit closure; caps=Sylvester minors; "
          "face=trinary law; realization=aligned phases (+t_i)")

    rng = np.random.default_rng(77)

    # ---- GATE 1: constructive sufficiency over random admissible magnitudes ---------------
    n_ok = 0
    worst_eig = float("inf")
    for _ in range(40000):
        x = rng.dirichlet((1.0, 1.0, 1.0))
        a, b, c = map(float, x)
        c1, c2, c3 = (b * c) ** 0.5, (a * c) ** 0.5, (a * b) ** 0.5
        t1 = float(rng.uniform(0, c1))
        t2 = float(rng.uniform(0, c2))
        t3 = float(rng.uniform(0, c3))
        if face_gap(a, b, c, t1, t2, t3) < 0:   # keep only face-respecting points
            continue
        M = aligned_matrix(a, b, c, t1, t2, t3)
        me = min_eig(M)
        worst_eig = min(worst_eig, me)
        assert me >= -1e-10, f"aligned realization NOT PSD: min-eig {me} at {(a,b,c,t1,t2,t3)}"
        n_ok += 1
        if n_ok >= 8000:
            break
    print(f"PASS_SUFFICIENCY_CONSTRUCTIVE  {n_ok} aligned realizations all PSD "
          f"(worst min-eig {worst_eig:.3e})")

    # ---- GATE 2 + 3: exactness — predicate and realization agree everywhere ---------------
    tested = 0
    diverged = 0
    for _ in range(60000):
        x = rng.dirichlet((1.0, 1.0, 1.0))
        a, b, c = map(float, x)
        c1, c2, c3 = (b * c) ** 0.5, (a * c) ** 0.5, (a * b) ** 0.5
        t1 = float(rng.uniform(0, c1))
        t2 = float(rng.uniform(0, c2))
        t3 = float(rng.uniform(0, c3))
        pred_caps = t1**2 <= b * c + TOL and t2**2 <= a * c + TOL and t3**2 <= a * b + TOL
        pred_face = face_gap(a, b, c, t1, t2, t3) >= -TOL
        pred = pred_caps and pred_face
        real = min_eig(aligned_matrix(a, b, c, t1, t2, t3)) >= -TOL
        tested += 1
        if pred != real:
            diverged += 1
            if diverged <= 3:
                print(f"  divergence at {(a,b,c,t1,t2,t3)}: pred={pred} real={real}")
    assert tested > 30000
    assert diverged == 0, f"{diverged}/{tested} classification divergences"
    print(f"PASS_EXACTNESS  {tested} magnitude points: predicate(caps∧face) ≡ "
          f"realized-PSD — zero divergences, region fully described")

    # ---- CONTROL C1 (must fail): face failing, caps passing -------------------------------
    a, b, c = 0.45, 0.45, 0.1
    t1, t2, t3 = (b * c) ** 0.5, (a * c) ** 0.5, 0.0
    assert t1**2 <= b * c + TOL and t2**2 <= a * c + TOL and t3**2 <= a * b + TOL
    g = face_gap(a, b, c, t1, t2, t3)
    assert g < -TOL, f"witness must fail the face: {g}"
    me = min_eig(aligned_matrix(a, b, c, t1, t2, t3))
    assert me < -TOL, f"realization must be non-PSD: {me}"
    print(f"FAIL_FACE_LOAD_BEARING  caps pass but gap={g:.6f}<0 → min-eig={me:.6f}<0")

    # ---- CONTROL C2 (must fail): caps failing, face passing --------------------------------
    a = b = c = 0.1
    t1 = t2 = t3 = 0.3
    g = face_gap(a, b, c, t1, t2, t3)
    assert g >= -TOL, f"witness must pass the face: {g}"
    caps_ok = t1**2 <= b * c + TOL and t2**2 <= a * c + TOL and t3**2 <= a * b + TOL
    assert not caps_ok, f"witness must fail the caps"
    me = min_eig(aligned_matrix(a, b, c, t1, t2, t3))
    assert me < -TOL, f"realization must be non-PSD: {me}"
    print(f"FAIL_CAPS_LOAD_BEARING  face passes (gap={g:.6f}≥0) but caps fail → "
          f"min-eig={me:.6f}<0 — both hypotheses independently necessary")

    print("HONEST_BOUNDARY  real-symmetric records THE (Lean rc=0, 0 sorry); complex-"
          "Hermitian analogue (continuous phase parameter) queued; apparatus bridge inherited")
    return 0


if __name__ == "__main__":
    sys.exit(main())
