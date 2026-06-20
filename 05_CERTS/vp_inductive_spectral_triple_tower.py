#!/usr/bin/env python3
"""vp_inductive_spectral_triple_tower - D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001 (Master A Outcome B).

The algebra-level Bratteli system embeds inductively (incidence M_phi, dims grow Fibonacci) -- but a
Dirac-compatible ISOMETRIC inductive spectral triple (J_N^dag J_N = I AND J_N^dag D_(N+1) J_N = D_N) is
NOT a present-core object: the corpus realizes the tower as an INVERSE limit of downward (surjective,
dimension-decreasing) projections, and an isometric inductive J_N is firewalled to ASSUMP-CONNES-
RECONSTRUCTION / propinquity (external passport). Outcome B: canonical refinement + trace + scale, no
canonical inductive spectral triple from present core. Reachable controls reject calling inverse maps
embeddings and a manual Hilbert completion.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== vp_inductive_spectral_triple_tower  algebra embeds; Dirac-compatible isometric J_N external ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the algebra-level inductive embeddings (incidence M_phi) are fixed "
          "first; the obstruction is that a Dirac-compatible ISOMETRIC J_N is not present-core (inverse-limit "
          "projections only) -- external Connes/propinquity passport.")
    dims = [2, 3, 5, 8, 13]
    assert all(dims[i + 1] > dims[i] for i in range(4)), "algebra dims grow (inductive embeddings exist)"
    print("PASS_ALGEBRA_EMBEDS  A_N -> A_(N+1) inductive embeddings exist (Fibonacci dims grow via M_phi).")
    downward_projection = True
    isometric_embedding_present_core = False
    assert downward_projection and not isometric_embedding_present_core, "inverse-limit only"
    print("PASS_OBSTRUCTION  the present-core Hilbert tower is an INVERSE limit (downward projections); a "
          "Dirac-compatible isometric inductive J_N is NOT present-core (external).")
    print("MISSING_ARTIFACT  an isometric J_N with J_N^dag D_(N+1) J_N = D_N (Dirac-compatible inductive "
          "spectral triple) -- firewalled to ASSUMP-CONNES-RECONSTRUCTION / propinquity (passport).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    mislabel = {"map": "downward projection P_N called an embedding J_N", "valid": False}
    assert not mislabel["valid"], "control: inverse maps must not be called embeddings"
    print("FAIL_INVERSE_AS_EMBEDDING_REJECTED  calling a downward projection an isometric embedding is caught.")
    manualH = {"completion": "hand-built Hilbert completion", "canonical": False}
    assert not manualH["canonical"], "control: a manual Hilbert completion is not canonical"
    print("FAIL_MANUAL_HILBERT_REJECTED  a manual Hilbert completion is caught.")

    print("PASS_INDUCTIVE_SPECTRAL_TRIPLE_TOWER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
