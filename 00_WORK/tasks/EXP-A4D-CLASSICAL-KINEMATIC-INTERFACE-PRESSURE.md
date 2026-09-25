# EXP-A4D-CLASSICAL-KINEMATIC-INTERFACE-PRESSURE

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Purpose

We are now close enough to a classical-looking local geometry that resemblance
is no longer evidence.

This task is a hostile **necessity / sufficiency audit** of the proposed
kinematic interface between the internal labelled relation geometry and an
ordinary local field/connection description.

The task must try to break the interface.

It must not assume in advance that:

- \`M = 0\`;
- \`R = 0\`;
- \`rank 𝓑 = 4\`;
- trivial labelled holonomy;

are four independent requirements, or even that all of them are necessary.

Derive the minimal interface from the owned equations.

## Read first

Read completely:

1. PR #123 / \`MEMO_A4D_RELATIVE_AE_COMPARISON_PRIMITIVE.md\`;
2. \`02_REGISTRY/research/MEMO_A4D_DIAGONAL_JUNCTION_OVERLAP_LAW.md\`;
3. \`02_REGISTRY/research/MEMO_A4D_LABELLED_REFERENCE_SELECTION_PRINCIPLE.md\`;
4. \`03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`;
5. \`03_FORMALIZATION/D0/Geometry/A4DReferenceJunctionCompressionBoundary.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/A4DRoleOverlapTwistedCocycle.lean\`;
7. PR #126 candidate \`A4DRelativeAEComparisonSpan.lean\` if not yet merged;
8. PR #125 candidate \`A4DConditionalSourcedDiagonalTransport.lean\` if not yet merged;
9. PR #124 candidate \`A4DRegularAEPassport.lean\` if not yet merged.

If any of #123–#126 are still unmerged at task start, treat their results as
provisional research/formal inputs and re-audit against then-current \`main\`
before Ready.

## Frozen internal objects

At one source site:

\[
\mathcal B:E_{\rm lab}\to V,
\qquad
\mathcal S:E_{\rm lab}\to V,
\]

\[
U=\operatorname{im}\mathcal B,
\qquad
K=\ker\mathcal B,
\]

\[
\mathscr R
=
\operatorname{im}(\mathcal B,\mathcal S)
\subset V\oplus V,
\]

\[
M=\mathcal S(K),
\]

and the rank-stratified canonical comparison

\[
J^{\rm can}:U\to V.
\]

For every Role label,

\[
R_r
=
\Delta v_r-J^{\rm can}\Delta b_r
=
\mathcal SP_K\varepsilon_r.
\]

The labelled path parent and endpoint-descent iff trivial labelled holonomy are
already owned.

## First mandatory question: how many seams are actually independent?

Prove or disprove, exactly:

\[
M=0
\iff
R_r=0\ \text{for every Role }r.
\]

If true, graphification and zero relative defect are the same seam globally,
not two independent classicality conditions.

Also keep separate the weaker statement

\[
R_r=0
\]

for one selected Role from the all-Role statement.

## Second mandatory question: is full rank actually classicality?

Audit the tempting condition

\[
\operatorname{rank}\mathcal B=4
\iff
U=V.
\]

Full rank implies:

- \(K=0\);
- \(M=0\);
- no extension freedom outside \(U\);
- \(J^{\rm can}\) is a full fibre endomorphism.

But determine whether this is **necessary for classical local geometry** or
only for global identifiability of the comparison on inactive directions.

Hostile controls:

### Constant pure affine shift

Here

\[
\mathcal B=\mathcal S=0,
\]

yet PR #120 keeps

\[
\delta=0,\qquad \kappa=b.
\]

A criterion declaring this background “nonclassical solely because rank is
zero” requires explicit justification.

### Exact translation-gauge rank drop

Use the L=3 gauge witness where the middle site has rank zero but exact
calibration and \(\kappa=0\) remain valid.

### Flat

Again \(U=0\), but the local geometry is not pathological merely because the
increment span vanishes.

These controls must decide whether full rank is:

- necessary;
- sufficient only;
- or merely an identifiability passport.

## Third mandatory question: active-span extension dependence

The PR #123 research claim is that downstream sourced transport only uses

\[
J^{\rm can}\Delta b_r.
\]

Test this through the **entire owned downstream chain**.

If two full extensions

\[
\widetilde J_1,\widetilde J_2:V\to V
\]

agree on \(U\), determine whether they produce exactly the same:

- relative defects \(R_r\);
- finite seed \(a_r\);
- predecessor decomposition;
- path sources;
- sourced solution space;
- selected mismatch \(\kappa\).

If all are identical, then full-rank/full-extension uniqueness is not part of
the physical kinematic seam.

## Fourth mandatory question: labelled path descent

Keep independent the path condition:

\[
\text{endpoint independence}
\iff
\text{all labelled loop holonomies trivial}.
\]

Audit whether relation graphification implies anything about labelled
holonomy.  It should not be assumed.

Likewise audit whether trivial labelled holonomy says anything about vertical
relation defect \(M\).  It should not be assumed.

## Candidate interface hierarchy

The task must test, not presuppose, the following hierarchy.

### Level K0 — relation geometry

General

\[
\mathscr R\subset V\oplus V,
\qquad M\ \text{possibly nonzero}.
\]

### Level K1 — active graph sector

\[
M=0.
\]

The relative A/e law is single-valued on actual affine increments.

### Level K2 — endpoint-local sector

K1 plus trivial labelled holonomy, so path provenance can be compressed to
endpoints.

### Level K3 — fully identifiable local comparison

K2 plus

\[
U=V.
\]

Here \(J^{\rm can}\) is uniquely known as a full endomorphism.

Determine whether K3 is genuinely a stronger physical/classical sector or only
a stronger epistemic/identifiability condition.

Do not call K3 “the classical sector” unless the hostile controls force that
conclusion.

## Mandatory logical-independence matrix

Construct exact examples for every logically possible separation that is not
algebraically forbidden.

At minimum:

1. \(M=0\), rank \(<4\), trivial holonomy;
2. \(M=0\), rank \(<4\), nontrivial holonomy;
3. \(M\ne0\) with trivial holonomy;
4. full-rank graph with nontrivial holonomy;
5. rank-jump family where relation stays finite but graph operator diverges.

If a requested combination is algebraically impossible, prove why.

In particular, because

\[
\dim E_{\rm lab}=\dim V=4,
\]

audit whether full rank automatically forces \(M=0\).

## Mandatory hostile physical controls

Keep literal:

- flat;
- constant pure affine shift;
- exact L=3 translation-gauge cycle;
- L=2 Nyquist;
- L=3 off-diagonal corner;
- duplicate affine increments with unequal solder increments;
- the rank-jump family
  \[
  \mathcal B_t\varepsilon_A=t e_A,\quad
  \mathcal S_t\varepsilon_A=e_B;
  \]
- one nontrivial labelled holonomy;
- exact L=2 positive-link period.

## Classical-language firewall

This task may establish an exact **kinematic interface passport**.

It may not claim:

- GR has been derived;
- a continuum manifold has been obtained;
- Einstein equations follow;
- QFT follows;
- finite \(F\) is constructed;
- a stress tensor exists;
- physical time has been derived.

“Classical” here means only:

- single-valued local relation on the relevant data;
- optionally endpoint-local path compression;
- optionally full fibre identifiability.

Use those words literally.

## Constitutive firewall

Finite graded \(F\) is still a separate dynamical seam.

Do not use success of a kinematic passport to bypass the finite-\(F\) gate.

## Pressure requirement

For every proposed equivalence or interface theorem include:

- one positive exact witness;
- one nearest negative witness;
- one rank-degenerate witness;
- one labelled-holonomy witness.

A theorem without hostile controls is incomplete.

## Preferred terminals

Positive:

- \`CLASSICAL-KINEMATIC-INTERFACE-PASSPORT-CONSTRUCTED\`;
- \`ACTIVE-GRAPH-PLUS-LABELLED-DESCENT-IS-MINIMAL-KINEMATIC-INTERFACE\`;
- \`FULL-RANK-IS-IDENTIFIABILITY-NOT-CLASSICALITY\`.

Scoped negative:

- \`KINEMATIC-CLASSICAL-INTERFACE-REQUIRES-ADDITIONAL-LOCALITY-DATUM\`;
- \`GRAPHIFICATION-DOES-NOT-SUFFICE-FOR-ENDPOINT-LOCALITY\`.

Use only the strongest result actually proved.

## Deliverable

One durable theorem-ready memo with:

1. exact seam definitions;
2. proof/refutation of \(M=0\iff\forall r\,R_r=0\);
3. full-rank audit;
4. full-extension-independence audit;
5. labelled-holonomy independence;
6. logical-independence matrix;
7. hostile finite controls;
8. exact minimal kinematic passport;
9. explicit statement of what remains nonclassical/dynamical;
10. theorem-ready handoff;
11. exactly one next pressure step.

No Lean source.

## GitHub-first flow

Fresh current \`main\` → lifecycle start → Draft PR immediately → research
inside PR → durable memo → self-retire → \`Lifecycle: REVIEW\` → Ready →
do not self-merge.

## Exit condition

The minimal necessary-and-sufficient kinematic interface from labelled
relation geometry to an ordinary local/endpoint description is derived and
survives the full hostile witness matrix, with full-rank identifiability,
graphification/relative-defect vanishing, and labelled-holonomy descent
correctly separated rather than assumed equivalent.
