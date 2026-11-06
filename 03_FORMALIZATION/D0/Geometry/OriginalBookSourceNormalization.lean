import D0.Geometry.OriginalBookGoldenCompleteness
import D0.Geometry.OriginalBookEffectWords
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# Consequences of the exact source Kraus completeness

The source word effect starts at I and follows the reverse Heisenberg loop
in pinned modular checker d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 217–222, at commit eebcb5e467742df3e9cf7fa9702042d7294aa742.
This proves mathematical trace preservation and normalization of each finite
chronological continuation from the actual completeness theorem. It does not
assert a physical preparation, admission, span, rank, or GR closure.
-/
open Matrix
open scoped BigOperators
open D0.Geometry.OriginalBookJuliaWords
open D0.Geometry.OriginalBookGoldenKraus
open D0.Geometry.OriginalBookGoldenCompleteness
open D0.Geometry.ChronologicalEffect
open D0.Geometry.OriginalBookEffectWords

namespace D0.Geometry.OriginalBookSourceNormalization

/-- For any complete finite Kraus family, adding all next outcomes preserves the effect. -/
theorem effect_extension {ι n : Type*} [Fintype ι] [Fintype n] [DecidableEq n]
    (K : ι → Matrix n n ℂ) (hK : (∑ j, (K j)ᴴ * K j) = 1) (path : List ι) :
    (∑ j, effect K (path ++ [j])) = effect K path := by
  induction path with
  | nil => simpa [effect, update] using hK
  | cons first tail ih =>
    simp only [List.cons_append, effect, update]
    rw [← Finset.sum_mul, ← Finset.mul_sum, ih]

/-- The actual source effect is the sum of its 128 one-step extensions. -/
theorem sourceEffect_extension (path : List (Fin 128)) :
    (∑ slot, sourceEffect (path ++ [slot])) = sourceEffect path := by
  simpa [sourceEffect] using effect_extension sourceKraus sourceKraus_complete path

/-- The exact finite forward source map preserves trace for every complex matrix. -/
theorem source_forward_trace (rho : Operator) :
    Matrix.trace (∑ slot : Fin 128, sourceKraus slot * rho * (sourceKraus slot)ᴴ) = Matrix.trace rho := by
  calc
    _ = ∑ slot : Fin 128, Matrix.trace (sourceKraus slot * rho * (sourceKraus slot)ᴴ) := by
      rw [Matrix.trace_sum]
    _ = ∑ slot : Fin 128, Matrix.trace ((sourceKraus slot)ᴴ * sourceKraus slot * rho) := by
      apply Finset.sum_congr rfl
      intro slot _
      rw [Matrix.trace_mul_comm, Matrix.mul_assoc]
    _ = Matrix.trace ((∑ slot : Fin 128, (sourceKraus slot)ᴴ * sourceKraus slot) * rho) := by
      rw [Finset.sum_mul, Matrix.trace_sum]
    _ = Matrix.trace rho := by rw [sourceKraus_complete, Matrix.one_mul]

end D0.Geometry.OriginalBookSourceNormalization
