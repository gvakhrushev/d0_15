# WRK-A4D-METRIC-NULL-COMPLEX-LEAN
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-metric-null-complex-lean`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DMetricNullHessianComplex.lean`
Execution: `GitHub-first`

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
State on registration: `PLANNED`
Affected claims: `D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001`

## Why delegated

Merged #270 has an exact 24-by-10 metric-response symbol and a pointwise
rank/kernel theorem supported by four projective chart covers. Porting those
matrix definitions, unit-ideal witnesses, and kernel arguments into Lean is a
substantial proof with a distinct review surface. CONTROL should not compress
that proof into a registry edit or infer the all-character result from a
generic rank calculation.

## Dependency gate

Use merged #270 at `7103412403e672ce7416bbfcc63028988f543494` for the exact
symbol and four projective chart covers. Use merged #292 at
`99ee2010239f9c63af073610db06d962bddc42a3` and
`02_REGISTRY/research/A4D_HAQ_COEFFICIENTWISE_IDENTITY.md` for the explicit
linear coefficient matrices `C_r` and the coefficientwise null identity.
The #292 ledger supplies the polynomial matrix entries; the #270 chart minors
still supply the pointwise rank/kernel proof.

## Objective

Create the exact polynomial map

`C(d) : Sym²(ℂ⁴) → ℂ²⁴`, `d = (d₀,d₁,d₂,d₃)`,

using the owner's `SYM = [(a,b) | 0 ≤ a ≤ b < 4]` coordinate order and
`vec_sym(ddᵀ)_(a,b) = d_a d_b` (no off-diagonal `sqrt(2)` factor). Prove:

1. `C(d) vec_sym(ddᵀ) = 0` for every `d`;
2. for every `d ≠ 0`, the rank is exactly 9 and the kernel is exactly the
   one-dimensional span of `vec_sym(ddᵀ)`;
3. the universal statement follows from the four normalized charts `d_j = 1`
   and the explicit 9-by-9 minor covers in #270, including a Lean-checkable
   certificate that the minors on each chart generate the unit ideal;
4. at `d = 0`, `C(0) = 0` and the fiber map `φ ↦ φ vec_sym(ddᵀ)` is zero, so
   the middle fiber homology has dimension 10.

The nonzero-`d` theorem must cover complex values, including points on
coordinate divisors `d_r = 0`; do not state that those divisors are rank-drop
strata. The origin is a special fiber. Do not infer nonzero global module
homology from its fiber dimension.

## Required checks

- Compile this module with `python3 tools/lean_task_build.py narrow D0.Geometry.A4DMetricNullHessianComplex`.
- Use the exact chart minors and no-common-zero witnesses from #270; a generic
  field-rank argument alone does not establish pointwise exactness.
- Keep the 24-by-10 matrix and coordinate convention independently auditable.
- Do not edit `D0/All.lean` or `D0/TheoremLedger/ClaimMap.lean`; the three
  formalization branches have disjoint source files, and CONTROL will integrate
  accepted modules together after their individual reviews.
- Run the repository's required final Lean and guard checks before REVIEW; no
  new `sorry`, axioms, or unreviewed assumptions.

## Scope guard

This is the finite polarized symbol complex only. Do not claim a nonlinear
diffeomorphism symmetry, physical Hodge law, stress cancellation, IR germ at
`z = (1,1,1,1)`, continuum equation, or global exactness of polynomial modules.
Do not modify BOOK text, claims, release statuses, or the HAQ coefficientwise
worker.

## Exit condition

The module compiles and proves the null identity, rank-9/kernel-line theorem
for every nonzero complex `d` from the four explicit chart covers, and the
origin fiber statement, with no unproved assumptions and the scope boundary
above preserved.

## GitHub execution contract

Start from current `main`; run
`python3 tools/task_lifecycle.py start WRK-A4D-METRIC-NULL-COMPLEX-LEAN` as the
first task-branch change; open a Draft PR before editing Lean; write the module
at the named artifact; validate it; retire the task in that same PR before
marking Ready with `Lifecycle: REVIEW`. Never self-merge.

## Chat handoff

Return the worker PR, the exact theorem names and narrow/full validation
results, and any precise chart or field blocker. Do not paste the proof into
chat.
