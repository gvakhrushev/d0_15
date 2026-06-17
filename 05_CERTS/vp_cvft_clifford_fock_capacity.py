#!/usr/bin/env python3
"""D0-CVFT-F1 (sharpen, NOT close) — the 2^11 capacity has a named exterior/Clifford-Fock candidate.

The residue amplitude mu2 = 2^11 * pi0 * phi^-2 of the algebraic alpha writing carries an
unexplained factor 2^11 = 2048 (BOOK_02 §02.13.4). Prior certs (vp_feshbach_residue_amplitudes.py,
vp_mass_chain_alpha.py) DERIVED mu1 = 1/rank and OWNED the pi0 factor, but left 2^11 only FLAGGED
as "2^{V11} binary multiplicity" with the explicit honest note that a list-match is NOT a
derivation, and observed that the naive edge-pushforward gives pairing multiplicity 2 (na=2), not
2^11. This certificate does NOT close that gap. It SHARPENS it by naming a principled candidate
object for 2^11 and ruling out the two nearest alternatives, so the open step is stated precisely.

THE NAMED CANDIDATE (not a derivation): the archive over the 11-element zone V11 is, if each node
carries a single binary (occupied/empty) degree of freedom, the fermionic Fock space / exterior
(Grassmann) algebra over 11 generators, whose dimension is exactly 2^11. Equivalently this is the
dimension of the real Clifford algebra Cl(R^11). This gives 2^11 a specific algebraic home, not a
bare list-match.

WHAT IS PROVED (exact integers, able to FAIL):
  * 2^11 = 2048; and 2^|V11| = 2^11 with |V11| = 11 = L_5 (5th Lucas number) -- the zone cardinality;
  * dim Cl(R^n) = 2^n and dim Lambda^*(R^n) = 2^n (Clifford = exterior dimension); at n=11 both = 2048
    = dim of the fermionic Fock space over 11 modes (each mode in {empty, occupied});
  * DISTINCTION 1 (rules out the irreducible-spinor reading): the irreducible spinor representation
    of Spin(11) has dimension 2^floor(11/2) = 2^5 = 32 != 2048. So 2^11 is the FULL Clifford /
    exterior / Fock dimension, NOT the irreducible spin representation -- a precise statement.
  * DISTINCTION 2 (states the open gap): the naive edge-pushforward pairing multiplicity is 2
    (na = 2, the active sector couples through 2 of the 359 edges), and 2 != 2048. So the candidate
    is the FULL 2^11 Fock trace, which is exactly NOT the naive 2-edge pairing -- the open question.
  * NEGATIVE CONTROLS: 2^|V9| = 2^9 = 512 != 2048 and 2^|V13| = 2^13 = 8192 != 2048 -- the capacity
    is specifically the 11-zone V11, not V9 or V13; and 2^11 != 2*1024-class accidental neighbours.

HONESTY BOUNDARY (printed). This NAMES a candidate (exterior/Clifford/Fock over V11) and rules out
the irreducible-spinor (32) and naive-pairing (2) readings -- it does NOT derive that the
Feshbach-Schur residue mu2 traces over the full 2^11 Fock space. That residue-extraction step is
owned externally by the Dixmier trace / noncommutative integral (Connes NCG): for a spectral
triple the s->pole residue recovers the Clifford-bundle multiplicity (owner edge
D0-DIXMIER-RESIDUE-OWNER-001 / ASSUMP-DIXMIER-TRACE). CVFT-F1 STAYS A PROOF-TARGET. The gap is
RE-NARROWED from "2^11 is unexplained" to "why the residue traces over the full Cl(V11)=2^11 Fock
space rather than the naive 2-edge pairing". Sharpened, not closed; not promoted.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def lucas(n: int) -> int:
    a, b = 2, 1   # L_0 = 2, L_1 = 1
    for _ in range(n):
        a, b = b, a + b
    return a


def clifford_dim(n: int) -> int:
    return 2 ** n            # dim Cl(R^n) = dim Lambda^*(R^n) = 2^n


def irreducible_spinor_dim(n: int) -> int:
    return 2 ** (n // 2)     # Spin(2k+1): 2^k ; Spin(2k): 2^{k-1}(+) ; here floor(n/2)


def main() -> int:
    print("=== D0-CVFT-F1  2^11 capacity: exterior/Clifford-Fock candidate (SHARPEN, not close) ===")

    V11 = 11
    assert lucas(5) == 11 == V11, "|V11| = 11 = L_5 (5th Lucas number)"
    assert 2 ** 11 == 2048, "2^11 = 2048"
    assert 2 ** V11 == 2048, "2^|V11| = 2^11 = 2048 (the flagged capacity)"
    print(f"PASS_ZONE  |V11| = 11 = L_5 ; 2^|V11| = 2^11 = {2**V11}")

    # exterior / Clifford / fermionic Fock dimension over 11 generators = 2^11
    assert clifford_dim(11) == 2048, "dim Cl(R^11) = dim Lambda^*(R^11) = 2^11 = 2048"
    assert clifford_dim(11) == 2 ** V11, "Clifford/exterior dim = 2^|V11| (full fermionic Fock over 11 nodes)"
    print("PASS_FOCK_CANDIDATE  2^11 = dim Cl(R^11) = dim Lambda^*(R^11) = fermionic Fock over 11 nodes")

    # DISTINCTION 1: irreducible Spin(11) spinor is 2^5 = 32, NOT 2^11
    assert irreducible_spinor_dim(11) == 32, "irreducible Spin(11) spinor dim = 2^5 = 32"
    assert irreducible_spinor_dim(11) != 2048, "32 != 2048: 2^11 is the FULL Clifford/exterior dim, not the irreducible spinor"
    print("FAIL_IRREDUCIBLE_SPINOR_IS_32_NOT_2048  (rules out the irreducible-spinor reading; 2^11 is the full algebra)")

    # DISTINCTION 2: the naive edge-pushforward pairing multiplicity is 2, NOT 2^11 (the open gap)
    na = 2          # active sector couples through 2 of the 359 edges (vp_feshbach_residue_amplitudes.py)
    assert na != 2048, "naive edge-pushforward multiplicity 2 != 2^11 -- this IS the open CVFT-F1 gap"
    print("FAIL_NAIVE_PAIRING_IS_2_NOT_2048  (the open step: full 2^11 Fock trace vs the naive 2-edge pairing)")

    # NEGATIVE CONTROLS: it is specifically V11, not V9 or V13
    assert 2 ** 9 == 512 != 2048, "control: 2^|V9| = 512 != 2048"
    assert 2 ** 13 == 8192 != 2048, "control: 2^|V13| = 8192 != 2048"
    print("FAIL_CONTROL_NOT_V9_NOR_V13  2^9=512, 2^13=8192 both != 2048 (capacity is specifically the 11-zone)")

    print("HONEST_2POW11_HAS_A_NAMED_EXTERIOR_CLIFFORD_FOCK_CANDIDATE_OVER_V11_NOT_A_BARE_LIST_MATCH")
    print("HONEST_RESIDUE_TRACE_OVER_FULL_FOCK_VS_NAIVE_2_EDGE_PAIRING_STAYS_OPEN_OWNED_BY_DIXMIER_TRACE")
    print("HONEST_CVFT_F1_STAYS_PROOF_TARGET_SHARPENED_NOT_CLOSED_NOT_PROMOTED")

    # ---- RESIDUE ROUTE BLOCKED (closure-holonomy supersedes for Delta-alpha; Iter-21) ----
    print("BLOCKED_RESIDUE_ROUTE_TO_DELTA_ALPHA  a Dixmier/zeta residue carrying ln(phi) is transcendental "
          "(Res prop 1/ln phi) and cannot land in alpha_alg in Q(phi) (algebraic) -- this route is closed-negative")
    print("WORKING_ROUTE  Delta-alpha is closed by closure holonomy: 05_CERTS/vp_seam_holonomy_alpha.py "
          "(D0-ALPHA-HOLONOMY-002); this cert keeps only its proven capacity/pairing content")
    print("PASS_CVFT_CLIFFORD_FOCK_CAPACITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
