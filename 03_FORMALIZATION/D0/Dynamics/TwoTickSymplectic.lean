import D0.Dynamics.ToralAutomorphism
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

namespace D0.Dynamics

open Matrix

/-- Canonical symplectic form on the 2D toral integer lattice. -/
def Jsymp : ZMat2 := !![0, 1; -1, 0]

/-- Canonical invariant Lorentzian / hyperbolic form on the 2D toral integer lattice. -/
def Gform : ZMat2 := !![-2, 1; 1, 2]

/-- The two-tick operator T² has explicit integer entries !![1, -1; -1, 2]. -/
theorem T_sq_entries : T ^ 2 = !![1, -1; -1, 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- The determinant of the two-tick operator is +1 (orientation-preserving). -/
theorem det_T_sq : Matrix.det (T ^ 2) = 1 := by
  rw [det_T_pow]
  norm_num

/-- One tick is strictly anti-symplectic: Tᵀ J T = -J. -/
theorem T_anti_symplectic : T.transpose * Jsymp * T = -Jsymp := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- Two ticks are symplectic: (T²)ᵀ J (T²) = J. -/
theorem T_sq_symplectic : (T ^ 2).transpose * Jsymp * (T ^ 2) = Jsymp := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- One tick reverses the Lorentzian form G: Tᵀ G T = -G. -/
theorem T_anti_G : T.transpose * Gform * T = -Gform := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- Two ticks preserve the Lorentzian form G: (T²)ᵀ G (T²) = G. -/
theorem T_sq_preserves_G : (T ^ 2).transpose * Gform * (T ^ 2) = Gform := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- The discriminant / determinant of Gform is -5 (indefinite, Lorentzian signature). -/
theorem det_G : Matrix.det Gform = -5 := by
  native_decide

/-- Two ticks are non-trivial: T² ≠ I. -/
theorem T_sq_ne_one : T ^ 2 ≠ 1 := by
  intro h
  have h00 : (T ^ 2) 0 1 = (1 : ZMat2) 0 1 := by rw [h]
  rw [T_sq_entries] at h00
  revert h00
  native_decide

/-- Parity theorem for time powers: (Tⁿ)ᵀ J (Tⁿ) = (-1)ⁿ • J. -/
theorem T_pow_anti_symplectic (n : ℕ) :
    (T ^ n).transpose * Jsymp * (T ^ n) = ((-1 : ℤ) ^ n) • Jsymp := by
  induction n with
  | zero =>
    ext i j
    fin_cases i <;> fin_cases j <;> native_decide
  | succ k ih =>
    have h1 : T ^ (k + 1) = T ^ k * T := pow_succ T k
    rw [h1, transpose_mul]
    have h_assoc : (T.transpose * (T ^ k).transpose) * Jsymp * (T ^ k * T) =
        T.transpose * ((T ^ k).transpose * Jsymp * (T ^ k)) * T := by
      simp only [Matrix.mul_assoc]
    rw [h_assoc, ih, Matrix.mul_smul, Matrix.smul_mul, T_anti_symplectic, smul_neg, ← neg_smul, pow_succ]
    congr 1
    ring

/-- Parity theorem for Lorentzian form: (Tⁿ)ᵀ G (Tⁿ) = (-1)ⁿ • G. -/
theorem T_pow_anti_G (n : ℕ) :
    (T ^ n).transpose * Gform * (T ^ n) = ((-1 : ℤ) ^ n) • Gform := by
  induction n with
  | zero =>
    ext i j
    fin_cases i <;> fin_cases j <;> native_decide
  | succ k ih =>
    have h1 : T ^ (k + 1) = T ^ k * T := pow_succ T k
    rw [h1, transpose_mul]
    have h_assoc : (T.transpose * (T ^ k).transpose) * Gform * (T ^ k * T) =
        T.transpose * ((T ^ k).transpose * Gform * (T ^ k)) * T := by
      simp only [Matrix.mul_assoc]
    rw [h_assoc, ih, Matrix.mul_smul, Matrix.smul_mul, T_anti_G, smul_neg, ← neg_smul, pow_succ]
    congr 1
    ring

/-- No non-zero integer bilinear form is invariant under the single-tick operator T. -/
theorem one_tick_no_invariant_form (B : ZMat2) (h : T.transpose * B * T = B) : B = 0 := by
  have h00 : (T.transpose * B * T) 0 0 = B 0 0 := by rw [h]
  have h01 : (T.transpose * B * T) 0 1 = B 0 1 := by rw [h]
  have h10 : (T.transpose * B * T) 1 0 = B 1 0 := by rw [h]
  have h11 : (T.transpose * B * T) 1 1 = B 1 1 := by rw [h]
  unfold T at h00 h01 h10 h11
  simp only [mul_apply, transpose_apply, Fin.sum_univ_two] at h00 h01 h10 h11
  norm_num at h00 h01 h10 h11
  have hb00 : B 0 0 = 0 := by linarith
  have hb11 : B 1 1 = 0 := by linarith
  have hb01 : B 0 1 = 0 := by linarith
  have hb10 : B 1 0 = 0 := by linarith
  ext i j
  fin_cases i <;> fin_cases j <;> simp [hb00, hb01, hb10, hb11]

/-- Full classification of all two-tick invariant bilinear forms:
    (T²)ᵀ B (T²) = B iff B has the exact two-parameter form !![-a, a - c; c, a]. -/
theorem two_tick_invariant_forms (B : ZMat2) :
    (T ^ 2).transpose * B * (T ^ 2) = B ↔ ∃ a c : ℤ, B = !![-a, a - c; c, a] := by
  constructor
  · intro h
    have h00 : ((T ^ 2).transpose * B * (T ^ 2)) 0 0 = B 0 0 := by rw [h]
    have h01 : ((T ^ 2).transpose * B * (T ^ 2)) 0 1 = B 0 1 := by rw [h]
    have h10 : ((T ^ 2).transpose * B * (T ^ 2)) 1 0 = B 1 0 := by rw [h]
    have h11 : ((T ^ 2).transpose * B * (T ^ 2)) 1 1 = B 1 1 := by rw [h]
    rw [T_sq_entries] at h00 h01 h10 h11
    simp only [mul_apply, transpose_apply, Fin.sum_univ_two] at h00 h01 h10 h11
    norm_num at h00 h01 h10 h11
    use B 1 1, B 1 0
    ext i j
    fin_cases i <;> fin_cases j
    · norm_num; linarith
    · norm_num; linarith
    · norm_num
    · norm_num
  · rintro ⟨a, c, rfl⟩
    rw [T_sq_entries]
    ext i j
    fin_cases i <;> fin_cases j <;> {
      simp only [mul_apply, transpose_apply, Fin.sum_univ_two]
      norm_num
      try ring
    }

/-- Rational 2-tick update on coordinates: q' = q - p. -/
def updateQ (q p : ℚ) : ℚ := q - p

/-- Rational 2-tick update on momenta: p' = -q + 2p. -/
def updateP (q p : ℚ) : ℚ := -q + 2 * p

/-- The discrete two-tick generating relations:
    p = q - q' and p' = q - 2q'. -/
theorem generating_relations_q_p (q p q' p' : ℚ)
    (hq : q' = updateQ q p) (hp : p' = updateP q p) :
    p = q - q' ∧ p' = q - 2 * q' := by
  have hq_unfold : q' = q - p := hq
  have hp_unfold : p' = -q + 2 * p := hp
  constructor
  · linarith
  · linarith

/-- Rational discrete Euler-Lagrange operator for the two-tick generating action. -/
def twoTickEL (qPrev q qNext : ℚ) : ℚ :=
  -qPrev + 3 * q - qNext

/-- Exact equivalence of the two-tick Euler-Lagrange condition with the step recurrence. -/
theorem twoTickEL_eq_zero_iff (qPrev q qNext : ℚ) :
    twoTickEL qPrev q qNext = 0 ↔ qNext = 3 * q - qPrev := by
  unfold twoTickEL
  constructor
  · intro h; linarith
  · intro h; linarith

/-- The standard two-tick trajectory satisfies the discrete Euler-Lagrange equation. -/
theorem twoTickEL_satisfied_by_evolution (q : ℤ → ℚ)
    (h_rec : ∀ k : ℤ, q (k + 1) = 3 * q k - q (k - 1)) (k : ℤ) :
    twoTickEL (q (k - 1)) (q k) (q (k + 1)) = 0 := by
  rw [twoTickEL_eq_zero_iff]
  exact h_rec k

end D0.Dynamics
