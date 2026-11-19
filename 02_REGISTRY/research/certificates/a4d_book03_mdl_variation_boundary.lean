import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Tactic

/-!
# Minimum description length does not determine a variational derivative

This is a scoped counterexample to the implication in Book 03 §03.3.0a that
"most probable = shortest code = `δS = 0`" is a tautology. It formalizes only
the mathematical boundary: finite action samples do not determine a smooth
first jet, and a constrained minimizer at the boundary need not be stationary
in the ambient derivative. It does not refute the separate finite stationarity
equation in §03.8 or assert a countermodel to the entire D0 core.
-/

namespace A4D.Book03MDLVariationBoundary

/-- A polynomial completion of two sampled action values with a prescribed
ambient derivative at the left sample. -/
def twoSampleCompletion (a b d x : ℝ) : ℝ :=
  a + (b - a) * x + (b - a - d) * x * (x - 1)

theorem twoSampleCompletion_at_zero (a b d : ℝ) :
    twoSampleCompletion a b d 0 = a := by
  simp [twoSampleCompletion]

theorem twoSampleCompletion_at_one (a b d : ℝ) :
    twoSampleCompletion a b d 1 = b := by
  simp [twoSampleCompletion]

theorem twoSampleCompletion_hasDerivAt (a b d : ℝ) :
    HasDerivAt (twoSampleCompletion a b d) d 0 := by
  unfold twoSampleCompletion
  convert ((hasDerivAt_const 0 a).add
    (((hasDerivAt_const 0 (b - a)).mul (hasDerivAt_id 0)).add
      (((hasDerivAt_const 0 (b - a - d)).mul
        ((hasDerivAt_id 0).mul ((hasDerivAt_id 0).sub_const 1)))))) using 1
  · ext x
    dsimp
    ring
  · norm_num

/-- The same two values at 0 and 1 admit every real first derivative at 0. -/
theorem every_first_jet_extends_two_samples (a b d : ℝ) :
    ∃ f : ℝ → ℝ, f 0 = a ∧ f 1 = b ∧ HasDerivAt f d 0 := by
  exact ⟨twoSampleCompletion a b d,
    twoSampleCompletion_at_zero a b d,
    twoSampleCompletion_at_one a b d,
    twoSampleCompletion_hasDerivAt a b d⟩

def linearCost (x : ℝ) : ℝ := x

def quadraticCost (x : ℝ) : ℝ := x ^ 2

theorem costs_agree_on_two_samples :
    linearCost 0 = quadraticCost 0 ∧ linearCost 1 = quadraticCost 1 := by
  constructor <;> simp [linearCost, quadraticCost]

/-- Both smooth completions have the same constrained minimum on [0,1]. -/
theorem linearCost_min_on_unit_interval :
    ∀ x ∈ Set.Icc (0 : ℝ) 1, linearCost 0 ≤ linearCost x := by
  intro x hx
  simpa [linearCost] using hx.1

theorem quadraticCost_min_on_unit_interval :
    ∀ x ∈ Set.Icc (0 : ℝ) 1, quadraticCost 0 ≤ quadraticCost x := by
  intro x hx
  simp [quadraticCost]
  positivity

theorem linearCost_unique_min_on_unit_interval :
    ∀ x ∈ Set.Icc (0 : ℝ) 1, linearCost x = linearCost 0 → x = 0 := by
  intro x hx h
  simpa [linearCost] using h

theorem quadraticCost_unique_min_on_unit_interval :
    ∀ x ∈ Set.Icc (0 : ℝ) 1, quadraticCost x = quadraticCost 0 → x = 0 := by
  intro x hx h
  simp [quadraticCost] at h
  nlinarith

theorem linearCost_deriv_at_zero : deriv linearCost 0 = 1 := by
  change deriv id (0 : ℝ) = 1
  exact deriv_id (0 : ℝ)

theorem quadraticCost_deriv_at_zero : deriv quadraticCost 0 = 0 := by
  change deriv (fun x : ℝ => x ^ 2) 0 = 0
  rw [deriv_pow_field]
  norm_num

/-- A minimizer of the same finite sampled costs can be stationary or
nonstationary depending on the smooth completion. -/
theorem same_samples_same_minimum_different_stationarity :
    (linearCost 0 = quadraticCost 0 ∧ linearCost 1 = quadraticCost 1) ∧
      (∀ x ∈ Set.Icc (0 : ℝ) 1, linearCost 0 ≤ linearCost x) ∧
      (∀ x ∈ Set.Icc (0 : ℝ) 1, quadraticCost 0 ≤ quadraticCost x) ∧
      (∀ x ∈ Set.Icc (0 : ℝ) 1, linearCost x = linearCost 0 → x = 0) ∧
      (∀ x ∈ Set.Icc (0 : ℝ) 1, quadraticCost x = quadraticCost 0 → x = 0) ∧
      deriv linearCost 0 = 1 ∧ deriv quadraticCost 0 = 0 := by
  exact ⟨costs_agree_on_two_samples,
    linearCost_min_on_unit_interval,
    quadraticCost_min_on_unit_interval,
    linearCost_unique_min_on_unit_interval,
    quadraticCost_unique_min_on_unit_interval,
    linearCost_deriv_at_zero,
    quadraticCost_deriv_at_zero⟩

end A4D.Book03MDLVariationBoundary
