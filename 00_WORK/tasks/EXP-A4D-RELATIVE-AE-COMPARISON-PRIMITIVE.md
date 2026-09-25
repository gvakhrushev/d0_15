# EXP-A4D-RELATIVE-AE-COMPARISON-PRIMITIVE

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Baseline

Start from fresh current \`main\` after merged PR #120 or newer.

## Read first

Read completely:

1. \`02_REGISTRY/research/MEMO_A4D_DIAGONAL_JUNCTION_OVERLAP_LAW.md\`;
2. \`02_REGISTRY/research/MEMO_A4D_LABELLED_REFERENCE_SELECTION_PRINCIPLE.md\`;
3. \`03_FORMALIZATION/D0/Geometry/A4DRoleOverlapTwistedCocycle.lean\`;
4. \`03_FORMALIZATION/D0/Geometry/A4DReferenceJunctionCompressionBoundary.lean\`;
5. \`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/A4DAffineOriginSolderBoundary.lean\`;
7. observer/frame owners from PR #103.

## Frozen frontier

PR #120 has already constructed the entire diagonal-selection mechanism
**conditional on one missing comparison primitive**.

For \(x=y-r\), define the source-fibre increments

\[
\Delta^b_r(y)
=
b_{y,r}-L_{x,r}^{-1}b_{x,r},
\]

\[
\Delta^v_r(y)
=
v_r(e,y)-L_{x,r}^{-1}v_r(e,x).
\]

The missing object is a source-fibre comparison map

\[
\mathfrak J_y(A,e):V_y\to V_y
\]

or an exactly equivalent edge-labelled partial map/relation, with

\[
\mathfrak J'_y=g_y\mathfrak J_y g_y^{-1}
\]

and exact translation-gauge calibration

\[
\mathfrak J_y\Delta^b_r=\Delta^v_r.
\]

Given such a primitive, PR #120 already owns at research level:

- the relative defect
  \[
  \mathfrak R^{A/e}=\Delta^v-\mathfrak J\Delta^b;
  \]
- the finite diagonal seed
  \[
  a_r=-\bar b_r-\mathfrak J\Delta^b_r;
  \]
- sourced append/reverse transport;
- classification \(\delta=a+h\) with \(h\) parallel;
- post-source observer-positive removal of the holonomy-fixed kernel;
- exact flat / pure-gauge / pure-shift / L=2 / L=3 controls;
- local rejection of \(z_{\rm curl}\);
- global rejection of \(z_{\rm harm}\).

Do not reopen those solved layers.

## Positive regular branch already known

Package the raw solder legs as

\[
B_e(x):V_{\rm ref}\to V_x,
\qquad
B_e(x)e_s=v_s(e,x),
\]

and affine shifts as

\[
C_A(x):V_{\rm ref}\to V_x,
\qquad
C_A(x)e_s=b_{x,s}.
\]

On the branch where \(B_e\) is invertible,

\[
K=B_e^{-1}C_A
\]

is frame invariant.

On the translation chart, with shift matrix \(D\),

\[
B=I+\eta D,\qquad C=D,
\]

and

\[
D-\eta D K=K.
\]

If

\[
\mathcal L_K:X\mapsto X-\eta XK
\]

is invertible, this reconstructs a unique translation-chart representative.

This is a **regular passport**, not a global selector.

## Objective

Construct or terminally classify the relative \(A/e\) comparison primitive
globally, including rank-deficient / singular raw-solder backgrounds.

The task must decide whether the correct object is:

1. a full endomorphism \(\mathfrak J_y\);
2. an edge-labelled partial linear map defined only on the span of actual
   increments \(\Delta^b_r\);
3. a linear relation / quotient map;
4. a rank-stratified extension of the regular passport;
5. or genuinely new geometric data.

Do not force a full endomorphism if the data only determine a smaller object.

## Mandatory acceptance laws

A successful primitive or equivalent must satisfy:

### 1. Pure-linear covariance

\[
\mathfrak J'_y=g_y\mathfrak J_yg_y^{-1},
\]

or the corresponding covariance law for the chosen partial/relation object.

### 2. Exact translation-gauge calibration

On the entire exact translation-gauge orbit,

\[
\mathfrak J_y\Delta^b_r=\Delta^v_r
\]

for every Role \(r\).

### 3. Flat compatibility

No spurious source when

\[
A=A_{\rm flat},\qquad e=0.
\]

### 4. Pure affine-shift compatibility

A constant pure shift must remain visible after the downstream PR #120
selection mechanism.

The primitive must not force \(\delta=-b\).

### 5. Degenerate raw-solder locus

Explicitly handle backgrounds where \(B_e\) is singular.

Do not silently restrict the physical configuration space to
\(\det B_e\ne0\).

### 6. Singular reconstruction locus

Explicitly handle or classify the locus where

\[
X\mapsto X-\eta XK
\]

is singular.

### 7. Rational boost firewall

Use the exact owned A/B rational boost.

Fixed numerical \(\eta\) as a vector endomorphism is not covariant; the new
object must pass the literal conjugation law.

### 8. Role-labelled compatibility

The comparison must not erase Role labels or collapse the labelled-path parent.

### 9. Longitudinal necessity

Retain PR #120's result that curvature/torsion/curl alone cannot distinguish
exact translation gauge from pure affine shift.

The primitive must carry the missing longitudinal \(A/e\) correlation.

## Mandatory candidate classes to test

### A. Span-only comparison

At each site define

\[
U_y=\operatorname{span}\{\Delta^b_r(y)\}_r.
\]

Ask whether the calibration data determine a canonical linear map

\[
J_y^{\rm span}:U_y\to V_y,
\qquad
J_y^{\rm span}(\Delta^b_r)=\Delta^v_r.
\]

Derive the exact well-definedness criterion:

every linear relation among the \(\Delta^b_r\) must be obeyed by the
corresponding \(\Delta^v_r\).

Test covariance and rank changes.

This is the highest-priority constructive route.

### B. Graph / linear-relation primitive

If span-map well-definedness fails on generic backgrounds, test the canonical
relation generated by pairs

\[
(\Delta^b_r,\Delta^v_r)\subset V_y\oplus V_y.
\]

Classify when that relation is the graph of a map and what extra selection is
needed otherwise.

### C. Rank-stratified regular passport

Use the positive \(K=B^{-1}C\) branch as an anchor.

Determine whether its reconstructed comparison extends continuously/algebraically
to lower-rank strata or whether extension is nonunique/singular.

### D. Generalized inverse / observer metric

Audit pseudoinverse-like constructions using the owned positive \(h_n\).

They are allowed only as **post-geometric extension tools**.

If they make the source depend on arbitrary observer choice, classify that
failure explicitly.

### E. Quotient comparison

If \(\ker \Delta^b\) is the obstruction, test whether the correct object lives
on a quotient of the Role-labelled input space rather than as an endomorphism
of \(V_y\).

### F. Orbitwise extension

Test whether a comparison can be defined canonically on pure-linear frame
orbits once one representative is known, and classify stabilizer ambiguity.

## Required hostile controls

At minimum include:

- exact L=3 translation-gauge cycle \((3,3,-6)e_B\);
- constant nonzero pure affine shift;
- L=2 Nyquist coframe;
- L=3 off-diagonal corner;
- one rank-deficient solder example;
- one singular \(\mathcal L_K\) example if such a point exists;
- exact rational A/B boost.

## Nonuniqueness firewall

If a primitive is determined only on
\(\operatorname{span}\{\Delta^b_r\}\), do not arbitrarily extend it to all of
\(V_y\) and call the extension canonical.

Classify the extension freedom.

## Observer firewall

Do not use \(h_n\) to manufacture the longitudinal source before the geometric
comparison is determined.

Observer positivity remains a downstream kernel/extension tool unless a theorem
proves observer-independence.

## Finite-E firewall

Do not start \`EXP-A4D-FINITE-GRADED-COFRAME-DRESSING\`.

That gate opens only after a usable global relative \(A/e\) comparison primitive
or explicitly adopted equivalent datum lands.

## Other firewalls

Do not:

- identify \(A=A(e)\);
- reopen affine representability;
- reopen row/vector typing;
- reopen sourced transport already solved in PR #120;
- reopen observer-kernel algebra;
- use \([H,T_b]\) as the bridge;
- start stress/Einstein/time/golden work;
- select the second jet.

## Preferred terminals

Positive:

- \`RELATIVE-AE-COMPARISON-PRIMITIVE-CONSTRUCTED\`;
- \`RELATIVE-AE-SPAN-MAP-CONSTRUCTED\`;
- \`RELATIVE-AE-LINEAR-RELATION-CONSTRUCTED\`.

Scoped:

- \`RELATIVE-AE-COMPARISON-REQUIRES-NEW-RANK-STRATIFIED-DATUM\`;
- \`RELATIVE-AE-COMPARISON-REQUIRES-OBSERVER-INDEPENDENT-EXTENSION-PRINCIPLE\`;
- \`OWNED-GEOMETRY-DOES-NOT-EXTEND-REGULAR-AE-PASSPORT-GLOBALLY\`.

Use only the strongest result actually established.

## Deliverable

One durable theorem-ready memo containing:

1. exact input/output type of the comparison object;
2. span-map well-definedness criterion;
3. covariance;
4. translation-gauge calibration;
5. regular passport compatibility;
6. degenerate-locus audit;
7. singular-reconstruction audit;
8. rank-stratified / relation / quotient alternatives;
9. observer/generalized-inverse audit;
10. hostile controls;
11. exact terminal;
12. theorem-ready handoff;
13. exactly one next step.

No Lean source.

## GitHub-first flow

Fresh branch → lifecycle start → Draft PR immediately → deep research →
durable memo → self-retire → \`Lifecycle: REVIEW\` → Ready → do not self-merge.

## Exit condition

A global relative \(A/e\) comparison primitive or equivalent canonical
rank-stratified/span/relation object is constructed and shown to satisfy exact
gauge calibration plus frame covariance across the degenerate locus, or the
earliest additional geometric datum required for such a global extension is
terminally identified.
