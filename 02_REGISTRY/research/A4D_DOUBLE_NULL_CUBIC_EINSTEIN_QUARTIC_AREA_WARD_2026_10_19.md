# D0 → GR: кубический вакуумный Ricci bootstrap и mixed quartic coframe jet

19 October 2026. **RESEARCH / EXACT CONTINUUM degree≤4 + EXACT LATTICE POISSON + EXACT LOCAL FINITE 40-EULER CUBIC JET + EXACT LOCAL MIXED [a²b²] 40-EULER COFRAME JET. Same Draft #334.** Pinned consumer: [exact original finite mixed all40 Cartan/Einstein result](A4D_DOUBLE_NULL_EXACT_FINITE_QUADRATIC_CARTAN_EINSTEIN_BOOTSTRAP_2026_10_19.md); [two-null coframe](A4D_DOUBLE_NULL_CARTAN_CROSSING_RICCI_WEYL_SPLIT_2026_10_19.md); [existing full Golden moving-volume PF quantile](A4D_BALANCED_NATIVE_GOLDEN_EXACT_SOURCE_SEAM_LOCAL_TO_VOLUME_MEAN_2026_10_19.md). No new action, gate, extra particle or fitted cosmological/Newton coefficient. **The cubic and mixed quartic results are local unwrapped perturbative jets; neither is a periodic carrier root, an all-order solution, or a compulsory physical D0 price.** Status GR_closed=false.

## 1. The third-order nonlinear Ricci source fixes a Poisson equation, not a new action

Let X=(x,y) and A,B be any fixed real transverse vectors satisfying A·B=0, with w=A_xB_y−A_yB_x ≠0, and consider the 2-null coframe
\[
e^+=du+\tfrac12J\,dv,\quad e^-=dv+\tfrac12H\,du,\quad e^{2,3}=dx,dy,
\]
where initially H=a(A·X), J=b(B·X); a,b formal independent wave amplitudes. On this uncorrected profile the first nonzero Ricci components after the EXACT mixed ab null cancellation are
\[
\boxed{
[\operatorname{Ric}_{uu}]_{a^2b}=\frac{|A|^2(B\cdot X)}8,\qquad
[\operatorname{Ric}_{vv}]_{ab^2}=\frac{|B|^2(A\cdot X)}8.
}
\tag{1}
\]
Every other Ricci coefficient of total degree≤3 vanishes, including all ab coefficients and all pure a or pure b coefficients. This is a tensor identity, not only a trace equality.

The two existing null pp operators at leading order read (for these profiles and curvature convention) \(\mathrm{Ric}_{uu}=\tfrac12\Delta_\perp H\) and \(\mathrm{Ric}_{vv}=\tfrac12\Delta_\perp J\). Cancel (1) with
\[
\boxed{\begin{aligned}
H&=a(A\cdot X)-\frac{a^2b\,|A|^2} {32}(B\cdot X)(x^2+y^2),\\
J&=b(B\cdot X)-\frac{ab^2\,|B|^2} {32}(A\cdot X)(x^2+y^2).
\end{aligned}}\tag{2}
\]
Indeed, in the transverse two-plane
\[
\boxed{\Delta_\perp[(V\cdot X)(x^2+y^2)]
       =\Delta_h^\perp[(V\cdot X)(x^2+y^2)]=8(V\cdot X),}\tag{3}
\]
for EVERY finite grid spacing h on the original five-point stencil. Direct calculation of ALL SIXTEEN components of the smooth Ricci tensor (including inverse metric and the exact metric cross-term HJ/4, not separate pp linearizations) gives
\[
\boxed{\operatorname{Ric}_{\mu\nu}=O_{\mathrm{total\ degree}\ge4}.}\tag{4}
\]
The correction retains the nonzero mixed Weyl curvature \(R^{2}{}_{3uv}=ab\,w/4+O_{\ge3}\) of the exact quadratic original-lattice owner.

**Scope:** (3) is an exactly finite discrete *scalar Poisson* identity, while (4) is a *continuum metric Ricci* identity. The separate [finite cubic Cartan checker](sources/d0_two_null_crossing_2026-10-19/check_cubic_finite_cartan_range.py) constructs a local polynomial response on the original six plaquettes that cancels all 24 link and 16 coframe Euler rows through total amplitude degree 3 for the arbitrary orthogonal affine family. A restricted [mixed-quartic range control](sources/d0_two_null_crossing_2026-10-19/check_quartic_finite_cartan_range.py) has no solution when the quartic coframe is held to the canonical area mode. Releasing all 16 quartic coframe components through spatial degree 4 gives an exact solution of the `[a²b²]` coefficient for `A=(1,0), B=(0,1)` in the [full-coframe checker](sources/d0_two_null_crossing_2026-10-19/check_quartic_full_coframe_range.py): a `600 × 916` rational system including (14), degree-5 quartic links and the full joint cubic affine family. This is a local coefficient result, not a periodic carrier root, uniform refinement, or nonzero all-order vacuum solution; other degree-4 amplitude sectors remain open.

## 2. Exact two-Killing orbit-current Ward from geometry

Because H,J depend only on x,y in the affine crossing and corrections (2), the metric has two commuting Killing coordinates u,v. Write its 2×2 orbit metric and positive orbit area
\[
\mathcal G=\begin{pmatrix}H&1+HJ/4\\1+HJ/4&J\end{pmatrix},
\qquad \rho=\sqrt{-\det\mathcal G}=\det e=\Omega=1-\frac{HJ}{4}>0.
\tag{5}
\]
The transverse metric is exactly \(-dx^2-dy^2\). For this purely geometric block metric, direct Christoffel computation gives the exact identity
\[
\boxed{
\partial_i\bigl(\rho\,\mathcal G^{-1}\partial_i\mathcal G\bigr)
=2\rho\,\mathcal G^{-1}\operatorname{Ric}_{\rm orbit}.
}\tag{6}
\]
Summation over i=x,y. Taking the matrix trace and using
\(\operatorname{tr}(\mathcal G^{-1}\partial_i\mathcal G)=2\partial_i\log\rho\) gives
\[
\boxed{
\Delta_\perp\rho=\rho\,\operatorname{tr}(\mathcal G^{-1}\operatorname{Ric}_{\rm orbit}).
}\tag{7}
\]
Thus a NECESSARY exact vacuum Einstein condition for this block family is
\[
\boxed{\Delta_\perp\rho=0.}\tag{8}
\]
This is a geometric reduced Einstein/Bianchi consequence, NOT the yet-unproved full native retained-history Ward of D0. It is a way to test the next coefficients of any proposed geometric continuation before computing all40 finite-source rows.

## 3. A new fourth-order obstruction to retaining ONLY the two original null functions

Insert the source-forced cubic particular solutions (2) into (5). Its full area coefficient at order \(a^2b^2\) is
\[
\boxed{
[\rho]_{a^2b^2}
=\frac{(|A|^2(B\cdot X)^2+|B|^2(A\cdot X)^2)(x^2+y^2)}{128}
=\frac{|A|^2|B|^2}{128}(x^2+y^2)^2
}\tag{9}
\]
(the final equality uses A·B=0 in TWO transverse dimensions).
Therefore
\[
\boxed{
[\Delta_\perp\rho]_{a^2b^2}
=\frac{|A|^2|B|^2}{8}(x^2+y^2)\ne0,
\quad
[\Delta_\perp^2\rho]_{a^2b^2}
=\frac{|A|^2|B|^2}{2}\ne0.
}\tag{10}
\]
This violates the necessary vacuum orbit-area law (8) at the next order. It is NOT an obstruction to the previously proved quadratic or cubic truncations; it is a failure of a *particular minimal two-function attempt* to extend them unchanged to all orders.

**Harmonic-freedom control.** Let \(F,G\) be any smooth transverse harmonic cubic-order additions with \(\Delta F=\Delta G=0\) and with the same amplitude monomials a²b, ab². They modify the area coefficient by products of a transverse linear function and a harmonic function. For any affine linear \(L=V\cdot X\),
\[
\Delta_\perp^2(LF)=L\Delta_\perp^2F+4V\cdot\nabla\Delta_\perp F=0.\tag{11}
\]
Hence these harmonic additions **cannot erase the nonzero biharmonic trace (10)**. This is a rigorous obstruction inside the explicitly declared *minimal branch-preserving coframe restriction*: no additional independent ab coframe corrections, no transverse metric deformation, no rescaled null leg and no extra physical source. It is NOT a no-go for arbitrary two-Killing vacuum metrics or full D0.

The finite native five-point stencil has an exact, useful companion:
\[
\Delta_h^\perp(x^2+y^2)^2=16(x^2+y^2)+4h^2,\qquad
(\Delta_h^\perp)^2(x^2+y^2)^2=64.\tag{12}
\]
Thus the area bi-Laplacian obstruction is also exactly nonzero at every finite h for THIS polynomial trace, although Eq.(8) is a continuum block-Einstein identity, NOT yet the same finite-Palatini Ward identity.

## 4. Reverse breakthrough: the necessary repair already lives inside the ORIGINAL 16 coframe variables

Do not add a source, action, gauge group or new degree-of-freedom beyond the original full coframe. Release ONE previously frozen null-leg scale,
\[
\boxed{
e^+=(1+\sigma)\,du+\tfrac12J\,dv,\quad
e^-=dv+\tfrac12H\,du,\quad e^{2,3}=dx,dy,
}\tag{13}
\]
where the order4 *geometry-determined* particular choice is
\[
\boxed{
[\sigma]_{a^2b^2}
=-\frac{|A|^2|B|^2}{128}(x^2+y^2)^2.
}\tag{14}
\]
Then
\[
\rho=\det e=1+\sigma-\frac{HJ}{4}
\quad\Rightarrow\quad
[\rho]_{a^2b^2}=0,\qquad [\Delta_\perp\rho]_{a^2b^2}=0.
\tag{15}
\]
This repairs the necessary **orbit-area trace** through fourth order; it does NOT imply all trace-free orbit-current or transverse Ricci equations vanish. The restricted test with only this canonical area mode is inconsistent, even after releasing the joint cubic kernel. The full-coframe checker then releases every quartic coframe component through spatial degree 4 and solves the mixed `[a²b²]` equations exactly. Thus the remaining local response is available inside the original coframe field; no new action or controller term is inserted. The result is still only one local coefficient and does not imply the other quartic equations or a periodic root.

**Strategic significance.** The same two-branch interaction that first generated the orientation/Weyl signal also forces a moving geometric measure at the next order. The correct geometric extension is NOT more H/J harmonic waves; it is the intrinsic orbit-area/half-density slot that was already needed for the Golden moving-PF volume/quantile source. This identifies a concrete common *kinematic* interface for future physical native-record/GR matching. It is not evidence that Book's complete \(H+J+R\) price actually chooses that slot and solves its own preparation/clock/controller equations.

## 5. Exact finite cubic and mixed-quartic response; next consumer

[Exact symbolic Python checker](sources/d0_two_null_crossing_2026-10-19/check_cubic_ricci_poisson.py) checks four independent orthogonal gradient examples and one symbolic arbitrary orthogonal pair \(A=(r,q),B=s(-q,r)\). It asserts all16 continuum Ricci components through degree3, exact five-point Poisson for both corrections, quartic area and its nonzero finite bi-Laplacian, the exact algebraic cancellation (15) and the arbitrary harmonic product bi-Laplacian identity. Independently verified symbolic finite Laplacian:
\(\Delta_h r^4=16r^2+4h^2,\ (\Delta_h)^2r^4=64\).

The finite cubic checker starts from the source-forced `H_3,J_3` and the exact cubic 24-link lift. The remaining coframe source is not removed by changing only those two radial coefficients. Releasing all 16 original coframe components together with degree-2 proper-Lorentz link jets gives a `192 × 240` rational response system for each of `[a²b]` and `[ab²]`. A particular exact solution is constructed by setting only algebraically free parameters of the linear solve to zero; direct substitution verifies every row as a polynomial identity in `x,y,r,q,s`. Thus all 40 finite Euler rows vanish for all ten amplitude monomials through total degree 3, and the exponentiated links satisfy the Lorentz condition through the same order. The linear mixed `[ab]` curvature remains the nonzero crossed-Weyl term of the quadratic owner.

The [restricted mixed-quartic range control](sources/d0_two_null_crossing_2026-10-19/check_quartic_finite_cartan_range.py) with its [receipt](sources/d0_two_null_crossing_2026-10-19/quartic_finite_cartan_range_result.json) first exposed a useful boundary: fixing the quartic coframe to the orbit-area mode leaves an inconsistent `480 × 676` system, even though the full 172-dimensional joint cubic affine family is released. That is not a full-coframe no-go.

The [full-coframe mixed-quartic checker](sources/d0_two_null_crossing_2026-10-19/check_quartic_full_coframe_range.py), with its [pinned receipt](sources/d0_two_null_crossing_2026-10-19/quartic_full_coframe_range_result.json), solves the same original 24 link and 16 coframe Euler rows at `[a²b²]` for `A=(1,0), B=(0,1)`. Its exact `600 × 916` rational affine system releases 172 joint cubic kernel parameters, 504 degree-≤5 proper-Lorentz link coefficients and all 240 quartic coframe coefficients (16 components, spatial degree≤4). Exact substitution into all spatial coefficients of the 40 rows and the proper-Lorentz check through amplitude degree 4 pass. This is a local mixed coefficient, not the full degree-4 jet: `[a⁴]`, `[a³b]`, `[ab³]`, and `[b⁴]` remain unchecked, as do periodicity and refinement.

The next finite step is a shared-kernel solve for all five quartic amplitude sectors; the same cubic kernel parameters must be used across sectors. Uniform refinement, convergence, periodic-carrier recovery, full same-programme Cost−Info/admission, and physical source selection remain open. Do not promote `GR_closed`, raw #216, or a physical Newton coefficient.
