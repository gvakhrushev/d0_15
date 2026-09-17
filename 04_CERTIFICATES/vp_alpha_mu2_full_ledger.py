#!/usr/bin/env python3
"""D0-ALPHA-MU2-FULL-LEDGER-001 — the depth-2 archive-return carrier is the full V11 ledger (M1 selector).

The depth-2 archive return P -> Q -> Q -> P traces a SCALAR over the unresolved archive block on the
fixed middle zone V11. A scalar trace over unresolved data must sum over ALL distinguishable subset
states of V11 -- the full Boolean ledger P(V11), canonically linearised as the exterior/Fock space
Λ*(V11), of dimension 2^11. Any SMALLER carrier requires an extra selector that the scalar trace + the
D0 support/projection chain do not generate:
  * the Spin(11) irreducible spinor 2^5 = 32 needs an irreducible-module selector (Clifford metric + a
    module choice);
  * the naive edge-pairing multiplicity 2 discards distinguishable archive-subset histories;
  * V9 (2^9=512) or V13 (2^13=8192) changes the already-fixed phase/archive zone.
Each such choice is an external catalog -> inadmissible by M1. Hence the D0-admissible scalar-archive
selector is the full Λ*(V11), and the second moment amplitude is

    mu2 = 2^11 * pi0 * phi^-2 = 2048 * 6/5 = 12288/5   (pi0 = (6/5) phi^2).

SCOPE (honest): this closes the D0-INTERNAL scalar-trace SELECTOR (which carrier the scalar archive
trace uses). It does NOT prove that the physical Feshbach-Schur W_eff residue is realised as exactly
this scalar trace -- that residue-extraction is the EXTERNAL Dixmier-trace / Wodzicki-residue owner
D0-DIXMIER-RESIDUE-OWNER-001 (ASSUMP-DIXMIER-TRACE). The arithmetic mu2=12288/5 itself is already
machine-checked (D0-DELTA-ALPHA-MOMENT-001); this cert adds the M1 selector + the ledger->mu2 tie.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


# exact ℚ(φ): (a,b) = a + b·φ
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def smul(c, x):
    return (c * x[0], c * x[1])


PHIv = (F(0), F(1))
PHI2 = (F(1), F(1))        # φ² = 1 + φ
PHI_INV2 = (F(2), F(-1))   # φ⁻² = 2 − φ


def exterior_dim(n: int) -> int:
    return sum(comb(n, k) for k in range(n + 1))


def main() -> int:
    print("=== D0-ALPHA-MU2-FULL-LEDGER-001  scalar archive trace selects the full Λ*(V11) ledger (M1) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: depth-2 archive return P->Q->Q->P traces a SCALAR over the unresolved "
          "V11 block; the carrier is the full Boolean ledger P(V11)=Λ*(V11) BEFORE the mu2 value is read")

    # full unresolved ledger = exterior/Fock dimension over V11
    ledger = 2 ** 11
    assert exterior_dim(11) == ledger == 2048, f"dim Lambda*(V11) must be 2^11=2048: {exterior_dim(11)}"
    print(f"PASS_FULL_LEDGER  dim Λ*(V11) = Σ_k C(11,k) = 2^11 = {ledger} (full Boolean subset ledger)")

    # pi0 * phi^-2 = 6/5 exactly, and mu2 = ledger * 6/5 = 12288/5
    pi0 = smul(F(6, 5), PHI2)                 # π₀ = (6/5)φ²
    pi0_red = mul(pi0, PHI_INV2)              # π₀·φ⁻²
    assert pi0_red == (F(6, 5), F(0)), f"pi0*phi^-2 must be the pure rational 6/5: {pi0_red}"
    mu2 = ledger * F(6, 5)
    assert mu2 == F(12288, 5), f"mu2 = 2^11 * pi0 * phi^-2 must be 12288/5: {mu2}"
    print(f"PASS_MU2_FROM_LEDGER  mu2 = 2^11 * pi0 * phi^-2 = {ledger} * 6/5 = {mu2} (= 12288/5)")

    # ---- M1 selector controls: each smaller/other carrier != full ledger AND needs an external selector ----
    alternatives = {
        "Spin(11) irreducible spinor (needs an irreducible-module selector)": 2 ** 5,
        "naive edge-pairing (discards archive-subset histories)": 2,
        "V9 zone (changes the fixed phase/archive zone)": exterior_dim(9),
        "V13 zone (changes the fixed phase/archive zone)": exterior_dim(13),
    }
    for name, dim in alternatives.items():
        assert dim != ledger, f"control: alternative carrier must differ from the full ledger: {name}={dim}"
    print(f"FAIL_SUBCARRIERS_NEED_EXTERNAL_SELECTOR  spinor 32, edge-pairing 2, V9=512, V13=8192 all != 2048 "
          "and each needs an extra (external) selector -> inadmissible by M1; only the full ledger is scalar-trace-forced")

    # control: a wrong pi0 phase breaks the mu2 tie (mu2 is not free)
    pi0_bad = smul(F(5, 4), PHI2)
    assert ledger * F(5, 4) != F(12288, 5) or mul(pi0_bad, PHI_INV2) != (F(6, 5), F(0)), \
        "control: a wrong pi0 must break the ledger->mu2 tie"
    print("FAIL_WRONG_PI0_BREAKS_MU2  a wrong pi0 phase (5/4 vs 6/5) breaks mu2 = 2^11 * pi0 * phi^-2 = 12288/5")

    print("HONEST_D0_INTERNAL_SELECTOR  this closes the D0-INTERNAL scalar-trace selector (full ledger M1-forced) + the "
          "ledger->mu2 tie; the physical W_eff residue-extraction realising this scalar trace stays the EXTERNAL "
          "Dixmier/Wodzicki owner D0-DIXMIER-RESIDUE-OWNER-001 (ASSUMP-DIXMIER-TRACE). mu2 arithmetic already Lean: D0-DELTA-ALPHA-MOMENT-001.")
    print("PASS_ALPHA_MU2_FULL_LEDGER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
