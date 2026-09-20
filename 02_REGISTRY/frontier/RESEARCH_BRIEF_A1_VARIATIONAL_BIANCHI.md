# Research Brief A1 — Natural Variational/Bianchi Mechanism for the D0 a2 Response

## Role

You are the expensive research-only agent. Do not inspect or update GitHub. Do not write Lean.
Do not spend tokens summarizing the D0 repository. Work only on the mathematical problem below and
return a compact technical memo with formulas, proofs/counterexamples, and theorem-ready statements.

## Given data

Work on an arbitrary finite undirected graph with symmetric edge variables h_ij=h_ji, h_ii=0 and positive
vertex weights rho_i>0. The frozen D0 scene K(9,11,13) is only a final specialization.

Define

S_A2(h,rho) = 2 * sum_{i<j} h_ij^2 / (rho_i rho_j).

For fixed rho, the raw edge gradient is

G_A2^{ij} = dS_A2/dh_ij = 4 h_ij/(rho_i rho_j),  i != j,
G_A2^{ii}=0.

Let

M_ij = h_ij/(rho_i rho_j),
d_i(M) = sum_j M_ij,
D_M = diag(d_i(M)),
L_M = D_M - M.

Known exact identities / constraints:

1. Raw divergence (row-sum convention):
   (Div G_A2)_i = 4 d_i(M), hence G_A2 is not conserved on any nontrivial positive scene.

2. Conserved Laplacian response:
   Div(2 L_M)=0.

3. Completion identity:
   G_A2 = 4 D_M - 4 L_M = 4 D_M - 2*(2 L_M)
   under the repository matrix convention.

4. On the frozen K(9,11,13), no divergence-free tensor can approach raw G_A2 in the previously demanded
   max-norm flat-decoupling sense; the old “small counterterm tending to zero” route is therefore closed.

5. There is an exact measure-coupling identity in the current audit:
   weighted-divergence(edge response) is tied to -2 rho_i * dS_A2/drho_i.
   Treat this as a hint, not as a desired conclusion.

6. A naive local-tick gauge route is unavailable: current D0 discrimination finds only global homogeneous
   tick rescaling gauge; inhomogeneous local tick profiles change an observable local ratio.

## Single research question

Find the most natural non-circular variational principle in which the physical Euler response associated
with S_A2 (or the minimally necessary corrected action) is divergence-free for structural reasons, OR
prove that no such mechanism exists within the candidate classes below.

The output must decide among mechanisms, not merely list possibilities.

## Candidate classes to analyze

### Route A — constrained edge/metric variation

Seek a constraint manifold C(h,rho)=0 defined independently of “Div G = 0”, for example fixed or
covarying weighted vertex measure/degree.

Derive the tangent space T_(h,rho) C and the restricted Euler covector.

Required question:
Does the restricted gradient have a canonical representative equal/proportional to L_M or to another
divergence-free tensor?

If yes, prove the universal property

< G_raw - G_phys, delta h > = 0

for every admissible delta h, and state exactly what inner product/pairing is used.

If not, give a minimal counterexample.

### Route B — measure covariation

Treat rho as a dependent or independent field rather than frozen data.

Analyze at least the scale-covariant family of local transformations

h_ij -> exp((xi_i+xi_j)/2) h_ij,
rho_i -> exp(xi_i) rho_i,

for which each monomial h_ij^2/(rho_i rho_j) is invariant.

Derive the exact Noether identity.

Then answer:

- Does the full Euler system E_h=0, E_rho=0 have nontrivial positive solutions for S_A2 alone?
- If E_rho=0 is impossible except for the trivial graph, prove it.
- What is the minimal additional constraint/volume term, if any, that makes the measure equation
  nontrivial while preserving the symmetry?
- Does eliminating rho then produce a divergence-free metric response?

Do not choose rho_i=sqrt(sum_j h_ij) merely because it cancels a term. If a relation rho(h) is proposed,
derive or characterize it by an independent principle.

### Route C — discrete Noether/Bianchi structure

Let a vertex gauge generator K map xi_i to an edge/measure variation.
Compute K* exactly under the chosen pairing.

Determine whether K* is:
- ordinary row-sum divergence,
- h-weighted divergence,
- a Hodge codifferential,
- or a different operator.

Prove the strongest correct implication

gauge invariance of S -> K*(Euler response)=0.

Then state clearly whether this is the conservation law needed by the D0 field equation or only a
weighted/extended conservation law involving the rho equation.

## Required outputs

Return exactly these sections.

### 1. Verdict
One page maximum:
- preferred mechanism, or
- precise no-go if all three routes fail.

### 2. Definitions
All configuration spaces, constraints, pairings, gauge actions and divergence operators used.

### 3. Main derivation
Step-by-step algebra, valid for arbitrary finite graphs whenever possible.

### 4. Theorem-ready statements
At least 3 exact statements suitable for Lean formalization.
Each must list hypotheses and conclusion with no physics prose inside the proposition.

### 5. K(9,11,13) specialization
Give explicit formulas for zone degrees 24,22,20 and show what the proposed mechanism yields there.

### 6. Negative controls
At least two:
- one graph/variation where a tempting but wrong mechanism fails;
- one check distinguishing genuine Noether conservation from “define the response to be a Laplacian”.

### 7. Minimal next artifact
If positive: exact formula for G_phys and the smallest proof package needed.
If negative: exact theorem ruling out the candidate class and the next mathematically distinct route.

## Forbidden shortcuts

- Do not call 2L the variational derivative of S_A2 unless derived under an explicit restricted principle.
- Do not impose Div G=0 as a definition of admissibility.
- Do not import continuum Einstein equations as an axiom.
- Do not use local tick reparametrization as gauge unless you construct a different observable quotient
  that makes it genuinely redundant.
- Do not fit coefficients to K(9,11,13); first derive on arbitrary finite graphs.
- Do not spend output on literature review, project history, code, GitHub, Lean syntax or phenomenology.

## Success criterion

A successful memo lets the integration agent implement one of two things without further conceptual search:

A. a canonical constrained/Noether variational theorem producing a divergence-free finite response; or
B. a sharp no-go theorem eliminating this entire mechanism class and forcing the project to a new carrier/action.
