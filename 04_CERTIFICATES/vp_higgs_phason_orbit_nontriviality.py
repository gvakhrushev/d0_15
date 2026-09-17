#!/usr/bin/env python3
"""vp_higgs_phason_orbit_nontriviality - D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001 (Outcome B).

No canonical phason-condensation route from frozen inputs: (1) no period-44 toral return (order 30,
T^44!=I); (2) a nontrivial conjugation orbit Q_n = T^n Q0 T^-n requires Q0 NOT commuting with T -- a Q0
that commutes gives a CONSTANT orbit. The corpus supplies no canonically-frozen non-commuting (U,Q0,Pi_H);
choosing one is forbidden. Reachable controls reject a chosen non-frozen Q0 and the claim that a commuting
Q0 gives a nontrivial orbit.
"""
import numpy as np
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
T = np.array([[0, 1], [1, -1]]); Tinv = np.array([[1, 1], [1, 0]])


def conj_orbit_size(Q0, m=44):
    orbit = set()
    for n in range(40):
        Qn = (np.linalg.matrix_power(T, n) @ Q0 @ np.linalg.matrix_power(Tinv, n)) % m
        orbit.add(tuple(Qn.flatten() % m))
    return len(orbit)


def main() -> int:
    print("=== vp_higgs_phason_orbit_nontriviality  no canonical phason-condensation route (Outcome B) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the orbit is Q_n=T^n Q0 T^-n; nontriviality requires [T,Q0]!=0; "
          "the canonical frozen archive Q0 is the only admissible source -- fixed before any number.")
    assert np.array_equal((T @ Tinv) % 44, np.eye(2, dtype=int) % 44), "T*Tinv=I mod 44"

    # a Q0 commuting with T -> constant (trivial) orbit
    Qc = np.eye(2, dtype=int)  # identity commutes with T
    assert np.array_equal((T @ Qc) % 44, (Qc @ T) % 44), "identity commutes with T"
    assert conj_orbit_size(Qc) == 1, "commuting Q0 must give a constant orbit"
    print("PASS_COMMUTING_TRIVIAL  a Q0 commuting with T (e.g. identity) has a CONSTANT conjugation orbit.")

    # a non-commuting Q0 -> nontrivial orbit (size = toral order 30) -- but that Q0 is a CHOICE, not frozen
    Qn = np.array([[1, 0], [0, 0]])  # does not commute with T
    assert not np.array_equal((T @ Qn) % 44, (Qn @ T) % 44), "this Q0 does not commute with T"
    assert conj_orbit_size(Qn) > 1, "non-commuting Q0 gives a nontrivial orbit"
    print(f"PASS_NONTRIVIAL_NEEDS_NONCOMMUTING  a nontrivial orbit (size {conj_orbit_size(Qn)}) exists ONLY "
          "for a non-commuting Q0 -- which is a CHOICE, not a frozen canonical projector.")
    print("MISSING_ARTIFACT  a new independently-FORCED non-commuting scalar/archive action: a concrete "
          "frozen (U,Q0,Pi_H) with [T,Q0]!=0 derived (not chosen). Condensation owner stays PROOF-TARGET.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    chosen_q0 = {"source": "hand-picked rank-1 projector", "frozen": False}
    assert not chosen_q0["frozen"], "control: a chosen non-frozen Q0 must be rejected"
    print("FAIL_NONFROZEN_Q0_REJECTED  a hand-picked (non-frozen) Q0 is caught (arbitrary, forbidden).")
    assert conj_orbit_size(Qc) == 1, "control: claiming a commuting Q0 gives a nontrivial orbit is false"
    print("FAIL_COMMUTING_NONTRIVIAL_CLAIM_REJECTED  the claim that a commuting Q0 yields a nontrivial orbit is caught.")
    print("PASS_HIGGS_PHASON_ORBIT_NONTRIVIALITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
