# D0_GAUGE_HORIZON_EDGE_COEFFICIENT_SYNTHESIS.md

## 1. Scope and Objective

This document formulates three D0 sector laws as finite operator algebra: gauge-boundary confinement, horizon emission, and the edge-sector electromagnetic coefficient target. External QFT, greybody and QED comparisons remain passport layers after the finite objects are frozen.

## 2. Confinement as Commutator Obstruction (Mass Gap)

The D0 confinement sector is the gauge-boundary lower-bound problem at the retained/traced cut $P_N/Q_N$.

**Sector law / theorem target (Gauge Boundary Obstruction).**
Let $g \in G$ be a gauge generator acting on $\mathcal{H}_N$.
1.  **Abelian Phase ($U(1)$):** The generator commutes with the active projection, $[P_N, g_{U(1)}] = 0$. Thus, $P_N$ is an invariant subspace. The operator $Q_N U_N P_N$ evaluates to zero for pure phase modes, yielding zero boundary leakage for this protected phase mode.
2.  **Non-Abelian Color ($SU(3)$):** The non-commutative generators do not preserve the boundary cut: $[P_N, g_{SU(3)}] \neq 0$. Applying a color rotation strictly mixes $P_N$ states into $Q_N$.
The internal lower-bound target for non-singlet color states is:
\[
\langle \psi_{color} | F_N | \psi_{color} \rangle = \| Q_N U_N P_N \psi_{color} \|^2 \ge m_{gap}^2 > 0.
\]
*Conclusion:* Non-singlet terminal stability is obstructed when this leakage is bounded away from zero. Continuum Yang-Mills comparison is a bridge/passport layer.

## 3. Horizon Emission as Conjugate Feedback

Horizon emission is represented internally as conjugate archive-to-retained leakage under boundary-capacity saturation.

**Sector law / theorem target (Conjugate Emission).**
When the active boundary $P_R$ reaches capacity saturation ($\sigma(R) \to 1$), information is quotiented into the Archive $Q_R$. The probability of emission back into the active sector is governed by the **conjugate feedback operator**:
\[
\tilde{F}_R^{emit} = Q_R U_R P_R U_R^\dagger Q_R.
\]
For a boundary mode $|\psi_{\ell, \omega}\rangle$, the finite greybody candidate is the diagonal element:
\[
\Gamma_\ell(\omega) = \langle \psi_{\ell, \omega} | \tilde{F}_R^{emit} | \psi_{\ell, \omega} \rangle.
\]
*Conclusion:* The finite emission object is the conjugate feedback expectation. Thermality and continuum greybody comparison are downstream passports.

## 4. Edge-Sector Trace and the $\alpha$ Target

The electromagnetic coefficient-origin program is reduced to an edge-sector trace/residue invariant.

**Theorem Target (1-Skeleton Feedback).**
Let $P_E$ be the orthogonal projector onto the 359 edges of the topological carrier $K(9,11,13)$. Let $U_E$ be the U(1) phase-return dynamics on edges. The finite target for the inverse topological electromagnetic normalization is the 1-loop feedback trace:
\[
\alpha_{top}^{-1} \stackrel{!}{=} \operatorname{Tr}(P_E U_E^\dagger Q_E U_E P_E).
\]
*   **Main trace:** Each of the 359 edges yields an irrational return phase contribution of $\varphi^{-2}$.
*   **Boundary Leakage:** The precise term $-\varphi^{-5}$ is the deterministic fractional leakage into the global memory torus due to its geometric aspect ratio $R/r = \varphi^5$.
This defines the D0 bare graph-invariant target; QED running and external numerical comparison are separate passports.

## 5. Negative Controls and Guardrails

*   **FAIL_MASS_GAP_FROM_QFT_LATTICE:** Do not cite lattice QCD Wilson loops to prove the mass gap. The D0 sector target is the $[P_N,g]\neq0$ boundary-leakage lower bound.
*   **FAIL_HAWKING_THERMODYNAMICS_PRIMITIVE:** Do not import Bogoliubov transformations or thermal KMS states as axioms. Emission is strictly $\langle \psi | \tilde{F} | \psi \rangle$; thermality is a downstream property of $Q$-sector capacity saturation.
*   **FAIL_ALPHA_FROM_RG_FIT:** Do not treat $359\varphi^{-2}$ as a tuned parameter to match $137.0359$. It must be evaluated algorithmically as a discrete $\operatorname{Tr}(F_E)$.

## 6. Certificate Skeletons (Ready for Python/Lean)

**Cert 1: Confinement Commutator (`vp_gauge_boundary_obstruction.py`)**
