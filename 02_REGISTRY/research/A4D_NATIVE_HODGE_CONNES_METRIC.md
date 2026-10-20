# Native operator first: exact flat Connes metric of the owned Hodge/CAR operator

Task: existing `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Input SOURCE: `569abdc48795b161aa5fe6d2a1c12ecdd05f66b0`.
Main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Supported D0 tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.

**Result:** the actual finite counting-pairing operator `hodgeCarDirac`, with
scalar point multiplication on the entire owned cubical cochain carrier,
induces exactly the Euclidean product-circle metric. This holds for every
`L=N+2>=2` and every pair of sites, without changing its differential or
introducing a twist. Its square is the already proved fibrewise difference
Laplacian. This is a genuine operator-to-metric implication, not a metric
assigned to fit a target and not a physical GR theorem.

The complete proof below is finite-dimensional analytic. The companion Lean
capsule proves the literal owned-operator commutator, all sixteen Fock-column
orthogonality/Parseval identities, and the actual square and adjoint bindings.
The supremum/operator-norm, multilinear interpolation, and distance theorem
are **not** advertised as a complete Lean formalization. Exact sparse integer
controls support those explicitly proved steps without extrapolating finite
rank data to an all-size conclusion.

The new commutator, Fock-column and adjoint proofs have only standard logical
axioms. The imported square owner retains its three `native_decide` CAR leaf
axioms; the receipt prints them literally and the integer checker independently
replays those CAR identities. They are not erased or described as kernel-only.

## 1. Fix the actual triple and its readout

Use the owners `ArchiveRolePhaseGroup`, `ArchiveCubicalDifferential`,
`ArchiveHodgeCARDirac` and `ArchiveHodgeCARDiracSquare` unchanged:

\[
X_L=(\mathbb Z/L\mathbb Z)^{\mathrm{Role}},\quad
\mathcal H_L=\mathbb R^{X_L\times\{0,1\}^4},\quad
\mathcal D_L=L\sum_{r=1}^4\left[
c_r^\dagger(S_r-I)+c_r(S_r^{-1}-I)\right].                 \tag{1}
\]

`S_r psi(x)=psi(x+e_r)`; `c_r` are the literal Jordan--Wigner matrices
with the owned Role order A,B,C,D. In particular (1) is **not** the distinct
`hoppingCarDirac`. Retain every site and all sixteen exterior grades. The
inner product is the owner's counting `cochainPairing`; multiplying both
norms by the common site-volume factor `L^-4` does not change an operator norm.

For a real scalar site field f, use its diagonal multiplication
`M_f psi(x,S)=f(x)psi(x,S)` on **every** grade. Let

\[
d_{\mathcal D,L}(x,y)=\sup\{ |f(x)-f(y)|:
\|[\mathcal D_L,M_f]\|_{2\to2}\le1\}.                     \tag{2}
\]

This specifies the algebra representation as well as the operator. It is
the commutative scalar point algebra on the archive, not a claim that it is
the entire noncommutative scene path algebra. Its mathematical multiplication
uses the actual scalar fields; physical apparatus access to every observable
in (2) is a separate admission question. No assertion that eigenvalues alone
determine (2) is used: the represented triple and its commutator are required.

Write `ell_r(x,y)=min(|x_r-y_r|,L-|x_r-y_r|)` with representatives in
`{0,...,L-1}`. The theorem is

\[
\boxed{d_{\mathcal D,L}(x,y)=L^{-1}
                 \sqrt{\sum_{r=1}^4\ell_r(x,y)^2}.}        \tag{3}
\]

## 2. Upper bound from every actual Fock column

Let `delta_r f(x)=f(x+e_r)-f(x)`. Direct expansion of (1), with its
zero-order terms cancelled rather than omitted from the operator, gives

\[
C_f=[\mathcal D_L,M_f]
 =L\sum_r\big[c_r^\dagger M_{\delta_r f}S_r
                 -c_r S_r^{-1}M_{\delta_r f}\big].         \tag{4}
\]

Fix a normalized basis vector at site x with occupation set S. For each
r exactly one CAR term acts. Its output has occupation `S symmetricDifference
{r}`, and all four outputs are orthogonal, even at the `L=2` spatial collision.
The literal Jordan--Wigner sign has squared value one. Consequently

\[
\|C_f e_{x,S}\|^2=L^2\left[
 \sum_{r\in S}|f(x+e_r)-f(x)|^2
 +\sum_{r\notin S}|f(x)-f(x-e_r)|^2\right].                \tag{5}
\]

Thus the norm gate in (2) implies the bracket in (5) is at most `L^-2`
for **every** site and all sixteen S. This is a necessary condition; it is
not substituted for the full operator-norm gate. For nonseparable f the Gram
`C_f^T C_f` can have off-diagonal entries and a larger norm than every column.
The checker retains an exact hostile witness against that substitution.

Interpolate f periodically and multilinearly on each unit lattice cube
before division by L. At a corner v of a cube, each coordinate derivative
of that interpolant is the forward edge difference if `v_r=0`, and the
backward edge difference if `v_r=1`. Select `S={r:v_r=0}` in (5). It follows
that the squared Euclidean norm of this corner gradient is at most `L^-2`.

At an interior point `t in [0,1]^4`, set
`w_v(t)=product_r (t_r if v_r=1 else 1-t_r)`. The derivative of the
multilinear interpolant is **the same convex combination of all corner
gradients**:

\[
\nabla F(t)=\sum_{v\in\{0,1\}^4}w_v(t)\nabla F(v),\quad
w_v\ge0,\quad\sum_v w_v=1.                               \tag{6}
\]

For its r-component the sum over the two possible v_r adds to one; this
proves (6) directly. The elementary squared-norm convexity identity

\[
\sum_v w_v\|u_v\|^2-\|\sum_v w_v u_v\|^2
 =\tfrac12\sum_{v,w}w_vw_w\|u_v-u_w\|^2\ge0
\]

then bounds the interpolated gradient by `L^-1`. In physical coordinates
`x/L` its gradient is bounded by one. The continuous periodic interpolant
is piecewise smooth and globally 1-Lipschitz: integrate along a shortest
straight torus segment, subdividing at cube boundaries. A segment contained
in a boundary follows by continuity or a displacement limit. It has the
original values at all grid points. Therefore every f in (2) satisfies the
upper bound in (3). No continuum reconstruction theorem is needed for this
finite interpolation argument.

## 3. Sharp lower bound from existing scalar fields

Translate the initial site to zero. Let
`tau(j)=min(j,L-j)` be the one-coordinate cyclic distance to zero and
`ell=(ell_r(0,y))`. Its forward differences sigma(j) are in `{-1,1}` for
even L and `{-1,0,1}` for odd L. For ell nonzero define

\[
f_y(x)=\frac{1}{L\|\ell\|_2}\sum_r\ell_r\tau(x_r).       \tag{7}
\]

This field belongs to the algebra in (2); the square root is determined by
its norm, not an independently selected action coefficient. Restriction to
rational-valued fields gives the same supremum by scaling rational
approximations from below.

For the separable unscaled numerator let

\[
A_r=c_r^\dagger M_{\sigma_r}S_r-c_r S_r^{-1}M_{\sigma_r}.
\]

Each `A_r^T=-A_r`. Distinct coordinate shifts/multipliers commute and
distinct CAR factors anticommute, so `A_r A_s+A_s A_r=0` for `r!=s`.
The nilpotent same-role CAR terms vanish, and the remaining two terms give

\[
A_r^T A_r=
 c_r c_r^\dagger S_r^{-1}M_{\sigma_r^2}S_r
 +c_r^\dagger c_r M_{\sigma_r^2}\ \le I.                 \tag{8}
\]

There is no omitted exterior sector in (8). It is diagonal on site/Fock
coordinates. Hence for the numerator of (7)

\[
C^T C=L^2\sum_r\ell_r^2 A_r^T A_r\le L^2\|\ell\|_2^2I. \tag{9}
\]

For even L equality holds in (9); for odd L the zeros of sigma give zero
entries in some summands but never enlarge the norm. Equation (9) proves
that f_y is admitted in (2). Its endpoint difference is exactly
`||ell||_2/L`. Together with Section 2 this proves (3) for every pair and
every L>=2. Equal endpoints give zero directly.

## 4. The prior diagonal obstruction does not describe this operator

For any `L in 4N`, take x=0 and y with A,B coordinates L/4 and the other
coordinates zero. Equation (3) gives

\[
d_{\mathcal D,L}(x,y)=\sqrt2/4,\qquad d_{\mathcal D,L}^2=1/8,
\]

not the path metric `1/2`. This is an exact all-level statement, not a
single small-size comparison.

`ArchiveHodgeDiracMetricMismatchNoGo.lean` genuinely proves
`(1/2)^2 != 1/8` and their squared ratio two. Those arithmetic propositions
remain correct. Its printed owner proposition contains no Dirac operator,
commutator, operator norm, scalar representation, or metric limit. The
comment that the owned Hodge/CAR operator necessarily induces the l1 path
metric is not proved there; with the triple (1)--(2), it is false.
`ArchiveNaturalTwistedDirac` proves the one-dimensional forward/backward
coefficient identity, not a necessity theorem for a nontrivial metric twist.
Neither comment may be used to require a new Riesz twist in this route.

This does not identify every graph incidence operator with (1). Different
Hilbert carriers and algebra representations can give different distances.
The existing l1 path metric remains its own legitimate graph observable.

## 5. What this actually opens, and what remains open

The metric and heat now have a checked **common fixed native operator** on
this carrier: the actual compiled `hodgeCarDirac_sq` is
`D_H^2=cochainDifferenceLaplacian`, on all sixteen grades. No external
metric is needed to define the flat readout (3). In the common flat torus
embedding every finite distance is exact; every torus point is within `1/L`
of a grid point. This supplies a finite metric-net bound, not a claim that
the native archive forgetting maps preserve physical metric readings.

In particular the long native RG maps, coframe/link transitions and their
action contrasts still require their own compatibility proofs. Native
archive level, phi scale and physical mesh are not identified by fiat.
The occurrence `L=N+2` here is the literal derivative scale in the owner.
There is no positive curved metric or Lorentz causal time in (3).

The next native-preparation question can therefore be asked **operator
first**: which actually admitted internal preparation deforms this operator
and its represented point algebra, which q/D/b/m readout does it induce,
and does its full heat/feedback price descend through that readout with a
well-defined joint tangent and native refinement? The current full joint
kinematic quotient is not asserted to parametrize all such preparations.
No deformation, selector, physical action or field law is installed here.

The previously requested `Gamma_h(X)` and `H=F(X)` remain unproved; so does
their absence for the whole core. The full heat derivative remains in the
price. The all-ten-component source, Ward identity, source-subtracted
stationarity, contrast transfer, nonempty curved roots, soundness, recovery,
causal constraints and global closure all remain required. The original
#310 fixed-source/raw-owner and independent #202/#317 terminals are unchanged.

For independent context, Dai--Song's
[original lattice calculation](https://arxiv.org/abs/hep-th/0101092)
constructs a CAR/difference Dirac whose two-dimensional lattice distance is
Euclidean. It supports checking the operator rather than assigning a graph
path metric to it. Our proof of the finite periodic four-role statement is
Sections 2--3; it does not apply that infinite-lattice result without a
hypothesis check or claim a new metric mechanism.

## Reproduction

Run the [capsule](certificates/a4d_native_hodge_connes_metric.lean) from
`03_FORMALIZATION` with `lake env lean ../02_REGISTRY/research/certificates/a4d_native_hodge_connes_metric.lean`.
The [compiler receipt](certificates/a4d_native_hodge_connes_metric_results.json)
and [output](certificates/a4d_native_hodge_connes_metric_output.txt) preserve
actual propositions, transitive owners, toolchain and source SHA.
The [exact checker](certificates/a4d_native_hodge_connes_metric_check.py)
replays full sparse operators, lower witnesses, all corner occupations,
interpolation identities, exceptional L=2/odd-L/wrap cases, and hostile
scope/hash mutations against its
[ledger](certificates/a4d_native_hodge_connes_metric_certificate.json).

