import D0.Geometry.A4DStarFiniteLorentzQuotient
import D0.Gravity.A2CompensatorNoether

/-! Research capsule. A null Gram pencil and the actual compensator's
unique auxiliary-stationary value. No physical volume readout is assumed
to be derived from these finite identities.
-/

open scoped BigOperators
open D0 D0.Geometry

namespace D0.Research.NativeVolumeFiber

noncomputable section

theorem null_gram_pencil (P : Matrix Role Role ℝ)
    (hP : P.transpose = P) (hnull : P * roleLorentzMetric * P = 0)
    (w s : ℝ) :
    (w • roleLorentzMetric + (s * w / 2) • P) * roleLorentzMetric *
      (w • roleLorentzMetric + (s * w / 2) • P).transpose =
      w^2 • roleLorentzMetric + (s * w^2) • P := by
  rw [Matrix.transpose_add, Matrix.transpose_smul, Matrix.transpose_smul,
    roleLorentzMetric_transpose, hP]
  simp only [Matrix.add_mul, Matrix.mul_add, Matrix.smul_mul, Matrix.mul_smul,
    roleLorentzMetric_sq, Matrix.one_mul]
  rw [Matrix.mul_assoc P roleLorentzMetric roleLorentzMetric,
    roleLorentzMetric_sq, Matrix.mul_one, hnull]
  ext i j
  simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul,
    Matrix.zero_apply, mul_zero, add_zero]
  ring

def nullPencilCoframe (N : ℕ) (w : ArchiveRolePhaseGroup N → ℝ)
    (P : Matrix Role Role ℝ) (s : ℝ) : LocalCoframeField N :=
  fun x r a => (w x - 1) * roleLorentzMetric r a + (s * w x / 2) * P r a

theorem null_pencil_raw_solder (N : ℕ) (w : ArchiveRolePhaseGroup N → ℝ)
    (P : Matrix Role Role ℝ) (s : ℝ) (x : ArchiveRolePhaseGroup N) :
    rawSolderMatrix N (nullPencilCoframe N w P s) x =
      w x • roleLorentzMetric + (s * w x / 2) • P := by
  ext r a
  simp only [rawSolderMatrix, nullPencilCoframe,
    Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

theorem literal_site_gram_null_pencil (N : ℕ) (w : ArchiveRolePhaseGroup N → ℝ)
    (P : Matrix Role Role ℝ) (hP : P.transpose = P)
    (hnull : P * roleLorentzMetric * P = 0)
    (s : ℝ) (x : ArchiveRolePhaseGroup N) :
    a4dSiteGram N (nullPencilCoframe N w P s) x =
      (w x)^2 • roleLorentzMetric + (s * (w x)^2) • P := by
  unfold a4dSiteGram
  rw [null_pencil_raw_solder]
  exact null_gram_pencil P hP hnull (w x) s

theorem factorized_readout_constant_on_fiber {G X Y : Type*}
    (volume : G → X) (readout : X → Y) (g k : G)
    (hvolume : volume g = volume k) :
    readout (volume g) = readout (volume k) := congrArg readout hvolume

open D0.Gravity.A2CompensatorNoether

theorem auxiliary_stationary_action_unique {V E : Type*}
    [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]
    (B : Matrix V E ℚ) (W h : E → ℚ) (hW : ∀ e, 0 < W e)
    {phi psi : V → ℚ}
    (hphi : normalOperator B W phi = BPlus B (weightedEdge W h))
    (hpsi : normalOperator B W psi = BPlus B (weightedEdge W h)) :
    extendedAction B W h (2 • phi) = extendedAction B W h (2 • psi) := by
  unfold extendedAction
  rw [physical_residual_unique B W h hW hphi hpsi]

theorem auxiliary_gate_has_unique_action_value {V E : Type*}
    [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]
    (B : Matrix V E ℚ) (W h : E → ℚ) (hW : ∀ e, 0 < W e) :
    ∃ value : ℚ, ∃ phi : V → ℚ,
      normalOperator B W phi = BPlus B (weightedEdge W h) ∧
      ∀ psi : V → ℚ,
        normalOperator B W psi = BPlus B (weightedEdge W h) →
        extendedAction B W h (2 • psi) = value := by
  obtain ⟨phi, hphi⟩ := normal_equation_exists B W h hW
  refine ⟨extendedAction B W h (2 • phi), phi, hphi, ?_⟩
  intro psi hpsi
  exact auxiliary_stationary_action_unique B W h hW hpsi hphi

#print axioms null_gram_pencil
#print axioms null_pencil_raw_solder
#print axioms literal_site_gram_null_pencil
#print axioms factorized_readout_constant_on_fiber
#print axioms auxiliary_stationary_action_unique
#print axioms auxiliary_gate_has_unique_action_value

end
end D0.Research.NativeVolumeFiber
