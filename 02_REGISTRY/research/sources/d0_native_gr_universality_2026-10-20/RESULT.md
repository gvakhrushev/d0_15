# Exact local coframe pullback for a nonseparable site-density pressure

**Consumer:** the `constitutive` / `native_sector` inputs of the existing positive-GR route.
**Status:** exact conditional theorem; the physical factorization premise is open.
**Scope:** vacuum six-face Palatini site densities on the original coframe/link carrier.  This is not a selected D0 action, a matter theorem, or a GR closure result.

## Theorem

Let there be finitely many sites (i=1,ldots,m).  At site (i), let (e_i) range in a finite-dimensional coframe vector space (V_i) of dimension (d_i), and let (U) denote all proper-Lorentz links.  Suppose each site density (f_i(e,U)) is (C^2), depends on the coframe only through (e_i), and is homogeneous of degree two in that coframe:

\[
f_i(e_1,ldots,t e_i,ldots,e_m,U)=t^2 f_i(e,U).
\]

The densities may share and depend arbitrarily on the links (U).  Let (F) be (C^2) on a neighborhood of (0\in\mathbb R^m), and put

\[
w_i=\partial_i F(0),\qquad w_i\ne0.
\]

For (s\) near zero define

\[
a_i(s)=\int_0^1\partial_iF(ts)\,dt,\qquad
q_i(s)=\sqrt{a_i(s)/w_i}.
\]

Since (a_i(0)=w_i), a sufficiently small neighborhood has (a_i(s)/w_i>0).  Define the coframe map, leaving every link unchanged, by

\[
\Phi(e,U)=(q_i(f(e,U))e_i)_{i=1}^m,\ U.
\]

Then the following identity holds exactly throughout that neighborhood:

\[
F(f(e,U))-F(0)=\sum_i w_i f_i(\Phi(e,U),U).
\tag{1}
\]

### Proof of the action identity

The fundamental theorem of calculus along the line (t\mapsto ts) gives

\[
F(s)-F(0)=\int_0^1\sum_i s_i\partial_iF(ts)\,dt
=\sum_i s_i a_i(s).
\]

Degree-two homogeneity gives (f_i(\Phi(e,U),U)=q_i(s)^2s_i=a_i(s)s_i/w_i), proving (1).  No separability of (F) is used; all mixed site derivatives are allowed.

### Proof that this is a local field-coordinate change

The induced scalar map is

\[
g_i(s)=q_i(s)^2s_i=s_i a_i(s)/w_i.
\]

It is (C^1), satisfies (g(0)=0), and has (Dg(0)=I_m); the inverse function theorem therefore makes (g) a local diffeomorphism near zero.

For completeness, this also implies invertibility on the full coframe chart, not just in the (m) scalar densities.  Write (D_ef) for the (m\times\sum_i d_i) density derivative, let (P_e:\mathbb R^m\to\bigoplus_i V_i) send (c\) to ((c_i e_i)_i), and set (A=D_s\log q).  With (Q=\operatorname{diag}(q_i I_{d_i})), differentiation gives

\[
D_e\Phi=Q(I+P_e A D_ef),\qquad D_ef\,P_e=2\operatorname{diag}(s).
\]

Sylvester's determinant identity and
\[
Dg=\operatorname{diag}(q_i^2)(I+2\operatorname{diag}(s)A)
\]
then yield

\[
\det D_e\Phi=\left(\prod_i q_i^{d_i-2}\right)\det Dg.
\tag{2}
\]

Near (s=0), every (q_i>0) and (Dg) is nonsingular, so (D_e\Phi) is nonsingular.  The joint map ((e,U)\mapsto(\Phi_e(e,U),U)) has block-triangular derivative and is locally invertible as well.  The inverse can depend on (U); the physical link variables themselves are not redefined.

### Euler zeros and second variation

Let (A_F(e,U)=F(f(e,U))-F(0)) and (A_w(e,U)=\sum_iw_if_i(e,U)).  Equation (1) says (A_F=A_w\circ\Phi).  At a stationary point, independent radial coframe variations (e_i\mapsto(1+t)e_i) give

\[
2s_i\partial_iF(s)=0 \quad\text{for }A_F,
\qquad 2w_i s_i=0 \quad\text{for }A_w.
\]

Shrink the neighborhood so every \(\partial_iF(s)\ne0\).  Either stationary system then has (s=0).  At (s=0), (q_i=1), so \(\Phi(e,U)=(e,U)).  Since \(\Phi) is a local diffeomorphism, (1) consequently gives the same pointwise stationary set in the original local field chart, including its link equations.

At a common stationary point (y=(e,U)), second-order expansion of (1) gives

\[
D^2 A_F(y)=D\Phi(y)^T D^2 A_w(y)D\Phi(y).
\tag{3}
\]

Thus the Hessians are congruent, and \(D\Phi\) maps their kernels isomorphically.  **Sharpening from independent site-radial variations:** in fact their null kernels are the **SAME subspace even in original raw coframe/link coordinates at every genuine common stationary vacuum**, although the Hessian matrices themselves need not agree.

To prove the stronger assertion, let \(Z_i\) be the moving radial vector field that scales coframe \(e_i\) and leaves every other coframe/link fixed.  The original degree-two identity gives \(d A_F[Z_i]=2s_i\,\partial_iF(s)\) and \(d A_w[Z_i]=2w_is_i\).  At a common stationary root \(s=0\), differentiate along any original tangent \(V\): all terms involving \(d A[ D_V Z_i]\) vanish by stationarity, so
\[
D^2 A_F[V,Z_i]=D^2 A_w[V,Z_i]=2w_i\,ds_i[V].
\]
Moreover at this same root the exact chain rule gives
\[
D^2A_F=D^2A_w+\sum_{i,j}\partial_i\partial_jF(0)\,ds_i\otimes ds_j.
\]
If \(V\in\ker D^2A_F\), the first identity forces \(ds_i[V]=0\) for every \(i\), making the extra term vanish, so \(V\in\ker D^2 A_w\).  The converse follows by identical reasoning using \(D^2 A_w[V,Z_i]=2w_i ds_i[V]\).  Hence
\[
\boxed{\ker D^2 A_F(y)=\ker D^2 A_w(y)}
\]
at every genuine common stationary point, **not merely congruent kernel dimensions**.  The distinction is relevant: arbitrary nonlocal Book mixed Hessian entries may modify offshell propagation/source residues but cannot change the full homogeneous linearized Euler nullspace under the theorem's radial and factorization premises.  This sharpened argument is developed in [the full arbitrary nonseparable vacuum universality owner](../../A4D_ARBITRARY_NONSEPARABLE_BOOK_COST_FINITE_EINSTEIN_VACUUM_UNIVERSALITY_2026_10_20.md).

## What this result buys the GR route

A future derivation need not prove that the complete history pressure is a separable sum of site terms.  It is enough to prove, on the admitted physical chart and after legitimate elimination of internal variables, that its entire geometric dependence is (F(f_1,\ldots,f_m)), with nonzero site derivatives.  If the (w_i) are a common constant, (1) is locally an exact pullback of the original unweighted Palatini star.  Unequal (w_i) only give a weighted star and do not establish a universal Einstein coupling.  A matter term, observer/preparation/clock/work contributions, or any dependence outside the (f_i) is not covered by this theorem.

The unresolved constitutive premise is precisely that factorization for the compulsory unchanged D0 program, together with the actual nonzero/common (w_i), and a same-run nonempty physical chart.  The present result does not select such a program.  The hostile 718-edge fixture in the adjacent checker is a constructed native-type countercontrol showing that a smooth, genuinely nonseparable complete-history pressure can satisfy the hypotheses; it does not show that D0 chooses its field-to-Info/Cost map.

## Replay boundary

`check_nonsplit_full_book_pressure_to_exact_weighted_star.mjs` exercises one floating-point (L=2) fixture on the original 16-site six-face star, the original 718 directed transitions, and all 8440 retained two-/three-step closed histories.  Its finite differences and eight-node Gauss–Legendre line integration are numerical witnesses for that fixture.  They do not prove (1)–(3), the local inverse theorem, or physical action selection; those are supplied by the analytic argument above or remain open as stated.
