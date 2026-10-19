# D0→GR: FINITE TERMINATING CARTAN INVERSE on polynomial fields + source-compatible quartic refinement grading

19 October 2026. **EXACT ALGEBRAIC ALL-POLYNOMIAL-DEGREE LINK INVERSE / EXACT QUARTIC DEGREE AUDIT / COEFFICIENTWISE C^k REFINEMENT. SAME Draft #334.** This is a strategic replacement for repeating 24-link rank/linear solves at every amplitude order. It works on the ORIGINAL unwrapped six-based-plaquette proper Lorentz-star operator; it adds NO action, no free connection multiplier, no new gravitational field, and no physical programme or source. **It does not establish a finite all-amplitude root, periodic/global boundary invertibility, full native H+J+R price, or GR closure.** GR_closed=false.

### Consumed owners
- [original universal Brinkmann six-plaquette all40](A4D_ARBITRARY_BRINKMANN_ALL40_CARTAN_DISCRETE_EINSTEIN_2026_10_19.md)
- [exact mixed quadratic Cartan/Einstein](A4D_DOUBLE_NULL_EXACT_FINITE_QUADRATIC_CARTAN_EINSTEIN_BOOTSTRAP_2026_10_19.md)
- [full cubic and *entire* quartic spatial Euler polynomials](A4D_DOUBLE_NULL_CUBIC_EINSTEIN_QUARTIC_AREA_WARD_2026_10_19.md)
- [original finite cubic engine](sources/d0_two_null_crossing_2026-10-19/check_cubic_finite_cartan_range.py)
- [exact rational full-spatial mixed quartic](sources/d0_two_null_crossing_2026-10-19/quartic_full_spatial_jet_solution.json)
- [other four quartic amplitudes, same cubic section](sources/d0_two_null_crossing_2026-10-19/quartic_all_sectors_shared_cubic_branch_solution.json).

## 1. Nonperturbative in POLYNOMIAL DEGREE: an exact finite inverse for the original flat 24 Cartan system

Let \(L\) be the *actual* linearization of all 24 proper-Lorentz left-link Euler equations of the ORIGINAL six-based action at constant flat solder \(v_r^a=\delta_r^a\) and all links \(U_r=I\), with the independent variation rule \(\delta U_{z,r}=X_{ij}U_{z,r}\), \(X_{ij}=(E_{ij}-E_{ji})\eta\), and the full odd first derivative \(D\mathcal R(P)[dP]=(dP+P^{-1}dP P^{-1})/2\). Do not freeze the neighbor plaquette: both based faces containing each link are included.

On the unwrapped infinite integer Role lattice, \(L\) is a constant-coefficient FINITE-SHIFT operator on \(\mathfrak{so}(1,3)^4\cong\mathbb Q^{24}\). Let \(T_r\) be the four true lattice shifts. Write
\[
L=L(T_u,T_v,T_x,T_y),\qquad
M=L(1,1,1,1),\quad \mathcal N=L-M.
\tag{1}
\]
The exact homogeneous matrix \(M\) is the accepted 24×24 flat Cartan Hessian:
\[
\boxed{
\operatorname{spec}M=\{2^{[4]},(-2)^{[4]},1^{[8]},(-1)^{[8]}\},\
\det M=256,\
(M^2-I)(M^2-4I)=0.
}\tag{2}
\]
This supplies an even more explicit exact inverse requiring NO solver:
\[
\boxed{M^{-1}=\frac{5M-M^3}{4}.}\tag{3}
\]
Indeed \(M(5M-M^3)/4=(5M^2-M^4)/4=I\).

Let \(\mathscr P_d=\mathbb Q[u,v,x,y]_{\le d}\) be the vector space of ALL polynomials of total spatial/Role degree at most d, evaluated on unwrapped lattice sites. Each \((T^\delta-I)f\) has total polynomial degree ≤d−1. Because L is finite-shift and its value at \(T=1\) is M, every term of \(\mathcal N\) is a combination of shifts minus identity. Hence
\[
\boxed{\mathcal N:\mathscr P_d^{24}\to\mathscr P_{d-1}^{24};\qquad
(M^{-1}\mathcal N)^{d+1}|_{\mathscr P_d}=0.}\tag{4}
\]
This is a purely finite discrete algebraic identity at *every* fixed d. No continuum limit or formal asymptotic series is used.

Therefore:
\[
\boxed{
L^{-1}\big|_{\mathscr P_d^{24}}
=\sum_{k=0}^{d}(-M^{-1}\mathcal N)^k\,M^{-1}
\quad \text{EXACTLY}.}\tag{5}
\]
One checks \((M+\mathcal N)(\sum_{k=0}^{d}(-M^{-1}\mathcal N)^kM^{-1})=I\), since the last remainder is nilpotent; the finite-dimensional bijection also gives the left inverse. The operator is EXACTLY invertible for polynomial link sources of ANY fixed degree, not just d≤4. No periodic Fourier denominators and no 24×24 rank recensus at subsequent polynomial amplitude orders.

**Constructive source recursion:** For every polynomial \(F\in\mathscr P_d^{24}\), \(\xi=L^{-1}F\) is the unique polynomial 24-link solution of the flat linearized Cartan system; compute \(\xi_0=M^{-1}F\), then \(\xi_{j+1}=\xi_j+M^{-1}(F-L\xi_j)\). The residual loses at least one polynomial degree each iteration, and \(\xi_d=L^{-1}F\). In a nonlinear two-amplitude perturbation, at order \(a^m b^n\), fixing the 16 coframe coefficient fields and all prior link coefficients yields an affine link equation \(L\omega_{mn}=-R_{\omega,mn}\). If its actual source belongs to \(\mathscr P_d^{24}\), (5) solves **all** 24 link coefficients at that order, uniquely within \(\mathscr P_d\). Source generation and gauge-invariant coframe compatibility remain separate.

**Boundary firewall:** Equation (5) is NOT an inverse on a finite periodic torus, finite fixed-collar region with a changed boundary operator, all smooth Fourier modes, or the original #216 full physical raw norm. On such carriers \(T-I\) is not nilpotent and the zero-frequency M alone cannot control resonance. In the unwrapped polynomial bulk, no new singular Cartan denominator appears at any degree. The remaining research problem is the 16-coframe reduced Schur equation after explicit elimination of the links.

## 2. Quantitative controlled h-refinement of the already solved quartic formal fields

The saved quartic solution was found on unit-step lattice coordinates \(X=(j_u,j_v,j_x,j_y)\), with two formal **dimensionless** amplitude variables \(a_1,b_1\). To represent a fixed physical transverse affine profile \(H(x,y)=a\,x\), \(J(x,y)=b\,y\) at physical spacing \(h\), use the SAME unit-grid solution, not a newly fitted solver, with
\[
X=x/h,\qquad a_1=h a,\quad b_1=h b,\qquad
v_{h,r}^a(x)=h\,e_{1,r}^a(X;ha,hb),\
U_{h,r}(x)=\exp\mathsf L_{1,r}(X;ha,hb),
\tag{6}
\]
where \(\mathsf L_1=\log U_1\) is the actual original proper-Lorentz Lie jet. The original based plaquette itself is unchanged under this reindexing. Since the original \(\star\)-density is **homogeneous quadratic in the original solder \(v\)**, for any reindexed lattice fields and independent original first variations there are exact identities
\[
\boxed{
\mathcal P_{\star,h}(h\,e,U)=h^2\mathcal P_{\star,1}(e,U),\quad
E_{v,h}=h E_{v,1},\quad
E_{U,h}=h^2 E_{U,1}.
}\tag{7}
\]
These are equations on the original action and 16+24 first derivatives (including all based return faces), not a new physical h-dependent normalization. The coframe/profile amplitude substitution in (6) simply changes the known independent input values.

For a degree-m amplitude coefficient that is a polynomial \(P_d(X)\) of spatial total degree d, its **physical coframe** contribution is \(h^{m-d}P_d(x)\), while the associated **physical connection** coefficient \(\mathsf L_h/h\) is \(h^{m-d-1}P_d(x)\). Consequently smooth bounded coefficientwise \(C^k\) refinement is guaranteed if
\[
\boxed{
\deg_X e_{(m)}\le m,\qquad
\deg_X \mathsf L_{(m)}\le m-1.}\tag{8}
\]
All quartic coefficients in the SAVED exact all-40 branch satisfy these inequalities, despite the *much larger permitted ansatz*.

Direct saved rational scan of ALL FIVE degree-four amplitude sectors:

| Amplitude | max spatial degree, 24 link-log coefficients | max spatial degree, 16 coframe coefficients |
|:--|--:|--:|
| (4,0) | none | none |
| (3,1) | 1 | none |
| (2,2) | **3** | **4** |
| (1,3) | 1 | none |
| (0,4) | none | none |

The mixed (2,2) branch has only 118 nonzero rational link polynomial coefficients and 20 nonzero coframe coefficients; all allowed but unused spatial degrees 4–6 (links) and 5 (coframe) are **exactly zero**, not a floating threshold. In particular the degree-four leading mixed coframe coefficient lives in original component \((a,r)=(2,2)\):
\[
[e^2{}_x]^{(2,2)}_{\mathrm{top}}=
\frac{3}{128}x^2y^2+\frac1{256}y^4.
\tag{9}
\]
It is one chosen gauge/section from the exact rational solver; it need not equal the earlier illustrative \(\sigma_4,\chi_4\) gauge or serve as physical matter normalization.

The cubic coframe source ansatz has degree≤3 from the explicit corrected \(H_3,J_3\), the 16-component cubic lift has degree≤2, the continuum-LC finite link jet has degree≤2, and its exact further cubic link lift has degree≤2. The quadratic mixed correction has coframe degree≤2 and link degree≤1. The linear profiles have degrees1 and0 respectively. Therefore the **ENTIRE degree≤4 local formal solution** satisfies (8), not merely its last mixed column.

For every fixed compact physical rectangle \(K\) and every fixed derivative order k, each finite amplitude coefficient in (6) has a smooth polynomial limit, with the lower-degree terms controlled by nonnegative powers of h:
\[
\boxed{
e_h^{[\le4]}=e_0^{[\le4]}+O_{C^k(K)}(h),\qquad
h^{-1}\mathsf L_h^{[\le4]}=
\omega_0^{[\le4]}+O_{C^k(K)}(h).
}\tag{10}
\]
Here [≤4] means a formal polynomial in a,b truncated at total amplitude degree four. The constants may depend on K, k and the retained finite coefficients; NO uniform-in-amplitude tail or convergence of the infinite nonlinear formal series follows. Existing quartic exact all-40 identities at unit spacing are carried by the exact scaling (7) to every physical h at every amplitude monomial of degree≤4.

The **crossed Weyl curvature survives this refinement**. Already
\([ab]P_{uv}^{\mathrm{unit}}=(w/4)J_{\rm rot}\) and the physical substitution makes
\[
\boxed{
h^{-2}[ab]P_{uv,h}=(w/4)J_{\rm rot},\quad
h^{-2}[ab]P_{xy,h}=-(w/4)B.
}\tag{11}
\]
Thus (10) is not a sequence collapsing to pure gauge/flat geometry. This is a genuine coefficientwise NONFLAT continuum curvature signal with the original source type.

**Limit of (10):** It is not an actual all-amplitude exact finite Palatini root, an \(O(h)\) bound on the untruncated nonlinear residual, a nonempty uniformly nondegenerate *whole-series* recovery, a proof on the original periodic carrier, or a physical D0→GR theorem. Exact full 40-Euler cancellation is coefficientwise through amplitude order four only.

## 3. Proof artifacts and independent bounded checks

- [check_polynomial_cartan_inverse.cjs](sources/d0_two_null_crossing_2026-10-19/check_polynomial_cartan_inverse.cjs) re-derives the ACTUAL flat link-linearization of the six-based-plaquette source, including BOTH adjacent faces and odd curvature derivative. It verifies the homogeneous 24×24 matrix in ALL 576 entries; the exact integer identities \(M^4-5M^2+4I=0\) and \(M^{-1}=(5M-M^3)/4\); and 140 independent polynomial-degree-loss fixtures in six-body direction tests at degrees1–4. The arbitrary-degree theorem follows from the finite-shift proof (4), not extrapolation from those samples. Script is standalone Node, no external package.
- [check_quartic_graded_refinement.cjs](sources/d0_two_null_crossing_2026-10-19/check_quartic_graded_refinement.cjs) reads both EXISTING SHA-pinned rational solution records, checks all five quartic amplitude sectors for negative h-degree, and prints the complete leading components. It does NOT recompute or alter the 840×1008 rational solve; the exact full-spatial all40 replay remains owned by [verify_quartic_full_spatial_jet.py](sources/d0_two_null_crossing_2026-10-19/verify_quartic_full_spatial_jet.py).
- The earlier exact fixed-h source owners retain their own independent coefficients, scalar/top CAR, OLD LEFT/RIGHT/reference and failure-probability law. The algebra above neither identifies different readout costs nor physically forces the AF-star field code.

**Next consuming move**: replace all repeated polynomial 24-link coefficient solves by formula (5), compute the TRUE 16-component reduced finite Einstein Schur operator and its polynomial image/Noether consistency **in the same graded carrier**. Then either build an all-order convergent section by a controlled elliptic/analytic inverse with specified boundary, or report its first exact cokernel. Only thereafter can full same-programme Book/PREP/CAR16/source/clock/old-history/refinement and raw #216 be tested for physical GR selection. GR_closed=false.
