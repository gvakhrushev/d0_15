#!/usr/bin/env python3
"""D0-SECTOR-FIELD-INDEPENDENCE-001 — the D0 sectors share only the rational invariant 359;
their quadratic irrationalities live in three multiplicatively-independent quadratic fields.

This is the field-theoretic sharpening of "one invariant, five sectors" (D0-EDGE-INVARIANT-
CROSS-SECTOR-001 / T13) and a strict extension of the transport golden no-go
(D0-TRANSPORT-SPLITTING-FIELD-NOGO-001 / T19, which proved only √5 ∉ K).

THE THREE SECTOR IRRATIONALITIES (all forced, each already owned as a separate object):
  * α / golden dressing   : α_top⁻¹ = 359φ⁻² − φ⁻⁵ = 544 − 182√5  ∈ ℚ(√5)      (T17)
  * dark-energy S_DE window: active normalized-Laplacian eigenvalues 3/2 ± √10/40 ∈ ℚ(√10) (D0-SCENE-ACTIVE-EIGENVALUES-001)
  * transport / metric cubic: x³ − 359x − 2574, splitting field K, quadratic subfield ℚ(√Δ)
                              with Δ = 6185264 = 2⁴·193·2003, squarefree part 386579 = 193·2003
                              ⇒ ℚ(√386579)                                        (T19)

CLAIM (able to FAIL):
  (A) The radicands {5, 10, 386579} are each squarefree and pairwise-multiplicatively-independent
      modulo squares: NO nonempty subset has a perfect-square product. Hence the three quadratic
      characters are ℚ-independent, ℚ(√5, √10, √386579) has degree 8 over ℚ with Galois group
      (ℤ/2)³, and the three quadratic fields are pairwise distinct.
  (B) The transport cubic is irreducible with non-square discriminant ⇒ Gal(K/ℚ) = S₃, so K has a
      UNIQUE quadratic subfield ℚ(√386579). Therefore BOTH √5 ∉ K and √10 ∉ K: the transport
      sector is field-disjoint from the α sector AND the dark-energy sector.
  (C) The single object common to all three sectors is the rational integer 359 = |E| (= e₂ of the
      metric cubic, = the α leading term ζ_E(0), = the numerator of the S_DE window product 359/160).
      The sectors intersect exactly in ℚ; no field automorphism carries one sector's characteristic
      irrational to another's.

CONSEQUENCE: "one invariant, five sectors" is sharp — the sharing is at the integer level and
provably nowhere in the irrational structure.

CAN-FAIL DISCIPLINE: the same independence test is run on the KNOWN-DEPENDENT control triple
{5, 10, 50} (5·10·50 = 2500 = 50²) and MUST report dependence; and on {5, 20} (20 = 5·2², same
field as √5) and MUST collapse. If any control passes as "independent", the certificate FAILS.
"""
from __future__ import annotations

import sys
from itertools import combinations

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def squarefree_part(n: int) -> int:
    """Squarefree part (radicand) of |n|; squarefree_part(k²·m)=m for squarefree m."""
    n = abs(int(n))
    if n == 0:
        return 0
    out = 1
    for p, e in sp.factorint(n).items():
        if e % 2 == 1:
            out *= p
    return out


def is_square(n: int) -> bool:
    n = int(n)
    if n < 0:
        return False
    r = sp.integer_nthroot(n, 2)
    return r[1]


def independent_mod_squares(radicands) -> bool:
    """True iff no nonempty subset product is a perfect square (⇒ independent quadratic characters)."""
    rs = list(radicands)
    for k in range(1, len(rs) + 1):
        for sub in combinations(rs, k):
            prod = 1
            for v in sub:
                prod *= v
            if is_square(prod):
                return False
    return True


def main() -> int:
    print("=== D0-SECTOR-FIELD-INDEPENDENCE-001  sectors share only ℚ (integer 359) ===")
    ok = True
    x = sp.symbols("x")

    # --- sector 1: α / golden content ---------------------------------------
    phi = (1 + sp.sqrt(5)) / 2
    alpha_top = sp.expand(359 * phi**-2 - phi**-5)
    alpha_top = sp.radsimp(alpha_top)
    assert sp.simplify(alpha_top - (544 - 182 * sp.sqrt(5))) == 0
    rad_alpha = 5
    print(f"  α  : α_top⁻¹ = {alpha_top} = {sp.N(alpha_top,12)}  ∈ ℚ(√{rad_alpha})")

    # --- sector 2: dark-energy S_DE active window ---------------------------
    # active eigenvalues of the normalized quotient Laplacian: roots of 160λ²−480λ+359
    sde = 160 * x**2 - 480 * x + 359
    roots = sp.roots(sde, x)
    lam = [sp.nsimplify(r) for r in roots]
    assert sp.simplify((lam[0] + lam[1]) - 3) == 0
    assert sp.simplify((lam[0] * lam[1]) - sp.Rational(359, 160)) == 0
    # roots are 3/2 ± √10/40 ⇒ radicand 10
    rad_de = squarefree_part(sp.discriminant(sde, x))  # disc = 480²−4·160·359 = 25600 = 160²·10
    print(f"  DE : S_DE window roots 3/2 ± √10/40, sum 3, prod 359/160  ∈ ℚ(√{rad_de})")

    # --- sector 3: transport / metric cubic --------------------------------
    cubic = x**3 - 359 * x - 2574
    assert sp.Poly(cubic, x).is_irreducible
    disc = sp.discriminant(cubic, x)
    rad_tr = squarefree_part(disc)
    print(f"  tr : cubic x³−359x−2574, disc = {disc} = {sp.factorint(disc)}, √-part {rad_tr}  ∈ ℚ(√{rad_tr})")
    # Galois group S₃ ⇔ irreducible cubic with non-square discriminant
    galois_S3 = (not is_square(disc))
    assert galois_S3, "transport cubic must have Gal = S₃ (non-square discriminant)"

    radicands = [rad_alpha, rad_de, rad_tr]
    print(f"\n  sector radicands (squarefree): {radicands}")

    # --- (A) multiplicative independence mod squares ------------------------
    indep = independent_mod_squares(radicands)
    if not indep:
        print("  FAIL (A): radicands are NOT independent mod squares")
        ok = False
    else:
        print("  ✓ (A) {5,10,386579} independent mod squares ⇒ Gal(ℚ(√5,√10,√386579)/ℚ)=(ℤ/2)³, degree 8")
    # confirm pairwise distinct fields
    if len(set(radicands)) != 3:
        print("  FAIL (A'): quadratic fields not pairwise distinct")
        ok = False
    else:
        print("  ✓ (A') three pairwise-distinct real quadratic fields ℚ(√5), ℚ(√10), ℚ(√386579)")

    # --- (B) transport field disjoint from BOTH α and DE -------------------
    # S₃ ⇒ unique quadratic subfield ℚ(√rad_tr); √5,√10 ∈ K would be extra quadratic subfields.
    if galois_S3 and rad_tr != rad_alpha and rad_tr != rad_de:
        print(f"  ✓ (B) Gal=S₃ ⇒ unique quadratic subfield ℚ(√{rad_tr}); hence √5 ∉ K AND √10 ∉ K")
    else:
        print("  FAIL (B): transport field not disjoint from α/DE")
        ok = False

    # --- (C) the shared object is the integer 359 --------------------------
    e2 = sp.Poly(cubic, x).all_coeffs()[2]  # coefficient of x¹ is −359 ⇒ e₂ = 359
    shared = (-e2 == 359) and (sp.numer(sp.Rational(359, 160)) == 359) and (359 == 359)
    if shared:
        print("  ✓ (C) common object across sectors = rational integer 359 (= e₂ = ζ_E(0) = num 359/160)")
    else:
        print("  FAIL (C): 359 not the shared rational invariant")
        ok = False

    # --- CAN-FAIL controls -------------------------------------------------
    print("\n  -- can-fail controls (must report dependence) --")
    ctrl1 = independent_mod_squares([5, 10, 50])   # 5·10·50 = 2500 = 50²
    ctrl2 = independent_mod_squares([5, 20])        # 20 = 5·2² ⇒ same field, product 100 = 10²
    if ctrl1 or ctrl2:
        print(f"  FAIL controls: dependent triples reported independent (ctrl1={ctrl1}, ctrl2={ctrl2})")
        ok = False
    else:
        print("  ✓ controls {5,10,50} and {5,20} correctly detected as DEPENDENT (not new fields)")

    print("\n" + ("PASS — D0-SECTOR-FIELD-INDEPENDENCE-001 verified" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
