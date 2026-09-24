import Mathlib.Tactic
import Mathlib.Algebra.Module.Torsion.Field
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.A4DScalarDeltaSecondJet
import D0.Geometry.A4DSecondOrderCartanCongruence

set_option linter.unusedSimpArgs false

/-!
# Owned flat translation and the background-independent tangent obstruction

PR #70's flat affine translation changes the coframe by exactly `t d_f ξ`.
The acceleration of that orbit is zero. A background-independent additive
two-jet representation cannot have every tangent equal to `G_ξ = M_ξ D`:
the scalar matrices satisfy `[G_{δ₀}, G_{δ₁}]_{00} = -L²/4`.

This does not quantify over background-dependent groupoid actions, and it
does not identify an affine fiber translation with a site permutation.
-/

namespace D0.Geometry

open TwoJet

theorem forwardGaugeCoframe_smul (N : ℕ) (t : ℝ) (xi : LocalRoleVector N) :
    forwardGaugeCoframe N (t • xi) = t • forwardGaugeCoframe N xi := by
  funext x r a
  simp only [forwardGaugeCoframe, Pi.smul_apply]
  have h := congrFun (forwardDifference_smul N r t (fun y => xi y a)) x
  simpa [Pi.smul_apply] using h

/-- The owned flat translation is linear in the scaling parameter. -/
theorem ownedFlatTranslation_is_linear (N : ℕ) (t : ℝ) (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    (affineGauge (translationGauge N (t • xi)) (flatAffineConnection N) x r).shift a =
      t * forwardGaugeCoframe N xi x r a := by
  rw [affineTranslation_flat_eq_forwardGaugeCoframe]
  have h := congrFun (congrFun (congrFun (forwardGaugeCoframe_smul N t xi) x) r) a
  simpa [Pi.smul_apply, smul_eq_mul] using h

/-- Therefore `e(t) = t d_f ξ` and the quadratic coefficient vanishes. -/
theorem ownedFlatTranslation_acceleration_zero (N : ℕ) (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    let e : ℝ → ℝ := fun t =>
      (affineGauge (translationGauge N (t • xi)) (flatAffineConnection N) x r).shift a
    e 0 = 0 ∧ ∀ t, e t = t * e 1 := by
  refine ⟨?_, ?_⟩
  · simpa using ownedFlatTranslation_is_linear N 0 xi x r a
  · intro t
    have ht := ownedFlatTranslation_is_linear N t xi x r a
    have h1 := ownedFlatTranslation_is_linear N 1 xi x r a
    dsimp
    rw [ht, h1]
    ring

theorem additiveTwoJet_tangents_commute {ι : Type*} [Fintype ι] [DecidableEq ι]
    (J K : TwoJet ι) (h : J.mul K = K.mul J) :
    J.lin * K.lin = K.lin * J.lin := by
  have hq := congrArg TwoJet.quad h
  simp only [TwoJet.mul] at hq
  rw [add_comm K.quad J.quad] at hq
  have h2 : (2 : ℚ) • (J.lin * K.lin) = (2 : ℚ) • (K.lin * J.lin) :=
    add_left_cancel hq
  exact (smul_right_inj (by norm_num : (2 : ℚ) ≠ 0)).mp h2

theorem backgroundIndependent_deltaTangents_do_not_commute {n : ℕ} [NeZero n] (hn : 3 ≤ n) :
    (scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleG (scalarSite (1 : Fin n)) :
        Matrix (Fin n) (Fin n) ℚ) ≠
      scalarCycleG (scalarSite (1 : Fin n)) * scalarCycleG (scalarSite (0 : Fin n)) := by
  intro h
  have hentry := congr_fun (congr_fun h (0 : Fin n)) (0 : Fin n)
  have hcomm := delta_commutator_entry hn
  have hzero :
      (((scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleG (scalarSite (1 : Fin n)) -
          scalarCycleG (scalarSite (1 : Fin n)) * scalarCycleG (scalarSite (0 : Fin n))) :
          Matrix (Fin n) (Fin n) ℚ) (0 : Fin n) (0 : Fin n)) = 0 := by
    simp [Matrix.sub_apply, hentry]
  rw [hcomm] at hzero
  have hn0 : n ≠ 0 := Nat.ne_of_gt (Nat.zero_lt_of_lt (Nat.lt_of_succ_le hn))
  exact (div_ne_zero (neg_ne_zero.mpr (pow_ne_zero 2 (Nat.cast_ne_zero.mpr hn0)))
    (by norm_num)) hzero

/-- No background-independent additive two-jet representation has both delta tangents.
The hypothesis is commutativity of the truncated product, not a groupoid cocycle. -/
theorem no_backgroundIndependent_deltaTangent_representation {n : ℕ} [NeZero n] (hn : 3 ≤ n)
    (J0 J1 : TwoJet (Fin n))
    (h0 : J0.lin = scalarCycleG (scalarSite (0 : Fin n)))
    (h1 : J1.lin = scalarCycleG (scalarSite 1))
    (hcomm : J0.mul J1 = J1.mul J0) : False := by
  have hlin := additiveTwoJet_tangents_commute J0 J1 hcomm
  rw [h0, h1] at hlin
  exact backgroundIndependent_deltaTangents_do_not_commute hn hlin

end D0.Geometry
