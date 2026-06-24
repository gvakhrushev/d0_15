# D0-v16 Parallel Dual Closure — Cross-Gate & Joint Report

Two parallel tracks, one discipline (D0 selects finite operators; string/quiver only as external templates;
no branes/flux/CY/Wilson/GSO/α′/SUSY/PDG/fitted-mass/chosen-row inputs).

## Joint chain (where each track honestly stands)

$$
K(9,11,13)\to \mathfrak Q_{D0}\to C_{U(1)}\to \ker M_{U(1)}=\operatorname{span}\{Y,B\!-\!L\}\quad(\text{Track A, Case A2})
$$
$$
K(9,11,13)\to \text{shell-overlap tensor}\to (Y_u,Y_d)\to(H_u,H_d)\to V,\gamma\Rightarrow |\sin\Theta|\le\|V\|/\gamma\quad(\text{Track B})
$$

- **Track A** → Case **A2**: kernel = 2-dim `span{Y,B−L}`; unique `span{Y}` only via `Ξ_Y` (bridge, MECH-LIMIT);
  graph-flow origin `Φ` open (PROOF-TARGET+PASSPORT). See `D0_FINITE_MASSLESS_U1_KERNEL_RESULT.md`.
- **Track B** → CKM topology CERTIFIED, magnitude **PROOF-TARGET**; finite Davis–Kahan bound `C=1` (new). Missing
  `Ξ_CKM`. See `D0_FINITE_YUKAWA_CKM_GAP_RESULT.md`.

## Cross-gate `[Q,Y]=0` over the kernel family — `D0-CKM-YUKAWA-KERNEL-CROSSGATE-001` (CORE-FORMALIZED)

The Yukawa must intertwine the gauge action for **every** generator of the Track-A kernel, not a hand-picked
row. With Higgs `H` of charges `(Y=1/2, B−L=0)`, the invariance residuals
`(X_Q−X_{u_R}+X_H,\ X_Q−X_{d_R}−X_H)` **vanish for both `Y` and `B−L`** (`crossgate_holds`, decidable over ℚ),
and break for a generator outside `span{Y,B−L}` (`crossgate_control`). So:

> The Yukawa is invariant under the **entire** 2-dim kernel `span{Y, B−L}` — it does **not** select the
> hypercharge row over `B−L`. This is the protection against a hidden hypercharge-row choice: Track B does not
> secretly assume what Track A leaves 2-dimensional. Row selection still requires `Ξ_Y` (the bridge), which the
> gate does **not** supply.

`NoHiddenCatalog`: no flux/modulus/phase/PDG/fitted/chosen-row input enters either track (cert guards +
`check_physical_bridge_discipline`).

## Minimal missing operators (named, owned)
- `Ξ_{U(1)} = Φ`: `ker B_graph (327) → Weyl charge ledger` — `D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`
  (PROOF-TARGET) + `PRIM-FINITE-SPECTRAL-TRIPLE-REP` (PASSPORT). Blocked by the representation-reconstruction NO-GO.
- `Ξ_{CKM}` ∈ {up/down pairing, common-left-carrier id `Ξ_{ud}`, holonomy→mismatch}: fixes the source-native
  `(Y_u,Y_d)` pair + `(V,γ)`.

## Build / source manifest
See `D0_PARALLEL_QUVER_YUKAWA_SOURCE_MANIFEST.json`. New Lean this campaign:
`D0.ParallelClosure.{FiniteDavisKahanGapBound, CrossGate}`; cert `d0_ckm_mismatch_bound_verify.py`. Everything
else is **cite-only** (Track A fully owned; Track B pair-NO-GO pre-existing). Gates green: `lake build D0.All`,
`d0_score` (integrity demotions 0), `check_cert_can_fail`, `check_physical_bridge_discipline`, book/coverage,
`validate_csv`.
