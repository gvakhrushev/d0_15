# EXP-A4D-Q0-STATIONARY-SHEET-STRESS

Class: EXPENSIVE  
State on registration: PLANNED  
Parent: CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE

Repository: gvakhrushev/d0_15  
Base: main  
Branch: exp/a4d-q0-stationary-sheet-stress  
Primary artifact: 02_REGISTRY/research/MEMO_A4D_Q0_STATIONARY_SHEET_STRESS.md  
Execution: GitHub-first

## Why delegated

The exact moving-kernel identity controls the connection equation under a
joint change of character and metric amplitude. It does not determine the
metric Euler response along a fixed-metric or prescribed metric path.
Determining whether a connection-stationary sheet continues along that path,
and whether its response agrees with the designated smooth sheet, is a
genuinely uncertain variational question. CONTROL should not turn the
identity into an assumed zero-stress result.

## Runtime and dependency gate

Before starting, use current main, confirm this task is still PLANNED, and
search open PRs for this exact task ID. Pin #216 and #270 owner SHAs and the
current status/head of PR #240. The submitted stationary-sheet synthesis in
PR #240 is open research, not a merged theorem; do not use it as accepted
evidence. If the task needs its source/comparator convention, wait until that
convention is accepted into main or obtain an explicit CONTROL dependency
decision before using it.

The starting calculation is the nontrivial-character section
$d_r(z)=z_r^{-1}-1$, $q_0(z)=d(z)d(z)^T$, on the full Laurent torus, not a
nine-orbit table. At $z=1$ the selected generator vanishes, so no rank-one
kernel claim is permitted there.

## Objective

Let $Q_{\rm sm}$ and its designated smooth connection comparison be the
accepted #216 realization. For a character $z$ and its physical Fourier
carrier, form the real metric path

$$
Q_\epsilon(x)=Q_{\rm sm}(x)+\epsilon\bigl(q_0(z)\chi_z(x)
 +\overline{q_0(z)\chi_z(x)}\bigr),
$$

using the #262 real conjugate-pair and Parseval convention. State the range
of $\epsilon$ for which the chosen Gram path remains nondegenerate. Keep the
prescribed source fixed throughout.

Compute the metric Euler response on this path in two typed senses:

1. the partial metric derivative of the owned action, with the connection
   held fixed as required by the definition of $E_Q$;
2. if it exists, the response evaluated on a differentiable
   connection-stationary continuation through the designated comparison
   sheet.

For the second case, either construct the continuation and compute the exact
response difference against the designated smooth sheet, or exhibit the
first exact obstruction to continuation. Derive both Euler slots from the
same action when a reduced action is used. State the first nonzero coefficient
in $\epsilon$ and a remainder bound in the chosen finite setting.

## Terminal and stopping rule

Return an exact stress formula or exact vanishing result for the declared
path and sheet, with the connection/source convention and normalization
fully stated. If the stationary continuation is not established, report the
precise obstruction and do not label an off-shell discrepancy as a
joint-critical counterexample. This task cannot close the global
#240 response question by itself.

## Scope fences

- Do not infer $E_Q=0$ from $C(z)q_0(z)=0$.
- Do not identify $q_0(z)$ with a smooth sitewise metric field; it is a
  Fourier amplitude paired with its conjugate.
- Do not retune the prescribed source after observing a candidate response.
- Do not repeat the nine-orbit FUGU census, rank-sum 11, floating SVD, or the
  already recorded $q_{11}$ shear component.
- Do not claim a physical NOGO unless both finite Euler equations, the fixed
  source, and the genuine Lorentz quotient are satisfied.
- No action changes, Lean-owner edits, claim promotion, or BOOK edits.

## GitHub execution contract

Start from current main; run
python3 tools/task_lifecycle.py start EXP-A4D-Q0-STATIONARY-SHEET-STRESS as
the first task-branch change; open a Draft PR before research edits; write
the memo and any exact certificate in that PR; run repository guards; refresh
against current main; retire the task before marking that same PR
Lifecycle: REVIEW. Never self-merge.

## Chat handoff

Return the execution PR, the declared real metric path and source convention,
whether the stationary sheet continues, the exact response result or first
obstruction, validation results, and the smallest remaining blocker.
