# Nonlinear log-det source: exact finite image and the missing physical map

Input: `32e7a1da7c191ef8567647d56d69995b475a84bb`.
Parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Status: finite source-image classification and scoped contrast obstruction,
pending CONTROL. **Native metric realization, independently generated matter,
physical Ward, nonlinear GR, soundness, recovery and global closure remain OPEN.**

This tests the already specified matrix/scalar feedback functional
`-log det(I-zF)`. It does not install that functional, a graph substitution,
a profile, a coupling or a source as a new physical law. The distinction is
essential: the formula has nonlinear responses, but its supplied operator
and admissible physical variations still need their own native owner.

## 1. What the existing owners actually prove

`Matter.HiggsLogdetStationary` specifies the rank-two scalar formula

\[
 S_z[f](t)=-2\log(1-zf(t)).                                    \tag{1}
\]

Its supported Lean result is a rational coefficient relation and a
stationarity equivalence for supplied `D,z,fprime,Sprime`. Its concrete
profile is `t/(1+t^2)`. The existing Python certificate differentiates that
profile and one actual 2-by-2 matrix; this is not an all-matrix Jacobi theorem.
The research capsule now proves the **real `HasDerivAt` statement**

\[
 D S_z[f](x)=\frac{2z f'(x)}{1-zf(x)}                          \tag{2}
\]

from an actual derivative of f and a nonzero denominator. It proves the
derivative and rational-cast binding of the existing concrete profile too.
The physical real-log branch below always has positive argument.
The identity between (1) and the rank-two scalar matrix determinant is
compiled, so its factor two is explicit.

`Cosmology.feedback_variation_universal_source` combines three supplied
Boolean flags; it contains no matrix, derivative or local stress tensor.
The actual proposition of
`HiggsRadialInstabilityBoundary.higgs_radial_dynamics_maximality_nogo_owner`
contains projector identities, the Pauli-X orbit, noncommutation and a trace.
These are positive finite facts. That proposition contains no quantification
over radial actions and cannot serve as a completeness theorem excluding
every radial dynamics. All three owner types are printed in the capsule.

### Arbitrary profiles do not select an action

For any real-valued function U on any state set and any fixed `z!=0`, put

\[
 f_U(x)=\frac{1-\exp(-U(x)/2)}z.
 \quad 1-zf_U(x)=\exp(-U(x)/2)>0,
 \quad -2\log(1-zf_U(x))=U(x).                               \tag{3}
\]

All of (3) is compiled for arbitrary U. If U is smooth, so is f_U; if
`z>0,U>=0`, it also satisfies `0<=f_U<1/z`. Thus even that positive profile
restriction does not choose a potential. For example, both `U(s)=s` and
`U(s)=(s-1)^2` on `s>=0` have profiles of this form; only the second has a
stable nonzero radial minimum. It can encode a quartic in a scalar amplitude
when `s=|Phi|^2`. This is an input-dependence control, not a newly chosen
Higgs action or a proof that the core owns either profile.

In particular, the existing certificate's nonzero sixth coefficient for
the special profile `f(t)=t` cannot exclude every log-det profile from
having a quartic composite. Conversely, encoding an Einstein action by
(3) would merely put that action into f; it supplies none of the required
state, variation, matter or refinement maps.

## 2. Noncommuting conjugation alone remains invisible

For every invertible finite real matrix U and every F,

\[
 \det(I-zUFU^{-1})=\det\bigl(U(I-zF)U^{-1}\bigr)
                 =\det(I-zF).                              \tag{4}
\]

This identity and the resulting log-det equality are compiled in every
finite dimension. No commutation assumption on U and F is needed. A
nonconstant projector orbit can therefore have exactly constant feedback
action. For the actual rational toral matrix `T=[[0,1],[1,-1]]` and owned
rank-one projector P0, the exact control checks `T P0 T^-1 != P0` but equal
feedback determinants for all scalar z.

This also applies to a similarity-equivariant operator construction from
simultaneously transformed inputs. If another operator or projector is held
fixed and the construction ceases to be similarity-equivariant, (4) does
not apply. An explicit fixed detector control distinguishes the two cases.
No claim about the absence of all radial dynamics follows from (4).

## 3. Full finite derivative, source and Ward identity

Let F be a symmetric real matrix and restrict to the open domain

\[
 H=I-zF>0,\qquad R=H^{-1},\qquad S(F)=-\log\det H.            \tag{5}
\]

For a symmetric variation V, multiplicativity of the determinant gives
`det(H-tzV)=det(H) det(I-tzRV)`. In the permutation expansion of the second
determinant, its linear coefficient is `-z tr(RV)`; every nonidentity
permutation moves at least two indices. Differentiating the scalar log
therefore proves in every dimension

\[
 DS(F)[V]=z\operatorname{tr}(RV),\qquad
 D^2S(F)[V,W]=z^2\operatorname{tr}(RV RW).                    \tag{6}
\]

The second identity follows by differentiating `H R=I`, giving
`D R[V]=z R V R`. No finite numerical experiment is used for these
all-size identities. For V=W, the second trace is
`||R^(1/2) V R^(1/2)||_HS^2`, hence strictly positive unless V=0.

Since H commutes with F, its inverse R commutes with F. Cyclicity of the
trace then gives the exact simultaneous-conjugation identity

\[
 DS(F)[KF-FK]=z\operatorname{tr}(R(KF-FK))=0.                 \tag{7}
\]

The generic trace identity with its explicit commutation hypothesis is
compiled. This is a finite conjugation Ward identity, not a physical
divergence law. A physical pullback `F(g,matter)` and its local derivative
would be needed before (6) is metric stress or (7) is a spacetime Ward law.

## 4. A shape-sensitive graph binding with a complete source image

Use a connected finite simple graph with at least two vertices. On the
actual four-Role graph this is the existing conductance variation map.
For an undirected edge e={u,v}, write `b_e=e_u-e_v`, `E_e=b_e b_e^T` and

\[
 F(w)=c\sum_e w_eE_e,\quad c>0,\quad k=zc\ne0,\quad
 H(w)=I-k\sum_e w_eE_e>0.                                   \tag{8}
\]

The weights w are unrestricted real coordinates on this open domain.
The owned four-Role scale is `c=L^2`. Its off-diagonal entries and compensating
row sums bind (8) to `ArchiveLocalLaplacianVariation.forwardMatrix`.
**Substitution of this operator into the feedback slot is the class being
tested, not a claim that the core already selected that substitution.**

The exact derivative and its Jacobian are

\[
 r_e(w)=\partial_{w_e}S=k\,b_e^TRb_e,\qquad
 J_{ef}(w)=k^2(b_e^TRb_f)^2.                                \tag{9}
\]

Every edge response has the sign of k. The source equals `z * edgeStressReadout(c,R_uu,R_vv,R_uv)` in the owned
normalization. Positivity of the inverse and this actual readout, including
its specialization to every real four-Role edge, are compiled, as is nonvanishing for either nonzero coupling sign. Consequently
the **full free unsourced edge gate has no solution** in class (8).
This is not an assertion that all sourced or constrained fibers are empty.

### Independent compatibility criterion and existence theorem

Let `W=1^perp`, let P0 project onto constant vectors, and let Q project onto W.
For a prescribed response r, put `q=r/k`. Define the following condition,
using only linear edge tests and positivity:

\[
 \exists\ C=C^T\text{ on }W,\ C>0:\quad
       b_e^TCb_e=q_e\quad\text{for every edge }e.             \tag{10}
\]

**Theorem.** A real weight vector w satisfying (8) and (9) exists if and
only if (10) holds. When it exists, it is unique. Criterion (10) does not
assume a local inverse or a stationary root; it is a positive-definite
completion problem with linear prescribed data.

**Necessity.** Every graph Laplacian kills constants, so `H 1=1` and
`R=P0+C` with C positive definite on W. Equation (9) is exactly (10).

**Sufficiency.** In the affine feasible set of (10), maximize

\[
 \Phi(C)=\log\det_W C-\operatorname{tr}_W C.                 \tag{11}
\]

This is a finite construction of the inverse, not an additional physical
action. It has an interior maximizer. Indeed, the unweighted graph
Laplacian `L_G=sum E_e` has kernel exactly the constants: its quadratic
form is the sum of squared edge differences, and connectedness makes
zero differences constant. Its restriction to W has a positive smallest
eigenvalue gamma. For every positive-semidefinite feasible C,

`gamma tr C <= tr(L_G C)=sum q_e`.

Thus the closed feasible set is bounded. A positive definite witness is
assumed in (10). Along a sequence tending to a singular boundary, at least
one eigenvalue tends to zero while all others are uniformly bounded, so
`Phi -> -infinity`. A maximizing sequence therefore has a positive definite
limit by finite-dimensional compactness. This verifies the existence and
interiority hypotheses; they are not supplied as extra stationary data.

For every symmetric tangent D with `tr(E_e D)=0`, first variation of (11)
at that maximizer gives `tr((C^-1-I_W)D)=0`. Finite-dimensional orthogonal
complement duality gives coefficients beta with

`C^-1-I_W=sum beta_e E_e|W`.

Extend by the constant mode and set `w_e=-beta_e/k`. Then
`H=P0+C^-1=I-k sum w_e E_e>0` and (9) holds. Independence of the E_e
follows from their distinct off-diagonal entries. Finally, (6) gives a
strictly positive Hessian on every nonzero conductance direction. The
domain in (8) is convex, so integration along any segment makes its
gradient injective. This proves uniqueness without discarding a gauge mode.

The theorem includes all four-Role sizes and all supplied compatible edge
sources in this precise signed-conductance class. It does not derive r
from an action of independent matter fields.

### Quantitative range, with its required bounds

If `m I <= H(w) <= M I`, `0<m<=M`, the previous exact source quotient gives

\[
 \delta w^T J\delta w
  =k^2\|R^{1/2}B(\delta w)R^{1/2}\|_{HS}^2
  \ge \frac{2k^2}{M^2}\|\delta w\|_2^2,\qquad
 \|J^{-1}\|\le\frac{M^2}{2k^2}.                             \tag{12}
\]

Here `B(w)=sum w_e E_e` and `B^*B=2I+A^T A`, with A the unsigned incidence.
The lower bound holds on every simple graph. On the four-Role graph with
`L>=3`, the upper bound is `18k^2/m^2`; at L=2 it is `10k^2/m^2`.
These follow by diagonalizing R in the Hilbert--Schmidt norm and using the
complete counting Gram spectrum already proved in
[the source quotient](A4D_NATIVE_EDGE_SOURCE_QUOTIENT.md).
The same lower bound integrated on a segment with the stated common M
gives the corresponding Lipschitz inverse estimate. Uniformity in h needs
native bounds on M/|k|; finite invertibility alone does not supply them.

## 5. Exact controls against false existence or uniformity claims

### Three vertices: complete explicit nonlinear inverse

For the complete three-vertex graph, `k=1`, prescribe edge responses
`r_01=r_12=1`, `r_02=t`. Let P_a project onto `(1,0,-1)` and P_b onto
`(1,-2,1)`. The unique possible centered completion is

\[
 R=P_0+\frac t2P_a+\frac{4-t}6P_b,\qquad
 H=P_0+\frac2tP_a+\frac6{4-t}P_b.                            \tag{13}
\]

It is admissible exactly when `0<t<4`. Direct multiplication verifies
`HR=I`; all three responses follow from (9). The actual weights are

\[
 w_{01}=w_{12}=\frac13-\frac2{4-t},\qquad
 w_{02}=\frac13-\frac1t+\frac1{4-t}.                          \tag{14}
\]

The determinant of the full response Jacobian is
`t^3(4-t)^3/32`. Its inverse on the response tangent `(0,0,1)` equals
the derivative of (14). In particular

\[
 \|J^{-1}\|\ge\frac2{(4-t)^2}\longrightarrow\infty.
                                                                    \tag{15}
\]

Every `t<4` near 4 is an actual nonempty sourced root with bounded,
strictly positive responses. The limiting source t=4 lies on the boundary
and has no positive definite completion; t>4 is outside the source image.
The degeneration is a loss of the uniform preparation bound, not a finite
rank/gauge ambiguity. Nonnegative conductance is a stricter class: for
example t=1 has negative weights and does not belong to it.

### Positive edge components are insufficient on the real Role graph too

In any positive definite C metric, along a four-cycle the length of one
edge is strictly less than the sum of the other three lengths. The three
successive difference vectors are linearly independent; positive
definiteness preserves that independence, excluding equality in the triangle
inequality. Every actual four-Role carrier with L>=4 contains such a
coordinate square. Assign q=1 on three edges and q=9 on the fourth.
All components are positive, but (10) is impossible. The assignment can
give positive values to every other edge as well; the four-edge obstruction
already suffices. This prevents source fitting from masquerading as a
general solution theorem.

### Free variations, sign and domain are load bearing

On a symmetric three-vertex graph at uniform weight, all components of r
coincide. Under the added constraint `sum w=constant`, the source pairs
to zero with every allowed tangent even though each component is nonzero.
This is a genuine constrained stationary example; such a constraint is
not silently attributed to the existing native owner.

For the invertible indefinite matrix `H=diag(1,-1)`, the edge vector
`(1,-1)` has zero inverse quadratic form. The positive-domain conclusion
cannot be extended merely from invertibility. At z=0 every derivative
vanishes. Replacing F by `-c B(w)` reverses the first-variation sign and
changes its domain. The signed source-image theorem covers either nonzero sign of k through q=r/k; it does not choose that sign.

For the unit-conductance binding of the actual four-Role map at L in 4N,
the alternating character has Laplacian eigenvalue `16 L^2`. All eigenvalues
are at most this value, by the squared edge-difference form, and it is
attained. Hence its positive resolvent domain is exactly

\[
 0<z<\frac1{16L^2}.                                        \tag{16}
\]

A fixed positive z cannot remain in that domain on an unbounded refining
sequence. A scale-dependent z_h, a normalized operator, a different sign
or different weights are protected alternatives needing their own owner.
For fixed negative z, the same unit-conductance matrices instead have
`I <= H <= (1+16|z|L^2)I`. Equation (12) then gives the actual uniform
finite inverse bound `(16+1/(16|z|))^2/2` for all L in 4N. This positive
range control is retained; the unsourced gate is still empty. No continuum
contrast obstruction is inferred from (16) without those choices and the
one-calibration requirement being fixed.

## 6. Convex prepared-contrast obstruction beyond quadratic actions

The first affine-profile obstruction extends to every differentiable
jointly convex action on a convex native state domain, with affine metric
fibers and the **full** auxiliary Euler gate. Assume independently that
stationary preparations exist in those fibers on both published curved
metric pencils and all required endpoints. Convexity and zero auxiliary
first variation make every such preparation a global fiber minimum.
Their common value F_h(q) is convex: a convex combination of two minimizing
states is feasible at the corresponding affine combination of metric data,
so its action bounds the minimum there from above by the same combination
of the two minimum values. No unique auxiliary state or uniform inverse
is required.

For a convex function on one pencil, every centered secant
`[F_h(s+epsilon)-F_h(s-epsilon)]/(2 epsilon)` is nondecreasing in s.
An elementary proof applies the two convex interpolation inequalities
to the interior points `s1+epsilon` and `s2-epsilon` of the common outside
interval `[s1-epsilon,s2+epsilon]` and adds them. This works even when
the two secant intervals overlap.

Consequently the quantitatively specified transfer
`|a^-1 Delta I_native-Delta I| <= C_(s,V) h`, with fixed `a!=0`,
`epsilon=h^(1/3)` and total recording/refinement errors included, would
give pointwise convergence of those secants to `a DI(g_s)[V]`.
The limit preserves their monotonicity. The already owned two probes at
the same smooth genuinely curved base have Einstein second variations
`-12 pi^2` and `+12 pi^2`. One sign contradicts each sign of a.
The precise pencils, 24-row preparation and ten packed metric conventions
are consumed unchanged from
[the published affine proof](A4D_NATIVE_AFFINE_PROBE_NOGO.md), Sections 3--5.
No error estimate is differentiated. The quantitative normalized error is
still `O_(s,V)(h^(2/3))`.

**Thus nonquadratic log-det dependence does not repair the transfer in
the full convex affine-fiber class.** By (6), positive log-det terms with
affine matrix inputs satisfy joint convexity on their positive domains;
affine prescribed-source subtraction preserves it. This does not assert
existence of their auxiliary fibers, or exclude nonlinear metric input
maps, nonlinear constraints, nonconvex domains/actions, changing the probe
class, or uncontrolled approximate roots. Equation (3) explicitly protects
arbitrary nonlinear supplied profiles from this stronger obstruction.

## 7. Actual coordinate-support obstruction and a corrector exception

The preceding finite inverse cannot replace the metric-operator map. For
the actual four-Role nearest-neighbor conductance owner and **direct nodal
sampling** into the fixed coordinate placement, there is a separate exact
obstruction, independent of weights, coupling, positivity or smoothness of
the prepared conductances.

At a site x, take two distinct Roles r,s and phase functions f,g with
`f(x_r)=g(x_s)=0`. The sampled product `psi(y)=f(y_r)g(y_s)` vanishes at x
and at every nearest neighbor: a neighbor changes only one Role. Every
matrix in the actual `LocalLaplacianVariation` consequently satisfies

\[
 (D\psi)(x)=0.                                               \tag{17}
\]

The neighbor statement, (17), and its binding to the literal
`forwardMatrix n w` are compiled for every n and every w. This is stronger
than a Taylor argument with smoothly converging weights.

There is also an exact weak-form obstruction. For any functions u of only
coordinate r and v of only coordinate s, r!=s,

\[
 u^T F(w)v=c\sum_{e=\{x,y\}}w_e
          (u(x)-u(y))(v(x)-v(y))=0.                          \tag{18}
\]

Every edge term vanishes. Thus any mesh normalization of this bilinear
pairing is zero, even for signed, divergent or rapidly oscillating weights.
This statement uses the actual local operator and exact sampled fields;
it is not an inference from an entrywise continuum limit.

For an explicit smooth genuinely curved physical control, let
`eta=diag(1,-1,-1,-1)`, `B=I+(1/2)e_01`, `bar_g=B^T eta B`, and

\[
 q(y)=1+\tfrac1{10}\cos(2\pi y_0)\cos(2\pi y_1),\quad
 g=q\bar g,\quad u=\sin(2\pi y_0),\quad v=\sin(2\pi y_1).
                                                                    \tag{19}
\]

Here `9/10<=q<=11/10`, `det bar_g=-1`, and `bar_g^{01}=1/2`.
The metric is Lorentzian by invertible congruence, periodic, smooth and
uniformly nondegenerate. Its scalar Dirichlet bilinear form is

\[
 \int_{\mathbb T^4}\sqrt{|g|}\,g^{ab}\partial_a u\partial_b v
   =\frac{\pi^2}{20}\ne0,                                  \tag{20}
\]

because `sqrt|g| g^{01}=q/2` and each squared cosine has mean 1/2.
At zero, its owner-sign scalar curvature is `30 pi^2/121 !=0`.
This follows from the constant-background conformal formula
`R_standard=-3 q^-2 bar_g^{ab} q_ab+(3/2)q^-3 bar_g^{ab}q_a q_b`:
the first derivatives vanish there, while
`bar_g^{00}+bar_g^{11}=-1/4` and
`q_00=q_11=-2 pi^2/5`. The exact certificate checks the inverse metric,
determinant, every second-jet Ricci contraction at this point and (20).
It also checks the pointwise scalar wave response on u*v, which is
`40 pi^2/11` while (17) is zero.

Equations (18)--(20) exclude the proposed scalar metric-operator/Dirichlet
map on this class even in the weak bilinear sense. This is conditional on
using that operator and the direct field readout. It is not by itself a
NO-GO for another action observable, another physical coordinate placement,
a larger stencil, or prepared fields with nonnegligible corrector energy.

### O(h) field corrections can defeat the direct-readout obstruction

The exception is exact, not an appeal to unspecified homogenization. In a
periodic two-Role cell of any even length L>=4, give both forward coordinate
edges from a site x weight 1 when `x_0+x_1` is even and weight 4 when it is
odd. These are unambiguous undirected edges at L>=4. For a prescribed
affine edge cocycle p=(p0,p1), minimize the ordinary positive edge energy
over a periodic corrector chi. With chi_even=0 and chi_odd=t, its mean is

\[
 E(p,t)=\tfrac12\{(p_0+t)^2+(p_1+t)^2
              +4(p_0-t)^2+4(p_1-t)^2\}.
                                                                    \tag{21}
\]

At `t=3(p0+p1)/10`, the divergence vanishes at **every** vertex:
on an even site it is `-3(p0+p1)+10t`, and on an odd site its negative.
Thus the solution is stationary under all periodic corrector variations,
not merely under the parity ansatz. Positivity and connectedness make it
the global minimum, unique up to the constant potential kernel. Its
effective quadratic form is

\[
 E_{\min}(p)=\frac{41}{20}(p_0^2+p_1^2)-\frac9{10}p_0p_1,
 \qquad A_{01}=-\frac9{20}\ne0.                             \tag{22}
\]

The other two Roles can have unit weights and zero corrector differences,
giving the same exact construction on the real four-Role graph. The
physical field correction is `h chi`, hence uniformly O(h), but its edge
derivatives and the mixed bilinear response in (22) do not vanish.
The certificate tests the full cell divergence and all edge energies at
L=4,8,12, including the four-Role L=4 case. This protects the distinction
between small values and small derivative/energy errors.

The affine cocycle p is fixed boundary data of this explicitly stated
cell problem. This is not a periodic zero-source solution for an
unconstrained scalar field, not a native physical preparation map, and
not a coupled Einstein solution or a homogenization theorem. It proves
that a broader obstruction cannot simply assume that O(h) field corrections
preserve (18). Such a preparation would need its own native owner and
quantitative action/refinement estimates. The earlier convex-profile
obstruction still applies if its own full hypotheses hold.

## 8. Flat calibration excludes a broader bounded nonlinear preparation class

There is a further obstruction for the **bare** graph log-det action that
does not require affine metric readouts, smooth variation in the spatial
coordinate, or an auxiliary Euler gate. It also allows arbitrary mesh
couplings and normalization. Its hypotheses on the native map must be
checked rather than inferred from the log-det formula.

Let `L_h(w)=sum w_e E_e`, `L_h^0=sum E_e`,
`S_h(w)=-log det(I-k_h L_h(w))`, and let gamma_h be any scalar normalization.
Assume the curved-probe endpoint preparations satisfy, uniformly in h,

\[
 0<m\le w_{h,e}^\pm\le M,\qquad
 \|w_h^+-w_h^-\|_\infty\le C_V\epsilon_h.                    \tag{23}
\]

All matrices are on their positive resolvent domains. The coupling k_h
may change size or sign; k_h=0 is a zero-action case. Assume two **fixed
flat metric probe experiments** have actual prepared uniform conductances
with ordered endpoint values in scalar intervals above M and below m,
respectively. Each interval's width is at least `c epsilon_h`, `c>0` fixed,
and its endpoints stay strictly above M or below m for small h. All these
flat preparations are in the positive domain. For example, a *specified*
inverse-metric rule `w(q eta)=1/q` has this property on two appropriate
constant conformal metric pencils; this example does not select that rule
as a native law.

**Theorem.** If the normalized native contrasts on those flat experiments
tend to zero after division by epsilon_h, then the normalized native
contrast on every curved preparation obeying (23) also tends to zero.
Thus this bare class cannot satisfy the requested calibrated Einstein
contrast transfer wherever its continuum Einstein variation is nonzero.

**Proof.** First suppose k_h>0. Put

`D_h^+=k_h tr((I-k_h M L_h^0)^-1 L_h^0)`.

For every w in the endpoint box, `L_h(w)<=M L_h^0`, so
`(I-k_h L_h(w))^-1 <= (I-k_h M L_h^0)^-1`. All edge derivatives have the
same sign by (9); hence their absolute sum is at most `D_h^+`.
The upper flat interval lies above M. Its scalar derivative is everywhere
at least `D_h^+`, so the absolute flat action difference is at least
`c epsilon_h D_h^+`. Its assumed vanishing contrast forces
`|gamma_h| D_h^+ ->0`.

For k_h<0, write a_h=|k_h| and put

`D_h^-=a_h tr((I+a_h m L_h^0)^-1 L_h^0)`.

Now `L_h(w)>=m L_h^0` gives the same upper bound `D_h^-` for the absolute
sum of edge derivatives. The lower flat interval lies below m, so its
derivative magnitude is everywhere at least `D_h^-`; again
`|gamma_h| D_h^- ->0`. This uses the lower experiment independently of
the upper one; sign-changing sequences are covered by their two subsequences.

For clarity, the inverse order used here follows directly from
`v^T A^-1 v=max_y(2 v.y-y^T A y)` for a positive definite A, proved by
completing the square. Increasing A decreases that maximum. Taking its
quadratic-form inequality against the positive matrix L_h^0 preserves
the trace inequality. Thus positivity and invertibility are verified at
each use; constant rank alone is not the argument.

The straight segment between w_h^- and w_h^+ remains in the positive
domain and in the box. Integrating (9) along it and using (23) gives

\[
 \frac{|\gamma_h|}{2\epsilon_h}
   |S_h(w_h^+)-S_h(w_h^-)|
       \le \frac{C_V}{2}|\gamma_h| D_h^\pm\longrightarrow0.  \tag{24}
\]

This proves the theorem without differentiating an asymptotic error.
If the proposed contrast transfer holds, the flat Einstein contrast is
zero and supplies the premise above. With epsilon_h=h^(1/3), O(h) total
record/refinement errors contribute only O(h^(2/3)) and leave (24) intact.
One fixed nonzero calibration cannot turn this zero limit into a nonzero
Einstein variation, for example on the already published curved probes.

This result includes arbitrary spatially oscillating positive weights and
nonlinear preparation maps satisfying the explicit probe bound (23). It
does not assume that the core supplies those bounds or the two flat maps.
Signed conductances, lack of a positive lower bound, unbounded probe
sensitivity, a flat preparation that does not realize the two uniform
comparison intervals, or additional geometry-dependent action subtractions
are outside this theorem. A state-independent constant subtraction makes
no difference. The arbitrary-profile construction (3) remains a control
against treating the required flat-map hypothesis as automatic. No new
counterterm, source, selector or normalization is chosen to evade the test.

## 9. Verification and remaining physical obligation

The research capsule compiles twenty-three propositions, including actual
real derivatives, rational-owner binding, rank-two normalization,
arbitrary-profile encoding, full determinant similarity and positive inverse
source and mixed-coordinate annihilation on the real four-Role edges. It prints the three existing owner
types and three new actual propositions. Only `propext`, `Classical.choice`
and `Quot.sound` occur; no `sorryAx` or new axiom is admitted.

The matrix derivative/Hessian, complete source-image theorem, quantitative
inverse, four-Role domain bound, weak direct-readout obstruction, exact corrector
exception, convex-profile and bounded positive flat-calibration obstructions are
all-size analytical proofs above. They are not advertised as compiled
matrix-calculus or continuum existence theorems. The immutable exact
certificate passes 91 grouped controls: derivatives and local coordinates,
source/image boundary controls, both Hessian signs for the consumed probes,
conjugation, normalization, all six direct mixed-coordinate tests, the curved
weak gap, full corrector equations and both-sign flat inverse-order bounds.
It pins 33 transitive D0 sources. Three false ledgers that erase the source
image boundary, inverse degeneration or mixed corrector response are rejected.

```sh
cd 03_FORMALIZATION
lake env lean ../02_REGISTRY/research/certificates/a4d_native_logdet_source.lean
cd ..
python3 02_REGISTRY/research/certificates/a4d_native_logdet_source_check.py
```

The finite source-image theorem solves a supplied-source equation for the
specified nonlinear operator class. It does not derive independent matter
or the native physical map, choose f/z/F, prove refinement compatibility,
or furnish the coupled metric--connection--matter system. The full-core
completeness obligation and original #310/#202/#317 terminals remain open.
