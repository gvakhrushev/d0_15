import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Real.Basic
import D0.Matter.LocalTraceSource
import D0.Matter.RepresentationCarrier
import D0.Spectrum.GenerationTensorExactness
import D0.Geometry.ArchivePhaseShift

open scoped BigOperators

namespace D0.Matter

def partialTraceV {V N : Type} [Fintype V] [Fintype N] (M : Matrix (V × N) (V × N) ℝ) : Matrix N N ℝ :=
  fun i j => ∑ v, M (v, i) (v, j)

theorem trace_partialTrace {V N : Type} [Fintype V] [Fintype N] (M : Matrix (V × N) (V × N) ℝ) :
    Matrix.trace (partialTraceV M) = Matrix.trace M := by
  unfold Matrix.trace partialTraceV Matrix.diag
  dsimp
  rw [Fintype.sum_prod_type]
  rw [Finset.sum_comm]

def kronecker_I_C {V N : Type} [Fintype V] [DecidableEq V] (C_N : Matrix N N ℝ) : Matrix (V × N) (V × N) ℝ :=
  fun ⟨v1, n1⟩ ⟨v2, n2⟩ => (if v1 = v2 then 1 else 0) * C_N n1 n2

theorem partial_trace_commutes_with_shift {V N : Type} [Fintype V] [DecidableEq V] [Fintype N] [DecidableEq N]
    (M : Matrix (V × N) (V × N) ℝ) (C_N : Matrix N N ℝ)
    (h_comm : M * (kronecker_I_C C_N) = (kronecker_I_C C_N) * M) :
    (partialTraceV M) * C_N = C_N * (partialTraceV M) := by
  ext n1 n3
  unfold partialTraceV
  have h_eq : ∀ v : V, (∑ n2, M (v, n1) (v, n2) * C_N n2 n3) = ∑ n2, C_N n1 n2 * M (v, n2) (v, n3) := by
    intro v
    have h_comm_v := congr_fun (congr_fun h_comm (v, n1)) (v, n3)
    rw [Matrix.mul_apply, Matrix.mul_apply] at h_comm_v
    unfold kronecker_I_C at h_comm_v
    dsimp at h_comm_v
    have h_lhs : (∑ x : V × N, M (v, n1) x * ((if x.1 = v then (1 : ℝ) else 0) * C_N x.2 n3)) = ∑ n2, M (v, n1) (v, n2) * C_N n2 n3 := by
      rw [Fintype.sum_prod_type]
      dsimp
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro n2 _
      rw [Finset.sum_eq_single v]
      · simp
      · intro v2 _ hne
        simp [hne]
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    have h_rhs : (∑ x : V × N, ((if v = x.1 then (1 : ℝ) else 0) * C_N n1 x.2) * M x (v, n3)) = ∑ n2, C_N n1 n2 * M (v, n2) (v, n3) := by
      rw [Fintype.sum_prod_type]
      dsimp
      rw [Finset.sum_eq_single v]
      · simp
      · intro v2 _ hne
        simp [hne.symm]
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    rw [h_lhs, h_rhs] at h_comm_v
    exact h_comm_v
  rw [Matrix.mul_apply, Matrix.mul_apply]
  have h_sum_comm : (∑ n2 : N, (∑ v : V, M (v, n1) (v, n2)) * C_N n2 n3) = ∑ v : V, ∑ n2 : N, M (v, n1) (v, n2) * C_N n2 n3 := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro v _
    rw [Finset.sum_mul]
  have h_sum_comm2 : (∑ n2 : N, C_N n1 n2 * ∑ v : V, M (v, n2) (v, n3)) = ∑ v : V, ∑ n2 : N, C_N n1 n2 * M (v, n2) (v, n3) := by
    simp_rw [Finset.mul_sum]
    rw [Finset.sum_comm]
  rw [h_sum_comm, h_sum_comm2]
  apply Finset.sum_congr rfl
  intro v _
  exact h_eq v

lemma diag_eq_of_comm_shift {n : Nat} [NeZero n] (A : Matrix (Fin n) (Fin n) ℝ)
    (h : A * (D0.Spectrum.cyclicShiftMatrix n) = (D0.Spectrum.cyclicShiftMatrix n) * A) (i : Fin n) :
    A i i = A (D0.Spectrum.shift_g i 1) (D0.Spectrum.shift_g i 1) := by
  let target : Fin n := D0.Spectrum.shift_g i 1
  have h_comm_v := congr_fun (congr_fun h i) target
  rw [Matrix.mul_apply, Matrix.mul_apply] at h_comm_v
  unfold D0.Spectrum.cyclicShiftMatrix at h_comm_v
  have h_lhs : (∑ j : Fin n, A i j * (if target.val = (j.val + 1) % n then (1 : ℝ) else 0)) = A i i := by
    rw [Finset.sum_eq_single i]
    · simp [target, D0.Spectrum.shift_g]
    · intro j _ hne
      have h_ne_mod : target.val ≠ (j.val + 1) % n := by
        intro h_eq
        have h_eq_val : i.val = j.val := by
          have h_t_val : target.val = (i.val + 1) % n := rfl
          have hi := i.isLt
          have hj := j.isLt
          have hn : n > 0 := Nat.pos_of_ne_zero (NeZero.ne n)
          have h_i_cases : i.val + 1 < n ∨ i.val + 1 = n := by omega
          have h_j_cases : j.val + 1 < n ∨ j.val + 1 = n := by omega
          rcases h_i_cases with hi1 | hi2
          · rcases h_j_cases with hj1 | hj2
            · rw [Nat.mod_eq_of_lt hi1] at h_t_val
              rw [Nat.mod_eq_of_lt hj1] at h_eq
              omega
            · rw [Nat.mod_eq_of_lt hi1] at h_t_val
              rw [hj2, Nat.mod_self] at h_eq
              omega
          · rcases h_j_cases with hj1 | hj2
            · rw [hi2, Nat.mod_self] at h_t_val
              rw [Nat.mod_eq_of_lt hj1] at h_eq
              omega
            · omega
        exact hne (Fin.ext h_eq_val).symm
      rw [if_neg h_ne_mod, mul_zero]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  have h_rhs : (∑ j : Fin n, (if j.val = (i.val + 1) % n then (1 : ℝ) else 0) * A j target) = A target target := by
    rw [Finset.sum_eq_single target]
    · simp [target, D0.Spectrum.shift_g]
    · intro j _ hne
      have h_ne_val : j.val ≠ (i.val + 1) % n := by
        intro h_eq
        unfold target D0.Spectrum.shift_g at hne
        exact hne (Fin.ext h_eq)
      rw [if_neg h_ne_val, zero_mul]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  rw [h_lhs, h_rhs] at h_comm_v
  exact h_comm_v

lemma diag_eq_of_comm_shift_k {n : Nat} [NeZero n] (A : Matrix (Fin n) (Fin n) ℝ)
    (h : A * (D0.Spectrum.cyclicShiftMatrix n) = (D0.Spectrum.cyclicShiftMatrix n) * A) (i : Fin n) (k : Nat) :
    A i i = A (D0.Spectrum.shift_g i k) (D0.Spectrum.shift_g i k) := by
  induction k with
  | zero =>
    rw [D0.Spectrum.shift_g_zero]
  | succ k ih =>
    rw [ih]
    have h_step := diag_eq_of_comm_shift A h (D0.Spectrum.shift_g i k)
    rw [D0.Spectrum.shift_g_step]
    exact h_step

theorem partial_trace_density_uniform_under_shift {V : Type} [Fintype V] {n : Nat} [NeZero n]
    (M : Matrix (V × Fin n) (V × Fin n) ℝ)
    (h_comm : (partialTraceV M) * (D0.Spectrum.cyclicShiftMatrix n) = (D0.Spectrum.cyclicShiftMatrix n) * (partialTraceV M)) :
    ∀ i j : Fin n, (partialTraceV M) i i = (partialTraceV M) j j := by
  intro i j
  let A := partialTraceV M
  have h_eq := diag_eq_of_comm_shift_k A h_comm i (j.val + n - i.val)
  have h_val : (i.val + (j.val + n - i.val)) % n = j.val := by
    have : i.val + (j.val + n - i.val) = j.val + n := by omega
    rw [this, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt j.isLt
  have : D0.Spectrum.shift_g i (j.val + n - i.val) = j := Fin.ext h_val
  rw [this] at h_eq
  exact h_eq

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
  rw [trace_partialTrace]
  rw [h_lift]
  rw [D0.Spectrum.stage3_trace_relation Γ_SM]
  rw [h_zero]
  simp

end D0.Matter
