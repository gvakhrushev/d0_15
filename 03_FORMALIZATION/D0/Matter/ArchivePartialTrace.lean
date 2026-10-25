import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Logic.Equiv.Fin.Rotate
import D0.Algebra.FiniteMatrixPartialTrace
import D0.Matter.LocalTraceSource
import D0.Matter.RepresentationCarrier
import D0.Spectrum.GenerationTensorExactness
import D0.Geometry.ArchivePhaseShift
import D0.Topology.ArchiveShiftTopology

open scoped BigOperators

namespace D0.Matter

def partialTraceV {V N : Type} [Fintype V] [Fintype N] (M : Matrix (V × N) (V × N) ℝ) : Matrix N N ℝ :=
  D0.Algebra.finiteMatrixPartialTraceLeft M

theorem trace_partialTrace {V N : Type} [Fintype V] [Fintype N] (M : Matrix (V × N) (V × N) ℝ) :
    Matrix.trace (partialTraceV M) = Matrix.trace M := by
  exact D0.Algebra.finiteMatrixPartialTraceLeft_trace M

/-- Compatibility name for Spectrum's shared `1 ⊗ C_N` tensor operator. -/
def kronecker_I_C {V N : Type} [Fintype V] [DecidableEq V] (C_N : Matrix N N ℝ) : Matrix (V × N) (V × N) ℝ :=
  D0.Spectrum.tensor_product_I C_N

theorem partial_trace_commutes_with_shift {V N : Type} [Fintype V] [DecidableEq V] [Fintype N] [DecidableEq N]
    (M : Matrix (V × N) (V × N) ℝ) (C_N : Matrix N N ℝ)
    (h_comm : M * (kronecker_I_C C_N) = (kronecker_I_C C_N) * M) :
    (partialTraceV M) * C_N = C_N * (partialTraceV M) := by
  apply D0.Algebra.finiteMatrixPartialTraceLeft_commutes_rightTensor
  simpa [kronecker_I_C, D0.Spectrum.tensor_product_I] using h_comm

private def finRotateArchiveTopology {n : Nat} [NeZero n] :
    D0.Topology.ArchiveTopology (Fin n) where
  shift := finRotate n
  is_single_orbit := by
    intro i j
    let k := j.val + n - i.val
    refine ⟨k, ?_⟩
    have h_val : (i.val + (j.val + n - i.val)) % n = j.val := by
      have h_sum : i.val + (j.val + n - i.val) = j.val + n := by omega
      rw [h_sum, Nat.add_mod_right]
      exact Nat.mod_eq_of_lt j.isLt
    have h_shift : D0.Spectrum.shift_g i k = j := Fin.ext h_val
    rw [D0.Spectrum.shift_g_eq_finRotate_iterate] at h_shift
    exact h_shift

lemma diag_eq_of_comm_shift {n : Nat} [NeZero n] (A : Matrix (Fin n) (Fin n) ℝ)
    (h : A * (D0.Spectrum.cyclicShiftMatrix n) = (D0.Spectrum.cyclicShiftMatrix n) * A) (i : Fin n) :
    A i i = A (D0.Spectrum.shift_g i 1) (D0.Spectrum.shift_g i 1) := by
  have h_topology : A * D0.Topology.shiftMatrix (finRotate n) =
      D0.Topology.shiftMatrix (finRotate n) * A := by
    simpa [D0.Spectrum.cyclicShiftMatrix_eq_topology_shift] using h
  have h_step := D0.Topology.commute_with_shift_step A (finRotate n) h_topology i
  rw [D0.Spectrum.shift_g_one_eq_finRotate]
  exact h_step

lemma diag_eq_of_comm_shift_k {n : Nat} [NeZero n] (A : Matrix (Fin n) (Fin n) ℝ)
    (h : A * (D0.Spectrum.cyclicShiftMatrix n) = (D0.Spectrum.cyclicShiftMatrix n) * A) (i : Fin n) (k : Nat) :
    A i i = A (D0.Spectrum.shift_g i k) (D0.Spectrum.shift_g i k) := by
  have h_topology : A * D0.Topology.shiftMatrix (finRotate n) =
      D0.Topology.shiftMatrix (finRotate n) * A := by
    simpa [D0.Spectrum.cyclicShiftMatrix_eq_topology_shift] using h
  have h_iterate := D0.Topology.commute_with_shift_iterate A (finRotate n) h_topology i k
  rw [← D0.Spectrum.shift_g_eq_finRotate_iterate] at h_iterate
  exact h_iterate

theorem partial_trace_density_uniform_under_shift {V : Type} [Fintype V] {n : Nat} [NeZero n]
    (M : Matrix (V × Fin n) (V × Fin n) ℝ)
    (h_comm : (partialTraceV M) * (D0.Spectrum.cyclicShiftMatrix n) = (D0.Spectrum.cyclicShiftMatrix n) * (partialTraceV M)) :
    ∀ i j : Fin n, (partialTraceV M) i i = (partialTraceV M) j j := by
  intro i j
  let A := partialTraceV M
  have h_topology : A * D0.Topology.shiftMatrix (finRotate n) =
      D0.Topology.shiftMatrix (finRotate n) * A := by
    simpa [A, D0.Spectrum.cyclicShiftMatrix_eq_topology_shift] using h_comm
  exact D0.Topology.abstract_shift_commute_implies_diagonal_constant
    A finRotateArchiveTopology h_topology i j

theorem archive_density_from_total_trace {V : Type} [Fintype V] {n : Nat} [NeZero n]
    (M : Matrix (V × Fin n) (V × Fin n) ℝ) (R : MatterRep)
    (h_trace : Matrix.trace M = (R.anomalySum : ℝ))
    (h_const : ∃ c : ℝ, ∀ i : Fin n, (partialTraceV M) i i = c)
    (i : Fin n) :
    localTraceDensity (partialTraceV M) i = (R.anomalySum : ℝ) / n := by
  unfold localTraceDensity
  obtain ⟨c, hc⟩ := h_const
  have hc_i := hc i
  rw [hc_i]
  have h_trace_pt := trace_partialTrace M
  rw [h_trace] at h_trace_pt
  unfold Matrix.trace Matrix.diag at h_trace_pt
  have h_sum_c : (∑ i : Fin n, (partialTraceV M) i i) = ∑ i : Fin n, c := Finset.sum_congr rfl (fun j _ => hc j)
  rw [h_sum_c, Finset.sum_const, nsmul_eq_mul, Finset.card_univ, Fintype.card_fin] at h_trace_pt
  have h_n_real : (n : ℝ) ≠ 0 := by
    exact_mod_cast NeZero.ne n
  have h_c : c = (R.anomalySum : ℝ) / n := by
    apply eq_div_of_mul_eq h_n_real
    rw [mul_comm]
    exact h_trace_pt
  exact h_c

theorem partial_trace_commutes_with_phase_shift {V : Type} [Fintype V] [DecidableEq V] {n : ℕ} [NeZero n]
    (Γ_tot : Matrix (V × ZMod n) (V × ZMod n) ℝ)
    (h_comm : Γ_tot * (kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) = (kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) * Γ_tot) :
    (partialTraceV Γ_tot) * (D0.Geometry.archiveShiftMatrix n) = (D0.Geometry.archiveShiftMatrix n) * (partialTraceV Γ_tot) :=
  partial_trace_commutes_with_shift Γ_tot (D0.Geometry.archiveShiftMatrix n) h_comm

/-- The archive component of `1 ⊗ Γ_SM` is the exact generation
multiplicity times `Γ_SM`. -/
theorem partial_trace_generation_lift {G : Type} [Fintype G] [DecidableEq G] {n : Nat}
    (Γ_SM : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) :
    partialTraceV (D0.Spectrum.tensor_product_I (G := G) Γ_SM) =
      Fintype.card G • Γ_SM := by
  rw [partialTraceV, D0.Spectrum.tensor_product_I]
  rw [D0.Algebra.finiteMatrixPartialTraceLeft_tensorProduct, Matrix.trace_one]
  rw [← Nat.cast_smul_eq_nsmul ℝ (Fintype.card G) Γ_SM]

theorem density_uniform_from_commute {V : Type} [Fintype V] [DecidableEq V] {n : ℕ} [NeZero n]
    (Γ_tot : Matrix (V × ZMod n) (V × ZMod n) ℝ)
    (h_comm : Γ_tot * (kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) = (kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) * Γ_tot) :
    ∃ c : ℝ, ∀ i : ZMod n, (partialTraceV Γ_tot) i i = c := by
  have h_pt_comm := partial_trace_commutes_with_phase_shift Γ_tot h_comm
  have h_const := D0.Geometry.commute_with_shift_implies_diagonal_constant (partialTraceV Γ_tot) h_pt_comm
  use (partialTraceV Γ_tot) 0 0
  intro i
  exact (h_const 0 i).symm

theorem archive_density_from_total_trace_zmod {V : Type} [Fintype V] {n : ℕ} [NeZero n]
    (M : Matrix (V × ZMod n) (V × ZMod n) ℝ) (R : MatterRep)
    (h_trace : Matrix.trace M = (R.anomalySum : ℝ))
    (h_const : ∃ c : ℝ, ∀ i : ZMod n, (partialTraceV M) i i = c)
    (i : ZMod n) :
    localTraceDensity (partialTraceV M) i = (R.anomalySum : ℝ) / n := by
  unfold localTraceDensity
  obtain ⟨c, hc⟩ := h_const
  have hc_i := hc i
  rw [hc_i]
  have h_trace_pt := trace_partialTrace M
  rw [h_trace] at h_trace_pt
  unfold Matrix.trace Matrix.diag at h_trace_pt
  have h_sum_c : (∑ i : ZMod n, (partialTraceV M) i i) = ∑ i : ZMod n, c := Finset.sum_congr rfl (fun j _ => hc j)
  rw [h_sum_c, Finset.sum_const, nsmul_eq_mul, Finset.card_univ, ZMod.card] at h_trace_pt
  have h_n_real : (n : ℝ) ≠ 0 := by
    exact_mod_cast NeZero.ne n
  have h_c : c = (R.anomalySum : ℝ) / n := by
    apply eq_div_of_mul_eq h_n_real
    rw [mul_comm]
    exact h_trace_pt
  exact h_c

theorem phase_symmetric_total_operator_yields_uniform_archive_density {V : Type} [Fintype V] [DecidableEq V] {n : ℕ} [NeZero n]
    (Γ_tot : Matrix (V × ZMod n) (V × ZMod n) ℝ) (R : MatterRep)
    (h_comm : Γ_tot * (kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) = (kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) * Γ_tot)
    (h_trace : Matrix.trace Γ_tot = (R.anomalySum : ℝ))
    (h_anomaly : R.anomalySum = 0) :
    (∑ i : ZMod n, localTraceDensity (partialTraceV Γ_tot) i) = 0 := by
  have h_const : ∃ c : ℝ, ∀ i : ZMod n, (partialTraceV Γ_tot) i i = c := density_uniform_from_commute Γ_tot h_comm
  have h_dens : ∀ i : ZMod n, localTraceDensity (partialTraceV Γ_tot) i = (R.anomalySum : ℝ) / n :=
    archive_density_from_total_trace_zmod Γ_tot R h_trace h_const
  have h_eq_zero : ∀ i : ZMod n, localTraceDensity (partialTraceV Γ_tot) i = 0 := by
    intro i
    rw [h_dens i, h_anomaly]
    simp
  have h_sum : (∑ i : ZMod n, localTraceDensity (partialTraceV Γ_tot) i) = 0 := by
    rw [Finset.sum_eq_zero]
    intro x _
    exact h_eq_zero x
  exact h_sum

theorem generation_trace_neutrality_connection {G : Type} [Fintype G] [DecidableEq G] {n : Nat}
    (Γ_SM : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) (Γ_lift : Matrix (G × archivePhaseIndex n) (G × archivePhaseIndex n) ℝ)
    (h_lift : Γ_lift = D0.Spectrum.tensor_product_I Γ_SM)
    (h_zero : Matrix.trace Γ_SM = 0) :
    NeutralSource (localTraceDensity (partialTraceV Γ_lift)) := by
  unfold NeutralSource
  rw [sum_localTraceDensity_eq_trace]
  rw [h_lift]
  rw [partial_trace_generation_lift]
  rw [Matrix.trace_smul, h_zero]
  simp

end D0.Matter
