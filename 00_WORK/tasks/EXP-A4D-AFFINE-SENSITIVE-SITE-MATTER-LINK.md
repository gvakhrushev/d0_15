# EXP-A4D-AFFINE-SENSITIVE-SITE-MATTER-LINK

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Start gate

SATISFIED on current \`main\` after merged PR #103, PR #107 and PR #108.

The parallel workers

- \`WRK-A4D-LABELLED-PATH-HOLONOMY-DESCENT\`;
- \`WRK-A4D-AFFINE-SHIFT-EXTERIOR-BLINDNESS\`

may run concurrently. Do not wait for them. Treat their target statements as theorem-ready until merged, and replace research restatements with literal Lean owners if they land during this task.

## Read first

Read completely, in this order:

1. \`02_REGISTRY/research/SYNTHESIS_A4D_ELEMENTARY_MATTER_LINK_THREE_CHANNEL.md\`;
2. \`02_REGISTRY/research/MEMO_A4D_PATH_GROUPOID_CROSSED_MATTER_LIFT.md\`;
3. \`02_REGISTRY/research/MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md\`;
4. \`02_REGISTRY/research/MEMO_A4D_CROSSED_CONSTITUTIVE_REPRESENTATION.md\`;
5. \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean\`;
7. \`03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean\`;
8. \`03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean\`;
9. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean\`;
10. \`03_FORMALIZATION/D0/Geometry/A4DLocatedFrameCompatibilityBoundary.lean\`;
11. \`03_FORMALIZATION/D0/Geometry/A4DCrossedDerivationIntegrability.lean\`;
12. PR #70 affine/path owners;
13. PR #101/#102 crossed first-jet/path-expression owners.

## Updated research thesis

Do **not** reopen the problem as:

- choose \(Q(e)\);
- choose a scalar coefficient;
- choose \(\mathcal S\);
- choose a universal \(K\);
- invent an abstract \(C_N\) and only later ask what one edge means.

The surviving fixed-N object is one positive labelled elementary matter arrow

\[
\ell_N^+(A,e,n;x,r):
V_{x+r}\xrightarrow{\sim}V_x,
\]

or an explicitly typed site-corner/path-expression equivalent if one local fibre map is too small.

The negative arrow is the shifted inverse.

The path transport

\[
\Pi_{A,e,n}(x;p)
\]

is **defined by the ordered product of these letters**. It is not an independent primitive.

The constitutive/energy object \(W\) is an explicit global assembly/section transported by the same arrow/word structure. It is not a second selector.

The heavy research problem is now:

> integrate the already-owned tangent/path data into one finite elementary letter and one assembly law.

## Frozen ownership

The repository already owns:

### Channel L — linear Cartan/exterior transport

PR #103 owns the exterior/frame/observer lift of the **linear** affine Cartan path transport on the existing 16-state Fock carrier, including exact composition, inverse, observer form and frame covariance.

The parallel blindness worker is formalizing the fact that this channel factors through the linear affine path part and is blind to a pure translation \((I,b)\).

Do not ask again whether the existing exterior transport sees \(b\).

### Channel E — raw coframe/constitutive tangent

PR #75 owns the complete uncentered first jet \(H(e)\).

PR #101 owns the exact pure-gauge chart.

PR #102 owns the additive path-expression support of the first jet.

PR #108 owns the scalar **infinitesimal descent constraints** for the landed first-jet law at \(L\ge3\):

- zero cycle sum;
- plaquette/closedness identity.

These #108 equations are not yet an exact nonlinear theorem about the unknown finite letter. They are the tangent equations the finite descended relations of the letter must differentiate to.

### Labelled word skeleton

PR #107 research-classifies the free labelled path parent and the descent boundary.

The labelled-path worker is formalizing:

- exact empty/append/reverse/inverse;
- endpoint independence iff trivial labelled holonomy;
- the exact \(L=2\) parallel-slot period consequence.

### Fixed-J boundary

PR #103 plus existing located owners already fix the observer/frame substrate and the located anchor obstruction.

The primal letter comes first. \(J\) only dualizes it afterward.

## One letter, three channels

The input \((A,e,n)\) contains three distinct mathematical roles.

### L — linear Cartan channel

Already owned.

It supplies the exterior lift of the linear part of the affine link.

### E — coframe amplitude / constitutive channel

Owned only at tangent level.

Its finite integration must be such that the global assembly has

\[
W_0=I,\qquad D_eW_0[e]=H(e).
\]

### B — affine translational/site channel

Missing.

This channel must make a pure affine translation \((I,b\ne0)\) visible somewhere in the elementary/site/path action if the claimed construction is affine-sensitive.

The current fibre-only exterior channel cannot do that.

### Critical rule

Do **not** assume in advance that

\[
\ell^+=\ell_L\,\ell_E\,\ell_B
\]

with commuting factors.

That is only one hypothesis.

The task must determine the actual coupling law:

- direct product;
- semidirect/crossed product;
- triangular/site-corner extension;
- path-expression corner;
- another explicit typed construction.

If no coupling works, identify the earliest failed coupling law.

## Objective

Construct or terminally classify one fixed-N positive elementary matter letter plus assembly with all of the following typed simultaneously:

\`\`\`text
ellPlus(A,e,n;x,r)
negative = shifted inverse
Pi(A,e,n;x;steps) = ordered product of ellPlus
W(A,e,n) = explicit global/site-corner assembly or section
\`\`\`

The target may enlarge a same-site \(16\times16\) fibre, but the enlargement must retain literal archive/site support and be explicit.

A phrase such as "take a representation of the affine group" is not a construction.

## Mandatory attack

### A. Exact carrier and corner typing

State the precise source and target of one positive letter.

Record:

- source site;
- target site;
- Fock degree/parity behavior;
- site idempotents/corners if global;
- whether it acts on one Fock fibre, a site corner of the global cochain carrier, or an enlarged typed fibre;
- the algebra in which inverse and multiplication live.

A global matrix with no site-corner typing is not sufficient.

### B. Negative letter is not independent

Define the negative letter by the shifted inverse of the positive letter in the literal archive convention.

Then derive the one-step reverse identity.

Do not introduce two unrelated directional links.

### C. Recover Channel L exactly

In the zero site-translation / flat amplitude limit, the positive letter must reduce exactly to the PR #103 exterior lift of the linear Cartan link.

For paths whose affine translation channel is trivial, products of the new letters must recover \`exteriorPathTransport\`.

This is an equality requirement, not just a continuum analogy.

### D. Construct Channel B — the actual new work

The link must distinguish a pure affine path/loop value

\[
(I,b),\qquad b\ne0,
\]

from the identity **if** the claimed target is affine-sensitive.

Use an exact \(L=3\) witness.

The response must carry site/path support. A translation acting only in an auxiliary fibre while the physical archive/site action remains unchanged does not solve the missing support problem unless an explicit projection/assembly back to the owned carrier is proved.

### E. Integrate Channel E into the same object

The complete owned \(H(e)\) is additive and has path-word length at most two.

The elementary letter is multiplicative.

Do not write \(H=\log\ell\) and stop.

Define an explicit assembly

\[
\operatorname{Asm}(\ell)(A,e,n)=W_{A,e,n}
\]

or an equivalent site-corner/global construction and prove or derive

\[
W_0=I,
\qquad
D_eW_0[e]=H(e)
\]

for arbitrary uncentered raw coframe directions in the claimed scope.

The derivative must recover literally:

- scalar edge polarization;
- both half-average pieces;
- mixed CAR blocks;
- both corner paths;
- \(L=2\) Nyquist sensitivity;
- \(L=3\) corner coefficient.

If a local letter cannot produce the additive first jet without an additional assembly datum, say exactly what assembly datum is missing. Do not rename that gap "another constitutive selector."

### F. Integrate PR #108 as the tangent of exact finite relations

This is now a central requirement.

In any sector where the labelled action descends to the compressed periodic endpoint algebra, derive the **exact finite cycle word relation** in the literal pull order:

\[
\ell_t(x)\ell_t(x+t)\cdots\ell_t(x+(L-1)t)=I.
\]

Differentiate this finite identity at the flat configuration and require the result to be exactly the #108 zero-cycle-sum theorem.

Likewise derive the exact descended plaquette equality:

\[
\Pi(x;[s,t])=\Pi(x;[t,s])
\]

in the repository's actual order.

Differentiate it and require the result to be exactly the #108 plaquette/closedness theorem.

This is the key integration test.

Do not merely check #108 afterward as an unrelated diagnostic.

### G. Keep generic curl/harmonic data free-path resolved

For generic backgrounds:

- plaquette curl is nontrivial relative labelled holonomy;
- harmonic period is nontrivial cycle holonomy.

Do not impose the finite cycle/plaquette identities before descent.

Endpoint compression is derived only after the relevant labelled holonomy is trivial.

### H. L=2 exact period

At \(L=2\), keep \`.fwd r\` and \`.bwd r\` as distinct labels.

When endpoint descent is imposed, derive/use the exact finite relation

\[
\ell^+(x,r)\,\ell^+(x+r,r)=I
\]

in the actual pull order.

Do not replace this by the centered fact that the #108 response formula degenerates at \(L=2\).

Both facts are required and they are different:

- #108: tangent scalar formula is zero at \(L=2\);
- labelled descent: exact finite period relation survives.

### I. Pure-gauge exact chart

For

\[
e=d_f\varphi,
\]

compare with the exact owned PR #101 chart

\[
\ell_t=F_\varphi U_tF_\varphi^{-1}.
\]

The new letter must either specialize to this law exactly or come with a proved typed equivalence to it.

Do not identify arbitrary raw \(e\) with a gauge potential.

### J. Keep \(A\), \(e\), \(n\) separate

Do not silently set \(A=A(e)\).

If the new Channel-B/E coupling needs a solder-Cartan compatibility map, derive it from an explicit principle inside this task or make that missing map the terminal.

Observer \(n\) enters through the owned \(h_n\) covariance structure.

It is not a fourth channel and is not physical time.

### K. Observer/frame covariance

Only after the primal letter exists, prove/test compatibility with the merged PR #103 owners:

- linear exterior covariance;
- moving observer-positive form;
- creator/contraction covariance where applicable;
- exact rational A/B boost.

Observer covariance constrains transport. It does not select an arbitrary scalar/Hessian coefficient.

### L. Fixed located-J dualization

Only after the primal letter and word action exist, derive the dual via fixed located \(J\).

Preserve:

- Fock degree/parity;
- complement orientation/sign;
- shifted anchors;
- distinction between common-fibre contragredience and sitewise archive placement.

If degree mixing produces a sum of shifted dual blocks, keep the sum. Do not force a single bare dual word.

## Candidate carriers to test

At minimum compare:

### 1. Current 16-state exterior fibre

Expected positive:
- exact Channel-L frame/path action.

Expected boundary:
- affine translation blindness.

Do not reject the carrier globally merely because the current action is blind; test whether site-corner coupling can use the same Fock fibre while adding archive support externally.

### 2. PR #101 nilpotent 16-state affine candidate

Test:

- translation sensitivity;
- degree/parity;
- normalization of the owned degree algebra;
- site support;
- pure-gauge chart;
- first-jet assembly;
- invertibility/path product.

### 3. Homogeneous 32-state affine exterior lift

Test:

- honest affine sensitivity;
- whether translations act nontrivially on the original physical \(16\)-state sector or only the auxiliary sector;
- return/projection to the owned archive matter carrier;
- site support;
- first jet;
- observer covariance;
- located-J consequences.

### 4. Site-corner/path-expression enlargement

This is the primary candidate class.

Test a construction in which site idempotents/path shifts are part of the letter target algebra while the local Fock fibre remains the owned \(16\)-state exterior carrier.

Determine whether this is the minimal target that simultaneously supports:

- Channel L;
- affine translation sensitivity;
- the path supports already present in \(H(e)\);
- exact inverse and labelled path multiplication.

## Required hostile controls

Use exact rational/symbolic controls for:

- flat identity background;
- one pure-gauge background;
- \(L=3\) pure affine translation \((I,b\ne0)\);
- \(L=3\) plaquette curl;
- \(L=3\) mixed corner;
- \(L=5\) nonzero harmonic cycle;
- \(L=2\) Nyquist;
- \(L=2\) parallel \`.fwd/.bwd\` labels and exact period;
- all five Fock degrees;
- parity;
- exact rational A/B Lorentz boost;
- one same-endpoint pair distinguished by affine shift before descent;
- one background where cycle/plaquette descent relations hold;
- one background where nontrivial labelled holonomy prevents descent.

## Second-order firewall

Do not open a separate \(Q\), \(\mathcal S\), \(K\), Hessian or scalar-coefficient search.

If the finite elementary letter plus assembly is constructed, then a same-axis two-letter product and the second derivative of \(W\) may be inspected as consequences.

If second-order freedom remains, record it as a jet of the already-constructed letter/assembly package.

Do not select it by hand.

## Tick interpretation firewall

A length-one positive letter may be described as the minimal algebraic distinguishability step of this fixed-N action.

A longer word is composition.

A closed word with trivial labelled holonomy returns to identity after descent.

Do not promote this operational statement to physical time, the Pisot arrow, causal \(e_0\), or golden refinement.

## Golden firewall

Do not use:

- \(\varphi\);
- AF/Bratteli index;
- a \(k=n\) rule;
- Tower-C scale data;

inside the fixed-N elementary letter.

The Tower-C ↔ Tower-B correspondence-grid path-selection problem is separate.

## Allowed terminals

Use the strongest terminal actually derived.

Preferred positive terminals include:

- \`AFFINE-SENSITIVE-ELEMENTARY-MATTER-LINK-AND-FIRST-JET-ASSEMBLY-CONSTRUCTED\`;
- \`SITE-CORNER-MATTER-LINK-CONSTRUCTED-PR108-FINITE-RELATIONS-INTEGRATED\`.

Scoped partial terminals include:

- \`SITE-CORNER-AFFINE-LINK-CONSTRUCTED-FIRST-JET-ASSEMBLY-MISSING\`;
- \`FIRST-JET-ASSEMBLY-CONSTRUCTED-AFFINE-TRANSLATION-CHANNEL-MISSING\`;
- \`AFFINE-MATTER-LINK-REQUIRES-SOLDER-CARTAN-COMPATIBILITY-PRIMITIVE\`;
- \`ELEMENTARY-LINK-INTEGRATION-FAILS-AT-CHANNEL-B-E-COUPLING\`.

Do **not** end merely with:

\`CROSSED-CONSTITUTIVE-REPRESENTATION-REQUIRED\`

unless the research proves that the elementary-link integration problem itself cannot be sharpened further.

## Deliverable

One durable theorem-ready memo in \`02_REGISTRY/research/\`.

It must contain:

1. exact carrier and site-corner typing;
2. positive letter;
3. shifted negative inverse;
4. product definition of labelled path transport;
5. exact Channel-L reduction;
6. Channel-B affine translation result;
7. explicit \(W\)/assembly rule;
8. complete first-jet calculation;
9. exact finite cycle relation and derivative-to-#108 calculation;
10. exact finite plaquette relation and derivative-to-#108 calculation;
11. \(L=2\) labelled period;
12. pure-gauge PR #101 comparison;
13. generic curl/harmonic holonomy boundary;
14. observer/frame covariance;
15. fixed-J dual result;
16. candidate carrier comparison;
17. hostile controls;
18. terminal verdict;
19. theorem-ready handoff;
20. exactly one recommended next step.

No Lean source.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start EXP-A4D-AFFINE-SENSITIVE-SITE-MATTER-LINK\`;
3. immediately open Draft PR before research edits;
4. research and durable memo only inside that PR;
5. before Ready self-retire the task;
6. set \`Lifecycle: REVIEW\`;
7. Ready for review;
8. do not self-merge.

## Exit condition

One fixed-N positive elementary matter letter is constructed or terminally classified on an explicit site-aware carrier such that its products define the labelled word action, its linear limit is the owned PR #103 exterior transport, its affine translation channel is explicitly resolved, its global assembly has first derivative equal to the complete owned \(H(e)\), its exact descended cycle/plaquette relations linearize to the PR #108 constraints, and its \(L=2\) endpoint descent obeys the exact labelled period; otherwise the earliest failed coupling among the L/E/B channels is identified as the next primitive without reopening \(Q\), \(\mathcal S\), \(K\), stress, Einstein, physical time or golden refinement.
