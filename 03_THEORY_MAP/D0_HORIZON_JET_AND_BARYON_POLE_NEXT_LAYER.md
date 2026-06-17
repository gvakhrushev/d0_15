# D0 Horizon Jet and Baryon Pole Next Layer

## 1. Status Split (Researcher B Integration)

This document records the current closure status for the horizon/jet and baryon anonymous pole layers after integration of Researcher B contributions.

- **HORIZON-EMISSION-LAW**: CLOSED. Horizon emission is archive-to-retained boundary leakage under capacity saturation. The conjugate feedback form \(\tilde F_R^{emit} = Q_R U_R P_R U_R^\dagger Q_R\) and greybody candidates are certified at the finite operator level (see vp_horizon_emission_conjugate_feedback.py and vp_horizon_jet_axis_observable.py).

- **OPTICAL-JET-COLLIMATION-TARGET**: OPEN finite inequality after frozen projectors. The axis observable and collimation target remain theorem targets; no claim of full law closure. The jet backreaction is a finite inequality on the saturated seam after the projectors are fixed.

- **BARYON-ANONYMOUS-POLE-SCAFFOLD-CLOSED**: CLOSED. The 40/56 carriers and anonymous pole equations on the image of the projectors are closed (see vp_cvft_baryon_40_56_decomposition.py and vp_baryon_40_56_anonymous_poles.py). Eigenvalues are computed on the image basis, not the padded full 216D matrix.

- **PDG passport**: EXTERNAL. All physical naming, GeV conversion, widths, and decay assignments remain passport-layer operations after the internal carriers and poles are frozen. No PDG data enters the definition of the finite objects or the choice of projectors.

## 2. Horizon Emission Law (Closed)

Horizon emission is represented internally as the conjugate archive-to-retained leakage under boundary-capacity saturation. The finite greybody candidate is the diagonal element of the conjugate feedback operator on boundary modes.

## 3. Optical Jet Collimation Target (Open)

The optical jet axis observable is a finite directional backreaction on the saturated archive seam. Collimation is expressed as a finite inequality after the retained/traced projectors and the emission operator are frozen. This is a synthesis target, not a closed law.

## 4. Baryon Anonymous Pole Scaffold (Closed)

On the certified carriers \(\Pi_B^{40}\) and \(\Pi_B^{56}\):

\[
U_{\rm eff}^{B,k} = \Pi_B^k P U P \Pi_B^k, \quad k \in \{40,56\}.
\]

Poles via \(\det(I - \zeta U_{\rm eff}^{B,k}) = 0\) on the image of the projectors. Eigenvalues of the compressed operator are obtained by restriction to the support of \(\Pi_B^k\) (image basis), not by zero-padding to the full 216-dimensional space.

## 5. Negative Controls / Guardrails
- Treating the jet collimation inequality as a closed law before the projectors are frozen is forbidden.
- Computing baryon poles on the full padded 216D matrix (instead of the image of the 40/56 projectors) is forbidden.
- Using PDG data to select the spin/flavour projectors or to close the anonymous poles is forbidden.

## 6. Cert Tokens
- PASS_HORIZON_EMISSION_LAW_CLOSED
- PASS_BARYON_ANONYMOUS_POLE_SCAFFOLD_CLOSED (image-basis eigenvalues)
- TARGET_OPTICAL_JET_COLLIMATION_INEQUALITY (open)
- FAIL_PDG_BEFORE_FROZEN_POLES
- FAIL_FULL_216D_BARYON_EIGENVALUES

## 7. Relation to Grand Synthesis and Book Patches
See Book 07 for the horizon emission law insertion and the jet observable target. See Book 04 for the baryon anonymous pole scaffold. External PDG passport remains the boundary for physical particle naming.

(Support in the v15 closure cert runner and the two new certs listed in Deliverable 3.)
