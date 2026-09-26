# EXP-A4D-STAR-TRANSLATION-ONSHELL-CONSTRAINT-SYMMETRY

Class: \`EXPENSIVE\`
State on registration: \`IN_PROGRESS\`
Parent: \`CTRL-A4D-FULL-AFFINE-SOLDER-GAUGE-QUOTIENT\`

Repository: \`gvakhrushev/d0_15\`
Base: \`main\`
Branch: \`exp/a4d-star-translation-onshell-constraint-symmetry\`
Primary artifact: \`02_REGISTRY/research/MEMO_A4D_STAR_TRANSLATION_ONSHELL_CONSTRAINT_SYMMETRY.md\`
Execution: \`GitHub-first\`

## Why this is EXPENSIVE

The preceding finite calculations leave a genuine theorem/no-go question.
The accepted star density is not known to possess a nonlinear affine
translation gauge symmetry, and the nonlinear solder translation law is not
selected beyond the flat chart.  It is unknown whether the existing Euler
constraints nevertheless generate a nontrivial on-shell translation identity
in a natural local class.

## Question

Classify whether the accepted finite star density has a **nontrivial on-shell
affine-translation / constraint symmetry** before enlarging the action.

The class under study must be narrow enough that a positive result is physical
information rather than the vacuous construction
\`delta z = M(z) EL(z)\`.

## Mandatory ansatz discipline

A candidate infinitesimal translation lift associated with a node vector field
\`xi_x\` must:

1. be linear in \`xi\`;
2. be Lorentz-covariant;
3. be local to a bounded cell/one-ring path expression already available from
   the owned link/solder/curvature data;
4. reduce at the flat identity background to the owned
   \`forwardGaugeCoframe\` tangent:
   \[
   \delta_\xi e = d_f\xi,\qquad \delta_\xi L=0;
   \]
5. permit a curvature-dependent \(\delta_\xi L\) away from flatness;
6. not depend on the Euler covector/Hessian itself;
7. preserve the independent affine-shift/solder distinction;
8. not add a new action term.

## KILL-FIRST gates

### TYPE
Write the tangent types for
\[
(\delta_\xi\Theta_x,\delta_\xi L_{x,r})
\]
and the source/target fibres of every candidate term.

### REPRESENTATION
Classify the lowest-locality Lorentz-equivariant maps from
\((\xi,e,L,R)\) into solder and connection tangents with the required flat
limit.  Identify any unavoidable moduli.

### SYMMETRY / NOETHER
For each surviving class, test whether
\[
dS_\star[V_\xi]
\]
is:
- identically zero off shell;
- a local linear combination of the existing Euler constraints;
- zero only on the full critical locus;
- or generically nonzero even at configurations satisfying the connection
  constraint.

### EXACT FINITE CONTROLS
At minimum use exact rational L=2 controls and, where aliasing could hide the
result, an L=3 control.  Include genuinely curved noncommuting Lorentz links.

### HOSTILE CONTROLS
- the PR #178 curved pure-translation witness;
- the PR #175 fact that connection EL is not the naive forward torsion;
- flat exact gauge tangent;
- nondegenerate solder;
- constant and nonconstant \`xi\`;
- curvature-zero but nonparallel solder;
- pure independent affine shift;
- reject any ansatz that changes the action only because it secretly uses
  Euler data.

## Desired terminal forms

Positive:
\[
\texttt{STAR-TRANSLATION-ONSHELL-CONSTRAINT-SYMMETRY-CONSTRUCTED}
\]
with an exact finite Noether identity.

Negative:
\[
\texttt{STAR-TRANSLATION-ONSHELL-SYMMETRY-NOGO-IN-CLASS}
\]
with the class and rank/witness stated exactly.

A negative result should say whether it forces a new translation-invariant
action completion, or only a broader gauge-law search.

## Scope

Research only.  No Lean source edits, no claims/release promotion, no
BOOK/public edits.  Do not identify the result with diffeomorphisms, Einstein
gravity, torsion-free geometry, waves or physical time.

## Lifecycle

Open Draft before substantive research.  Before Ready, self-retire this
EXPENSIVE task from the manifest/status and remove this executable brief, while
retaining the durable research memo/certificates.

## Handoff

PR number, terminal verdict, exact certificate result, and one remaining
blocker/fork.  Do not self-merge.
