# G0: complete primitive action fibers and the actual Ward input boundary

Research continuation of #310. Input head:
`7743910de8e8914f06b68f63aca917997344d1ae`.
The first primitive-interface result was published at that head; this
continuation tests the actual composition rule needed by the same G0 chain.
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
polynomial premise excludes an actual native constant generator.

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
turn a conditional two-jet family into the full native system.

## 6. What this closes inside G0, and the remaining proposition

**Discharged input question:** neither arbitrary transition costs nor
background constitutive maps become determined merely by citing the
verification/action-quantum contract and conditional passive Ward owner.
The canonical least transition cost, full cost fiber, full invariant-action
fiber and exact Ward premise boundary now have proofs. The complete exact-polynomial premise and its genuine
order-two replacement are also proved, with a native counterexample
showing why they must not be confused. No further spectral
candidate or coefficient sweep is needed to establish this conclusion.

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

## 7. Replay and negative controls

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
also preserves the scope and remaining G0 premise. These finite controls
are not used as substitutes for the generic equivalences.

```sh
# From 03_FORMALIZATION, after the actual imports are built:
lake env lean ../02_REGISTRY/research/certificates/a4d_native_dynamical_ownership.lean
# From the repository root:
python3 02_REGISTRY/research/certificates/a4d_native_dynamical_ownership_check.py
```

The extended capsule compiles 33 declarations with 26 transitive D0
source pins. Its checker replays 54 exact controls. Eleven prior scope
mutations and six composition-specific mutations are rejected.

Hostile ledger mutations must reject a full-core NO-GO, positive GR,
physical-response nonuniqueness, canonical-action nonexistence, a selected
zero geometric action, a closed G0, and disappearance of the four map
premises. The supported D0 source tree remains unchanged; this is a
source-bound research capsule, not a supported-owner promotion.
