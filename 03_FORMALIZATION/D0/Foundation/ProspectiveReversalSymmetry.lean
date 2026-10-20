import D0.Foundation.ProspectiveExecution

/-! Native #334 extension extracted without changing the accepted base owner.
Original declarations: `03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean` at
`07f2f2b15b7050a612d0075aa73db8dc46087a95`.
The shared definitions are imported from their maintained main modules. -/

namespace D0.Foundation.EndogenousActionQuantum

open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.PopperianBootstrap

/-- An actual prospective selection task with a genuine reversal
symmetry of ALL its admissible histories and FULL physical cost.
The symmetry assumptions are explicit obligations for a concrete
M1/G0 application; a scalar Book reversal alone does not establish
symmetry of the whole original Book03 H+J+R and CAR source. -/
structure ProspectiveReversalSymmetry where
  Candidate : Type
  feasible : Candidate → Prop
  fullPrice : Candidate → ℝ
  reverse : Candidate → Candidate
  reverse_reverse : ∀ x, reverse (reverse x) = x
  reverse_feasible : ∀ x, feasible x → feasible (reverse x)
  price_reversal : ∀ x, fullPrice (reverse x) = fullPrice x
  signedSource : Candidate → ℝ
  signed_reversal : ∀ x, signedSource (reverse x) = -signedSource x

/-- Prospective physical optimum among all ACTUALLY admissible
source histories at identical complete initial/boundary/test task. -/
def ProspectiveReversalSymmetry.IsMinimum
    (S : ProspectiveReversalSymmetry) (x : S.Candidate) : Prop :=
  S.feasible x ∧ ∀ y, S.feasible y → S.fullPrice x ≤ S.fullPrice y

/-- If ALL full-task and full-price reversal hypotheses hold,
a minimum has an equally good actual reversed minimum. -/
theorem ProspectiveReversalSymmetry.reverse_minimum
    (S : ProspectiveReversalSymmetry) {x : S.Candidate}
    (hx : S.IsMinimum x) :
    S.IsMinimum (S.reverse x) := by
  constructor
  · exact S.reverse_feasible x hx.1
  · intro y hy
    rw [S.price_reversal]
    exact hx.2 y hy

/-- At a reversal-fixed genuinely admissible physical history,
every honest orientation-ODD source is necessarily zero. -/
theorem ProspectiveReversalSymmetry.fixed_point_signed_zero
    (S : ProspectiveReversalSymmetry) {x : S.Candidate}
    (h : S.reverse x = x) : S.signedSource x = 0 := by
  have hh := S.signed_reversal x
  rw [h] at hh
  linarith

/-- If prospective D_min really determines a UNIQUE history from
fully symmetric constraints and full price, its signed chirality is
zero. Unique oriented nonzero gravity needs a physical symmetry
breaker in the actual initial data/required tests/paid native source,
not an arbitrary external choice. -/
theorem ProspectiveReversalSymmetry.unique_minimum_signed_zero
    (S : ProspectiveReversalSymmetry) {x : S.Candidate}
    (hx : S.IsMinimum x)
    (hunique : ∀ y, S.IsMinimum y → y = x) :
    S.signedSource x = 0 := by
  have heq := hunique (S.reverse x) (S.reverse_minimum hx)
  exact S.fixed_point_signed_zero heq

/-- Conversely a nonzero oriented optimum NECESSARILY has a distinct
equally-priced reversed optimum under complete symmetry. This is
deterministic non-uniqueness, not a stochastic physical law. -/
theorem ProspectiveReversalSymmetry.nonzero_minimum_pair
    (S : ProspectiveReversalSymmetry) {x : S.Candidate}
    (hx : S.IsMinimum x) (hodd : S.signedSource x ≠ 0) :
    S.IsMinimum (S.reverse x) ∧ S.reverse x ≠ x ∧
      S.fullPrice (S.reverse x) = S.fullPrice x := by
  refine ⟨S.reverse_minimum hx, ?_, S.price_reversal x⟩
  intro hfixed
  exact hodd (S.fixed_point_signed_zero hfixed)

/-- If a criterion does not permit the reversed candidate, it is
NOT a reversal-symmetric FULL future task, even if its scalar
primitive Book edge counts and costs are symmetric. This is where
an original orientation-sensitive initial record/reference/target
may enter WITHOUT postulating a random choice or fitted gravity. -/
theorem ProspectiveReversalSymmetry.unique_nonzero_impossible
    (S : ProspectiveReversalSymmetry)
    (h : ∃ x, S.IsMinimum x ∧ S.signedSource x ≠ 0)
    (hunique : ∀ x y, S.IsMinimum x → S.IsMinimum y → x = y) :
    False := by
  obtain ⟨x, hx, hodd⟩ := h
  have heq : S.reverse x = x :=
    hunique (S.reverse x) x (S.reverse_minimum hx) hx
  exact hodd (S.fixed_point_signed_zero heq)

end D0.Foundation.EndogenousActionQuantum
