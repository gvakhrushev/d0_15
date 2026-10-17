import D0.Representation.GoldenCoherentMemory
import Mathlib.Tactic

/-! Generic research kernel. The analytic fixed-space classification and the
actual AF path/frame/spectral binding are separate exact-certificate evidence.
These propositions do not assert physical preparation or refinement admission. -/
namespace D0.Research.FibonacciRecordActivation
noncomputable section
open Matrix D0.Representation.GoldenRelativeChannel

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]

def lift (V : Matrix m n ℝ) (U : Matrix n n ℝ) : Matrix m m ℝ :=
  V*U*V.transpose+(1-V*V.transpose)

theorem lift_on_frame (V : Matrix m n ℝ) (U : Matrix n n ℝ)
    (hV : V.transpose*V=1) : lift V U * V = V*U := by
  simp [lift, Matrix.add_mul, Matrix.sub_mul, Matrix.mul_assoc, hV]

theorem lift_composition (V : Matrix m n ℝ) (U T : Matrix n n ℝ)
    (hV : V.transpose*V=1) : lift V U * lift V T = lift V (U*T) := by
  have hc (X : Matrix n m ℝ) : V.transpose*(V*X)=X := by
    rw [← Matrix.mul_assoc, hV, Matrix.one_mul]
  simp only [lift, Matrix.add_mul, Matrix.mul_add, Matrix.sub_mul,
    Matrix.mul_sub, Matrix.mul_one, Matrix.one_mul, Matrix.mul_assoc, hc]
  abel

theorem whole_lift_orthogonal (V : Matrix m n ℝ) (U : Matrix n n ℝ)
    (hV : V.transpose*V=1) (hU : U.transpose*U=1) :
    (lift V U).transpose * lift V U = 1 := by
  have ht : (lift V U).transpose = lift V U.transpose := by
    simp [lift, Matrix.transpose_add, Matrix.transpose_sub, Matrix.transpose_mul,
      Matrix.mul_assoc]
  rw [ht, lift_composition V U.transpose U hV, hU]
  simp [lift]

omit [DecidableEq m] in
theorem full_cut_idempotent (V : Matrix m n ℝ) (P : Matrix n n ℝ)
    (hV : V.transpose*V=1) (hP : P*P=P) :
    (V*P*V.transpose)*(V*P*V.transpose)=V*P*V.transpose := by
  have hc (X : Matrix n m ℝ) : V.transpose*(V*X)=X := by
    rw [← Matrix.mul_assoc, hV, Matrix.one_mul]
  calc
    _ = V*(P*P)*V.transpose := by simp [Matrix.mul_assoc, hc]
    _ = _ := by rw [hP]

theorem passive_has_no_detail (J : Matrix m n ℝ) (W : Matrix m m ℝ)
    (U : Matrix n n ℝ) (hJ : J.transpose*J=1) (h : W*J=J*U) :
    (1-J*J.transpose)*W*J=0 := by
  rw [Matrix.mul_assoc, h]
  have hc : J.transpose*(J*U)=U := by
    rw [← Matrix.mul_assoc, hJ, Matrix.one_mul]
  simp [Matrix.sub_mul, Matrix.mul_assoc, hc]

theorem fixed_space_obstruction (k : ℕ) (hk : k<8)
    (F : (Fin 8 → ℝ) →ₗ[ℝ] (Fin k → ℝ)) : ¬ Function.Injective F := by
  intro hf
  have h := LinearMap.finrank_le_finrank_of_injective hf
  simp only [Module.finrank_pi, Fintype.card_fin] at h
  omega

theorem actual_first_fixed_dimensions :
    (1^2+0^2+0^2+1^2 : ℕ)<8 ∧
    (1^2+1^2+1^2+0^2 : ℕ)<8 ∧
    (2^2+1^2+1^2+1^2 : ℕ)<8 ∧
    (3^2+2^2+2^2+1^2 : ℕ)=18 := by norm_num

theorem inherited_frame_norms (p : ℝ) (hp : p+p^2=1) :
    3*p^3+2*p^4=1 ∧ 2*p^2+p^3=1 := by
  constructor
  · linear_combination (2*p^2+p+1)*hp
  · linear_combination (p+1)*hp

theorem regular_multiplicities (A B : ℝ) :
    A*(13*A+8*B)+B*(8*A+5*B)=(3*A+2*B)^2+(2*A+B)^2 := by ring

theorem vieta_implies_both_quadratics (x y : ℝ)
    (hA : x+y=1) (hB : x*y = -1) : x^2=x+1 ∧ y^2=y+1 := by
  constructor
  · linear_combination x*hA-hB
  · linear_combination y*hA-hB

theorem delta_corner_and_feedback (p : ℝ) (hp : p+p^2=1) :
    p^6=4*(delta p)^2 ∧ 4*p^3=8*delta p := by
  have hd := twice_delta p hp
  constructor
  · calc
      p^6 = (p^3)^2 := by ring
      _ = 4*(delta p)^2 := by rw [← hd]; ring
  · linarith

theorem cube_normalization (p : ℝ) (hp : p+p^2=1) :
    (2*delta p)*(1+p)^3=1 := by
  rw [twice_delta p hp]
  linear_combination (p^4+2*p^3+2*p^2+p+1)*hp

theorem tensor_feedback_scalar (x y : ℝ) :
    1-(1-x)*(1-y)=x+(1-x)*y := by ring

/-- A normalized cyclic trace cannot increase a corner probability through
unitary left multiplication. The trace hypothesis is explicit, not derived. -/
theorem tracial_corner_unchanged (tau : Matrix n n ℝ → ℝ)
    (htrace : ∀ A B, tau (A*B)=tau (B*A))
    (U e : Matrix n n ℝ) (hU : U*U.transpose=1) :
    tau (U.transpose*e*U)=tau e := by
  rw [htrace (U.transpose*e) U, ← Matrix.mul_assoc, hU, Matrix.one_mul]

end
end D0.Research.FibonacciRecordActivation

#print axioms D0.Research.FibonacciRecordActivation.lift_on_frame
#print axioms D0.Research.FibonacciRecordActivation.lift_composition
#print axioms D0.Research.FibonacciRecordActivation.whole_lift_orthogonal
#print axioms D0.Research.FibonacciRecordActivation.full_cut_idempotent
#print axioms D0.Research.FibonacciRecordActivation.passive_has_no_detail
#print axioms D0.Research.FibonacciRecordActivation.fixed_space_obstruction
#print axioms D0.Research.FibonacciRecordActivation.actual_first_fixed_dimensions
#print axioms D0.Research.FibonacciRecordActivation.inherited_frame_norms
#print axioms D0.Research.FibonacciRecordActivation.regular_multiplicities
#print axioms D0.Research.FibonacciRecordActivation.vieta_implies_both_quadratics
#print axioms D0.Research.FibonacciRecordActivation.delta_corner_and_feedback
#print axioms D0.Research.FibonacciRecordActivation.cube_normalization
#print axioms D0.Research.FibonacciRecordActivation.tensor_feedback_scalar
#print axioms D0.Research.FibonacciRecordActivation.tracial_corner_unchanged
#print axioms D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
