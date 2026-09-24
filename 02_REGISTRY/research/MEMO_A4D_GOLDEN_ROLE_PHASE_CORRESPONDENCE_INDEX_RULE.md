# MEMO_A4D_GOLDEN_ROLE_PHASE_CORRESPONDENCE_INDEX_RULE

**Task:** `EXP-A4D-GOLDEN-ROLE-PHASE-CORRESPONDENCE-INDEX-RULE`  
**Baseline:** `main` after PR #104, `069c510557b1573f89509f0de105c26a6295dd9c`  
**Inputs read:** `MEMO_A4D_GOLDEN_ROLE_PHASE_CARRIER_OPERATOR_WELD`,
`MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD`,
`ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS`,
`FibonacciAFTower`, `A4DGoldenRolePhaseRGDefect`,
`A4DGoldenCarrierWeldBoundary`, `ArchiveRolePhaseCarrier`,
`ArchiveRolePhaseProductCarrier`, `ArchiveRolePhaseGroup`,
`ArchiveRolePermutationAction`, and `ArchiveLaplacianRG`.

## 0. Verdict and scope

**GOLDEN-ROLE-PHASE-CORRESPONDENCE-INDEX-PRIMITIVE-REQUIRED.**

Finite-dimensional `A_k`–`C(B_n)` correspondences exist abundantly, including
faithful-left/full-right families. Their exact multiplicity transformations give
four well-typed squares, but impose **no relation** between the AF depth `k`
and the Role-phase period `n`. In particular the positive induction/pullback
square has solutions for every pair of successive levels, including constant
Role-invariant, faithful/full solutions. The other orientations have precise
cone, support, or integrality conditions, not a universal correspondence no-go.

The inverse-incidence positivity obstruction is real but scoped: repeatedly
lifting a *fixed nonzero integer multiplicity* backwards through restriction
cannot continue indefinitely. It does not obstruct forward AF induction or
one finite restriction step. The nonuniform Role fibers obstruct a **constant,
unweighted, simultaneous pullback/direct-image** condition, not equivariant
integer pushforward itself. Neither obstruction selects a canonical diagonal
`k(n)` or turns the independent scalar `phi` probe into a carrier comparison.

This is a mathematical classification of the finite stage implied by the
incidence owner, not a claim that Lean already contains concrete matrix-block
inclusions, a Tower-C `S4` action, or this correspondence family. No Lean
source or downstream geometric operators are changed.

## 1. Exact finite-stage classification

Put `d_k=(a_k,b_k)`, `d_0=(1,1)` and

```text
M = M_phi = [[1,1],[1,0]],    d_(k+1) = M d_k,
A_k = M_(a_k)(C) ⊕ M_(b_k)(C),
B_n = Role -> Fin(n+2),       C(B_n) = ∏_(x∈B_n) C.
```

Assume *finite-dimensional, unital/nondegenerate* left representations.
The minimal central projections `e_x` of the right algebra decompose every
right Hilbert module `X` orthogonally into `X_x=X e_x`. The left action
commutes with right multiplication, so it restricts to a representation on
each `X_x`. Semisimplicity of matrix algebras gives, uniquely up to a
right-module unitary intertwining the left action,

```text
X_x ≅ (C^(a_k) ⊗ C^(p_x)) ⊕ (C^(b_k) ⊗ C^(q_x)),
m_(k,n)(x)=(p_x,q_x)∈N²,   dim_C X_x=a_k p_x+b_k q_x.
```

Conversely **every** field `B_n -> N²` constructs one such correspondence.
There are no constraints between distinct fibers. This classification includes
zero fibers and the zero module; it excludes arbitrary summands on which the
unit of `A_k` acts by zero. If degenerate left actions are allowed, an extra
zero-action dimension at each fiber must be recorded.

Qualifiers, kept separate:

| Property | Exact condition |
|---|---|
| bare finite correspondence | any `m(x)∈N²` |
| full right `C(B_n)` module | `p_x+q_x>0` for **every** `x` |
| faithful left action | `Σ_x p_x>0` **and** `Σ_x q_x>0` |
| both | both preceding conditions; e.g. `m(x)=(1,1)` everywhere |
| `A_k`–`C(B_n)` imprimitivity | impossible: Morita equivalence identifies centers/spectra, but one center has two points and `|B_n|=(n+2)^4≥16` |

The last line does not forbid the other three classes or noncanonical reverse
representations `C(B_n)->A_k`. At `k=0,1` the character exceptions from PR
#104 remain; no unital hom `A_k->C(B_n)` exists at `k≥2`.

## 2. Role permutations and the missing left action

The owned action on `B_n` relabels four coordinates; the coordinatewise
projection commutes with it. Give `A_k` the **trivial** `S4` action solely as a
control. An equivariant unitary `U_sigma:X_x -> X_(sigma.x)` intertwining the
left action exists precisely when

```text
m(sigma.x)=m(x) for every sigma∈S4 and x∈B_n.
```

Thus equivariant multiplicities descend to the multisets of four phase
coordinates. Equality on orbits is sufficient for *existence* (choose trivial
isotropy actions and transport around each orbit). It does **not** classify
all equivariant modules: for each orbit representative, representations of
its stabilizer on the two multiplicity spaces supply additional equivariant
structures. A delta at one nonsymmetric point is not invariant; the sum over
its orbit is. A delta at `(0,0,0,0)` is invariant.

For `k≥1`, `a_k≠b_k`. Therefore a `*`-automorphism of the concrete two-block
algebra cannot interchange its two central blocks; it is inner on each block.
At `k=0`, a swap of the two scalar blocks is mathematically possible, but
choosing a homomorphism `S4->S2` and extending it across the unequal-block
stages is **not** an owned action. Inner actions can be chosen abstractly;
none is selected by `FibonacciAFTower`, and their isotropy/intertwiner data
are additional to the multiplicity field. Absence of an owned action is a
typing boundary, not a universal nonexistence theorem.

## 3. AF inclusion and exact multiplicity transport

The literal Bratteli incidence `M` has new-block rows and old-block columns.
Indeed `d_(k+1)=(a_k+b_k,a_k)`: the first new defining representation
restricts to **one of each** old defining representation; the second to
**one of the first**. Hence for a fine left multiplicity column `v=(r,s)^T`,

```text
R(v) = m_(A_k)(Res_(A_k)^(A_(k+1)) X) = M^T v = M v = (r+s,r)^T.
```

Symmetry makes `M^T=M` here; the row/column convention is still substantive.
The inverse condition for a proposed coarse column `u=(p,q)^T` is

```text
R(v)=u  iff  v=M^(-1)u=(q,p-q)^T∈N²
         iff  p≥q≥0,           M^(-1)=[[0,1],[1,-1]].
```

If a concrete unital finite-block inclusion is supplied, the standard
left-induction bimodule `A_(k+1)` over `A_k` (completed with a faithful
conditional expectation, e.g. from a specified compatible trace) sends old
multiplicities `u` to

```text
I(u)=M u=(p+q,p)^T.
```

For example at `k=0`, the old two characters induce respectively to `(1,1)`
and `(1,0)` in `M_2(C)⊕C`. At the level of unitary representation types this
formula depends only on incidence. A particular inner product, conditional
expectation, and inclusion are **extra choices**; the current Lean owner
supplies incidence and trace scalar identities, not a complete concrete
induction functor.

The repeated *inverse* cone is much smaller than a one-step cone. If
`u=M^t v_t`, `v_t∈N²` for every `t≥0`, then `u=0`: the cone `M^t R_+²` is
bounded by the two adjacent Fibonacci column slopes, which converge to the
irrational Perron ray `(phi,1)`. Their intersection is that ray; it contains
no nonzero integer vector. For the explicit seed `(1,1)`, successive inverse
columns are `(1,1),(1,0),(0,1),(1,-1)`. This is a no-go for an infinite
restriction-lift **of the same base fiber**, not for finite-stage or forward
induction solutions. `phi` is an asymptotic slope of `M`; it is not an index
rule or a Role-phase weight.

## 4. Literal B pullback, direct image, and exact fibers

Write `L=n+2`, `p=p_n:B_(n+1)->B_n`, with each coordinate reduced from
`Fin(L+1)` modulo `L`. The coarse coordinates `0` have two preimages
`0,L`; each `1,...,L-1` has exactly one. Define

```text
t(x)=#{r∈Role | x_r=0},       f_n(x)=|p^(-1){x}|=2^(t(x)).
```

There are `binom(4,t)(L-1)^(4-t)` coarse points with fiber size `2^t`.
All `1,2,4,8,16` sizes occur at every `n`. Their multiplicities total
`Σ_x f_n(x)=(L+1)^4`; averaging them to `phi` loses the actual map.

Scalar base change `p^*:C(B_n)->C(B_(n+1))` produces the **pullback** module
`p^*X=X⊗_(C(B_n)) C(B_(n+1))`, with

```text
(P u)(y)=u(p(y)).
```

Direct image of a fine module, using the canonical unweighted finite sum
inner product, is `p_*Y`, with `(p_*Y)_x=⊕_(p(y)=x)Y_y`, so

```text
(D v)(x)=Σ_(p(y)=x) v(y),      D P u(x)=f_n(x) u(x).
```

The literal representatives define an `S4`-equivariant finite-set section
`s_n(x)_r=x_r∈Fin(L+1)`, satisfying `p s_n=id`. Consequently a delta lift
`v(s_n(x))=w(x)`, zero off its image, has `D v=w` for **any** orbit-invariant
integer field `w`. This section does not intertwine cyclic group
translations. It proves that integer direct image has no blanket obstruction
from the varying fibers. Such a delta lift generally loses full right support
on the fine side.

## 5. Four refinement squares: exact equations

Let `u=m_(k,n):B_n->N²` and `v=m_(k+1,n+1):B_(n+1)->N²`.
All equations below are alternatives with specified variance. Both AF maps
act on the two multiplicity coordinates; both B maps act on the fibers.
They commute *as operations on independent axes* (`RP=PR`, `RD=DR`,
`IP=PI`, `ID=DI`) wherever induction is supplied. Identifying the resulting
diagonal with `u` and `v` is an additional condition:

| Square | Diagonal equation | Exact solution class |
|---|---|---|
| 1. restriction / pullback | `R v=P u`, i.e. `M v(y)=u(p y)` | iff every `u(x)=(p_x,q_x)` has `p_x≥q_x`; then uniquely `v(y)=(q_x,p_x-q_x)` |
| 2. induction / pullback | `v=I P u`, i.e. `v(y)=M u(p y)` | every `u≥0`; uniquely determined `v` once the induction model is supplied |
| 3. restriction / pushforward | `u=R D v`, i.e. `u(x)=M Σ_(py=x)v(y)` | iff `M^(-1)u(x)≥0`; many lifts, including the equivariant section lift |
| 4. induction / pushforward | `D v=I u`, i.e. `Σ_(py=x)v(y)=M u(x)` | every `u≥0`; many lifts, including the equivariant section lift |

At a single step the `M^(-1)` cone conditions in 1 and 3 are identical;
pushforward has many allocations, whereas pullback fixes each fine fiber.
There is no numerical comparison of `k` to `n` in any equation. In 2, the
choice `u(x)=d_k` (constant) gives `v(y)=d_(k+1)` for every independent
`k,n`; it is `S4`-invariant, full on both sides, and faithful on both sides.
This supplies a **positive refinement-compatible family on the product
index category**. Restricting it to any path of pairs `(k,n)` is possible and
selects none of those paths as canonical.
It is the regular left representation on each AF fiber: a matrix block
`M_a(C)` acting on itself has `a` copies of its defining representation.
Thus the constant field `d_k=(a_k,b_k)` can be realized by a finite regular
module at every B point, rather than by a guessed scalar dimension match.

Pushforward can also preserve full right support for one step when the coarse
mass is sufficiently large. For square 4 take `u(x)=(16,16)` everywhere;
`M u=(32,16)`. Assign `(1,0)` to *each* point of the fine fiber and the
remainder `(32-f_n(x),16)` at its section point. Every fine fiber is nonzero,
the coarse and fine left actions are faithful, and the construction commutes
with `S4`. Square 3 follows by taking `u=M(16,16)=(32,16)` and assigning
`(1,0)` to each fine point, with remainder `(16-f_n(x),16)` at the section.
These are one-step existential controls, not a canonical trace selection.

### Compatibility if one additionally forces two B variances

For a pullback-defined fine field, direct image multiplies it by the **actual**
`f_n(x)`. Therefore squares 1 and 3 imposed on the same `(u,v)` imply
`(f_n(x)-1)u(x)=0`; the same is true of squares 2 and 4. Such a field may
still live on the nonempty zero-free coarse locus `t(x)=0`, where `f=1`.
It cannot be full right at the coarse level unless it vanishes nowhere,
which this condition forbids. A nonzero **constant** field cannot satisfy
both B variances. Opposite AF orientations 1+2 or 3+4 on the same `(u,v)`
instead imply `(M²-I)u=0`, hence `u=0` since `det(M²-I)=-1`. These are
scoped simultaneous demands; the four candidate squares are not an
instruction to impose all of them together.

## 6. Hostile exact controls

| `k` | `(a_k,b_k)` | `dim A_k` |
|---:|---:|---:|
| 0 | `(1,1)` | 2 |
| 1 | `(2,1)` | 5 |
| 2 | `(3,2)` | 13 |
| 3 | `(5,3)` | 34 |
| 4 | `(8,5)` | 89 |
| 5 | `(13,8)` | 233 |
| 6 | `(21,13)` | 610 |

An `S4` orbit of a point is determined by the multiset of its four
coordinates. The number of orbits is `binom(L+3,4)`. Entries in the next
table list **number of orbits of each size**, not number of points.

| `n` | `L` | `|B_n|` | orbits | size 1 | size 4 | size 6 | size 12 | size 24 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 16 | 5 | 2 | 2 | 1 | 0 | 0 |
| 1 | 3 | 81 | 15 | 3 | 6 | 3 | 3 | 0 |
| 2 | 4 | 256 | 35 | 4 | 12 | 6 | 12 | 1 |
| 3 | 5 | 625 | 70 | 5 | 20 | 10 | 30 | 5 |
| 4 | 6 | 1296 | 126 | 6 | 30 | 15 | 60 | 15 |
| 5 | 7 | 2401 | 210 | 7 | 42 | 21 | 105 | 35 |
| 6 | 8 | 4096 | 330 | 8 | 56 | 28 | 168 | 70 |

For `t=0,1,2,3,4`, the fiber-size multiset is the **exact** pair
`(count,size)=(binom(4,t)(L-1)^(4-t),2^t)`; at `n=0` this is
`(1,1),(4,2),(6,4),(4,8),(1,16)`, and at `n=1` it is
`(16,1),(32,2),(24,4),(8,8),(1,16)`. These sum to `81` and `256`
fine points respectively; the same formula checks `n=0..6` exactly.

One crossed nontrivial step uses `k=0->1` and `n=0->1`:

* Square 2: constant `u=(1,1)` pulls back and induces to constant
  `v=(2,1)` on all 81 fine points. Direct image of this `v` is
  `2^t(2,1)` at a coarse point with `t` zero coordinates: `(2,1)`
  at `(1,1,1,1)`, but `(32,16)` at `(0,0,0,0)`.
* Square 1: constant `u=(2,1)` gives the unique `v=(1,1)`; constant
  `u=(1,1)` gives `v=(1,0)` at one step and fails by the third inverse step.
* Square 3: constant fine `v=(1,1)` gives coarse `u=2^t(2,1)`, not a
  constant field. Orbit-delta fine fields give orbit-supported coarse fields.
* Square 4: coarse constant `u=(1,1)` has an integral equivariant lift
  `(2,1)` on the section and zero elsewhere; its pushforward is `(2,1)`.

Faithfulness survives the displayed constant `u=(1,1)` square-2 example;
fullness survives pullback. The section lifts demonstrate equivariant
pushforward, while the `(16,16)` controls demonstrate that section lifts can
be thickened to full/faithful one-step solutions. A one-point delta with
only `(1,0)` fails faithfulness, and a delta supported on a proper subset
fails fullness; neither is a general obstruction.

## 7. Index rule, weights, and residual interface

Square 2 exists for *all* `k,n` and is preserved by arbitrary independently
chosen AF and B step counts. Thus refinement compatibility alone cannot
distinguish a graph `n↦k(n)` from the full two-index grid. The other three
squares constrain multiplicities or their support, but likewise include
nonzero solutions at every `k,n`. No equation contains an integer equality
that forces `k=n`, `n+2` to be a Fibonacci number, or any canonical
subsequence. Choosing a minimal rank, prescribed trace, or B-side measure
could change the question, but none is an owned cross-tower normalization.

A canonical Role-equivariant **probability** kernel is available at the set
level: assign each `y∈p^(-1){x}` weight `1/f_n(x)`. It makes fiber averaging
`E_n(g)(x)=Σ_(py=x)g(y)/f_n(x)` unital and `E_n p^*=id`.
Given a coarse probability `mu_n`, the lifted probability
`mu_(n+1)(y)=mu_n(p y)/f_n(p y)` pushes forward to `mu_n`.
These rational weights follow from actual finite fibers and contain no
inserted `phi`; they select neither `k(n)` nor an AF comparison. Uniform
counting probabilities at *both* B stages are not preserved by `p`: the
coarse pushforward mass at `x` is `f_n(x)/(L+1)^4`, not `1/L^4`.

Dividing an integer multiplicity `M u(x)` evenly among `f_n(x)` fine points
usually leaves `N²`: for `n=0`, `u=(1,1)` and `x=(0,0,0,0)`, one gets
`(2,1)/16=(1/8,1/16)`. Such data may define a Markov kernel, measured
correspondence, or CP/trace channel with specified measures; they are **not**
dimensions of representations of the matrix blocks. Merely rescaling the
Hilbert-module inner product does **not** change integer ranks or turn
`D P u=f_n u` into `u`. Trace compatibility with Tower C would additionally
need a concrete AF inclusion and a cross-tower state/normalization; the
Perron scalar identity does not provide either on B.

No `P` of the one-dimensional phase-index type consumed by PR #99 follows
from a multiplicity field or any of these squares. Consequently this task
does **not** evaluate `goldenRGResidual` or `goldenEnergyCorrection` on an
invented comparison. The PR #99 operator and energy residuals remain
separate conditional interfaces; `c=phi` remains a scalar probe.

## 8. Theorem-ready handoff and one next step

The finite mathematical lemmas ready for a future formalization are:

1. semisimple fiber classification with exact faithful/full criteria and the
   center-count imprimitivity obstruction;
2. trivial-left-action `S4` orbit-constancy iff existence of equivariant
   structure, with separate stabilizer-representation classification;
3. incidence `R(v)=M v`, inverse cone `p≥q`, conditional induction type
   `I(u)=M u`, and the infinite integer inverse-cone intersection `{0}`;
4. fiber formula `f_n(x)=2^t`, its binomial frequency, equivariant section,
   pullback/direct-image laws and the four diagonal equations above;
5. the constant full/faithful induction/pullback family for arbitrary
   `k,n`, which proves the missing-index conclusion *within this class*.

All assertions here about concrete correspondences are research mathematics
until formalized. The repository's scalar residual or finite controls do not
prove a carrier or operator weld.

**Exactly one recommended next step:** define and independently justify a
cross-tower **normalized, Role-equivariant comparison primitive** specifying
both its AF-side action/representation and how it selects a Role-phase period
for each AF depth; then test that explicit primitive against these integer
squares. Its index selection must come from the new structure, not from
matching displayed dimensions, inserting `phi` into weights, or relabeling
the two independent indices.
