import Mathlib.Tactic
import D0.Representation.OrientationNontrivialGrading
import D0.Extensions.RepresentationReadoutExtension
import D0.Matter.CanonicalZoneCirculation
import D0.Foundation.ObservableCompletionCanonicity

/-!
# D0.Synthesis.RepresentationAndCirculationCanonicity

Theoretical owner: `D0-REPRESENTATION-AND-CIRCULATION-CANONICITY-001`.

Foundational synthesis linking the new representation / grading and matter circulation
results to the canonical `ObservableCompletionCanonicity` framework:

1. **Orientation Nontrivial Grading Canonicity**:
   - Any 3-dimensional generation grading satisfying `BothSignsPresent` has signatures
     in `{(2,1), (1,2)}`.
   - The observable `readout := fun (p, q) => ncCount p q` evaluates to `8` on ALL
     such completions.
   - By `constant_readout_m1_forced`, the neutral-current count `8` is `M1Forced`
     WITHOUT variational MDL / commutant-minimization!

2. **Canonical Zone Circulation Direction Canonicity**:
   - For any nonzero divergence-free zone-homogeneous flow $J$ on $K(9,11,13)$,
     all three components are nonzero and proportional to $(13, 9, 11)$.
   - The normalized orientation ray / projectivized circulation line is uniquely forced.
-/

namespace D0.Synthesis.RepresentationAndCirculationCanonicity

open D0.Representation.OrientationNontrivialGrading
open D0.Extensions.RepresentationReadoutExtension
open D0.Matter.CanonicalZoneCirculation
open D0.Foundation.ObservableCompletionCanonicity
open D0.Foundation

/-- Admissible 3-generation grading completion: non-negative integer pair `(p, q)`
summing to 3 with both signs present. -/
def AdmissibleGradingSignature (sig : ℕ × ℕ) : Prop :=
  sig.1 + sig.2 = 3 ∧ BothSignsPresent sig.1 sig.2

/-- Observable readout map: neutral-current channel count. -/
def ncReadout (sig : ℕ × ℕ) : ℕ :=
  ncCount sig.1 sig.2

/-- Concrete witness: `(2, 1)` is admissible. -/
theorem admissible_grading_21 : AdmissibleGradingSignature (2, 1) := by
  refine ⟨rfl, ⟨by norm_num, by norm_num⟩⟩

/-- All admissible grading completions produce identical readout `8`. -/
theorem all_admissible_gradings_give_eight (sig : ℕ × ℕ) (hs : AdmissibleGradingSignature sig) :
    ncReadout sig = 8 := by
  rcases hs with ⟨hsum, hboth⟩
  unfold ncReadout
  exact nontrivial_signature_nc sig.1 sig.2 hsum hboth

/-- **Theorem: Neutral-current count 8 is M1-forced by orientation nontriviality.**
This upgrades the previous commutant-minimization selection to exact proof-theoretic
canonicity under `ObservableCompletionCanonicity`. -/
theorem nc_count_eight_m1_forced :
    M1Forced
      (CompletionForcesReadout AdmissibleGradingSignature ncReadout)
      8 := by
  have h_const : ∀ sig, AdmissibleGradingSignature sig → ncReadout sig = ncReadout (2, 1) := by
    intro sig hsig
    rw [all_admissible_gradings_give_eight sig hsig]
    rw [all_admissible_gradings_give_eight (2, 1) admissible_grading_21]
  have h_forced := constant_readout_m1_forced
    AdmissibleGradingSignature ncReadout (2, 1) admissible_grading_21 h_const
  have h_val : ncReadout (2, 1) = 8 := all_admissible_gradings_give_eight (2, 1) admissible_grading_21
  rw [h_val] at h_forced
  exact h_forced

/-- Admissible circulation ray: ratio of $x$ to $y$ component for any nonzero divergence-free current. -/
def circulationRatio (J : ZoneFlow) : ℚ :=
  J.x / J.y

/-- For every nonzero divergence-free zone-homogeneous current, the circulation ratio
$J_x / J_y$ is invariant and identically equals $13 / 9$. -/
theorem circulation_ratio_invariant
    (J : ZoneFlow) (hJ : DivergenceFree J) (hnz : J.x ≠ 0 ∨ J.y ≠ 0 ∨ J.z ≠ 0) :
    circulationRatio J = 13 / 9 := by
  obtain ⟨t, hx, hy, hz⟩ := divergenceFree_classification J hJ
  have ht_nonzero : t ≠ 0 := by
    intro ht0
    subst t
    simp at hx hy hz
    rcases hnz with h | h | h
    · exact h hx
    · exact h hy
    · exact h hz
  unfold circulationRatio
  rw [hx, hy]
  have h9t : (9 : ℚ) * t ≠ 0 := mul_ne_zero (by norm_num) ht_nonzero
  calc (13 * t) / (9 * t) = (13 / 9 : ℚ) * (t / t) := by ring
  _ = (13 / 9 : ℚ) * 1 := by rw [div_self ht_nonzero]
  _ = 13 / 9 := mul_one _

/-- Summary owner connecting representation and matter circulation to the canonicity framework. -/
theorem representation_circulation_canonicity_owner :
    M1Forced (CompletionForcesReadout AdmissibleGradingSignature ncReadout) 8 ∧
    (∀ J : ZoneFlow, DivergenceFree J → (J.x ≠ 0 ∨ J.y ≠ 0 ∨ J.z ≠ 0) →
      circulationRatio J = 13 / 9) :=
  ⟨nc_count_eight_m1_forced, circulation_ratio_invariant⟩

end D0.Synthesis.RepresentationAndCirculationCanonicity
