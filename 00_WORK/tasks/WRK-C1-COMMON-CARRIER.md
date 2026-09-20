# WRK-C1-COMMON-CARRIER

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

## Exit Condition
Formalize the research-certified common-carrier theorem on the literal K(9,11,13) edge space: unsigned B₊, signed B₋ with transitive orientation, their exact kernel dimensions, the explicit H-equivariant Euclidean isometry U:ker(B₊)→ker(B₋), the rank-10 correction, the omega complement and projector identities, while preserving the semantic firewall that B₊ is the A1 Weyl/Ward endpoint-sum operator and is not the signed Hodge/current divergence.
