# Research Brief A-X — does the A1 compensator-completed a2 action generate gravity dynamics or only a conserved projection?

## Role

You are the expensive research-only agent.

Do not inspect GitHub.
Do not write Lean.
Do not summarize the D0 project.
Do not search broadly.

This is a finite linear-algebra / variational question. Return exact formulas, proofs/no-go statements, spectral calculations, and theorem-ready outputs.

## Why this task exists

The A1 research pass found a genuine variational/Noether completion of the raw a2 response.

That closes the question:

"Can the a2 edge response be made row-divergence-free for structural variational reasons?"

Answer: yes, by the compensator construction C'.

But a conserved response is not yet a gravitational kinetic operator.

The immediate concern is that, on a homogeneous background, the reduced action may have a flat Hessian on all physical edge modes. If true, then A1 supplies a Bianchi/gauge mechanism but not by itself a Poisson / wave / long-range gravity dynamics.

We need a theorem, not intuition.

## Finite setup

Let G=(V,E) be a finite undirected graph.

Let

B_+ : R^E -> R^V

be the unsigned incidence / row-divergence:

(B_+ T)_v = sum_{e incident to v} T_e.

Let

J_+ = B_+^T,

so

(J_+ phi)_{ij}=phi_i+phi_j.

Let rho_v>0 and

W = diag(W_e),
W_{ij}=1/(rho_i rho_j).

The raw a2 action is

S_A2(h)=2 h^T W h.

The A1 compensator reduction gives

K = B_+ W B_+^T,

K phi = B_+ W h,

w = h - B_+^T phi,

G_phys = 4 W w.

The projected w is unique even if phi is not.

Equivalently define

P_W = I - B_+^T K^+ B_+ W,

where K^+ is any generalized/Moore-Penrose inverse giving the canonical projected solution.

Then

w=P_W h,

B_+ W P_W=0,

and

S_phys(h)=2 (P_W h)^T W (P_W h).

Because P_W is the W-orthogonal projection, one expects

S_phys(h)=2 h^T W P_W h

and

H_phys := Hess_h S_phys
        = 4 W P_W
        = 4(W - W B_+^T K^+ B_+ W).

Verify every identity and the precise inverse assumptions yourself.

## Homogeneous-background specialization

If rho_v=rho_0 for all v, then

W=c I,   c=rho_0^{-2}.

For a connected non-bipartite graph, B_+ has full row rank.

Then

P_W = P_+ := I - B_+^T(B_+B_+^T)^{-1}B_+,

the Euclidean orthogonal projector onto ker(B_+).

The expected Hessian is

H_phys = 4c P_+.

Hence its spectrum would be

0 on range(B_+^T),
4c on ker(B_+).

For K(9,11,13):

|E|=359,
rank(B_+)=33,
dim ker(B_+)=326,

so the predicted Hessian spectrum is

0^33,
(4c)^326.

This is the central object to test.

## Existing D0 weak-field target to compare against

Separately, the repository has a scalar Poisson equation on an archive phase carrier:

L_archive Phi = rho_source,

with a genuine graph/cycle Laplacian L_archive, neutral source, and solution unique modulo constants.

The repository also has a finite TT/spin-2 carrier and wave operator, but those are currently separate constructions.

Do NOT assume these are already derived from S_phys.

The question is exactly whether they can be.

## Single research question

Does the compensator-completed a2 action S_phys contain a genuine gravitational kinetic/propagation operator capable of yielding a Poisson scalar sector and nontrivial TT dispersion, or is it only a gauge-invariant local stiffness/projection?

If it is insufficient, prove the sharp no-go and identify the mathematically minimal new ingredient required.

## Task 1 — exact reduced Hessian

Derive S_phys and its first/second derivatives for arbitrary positive diagonal W.

Prove or correct:

H_phys = 4(W - W B_+^T(B_+ W B_+^T)^+ B_+ W).

Required:
- symmetry/self-adjointness under the correct pairing;
- positive semidefiniteness;
- kernel;
- rank;
- action on the physical quotient.

State separately:
- Euclidean Hessian;
- W-weighted operator if those differ by conjugation.

## Task 2 — homogeneous-rho spectrum

For W=cI prove the exact spectral statement

H_phys = 4c P_{ker B_+}.

Then prove:

- gauge eigenvalue 0 with multiplicity rank(B_+);
- physical eigenvalue 4c with multiplicity |E|-rank(B_+).

Specialize to K(9,11,13):

0^33 + (4c)^326.

This is not merely a dimension count: prove the operator equality.

## Task 3 — dynamical adequacy test

Answer rigorously:

Does an equation

H_phys h = T

for a conserved source T in ker(B_+) produce any nonlocal Green function / distance-dependent propagation?

For homogeneous W, compute the pseudoinverse on the physical space.

If

h_phys = (1/(4c)) T

up to gauge,

state/prove that the action has no internal momentum/distance dispersion on the edge physical modes.

Give a precise meaning of "no propagation" suitable for a finite theorem:
e.g. the physical Hessian has only one nonzero eigenvalue and its Green operator is scalar on the entire physical subspace.

Do not over-interpret beyond that theorem.

## Task 4 — scalar pullback test

A possible loophole is that h is not the scalar potential; perhaps a canonical map

R : scalar vertex potentials -> edge perturbations

pulls S_phys back to a nontrivial Laplacian.

Test at least the following maps.

### 4A. Unsigned endpoint map

R_+ = B_+^T.

This is pure A1 gauge.

Prove S_phys(R_+ phi)=0.

### 4B. Signed gradient

Choose an orientation and let

B_- : R^E -> R^V

be the ordinary signed incidence.

Use

R_- = B_-^T.

Compute exactly

K_scalar := R_-^T H_phys R_-
          = 4 B_- W P_W B_-^T

(with correct transpose/order).

For homogeneous W on K(9,11,13), determine its exact spectrum and compare it with the ordinary graph Laplacian

L_- = B_- B_-^T.

Questions:

1. Is K_scalar proportional to L_-?
2. Is it a polynomial/rational function of L_-?
3. Does it have the same kernel only, or genuinely the same dispersion?
4. Is it H=S9 x S11 x S13 equivariant?
5. What changes under a different uniform zone-pair orientation?

This calculation is high priority.

### 4C. Any canonical local H-equivariant scalar->edge map

Classify, if feasible, the H-equivariant maps R:R^V->R^E with block-local support.

Determine whether any such R makes

R^T H_phys R

equal/proportional to the canonical graph Laplacian without inserting empirical coefficients.

If impossible, prove a class-scoped no-go.

## Task 5 — relation to the existing Poisson owner

The existing Poisson equation lives on a separate archive phase/cycle carrier, not automatically on the 33-scene vertex carrier.

Do not equate them.

Determine what additional typed map would be required for a derivation of

L_archive Phi = rho_source

from S_phys.

Return the minimal commutative diagram of carriers/operators that would have to exist.

Mark each arrow as:
- already mathematically determined by A1;
- finite-map candidate;
- genuinely new structure.

## Task 6 — TT/wave adequacy

Do not rebuild the full TT theory.

At the finite operator level answer:

Can a Hessian with one nonzero physical eigenvalue support nontrivial mode-dependent wave frequencies without an additional kinetic/time or spatial operator?

If no, state the exact missing structure.

Distinguish:
- field-space stiffness Hessian;
- time kinetic term;
- spatial propagation operator.

The current D0 TT wave operator may still be valid as an independent downstream operator; the issue is whether A1 derives it.

## Task 7 — minimal extension if A1 is insufficient

If the flat-Hessian concern is confirmed, classify the smallest mathematically natural extension.

Candidates to compare:

1. add a gauge-invariant edge operator Q:
   S = S_phys + alpha <w,Qw>;
2. use the next heat coefficient/a4 term;
3. use a Hodge/line-graph Laplacian on the physical edge quotient;
4. make W itself geometry-dependent with derivative couplings;
5. pull back through a separately forced scalar/metric map.

Requirements for an admissible extension:

- invariant under h -> h+B_+^T xi;
- response remains B_+-conserved;
- H-equivariant on K(9,11,13);
- no fitted coefficient needed to create the operator shape;
- has at least two distinct nonzero physical eigenvalues / genuine dispersion;
- admits a scalar sector whose operator can be compared to a Laplacian.

Do not select a candidate just because it gives the desired answer. State which additional principle would force it.

## Task 8 — K(9,11,13) exact representation analysis

Use H=S9 x S11 x S13.

Decompose the physical 326-dimensional ker(B_+) into its H-isotypic sectors:

K0
+ A9
+ A11
+ A13

with dimensions

296 + 8 + 10 + 12.

For H_phys at homogeneous rho, verify it is scalar on all four sectors.

Then determine what is the most general H-equivariant self-adjoint operator on ker(B_+).

Because these sectors are inequivalent/multiplicity-free after restriction to ker(B_+), expect one scalar per irreducible sector.

This gives a finite classification of the minimum spectral freedom a future physical operator could have.

Check the decomposition and statement carefully.

## Required outputs

Return exactly these sections.

### 1. Verdict
Choose one:
- A1 already contains nontrivial gravity dynamics;
- A1 is a conserved/stiffness mechanism only;
- intermediate result with a precise condition.

### 2. Exact Hessian
General W and homogeneous W.

### 3. K(9,11,13) spectrum
Full multiplicities and H-sector action.

### 4. Source response / Green operator
Exact finite formula.

### 5. Scalar pullback
Especially R_-=B_-^T and comparison with the graph Laplacian.

### 6. TT/wave implication
Exact statement of what A1 does/does not derive.

### 7. Minimal admissible extension
Rank candidates by mathematical naturality, not desired physics.

### 8. Theorem-ready statements
At least 6 exact propositions suitable for Lean.

### 9. Negative controls
At least:
- pure gauge R_+ gives zero action;
- replace P_W by identity to show conservation is load-bearing;
- a hand-chosen Q that yields dispersion but violates gauge invariance;
- an H-breaking edge operator.

### 10. Next integration artifact
Tell the worker exactly which finite matrices/theorems to implement next.

## Forbidden shortcuts

- Do not call conservation "Einstein dynamics".
- Do not identify the 33-scene vertex space with the archive phase carrier.
- Do not assume the existing Poisson theorem is derived from A1.
- Do not import a continuum Laplacian by hand.
- Do not fit an operator spectrum.
- Do not use phenomenology.
- Do not spend output on GitHub/Lean syntax.

## Success criterion

A successful memo decides whether A1 closes only the Bianchi/variational gate or also supplies the beginning of the kinetic Einstein gate.

A sharp no-go is a successful result if it tells us exactly which new operator/principle must be added.
