# Exact sampled Einstein source: arithmetic and generic infeasibility

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Audited input: `cfb308ed8ca4b053b680fc0385b4f8d36d66cb42`.
Status: **exact source infeasibility on the specified warp and a residual set of smooth metrics**.
The parent response-decoupling task remains PARTIAL / OPEN.

For the fixed warp below and its independently declared continuum Einstein
source in the owned Gram-dual convention, there is **no real full-link
solution** of
\[
E_K(Q_h,K)=0,\qquad \Xi(Q_h,K)=h^2\tau_h
\tag{1}
\]
on any allowed mesh $L\in4\mathbb N$, $h=1/L$. The proof applies to
every physical Lorentz link, including rough fields, noncommuting shared
links, singular stationary loci and nongauge moduli. It needs no small-log,
normal-graph, Fourier-support, inverse or refinement estimate.

This is the second outcome of the fixed-source existence attack. It is not
`A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`: that verdict would require
an exact sourced sequence with a separated response, and (1) has none here.

Section 8 proves the stronger general realization obstruction: in every open
smooth metric neighborhood, a residual set of fixed metrics with their fixed
continuum Einstein sources has no full real Lorentz joint root on any mesh.
The proof uses finite critical values and metric two-jet freedom, with no
arithmetic assumption. It does not establish the parent raw-response
implication on exceptional realizable pairs.

## 1. Fixed geometry and a fully typed source

Fix, before choosing connections,
\[
f(y)=1+\frac{1-\cos(2\pi y)}{50},\quad
S(y)=\operatorname{diag}(1,1,f(y_1),f(y_1)),\quad
g=S^T\eta S=\operatorname{diag}(1,-1,-f^2,-f^2),
\quad\eta=\operatorname{diag}(1,-1,-1,-1).
\tag{2}
\]
The metric is smooth, nondegenerate and nonconstant, and has nonzero
curvature. Use exactly $Q_h(x)=g(hx)$ and $\tau_h(x)=\tau(hx)$.

The ten packed metric covector slots are
`(00,01,02,03,11,12,13,22,23,33)`. Packing already includes the factor
two on off-diagonal covectors. Put $p=f'$, $q=f''$, and declare
\[
\boxed{\tau=
(-fq-p^2/2,0,0,0,p^2/2,0,0,q/(2f),0,q/(2f)).}
\tag{3}
\]
This source depends only on (2), never on a candidate connection or its
output.

Here is the normalization of (3). In the standard Ricci convention used by
the [designated-rescue normal-jet owner](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md#6-physical-response-normalization-and-the-einstein-normal-jet),
\[
R_{\rm standard}=4q/f+2p^2/f^2,\qquad
\tau=\frac{\sqrt{|\det g|}}2
\operatorname{pack}(G_{\rm standard}^{ab}),\qquad
\sqrt{|\det g|}=f^2.
\tag{4}
\]
Both indices of the standard Einstein tensor are raised by $g^{-1}$.
The independent Christoffel computation and the literal smooth Euler
calculation give exactly (3). This is the raw covector representation of
the owned continuum response; the displayed `-G[g]/2` in #216 uses its
reconstruction/sign convention. A lower-index standard tensor cannot be
inserted into the raw Gram slots without that conversion.

The obstruction below also holds for the opposite overall sign of (3),
or any nonzero real-algebraic constant multiple of it. A sign convention
cannot remove it.

## 2. Return to the finite action: an algebraic critical-value lemma

Let $k=\mathbb R_{\rm alg}$, the field of real algebraic numbers.
Let $U_1,\ldots,U_N\in SO^+(1,3)$ be arbitrary real matrices, and let
$A(U_1,\ldots,U_N)$ be a polynomial with coefficients in $k$.
Take the six rational physical generators $X_a$ of
$\mathfrak{so}(\eta)$.

**Lemma.** If every right-invariant Euler derivative
\[
dA[U_jX_a]=0\qquad(j=1,\ldots,N;\ a=1,\ldots,6),
\tag{5}
\]
then $A(U_1,\ldots,U_N)\in k$.
The link entries themselves need not be algebraic.

**Proof.** Let $F=k(\text{all entries of all }U_j)\subset\mathbb R$.
This is a finitely generated field of characteristic zero. Suppose
$t=A(U)\notin k$. A real number algebraic over $k$ is algebraic over
$\mathbb Q$, so $t$ is transcendental over $k$.

Extend $\{t\}$ to a transcendence basis
$\{t,t_2,\ldots,t_d\}$ of $F/k$.
On $k(t,t_2,\ldots,t_d)$, define a $k$-derivation $D$ by
$Dt=1$ and $Dt_i=0$ for $i>1$.
The remaining extension to $F$ is finite and separable. Thus $D$
extends to $F$: for each algebraic generator $\alpha$ with minimal
polynomial $b$,
\[
D\alpha=-\frac{(Db)(\alpha)}{b'(\alpha)}.
\tag{6}
\]
Characteristic zero makes the denominator nonzero. This is ordinary field
differentiation, not a regularity hypothesis on the stationary locus.

Differentiate $U_j^T\eta U_j=\eta$ in $F$. Then
\[
Y_j=U_j^{-1}DU_j,\qquad Y_j^T\eta+\eta Y_j=0.
\tag{7}
\]
Write $Y_j=\sum_a\xi_{ja}X_a$, with $\xi_{ja}\in F\subset\mathbb R$.
Polynomial chain rule and (5) give
\[
DA=\sum_{j,a}\xi_{ja}\,dA[U_jX_a]=0,
\tag{8}
\]
contradicting $DA=Dt=1$. This proves the lemma.

The matrices $DU_j=U_jY_j$ are genuine real tangents. The curves
$U_j\exp(sY_j)$ preserve the physical component for small real $s$.
No compactness, connected-component enumeration, algebraicity of the
roots, nonsingular Hessian or stationary continuation in the metric
variables is used.

Equivalently, if a claimed source forces $A=r\pi^2$, $r\in k\setminus\{0\}$,
one may take $D\pi^2=1$ and obtain $DA=r\ne0$ directly.

## 3. Why the full D0 lattice action satisfies the lemma

For every finite $L$, the values
\[
\cos(2\pi n/L)=\tfrac12(\zeta_L^n+\zeta_L^{-n})
\tag{9}
\]
are real algebraic numbers. The sampled coframe (2), its inverse, the
complementary wedge weights, $\eta$, and the declared rational mesh
normalizations therefore lie in $k$.

The [literal full-current owner](A4D_FINITE_CURRENT_CORRELATION_MEMORY.md#3-the-exact-polynomial-degree-bound)
uses physical Lorentz matrices $U$, with
\[
U^{-1}=\eta U^T\eta.
\]
Every based plaquette and its inverse are products of four factors linear
in the entries of the physical links. The naked action
\[
\mathscr A_h(S,U)=\sum_{x,r<s}
\langle W_{rs}(S_x),\tfrac12(P_{x,rs}-P_{x,rs}^{-1})\rangle
\tag{10}
\]
is consequently a polynomial of degree at most four with coefficients in
$k$. All shared-link incidences remain present. Vanishing of all $24L^4$
physical Euler rows is equivalent to (5). Left and right trivializations
differ by invertible adjoint maps, so their zero equations agree; no
historical Bloch placement is used here.

If a notation uses frame-dressed links
$K_{x,r}=\Theta_xU_{x,r}\Theta_{x+e_r}^{-1}$, apply the lemma to the
original physical $U$. On (2) the fixed frame transformations are
algebraic, so the action still has coefficients in $k$. One must not
assume a generally dressed matrix is itself $\eta$-Lorentz.

Therefore every real exact connection-stationary field on this sampled
background has
\[
\boxed{\mathscr A_h(S_h,K)\in\mathbb R_{\rm alg}.}
\tag{11}
\]

The derivation fixes sampled coframe values in (9). It is not differentiation
of a trigonometric function with respect to its analytic argument.
There is no conflict between $D\pi^2=1$ and fixing those algebraic samples.

## 4. Exact source substitution gives a contradictory action value

The existing [full-field homogeneity identity](A4D_WARPED_TRANSVERSE_MEAN_REDUCTION.md#7-an-exact-stationary-action-identity-for-the-full-four-dimensional-field)
is
\[
\mathscr A_h(S,K)=\sum_xQ_x:\Xi(S,K)_x.
\tag{12}
\]
It follows from the degree-two homogeneity of each weight in $S$:
the genuine Gram radial variation $\dot Q=Q$ has lift $\dot S=S/2$.
The off-diagonal factor is already packed into $\Xi$, so it is not
multiplied again. On full connection-stationary fields, this is the
descended metric Euler entering (1).

For the source (3),
\[
Q:\tau=-2ff''-(f')^2.
\tag{13}
\]
Put $c=\cos(2\pi y_1)$. Direct substitution gives
\[
Q:\tau=\frac{\pi^2}{625}(3c^2-102c-1).
\tag{14}
\]
For every $L\ge3$, the two geometric sums
$\sum_n\zeta_L^n=\sum_n\zeta_L^{2n}=0$ imply
\[
\sum_{n=0}^{L-1}c_n=0,\qquad
\sum_{n=0}^{L-1}c_n^2=L/2.
\]
Consequently, with all $L^3$ transverse copies retained,
\[
\sum_{x\in(\mathbb Z/L)^4}Q_h(x):\tau_h(x)=\frac{\pi^2L^4}{1250}.
\tag{15}
\]
Every exact sourced field in (1) would thus have
\[
\boxed{\mathscr A_h=h^2\sum_xQ_h:\tau_h
       =\frac{\pi^2L^2}{1250}.}
\tag{16}
\]
The right side is transcendental: $L^2/1250\ne0$ is rational and
$\pi^2$ is transcendental. Equations (11) and (16) contradict each other.
This proves nonexistence on every allowed mesh, without any passage to a
limit. In fact the same proof works for all $L\ge3$.

For a general nonzero rational warp amplitude $a>-1/2$, so that the fixed
warp remains positive and nondegenerate, the exact mean in
(14) is $2\pi^2a^2$, and (16) becomes $2\pi^2a^2L^2$.
At $a=0$ the trace vanishes, so this obstruction disappears, as it should.

## 5. The first smooth-comparator correction is also explicit

The [literal comparator checker](certificates/a4d_warped_smooth_comparator_bias_check.py)
reconstructs all 24 shared-face connection rows through order three, and
the ten genuine Gram readouts. In relative notation for the smooth
one-coordinate construction,
\[
h^{-2}\Xi(Q_h,K_h^{\rm sm})
=\rho_0+h\rho_1+O(h^2),\qquad \rho_0=\tau,
\]
\[
\boxed{\rho_1=
(3pq/2,0,0,0,-pq/2,p^3/(2f),p^3/(2f),0,0,0).}
\tag{17}
\]
An arbitrary 24-component third logarithmic coefficient cannot alter
the order-three metric readout; all third connection rows can be solved
by the owned constant-character Hessian. The checker retains this fact
instead of silently setting that coefficient to zero.

For (2), at $y_1=1/8$,
\[
\rho_{1,00}=3\pi^3/1250\ne0.
\]
Thus (17) is the first nonzero smooth-comparator bias on an open set.
If exact solutions with the source $\rho_0$ existed, the established
fixed-source Riemann-sum gate would give a normalized raw owner gap of
order $h^{-3}$, with
\[
h^3\left[h^{-2}\|\Xi(K_h)-\Xi(K_h^{\rm sm})\|_{\rm owner,1}\right]
\longrightarrow\int_{\mathbb T^4}\|\rho_1\|_{\rm owner,1}>0.
\tag{18}
\]
But Section 4 excludes those solutions. Equation (18) is a conditional
control, not an instantiated counterexample or parent NO-GO.

## 6. What this resolves and what it leaves

The [exact warped rescue](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md) still
provides a full connection-stationary root. Its output source depends on
the mesh and its response is super-algebraically close to the comparator.
Its stationary action is algebraic at each finite mesh and can approximate
(16) without equalling it. There is no contradiction with that theorem.

For a predeclared transverse-invariant source, the final equation of the
[mean reduction](A4D_WARPED_TRANSVERSE_MEAN_REDUCTION.md) already fixes
$\mathcal R_h(v)=h^2\tau_h-G_h(0)$.
A contraction in a new scale cannot change that prescribed difference.
The connection-only super-algebraic residual also does not make the
independent metric-source residual super-algebraic. On the particular
pair (2)--(3), there are no transverse exact joint fields to estimate.

The proof constrains **one total action/trace**, not every pointwise
response slot or link entry. This one scalar is sufficient because the
fixed source has the explicit nonzero transcendental trace (16).
Nonalgebraic moduli and response-visible stationary fields remain
possible with algebraic total action; the retained exact flat boost
control has nonzero sitewise traces and zero total four-phase trace.

This resolves the selected fixed-source existence attack by proving that
its exactly sampled sourced class is empty. It identifies an incompatibility
of this exact discretized prescription on one curved geometry. It does
not prove general source-image closure, a continuum failure of Einstein
gravity, or the original response-gap NO-GO. No source, norm, action,
selector, Lean owner, public claim or task terminal is changed.

## 7. Verification

The arithmetic-source checker independently reconstructs Christoffels,
Ricci and the raised density source; verifies literal face/Gram homogeneity
including off-diagonal weights; checks exact cyclotomic sample sums and
the all-L geometric-series identity; and checks the six-generator tangent
span and the response-visible stationary control. The bias checker
verifies all 24 connection rows, independence from arbitrary third
coefficients, the complete odd-curvature projection, and hostile omission
and swapped-incidence controls. Their pinned ledgers distinguish these
finite exact checks from the analytic field-derivation proof in Section 2.

```bash
python 02_REGISTRY/research/certificates/a4d_fixed_source_algebraic_stationarity_check.py
python 02_REGISTRY/research/certificates/a4d_warped_smooth_comparator_bias_check.py
```

The two source/normalization audits and a separate scale/field-derivation
audit agreed independently. Local repository checks and published-head CI
are tracked separately from the mathematical conclusion.

Both fresh pinned replays and the retained stationary-response-memory and
full-current transport controls pass locally. Canonical architecture,
generated Lean views, active work, agent protocol, claim-strength,
formalization-debt non-growth, certificate freshness, Python syntax and
whitespace checks pass. No Lean source changed; no full release build is
inferred from these checks. The published-head Actions run is reported
separately in PR #310.

## 8. Generic exact-source infeasibility without arithmetic hypotheses

The obstruction is structural, rather than specific to algebraic cosine
samples. Keep the unchanged action, all physical link Euler rows, and the
same packed continuum source

\[
 \tau_E[g]=\operatorname{pack}\!\left(
 \tfrac12\sqrt{|\det g|}\,g^{-1}G_{\rm std}[g]g^{-1}\right).
 \tag{19}
\]

The off-diagonal entries are packed with factor two. This is the owner
reconstruction of `-G/2` used in Sections 1--4. For a fixed metric, (19)
is one smooth source declared before the links and retained on every
mesh. No mesh-dependent source is introduced in this section. A continuous
pointwise Gram section is fixed on the metric neighborhood below; another
proper Lorentz section has the same full-fiber feasibility by node gauge
covariance.

**Theorem (generic exact sampled-Einstein infeasibility).** Let
\(\mathcal U\) be a nonempty open set, in the usual \(C^\infty\) topology,
of smooth periodic Lorentz metrics on \(\mathbb T^4\) in a neighborhood
where the owned nondegenerate solder section exists. It may be chosen
inside the original background chart and inside the open set of metrics
with nonzero curvature somewhere. There is a residual, hence dense,
subset \(\mathcal R\subset\mathcal U\) such that each one fixed
\(g\in\mathcal R\), with its one fixed source (19), has **no full real
Lorentz joint root on any allowed mesh**:

\[
 E_K(g(hx),K)=0,\qquad
 \Xi(g(hx),K)=h^2\tau_E[g](hx),\qquad L\in4\mathbb N.
 \tag{20}
\]

The conclusion covers the entire physical Lorentz link space, including
all rough and nonalgebraic links and singular stationary fibers. It
therefore also covers the original sufficiently small log chart. No
\(C^7\) bound or expansion of an unknown connection is imposed.

### 8.1 A finite critical-value set on each fixed mesh

Freeze arbitrary real sampled solders \(S_h\), without assuming that their
entries are algebraic. On
\(\mathcal M_L=SO^+(1,3)^{4L^4}\), the literal action (10) is a polynomial
with real coefficients of degree at most four. The physical Lorentz
manifold is smooth and semialgebraic. Its connection-critical set is
semialgebraic: use the six globally spanning right-invariant generators
on every link and impose all their polynomial action derivatives equal
to zero.

There are finitely many connected components of this set. Each component
is connected by piecewise smooth semialgebraic paths. Along every smooth
piece, the action derivative vanishes, because the tangent lies in the
physical Lorentz manifold and every right-invariant Euler row vanishes.
Continuity joins the pieces. Thus the action is constant on each component:

\[
 \mathcal C_L(S_h)=\{
 \mathscr A_h(S_h,K):E_K(S_h,K)=0\}
 \quad\hbox{is finite}.
 \tag{21}
\]

This also follows directly from the semialgebraic Sard theorem for a
real-valued polynomial on a smooth semialgebraic manifold: its critical
value set has dimension less than one. See Michel Coste,
[An introduction to semialgebraic geometry, Theorem 4.8 and Exercise 4.9](https://perso.univ-rennes1.fr/michel.coste/polyens/SAG.pdf).
No regularity of the critical locus or nondegenerate Hessian is required.
The number and positions of these values may depend on the mesh and its
sampled solder; no uniform spectral separation is asserted.

The exact homogeneity identity (12) gives the necessary condition for (20)

\[
 W_L(g):=h^2\sum_x g(hx):\tau_E[g](hx)
 =-\frac{h^2}{2}\sum_x\sqrt{|\det g(hx)|}\,R_{\rm std}[g](hx)
 \in\mathcal C_L(S_h).
 \tag{22}
\]

Only one necessary scalar is used to exclude all full joint roots. It is
not treated as sufficient for the ten pointwise metric equations.

### 8.2 Preserve the entire sampled metric and change its source trace

Fix a mesh and one node \(y_*\). Choose a smooth periodic function \(u\)
supported in a coordinate ball that contains no other node, with

\[
 u(y_*)=0,\quad du(y_*)=0,\quad
 (\partial_a\partial_bu)(y_*)=\tfrac14 g_{ab}(y_*).
 \tag{23}
\]

For example, multiply
\(\tfrac18 g_{ab}(y_*)\xi^a\xi^b\) by a bump equal to one near the
origin. Then \(\Box_gu(y_*)=1\). Put \(g_t=e^{2tu}g\). For all small real
\(t\), \(g_t\in\mathcal U\), and the values and first jets of the metric
at **every** mesh node are unchanged. Choose the solder
\(S_t=e^{tu}S\); its samples are exactly the original \(S_h\).
Consequently the whole finite action, all its connection equations and
the finite set (21) are unchanged.

At a node where \(u=du=0\), the Christoffel difference and its derivative
give, exactly in \(t\),

\[
 \operatorname{Ric}_{\rm std}[g_t]-\operatorname{Ric}_{\rm std}[g]
 =-2t\,\partial^2u-tg\,\Box_gu,
 \qquad
 R_{\rm std}[g_t]-R_{\rm std}[g]=-6t\,\Box_gu.
 \tag{24}
\]

Indeed the Christoffels themselves are unchanged at the node, while
\(\partial_b(\Gamma_t^k{}_{ij}-\Gamma^k{}_{ij})
=t(\delta_i^k u_{jb}+\delta_j^k u_{ib}-g_{ij}g^{ka}u_{ab})\).
The quadratic Christoffel terms therefore cancel in the Ricci difference.
This derivation applies with arbitrary background first and second jets,
not just in normal coordinates. It agrees with the pseudo-Riemannian
conformal connection formula in Kuehnel and Rademacher,
[Conformal Transformations of Pseudo-Riemannian manifolds, Proposition 2.2](https://www.math.uni-leipzig.de/~rademacher/esi.pdf).

Writing \(H=\partial^2u\), the change of the raised density source (19) at
such a node is

\[
 \delta\tau_E= t\,\operatorname{pack}\!\left(
 \sqrt{|\det g|}\,[-g^{-1}Hg^{-1}+g^{-1}\operatorname{tr}(g^{-1}H)]
 \right),\qquad
 g:\delta\tau_E=3t\sqrt{|\det g|}\,\Box_gu.
 \tag{25}
\]

All other sampled source values are unchanged, so (22) becomes

\[
 W_L(g_t)=W_L(g)+3h^2\sqrt{|\det g(y_*)|}\,t.
 \tag{26}
\]

The slope is nonzero. The permitted source trace values (21) are finite
and independent of \(t\); hence only finitely many \(t\) can possibly
admit any full joint root. In every neighborhood of every fixed smooth
metric there are therefore metrics for which (20) has no root on this
mesh. This varies the prescribed pair before solving; it does not vary
the source with a chosen connection.

### 8.3 One fixed metric and source fail on every mesh

For integers \(L\in4\mathbb N\) and \(m\ge1\), let
\(\mathcal B_{L,m}\subset\mathcal U\) consist of metrics admitting a root
of (20) whose physical link matrices all have Frobenius norm at most
\(m\). This is a closed set relative to \(\mathcal U\). If
\(g_n\to g\) in \(C^\infty\) and such roots exist, the finite product of
bounded physical Lorentz matrices is compact. The component can be
written with \(U^T\eta U=\eta\), \(\det U=1\), \(U_{00}\ge1\), so it is
closed under these bounded limits. A subsequence of the roots converges;
continuity of the finite Euler formulas and of the source's two-jet
sampling preserves all equations in the limit.

Equation (26) proves that \(\mathcal B_{L,m}\) has empty interior, so it
is nowhere dense. Every finite real Lorentz root has some finite matrix
bound \(m\). The \(C^\infty\) metric space is a Frechet space, and its open
subset \(\mathcal U\) is a Baire space. Consequently

\[
 \mathcal R=\mathcal U\setminus
 \bigcup_{L\in4\mathbb N}\bigcup_{m\ge1}\mathcal B_{L,m}
 \tag{27}
\]

is residual and dense. Each metric selected once from \(\mathcal R\)
and its source (19) stay fixed for **all** meshes. There is no refining
rooted subsequence, even if one allows the full Lorentz domain. This
proves the theorem. The Baire argument is about a single fixed pair in
the complement of countably many feasibility sets; it is not the weaker
convention of a sequence \(\tau_h\to\tau\).

### 8.4 What this decides for closure

There is no exact sampled-Einstein realization assignment on any nonempty
open family of smooth metrics under (20), even a discontinuous assignment
and even before imposing native carrier coherence. In particular, a
universal native-to-exact-root bridge over such a family cannot be the
missing closure step. This conclusion does not depend on arithmetic
constants: \(\pi\), \(\varphi\), \(\pi_0\), a spectral circle or an amplitude
classification never enter (21)--(27).

**Concrete fixed-background corollary.** Already for the single fixed
cosine warp (2), there is **no** fixed smooth source \(\tau\) and refining
exact joint sequence in the original chart for which the original owner
response converges. If such a pair existed, (29) below would force
\(\tau=\tau_E[g]\). The arithmetic theorem in Sections 2--4 excludes
every exact joint root for that very source on every mesh, giving a
contradiction. This conclusion also holds for the already proved
arbitrarily small nonzero rational-amplitude cosine warps, so the
background can be selected once inside any prescribed sufficiently small
metric neighborhood. Neither the metric nor its source varies with the
mesh or with a chosen connection.

Thus nonempty exact fixed-source realizability and the unchanged positive
owner completion are incompatible even on one explicit smooth curved
background, allowing the source to be chosen freely in advance. This is
an obstruction to their conjunction. It does not assert that every fixed
source fiber is empty, construct a rooted response-gap witness, or settle
the parent's conditional implication on realizable pairs.

**Synthesis theorem: nonvacuous universal response completion is impossible,
even with arbitrary fixed smooth sources.** Let \(\mathcal P\subset\mathcal U\)
be the backgrounds for which there exists at least one smooth source
\(\tau\), fixed across meshes, and a refining sequence of exact joint roots
inside the original small log chart, satisfying the unchanged owner limit

\[
 h^{-2}\|\Xi(g(hx),K_h)-\Xi(g(hx),K_h^{\rm sm})\|_{\mathrm{owner},1}
 \longrightarrow0.
 \tag{28}
\]

Then \(\mathcal P\) is meagre in \(\mathcal U\); in particular it cannot
contain a nonempty open set. This statement does not assume any regularity
of the unknown links and does not prescribe the source to be Einstein at
the outset.

To prove it, use only the leading owned comparator limit
\(\rho_{{\rm sm},h}=h^{-2}\Xi(g(hx),K_h^{\rm sm})
=\tau_E[g]+O(h)\), uniformly at the nodes, in the same packed covector
convention as (19). At an exact sourced root, the normalized difference
is exactly \(\tau(hx)-\rho_{{\rm sm},h}(hx)\). Its nodal supremum is at
most its unweighted owner sum. Every point lies within \(2h\) of a node;
smoothness of the two fixed sources and the uniform comparator remainder
therefore give

\[
 \|\tau-\tau_E[g]\|_{C^0,\mathrm{packed},1}
 \le h^{-2}\|\Xi-\Xi_{\rm sm}\|_{\mathrm{owner},1}+C_{g,\tau} h
 \longrightarrow0.
 \tag{29}
\]

Thus \(\tau=\tau_E[g]\) identically. Every \(g\in\mathcal P\) consequently
admits an exact sampled-Einstein root on at least one allowed mesh, and
hence belongs to the countable union of closed nowhere-dense sets in
(27). This proves the meagreness assertion.

Equivalently, there is no source assignment \(g\mapsto\tau(g)\), even a
discontinuous one and even with arbitrary choices of smooth source, for
which **both** exact refining nonemptiness and (28) hold on an open family
of smooth curved backgrounds. Source selection cannot evade the
obstruction: the unchanged response limit itself forces its Einstein
value. This rules out a nonvacuous universal positive completion of this
exact-sampling theory. It uses the original norm, comparator and chart;
no new selector or candidate family is introduced.

The open-family nonemptiness premise is essential to that physical
conclusion. The conditional implication on exceptional realizable pairs
is a different statement. Neither its proof nor a rooted response-gap
counterexample follows from meagreness; neither parent terminal is set.

This is a feasibility obstruction for the **exact sampling prescription**.
It neither rules out asymptotic Einstein convergence with corrected metric
or source samples nor supplies an exact rooted response-gap witness. It
also does not determine the exceptional source image
\(B(g,\tau)\) of the parent task. On that exceptional image, the unchanged
original obligation remains \(B\Rightarrow J\), or a fixed admissible pair
with \(B\) and not \(J\). Residual empty Einstein fibers cannot be promoted
to either parent raw-response terminal. The task remains PARTIAL / OPEN.

### 8.5 Exact check and its boundary

The existing arithmetic-source checker now also derives (24)--(25) from
Christoffel two-jets using a generic ten-parameter triangular Lorentz
solder and all ten independent Hessian parameters. This parameterization
covers a neighborhood of the original Gram chart. It checks every raised
packed source slot, the nonzero direction \(H=g/4\), the action slope
(26), and a hostile control omitting the off-diagonal packing factor.
It certifies these algebraic identities; the finite-critical-value and
Baire arguments above are analytic proofs, not inferred from a finite
sample or a green guard.
