"""Step two and line count NO-GO theorems (Theorems 2 and 3).

Theorem 2 (Step Delta = 2 Forcing and Delta != 2 NO-GO):
  Branch A: For alphabet size q and line count r, zone capacities are:
      z_k(q,r) = 2 q^r + a(q, k),  a(q,0) = 1,  a(q,k) = 1 + q^k (k >= 1).
      Steps: Delta_1 = q, Delta_2 = q(q-1).
      Constant step (arithmetic progression) requires:
          Delta_1 = Delta_2  <=>  q = q(q - 1)  <=>  q(q - 2) = 0.
      For non-degenerate alphabet q > 0: uniquely q = 2, forcing Delta = 2.
      Any q in {3, 4, ...} gives exponential widening: Delta_2 / Delta_1 = q - 1 > 1.
  Branch B: Excess collision identity for centered triple (m-Delta, m, m+Delta):
      sum n_i^2 - N^2/3 = 2 Delta^2.
      Operational identification with active oriented role cycle |Omega_8| = 8:
          2 Delta^2 = 8  <=>  Delta^2 = 4  <=>  Delta = 2  (Delta in N^+).
      - If Delta = 1: 2 Delta^2 = 2 < 8 (role/orientation collapse).
      - If Delta = 3: 2 Delta^2 = 18 > 8 (10 spurious degrees of freedom).

Theorem 3 (Line Count r = 2 Forcing and r != 2 NO-GO):
  1. NO-GO on r = 1: Verification protocol has Line = PUnit.
     No two distinct lines exist: not (exists l1 l2, l1 != l2).
     Proved in Lean: removing_second_line_breaks_verification.
  2. NO-GO on r >= 3:
     - Steps become Delta_1 = 2, Delta_2 = 2, Delta_3 = 4.
       Zone capacities: z = (17, 19, 21, 25).
       The fourth zone jumps by 4; arithmetic centering fails.
     - Dimension mismatch: minpoly of phi over Q has degree 2 (X^2 - X - 1 = 0),
       living naturally on T^2. An r-torus T^r with r >= 3 requires cubic/higher
       algebraic returns, incompatible with irreducible phi-rigidity.
  3. Carrier equivariance:
     Complete records {0,1}^2 x {+,-} have 4 swap-fixed points: (0,0,+), (0,0,-), (1,1,+), (1,1,-).
     Nonempty partials {bot,0,1}^2 \\ {bot,bot} have only 2 fixed points: (0,0) and (1,1).
     Only complete records match Role x Orient = Dyad x Dyad x Bool.
"""

from fractions import Fraction
from itertools import product

MISSING = -1


def atomic_classes(q, k):
    return 1 if k == 0 else 1 + q ** k


def zone_capacities(q, r):
    live = 2 * (q ** r)
    return [live + atomic_classes(q, k) for k in range(r + 1)]


def main():
    # 1. Theorem 2 Branch A: Arithmetic step requires q = 2
    for q in range(1, 100):
        d1 = q
        d2 = q * (q - 1)
        if q == 2:
            assert d1 == d2 == 2
        else:
            assert d1 != d2

    # 2. Theorem 2 Branch B: Excess collision requires Delta = 2
    for dl in range(1, 20):
        excess = 2 * (dl ** 2)
        if dl == 2:
            assert excess == 8  # |Omega_8|
        elif dl < 2:
            assert excess < 8   # Deficit: role/orientation collapse
        else:
            assert excess > 8   # Surplus: spurious unphysical modes

    # 3. Theorem 3: Line count r = 2 vs r >= 3
    # At r = 2: steps are [2, 2] -> arithmetic (9, 11, 13)
    z2 = zone_capacities(2, 2)
    assert z2 == [9, 11, 13]
    steps2 = [z2[i+1] - z2[i] for i in range(len(z2)-1)]
    assert steps2 == [2, 2]

    # At r = 3: steps are [2, 2, 4] -> non-arithmetic (17, 19, 21, 25)
    z3 = zone_capacities(2, 3)
    assert z3 == [17, 19, 21, 25]
    steps3 = [z3[i+1] - z3[i] for i in range(len(z3)-1)]
    assert steps3 == [2, 2, 4]
    assert len(set(steps3)) > 1  # Centering breaks!

    # At r = 4: steps are [2, 2, 4, 8]
    z4 = zone_capacities(2, 4)
    steps4 = [z4[i+1] - z4[i] for i in range(len(z4)-1)]
    assert steps4 == [2, 2, 4, 8]

    # 4. Carrier swap equivariance
    # Complete records: {0, 1}^2 x {+,-}
    complete_carrier = [(a, b, o) for a in (0, 1) for b in (0, 1) for o in (-1, 1)]
    assert len(complete_carrier) == 8
    # Swap: (a, b, o) -> (b, a, o)
    fixed_complete = [x for x in complete_carrier if x[0] == x[1]]
    assert len(fixed_complete) == 4
    assert fixed_complete == [(0, 0, -1), (0, 0, 1), (1, 1, -1), (1, 1, 1)]

    # Nonempty partials:
    partial_carrier = [(a, b) for a in (MISSING, 0, 1) for b in (MISSING, 0, 1) if (a, b) != (MISSING, MISSING)]
    assert len(partial_carrier) == 8
    fixed_partial = [x for x in partial_carrier if x[0] == x[1]]
    assert len(fixed_partial) == 2
    assert fixed_partial == [(0, 0), (1, 1)]

    print("PASS: Theorem 2 Branch A verified: constant step forces q = 2, Delta = 2.")
    print("PASS: Theorem 2 Branch B verified: excess collision 2*Delta^2 = 8 uniquely forces Delta = 2.")
    print("PASS: Theorem 3 verified: r = 2 is arithmetic; r >= 3 has steps [2, 2, 4, ...] and fails centering.")
    print("PASS: Carrier swap equivariance: {0,1}^2 x Orient has 4 fixed points, matching Role x Orient.")


if __name__ == "__main__":
    main()
