import D0.Geometry.OriginalBookEffectWords
import Mathlib.Tactic

/-!
# Eliminating the Golden square root inside actual source effects

Pinned original sources: uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
lines 94–100, and modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 174–182 and 217–222 at commit eebcb5e467742df3e9cf7fa9702042d7294aa742.

For an odd source port, the actual K is sqrt(p) times the stated reduced
operator; its Heisenberg update is p times the reduced update. This applies
also to the anchor row and to every finite chronological path. The reduced
operators are a proof device for these effects: no claim identifies them with
the actual Kraus operators or permits replacing coherent inter-port amplitudes.
No coefficient-ring embedding, modular-rank transfer or effect independence is
assumed or asserted.
-/

open Matrix
open scoped BigOperators
open D0.Geometry.OriginalBookJuliaWords
open D0.Geometry.OriginalBookGoldenKraus
open D0.Geometry.ChronologicalEffect
open D0.Geometry.OriginalBookEffectWords

namespace D0.Geometry.OriginalBookEffectRadicalReduction

/-- For each actual slot: even ports retain K; odd ports remove the real sqrt(p). -/
noncomputable def reducedKraus (slot : Fin 128) : Operator :=
  if krausPort slot = 0 then
    (if krausRow slot = 0 then 1 else 0) - (2 * goldenP ^ 2) • sourceV (krausRow slot)
  else (-(2 * goldenP) : ℝ) • sourceV (krausRow slot)

/-- The missing positive weight for an odd Heisenberg update. -/
noncomputable def portWeight (slot : Fin 128) : ℝ :=
  if krausPort slot = 0 then 1 else goldenP

lemma portWeight_pos (slot : Fin 128) : 0 < portWeight slot := by
  unfold portWeight
  split_ifs
  · norm_num
  · exact goldenP_pos

/-- An odd actual source Kraus slot has precisely the removed positive factor. -/
private lemma oddPort_factor (slot : Fin 128) (h : krausPort slot ≠ 0) :
    sourceKraus slot = Real.sqrt goldenP • reducedKraus slot := by
  simp only [reducedKraus, h, if_false, sourceKraus, sourceGoldenPair]
  have hc : -(2 * goldenP * Real.sqrt goldenP) =
      Real.sqrt goldenP * (-(2 * goldenP)) := by ring
  rw [hc, smul_smul]

/-- The exact source update equals a weighted reduced update for every X. -/
theorem source_update_reduced (slot : Fin 128) (X : Operator) :
    (sourceKraus slot)ᴴ * X * sourceKraus slot =
      portWeight slot • ((reducedKraus slot)ᴴ * X * reducedKraus slot) := by
  by_cases h : krausPort slot = 0
  · simp [reducedKraus, portWeight, sourceKraus, sourceGoldenPair, h]
  · rw [oddPort_factor slot h]
    simp only [Matrix.conjTranspose_smul, star_trivial, Matrix.smul_mul, Matrix.mul_smul,
      smul_smul, portWeight, h, if_false]
    rw [← pow_two, goldenRoot_sq]

/-- Product of the actual per-port factors in chronological order. -/
noncomputable def pathWeight (path : List (Fin 128)) : ℝ :=
  (path.map portWeight).prod

/-- All path factors are strictly positive, including words containing zero K. -/
theorem pathWeight_pos (path : List (Fin 128)) : 0 < pathWeight path := by
  induction path with
  | nil => simp [pathWeight]
  | cons slot tail ih =>
    simpa [pathWeight] using mul_pos (portWeight_pos slot) ih

/-- Exact chronological source effect with sqrt(p) removed from every odd update. -/
theorem sourceEffect_eq_weighted_reduced (path : List (Fin 128)) :
    sourceEffect path = pathWeight path • effect reducedKraus path := by
  induction path with
  | nil => simp [sourceEffect, effect, pathWeight]
  | cons slot tail ih =>
    calc
      sourceEffect (slot :: tail) = pathWeight tail •
          ((sourceKraus slot)ᴴ * effect reducedKraus tail * sourceKraus slot) := by
        rw [sourceEffect_cons, ih]
        simp
      _ = pathWeight tail • (portWeight slot •
          ((reducedKraus slot)ᴴ * effect reducedKraus tail * reducedKraus slot)) := by
        rw [source_update_reduced]
      _ = pathWeight (slot :: tail) • effect reducedKraus (slot :: tail) := by
        simp [pathWeight, effect, update, smul_smul, mul_comm]

/-- The original odd anchor port obeys the same reduction for arbitrary input. -/
theorem anchor_odd_update_reduced (X : Operator) :
    (sourceKraus (krausIndex 0 1))ᴴ * X * sourceKraus (krausIndex 0 1) =
      goldenP • ((reducedKraus (krausIndex 0 1))ᴴ * X * reducedKraus (krausIndex 0 1)) := by
  have hport : krausPort (krausIndex 0 1) = 1 := (krausIndex_coordinates 0 1).2
  simpa [portWeight, hport] using source_update_reduced (krausIndex 0 1) X

/-- Positive real word weights are nonzero complex scalars. -/
noncomputable def pathWeightUnit (path : List (Fin 128)) : ℂˣ :=
  Units.mk0 (pathWeight path : ℂ) (by exact_mod_cast (ne_of_gt (pathWeight_pos path)))

/-- Exactly the same indexed effects are independent before and after reduction. -/
theorem sourceEffects_linearIndependent_iff {ι : Type*} (paths : ι → List (Fin 128)) :
    LinearIndependent ℂ (fun i => sourceEffect (paths i)) ↔
      LinearIndependent ℂ (fun i => effect reducedKraus (paths i)) := by
  have heq : (fun i => sourceEffect (paths i)) =
      (fun i => pathWeightUnit (paths i)) • (fun i => effect reducedKraus (paths i)) := by
    funext i
    rw [sourceEffect_eq_weighted_reduced]
    ext a b
    simp [pathWeightUnit, Complex.real_smul]
  rw [heq]
  exact LinearIndependent.units_smul_iff _ _
end D0.Geometry.OriginalBookEffectRadicalReduction
