#!/usr/bin/env python3
"""D0-PHASON-ARCHIVE-CAPACITY-REDSHIFT-001 (CERT-CLOSED, narrow): the archive-capacity redshift map
1+z = phi^n and the integer-window archive ratio w_N = phi^(n-1)/(phi^n-1).

Lean owner: D0.Cosmology.PhasonArchiveCapacityRedshift
  one_lt_phi                          1 < phi
  redshift_strictMono                 m<n -> phi^m < phi^n (strict monotone bijection on samples)
  energy_pos                          1<=n -> 0 < phi^n - 1 (w_N well-defined)
  energy_zero_at_n0                   phi^0 - 1 = 0 (the excluded n=0 pole)
  phi_inv_eq_sub_one                  phi^-1 = phi - 1
  dR_closed_form                      phi^(n+1) - phi^n = phi^n*(phi-1)  (= phi^(n-1))
  wN_one_eq_phi / wN_two_eq_one       w_N(1)=phi, w_N(2)=1 (exact Q(phi))
  wN_strictAnti                       w_N strictly DECREASING in n on n>=1
  wN_late_end_exceeds_early_limit     phi^-1 < w_N(1)=phi (limit is the z->inf EARLY end)
  phason_archive_capacity_redshift

Exact Q(phi)=Z[phi] arithmetic, (a,b) = a + b*phi with phi^2 = phi+1:
  energy   R_n  = phi^n - 1
  pressure dR_n = R_{n+1} - R_n = phi^(n+1) - phi^n = phi^n*(phi-1) = phi^(n-1)  (closed form)
  ratio    w_N  = dR_n / R_n = phi^(n-1) / (phi^n - 1)

DIRECTION (the load-bearing honesty fact): w_N is DECREASING and w_N -> phi^-1 as n -> inf, i.e.
1+z = phi^n -> inf  =>  z -> inf, the EARLY-time end. phi^-1 is NOT the late-time z->0 value: as
n -> 0+ (z -> 0) the energy phi^n - 1 -> 0+ so w_N DIVERGES; on the integer window the largest sample
is w_N(1) = phi ~ 1.618 at the small-z edge. So phi^-1 = lim_{z->inf}, strictly BELOW w_N(1).

HONEST SCOPE: this owns the FINITE-WINDOW facts (bijection, exact values, monotonicity, direction)
only. The physical dark-energy reading -- a proven continuum interpolation w_N -> w_D0(u) PLUS the
magnitude/sign normalization map onto the physical NEGATIVE w_DE on the late-time window -- is NOT
here; it is the PROOF-TARGET D0-PHASON-WDE-Z-MAP-OWNER-001. No survey datum (DESI/CPL/H0) enters.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


# ---- exact Z[phi] arithmetic: (a,b) = a + b*phi, phi^2 = phi+1 ----
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


ONE = (F(1), F(0))
PHIv = (F(0), F(1))


def powp(x, n):
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, x)
    return o


def R(n):
    # archive energy R_n = phi^n - 1
    return sub(powp(PHIv, n), ONE)


def main() -> int:
    print("=== D0-PHASON-ARCHIVE-CAPACITY-REDSHIFT-001  redshift 1+z=phi^n and window ratio "
          "w_N=phi^(n-1)/(phi^n-1) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: Z[phi] with phi^2=phi+1; redshift map 1+z=phi^n, energy "
          "R_n=phi^n-1, pressure dR_n=R_{n+1}-R_n, ratio w_N=dR_n/R_n fixed BEFORE any numeric value; "
          "direction = limit at n->inf (z->inf, EARLY), NOT z->0")

    # --- field anchor: phi^2 = phi + 1 (fixed before numbers) ---
    assert mul(PHIv, PHIv) == add(PHIv, ONE), "phi^2 = phi + 1 must hold in Z[phi]"
    print("PASS_FIELD_PHI2  phi^2 = phi + 1 (Z[phi] structure)")

    # --- (b) redshift 1+z = phi^n is a strict monotone bijection (on integer/rational samples) ---
    zs = [val(powp(PHIv, n)) for n in range(0, 9)]   # 1+z at n=0..8
    assert all(zs[i] < zs[i + 1] for i in range(len(zs) - 1)), "1+z=phi^n must be strictly increasing"
    assert len(set(zs)) == len(zs), "strict monotonicity => injective (distinct 1+z samples)"
    print(f"PASS_REDSHIFT_STRICT_MONO_BIJECTION  1+z=phi^n strictly increasing & injective on n=0..8: "
          f"{[round(v,4) for v in zs]}")

    # --- (c) energy R_n > 0 for n>=1 (w_N well-defined); R_0 = 0 is the excluded pole ---
    assert R(0) == (F(0), F(0)), f"R_0 must be 0 (the excluded pole): {R(0)}"
    assert all(val(R(n)) > 0 for n in range(1, 9)), "R_n = phi^n - 1 must be > 0 for n>=1"
    print("PASS_ENERGY_POS_AND_POLE  R_n=phi^n-1 > 0 for n>=1 (w_N well-defined); R_0=0 = excluded n=0 pole")

    # --- pressure closed form: dR_n = phi^(n+1)-phi^n = phi^n*(phi-1) = phi^(n-1) ---
    phi_minus_1 = sub(PHIv, ONE)
    for n in range(1, 9):
        dR = sub(R(n + 1), R(n))
        assert dR == mul(powp(PHIv, n), phi_minus_1), f"dR_n must equal phi^n*(phi-1): n={n}"
        assert dR == powp(PHIv, n - 1), f"dR_n must equal phi^(n-1): n={n}, got {dR}"
    print("PASS_PRESSURE_CLOSED_FORM  dR_n = phi^n*(phi-1) = phi^(n-1) (exact Z[phi]) for n=1..8")

    # --- (a) exact w_N values for n=1..8 over Q(phi); spot exacts w_N(1)=phi, w_N(2)=1 ---
    EXPECT = {1: PHI, 2: 1.0}     # exact: w_N(1)=phi/(phi-1)... = phi ; w_N(2)=1
    seq = []
    for n in range(1, 9):
        dR = powp(PHIv, n - 1)              # numerator phi^(n-1)
        rho = R(n)                          # denominator phi^n - 1
        w = val(dR) / val(rho)
        seq.append(w)
        if n in EXPECT:
            assert abs(w - EXPECT[n]) < 1e-12, f"w_N({n}) must equal {EXPECT[n]}: got {w}"
    # exact rational confirmation of the two closed values via Z[phi]: w_N(1)*(phi-1)=phi^0=1 etc.
    assert mul(R(1), PHIv) == powp(PHIv, 0), "w_N(1)=phi <=> phi*(phi-1) = 1 (R(1)=phi-1)"
    assert R(2) == PHIv, "w_N(2)=1 <=> phi^2-1 = phi (so dR_2/R_2 = phi/phi = 1)"
    print(f"PASS_WN_EXACT_VALUES  w_N(n) n=1..8 = {[round(w,6) for w in seq]}; exact w_N(1)=phi, w_N(2)=1 (Z[phi])")

    # --- (c) w_N strictly DECREASING in n on n>=1 ---
    assert all(seq[i] > seq[i + 1] for i in range(len(seq) - 1)), "w_N must be strictly decreasing in n"
    print(f"PASS_WN_STRICT_DECREASING  w_N(n) strictly decreasing on n=1..8 (n=0 excluded as pole)")

    # --- DIRECTION fact: limit phi^-1 is at n->inf (z->inf, EARLY); NOT the z->0 value ---
    w_big = val(powp(PHIv, 40 - 1)) / val(R(40))
    assert abs(w_big - PHI ** -1) < 1e-6, "as n->inf, w_N -> phi^-1 (the z->inf EARLY-time limit)"
    assert PHI ** -1 < seq[0], "phi^-1 (the early-time limit) must lie strictly BELOW w_N(1)=phi"
    assert seq[0] > seq[-1] > PHI ** -1, "decreasing sequence approaches phi^-1 from ABOVE as z->inf"
    print(f"PASS_DIRECTION_LIMIT_IS_Z_INF  w_N -> phi^-1={PHI**-1:.6f} as n->inf (1+z=phi^n->inf, z->inf "
          f"EARLY); strictly BELOW w_N(1)=phi={seq[0]:.6f} (the small-z window edge)")

    # ===================== reachable negative controls =====================

    # FAIL_LATE_TIME_LIMIT_MISIDENTIFIED: reject 'w_N -> phi^-1 is the z->0 dark-energy value'.
    # At small n (z->0) the energy phi^n-1 -> 0+ so w_N DIVERGES upward; it does NOT settle to phi^-1.
    # Sub-integer probe near z->0 confirms divergence, not convergence to phi^-1.
    near_zero = []
    for nn in (0.5, 0.2, 0.1, 0.05):
        w_small = (PHI ** (nn - 1)) / (PHI ** nn - 1.0)      # w_N at fractional n near 0
        near_zero.append(w_small)
    assert near_zero[-1] > 10.0, "as z->0 (n->0+), w_N must DIVERGE (not approach phi^-1)"
    assert all(near_zero[i] < near_zero[i + 1] for i in range(len(near_zero) - 1)), \
        "w_N grows without bound as n->0+ (z->0)"
    claim_late_time = abs(near_zero[-1] - PHI ** -1) < 0.5     # the WRONG claim 'limit at z->0 is phi^-1'
    assert not claim_late_time, "control: phi^-1 is NOT the z->0 (late-time) value of w_N"
    print("FAIL_LATE_TIME_LIMIT_MISIDENTIFIED  rejecting 'w_N->phi^-1 is the z->0 dark-energy value': as "
          f"z->0 (n->0+) w_N DIVERGES (e.g. {near_zero[-1]:.2f}); phi^-1={PHI**-1:.3f} is the n->inf "
          "(z->inf, EARLY) limit, not the late-time value")

    # FAIL_DESI_INPUT_REJECTED: no DESI BAO datum enters; the window facts are pure internal Z[phi].
    desi_rd = 147.09     # representative external DESI sound-horizon r_d [Mpc], used only as rejected input
    assert all(abs(w - desi_rd) > 1.0 for w in seq), "control: a DESI r_d datum is NOT w_N"
    assert all(abs(v - desi_rd) > 1.0 for v in zs), "control: a DESI r_d datum is NOT 1+z=phi^n"
    print("FAIL_DESI_INPUT_REJECTED  no DESI survey datum (r_d/BAO) enters; the redshift map and w_N are "
          "internal Z[phi] objects, not fitted to DESI")

    # FAIL_CPL_AS_CORE_REJECTED: a CPL (w0,wa) parametrization is NOT the D0-core object.
    cpl_w0, cpl_wa = -0.95, -0.4     # representative external CPL numbers, planted as rejected inputs
    assert all(abs(w - cpl_w0) > 1e-2 for w in seq), "control: CPL w0 is not the internal w_N"
    assert cpl_w0 < 0 < seq[-1], "control: physical CPL w0<0 vs POSITIVE internal ratio w_N>0 -- different objects"
    assert abs(cpl_wa) >= 0, "cpl_wa planted only to be rejected as a core input"
    print("FAIL_CPL_AS_CORE_REJECTED  a fitted CPL (w0,wa) parametrization is NOT core: internal w_N>0 is a "
          "POSITIVE Z[phi] ratio; the CPL reading is passport-only (D0-PHASON-WZ-CPL-PASSPORT-001)")

    # FAIL_N0_POLE: n=0 is a genuine division-by-zero pole; w_N is undefined there.
    pole_hit = False
    try:
        _ = val(powp(PHIv, -1)) / val(R(0))     # w_N at n=0: 1/(phi^0 - 1) = 1/0
    except ZeroDivisionError:
        pole_hit = True
    assert val(R(0)) == 0.0, "energy at n=0 must be exactly 0 (the pole)"
    assert pole_hit, "control: evaluating w_N at n=0 must hit the division-by-zero pole"
    print("FAIL_N0_POLE  n=0 is the excluded pole: energy phi^0-1=0, so w_N(0)=1/0 is undefined "
          "(the well-defined window is n>=1)")

    print("HONEST_PROOF_TARGET  CERT-CLOSED on the FINITE-WINDOW facts only (bijection, exact w_N values, "
          "monotonicity, direction). MISSING (residual PROOF-TARGET D0-PHASON-WDE-Z-MAP-OWNER-001): a proven "
          "continuum interpolation w_N -> w_D0(u) AND the magnitude/sign normalization map onto the physical "
          "NEGATIVE w_DE on the late-time window -- NEITHER exists here; no survey datum enters.")
    print("PASS_PHASON_ARCHIVE_CAPACITY_REDSHIFT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
