#!/usr/bin/env python3
"""D0-GHP-GOLDEN-CAUCHY-BOUND-001 — the golden refinement series converges (CERT-CLOSED / CORE-backed).

Front E construction. The internal graph-refinement sequence G_k -> G_{k+1} contracts at the golden
scale delta0 = 1/(2 phi^3), the dimension-quantum half-gap (D0.Core.Delta:
delta0 = (phi^-1 - phi^-2)/2 = 1/(2 phi^3)). Computed EXACTLY in Q(phi):
    phi^-1 = (-1,1), phi^-2 = (2,-1), so phi^-1 - phi^-2 = (-3,2), and delta0 = (-3/2, 1)
    = -3/2 + 1*phi ~ 0.118.
Because 0 < delta0 < 1, the step-bound series Sum_k C*delta0^k is summable (a convergent geometric
majorant) with exact sum C/(1-delta0); the refinement sequence is GHP-Cauchy FOR THE INTERNAL STEP
BOUND. This is the finite, OWNED half, mirrored exactly by the Lean owner D0.Geometry.GHPGoldenCauchyBound
(delta0_lt_one, delta0_pos, ghp_refinement_summable, ghp_golden_cauchy_bound, ghp_golden_cauchy_sum).

The exact positivity argument needs NO float: delta0 = 1/(2 phi^3) with phi^3 = 2 phi + 1 > 0 (since
phi > 1 > 0), so delta0 > 0; and 2 phi^3 = 4 phi + 2 > 1 (phi > 1), so delta0 = 1/(2 phi^3) < 1.

HONESTY BOUNDARY (printed). What is CERT-CLOSED here is the internal-metric Cauchy/summability bound
from delta0 < 1. The full Gromov-Hausdorff(-Prokhorov) convergence to a SMOOTH manifold, and the
identification of the limit object, stay the external owners D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 and
D0-CONNES-RECONSTRUCTION-OWNER-001. This row owns only the geometric-series step bound.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def smul(c, x):
    return (c * x[0], c * x[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


ONE = (F(1), F(0))
PHI_INV = (F(-1), F(1))      # phi^-1 = phi - 1 = -1 + 1*phi


def powp(x, n):
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, x)
    return o


def geo_partial(C, r_val, N):
    """Exact partial sum Sum_{k=0}^{N-1} C * r^k as a Fraction (r a Fraction)."""
    s = F(0)
    rk = F(1)
    for _ in range(N):
        s += C * rk
        rk *= r_val
    return s


def main() -> int:
    print("=== D0-GHP-GOLDEN-CAUCHY-BOUND-001  Sum_k C*delta0^k converges (delta0=1/(2 phi^3) exact) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: delta0 = (phi^-1 - phi^-2)/2 = 1/(2 phi^3) (D0.Core.Delta, the "
          "dimension-quantum half-gap) is fixed BEFORE any value/limit; it is the internal contraction "
          "ratio, NOT a delta chosen after a target smooth space")

    # --- delta0 exact in Q(phi) ----------------------------------------------------
    phi_inv2 = mul(PHI_INV, PHI_INV)
    assert PHI_INV == (F(-1), F(1)), f"phi^-1 must be (-1,1): {PHI_INV}"
    assert phi_inv2 == (F(2), F(-1)), f"phi^-2 must be (2,-1): {phi_inv2}"
    delta0 = smul(F(1, 2), sub(PHI_INV, phi_inv2))
    assert delta0 == (F(-3, 2), F(1)), f"delta0 = (phi^-1 - phi^-2)/2 must be (-3/2, 1): {delta0}"
    print(f"PASS_DELTA0_EXACT  delta0 = (phi^-1 - phi^-2)/2 = {delta0} = -3/2 + 1*phi = {val(delta0):.6f}")

    # delta0 = 1/(2 phi^3): verify 2*phi^3*delta0 = 1 EXACTLY in Q(phi)
    phi3 = powp((F(0), F(1)), 3)
    assert phi3 == (F(1), F(2)), f"phi^3 must be (1,2)=2phi+1: {phi3}"     # phi^3 = 2 phi + 1
    chk = mul(smul(F(2), phi3), delta0)
    assert chk == ONE, f"2*phi^3*delta0 must equal 1 exactly: {chk}"
    print(f"PASS_DELTA0_IS_INV_2PHI3  2*phi^3*delta0 = 1 exactly  ==>  delta0 = 1/(2 phi^3); phi^3 = {phi3} = 2phi+1")

    # --- 0 < delta0 < 1 by EXACT reasoning (no float as proof) ----------------------
    # delta0 = a + b*phi with a=-3/2, b=1. phi = (1+sqrt5)/2 lies strictly in (1, 2):
    # exact bounds 1 < phi < 2 from 2 < sqrt5 < 3 (since 4 < 5 < 9). So delta0 in:
    #   lower: a + b*1   = -3/2 + 1   = -1/2   (too loose), tighten with phi > 3/2 (since sqrt5 > 2 => phi > 3/2):
    a, b = delta0
    # exact rational enclosure of phi: 8/5 < phi < 13/8  (continued-fraction convergents of phi; both verifiable:
    #   (8/5)^2 = 64/25 = 2.56 < (phi)^2=phi+1; check 8/5 < phi  <=>  (2*8/5-1)^2 < 5  <=> (11/5)^2=121/25=4.84<5 OK
    #   13/8 > phi  <=>  (2*13/8-1)^2 > 5  <=> (18/8)^2=(9/4)^2=81/16=5.0625>5 OK)
    lo_phi, hi_phi = F(8, 5), F(13, 8)
    assert (2 * lo_phi - 1) ** 2 < 5, "exact: 8/5 < phi  (since (2*8/5-1)^2 = 121/25 < 5)"
    assert (2 * hi_phi - 1) ** 2 > 5, "exact: 13/8 > phi  (since (2*13/8-1)^2 = 81/16 > 5)"
    # b = 1 > 0 so delta0 is increasing in phi: lower bound uses lo_phi, upper bound uses hi_phi
    delta0_lo = a + b * lo_phi
    delta0_hi = a + b * hi_phi
    assert delta0_lo > 0, f"exact lower bound delta0 > -3/2 + 8/5 = {delta0_lo} > 0"
    assert delta0_hi < 1, f"exact upper bound delta0 < -3/2 + 13/8 = {delta0_hi} < 1"
    print(f"PASS_DELTA0_BETWEEN_0_AND_1  exact rational enclosure: 0 < {delta0_lo} <= delta0 <= {delta0_hi} < 1 "
          f"(via 8/5 < phi < 13/8); cite Lean delta0_pos & delta0_lt_one")

    # --- geometric series converges with exact closed form C/(1-delta0) -------------
    # exact ratio as a single Fraction by using the rational enclosure midpoint is NOT a proof; the PROOF is:
    # since 0 <= delta0 < 1, Sum_k C*delta0^k = C/(1-delta0) (Lean ghp_golden_cauchy_sum). We exhibit the
    # exact partial-sum recursion S_N = C*(1 - r^N)/(1 - r) using a RATIONAL r in (delta0_lo, delta0_hi)
    # purely as a convergence WITNESS (monotone, bounded), the closed form being the cited Lean theorem.
    C = F(7, 3)
    r_rat = F(3, 25)        # 0.12, inside (delta0_lo, delta0_hi) = (0.1, 0.125): a concrete contraction ratio < 1
    assert delta0_lo < r_rat < delta0_hi, "witness ratio must lie in the exact delta0 enclosure"
    closed = C / (1 - r_rat)
    parts = [geo_partial(C, r_rat, N) for N in (5, 20, 80)]
    assert all(parts[i] < parts[i + 1] for i in range(len(parts) - 1)), "partial sums strictly increasing"
    assert all(p < closed for p in parts), "every partial sum is bounded above by C/(1-r) (convergence)"
    assert closed - parts[-1] == C * r_rat ** 80 / (1 - r_rat), "exact tail = C*r^N/(1-r)"
    print(f"PASS_GEOMETRIC_CONVERGES  Sum_k C*delta0^k -> C/(1-delta0) (Lean ghp_golden_cauchy_sum); witness "
          f"r={r_rat} in enclosure: partial sums {[float(p) for p in parts]} -> closed {float(closed):.6f}, bounded")

    # ================= NEGATIVE CONTROLS (reachable) =================
    # Control 1: an arbitrary ratio r >= 1 (e.g. r = phi > 1) gives a DIVERGENT series.
    r_div = F(13, 8)        # > 1 (an exact over-estimate of phi > 1)
    assert r_div >= 1, "control ratio must be >= 1"
    div_parts = [geo_partial(F(1), r_div, N) for N in (5, 20, 80)]
    assert div_parts[0] < div_parts[1] < div_parts[2], "control: r>=1 partial sums keep growing"
    # divergence witness: terms r^k do NOT go to 0 (they grow); no finite upper bound
    assert r_div ** 80 > div_parts[1], "control: the 80th term alone exceeds an early partial sum => no bound => divergent"
    print("FAIL_RATIO_GE_1_DIVERGES_REJECTED  r=13/8>1 (=r>=1): Sum_k r^k DIVERGES (terms r^k grow, no finite bound) "
          "— only delta0<1 is admissible")

    # Control 2: a delta chosen AFTER a target smooth space is rejected — delta0 is the INTERNAL 1/(2 phi^3),
    # not a free fit. Plant a 'tuned' delta (e.g. delta=1/2 picked to match some target) and show it is NOT delta0.
    tuned_delta = F(1, 2)
    assert (tuned_delta, F(0)) != delta0, "control: a post-hoc tuned delta=1/2 is NOT the internal delta0=1/(2phi^3)"
    assert mul(smul(F(2), phi3), (tuned_delta, F(0))) != ONE, \
        "control: tuned delta=1/2 fails 2*phi^3*delta=1, so it is not the forced internal ratio"
    print("FAIL_POSTHOC_DELTA_REJECTED  a delta=1/2 chosen to fit a target smooth space fails 2*phi^3*delta=1 "
          "— delta0 is fixed by the internal half-gap BEFORE any limit, not tuned after a target")

    print("HONEST_SCOPE  CERT-CLOSED = the internal-metric GHP-Cauchy/summability step bound from delta0<1 "
          "(mirrors Lean D0.Geometry.GHPGoldenCauchyBound). The SMOOTH-manifold GH(P) limit + limit-object "
          "identification stay external owners D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 + D0-CONNES-RECONSTRUCTION-OWNER-001; "
          "smooth manifold stays D0-SMOOTH-MANIFOLD-PASSPORT-001. No survey/CODATA/PDG datum enters.")
    print("PASS_GHP_GOLDEN_CAUCHY_BOUND")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
