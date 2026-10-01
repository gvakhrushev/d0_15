# Fixed warp: transverse-mean reduction about the exact designated root

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Background owner: A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md.
Status: analytic reduction for arbitrary four-dimensional O(h) fields; not a task terminal.

## 1. Setup

Fix
\[
S(y)=\operatorname{diag}(1,1,f(y_1),f(y_1)),\qquad
f(y)=1+\frac{1-\cos(2\pi y)}{50},
\]
with h=1/L. Let K_h^*(x_1) be the exact designated connection from the
warped designated rescue. It is invariant in x_0,x_2,x_3 and satisfies
\[
E_K(Q_h,K_h^*)=0.
\]

Take an arbitrary full-lattice field in the same compact log chart,
\[
K_h=K_h^*\exp u_h,\qquad \|u_h\|_\infty\le Ch,
\tag{1}
\]
and assume the full connection equation E_K(Q_h,K_h)=0.

Let P_0 be the normalized average over x_0,x_2,x_3 at fixed x_1, applied
componentwise to the 24 link-log coordinates. Put
\[
\bar u_h=P_0u_h,\qquad u_h^\perp=(I-P_0)u_h.
\tag{2}
\]

## 2. Linearization commutes with the transverse mean

Define
\[
F_h(u)=E_K(Q_h,K_h^*e^u),\qquad H_h=DF_h(0).
\]
The background and the literal finite stencil are translation-equivariant in
x_0,x_2,x_3, hence
\[
P_0H_h=H_hP_0.
\tag{3}
\]

Finite incidence and analyticity on the compact chart give
\[
F_h(u)=H_hu+N_h(u),\qquad
\|N_h(u)\|_\infty\le C_g\|u\|_\infty^2.
\tag{4}
\]
Applying P_0 to the exact equation yields
\[
H_h\bar u_h=-P_0N_h(u_h).
\tag{5}
\]

## 3. The zero-transverse block is uniformly invertible

Restricted to fields invariant in x_0,x_2,x_3, H_h is exactly the 24L
connection derivative of the warped designated rescue. Its literal
variable-coefficient parametrix gives, for sufficiently fine meshes,
\[
\|(H_h|_{\operatorname{im}P_0})^{-1}\|_{\ell^\infty\to\ell^\infty}\le18.
\tag{6}
\]

Combining (1), (4)--(6),
\[
\boxed{\|\bar u_h\|_\infty\le18C_gC^2h^2.}
\tag{7}
\]

Thus the full leading O(h) correction has zero transverse mean:
\[
u_h=h\,b_h^\perp+O(h^2),\qquad P_0b_h^\perp=0.
\tag{8}
\]

No smoothness, derivative bound, Fourier support, or four-phase ansatz for
u_h^\perp is assumed.

## 4. Interpretation

The exact designated root already carries the order-h Cartan transport.
Equation (7) proves that an additional exact O(h) field cannot replace it in
the transverse-zero channel. Any surviving leading microstructure is
genuinely oscillatory in at least one of x_0,x_2,x_3.

This strengthens the Cartan-scale dichotomy: the unresolved class is
zero-mean transverse rough Cartan-scale microstructure about the designated
connection.

## 5. Add the independently prescribed smooth source

Assume additionally
\[
E_Q(Q_h,K_h)=h^2\tau(hx_1),
\tag{9}
\]
with tau fixed independently of the candidate. The source and the comparator
are transverse-invariant, so every nonzero-transverse component of the metric
response difference is zero.

Expanding the metric rows,
\[
E_Q(Q_h,K_h)-E_Q(Q_h,K_h^*)
=C_hu_h+R_{Q,h}(u_h,u_h)+O(\|u_h\|_\infty^3),
\tag{10}
\]
and projecting the connection and metric equations to nonzero transverse
characters gives for b_h^\perp=u_h^\perp/h
\[
H_hb_h^\perp=O(h),\qquad
C_hb_h^\perp=O(h),\qquad
P_0b_h^\perp=0.
\tag{11}
\]

Therefore every defect/correlation measure of the surviving leading field is
supported on the joint connection/metric kernel of the frozen physical
symbol. The smooth Cartan component has already been removed by (7).

The transverse-zero metric equation at order h^2 consists of the O(h^2)
mean range correction determined by (5), plus the quadratic zero-character
correlation of b_h^\perp. Eliminating the former is exactly the Schur/reduced
quadratic response in the owned correlation law.

## 6. Residual terminal on this fixed curved metric

For arbitrary O(h) exact sourced sequences in the compact chart, the
fixed-warp problem is reduced to one statement:
\[
\boxed{
\text{the reduced quadratic metric form vanishes on every nonlinear-realizable
zero-mean transverse joint-kernel correlation.}
}
\tag{12}
\]

If (12) holds, the designated exact branch and owned reconstruction give the
Einstein response on this fixed genuinely curved metric. If it fails,
exactifying a realizing correlation gives the independently sourced
counterexample.

Verdict: WARPED-FULL4D-LEADING-MEAN-REDUCED-TO-JOINT-CORRELATIONS.

No all-torus classification, realizability theorem, action change, selector,
BOOK/CORE promotion, or task-level terminal is asserted.
