#!/usr/bin/env python3
"""D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001 — colour SU(3) is not source-derived on the
scene/terminal carriers; the tempting "three zones = colour" is the GENERATION algebra, not colour.

Two exact finite obstructions (migrated from the session matter-sector analysis, consolidated):

(A) TYPED COLLAPSE (scene-zone carrier ℂ³³, algebra ⟨Aut K, D_zone⟩).
    The raw commutant on the three zone-lines is the full matrix algebra M₃(ℂ), dim 9. But the typed
    degree operator D_zone = diag(24,22,20) has a SIMPLE (distinct-eigenvalue) spectrum on the zone-line
    triple, so its commutant inside M₃(ℂ) is the DIAGONAL algebra ℂ³ (dim 3) — abelian. Hence the raw M₃
    is DESTROYED by D_zone: the three zone-lines are the abelian GENERATION lines (3 families), NOT an
    unbroken non-abelian colour. "baryon = 3 quarks = rank-3 = three zones = colour" fails on this carrier.

(B) COMMUTANT GAP (terminal spinor carrier ℂ⁸ = ℂ[Q₈], Ω₈ ≅ Q₈).
    A source-native colour M₃ would have to commute with the source weak action, i.e. lie in
    Commutant(weak). On the frozen terminal ℂ⁸ the commutant of the (left-regular) weak algebra is the
    right-regular algebra R(Q₈), of dim 8 < 9 = dim M₃(ℂ). No 9-dimensional M₃ fits: the joint quark
    gauge module ℂ³⊗ℂ² requires an EXTERNAL ⊗ℂ³ (the inserted 𝒜_F completion ℋ_q = W₃⊗V₂), not source-derived.

Scope (honest, not overstated): NO-GO-CLOSED on the scene-zone and terminal carriers — the most tempting
false candidate is removed. It does NOT classify colour on H_edge / P·Q feedback globally; global colour
embedding remains a terminal-passport (octonion/E8) route, unclassified as scene-native. This is exactly
the corpus position (BOOK_04 §04.11: scene cannot geometrically derive the SM root/Weyl structure).
"""
from __future__ import annotations

import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def commutant_dim(mats):
    """dim of {X : X M = M X for all M in mats} on C^n, over the reals of a complex solve."""
    n = mats[0].shape[0]
    rows = []
    I = np.eye(n)
    for M in mats:
        # vec([X,M]) = (I⊗M^T - M⊗I) vec(X) = 0  (row-major kron convention)
        rows.append(np.kron(I, M.T) - np.kron(M, I))
    A = np.vstack(rows)
    # nullity via SVD rank
    s = np.linalg.svd(A, compute_uv=False)
    tol = max(A.shape) * (s[0] if s.size else 1.0) * 1e-10
    rank = int((s > tol).sum())
    return n * n - rank


def q8_left_regular():
    # Q8 = {0:+1,1:-1,2:+i,3:-i,4:+j,5:-j,6:+k,7:-k}; build Cayley table then left-regular perms.
    names = ["+1", "-1", "+i", "-i", "+j", "-j", "+k", "-k"]
    idx = {nm: a for a, nm in enumerate(names)}
    # quaternion multiplication on {1,i,j,k} with signs
    base = {("1", "1"): ("1", 1), ("1", "i"): ("i", 1), ("1", "j"): ("j", 1), ("1", "k"): ("k", 1),
            ("i", "1"): ("i", 1), ("i", "i"): ("1", -1), ("i", "j"): ("k", 1), ("i", "k"): ("j", -1),
            ("j", "1"): ("j", 1), ("j", "i"): ("k", -1), ("j", "j"): ("1", -1), ("j", "k"): ("i", 1),
            ("k", "1"): ("k", 1), ("k", "i"): ("j", 1), ("k", "j"): ("i", -1), ("k", "k"): ("1", -1)}

    def mul(a, b):
        sa, la = (1, a[1:]) if a[0] == "+" else (-1, a[1:])
        sb, lb = (1, b[1:]) if b[0] == "+" else (-1, b[1:])
        core, sc = base[(la, lb)]
        s = sa * sb * sc
        return ("+" if s > 0 else "-") + core

    L = []
    for g in names:
        M = np.zeros((8, 8))
        for h in names:
            M[idx[mul(g, h)], idx[h]] = 1.0
        L.append(M)
    return L


def main() -> int:
    print("=== D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001 ===")

    # ---- (A) typed collapse: D_zone destroys raw M3 -> abelian C^3 --------------------------
    Dz = np.diag([24.0, 22.0, 20.0])            # degree frame on the three zone-lines
    raw_M3 = commutant_dim([np.eye(3)])          # commutant of scalars = full M3 (raw) = 9
    typed = commutant_dim([Dz])                  # commutant of D_zone (distinct evals) = diagonal = 3
    print(f"[A] raw commutant on zone-lines = M3(C), dim = {raw_M3}")
    print(f"[A] typed commutant with D_zone=diag(24,22,20), dim = {typed}  (diagonal = abelian generations)")
    assert raw_M3 == 9, "raw commutant must be the full M3 (dim 9)"
    assert typed == 3, "D_zone with distinct eigenvalues must collapse M3 to the 3-dim diagonal"
    print("PASS_TYPED_COLLAPSE  raw M3 (9) -> typed abelian C^3 (3): three zones = GENERATIONS, not colour")

    # control: a degenerate degree frame does NOT collapse (distinctness is load-bearing)
    Dz_deg = np.diag([24.0, 24.0, 20.0])
    typed_deg = commutant_dim([Dz_deg])
    assert typed_deg > 3, "control: a repeated eigenvalue must leave a non-abelian block (dim>3)"
    print(f"FAIL_DEGENERATE_FRAME_WOULD_KEEP_BLOCK  diag(24,24,20) commutant dim = {typed_deg} (>3): "
          "the +2 zone increment (distinct degrees) is what forbids colour")

    # ---- (B) Q8 commutant gap: dim Comm(weak) = dim R(Q8) = 8 < 9 = dim M3 ------------------
    L = q8_left_regular()
    comm = commutant_dim(L)                      # commutant of left-regular algebra = right-regular = 8
    print(f"[B] dim Commutant(weak) on C^8=C[Q8] = dim R(Q8) = {comm}")
    assert comm == 8, "commutant of the Q8 left-regular algebra must be the 8-dim right-regular algebra"
    assert comm < 9, "the commutant (8) is strictly below dim M3(C) = 9"
    print("PASS_COMMUTANT_GAP  dim Comm(weak)=8 < 9=dim M3(C): a source-native colour M3 does NOT fit; "
          "the quark module C^3⊗C^2 needs an EXTERNAL ⊗C^3 (inserted A_F completion H_q=W3⊗V2)")

    # control: the full matrix algebra M8 has commutant = scalars (dim 1) — sanity on the solver
    full = commutant_dim([np.diag(np.arange(1, 9).astype(float)),
                          np.eye(8) + np.eye(8, k=1) + np.eye(8, k=-1)])
    assert full == 1, "control: an irreducible-enough algebra must have scalar commutant (dim 1)"
    print(f"FAIL_TRIVIAL_IF_SOLVER_WRONG  full-algebra commutant dim = {full} (=1 scalars): solver sane")

    print("HONEST_SCOPE  NO-GO on scene-zone + terminal carriers only; global colour stays a terminal-"
          "passport (octonion/E8) route, not scene-native — consistent with BOOK_04 §04.11")
    print("PASS_COLOUR_GENERATION_TYPED_CARRIER_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
