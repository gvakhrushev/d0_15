import D0.Geometry.A4DDiscreteEnergyKernel
import D0.Geometry.A4DConstitutiveKernelClassification
import D0.Geometry.A4DStarFiniteLorentzQuotient
import D0.Geometry.ArchiveExteriorFrameLift

/-! Research capsule: actual finite flux gates, without registry promotion.
The memo derives these gates from the existing fluxEnergy polynomial.
No desired gravitational contrast is included in either gate.
-/

open scoped BigOperators
open D0 D0.Geometry

namespace D0.Research.NativeFluxGate

noncomputable section

theorem energy_coframe_affine (N : ℕ) (e v : LocalCoframeField N)
    (ψ : ArchiveCochain N) (t : ℝ) :
    fluxEnergy N (e + t • v) ψ = fluxEnergy N e ψ +
      t * (fluxEnergy N v ψ - fluxEnergy N 0 ψ) := by
  unfold fluxEnergy
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply,
    zero_mul, mul_zero, Finset.sum_const_zero, sub_zero, add_zero]
  simp_rw [add_mul, Finset.sum_add_distrib, mul_assoc, ← Finset.mul_sum]
  ring

theorem energy_coframe_first_variation (N : ℕ) (e v : LocalCoframeField N)
    (ψ : ArchiveCochain N) (t : ℝ) :
    fluxEnergy N (e + t • v) ψ = fluxEnergy N e ψ +
      t / 2 * cochainPairing N ψ (flatStaggeredH N v ψ) := by
  rw [energy_coframe_affine]
  have hv := fluxEnergy_polarization_eq_H N v ψ
  have h0 := fluxEnergy_polarization_eq_H N 0 ψ
  rw [cochainPairing_add_right] at hv
  rw [flatStaggeredH_zero] at h0
  simp at h0
  linear_combination t / 2 * hv - t / 2 * h0

theorem energy_field_first_variation (N : ℕ) (e : LocalCoframeField N)
    (ψ φ : ArchiveCochain N) (t : ℝ) :
    fluxEnergy N e (ψ + t • φ) = fluxEnergy N e ψ +
      t * cochainPairing N φ (ψ + flatStaggeredH N e ψ) +
      t ^ 2 * fluxEnergy N e φ := by
  have hH : flatStaggeredH N e (ψ + t • φ) =
      flatStaggeredH N e ψ + t • flatStaggeredH N e φ := by
    rw [← fluxHMatrix_apply, ← fluxHMatrix_apply, ← fluxHMatrix_apply]
    simp [Matrix.mulVec_add, Matrix.mulVec_smul]
  have ht := fluxEnergy_polarization_eq_H N e (ψ + t • φ)
  rw [hH] at ht
  have hrearr : ψ + t • φ + (flatStaggeredH N e ψ + t • flatStaggeredH N e φ) =
      (ψ + flatStaggeredH N e ψ) + t • (φ + flatStaggeredH N e φ) := by
    simp only [smul_add]
    abel
  rw [hrearr, cochainPairing_add_left] at ht
  simp_rw [cochainPairing_add_right, cochainPairing_smul_left,
    cochainPairing_smul_right] at ht
  have hcross : cochainPairing N ψ (φ + flatStaggeredH N e φ) =
      cochainPairing N φ (ψ + flatStaggeredH N e ψ) := by
    rw [cochainPairing_add_right, cochainPairing_add_right]
    rw [cochainPairing_symm N ψ φ, ← flatStaggeredH_selfAdjoint,
      cochainPairing_symm N (flatStaggeredH N e ψ) φ]
  rw [hcross] at ht
  have hp := fluxEnergy_polarization_eq_H N e ψ
  have hf := fluxEnergy_polarization_eq_H N e φ
  simp_rw [cochainPairing_add_right] at ht hp hf ⊢
  linear_combination (1 / 2 : ℝ) * ht - (1 / 2 : ℝ) * hp - (t ^ 2 / 2) * hf

theorem exterior_frame_fixes_scalar_unit (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveExteriorFrameLift L (archiveFockExteriorEquiv.symm 1) =
      archiveFockExteriorEquiv.symm 1 := by
  simp [archiveExteriorFrameLift]

def FieldGate (N : ℕ) (e : LocalCoframeField N) (ψ : ArchiveCochain N) : Prop :=
  ψ + flatStaggeredH N e ψ = 0

def CoframeGate (N : ℕ) (ψ : ArchiveCochain N) : Prop :=
  ∀ v : LocalCoframeField N, cochainPairing N ψ (flatStaggeredH N v ψ) = 0

theorem field_gate_energy_zero (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) (h : FieldGate N e ψ) : fluxEnergy N e ψ = 0 := by
  have he := fluxEnergy_polarization_eq_H N e ψ
  rw [show ψ + flatStaggeredH N e ψ = 0 from h] at he
  simp [cochainPairing] at he
  linarith

theorem counting_self_zero (N : ℕ) (ψ : ArchiveCochain N)
    (h : cochainPairing N ψ ψ = 0) : ψ = 0 := by
  have hs : (∑ x, ∑ S, (ψ (x, S)) ^ 2) = 0 := by
    simpa only [cochainPairing, pow_two] using h
  have hx : ∀ x, (∑ S, (ψ (x, S)) ^ 2) = 0 := by
    intro x
    exact (Finset.sum_eq_zero_iff_of_nonneg
      (fun y _ => Finset.sum_nonneg (fun S _ => sq_nonneg (ψ (y, S))))).1
      hs x (Finset.mem_univ x)
  funext p
  have hp : (ψ p) ^ 2 = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg
      (fun S _ => sq_nonneg (ψ (p.1, S)))).1 (hx p.1) p.2 (Finset.mem_univ p.2)
  exact (sq_eq_zero_iff).1 hp

theorem full_joint_gate_forces_zero_field (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) (hf : FieldGate N e ψ) (hc : CoframeGate N ψ) :
    ψ = 0 := by
  apply counting_self_zero N ψ
  have hh := congrArg (cochainPairing N ψ) hf
  rw [cochainPairing_add_right, hc e] at hh
  simpa [cochainPairing] using hh

theorem zero_field_full_gate (N : ℕ) (e : LocalCoframeField N) :
    FieldGate N e 0 ∧ CoframeGate N 0 ∧ fluxEnergy N e 0 = 0 := by
  have hh : flatStaggeredH N e 0 = 0 := by
    rw [← fluxHMatrix_apply]
    simp
  refine ⟨?_, ?_, ?_⟩
  · simp [FieldGate, hh]
  · intro v
    simp [cochainPairing]
  · simp [fluxEnergy]

theorem full_joint_gate_iff_zero_field (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    (FieldGate N e ψ ∧ CoframeGate N ψ) ↔ ψ = 0 := by
  constructor
  · intro h
    exact full_joint_gate_forces_zero_field N e ψ h.1 h.2
  · rintro rfl
    exact ⟨(zero_field_full_gate N e).1, (zero_field_full_gate N e).2.1⟩

theorem small_coframe_field_gate_forces_zero (N : ℕ)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N)
    (hsmall : 8196 * ‖e‖ < 1) (hf : FieldGate N e ψ) : ψ = 0 := by
  by_contra hn
  have hp := fluxEnergy_small_e_positive_max N e hsmall ψ hn
  rw [field_gate_energy_zero N e ψ hf] at hp
  exact (lt_irrefl 0) hp

theorem polynomial_positive_gate_forces_zero
    {n : Type*} [Fintype n] [DecidableEq n]
    (α : ℝ) (hα : (1 : ℝ) / 4 < α) (H : Matrix n n ℝ)
    (hH : H.transpose = H) (ψ : n → ℝ)
    (hf : (kernelPoly α H).mulVec ψ = 0) : ψ = 0 := by
  by_contra hn
  have hp := kernelPoly_positive_of_quarter_lt α hα H hH ψ hn
  rw [hf] at hp
  simp at hp

end
end D0.Research.NativeFluxGate

#check D0.Research.NativeFluxGate.full_joint_gate_iff_zero_field
#check D0.Research.NativeFluxGate.energy_coframe_first_variation
#check D0.Research.NativeFluxGate.energy_field_first_variation
#check D0.Research.NativeFluxGate.small_coframe_field_gate_forces_zero
#check D0.Research.NativeFluxGate.polynomial_positive_gate_forces_zero
#print axioms D0.Research.NativeFluxGate.full_joint_gate_iff_zero_field
#print axioms D0.Research.NativeFluxGate.energy_coframe_first_variation
#print axioms D0.Research.NativeFluxGate.energy_field_first_variation
#print axioms D0.Research.NativeFluxGate.exterior_frame_fixes_scalar_unit
#print axioms D0.Research.NativeFluxGate.small_coframe_field_gate_forces_zero
#print axioms D0.Research.NativeFluxGate.polynomial_positive_gate_forces_zero
