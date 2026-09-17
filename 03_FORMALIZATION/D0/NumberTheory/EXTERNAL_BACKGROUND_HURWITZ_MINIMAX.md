# EXTERNAL_BACKGROUND_HURWITZ_MINIMAX

## Exact Theorem Missing

This file records external mathematical background, not an active D0-core
dependency.  Local D0 dimensions 1/2/4/8 are closed in
`D0.Algebra.D0InternalDimensionSelector`; the external upstream theorem is the
global classification statement:

```lean
def globalHurwitzLagrangeClassificationStatement : Prop :=
  forall n : Nat,
    GlobalHurwitzDivisionDimension n -> d0AdmissibleInternalDimension n
```

Equivalently, every global normed-division/Hurwitz-Lagrange dimension must be
one of the four locally witnessed dimensions:

```lean
theorem global_hurwitz_lagrange_classification :
  forall n : Nat,
    GlobalHurwitzDivisionDimension n ->
      n = 1 \/ n = 2 \/ n = 4 \/ n = 8
```

## Mathlib Modules Searched

- `Mathlib.Algebra.ContinuedFractions.*`
- `Mathlib.Algebra.ContinuedFractions.Computation.*`
- `Mathlib.NumberTheory.DiophantineApproximation.Basic`
- `Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions`
- `Mathlib.Analysis.SpecificLimits.Fibonacci`

The available API covers continued-fraction computations and approximation
infrastructure, but not a ready global Hurwitz/Lagrange classification theorem
that can discharge the exact D0 statement above.

## Dependencies Needed

- an upstream predicate/API for global normed-division/Hurwitz-Lagrange
  dimensions;
- a classification theorem proving that only 1, 2, 4, and 8 satisfy that
  global predicate;
- a compatibility lemma connecting the upstream predicate to
  `GlobalHurwitzDivisionDimension`.

## Already Proved In Lean

Module: `D0.NumberTheory.HurwitzMinimaxPhi`

- `alphaD0_eq_phi_inv_sq`
- `alphaD0_eq_two_sub_phi`
- `unique_D0_phase_generator`
- `unique_D0_phase_generator_is_phi_inv_sq`
- `alphaD0_cf_head`
- `alphaD0_cf_second`
- `alphaD0_cf_tail_ones`
- `alphaD0_convergents_numerators_fibonacci`
- `alphaD0_convergents_denominators_fibonacci`
- `periodOneTail_fixed_point`
- `periodOnePhase_one_eq_alphaD0`
- `periodOneBadApproxConstant_max_at_one`
- `alphaD0_is_extremal_among_period_one_contfrac`
- `HURWITZ_MINIMAX_D0_CLASS_PROVED`

Module: `D0.Algebra.HurwitzLocalBoundary`

- `dim_one_admissible`
- `dim_two_admissible`
- `dim_four_admissible`
- `dim_eight_admissible`
- `dim_one_has_local_finite_witness`
- `dim_two_has_local_finite_witness`
- `dim_four_has_local_finite_witness`
- `dim_eight_has_local_finite_witness`
- `hurwitz_local_boundary_split`
- `remaining_hurwitz_open_is_single_precise_statement`

## What Remains

The D0-relevant local dimensions and finite witnesses are proved internally.
They are not promoted to the global classification theorem; the global theorem
is no longer an active D0 core dependency.
