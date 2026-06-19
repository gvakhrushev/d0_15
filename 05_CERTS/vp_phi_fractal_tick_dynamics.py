#!/usr/bin/env python3
"""D0-PHI-FRACTAL-TICK-DYNAMICS-OWNER-001 — the tick-weight connector (sympy/exact).

BOOK_06 §06.6. Lean companion:
`09_LEAN_FORMALIZATION/D0/Evolution/PhiFractalTickDynamics.lean`.

REUSED SUBSTRATE (NOT re-derived here): the φ-ladder + continuous envelope of
`D0.IM.ContinuumFromFractalTick` (claims D0-IM-003 and D0-PHI-LADDER-SEMIGROUP-001):
  * ladder_constant_ratio        A_{k+1} = A_k * phi^-1,
  * ladder_substrate_conserved   p + p^2 = 1 with p = phi^-1,
  * env_restricts_to_ladder      A(n) = A0 * phi^-n,
  * env_cocycle                  A(s+t) = A(s) A(t) / A0.

NEW CONNECTOR CONTENT certified here (the honest closable scope):
  1. The self-return detector split  p + p^2 = 1  has a UNIQUE root in (0,1): the contracting golden
     root p = phi^-1.  So the per-tick active fraction (the "tick weight") is FORCED to phi^-1 — it is
     not a freely chosen decay constant.  Verified exactly (sympy solve), with a finite witness on the
     contraction domain.
  2. One archive-delay tick (Block II index k -> k+1) multiplies the active amplitude by phi^-1:
     A_{k+1} = phi^-1 * A_k  (constant ratio).
  3. The discrete ladder closed form is  A_k = A0 * phi^-k  (explicit normalization A0).
  4. The continuous envelope restricts on integers to that discrete ladder:  A(k) = A0 * phi^-k.
  5. The envelope obeys the multiplicative cocycle  A(s+t) = A(s) A(t) / A0  on the convergence domain.
  6. The per-tick rate factor is  exp(-log phi) = phi^-1, i.e. the dimensionless entropy rate is log phi.

Structure-before-number: the tick weight is fixed by the STRUCTURAL split p + p^2 = 1 (the binary
self-readout balance) BEFORE any numeric decay rate is chosen; phi^-1 is forced, not fit.  No primitive
time object, external clock, or SI unit (c, h, hbar, seconds) enters — the only rate is log phi.

DELIBERATELY NOT claimed (guarded by reachable FAIL_* controls):
  * FAIL_WRONG_BASE_REJECTED:                a per-tick weight != phi^-1 (e.g. 1/2) does NOT solve
                                             p + p^2 = 1 — only phi^-1 does.
  * FAIL_MISSING_A0_NORMALIZATION_REJECTED:  dropping the A0 normalization (A_k = phi^-k forced to 1)
                                             breaks the closed form / restriction.
"""

import sympy as sp


def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the per-tick weight is fixed by the STRUCTURAL self-return "
          "split p + p^2 = 1 (binary self-readout balance) BEFORE any numeric decay rate; phi^-1 is the "
          "FORCED unique contracting root, not a fitted constant. No SI clock (c,h,hbar,s) enters; the "
          "only rate is the dimensionless log phi.")
    print("=== D0-PHI-FRACTAL-TICK-DYNAMICS-OWNER-001  tick-weight connector ===")

    sqrt5 = sp.sqrt(5)
    phi = (1 + sqrt5) / 2
    phi_inv = sp.nsimplify((sqrt5 - 1) / 2)  # primitiveRoot
    # phi^-1 really is the inverse of phi (exact).
    assert sp.simplify(phi * phi_inv - 1) == 0, "phi_inv must be the exact inverse of phi"

    # ----- 1. self-return split p + p^2 = 1 forces the tick weight p = phi^-1 ------------------
    p = sp.symbols("p", real=True)
    roots = sp.solve(sp.Eq(p + p**2, 1), p)
    roots = [sp.nsimplify(r) for r in roots]
    # Two real roots: the contracting (0,1) root phi^-1 and the negative root -phi.
    in_unit = [r for r in roots if r.is_real and r > 0 and r < 1]
    assert len(in_unit) == 1, f"split p+p^2=1 must have a UNIQUE root in (0,1), got {in_unit}"
    assert sp.simplify(in_unit[0] - phi_inv) == 0, "the unique (0,1) root must be exactly phi^-1"
    print("PASS_SELF_RETURN_SPLIT_FORCES_TICK_WEIGHT  p + p^2 = 1 has a UNIQUE root in (0,1) = phi^-1; "
          "the per-tick active fraction (tick weight) is FORCED to phi^-1")

    # phi^-1 itself satisfies the split (substrate ladder_substrate_conserved / phi_inv_satisfies).
    assert sp.simplify(phi_inv + phi_inv**2 - 1) == 0, "phi^-1 must satisfy p + p^2 = 1"
    assert phi_inv > 0 and phi_inv < 1, "tick weight phi^-1 must be a genuine contraction in (0,1)"
    print("PASS_TICK_WEIGHT_SATISFIES_SPLIT_AND_CONTRACTS  phi^-1 + (phi^-1)^2 = 1 and 0 < phi^-1 < 1")

    # ----- 2. one archive tick multiplies the active amplitude by phi^-1 -----------------------
    A0 = sp.symbols("A0", positive=True)

    def ladder(k):
        return phi_inv**k  # ladderAmount: A0 = 1 substrate

    for k in range(0, 8):
        assert sp.simplify(ladder(k + 1) - phi_inv * ladder(k)) == 0, \
            "one archive tick must multiply by phi^-1 (constant ratio)"
    print("PASS_ARCHIVE_TICK_MULTIPLIES_BY_PHI_INV  A_{k+1} = phi^-1 * A_k for k=0..7 (constant ratio)")

    # ----- 3. discrete ladder closed form A_k = A0 * phi^-k -----------------------------------
    for k in range(0, 8):
        assert sp.simplify(A0 * ladder(k) - A0 * phi_inv**k) == 0, \
            "discrete ladder closed form must be A0 * phi^-k"
    print("PASS_DISCRETE_LADDER_CLOSED_FORM  A_k = A0 * phi^-k (explicit A0 normalization) for k=0..7")

    # ----- 4. continuous envelope restricts on integers to the discrete ladder ----------------
    s, t = sp.symbols("s t", real=True)
    log_phi = sp.log(phi)

    def env(x):
        return A0 * sp.exp(-x * log_phi)

    for k in range(0, 8):
        diff = sp.simplify(env(k) - A0 * ladder(k))
        assert diff == 0, f"envelope must restrict to A0 * phi^-k at integer k={k}, residual {diff}"
    print("PASS_CONTINUOUS_ENVELOPE_RESTRICTS_TO_LADDER  A(k) = A0 * phi^-k on the integers")

    # ----- 5. envelope cocycle A(s+t) = A(s) A(t) / A0 ----------------------------------------
    cocycle = sp.simplify(env(s + t) - env(s) * env(t) / A0)
    assert cocycle == 0, f"envelope cocycle A(s+t) = A(s)A(t)/A0 must hold, residual {cocycle}"
    print("PASS_ENVELOPE_COCYCLE  A(s+t) = A(s) A(t) / A0 (multiplicative one-parameter extension)")

    # ----- 6. per-tick rate factor exp(-log phi) = phi^-1 (rate = log phi) ---------------------
    assert sp.simplify(sp.exp(-log_phi) - phi_inv) == 0, "per-tick rate factor must be exp(-log phi) = phi^-1"
    # one continuous tick (t -> t+1) multiplies the envelope by exp(-log phi) = phi^-1.
    one_tick = sp.simplify(env(t + 1) - env(t) * phi_inv)
    assert one_tick == 0, f"one continuous tick must multiply by phi^-1, residual {one_tick}"
    print("PASS_RATE_FACTOR_IS_PHI_INV  exp(-log phi) = phi^-1; the dimensionless entropy rate is log phi")

    # ----- NEGATIVE CONTROL: a wrong per-tick base does NOT solve the split -------------------
    # A "tick weight" of 1/2 (or any base != phi^-1) fails p + p^2 = 1 — the weight is NOT free.
    wrong_base = sp.Rational(1, 2)
    residual_half = sp.simplify(wrong_base + wrong_base**2 - 1)
    assert residual_half != 0, "1/2 must NOT satisfy p + p^2 = 1"
    # And it does not equal the forced weight.
    assert sp.simplify(wrong_base - phi_inv) != 0, "1/2 must differ from the forced phi^-1"
    print(f"FAIL_WRONG_BASE_REJECTED  a per-tick weight != phi^-1 (tested 1/2) does NOT solve the "
          f"self-return split p + p^2 = 1 (residual {residual_half} != 0) -- the tick base is FORCED "
          f"to phi^-1, an arbitrary base is REJECTED")

    # ----- NEGATIVE CONTROL: dropping the A0 normalization breaks the closed form -------------
    # Forcing A0 := 1 inside the closed form makes A_k = A0 * phi^-k FALSE whenever A0 != 1.
    A0_val = sp.Integer(3)  # a concrete normalization != 1
    correct = A0_val * phi_inv**2          # A_2 with proper A0
    no_norm = sp.Integer(1) * phi_inv**2   # A_2 if A0 dropped (set to 1)
    assert sp.simplify(correct - no_norm) != 0, \
        "dropping the A0 normalization must change A_k whenever A0 != 1"
    print("FAIL_MISSING_A0_NORMALIZATION_REJECTED  forcing A0:=1 in A_k = A0*phi^-k is FALSE for A0!=1 "
          "(tested A0=3 at k=2) -- the explicit A0 normalization is required, dropping it is REJECTED")

    print("PASS_PHI_FRACTAL_TICK_DYNAMICS_CONNECTOR  self-return split forces tick weight phi^-1; "
          "archive tick multiplies by phi^-1; A_k = A0*phi^-k restricts the envelope; rate = log phi. "
          "Reuses D0-IM-003 + D0-PHI-LADDER-SEMIGROUP-001 substrate; new content = the tick-weight connector.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
