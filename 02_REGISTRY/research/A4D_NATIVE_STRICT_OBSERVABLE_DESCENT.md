# Actual archive observables: strict persistence is not growing spatial resolution

Parent: existing `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, [#310](https://github.com/gvakhrushev/d0_15/pull/310).
Input SOURCE: `adee3e64e0cd07ab792610a1f52a95a5e4e9cb0f`.
Main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Date: 2026-10-10. Supported D0 tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.

**Result:** the literal exact scalar rule `F_(n+1)=F_n composed with pi_n`,
starting at one fixed native level, describes only persistence of that
level's readings. On the actual archive tower its entire base-zero class
is exactly the sixteen-coordinate scalar algebra, at every later level.
It fails to distinguish two explicit retained native records. Representing
that entire algebra on the existing full counting Hodge/CAR carrier makes
its point metric have diameter at most `15/L`, for every bijective site
identification, where `L=N+2` is the operator's actual derivative scale.
Thus this class cannot provide a noncollapsed spatial limit of that triple.

This is a complete classification of a **specific existing compatibility
rule and represented scalar reading**, not an assertion that every D0
observable or preparation has this rule. It does not prove absence of
Gamma/F or GR throughout the core. No quotient is installed, and every
archive mode remains in the full price.

The twenty new Lean propositions bind the actual composite projections,
the complete scalar-family factorization, and the explicit retained-record
counterexample. The finite scalar-subalgebra classification, operator-norm
metric bound, and recovery packing below have elementary analytic proofs;
they are **not claimed to be fully formalized in Lean**. Exact finite
controls exercise the actual projections, periodic adjacency, CAR columns,
coarse labels and the distinction between persistence and new cylinders.

## 1. Primary rule and actual owners

BOOK_02, section "Counter-term ban", says CORE observables are fixed by
the whole rule `F_(k-1) composed with pi_(k to k-1) = F_k`.
Its footnote refers to GOLDEN Book V LEM 21.4.2. The original DEF 21.4.1
has exactly that equality; THE 21.4.3 also calls these the locally constant
observables of the inverse limit. Here only the displayed **scalar equality**
is used. It is not conflated with transport of a field whose value spaces
and coordinates change with the level, or with conditional expectations of
a martingale. Those are different diagrams requiring their own owner.

The diagram used here is the actual `ArchiveRefinementTower`:

\[
 A_n=\operatorname{Fin}((n+2)^4),\qquad
 \pi_n:A_{n+1}\longrightarrow A_n,
 \quad \pi_n(j)=j\bmod (n+2)^4.                         \tag{1}
\]

Long maps are the **composites** of (1), never one direct modulo or the
different coordinatewise Role projection. `ArchiveLightProfinite` binds
this sequence to the genuine Mathlib categorical diagram and limit.
`CondensedAnchor.DetectorSupportGoldenWeight.readout_factors_through_finite_level`
is a different, legitimate statement: every locally constant readout of
a profinite support factors through **some** finite quotient. It does not
say that all such readouts factor through one fixed initial quotient.

## 2. Whole-class factorization, not a selected sixteen-point ansatz

Let `p_n:A_n -> A_0` be the actual composite, with `p_0=id`, and allow any
codomain Y. Induction in the displayed compatibility rule gives

\[
 F_n=F_0\circ p_n.                                       \tag{2}
\]

Conversely every `F_0:A_0 -> Y` gives a compatible family by (2).
Evaluation at level zero and this construction are mutually inverse;
the capsule constructs the equivalence. Each p_n is surjective by
composition of the actual surjective owner arrows. Thus different F_0
give different families, and even eventual equality identifies no further
families: equality at any later level already gives equality of F_0.

For real scalar fields, the represented algebra is therefore exactly

\[
 \mathcal A_n^0=\{f\circ p_n:f\in\mathbb R^{A_0}\}
       \simeq\mathbb R^{16}.                             \tag{3}
\]

All sixteen fibre indicators are present. Its dimension is sixteen, not
`(n+2)^4`; increasing record capacity does not add an observable to this
particular class. Boolean families number `2^16=65536`. Any fixed birth
level b has the same proof with `(b+2)^4` in place of sixteen. The claim
is not restricted to a chosen basis, polynomial degree or a finite sample
of operators.

## 3. A genuinely new retained cylinder is outside this strict class

At the actual first arrow `A_1 -> A_0`, labels zero and sixteen both map
to zero. The finite test `chi(j)=(j=16)` distinguishes them. There can be
no function f on A_0 with `chi=f composed with pi_0`.

This is not a transient or off-shell record artefact. The two full actual
inverse-limit records are

\[
 u_n=0\ (\forall n),\qquad
 v_0=0,\quad v_n=16\ (n\ge1).                            \tag{4}
\]

They are coherent under every real successor arrow: `16 mod 16=0`, and
sixteen is smaller than every later modulus. They are distinct and retained,
but **every** strict compatible family in (2) reads them identically at
every level. The capsule proves all of these facts against the actual owner.

The level-one cylinder pulls back consistently to all levels **at or above
one**. It cannot extend backward as a scalar value through level zero.
Hence "each finite cylinder persists once available" and "every scalar
family begins at level zero" are distinct assertions. The usual union of
finite cylinder algebras contains the former, as does the space of locally
constant functions on the profinite limit; it is not the latter algebra
(3). This identifies the mismatch in the cited identification with all
locally constant observables. It does not decide physical admission of the
new cylinder or introduce an operational test gate.

## 4. Complete finite scalar-algebra classification

For a finite set X, **every** unital real subalgebra `A subset R^X` is
the algebra of functions constant on the classes of

\[
 x\sim_A y\quad\Longleftrightarrow\quad
      f(x)=f(y)\text{ for all }f\in A.                   \tag{5}
\]

Proof: A is contained in that class-constant algebra by definition.
For one class C and every other class D choose `f_CD in A` whose values
at C and D differ. Constants and scalar multiplication give
`g_CD=(f_CD-f_CD(D))/(f_CD(C)-f_CD(D)) in A`.
The product over all D is the indicator of C: it equals one on C and
zero on every other class. Products are allowed in A; the empty product
covers the one-class case. These indicators span every class-constant
function, proving the reverse inclusion. There is no field preparation,
heat spectrum or physical parameter choice in this classification proof.

Consequently all represented unital scalar subalgebras can be treated by
their actual partition. Noncommutative/path algebras and representations
that are not scalar multiplication on all grades are outside this class.

## 5. Actual Hodge metric collapses for every fixed finite partition

Use the unchanged triple in
[the operator-first metric proof](A4D_NATIVE_HODGE_CONNES_METRIC.md):

\[
 X_L=(\mathbb Z/L)^4,\quad \mathcal H_L=\mathbb R^{X_L\times\{0,1\}^4},
 \mathcal D_L=L\sum_r[c_r^\dagger(S_r-I)+c_r(S_r^{-1}-I)]. \tag{6}
\]

For a unital scalar subalgebra A define its point pseudometric using the
**full** counting operator norm, on all sites and sixteen Fock grades:

\[
 d_{A,L}(x,y)=\sup\{|f(x)-f(y)|:f\in A,
                        \|[\mathcal D_L,M_f]\|\le1\}.    \tag{7}
\]

The already derived literal commutator, or its vacuum-to-one-particle
matrix entry, gives for every nearest-neighbour edge

\[
 \|[\mathcal D_L,M_f]\|\ge L|f(x+e_r)-f(x)|.              \tag{8}
\]

No column condition is substituted for the full norm gate: (8) is only a
necessary lower bound on that norm. It remains true at L=2, where the two
site shifts agree; the annihilator annihilates the vacuum, so the entry
does not cancel. The complete counting Hilbert carrier is unchanged.

Let the partition (5) have m nonempty classes. Form the quotient graph
with an edge when a real periodic grid edge crosses two classes. The
periodic grid is connected, hence its quotient graph is connected.
Every two classes have a simple quotient path of at most m-1 edges.
Since f is constant within each class, (8) bounds its difference across
each quotient edge by `1/L`. Summation along that simple path proves

\[
 \boxed{\operatorname{diam}(X_L,d_{A,L})\le(m-1)/L.}       \tag{9}
\]

Within a class the distance is exactly zero. The argument covers every
unital real scalar subalgebra, including arbitrary nonlinear generators.
It does not assume a smooth curve or independently allowed spectral jets.

Now transport the native partition (3) to X_L by **any** bijection
`e_n:A_n -> X_L`, with `L=n+2`. Surjectivity of p_n gives exactly sixteen
nonempty classes, and (9) becomes

\[
 \boxed{\operatorname{diam}d_{\mathcal A_n^0,L}\le15/L
                   \longrightarrow0.}                 \tag{10}
\]

This is an all-size, all-numberings obstruction, not a search over them.
For even L the full scalar Hodge metric has diameter exactly one by its
already proved product-circle formula. Thus its uniform discrepancy from
this strict reading is at least `max(0,1-15/L)`; even o(1) recovery of that
noncollapsed metric fails. A fixed common nonzero calibration changes the
scale of both distances, not the limiting collapse. A level-dependent
rescaling is outside the statement and has no native calibration owner here.

## 6. Quantitative resolution required for the full flat target

For any proposed unital scalar A with m classes, suppose
`sup_(x,y)|d_(A,L)(x,y)-d_(D,L)(x,y)| <= C/L`, for fixed C>=0,
where d_(D,L) is the full product-circle Hodge metric. Each class has
full metric diameter at most `C/L`, because its d_A is zero. Fix one
site in each class. Every coordinate of a site in that class is then
within floor(C) cyclic lattice steps of this site. Each class has at
most `(2 floor(C)+1)^4` sites, including all wraps. Therefore

\[
 \boxed{L^4\le m(2\lfloor C\rfloor+1)^4.}                \tag{11}
\]

A uniformly O(h)-accurate scalar reading of this particular flat target
must have order L^4 distinguishable classes; one fixed finite birth
algebra cannot suffice. This is a necessary resolution condition, not a
sufficient norm, physical admission, action-contrast or curved recovery
theorem. It does not transfer the metric conclusion to a different
observable or a conditional-expectation refinement without proof.

## 7. Consequence for the first native-preparation arrow

The literal scalar pro-equality is now classified once: it preserves an
old reading and cannot by itself generate increasingly resolved geometry.
Invoking it, or merely renumbering its fibres, cannot supply the missing
physical readout of a full-price preparation. Keeping records and adding
new admitted comparisons must be treated with their actual respective
arrows; the new observations need not be old scalar readings extended
backward. This matches the distinction between retained memory and newly
available resolution, without installing a replacement refinement rule.

Next derive **which newly available represented observations are admitted
by the native detector/recording/comparison preparation, with its budget**,
and their induced q,D,b,m and paired-probe transitions. The mathematical
space of all finite cylinder functions is not an admission proof. The full
heat/feedback/pairing/matter price and genuine internal-shell equations
must still descend through that readout; unchanged hidden modes cannot
be declared gauge or removed from the heat trace because this particular
scalar algebra misses them. No zero derivative, selector F, ceiling or
desired stationarity is made an admission criterion.

T0 remains open. Own source/Ward, all ten packed metric components and
six independent link directions per edge, fixed-calibration contrast,
native stationarity, curved joint roots, soundness/recovery and physical
constraints remain required. All forty-four canonical dependency contracts
and the original fixed-source/raw-owner #310 and independent #202/#317
terminals are preserved.

## Reproduction and proof boundaries

Run the [capsule](certificates/a4d_native_strict_observable_descent.lean)
from `03_FORMALIZATION` with `lake env lean ../02_REGISTRY/research/certificates/a4d_native_strict_observable_descent.lean`.
The [output](certificates/a4d_native_strict_observable_descent_output.txt)
and [receipt](certificates/a4d_native_strict_observable_descent_results.json)
retain real propositions, transitive axioms and pinned source inputs.
The [checker](certificates/a4d_native_strict_observable_descent_check.py)
and [certificate](certificates/a4d_native_strict_observable_descent_certificate.json)
check full actual successor composites, the explicit retained records,
strict/tail cylinder controls, actual periodic quotient connectivity,
vacuum CAR entries, packing and false-scope ledgers. Finite tests support
the analytic all-size proof; finite rank or numeric spectra are not used
as an all-size theorem.
