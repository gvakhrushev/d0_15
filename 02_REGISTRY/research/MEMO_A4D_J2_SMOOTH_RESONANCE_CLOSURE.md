# A4D naked star — fixed-realization local J² theorem

Task: `EXP-A4D-J2-SMOOTH-RESONANCE-CLOSURE`
Execution: PR #216, continuation of merged #201 and #208
Canonical baseline: `d9ae828a7d56ea9c28670d0c227a43b566b2504f`
Audited incoming PR head: `26d840ddcc73ca6aac9ff3cf6b57b1fa785bf143`
Status: **PARTIAL / full stationary-correspondence estimate unresolved**

## 0. Verdict and proof boundary

The coefficient is fixed:
\[
T_1^{[2]}=\tfrac14 E_\eta,\qquad E_\eta(J)=-2G(J).
\]
The target is therefore
\[
E_{\star,h}[g](x)=-\tfrac12G[g](x)+O(h)+O(h^\infty).
\tag{0.1}
\]
This memo proves the fixed smooth Fourier-tail lemma, the nonlinear normal-center
cancellation, a summable multilinear remainder estimate, and uniform IR
parametrix construction. A new exact certificate supplies the missing
constant-solder Hessian congruence and an explicit canonical IR gap.

**(0.1) is conditional for the actual stationary correspondence.** The one
remaining dynamical obligation is a **refinement-uniform normal rescue for the
full coupled connection equations over the slowly varying smooth background**,
with control of their metric response. Constant-background, individual-character
isolation/degree estimates alone do not supply this obligation.

Current task terminal:

```text
J2-SMOOTH-PARTIAL-CLOSURE
NAKED-STAR-J2-BLOCKED-UNIFORM-COUPLED-NORMAL-RESCUE
```

The preferred terminal `NAKED-STAR-J2-LOCAL-EINSTEIN-OPERATOR-CLOSED` is not reached.
No actual star counterexample to (0.1) is certified here. This is a missing
estimate, not a claimed nonlinear no-go.

The shrinking metric bumps and pairwise bump program in the incoming head are
superseded as the primary proof. Their derivations remain in Git history.
The diagonal source remains closed; no new orbit search is undertaken.

## 1. Evidence and exact assumptions

### 1.1 Owners

| Input | Owner and exact scope |
|---|---|
| Intrinsic nonlinear metric quotient | Merged #208; `Q=Theta eta Theta^T`, dressed metric-compatible links; genuine local-Lorentz quotient |
| Linear quadratic coefficient | Merged #201, `certificates/a4d_star_qr_einstein_detector_check.py`; **ten quadratic small-momentum coefficient matrices**, not equality of complete lattice symbols |
| Normal Einstein identity | `ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md` (E-NJET); arbitrary normal metric Hessians, stated Ricci convention, centered radius-two consistency |
| Exact constant flat branch | Selected star density has zero curvature at identity links; its connection variation telescopes for constant solder on the periodic carrier |
| Diagonal nonlinear rescue | Existing `certificates/a4d_j2_smooth_resonance_closure_check.py`; rational nondegenerate root for the declared sourced reduction and resulting cubic Puiseux branch |
| Entire constant-solder zero-phase block and canonical gap | New `certificates/a4d_j2_fixed_realization_ir_check.py`; symbolic identity for all 16 solder entries, exact Laurent coefficient bounds |
| Sampling/reconstruction | `ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`; actual framed sampler, not a finite sampler on an ordinary 2-jet |
| Corrected parabolic control | Live #202 full-transverse certificate `a4d_resolved_curved_stationary_e2_enlarged12_full_transverse_check.py`: the stored `e2_closed` matrices are Cayley transforms of `span{M2,M3,-J23}` with true complement `{K1,N2,N3}`. On `e2=(0,0,j,0,0,j,gamma,delta,0,delta,-gamma,0)` the full 24 Lorentz-link derivatives force `j=gamma=delta=0`; the older restricted `8+6` family is superseded as a full-stationarity claim. |

The old diagonal certificate freezes the reduced quartic polynomial and verifies
its sourced rational Newton contraction; it does not independently reconstruct
all of the original range elimination. This distinction is retained. Its
already accepted diagonal result is used without reopening the source.

### 1.2 The theorem's hypotheses

**H-REAL.** One fixed smooth periodic metric/solder realization is actually
sampled on the whole finite carrier. Solder stays nondegenerate; a compatible
smooth chart/section realizes the intrinsic metric quotient. At the observation
point use a metric-normal chart and the owner's response pairing and
reconstruction. A local radius-two sampler alone is not a global Fourier
realization. Changing coordinates must transport that geometric realization.

**H-STAR.** Use the selected naked star action, its actual finite-stencil
connection Euler equations and metric partial Euler response. Local exponential
link and Gram-section coordinates are analytic with no negative powers of `h`
in their dimensionless formulas. Apply `h^-2` only to the final metric response.
The genuine gauge quotient is fixed before taking normal complements.

**H-IR.** On each compact nondegenerate constant-solder parameter family, the
connection symbol has an analytic inverse in a fixed complex neighborhood of
zero phase. Section 3 proves this from the new exact congruence. No bound uniform
up to degenerate solder, or over an unbounded family, is asserted.

**H-NORMAL-RESCUE (OPEN).** For the actual sampled smooth backgrounds, all small
exact stationary sheets in the specified flat-approaching neighborhood admit
normal estimates relative to the smooth approximate sheet and its genuine flat
moduli, uniformly in refinement and in all coupled resonant variables. There
is at least one such sheet. The estimate must also control the metric response;
physical tangent flat moduli may not silently be discarded as gauge. Section 8
states a sufficient quantitative contract.

H-REAL and H-STAR specify what object the theorem concerns. H-IR has an exact
finite owner plus the analytic argument below. H-NORMAL-RESCUE is the single
unproved dynamical bridge. The analytic lemmas here do not count as Lean owners
or a release promotion.

## 2. Choose the realization once; smooth tails and aliasing

Use `T^4=(R/2pi Z)^4`, with mesh `h=2pi/L`. On the unit-period convention replace
`hn` by `2pi hn`; all estimates and geometric normalization transform together.
For a normal 2-jet let
\[
q(y)=\chi(y/\rho)P_J(y),\qquad
P_J(y)=\tfrac12J_{ab,cd}y^cy^d.
\tag{2.1}
\]
Here `rho>0` is chosen once, independently of `h`. Small fixed support keeps
`eta+q` Lorentzian and places the realization in the analytic metric section.
There is no small-curvature restriction on the prescribed finite jet.

Define
\[
a=\|q\|_{W^0}=\sum_n\|\widehat q_n\|,
\qquad b_k=\sum_n |n|^k\|\widehat q_n\|.
\tag{2.2}
\]
For a fixed compact smooth bump profile in four dimensions, rescaling its Fourier
transform and summing Schwartz bounds gives
\[
a\le C_J\rho^2,\qquad b_k\le C_{J,k}\rho^{2-k}
\]
for `0<rho` in a fixed small interval. Thus `a` can meet a fixed analytic radius,
while every `b_k` is finite after `rho` is chosen. Large derivative constants
are allowed; they do not vary with refinement.

**Fourier-tail lemma.** Smoothness gives
`||qhat_n|| <= C_s(1+|n|)^(-s)` for every `s`. Summing over `Z^4`, with `s>M+4`,
\[
\sum_{|hn|\ge\theta_0}\|\widehat q_n\|
\le C_s\sum_{|n|\ge\theta_0/h}(1+|n|)^{-s}
\le C'_s h^{s-4}=O(h^M).
\tag{2.3}
\]
Since `M` is arbitrary, this is `O(h^infty)` in the **sum norm**, not just for a
single resonant Fourier coefficient.

The sampled coefficient is exactly
\[
\widehat q^{(L)}_k=\sum_{\ell\in\mathbb Z^4}\widehat q_{k+L\ell}.
\tag{2.4}
\]
For a principal lattice character whose phase is separated from zero, every
alias representative has frequency at least `c/h`. Summing the absolute alias
coefficients uses each continuum frequency once and is bounded by (2.3).
Hence aliasing preserves the sum estimate. The same argument applies with any
fixed polynomial weight.

If `||u_h|| <= C h^-p ||s_h||^beta` with fixed `beta>0` and `s_h=O(h^infty)`, then
`u_h=O(h^infty)`: for any desired power `K`, choose the source estimate with
`M>(K+p)/beta`. The final `h^-2` normalization also preserves this property.
The missing issue is obtaining this estimate for the actual coupled solve.

## 3. Uniform IR gap around every constant metric/solder

Let `E` be the matrix of constant internal solder vectors, `v_r=E e_r`, and let
`H_E(theta)` be the polarized `24 x 24` Lorentz connection block. The certificate
uses the mixed amplitude block; the Euler equation uses its transpose. All
singular-value estimates below hold for either convention.

At standard solder the new certificate proves
\[
\det H_I(0)=256,\qquad
\operatorname{spec}(H_I(0)^TH_I(0))=\{1^{(16)},4^{(8)}\}.
\tag{3.1}
\]
For every real phase, entrywise Laurent coefficient sums give
\[
\|\partial_{\theta_j}H_I(\theta)\|_F\le6.
\]
Consequently
\[
\sigma_{\min}H_I(\theta)\ge1-6\|\theta\|_1\ge\tfrac12
\quad(\|\theta\|_1\le1/12).
\tag{3.2}
\]
This concerns the full polarized block; a chiral decomposition is unnecessary.

The all-parameter polynomial identity checked by the certificate is
\[
(E^T\otimes I_6)^T H_E(0)(E^T\otimes I_6)=\det(E)H_I(0).
\tag{3.3}
\]
It follows by the alternating four-solder contraction of the homogeneous
commutator term. If `E` is invertible, put `P=E^-T tensor I_6`. Then
\[
H_E(0)=\det(E)P^TH_I(0)P,\qquad
\sigma_{\min}H_E(0)\ge\frac{|\det E|}{\|E\|_2^2}.
\tag{3.4}
\]
On any compact `K` of nondegenerate constant solders the lower bound has a
positive minimum `mu_K`. Laurent coefficients are polynomial in the solder
entries; their first phase derivatives have a finite common bound `D_K`.
A fixed phase ball of radius less than `mu_K/(2D_K)` has inverse norm at most
`2/mu_K`. Continuity of the finite Laurent symbol gives a smaller **complex**
phase neighborhood with the same type of bound. This supplies analytic inverse
symbols, uniformly over `K`.

Local analytic Gram sections give the corresponding statement for constant
metric parameters. Covering any compact metric parameter set by finitely many
sections suffices. There is no legitimate single constant uniform on the whole
noncompact Lorentz cone. Genuine gauge verticals are removed by this section;
(3.1) has no residual zero-phase kernel in its 24 coordinates.

## 4. Analytic IR construction and its exact limitation

### 4.1 A low-phase ball is not a convolution algebra

Translation invariance gives output phase
`theta_out=sum theta_i` modulo the reciprocal lattice. During nonlinear
elimination, every internal subtree has its own partial sum. A bound
`|theta_i|<theta_0` for each input does **not** keep these sums in the regular
ball for arbitrary `m`.

The correct common analytic germ is
\[
\mathcal D_m=\{(\theta_1,\ldots,\theta_m):
                    \sum_i\|\theta_i\|_1<r\},
\tag{4.1}
\]
with `r` inside the complex inverse neighborhood of Section 3. Every subtree
sum then lies in that neighborhood. Claiming a full exact stationary branch
analytic on the fixed product ball for all `m` would require a separate theorem.
The existing UV resonance does not supply one.

### 4.2 A proof parametrix with uniform Wiener radius

Write the literal connection equation in a section about constant solder as
\[
\mathcal F_h(A,q)=H_hA+N_h(A,q).
\]
`D_A N_h(0,0)=0`. Finite shifts are isometries of `W^0`; finite-dimensional
analytic exponentials and Gram sections act analytically on its Banach algebra.
Their estimates, and those of `N_h`, are independent of the mesh.

For analysis choose a smooth real even phase cutoff `phi` supported entirely
inside the inverse neighborhood and equal to one on a smaller fixed ball. Set
\[
B_h(\theta)=\phi(\theta)H(\theta)^{-1}
\]
there, extended by zero. Its Fourier multiplier norm on `W^0` is uniformly
bounded. The analytic contraction/implicit theorem solves
\[
A_h^{\rm IR}(q)=-B_h N_h(A_h^{\rm IR}(q),q)
\tag{4.2}
\]
for `a<R_K`, with a radius independent of `h` and uniform on `K`. At any constant
metric in that radius, `A_h^IR=0` exactly. The same construction about each
constant metric covers the compact family.

The variable `A` is the dimensionless logarithm of a Lorentz link. For a
fixed smooth realization the physical connection scale is `omega_h=A_h^IR/h`.
Constant-field vanishing and the same sum-domain estimate as Section 6 give
\[
\|A_h^{\rm IR}/h\|_{W^0}
\le\frac{C b_1}{R(1-a/R)^2}.
\]
More generally `||A_h^IR/h||_(W^k)` is bounded by
`C b_(k+1) sum_(m>=1) R^-m m^(k+1) a^(m-1)` (with the zero-order norm
included when defining an inhomogeneous weight). This is finite for the fixed
smooth field. Thus the analytic **input radius** is mesh-independent in
`W^0`, and the correctly rescaled connection obeys uniform tame derivative
bounds. No uniformly bounded map from arbitrary `W^0` fields to the physical
connection in `W^0` is asserted; one derivative of the input is needed.

Equation (4.2) is a **proof-only approximate solve**. It is not a filter in the
physical action and is not asserted to be an exact full stationary connection.
Indeed its literal residual is
\[
r_h=\mathcal F_h(A_h^{\rm IR},q)=(1-\phi)N_h(A_h^{\rm IR},q).
\tag{4.3}
\]
It must be removed by H-NORMAL-RESCUE before a physical conclusion is drawn.

The Banach analytic coefficients have bounds `C R^-m` after shrinking `R` to
absorb the polarization constants. Evaluating coefficients on single Fourier
characters gives symmetric multilinear kernels with the same bounds. Weighted
convolution uses
`(sum_i |n_i|)^k <= m^(k-1) sum_i |n_i|^k`.
Thus for fixed smooth `q` the series is bounded in every `W^k`, uniformly in
`h`: the extra `m^k` is summable against `(a/R)^m`. Applying (2.3) to (4.3) gives
\[
\|r_h\|_{W^0}=O(h^M)\quad\text{for every }M.
\tag{4.4}
\]
The argument may be performed on continuum Fourier series with the periodic
multiplier `B(hn)` and then sampled. Periodicity of that multiplier makes
sampling commute with it, so this proof does not presume an alias-free product.

### 4.3 Symbols of the metric response

Use the actual **partial metric Euler response** at `A_h^IR(q)`, before `h^-2`
normalization, rather than declaring the approximate connection on shell.
It has the uniformly convergent analytic expansion
\[
\mathcal R_h^{\rm IR}[q]=\sum_{m\ge1}\mathcal R_h^{(m)}[q,\ldots,q].
\tag{4.5}
\]
Translation invariance gives
\[
\mathcal R_h^{(m)}(x)=
\sum_{n_1,\ldots,n_m}e^{i(\sum n_i)\cdot x}
T_m(hn_1,\ldots,hn_m)[\widehat q_{n_1},\ldots,\widehat q_{n_m}].
\tag{4.6}
\]
Real-phase kernels are bounded by `C R^-m`. On `D_m`, all inverse factors and
all finite shifts are analytic, so these are the genuine IR formal elimination
kernels, independent of how the proof cutoff was extended. They depend
analytically on the local constant metric/solder parameter. This is the
correct uniform analytic IR statement; exact stationary UV sheets can remain
multivalued and nonanalytic.

## 5. Constant branch and nonlinear normal-center locality

For every sufficiently small constant symmetric `c`, identity links give
\[
\mathcal R_h^{\rm IR}[c]=0.
\]
Differentiating along `t c` at `t=0` shows
`T_m(0,...,0)[c,...,c]=0`. Since the Volterra kernels are symmetrized Fréchet
coefficients, polarization proves
\[
T_m(0,\ldots,0)=0\quad\text{as an }m\text{-linear map},\qquad m\ge1.
\tag{5.1}
\]
This argument does not assert separate vanishing of unsymmetrized summands.

Taylor-expand on (4.1) through total phase degree two. Each polynomial
monomial `prod_j theta_j^alpha_j` becomes a local product of derivatives
`prod_j partial^alpha_j q`; constant tensor contractions do not change its
derivative allocation.

At a normal center `q(x)=0`, `partial q(x)=0`. For `m>=2` and
`sum_j |alpha_j|<=2`, either some factor has order zero, or `m=2` and both
factors have order one. The first case contains `q(x)=0`; the second contains
two first derivatives. Thus every such product vanishes. Equivalently the
only possibilities beyond degree zero are
\[
q^{m-1}\partial q,\qquad
q^{m-1}\partial^2q,\qquad
q^{m-2}(\partial q)^2.
\]
Therefore
\[
T_m^{[\le2]}[q,\ldots,q](x)=0\quad(m\ge2).
\tag{5.2}
\]
For `m=1`, degree zero is zero by (5.1), degree one vanishes at the normal
center, and degree two is precisely the ten-coefficient #201 owner. E-NJET
therefore gives the leading reconstructed value `-(1/2)G(J)`.
This proves nonlinear locality of the low-degree differential polynomial;
it does not by itself estimate the full nonlinear response.

## 6. Full summed IR remainder for a fixed realization

A Cauchy estimate along the radial complex phase variable on (4.1) gives
\[
\|T_m(\theta)-T_m^{[\le2]}(\theta)\|
\le C R^{-m}\Big(\sum_j\|\theta_j\|_1\Big)^3
\tag{6.1}
\]
when that sum is sufficiently small. Uniform real-phase bounds extend the
same type of estimate to the complementary region: there the sum is bounded
below by a fixed positive number, and the degree-two polynomial is bounded
by `C R^-m(1+S+S^2) <= C' R^-m S^3`. Use unwrapped frequencies for `S`; the
actual symbol remains periodic. Cauchy constants are independent of `m`
because every phase tuple is scaled inside the same sum domain.

Using `(sum |n_i|)^3 <= m^2 sum |n_i|^3`, the **complete** normalized remainder is
\[
\begin{aligned}
\|R_{\rm IR}(h)\|
&\le Ch\sum_{m\ge1}R^{-m}m^3 b_3 a^{m-1}\\
&=\frac{Chb_3}{R}
  \frac{1+4t+t^2}{(1-t)^4},\qquad t=a/R<1.
\end{aligned}
\tag{6.2}
\]
All nonlinear orders have been summed; a linear single-frequency estimate
would not suffice. Constants depend on the fixed realization, hence on its
chosen support and derivatives, and never on `h`.

For any order `k`, tuples outside the analytic sum neighborhood also obey
\[
\sum_{h\sum|n_i|\ge r}\prod_i\|\widehat q_{n_i}\|
\le (h/r)^k m^k b_k a^{m-1}.
\tag{6.3}
\]
After summing in `m` and applying `h^-2`, their contribution is `O(h^infty)`.
This accounts for high total momentum generated by convolution, rather than
pretending the input IR ball is closed under multiplication.

Combining (5.2), (6.2), #201 and E-NJET yields for this proof parametrix
\[
h^{-2}\mathcal R_h^{\rm IR}[q](x)
=-\tfrac12G[g](x)+O(h).
\tag{6.4}
\]
The centered stencil's own `O(h^2)` consistency is compatible with this
conservative full remainder. No complete-symbol identity is used.

## 7. Arbitrary fixed smooth realizations: amplitude versus refinement

The small Wiener radius proves (6.4) for fixed bump realizations of every
normal jet. It must not be used to assert that an arbitrary global metric is
small relative to a constant one.

There is an alternative smooth approximate solve under H-REAL and H-STAR.
For the fixed smooth nondegenerate solder field insert a formal local series
\[
A_h^{\rm sm}=\sum_{j\ge1}h^j A_j[g]
\]
into the literal finite-stencil Euler equation. Expanding a shift of a smooth
field gives local differential coefficients. At order `h^j`, the unknown
`A_j` is multiplied by `H_{E(x)}(0)`; all other terms are already determined
by lower orders. The inverse in (3.4), uniformly over the compact image of
this one fixed solder field, determines `A_j` recursively. These coefficient
functions are smooth. This constructs a formal approximate solution, not an
exact stationary branch.

Choose smooth cutoffs on the successive terms with sufficiently fast shrinking
parameter support. The resulting asymptotic sum matches each finite truncation
in every fixed smooth seminorm. Taylor expansion of the finite shifts then gives
\[
E_K(Q_h,K_h^{\rm sm})=O(h^\infty).
\tag{7.1}
\]
This connection approximation can depend on `h`; the metric realization
remains fixed. Compatible solder charts must be glued using the actual finite
gauge transformation, as required by H-REAL.

The raw metric response coefficient at each order `h^j` is a local differential
expression of total derivative order `j`. At a normal center the terms through
order two have the same derivative allocation as Section 5, with coefficient
functions evaluated at `g(x)=eta`. Only the linear metric Hessian survives;
its coefficient is #201. Hence this smooth approximate sheet also has
\[
h^{-2}E_Q(Q_h,K_h^{\rm sm})(x)=-\tfrac12G[g](x)+O(h).
\tag{7.2}
\]
The recurrence/asymptotic-sum argument is an analytic lemma, not a finite
checker or Lean theorem. It addresses large global amplitudes for an admissible
fixed smooth realization. Turning (7.1) into an exact sheet remains precisely
H-NORMAL-RESCUE. Small residual at a singular equation is not an existence proof.

## 8. UV normal theorem: what a sufficient certificate must actually say

### 8.1 Finite normal-bundle lemma

For a compact parameter chart `P` of a resonance stratum, include the constant
metric parameter and bounded flat tangent moduli. In a genuine normal bundle
coordinate `v`, suppose the **full range-reduced** equation is
\[
F(p,v,s)=0,\qquad F(p,0,0)=0.
\]
Assume zero-source normal isolation on a common closed ball, no zeros on its
boundary, and nonzero normal Brouwer degree. The normal domain/codomain must
have matching dimension. Any remaining tangent Euler equations must already
be satisfied or included; deleting them is not a quotient.

Nonzero degree gives local existence for small sources. If the graphs and
normal distance are compact subanalytic and the entire zero set at `s=0` in
this tube is the flat bundle, applying the inequality to
`f(p,v)=||F(p,v,0)||`, `g(p,v)=||v||` gives
\[
\|v\|\le C\|F(p,v,0)\|^\beta.
\]
A uniform Lipschitz source perturbation then gives `||v|| <= C' ||s||^beta`
for every existing root. The constants are joint in the compact parameters;
a pointwise exponent is insufficient. This is the application of
[Bierstone–Milman, Theorem 6.4](https://www.numdam.org/item/PMIHES_1988__67__5_0.pdf).

A connected normal chart with boundary nonvanishing has constant degree.
An odd normal map has odd degree only if the involution genuinely acts as
`v -> -v` on that normal fiber and the boundary is zero-free. Those hypotheses
are not consequences of merely naming a Fourier resonance.

Isolation alone does not imply existence: `F(v)=v^2` has an isolated zero but
cannot solve a negative scalar source. The new certificate checks this hostile
inference control.

### 8.2 Why that finite lemma is not yet the full lattice theorem

The source reaching a resonant block is the residual **after smooth IR
elimination**, including all mode interactions. It is not automatically the
original `qhat_UV`. A per-character map omits resonant convolutions and its
regular complement can lose a gap at neighboring rank changes. Refinement
also increases the number of coupled variables. Applying a finite-dimensional
Łojasiewicz theorem at each `L` does not make its constants uniform in `L`.
For example `F_L(v)=v^(2L+1)` has isolated zero and degree one at every `L`;
the super-algebraic source `s_L=h^(2L+1)` still has the merely order-`h` root.

More sharply, isolation/degree at a constant background need not persist under
slow-background corrections. The analytic gradient model
\[
F_h(v)=v^3-hv,
\qquad V_h(v)=v^4/4-hv^2/2
\tag{8.1}
\]
has an isolated, odd degree-one zero at `h=0`, but at zero source and `h>0` it
has stationary sheets `v=0,+sqrt(h),-sqrt(h)`. All approach the same original
flat point; two do not obey `O(h^infty)`. The polynomial substitutions are
checked exactly in the new certificate using `h=t^2`.

(8.1) is a counterexample to the **inference**, not a proposed star action or a
certified star obstruction. It shows why a theorem for the full slowly varying
normal germ is needed, even after constant-family isolation is established.
An inequality measuring distance to all these zeros would not measure distance
to the designated flat sheet. They cannot be declared flat/gauge by definition.

### 8.3 Single open quantitative contract

Let `C_h={(Q,K):E_K(Q,K)=0}` for the unchanged naked star. Over each sampled
fixed smooth `Q_h`, let `K_h^sm` be the approximate sheet from Section 4 or 7,
with residual `r_h=O(h^infty)`. A sufficient H-NORMAL-RESCUE certificate proves:

1. The full equations have a flat-approaching exact sheet for this residual;
   all normal/tangent equations are accounted for.
2. Every exact sheet in a uniform specified normal tube satisfies, in a sum norm,
   \[
   d_\perp(K_h,\mathcal Z_h^{\rm sm})
       \le C h^{-p}\|r_h\|^\beta,\quad \beta>0,
   \tag{8.2}
   \]
   with constants uniform in `h`, coupled mode count, chart overlaps, the slow
   background, and compact metric/flat parameters. `Z_h^sm` denotes the
   designated smooth approximate fiber and its actual allowed flat moduli;
   it is not enlarged to contain arbitrary curved stationary roots.
3. Genuine gauge directions are identified. Any physical flat tangent moduli
   retained in that fiber have the same metric response up to `O(h^infty)`, or
   are controlled by an explicit estimate. For normal deviations the literal
   metric response has at worst polynomial sensitivity:
   \[
   \|E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{\rm sm})\|
       \le C'h^{-p'}d_\perp+O(h^\infty).
   \tag{8.3}
   \]

Finite-stencil analyticity gives local Lipschitz response bounds in a fixed
chart, but does not prove response independence along physical flat moduli.
A stationary correspondence is sufficient; no unique global connection is
required. Equations (8.2)–(8.3) and (4.4)/(7.1) give super-algebraic response
agreement after `h^-2`, on **all** the indicated sheets.

This is the single missing mathematical bridge. A certificate covering only
one isolated character or only the diagonal source does not prove it.

### 8.4 Parabolic control after the full-transverse replay

Live #202 now owns the omitted ambient Euler pressure exactly.  The stored
`e2_closed` matrices are Cayley transforms of
(operatorname{span}{M_2,M_3,-J_{23}}), so the true Lorentz complement is
({K_1,N_2,N_3}).  The previously supplied rows based on
({K_1,M_2,M_3}) were derivatives of a mismatched algebra base, not of the
stored matrices.

On the three-parameter sheet
[
e_2=(0,0,j,;0,0,j,;gamma,delta,0,;delta,-gamma,0)
]
the exact role-2/3 complement equations reduce to
[
gamma(j^2+4)-2j^2=0,qquad
gamma(j^2+4)+2j^2=0,
]
[
delta(j^2+4)+4j=0,qquad
delta(j^2+4)-4j=0.
]
Over the reals these force
[
oxed{j=gamma=delta=0.}
]
In particular, even the configuration line (gamma=delta=0) is not
stationary for (j
e0); one exact derivative is
(128j/(j^2+4)).

Thus this homogeneous parabolic sheet is a stronger finite control than the
earlier premise: its full-star stationary germ is isolated at the origin.
The matched-affine result remains independently useful: the old det/adj
residual is dormant on this rank-two parabolic sheet, so the selected
quadratic (I)-channels cannot repair the star Euler obstruction there.

This finite control still does **not** prove H-NORMAL-RESCUE.  Equation (8.1)
shows why: isolation on one constant homogeneous sheet does not exclude new
flat-approaching exact sheets created by slow-background corrections and
coupled resonant variables as (h	o0).

## 9. Conditional local Einstein theorem and extension independence

**Theorem.** Under H-REAL, H-STAR and H-NORMAL-RESCUE, with the IR lemma of
Section 3 and the owner's response normalization, each admissible fixed smooth
Lorentz realization, observation point, and metric-normal reconstruction has
\[
E_{\star,h}[g](x)=-\tfrac12G[g](x)+O(h)+O(h^\infty)
\]
on all stationary sheets in the certified flat-approaching neighborhood.

**Proof.** Section 6 supplies the approximate-sheet estimate for small fixed
realizations, and Section 7 supplies it for admissible arbitrary fixed smooth
realizations. The full rescue contract changes the normalized metric response
by `O(h^infty)`. Sections 5–6 and #201 leave exactly `1/4 E_eta` at a normal
center. E-NJET identifies that value with `-(1/2)G`. No new coefficient or
continuum equation is inserted. ∎

For two fixed realizations of the same local 2-jet, apply this theorem
separately. Their limits agree because both are `-(1/2)G(J)`. The error constants
may differ; each is fixed before refinement. This proves extension independence
as a corollary. A theorem for one preferred bump alone would not establish this
corollary for an arbitrary second global realization.

## 10. What follows after genuine metric-only closure

Once the theorem is proved for all admissible frames/grids and realizations
with the stated reconstruction, their limits are the same geometric `-(1/2)G`.
Frame/solder/grid erasure then follows by comparison. Equality for one preferred
normal sampler does not already certify erasure for a larger unexamined class.

For the resulting genuine smooth metric-only bundle map on `J^2 Met_(1,3)(T^4)`,
local diffeomorphism naturality follows from that of the geometric Einstein
operator and the existing framed pullback square. Contracted Bianchi gives its
covariant divergence directly. This does **not** certify the independent
same-object passage from finite Noether identities to covariant divergence;
that stronger internal argument keeps its own obligation.

The fixed-manifold [Navarro–Navarro formulation](https://arxiv.org/abs/1005.2386)
then packages the already identified operator in the four-dimensional Lovelock
span. It is not needed to search for a tensor or fit a coefficient here.
No matter equation, Newton normalization, or independent zeroth-order channel
is selected by this theorem.

## 11. Minimal worker certificate requests

These are specifications for CONTROL, not newly registered/delegated tasks.

| Request | Minimal reviewable evidence |
|---|---|
| One coupled normal-rescue owner | Actual full Euler/range reduction over the slow sampled background; designated flat fibers; normal sphere boundary bound and degree or another existence mechanism; joint normal inequality; uniform constants in lattice size and coupled mode count; tangent-response and range-complement estimates (8.2)–(8.3) |
| Parabolic hostile replay inside that owner | Missing ambient transverse Euler component(s), distinction of `j` from normals, denominator guards and compact range; verify the corrected control rather than the old restricted `8+6` result |
| Implementation replay of analytic lemmas | Reconstruct the finite-stencil equation and response normalization used by Sections 4/7, and verify their smooth residual. Generic Fourier/combinatorial lemmas need proof owners if formal promotion is later requested |

The IR finite gap/congruence request has been discharged in this PR. No new
diagonal Newton search, orbit inventory, finite-Sobolev optimization, separate
pairwise bump study, or tensor selector is requested.

## 12. Failure modes and final disposition

The precise ways the conditional inference can fail are:

- the true coupled normal system has no small stationary sheet for the smooth
  residual, despite a degree calculation on a restricted subsystem;
- slow-background or intermode coupling creates extra flat-approaching normal
  stationary germs, as the inference control (8.1) illustrates;
- constants/exponents or complement bounds deteriorate with refinement or at
  rank-changing chart boundaries;
- uncontrolled physical tangent flat moduli alter the metric response;
- the purported global realization or geometric reconstruction is not the
  actual finite sampled star object.

None is certified to occur for the star here. They are the explicit exclusions
required by the **one** full stationary-correspondence estimate.

**Proposed current terminal:**
`NAKED-STAR-J2-BLOCKED-UNIFORM-COUPLED-NORMAL-RESCUE`.

**Promotion condition:** only after (8.2)–(8.3), existence, and the actual
realization/reconstruction contract are owned may CONTROL accept
`NAKED-STAR-J2-LOCAL-EINSTEIN-OPERATOR-CLOSED`, with `E_star=-(1/2)G`.
There is no unconditional continuum Einstein claim in this PR.

## 13. Validation record

- New narrow certificate: 17 exact checks passed; arbitrary-solder identity is
  a polynomial calculation in all 16 independent entries.
- Independent comparison of the reconstructed full Laurent block with `HAB`
  from the merged polarized owner passed entry by entry. This verifies the
  BCH reconstruction uses the same selected symbol, beyond zero phase.
- Repository architecture, formalization debt non-growth, claim-strength lint,
  generated Lean views, work/protocol validation and their self-tests, generated
  work views, Python syntax and whitespace checks passed.
- No Lean/formalization source changed. No continuum theorem was promoted.
- Remote guards remain the acceptance evidence for the published head; local
  checks do not change the scientific terminal or turn the Draft into Ready.
