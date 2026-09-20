# Research Brief C1-X — canonical common carrier between A1 gravity and signed Hodge matter

## Role

You are the expensive research-only agent.

Do not inspect GitHub.
Do not write Lean.
Do not summarize the D0 project.
Do not search broadly unless absolutely necessary.

Work only on the finite linear-algebra / representation problem below and return a compact mathematical memo with exact formulas, proofs or no-go statements, and theorem-ready outputs.

## Why this task

The A1 gravity mechanism is now structurally clear:

- gravity edge responses live in the kernel of an UNSIGNED incidence/divergence operator B_+;
- the existing matter/Hodge language uses the usual SIGNED incidence B_-.

For K(9,11,13), these are not the same complex and cannot be related by a trivial sign switching of rows/columns because the graph is non-bipartite.

The task is to determine whether there is nevertheless a canonical D0-specific common carrier / embedding, and if so construct it explicitly.

## Frozen scene

Let

V = V_9 disjoint-union V_11 disjoint-union V_13

with sizes

|V_9|=9, |V_11|=11, |V_13|=13.

The edge space is

E = E_9,11 direct-sum E_9,13 direct-sum E_11,13

with dimensions

99 + 117 + 143 = 359.

Identify an edge field with three real matrices

X_9,11 in R^(9 x 11),
X_9,13 in R^(9 x 13),
X_11,13 in R^(11 x 13).

The automorphism subgroup preserving the intrinsic degree zones is

H = S_9 x S_11 x S_13.

Because the zone sizes/degrees are distinct, the three zones are intrinsically distinguishable.

## Unsigned gravity divergence B_+

B_+ : R^E -> R^V is the row-sum / endpoint-sum operator:

for u in V_9:
  (B_+ X)(u) = rowSum(X_9,11)(u) + rowSum(X_9,13)(u);

for v in V_11:
  (B_+ X)(v) = colSum(X_9,11)(v) + rowSum(X_11,13)(v);

for w in V_13:
  (B_+ X)(w) = colSum(X_9,13)(w) + colSum(X_11,13)(w).

This is exactly the A1 row divergence.

Known exact facts:

rank(B_+) = 33,
dim ker(B_+) = 359 - 33 = 326.

The A1 physical response G_phys lies in ker(B_+).

## Signed Hodge incidence B_-

Choose the intrinsic transitive zone orientation

V_9 -> V_11,
V_9 -> V_13,
V_11 -> V_13.

Let B_- be the usual oriented incidence/divergence.

For this connected graph:

rank(B_-) = 32,
dim ker(B_-) = 359 - 32 = 327.

There is no diagonal sign-switch equivalence B_+ <-> B_- on the full edge/vertex spaces:
such an equivalence exists iff the graph is bipartite; K(9,11,13) contains triangles.

Treat this as given unless you discover a flaw.

## H-representation decomposition already derived

Write

R^9  = 1 + A_9,   dim A_9=8,
R^11 = 1 + A_11,  dim A_11=10,
R^13 = 1 + A_13,  dim A_13=12,

where A_n is the standard zero-sum representation.

Then the edge space decomposes as

R^E =
  1^3
  + A_9^2
  + A_11^2
  + A_13^2
  + (A_9 tensor A_11)
  + (A_9 tensor A_13)
  + (A_11 tensor A_13).

Dimensions:

trivial: 3,
two A_9 copies: 16,
two A_11 copies: 20,
two A_13 copies: 24,
A_9 tensor A_11: 80,
A_9 tensor A_13: 96,
A_11 tensor A_13: 120,

total 359.

Define the blockwise double-centering projectors

C_n = I_n - (1/n) 1 1^T,

P_ab(X) = C_a X C_b.

The direct sum

K_0 =
 im P_9,11
 direct-sum im P_9,13
 direct-sum im P_11,13

has dimension

8*10 + 8*12 + 10*12 = 296.

Every element of K_0 has zero row and column margins in every block.

Therefore K_0 is contained in both ker(B_+) and ker(B_-) for any zone-pair orientation.

## More exact structure for the transitive orientation

For the intrinsic orientation 9 -> 11 -> 13:

ker(B_+) has H-type

K_0 + A_9 + A_11 + A_13

dimension

296 + 8 + 10 + 12 = 326.

ker(B_-) has H-type

K_0 + A_9 + A_11 + A_13 + 1

dimension

327.

However, the actual A_11 kernel lines inside the two A_11 copies differ between B_+ and B_-.

For an A_11 vector represented by coefficients (alpha,beta) on
E_9,11 and E_11,13 respectively:

B_+ condition:
  9 alpha + 13 beta = 0.

B_- condition:
  9 alpha - 13 beta = 0.

Thus convenient spanning lines are

v_+ = (13,-9),
v_- = (13,+9).

With the natural edge inner product, the multiplicity-space metric is diag(9,13).

Hence

< v_+, v_- > = 9*13^2 - 13*9^2
               = 9*13*(13-9),

||v_+||^2 = ||v_-||^2
          = 9*13*(13+9),

so the normalized overlap is

cos(theta_11) = (13-9)/(13+9) = 4/22 = 2/11.

This is nonzero.

For A_9 and A_13, the unsigned and signed kernel lines coincide under this transitive orientation.

Therefore the orthogonal projection

P_- restricted to ker(B_+)

is expected to have singular values

1 on 316 dimensions,
2/11 on the 10-dimensional A_11 sector,

and hence be injective.

The 1-dimensional complement in ker(B_-) is the zone-level oriented triangle circulation.
For block-constant values (x_9,11, x_9,13, x_11,13), one convenient nonzero cycle is proportional to

(13, -11, 9),

because

-11*x_9,11 -13*x_9,13 = 0,
  9*x_9,11 -13*x_11,13 = 0,
  9*x_9,13 +11*x_11,13 = 0.

Verify all normalization details yourself.

## Single research question

Does there exist a canonical, automorphism-equivariant and orientation-natural common carrier map

U : ker(B_+) -> ker(B_-)

suitable for binding the A1 gravity response to the signed Hodge/matter current space?

If yes, construct the strongest natural U and characterize its image and one-dimensional complement exactly.

If no, prove the sharpest no-go under explicit naturality/locality assumptions.

## Candidate constructions to analyze

### Route 1 — orthogonal projection

Let P_- be the orthogonal projector onto ker(B_-).

Analyze

F = P_- | ker(B_+).

Questions:

1. Is F injective for K(9,11,13)?
2. Are its singular values exactly 1 and 2/11 with multiplicities 316 and 10?
3. Is the image exactly the codimension-one orthogonal complement of the trivial zone-circulation mode?
4. Does F commute with H=S_9 x S_11 x S_13?
5. How does F transform if the orientation convention on zone pairs is changed?

### Route 2 — polar-normalized embedding

If F is injective, define

U = F (F^* F)^(-1/2)

on ker(B_+).

This is a canonical isometric embedding once inner products and orientation are fixed.

Determine whether U admits an explicit sectorwise formula:

- identity on K_0,
- identity on A_9 and A_13,
- a fixed 2x2 multiplicity-space map on A_11.

Give exact coefficients for the 9/11/13 scene.

### Route 3 — direct representation-theoretic intertwiner

Classify

Hom_H(ker(B_+), ker(B_-)).

Because each A_9,A_11,A_13 and each tensor product appears with multiplicity one inside each kernel,
an H-equivariant map should be sectorwise scalar after the kernel lines are fixed.

Determine:
- dimension of Hom_H;
- which additional conditions (isometry, locality, orientation naturality, block support) make U unique;
- whether degree ordering 9<11<13 is sufficient to remove orientation ambiguity canonically.

### Route 4 — literal common subspace K_0

If no full 326-dimensional canonical embedding survives orientation/naturality requirements, determine whether

K_0, dim 296,

is the maximal canonical common subspace.

Prove or disprove:

K_0 = maximal H-invariant subspace that is simultaneously divergence-free for B_+
and for every zone-pair orientation of B_-.

Be careful:
- "every arbitrary edge orientation" would force a much smaller/trivial space;
- the intended orientation family is uniform orientation per zone pair.

## Matter/gravity relevance test

Do not stop at an abstract intertwiner.

For the preferred construction, answer:

1. Given G_phys in ker(B_+), what is J_mg(G_phys) in the signed Hodge carrier?
2. Is conservation automatic:
   B_- J_mg(G_phys)=0?
3. Is the map injective?
4. What physical/mathematical meaning does the 1D Hodge complement have?
5. Does the map preserve the blockwise high-frequency/double-centered sector K_0 exactly?
6. Which 30 standard-zone modes are altered by the map?
7. Is there a natural adjoint map from matter currents back to gravity sources?
8. Can one define a projector
   T_matter -> image(U)
   without choosing empirical coefficients?

## Weak-field / continuum sanity test

We are NOT asking for a full continuum proof.

But determine whether the signless symmetric-gradient operator J_+=B_+^T is better interpreted as a discrete symmetric-gradient / Killing-type operator rather than an ordinary 1-form coboundary.

State clearly:

- what the closest continuum linear operator is;
- whether its adjoint is a divergence of a symmetric tensor;
- which features of C' are compatible with that analogy;
- which features are too weak to claim a discrete diffeomorphism.

This section should be mathematical, not rhetorical.

## Required outputs

Return exactly these sections.

### 1. Verdict
Maximum one page.
Choose:
- canonical 326 -> 327 embedding exists;
- only canonical 296 common carrier exists;
- or a precise no-go.

### 2. Exact decomposition
Derive the H-representation decomposition of edge space, ker(B_+), ker(B_-).

### 3. Projection calculation
Compute F=P_-|ker(B_+) exactly, including all singular values and multiplicities.

### 4. Canonical map
Give an explicit formula for the preferred U or prove why no such U is canonical.

### 5. Complement
Identify the 1D signed-Hodge complement explicitly and its transformation properties.

### 6. Orientation naturality
Prove how U changes under reversal of one or more zone-pair orientations.
Distinguish convention dependence from physical dependence.

### 7. Source/coupling map
Give exact formulas for the forward gravity->Hodge map and, if possible, the adjoint matter->gravity projection.

### 8. Theorem-ready statements
At least 5 exact finite-dimensional statements suitable for Lean.
List all hypotheses.

### 9. Negative controls
At least:
- equal outer sizes a=c, where the 2/11 overlap mechanism should degenerate/vanish;
- a bipartite complete graph, where signed/unsigned switching behaves differently;
- a cyclic zone orientation, to test which statements are orientation-dependent.

### 10. Minimal implementation artifact
Tell the integration agent exactly what finite matrices/projectors/theorems to implement first.

## Forbidden shortcuts

- Do not identify B_+ and B_- by "choosing orientation"; non-bipartiteness forbids a global sign-switch equivalence.
- Do not use dimension equality as an isomorphism proof.
- Do not call an H-equivariant map canonical unless you state the extra structure that fixes its sectorwise scalars.
- Do not use empirical data or phenomenology.
- Do not spend output on GitHub/Lean syntax.
- Do not search for a different theory; solve this finite classification problem.

## Success criterion

A successful memo lets the integration agent implement one of:

A. a canonical injective 326-dimensional gravity -> Hodge carrier map with an explicit 1D matter-only complement; or

B. a theorem that only the 296-dimensional double-centered carrier is canonical, plus a precise obstruction to extending it.

Either result materially advances D0-HODGE-LINKS-001.
