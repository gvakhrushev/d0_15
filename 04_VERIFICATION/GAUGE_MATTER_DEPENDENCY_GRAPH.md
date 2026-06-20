# D0 Gauge–Matter Functor — Dependency Graph (Iteration 22)

The finite gauge–matter spine, each node either a machine-owned closure or a named PROOF-TARGET with
its exact missing artifact (`GAUGE_MATTER_BLOCKERS.csv`). **Global closure is NOT claimed** — the
unified functor is open until the lepton resolvent, the Higgs double-well sign, and the CKM overlap
close. No SM charge table / PDG mass / measured CKM angle / 246 GeV is an input anywhere.

```
FiniteSceneData  K(9,11,13): 33 V, 359 E, cycle rank 327; rank 3 / nullity 30; DΣ = 5 roles; q_T=44
  └─ A. DΣ role-cycle carrier  DSigma -> Lambda_flow                         [PROOF-TARGET: scene-determined 5-role carrier not built]
  └─ B. Hypercharge -> Weyl ledger
        • 5-field anomaly ROW  D0-SM-HYPERCHARGE-ROW-OWNER-001                [CERT-CLOSED ✓ new]
            cubic = −18a(t−3a)(t+3a) ⇒ rays {a=0, t=3a, t=−3a}; SM = t=−3a, a=1/6, unique up to
            normalization + u↔d labeling + excluding degenerate Y_Q=0; B−L is the added-ν_R direction
        • flow lattice dim 327  D0-HYPERCHARGE-FLOW-LATTICE-001              [CERT-CLOSED, frozen]
        • minimal denominator 6 D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001    [CERT-CLOSED, frozen]
        • 6-field anomaly variety 2-dim  D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001  [NO-GO, frozen]
        • flow→Weyl map Φ  D0-HYPERCHARGE-FLOW-TO-WEYL-MAP / …GRAPH-FLOW-OWNER   [PROOF-TARGET: Φ from flow not built]
  └─ C. CKM selector + overlap
        • class-5 exclusion  D0-CKM-CLASS5-SELECTOR-OWNER-001 / D0-CLASS5-ALIASING-001  [CERT/CORE, frozen]
        • positive order-step-det selector  D0-CKM-ORDER-STEP-DET-SELECTOR-001          [PROOF-TARGET]
        • finite overlap invariant  D0-CKM-FINITE-OVERLAP-INVARIANT-001                 [PROOF-TARGET: up/down carriers]
  └─ D. Lepton shell Green resolvent
        • branch index 1/n + genus-0  D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001        [CERT-CLOSED, frozen]
        • branch index ⊬ operator  D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001         [NO-GO, frozen]
        • Green resolvent + projectors  D0-LEPTON-SHELL-GREEN-RESOLVENT / …BRANCH-PROJECTOR  [PROOF-TARGET, projector labels BOUNDED by the NO-GO]
  └─ E. Higgs rank-2 scalar feedback
        • log-det variation + stationarity  D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001    [CERT-CLOSED, frozen]
        • rank-2 scalar projector  D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001           [CORE, frozen]
        • Hessian double-well sign  D0-HIGGS-PHASON-HESSIAN-SIGN / …CONDENSATION-OWNER  [PROOF-TARGET: missing finite Q(θ) with f''(0)<0]
  └─ F. Unified Gauge–Matter Functor  D0-GAUGE-MATTER-FUNCTOR-OWNER-001       [PROOF-TARGET: assembles closed pieces; open until A/C-overlap/D/E close]
```

## Closed this campaign (1 new)
`D0-SM-HYPERCHARGE-ROW-OWNER-001` (CERT-CLOSED, Lean `D0.Matter.SMHyperchargeRowOwner`): the hypercharge
row is the **unique** anomaly-free 5-field assignment up to normalization, u↔d labeling, and the
degenerate branch — the cubic factors exactly as `−18a(t−3a)(t+3a)`. This converts the eight-front
"row not unique" finding into its precise resolution: the 2-dimensional freedom was the *added* ν_R
(B−L), not the row.

## Remaining (exact, in GAUGE_MATTER_BLOCKERS.csv)
Two are **bounded by existing no-gos** (not open-ended): the lepton branch-projector labels cannot be
uniquely operator-determined (`D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001`), and the hypercharge
*flow*-map Φ remains while the *row* is now owned by the anomaly route. The genuinely-open frontier:
the DΣ role-cycle carrier (A), the lepton finite Green resolvent (D), the Higgs double-well finite
`Q(θ)` (E), and the CKM up/down overlap carriers (C). The unified functor (F) is the assembly step.
