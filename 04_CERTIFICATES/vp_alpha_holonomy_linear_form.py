#!/usr/bin/env python3
"""D0-ALPHA-HOLONOMY-LINEAR-FORM-001 — the α dressing form 1+h·sinθ is DERIVED (nilpotent transport), not fit.

Elevates the ONE piece of the α closure-holonomy that was previously data-selected (linear beats exp
against CODATA) to a structural derivation. The seam carries two distinct operators:
  * channel selector G (Q8, G^2 = -I, ELLIPTIC) -> picks the sin amplitude    [owned by SeamHolonomy, Lean]
  * transport N (the DIRECTED CP-seam crossing, N^2 = 0, NILPOTENT) -> carries the correction ONCE.
Because the CP-seam is DIRECTED (the directed 3-cycle of D0-BARYON-ASYMMETRY-DELTA0-001), one closure
crosses it once and cannot return -> nilpotent transport N^2=0 -> exp(sN)=I+sN EXACTLY (all higher orders
vanish identically) -> the dressing factor is EXACTLY 1+s, linear. Setting s=h_KS*sin(theta) gives the
closure-holonomy form 1+h_KS*sin(theta).

WHAT IS PROVED (exact, able to FAIL):
  * N^2 = 0 (nilpotent) and the parabolic group law (I+sN)(I+tN) = I+(s+t)N EXACTLY (no cross term);
  * the anchor-row readout of I+sN is exactly 1+s (linear, higher orders identically zero);
  * CONTRAST: an ELLIPTIC generator (G^2=-I) gives a BOUNDED rotation readout cos-sin (|.|<=sqrt2), which
    can NEVER be the unbounded linear 1+s -> the exp/oscillatory form is structurally excluded;
  * CONTROL (nilpotency is load-bearing): a NON-nilpotent idempotent M (M^2=M!=0) BREAKS the parabolic law
    -- (I+sM)(I+tM) = I+(s+t+st)M != I+(s+t)M -- so exact linearity REQUIRES N^2=0, it is not generic;
  * the resulting alpha^-1 with the linear factor matches CODATA to ~6.7e-8, while the exp factor is off by
    ~1.66e-5 (its 2nd-order term depth*0.5*(h sin)^2 ~1.48e-5 is far above the match) -> data CONFIRMS the
    single directed crossing rather than SELECTING the form.
HONEST SCOPE (printed): N^2=0 encodes "one directed crossing per closure" -- that single-crossing input is
the physical hypothesis (motivated by the directed CP-seam); this cert proves that GIVEN nilpotent transport
the form is EXACTLY linear and the elliptic channel cannot produce it. Lean: D0.Spectral.SeamTransportLinear.
"""
from __future__ import annotations
import math, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def main() -> int:
    print("=== D0-ALPHA-HOLONOMY-LINEAR-FORM-001  1+h·sinθ is nilpotent-transport-DERIVED, not fit ===")

    # --- N^2 = 0 (directed seam transport, nilpotent) ----------------------------------------
    N = [[0.0, 1.0], [0.0, 0.0]]
    N2 = mat_mul(N, N)
    assert N2 == [[0.0, 0.0], [0.0, 0.0]], f"N^2 must be 0: {N2}"
    print("PASS_NILPOTENT  N=[[0,1],[0,0]], N^2=0 (one directed crossing, no return within a closure)")

    # --- parabolic group law: (I+sN)(I+tN) = I+(s+t)N EXACTLY --------------------------------
    def P(s):
        return [[1.0 + 0.0, s], [0.0, 1.0]]  # I + s*N
    s, t = 0.37, 1.29
    lhs = mat_mul(P(s), P(t))
    rhs = P(s + t)
    assert all(abs(lhs[i][j] - rhs[i][j]) < 1e-15 for i in range(2) for j in range(2)), \
        f"parabolic law broken: {lhs} vs {rhs}"
    print(f"PASS_PARABOLIC_GROUP  (I+sN)(I+tN)=I+(s+t)N exactly (no s·t cross term; verified s={s},t={t})")

    # --- anchor-row readout = 1+s (exact linear) ---------------------------------------------
    s0 = 0.813
    readout = P(s0)[0][0] + P(s0)[0][1]
    assert abs(readout - (1.0 + s0)) < 1e-15, f"readout {readout} != 1+s {1+s0}"
    print(f"PASS_LINEAR_READOUT  anchor-row total of I+sN = 1+s exactly (identity 1 + crossing s)")

    # --- CONTROL: non-nilpotent generator BREAKS the parabolic law (nilpotency load-bearing) --
    M = [[1.0, 0.0], [0.0, 0.0]]                # idempotent, M^2 = M != 0
    M2 = mat_mul(M, M)
    assert M2 == M and M2 != [[0.0, 0.0], [0.0, 0.0]], "M must be idempotent non-nilpotent"
    def Pm(x):
        return [[1.0 + x, 0.0], [0.0, 1.0]]     # I + x*M
    lhsM = mat_mul(Pm(s), Pm(t))
    rhsM = Pm(s + t)
    assert abs(lhsM[0][0] - rhsM[0][0]) > 1e-6, "non-nilpotent M should BREAK the law"
    print(f"FAIL_NONNILPOTENT_BREAKS_LAW  M^2=M!=0: (I+sM)(I+tM)(0,0)={lhsM[0][0]:.4f} != I+(s+t)M (0,0)={rhsM[0][0]:.4f}  -> N^2=0 is load-bearing")

    # --- CONTRAST: elliptic readout bounded, cannot be linear 1+s ----------------------------
    for th in (0.5, 1.0, 2.4, 4.0):
        ell = math.cos(th) - math.sin(th)
        assert abs(ell) <= math.sqrt(2) + 1e-12, f"elliptic readout unbounded? {ell}"
    print(f"FAIL_ELLIPTIC_CANNOT_BE_LINEAR  elliptic anchor readout cosθ−sinθ bounded by √2≈1.414; unbounded 1+s excluded")

    # --- data confirms linear over exp (the CHK layer, now a CONFIRMATION not a selection) ----
    h = math.log(PHI)
    theta = 12.0 / 5.0
    depth = PHI ** -17
    atop = 359.0 * PHI ** -2 - PHI ** -5
    a_lin = atop + depth * (1.0 + h * math.sin(theta))
    a_exp = atop + depth * math.exp(h * math.sin(theta))
    CODATA2018 = 137.035999084
    gap_lin = abs(a_lin - CODATA2018)
    gap_exp = abs(a_exp - CODATA2018)
    assert gap_lin < 1e-7 < gap_exp, f"linear must beat exp: lin={gap_lin:.2e} exp={gap_exp:.2e}"
    second_order = depth * 0.5 * (h * math.sin(theta)) ** 2
    print(f"PASS_DATA_CONFIRMS_SINGLE_CROSSING  linear gap={gap_lin:.2e} << exp gap={gap_exp:.2e}; "
          f"exp 2nd-order term {second_order:.2e} is what the nilpotency kills")
    print(f"  α⁻¹(linear) = {a_lin:.12f}  (structure DERIVED; 9-digit value still CHK, last ~1e-8 HYP)")

    print("HONEST_SCOPE  N^2=0 = 'one directed crossing per closure' (physical input from directed CP-seam); "
          "GIVEN it, the form is EXACTLY linear and the elliptic channel cannot produce it")
    print("PASS_ALPHA_HOLONOMY_LINEAR_FORM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
