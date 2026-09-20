# WRK-C1-COMMON-CARRIER — REVIEW

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective
Formalize the research-certified common-carrier theorem on the literal $K(9,11,13)$ edge space: unsigned $B_+$, signed $B_-$ with transitive orientation, their exact kernel dimensions, the explicit $H$-equivariant Euclidean isometry $U: \ker(B_+) \to \ker(B_-)$, the rank-10 correction, the $\omega$ complement and projector identities.

## Scope
1. Define the literal edge operators $B_+$ and $B_-$ with canonical transitive orientation $V_9 \to V_{11}$, $V_9 \to V_{13}$, $V_{11} \to V_{13}$.
2. Prove $\dim \ker B_+ = 326$ and $\dim \ker B_- = 327$.
3. Define the explicit map $U$: identity on $(9,11)$ and $(9,13)$, and $U(X) = X - \frac{2}{13} C_{11} X \mathbf{1}\mathbf{1}^T$ on $(11,13)$.
4. Prove $U(\ker B_+) \subseteq \ker B_-$, $U^* U = I_{\ker B_+}$.
5. Prove for $\omega = (13, -11, 9)$ that $B_- \omega = 0$, $\|\omega\|^2 = 42471$, $\operatorname{im} U = \ker B_- \cap \omega^\perp$, and $U U^* = I - \frac{\omega\omega^T}{42471}$ on the signed cycle space.
6. **Semantic Firewall:** Do not state $B_+ = B_-$, A1 Ward = Bianchi, unsigned endpoint-sum = signed current divergence, $U$ proves physical gravity coupling, $\omega$ is a physical propagating mode, or $Q_H$ is selected.

## Source Material
- `02_REGISTRY/frontier/C1_COMMON_CARRIER_RESULT.md`
- `02_REGISTRY/frontier/C1_COMMON_CARRIER_LEAN_TASK.md`
- `04_CERTIFICATES/vp_c1_common_carrier_reduced.py`

## Affected Claims
- `D0-HODGE-LINKS-001`
- `D0-SPECTRAL-EINSTEIN-001`

## Implementation & Formalization Evidence
- Lean module: `03_FORMALIZATION/D0/Geometry/SignlessSignedCommonCarrier.lean`
- Reused symmetry group: `LocalRelabelling := Equiv.Perm V9T × Equiv.Perm V11T × Equiv.Perm V13T`
- Induced edge relabelling: `edgeRelabel` on literal `SceneEdge`
- Carrier action: `sceneAction h X = fun e => X (edgeRelabel (localRelabellingInv h) e)`
- Proved symmetry theorems:
  - `BPlus_equivariant : BPlus (sceneAction h X) = vertexAction h (BPlus X)`
  - `BMinus_equivariant : BMinus (sceneAction h X) = vertexAction h (BMinus X)`
  - `U_equivariant : U (sceneAction h X) = sceneAction h (U X)`
- Exact kernel dimensions and isomorphism bridge:
  - `BPlusMatrix` and `BPlusLin` unify the operator on the literal edge carrier.
  - `BPlus_rank : Matrix.rank BPlusMatrix = 33`
  - `BPlus_kernel_finrank : Module.finrank ℚ (LinearMap.ker BPlusLin) = 326`
  - `BMinus_rank : Matrix.rank sceneBoundary1 = 32`
  - `BMinus_kernel_finrank : Module.finrank ℚ (LinearMap.ker BMinusLin) = 327`
  - `ker_BPlus_iso_ker_BMinus_perp` establishes the isomorphism between $\ker B_+$ and the sector orthogonal to $\omega$.
- Complement and Projector owners:
  - `omega_norm : ∑ e, (omega e)^2 = 42471`
  - `omega_BMinus_zero : BMinus omega = 0`
  - `Pmg` projector defines the matter-gravity sector mapping.
  - `ker_BMinus_decomposition` provides the explicit decomposition $Y = P_{mg}Y + \frac{\langle Y,\omega \rangle}{42471} \omega$.
- Rank-10 correction:
  - `RowCorrectionSpace` identifies the 10-dimensional space of centered row corrections.
  - `U_minus_I_in_RowCorrectionSpace` proves that $U - I$ maps into this space.
- Involutive Isometry:
  - `U_involutive` ($U^2 = I$)
  - `U_isometry` (Euclidean isometry on `SceneC1`)
- Companion exact Python certificate: `04_CERTIFICATES/vp_c1_common_carrier_reduced.py` (all checks PASS)
- Semantic firewall preserved: $B_+$ is unsigned endpoint sum (Weyl/Ward generator adjoint), $B_-$ is signed current divergence; no TT/Spin-2 module imported.

## Exit Condition
Formalize the research-certified common-carrier theorem on the literal K(9,11,13) edge space: unsigned B₊, signed B₋ with transitive orientation, their exact kernel dimensions, the explicit H-equivariant Euclidean isometry U:ker(B₊)→ker(B₋), the rank-10 correction, the omega complement and projector identities, while preserving the semantic firewall that B₊ is the A1 Weyl/Ward endpoint-sum operator and is not the signed Hodge/current divergence.
