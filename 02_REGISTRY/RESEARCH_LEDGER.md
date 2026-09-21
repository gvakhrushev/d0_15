# D0 Research Ledger

This file is a CONTROL research ledger, not a claim registry and not a proof owner.

Purpose: keep expensive research that materially changes the roadmap visible in the repository before it is promoted to Lean/claim/book ownership. A row may be accepted, accepted-with-repair, superseded, or pending. Nothing in this file upgrades `claims.csv` by itself.

Baseline mathematical snapshot for the gravity lane: `e6d9d4b7f17a4cf2f478cb737c90a98487939eaa`.

| Research | CONTROL disposition | Durable result affecting roadmap | Not yet owned / caution |
|---|---|---|---|
| A-X — dynamics adequacy of A1 | ACCEPT | The compensator-completed A1 Hessian is contact/constraint stiffness. For unit weight it is scalar on the 326-dimensional physical carrier and does not supply spatial dispersion. A separate kinetic operator is required. | Do not derive Q_H from the A1 Hessian. |
| A-EXT — continuum / spectral / TT bridge | ACCEPT WITH REPAIRS | Rieffel/GHP + Connes reconstruction do not own graded Hodge convergence, cochain→form/tensor lift, Lorentzian background, or TT readout. Continuum TT/Einstein remains an explicit external bridge stack. | Do not broaden the existing smooth-manifold passport into a tensor/TT passport. |
| A-CPL — weighted source/action coupling | ACCEPT WITH MAJOR SCOPE REPAIR | If the A1 conformal weight is typed to the owned unit scene weight, then W=I and the Euclidean C1 map U is the correct source/carrier transport with no new continuous coupling coefficient. The old request to identify A1 rho with the Perron profile is a category error. | The equality A1.rho = SceneSpectralAction.rho1 is not yet a typed theorem. Claims that W=I is already forced are conditional. Some early statements about Delta1 not preserving K+ are superseded by A-GRAV/A-SEL. |
| A-GRAV — terminal gravity audit | ACCEPT WITH REPAIRS | Literal Delta1 preserves K+ and commutes with U. Alpha remains unfixed by current finite stability/energy conditions. The old universal argument that 2L is “100% trace-mode” is withdrawn; the robust TT obstruction is representation-theoretic. | Finite gravity is not terminal while dynamics selection and physical readout remain unclassified. |
| A-SEL — exhaustive dynamics selector | ACCEPT AS RESEARCH | End_H(K+) is 6-dimensional. Under intrinsic degree-1 kinetic locality the class is span{I,Q_H,eps_A11}; imposing Hodge form leaves Q=c(Q_H+m^2 I), projectively one spatial modulus. The A11 direction is the unique non-Hodge kinetically-local defect/source direction. | The further specialization m^2=4 requires a theorem fixing the relative normalization of the Hodge kinetic term and the A1 contact term. It is conditional, not CORE. |
| A-MTT — mode-labelled spin-2 readout | ACCEPT AS RESEARCH | Full H=S9×S11×S13 admits no coefficient-free two-polarization readout. Replacing a total R^2 target by mode-labelled rank-2 fibres does not remove the obstruction; a genuine 2D fibre requires symmetry reduction/frame data. Existing Fin4 TT algebra can only be reused as a fibre/local chart, not the global scene target. | No TT readout has been built. Symmetry reduction/frame selection remains a genuine internal choice or an external readout input. |
| A-RAD — source-stratified radiative carrier | ACCEPT AS RESEARCH | General ordered-tripartite sign-pattern theorem: for any transitive orientation the C1/source defect is exactly the standard sector of the middle orientation zone; on the repository order this is A11. The projected signed vertex-source Gram is 4pq/(p+q) on that sector, not generically 2pq/m. The blockwise-zero-marginal tensor sector is canonical and carrier-free orthogonal to every linear signed vertex source, giving LINEAR-VERTEX-RADIATION-NOGO. The omega line is a uniform triangle source; triangle and quadratic vertex sources provide positive escape routes. Durable packet: `02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`. | Not TT/graviton ownership. The quadratic J⊗J coupling is a research map, not derived from the owned A1 action. Source stratification fixes neither m² nor alpha. The theorem-ready carrier-free core is assigned to `WRK-SOURCE-STRATIFICATION-NOGO`. |

| A-STRESS — quadratic matter→tensor source | ACCEPT AS RESEARCH | The A-RAD quadratic route spans the full tensor block once a scene vertex amplitude is supplied. Exact character theory gives dim Hom_H(Sym^2 C0,Z)=3, so all H-equivariant quadratic completions are the three block-weight directions; two essential selector ratios remain after overall scale. Current D0 matter ownership supplies no typed matter→SceneC0 amplitude, and ArchiveStressCoupling is anomalySum·archiveLaplacian, hence zero for anomaly-free matter and on the wrong carrier. Primary boundary: SOURCE-CARRIER-MISSING; secondary: SELECTOR-NOGO. Durable packet: `02_REGISTRY/research/ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md`. | No physical stress-energy/TT claim. A scene matter amplitude and a selector/action principle remain new primitives. The existing matter-stress CORE row remains valid for its literal zero-for-anomaly-free minimal coupling. |

| A-SOURCE — action/naturality selector | IN PROGRESS | Conditions on an abstract scene matter amplitude and tests whether triangle factorisation, Hodge exactness, SceneSpectralAction unit weight, universal edge-local actions, Dirichlet variation, cochain products, zone-relabel naturality, A1 pairing or Q_H compatibility reduce the exact 3-dimensional quadratic source class to one line. | Do not reopen A-STRESS's SOURCE-CARRIER-MISSING result. Active task: `EXP-ASOURCE-ACTION-NATURALITY-SELECTOR`. |

## Current gravity closure map

The finite lane should presently be read as:

```text
A1 Ward/source sector
    -> common carrier C1
    -> Hodge kinetic candidate / selector class
    -> temporal symplectic law
    -> physical readout
    -> external continuum/tensor/Einstein passport
```

CONTROL stop rule: each load-bearing arrow must eventually be CORE, NO-GO, BRIDGE/PASSPORT, or EMPIRICAL. Research results in this ledger are inputs to that classification, not terminal ownership by themselves.
