import D0.Core.Phi
import D0.Representation.GoldenCoherentMemory
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic

namespace D0.Research.NativeConstrainedPriceSource
open Matrix
noncomputable section
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
variable {n : Type*} [Fintype n] [DecidableEq n]
abbrev Mat (n : Type*) := Matrix n n ℝ

def fp (A B : Mat n) : ℝ := (A.transpose * B).trace

def sym (A : Mat n) : Mat n := (1/2:ℝ) • (A + A.transpose)
def skew (A : Mat n) : Mat n := (1/2:ℝ) • (A - A.transpose)

theorem fp_add_left (A B C : Mat n) : fp (A+B) C=fp A C+fp B C := by
  simp [fp,Matrix.add_mul]
theorem fp_add_right (A B C : Mat n) : fp A (B+C)=fp A B+fp A C := by
  simp [fp,Matrix.mul_add]
theorem fp_sub_left (A B C : Mat n) : fp (A-B) C=fp A C-fp B C := by
  simp [fp,Matrix.sub_mul]
theorem fp_sub_right (A B C : Mat n) : fp A (B-C)=fp A B-fp A C := by
  simp [fp,Matrix.mul_sub]
theorem fp_smul_left (c : ℝ) (A B : Mat n) : fp (c • A) B=c*fp A B := by
  simp [fp,Matrix.smul_mul]
theorem fp_smul_right (c : ℝ) (A B : Mat n) : fp A (c • B)=c*fp A B := by
  simp [fp,Matrix.mul_smul]

theorem trace_skew_zero (K : Mat n) (hK : K.transpose = -K) : K.trace=0 := by
  have h := Matrix.trace_transpose K
  rw [hK,Matrix.trace_neg] at h
  linarith

theorem trace_symmetric_skew_zero (A K : Mat n)
    (hA : A.transpose=A) (hK : K.transpose = -K) : (A*K).trace=0 := by
  have h := Matrix.trace_transpose (A*K)
  rw [Matrix.transpose_mul,hA,hK,Matrix.neg_mul,Matrix.trace_neg,
    Matrix.trace_mul_comm] at h
  linarith

theorem fp_symmetric_probe (A V : Mat n) (hV : V.transpose=V) :
    fp A V=fp (sym A) V := by
  have hh : (A*V).trace=(A.transpose*V).trace := by
    have h := Matrix.trace_transpose (A*V)
    rw [Matrix.transpose_mul,hV,Matrix.trace_mul_comm] at h
    exact h.symm
  simp [fp,sym,Matrix.add_mul,Matrix.smul_mul,hh]
  ring

theorem symmetric_involution_tangent_is_skew (H dH : Mat n)
    (hH : H.transpose=H)
    (hj : dH.transpose*H+H.transpose*dH=0) :
    (H*dH).transpose=-(H*dH) := by
  rw [Matrix.transpose_mul,hH]
  rw [hH] at hj
  exact eq_neg_of_add_eq_zero_left hj

theorem involution_tangent_trace_zero (H dH : Mat n)
    (hH : H.transpose=H) (hHH : H*H=1)
    (hj : dH.transpose*H+H.transpose*dH=0) :
    dH.trace=0 ∧ (H*dH).trace=0 := by
  have hk := symmetric_involution_tangent_is_skew H dH hH hj
  have hd : H*(H*dH)=dH := by rw [←Matrix.mul_assoc,hHH,Matrix.one_mul]
  constructor
  · simpa only [hd] using trace_symmetric_skew_zero H (H*dH) hH hk
  · exact trace_skew_zero (H*dH) hk

theorem two_tick_resolvent_pairing_zero (H dH : Mat n) (a b : ℝ)
    (hH : H.transpose=H) (hHH : H*H=1)
    (hj : dH.transpose*H+H.transpose*dH=0) :
    ((a • (1 : Mat n)+b • H)*(dH+dH.transpose)).trace=0 := by
  obtain ⟨htr,htrH⟩ := involution_tangent_trace_zero H dH hH hHH hj
  have ht : (H*dH.transpose).trace=(H*dH).trace := by
    have h := Matrix.trace_transpose (H*dH.transpose)
    rw [Matrix.transpose_mul,Matrix.transpose_transpose,hH,Matrix.trace_mul_comm] at h
    exact h.symm
  simp [Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,htr,htrH,ht]

theorem involution_polynomial_mul (H : Mat n) (a b c d : ℝ) (hH : H*H=1) :
    (a • (1 : Mat n)+b • H)*(c • (1 : Mat n)+d • H)=
      (a*c+b*d) • (1 : Mat n)+(a*d+b*c) • H := by
  simp only [Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,Matrix.mul_smul,
    Matrix.one_mul,Matrix.mul_one,hH,smul_smul]
  module

def involutionResolvent (H : Mat n) (c : ℝ) : Mat n :=
  ((1-c)/(1-2*c)) • 1 + (c/(1-2*c)) • H

theorem involution_resolvent_inverse (H : Mat n) (c : ℝ)
    (hH : H*H=1) (hc : 1-2*c≠0) :
    ((1-c) • (1 : Mat n)+(-c) • H)*involutionResolvent H c=1 := by
  unfold involutionResolvent
  rw [involution_polynomial_mul H _ _ _ _ hH]
  have h1 : (1-c)*((1-c)/(1-2*c))+(-c)*(c/(1-2*c))=1 := by
    calc
      _ = ((1-c)*(1-c)-c*c)/(1-2*c) := by ring
      _ = (1-2*c)/(1-2*c) := by congr 1; ring
      _ = 1 := div_self hc
  have h0 : (1-c)*(c/(1-2*c))+(-c)*((1-c)/(1-2*c))=0 := by ring
  rw [h1,h0]; simp

variable {m : Type*} [Fintype m] [DecidableEq m]

theorem relative_isometry_first_jet (R dR dS : Matrix m n ℝ) (H : Mat n)
    (hR : dR.transpose*R+R.transpose*dR=0)
    (hS : dS.transpose*(R*H)+(R*H).transpose*dS=0) :
    (dR.transpose*(R*H)+R.transpose*dS).transpose*H+
      H.transpose*(dR.transpose*(R*H)+R.transpose*dS)=0 := by
  have he : (dR.transpose*(R*H)+R.transpose*dS).transpose*H+
      H.transpose*(dR.transpose*(R*H)+R.transpose*dS)=
      H.transpose*(dR.transpose*R+R.transpose*dR)*H+
        (dS.transpose*(R*H)+(R*H).transpose*dS) := by
    simp only [Matrix.transpose_add,Matrix.transpose_mul,Matrix.transpose_transpose,
      Matrix.mul_add,Matrix.add_mul,Matrix.mul_assoc]
    abel
  rw [he,hR,hS]; simp


def retained (a p : ℝ) (H : Mat n) : Mat n := a^2 • 1-p^2 • H

def retainedJet (p : ℝ) (dH : Mat n) : Mat n := -(p^2) • dH

def feedbackJet (A dA : Mat n) : Mat n := -(dA.transpose*A+A.transpose*dA)

theorem feedback_jet_expansion (a p : ℝ) (H dH : Mat n) :
    feedbackJet (retained a p H) (retainedJet p dH) =
      (a^2*p^2) • (dH+dH.transpose) -
      p^4 • (dH.transpose*H+H.transpose*dH) := by
  simp only [feedbackJet,retained,retainedJet,Matrix.transpose_sub,
    Matrix.transpose_smul,Matrix.transpose_one,Matrix.add_mul,Matrix.mul_add,
    Matrix.sub_mul,Matrix.mul_sub,Matrix.smul_mul,Matrix.mul_smul,
    Matrix.one_mul,Matrix.mul_one]
  module

theorem golden_feedback_jet (a p : ℝ) (H dH : Mat n)
    (ha : a^2=p) (hj : dH.transpose*H+H.transpose*dH=0) :
    feedbackJet (retained a p H) (retainedJet p dH)=p^3 • (dH+dH.transpose) := by
  rw [feedback_jet_expansion,ha,hj,smul_zero,sub_zero]
  congr 1
  ring

theorem golden_involution_feedback (a p : ℝ) (H : Mat n)
    (ha : a^2=p) (hp : p+p^2=1) (hH : H.transpose=H) (hHH : H*H=1) :
    1-(retained a p H).transpose*retained a p H=(2*p^3) • (1+H) := by
  have hp3 : p^2+p^3=p := by nlinarith [congrArg (fun x : ℝ => p*x) hp]
  have hp4 : p^3+p^4=p^2 := by nlinarith [congrArg (fun x : ℝ => p^2*x) hp]
  have hscalar : 1-p^2-p^4=2*p^3 := by linarith
  simp only [retained,ha,Matrix.transpose_sub,Matrix.transpose_smul,
    Matrix.transpose_one,hH,Matrix.sub_mul,Matrix.mul_sub,Matrix.smul_mul,
    Matrix.mul_smul,Matrix.one_mul,Matrix.mul_one,hHH]
  linear_combination (norm := module) hscalar • (1 : Mat n)

theorem full_archive_two_tick_jacobi_zero (R dR dS : Matrix m n ℝ)
    (H : Mat n) (a p z : ℝ)
    (hR : dR.transpose*R+R.transpose*dR=0)
    (hS : dS.transpose*(R*H)+(R*H).transpose*dS=0)
    (hH : H.transpose=H) (hHH : H*H=1) (ha : a^2=p) :
    z*(involutionResolvent H (2*z*p^3) *
      feedbackJet (retained a p H)
        (retainedJet p (dR.transpose*(R*H)+R.transpose*dS))).trace=0 := by
  have hj := relative_isometry_first_jet R dR dS H hR hS
  rw [golden_feedback_jet a p H _ ha hj]
  unfold involutionResolvent
  rw [Matrix.mul_smul,Matrix.trace_smul,
    two_tick_resolvent_pairing_zero H _ _ _ hH hHH hj]
  simp

/-- A differential that is zero on the full declared operator tangent stays
zero after any native first-jet map into that tangent; no metric fit is used. -/
theorem zero_differential_pullback {E F : Type*} [AddCommGroup E] [Module ℝ E]
    [AddCommGroup F] [Module ℝ F] (L : F →ₗ[ℝ] ℝ) (J : E →ₗ[ℝ] F)
    (h : ∀ w, L w=0) (v : E) : L (J v)=0 := h (J v)

/-- Trace-cyclic normal form of the actual joint tangent parameterization.
R is instantiated as q_source inverse times D only after the carrier proof. -/
theorem fp_right_product (A Z R : Mat n) : fp A (Z*R)=fp (A*R.transpose) Z := by
  simp only [fp,Matrix.transpose_mul,Matrix.transpose_transpose]
  simpa only [Matrix.mul_assoc] using Matrix.trace_mul_cycle A.transpose Z R

theorem fp_congruence (A D V : Mat n) : fp A (D*V*D.transpose)=fp (D.transpose*A*D) V := by
  simp only [fp,Matrix.transpose_mul,Matrix.transpose_transpose]
  simpa only [Matrix.mul_assoc] using Matrix.trace_mul_cycle (A.transpose*D) V D.transpose

def jointLift (D R Vs Vt K : Mat n) : Mat n :=
  ((1/2:ℝ) • (Vs-D*Vt*D.transpose)+K)*R

theorem intrinsic_source_normal_form (As At B D R Vs Vt K : Mat n) :
    fp As Vs+fp At Vt+fp B (jointLift D R Vs Vt K) =
      fp (As+(1/2:ℝ) • (B*R.transpose)) Vs+
      fp (At-(1/2:ℝ) • (D.transpose*(B*R.transpose)*D)) Vt+
      fp (B*R.transpose) K := by
  rw [jointLift,fp_right_product,fp_add_right,fp_smul_right,fp_sub_right,fp_congruence]
  simp only [fp_add_left,fp_sub_left,fp_smul_left]
  ring

/-- Conormal changes are evaluated on the entire joint constraint jet. -/
theorem conormal_restriction_zero (Λ qt D Vs Vt W : Mat n)
    (hj : D*Vt*D.transpose+W*qt*D.transpose+D*qt*W.transpose-Vs=0) :
    fp Λ (D*Vt*D.transpose+W*qt*D.transpose+D*qt*W.transpose-Vs)=0 := by
  rw [hj]; simp [fp]


def swapBit : Mat (Fin 2) := !![0,1;1,0]

theorem swapBit_symmetric : swapBit.transpose=swapBit := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [swapBit]

theorem swapBit_involution : swapBit*swapBit=1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [swapBit,Matrix.mul_apply,Fin.sum_univ_succ]

def jointStep (a p : ℝ) (R S : Matrix m n ℝ) (V : Mat m) : Mat (n ⊕ m) :=
  Matrix.fromBlocks (a • 1) ((-p) • R.transpose) (p • S) (a • (S*R.transpose)+V)

theorem full_archive_retained_binding (a p : ℝ) (R S : Matrix m n ℝ) (V : Mat m) :
    ((jointStep a p R S V)*(jointStep a p R S V)).toBlocks₁₁=retained a p (R.transpose*S) := by
  simp [jointStep,retained,Matrix.fromBlocks_multiply,Matrix.smul_mul,Matrix.mul_smul,pow_two]
  module

theorem recorded_gate_owned_binding (a p : ℝ) :
    (D0.Representation.GoldenCoherentMemory.fullStep a p).submatrix
      finSumFinEquiv finSumFinEquiv = jointStep a p (1 : Mat (Fin 2)) swapBit 0 := by
  ext i j
  rcases i with i|i <;> rcases j with j|j <;>
    fin_cases i <;> fin_cases j <;>
    simp [D0.Representation.GoldenCoherentMemory.fullStep,jointStep,swapBit,
      Matrix.submatrix,finSumFinEquiv,Matrix.fromBlocks]

theorem recorded_full_archive_jacobi_zero (R dR dS : Matrix m (Fin 2) ℝ)
    (a p z : ℝ) (ha : a^2=p)
    (hR : dR.transpose*R+R.transpose*dR=0)
    (hS : dS.transpose*(R*swapBit)+(R*swapBit).transpose*dS=0) :
    z*(involutionResolvent swapBit (2*z*p^3) *
      feedbackJet (retained a p swapBit)
        (retainedJet p (dR.transpose*(R*swapBit)+R.transpose*dS))).trace=0 :=
  full_archive_two_tick_jacobi_zero R dR dS swapBit a p z hR hS
    swapBit_symmetric swapBit_involution ha

/-- The ordinary golden operation has H = identity at every active size. -/
theorem direct_full_archive_jacobi_zero (R dR dS : Matrix m n ℝ)
    (a p z : ℝ) (ha : a^2=p)
    (hR : dR.transpose*R+R.transpose*dR=0)
    (hS : dS.transpose*R+R.transpose*dS=0) :
    z*(involutionResolvent (1 : Mat n) (2*z*p^3) *
      feedbackJet (retained a p (1 : Mat n))
        (retainedJet p (dR.transpose*R+R.transpose*dS))).trace=0 := by
  simpa only [Matrix.mul_one] using
    full_archive_two_tick_jacobi_zero R dR dS (1 : Mat n) a p z hR
      (by simpa only [Matrix.mul_one] using hS) (by simp) (by simp) ha


/-- The entire second-step active feedback, including every archive row. -/
theorem orthogonal_feedback_retained_identity (U : Mat (n ⊕ m))
    (hU : U.transpose*U=1) :
    U.toBlocks₂₁.transpose*U.toBlocks₂₁=1-U.toBlocks₁₁.transpose*U.toBlocks₁₁ := by
  have hu : (Matrix.fromBlocks U.toBlocks₁₁ U.toBlocks₁₂ U.toBlocks₂₁ U.toBlocks₂₂).transpose*
      Matrix.fromBlocks U.toBlocks₁₁ U.toBlocks₁₂ U.toBlocks₂₁ U.toBlocks₂₂=1 := by
    simpa only [Matrix.fromBlocks_toBlocks] using hU
  rw [Matrix.fromBlocks_transpose,Matrix.fromBlocks_multiply,
    ←Matrix.fromBlocks_one (l:=n) (m:=m)] at hu
  have hh := (Matrix.fromBlocks_inj.mp hu).1
  rw [←hh]
  abel

theorem orthogonal_composition_self (U : Mat n) (hU : U.transpose*U=1) :
    (U*U).transpose*(U*U)=1 := by
  calc
    _ = U.transpose*(U.transpose*U)*U := by simp only [Matrix.transpose_mul,Matrix.mul_assoc]
    _ = 1 := by rw [hU,Matrix.mul_one,hU]

theorem full_archive_feedback_binding (a p : ℝ) (R S : Matrix m n ℝ) (V : Mat m)
    (hU : (jointStep a p R S V).transpose*jointStep a p R S V=1) :
    ((jointStep a p R S V)*(jointStep a p R S V)).toBlocks₂₁.transpose*
      ((jointStep a p R S V)*(jointStep a p R S V)).toBlocks₂₁ =
      1-(retained a p (R.transpose*S)).transpose*retained a p (R.transpose*S) := by
  rw [orthogonal_feedback_retained_identity _ (orthogonal_composition_self _ hU),
    full_archive_retained_binding]

end
end D0.Research.NativeConstrainedPriceSource

/- Actual proposition and transitive-axiom diagnostics; no general analytic Jacobi theorem is imported as an axiom. -/
#check D0.Research.NativeConstrainedPriceSource.fp_add_left
#print axioms D0.Research.NativeConstrainedPriceSource.fp_add_left
#check D0.Research.NativeConstrainedPriceSource.fp_add_right
#print axioms D0.Research.NativeConstrainedPriceSource.fp_add_right
#check D0.Research.NativeConstrainedPriceSource.fp_sub_left
#print axioms D0.Research.NativeConstrainedPriceSource.fp_sub_left
#check D0.Research.NativeConstrainedPriceSource.fp_sub_right
#print axioms D0.Research.NativeConstrainedPriceSource.fp_sub_right
#check D0.Research.NativeConstrainedPriceSource.fp_smul_left
#print axioms D0.Research.NativeConstrainedPriceSource.fp_smul_left
#check D0.Research.NativeConstrainedPriceSource.fp_smul_right
#print axioms D0.Research.NativeConstrainedPriceSource.fp_smul_right
#check D0.Research.NativeConstrainedPriceSource.trace_skew_zero
#print axioms D0.Research.NativeConstrainedPriceSource.trace_skew_zero
#check D0.Research.NativeConstrainedPriceSource.trace_symmetric_skew_zero
#print axioms D0.Research.NativeConstrainedPriceSource.trace_symmetric_skew_zero
#check D0.Research.NativeConstrainedPriceSource.fp_symmetric_probe
#print axioms D0.Research.NativeConstrainedPriceSource.fp_symmetric_probe
#check D0.Research.NativeConstrainedPriceSource.symmetric_involution_tangent_is_skew
#print axioms D0.Research.NativeConstrainedPriceSource.symmetric_involution_tangent_is_skew
#check D0.Research.NativeConstrainedPriceSource.involution_tangent_trace_zero
#print axioms D0.Research.NativeConstrainedPriceSource.involution_tangent_trace_zero
#check D0.Research.NativeConstrainedPriceSource.two_tick_resolvent_pairing_zero
#print axioms D0.Research.NativeConstrainedPriceSource.two_tick_resolvent_pairing_zero
#check D0.Research.NativeConstrainedPriceSource.involution_polynomial_mul
#print axioms D0.Research.NativeConstrainedPriceSource.involution_polynomial_mul
#check D0.Research.NativeConstrainedPriceSource.involution_resolvent_inverse
#print axioms D0.Research.NativeConstrainedPriceSource.involution_resolvent_inverse
#check D0.Research.NativeConstrainedPriceSource.relative_isometry_first_jet
#print axioms D0.Research.NativeConstrainedPriceSource.relative_isometry_first_jet
#check D0.Research.NativeConstrainedPriceSource.feedback_jet_expansion
#print axioms D0.Research.NativeConstrainedPriceSource.feedback_jet_expansion
#check D0.Research.NativeConstrainedPriceSource.golden_feedback_jet
#print axioms D0.Research.NativeConstrainedPriceSource.golden_feedback_jet
#check D0.Research.NativeConstrainedPriceSource.golden_involution_feedback
#print axioms D0.Research.NativeConstrainedPriceSource.golden_involution_feedback
#check D0.Research.NativeConstrainedPriceSource.full_archive_two_tick_jacobi_zero
#print axioms D0.Research.NativeConstrainedPriceSource.full_archive_two_tick_jacobi_zero
#check D0.Research.NativeConstrainedPriceSource.zero_differential_pullback
#print axioms D0.Research.NativeConstrainedPriceSource.zero_differential_pullback
#check D0.Research.NativeConstrainedPriceSource.fp_right_product
#print axioms D0.Research.NativeConstrainedPriceSource.fp_right_product
#check D0.Research.NativeConstrainedPriceSource.fp_congruence
#print axioms D0.Research.NativeConstrainedPriceSource.fp_congruence
#check D0.Research.NativeConstrainedPriceSource.intrinsic_source_normal_form
#print axioms D0.Research.NativeConstrainedPriceSource.intrinsic_source_normal_form
#check D0.Research.NativeConstrainedPriceSource.conormal_restriction_zero
#print axioms D0.Research.NativeConstrainedPriceSource.conormal_restriction_zero
#check D0.Research.NativeConstrainedPriceSource.swapBit_symmetric
#print axioms D0.Research.NativeConstrainedPriceSource.swapBit_symmetric
#check D0.Research.NativeConstrainedPriceSource.swapBit_involution
#print axioms D0.Research.NativeConstrainedPriceSource.swapBit_involution
#check D0.Research.NativeConstrainedPriceSource.full_archive_retained_binding
#print axioms D0.Research.NativeConstrainedPriceSource.full_archive_retained_binding
#check D0.Research.NativeConstrainedPriceSource.recorded_gate_owned_binding
#print axioms D0.Research.NativeConstrainedPriceSource.recorded_gate_owned_binding
#check D0.Research.NativeConstrainedPriceSource.recorded_full_archive_jacobi_zero
#print axioms D0.Research.NativeConstrainedPriceSource.recorded_full_archive_jacobi_zero
#check D0.Research.NativeConstrainedPriceSource.direct_full_archive_jacobi_zero
#print axioms D0.Research.NativeConstrainedPriceSource.direct_full_archive_jacobi_zero
#check D0.Research.NativeConstrainedPriceSource.orthogonal_feedback_retained_identity
#print axioms D0.Research.NativeConstrainedPriceSource.orthogonal_feedback_retained_identity
#check D0.Research.NativeConstrainedPriceSource.orthogonal_composition_self
#print axioms D0.Research.NativeConstrainedPriceSource.orthogonal_composition_self
#check D0.Research.NativeConstrainedPriceSource.full_archive_feedback_binding
#print axioms D0.Research.NativeConstrainedPriceSource.full_archive_feedback_binding
