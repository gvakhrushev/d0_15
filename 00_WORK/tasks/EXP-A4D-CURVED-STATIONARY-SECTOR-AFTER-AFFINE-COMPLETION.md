# EXP-A4D-CURVED-STATIONARY-SECTOR-AFTER-AFFINE-COMPLETION

Class: `EXPENSIVE`  
Parent: `CTRL-A4D-FULL-AFFINE-SOLDER-GAUGE-QUOTIENT`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `exp/a4d-curved-stationary-sector-after-affine-completion`
Primary artifact: `02_REGISTRY/research/MEMO_A4D_CURVED_STATIONARY_SECTOR_AFTER_AFFINE_COMPLETION.md`
Execution: `GitHub-first`

## Objective

Move beyond gauge-law classification and decide whether the minimal full-affine
completed action has a genuinely curved stationary sector.

Use as hypotheses only results that are either on current `main` or are
independently reproduced here. In particular, active PRs #184/#185/#186 are
not repository truth until reproduced.

The central question is whether there exist finite configurations with

[
C \neq 0
]

such that the independent Euler equations of the completed theory vanish after
quotienting the known gauge directions.

## Required decomposition

Separate:

1. solder/relative-solder Euler equation;
2. Lorentz-connection Euler equation;
3. affine translational-holonomy residual equation;
4. gauge identities relating dependent variations.

Do not infer one from another.

## First gate: local algebraic curvature kernel

At canonical nondegenerate solder, compute the exact linear map from the six
curvature bivectors to the 16 solder-Euler components. Record rank/nullity.

Then impose algebraic curvature pair symmetry and first Bianchi in a declared
subclass. Determine whether the surviving kernel is nonzero and identify its
representation content where possible.

This gate decides whether the solder Euler equation alone forces flatness.

## Second gate: finite holonomy realizability

For any nonzero local curvature kernel element, determine whether it is
realizable by exact finite proper-Lorentz plaquette holonomies on the periodic
L=2 carrier.

Reject curvature tensors that cannot arise from links.

## Third gate: joint Euler closure

For realizable curved candidates, evaluate the exact connection Euler equation.
If the relative-solder completion alone overquotients nongauge affine edge
directions, reproduce that defect and include the lowest full-affine invariant
translation-curvature carrier capable of detecting those modes.

The preferred minimal extension to test is a two-holonomy polynomial residual,
but its covariance/detection properties must be reproduced independently if
they are not yet on `main`.

Classify the smallest family

[
S_{\rm trial}=S_{\rm rel}+\mu S_R
]

(or the actual independently derived minimal family) and determine whether
stationarity selects `mu`, leaves a modulus, or has no curved solution.

## Hostile controls

- exact L=2 witness from the affine-solder packet;
- one independently generated exact L=2 curved configuration;
- one L=3 curved configuration before any broad claim;
- flat limit;
- pure gauge translation;
- nongauge affine edge mode;
- site-dependent proper-Lorentz covariance;
- degenerate solder stabilizer control;
- exact rational arithmetic for load-bearing ranks/witnesses.

## Desired terminals

Positive:
`CURVED-STATIONARY-SECTOR-SURVIVES-MINIMAL-FULL-AFFINE-COMPLETION`.

Negative scoped:
`CURVED-STATIONARY-SECTOR-NOGO-IN-DECLARED-MINIMAL-COMPLETION-CLASS`.

Intermediate structural:
`SOLDER-EULER-DOES-NOT-FORCE-FLATNESS-CONNECTION-COMPATIBILITY-IS-FIRST-BLOCKER`.

Do not state a universal flatness theorem from finite test sets.

## Scope

Research only. No Lean source edits, no claims/release promotion, no BOOK/public
edits. No Einstein equations, GR equivalence, spacetime diffeomorphism, time,
wave, or continuum interpretation.

## Lifecycle

Open Draft before durable research artifacts. Before Ready, self-retire the
EXPENSIVE task, preserve memo/certificates, refresh collision fence, and run
repository guards.

## Handoff

Report the strongest stable theorem, exact ranks/witnesses, whether curvature
survives both Euler equations, and the smallest remaining blocker. Do not
self-merge.
