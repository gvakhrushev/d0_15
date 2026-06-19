# D0 Continuation Finish Campaign — Dependency Graph (Iteration 22)

Consolidation of the inherited closure campaigns (eight-front, static-to-dynamics, Nature bridge, deep-stitch). State discovery found the **closable items already closed** by prior committed campaigns; duplicates and mathematically-false-to-close items were NOT re-minted (recorded in `D0_CONTINUATION_STATE_TABLE.csv`). **Global closure is NOT asserted**: 18 named global blockers remain, each with an EXACT missing artifact in `FINAL_CONTINUATION_BLOCKERS.csv`.

## Tally

- Closed (CERT-CLOSED / NO-GO / CORE / PASSPORT-CLOSED / BRIDGE): 34
- PROOF-TARGET (exact gap named): 19
- Global blockers: 18
- Dropped as duplicate / mathematically-false-to-close (NOT minted): 10 (see state table)

## Not re-minted (would be faking)

- `...HYPERCHARGE-FLOW-TO-WEYL-MAP` / `...DSIGMA-ROLE-ORTHOGONALITY` / `...SM-HYPERCHARGE-ROW-OWNER` — row uniqueness is **false** (anomaly variety is 2-dim `span{Y,B-L}`, NO-GO `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`); folded into `D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001` (PROOF-TARGET).
- `...LEPTON-BRANCH-INDEX-UNIQUENESS` — Riemann-Hurwitz is genus-0 for every cyclic cover; does **not** force (4,3).
- `...CKM-CLASS5-POINTER-COLLISION` / `...CABIBBO-SOFT-JOINT-CLOSED` — duplicate of CORE `D0-CLASS5-ALIASING-001`.
- `...HIGGS-RANK2-SCALAR-SECTOR-PROJECTION` — duplicate of CORE `D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001`.
- `...ALPHA-FESHBACH-DIXMIER-NORMALIZATION-OWNER` — duplicate of `D0-ALPHA-FESHBACH-DIXMIER-OWNER-001`.

## Remaining global blockers (exact missing artifact each)

- **D0-ALPHA-FESHBACH-DIXMIER-OWNER-001** (C1-alpha): missing profinite/tower Dixmier pairing: residue->Delta_alpha normalization over the infinite 2^11 tower (external Dixmier/Wodzicki); finite heat trace cannot supply the 1/s pole
- **D0-DELTA-ALPHA-RESIDUE-PAIRING-OWNER-001** (C1-alpha): missing profinite/tower Dixmier pairing owner (same gap as D0-ALPHA-FESHBACH-DIXMIER-OWNER-001); the finite Feshbach residue recovers alpha_alg but not the Delta_alpha normalization
- **D0-DELTA-ALPHA-HEATTRACE-COEFFICIENT-OWNER-001** (C1-alpha): no positive owner from a finite trace (c_-1=0, c_0=dim=30); missing a regularized profinite trace whose s^-1 coefficient is 2^11*pi0*phi^-2
- **D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001** (C3-lepton): missing finite Green resolvent G_shell over the shell torus with provably-(0,1/4,1/3) branch indices PLUS operator uniqueness (branch index alone does not determine the operator)
- **D0-PHASON-WZ-EXPLICIT-FUNCTION-001** (C4-phason): missing continuum interpolation w_N -> w_D0(u) of the integer-window ratio on a declared late-time domain
- **D0-PHASON-WDE-Z-MAP-OWNER-001** (C4-phason): missing continuum interpolation PLUS the physical sign/magnitude normalization map to negative w_DE on the late-time window
- **D0-TORAL-TIME-MARKOV-CONJUGACY-001** (C5-toral): missing explicit Williams strong-shift-equivalence (R,S,L) chain witnessing topological conjugacy (SE invariants are necessary not sufficient; external Adler-Weiss)
- **D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001** (C5-toral): missing Voronoi/Lucas-cell-exact Markov-partition existence proof (boundary mapping); external Adler-Weiss owner stands
- **D0-LUCAS-MARKOV-PARTITION-OWNER-001** (C5-toral): missing internal Lucas/Voronoi Markov-partition existence proof; the GL(2,Z) similarity + SE invariants are CERT-CLOSED (D0-WILLIAMS-SHIFT-EQUIVALENCE-OWNER-001)
- **D0-HIGGS-PHASON-CONDENSATION-OWNER-001** (C6-higgs): missing proven double-well negative-quadratic sign f''(0)<0 (the spontaneous-symmetry-breaking condition is not forced); EOM stationarity is closed
- **D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001** (C7-hypercharge): missing flow->Weyl ledger map Phi PLUS an internally-derived Y_nuRc=0 and up/down branch selector; anomaly+constraints leave a 2-dim span{Y,B-L} variety (D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 NO-GO)
- **D0-CMB-PHASON-SPECTRUM-OWNER-001** (C8-cmb): missing canonical internally-forced IDS smoothing functional fixing (k,u) so n_s = f({lambda_i}) is a single determined value
- **D0-CMB-IDS-SMOOTHING-OWNER-001** (C8-cmb): missing canonical internally-forced smoothing/evaluation rule fixing the pair (k,u); spectrum alone does NOT determine n_s (NO-GO closed in D0-CMB-NS-LAPLACIAN-IDS-OWNER-001)
- **D0-SMOOTH-MANIFOLD-INTERNAL-RECONSTRUCTION-001** (D-geometry): missing finite-atlas -> smooth-shadow reconstruction (local-dim stability + discrete Poincare + heat-kernel Weyl); external Rieffel/GHP owner stands (ASSUMP-RIEFFEL-GHP)
- **D0-CONNES-GHP-SMOOTH-ATLAS-OWNER-001** (D-geometry): missing GHP-Cauchy convergence proof for the D0 refinement sequence (external Rieffel quantum-metric / GHP limit)
- **D0-GW-HORIZON-HUM-PASSPORT-001** (D-passport): missing external-data manifest (GWOSC event list + template-subtraction + pre-registered residual statistic); frozen internal object I_f=log phi exists
- **D0-GW-ECHO-SHORT-DELAY-PASSPORT-001** (D-passport): missing horizonless-seam short-echo-delay target + GWOSC external-data manifest
- **D0-DARK-RATIO-PASSPORT-001** (D-passport): missing cosmological-parameter external-data manifest for Omega_dark/Omega_visible; frozen internal object rank/nullity=3/30, visible 1/11, dark 10/11 exists

## Guards

`vp_final_continuation_dependency_graph.py` (graph integrity), `vp_continuation_no_status_only_diff.py` (no status-only promotion), `vp_continuation_no_overclaim.py` (no grand-closure / external-confirmation), `vp_static_dynamics_hamiltonian_bridge_integration.py` (S2D <-> Nature bridge, FORMALISM). Umbrella owners: `D0-CONTINUATION-FINAL-BLOCKER-GRAPH-001`, `D0-CONTINUATION-NO-STATUS-ONLY-DIFF-001`, `D0-STATIC-DYNAMICS-HAMILTONIAN-BRIDGE-INTEGRATION-001`.
