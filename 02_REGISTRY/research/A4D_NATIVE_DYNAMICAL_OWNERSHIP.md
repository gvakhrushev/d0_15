# G0: complete primitive action fibers and the actual Ward input boundary

Research continuation of #310. Input head:
`c9668dca8a900310cf49dbf56a8bcd8f51d872ab`.
The prior primitive-interface and order-two results are retained; this
continuation classifies simultaneous flat translation lifts and their
background derivatives within the same G0 chain.
Consumer: G0 (`constitutive`, `native_sector`) of the
[CONTROL critical plan](https://github.com/gvakhrushev/d0_15/blob/7beb7cb196c4db3304b87d607815c235877bee8e/02_REGISTRY/research/D0_CLOSURE_CRITICAL_PLAN_2026-10-07.md).

**Result.** The entire actual `ActionProtocol P` fiber is classified,
for every verification protocol P, without a finite-state restriction.
Verification plus the endogenous action quantum does not force its
relative transition costs. The canonical action is nevertheless the
unique pointwise least representative. The entire invariant background
action fiber consists of arbitrary functions on the symmetry quotient.
The actual conditional moving Ward conclusion needs only its four map
covariance premises; its `geometryAction` premise can be eliminated.
Passive Hodge transport is injective in the supplied seed. The literal
polynomial groupoid-composition premise is now completely classified and
distinguished from a genuine total-degree-two composition law. The corrected
order-two implication admits every supplied generator; the stronger exact
polynomial premise excludes an actual native constant generator. The complete
simultaneous flat transport fiber is now classified with its isotropy. Its
actual metric image and Ward annihilator are computed: translation tests
are not all metric tests. Every strongly coframe-convergent smooth
nondegenerate continuum limit of this flat orbit has zero Riemann curvature.

This discharges the G0 premise audit for these named interfaces. It does
**not** classify every composition or physical realization of the D0 core.
It does not identify transition cost with a gravitational functional,
prove physical response nonuniqueness, or close G0, positive GR, or the
original #310/#202/#317 terminals. No candidate physical action is added.
The dependency graph keeps its 44 nodes and all 11 original open nodes.

## 1. The precise question and owned input chain

The prior candidate classifications did not show that their union was
all native dynamics. This package instead tests a proposed derivation:

> Does the actual verification/action-quantum interface, followed by
> passive covariance and the existing conditional Ward theorem, already
> determine the constitutive action required by the physical probe law?

| Arrow | Actual owner and independently supplied data | Disposition |
|---|---|---|
| Verification → distinguishable records | `VerificationContract` / `KillingTest` in `VerifiabilityNecessity` / `PopperianBootstrap`; P supplies states, records, lines, catalogue, recording and comparison | Record correctness and injectivity are owned. There is no metric, action derivative, or refinement equation in this contract. |
| States → transition costs | `EndogenousActionQuantum.ActionProtocol P`; action zero on equal states and at least one otherwise | Complete fiber (1) below. All excess costs are independent inputs. |
| Canonical transition cost | `canonicalActionProtocol P` | Existing legitimate representative, proved here uniquely pointwise least. This fact does not assert that it is a differentiable physical field action. |
| Pairing and primal frame change → dual change | `ArchivePrimalDualMovingAction.dualAction` | Unique dual transformation for the supplied perfect pairing. This is not uniqueness of a Hodge/constitutive map. |
| Hodge seed → transported map | `movingHodge QD S QP` | Complete seed recovery (3). Fixed frame transport cannot identify different seeds. Additional stabilizer/field constraints could restrict seeds and must be supplied independently. |
| Background symmetry → invariant scalar | `geometryAction` premise of `physicalMovingWard_of_constitutiveAction` | Whole invariant-action fiber (2). No relation equating this scalar's derivative to the supplied maps occurs in that theorem's type. |
| Four map covariance identities → mixed-parent Ward identity | `A4DPathWordParentWard` on actual `FinitePrimalDualHodgeData` | Compiled premise-elimination theorem (4). The four identities remain hypotheses, not conclusions of a constitutive derivation. |
| Native field action → physical coframe/link/matter Euler response and refinement | Consuming nodes `constitutive`, `native_sector`, `matter_source_ward`, `contrast_refinement_transfer` | **OPEN.** The centered/transported kinematic preparations do not themselves construct this arrow. |

All source files, transitive D0 imports, toolchain inputs and actual
compiled declarations are hashed in the [Lean receipt](certificates/a4d_native_dynamical_ownership_results.json).
The receipt pins the input head above. This is a statement about the named
types, not a claim based on the failure of a text search to find a theorem.

## 2. Complete action fiber, not a census of examples

Put \(D_P=\{(x,y)\in P.State^2:x\ne y\}\). The compiled equivalence is

\[
\operatorname{ActionProtocol}(P)
\;\simeq\; \{c:D_P\to\mathbb R_{\ge0}\},\qquad
A_c(x,y)=\begin{cases}0&x=y,\\1+c(x,y)&x\ne y.\end{cases}
\tag{1}
\]

The inverse sends A to A(x,y)-1 on distinct pairs. Both inverse identities
are proved using the actual structure, including equality of its proof
fields. This includes every admitted action and all asymmetric costs;
it assumes neither finite cardinality, symmetry, triangle inequalities,
nor smoothness. A `KillingTest P` adds no condition on c.

The canonical action is c=0. For every A and every x,y,
\(A_{can}(x,y)\le A(x,y)\). Conversely, an A lying below every other
admitted action pointwise equals A_can. Thus the result neither denies
existence of the canonical representative nor manufactures a need to
choose a unique action if all physical readouts were eventually identical.
The action-quantum lower-bound theorem alone does not state that every A
attains one; the following countermodels do attain it.

### A difference that survives unit calibration and all relabelings

Use one fixed verification protocol with states/records Fin 3, identity
recording, two Bool lines, Unit catalogue, and exact inequality comparison.
Its actual KillingTest compiles. On these same data take

\[
A_0=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
A_1=\begin{pmatrix}0&1&2\\1&0&1\\2&1&0\end{pmatrix}.
\]

Both satisfy the actual action protocol, symmetry, every triangle
inequality and A(0,1)=1. Their relative costs A(0,2)/A(0,1) are 1 and 2.
The actual calibration theorem preserves these ratios under any positive
common change of units. More strongly, for every permutation e and every
real a, \(A_0(x,y)=aA_1(e(x),e(y))\) cannot hold for all x,y: the
preimages of (0,1) and (0,2) would give 1=a and 1=2a.

The existing `ObservableCompletionCanonicity.distinct_readouts_no_m1_forced`
then proves that this relative-cost readout is not M1-forced over even the
normalized metric-cost subfamily. This is a **transition-cost observable**,
not an Einstein metric response. The physical readout map has not been
constructed, so no conclusion that these parameters survive the physical
quotient is drawn. The countermodels are mathematical completions used to
test implication, not new physical actions selected for D0.

## 3. Full symmetry fiber and seed retention

For any equivalence relation r on backgrounds B, the compiled equivalence is

\[
\{F:B\to\mathbb R\mid x\mathrel r y\Rightarrow F(x)=F(y)\}
\;\simeq\;(B/r\to\mathbb R).
\tag{2}
\]

For a supplied symmetry σ, take r to be the equivalence closure of
\(x\sim\sigma(x)\). The capsule proves that F∘σ=F is equivalent to
constancy on this complete generated relation; (2) therefore describes
**all** invariant actions, not just polynomial candidates. A transitive
symmetry can leave only constants. Additional locality, regularity,
variational or constitutive equations are not assumed by (2) and may
restrict that family if they have independent owners.

In particular an invariant observable q admits every profile f(q).
On B=R² with the nonidentity symmetry (x,y)↦(x,-y), the two scalars 0
and x²−1 agree at x=1 and obey the same symmetry, but their x derivatives
there are 0 and 2. These derivative statements compile. This is a witness
about the background-action input, not a native metric/source solution.
It cannot be combined with the transition-cost countermodels by silently
inventing the missing physical arrow.

For the actual passive transport
\(T(S)=Q_D S Q_P^{-1}\),

\[
Q_D^{-1}T(S)Q_P=S.
\tag{3}
\]

The compiled theorem uses the literal `movingHodge` definition and proves
injectivity in S. Hence transport moves each supplied seed faithfully;
it supplies no criterion selecting one seed. The theorem is for a given
pair of frame changes. It does not declare arbitrary seeds invariant under
a fixed nontrivial stabilizer or construct a globally equivariant field.

## 4. Actual Ward premise elimination

The owner `physicalMovingWard_of_constitutiveAction` takes independently:

* a background scalar `geometryAction` and symmetry;
* pairings and frame maps Q0,Q1;
* four functions `dPof`, `dDof`, `S0of`, `S1of` of the background;
* equality of the scalar under the symmetry and four covariance identities
  for those functions.

Its conclusion is equality of the mixed matter-parent action built from
the four maps and three fields. It is not an Euler equation for
`geometryAction`. The new theorem on the **same actual carrier types** is

\[
\text{four map covariance identities}
\quad\Longrightarrow\quad
\text{the same mixed-parent action equality}.
\tag{4}
\]

It follows by applying the real owner with the constant zero scalar, whose
invariance is reflexive. This proof instantiation does not select zero as
a physical action: the scalar slot disappears from the resulting theorem.
Its absence is also visible in the printed real proposition and proof.

Therefore this conditional Ward theorem cannot serve as a derivation of
its supplied maps from the geometric action. Such a derivation would need
an additional relation/owner, for example an actual variation identity
tying the action to those maps. The existing parent stress-descent theorem
also retains its compatibility, parent-Ward, auxiliary-EOM and coframe-EOM
hypotheses. Equation (4) does not discharge those EOM hypotheses or turn
passive covariance into a physical conservation/Einstein theorem.

## 5. Complete composition-premise classification and an order-two repair

The next G0 arrow consumes `A4DActionGroupoidSecondJet`. Its owner is a
correct conditional theorem, but its `hcomp` is **exact polynomial equality
for all s,t**, not equality modulo terms of total degree at least three.
The comments' jet terminology cannot weaken that actual hypothesis.

Use the owner's literal matrices, with D denoting its supplied `Dg`:

\[
R_m(s,t)=I+sG+stD+\tfrac12s^2K,\quad
R_b(t)=I+tG+\tfrac12t^2K,\quad
R_\Sigma(s,t)=I+(s+t)G+\tfrac12(s+t)^2K.
\]

Their complete product residual, already expanded by the actual owner, is

\[
R_mR_b-R_\Sigma=stX+st^2A+st^3E+s^2tB+s^2t^2C,
\tag{5}
\]

where
\(X=G^2+D-K\), \(A=GK/2+DG\), \(E=DK/2\),
\(B=KG/2\), \(C=K^2/4\).
The new generic Lean theorem proves the exact equivalence

\[
\texttt{hcomp}\quad\Longleftrightarrow\quad X=A=E=B=C=0.
\tag{6}
\]

This classifies **every** rational finite matrix tuple (G,D,K) satisfying
that premise. It is not a restriction to a tested dressing or weight
ansatz. Necessity follows entrywise from five evaluations at
(1,1), (-1,1), (1,-1), (-1,-1), (1,2); their coefficient matrix has
nonzero determinant -96. Sufficiency uses the actual full expansion.
Thus a finite extraction proves a generic polynomial statement; no
finite sampling is substituted for an unrestricted functional identity.

For D=0, the complete specialization is

\[
\texttt{hcomp}\quad\Longleftrightarrow\quad K=G^2\ \text{and}\ G^3=0.
\tag{7}
\]

The cubic condition is an extra demand of exact composition of the
quadratic *polynomials*. It is not a condition for existence of an
order-two jet or of an actual one-parameter flow. In particular the
real finite-matrix family U(t)=exp(tG) obeys U(s+t)=U(s)U(t), with
U'(0)=G and U''(0)=G², for arbitrary G. These statements are compiled
from Mathlib's actual matrix-exponential theorem with commutation of
scalar multiples proved; the real finite-matrix completeness/norm
instances discharge its analytic hypotheses. The norm supplies the usual
finite-dimensional topology, not a physical positive-energy assumption.
This flow is a mathematical control, not a selected D0 matter evolution.
It does not assert a simultaneous additive representation for different,
noncommuting displacement generators.

### The mismatch occurs on the actual scalar-cycle owner

For the actual `scalarOnes 4`, `scalarDisplacement` is zero and
`scalarCycleG` is the skew cycle difference

\[
G=\begin{pmatrix}
0&2&0&-2\\-2&0&2&0\\0&-2&0&2\\2&0&-2&0
\end{pmatrix},\qquad (G^3)_{01}=-32.
\]

The zero displacement and cube entry compile on the literal definitions;
the rational entry is checked by exact kernel-checked normalization. Therefore no K satisfies
the exact polynomial `hcomp` for this G and D=0. Nevertheless its
order-two law is satisfied by K=G², and the full real exponential control
has those same derivatives. This is an input-premise counterexample in
the owned scalar reduction. It is not an assertion that this flow already
has a native matter action, physical readout, refinement or joint roots.

If D is interpreted as a derivative of a background function along this
zero displacement, D=0 follows. An independently varied extra background
would require its own direction and is outside that specialization.
The D=0 qualifier is essential: a four-by-four nilpotent Jordan G with
G³ nonzero, K=2E_{1,3} in zero-based indices, and D=K−G² satisfies all five
conditions in (6). Nonzero D must not be silently discarded.

### A usable order-two implication

Define H(s,t) to be the four terms in (5) after stX. The new capsule binds
this exact remainder to the actual product and proves

\[
R_mR_b-H=R_\Sigma\ \text{for all }s,t
\quad\Longleftrightarrow\quad K=G^2+D.
\tag{8}
\]

Every monomial in H has total degree three or four. In any fixed
finite-dimensional norm, for rho=|s|+|t|<=1,
\(\|H\|\le(\|A\|+\|B\|+\|C\|+\|E\|)\rho^3\).
This elementary analytic bound gives the intended Taylor meaning; the
exact decomposition and equivalence (8) are compiled. No uniform bound
as the carrier size grows is asserted.

For every supplied G,D, the order-two fiber is nonempty with K=G²+D.
Thus (8) is the research replacement to consume for an order-two argument;
(6) is used only if exact polynomial composition is independently intended.
The supported owner is preserved, with a CONTROL review disposition to
clarify/extend its interface. No theorem is declared false and no native
gate is redefined. The original background-independent noncommuting-delta
obstruction remains separate and valid.

**Remaining derivation:** (8) still does not construct D=(D_e g)[h],
integrate a background-dependent groupoid action, choose its constitutive
seed, or tie its Euler equations to the physical response/refinement map.
The absent native constitutive law cannot be replaced by setting D=0
without a proved zero background direction. This check removes an
incorrectly strong premise from the prospective G0 argument; it does not
turn a conditional two-jet family into the full native system. Section 6
below now supplies the complete compatible flat-orbit lift family and its
second derivatives; physical admission remains a separate step.

## 6. Complete flat-translation lift family, including its stabilizer

The order-two repair leaves a joint question: which background derivatives
can belong to one simultaneous transport, rather than unrelated one-direction
jets? Here that question is answered for the **entire smooth representation
interface of the owned flat coframe translation**. This is a kinematic
classification. Admission by the constitutive, locality, physical-readout
and refinement owners is a separate obligation.

### 6.1 Exact transport: retain the isotropy

Let V,E,F be finite-dimensional real vector spaces, let d:V→E and
G:V→End(F) be linear, and put X=im d and H=ker d. Fix a linear right
inverse j:X→V; write ξ=j(dξ)+cξ with cξ∈H. On the flat orbit, translations
act by e↦e+dξ. Each arrow is uniquely (target e+dξ, source e, cξ).
The action groupoid is therefore Pair(X)×H, **not** just Pair(X).

For any groups H,K and base b∈X, the compiled equivalence is

\[
 \{T:X\times X\times H\to K:\ T(x,y,h)T(y,z,k)=T(x,z,hk),\ T(x,x,1)=1\}
 \simeq \{U:X\to K:U(b)=1\}\times\operatorname{Hom}(H,K),
\]
\[
 T(x,y,h)=U(x)\rho(h)U(y)^{-1},\quad
 U(x)=T(x,b,1),\quad \rho(h)=T(b,b,h).                 \tag{9}
\]

The proof composes the three arrows (x,b,1), (b,b,h), (b,y,1).
Both inverse identities compile; all group-valued transports are included.
No flatness of the spacetime connection or disappearance of nontrivial
isotropy is inferred from this representation normal form.

For real matrix transports take K=GL(F) and additive H. In the C² class,
the prescribed flat generator G is integrable **if and only if**

\[
 [G(c),G(c')]=0\quad(c,c'\in\ker d).                 \tag{10}
\]

Necessity follows by differentiating commuting isotropy translations.
For sufficiency put A(e)=G(j e), C(c)=G(c), choose any C² normalized
U:X→GL(F) with derivative A at zero, and set

\[
 R(e,\xi)=U(e+d\xi)\exp(C(c_\xi))U(e)^{-1}.         \tag{11}
\]

Cancellation of the middle U and commutation in (10) give the exact
composition R(e+dξ,ζ)R(e,ξ)=R(e,ξ+ζ). Its flat derivative is G(ξ).
For a smooth additive isotropy representation with derivative C,
ρ(tc) solves ρ'=C(c)ρ, ρ(0)=I. Differentiating
exp(−tC(c))ρ(tc) shows it is constant; hence ρ(c)=exp(C(c)).
Together with (9), this proves completeness, not only existence of (11).
The finite-dimensional analytic argument is given here; the exact normal
form (9) and the coefficient identities below are compiled.

### 6.2 The complete background-derivative freedom

Write the Taylor expansion of an arbitrary U at zero as

\[
 U(e)=I+A(e)+\tfrac12\{A(e)^2+S(e,e)\}+o(\|e\|^2),
\]

where S:X×X→End(F) is **any symmetric bilinear map**. Conversely every S
is realized by the globally invertible mathematical transport
U_S(e)=exp(A(e)+S(e,e)/2). This realizes every permitted second jet;
it does not assert that every full U is a quadratic exponential.

For g_ζ(e)=∂_t R(e,tζ)|₀, ordinary product differentiation gives

\[
 (D_e g_\zeta)_0[h]
 =S(h,d\zeta)+\tfrac12[A(h),A(d\zeta)]+[A(h),C(c_\zeta)].       \tag{12}
\]

Its antisymmetric mixed part is precisely the groupoid equation
B(ζ,dξ)−B(ξ,dζ)+[G(ζ),G(ξ)]=0. The residual for arbitrary split matrices
is [C(cζ),C(cξ)], so (10) is essential. The diagonal second derivative is

\[
 K_\xi=A(d\xi)^2+2A(d\xi)C(c_\xi)+C(c_\xi)^2+S(d\xi,d\xi)
       =G(\xi)^2+(D_e g_\xi)_0[d\xi].                \tag{13}
\]

These noncommutative coefficient identities compile. A direction in
ker d has K=G²; an arbitrary second derivative cannot be assigned to an
isotropy direction. Non-isotropy directions have the symmetric freedom
S, with compatibility across directions. The one-direction relation (8)
alone does not impose this simultaneous compatibility.

### 6.3 Binding to the actual native owners

**Scalar owner.** For every n≥3 use the literal
`scalarDisplacement` dξ=n(ξ(i+1)−ξ(i)) and `scalarCycleG` Gξ=MξD.
The capsule proves for every n that ker d is exactly the constant fields,
that centering ξ by its mean preserves dξ, and that a mean-zero preimage
is unique. Thus j is the mean-zero inverse on X=im d. Explicitly, for a
zero-sum h set v_i=n⁻¹Σ_{k<i}h_k and subtract its mean; the periodic last
edge follows from Σh=0. Here cξ=mean ξ and C(c)=cD, so (10) holds.
For the smooth construction take the realification of these finite rational
formulas; this makes no continuum-in-n claim. This gives a nonempty full
simultaneous transport family with the actual
flat generator, despite the noncommuting local delta generators.

The actual `advectiveBackgroundDerivative` B_adv is a proved particular
mixed cocycle. Every bilinear solution on V×X is exactly

\[
 B(\zeta,h)=B_{adv}(\zeta,h)+Q(d\zeta,h),\qquad Q:X\times X\to End(F)
 \text{ symmetric bilinear}.                        \tag{14}
\]

Indeed the difference T of two solutions obeys T(ζ,dξ)=T(ξ,dζ).
For c∈ker d this gives T(c,h)=0 for all h∈X, so T factors uniquely
through d in its first slot; the remaining equation is symmetry of Q.
Conversely any Q satisfies the equation. This factorization uses
bilinearity, not just a sample of directions. The capsule proves the
exact native mixed-equation/symmetric-difference equivalence and the
arbitrary symmetric-correction implication. Formula (12), with
S chosen to match B_adv on mean-zero vectors and then shifted by Q,
realizes every fiber (14) by an exact smooth groupoid. Values of B on
transverse coframe directions outside X are not determined by (14).

**Literal four-role/Fock owner.** This is not promoted from an unproved
scalar embedding. On `ArchiveRolePhaseGroup N=(Z/(N+2))^Role`, set
d=`forwardGaugeCoframe` and G=`a4dCartanGenerator` on `ArchiveCochain N`.
The owned `cartanGenerator_exact_expansion` is linear in ξ. Vanishing dξ
makes each component of ξ invariant under each unit role shift; these
shifts generate the entire finite torus, so ker d consists exactly of
four constant components. The same mean-zero inverse exists on im d.

The capsule directly proves from the literal owner that for constant c

\[
 G_c\psi=\sum_r c^r C_r\psi,\qquad
 [G_c,G_b]=0,                                       \tag{15}
\]

where C_r is the owned centeredDifference, acting identically on each
Fock label. The proof consumes the actual centered-difference commutation
theorem. The source expansion originally depended on a finite CAR
`native_decide` axiom. The capsule proves that identical integer CAR
proposition with `decide +kernel`, expands the source proof with that
replacement, and has Lean check the resulting theorem. Its transitive
axiom list and both native corollaries contain only the three standard
axioms; the supported owner is unchanged. Consequently (9)–(13) apply to the **full flat four-role cochain
translation interface**, for every finite N, including N+2∈4N.
The capsule also binds d directly to the actual affine owner through
`ownedFlatTranslation_is_linear`, with its transitive sources pinned.
This constructs compatible mathematical completions on that flat orbit.
It does not establish their admission on curved connection backgrounds,
or that all points in the unrestricted coframe orbit are physically
nondegenerate. Restrictions to a nondegenerate neighborhood retain the
local conclusions; no curved on-shell realization is asserted.

### 6.4 Which freedom could be physical?

For the same isotropy representation, two choices U,V obey the compiled
intertwining identity with J(e)=V(e)U(e)⁻¹:

\[
 J(x)T_U(x,y,h)=T_V(x,y,h)J(y).                      \tag{16}
\]

For any action of GL(F) on a space Y, a transported section U(e)·v is
covariant exactly when its base value v is fixed by **all** ρ(H); this
criterion also compiles. In particular an invariant quadratic seed gives
W_e(ψ,φ)=W_0(U(e)⁻¹ψ,U(e)⁻¹φ). The intertwiner (16) preserves this value
when fields are transformed together. Therefore counting the free S or U
as physical degrees of freedom would be premature.

Conversely (16) is an abstract bundle isomorphism. It need not be an owned
physical gauge transformation: it may change locality, the prescribed
coframe/link/matter readout or refinement maps. The exact remaining
consumer is to prove those compatibilities and the constitutive seed from
native owners. No arbitrary U, Q, seed, geometric action or EOM is selected
here. Nonzero-curvature translation laws, transverse coframe variations,
source, quantitative refinement, joint solutions and GR remain open.

This result closes the **flat simultaneous-lift integrability/fiber question**
inside the existing G0 nodes. It rules out two unproductive next steps:
continuing to guess one Dg on that orbit, or requiring all local generators
to commute. The remaining G0 work must consume the physical admission and
readout/refinement conditions just identified.

### 6.5 Complete metric image and what the translation Ward identity says

The next consumer can be decided without selecting any U or Hessian S.
Use the **literal** `coframeMetricReadout`, `solderMetricMatrix` and
`symmetricRoleGradient` on the same four-role carrier. Put L=N+2,
M=L^4, D_r=L(U_r-U_r^{-1})/2 and write K for their flat translation
metric tangent. The supported owners, rebound in the capsule, give

\[
 C(d\xi)_{ra}=D_r\xi^a,\qquad
 K\xi_{ab}=D_a\xi^b+D_b\xi^a,\qquad
 G(t d\xi)=\eta+tK\xi+t^2 C(d\xi)\eta C(d\xi)^T.       \tag{17}
\]

The pre-existing `coframeDifferential_ker_constant` proves the **raw**
kernel is four constants. Its complete raw quotient dimension
12M+4 is already owned in `A4DCellHessianTransverseModulus`; that result
is consumed here, not rediscovered. Centering and the symmetric metric
readout have a larger kernel, which must be computed separately.

The complete Fourier basis on the periodic carrier has D_r multiplier
i s_r, with s_r=L sin(2 pi k_r/L). At a nonzero s the symbol, after
absorbing i into the vector, is v -> s v^T+v s^T. It is injective:
choose s_r != 0; its rr entry forces v_r=0, then every ra entry forces
v_a=0. This generic implication is compiled over C. Hence its rank is
four for every s != 0 and zero for s=0. There are exactly
z=gcd(L,2)^4 zero-symbol frequencies: k_r=0, and also L/2 when L is even.
Fourier orthogonality follows by summing the finite geometric series;
there are M independent characters, so these are all the modes. Since
the operator is real, its real rank equals its complex rank. Therefore

\[
 \dim\ker K=4z,\quad \operatorname{rank}K=4(M-z),\quad
 \dim\operatorname{coker}K=6M+4z.                    \tag{18}
\]

For every required L in 4N the dimensions are 64, 4M-64 and 6M+64.
The 60 nonconstant translation directions lost by the metric tangent
are retained as readout-null directions, not declared physical gauge.
At L=2 the entire centered derivative vanishes, consistently with (18).
The rank and complete Fourier decomposition are analytic proofs in this
text; only symbol injectivity and the exact native identities are claimed
as compiled.

This also explicitly describes the full missing metric space. In the
full Frobenius pairing (weight two on every packed off-diagonal slot),
at any real s != 0 and complex symmetric T put

\[
 v=\frac{Ts}{|s|^2}-\frac{s(s^T T s)}{2|s|^4},\quad
 T_\parallel=sv^T+vs^T,\quad T_\perp=T-T_\parallel.    \tag{19}
\]

Then T_perp s=0 and this is the unique orthogonal range/complement
decomposition. Indeed (sv^T+vs^T)s=|s|^2v+s(s^Tv), and pairing a symmetric
T with sw^T+ws^T gives 2 w^T T s; the Hermitian version gives the same
orthogonality since s is real. The complement has dimension six. At
s=0 the complement is all ten components. Thus this is a complete
metric image calculation, not a collection of sample obstructions.

The actual `symmetricRoleGradient_adjoint` and parent descent owners give
the compiled equivalence

\[
 [\ \langle T,K\xi\rangle=0\ \text{for every }\xi\ ]
 \quad\Longleftrightarrow\quad
 \operatorname{div}_D T=0.                           \tag{20}
\]

The sign and normalization are \(\langle K\xi,T\rangle
=-2\langle\xi,\operatorname{div}_D T\rangle\).
This is weaker than T=0 or vanishing against every metric probe.
The capsule constructs the actual constant identity tensor on the same
carrier: its divergence and all translation pairings vanish, while its
pairing with the smooth constant identity metric probe is 4M>0 (4 after
normalized counting). The constant probe has the literal raw-coframe lift e=I/2, also compiled.
No source is fitted and no alternative action is
introduced; it is a counterexample to the proposed **logical implication**
from translation tests to all metric tests. It is not asserted to be the
residual of an actual on-shell matter/gravity solution.

Consequently the full transport classification and even an established
translation Ward identity cannot replace the independent metric Euler
equations. The missing transverse probes are present already at fixed
smooth frequencies; their loss is not merely a high-frequency anomaly.

### 6.6 Every smooth, strongly coframe-convergent flat-orbit limit is flat

There is also a nonlinear obstruction to using this same orbit as the
whole curved state sector. It is independent of U, S and the transported
matter seed. Consider **any** sequence e_h=d_h xi_h on periodic carriers,
h=1/L -> 0, and the literal centered solders
Theta_h=eta+C_h(e_h). Suppose their piecewise-constant reconstructions
converge strongly in L2 to a C2 field Theta, with det Theta nowhere zero.
No bound on xi_h or its derivatives is assumed. Then

\[
 G_h\longrightarrow g=\Theta\eta\Theta^T\quad\text{in }L^1,
 \qquad \operatorname{Riem}[g]=0.                   \tag{21}
\]

**Proof.** Commuting centered differences and (17) give exactly
D_r Theta_h,sa-D_s Theta_h,ra=0. The capsule proves the nonconstant
part of this identity for all native sizes; constants contribute zero.
For every smooth periodic scalar test phi, discrete skew-adjointness gives

    h^4 sum_x [Theta_h,sa(x) D_r phi(hx)
               - Theta_h,ra(x) D_s phi(hx)] = 0.

The piecewise-constant reconstruction of D_r phi(hx) converges uniformly
to partial_r phi, by Taylor's formula and cell diameter O(h). Strong L2
convergence implies bounded L2 norm and L1 convergence on the unit torus,
so the displayed equality passes to the limit. Thus each column one-form
theta^a=Theta_ra dx^r is closed distributionally, hence classically.
On a coordinate ball its path integral F^a is independent of rectangular
path subdivisions (the difference is the integral of the zero curl),
and partial_r F^a=Theta_ra. Nonsingularity makes F local coordinates;
in those coordinates g is the constant Lorentz form eta, so its Riemann
curvature is zero. Finally the product estimate

    ||Theta_h eta Theta_h^T-Theta eta Theta^T||_L1
      <= ||eta|| (||Theta_h||_L2+||Theta||_L2)
                    ||Theta_h-Theta||_L2

proves the asserted metric convergence. This continuum argument is an
analytic proof, not a claimed Lean theorem or a native compactness theorem.

This excludes a genuinely curved recovery target for the **entire**
flat-translation orbit with this smooth coframe limit, regardless of the
choice of compatible transport. It does not exclude general raw coframes,
curved affine-link backgrounds, or sequences for which only the metric
converges and no such strong coframe limit exists. Oscillatory frame factors
cannot be removed by asserting an unproved physical gauge. Nor does it
assert that every finite lattice curvature expression vanishes: (21)
concerns the Levi-Civita curvature of the stated continuum metric limit.

**Closed consumer and next obligation.** For this whole flat interface,
the metric-variation image, Ward-annihilator boundary and smooth curved
recovery obstruction are now fixed. Further choices of U or S cannot
repair them. G0 must instead construct its native action and genuine
independent Euler equations on the already available full coframe/link
state carrier, with its transverse metric variations and physical
refinement conditions. The existing general centered and transported
kinematic preparations remain available; their action/source/gate link
is still required. This conclusion preserves G0 and all parent terminals.

## 7. What this closes inside G0, and the remaining proposition

**Discharged input question:** neither arbitrary transition costs nor
background constitutive maps become determined merely by citing the
verification/action-quantum contract and conditional passive Ward owner.
The canonical least transition cost, full cost fiber, full invariant-action
fiber and exact Ward premise boundary now have proofs. The complete exact-polynomial premise and its genuine
order-two replacement are also proved, with a native counterexample
showing why they must not be confused. The complete simultaneous flat
translation representation and second-jet fibers are now classified, with
a direct binding to the four-role/Fock constant generators and the exact
intertwiner for their representation freedom. The exact metric image,
translation-Ward annihilator and smooth flat-orbit recovery boundary are
proved in Sections 6.5–6.6. Thus the next proof must supply transverse
physical metric variations and independent Euler equations on the full
coframe/link carrier. No further spectral
candidate or coefficient sweep is needed to establish this conclusion.

The [complete mixed-parent field-frame consumer](A4D_NATIVE_PARENT_SOURCE_BOUNDARY.md#6-complete-field-frame-class-full-background-source-and-joint-roots)
now removes one genuine redundancy from this target. For any smooth invertible
field reparametrization of a fixed parent family, with the four operator slots
and pairing transformed, the actual source defect is exactly the contraction
of the three full field residuals with the frame generator. It vanishes on the
full matter gate in every background direction, including transverse coframe
and link directions. Joint background roots with the same geometric action
therefore coincide. In the entire fixed-seed field-frame class, every full
root has zero background source, even for indefinite or singular forms.
This is not a physical gauge assertion: constraints,
readout and refinement need their own admission. Distinct transverse seed jets
can still give different Euler covectors on the same full matter root; their
source difference survives every such frame. The actual seed/background law,
rather than another representation U or Hessian choice, remains the next
physical input to derive. The proof has 32 compiled declarations and 75 exact
controls in its own existing source package; no new dependency node is added.

**Remaining G0 proposition:** construct from independently owned native
primitives/composition rules the complete admitted family
\((X_h,I^N_{h,\theta},\mathcal V_{h,\theta},E^N_{h,\theta},P_h,R_h)\),
or prove a boundary for that complete family. It must tie the action and
its variations to the *same* coframe/link/matter state and physical readout,
and specify which refinement transitions admit that state. The free slots
identified above are exact targets for that derivation. If another core
owner constrains them, its actual theorem and hypotheses must be consumed.
If it is an independent external physical datum, the interface must be
classified at that precise scope through CONTROL.

This package does not prove that no such owner/composition can exist. The
whole `ActionProtocol` fiber is complete for **that structure**, not the
whole D0 core. A typed linking theorem could restrict it; physical response
universality could remove remaining action parameters. Both possibilities
remain protected. G0 stays OPEN; source, contrast transfer, stationarity,
curved roots, soundness and recovery are not declared complete.

## 8. Replay and negative controls

The generic statements compile in the [capsule](certificates/a4d_native_dynamical_ownership.lean),
with the real input types and Ward proof printed in its
[output](certificates/a4d_native_dynamical_ownership_output.txt).
Only `propext`, `Classical.choice`, `Quot.sound` are allowed transitively;
no `sorryAx`, evaluation axiom or new physical axiom is accepted.

The [exact checker](certificates/a4d_native_dynamical_ownership_check.py)
replays the normalized cost matrices, all six relabelings, the independent
symmetry/variation witness and a nontrivial seed-transport example. It also
checks the complete five-coefficient extraction, the actual length-four
scalar generator, the nonzero-D exception, and the explicit cubic/quartic
remainder, rejecting the exact-polynomial-as-jet substitution. Its
immutable [ledger](certificates/a4d_native_dynamical_ownership_certificate.json)
also preserves the scope and remaining G0 premise. The continuation
checks exact groupoid composition with nontrivial isotropy, intertwiners,
and every tested mixed direction at native scalar sizes 4, 5 and 8.
It rejects antisymmetric Hessian corrections and erasure of the stabilizer. These finite controls
are not used as substitutes for the generic equivalences.

```sh
# From 03_FORMALIZATION, after the actual imports are built:
lake env lean ../02_REGISTRY/research/certificates/a4d_native_dynamical_ownership.lean
# From the repository root:
python3 02_REGISTRY/research/certificates/a4d_native_dynamical_ownership_check.py
```

The extended capsule compiles 61 declarations with 83 transitive D0
source pins. Its checker replays 128 exact controls. The 25 earlier scope
mutations and seven metric-consumer scope mutations are rejected.

Hostile ledger mutations must reject a full-core NO-GO, positive GR,
physical-response nonuniqueness, canonical-action nonexistence, a selected
zero geometric action, a closed G0, and disappearance of the four map
premises. The supported D0 source tree remains unchanged; this is a
source-bound research capsule, not a supported-owner promotion.
