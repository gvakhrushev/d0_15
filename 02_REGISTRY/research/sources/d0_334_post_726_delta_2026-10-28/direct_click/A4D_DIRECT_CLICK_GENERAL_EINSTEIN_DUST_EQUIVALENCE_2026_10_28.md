# Direct-click nonlinear source: general local Einstein–dust equivalence and source recovery

28 October 2026. Existing research PR #334, `gvakhrushev/d0_15`.
Input: `726192353504a81a9ab2b751f9b6c7866271e75a`.

[Full Russian proof](sources/d0_mass_coordinate_equivalence_2026-10-28/PROOF_RU.md), [executed checker](sources/d0_mass_coordinate_equivalence_2026-10-28/check_equivalence.py), [observed receipt](sources/d0_mass_coordinate_equivalence_2026-10-28/result.json).

## Existing parent and the discharged restriction

Consume [the nonlinear direct-click Einstein–dust source](A4D_CLOSED_HISTORY_NONLINEAR_EINSTEIN_DUST_2026_10_28.md), blob `154b341f17adce88594b0b5e9df0d38c0283d288`. Its forward equation theorem and generic native source estimates are retained. Its explicit reverse/recovery example was LTB. This application removes that particular-geometry restriction, not the original full128/source-admission boundary.

## General theorem, not an additional special metric

Fix the existing regular positive branch of the SAME original polynomial r(x,y), with x=tau E R/2, y=tau q, y0>0, x0 r_x-y0 r_y=0, r_x>0, r_y<0, and invertible trace/Ward Jacobian. Define q0=y0/tau and kappa=-r_y/r_x=-x0/y0. This is the old exact algebraic branch; no fitted coupling or added matter action.

Every sufficiently smooth local Einstein–dust solution with THAT kappa, positive density, unit geodesic velocity and locally exact velocity one-form has a representation solving all16 coframe, all24 independent Lorentz-connection and both scalar Euler equations of the unchanged nonlinear functional. No spherical/homogeneous/LTB ansatz or weak-curvature approximation is needed.

The proof is constructive. Use the dust's own proper time t and transported spatial labels y. Continuity gives M(y)=rho E_y, independent of t. Set

    X1=(1/(2q0)) integral M(s,y2,y3) ds, X2=y2, X3=y3.

Its real positive Jacobian is M/(2q0), hence rho E_X=2q0. The SAME metric and psi_A=n_A sqrt(q0)t+c_A satisfy q=q0 and E_X R/2=-kappa q0. Thus the original nonlinear source equals tau r_x times the full source of integral[E R/2-kappa q], which vanishes in EVERY ambient direction. Coordinates are held fixed when varying; mass normalization and alignment are NOT imposed on the variations. The independent connection is varied before the Levi-Civita solution is inserted.

Together with the parent's forward theorem, this gives local two-way solution-class correspondence for the declared aligned timelike sector. Spatial labels remain nonunique; no identification of all microscopic archives is claimed. The method uses standard comoving mass coordinates, explicitly credited, not a new observer or clock primitive.

Separately, with both scalar fields constant, the regular branch is exactly vacuum Einstein: every Ricci-flat local Lorentz metric solves the same nonlinear continuum source, and its stationary constant-matter sector is Ricci-flat. The positive-density coordinate map is NOT continued through rho=0.

## Consume the actual finite-source theorem

The parent's regular C3 sampling/decoder and full-price finite-word comparison estimates apply to every lifted regular solution, not only LTB. At actual gain and sampling norm, one obtains

    ||ell_hat_h o DSample_h||_(C3*) <= C_tau h+epsilon_h ->0.

This is complete normalized-source recovery, not an exact stationary finite word. It retains same-input/clock/work comparisons and the true errors. At each level retention depth K is fixed across its stencil. Incoming7dc's positive different-duration price is preserved; growth is not free or price-neutral. Incoming7db's different original-full128 scale balance is also preserved and not relabelled as this result.

## Verification and limits

109 checks executed under ordinary Python and python -O with byte-identical JSON. All16 coframe derivatives at fixed independent connection, all24 connection derivatives, and two scalar rows vanish SYMBOLICALLY on an anisotropic dust control, with nonzero shear. The actual mass Jacobian and the nonlinear trace-equation syzygy are also exact. Omitting the volume Jacobian leaves a nonzero coframe row. Branch decimal calculations are diagnostics; the old strict interval owner is consumed, not rerun as a new certificate.

Proof SHA256 `d70ee9c87041dea710c86ab42217f6397510568a2cf6ec9ac66d7c2026646145`; Git blob `8cbf01f2c1cbdc01faf6755d4909c41591f41b0b`.
Checker SHA256 `b6cafe1585008dde4f02d7b1532a6eff5b6d4813e32cbe8fcbd9de5cfb9a3773`; Git blob `148b4def42505e1dd97d2301d96f9e331c4b8f39`.
Receipt SHA256 `4f2253e74b024f10ee10f53c9ea4bbdba9eddebc94a27a4ad05998160f853009`; Git blob `6b8cf153ea257d129b37a294cf429339832cf668`.

This proves a general reverse continuum theorem and consumes it in the existing source-recovery interface. It does NOT equate this programmed direct-click price to original full128, prove physical admission of every open-field direction, solve every independent apparatus equation, or produce exact finite stationary words. Arbitrary vortical/pressured matter, caustics, global total-mass/volume compatibility and universal Newton calibration are outside this theorem. No new native compiler, full128, Lean or repository CI run; no merge, lifecycle, raw216 or scientific promotion. `GR_closed=false`.
