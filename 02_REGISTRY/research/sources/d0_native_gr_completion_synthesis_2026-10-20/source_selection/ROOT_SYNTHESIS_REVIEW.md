# Independent bounded review of the root synthesis

20 October 2026. Reviewed read-only:

- `/Users/grigorijvahrusev/.codex/worktrees/book-source-universality/d0_15/02_REGISTRY/research/A4D_GOLDEN_FULL_SOURCE_SELECTION_SYNTHESIS_2026_10_20.md`
- `/Users/grigorijvahrusev/.codex/worktrees/book-source-universality/d0_15/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/RESIDUAL_AND_AVERAGING.md`

Also inspected the cited same-representative residual equation (16), the
Schur-completion theorem's assumptions, compiler tick corollary, and stopped
Golden source equation (8). This was a bounded review, not fresh research.

## Actionable corrections

1. **Signed numerical difference.** The synthesis table currently calls
   `+3.51455e-11` the difference of the full residual and leading formula.
   The cited original values give, by independent Decimal arithmetic:

       2.842442552963308e-5 - 2.8424460675141278e-5
          = -3.5145508198e-11.

   Change the wording to the **absolute difference**, or retain the negative
   sign. The intended rejection of an error below 1e-12 is correct.

2. **Residual operator type.** `RESIDUAL_AND_AVERAGING.md`, line 15:
   replace "R is a Hermitian effect" with "R is a Hermitian operator".
   A signed Cost-minus-Info residual need not be positive or bounded by I,
   whereas "effect" has that conventional operator meaning. The subsequent
   moving-split calculation correctly allows an indefinite R.

No other correctness defect was found in the requested review scope.

## Checks and boundaries

- The fixed linear-idempotent averaging statement is exact:
  `Mr=c` has solutions iff `Mc=c`, and its full linear-domain solution set is
  `c+ker M`. The document correctly refrains from treating arbitrary kernel
  elements as physically admitted prices.
- The moving-law differential includes both `E[dr]` and the score-covariance
  term. Its `(1,-1)` and `(1/2+y,1/2-y)` countercontrol gives derivative 2.
- Moving decomposition of G preserves the full source only with all
  `da`, `db`, and `b dE_mark` terms. These are present and correct.
- The table does not claim that all seven proposals are false. It separates
  under-specified comparisons, conditional mathematical interfaces and
  actual counterexamples.
- The HJR statement is backed by a common stationary root, actual internal
  quotient and invertible Schur block in its linked proof. The three-negative-
  directions theorem concerns the additional Hessian, not negative costs,
  probabilities, or three new fields.
- The positive bit-continuation theorem retains the same task, one-tick
  compiler premise and all continuation source terms. Five or six ticks are
  a conditional search criterion, not an asserted foundational obligation.
- The stopped-programme paragraph identifies a different supplied task,
  fixes the k-family, retains repeated paid preparation and source-sign
  reversal, and leaves compulsory task admission and full valuation open.
  Its displayed coefficient agrees with the owner's equation (8).
- The Fisher/Beatty statements retain their fixed-law scopes and do not
  prohibit arbitrary auxiliary clocks or couplings.
- The C1 theorem is correctly stated for derivatives of expected readouts
  on fixed K913; it is not confused with samplewise derivatives or h-refinement.
- The final physical boundary is sound: programme selection at fixed fields
  does not establish stationarity, stability, continuum normalization or
  selection of the full Book action.

The algebraic checker `check_residual_transport.py` was inspected. An
independent replay using the bundled Python failed immediately because that
runtime lacks sympy; no successful independent Sympy run is claimed here.
The numerical difference above was independently recomputed successfully
with Python's standard-library Decimal, and the other requested equalities
were checked algebraically from their displayed formulas.

**Receipt status:** mathematically acceptable in the reviewed scope after
the two explicit wording/sign corrections above. No repository edits made
by this reviewer.


## Final integration review at the all-cost extension

The same reviewer read the updated Russian synthesis and the final general
adaptive proof after incorporation of45372df3. No material mathematical or
status defect was found. The finite active-action reduction, uniform complete
entropy envelope, directional first jet at ties and true local-minimum
implication are consistent. The synthesis correctly consumes Golden Kraft
normalization and algebraic norm separation, the two-native-8D first-source
construction, and the explicit Info-algebra dependence. It retains the
T>=5,ell>=1 source domain and leaves compulsory physical task/Info open.

At the first filesystem pass the newly linked adaptive proof had not yet
been copied. Integration has now copied the final reviewed bytes to
`records/ADAPTIVE_ALL_COST_EXTENSION.md`; its exact hash and independent
mathematical review are in `records/ADAPTIVE_ALL_COST_REVIEW.md`.
