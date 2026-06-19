#!/usr/bin/env python3
"""D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001 (CERT-CLOSED, narrow arithmetic + identity, NO uniqueness).

Front F3. The charged-lepton shell-torus cover is built from cyclic companion blocks
(D0-EDGE-RAMIFICATION-001): the 4-cycle C4 (charpoly x^4 - lam) and the 3-cycle R3 (charpoly x^3 - lam).
At a branch point the cover z^n - lam solves as z = lam^(1/n), so the Puiseux/ramification exponent of an
n-cycle is 1/n and the ramification index is n.

This cert machine-checks, with exact Fraction/integer arithmetic (no floats anywhere structural):
  (a) the cyclic relations C4^4 = lam*I and R3^3 = lam*I over Fraction;
  (b) the ramification exponent 1/n for n = 2..5 (index = n, exponent = 1/n exact);
  (c) the Riemann-Hurwitz GENUS-0 CONSISTENCY identity: for a connected cyclic degree-n cover of P^1 with
      total ramification defect 2(n-1) (totally ramified over two branch points), the genus g solves
      2 - 2g = n*2 - 2(n-1) = 2, hence g = 0 -- for EVERY n = 2..5 (integer identity).

HONESTY BOUNDARY -- what is NOT claimed:
  * Riemann-Hurwitz does NOT force the pair (4,3) uniquely. EVERY connected cyclic cover is genus 0, so
    the genus identity holds for n = 2,3,4,5 alike. The negative control FAIL_RH_FORCES_PAIR_43_REJECTED
    fires on the false "R-H makes (4,3) unique" claim.
  * No PDG mass enters (FAIL_PDG_MASS_INPUT_REJECTED).
  * The branch index does NOT determine the operator -- that shortcut is independently FORBIDDEN by
    D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 (two distinct 4x4 operators, same index 1/4);
    FAIL_BRANCH_INDEX_DETERMINES_OPERATOR_REJECTED cites that NO-GO.
  * The finite Green resolvent + branch-index uniqueness stay PROOF-TARGET
    (D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001).
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def matmul(A, B):
    """Exact matrix product of two square Fraction matrices (lists of lists)."""
    n = len(A)
    m = len(B[0])
    k = len(B)
    return [[sum((A[i][t] * B[t][j] for t in range(k)), F(0)) for j in range(m)] for i in range(n)]


def matpow(A, p):
    """Exact A**p for a square Fraction matrix (p >= 0)."""
    n = len(A)
    R = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    for _ in range(p):
        R = matmul(R, A)
    return R


def lam_identity(n, lam):
    """The matrix lam*I_n over Fraction."""
    return [[lam if i == j else F(0) for j in range(n)] for i in range(n)]


def companion_C4(lam):
    """Forward 4-cycle companion (D0.Edge.companionC4): charpoly x^4 - lam, C4^4 = lam*I."""
    lam = F(lam)
    return [[F(0), F(1), F(0), F(0)],
            [F(0), F(0), F(1), F(0)],
            [F(0), F(0), F(0), F(1)],
            [lam,  F(0), F(0), F(0)]]


def companion_R3(lam):
    """3-cycle companion (D0.Edge.companionR3): charpoly x^3 - lam, R3^3 = lam*I."""
    lam = F(lam)
    return [[F(0), F(1), F(0)],
            [F(0), F(0), F(1)],
            [lam,  F(0), F(0)]]


def ram_index(n: int) -> int:
    """Ramification index of an n-cycle companion cover z^n - lam: index = n (all n sheets collapse)."""
    assert n >= 1, "cycle length must be >= 1"
    return n


def puiseux_exp(n: int) -> F:
    """Puiseux/ramification exponent of an n-cycle cover z^n - lam: z = lam^(1/n) => exponent 1/n exact."""
    assert n >= 1, "cycle length must be >= 1"
    return F(1, n)


def ram_defect(n: int) -> int:
    """Total ramification defect of a connected cyclic degree-n cover of P^1 totally ramified over two
    branch points: each totally-ramified fibre contributes (n-1), so the total defect is 2(n-1).
    """
    return 2 * (n - 1)


def cover_euler(n: int) -> int:
    """Riemann-Hurwitz Euler characteristic of the cover: base chi(P^1) = 2, degree-n cover with total
    ramification defect R has chi = n*2 - R. With R = 2(n-1) this is n*2 - 2(n-1).
    """
    return n * 2 - ram_defect(n)


def genus_from_euler(chi: int):
    """Solve 2 - 2g = chi for the genus g; return g if integral, else None."""
    num = 2 - chi
    if num % 2 != 0:
        return None
    return num // 2


def main() -> int:
    print("=== D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001  cyclic-cover branch index + genus-0 (NO uniqueness) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the cyclic cover structure (n-cycle => index n, exponent 1/n, "
          "defect 2(n-1)) is fixed BEFORE any value; the Riemann-Hurwitz balance 2-2g = n*2 - 2(n-1) is "
          "written down BEFORE solving for the genus, and the genus is read out (g=0) AFTER the structure")

    # ---- (a) the cyclic relations C4^4 = lam*I, R3^3 = lam*I hold exactly over Fraction --------------
    for lam in (1, 7, -3, F(2, 5)):
        assert matpow(companion_C4(lam), 4) == lam_identity(4, F(lam)), f"C4^4 must equal lam*I at lam={lam}"
        assert matpow(companion_R3(lam), 3) == lam_identity(3, F(lam)), f"R3^3 must equal lam*I at lam={lam}"
    print("PASS_CYCLIC_RELATIONS  C4^4 = lam*I and R3^3 = lam*I over Fraction at lam in {1,7,-3,2/5} "
          "(4-cycle and 3-cycle companion covers)")

    # ---- (b) ramification exponent 1/n for n = 2..5 (index = n, exponent = 1/n exact) ----------------
    expected_exp = {2: F(1, 2), 3: F(1, 3), 4: F(1, 4), 5: F(1, 5)}
    for n in range(2, 6):
        assert ram_index(n) == n, f"ramification index of n-cycle must be n, got {ram_index(n)} for n={n}"
        e = puiseux_exp(n)
        assert e == expected_exp[n], f"Puiseux exponent must be 1/{n}, got {e}"
        assert e == F(1, ram_index(n)), "exponent must be the reciprocal of the ramification index"
        assert isinstance(e, F) and 0 < e <= F(1, 2), "each exponent must be an exact rational in (0,1/2]"
    # explicit muon (4) and tau (3) row entries
    assert puiseux_exp(4) == F(1, 4) and puiseux_exp(3) == F(1, 3), "muon=1/4, tau=1/3"
    print("PASS_PUISEUX_EXPONENTS  index(n)=n and exponent(n)=1/n exact for n=2..5 "
          f"(muon 1/{4} via C4, tau 1/{3} via R3)")

    # ---- (c) Riemann-Hurwitz genus-0 consistency identity for n = 2..5 -------------------------------
    for n in range(2, 6):
        defect = ram_defect(n)
        assert defect == 2 * (n - 1), f"total ramification defect must be 2(n-1), got {defect} for n={n}"
        chi = cover_euler(n)
        # the arithmetic core: n*2 - 2(n-1) = 2 for every n
        assert chi == n * 2 - 2 * (n - 1), "cover Euler char must be n*2 - 2(n-1)"
        assert chi == 2, f"cover Euler characteristic must be identically 2, got {chi} for n={n}"
        g = genus_from_euler(chi)
        assert g == 0, f"Riemann-Hurwitz balance 2-2g={chi} must force genus g=0, got {g} for n={n}"
    print("PASS_GENUS_ZERO_IDENTITY  defect=2(n-1) => cover Euler char = n*2 - 2(n-1) = 2 => genus g=0 "
          "for EVERY n=2..5 (Riemann-Hurwitz genus-0 consistency)")

    # ================================================================================================
    # negative controls (reachable FAIL_, planted wrong inputs rejected)
    # ================================================================================================

    # (1) "Riemann-Hurwitz FORCES the pair (4,3) uniquely" -> REJECTED.
    #     The genus identity holds for n=2,3,4,5 ALL alike (every cyclic cover is genus 0), so it cannot
    #     single out (4,3). We show >=2 OTHER n also give genus 0, so the would-be uniqueness is false.
    genus_zero_set = {n for n in range(2, 6) if genus_from_euler(cover_euler(n)) == 0}
    rh_makes_43_unique = (genus_zero_set == {3, 4})  # the false claim: only (3,4) satisfy the identity
    assert rh_makes_43_unique is False, \
        "control: R-H must NOT make (4,3) unique -- other n also give genus 0"
    assert {2, 5}.issubset(genus_zero_set), \
        "control: n=2 and n=5 (besides 3,4) must also satisfy the genus-0 identity"
    assert len(genus_zero_set) >= 4, "control: at least 4 distinct n give genus 0 -> not unique"
    print("FAIL_RH_FORCES_PAIR_43_REJECTED  Riemann-Hurwitz gives genus 0 for n in "
          f"{sorted(genus_zero_set)} ALL alike -> it does NOT make the pair (4,3) unique (uniqueness is FALSE)")

    # (2) "a PDG mass ratio is a valid INPUT to this front" -> REJECTED.
    #     This front uses only cycle lengths (integers) -> exponents/indices/genus. No PDG mass enters;
    #     the PDG datum is neither an exponent (1/n) nor a ramification index (n) nor the genus (0).
    pdg_mass_ratio = F(2067682830, 10000000)  # PDG m_mu/m_e ~ 206.768, a would-be mass INPUT
    assert pdg_mass_ratio not in {puiseux_exp(n) for n in range(2, 6)}, \
        "control: a PDG mass ratio is not a Puiseux exponent 1/n"
    assert int(pdg_mass_ratio) not in {ram_index(n) for n in range(2, 6)}, \
        "control: a PDG mass ratio is not a ramification index n in {2,3,4,5}"
    assert genus_from_euler(cover_euler(4)) == 0 and pdg_mass_ratio != 0, \
        "control: the genus (0) is mass-free; the PDG ratio is nonzero and irrelevant"
    print("FAIL_PDG_MASS_INPUT_REJECTED  the PDG mass ratio 206.768 is neither an exponent (1/n) nor an "
          "index (n) nor the genus (0); this front is mass-free -> a PDG mass INPUT is rejected")

    # (3) "the branch index DETERMINES the operator" -> REJECTED (cite the existing obstruction NO-GO).
    #     D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 exhibits TWO distinct 4x4 operators that both
    #     satisfy M^4 = lam*I (same charpoly x^4 - lam, same branch index 1/4). We reproduce the witness
    #     here: index 1/4 -> operator is many-to-one, so the index does NOT pin the operator.
    def companion_C4_alt(lam):
        """Reverse-orientation 4-cycle companion (D0.Matter.companionC4Alt): charpoly x^4 - lam,
        C4Alt^4 = lam*I, DISTINCT from companion_C4 (differs in entry (0,1)).
        """
        lam = F(lam)
        return [[F(0), F(0), F(0), lam],
                [F(1), F(0), F(0), F(0)],
                [F(0), F(1), F(0), F(0)],
                [F(0), F(0), F(1), F(0)]]

    for lam in (1, 7, -3, F(2, 5)):
        A = companion_C4(lam)
        B = companion_C4_alt(lam)
        assert matpow(A, 4) == lam_identity(4, F(lam)), f"C4^4 must equal lam*I at lam={lam}"
        assert matpow(B, 4) == lam_identity(4, F(lam)), f"C4Alt^4 must equal lam*I at lam={lam}"
        assert A != B, f"the two operators must be DISTINCT at lam={lam}"
        assert puiseux_exp(4) == F(1, 4), "both carry the SAME branch index 1/4"
    branch_index_determines_operator = (companion_C4(1) == companion_C4_alt(1))
    assert branch_index_determines_operator is False, \
        "control: if the index fixed the operator the two witnesses would coincide -- they do not"
    print("FAIL_BRANCH_INDEX_DETERMINES_OPERATOR_REJECTED  two DISTINCT 4x4 operators both satisfy "
          "M^4 = lam*I (branch index 1/4) -> index -> operator is many-to-one; cited NO-GO "
          "D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 -> 'index determines operator' is rejected")

    # ---- honest residual (asserted OPEN) -----------------------------------------------------------
    print("HONEST_RESIDUAL  this front closes ONLY the narrow arithmetic (cyclic relations, 1/n exponents, "
          "genus-0 consistency); it asserts NO uniqueness. The finite Green RESOLVENT over the full "
          "shell-torus cover + the branch-index UNIQUENESS certificate are still MISSING -> "
          "D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001 stays PROOF-TARGET.")

    print("PASS_LEPTON_RIEMANN_HURWITZ_BRANCH_INDEX")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
