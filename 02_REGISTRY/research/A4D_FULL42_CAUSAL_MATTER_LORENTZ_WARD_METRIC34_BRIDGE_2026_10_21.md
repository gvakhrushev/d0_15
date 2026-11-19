# D0 — robust SAME FULL 42→34 bridge after genuine 4D two-CAR-field correction: nondegenerate Lorentz gauge, metric10 and link24

21 October 2026, existing Draft PR #334 / EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constitutive/native-programme-v1. Positive exact finite Lorentz-source/metric-coordinate theorem on the original diagonal rank-two coframe chart, **without** special restrictions on the TWO scalar stress directions. Consumes the genuinely full-4D causal material solver \`A4D_CAUSAL_TWO_SCALAR_FULL4D_EXACT_MATTER_SCHUR_2026_10_21.md\`, the ORIGINAL gauge/Ward12 reduction \`check_ward12_spatial_source_equivalence.py\`, old \`A4D_ORIGINAL_FULL128_COMMON_METRIC10_LINK24_JONES_TOMOGRAPHY_2026_10_20.md\`, and the complete original six-face Star+CAR source. No new field, action, Info contract, or root claim. \`GR_closed=false\`.

## 1. An actual hostile mismatch: correcting both real matter equations adds new offdiagonal coframe sources

The old rank-two \`42→12\` theorem is EXACT but uses more than SO Ward: it requires the very special diagonal-coframe/pure-boost stress/source support (7 coframe+15 spatial-link slots). On true n24/L8 4D Golden PF, the newly corrected two-scalar Cauchy solution has generic nonzero off-diagonal products
\[
T_{\mu\nu}^{(\Psi)}
=\sum_{A=0}^1D_\mu^+\Psi_A D_\nu^+\Psi_A .
\]
Direct original source audit gives nonzero \(\max|T_{tx}|\approx1.68481\times10^{-4}\), \(\max|T_{ty}|\approx7.36183\times10^{-5}\), \(\max|T_{xy}|\approx9.40879\times10^{-5}\). These give genuine NEW ambient coframe source components under \(q=g^{\mu\nu}T_{\mu\nu}\), even when the independent two matter Euler rows vanish. In particular at diagonal \(e=\operatorname{diag}(A,B,C,D)\), \(\eta=\operatorname{diag}(1,-1,-1,-1)\),
\[
\boxed{\frac{\partial q}{\partial e_{0,1}}=
\frac{2}{AB^2}T_{tx},\qquad
\frac{\partial q}{\partial e_{1,2}}=
\frac{2}{BC^2}T_{xy}.}
\tag{1}
\]
The true native nonlinear material coefficient \(F_y\) is nonzero on this strict chart. Thus setting all old 12 selected spatial-link rows to zero is NOT by itself a complete zero test for the corrected full 4D matter solution. Trying to combine those owners without rechecking the stress support would be a false GR closure.

## 2. NEW uniform coframe-only six-dimensional Ward pivot

The exact original six-face plus scalar N1 action is invariant under every **local proper Lorentz frame rotation**, acting at each site as
\[
\delta_Ze=Z e,\qquad
\delta_ZU_{xy}=Z_xU_{xy}-U_{xy}Z_y,\qquad
\delta_Z\Psi_A=0,
\tag{2}
\]
for \(Z^T\eta+\eta Z=0\). PF weights are the fixed actual Golden address numbers, not additional frame fields. Original star and q are each invariant under (2), so the local source Ward identity is an exact off-shell identity for ARBITRARY two-scalar gradients, not only the original restricted scalar ansatz:
\[
\boxed{W_e E_e+W_U E_U=0.}\tag{3}
\]
The two scalar Euler rows have no local Lorentz transformation because the scalar fields are internal singlets, so the identity does not assume material stationarity.

Use the six original Lie generators \(K_1,K_2,K_3,J_{12},J_{13},J_{23}\) and choose six actual coframe source entries as Ward pivots:
\[
\mathcal P=\{e_{0,1},e_{0,2},e_{0,3},e_{1,2},e_{1,3},e_{2,3}\}.
\tag{4}
\]
At ANY diagonal coframe \(e=\operatorname{diag}(A,B,C,D)\), their exact transformation matrix is
\[
\boxed{
W_{\mathcal P}=
\operatorname{diag}(B,C,D,C,D,D),\qquad
\det W_{\mathcal P}=BC^2D^3\ne0.
}\tag{5}
\]
For the old rank-two metric \(A=\sqrt r\,e^{-r^2/4}\), \(B=1/A\), \(C=D=r>0\), the EXACT determinant is \(r^5/A\). It remains uniformly separated from zero on a compact positive-radius time chart.

**Crucial refinement improvement:** the old special six-pivot minor was \(-X^3\sinh(hk_2)^3\), whose inverse norm may blow up as \(h^{-3}\). New (5) needs NO boost, no nonzero spin k2 and NO h-dependent singular pivot. It is a UNIFORM Lorentz gauge/source chart for general corrected scalar stress, not a source-support-specific shortcut.

The local Ward identities solve all six pivot source components:
\[
E_{\mathcal P}
=-W_{\mathcal P}^{-1}(W_{\rm rest} E_{\rm rest}
                     +W_U E_U).
\tag{6}
\]
Consequently, on the stated nondegenerate coframe chart the FULL 42 native field Euler equations vanish iff the **remaining 36** nonpivot equations (10 coframe+24 proper Lorentz+2 real material) vanish. This is a test of genuine ambient field stationarity; no sign fit or six forbidden equations have been discarded. At a nearby non-diagonal coframe, determinant continuity and the implicit local Lorentz action allow the same six gauge conditions to be maintained after a frame change.

## 3. The coframe gauge is literally metric10, not just dimension counting

Fix the local Lorentz gauge \(e_{a\mu}=0\) for the six *upper triangular* entries (4). This is a legitimate smooth local gauge near positive diagonal coframe by (5). Its ten remaining lower-triangular coframe entries map into the TRUE metric ten
\(g_{\mu\nu}=(e^T\eta e)_{\mu\nu}\).
Their exact 10×10 Jacobian at diag(A,B,C,D), with conventional (00,10,11,20,21,22,30,31,32,33) coordinate ordering, is
\[
\boxed{
\det D_{\mathrm{coframe10}}g_{10}
=-16 A B^2 C^3 D^4\ne0.
}\tag{7}
\]
On the rank-two chart it is \(-16r^7/A\). Hence the remaining ten coframe variables are not vague “metric-like” parameters; they are locally analytically equivalent to all ten genuine independent symmetric metric components. The original four SO(1,3) links carry 4×6=24 independent proper-Lorentz variations.

Combining (5)–(7), the geometrical quotient after a legitimate on-shell material elimination has the exact native field-coordinate type
\[
\boxed{\mathrm{metric}_{10}\oplus\mathrm{LorentzLinks}_{24},\qquad
\mathrm{rank}=34.}\tag{8}
\]
This agrees with the previously proved ORIGINAL full128 Jones tomography **type and rank** (metric10+link24), rather than merely sharing an unexplained integer. The tomography theorem is computed on its own original Jones/Fourier input, however: no claim is made that its 34 observed event-score one-forms have already been physically identified with the metric/link coordinates of this genuinely corrected 4D Cauchy solution. The same preparation, controller, clock, retained archive, physical code and moving observer are additional maps to prove.

## 4. True causal matter Schur and the honest outgoing boundary term

The preceding analytic theorem proves that, for every fixed finite original Golden PF chart with a diagonal positive \(g^{00}\), sufficiently small Cauchy/inflow two-field data have exact interior Euler solutions. Its entire material Jacobian is a causally ordered 2×2 block lower triangular product, with positive factors \(g_t W\) and \(\Delta_z\) near zero. Therefore an actual geometric perturbation is propagated through the matter solution by solving these same invertible 2×2 blocks in causal order:
\[
(D_{\Psi_{\rm interior}} E_\Psi) D_g\Psi_{\rm interior}
=-D_g E_\Psi.
\tag{9}
\]
No massive 2592×2592 or indefinite global matter Hessian inverse is required. This is a TRUE nonlinear material Schur/implicit graph in the Cauchy-inflow source class, not a claim of a stationary material minimum.

**Boundary firewall:** This is a Cauchy/inflow, not all-face Dirichlet, reduction. Geometric source differentiation of the on-shell action includes the explicit source conjugate to the *outgoing* matter boundary values:
\[
D_g S_{\rm red}
 =D_g S|_{\Psi}+
 (D_{\Psi_{\rm out}}S)\,D_g\Psi_{\rm out}.
\tag{10}
\]
The material bulk Euler terms vanish exactly but the outgoing boundary term does not vanish automatically. A genuinely stationary full Book action needs its actual boundary/cut/history term and field selection. One may NOT invoke (8) to claim the remaining 34 bulk source rows have vanished without this calculation.

## 5. What this actually supplies to the same physical source programme

The combined new theorem is the first stated **full-four-dimensional** typed material+Lorentz local reduction for the already owned real two-field nonlinear N1 Golden price:
- exactly all 2 material interior Euler classes solvable by a causal small-data analytic recursion on ANY finite positive native PF mesh, and their complete source derivatives are propagated via a local 2×2 triangular Jacobian;
- all 6 local Lorentz pivot Euler rows vanish whenever the remaining 36 genuine rows vanish, with one explicitly NONDEGENERATE coframe-only pivot that remains regular in the mesh limit;
- the remaining coframe metric variables are EXACTLY 10 independent true metric coordinates, alongside 24 proper-Lorentz link variables, for a typed 34-dimensional geometric source solver;
- the material correction invalidates the old special 12-target support shortcut, and the authentic outflow/boundary source is retained.

The previously proved Jones/full128 rank34 tomography can now be tested against exactly this **34-variable** geometrical quotient, provided both are actually carried by the SAME native preparation; it is NOT an Einstein action selection or a right-inverse theorem.

**Open:** a gauge/boundary-compatible simultaneous solution of the remaining 34 geometry equations with the new matter/boundary response; actual Book03 absolute Info/heat/oldRIGHT/clock and autonomous future-task selection; actual common-initial writer, Ward in the complete physical input chart, and uniform GR refinement. Original null/Brinkmann fixed family remains a separate configured exact positive witness; the rank-two arbitrary-Fourier case is not yet a complete finite GR root. \`GR_closed=false\`.

**Reproduction:** \`sources/d0_causal_full4d_scalar_schur_2026-10-21/check_uniform_metric34_ward.py\` verifies exactly the 6×6 Ward pivot and 10×10 true-metric gauge Jacobian symbolically for arbitrary two-scalar input gradients, not only for the pre-correction special profile. Numeric full 4D honest stress/source tests in \`check_causal_4d_two_scalar_all_euler.py\`. No independent formal Lean acceptance claimed.


## 6. Native Golden two-bin CFL and material-stable rectangular refinement (new consumer 21 October)

The genuine [native rectangular CFL theorem](A4D_NATIVE_GOLDEN_RECTANGULAR_CFL_AND_CAUSAL_TWO_SCALAR_2026_10_21.md) closes a distinct **uniform linearized material-stability** premise previously absent from this 42→34 reduction. The exact Cauchy 2×2 local inversion in §4 is valid at each fixed mesh but is NOT automatically a stable refinement: at the rank-two coframe e=diag(A,1/A,r,r), A=√r exp(-r²/4), the genuine N=1 two-scalar zero-amplitude linearization has spatial Courant sum C(r)=r² exp(-r²)+2 exp(-r²/2)/r. On the original h_t=h_s frozen problem, C(1)=1.5809407605967>1, so a high-frequency mode grows by factor 4.0785796486 EVEN WITH EXACTLY SMOOTH PF; by the checkerboard Rayleigh quotient the instability survives arbitrary positive spatial native PF weight W. Small Euler residuals and finite 2592-variable invertibility alone never justified continuum evolution.

A geometrically exact two-bin RECTANGULAR ROLE QUOTIENT from unchanged original isotropic fine F/R box addresses at side2L, merging only 2×2×2 spatial fine cells per observed macro-site, has 2L×L³ sites and h_t/h_s=1/2, with EVERY true Golden fine address, failure, clock and oldRIGHT still retained. The true density is rho_rect=(1/8)sum_delta rho_fine, so original all-order native PF smoothing applies. Inverse-PF site first-source transport is EXACTLY P_READY/(2L⁴) sum_z Dfhat_z = P_READY*h_t*h_s³ sum_z Dfhat_z (likewise genuine matter): no newly assigned volume/coupling. This is a source WEIGHT identity; full ANISOTROPIC 16+24 star source remains to be compiled.

On the whole positive chart r>=3/5, the exact elementary bound C(r)<23/6<4 gives a uniform positive CFL-energy gap >=1/24 for the TWO-bin scheme with uniform W; the already owned high-depth PF theorem forces Wmax/Wmin->1, hence the genuine N1 rectangular linearization is strictly stable at sufficiently fine mesh. Its 2×2 nonlinear causal input solves remain analytically invertible on every finite rectangle after including h_t/h_s=1/2 in the genuine current equation; the full time-varying proof additionally needs C1 geometry/ledger bounds, and the outgoing boundary source is still live.

Bounded owner-controlled replay: original 75025 cost24 words at fine L8 group to TRUE 512 macro sites (counts89..260), retain P_READY=.341640786512; genuine same Golden N1 W ratio1.0000915, two-bin CFL margin .6047286; 140 steps of 64-site positive energy drift <8e-16. These are not an all34 geometry-source root or physical Book selection. The only remaining geometry-coupled subject of THIS bridge is still a compatible right inverse of all metric10+link24 equations including new non-diagonal CAR stress and real outgoing boundary term. The physical HJR/Info/controller/clock selection and anisotropic star/collar remain separate. GR_closed=false.
