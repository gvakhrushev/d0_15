#!/usr/bin/env python3
"""D0-CONTINUOUS-TIME-SEMIGROUP-ENVELOPE-001 — continuous envelope of the phi-tick (sympy/exact).

BOOK_06 §06.6. Lean companion:
`09_LEAN_FORMALIZATION/D0/Evolution/PhiFractalTickDynamics.lean`.

REUSED SUBSTRATE (NOT re-derived here): the continuous envelope owner of
`D0.IM.ContinuumFromFractalTick` (claim D0-PHI-LADDER-SEMIGROUP-001):
  * envAmount               A(t) = A0 * exp(-t * log phi),
  * env_cocycle             A(s+t) = A(s) A(t) / A0,
  * env_restricts_to_ladder A(n) = A0 * phi^-n.

This cert verifies the continuous-time leg of the tick-weight connector: the unique MULTIPLICATIVE
one-parameter envelope of the discrete phi-tick, its restriction to the integer ladder, and that the
decay rate is the FORCED log phi (= -log of the tick weight phi^-1), not an arbitrary constant.

What is CERTIFIED here (the honest closable scope):
  1. A(s) = A0 * exp(-s * log phi) obeys the multiplicative cocycle A(s+t) = A(s) A(t) / A0 EXACTLY
     (on the convergence domain of the real exponential).
  2. A(0) = A0 (normalization) and A(s+t)/A0 factorizes as (A(s)/A0)*(A(t)/A0) — a genuine semigroup.
  3. The envelope restricts on integers to the certified discrete ladder A(k) = A0 * phi^-k.
  4. The continuous decay rate is FORCED: kappa = log phi, and the per-unit factor exp(-kappa) = phi^-1
     equals the discrete tick weight. So the continuous and discrete descriptions are one object.

Structure-before-number: the cocycle (multiplicative semigroup) STRUCTURE and the integer restriction
are fixed BEFORE any numeric rate; the rate log phi is then FORCED by matching the discrete tick weight
phi^-1, not chosen.  No primitive time object, external clock, or SI unit (c, h, hbar, seconds) enters.

DELIBERATELY NOT claimed (guarded by reachable FAIL_* controls):
  * FAIL_ADDITIVE_ENVELOPE_REJECTED:     an ADDITIVE envelope A0 - s*log phi does NOT obey the
                                         multiplicative cocycle and does NOT restrict to A0*phi^-k.
  * FAIL_ARBITRARY_DECAY_RATE_REJECTED:  a decay rate kappa != log phi fails to restrict to the
                                         certified phi^-k ladder — the rate is FORCED, not free.
"""

import sympy as sp


def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the multiplicative-cocycle (semigroup) STRUCTURE and the "
          "integer restriction are fixed BEFORE any numeric rate; the decay rate kappa = log phi is then "
          "FORCED by matching the discrete tick weight phi^-1, not chosen. No SI clock (c,h,hbar,s) "
          "enters the envelope.")
    print("=== D0-CONTINUOUS-TIME-SEMIGROUP-ENVELOPE-001  continuous envelope of the phi-tick ===")

    sqrt5 = sp.sqrt(5)
    phi = (1 + sqrt5) / 2
    phi_inv = sp.nsimplify((sqrt5 - 1) / 2)
    log_phi = sp.log(phi)
    A0 = sp.symbols("A0", positive=True)
    s, t = sp.symbols("s t", real=True)

    def env(x):
        return A0 * sp.exp(-x * log_phi)

    # ----- 1. multiplicative cocycle A(s+t) = A(s) A(t) / A0 ----------------------------------
    cocycle = sp.simplify(env(s + t) - env(s) * env(t) / A0)
    assert cocycle == 0, f"envelope cocycle must hold exactly, residual {cocycle}"
    print("PASS_ENVELOPE_COCYCLE  A(s+t) = A(s) A(t) / A0 (exact, on the convergence domain)")

    # ----- 2. normalization A(0) = A0 and semigroup factorization -----------------------------
    assert sp.simplify(env(0) - A0) == 0, "A(0) must equal A0 (normalization)"
    factor = sp.simplify(env(s + t) / A0 - (env(s) / A0) * (env(t) / A0))
    assert factor == 0, f"normalized envelope must factorize as a semigroup, residual {factor}"
    print("PASS_NORMALIZATION_AND_SEMIGROUP  A(0) = A0 and (A(s+t)/A0) = (A(s)/A0)(A(t)/A0)")

    # ----- 3. envelope restricts on integers to the certified discrete ladder -----------------
    for k in range(0, 8):
        diff = sp.simplify(env(k) - A0 * phi_inv**k)
        assert diff == 0, f"envelope must restrict to A0 * phi^-k at k={k}, residual {diff}"
    print("PASS_ENVELOPE_RESTRICTS_TO_DISCRETE_LADDER  A(k) = A0 * phi^-k on the integers")

    # ----- 4. the continuous decay rate is FORCED: exp(-log phi) = phi^-1 ----------------------
    assert sp.simplify(sp.exp(-log_phi) - phi_inv) == 0, "per-unit factor exp(-log phi) must equal phi^-1"
    one_tick = sp.simplify(env(t + 1) - env(t) * phi_inv)
    assert one_tick == 0, f"one continuous unit must multiply by phi^-1, residual {one_tick}"
    print("PASS_DECAY_RATE_FORCED  kappa = log phi; exp(-kappa) = phi^-1 = discrete tick weight")

    # ----- NEGATIVE CONTROL: an additive envelope is NOT a semigroup --------------------------
    # A_add(s) = A0 - s*log phi (linear melting) fails the multiplicative cocycle and the restriction.
    def env_add(x):
        return A0 - x * log_phi

    add_cocycle = sp.simplify(env_add(s + t) - env_add(s) * env_add(t) / A0)
    assert add_cocycle != 0, "additive envelope must FAIL the multiplicative cocycle"
    # It also does not restrict to the phi^-k ladder (already at k=2 it differs).
    add_restrict = sp.simplify(env_add(2) - A0 * phi_inv**2)
    assert add_restrict != 0, "additive envelope must FAIL the discrete-ladder restriction at k=2"
    print("FAIL_ADDITIVE_ENVELOPE_REJECTED  the ADDITIVE envelope A0 - s*log phi does NOT obey the "
          "multiplicative cocycle and does NOT restrict to A0*phi^-k (fails at k=2) -- linear melting "
          "is REJECTED; the envelope must be multiplicative")

    # ----- NEGATIVE CONTROL: an arbitrary decay rate fails the ladder restriction -------------
    # kappa' = log 2 != log phi gives exp(-2*kappa') = 1/4 != phi^-2, so it cannot match the tick ladder.
    kappa_wrong = sp.log(2)

    def env_wrong(x):
        return A0 * sp.exp(-x * kappa_wrong)

    wrong_restrict = sp.simplify(env_wrong(2) - A0 * phi_inv**2)
    assert wrong_restrict != 0, "an arbitrary rate (log 2) must FAIL the phi^-k restriction at k=2"
    assert sp.simplify(sp.exp(-kappa_wrong) - phi_inv) != 0, "exp(-log 2) must differ from phi^-1"
    print("FAIL_ARBITRARY_DECAY_RATE_REJECTED  a decay rate kappa != log phi (tested log 2) gives "
          "exp(-kappa) != phi^-1 and fails to restrict to A0*phi^-k (k=2) -- the rate is FORCED to "
          "log phi, an arbitrary rate is REJECTED")

    print("PASS_CONTINUOUS_TIME_SEMIGROUP_ENVELOPE  multiplicative cocycle + integer restriction to the "
          "phi^-k ladder + forced rate log phi certified. Reuses the D0-PHI-LADDER-SEMIGROUP-001 "
          "env_cocycle owner; new content = the continuous leg of the tick-weight connector.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
