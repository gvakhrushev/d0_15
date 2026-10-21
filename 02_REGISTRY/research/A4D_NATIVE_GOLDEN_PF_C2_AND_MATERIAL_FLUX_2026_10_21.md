# D0 — Original Golden C² PF refinement and an exact finite nonlinear matter Euler root on the same N=1 source

21 October 2026. Existing Draft #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constitutive / gr_operational_realization. **Proved quantitative native PF compatibility + analytical scalar-flux elimination and one genuine finite numerical witness.** Not compulsory Book03, not the 42-row joint root, no GR promotion.

Inputs are unchanged and identified: original 4D Golden nested boxes and quantitative discrepancy (02_REGISTRY/gr_assembly/sources/d0_original_golden_moving_mean_j2_2026-10-19/theorem.md); original literal weighted shift/true adjoint (sources/d0_w2_weighted_source_2026-10-16/RESULT_RU.md); correct sigma-minus SAME full N=1 GoldenMaster (sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py); actual finite non-VSI six-face scalar and hostile positive-PF jump (sources/d0_star_rank2_seam_2026-10-21/check_global_star_pf_jump.py); old actual Golden READY / 0/10 measured-CQ tree and its 42-source (A4D_ORIGINAL_GOLDEN_READY_COMPLETE_CQ_COST_INFO_PF_SOURCE_2026_10_21.md).

## 1. Exact theorem — logarithmic genuine Golden history depth creates DISCRETE C² PF, not merely positive PF

Let p=φ⁻¹, h=1/L, L≥4. Use only the ORIGINAL equal-cost Golden F/R words, the unchanged 4D nested-box site map X_w and the true counts N_(n,z), no uniform decoder or independent site prior:
\[
\rho_{n,L}(z)=L^4 N_{n,z}/F_{n+1},\quad
a_n=F_{n+1}p^n,\quad a_\infty=\varphi/\sqrt5=(5+\sqrt5)/10>7/10.
\]
Take the finite genuine cost schedule
\[
s(L)=\min\{s\ge0:\varphi^s\ge L\},\qquad
\boxed{n(L)=64s(L)+128=O(\log L).}\tag{1}
\]
This is a CONSTRUCTION/REFINEMENT schedule, not an asserted physically selected future depth. The owned exact original-box estimate is, for k=floor(n/4),
\[
\|\rho_{n,L}-1\|_\infty\le
\frac{L^4\epsilon_{n,k}+128L\delta_k+|a_n-a_\infty|}{a_n},
\quad
\delta_k=2p^{\lfloor k/4\rfloor},\
\epsilon_{n,k}=p^{2(n-2k)+1}/\sqrt5.
\tag{2}
\]
For (1), n=64s+128 is EVEN, k=16s+32 and δ_k=2p^(4s+8)≤2p^8 L^-4<1/(2L), so the owner estimate applies. The exact Golden a_n=a∞+p^(2n+1)/sqrt5 is ≥a∞. Since p^s≤1/L,
\[
L^7\epsilon_{n,k}\le p^{129}/\sqrt5,\quad
128L^4\delta_k\le256p^8,\quad
L^3|a_n-a_\infty|\le p^{257}/\sqrt5.
\]
Using ONLY the certified rational bounds 3/5<p<5/8 and a∞>7/10, one integer-rational inequality proves on ALL original native L≥4:
\[
\boxed{L^3\|\rho_{n(L),L}-1\|_\infty
<\frac{10}{7}\,[256(5/8)^8+2(5/8)^{129}]
=8.5149492536\ldots<9.}\tag{3}
\]
No astronomical Fibonacci enumeration, external spatial sampling or invented moving source measure enters this proof.

Thus all 256 or L⁴ genuine original site cells have rho in [1-9h³,1+9h³], and for each original coordinate forward, backward or mixed differences:
\[
\boxed{\|\nabla_h\log\rho\|_\infty\le36h^2,\qquad
\|\nabla_h^2\log\rho\|_\infty\le72h.}\tag{4}
\]
Indeed |log rho|≤18h³ for h≤1/4, and any first/second difference has at most 2/4 such samples. The raw ρ satisfies first/second difference bounds 18h²/36h. **Original integer counts need not individually become smooth**; their normalized finite-difference fields do. This rules out the recent fixed (rho_prev,rho_cur)=(1,2) finite-time PF-jump counterexample specifically on the genuine high-depth Golden schedule, without denying that it is valid for an arbitrary positive fake density or for shallow n=20/24.

### 1.1. The previously troublesome OPEN weighted Dirac endpoint source is now quantitatively small, not deleted

In the existing literal stored shift, after the actual PF scalar site-weight factor and unchanged orthonormal frame,
\[
\alpha_{xy}=\sqrt{\rho_x/\rho_y},\qquad
\log\alpha_{xy}=\tfrac12(\log\rho_x-\log\rho_y).
\]
The finite exact weighted-adjoint distinction S*≠S^-1 remains. But (3) gives
\[
|\alpha_{xy}-1|,\ |\alpha_{xy}^{-1}-1|
\le\frac{9h^3}{1-9h^3}<11h^3.\tag{5}
\]
For uniformly bounded original coframe/CAR creation and actual proper-link transports, on the SAME uniformly bounded reference chart the true literal stored difference satisfies
\[
\boxed{\|D_{\rho,h}-D_{1,h}\|\le C h^2.}\tag{6}
\]
For the true positive adjoint completion Δ_h=D_h*D_h, with D_h bounded by C'/h,
\[
\boxed{\|\Delta_{\rho,h}-\Delta_{1,h}\|\le C''h.}\tag{7}
\]
If the original uniform-PF stored D is genuinely selfadjoint for that chart, its nonuniform-PF adjoint defect is O(h²). These are OPERATOR NORM bounds for the original PF component, not assertions of exact selfadjointness of the weighted stored D, replacement S^-1=S*, or vanishing of full Book H+J+R trace and its derivatives when physical mode counts, metric-dependent whitening, regulators and actual cut move. True physical observer/volume derivatives remain separate.

### 1.2. True original Golden READY signal stays positive

For the SAME genuine cost schedule, the old original FR/RF paid READY subrecord has mass
\[
\boxed{P_{\rm READY,n}=2p^3 a_n\to2p^3 a_\infty
=0.341640786499874\ldots>0.}\tag{8}
\]
Every first-crossing overshoot, FF/RR and FR/RF leaf remains in the full record. Its complete measured Golden prefix Shannon H_phi is exactly its actual expected native prefix CODE cost, for every n. Growing n changes the true absolute duration/cost O(log L) but does not introduce a new field source from this measured prefix code. The previously owned nonzero all42 READY + inverse-PF first source remains EXACT for genuine ρ_n.

A smaller continuum SOURCE interface is possible: without using an EXACT inverse-PF reciprocal coin, the genuine original measured-site mean of a bounded smooth source test V_z differs from the uniform mean by
\[
\left|\frac1{F_{n+1}}\sum_z N_{n,z}V_z-\frac1{L^4}\sum_zV_z\right|
\le9h^3\frac1{L^4}\sum_z|V_z|.
\tag{9}
\]
This is a quantified same-native-measure *approximation*, NOT equality of finite physical actions or a substitute for all RAW 42 high-frequency row norms. It removes the need for computing the full enormous PF reciprocal census only when the consumer needs this controlled continuum mean.

## 2. EXACT NONLINEAR material1 Euler elimination at fixed real temporal scalar endpoints — not an affine surrogate

Take the **unchanged** actual cap-one sigma-minus GoldenMaster F(x,y) from the pinned original native_master.py, including both click bands and its true measured-CQ entropy factor. On a finite rank-two time slab with fixed original coframe/plaquette and any TRUE positive native PF density ρ_i, write
\[
u_i=(\psi_{i+1}-\psi_i)/h,\quad
q_i(u_i)=a_i u_i^2+b_i,\quad a_i=g_i^{00}>0,\
b_i=g_i^{11}\epsilon^2<0,
\]
where ε is the existing second scalar's forward spatial gradient. The full original N=1 price restricted to the actual scalar1 inputs is
\[
\mathscr S=h\sum_{i=0}^{N-1}\rho_i
 F(-\tau f_i/\rho_i,\tau q_i(u_i)/\rho_i).\tag{10}
\]
No q_i=0 is imposed after variation; its true generated nonlinear value is retained in F. Independently varying EVERY interior scalar1 value while preserving BOTH physical endpoint field values yields EXACTLY
\[
\boxed{\partial_{\psi_j}\mathscr S
=2\tau[J_{j-1}-J_j],\quad
J_i=F_y(x_i,y_i)a_i u_i,\qquad j=1,\dots,N-1.}\tag{11}
\]
The original inverse-PF factors cancel by the actual chain rule, not by a counterterm or an assumed flat density.

Define G_i(u)=F_y(-τ f_i/ρ_i,τ(a_i u²+b_i)/ρ_i)a_i u. If the already-owned positive analytic price chart obeys
\[
\boxed{G_i'(u)=a_i[F_y+(2\tau a_i u^2/\rho_i)F_{yy}]>0}\tag{12}
\]
on the genuine bracket of each u, each G_i has an inverse. Solving G_i(u_i(J))=J and enforcing the one actual global Dirichlet condition
\[
\boxed{h\sum_{i=0}^{N-1}u_i(J)=\psi_N-\psi_0}\tag{13}
\]
gives a UNIQUE J and UNIQUE nearby finite scalar profile whenever the genuine boundary difference lies inside the corresponding bracketed values. Then ALL N−1 interior nonlinear material1 rows vanish EXACTLY. For small bounded ε and small h the derivative is positive from the real F_y(0,0)>0 by continuity, because the correction in (12) is O(ε²)+O(h). This is a full finite scalar-root theorem in its stated analytic interval, not a global root of the 16+24+2 coupled geometry.

**Numerical same-original-carrier witness:** calculate the REAL original (n,L)=(24,8) 4096 native cells from the unchanged nested Golden F/R boxes, not a fabricated PF curve. Along actual spatial column (4,4,4), use the true 8 original rho sites (1.637854049,1.146497834,1.801639454,1.146497834,1.583258914,1.801639454,0.928117294,1.310283239). Compute the original finite four-edge noncommuting six-face star scalar, not its h→0 truncation, and use ORIGINAL cap-one GoldenMaster F_y with correct sigma-minus orientation. Solve (11) by one common flux J with the native fixed scalar endpoint jump. On this actual finite slab:
\[
\begin{array}{ll}
\max|\text{material1 Euler residual before}|=3.79108833088\cdot10^{-4},\\
\max|\text{material1 Euler residual after}|=4.4408920985\cdot10^{-16},\\
\max|\text{independent full nonlinear CQ price secant}|=1.4107410182\cdot10^{-15},\\
\max|\delta(\text{physical scalar gradient})|=4.5168659782\cdot10^{-5},\\
\max|q_{\mathrm{new}}|=1.3204284165\cdot10^{-5},\quad
|\delta(\psi_{\rm endpoint})|=0.
\end{array}
\]
These residuals are numerical precision checks, NOT a rigorous interval root certificate at the particular L8 parameters; the local existence theorem follows from (12) and the bracket hypothesis. The full time-dependent second scalar with SPATIALLY changing ρ requires its own actual transverse Euler solve; it is not claimed solved by (11).

## 3. NEW synthesis: compatibility with non-VSI rank-two SAME complete N1 price on the true refining Golden tower

The inherited original actual rank-two six-face scalar has exact compact-time expansion f_star,h(t)=h c(t)+O(h²); importantly c(t)=3(r(t)^4−1)e^(−r(t)²)/(4r(t)²) is GENERICALLY NONZERO, with accidental zero at r=1. The ORIGINAL GoldenMaster F_y is analytic on its strict 0<r<1 output chart.

For the same finite original uncorrected rank-two scalar current, each true coefficient change due only to site PF is
\[
|F_y(-\tau f_i/\rho_i,0)-F_y(-\tau f_i,0)|
\le C|f_i||1/\rho_i-1|\le C'h\,\|\rho-1\|_\infty.
\]
Dividing the TWO neighboring true material current contributions by h yields the uniform quantitative HOSTILE-CONTROL REPAIR
\[
\boxed{|\mathcal E_{\psi_1}(\rho)-\mathcal E_{\psi_1}(1)|
\le C''\|\rho-1\|_\infty=O(h^3),}\tag{14}
\]
on the genuine native deep-cost schedule, rather than O(1) for a fixed adjacent PF-jump (1,2). This does not require smoothing actual integer n_z by assumption or importing a continuum PF prior. It is compatible with the separately performed exact finite scalar1 flux solve in §2, whose generated q≠0 enters all remaining geometric and material sources.

This composition removes TWO actual source gates: (i) the PF-regularity exception in the non-VSI original N1 source/refinement programme and (ii) the one-dimensional full nonlinear scalar1 stationary row at any chosen finite positive PF/time chart. The remaining tasks are genuine: jointly solve 16 coframe +24 covariantly neighbor-coupled Lorentz links + the transverse material2 equation with the corrected q, retain actual collar/gauge and original inverse norms, and establish the compulsory whole physical Book03 H+J+R/Info/clock/writer admission rather than equating its action with the chosen measured-CQ functional. No controlled 42-root, uniform GR theorem, independent review or Book status promotion is asserted. GR_closed=false.

## 4. Reproduction and provenance

- sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_golden_pf_c2_source.py — originally executed exact rational envelope and original Golden counts/census; native scalar diagnostic and CAR16 weighted two-node perturbation.
- sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_scalar_flux.py — independently executed original 24/8 4D Golden histogram, genuine non-VSI based-six-face scalar, SAME true GoldenMaster N1 full price derivative, one common interior nonlinear scalar flux and native endpoint Dirichlet, independent complete-CQ scalar price secants.

The signed native r-slope and other all42 geometric/matter identities are consumed from their existing owned source files; they were NOT regenerated or assumed from the above two isolated proofs. The native L4/L8 census is an actual enumeration for the narrow check; the huge high-depth schedule's theorem is an analytical consequence of the parent's exact uniform discrepancy and does not enumerate exponential path counts. Both checks are AUTHOR tests, not independent peer review, not a full GitHub scientific CI root and not a Book03 selection proof.

## 5. All fixed derivative orders — a stronger tower theorem on the SAME original Golden boxes

The C² diagonal above is the order-two case of a general EXACT result. For any fixed integer \(r\ge0\), set \(R=\max(r,2)\), choose \(s(L)=\min\{s:\varphi^s\ge L\}\) as before, and choose the true original Fibonacci/GOLDEN cost
\[
\boxed{n_r(L)=16(R+2)s(L)+128=O_r(\log L).}\tag{15}
\]
The unchanged owned original-box bound (2), now with \(k=n_r/4=4(R+2)s+32\), gives
\[
\delta_k=2p^{(R+2)s+8}\le 2p^8L^{-(R+2)},
\quad \epsilon_{n,k}=p^{n+1}/\sqrt5,
\quad a_n\ge a_\infty>7/10.
\]
Multiply the original discrepancy inequality by \(L^{R+1}\). The three terms are bounded respectively by \(p^{129}/\sqrt5\), \(256p^8\), \(p^{257}/\sqrt5\). Therefore by EXACTLY the same rational constant \(8.51494925\ldots<9\),
\[
\boxed{\|\rho_{n_r(L),L}-1\|_\infty<9h^{R+1}
\le9h^{r+1}.}\tag{16}
\]
Because \(R\ge2\), all original site densities are at least \(55/64\) for ALL \(L\ge4\), so the logarithm and every positive coframe square root are well defined. Every coordinate, mixed or iterated j-th finite difference, \(0\le j\le r\), satisfies the UNIFORM theorem
\[
\boxed{
\|\nabla_h^j\log\rho\|_\infty
\le18\,2^j h^{R+1-j}
\le18\,2^j h^{r+1-j}.}\tag{17}
\]
The proof uses only \(|\log\rho|\le2|\rho-1|\) and the \(2^j\) signed terms of a genuine j-fold difference; it does NOT assume pointwise differentiability of any unrefined integer count. Exactly the same type of bounds applies to \(1/\rho\) and \(\sqrt\rho\) with other fixed universal constants. Hence the original site density and its physically coframe-dressed metric can be made discrete \(C^r\)-close to a uniform PF carrier to any specified FIXED r, still at logarithmic authentic native history depth \(O_r(\log L)\). At r=2 the metric and Christoffel/Riemann finite-difference perturbations induced solely by this native spatial PF are \(O(h)\) on a uniformly bounded regular coframe chart, not a new claim about a generic unbounded HJR operator.

**New strategic cut:** The genuine original Golden histogram is NOT itself a finite-regularity obstruction to any FIXED-ORDER continuum gravity/Dirac source, including the second-order Einstein tensor. Previously the only proof was a uniform \(C^0\) spatial discrepancy; the new theorem upgrades that SAME owned count distribution without changing the spatial decoder, original F/R alphabet, trace type or Golden source probability. The cost of the fixed desired jet order is only a larger coefficient in n_r(L), while the complete paid per-history code grows with n_r and READY signal remains nonzero. This does NOT bound the number of simultaneously required Hilbert history branches (which is enormous), the TRUE physical Book03 full entropy/heat trace with growing matrix dimensions, or prove that native M1 selects this particular refinement schedule.

**Independent exact-rational and high-precision check**:
sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_golden_pf_allorders.py
was executed with r=0,1,2,3,4,6,8,16,32,64 and L=4,8,16,64,256,1024. It verifies the exact rational majorant <9, the inherited original-box bound with the unchanged Fibonacci renewal coefficient and positive READY mass for all checked cases. The **all-order theorem is analytic** from the preceding bound; the finite parameter checks are not evidence replacing this induction.


## 6. Genuine two-scalar simultaneous finite Euler solve — same REAL n24/L8 PF and SAME full nonlinear N1 price

The one-scalar current theorem §2 covers one time column. This continuation gives a stronger simultaneous **numerical** root for BOTH independently varied scalar species at once, using the TRUE original full eight-by-eight time/spatial slab. The underlying Euler equation is an exact analytic identity; the finite root is a numerical witness, not yet an interval existence certificate.

Consume the native original cost24/L8 4D nested-box census (75025 real Golden equal-cost words), on the true Role sites (time i, spatial j, fixed other coordinates 4,4). Its actual nonuniform PF density lies between 0.54595134955 and 1.85623458847. Keep original rank2 metric g_tt=A(t)^2, g_xx=-B(t)^2, A B=1, true based six-face f_i including the noncommuting boost/time plaquettes, and both real scalar fields psi_A(i,j), A=0,1. Their entire original Dirichlet boundary collar is fixed. The exact finite nondensitized source is
\[
q_{ij}=\sum_{A=0}^1[g_i^{tt}(D_t^+\psi_A)^2+g_i^{xx}(D_x^+\psi_A)^2]
\]
on 7×7 actual original forward cells. The unchanged full sigma-minus native GoldenMaster N1 price is
\[
\boxed{\mathscr S_{N1}=h^2\sum_{i,j=0}^6 \rho_{ij}
 F_{N1}(-\tau f_i/\rho_{ij},\tau q_{ij}/\rho_{ij}).}\tag{18}
\]
Real fixed positive readiness factors and code/factory baseline belong to this same process and multiply/add to it without changing its declared matter source; no q=0 constraint is imposed after variation and no affine Einstein action is substituted. The original F_N1 has the REAL two-band nonlinear Golden probability and correct original sigma-minus material orientation.

For EACH species A and EACH independently varied interior scalar value, 1≤i,j≤6, the exact genuine Euler has the divergence form
\[
\boxed{E_{A,ij}=J_{A,t}(i-1,j)-J_{A,t}(i,j)
+J_{A,x}(i,j-1)-J_{A,x}(i,j)=0,}\tag{19}
\]
with
\[
J_{A,t}=F_y\,g^{tt}D_t^+\psi_A,\qquad
J_{A,x}=F_y\,g^{xx}D_x^+\psi_A.
\]
The actual derivative of the written price is exactly 2 tau h times (19). The site rho cancels between the paid prefactor and query derivatives, but true rho remains in BOTH arguments of F_y. Geometry/coframe/link fields are fixed for this MATTER-SUBSYSTEM solve, and ALL original scalar boundary values remain fixed.

The jointly solved 72-dimensional system comprises 2×6×6 true scalar variables. On the original zero-q rank2 seed it has a nonzero full N1 EULER due to real f and site PF. A direct finite Newton root using SciPy hybr and original 75025-word site counts gave:

| Genuine original n24/L8 diagnostic | Measured |
|---|---:|
| Max 72-scalar Euler residual BEFORE | 7.70066696072e-5 |
| Max 72-scalar Euler residual AFTER | 2.60188192606e-16 |
| Scalar species0/source0 AFTER | 2.60188192606e-16 |
| Scalar species1/source1 AFTER | 2.49800180541e-16 |
| Max correction of physical scalar field values | 2.17120991899e-5 |
| Max TRUE generated nonlinear q | 3.09521682355e-5 |
| Changed scalar boundary/collar values | 0 |
| 72×72 numerical Jacobian smallest singular value | 0.87006550687 |
| Numerical Jacobian 2-norm condition number | 57.56104684575 |

The numerical Jacobian is full rank and modestly conditioned. This is NOT yet an exact interval proof of the 72D finite solution, nor a 4D full-lattice scalar theorem. The source uses the actual original local six-face scalar f and the real original sigma-minus full N1 F_y, not the separate sigma-plus price or an affine model. An independently coded complete Bernoulli-entropy CQ price finite difference on eight representative interior variables across BOTH scalar species agrees with the exact source derivative before correction to absolute error below 3.3e-16; after the root its numeric secants are below 3.3e-16 at step 3e-5. This is a literal same-price control.

**The genuinely changed parent obligation:** both material scalar species can be simultaneously stationary on this actual finite Golden non-VSI 2D slice; the second species is not an automatic unsolved source if the two fields vary together. The original 42-Euler root STILL needs full 4D gauge/collar, all independent16 coframe+24 covariant neighbor-coupled Lorentz equations at the corrected nonzero q, actual native oldRIGHT/controller/clock/absolute Book03 source, compulsory action and uniform refinement. Not even the numerical matter root is claimed an exact finite all42 solution. Physical GR_closed=false.

### True native 4D Golden PF: both N1 material fields solved on the full slab

The full-slab finite check now solves both scalar fields together on the original $(n,L)=(24,8)$ Golden carrier: 75,025 histories, 4,096 sites, 2,401 positive-neighbor cells, 2×6⁴=2,592 interior scalar variables, and the complete four-dimensional Dirichlet collar held fixed. It uses the same original rank-two non-VSI coframe, the actual finite six-face scalar, the native site PF, and the true sigma-minus N1 output-entropy price; every cell's q includes both fields and all four metric-gradient directions.

The sparse Newton iteration takes four updates. Its assembled double-precision Euler norm falls from 1.58786837324×10⁻³ to 4.99860569603×10⁻¹⁵. A separate 80-digit evaluation of the derivative of the written Bernoulli-entropy price, reconstructed directly from nodal field differences, gives max absolute price derivative 3.85234486172×10⁻²¹ and max normalized Euler 1.28157190164×10⁻¹¹. The latter is the conservative root-accuracy figure: near-root cancellation makes the separately assembled double-precision rows understate the independently reconstructed normalized residual. Ten direct entropy-price secants (five variables from each species, before and after the root, step 10⁻⁷) agree with that high-precision derivative to at most 4.46×10⁻²². Independent directional finite differences check the sparse analytic Jacobian to relative errors 8.03×10⁻⁹ before and 7.85×10⁻⁹ after.

The correction has max field-value magnitude 7.87715722090×10⁻⁵ and generates nonzero q with maximum |q| = 1.82199493241×10⁻⁴; all original boundary values stay fixed. This is a numerical root of the finite, fixed-geometry matter subsystem. It is not an interval proof, a 16-coframe+24-link root, a compulsory same-execution Book03 price, or a refinement theorem; physical GR remains open. Replay the independent checks with [the price-gradient verifier](sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_two_scalar_full4d_price_gradient.py) and its [captured result](sources/d0_native_golden_pf_material_flux_2026-10-21/FULL4D_RESULT.json); the underlying solver is [the full 4D root](sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_two_scalar_full4d.py).

Executable same-owner scripts:
- sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_two_scalar_2d.py: true 8×8 site density, real rank2 six-face, 72D simultaneous nonlinear matter root, numerical SVD.
- sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_two_scalar_price_secant.py: independently evaluated TRUE N1 output-entropy price secants before/after root on both scalar species.
- sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_two_scalar_full4d_price_gradient.py and FULL4D_RESULT.json: independent high-precision full-slab price gradient, representative raw-price secants, and sparse-Jacobian directional controls.
