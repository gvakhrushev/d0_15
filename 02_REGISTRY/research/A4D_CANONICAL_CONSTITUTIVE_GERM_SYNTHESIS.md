# A4D: canonical constitutive germ and regular stationary response closure

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Research input: 4c5aec1de80a34e610951c35bd7504584aba2f8b; main input:
e80a3b1ccf615fb4f70bf5900181592604928497.

**Positive analytic result.** The unchanged full connection equations determine
one formal constitutive germ. More strongly, all exact mesh-stationary
connections in a fixed sufficiently small log chart with uniformly bounded
smooth $C^7$ extensions have the designated response in the original
normalized, unweighted owner sum, with error $O(h)$. No power series assumption
on those connections and no inverse of the full UV operator is needed.
Uniform bounds in every smooth seminorm give a super-algebraic gap.

This closes an explicitly regular response sector and the formal constitutive
law. It does **not** close the parent all-admissible microstructure theorem.
The native detector-to-response interface is kept separate below. No action,
source convention, parent admissibility predicate, Lean owner, or public claim
is changed. In particular, the mandatory #232 response-null UV control is
not declared inadmissible.

## 1. Inputs that the assembly actually uses

| Input | Contribution | Boundary retained |
|---|---|---|
| [#216 smooth realization](MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md), §§3,5,7 | All-solder zero-phase inverse, formal recurrence, Borel comparator, normal-$J^2$ allocation | Borel residual is not an exact zero |
| [All-solder checker](certificates/a4d_j2_fixed_realization_ir_check.py) | Generic sixteen-parameter polynomial congruence; determinant 256; squared singular values $1^{16},4^8$ | No full UV inverse |
| [Direct Schur identification](certificates/a4d_schur_einstein_direct_identification_check.py) | Independent standard Einstein reconstruction, all 100 quadratic polynomial entries | Raw/reconstructed index and sign conventions remain typed |
| [ObservableCompletionCanonicity](../../03_FORMALIZATION/D0/Foundation/ObservableCompletionCanonicity.lean) | Nonempty constant-readout class implies M1 forcing | Constancy must first be proved |
| [Exact curved rescue](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md) | Nonempty exact connection-stationary class on the cosine warp | Its stage source is an output, not exactly sampled continuum data |
| [Fixed-source compatibility](A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md) | No exact full joint root for the declared continuum Einstein samples on that warp | Source infeasibility is not a response-gap NO-GO |

Use the physical Euler orientation. Write
$B_E=H_E(0)^T$, where the polarized coefficient owner calls its block $H_E$.
The generic identity is

\[
(E^T\otimes I_6)^T H_E(0)(E^T\otimes I_6)=\det(E)H_I(0),
\qquad \det H_I(0)=256.
\tag{1}
\]

At zero phase the block is symmetric, so $B_E=H_E(0)$ there. This does not
permit exchanging the corrected nonzero-phase physical Euler and polarized
symbols. For one fixed smooth nondegenerate solder, compactness gives

\[
\sigma_{\min}B_{E(y)}\ge \frac{|\det E(y)|}{\|E(y)\|_2^2}\ge\mu>0.
\tag{2}
\]

The analysis takes place in one owned H-REAL section, with the H-STAR finite
analytic formula. The physical Lorentz links are $U_r=\exp A_r$, not an
arbitrary dressed matrix asserted to be $\eta$-Lorentz.

## 2. The positive comparison theorem

Let $h=1/L$, $L\in4\mathbb N$, and fix the smooth periodic solder $E(y)$ on
$\mathbb T^4$ once. Keep the original finite action and every shared-link
Euler row. Let $B_h(y)=A_h^{\rm sm}(y)$ be the #216 smooth asymptotic sum:

\[
\|B_h\|_{C^j}=O(h),\qquad F_h(B_h)=O(h^\infty)
\quad\hbox{in every fixed }C^j.
\tag{3}
\]

Here $F_h$ is the continuous extension of the literal finite-stencil Euler
formula: evaluate the same expression at $y+h s$ for its finite, fixed set
of integer offsets $s$. On the mesh it is exactly the physical $E_K$.

**Theorem.** There is $\delta>0$, depending on the fixed solder and local
analytic chart, such that the following holds. Fix an integer $R\ge1$ and
a family of periodic log extensions $A_h:\mathbb T^4\to\mathbb R^{24}$ with

\[
\|A_h\|_{C^0}\le\delta,\qquad \|A_h\|_{C^R}\le M_R.
\tag{4}
\]

Define the mesh Euler error
$e_h=\max_x|F_h(A_h)(hx)|$. For all sufficiently small $h$,

\[
\|A_h-B_h\|_{C^0}\le C_R(e_h+h^R),\qquad
h^{-2}\|\Xi(A_h)-\Xi(B_h)\|_{\rm owner,1}
\le C_R(h^{-6}e_h+h^{R-6}).
\tag{5}
\]

Constants are independent of the mesh population. Thus exact sampled
stationarity and $R=7$ give the original raw response gap $O(h)$.
No convergence of $A_h$ to zero is assumed: (5) implies it for exact regular
roots. If all $C^R$ norms are uniformly bounded and $e_h=O(h^\infty)$, both
differences in (5) are $O(h^\infty)$. Every exact regular root is included.

Existence of extensions with the bounds in (4) is a genuine hypothesis.
A mesh field is not regular merely because a smooth interpolant exists at
each individual mesh. The constants must remain bounded under refinement.

### 2.1 Sampled zeros control the off-grid residual

For a periodic $C^R$ vector function $f$ and $0\le j<R$,

\[
\|f\|_{C^j}\le C_{R,j}\left(
h^{-j}\max_x|f(hx)|+h^{R-j}\|f\|_{C^R}\right).
\tag{6}
\]

To prove this, Taylor-expand at an arbitrary observation point $y$ through
total degree $R-1$. Choose $R$ consecutive nearby mesh nodes in each
coordinate, in a local periodic lift. Their scaled coordinates are
$k-a$, with $k_i=0,\ldots,R-1$ and $a_i\in[0,1]$.
The rescaled Taylor polynomial

\[
p_y(z)=\sum_{|\beta|<R}
\frac{h^{|\beta|}\partial^\beta f(y)}{\beta!}z^\beta
\]

has values at these nodes bounded by
$\max_x|f(hx)|+C_R h^R\|f\|_{C^R}$. Its degree in each coordinate is
at most $R-1$, so tensor Lagrange interpolation reproduces it exactly.
Derivatives of the scaled basis at zero are uniformly bounded for
$a\in[0,1]^4$. This bounds
$h^{|\beta|}|\partial^\beta f(y)|$ by the same quantity, proving (6).
Only total derivatives through order $R$ occur in the Taylor remainder;
using a tensor node set does not require $4R$ derivatives.
A total-degree Newton simplex node set gives the same conclusion.

The finite analytic formula and (4) bound $\|F_h(A_h)\|_{C^R}$ uniformly.
Applying (6) and subtracting (3), with
$r_h=F_h(A_h)-F_h(B_h)$, gives

\[
\|r_h\|_{C^j}\le C_R(h^{-j}e_h+h^{R-j})+O(h^\infty),
\quad 0\le j<R.
\tag{7}
\]

An equation that vanishes only on nodes has not been differentiated as an
off-grid identity; (6) supplies precisely the missing estimate.

### 2.2 A finite inverse identity replaces the full UV inverse

Put $D=A_h-B_h$. The exact mean-value formula for the local stencil is

\[
r_h=\sum_s C_{h,s}(y)\,D(y+h s),\qquad
M_h(y)=\sum_s C_{h,s}(y).
\tag{8}
\]

The matrices are averaged local derivatives along $B_h+tD$, $0\le t\le1$.
Their $C^j$ bounds, $j\le R$, are uniform. At zero links and zero mesh their
sum is $B_{E(y)}$. Smooth dependence and the fixed smooth solder imply

\[
\|M_h-B_E\|_{C^0}\le C(\delta+h).
\tag{9}
\]

Choose $\delta$ and then $h$ so that this is less than $\mu/2$.
$M_h$ is pointwise invertible; $M_h^{-1}$ has uniform $C^j$ bounds: differentiate
$M_hM_h^{-1}=I$ and use the uniform coefficient bounds. This is not an
inverse of an operator on arbitrary mesh vectors.

Define

\[
\mathcal D_h=M_h^{-1}\sum_s C_{h,s}(T_{h s}-I),\qquad
T_{h s}D(y)=D(y+h s).
\]

The integral shift formula gives
$\|\mathcal D_h w\|_{C^j}\le C_jh\|w\|_{C^{j+1}}$.
Equation (8) is exactly
$D=M_h^{-1}r_h-\mathcal D_hD$. Iterate this identity only $R$ times:

\[
D=\sum_{n=0}^{R-1}(-\mathcal D_h)^nM_h^{-1}r_h
  +(-\mathcal D_h)^R D.
\tag{10}
\]

No infinite Neumann series or UV contraction is being claimed.
Each term loses at most $n$ derivatives and gains $h^n$. Consequently

\[
\|D\|_{C^0}\le C_R\left(
\sum_{n=0}^{R-1}h^n\|r_h\|_{C^n}
+h^R\|D\|_{C^R}\right)\le C_R(e_h+h^R).
\tag{11}
\]

The site response is uniformly Lipschitz in its fixed number of nearby
log-link coordinates on this chart. There are $L^4=h^{-4}$ sites and ten
slots. Thus the final $h^{-2}$ normalization costs $h^{-6}$, proving (5).
The loss in #226 has been retained and overcome by (10), not dropped.

### 2.3 The exact class is nonempty on the owned curved warp

The existing invariant rescue provides $A_h^*$ with all full $E_K$ rows zero
and mesh difference $A_h^*-B_h=O(h^\infty)$ in sup norm. Interpolate that
mesh difference by a real trigonometric polynomial and add it to $B_h$.
The $C^j$ norm of the interpolant costs only a polynomial factor in $L$:
a bound $C_jL^{4+j}\max_x|A_h^*(x)-B_h(hx)|$ suffices.
It remains super-algebraic for every fixed $j$.
This gives uniformly regular extensions of an actual exact curved root.

Hence the theorem is not solely about an empty class or a formal object.
It compares every other regular exact connection root on this warp with
that response. The exactly sampled continuum Einstein source still has
no joint root, by the separate arithmetic theorem.

## 3. Canonical constitutive law before choosing a finite candidate

Interpret shifts formally as $\exp(hs\cdot\partial)$ and seek
$A^{\rm can}=\sum_{j\ge1}h^jA_j$. At each order,

\[
[h^j]F_h(A^{\rm can})
=B_EA_j+P_j[E;A_1,\ldots,A_{j-1}].
\tag{12}
\]

Equation (2) constructs $A_j=-B_E^{-1}P_j$. Two formal roots first differing
at order $m$ would satisfy $B_E(A_m-A'_m)=0$; hence the entire formal germ
is unique. Its finite stationary jet spaces are nonempty singletons.
Truncation maps compose exactly, and their leading response readout
$[h^2]\Xi$ commutes with truncation on levels retaining the required
coefficients, for example stationary jet orders $N\ge2$.

Every uniformly $C^\infty$-bounded stationary completion in the small chart
has this germ by (5), even when no expansion was initially assumed.
Different smooth extensions and different Borel sums give the same
response germ, with super-algebraic agreement in the original raw norm.
Super-algebraic $C^0$ agreement and uniform bounds in all higher seminorms
also imply agreement in each fixed $C^j$ seminorm by smooth interpolation.

Define, as a universal formal functional of the declared solder,

\[
\tau^{\rm can}[g](h)=h^{-2}\Xi(g,\exp A^{\rm can}[g])
=\rho_0[g]+h\rho_1[g]+h^2\rho_2[g]+\cdots.
\tag{13}
\]

This functional is determined by the action and (12), before consulting
an arbitrary exact finite root. Substituting $A^{\rm can}$ into the formal
action gives a formal effective action whose metric derivative is $\Xi$.
Multiplying that action by $h^{-2}$ gives the source normalization (13);
an integrated density also retains its declared volume factor.
The formal chain-rule connection term vanishes because $F_h=0$
coefficientwise. For coefficients involving derivatives, use formal
integration by parts, with the adjoint shift $\exp(-hs\cdot\partial)$.
There is no independent correction law to tune.

At an owned normal metric center $g=\eta$, $dg=0$, the derivative-allocation
theorem eliminates all nonlinear terms through order two. The remaining
linear metric Hessian is exactly the Schur coefficient
$K_{\rm Schur}=-K_G^{(1)}/2$. With the existing reconstruction,
$\rho_0$ is $-G[g]/2$. This identifies the natural leading tensor and its
continuum Bianchi identity. Higher coefficients retain stencil data;
their diffeomorphism naturality has not been proved.

The class of smooth approximate completions is constructively nonempty
by (3), and its response germ is constant by (5). These are the actual
premises needed to apply the existing observable-canonicity theorem.
M1 forcing is thereby valid for this stated completion class.
It is not asserted for the full native detector class without a bridge.
Gauge comparison must use the actual finite action transformation owner,
[the nonlinear Lorentz quotient](MEMO_A4D_STAR_DENSITY_LORENTZ_NONLINEAR_QUOTIENT.md),
not merely the narrower Lean Gram/endpoint-link invariance file.

## 4. Native κ architecture and the source-lift distinction

BOOK_02 §02.13.5 uses $A_k=B+C_k+r_k$, with $C_k$ fixed by a whole
pro-family rule and a controlled residue. The constitutive recurrence
provides precisely a correction rule without free coefficients:

\[
h^{-2}\Xi=\rho_0+C_h^{(N)}+r_h^{(N)},\quad
C_h^{(N)}=\sum_{j=1}^N h^j\rho_j,\quad
r_h^{(N)}=O(h^{N+1}).
\tag{14}
\]

This is a valid formal implementation of that structure. Identifying it
with native detector levels requires actual operator/response descent.
Bratteli depth, Role period $L$, and jet truncation order are different
indices. The owned $\phi$ scale ratio does not identify their bonding maps.
The condensed operator-naturality owner transfers a *supplied* intertwining
family; it does not construct the missing gravitational family.

For the cosine warp, with $p=f'$, $q=f''$, the forced first coefficient is

\[
\rho_1=(3pq/2,0,0,0,-pq/2,p^3/(2f),p^3/(2f),0,0,0),
\qquad Q:\rho_1=2pq=\partial_{y_1}(p^2).
\tag{15}
\]

It is nonzero locally, while its trace sum vanishes on each allowed mesh.
It is a structural coefficient, not a fitted counterterm.

**All finite source truncations are still infeasible on that warp.**
Here the coefficients use the original diagonal solder section and
$y$-coordinate stencil; a normal recharting or a Borel cutoff is not part
of their definition. The coefficient $A_j$ is homogeneous of total
derivative weight $j$; $\rho_j$ has weight $j+2$. A product carries the sum
of the orders of its derivative factors. This grading follows from (12):
each Taylor shift adds equal powers of $h$ and differentiation, and the
zero-phase inverse has weight zero. The naked formula has no other
explicit mesh dependence. All numerical coefficients
are rational and sampled solder inverses are algebraic. At cyclotomic mesh
points an $m$th derivative of $f$ is $\pi^m$ times an algebraic number.
Therefore an exact source prescribed by any finite truncation would force

\[
h^2\sum_x Q_h:\sum_{j=0}^N h^j\rho_j
=\sum_{j=0}^N b_{j,L}\pi^{j+2},\qquad
b_{0,L}=L^2/1250\ne0,\quad b_{j,L}\in\mathbb R_{\rm alg}.
\tag{16}
\]

A nonconstant polynomial in $\pi$ over algebraic numbers is transcendental.
Every full stationary critical action value for this algebraic sampled
coframe is algebraic. Thus (16) cannot be an exact joint source.
More terms in a finite expansion cannot solve the stage-realization problem.
An exact stage functional can nevertheless have this asymptotic germ;
the already owned exact invariant warp root demonstrates that possibility.

$\pi_0=(6/5)\phi^2$ is the structural algebraic phase constant.
Replacing the derivative $\pi^2$ by $\pi_0^2$ on the same cosine metric
leaves a fixed mismatch in the stationary trace limit; replacing the
cosine phase as well loses one-periodicity. Neither operation supplies a
source lift. Arbitrary Borel representatives also retain flat-in-$h$
freedom; formal uniqueness does not make every such finite representative exact.

**The exact-source bridge also fails generically, without arithmetic.**
[The general feasibility theorem](A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md#8-generic-exact-source-infeasibility-without-arithmetic-hypotheses)
shows that a residual set of fixed smooth metrics in every open
neighborhood has no real full-Lorentz joint root on any mesh for its
exactly sampled continuum Einstein source. At fixed node values the
polynomial action has finitely many critical values; a metric two-jet
perturbation preserves those samples and changes the source trace.
Thus no universal exact realization assignment on an open smooth family
can implement the native response bridge. Formal germ uniqueness and
the proved asymptotic measurement theorem remain valid. The exceptional
parent source-image implication is still open.

### 4.1 The golden residue has enough decay for the original four-dimensional owner sum

There is a useful quantitative synthesis of the two constants, without
changing the source, comparator or norm. The scale is
$h_n=h_0\phi^{-n}$; $\phi$ itself is fixed. The scalar formula
$\phi_{n+1}=\phi_n+1$ is not a refinement identity. The owned identities
are the scale step in
[PhiDiscreteRG](../../03_FORMALIZATION/D0/Bridge/PhiDiscreteRG.lean)
and the Fibonacci/Perron recurrence in
[FibonacciAFTower](../../03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean).

The closure balance for $\pi_0$ supplies

\[
 \delta_0=\frac{3}{5\pi_0\phi}=\frac1{2\phi^3},
 \qquad
 \boxed{\phi^4\delta_0=\frac{\phi}{2}<1.}
 \tag{G1}
\]

Thus a golden residue for the **normalized metric response** would
outpace the growth of the four-dimensional site count. This is more
than an assertion that a ladder has a limit: it fixes the exact decay
budget needed for this owner's raw norm.

Here is the complete implication, with the missing premise visible.
For every allowed mesh put

\[
 n(h)=\left\lfloor\log_\phi\frac{L}{4}\right\rfloor,\qquad h=L^{-1},
 \qquad
 D_h(y)=\tau(y)-h^{-2}\Xi_h^{\rm sm}(y).
\]

The comparator has its owned continuous finite-stencil extension.
For exact joint roots, $h^{-2}(\Xi-\Xi_{\rm sm})(x)=D_h(hx)$
by the prescribed source equation; no extension or derivative bound
of the unknown connection is involved. If native response descent
proves the single uniform estimate

\[
 \sup_{\substack{L\in4\mathbb N\\ n(1/L)=n}}
     \|D_{1/L}\|_{C^0,\mathrm{packed},1}
 \le C\delta_0^n
 \quad\text{on every realizable fixed-source pair},
 \tag{G2}
\]

then the unchanged full owner sum obeys

\[
 \begin{aligned}
 h^{-2}\|\Xi-\Xi_{\rm sm}\|_{\mathrm{owner},1}
 &\le L^4\|D_h\|_{C^0,\mathrm{packed},1}\\
 &\le C(4\phi)^4(\phi^4\delta_0)^{n(h)}
 =C(4\phi)^4(\phi/2)^{n(h)}\longrightarrow0 .
 \end{aligned}
 \tag{G3}
\]

This covers all admitted meshes, not just a selected subsequence.
Equivalently the rate is $O(h^\gamma)$ with
$\gamma=\log_\phi 2-1>0$. It is a $C^7$-free sufficient
closure estimate for the original response object. It would force
precisely the fixed-source comparator jet gate already proved in the
[end-to-end owner](A4D_SOURCE_IMAGE_END_TO_END_ATTEMPT.md#2-the-complete-logical-endpoint);
it does not evade that gate.

A compatible, calibrated response-error family with consecutive
sup-norm increments bounded by $C\delta_0^n$ has a tail bounded by
$C\delta_0^n/(1-\delta_0)$, by the actual
[golden Cauchy owner](../../03_FORMALIZATION/D0/Geometry/GHPGoldenCauchySequence.lean).
Calibration of the limiting error to zero and control of every mesh
in (G2) are necessary; a subsequence step bound alone is insufficient.
The Cauchy owner concerns a supplied step inequality and does not
prove (G2) for gravitational responses.

The normalization is load-bearing. A bound only on the
**unnormalized** $\Xi-\Xi_{\rm sm}$ by $C\delta_0^n$ incurs both
the site count and $h^{-2}$; its majorant has ratio
$\phi^6\delta_0=\phi^3/2>1$ and does not imply this closure.
Likewise the golden cylinder mass identity proves exact preservation
of weights, rather than a contraction of metric-response error.
Neither a phase constant nor the four scalar branch identities supplies
the response inequality in (G2).

Consequently (G1)--(G3) identify exactly where $\phi$ and $\pi_0$ could
close the original object. The quantitative implication is proved;
its native metric-response premise is not asserted. A finite current,
signed record or operator refinement must derive (G2) from the original
joint equations, rather than insert it as a new admissibility selector.

### 4.2 A structural turn cannot change a fixed smooth Einstein source by relabeling its angle

The machine-checked
[pi0 forcing](../../03_FORMALIZATION/D0/Geometry/Pi0DiscreteAngle.lean)
solves $\delta_0=3/(5p\phi)$ uniquely for $p=\pi_0$ and proves
$2\pi_0(2-\phi)=12/5$. It does not assert that ordinary real
sine and cosine have period $2\pi_0$.

If the structural full-turn coordinate is denoted $a=2\pi_0 y$,
a continuous faithful one-turn rotation bridge must have angular rate
$\pi/\pi_0$ (up to orientation). Indeed a one-parameter rotation
$R(\omega a)$ closes at $2\pi_0$ only if
$\omega\,2\pi_0\in2\pi\mathbb Z$; faithfulness makes the degree
$\pm1$. In positive orientation this gives

\[
 \cos_0(a):=\cos(\pi a/\pi_0),\qquad
 \cos_0(2\pi_0y)=\cos(2\pi y).
 \tag{G4}
\]

This is a conditional smooth bridge computation, not an additional
CORE circle owner. It keeps both constants in their own types.
If it describes the same fixed metric, the Gram components, volume
element and derivative operator must transform with the coordinate.
In particular $\partial_y=2\pi_0\partial_a$ and the factor $\pi/\pi_0$
in (G4) restores the original $2\pi$ derivative. The Einstein tensor,
its variational source and the finite samples are unchanged after
conversion back to the declared $y$-coordinates.

The critical-value obstruction is over all real algebraic numbers,
not merely Q(phi), and covers arbitrary real Lorentz link entries.
Thus the algebraic-critical-value obstruction (16) survives the
structural phase spelling of that **same** cosine metric. Replacing
only the derivative factor $\pi^2$ by $\pi_0^2$ prescribes a different
source; replacing the ordinary phase by $2\pi_0y$ fails unit
periodicity. A genuinely finite native cycle may be read without
classical trigonometry, but its realization as this fixed smooth
metric requires a bridge and cannot be obtained by scalar substitution.

There is also a direct finite control:
[the full-Lorentz witness, Section 3.1](A4D_GLOBAL_LORENTZ_FIXED_SOURCE_NOGO.md#31-the-same-field-has-an-actual-signed-native-q8-lift),
has links that are integer matrices obtained from actual signed Q8
words, with $\tau=0$ fixed in advance. No classical angle is an input
to those links. The refusal of unrestricted instantaneous Einstein
response therefore cannot be removed by attributing their finite-cycle
construction to an imported value of $\pi$. Q8 support still does not
supply full native admissibility or settle the original small-chart task.

## 5. What the native projection tests establish

The [owned Role projection](../../03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseCarrier.lean)
uses [the consecutive phase modulus](../../03_FORMALIZATION/D0/Geometry/ArchiveLaplacianRG.lean),
coordinatewise $x\mapsto x\bmod L$.
It is not the [legacy flat-record modulus](../../03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean)
on $\mathrm{Fin}(L^4)$.
Composing its maps from 8 to 4 gives
$(0,1,2,3,4,5,6,7)\mapsto(0,1,2,3,0,0,0,0)$.
The period-four boost signs cannot pull back coherently: fine points 0
and 6 have opposite signs and the same image. This excludes that one
exactly coherent profile, not all microscopic stationary states.

Two distinct coherent threads, 0 and 1, can retain different readouts
under a natural identity operator. Coherence therefore supplies no general
observable uniqueness theorem. Moreover a profile $L^{-4}\sigma$ can have
$O(L^{-4})$ pullback discrepancy and vanish locally while its raw sum is 1.
A κ topology that ignores that discrepancy differs from the parent norm.

The consecutive coordinate tower also does not directly implement smooth
geometric sampling. Every coordinate thread eventually becomes a fixed
integer, so its sampled position $x_L/L$ tends to zero; nonconstant sampled
fields nevertheless retain macroscopic sup variation across threads at each
level. A geometric response/jet map must be proved, not inferred from
point coherence or from equal carrier cardinalities.

## 6. Constructed finite-probe transfer and its exact boundary

The [finite action-probe completion](A4D_NATIVE_FINITE_PROBE_COMPLETION.md)
now supplies a complete quantitative construction of one measured response
factor, retaining arbitrary exact log-$O(h)$ UV central states. On a fixed
smooth metric pencil, the explicit preparations
$\exp(h\omega_{\rm LC})$ have full connection residual $O(h^2)$.
The full-field action secant identity gives action diameter $O(h)$ for
every log-$O(h)$ preparation with that residual tolerance, without a
derivative bound or a full UV inverse. The literal smooth action converges
globally to the owned Einstein-Hilbert functional, and all ten Gram
components of its variation are identified on general smooth coframes.

Read the central and two independently prepared endpoint actions. The
average of the two one-sided readings is the centered action probe;
its error is $O(h/\epsilon+\epsilon^2)$, uniformly over every endpoint
choice. Taking $\epsilon=h^{1/3}$ gives $O(h^{2/3})$ and proves one
catalogue-independent output from actual finite data. Geometric measurement
intervals construct its singleton completion; predeclared localized probes
give the pointwise canonical Einstein germ. The generic native canonicity
interface is instantiated after this physical constancy estimate is proved.
This analytic construction is not claimed to be a new Lean owner.

The finite record retains the original central connection and its sitewise
Xi. Thus the #232 curved nongauge null family is retained; the #227 visible
family is retained too, with its raw Xi still nonzero. Their completed
action-probe outputs agree at a flat metric. This explicitly describes a
coarser measured factor, rather than declaring #227 invisible in the
original response topology.

The [exact full-Lorentz witness](A4D_GLOBAL_LORENTZ_FIXED_SOURCE_NOGO.md)
now rules out extending instantaneous-response fidelity to every state of
the full nondegenerate Lorentz configuration domain. It has one fixed
curved metric, one fixed smooth vacuum source and zero full Euler rows,
but a nonzero continuum comparator gap. Its involutive plaquette spectrum
excludes every sufficiently small identity chart, in every node gauge.
Thus it coexists with the small-log positive construction and identifies
the actual domain restriction an unrestricted native transfer would need.

For the original fixed-source, unweighted owner theorem, the outstanding
result remains a uniform comparator estimate on the full realizable source
image, including UV fields without uniform C7 extensions. Constructible
approximate probe preparations do not imply exact independently sourced
joint roots. The new experiment closes its own response completion; it is
not substituted for the parent raw-response assertion or a proof that
every untyped native state has an owned metric realization.

Allowing canonically determined refinement corrections to the metric or
source is a different coupled realization question. Its existence requires
metric/gauge/source compatibility in addition to (12); neither the
connection recurrence nor a candidate-dependent source supplies it.

## 7. Verification and exact hostile controls

The [new finite checker](certificates/a4d_regular_stationary_germ_canonicity_check.py)
and [pinned output](certificates/a4d_regular_stationary_germ_canonicity_results.json)
replay the all-solder and independent Schur owners, check translated nodal
reconstruction, and test the regularity threshold against an exact stencil
with a UV kernel. Native projection controls retain distinct threads and
the κ/raw topology mismatch. The analytic estimates above are proofs;
a finite replay is not represented as a certificate of every smooth family.

The hostile stencil has $F_h a=a+(T_h+T_{-h})a/2$, frozen block 2 and an
exact alternating kernel. On a four-dimensional mesh,
$a_h=h^6\cos(\pi y_1/h)$ has bounded $C^6$ norm, zero Euler residual,
and scalar raw normalized readout 1. Its $C^7$ norm diverges.
Replacing $h^6$ by $h^7$ gives bounded $C^7$ norm and raw gap $h$,
matching (5). Thus frozen invertibility alone is insufficient, the proof
does not require full UV invertibility, and the exponent six cannot
generally replace seven in this finite-stencil argument.
This is a hostile inference model, not an A4D counterexample.
