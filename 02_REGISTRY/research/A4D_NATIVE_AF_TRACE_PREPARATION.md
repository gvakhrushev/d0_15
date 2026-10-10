# What Fibonacci refinement fixes in a full preparation

Parent: existing #310. Input SOURCE
`abe5d0677fb68396e824c4894fce7d1254b979b2`.
Status: completeness of the compatible tracial state, and an exact boundary
between that state and a faithful density on the full GNS carrier.
Common physical preparation T0 remains open.

The [actual golden-cost refinement](A4D_NATIVE_GOLDEN_COST_REFINEMENT.md)
provides the full algebras, inclusions and trace. This continuation proves
that positivity and compatibility on the entire tower force that trace
without assuming a Perron eigenprofile. It then answers the next preparation
question: the forced trace does **not** specify a full GNS density. Even
fixing the protected zero vector, positivity of heat and invariance under
internal matrix-coordinate conjugations leaves different thermal prices.

This is a complete statement about the interfaces defined below. It does
not assert that the alternative full densities are physically prepared by
D0, or that all native preparations pass through a Gibbs identification.
No heat, state selector, temperature, action or physical operation is added.

## Positivity forces the trace on all levels

At level n write `(a_n,b_n)=FibonacciAFTower.pathCount(n)` and

\[
 A_n=M_{a_n}(\mathbb C)\oplus M_{b_n}(\mathbb C),\qquad
 \iota_n(A,B)=(\operatorname{diag}(A,B),A).
\]

Every tracial positive functional on this full finite algebra has the form
`tau_n(A,B)=x_n Tr(A)+y_n Tr(B)`, with `x_n,y_n>=0`. This is exhaustive:
the trace property on matrix units kills off-diagonal coefficients and
makes all diagonal coefficients in each simple block equal. Positivity
gives their nonnegative signs. Normalization at level zero is `x_0+y_0=1`.
Compatibility with the **actual** inclusion is exactly

\[
 x_n=x_{n+1}+y_{n+1},\qquad y_n=x_{n+1}.                 \tag{1}
\]

There is no assumed eigenvector, stationarity, fixed ratio or strictly
positive lower bound. Let `p=phi^-1`, so `0<p<1` and `p+p^2=1`.
Equation (1) gives `x_n=x_(n+1)+x_(n+2)` and `0<=x_n<=1`. Set
`e_n=x_(n+1)-p*x_n`. Then

\[
 e_n=-p e_{n+1},\qquad e_n=(-p)^k e_{n+k},\qquad |e_j|\le1.
\]

For every k, `|e_n|<=p^k`; hence `e_n=0`. Normalization now gives
`x_0=p`, and (1) proves

\[
                 x_n=p^{n+1},\qquad y_n=p^{n+2}.          \tag{2}
\]

Thus the compatible normalized tracial state is unique and automatically
faithful at every finite level. A parameterized family satisfying the same
conditions has exactly the same trace for every parameter value. All trace
weight secants and derivatives vanish. This is not a statement that every
observable, operator or physical source vanishes.

The earlier `FibonacciPerronTraceCanonicity` proves uniqueness within a
supplied positive Perron-eigenprofile. The new argument obtains the profile
from nonnegative compatibility across all levels; that is the additional
completeness statement.

## Finite depth has a quantitative boundary

Requiring only r further levels does not force (2) exactly. At level k let
`(a,b)=(a_k,b_k)`, and write

\[
 M^r=\begin{pmatrix}u&v\\v&w\end{pmatrix},\quad
 (A,B)=(au+bv,av+bw)=(a_{k+r},b_{k+r}).
\]

Every positive normalized terminal trace has weights `(s,t)` with
`As+Bt=1`. Its pulled-back first coefficient is `us+vt`. Consequently its
complete range is the closed interval with endpoints `u/A` and `v/B`.
The endpoints are realized by terminal states supported on one simple
block. Both are allowed in the nonnegative class being classified.

Since `det M^r=(-1)^r`, the interval width is `b/(AB)`; the second
coefficient's width is `a/(AB)`. On the defining representation
`C^a (+) C^b`, the trace distance from (2) is bounded by

\[
 {ab\over AB}\le2^{-r}.                                  \tag{3}
\]

Indeed normalization gives `a delta_x+b delta_y=0`, so the distance is
`a|delta_x|`. The canonical trace is inside the interval. At each step
`(a+b)a>=2ab`, since actual path counts obey `a>=b>0`, proving the last
bound. Formula (3) concerns trace states on the defining representation,
not densities on a GNS space of dimension `a^2+b^2` and not an error bound
for the physical action.

## The full GNS state fiber

Fix a level and put `a=a_n`, `b=b_n`, `t=p^(n+1)` and
`u=ta`, `v=ptb`, so `u+v=1`. In normalized Hilbert-Schmidt coordinates,

\[
 \mathcal H_n=(\mathbb C^a\otimes\overline{\mathbb C^a})
       \oplus(\mathbb C^b\otimes\overline{\mathbb C^b}),\quad
 \pi(A,B)=(A\otimes I_a)\oplus(B\otimes I_b).
\]

Its dimension is `d=a^2+b^2`. A full density sigma induces the forced
trace on this represented algebra **if and only if**

\[
 \sigma\ge0,\quad
 \operatorname{Tr}_{right}\sigma_{aa}=tI_a,\quad
 \operatorname{Tr}_{right}\sigma_{bb}=ptI_b.               \tag{4}
\]

Normalization follows from (4). Cross-block entries are invisible to the
represented algebra but remain part of sigma and are constrained by its
positivity. This describes the entire fiber, not merely diagonal examples.
The partial-trace map on Hermitian matrices is onto: use diagonal blocks
`K tensor I_a/a` and `L tensor I_b/b`. Therefore its affine fiber has real
dimension `d^2-d`. It has a faithful interior, for example
`(t/a)I_(a^2) (+) (pt/b)I_(b^2)`. Faithfulness imposes an open positivity
condition; it does not remove this dimension.

The canonical cyclic vector is

\[
 e_a=\operatorname{vec}I_a/\sqrt a,\quad
 e_b=\operatorname{vec}I_b/\sqrt b,\quad
 \Omega=\sqrt u\,e_a+\sqrt v\,e_b.
\]

It induces the same faithful trace on `pi(A_n)`, but
`|Omega><Omega|` has rank one on `B(H_n)`. For `d>1` it cannot be the Gibbs
density of a finite heat matrix on the entire carrier. Changing the
observable algebra is substantive; the two faithfulness claims cannot
be interchanged.

## Price freedom survives a protected zero vector

For every actual level `n>=2`, `a,b>=2`. Put

\[
 \eta=\sqrt v\,e_a-\sqrt u\,e_b,\qquad r_0=uv,
 \quad r_a={u-uv^2\over a^2-1},\qquad
 r_b={v-u^2v\over b^2-1},
\]

and let `P_a`, `P_b` be the full orthogonal projections onto traceless
matrices in their respective blocks. Define

\[
 R=r_0|\eta\rangle\langle\eta|+r_aP_a+r_bP_b.            \tag{5}
\]

All three coefficients are positive. The eigenvalue multiplicities are
`1,a^2-1,b^2-1`; their weighted sum is one. The identities
`Tr_right |e_a><e_a|=I_a/a` and
`Tr_right P_a=(a-1/a)I_a`, and their b counterparts, show that R satisfies
(4). Its kernel is exactly the line Omega; every complementary direction
is retained with positive weight. Define, for `1/2<=lambda<1`,

\[
 \sigma_\lambda=\lambda|\Omega\rangle\langle\Omega|
                       +(1-\lambda)R.                  \tag{6}
\]

These are faithful full densities inducing the **same** trace (2).
Their simple largest eigenvalue is lambda with eigenvector Omega; all
other eigenvalues are `(1-lambda)r_i`, strictly between zero and lambda.
They are invariant under every internal change of matrix coordinates
`X -> V_a X V_a*`, `Y -> V_b Y V_b*`. This covariance therefore does not
select lambda. The family is defined at every level n>=2 and gives the
same compatible observable trace across those levels.

Apply the already proved [full Gibbs reconstruction](A4D_NATIVE_MODULAR_PREPARATION_BOUNDARY.md),
conditional on using this normalized-state interface at a fixed beta>0.
Positive heat with the protected kernel `span(Omega)` is uniquely

\[
 H_\lambda=\beta^{-1}(\log\lambda\,I-\log\sigma_\lambda),
 \qquad B_{H_\lambda}=-\beta^{-1}\log\lambda.             \tag{7}
\]

Every mode is included in the ordinary operator trace. This is no longer
the scalar-shift freedom: the ground-zero condition has fixed that shift.
The full state itself varies within (4). At `lambda=1/2` and `3/4` the
prices differ by `beta^-1 log(3/2)>0`. In the open interval,

\[
                 {d B\over d\lambda}=-{1\over\beta\lambda}\ne0.
\]

The difference survives every unitary conjugacy because the largest
state eigenvalue and the thermal price are invariants. It is not a basis
gauge. It proves that the trace/readout data alone do not determine the
full price, even with a protected constant zero mode and this intrinsic
covariance. It does not make lambda a native variable, a physical source
or a new selector. The full physical refinement/admission of (6) has not
been derived and is not asserted.

### Every state in this interface has a descent direction

At the same actual levels `n>=2`, the failure of thermal minimization
holds on the entire stated state fiber. Let sigma be **any** faithful full
density satisfying (4) for which Omega
is its simple largest-eigenvalue vector, with eigenvalue `0<lambda<1`.
These are exactly the states whose positive ground-zero Gibbs heat has
kernel `span(Omega)`. For `0<=s<1` put

\[
 \sigma(s)=(1-s)\sigma+s|\Omega\rangle\langle\Omega|.
\]

This curve preserves (4), trace one, every mode's positive state weight,
and the protected heat kernel. Its largest eigenvalue is
`lambda(s)=lambda+s*(1-lambda)`; all other eigenvalues are multiplied by
`1-s`. If sigma has internal coordinate covariance, the entire curve has
it. Near zero the curve also extends to negative s by faithfulness and
the strict spectral gap above the protected ground line. Hence, with the
same beta and ground-zero convention,

\[
 {dB\over ds}(0)=-{1-\lambda\over\beta\lambda}<0.           \tag{8}
\]

Every point admits this strict descent. On this full class the thermal
price has infimum zero and no finite minimizer or stationary point. Its
infimum is approached as `s->1`; the boundary cyclic density has rank one,
so it is not a finite-temperature Gibbs density on the full carrier.
Indeed the complementary heat energies diverge. The feedback/rest terms
remain fixed only if that is part of the declared interface; if they are
fixed, the same descent holds for the existing complete bootstrap price.
No such curve with fixed other terms is asserted to be natively admitted.

Thus fixing the entire compatible AF trace and the constant zero vector
does not supply the missing stationary preparation law. The actual law
must constrain this state direction or provide the jointly varying price
terms. This result does not prescribe either remedy and does not exclude
all native preparation or all protected-zero subspaces.

## Full density refinement is an additional condition

The actual GNS isometry J retains the coarse algebra in a larger space.
Normalized density compatibility cannot mean
`sigma_coarse=J* sigma_fine J` for faithful full sigma_fine: if the
orthogonal complement is nonzero, positivity gives

\[
 \operatorname{Tr}(J^*\sigma_{fine}J)
 =1-\operatorname{Tr}((I-JJ^*)\sigma_{fine})<1.             \tag{9}
\]

In particular a full normalized compatible density cannot be obtained by
silently dropping or renormalizing that complement. A physical density
refinement may instead use a specified trace-preserving channel or a
retained larger state, but that is another owned map to construct. Neither
(4) nor the equality of visible traces supplies it. Equation (9) is a
complete obstruction for the stated normalized-compression interface,
not for all refinement channels or all native preparations.

The next native law must therefore identify the actual observable algebra,
the full prepared state or relevant weaker price data, and its retained
refinement. A trace-weight selector is unnecessary: (1) already forces the
trace. A selector for (6) cannot be inferred from that forcing. T0--T3,
all 44 dependency nodes, source/Ward, quantitative native contrast,
curved roots and original #310/#202/#317 terminals remain open.

## Proof and verification scope

The Lean capsule compiles 16 propositions, with only `propext`,
`Classical.choice` and `Quot.sound` in their transitive axiom union. It proves the infinite nonnegative-compatible-weight
classification, its parameter independence, the finite interval-width
identity, residual coefficient identities, and the nonzero scalar thermal
price derivative and its negative coefficient for cyclic mixing.
The application of this derivative to the complete matrix-state class,
matrix-unit classification, full GNS extension dimension,
all-size partial traces, covariance, positivity and equation (9) have
analytic proofs above. Exact matrix controls replay the actual carrier
and include cross-block coherences. The matrix/Gibbs statements are not
advertised as newly compiled Lean propositions.

The exact checker passes 1824 controls in 48 groups, rejects nine
executed mathematical mutants and twenty-one false scope ledgers, and pins
24 inputs. It tests finite-horizon intervals at eight starting levels,
full GNS densities of dimensions 13 and 34, all spectral projectors and
cross-block coherences, complex phase and nontrivial rotation covariance,
the literal 13-to-34 GNS embedding, and descent from both covariant and
noncovariant states in the full fiber. The universal conclusions come
from the analytic and Lean proofs, not extrapolation of those fixtures.
