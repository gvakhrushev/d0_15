# Independent review of the exact weight-binding substitution

20 October 2026. Reviewer: metric_source_synthesis. Read-only review for
existing PR #334 at source head `2c592f9b9437cd302fcd39352b85212341bff968`.

**Result: ACCEPT within the stated carrier and supplied-task scope.**

## Frozen inputs

* `EXACT_DOOB_BINDING_CRITERION.md`, SHA-256
  `f4faa541795b02be1478da158fb1d52bc38cbf91e008bf912cc532771f016225`.
* `FOUNDATIONAL_WEIGHT_BRIDGES.md`, SHA-256
  `b8ff0a2f47cb582fb607f66b97e0048fa2cdbfd392ad153d9d46630ee0cf000f`.

Both inputs are in `/private/tmp/d0_puzzle_weight_20261020/` at review.
Hashes were checked after the final changes.

## Mathematical checks

1. The signs in the finite suffix defect are correct:
   `D_e=S_e+log_phi(q_e)-log_phi(h(t_e))` is constant exactly when
   `q_e=K_e h(t_e)/h(s)`; its constant is `-log_phi(h(s))`.
   The original two-step counts give `11*22+13*20=502` and the
   single-neighbour ratio `22/20=11/10`; discarding the suffix fails
   the same finite identity.

2. On the actual positive, irreducible original 718-edge carrier,
   `Omega=c+V_u-V_v` and row normalization imply
   `K phi^V=phi^c phi^V`, hence the positive Perron pair and `q=P`.
   The converse is immediate. The consumed original 2/3-cycle
   reconstruction and source-annihilator theorem have the appropriate
   constant-plus-coboundary type. No new cycle rank or archive rank is
   needed. The notes correctly use K's Perron preparation for `G_Omega`.

3. The constructive Poisson test is exact. If the cochain is a constant
   plus a potential difference, its P-row average is
   `a=c*1+(I-P)V`; applying `Z` to the centred average recovers the
   centred potential. Conversely zero edge residual explicitly supplies
   that potential. The balanced-flow KL identity follows by telescoping
   the Perron potential, with the displayed nonnegative sign.

4. The final absolute-scale caveat is necessary and correct:
   `K -> a(y)K` preserves P, the zero-residual test and the KL gap,
   while shifting `-d log_phi lambda` by `-d log_phi a`.
   Normalized branch observations therefore cannot fix the absolute
   price source. The note keeps the actual cost/complete clock anchor.

5. The companion's response-defect odds identity includes both the
   suffix partition and the actual quadratic response. Its corrected
   all-input operator criterion is precisely `F_e=B_e H` with common
   `H=(sum F)/(sum B)`; a complete instrument makes
   `H=I/(sum B)`. A general normalized response does not itself force
   scalar effects. The formerly missing qualification is now explicit.

6. Weighted primitive intertwining implies each finite continuation
   identity by induction. Moving relabellings require their derivative;
   variable clock reductions retain boundary and direct terms. The Gram
   response distinguishes coefficients w from amplitudes sqrt(w).
   Neither unweighted future equivalence nor Born normalization removes
   this distinction. The source convention with
   `mu_ref,uv=phi^(-C_uv)` has the stated endpoint, clock and pressure
   signs, and its stationary mean yields conditional entropy.

## Scope retained

The 718-edge scalar ensemble is not silently identified with the Julia
reporter or its Golden conditional law. The proposed next test requires
the same actual instrument, complete preparation and archive, terminal
contract and weighted compiler. Passing a pointwise normalized-law test
does not prove an all-field source identity. The consistency KL is used
as a diagnostic, not installed as physical Info or a stabilizing action.
Neither note supplies a compulsory task or derives Einstein equations.

Validation was independent algebraic reading and comparison with the
consumed original PF/source-annihilator and native branch-cocycle owners.
No new numerical rank calculation, checker or repository edit was made.
