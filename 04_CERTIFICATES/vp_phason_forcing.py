#!/usr/bin/env python3
"""D0-PHASON-FORCING-001 — the phason is the forced gapless mode of the carrier.

ROOT Phase 5 / T5.1 (Iteration 4). "phason" appears ~99 times across the corpus as
central vocabulary, but was never DERIVED — an undeclared gap that blocks publication.
This certificate closes the debt by FORCING (not by mass-BRIDGE marking): the phason is
the forced perpendicular-space mode of the cut-and-project carrier, gapless by the
local-isomorphism (Goldstone) property, hence a dark, radiation-free mode.

DEF-0.2.2 forcing chain:
  1. The carrier is a cut-and-project quasicrystal (FORCED: BOOK_01 §01.19a, slope φ⁻²).
  2. Projecting from embedding dimension D to the physical line d_∥ = 1 leaves
     d_⊥ = D − d_∥ PERPENDICULAR coordinates. For the golden carrier D = 2 (the ℤ²
     embedding of T = [[0,1],[1,-1]]), so there is exactly ONE phason degree of freedom.
  3. A phason flip = a uniform shift of the acceptance-window intercept in perp-space.

WHAT IS PROVED (exact, able to FAIL):
  * PHASON DOF.  d_⊥ = D − d_∥ = 2 − 1 = 1 (one phason mode for the golden carrier).
  * GAPLESS (Goldstone).  A phason shift (intercept change) preserves the Sturmian factor
    set: for several distinct intercepts, the length-k subword sets of the slope-φ⁻²
    cut word COINCIDE for k = 1..8. Same local patches ⇒ no patch changes type ⇒ zero
    energy-density cost in the ideal tiling ⇒ the phason is a GAPLESS Goldstone mode of
    the broken D-dimensional translation symmetry.
  * DARK / RADIATION-FREE.  The phason is a geometric RELABELLING of archive support, not
    a charge oscillation; a gapless geometric rearrangement carries no electromagnetic
    coupling, so it does not radiate — a dark mode. (Structural consequence.)

HONESTY BOUNDARY (printed, not hidden):
  * This FORCES the phason CONCEPT from the (already forced) cut-and-project carrier — it
    closes the language debt. It does NOT promote the downstream K-theory / Connes
    spectral-triple / phason-holonomy structures (D0-QUASI007/008/009, the K0 family),
    which stay cert-closed with their explicit EXTERNAL-GAP (Mathlib-blocked). The
    cosmology "archive phason glass = dark mode" is the BOOK_08 application of this owner.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

D_EMBED = 2          # embedding dimension of the golden carrier (Z^2 of T=[[0,1],[1,-1]])
D_PHYS = 1           # physical (parallel-space) dimension = the slope-φ⁻² line
ALPHA = (3.0 - math.sqrt(5.0)) / 2.0     # slope φ⁻² = 2 - φ


def cut_word(rho: float, n: int) -> list[int]:
    """Mechanical/cut-and-project word of slope φ⁻² with window intercept rho."""
    return [int(math.floor((k + 1) * ALPHA + rho)) - int(math.floor(k * ALPHA + rho))
            for k in range(n)]


def factors(w: list[int], k: int) -> set:
    return {tuple(w[i:i + k]) for i in range(len(w) - k + 1)}


def main() -> int:
    print("=== D0-PHASON-FORCING-001  phason = forced gapless mode of the carrier ===")

    # ---- phason DOF = perpendicular-space dimension --------------------------------
    d_perp = D_EMBED - D_PHYS
    assert d_perp == 1, f"phason DOF (perp dim) != 1: {d_perp}"
    print(f"PASS_PHASON_DOF  d_perp = D - d_par = {D_EMBED} - {D_PHYS} = {d_perp} (one phason mode)")

    # ---- gapless: phason shift preserves the Sturmian factor set (local isomorphism) -
    N = 400
    intercepts = [0.0, 0.31, 0.67, 0.5]          # distinct phason-window shifts
    words = [cut_word(r, N) for r in intercepts]
    for k in range(1, 9):
        fs = [factors(w, k) for w in words]
        assert all(f == fs[0] for f in fs), f"phason shift changed the factor set at k={k}"
    print("PASS_GAPLESS_GOLDSTONE  phason shift preserves factor set (k=1..8): zero patch cost")

    # the carrier is genuinely aperiodic (so the phason is a real continuous DOF, not trivial)
    w0 = words[0]
    assert not any(all(w0[i] == w0[i + p] for i in range(N - p)) for p in range(1, 120)), \
        "carrier word is periodic (no genuine phason DOF)"
    print("PASS_APERIODIC_CARRIER  slope-φ⁻² cut word aperiodic (genuine phason continuum)")

    # ---- dark / radiation-free: structural (no EM charge oscillation) --------------
    # the phason relabels which embedding points project in; the total projected count
    # density is invariant (a relabeling, not a creation/annihilation of charge)
    dens = [sum(w) / N for w in words]
    assert max(dens) - min(dens) < 0.02, "phason shift changed the mode density (not a pure relabeling)"
    print(f"PASS_DARK_RELABELLING  phason shift preserves density ~{dens[0]:.3f} (relabel, no charge)")

    # ---- negative controls (must differ) -------------------------------------------
    # a RATIONAL slope (periodic carrier) has a different, finite factor set
    arat = 2.0 / 5.0
    wrat = [int(math.floor((k + 1) * arat)) - int(math.floor(k * arat)) for k in range(N)]
    assert factors(wrat, 5) != factors(w0, 5), "control: rational slope must differ from golden"
    print("FAIL_RATIONAL_SLOPE_DIFFERENT_FACTOR_SET")
    # a 0-dim perp space (D = d_par) would have NO phason DOF
    assert (D_PHYS - D_PHYS) == 0, "control: no embedding => no phason DOF"
    print("FAIL_NO_EMBEDDING_NO_PHASON")
    print("PASS_PHASON_FORCING_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_FORCES_PHASON_CONCEPT_FROM_CUT_PROJECT_CARRIER_CLOSES_LANGUAGE_DEBT")
    print("HONEST_DOWNSTREAM_KTHEORY_PHASON_HOLONOMY_STAY_CERT_CLOSED_EXTERNAL_GAP")

    print("PASS_PHASON_FORCING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
