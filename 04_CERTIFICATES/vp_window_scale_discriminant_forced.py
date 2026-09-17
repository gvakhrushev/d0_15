#!/usr/bin/env python3
"""vp_window_scale_discriminant_forced - D0-WINDOW-SCALE-DISCRIMINANT-FORCED-001 (POSITIVE + honest rejection).

An exact forced closed form for the S_DE window-scale splitting, plus the disciplined finding that the sqrt10
field of the scene is a SIZE-fingerprint, not a forced golden-departure (rejecting the tempting
"sign of sqrt10 = orientation bit" reading out loud).

Setup. The two nontrivial normalized-Laplacian eigenvalues of the scene (the S_DE window scales
lambda_c, lambda_r, D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001 / D0-SCENE-ACTIVE-EIGENVALUES-001) satisfy
lambda_c + lambda_r = 3 = Z (owned trace identity) and lambda_c * lambda_r = |E|/160 = 359/160. Their
splitting is governed by the discriminant D = (lambda_r - lambda_c)^2 = 9 - 4*(product).

Forced closed form. For a general +2 zone progression {m, m+2, m+4} (N = 3m+6), the product of the two
nontrivial normalized-Laplacian eigenvalues is the RATIONAL e2 of I - R (R the zero-diagonal symmetric
reduced matrix, R_ij^2 = n_i n_j / (d_i d_j), d_i = N - n_i), giving
    P(m) = (9m^2 + 36m + 24) / (4m^2 + 16m + 12),
    D(m) = 9 - 4 P(m) = 3 / ((m+1)(m+3)).
Since degrees are d = 2(m+3), 2(m+2), 2(m+1), the denominator is the product of the SMALLEST and LARGEST
degree-halves: D(m) = Z / (h_min * h_max) with Z = 3, h_min = m+1 = d_min/2, h_max = m+3 = d_max/2. At the
scene m = 9: D = 3/(10*12) = 1/40, so lambda = 3/2 +- sqrt(D)/2 = 3/2 +- sqrt(10)/40 -- reproducing the
corpus eta_EP = sqrt(10)/40 exactly, now from a closed form rather than a bare readout.

Honest rejection (the discipline). D(m) = 3/((m+1)(m+3)) > 0 for every valid m, so the two window scales
are ALWAYS real and distinct: the "orientation = sign of the discriminant" reading (BOOK_01) yields a
CONSTANT (+) orientation, never a Z_2 flip. Hence sqrt10 is NOT an orientation bit. Moreover the field is
Q(sqrt(squarefree(3(m+1)(m+3)))), a pure SIZE-fingerprint: the golden field Q(sqrt5) occurs at m = 29
(zones 29,31,33), NOT at the scene m = 9. The scene's sqrt10 = squarefree(3*10*12) = squarefree(360) = 10
carries no forced "departure from golden" meaning. What IS forced is the closed form and the trace sum 3;
the specific surd is size-specific and is claimed as such. (The earlier NO-GO that sqrt10 !in Q(phi),
D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001, stays correct and is now explained: it is generic, not a near-miss.)

Falsifiable: breaks (rc=1) if D(m) != 3/((m+1)(m+3)) at sampled m, if the scene value != 1/40, if the field
surd at m=9 is not 10 or at m=29 is not 5, or if the (rejected) positivity/orientation claims are flipped.
"""
import sys
from fractions import Fraction as Fr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)


def squarefree_part(num, den):
    """squarefree part of the rational num/den (times den to clear denom): squarefree(num*den)."""
    v = num * den
    sf = 1
    d = 2
    while d * d <= v:
        e = 0
        while v % d == 0:
            v //= d
            e += 1
        if e % 2 == 1:
            sf *= d
        d += 1
    if v > 1:
        sf *= v
    return sf


def window_product(m):
    """Exact rational product of the two nontrivial normalized-Laplacian eigenvalues, zones {m,m+2,m+4}."""
    n = [m, m + 2, m + 4]
    N = sum(n)
    d = [N - x for x in n]
    # P = 3 - sum_{i<j} n_i n_j/(d_i d_j)   (e2 of I - R, R zero-diagonal)
    S2 = sum(Fr(n[i] * n[j], d[i] * d[j]) for i in range(3) for j in range(i + 1, 3))
    return Fr(3) - S2


def main():
    print("=== vp_window_scale_discriminant_forced  D(m)=3/((m+1)(m+3)), sqrt10 is a size-fingerprint ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the +2 zone progression is M1-forced; D(m) and its field are the "
          "computed consequence. The field VALUE is claimed as size-specific, not as a forced golden-miss.")

    # forced closed form D(m) = 3/((m+1)(m+3)) verified against the exact eigenvalue product
    for m in [1, 3, 5, 7, 9, 11, 13, 15, 29, 41]:
        P = window_product(m)
        D = Fr(9) - 4 * P
        closed = Fr(3, (m + 1) * (m + 3))
        if D != closed:
            die(f"CLOSED_FORM  D({m})={D} != 3/((m+1)(m+3))={closed}")
        if P + P != P * 2:  # trivial guard keeps P referenced
            die("unreachable")
    print("PASS_DISCRIMINANT_CLOSED_FORM  D(m) = (w_r - w_c)^2 = 9 - 4·product = 3/((m+1)(m+3)) verified "
         "exactly at m = 1,3,5,7,9,11,13,15,29,41 (product = e2 of the reduced normalized Laplacian).")

    # degree-half reading: denominator = (d_min/2)(d_max/2)
    m = 9
    N = 3 * m + 6
    degs = sorted(N - x for x in [m, m + 2, m + 4])  # [20,22,24]
    h_min, h_max = degs[0] // 2, degs[-1] // 2       # 10, 12
    if (m + 1, m + 3) != (h_min, h_max):
        die(f"DEGREE_HALF  (m+1,m+3)=({m+1},{m+3}) must equal (d_min/2,d_max/2)=({h_min},{h_max})")
    print(f"PASS_DEGREE_HALF_DENOMINATOR  denom (m+1)(m+3) = (d_min/2)(d_max/2) = {h_min}·{h_max}: "
          f"D = Z / (h_min·h_max) with Z = 3 (zone count).")

    # scene value reproduces sqrt10/40
    Dscene = Fr(3, (9 + 1) * (9 + 3))
    if Dscene != Fr(1, 40):
        die(f"SCENE_VALUE  D(9) must be 1/40: {Dscene}")
    # lambda = 3/2 +- sqrt(D)/2 ; sqrt(1/40)/2 = sqrt(10)/40 since sqrt(1/40)=sqrt(10)/20
    # check 40 * (sqrt10/40)^2 *? -> verify (sqrt(D)/2)^2 == (sqrt10/40)^2 => D/4 == 10/1600 => 1/160==1/160
    if Fr(1, 40) / 4 != Fr(10, 1600):
        die("SCENE_SPLIT  (sqrt(D)/2)^2 must equal (sqrt10/40)^2 = 10/1600")
    print("PASS_SCENE_REPRODUCES_SQRT10  D(9) = 1/40, so lambda = 3/2 ± sqrt(1/40)/2 = 3/2 ± sqrt(10)/40 "
          "= corpus eta_EP — the bare readout is now a closed-form consequence.")

    # ALWAYS positive -> always real & distinct -> constant orientation, no Z_2 flip
    for m in range(1, 200):
        if Fr(3, (m + 1) * (m + 3)) <= 0:
            die(f"POSITIVITY  D({m}) must be > 0")
    print("PASS_ALWAYS_POSITIVE_NO_ORIENTATION_FLIP  D(m) = 3/((m+1)(m+3)) > 0 for all m: the two window "
          "scales are ALWAYS real & distinct, so 'orientation = sign of discriminant' is CONSTANT (+) — "
          "sqrt10 is NOT a Z_2 orientation bit. That tempting reading is REJECTED.")

    # field is a size-fingerprint: golden at m=29, not the scene m=9
    sf_scene = squarefree_part(3, (9 + 1) * (9 + 3))          # squarefree(3*120)=squarefree(360)=10
    sf_golden = squarefree_part(3, (29 + 1) * (29 + 3))       # squarefree(3*960)=squarefree(2880)=5
    sf_rational = squarefree_part(3, (5 + 1) * (5 + 3))       # squarefree(3*48)=squarefree(144)=1
    if sf_scene != 10:
        die(f"SCENE_FIELD  scene surd must be 10: {sf_scene}")
    if sf_golden != 5:
        die(f"GOLDEN_AT_29  golden field sqrt5 must occur at m=29: {sf_golden}")
    if sf_rational != 1:
        die(f"RATIONAL_AT_5  m=5 must give rational scales: {sf_rational}")
    print(f"PASS_FIELD_IS_SIZE_FINGERPRINT  field = Q(sqrt(squarefree(3(m+1)(m+3)))): scene m=9 -> sqrt10, "
          f"golden Q(sqrt5) at m=29 (zones 29,31,33) NOT the scene, m=5 -> rational. So sqrt10 is the "
          f"fingerprint of sizes 9,11,13 — no forced golden-departure meaning; claimed as size-specific.")

    print("PASS_WINDOW_SCALE_DISCRIMINANT_FORCED — exact forced closed form D(m)=3/((m+1)(m+3)) reproduces "
          "the scene's sqrt10/40; the surd itself is a size-fingerprint (golden at m=29, not m=9) and the "
          "always-positive discriminant refutes any sqrt10-as-orientation-bit reading.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
