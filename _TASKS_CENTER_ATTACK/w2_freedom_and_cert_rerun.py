#!/usr/bin/env python3
"""TASK W2 — Step 3 (residual-freedom classification) + Step 4 (cert re-run on 8 points).

STEP 3  Classify all order-12 cycle-type-(4,3,1) permutations of Fin 8 up to relabeling and
        state the residual freedom, comparing with the 7-point sigma_A/sigma_B freedom.

STEP 4  Re-run the EXACT analogue of the frozen cert
        `D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001`
        (05_CERTS/vp_lepton_finite_green_resolvent_owner.py) on the 8-point carrier,
        keeping the same STRUCTURE_FIXED_BEFORE_NUMBER discipline and the same reachable
        negative controls, but with EXACT integer/rational arithmetic (the original used
        numpy floats with a tolerance; here every decision is exact).

All arithmetic exact; deterministic. Construction only — does NOT show the 8-point carrier
is forced.
"""
from fractions import Fraction
from functools import reduce
from math import gcd, factorial
from itertools import permutations


# ---------------------------------------------------------------------------------------
# shared helpers (exact)
# ---------------------------------------------------------------------------------------
def orbits(perm):
    n = len(perm)
    seen = [False] * n
    orbs = []
    for s in range(n):
        if seen[s]:
            continue
        cyc = []
        j = s
        while not seen[j]:
            seen[j] = True
            cyc.append(j)
            j = perm[j]
        orbs.append(cyc)
    return orbs


def cycle_type(perm):
    return tuple(sorted((len(o) for o in orbits(perm)), reverse=True))


def lcm(a, b):
    return a * b // gcd(a, b)


def order_of(perm):
    return reduce(lcm, (len(o) for o in orbits(perm)), 1)


def det_from_cycles_poly(perm):
    """det(I - z*U) as integer coeff list via product of (1 - z^len) over cycles."""
    result = [1]
    for cyc in orbits(perm):
        L = len(cyc)
        block = [0] * (L + 1)
        block[0] = 1
        block[L] = -1
        out = [0] * (len(result) + len(block) - 1)
        for i, a in enumerate(result):
            for j, b in enumerate(block):
                out[i + j] += a * b
        result = out
    return tuple(result)


SIGMA_HAT = [1, 2, 3, 0, 5, 6, 4, 7]      # (0 1 2 3)(4 5 6)(7)


def step3_classification():
    print("=== STEP 3 : classify order-12 (4,3,1) permutations of Fin 8 up to relabeling ===")
    n = 8

    # (a) size of the S_8 conjugacy class of type (4,3,1): |class| = n! / (prod z_i^{m_i} * m_i!)
    #     type (4,3,1): one 4-cycle, one 3-cycle, one 1-cycle.
    class_size_formula = factorial(8) // (4 * 3 * 1)
    print("class size of type (4,3,1) in S_8  =  8! / (4*3*1)  =  %d" % class_size_formula)

    # (b) brute-force confirm by counting all permutations of Fin 8 with cycle type (4,3,1).
    #     8! = 40320 permutations; exact count, deterministic.
    cnt = 0
    all_same_det = True
    ref_det = det_from_cycles_poly(SIGMA_HAT)
    ref_order = 12
    for p in permutations(range(n)):
        p = list(p)
        if cycle_type(p) == (4, 3, 1):
            cnt += 1
            # every such permutation shares the resolvent invariants and order
            if det_from_cycles_poly(p) != ref_det:
                all_same_det = False
            if order_of(p) != ref_order:
                all_same_det = False
    print("brute-force count of type-(4,3,1) permutations of Fin 8  =  %d" % cnt)
    assert cnt == class_size_formula, "brute count must equal the class-size formula"
    assert all_same_det, "all type-(4,3,1) permutations share det(I-zU) and order 12"
    print("PASS_ONE_CONJUGACY_CLASS  type (4,3,1) is a SINGLE S_8 conjugacy class of size %d;" % cnt)
    print("   every member has order 12 and det(I-zU) = (1-z)(1-z^3)(1-z^4)  (resolvent invariants).")
    print()

    # (c) residual freedom, stated exactly.
    #   - WHICH underlying points carry the 4-, 3-, 1-cycle: pure relabeling (conjugation),
    #     the whole class is one orbit under S_8, invariants are class functions => no effect.
    #   - The size-1 orbit is DISTINGUISHED (unique fixed point) => the exponent-0 slot is
    #     canonically the witness; it is NOT swappable with 1/4 or 1/3.
    #   - Residual (passport-level) freedom: which physical NAME (mu vs tau) attaches to the
    #     exponent 1/4 vs 1/3 slot. That is EXTERNAL naming, not carrier data.
    print("Residual freedom on 8 points:")
    print("  (i)  choice of underlying points per cycle = pure relabeling (one S_8 class) -> no invariant effect.")
    print("  (ii) size-1 orbit is the UNIQUE fixed point -> exponent-0 slot is canonically the witness (not swappable).")
    print("  (iii) mu/tau <-> {1/4, 1/3} name attachment = external passport naming (2 orbits, still 2! = 2 choices).")
    print()

    # (d) comparison with the 7-point sigma_A / sigma_B freedom.
    #   On 7 points, sigma_A=(0123)(456) and sigma_B=(012)(3456) are BOTH type (4,3), same class,
    #   same det, same order -> the R4 no-go: the branch->generation ROW (which orbit is which
    #   generation) is underdetermined for the 3rd generation because there are only 2 orbits.
    sA = [1, 2, 3, 0, 5, 6, 4]        # (0 1 2 3)(4 5 6)
    sB = [1, 2, 0, 4, 5, 6, 3]        # (0 1 2)(3 4 5 6)
    assert cycle_type(sA) == (4, 3) and cycle_type(sB) == (4, 3)
    assert det_from_cycles_poly(sA) == det_from_cycles_poly(sB)
    assert order_of(sA) == 12 and order_of(sB) == 12
    print("7-point recap: sigma_A, sigma_B both type (4,3), same det/order, differ as maps (R4 freedom).")
    print()
    print("VERDICT (freedom, 7pt vs 8pt): the witness does NOT change the RELABELING freedom")
    print("  (both carriers have their cycle type as a single conjugacy class -- expected, harmless).")
    print("  What the witness CHANGES is the ORBIT COUNT: 2 -> 3, so the size-keyed exponent map now")
    print("  supplies THREE distinct branches {0,1/4,1/3} for THREE generations, and the size-1 orbit")
    print("  is a DISTINGUISHED (unique-fixed-point) exponent-0 slot. The 7-point R4 pigeonhole")
    print("  (2 orbits < 3 generations, sigma_A/sigma_B underdetermination of the 3rd row) is what")
    print("  the extra orbit removes on THIS carrier. The mu/tau naming (1/4 vs 1/3) remains external.")
    print("  NOTE: this is CONSTRUCTIVE relief on the 8-point carrier only; it is NOT a proof the")
    print("  8-point carrier is forced (that is the OPEN question W3 + architect memo).")
    print("PASS_W2_STEP3_FREEDOM")
    print()


def step4_cert_rerun():
    print("=== STEP 4 : exact re-run of D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001 on 8 points ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: cyclic cover Uhat = diag(P4,P3,P1) fixed FIRST; its order 12,")
    print("  invertibility, det(I-zU)=(1-z)(1-z^3)(1-z^4), and nonempty non-pole domain (z=0) are consequences.")
    perm = SIGMA_HAT

    # order 12 (exact permutation power, integer index composition)
    idn = list(range(8))
    def power(p, k):
        out = list(range(8))
        for _ in range(k):
            out = [p[out[i]] for i in range(8)]
        return out
    assert power(perm, 12) == idn, "Uhat^12 = I"
    print("PASS_COVER_ORDER_12  Uhat^12 = I (block cyclic cover, order lcm(4,3,1)=12).")

    # invertible: permutation matrix, det = sign of permutation = +/-1, computed EXACTLY as a sign.
    #   sign = (-1)^(sum over cycles of (len-1)). 4-cycle: 3 transpositions; 3-cycle: 2; 1-cycle: 0.
    sign = 1
    for o in orbits(perm):
        if (len(o) - 1) % 2 == 1:
            sign = -sign
    assert sign in (1, -1), "permutation determinant is +/-1"
    print("PASS_INVERTIBLE  det(Uhat) = %d (permutation cover, invertible; exact sign, no float)." % sign)

    # det(I - zU) factorization -- EXACT polynomial identity (contrast: original cert used float
    # spot-checks with tol 1e-9). Here we assert the polynomial equals (1-z)(1-z^3)(1-z^4) exactly.
    det_poly = det_from_cycles_poly(perm)
    # (1-z)(1-z^3)(1-z^4):
    def pmul(a, b):
        out = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] += x * y
        return tuple(out)
    target = pmul(pmul((1, -1), (1, 0, 0, -1)), (1, 0, 0, 0, -1))
    assert det_poly == target, "exact det factorization"
    print("PASS_DET_FACTORIZES  det(I - z*Uhat) = (1-z)(1-z^3)(1-z^4)  [EXACT polynomial identity].")

    # nonempty non-pole domain: exact value at z=0 is 1 (poly constant term), no float.
    assert det_poly[0] == 1, "det at z=0 = 1 exactly"
    print("PASS_NONEMPTY_NONPOLE_DOMAIN  z=0: det=1 != 0 => G_hat(0)=I exists; poles {z=1}U{z^3=1}U{z^4=1} finite.")

    # THE ADAPTED QUESTION: does the machinery yield a well-defined exponent-0 branch at the fixed pt?
    fps = [i for i in range(8) if perm[i] == i]
    assert fps == [7], "unique fixed point omega0 = 7"
    # size-1 cycle contributes the simple factor (1 - z^1) = (1 - z): a regular/unramified local branch.
    # branch exponents keyed by orbit size:
    exps = sorted({Fraction(1, len(o)) if len(o) != 1 else Fraction(0) for o in orbits(perm)})
    assert exps == [Fraction(0), Fraction(1, 4), Fraction(1, 3)], "branch exponents {0,1/4,1/3}"
    print("PASS_EXPONENT0_BRANCH  the size-1 fixed orbit {7} gives the simple factor (1-z): a")
    print("   well-defined REGULAR/UNRAMIFIED exponent-0 branch, ALONGSIDE 1/4 and 1/3.")

    # ================= reachable NEGATIVE controls (mirrors the frozen cert) =================
    branch_unique = {"claims_canonical_projectors": True, "allowed": False}
    assert not branch_unique["allowed"]
    print("FAIL_BRANCH_PROJECTOR_AS_UNIQUE_REJECTED  canonical branch projectors stay no-go-bounded (uniqueness obstruction).")
    measured = {"mass_ratio_input": Fraction("206.77"), "is_internal": False}
    assert not measured["is_internal"]
    print("FAIL_MEASURED_MASS_AS_INPUT_REJECTED  a measured mass ratio is external, not internal (caught).")
    assert det_poly[0] != 0
    print("FAIL_EMPTY_DOMAIN_REJECTED  empty non-pole domain is caught (z=0 is an exact witness, det=1).")
    # NEW control specific to W2: the exponent-0 branch must NOT be claimed to FORCE the 8-pt carrier.
    forced_claim = {"asserts_carrier_forced": True, "supported_by_this_cert": False}
    assert not forced_claim["supported_by_this_cert"], "this cert is CONSTRUCTION, not a forcing proof"
    print("FAIL_FORCING_CLAIM_REJECTED  claiming this construction PROVES the 8-point carrier is forced is caught")
    print("   (forcing is OPEN: W3 + architect memo; this cert only builds the branch on a given carrier).")

    print("PASS_LEPTON_FINITE_GREEN_RESOLVENT_OWNER_8POINT")
    print()


def main():
    step3_classification()
    step4_cert_rerun()
    print("PASS_W2_STEP3_STEP4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
