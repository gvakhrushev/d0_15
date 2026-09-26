# EXP-A4D-JOINT-HOLONOMY-QUOTIENT-COMPLETENESS

Class: `EXPENSIVE`  
State on registration: `IN_PROGRESS`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `exp/a4d-joint-holonomy-quotient-completeness`  
Primary artifact: `02_REGISTRY/research/MEMO_A4D_JOINT_HOLONOMY_QUOTIENT_COMPLETENESS.md`  
Execution: `GitHub-first`

## Why delegated

This is an independent exact finite classification problem rather than a small
CONTROL repair: it requires sector-by-sector symbolic rank calculations,
Role-orbit decomposition, hostile generic controls and scalar-channel
classification.

## Objective

Independently reproduce the polynomial joint two-holonomy affine residual and
classify whether the full residual family separates the affine edge-shift
quotient on an exact curved finite background.

The task must then decompose ordered face-pair channels under the spatial Role
stabilizer, determine which orbit channels are quotient-complete, and classify
the remaining scalar/action moduli.

## Starting point

The active translation-curvature frontier proposes the polynomial residual

[
R_{2|1}
=
det(I-P_1)t_2
-
(I-P_2)operatorname{adj}(I-P_1)t_1,
]

which transforms as a Lorentz vector under simultaneous affine conjugation.
This task does not assume the active PR result as repository truth; it must
reproduce the formula and all load-bearing consequences independently.

## KILL-FIRST gates

1. Construct an exact rational homogeneous curved `L=2` Lorentz-link
   background with all six plaquettes on the generic
   `det(I-P) != 0` stratum.
2. Build the full linear map from 256 affine edge-shift components to all
   ordered two-holonomy residuals.
3. Compare its kernel exactly with the image of the covariant node-difference
   `D_L`.
4. Repeat sector-by-sector on all 16 period-two characters.
5. Decompose ordered face pairs into spatial-Role-stabilizer orbits and rank
   every orbit separately.
6. Identify any nongauge residual null explicitly rather than only by nullity.
7. Test quadratic Lorentz and observer-positive scalar channels.
8. Preserve the accepted flat Hessian: any new polynomial residual term must
   be checked at flat holonomy.
9. Compare any exceptional momentum with already-owned checkerboard rank-drop
   sectors, without calling it a wave/time mode.
10. If more than one invariant quotient-complete scalar survives, record the
    modulus/no-selector result instead of choosing a coefficient by taste.

## Exact controls

- all six generic plaquette holonomies;
- all 16 period-two momenta;
- node gauge rank and kernel inclusion;
- six spatial Role ordered-pair orbits;
- explicit extra null witness if present;
- target-loop orientation reversal;
- flat `P=I` regression.

Use exact rational/symbolic arithmetic.

## Scope

Research only. No Lean edits, no claim/release promotion, no BOOK/public edits.
No Einstein, diffeomorphism, torsion-free, time, wave, continuum or empirical
interpretation.

## Handoff

Report the exact quotient rank, orbit-rank table, scalar-channel classification,
flat regression, and the first remaining selector/modulus. Do not self-merge.


## GitHub execution contract

Work only on `exp/a4d-joint-holonomy-quotient-completeness`.
Keep the primary memo and exact certificate durable in this PR.
Before Ready, retire this EXPENSIVE task from the manifest/status, delete this
brief, set the PR lifecycle to REVIEW and satisfy repository guards.
Do not self-merge.

## Chat handoff

Return PR #186, the terminal quotient-rank/modulus verdict, final guard status,
and the next selector blocker.
