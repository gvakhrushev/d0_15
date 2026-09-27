# WRK-A4D-SCHUR-EINSTEIN-DIRECT-LEAN
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-schur-einstein-direct-lean`
Primary artifact: `03_FORMALIZATION/D0/Gravity/A4DSchurEinsteinDirectIdentification.lean`
Execution: `GitHub-first`

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
State on registration: `PLANNED`
Affected claims: `D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001`

## Why delegated

Merged #273 independently constructs two 10-by-10 polynomial symbols and
checks 100 exact entry identities, plus Bianchi and convention controls.
Translating the independent tensor construction and symmetric-coordinate
normalization into Lean is a substantial formal proof. Existing modules with
"Einstein" in their names describe different operators and do not own this
direct Schur comparison.

## Dependency gate

Use merged PR #273 at its current `main` owner
`02_REGISTRY/research/A4D_SCHUR_EINSTEIN_DIRECT_IDENTIFICATION.md` and exact
certificate `02_REGISTRY/research/certificates/a4d_schur_einstein_direct_identification_check.py`.
Do not import the target equality as an axiom or route through `E_eta`.

## Objective

In the repository's ten symmetric metric coordinates, independently define:

- the finite Schur symbol `K_Schur(k) = -C₁(k)ᵀ A₀⁻¹ C₁(k)` using the
  accepted regular block `det A₀ = 256`;
- the standard flat linearized Einstein tensor from the index formula in
  #273, with Minkowski signature `diag(1,-1,-1,-1)`, raised output indices,
  and factor 2 on off-diagonal symmetric Euler coordinates.

Prove coefficientwise over the four momentum variables that

`K_Schur(k) = -(1/2) K_G1(k)`

for every one of the 100 matrix entries, and prove the four polynomial Bianchi
identities `k_μ G⁽¹⁾^{μν} = 0`. Include exact negative controls showing the
identity fails under each nearby convention: lowered output indices, omitted
off-diagonal factor 2, and reversed Schur sign. Keep these controls exact and
small; they must identify a concrete nonzero coefficient.

## Required checks

- Compile with `python3 tools/lean_task_build.py narrow D0.Gravity.A4DSchurEinsteinDirectIdentification`.
- Reproduce the direct tensor formula and coordinate convention from #273; do
  not define the Einstein symbol by simplifying the Schur symbol.
- Do not edit `D0/All.lean` or `D0/TheoremLedger/ClaimMap.lean`; the three
  formalization branches have disjoint source files, and CONTROL will integrate
  accepted modules together after their individual reviews.
- Run the repository's required final Lean and guard checks before REVIEW; no
  new `sorry`, axioms, or unreviewed assumptions.

## Scope guard

This is an exact flat linear-symbol identity. Do not claim nonlinear Einstein
dynamics, a continuum limit, finite exact diffeomorphism gauge symmetry,
graviton propagation, or the curved #232 response. Do not add a generic rank or
kernel theorem beyond this task's stated target. Do not modify BOOK text,
claims, or release statuses.

## Exit condition

The standalone module proves all 100 direct Schur/Einstein coefficient
identities, the four Bianchi identities, and the three exact negative
convention controls, with no unproved assumptions and the scope boundary
above preserved.

## GitHub execution contract

Start from current `main`; run
`python3 tools/task_lifecycle.py start WRK-A4D-SCHUR-EINSTEIN-DIRECT-LEAN` as
the first task-branch change; open a Draft PR before editing Lean; write the
module at the named artifact; validate it; retire the task in that same PR
before marking Ready with `Lifecycle: REVIEW`. Never self-merge.

## Chat handoff

Return the worker PR, theorem names, the 100-entry/Bianchi results, narrow/full
validation, and any exact convention blocker. Do not paste the proof into
chat.
