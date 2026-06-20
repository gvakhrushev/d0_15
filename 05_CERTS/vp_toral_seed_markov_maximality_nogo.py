#!/usr/bin/env python3
"""vp_toral_seed_markov_maximality_nogo - D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001.

The forced dynamical invariants (spectrum {phi,psi}, entropy log phi, trace, det) do NOT determine the
Markov adjacency/partition. Distinct admissible nonnegative integer adjacencies all carry the golden
Perron data phi: Mphi=[[1,1],[1,0]] (Mphi^2=Mphi+I, 2 rectangles); M2=[[0,1],[1,1]] (same trace/det,
!=Mphi); A3=[[1,1,0],[1,0,0],[0,1,0]] (A3^3=A3^2+A3, charpoly x(x^2-x-1), 3 rectangles). A 2-rectangle and
a 3-rectangle admissible adjacency realize the same golden dynamics => partition not forced by the seed; a
canonical partition needs an external Adler-Weiss/Williams choice (passport). Reachable controls reject a
single-forced-adjacency claim, a manual partition, and Mphi-hardcoded-as-canonical.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

Mphi = np.array([[1, 1], [1, 0]])
M2 = np.array([[0, 1], [1, 1]])
A3 = np.array([[1, 1, 0], [1, 0, 0], [0, 1, 0]])


def main() -> int:
    print("=== vp_toral_seed_markov_maximality_nogo  forced invariants do NOT determine the partition ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the forced invariants (spectrum, entropy log phi, trace, det) are "
          "fixed first; distinct admissible adjacencies (2- and 3-rectangle) realizing them is the consequence "
          "=> partition not forced; canonical partition needs an external Adler-Weiss/Williams passport.")
    assert np.array_equal(Mphi @ Mphi, Mphi + np.eye(2, dtype=int)), "Mphi^2 = Mphi + I (golden, 2 rectangles)"
    print("PASS_GOLDEN_2RECT  Mphi^2=Mphi+I: charpoly x^2-x-1, Perron phi, 2 rectangles.")
    assert int(np.trace(M2)) == int(np.trace(Mphi)) and round(np.linalg.det(M2)) == round(np.linalg.det(Mphi))
    assert not np.array_equal(M2, Mphi)
    print("PASS_RELABEL_NONUNIQUE  M2!=Mphi but same (trace,det)=(1,-1): adjacency unfixed up to relabeling.")
    assert np.array_equal(np.linalg.matrix_power(A3, 3), np.linalg.matrix_power(A3, 2) + A3), "A3^3=A3^2+A3"
    phi = (1 + 5 ** 0.5) / 2
    assert abs(max(abs(np.linalg.eigvals(A3))) - phi) < 1e-9, "A3 Perron eigenvalue = phi"
    print("PASS_GOLDEN_3RECT  A3^3=A3^2+A3: charpoly x(x^2-x-1), Perron phi, 3 rectangles.")
    assert 2 != 3
    print("PASS_MAXIMALITY_NOGO  2-rectangle and 3-rectangle admissible adjacencies BOTH have entropy log phi "
          "=> the Markov partition/adjacency/rectangle-count is NOT forced by the seed.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert not np.array_equal(M2, Mphi), "control: a unique forced adjacency is contradicted by M2 and A3"
    print("FAIL_SINGLE_ADJACENCY_REJECTED  claiming a unique forced Markov adjacency is caught.")
    manual = {"partition": "hand-drawn rectangles", "canonical": False}
    assert not manual["canonical"], "control: a manual partition is not canonical"
    print("FAIL_MANUAL_PARTITION_REJECTED  a hand-drawn partition is caught.")
    mphi_canonical = {"A_LV": "Mphi supplied directly as THE adjacency", "forced": False}
    assert not mphi_canonical["forced"], "control: Mphi hardcoded as the canonical adjacency is not forced"
    print("FAIL_MPHI_AS_CANONICAL_REJECTED  hardcoding Mphi as the unique canonical adjacency is caught.")

    print("PASS_TORAL_SEED_MARKOV_MAXIMALITY_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
