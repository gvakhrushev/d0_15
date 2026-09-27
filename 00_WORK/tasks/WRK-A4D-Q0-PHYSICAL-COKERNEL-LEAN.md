# WRK-A4D-Q0-PHYSICAL-COKERNEL-LEAN
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-q0-physical-cokernel-lean`
Primary artifact: `03_FORMALIZATION/D0/Gravity/A4DQ0PhysicalCokernel.lean`
Execution: `GitHub-first`

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
State on registration: `PLANNED`
Affected claims: `D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001`

## Why delegated

Merged #290 owns exact conjugate-paired physical matrices, a rank-one left
cokernel on two orbit types, rational Hermitian residual norms, and a separate
same-carrier transport identity. Formalizing both sides of that distinction
as exact complex linear algebra is a substantial, reviewable proof and guards
against reading a carrier mismatch as a stationary-sheet obstruction.

## Dependency gate

Use merged PR #290 at `c29aafa887a1d9cdc7e81f109aae686e7cbaeec8`, specifically
`02_REGISTRY/research/A4D_Q0_PHYSICAL_FORCING_IMAGE.md` and its exact checker
`02_REGISTRY/research/certificates/a4d_q0_physical_forcing_image_check.py`.
PR #278 was superseded and closed; do not use its stale base as the owner.

## Objective

In exact arithmetic over `ℚ(i)` (or a definitionally equivalent exact complex
field), formalize the physical carrier matrix

`P_(ζ,χ) = [H_AA(ζ) | H_AQ(χ)]`, `χ = ζ⁻¹ = conjugate(ζ)`,

with its 24 output rows, 24 connection columns, and 10 metric columns. For the
merged #290 orbit representatives 5 and 7, prove:

1. `rank P = 23`, hence the physical left cokernel is one-dimensional;
2. the exact cross-character membership patterns are `[out,out,in,in]` on
   orbit 5 and `[out,in,in,out]` on orbit 7;
3. the exact squared Hermitian residual norms for the raw forcing are
   `[8/5,8/5,0,0]` and `[2,0,0,2]`, respectively, with unit-`q₀` values
   `[1/25,1/25,0,0]` and `[1/46,0,0,1/46]`;
4. every same-carrier moving-germ forcing is in the image, with explicit
   witness `(0, -D_j q₀(χ))` and zero cokernel class.

Use the exact orbit conventions and left-cokernel vectors from #290. Keep the
cross-character forcing `w_j(ζ)` distinct from the same-carrier forcing at
`χ`; do not merge their labels or formulas.

## Required checks

- Compile with `python3 tools/lean_task_build.py narrow D0.Gravity.A4DQ0PhysicalCokernel`.
- Derive all ranks, image tests, and norms inside Lean from exact matrices;
  no floating-point projector, SVD, or imported result proposition.
- Do not edit `D0/All.lean` or `D0/TheoremLedger/ClaimMap.lean`; the three
  formalization branches have disjoint source files, and CONTROL will integrate
  accepted modules together after their individual reviews.
- Run the repository's required final Lean and guard checks before REVIEW; no
  new `sorry`, axioms, or unreviewed assumptions.

## Scope guard

The nonzero cross-character cokernel class is a carrier-mismatch diagnostic.
The task must also retain #290's exact zero class for the actual same-carrier
moving germ. Do not infer stationary-sheet stress, failure of continuation,
nonlinear joint branches, response anomaly, or an Einstein equation. Do not
modify BOOK text, claims, or release statuses.

## Exit condition

The standalone module proves the two rank-23/one-dimensional-cokernel cases,
the stated exact membership and residual-norm tables, and the same-carrier
image witnesses, with no unproved assumptions and the scope boundary above
preserved.

## GitHub execution contract

Start from current `main`; run
`python3 tools/task_lifecycle.py start WRK-A4D-Q0-PHYSICAL-COKERNEL-LEAN` as the
first task-branch change; open a Draft PR before editing Lean; write the module
at the named artifact; validate it; retire the task in that same PR before
marking Ready with `Lifecycle: REVIEW`. Never self-merge.

## Chat handoff

Return the worker PR, exact theorem names, both orbit verdicts, narrow/full
validation, and any exact-field or matrix-rank blocker. Do not paste the proof
into chat.
