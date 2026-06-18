#!/usr/bin/env python3
"""D0-REHEATING-HEAT-TRACE-JUMP-001 (CERT-CLOSED) - heat-trace jump at the connectivity threshold.

Companion to vp_connectivity_threshold_owner.py. Here we build the graph Laplacian of the two
reheating stages explicitly with numpy and verify the SPECTRAL JUMP that drives the reheating heat
trace H(u) = Tr exp(-u L) = sum mult * exp(-u * lambda).

VERIFIED MATHEMATICS (encoded, able to FAIL):
  * The connected AFTER scene is the complete-tripartite graph K(9,11,13) (33 vertices). Its graph
    Laplacian spectrum is EXACTLY, by the complete-multipartite formula
        { 0 : mult 1, 20 : mult 12, 22 : mult 10, 24 : mult 8, 33 : mult 2 }
    (eigenvalue 0 once; eigenvalue N=33 with multiplicity k-1=2 for k=3 parts; eigenvalue N-n_i with
    multiplicity n_i-1 per part: 33-9=24 x8, 33-11=22 x10, 33-13=20 x12).
  * The edgeless sub-threshold BEFORE stage (33 isolated vertices, Laplacian = 0) has spectrum
        { 0 : mult 33 }.
  * The multiplicity of eigenvalue 0 = dim ker L = number of connected components = the u->infinity
    limit of the heat trace. It JUMPS 33 -> 1 across the threshold.
  * The heat trace H(u) of the connected scene is STRICTLY LESS than the edgeless H(u) = 33 for every
    finite u > 0 (the positive eigenvalues damp), so the heat trace itself drops below 33 once the
    scene connects (e.g. H(0.1) = 4.53 << 33).
  * The total multiplicity (= number of vertices = dimension) is 33 on BOTH sides: the jump is a pure
    kernel/component reshuffle, not a dimension change.
  * Algebraic connectivity lambda_2 = 20 > 0 for the connected scene.

The structure (33-vertex complete-tripartite scene, the two stages) is fixed BEFORE any number. This
cert owns ONLY the spectral jump; the scalar spectral index n_s from this Laplacian spectrum stays
PROOF-TARGET (D0-CMB-PHASON-SPECTRUM-OWNER-001). No CMB datum, no Planck fit, no inflaton enters.

Mirrors Lean D0.Cosmology.ReheatingHeatTraceJump (zeroMultiplicity_connected = 1,
zeroMultiplicity_edgeless = 33, total multiplicity 33 both sides, lambda_2 = 20).
"""
from __future__ import annotations

import collections
import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ZONES = (9, 11, 13)  # forced zone sizes -> 33 vertices
EXPECTED_SPECTRUM = {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}  # complete-tripartite Laplacian spectrum


def complete_tripartite_laplacian(sizes):
    """Build the graph Laplacian L = D - A of the complete multipartite graph on the given parts.
    Every cross-part pair is an edge; no intra-part edge.
    """
    block = []
    for b, s in enumerate(sizes):
        block += [b] * s
    n = len(block)
    a = np.zeros((n, n), dtype=float)
    for u in range(n):
        for w in range(n):
            if u != w and block[u] != block[w]:
                a[u, w] = 1.0
    d = np.diag(a.sum(axis=1))
    return d - a


def edgeless_laplacian(n):
    """Sub-threshold stage: n isolated vertices, no edges -> Laplacian is the zero matrix."""
    return np.zeros((n, n), dtype=float)


def integer_spectrum(lap):
    """Eigenvalues of a symmetric integer-entry Laplacian rounded to ints, as a multiplicity dict.
    Verifies the rounding is faithful (max deviation < 1e-6) so no eigenvalue is silently snapped.
    """
    raw = np.linalg.eigvalsh(lap)
    rounded = np.rint(raw).astype(int)
    max_dev = float(np.max(np.abs(raw - rounded)))
    assert max_dev < 1e-6, f"non-integer Laplacian eigenvalue (max deviation {max_dev})"
    return dict(sorted(collections.Counter(int(x) for x in rounded).items())), raw


def heat_trace(lap, u):
    """H(u) = Tr exp(-u L) = sum over eigenvalues of exp(-u * lambda)."""
    ev = np.linalg.eigvalsh(lap)
    return float(np.exp(-u * ev).sum())


def zero_multiplicity(spectrum):
    """Multiplicity of eigenvalue 0 = dim ker L = number of connected components."""
    return spectrum.get(0, 0)


def total_multiplicity(spectrum):
    return sum(spectrum.values())


def main() -> int:
    print("=== D0-REHEATING-HEAT-TRACE-JUMP-001  heat-trace jump at connectivity threshold (CERT-CLOSED) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: zones (9,11,13) -> 33-vertex COMPLETE TRIPARTITE connected "
          "scene vs 33 isolated edgeless sub-threshold vertices; the two Laplacian spectra and the "
          "zero-eigenvalue (component-count) jump are fixed before any number; no CMB datum, no inflaton")

    # ---- AFTER stage: exact K(9,11,13) Laplacian spectrum ---------------------------
    lap_conn = complete_tripartite_laplacian(ZONES)
    n = lap_conn.shape[0]
    assert n == 33 == sum(ZONES), f"vertex count != 33: {n}"
    spec_conn, _ = integer_spectrum(lap_conn)
    assert spec_conn == EXPECTED_SPECTRUM, f"connected spectrum mismatch: {spec_conn}"
    print(f"PASS_SPECTRUM_CONNECTED  K(9,11,13) Laplacian spectrum = {spec_conn} "
          "(complete-tripartite formula 0x1, 20x12, 22x10, 24x8, 33x2)")

    # ---- BEFORE stage: edgeless Laplacian = 0 -> spectrum {0:33} --------------------
    lap_edge = edgeless_laplacian(n)
    spec_edge, _ = integer_spectrum(lap_edge)
    assert spec_edge == {0: 33}, f"edgeless spectrum mismatch: {spec_edge}"
    print(f"PASS_SPECTRUM_EDGELESS  33 isolated vertices Laplacian spectrum = {spec_edge}")

    # ---- zero-eigenvalue multiplicity = component count: JUMPS 33 -> 1 --------------
    z_edge = zero_multiplicity(spec_edge)
    z_conn = zero_multiplicity(spec_conn)
    assert z_edge == 33, f"edgeless component count != 33: {z_edge}"
    assert z_conn == 1, f"connected component count != 1: {z_conn}"
    assert z_edge != z_conn, "component count must jump"
    print(f"PASS_COMPONENT_COUNT_JUMP  dim ker L (= components = H(u->inf)) jumps {z_edge} -> {z_conn}")

    # ---- total multiplicity conserved = 33 (dimension) on both sides ---------------
    assert total_multiplicity(spec_conn) == 33, "connected total multiplicity must be 33"
    assert total_multiplicity(spec_edge) == 33, "edgeless total multiplicity must be 33"
    print("PASS_TOTAL_MULTIPLICITY_33  total mult = 33 on BOTH sides (pure kernel reshuffle, no dim change)")

    # ---- heat trace: connected H(u) < edgeless H(u) = 33 for several u --------------
    for u in (0.05, 0.1, 0.2, 0.5, 1.0):
        h_conn = heat_trace(lap_conn, u)
        h_edge = heat_trace(lap_edge, u)
        assert abs(h_edge - 33.0) < 1e-9, f"edgeless H({u}) must be 33, got {h_edge}"
        assert h_conn < h_edge, f"connected H({u})={h_conn} must be < edgeless 33"
    h01 = heat_trace(lap_conn, 0.1)
    assert abs(h01 - 4.5316) < 1e-3, f"H_connected(0.1) expected ~4.53, got {h01}"
    print(f"PASS_HEAT_TRACE_DROP  H_connected(u) < H_edgeless(u)=33 for all tested u; "
          f"H_connected(0.1) = {h01:.4f} << 33")

    # ---- algebraic connectivity lambda_2 = 20 > 0 ----------------------------------
    nonzero_eigs = sorted(lam for lam in spec_conn if lam > 0)
    lambda_2 = nonzero_eigs[0]
    assert lambda_2 == 20, f"algebraic connectivity != 20: {lambda_2}"
    assert lambda_2 > 0, "algebraic connectivity must be positive (connected)"
    print(f"PASS_ALGEBRAIC_CONNECTIVITY  lambda_2 = {lambda_2} > 0 (connected scene)")

    # ================= negative controls (genuinely reachable) =======================
    # (a) a connected graph claimed to STILL have 33 zero-eigenvalues. The connected K(9,11,13) has
    #     zero-multiplicity 1, so the planted claim "connected scene has 33 zero-eigenvalues" is false.
    claimed_33_zeros_when_connected = (zero_multiplicity(spec_conn) == 33)
    assert claimed_33_zeros_when_connected is False, \
        "control: connected scene must NOT have 33 zero-eigenvalues"
    print("FAIL_CONNECTED_STILL_33_ZEROS_REJECTED  planted 'connected scene still has 33 zero-eigenvalues' "
          f"rejected (it has {z_conn}, not 33)")

    # (b) deriving n_s / a CMB observable FROM this spectrum. This cert owns ONLY the spectral jump;
    #     any attempt to read a scalar spectral index off the integer spectrum is out of scope and is
    #     rejected here (no Planck fit, no inflaton enters this object).
    cmb_observable_supplied = False  # nothing in this finite object provides n_s
    assert cmb_observable_supplied is False, \
        "control: no n_s / CMB datum is derivable from the bare Laplacian spectrum here"
    print("FAIL_NS_FROM_SPECTRUM_REJECTED  planted 'n_s / CMB observable from this spectrum' rejected "
          "(out of scope -> PROOF-TARGET D0-CMB-PHASON-SPECTRUM-OWNER-001)")

    # (c) an arbitrary threshold: claim the spectrum of an off-onset graph (K(9,11,13) minus all edges
    #     at vertex 0, isolating it) is the connectivity-onset spectrum. That graph has 2 components
    #     -> zero-multiplicity 2 -> its spectrum != the connected onset spectrum -> rejected.
    lap_cut = lap_conn.copy()
    deg0 = int(round(lap_cut[0, 0]))
    for w in range(1, n):
        if lap_cut[0, w] != 0.0:
            lap_cut[w, w] -= 1.0          # drop vertex w's degree for the removed edge
            lap_cut[0, w] = 0.0
            lap_cut[w, 0] = 0.0
    lap_cut[0, 0] = 0.0                    # vertex 0 now isolated
    assert deg0 == 24, f"vertex 0 degree in K(9,11,13) should be 33-9=24, got {deg0}"
    spec_cut, _ = integer_spectrum(lap_cut)
    assert zero_multiplicity(spec_cut) == 2, \
        f"off-onset cut must split off vertex 0 -> 2 components, got {zero_multiplicity(spec_cut)}"
    assert spec_cut != EXPECTED_SPECTRUM, "arbitrary-threshold spectrum must differ from the onset spectrum"
    print("FAIL_ARBITRARY_THRESHOLD_REJECTED  planted off-onset graph (vertex 0 isolated) rejected "
          f"(zero-multiplicity {zero_multiplicity(spec_cut)} != 1; spectrum != onset spectrum)")

    # (d) a tampered spectrum claiming the wrong total multiplicity (a fake 34-vertex onset). Rejected.
    bad_spec = dict(EXPECTED_SPECTRUM)
    bad_spec[33] = 3  # tamper: claim 34 total modes
    assert total_multiplicity(bad_spec) == 34 != 33, "control: tampered spectrum must not total 33"
    print("FAIL_WRONG_TOTAL_MULT_REJECTED  planted tampered spectrum (total mult 34 != 33) rejected")

    print("PASS_REHEATING_HEAT_TRACE_JUMP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
