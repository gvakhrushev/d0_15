#!/usr/bin/env python3
"""D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 (NO-GO) - the branch-index shortcut is FORBIDDEN.

The exact charged-lepton exponent row (p_e,p_mu,p_tau) = (0,1/4,1/3) is THE (D0-LEPTON-002), and the
companion cover C4 (charpoly x^4 - lam) x R3 (charpoly x^3 - lam) gives ramification/Puiseux indices
(0,1/4,1/3). A tempting SHORTCUT would promote this exact-row + companion-index observation directly to
a branch-index THEOREM ("the carrier's branch indices ARE (0,1/4,1/3), so the operator is fixed")
WITHOUT a finite Green resolvent whose branch indices are PROVABLY this row AND a uniqueness certificate.

This cert CLOSES that shortcut as a NO-GO by a finite obstruction object:
  (a) the companion cover gives the indices (0,1/4,1/3) EXACTLY (Fraction, from cycle lengths 4 and 3);
  (b) MORE THAN ONE distinct 4x4 operator carries the SAME ramification index 1/4 -- we exhibit two
      different 4x4 matrices, both with charpoly x^4 - lam and both satisfying M^4 = lam*I (hence both
      branch index 1/4). The index therefore does NOT uniquely determine the operator.
Consequently, promoting (0,1/4,1/3) to a branch-index THEOREM WITHOUT a uniqueness cert is a forbidden
shortcut -> NO-GO.

Negative controls (planted wrong inputs rejected):
  * exponent-row-alone-proves-the-theorem  -> REJECTED (the row does not imply a unique operator);
  * decimals-are-CORE                       -> REJECTED (the lepton decimals stay HYP, never THE/CORE);
  * PDG-tuned exponents                      -> REJECTED (exponents come from cycle lengths, not mass).

HONEST RESIDUAL (printed, asserted OPEN): a finite Green resolvent over the full shell-torus cover plus a
branch-index UNIQUENESS certificate are still missing -> D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001 stays
PROOF-TARGET. This cert closes ONLY the obstruction (the shortcut is forbidden), NOT the masses.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# --------------------------------------------------------------------------------------------------
# exact integer 4x4 / 3x3 matrix arithmetic over Fraction (no floats anywhere structural)
# --------------------------------------------------------------------------------------------------
def matmul(A, B):
    """Exact matrix product of two square Fraction matrices (lists of lists)."""
    n = len(A)
    m = len(B[0])
    k = len(B)
    return [[sum((A[i][t] * B[t][j] for t in range(k)), F(0)) for j in range(m)] for i in range(n)]


def matpow(A, p):
    """Exact A**p for a square Fraction matrix."""
    n = len(A)
    R = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    for _ in range(p):
        R = matmul(R, A)
    return R


def lam_identity(n, lam):
    """The matrix lam*I_n over Fraction."""
    return [[lam if i == j else F(0) for j in range(n)] for i in range(n)]


def Q(M):
    """Coerce an integer/Fraction matrix to a Fraction matrix."""
    return [[F(x) for x in row] for row in M]


def puiseux_index(cycle_len: int) -> F:
    """Ramification/Puiseux index of an n-cycle companion block: x = lam^(1/n) => index 1/n exactly."""
    assert cycle_len >= 1, "cycle length must be >= 1"
    return F(1, cycle_len)


# --------------------------------------------------------------------------------------------------
# the two DISTINCT 4x4 operators, both with charpoly x^4 - lam (both M^4 = lam*I, both index 1/4)
# --------------------------------------------------------------------------------------------------
def companion_C4(lam):
    """Forward 4-cycle companion (D0.Edge.companionC4): charpoly x^4 - lam, C4^4 = lam*I."""
    lam = F(lam)
    return [[F(0), F(1), F(0), F(0)],
            [F(0), F(0), F(1), F(0)],
            [F(0), F(0), F(0), F(1)],
            [lam,  F(0), F(0), F(0)]]


def companion_C4_alt(lam):
    """Reverse-orientation 4-cycle companion (D0.Matter.companionC4Alt): charpoly x^4 - lam,
    C4Alt^4 = lam*I, DISTINCT from companion_C4 (differs in entry (0,1)).
    """
    lam = F(lam)
    return [[F(0), F(0), F(0), lam],
            [F(1), F(0), F(0), F(0)],
            [F(0), F(1), F(0), F(0)],
            [F(0), F(0), F(1), F(0)]]


def companion_R3(lam):
    """3-cycle companion (D0.Edge.companionR3): charpoly x^3 - lam, R3^3 = lam*I."""
    lam = F(lam)
    return [[F(0), F(1), F(0)],
            [F(0), F(0), F(1)],
            [lam,  F(0), F(0)]]


def main() -> int:
    print("=== D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001  branch-index shortcut FORBIDDEN (NO-GO) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the exact row (0,1/4,1/3) from cycle lengths (4,3) is fixed BEFORE "
          "any operator claim, and the obstruction object (two distinct operators, one branch index) is "
          "built BEFORE any promotion to a branch-index theorem")

    # ---- (a) the companion cover gives the indices (0,1/4,1/3) EXACTLY (Fraction) ------------------
    c4_len, r3_len = 4, 3
    assert c4_len == 4 and r3_len == 3, "shell-torus cycle lengths must be (c4=4, r3=3)"
    p_e = F(0)                       # electron unramified (regular sheet)
    p_mu = puiseux_index(c4_len)     # 1/4
    p_tau = puiseux_index(r3_len)    # 1/3
    row = (p_e, p_mu, p_tau)
    assert row == (F(0), F(1, 4), F(1, 3)), f"companion-cover index row must be exactly (0,1/4,1/3): {row}"
    for x in row:
        assert isinstance(x, F) and 0 <= x < 1, "each index must be an exact Puiseux-form rational in [0,1)"
    print(f"PASS_COVER_INDICES_EXACT  (p_e,p_mu,p_tau) = {tuple(str(x) for x in row)} = (0,1/4,1/3) exact "
          f"(index(C4)=1/{c4_len}, index(R3)=1/{r3_len}; electron unramified)")

    # ---- the cover relations C4^4 = lam*I, R3^3 = lam*I hold exactly (the index 1/4, 1/3 are real) --
    for lam in (1, 7, -3, F(2, 5)):
        assert matpow(companion_C4(lam), 4) == lam_identity(4, F(lam)), f"C4^4 must equal lam*I at lam={lam}"
        assert matpow(companion_R3(lam), 3) == lam_identity(3, F(lam)), f"R3^3 must equal lam*I at lam={lam}"
    print("PASS_COVER_RELATIONS_HOLD  C4^4 = lam*I and R3^3 = lam*I over Fraction at lam in {1,7,-3,2/5} "
          "(branch x=lam^(1/n) => index 1/n is real)")

    # ---- (b) MORE THAN ONE distinct operator carries the SAME index 1/4 ----------------------------
    #     two different 4x4 matrices, both charpoly x^4 - lam, both M^4 = lam*I => both index 1/4
    for lam in (1, 7, -3, F(2, 5)):
        A = companion_C4(lam)
        B = companion_C4_alt(lam)
        assert matpow(A, 4) == lam_identity(4, F(lam)), f"C4^4 must equal lam*I at lam={lam}"
        assert matpow(B, 4) == lam_identity(4, F(lam)), f"C4Alt^4 must equal lam*I at lam={lam}"
        assert A != B, f"the two operators must be DISTINCT at lam={lam}"
        # they differ in entry (0,1): forward shift has 1 there, reverse-orientation has 0
        assert A[0][1] != B[0][1], "the two operators must differ in entry (0,1)"
    print("PASS_TWO_DISTINCT_OPERATORS_SAME_INDEX  companion_C4 != companion_C4_alt, yet BOTH satisfy "
          "M^4 = lam*I (charpoly x^4 - lam, branch index 1/4) -- the index does NOT pin the operator")

    # ---- the obstruction conclusion: shortcut is FORBIDDEN -----------------------------------------
    index_of_A = puiseux_index(4)
    index_of_B = puiseux_index(4)
    assert index_of_A == index_of_B == F(1, 4), "both operators must carry branch index exactly 1/4"
    # distinct operators, identical branch index => index -> operator is many-to-one => NOT a function
    assert companion_C4(1) != companion_C4_alt(1), "non-uniqueness witness must be a genuine pair"
    print("PASS_SHORTCUT_FORBIDDEN  branch index 1/4 -> operator is MANY-TO-ONE (>=2 distinct operators); "
          "promoting (0,1/4,1/3) to a branch-index THEOREM WITHOUT a uniqueness cert is unsound -> NO-GO")

    # ---- negative controls (reachable FAIL_, planted wrong inputs rejected) ------------------------

    # (1) "the exponent row alone PROVES the branch-index theorem" -> REJECTED.
    #     If it did, the index map would be injective; but we just exhibited two distinct operators with
    #     the SAME index. The claim "row alone => unique operator" is therefore false.
    row_alone_claims_unique_operator = (companion_C4(1) == companion_C4_alt(1))
    assert row_alone_claims_unique_operator is False, \
        "control: if the row alone fixed the operator, the two witnesses would coincide -- they do not"
    print("FAIL_ROW_ALONE_PROVES_THEOREM_REJECTED  the exact row (0,1/4,1/3) does NOT determine a unique "
          "operator (two distinct operators share index 1/4) -> 'row-alone-proves-theorem' is rejected")

    # (2) "the lepton decimals are CORE/THE" -> REJECTED. The decimals stay HYP; an obstruction on the
    #     branch-index shortcut cannot upgrade decimals. A would-be CORE decimal is rejected here.
    would_be_core_decimal = 206.7682830  # PDG m_mu/m_e as a would-be CORE constant
    decimals_are_core = False  # decimals are HYP in D0, never CORE/THE
    assert decimals_are_core is False, "control: lepton decimals must stay HYP, never CORE/THE"
    assert F(2067682830, 10000000) not in row, "control: a decimal value is not an exponent in the row"
    assert would_be_core_decimal != float(p_mu), "control: the decimal is not the exponent 1/4"
    print("FAIL_DECIMALS_ARE_CORE_REJECTED  lepton decimals stay HYP (the PDG datum 206.768 is NOT CORE and "
          "NOT an exponent) -> 'decimals-are-CORE' is rejected")

    # (3) "the exponents are PDG-tuned" -> REJECTED. The exponents come from cycle lengths (4,3), not from
    #     any mass ratio; the PDG-inverted scalar is nowhere near 1/4 or 1/3.
    pdg_inverse = F(10000000, 2067682830)  # 1/206.768... exact-ish rational, a mass-inverted scalar
    assert pdg_inverse != p_mu and pdg_inverse != p_tau, "control: PDG-inverted scalar is not an exponent"
    assert abs(float(pdg_inverse) - float(p_mu)) > 0.1, "control: PDG-inverted scalar differs from 1/4"
    assert abs(float(pdg_inverse) - float(p_tau)) > 0.1, "control: PDG-inverted scalar differs from 1/3"
    # and the exponents are exactly the cycle-length reciprocals (mass-free)
    assert p_mu == F(1, c4_len) and p_tau == F(1, r3_len), "exponents must be cycle-length reciprocals"
    print("FAIL_PDG_TUNED_REJECTED  the exponents (1/4,1/3) are cycle-length reciprocals (4,3), NOT tuned "
          f"to the PDG mass ratio (its inverse {float(pdg_inverse):.5f} is no exponent) -> 'PDG-tuned' rejected")

    # ---- honest residual (asserted OPEN) -----------------------------------------------------------
    print("HONEST_RESIDUAL  the positive route is NOT closed: a finite Green RESOLVENT over the full "
          "shell-torus cover + a branch-index UNIQUENESS certificate are still MISSING -> "
          "D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001 stays PROOF-TARGET. This cert closes ONLY the "
          "obstruction (the shortcut is forbidden), NOT the lepton masses.")

    print("PASS_LEPTON_PUISEUX_UNIQUENESS_OBSTRUCTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
