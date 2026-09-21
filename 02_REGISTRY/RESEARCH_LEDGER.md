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
| rev.5 source stratification | PENDING EXPENSIVE AUDIT | Evidence: the three tensor sectors (dim 296) have zero row/column marginals; the projected signed vertex-source channel reaches only A11; triangle sources reach tensor sectors. Repeated coefficient 234=2·9·13 and 234/11 appears in the same A11 defect channel. | Must determine whether “V11 is special” is intrinsic or merely the middle-zone consequence of the chosen transitive orientation. General K(a,b,c) theorem is the next research target. |

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
