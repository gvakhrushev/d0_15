# A4D theory-closure publication checkpoint — 2026-10-06

Repository: `gvakhrushev/d0_15`
Task: `EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION`
Working PR: #317, Draft / IN_PROGRESS.
Canonical primary artifact: [A4D_RESONANCE_DIVISOR_STRATIFICATION.md](A4D_RESONANCE_DIVISOR_STRATIFICATION.md).

This is a current handoff/status addendum, not a new task or a promotion of either research lane. It updates the response-entry pointers in the older [master brief](A4D_THEORY_CLOSURE_MASTER_BRIEF.md) and [extended handoff](A4D_THEORY_CLOSURE_HANDOFF.md); their exact algebraic tables and historical calculations are retained unchanged. Read this checkpoint before using their historical response heads as current execution instructions.

## Publication provenance

The preceding execution's local commit `402abb58` and its two-file synchronization were not recoverable in the current environment. This addendum is a fresh reconstruction against published source; it does not claim those two old edits were pushed. The required PR metadata was already restored in the PR description. This source commit now produces a new synchronize event instead of reusing the old metadata-failure run as validation.

## Pinned current inputs

- Canonical main: `e80a3b1ccf615fb4f70bf5900181592604928497`.
- Unchanged algebraic input of #317: `3e5b5a873002a7dc52565b2bad343f5591384088`.
- Published response input of #310: `c55a78aa1dcd6aae0641084e20e29d2d9fb4cb3d`.
- Reconstructed, newly published amplitude corollary in #310: `1857d4a3c1a5bf7802ed1d0ce7830b1855d8734f`.

Always refresh the actual branch before writing. Reuse the existing PR and task; this file registers no child execution.

## What #317 owns and still owes

The degree-18, 671-term chiral numerator and its coefficient-conjugate partner give the exact arithmetic Laurent factorization. Irreducibility over Q(i), their nonassociation, generic arithmetic rank 23, the complex rank-23 witness, and the physical-unit-torus even-rank/Hodge identities retain their published scopes.

Absolute geometric factorization over C and the full higher-codimension rank-drop ideals, strata and ranks remain OPEN. The response progress below neither completes that algebraic terminal nor follows merely from the determinant factorization.

## Current response boundary

The [original response memo](https://github.com/gvakhrushev/d0_15/blob/c55a78aa1dcd6aae0641084e20e29d2d9fb4cb3d/02_REGISTRY/research/MEMO_A4D_JOINT_RESPONSE_DECOUPLING_MICROSTRUCTURE.md) keeps the original exact-source/raw-owner task PARTIAL / OPEN.

The [completed variational criterion](https://github.com/gvakhrushev/d0_15/blob/c55a78aa1dcd6aae0641084e20e29d2d9fb4cb3d/02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md) uses independently prepared rough endpoints with logs bounded by R h and all 24 connection Euler rows bounded by M h^2. It gives

    W_h(V) = integral (rho0[g] - sigma):V + O_V(h^(2/3)).

Its completed law holds exactly when the fixed source sigma equals rho0[g]. It is a revised observable criterion, not the exact finite equation Xi=h^2 sigma or the original unweighted raw-owner limit. Do not retire the original task under this new criterion.

The [forward conformal theorem](https://github.com/gvakhrushev/d0_15/blob/c55a78aa1dcd6aae0641084e20e29d2d9fb4cb3d/02_REGISTRY/research/A4D_CONFORMAL_FORWARD_SOURCE_BRIDGE.md) starts from the same retained exact connection-stationary root. For logs bounded by r_h>=h with r_h^3/h^2 tending to zero, it forces g:(tau-rho0[g])=0 for a fixed exact smooth sampled source, with tested error O(r_h^2/h^(4/3)). Its nine traceless channels and the original fixed-amplitude chart are not closed by that theorem.

The [published amplitude corollary](https://github.com/gvakhrushev/d0_15/blob/1857d4a3c1a5bf7802ed1d0ce7830b1855d8734f/02_REGISTRY/research/A4D_FIXED_SOURCE_AMPLITUDE_ESCAPE.md) combines that implication with the literal finite-action arithmetic obstruction. On the specified cosine warp, every fixed smooth source has no refining exact joint-root sequence with logs o(h^(2/3)); any remaining root in the original chart must obey a source-dependent lower bound c_tau h^(2/3) for sufficiently small h. Sources with the Einstein trace are excluded on every allowed mesh even with arbitrary trace-free additions. This is a necessary-amplitude/existence obstruction, not a constructed separated-gap counterexample or a sharp-threshold claim.

The native archive record/operator construction remains distinct from identification of the physical Role/state/action gate. The corrected finite Y normal-jet input is retained as a finite input only. The additional 96-variable Y-horizontal rank checker reported in the preceding chat was not recovered or replayed and is not promoted by this checkpoint.

## Next live decisions

For the original response task, retain one fixed smooth source and one fixed smooth background, selected before links and meshes, and the original comparator and norm. Either prove the required implication on the realizable source image, or construct an exact refining sourced sequence in the original small chart with the required separated gap. A mesh-dependent source sequence, an empty source fiber, a finite off-shell residue or a different variational criterion is not that terminal.

For #317, continue its own absolute-factor/higher-codimension obligations only where needed; do not restart old Y/quarter-wave scans or duplicate #310. The full-affine curved-stationary task #202 stays on its separate carrier.

## Validation

This commit adds only this status/handoff document. No algebraic certificate, expected ledger, Lean owner, action, admission rule or task lifecycle changes. Existing algebraic certificates are not claimed to have been rerun locally during this publication. Current-head remote CI must be checked on the new source head; old successful or failed runs are not evidence for it.
