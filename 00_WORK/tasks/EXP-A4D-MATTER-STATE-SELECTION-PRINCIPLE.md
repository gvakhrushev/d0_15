# EXP-A4D-MATTER-STATE-SELECTION-PRINCIPLE

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Classify whether current D0 contains any principle selecting a nonconstant physical CAR/Hodge matter state or density matrix once an explicit finite Dirac/Hodge operator exists.

Repository edits: **NONE**.

## Required reading

- \`02_REGISTRY/research/A4D_CAR_MATTER_STATE_ACTION_PROVENANCE.md\`
- \`02_REGISTRY/research/A4D_CAR_HODGE_METRIC_ACTION.md\`
- CAR/Dirac/parity owners;
- anomaly-free matter/species/generation owners;
- action/minimality/finite-cost owners;
- localization and source-selection no-gos.

Use the current CAR worker result if it has landed. If not, work conditionally on a generic finite self-adjoint/parity-odd Dirac operator of the exact advertised type; do not duplicate the worker.

## Distinctions

Separate rigorously:

- selecting an eigenspace;
- selecting a spectral projector;
- selecting a density matrix;
- selecting a pure ray/state;
- choosing an initial condition;
- choosing a ground/lowest-positive state;
- choosing a thermal/KMS-like state;
- anomaly-free internal species data;
- geometric 16-state exterior/Fock fibre.

Do not identify internal species with geometric Fock states by equal cardinality.

## Candidate selectors

Audit:

- zero modes;
- lowest positive spectral shell;
- parity/chirality;
- minimal action/energy;
- finite ActionProtocol;
- thermal/max-entropy state;
- archive localization;
- canonical trace state;
- evolution from a distinguished vacuum;
- anomaly cancellation;
- generation symmetry;
- any owned finite boundary/initial condition.

For each candidate determine whether it selects:

1. nothing;
2. a degenerate subspace;
3. a mixed state;
4. a unique pure state up to phase;
5. a nonconstant local excitation.

## Positive target

A provenance-bearing rule
\[
\text{owned D0 data}\mapsto \psi_N
\]
or a canonical density matrix \(\rho_N\) on the local CAR/Hodge Hilbert carrier, with a nontrivial local stress witness once the metric action exists.

## Negative target

If no owned principle selects the state, identify the narrowest new physics primitive needed and stop treating state selection as a formalization backlog.

## Terminal verdict

Return exactly one:

- \`CAR-MATTER-STATE-SELECTED\`
- \`CAR-SPECTRAL-SUBSPACE-ONLY\`
- \`CAR-CANONICAL-MIXED-STATE-ONLY\`
- \`CAR-STATE-SELECTION-NOGO-TERMINAL\`
- \`CAR-STATE-PREPARATION-PRIMITIVE-REQUIRED\`

## Deliverable

\`MEMO_40_A4D_MATTER_STATE_SELECTION_PRINCIPLE.md\`
