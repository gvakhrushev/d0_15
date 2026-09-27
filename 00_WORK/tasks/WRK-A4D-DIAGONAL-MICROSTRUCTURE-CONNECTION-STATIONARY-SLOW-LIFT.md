# WRK-A4D-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-SLOW-LIFT

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-diagonal-microstructure-connection-stationary-slow-lift`  
Primary artifact: `02_REGISTRY/research/A4D_DIAGONAL_MICROSTRUCTURE_CONNECTION_STATIONARY_SLOW_LIFT.md`  
Execution: `GitHub-first`

## Why delegated

Merged #241 found an exact pointwise slow-background metric-response term
(Delta E_{Q,01}=-sigma(p)hz/(4+3z^2)) for the curved nongauge #232 microstructure,
with a nonzero normalized limit at (z_h=h).  That result deliberately did not impose
the connection Euler equation on the perturbed background.  Before the EXPENSIVE
response-decoupling lane can use the coefficient as evidence for or against a genuine
joint-critical counterexample, a bounded exact finite calculation must determine whether
the #232 microstructure admits a nearby connection-stationary lift over the same slow
background and what that lift does to the (hz) response coefficient.

## Inputs and conventions

Consume merged #232 and merged #241 as owners.  Use #226 only for the single final
(h^{-2}) normalization/sensitivity interpretation and #216/#223 only for the declared
smooth-comparison context.  Pin the launch-time merge SHAs.  Preserve the #241 slow
profiles, phase convention, Gram lift, pointwise-versus-average distinction, and the
actual finite naked-star Euler maps.  Do not replace (E_K) by a continuum torsion-free
equation.

## Objective

For the valued slow background from #241,

[
Q_h=eta+halpha+h^2x_0eta,
]

and the exact #232 period-four family (K(z)), seek a corrected connection in a stated
local chart,

[
K_h^{m corr}=K(z),exp!ig(delta A(h,z)ig)
]

(or an exactly equivalent Cayley-coordinate ansatz), with the correction allowed to use
the minimal phase/role Fourier support demanded by the Euler equations.  Expand the full
finite connection Euler map (E_K(Q_h,K_h^{m corr})) jointly in (h,z).

The load-bearing question is the first order at which #241's pointwise metric response
can matter after (z_h=h): determine whether the connection equation can be solved
through every monomial capable of changing the (h z) and (h^2) normalized response.
If solvable, substitute the solved correction into the finite metric partial and compute
the corrected leading (Delta E_Q) coefficient exactly.  If not solvable, identify the
first exact cokernel obstruction.

Also repeat the order accounting for (z_h=h^2), where #241's uncorrected normalized
response vanished, to check whether the connection correction itself can generate an
(O(h^2)) metric term.

## Required gates

1. Reproduce the #232 flat control (E_K(eta,K(z))=0) and the merged #241 uncorrected
   (hz) metric-response coefficient before adding correction variables.
2. Use the full finite connection Euler equations on the declared slow background.  State
   the correction carrier, phase/role support, gauge convention, and all quotient choices.
3. At each relevant bidegree ((m,n)), compute the exact linearized correction operator,
   its rank/cokernel, and the inhomogeneous slow-background forcing.  No numerical least
   squares or floating rank may decide solvability.
4. Continue only as far as necessary to decide every correction that can alter the
   pointwise normalized response at (z_h=h) or (z_h=h^2).
5. If a correction exists, recompute the metric partial after substitution and separate
   pointwise phase values from the four-phase average.
6. Distinguish connection stationarity from the metric/source equation.  A successful
   (E_K=0) lift is not yet an exact same-source joint solution and must not be described
   as one.
7. Check that any surviving response term is nongauge in the owned #232 sense; do not
   quotient it away merely because its phase average vanishes.

## Terminals

Use

`J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-OBSTRUCTION-PERSISTS`

only if an exact local (E_K=0) lift exists through the response-relevant orders and the
corrected pointwise (h^{-2}Delta E_Q) retains a certified nonzero finite/divergent term
for (z_h=h) or (z_h=h^2).

Use

`J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-CANCELS`

only if the required exact (E_K=0) correction exists and cancels all pointwise
response terms through (o(h^2)) for the declared tested scalings.

Use

`J2-DIAGONAL-MICROSTRUCTURE-SLOW-BACKGROUND-CONNECTION-LIFT-BLOCKED`

only with an exact finite-rank/cokernel obstruction proving that no correction in the
declared complete local carrier can solve (E_K=0) at the first obstructed bidegree.

Otherwise remain Draft/BLOCKED and name the single missing carrier/completeness or
higher-order identity.  Do not convert a partial ansatz failure into a no-go.

## Scope fences

No new action density, Holst term, torsion constraint, spectral filter, boundary
selector, or connection-selection principle.  No claim/release promotion, BOOK edits,
Lean-owner edits, #202 edits, or child-task creation.  Do not impose the metric source
equation in this worker; its output is a finite connection-stationary input to EXP #240
and, if needed, a later same-source joint-critical task.

## GitHub execution contract

Start from fresh current `main`; run
`python tools/task_lifecycle.py start WRK-A4D-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-SLOW-LIFT` as the first task-branch change;
open a Draft PR before adding the memo/certificate; keep all exact derivations in that
PR; refresh against current `main`; run repository guards; retire the task in the same
PR before Ready; set `Lifecycle: REVIEW`; never self-merge.

## Chat handoff

Return the execution PR number/head, the exact terminal or blocker, the first relevant
(E_K) forcing/cokernel bidegree, the corrected pointwise metric-response coefficient
for (z_h=h) and (z_h=h^2), the phase-average comparison, and validation commands.
Do not paste the full derivation into chat.
