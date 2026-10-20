# Positive native point states: complete refinement classification and volume boundary

Input: `60ebc9b6832ee2c12d08b5b3fdb3d3725e6feba5`.
Parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Status: complete classification of the stated positive point-state class and
its scoped physical-volume obstruction, pending CONTROL. **The full native
state/variation/action map, independent matter, physical Ward, nonlinear GR,
soundness, recovery and global closure remain OPEN.**

This examines the actual coordinatewise Role-phase projections, their dual
positive states and possible physical readouts. No projection, measure,
action or physical postulate is added to D0. It does not identify a state on
the point-observable algebra with a state on the much larger field space.

## 1. Actual objects and exhaustive scope of the positive-state class

The phase owner is `archivePhaseIndex n = Fin(n+2)`. Put L=n+2. Its actual
`archiveRGPhaseProjection` is

\[
 p_L:\{0,\ldots,L\}\to\{0,\ldots,L-1\},\qquad p_L(j)=j\bmod L.
                                                               \tag{1}
\]

The four-Role point carrier is the existing
`ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint n`, namely
`Role -> Fin L`, with four Roles. The coordinatewise product of (1) is the
refinement analyzed here. The flattened `ArchivePoints n = Fin(L^4)` and its
single modulo-L^4 projection are a **different diagram**, not an alternative
notation for this product projection.

A positive normalized real linear functional on all point observables is

\[
 \ell_L:\mathbb R^{X_L}\to\mathbb R,\quad
 f\ge0\Rightarrow\ell_L(f)\ge0,\quad\ell_L(1)=1,
 \qquad X_L=\{0,\ldots,L-1\}^{\mathrm{Role}}.                  \tag{2}
\]

Every such functional, with no diagonal-weight ansatz, is uniquely
\(\ell_L(f)=\sum_x\mu_L(x)f(x)\), where
\(\mu_L(x)=\ell_L(1_{\{x\}})\ge0\) and \(\sum_x\mu_L(x)=1\).
Indeed the point indicators form a basis and sum to one. These statements
are compiled for every finite point set. They also apply to the real
self-adjoint part of the actual complex `RolePhaseFunctionAlgebra`.

Compatibility means the actual dual of observable pullback:

\[
 \ell_M(f\circ P_{L,M})=\ell_L(f)\quad\text{for every }f,
 \qquad \mu_L=(P_{L,M})_*\mu_M.                              \tag{3}
\]

The equivalence with the weight equation, positivity and preservation of
total mass are compiled. Thus the class below is **all positive normalized
states of this point diagram**, not just the uniform or factorized ones.
Arbitrary correlations among the four coordinates are included.

There is a direct scalar Hodge interpretation, when that interpretation is
actually proposed. For the weighted scalar pairings
\(\langle f,f\rangle_L=\sum_x\mu_L(x)f(x)^2\), pullback isometry
for every f is equivalent to (3). Necessity follows by testing each point
indicator; sufficiency follows by summing along fibers. This equivalence
is compiled generically and specialized to the literal phase projection.
It is a criterion for a proposed physical scalar mass/volume map, not a
claim that the core already identifies (2) with spacetime volume.

The separately owned `Probability.FiniteArchiveMeasure.archiveStageMeasure`
is the same eight-atom rational cross at every n: its stage argument is
unused. Those actual facts are compiled. It is neither the uniform Role
grid measure nor the golden flattened-record measure.

## 2. Actual composition and the countable history space

Define \(c_L(j)=j\) for \(j<L\), and zero otherwise. The actual composite
of (1), for every M>=L, is

\[
 P_{L,M}(x)_r=c_L(x_r),\qquad c_L(c_M(j))=c_L(j).             \tag{4}
\]

An index j>=L is first sent to zero at its own phase step p_j and stays
zero. An index below L never changes. A single `j mod L` for a long jump
would be a changed map: at j=L+1 the true composite is zero but that shortcut
is one. The formula remains true on the cofinal physical sizes L in 4N,
provided the transitions are these actual composites.

The [published archive-record proof](https://github.com/gvakhrushev/d0_15/blob/af221e2fed92821c52afc88a5500774de8cd9a93/02_REGISTRY/research/A4D_NATIVE_ARCHIVE_RECORD_BRIDGE.md#5-the-coordinatewise-role-inverse-limit-has-a-different-exact-type)
already identified the history space. Here its exact type is compiled
against the real owner. A nonzero phase address j can never move again.
Every infinite history has the unique form

\[
 x_L=c_L(j),\qquad j\in\mathbb N,                            \tag{5}
\]

where j=0 codes the all-zero history. The code map is a compiled bijection;
the four-Role histories are a compiled countable finite product. This
point countability is reused, not presented as a new physical no-go by
itself. The new consequence is the full positive-state classification.

## 3. All compatible positive states, including correlations

**Theorem.** Every family satisfying (2)--(3) has a unique representation

\[
 \mu_L=\sum_{a\in\mathbb N^{\mathrm{Role}}}
               A_a\,\delta_{c_L(a)},\qquad
 A_a\ge0,\qquad\sum_a A_a=1.                                \tag{6}
\]

Conversely every such summable family defines a compatible positive state.
Here c_L acts coordinatewise. The result holds on every unbounded cofinal
subsequence with the actual composite maps, including L in 4N. It requires
neither coordinate independence nor strict positivity of finite-stage
weights. The following elementary proof does not invoke an unspecified
projective-measure theorem.

First consider one coordinate. For j>0, its mass is unchanged at every
level larger than j, since that fiber is a singleton. Denote it by b_j.
Nonnegativity gives \(\sum_{1\le j<L}b_j\le1\); therefore \(\sum_{j>0}b_j\le1\).
Set \(b_0=1-\sum_{j>0}b_j\). At level L the zero mass is
\(b_0+\sum_{j\ge L}b_j\), and every other mass is b_j. This proves (6)
in one dimension and its uniqueness, on any unbounded subsequence.

For four possibly correlated coordinates, apply that argument to each
marginal; denote its coefficients by \(b_{r,j}\). If
\(B_R=\{0,\ldots,R\}^{\mathrm{Role}}\), then, for L>R,

\[
 \mu_L(B_R^c)\le\sum_r\sum_{j>R}b_{r,j}=:\tau_R,
 \qquad \tau_R\longrightarrow0.                            \tag{7}
\]

For a fixed vector a and levels L>max a, compatibility implies
\(\mu_L(a)\ge\mu_M(a)\) when M>=L: a itself is one preimage and all other
preimage masses are nonnegative. Hence \(A_a=\lim_L\mu_L(a)\) exists.
For a finite box, passing to the limit in (7) gives
\(1-\tau_R\le\sum_{a\in B_R}A_a\le1\). Increasing R proves
\(\sum_a A_a=1\). For any fixed coarse x, use (3), split its preimage
into B_R and its complement, bound the latter by (7), and pass first to
M→infinity and then R→infinity. This gives exactly (6). It also proves
uniqueness. Conversely (4) and absolute convergence immediately give (3).

Thus positivity plus the actual refinement determines the **whole class**
to be probability mixtures of countably many persistent address histories.
No particular native probability or matter state is selected by this theorem.

## 4. Arbitrary point readouts still cannot recover smooth metric volume

Let Y be any compact metric space, in particular the physical four-torus.
Allow arbitrary deterministic maps R_L:X_L→Y; they need not preserve
coordinates, converge, or even be related at adjacent levels. From (6),

\[
 (R_L)_*\mu_L=\sum_a A_a\delta_{R_L(c_L(a))}.                 \tag{8}
\]

**Theorem. Every weakly convergent subsequence of (8) has a purely atomic
probability limit.** To prove it, enumerate the countable a's. Compactness
and a diagonal subsequence give a limit y_a for each corresponding point
R_L(c_L(a)). For a bounded continuous test, truncate the absolutely summable
series: the tail is at most its sup norm times \(\sum_{a\notin F}A_a\),
uniformly in L; the finite part converges. The weak limit is therefore
\(\sum_a A_a\delta_{y_a}\). Any originally convergent subsequence has this
same weak limit. Compactness is used only for the finite-coordinate
subsequence extractions; Y=the periodic torus satisfies it.

This includes arbitrary relabeling and moving placements. It also includes
positive probability reconstruction kernels whose support has diameter
at most \(d_L\to0\) around the corresponding R_L(x). Uniform continuity
bounds the difference on each continuous test by its modulus of continuity
at d_L, so their weak limits are the same. Small spatial correctors and
vanishing cell smearing do not change the result.

In contrast, a smooth nondegenerate metric in the declared compact class has

\[
 \nu_g=\frac{\sqrt{|\det g(y)|}\,dy}
                 {\int_{\mathbb T^4}\sqrt{|\det g|}\,dy}.    \tag{9}
\]

Its density is bounded and positive. A point has zero mass, as the mass of
a ball of radius d is bounded by a constant times d^4. Thus (9) is nonatomic
and cannot be a limit in (8). At least one A_a is positive because they sum
to one, whereas (9) has no positive atom.

This is a **complete obstruction for compatible positive point states and
deterministic or shrinking local positive volume readouts** on this diagram.
It is stronger than a failure of the uniform mesh weights or one chosen
coordinate map. It is not a completeness theorem for all native field
states, nonlocal observables, actions or other refinement diagrams.

For the direct placement R_L(x)=x/L mod 1 there is an even sharper result:
each fixed c_L(a)/L tends to the origin, so (8) tends to the single atom
delta_0. Arbitrary four-coordinate correlations do not avoid this collapse.

## 5. Approximate compatibility: total error, not one-step smallness

For finite probability measures use
\(\mathrm{TV}(\mu,\nu)=\tfrac12\sum_x|\mu(x)-\nu(x)|\).
Pushforward and positive probability kernels contract TV: sum the absolute
value of each fiber sum, apply the triangle inequality, and then sum the
disjoint fibers. No rank or continuum regularity assumption is involved.

Suppose the **total composed** defect satisfies

\[
 \sup_{M\ge L}\mathrm{TV}\bigl(\mu_L,(P_{L,M})_*\mu_M\bigr)
                  \le\epsilon_L,\qquad\epsilon_L\to0.      \tag{10}
\]

Then all the conclusions about possible weak volume limits still hold.
For each fixed L the projected measures lie in a compact finite simplex.
A diagonal subsequence as M→infinity gives limits \(\widetilde\mu_L\)
simultaneously. Their compatibility follows from (4) and the finite linear
pushforward maps; they remain positive and normalized. Closedness of the
finite TV bound gives \(\mathrm{TV}(\mu_L,\widetilde\mu_L)\le\epsilon_L\).
Apply (6)--(8) to the compatible family. The difference on a bounded test,
even after a varying readout/kernel, is at most
\(2\epsilon_L\|f\|_\infty\), tending to zero.

In particular, if consecutive actual-step defects are e_L and
\(\sum_L e_L<\infty\), contraction and telescoping give (10) with
\(\epsilon_L=\sum_{k\ge L}e_k\). The same argument works for any declared
cofinal sequence, including L in 4N, using its actual composite steps.
The total error must include recording and reconstruction errors when they
are used to assert (10).

**This TV premise is not inferred from the requested action-contrast
estimate.** A contrast bound on one specified observable does not imply
compatibility of all positive point states. Conversely a proposed state or
scalar-volume reconstruction satisfying (10) is obstructed before its
Einstein action or source is considered. The distinction keeps this proof
from replacing the original native contrast obligation by a stronger gate.

## 6. Direct physical readout: smooth weak compatibility already fails

For the direct placement, the obstruction does not need the strong TV
premise (10). There is an exact continuum expression for the actual
L-to-2L composite. On the circle represented by t in [0,1), define

\[
 T(t)=\begin{cases}2t\pmod1,&0\le t<1/2,\\0,&1/2\le t<1.\end{cases}
 \qquad \mathcal T(y)_r=T(y_r).
\]

T is continuous on the circle: the left limit at 1/2 is 1, which is the
same circle point as zero; the endpoints also agree. It is 2-Lipschitz
in the circle distance. For every actual grid point x,

\[
 R_L(P_{L,2L}(x))=\mathcal T(R_{2L}(x)).
\]

The coordinate identity is compiled with the actual composite cap formula.
Suppose the physical placed measures \((R_L)_*\mu_L\) converge weakly to
some probability nu, and the total native refinement error tends to zero
on **each fixed smooth periodic test**:

\[
 \ell_L(f\circ R_L)-\ell_{2L}(f\circ R_L\circ P_{L,2L})\to0.
\]

Continuity of the collapse map gives
\(\int f\,d\nu=\int f\circ\mathcal T\,d\nu\). Smooth periodic tests
determine a measure here. Explicitly, convolution with the product of
the one-dimensional Fejer kernels
\(K_N(t)=N^{-1}(\sin(N\pi t)/\sin(\pi t))^2\) gives trigonometric
polynomials. Each kernel is nonnegative and has integral one by its finite
Fourier expansion. Outside circle distance delta it is at most
\(1/(N\sin^2(\pi\delta))\). Splitting the convolution into a delta
neighborhood and its complement, uniform continuity of a continuous
function on the compact torus proves uniform convergence. Equality on
smooth tests therefore extends to continuous tests. Thus nu is invariant under
\(\mathcal T\). Its **only invariant probability is delta_0**. Indeed,
every point reaches zero after finitely many iterates: a positive circle
coordinate doubles until it enters [1/2,1) and is then collapsed. For a
continuous test, the bounded functions \(f\circ\mathcal T^k\) tend
pointwise to f(0). The expectation limit follows by truncating the sets
with absorption time greater than k; these sets decrease to the empty
set and their probabilities tend to zero. Invariance proves the claim.

For a smooth normalized metric density \(0<m\le\rho\le M\), a fixed
smooth witness gives an explicit positive gap, without invoking TV or
all-test norm convergence. The box [1/2,1)^4 contributes an atom at zero
of mass at least m/16 to \(\mathcal T_*\nu\). Put

\[
 f_N(y)=\prod_{r=0}^3\cos^{2N}(\pi y_r),\qquad
 b_N=4^{-N}{2N\choose N}.
\]

This probe is smooth and periodic, lies in [0,1], and equals one at zero.
Its ordinary torus mean is \(b_N^4\). Expanding the even cosine power
shows that only its zero Fourier coefficient survives the integral.
The recurrence \(b_{N+1}=b_N(2N+1)/(2N+2)\) gives
\(b_N^2\le1/(N+1)\) by induction, since
\((2N+1)^2(N+2)\le4(N+1)^3\); the polynomial inequality is compiled.
Choose a fixed N with \((N+1)^2\ge32M/m\). Then

\[
 \int f_N\,d(\mathcal T_*\nu)-\int f_N\,d\nu
       \ge m/16-M/(N+1)^2\ge m/32>0.
\]

Consequently even o(1) total refinement errors on all fixed smooth physical
volume probes are impossible for a nondegenerate smooth metric limit.
Uniformly o(1) perturbations of the direct placement and shrinking positive
cell reconstructions preserve the conclusion, by uniform continuity and
the Lipschitz bound for T. Corrected metrics that recover the same volume
limit are included. No exact-sampling gate is assumed.

This weaker test condition is a requirement on the proposed **physical
volume/readout arrow**. It is still not automatically a consequence of an
Einstein action-contrast bound for a different observable. For arbitrary
nongeometric point placements, Section 4 uses exact state compatibility
or Section 5's total TV hypothesis; it does not silently extend the present
weaker direct-placement theorem to those maps.

## 7. Exact smooth controls and accumulated defects

Uniform Role-grid probabilities are a nonempty diffuse recovery family;
they fail the native compatibility. In one coordinate their one-step TV
defect is

\[
 e_L=\frac{L-1}{L(L+1)}=O(L^{-1}),                           \tag{11}
\]

although the composed L-to-2L defect tends to 1/2. In four coordinates the
exact defect from level M to L is

\[
 \frac12\sum_{k=0}^4{4\choose k}(L-1)^{4-k}
       \left|\frac{(M-L+1)^k}{M^4}-\frac1{L^4}\right|.       \tag{12}
\]

For M=L+1 it is at most four times (11), hence also O(1/L). For M=2L it
tends to 15/16. More directly, the **fixed smooth periodic** probe

\[
 f(y)=\prod_{r=0}^3(1-\cos(2\pi y_r)),\quad0\le f\le16      \tag{13}
\]

has mean one on every uniform L-grid with L>=2. Its mean on the coarse
placement of the actually projected M-grid is exactly (L/M)^4: f vanishes
whenever a coordinate is collapsed to zero, and the remaining sum
factorizes. Thus the L-to-2L discrepancy is exactly 15/16 at every L,
including every L in 4N. No discontinuous test or differentiated asymptotic
error is used. The geometric-series identity for roots of unity proves
the sums in every size; exact finite controls independently test them.

There is also a genuinely curved fixed metric control. Let

\[
 \eta=\operatorname{diag}(1,-1,-1,-1),\quad
 q(y)=1+\tfrac1{10}\cos(2\pi y_0),\quad g=q\eta.             \tag{14}
\]

It is periodic, Lorentzian and uniformly nondegenerate; its volume density
is q^2, with total volume 201/200. Its scalar curvature at zero, in the
consumed owner sign convention, is \(-120\pi^2/121\ne0\).
The certificate checks all second-jet Ricci contractions and the sign.
On L in 4N the sampled normalized volume is exact. For the fixed smooth
probe \(v(y)=1-\cos(2\pi y_1)\), its expectation is one, while projecting
the level-2L measure by the actual composite and using the coarse placement
gives 1/2. The density depends only on coordinate zero, so it factors out
of this calculation.

If corrected metrics Q_L converge uniformly to the samples of (14),
uniform nondegeneracy makes their determinant-volume probabilities differ
by o(1) in TV. Pushforward contraction preserves that error. The same
smooth discrepancy is therefore 1/2+o(1). This explicitly protects the
distinction between the old exact-sampling gate and the allowed small
metric corrections: such corrections do not repair this particular volume
arrow. We do not assert uniform metric convergence from an unspecified
weaker topology, or infer a joint field equation from this volume control.

## 8. Protected exceptions and actual remaining interface

* Uniform sampled metrics have diffuse limits and adjacent error O(1/L).
  They disprove extending the theorem to merely vanishing adjacent errors.
* Every finite prefix can be made compatible by projecting a uniform top
  measure downwards. Changing the top changes the earlier state; this is
  not one fixed infinite compatible family with diffuse recovery.
* An alternative dyadic projection `j -> floor(j/2)` has compatible uniform
  measures and diffuse physical volume under ordinary nested placement.
  This is an exact countercontrol to a general finite-grid no-go, not a
  replacement of the native projections. A long-jump single modulo is
  likewise not their actual composite.
* A macroscopic probability kernel can send even one atom to any chosen
  diffuse target. Such a kernel supplies the target distribution as input;
  it violates the shrinking-support condition and is not constructed here
  as a native physical law. Nonlocal physical readouts need their own owner.
* A positive definite **nonlocal quadratic matrix** need not define a
  positive state by pairing with the constant function: the matrix
  `[[1,-2],[-2,5]]` is positive definite but has row sums (-1,3).
  Positive definiteness alone cannot supply premise (2).
* Field configurations, signed functionals without the required variation
  bounds, and the distinct flattened archive diagram are outside the class.
  The already constructed full-support golden record measure on that
  flattened diagram is retained. Point countability does not eliminate
  continuous field degrees of freedom or prove a full-core obstruction.

The smallest consequence for the gravity programme is precise: a proposed
physical volume or scalar Hodge state cannot simultaneously use this
coordinate point algebra, these exact (or totally vanishing-TV-error)
refinement transitions, and deterministic/local positive recovery of a
smooth nondegenerate metric volume. A different owned state/readout map
or an explicitly weaker and sufficient physical-observable refinement law
must be proved. The proof does not introduce either as a new selector.

## 9. Verification

The research capsule checks the actual phase projection, composite history
law, bijective history coding and countability of the real four-Role
histories, the doubled coordinate readout and the smooth-peak recurrence
bound. It also compiles the exhaustive finite positive-state reduction,
dual pushforward identities, scalar quadratic-pairing equivalence and the
literal eight-atom stage facts. Only standard Lean axioms are permitted.
The infinite positive-state classification, arbitrary-readout atomic limit,
total-error extension, smooth-test limit obstruction and curved quantitative controls are analytical
proofs above, not advertised as compiled measure-theoretic limit theorems.

The capsule compiles 25 propositions with 25 transitive D0 source pins.
The exact checker and immutable receipt replay 92 grouped controls. They verify
actual composites, positive correlated mixtures, state/pairing duality,
uniform and curved weak defects, TV formulas, accumulated error controls
and the explicit exceptions. Four hostile ledgers separately falsify the
atomic-limit class, the curved gap, the adjacent-error boundary and the
direct smooth-test terminal; immutable replay rejects each. Counts and
transitive source pins are recorded in the certificate and compiler receipt.
Original #310/#202/#317 terminals,
claim/release labels and supported Lean owners remain unchanged.
