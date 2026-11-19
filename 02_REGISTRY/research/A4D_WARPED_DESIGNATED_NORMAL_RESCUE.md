# Exact designated continuation on a fixed curved warped background

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Exact inverse developed from `aa90a4359bb0f5a07e97c3d07e693e5f0d3aab60`;
publication inputs refreshed through `ae0285cc765a8d058fee5cad1d310c87c9350260`.
The 2026-10-01 authoritative v2 handoff is applied: this is scoped
Target D (designated continuation), with Target U kept separate.
No change to the action, Lorentz quotient, or source convention.

Status: an exact parametric Laurent inverse and an analytic uniform
variable-coefficient rescue theorem in a nonlinear invariant sector.
This proves existence of a full connection-stationary branch on the
fixed curved metric used in the earlier L=8,12 probe, for all sufficiently
fine meshes. It also proves its response agreement with the designated
smooth comparator in the unweighted owner sum norm. It does not classify
other stationary branches or impose the task's independent metric source.

The [exact certificate](certificates/a4d_warped_designated_normal_rescue_check.py)
and [coefficient ledger](certificates/a4d_warped_designated_normal_rescue_results.json)
contain a two-sided polynomial inverse identity, kernel and first-moment
bounds, and the independently checked physical normal-jet normalization.

## 1. Metric, variables and theorem

Fix a positive, one-periodic smooth function f and sample

\[
S(y)=\operatorname{diag}(1,1,f(y_1),f(y_1)),\qquad
g=S^T\eta S=\operatorname{diag}(1,-1,-f^2,-f^2).
\]

First take `1<=f<=26/25`. This includes the same fixed nonflat metric

\[
f(y_1)=1+\tfrac1{50}(1-\cos(2\pi y_1))
\tag{1}
\]

at every refinement. Its amplitude is not sent to zero with h. At y1=0,
`g=eta`, `dg=0`, and `f''=2*pi^2/25!=0`.

Let h=1/L. The connection variables are all 24 independent Lorentz link
coordinates at each x1, constant in x0,x2,x3. Denote this sector by X_L.
There is no restriction on their x1 frequencies or on their six generator
components. X_L is closed under every shift, product, exponential and
inverse in the actual equation. The sampled metric has the same symmetry.

Choose the #216 formal smooth comparison connection in this symmetry
class and write `A_h^sm=log K_h^sm`. Its recurrence and asymptotic summation
give, for this fixed C-infinity f,

\[
\|A_h^{\rm sm}\|_\infty\le M_A h,\qquad
r_h=E_K(Q_h,e^{A_h^{\rm sm}})=O(h^\infty).
\tag{2}
\]

Here the sup norm is the largest generator coordinate. The residual is
super-algebraic in every fixed smooth seminorm, hence also in the physical
unweighted sum after multiplication by the polynomial site count.
The #216 construction remains an approximate solve until the argument below.

**Theorem.** For all sufficiently large L there is a real exact connection
`K_h^*=exp(A_h^sm+u_h)` in X_L with

\[
E_K(Q_h,K_h^*)=0,\qquad
\|u_h\|_{\ell^p}\le36\|r_h\|_{\ell^p},\quad 1\le p\le\infty.
\tag{3}
\]

The norm is the same component convention on input and output; the
unweighted owner sum is included. Consequently, also in the physical
four-dimensional unweighted sum,

\[
\boxed{h^{-2}\|E_Q(Q_h,K_h^*)-E_Q(Q_h,K_h^{\rm sm})\|_1
=O(h^\infty).} \tag{4}
\]

The actual relative increment
`delta_h=log((K_h^sm)^(-1) K_h^*)` has the same super-algebraic bound:
the pointwise logarithm/BCH coordinate change has a uniformly bounded
derivative in this shrinking chart. Thus (3) is a rescue about the same
curved comparator, not a forcing estimate involving `||g-eta||`.

The solution is locally unique in a sufficiently small X_L neighborhood. No
uniqueness among arbitrary four-dimensional connection fields is asserted.
All fields in X_L have transverse characters `(z0,z2,z3)=(1,1,1)`;
the diagonal quarter center and all six continuous physical rank-23
circles are absent from this sector. See the corrected
[A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md](A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md). Its correction therefore has zero
coordinate on those resonant fibers without a nonlinear Fourier cutoff.
The sector is preserved by the full equation, and the construction solves
all its connection rows rather than only a projected range equation.

In the #216 reconstruction convention the sign-independent comparison (4)
gives `R_h[h^-2 E_Q(Q_h,K_h^*)]=-G[g]/2+O(h)`. The raw Gram-dual
normalization checked separately in Section 6 is typed explicitly there.

## 2. Exact inverse of the entire frozen one-coordinate symbol

Freeze f at a value s>0. In generator order
`(K1,K2,K3,J12,J13,J23)` and role-major connection coordinates, let
`H_s(z)=A_s(1,z,1,1)^T` be the literal connection Euler symbol.
The six complementary solder weights are

\[
(s^2,s,s,s,s,1)
\]

in face order `(01,02,03,12,13,23)`. Thus H has s-degree at most two
and Laurent z-degree in `{-1,0,1}`.

The exact checker constructs a matrix P_s(z) of s-degree four and
Laurent support `-4<=degree_z<=4`, and verifies every coefficient of

\[
\boxed{
H_s(z)P_s(z)=P_s(z)H_s(z)=s^2 D_s(z)I_{24},\qquad
D_s(z)=18-4s^2+(2s^2-1)(z^2+z^{-2}).
} \tag{5}
\]

Interpolation is used only to propose P. Both complete polynomial
products are then checked identically over Q. The proof of (5) therefore
does not depend on a finite character grid. Additional direct checks use
Gaussian-rational physical characters outside the interpolation set.

On the unit circle,

\[
D_s(e^{i\theta})=16+4(1-2s^2)\sin^2\theta.
\]

It is bounded away from zero on any compact interval
`0<a<=s<=b<sqrt(5/2)`. All these frozen operators are invertible on
the **whole** character circle, including short wavelengths.

At s=1 the absolute row and column coefficient sums of P_1 are both 70.
Since `D_1=14+z^2+z^-2`, its geometric inverse has convolution norm at
most 1/12. Hence

\[
\|H_1(T)^{-1}\|_{\ell^p\to\ell^p}\le35/6
\tag{6}
\]

on every period, for every p. No low-frequency projection is involved.

For the interval `[1,26/25]`, the certificate gives the following
coefficientwise majorants. They bound the sum of suprema of the kernel
coefficients over s; they are strong enough for variable coefficients.

| Quantity | Exact upper bound |
|---|---:|
| absolute coefficient envelope of `P_s/s^2` | `63406/625` |
| `alpha_min-2*beta_max`, with `alpha=18-4s^2`, `beta=2s^2-1` | `7092/625` |
| inverse-kernel envelope B0 | `31703/3546 < 9` |
| first absolute kernel moment B1 | `247885757/6287058 < 40` |
| coefficient envelope of `partial_s H_s` | `129/25` |

To see the moment bound explicitly, expand

\[
D_s(T)^{-1}=\alpha_s^{-1}
\sum_{n\ge0}\left[-\frac{\beta_s}{\alpha_s}(T^2+T^{-2})\right]^n.
\]

Put `a0=alpha_min`, `b0=beta_max` and `d=a0-2*b0>0`. The scalar
kernel has total absolute mass at most 1/d and first moment at most
`4*b0/d^2`. Multiplication by `P_s/s^2`, whose support radius is four,
gives `B1 <= (63406/625)*(4/d+4*b0/d^2)`. Periodization can only
decrease these coefficient majorants, so the bounds are uniform in L.

The compact range is a substantive hypothesis. At s=2 the polynomial
`7*z^4+2*z^2+7` has four unit-circle zeros. Modulo that polynomial,
the `(1,9)` entry of `z^4 P_2(z)` is `40*z^3/7`, using zero-based indices.
It is nonzero at every such zero. Equation (5) therefore supplies a
nonzero physical kernel vector there. A uniform frozen inverse on all
positive warp values would be false.

## 3. Intercell coupling: an explicit variable-coefficient parametrix

Write the frozen symbol as `H_s(z)=sum_j H_j(s)z^j`. The actual frozen
coefficient operator on the varying background is

\[
(\mathcal H_h^{\rm fr}u)(x)=\sum_{j=-1}^1H_j(f(hx))u(x+j).
\]

Let B_k(s) be the inverse kernel from (5) and define the left-quantized
parametrix

\[
(\mathcal B_h u)(x)=\sum_{k\in\mathbb Z}B_k(f(hx))u(x+k).
\tag{7}
\]

Use the periodic lift of u and f in this absolutely convergent sum. The
preceding envelopes give `||B_h||_p<9`, including both endpoint norms
and the component-sum version of every p.

The exact product differs from the frozen identity by

\[
(\mathcal B_h\mathcal H_h^{\rm fr}-I)u(x)
=\sum_{k,j}B_k(f(hx))
\left[H_j(f(h(x+k)))-H_j(f(hx))\right]u(x+k+j).
\]

This keeps all links crossing cell boundaries. Periodicity and the
ordinary mean-value estimate give
`|f(h(x+k))-f(hx)|<=h|k| ||f'||_infinity` for every integer k.
The kernel moment and derivative bounds imply

\[
\|\mathcal B_h\mathcal H_h^{\rm fr}-I\|_p
\le207h\|f'\|_\infty. \tag{8}
\]

The coefficientwise majorants are why (8) also holds in unweighted
ell-one. No Fourier cutoff, blockwise resetting, or growing-dimensional
norm comparison occurs in this step.

## 4. Move the derivative to the actual smooth curved comparator

Set `F_h(A)=E_K(Q_h,exp A)` using the right-trivialized Euler components
and the generator log coordinates. Let `H_h=DF_h(A_h^sm)`.
This need not be a symmetric Hessian at a nonstationary comparator;
the inverse argument concerns this actual derivative.

Two elementary finite-stencil bounds control its difference from the
frozen operator:

\[
\|H_h-\mathcal H_h^{\rm fr}\|_p
\le h\left(300\|f'\|_\infty+8192M_A\right),
\quad\|A_h^{\rm sm}\|_\infty\le M_Ah\le1/48.
\tag{9}
\]

Here is a deliberately conservative count establishing the constants.
Each Euler component receives six incident-face contributions. Its
derivative has at most four link positions and six generator coordinates
per face, hence 144 scalar contributions in either row or column sums.
Every Lorentz generator has matrix operator norm one. Each face weight
matrix has nuclear norm at most `(26/25)^2`. The corresponding area
weight is sampled at distance at most one from the output link. Its
variation is at most `2*(26/25)*h||f'||`; thus the coefficient shift
bound is `144*2*(26/25)<300`.

For log coordinates with maximum component magnitude a, every matrix
log has norm at most 6a. The four factors give `exp(24a)`. Differentiating
a Jacobian term in another log direction costs at most 24 times that
coordinate sup norm, by the first and second exponential differential
bounds. For `a<=1/48`, use `exp(24a)<=2`; consequently the Jacobian
Lipschitz bound is at most
`144*24*2*(26/25)^2=4672512/625<8192`. The same row/column incidence
count proves the endpoint operator bounds and their component-sum versions.
It applies to the right-trivialized Euler map in log inputs, not just a
restriction of the action to a scalar ansatz.

Combining (8)--(9) gives the concrete estimate

\[
\|\mathcal B_h H_h-I\|_p
\le h\left(2907\|f'\|_\infty+73728M_A\right). \tag{10}
\]

For h small enough that the right side is at most one half, Neumann
inversion gives a left inverse with norm at most 18. On the finite
24L-dimensional sector a left inverse is an inverse. Thus

\[
\boxed{\|[DF_h(A_h^{\rm sm})]^{-1}\|_p\le18.} \tag{11}
\]

This is a derivative at the actual varying smooth comparator, uniformly
over all x1 frequencies. It is not the false replacement of the full
four-dimensional operator by `A(1)+O(h)`.

## 5. Nonlinear existence, owner-sum rescue and full stationarity

The same analytic bounds give the uniform relative remainder estimate

\[
F_h(A_h^{\rm sm}+u)=r_h+H_hu+N_h(u),\qquad
\|N_h(u)\|_p\le4096\|u\|_\infty\|u\|_p
\tag{12}
\]

in the stated chart, with the corresponding Lipschitz bound for the
sup-norm contraction. Solve

\[
u=-H_h^{-1}(r_h+N_h(u)).
\]

For example, `18^2*8192*||r_h||_infinity<=1/4`, together with inclusion
of the radius `36||r_h||_infinity` in the log chart, is a sufficient
contraction condition. Both hold for all sufficiently small h by (2).
This proves existence, not just a small-residual estimate. Absorbing
(12) in every p proves (3), on the same solution constructed in sup norm.

There is no missing transverse Euler equation for this solution. The
full action and Q_h are invariant under translations in x0,x2,x3.
The gradient at an invariant connection is invariant under those
translations. Its 24 components at each x1 are exactly the equations
solved above. Vanishing of those components is therefore vanishing of
every independent link derivative on the full carrier, including the
derivative against arbitrary noninvariant perturbations. This argument
does not say that the full Hessian is invertible in such directions.

Lifting an invariant field from L sites to L^4 sites repeats every
component L^3 times. Both sides of (3) acquire the same factor; the
unweighted sum estimate is preserved. The finite-stencil metric response
is uniformly Lipschitz on the compact solder/log chart in that actual
sum norm. This proves (4) and removes the #216 smooth residual for this
fixed genuinely curved class.

The construction also works on any compact warp interval
`0<a<=f<=b<sqrt(5/2)`, using the finite coefficient and moment bounds
provided by (5). The numerical constants 18 and 36 above are specifically
for `[1,26/25]`.

## 6. Physical response normalization and the Einstein normal jet

Use the literal metric partial in the ten symmetric Gram slots
`(00,01,02,03,11,12,13,22,23,33)`. Its physical mixed forcing has the
opposite phase to its readout. At f=1,

\[
C(z)=(z-1)J,\qquad B(z)=C(z^{-1})^T,
\qquad S_{\rm phys}(z)=-C(z)H_1(z)^{-1}C(z^{-1})^T.
\]

An independent literal base-area variation and edge-incidence assembly
checks this opposite-phase forcing on all ten metric inputs and rejects
the same-phase alternative. For `z=exp(t)`, the second derivative coefficient of the response is
`J H_1(1)^(-1) J^T`. The new checker constructs the standard Ricci
normal-Hessian expression independently and verifies on all ten inputs
that this matrix is precisely the Gram-dual half-Einstein operator:

\[
r[J_{ab,11}]=\tfrac12G_{\rm standard}[J_{ab,11}]. \tag{13}
\]

Raised output indices and the factor two on off-diagonal metric slots
are included. The opposite sign fails this exact check. This agrees with
the already owned #310/#273 normalization `r=G_standard[J]/2=-K_Schur[J]`.
The relation between a Fourier k^2 polynomial and a local second-derivative
jet supplies that minus sign. No action sign is changed to fit a probe.
The displayed `E_star` convention in #216 must not be silently identified
with a raw partial carrying a different normalization.

At a metric-normal observation point with `f=1`, `f'=0`, the second-order
coefficient of the smooth formal solution depends only on the normal
metric Hessian. Nonlinear products of first derivatives vanish there,
as in #216's normal-center argument. Combining that local calculation
with (4) yields the actual branch response

\[
\boxed{h^{-2}E_Q(Q_h,K_h^*)(0)
=\tfrac12G_{\rm standard}[g](0)+O(h).} \tag{14}
\]

Equation (14) is pointwise in the declared normal reconstruction. The
super-algebraic comparator-to-exact error in (4) is in the stronger owner
sum norm. A generic pointwise O(h) discretization error in (14) is not
asserted to be O(h) after an unweighted sum over L^4 sites.

For a fixed C4 warp, the finite smooth expansion through order h^2 has
connection residual O(h^3) in sup norm. The same inverse and contraction
give a correction O(h^3); hence the pointwise O(h) conclusion in (14)
persists. The super-algebraic owner-sum statement (4) uses the C-infinity
realization and is not inferred from C4 regularity.

## 7. Numerical controls on the same fixed curved metric

The optional [probe](experiments/a4d_warped_designated_response_probe.py)
retains all 24L connection variables and differentiates the literal
plaquette action. The metric derivative uses the genuine local Gram lift
`delta S=S Q^(-1) delta Q/2`, with K held fixed. The
[ledger](experiments/a4d_warped_designated_response_results.json) records
the result at the same epsilon=1/50 in (1):

| L | full connection residual, sup | `h^-2 E_Q[00](0)` | largest error against (13) |
|---:|---:|---:|---:|
| 8 | 8.70e-16 | -0.7509047312 | 0.0386636209 |
| 12 | 6.67e-16 | -0.7722106427 | 0.0173577094 |
| 16 | 6.00e-16 | -0.7797702644 | 0.0097980876 |
| 24 | 4.57e-16 | -0.7852027160 | 0.0043656361 |
| 32 | 5.27e-16 | -0.7871105281 | 0.0024578240 |

The independently specified target vector is

\[
f''(0)(-1,0,0,0,0,0,0,\tfrac12,0,\tfrac12),\qquad
f''(0)=0.7895683520871487\ldots.
\]

These are floating-point controls, not interval-validated roots. Neither
the exact existence theorem nor the asymptotic remainder order is inferred
from this table. The conservative proof threshold in (10) is not claimed
to include L=8 or L=12. No candidate-dependent metric source is assigned.

## 8. Remaining scope of the joint microstructure task

This closes a genuine curved designated-sheet existence and response
problem, including intercell coupling and every frequency in its invariant
sector. In particular the previous curved continuation is no longer
supported only by Newton residuals at two meshes.

It does not close `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED` for
arbitrary joint-critical microstructures. The #232 quarter microstructure
varies in the three translations used here; it is outside X_L. The full
derivative about the same curved comparator still has the previously
certified high-frequency gap obstruction. To establish the task terminal,
one must control the response of existing transverse mixed joint fields
relative to this exact branch, under the independently prescribed source,
or construct the required joint counterexample. Their response cannot be
settled by uniqueness inside X_L or by redefining that source.

The new theorem supplies a proved exact curved comparator to that next
step. It does not promote a universal Einstein theorem, a new selector,
or a physical/BOOK claim. Keep #310 Draft / IN_PROGRESS.

The subsequent constant-coframe quarter owners through `d422070d` were
also consumed before publication. Their nonlinear frozen readout gain and
conditional correlation-null theorem complement the present exact curved
comparator. They still do not imply the required support restriction or
owner-sum bound for arbitrary transverse joint fields.

The v2 split and the newer first-slow/parabolic identity-sheet owners were
also read at `ae0285cc`. They sharpen local joint-symbol information but
do not supply the missing full variable-background inverse. In particular,
joint-symbol injectivity is not an inverse of the connection-only Hessian
with a freely discarded metric equation. Outside X_L, a projected range
solve at zero center must still be shown to satisfy the unselected center
equations exactly; an `O(h^infty)` center residual is not zero. The proof
here avoids this issue by inverting the square full connection system in
the invariant sector and then lifting its zero gradient to all sites.

Smallest remaining Target-D object: a finite-polynomial inverse together
with exact center compatibility for the actual full four-dimensional
connection operator at `K_h^sm(g)`. Target-U additionally requires the
varying-coframe response commutator on exact extra-center branches.

The subsequent [warped regular-quarter theorem]
(A4D_WARPED_QUARTER_REGULAR_RESPONSE.md) now addresses one part of
Target U. Its literal first-slow shared-link compatibility and the owned
real quadratic metric cone have no nonzero common amplitude near f=1.
Every regular integer-h four-phase envelope on a fixed sufficiently small
nonconstant warp is therefore flat to all orders relative to this
comparator, with the same owner-sum response agreement. This does not
cover nonanalytic or nonuniform exact center families, and its existential
coframe radius is not identified with the numerical epsilon=1/50 probe.

## Reproduction

```bash
python 02_REGISTRY/research/certificates/a4d_warped_designated_normal_rescue_check.py --expect 02_REGISTRY/research/certificates/a4d_warped_designated_normal_rescue_results.json
OPENBLAS_NUM_THREADS=1 python 02_REGISTRY/research/experiments/a4d_warped_designated_response_probe.py
```

The exact checker reconstructs its inverse from the literal frozen face
formula and then checks both full multivariate products. It uses NumPy
object arrays and rational arithmetic; no floating singular values enter
the certificate. The variable-coefficient and nonlinear conclusions are
the analytic proof above, not Lean formalizations.
