import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCubicalCochainCarrier
import D0.Geometry.Archive1DCochainRefinement

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveRefinementHodgeWeights

Owner: `D0-ARCHIVE-REFINEMENT-HODGE-WEIGHTS-001`.

The finite construction and counting conventions are stated in
`02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md`, §3. There the full
counting trace on degree `k` is `L^k * (L + 1)^(4-k)`, including the trace
of the identity on each occupied direction. At `L = 2` the per-sector values
are `81, 54, 36, 24, 16` and the sector-weighted total is `625`. Dividing each
degree-`k` trace by `2^k` yields the different, partially normalized values
`81, 27, 9, 3, 1` and their sector-weighted total `256`.

This module proves the corresponding scalar arithmetic only. It does not
define the four-dimensional refinement maps `B_S` or matrices `W_S`, prove
their counting-trace formulas, or derive uniqueness of a Hodge metric.
-/

/-- Prescribed partially normalized per-sector scalar formula at `L = 2`, for
the physical degree range `0 ≤ k ≤ 4`.
Its interpretation through refinement matrices is external to this module. -/
def hodgeGramTraceDegree (k : ℕ) : ℕ :=
  3 ^ (4 - k)

theorem hodge_gram_trace_0 : hodgeGramTraceDegree 0 = 81 := rfl
theorem hodge_gram_trace_1 : hodgeGramTraceDegree 1 = 27 := rfl
theorem hodge_gram_trace_2 : hodgeGramTraceDegree 2 = 9 := rfl
theorem hodge_gram_trace_3 : hodgeGramTraceDegree 3 = 3 := rfl
theorem hodge_gram_trace_4 : hodgeGramTraceDegree 4 = 1 := rfl

/-- Arithmetic sum of the partially normalized values weighted by the
prescribed sector counts. This is not the full counting Gram trace. -/
def totalHodgeGramTraceSum : ℕ :=
  1 * 81 + 4 * 27 + 6 * 9 + 4 * 3 + 1 * 1

theorem total_hodge_gram_trace_sum_eq : totalHodgeGramTraceSum = 256 := rfl

/-- Full-counting per-sector scalar formula at `L = 2`, for `0 ≤ k ≤ 4`, including the `2^k`
factor absent from the partially normalized formula. -/
def fullCountingGramTraceDegreeL2 (k : ℕ) : ℕ :=
  2 ^ k * hodgeGramTraceDegree k

/-- Arithmetic full-counting expression with the prescribed sector counts.
The trace interpretation is established in the cited research source, not by
constructing the refinement matrices in this module. -/
def fullCountingGramTraceSumL2 : ℕ :=
  1 * fullCountingGramTraceDegreeL2 0 +
  4 * fullCountingGramTraceDegreeL2 1 +
  6 * fullCountingGramTraceDegreeL2 2 +
  4 * fullCountingGramTraceDegreeL2 3 +
  1 * fullCountingGramTraceDegreeL2 4

/-- The full-counting arithmetic expression at `L = 2` is 625. -/
theorem full_counting_gram_trace_sum_l2_eq : fullCountingGramTraceSumL2 = 625 := rfl

/-- The full-counting and partially normalized arithmetic totals differ. -/
theorem full_counting_gram_trace_sum_l2_ne_partially_normalized :
    fullCountingGramTraceSumL2 ≠ totalHodgeGramTraceSum := by decide

/-- **D0-ARCHIVE-REFINEMENT-HODGE-WEIGHTS-001 (Owner, scalar scope)**:
Collects the endpoint degree values, arithmetic total, and role count. The
claimed derivation from refinement maps remains open. -/
theorem archive_refinement_hodge_weights_owner :
    (hodgeGramTraceDegree 0 = 81) ∧
    (hodgeGramTraceDegree 4 = 1) ∧
    (totalHodgeGramTraceSum = 256) ∧
    (Fintype.card Role = 4) :=
  ⟨rfl, rfl, total_hodge_gram_trace_sum_eq, card_role⟩

end D0.Geometry
