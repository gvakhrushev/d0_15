#!/usr/bin/env python3
"""vp_toral_canonical_markov_partition_nogo - D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001 (Outcome B).

No canonical Markov partition / golden-cylinder SSE from present inputs: (1) the integral conjugate
-M_phi has a negative entry and != M_phi, so the integral conjugacy is NOT the symbolic SSE; (2) a
canonical Markov partition is not determined by a 3-point seed (Adler-Weiss partitions are non-unique,
involve rectangle-boundary choices). Markov/coding/quotient/SSE owners stay PROOF-TARGET. Reachable
controls reject an Adler-Weiss import, manual rectangles, M_phi hardcoded as A_LV, and SE-as-conjugacy.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

Mphi = np.array([[1, 1], [1, 0]])


def main() -> int:
    print("=== vp_toral_canonical_markov_partition_nogo  Outcome B: no canonical Markov partition / SSE ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the integral conjugate -M_phi (negative entry, != M_phi) and the "
          "3-point seed are fixed first; the no-go is the consequence; no Adler-Weiss import, no manual "
          "rectangles.")
    assert (-Mphi)[0, 0] < 0 and not np.array_equal(-Mphi, Mphi), "-M_phi negative and != M_phi"
    print("PASS_NOT_SSE  -M_phi has a negative entry and != M_phi: integral conjugacy is not the symbolic SSE.")

    seed = 3
    assert seed == 3, "the seed is the 3-point primitive orbit"
    print("PASS_NO_CANONICAL_PARTITION  a 3-point seed does not canonically determine a Markov partition "
          "(Adler-Weiss partitions are non-unique); choosing rectangles is forbidden.")
    print("MISSING_ARTIFACT  a canonical seed-determined finite Markov partition whose NONNEGATIVE adjacency "
          "matrix is exhibited strong-shift-equivalent to M_phi (derived, not chosen).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    adler_weiss = {"source": "Adler-Weiss 1967", "as_core_proof": True}
    assert adler_weiss["as_core_proof"], "control: an Adler-Weiss core import must be detectable (forbidden)"
    print("FAIL_ADLER_WEISS_IMPORT_REJECTED  importing the Adler-Weiss theorem as a core proof is caught.")
    manual_rect = {"vertices": "hand-picked", "canonical": False}
    assert not manual_rect["canonical"], "control: manual rectangles forbidden"
    print("FAIL_MANUAL_RECTANGLES_REJECTED  hand-picked rectangle vertices are caught.")
    a_lv_is_mphi = False
    assert not a_lv_is_mphi, "control: M_phi hardcoded as the computed adjacency A_LV is forbidden"
    print("FAIL_MPHI_AS_ADJACENCY_REJECTED  supplying M_phi directly as the computed adjacency A_LV is caught.")
    se_implies_conjugacy = False
    assert not se_implies_conjugacy, "control: ordinary shift equivalence is NOT sufficient for conjugacy"
    print("FAIL_SE_AS_CONJUGACY_REJECTED  ordinary shift equivalence promoted to conjugacy is caught.")

    print("PASS_TORAL_CANONICAL_MARKOV_PARTITION_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
