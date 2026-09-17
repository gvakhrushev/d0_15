#!/usr/bin/env python3
"""D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001 (CERT-CLOSED) - Fiedler value > 0 at connectivity.

Front P4 (companion to vp_connectivity_threshold_owner.py / D0.Cosmology.ReheatingPercolationOwner).
Signal propagation along the scene graph exists only when the graph is CONNECTED, and connectivity is
detected by the algebraic connectivity = the Fiedler value lambda_2 = the SMALLEST NONZERO eigenvalue
of the combinatorial Laplacian L = D - A. The forced scene is the complete tripartite graph
K(9,11,13) (zones 9, 11, 13 -> 33 vertices, every cross-zone pair an edge, no intra-zone edge).

WHAT IS PROVED (exact, able to FAIL):
  * The 33x33 Laplacian of K(9,11,13) has Fiedler value lambda_2 = 20 (= n - max_part = 33 - 13),
    computed as the second-smallest eigenvalue via numpy eigvalsh; lambda_2 = 20 > 0 -> CONNECTED.
  * The exact spectrum matches the closed-form complete-multipartite Laplacian spectrum
    {0 (x1), 20 (x12), 22 (x10), 24 (x8), 33 (x2)} (eigenvalues n - n_i with mult n_i - 1, and
    n with mult k-1), verified to 9 decimals and trace-consistent (sum = 2*edges = 718).
  * The EDGELESS 33-vertex stage has Laplacian 0, so lambda_1 = lambda_2 = 0 -> DISCONNECTED, no gap.
  * Two Laplacian eigenvalues are exhibited by EXPLICIT integer eigenvectors (matching the Lean
    native_decide eigenvector proofs): all-ones -> eigenvalue 0; a part-2 vector summing to zero ->
    eigenvalue 20.

The structure (33-vertex complete tripartite, no input speed) is fixed BEFORE any number. No SI speed
of light enters as input; no Planck/CMB datum enters. Lean owner:
D0.Cosmology.CLightconePercolationOwner.
"""
from __future__ import annotations

import sys
from fractions import Fraction

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ZONES = (9, 11, 13)  # forced zone sizes -> 33 vertices
N = sum(ZONES)


def part_labels(sizes):
    """Contiguous part label per vertex 0..N-1."""
    labels = []
    for b, s in enumerate(sizes):
        labels += [b] * s
    return labels


def laplacian(sizes):
    """Combinatorial Laplacian L = D - A of the complete multipartite graph on the given parts."""
    labels = part_labels(sizes)
    n = len(labels)
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j and labels[i] != labels[j]:
                A[i, j] = 1.0
    D = np.diag(A.sum(axis=1))
    return D - A


def sorted_eigs(L):
    return np.sort(np.linalg.eigvalsh(L))


def fiedler_value(L):
    """Algebraic connectivity = second-smallest Laplacian eigenvalue."""
    return float(sorted_eigs(L)[1])


def closed_form_spectrum(sizes):
    """Exact closed-form Laplacian spectrum of complete multipartite K(sizes):
    0 (x1), n - n_i (x (n_i - 1)) for each part, n (x (k-1)).
    """
    n = sum(sizes)
    spec = [0]
    for ni in sizes:
        spec += [n - ni] * (ni - 1)
    spec += [n] * (len(sizes) - 1)
    return sorted(spec)


def main() -> int:
    print("=== D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001  Fiedler value > 0 at connectivity (CERT-CLOSED) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: zones (9,11,13) -> 33-vertex COMPLETE TRIPARTITE Laplacian "
          "L = D - A is fixed before any number; the claim is lambda_2 > 0 <=> connected (algebraic "
          "connectivity), with no input speed and no CMB/Planck datum")

    L = laplacian(ZONES)
    assert L.shape == (33, 33), f"Laplacian must be 33x33, got {L.shape}"
    print(f"PASS_LAPLACIAN_SHAPE  K(9,11,13) Laplacian is {L.shape[0]}x{L.shape[1]} (33 vertices)")

    # ---- Fiedler value lambda_2 = 20 > 0 (connected) --------------------------------
    lam2 = fiedler_value(L)
    assert abs(lam2 - 20.0) < 1e-9, f"Fiedler value must be 20, got {lam2}"
    assert lam2 > 0.0, "Fiedler value must be strictly positive (connected)"
    print(f"PASS_FIEDLER_VALUE_20  lambda_2(K(9,11,13)) = {lam2:.9f} = 20 = n - max_part (33 - 13) > 0 "
          "-> CONNECTED")

    # ---- exact spectrum matches the closed form, trace-consistent -------------------
    eigs = sorted_eigs(L)
    cf = closed_form_spectrum(ZONES)
    assert len(cf) == 33, f"closed-form spectrum must have 33 entries, got {len(cf)}"
    assert np.allclose(eigs, np.array(cf, dtype=float), atol=1e-9), \
        "numpy spectrum must match closed-form {0,20x12,22x10,24x8,33x2}"
    # trace consistency via EXACT integer arithmetic (Fraction)
    n_edges = ZONES[0] * ZONES[1] + ZONES[0] * ZONES[2] + ZONES[1] * ZONES[2]
    assert n_edges == 359, f"cross-zone edges must be 359, got {n_edges}"
    spec_sum = sum(Fraction(x) for x in cf)
    assert spec_sum == Fraction(2 * n_edges) == Fraction(718), \
        f"sum of eigenvalues must equal trace 2*edges=718, got {spec_sum}"
    print(f"PASS_SPECTRUM_CLOSED_FORM  spectrum = {{0x1, 20x12, 22x10, 24x8, 33x2}}, "
          f"sum = {int(spec_sum)} = 2*{n_edges} = trace(L)")

    # ---- smallest nonzero eigenvalue is exactly 20 ----------------------------------
    nonzero = [x for x in cf if x != 0]
    assert min(nonzero) == 20, f"smallest nonzero eigenvalue must be 20, got {min(nonzero)}"
    assert cf.count(0) == 1, f"connected graph must have exactly one zero eigenvalue, got {cf.count(0)}"
    print(f"PASS_GAP_IS_SMALLEST_NONZERO  min nonzero eig = {min(nonzero)}, zero-eig multiplicity = "
          f"{cf.count(0)} (kernel dim 1 -> single component)")

    # ---- explicit eigenvectors (mirror the Lean native_decide proofs) ---------------
    ones = np.ones(33)
    assert np.allclose(L @ ones, np.zeros(33), atol=1e-12), "all-ones must be a 0-eigenvector"
    fied = np.zeros(33)
    fied[20] = 1.0   # vertex 20 in the size-13 part
    fied[21] = -1.0  # vertex 21 in the size-13 part (sums to zero on part 2)
    assert np.allclose(L @ fied, 20.0 * fied, atol=1e-12), "part-2 zero-sum vector must be a 20-eigenvector"
    print("PASS_EXPLICIT_EIGENVECTORS  L*ones = 0 (eigval 0); L*fied = 20*fied (eigval 20) "
          "[matches Lean lap_ones_eigen0 / lap_fiedler_eigen20]")

    # ---- edgeless stage: lambda_2 = 0 (disconnected, no gap) ------------------------
    L0 = np.zeros((33, 33))
    eig0 = sorted_eigs(L0)
    assert abs(eig0[1]) < 1e-12, "edgeless Fiedler value must be 0"
    assert abs(eig0[0]) < 1e-12, "edgeless smallest eigenvalue must be 0"
    print("PASS_EDGELESS_GAP_ZERO  edgeless 33-vertex Laplacian = 0 -> lambda_2 = 0 -> DISCONNECTED "
          "(no positive gap, no propagation)")

    # ---- negative controls (genuinely reachable) ------------------------------------
    # (a) over-claim lambda_2 = 2: it is 20, NOT 2 (do NOT assert an unproven Cheeger equality).
    overclaim_lambda2_is_2 = abs(fiedler_value(L) - 2.0) < 1e-9
    assert overclaim_lambda2_is_2 is False, "control: lambda_2 = 2 over-claim must be rejected"
    print(f"FAIL_LAMBDA2_EQUALS_2_REJECTED  planted 'lambda_2 = 2' rejected "
          f"(actual lambda_2 = {fiedler_value(L):.6f} = 20, not 2; no Cheeger equality is claimed)")

    # (b) edgeless graph claimed to carry c=1 propagation: lambda_2 = 0 -> no propagation.
    edgeless_supports_propagation = fiedler_value(L0) > 0.0
    assert edgeless_supports_propagation is False, \
        "control: disconnected (edgeless) graph must NOT support propagation"
    print("FAIL_DISCONNECTED_PROPAGATION_REJECTED  planted 'edgeless graph propagates at c=1' rejected "
          "(lambda_2 = 0 -> no connected path -> nothing propagates)")

    # (c) wrong Fiedler value for the WRONG scene: K(9,11,15) (35 vertices) has lambda_2 = 35-15 = 20?
    #     Actually n=35, max part 15 -> lambda_2 = 20 too, but n != 33 and edge count differs;
    #     reject it as the forced scene by its vertex count and trace.
    Lbad = laplacian((9, 11, 15))
    assert Lbad.shape == (35, 35) and Lbad.shape != (33, 33), "wrong scene must not be 33x33"
    bad_trace = float(np.trace(Lbad))
    assert abs(bad_trace - 718.0) > 1e-9, "wrong scene trace must differ from 718"
    print(f"FAIL_WRONG_SCENE_REJECTED  planted K(9,11,15) (35 vertices, trace {bad_trace:.0f} != 718) "
          "rejected as the forced scene")

    print("HONEST_GAP_POSITIVE_CHEEGER_NORMALIZED_BOUND_IS_THEOREM_TARGET")
    print("PASS_CONNECTIVITY_SPECTRAL_GAP_SPEED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
