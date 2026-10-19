# D0→GR: TRUE original all40 Schur symbol has generic rank SIX, exact 10 gauge-null directions and finite variational adjoint

19 October 2026. **EXACT ALGEBRAIC GENERIC RANK THEOREM via original-action Ward + F1009 nonzero minor; same PR #334.** This directly consumes [the terminating ALL-polynomial Cartan inverse](A4D_POLYNOMIAL_CARTAN_EXACT_INVERSE_AND_QUARTIC_REFINEMENT_2026_10_19.md) and its original six-based star action. Unlike a merely selected full10 Lorentz continuum principal symbol, this calculation takes the complete **actual finite difference** Lorentz-star first and second source, all six original based faces, their two adjacent link variations, and 16+24 independent directions, then eliminates the 24 link variables of the SAME linearized action. This is a theorem on the **flat vacuum** source operator; it does NOT assert nonlinear exact lattice diffeomorphism invariance, universal finite characteristic cone, a generic exact root, or physical native D0 Cost−Info selection. GR_closed=false.

## 1. The Schur operator is a typed consequence of the already-owned 40-row action

At flat \(e^a{}_\mu=\delta^a_\mu,\ U_\mu=I\), the original proper-Lorentz \(\star\)-density has vanishing coframe–coframe Hessian because its curvature vanishes and its coframe dependence is quadratic. Its true joint flat Hessian has the exact off-diagonal block structure
\[
\boxed{\mathcal H_h=\begin{pmatrix}
0&C\\B&L
\end{pmatrix},\qquad L=\frac{\partial E_\omega^{24}}{\partial \omega^{24}},
\quad B=\frac{\partial E_\omega^{24}}{\partial e^{16}},
\quad C=\frac{\partial E_e^{16}}{\partial \omega^{24}}.}
\tag{1}
\]
In discrete Laurent symbol \(z=(z_u,z_v,z_x,z_y)\), \(L(z)\) is the full 24×24 original based-plaquette link Hessian. At z=1, \(L(1)=M\) has det256; therefore \(\det L(z)\) is NOT identically zero, so \(L^{-1}\) exists **as a rational Laurent matrix over the field \(\mathbb Q(z_u,z_v,z_x,z_y)\)**. The exact 16×16 reduced solder response is
\[
\boxed{S(z)=-C(z)L(z)^{-1}B(z).}\tag{2}
\]
No new Fierz–Pauli action or Einstein source has been introduced: this is solely the Schur complement of the ORIGINAL 40-variation operator.

Variational symmetry of the original real based action is the Laurent-adjoint identity, NOT pointwise \(S(z)^T=S(z)\):
\[
\boxed{L(z)^T=L(z^{-1}),\qquad C(z)=B(z^{-1})^T,\qquad S(z)^T=S(z^{-1}).}\tag{3}
\]
The complete explicit all-40 numerical stencil derives (1) without reusing a pre-imposed metric-only symbol and checks the last identity at distinct generic and null Laurent points. The independent exact F1009 checker evaluates the same 40-direction geometry and tests (3) as an exact finite-field identity at its specified points.

## 2. TEN EXACT right kernels are forced by the underlying lattice action

### 2.1. Six internal Lorentz gauge directions

The originally owned exact local proper Lorentz transformations at flat e,U have velocity
\[
\delta_K e_{z,\mu}=K_z e_{z,\mu},\quad
\delta_KU_{z,\mu}=K_zU_{z,\mu}-U_{z,\mu}K_{z+\hat\mu}.
\]
For one plane wave \(K_z=z^zK_0\), its 16 solder input is \(\delta e^a{}_\mu=(K_0)^a{}_\mu\). Since the original *same* star action is locally Lorentz invariant and its flat first Euler source is zero, the mixed Hessian kills this full 40-vector. Eliminating the link part in (2) gives
\[
\boxed{S(z)\,\mathrm{vec}(K_0)=0\quad\forall K_0\in\mathfrak{so}(1,3).}\tag{4}
\]
The six original generators are independent.

### 2.2. Four EXACT backward-gradient lattice directions

Let \(D^-_\mu:=I-T_\mu^{-1}\), with Fourier multiplier \(d^-_\mu(z)=1-z_\mu^{-1}\). For each constant four-vector \(\xi^a\), set
\[
\delta_\xi e^a{}_\mu(z)=D^-_\mu\,\xi^a(z)
\quad\Longleftrightarrow\quad
\delta_\xi e^a{}_\mu=\xi^a(1-z_\mu^{-1}) .
\tag{5}
\]
At the FLAT background, the original mixed coframe-to-link first source is an antisymmetrized composition of based-face differences. Since ALL the shifts commute, the **discrete exterior nilpotence** \(D^-_{[\mu}D^-_{\nu]}=0\) gives
\[
\boxed{B(z)\,(\xi\otimes d^-(z))=0,\qquad
S(z)\,(\xi\otimes d^-(z))=0\qquad\forall\xi\in\mathbb R^4.}\tag{6}
\]
This is an EXACT **linearized** finite-grid gradient gauge, not an assertion of full nonlinear lattice diffeomorphism covariance. The original true mixed source was evaluated separately on every one of the 24 link rows. This all-zero identity is algebraic: the two based-face contributions appear with opposite shifted coefficients, independent of numerical floating tolerances.

For generic \(z\), the 6 Lorentz and 4 gradient input directions are independent: an exact mod1009 rank-10 witness at z=(2,3,5,7) shows the determinant of one 10×10 minor is a nonzero Laurent rational function. Thus **the generic 16×16 reduced operator satisfies**
\[
\boxed{\operatorname{rank}_{\mathbb Q(z)} S(z)\le6.}\tag{7}
\]
The left counterparts follow by (3): there are four exact \(D^+\) divergence constraints on the output source and six antisymmetric internal Lorentz constraints.

## 3. Exact finite-field rank-six witness proves the GENERIC upper bound is sharp

[Original-action exact F1009 audit](sources/d0_two_null_crossing_2026-10-19/check_full40_schur_rank_modular.cjs) constructs L,B,C from the original four-dimensional null eta, all SIX based plaquettes, all 16+24 variations, including original odd derivative and both based faces, without assuming a continuum Einstein operator. It eliminates L by EXACT Gauss–Jordan arithmetic modulo the prime1009 (all denominators invertible at the selected points), and verifies:

| Laurent point z=(u,v,x,y) in F1009 | rank L | rank of 6+4 gauge vectors | rank S | dim ker S |
|---|---:|---:|---:|---:|
| (2,3,5,7) | 24 | 10 | **6** | 10 |
| (2,1,3,5) | 24 | 10 | **6** | 10 |
| (2,2,2,2) | 24 | 10 | **4** | 12 |
| (2,1,1,1) | 24 | 10 | **4** | 12 |

All exact \(S(z)^T=S(z^{-1})\), six Lorentz-null and four backward-gradient-null source tests pass at each point. Nonzero mod1009 6×6 minor with invertible L at z=(2,3,5,7) proves the same rational Laurent minor is NOT identically zero over characteristic0. Combined with (7):
\[
\boxed{\operatorname{rank}_{\mathbb Q(z_u,z_v,z_x,z_y)}S(z)=6.}\tag{8}
\]
This is a **PROOF OF THE GENERIC FINITE LATTICE RANK**, not a floating singular-value estimate and not merely a continuum h→0 statement. It contains exactly 10 independent null solder directions: six original Lorentz and four original-action linear discrete coordinate-gradient directions. The alternative finite points exhibiting rank4 confirm additional characteristic degeneracy, but by themselves do NOT classify the complete characteristic variety or prove a full Lorentz-invariant finite dispersion relation. Some continuum-null candidate momentum choices retain rank6 at finite spacing. A physical h→0 dispersion/small-divisor theorem requires the precise Laurent characteristic polynomial and norm.

[Independent ordinary-real Laurent check](sources/d0_two_null_crossing_2026-10-19/check_full40_flat_schur_symbol.cjs) exercises five other different z values and checks original 24-link invertibility, rank6 generic/rank4 special, exact transpose-to-reciprocal up to floating precision, Lorentz kernel to 10^(-18), and precisely the **backward**, not forward, discrete-gradient gauge to numerical precision. The forward or continuum-log gradients give small but NONZERO finite residuals except special isotropic momenta. This is a decisive finite-grid clock/metric discretization convention, not a freely replaceable derivative.

An exact characteristic-zero polarization check evaluates the same Laurent polynomials at the two-periodic null point \(z=(1,-1,1,1)\). There \(\operatorname{rank}L=24\), \(\operatorname{rank}S=4\), and the 12-dimensional kernel is exactly the ten independent Lorentz/backward-gradient vectors plus
\[
h^{\rm TT}_+=e^2{}_x-e^3{}_y,\qquad
h^{\rm TT}_\times=e^2{}_y+e^3{}_x.
\]
These are exact rational transverse-traceless null modes on this finite null wave, not just vectors in the modular kernel. The companion opposite-direction point \(z=(-1,1,1,1)\) also has both TT vectors in the rational kernel, but the displayed gauge span has rank 9 there and leaves one further null direction unclassified. The [exact rational TT checker](sources/d0_two_null_crossing_2026-10-19/check_full40_rational_tt_null_mode.cjs) records both results. This establishes two finite-lattice TT polarizations at one periodic null point; it does not establish the full characteristic variety, all-direction dispersion, or continuum propagation.

## 4. New consuming equation: four genuine finite SOURCE obstructions at each nonlinear order

Once the 24 proper-Lorentz link coefficients are eliminated using the prior exact ALL-POLYNOMIAL inverse, the remaining 16 coframe equations reduce to 10 metric rows by (4), and at flat first order only six are independent after the four additional exact source identities (6). At nonlinear amplitude order \(n\), write the Schur recursion schematically
\[
\boxed{S\,e_n=J_n(e_1,\dots,e_{n-1},\omega_1,\dots,\omega_{n-1}),}
\tag{9}
\]
where \(J_n\) is the **actual original-action** nonlinear residual after solving the 24 finite Cartan equations, not a prescribed Einstein tensor. By the exact Laurent adjoint, a necessary compatibility condition at that order is
\[
\boxed{
\sum_{\mu}D_\mu^+\,J_n^{a\mu}=0
\quad(a=+,-,2,3),}
\tag{10}
\]
as well as the Lorentz Ward projection. Here the discrete forward divergence is the left adjoint of (5); it is NOT permission to assert full nonlinear lattice coordinate covariance. If the nonlinear source violates (10), the next coframe coefficient cannot fix it using this same linearized operator, even if the 24 Cartan equations are solvable. Thus the **next exact calculation should test the four source-Ward constraints at degree5**, after the already built degree4 source, before running a new enormous 40-variable rank solve. A failure would be a genuine obstruction to that specific analytic/polynomial continuation chart, not to all D0 dynamics, gauge choices, source sectors, or GR.

For a fixed infinite polynomial/unwrapped carrier, the Lorentz and backward-gradient source constraints are exact. On a finite fixed collar the adjoint also carries boundary flux terms; on a periodic Fourier carrier small divisors and nonzero-momentum link resonances may occur. On a generic coframe, the full tensor/metric Ward is conditional on solving ALL observer, preparation, old history, CAR and same retained physical source equations; one must not promote (10) into a compulsory Book price theorem.

## 5. Strategic interpretation

The previous finite exact \([ab]\), cubic and quartic polynomial solutions are now connected to an **all-field flat Schur theorem**: rank 24 link + rank6 generic reduced coframe on 40 independent variables, with ten generic gauge nulls. At the exact period-two null point \(z=(1,-1,1,1)\), the rank-four degeneration has precisely two TT directions after quotienting those ten gauges. The opposite null direction has an additional unclassified null. This is a finite-lattice polarization result at a specific wave, not the full continuum on-shell spectrum. The final null-plus-matter theorem still needs one compulsory Book/Cost−Info execution to select these source equations. The geometric statement is explicitly linear and exact finite, not physical closure.

**Next smallest decisive gate**: compute the exact fifth-order four-component divergence of the native cubic/quartic coframe source on the saved rational branch, with a boundary-collar convention, and the first rank-six minor/denominator in the limit h→0. If both are controlled, the existing terminating Cartan inverse plus rank-six Schur pave a principled all-order analytic existence route. Otherwise the first nonzero Ward defect identifies precisely the missing coframe/source compatibility. Do NOT launch another undirected bulk rank census or claim GR_closed=true.


## 6. Constructive exact TWO finite transverse-traceless wave solutions on the original linearized star, for any null u-profile

The rank-four special point z=(2,1,1,1) in §3 has a *structural* explanation rather than being merely a characteristic minor. Keep the same flat null coframe, ORIGINAL 16 coframe plus24 independent link Euler, and take an arbitrary real lattice function \(f(u)\) in one original null direction u; no dependence on v,x,y. Put \(D_u^-:=1-T_u^{-1}\). There are TWO linearly independent transverse-traceless coframe directions:
\[
\begin{array}{lll}
(+):&
\delta e^2{}_x=f(u),&\delta e^3{}_y=-f(u),\\
(\times):&
\delta e^2{}_y=f(u),&\delta e^3{}_x=f(u).
\end{array}
\tag{11}
\]
All other 16 coframe perturbations are zero. Their **original proper-Lorentz** link corrections are fixed, with NO free profile fit:
\[
\boxed{
\begin{array}{lll}
(+):&\omega_x=D_u^-f\,N_2,&\omega_y=-D_u^-f\,N_3,\\
(\times):&\omega_x=D_u^-f\,N_3,&\omega_y=D_u^-f\,N_2,
\end{array}
\quad\omega_u=\omega_v=0.
}\tag{12}
\]
In the exact original generator order \(X_{ij}=(E_{ij}-E_{ji})\eta\) for
\((01,02,03,12,13,23)\), \(X_{12}=-N_2\) and \(X_{13}=-N_3\).
For a Laurent u-wave \(f(u)\sim t^{j_u}\), its two Euler blocks are
\[
\boxed{L(t)\omega(t)+B(t)\delta e(t)=0,\qquad
C(t)\omega(t)=0,\qquad\forall t\ne0.}\tag{13}
\]
This is an EXACT rational-Laurent identity in \(t\), not only a modular
rank4 witness. Derivation: \(L(t)\) depends on \(t^{-1},1,t\) only, by
the two based adjacent faces and linearity in the one-site u-wave.
For each of the two constant TT vectors, the true
\(B(t)e=(1-t^{-1})b_0\), while their constant link seed \(w_0\)
satisfies \(L(t)w_0=-b_0\).
The latter Laurent degree≤1 identity is proved coefficientwise by
three exact dyadic substitutions t=1,2,4, which determine every
coefficient of \(tL(t)w_0+t b_0\), a degree≤2 polynomial.
The old \(\epsilon\)-contracted solder return obeys
\(C(t)w_0=0\) because \(C(t)=(t-1)C_1\) in the u-only sector
and the explicit direct contraction \(C_1w_0=0\).
Thus \(w(t)=(1-t^{-1})w_0\) solves both original Euler blocks.
By discrete Fourier/Laurent superposition, every polynomial or finitely
supported u-profile satisfies (13) wherever its original site and
boundary/collar equations are defined.

**Interpretation:** The exact flat finite-star principal system
already has BOTH spin-two TT polarisations, with native proper-Lorentz
connections determined by the same Cartan source. This explains
constructively why the reduced rank drops from 6 to4 on this null
characteristic, while the ten generic gauge directions are retained.
The two linearized TT waves are NOT an all-amplitude nonlinear vacuum
family, do NOT establish a general Lorentz-invariant finite lattice
dispersion relation, and do NOT select a compulsory historical D0 price.
They complement the earlier NONLINEAR exact pp-wave root, whose coframe
gauge is different.

The bounded dyadic interpolation/proper-link and 16-coframe direct check
is added to the independent [full40 ordinary Laurent checker]
(sources/d0_two_null_crossing_2026-10-19/check_full40_flat_schur_symbol.cjs)
as exactTwoNullTT(). It uses both original TT polarisation fields
and checks all 24+16 Euler coefficients, not just the Schur rank.
The exact finite-field checker still supplies the separate generic
rank6 witness.
