import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Logic.Equiv.Fin.Rotate
import D0.Algebra.FiniteMatrixTensorProduct
import D0.Algebra.FiniteMatrixPartialTrace
import D0.Topology.ArchiveShiftTopology

open scoped BigOperators

namespace D0.Spectrum

/-- Compatibility name for the shared finite matrix tensor product `1 ⊗ Γ_SM`. -/
def tensor_product_I {G N : Type} [Fintype G] [DecidableEq G] (Γ_SM : Matrix N N ℝ) : Matrix (G × N) (G × N) ℝ :=
  D0.Algebra.finiteMatrixTensorProduct (1 : Matrix G G ℝ) Γ_SM

theorem stage1_tensor_exactness {G N : Type} [Fintype G] [DecidableEq G] [Fintype N]
    (Γ_lift : Matrix (G × N) (G × N) ℝ) (Γ_SM : Matrix N N ℝ)
    (h_off : ∀ (g1 g2 : G) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_diag : ∀ (g : G) (n1 n2 : N), Γ_lift ⟨g, n1⟩ ⟨g, n2⟩ = Γ_SM n1 n2) :
    Γ_lift = tensor_product_I Γ_SM := by
  ext ⟨g1, n1⟩ ⟨g2, n2⟩
  change Γ_lift (g1, n1) (g2, n2) =
    (1 : Matrix G G ℝ) g1 g2 * Γ_SM n1 n2
  rw [Matrix.one_apply]
  split_ifs with hg
  · subst g2
    rw [one_mul]
    exact h_diag g1 n1 n2
  · rw [zero_mul]
    exact h_off g1 g2 n1 n2 hg

def cyclicShiftMatrix (n : Nat) : Matrix (Fin n) (Fin n) ℝ :=
  fun i j => if j.val = (i.val + 1) % n then 1 else 0

theorem cyclicShiftMatrix_eq_topology_shift {n : Nat} :
    cyclicShiftMatrix n = D0.Topology.shiftMatrix (finRotate n) := by
  ext i j
  have h_rotate : (finRotate n i).val = (i.val + 1) % n := by
    rw [finRotate_apply]
    simp [Fin.val_add]
  change (if j.val = (i.val + 1) % n then (1 : ℝ) else 0) =
    (if j = finRotate n i then 1 else 0)
  have h_condition : j.val = (i.val + 1) % n ↔ j = finRotate n i := by
    constructor
    · intro h_val
      exact Fin.ext (h_val.trans h_rotate.symm)
    · intro h_eq
      subst j
      exact h_rotate
  simp [h_condition]

/-- Compatibility name for the shared finite matrix tensor product `C_G ⊗ 1`. -/
def kronecker_C_I {G N : Type} [Fintype G] [DecidableEq G] [DecidableEq N] (C_G : Matrix G G ℝ) : Matrix (G × N) (G × N) ℝ :=
  D0.Algebra.finiteMatrixTensorProduct C_G (1 : Matrix N N ℝ)

def shift_g {n : Nat} [NeZero n] (g : Fin n) (k : Nat) : Fin n :=
  ⟨(g.val + k) % n, Nat.mod_lt _ (NeZero.pos n)⟩

private def generationShiftPerm {N : Type} (n : Nat) : Equiv.Perm (Fin n × N) where
  toFun x := (finRotate n x.1, x.2)
  invFun x := ((finRotate n).symm x.1, x.2)
  left_inv x := by
    rcases x with ⟨g, n'⟩
    apply Prod.ext
    · exact Equiv.symm_apply_apply _ _
    · rfl
  right_inv x := by
    rcases x with ⟨g, n'⟩
    apply Prod.ext
    · exact Equiv.apply_symm_apply _ _
    · rfl

private lemma kronecker_C_I_cyclicShift_eq_topology_shift {N : Type} [Fintype N] [DecidableEq N]
    {n : Nat} [NeZero n] :
    kronecker_C_I (cyclicShiftMatrix n) =
      D0.Topology.shiftMatrix (generationShiftPerm (N := N) n) := by
  ext ⟨g1, m1⟩ ⟨g2, m2⟩
  change (cyclicShiftMatrix n) g1 g2 * (1 : Matrix N N ℝ) m1 m2 =
    (if (g2, m2) = generationShiftPerm (N := N) n (g1, m1) then (1 : ℝ) else 0)
  rw [Matrix.one_apply, cyclicShiftMatrix_eq_topology_shift]
  by_cases hg : g2 = g1 + 1 <;> by_cases hm : m1 = m2 <;>
    simp [D0.Topology.shiftMatrix, generationShiftPerm, hg, hm, eq_comm]

lemma shift_g_zero {n : Nat} [NeZero n] (g : Fin n) : shift_g g 0 = g := by
  unfold shift_g
  simp only [add_zero]
  exact Fin.ext (Nat.mod_eq_of_lt g.isLt)

lemma shift_g_step {n : Nat} [NeZero n] (g : Fin n) (k : Nat) :
    shift_g g (k + 1) = shift_g (shift_g g k) 1 := by
  unfold shift_g
  ext
  dsimp
  rcases n with _|n
  · rcases g with ⟨_, isLt⟩
    contradiction
  rcases n with _|n
  · omega
  · have h1 : 1 % (n + 2) = 1 := rfl
    have h_mod := Nat.add_mod (g.val + k) 1 (n + 2)
    change (g.val + (k + 1)) % (n + 2) = ((g.val + k) % (n + 2) + 1) % (n + 2)
    have h_eq : g.val + (k + 1) = g.val + k + 1 := by omega
    rw [h_eq, h_mod, h1]

lemma shift_g_one_eq_finRotate {n : Nat} [NeZero n] (g : Fin n) :
    shift_g g 1 = finRotate n g := by
  apply Fin.ext
  change (g.val + 1) % n = (finRotate n g).val
  rw [finRotate_apply]
  simp [Fin.val_add]

lemma shift_g_eq_finRotate_iterate {n : Nat} [NeZero n] (g : Fin n) (k : Nat) :
    shift_g g k = ((finRotate n : Fin n → Fin n)^[k]) g := by
  induction k with
  | zero =>
      rw [shift_g_zero]
      rfl
  | succ k ih =>
      rw [shift_g_step, shift_g_one_eq_finRotate]
      rw [Function.iterate_succ', ih]
      rfl

lemma flavor_blindness_step_of_commute {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g : Fin n) (n1 n2 : N) :
    Γ_lift (g, n1) (g, n2) = Γ_lift (shift_g g 1, n1) (shift_g g 1, n2) := by
  have h_topology : Γ_lift * D0.Topology.shiftMatrix (generationShiftPerm n) =
      D0.Topology.shiftMatrix (generationShiftPerm n) * Γ_lift := by
    rw [kronecker_C_I_cyclicShift_eq_topology_shift] at h_comm
    exact h_comm
  have h_entries := D0.Topology.commute_with_shift_entries
    Γ_lift (generationShiftPerm n) h_topology (g, n1) (g, n2)
  have h_rotate : shift_g g 1 = finRotate n g := by
    apply Fin.ext
    change (g.val + 1) % n = (finRotate n g).val
    rw [finRotate_apply]
    simp [Fin.val_add]
  rw [h_rotate]
  exact h_entries

lemma flavor_blindness_step {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ)
    (_h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g : Fin n) (n1 n2 : N) :
    Γ_lift (g, n1) (g, n2) = Γ_lift (shift_g g 1, n1) (shift_g g 1, n2) :=
  flavor_blindness_step_of_commute Γ_lift h_comm g n1 n2

lemma flavor_blindness_step_k {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ)
    (h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g : Fin n) (k : Nat) (n1 n2 : N) :
    Γ_lift (g, n1) (g, n2) = Γ_lift (shift_g g k, n1) (shift_g g k, n2) := by
  induction k with
  | zero =>
    rw [shift_g_zero]
  | succ k ih =>
    rw [ih]
    have h_step := flavor_blindness_step Γ_lift h_off h_comm (shift_g g k) n1 n2
    rw [shift_g_step]
    exact h_step

theorem stage2_flavor_blindness {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ)
    (h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g1 g2 : Fin n) (n1 n2 : N) :
    Γ_lift (g1, n1) (g1, n2) = Γ_lift (g2, n1) (g2, n2) := by
  have h_eq := flavor_blindness_step_k Γ_lift h_off h_comm g1 (g2.val + n - g1.val) n1 n2
  have h_val : (g1.val + (g2.val + n - g1.val)) % n = g2.val := by
    have : g1.val + (g2.val + n - g1.val) = g2.val + n := by omega
    rw [this, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt g2.isLt
  have : shift_g g1 (g2.val + n - g1.val) = g2 := Fin.ext h_val
  rw [this] at h_eq
  exact h_eq

theorem stage3_tensor_exactness {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ) (Γ_SM : Matrix N N ℝ)
    (h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g0 : Fin n) (h_g0 : ∀ n1 n2 : N, Γ_lift (g0, n1) (g0, n2) = Γ_SM n1 n2) :
    Γ_lift = tensor_product_I Γ_SM := by
  apply stage1_tensor_exactness Γ_lift Γ_SM h_off
  intro g n1 n2
  rw [stage2_flavor_blindness Γ_lift h_off h_comm g g0 n1 n2]
  exact h_g0 n1 n2

theorem stage3_trace_relation {G N : Type} [Fintype G] [DecidableEq G] [Fintype N]
    (Γ_SM : Matrix N N ℝ) :
    Matrix.trace (tensor_product_I (G := G) Γ_SM) = Fintype.card G * Matrix.trace Γ_SM := by
  calc
    Matrix.trace (tensor_product_I (G := G) Γ_SM) =
        Matrix.trace (D0.Algebra.finiteMatrixPartialTraceLeft
          (tensor_product_I (G := G) Γ_SM)) := by
      symm
      exact D0.Algebra.finiteMatrixPartialTraceLeft_trace
        (tensor_product_I (G := G) Γ_SM)
    _ = Matrix.trace (Matrix.trace (1 : Matrix G G ℝ) • Γ_SM) := by
      congr 1
      simpa [tensor_product_I] using
        (D0.Algebra.finiteMatrixPartialTraceLeft_tensorProduct
          (A := (1 : Matrix G G ℝ)) Γ_SM)
    _ = Fintype.card G * Matrix.trace Γ_SM := by
      simp [Matrix.trace_smul, Matrix.trace_one]

theorem stage3_trace_relation_three {G N : Type} [Fintype G] [DecidableEq G] [Fintype N]
    (Γ_SM : Matrix N N ℝ) (h_card : Fintype.card G = 3) :
    Matrix.trace (tensor_product_I (G := G) Γ_SM) = 3 * Matrix.trace Γ_SM := by
  rw [stage3_trace_relation Γ_SM, h_card]
  push_cast
  rfl

end D0.Spectrum
