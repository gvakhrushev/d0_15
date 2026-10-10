import D0.Representation.GoldenCoherentMemory
import D0.Representation.FiniteProtocolClock
import D0.Synthesis.SceneHeatKernel
import D0.Representation.SourcePortPreparation
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Data.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-! Joint golden completions and the existing feedback action on composed histories.
No differential equation or physical variation is supplied by a matrix parameter. -/
namespace D0.Research.NativeComposedFeedbackDynamics
noncomputable section
open Matrix

section JointCompletion
variable {n m : Type*} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]

def archiveBlock (a : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ) : Matrix m m ℝ :=
  a • (S*R.transpose)+V

def joint (a p : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ) :
    Matrix (n ⊕ m) (n ⊕ m) ℝ :=
  fromBlocks (a • 1) ((-p) • R.transpose) (p • S) (archiveBlock a R S V)

theorem archive_on_incoming (a : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (hR : R.transpose*R=1) (hV : V*R=0) :
    archiveBlock a R S V * R = a • S := by
  simp [archiveBlock,Matrix.add_mul,Matrix.smul_mul,Matrix.mul_assoc,hR,hV]

theorem archive_transpose_on_outgoing (a : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (hS : S.transpose*S=1) (hV : S.transpose*V=0) :
    (archiveBlock a R S V).transpose*S = a • R := by
  have hv : V.transpose*S=0 := by
    simpa using congrArg Matrix.transpose hV
  simp [archiveBlock,Matrix.add_mul,Matrix.smul_mul,Matrix.mul_assoc,hS,hv]

theorem archive_left_gram (a : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (hS : S.transpose*S=1) (hSV : S.transpose*V=0) :
    (archiveBlock a R S V).transpose*archiveBlock a R S V =
      a^2 • (R*R.transpose)+V.transpose*V := by
  have hd := archive_transpose_on_outgoing a R S V hS hSV
  have hv : (archiveBlock a R S V).transpose*V=V.transpose*V := by
    simp [archiveBlock,Matrix.add_mul,Matrix.smul_mul,Matrix.mul_assoc,hSV]
  calc
    (archiveBlock a R S V).transpose*archiveBlock a R S V =
      a • (((archiveBlock a R S V).transpose*S)*R.transpose)+
        (archiveBlock a R S V).transpose*V := by
          simp only [archiveBlock,Matrix.mul_add,Matrix.mul_smul,Matrix.mul_assoc]
    _ = a^2 • (R*R.transpose)+V.transpose*V := by
      rw [hd,hv,Matrix.smul_mul,smul_smul,pow_two]

theorem archive_right_gram (a : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (hR : R.transpose*R=1) (hVR : V*R=0) :
    archiveBlock a R S V*(archiveBlock a R S V).transpose =
      a^2 • (S*S.transpose)+V*V.transpose := by
  have hd := archive_on_incoming a R S V hR hVR
  have hv : archiveBlock a R S V*V.transpose=V*V.transpose := by
    have hrv : R.transpose*V.transpose=0 := by
      simpa using congrArg Matrix.transpose hVR
    simp [archiveBlock,Matrix.add_mul,Matrix.smul_mul,Matrix.mul_assoc,hrv]
  calc
    archiveBlock a R S V*(archiveBlock a R S V).transpose =
      a • ((archiveBlock a R S V*R)*S.transpose)+archiveBlock a R S V*V.transpose := by
        simp only [archiveBlock,Matrix.transpose_add,Matrix.transpose_smul,
          Matrix.transpose_mul,Matrix.transpose_transpose,Matrix.mul_add,
          Matrix.mul_smul,Matrix.mul_assoc]
    _ = a^2 • (S*S.transpose)+V*V.transpose := by
      rw [hd,hv,Matrix.smul_mul,smul_smul,pow_two]

/-- The entire initial-archive complement is retained by a partial orthogonal map. -/
theorem joint_left_orthogonal (a p : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (h : a^2+p^2=1) (hS : S.transpose*S=1) (hSV : S.transpose*V=0)
    (hVV : V.transpose*V=1-R*R.transpose) :
    (joint a p R S V).transpose*joint a p R S V=1 := by
  have hd := archive_transpose_on_outgoing a R S V hS hSV
  have hd' : S.transpose*archiveBlock a R S V=a • R.transpose := by
    simpa using congrArg Matrix.transpose hd
  have hg := archive_left_gram a R S V hS hSV
  rw [joint,Matrix.fromBlocks_transpose,Matrix.fromBlocks_multiply,
    ← Matrix.fromBlocks_one (l:=n) (m:=m)]
  apply Matrix.fromBlocks_inj.mpr
  refine ⟨?_,?_,?_,?_⟩
  · simp only [Matrix.transpose_smul,Matrix.transpose_one,Matrix.smul_mul,
      Matrix.mul_smul,Matrix.one_mul,smul_smul,hS]
    rw [← add_smul,← pow_two,← pow_two,h,one_smul]
  · simp only [Matrix.transpose_smul,Matrix.transpose_one,Matrix.smul_mul,
      Matrix.mul_smul,Matrix.one_mul,smul_smul,hd']
    module
  · simp only [Matrix.transpose_smul,Matrix.transpose_transpose,Matrix.smul_mul,
      Matrix.mul_smul,Matrix.mul_one,smul_smul,hd]
    module
  · simp only [Matrix.transpose_smul,Matrix.transpose_transpose,Matrix.smul_mul,
      Matrix.mul_smul,smul_smul,hg,hVV]
    have hp : (-p)*(-p)=p^2 := by ring
    rw [hp]
    calc
      p^2 • (R*R.transpose)+(a^2 • (R*R.transpose)+(1-R*R.transpose)) =
        (a^2+p^2) • (R*R.transpose)+(1-R*R.transpose) := by module
      _ = 1 := by rw [h,one_smul]; abel

/-- Extract every coupled equation, not only a retained norm check. -/
theorem full_left_block_equations (A : Matrix n n ℝ) (B : Matrix n m ℝ)
    (C : Matrix m n ℝ) (D : Matrix m m ℝ)
    (hU : (fromBlocks A B C D).transpose*fromBlocks A B C D=1) :
    A.transpose*A+C.transpose*C=1 ∧ A.transpose*B+C.transpose*D=0 ∧
    B.transpose*A+D.transpose*C=0 ∧ B.transpose*B+D.transpose*D=1 := by
  rw [Matrix.fromBlocks_transpose,Matrix.fromBlocks_multiply,
    ← Matrix.fromBlocks_one (l:=n) (m:=m)] at hU
  exact Matrix.fromBlocks_inj.mp hU

/-- The normalized parameters exhaust all real blocks when p is nonzero. -/
theorem reconstruct_all_raw_blocks (a p : ℝ) (hp : p≠0)
    (B : Matrix n m ℝ) (C : Matrix m n ℝ) (D : Matrix m m ℝ) :
    joint a p (((-p)⁻¹) • B.transpose) (p⁻¹ • C)
      (D-a • ((p⁻¹ • C)*(((-p)⁻¹) • B.transpose).transpose)) =
      fromBlocks (a • 1) B C D := by
  unfold joint archiveBlock
  congr 1
  · simp [smul_smul,hp]
  · simp [smul_smul,hp]
  · abel

/-- Complete all-archive left-orthogonality criterion for the normalized family. -/
theorem joint_orthogonality_iff (a p : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (h : a^2+p^2=1) (hp : p≠0) :
    (joint a p R S V).transpose*joint a p R S V=1 ↔
      S.transpose*S=1 ∧ S.transpose*V=0 ∧ V.transpose*V=1-R*R.transpose := by
  constructor
  · intro hU
    have blocks := full_left_block_equations (a • 1) ((-p) • R.transpose)
      (p • S) (archiveBlock a R S V) hU
    have gram : a^2 • (1 : Matrix n n ℝ)+p^2 • (S.transpose*S)=1 := by
      simpa [Matrix.smul_mul,Matrix.mul_smul,smul_smul,pow_two] using blocks.1
    have hs0 : p^2 • (S.transpose*S-1)=0 := by
      calc
        p^2 • (S.transpose*S-1) =
          (a^2 • (1 : Matrix n n ℝ)+p^2 • (S.transpose*S))-(a^2+p^2) • 1 := by module
        _ = 0 := by rw [gram,h,one_smul]; simp
    have hs : S.transpose*S=1 :=
      sub_eq_zero.mp ((smul_eq_zero.mp hs0).resolve_left (pow_ne_zero _ hp))
    have cross : (a*(-p)) • R+p • ((archiveBlock a R S V).transpose*S)=0 := by
      simpa [Matrix.smul_mul,Matrix.mul_smul,smul_smul] using blocks.2.2.1
    have hc0 : p • ((archiveBlock a R S V).transpose*S-a • R)=0 := by
      calc
        p • ((archiveBlock a R S V).transpose*S-a • R) =
          (a*(-p)) • R+p • ((archiveBlock a R S V).transpose*S) := by module
        _ = 0 := cross
    have hc : (archiveBlock a R S V).transpose*S=a • R :=
      sub_eq_zero.mp ((smul_eq_zero.mp hc0).resolve_left hp)
    have hsv' : V.transpose*S=0 := by
      have he : (archiveBlock a R S V).transpose*S=a • R+V.transpose*S := by
        simp [archiveBlock,Matrix.add_mul,Matrix.mul_assoc,hs]
      rw [hc] at he
      have hz : a • R+V.transpose*S=a • R+0 := by simpa using he.symm
      exact add_left_cancel hz
    have hsv : S.transpose*V=0 := by simpa using congrArg Matrix.transpose hsv'
    have last : p^2 • (R*R.transpose)+
        (archiveBlock a R S V).transpose*archiveBlock a R S V=1 := by
      simpa [Matrix.smul_mul,Matrix.mul_smul,smul_smul,pow_two] using blocks.2.2.2
    rw [archive_left_gram a R S V hs hsv] at last
    have hlast : (R*R.transpose)+V.transpose*V=1 := by
      calc
        (R*R.transpose)+V.transpose*V = (a^2+p^2) • (R*R.transpose)+V.transpose*V := by rw [h,one_smul]
        _ = p^2 • (R*R.transpose)+(a^2 • (R*R.transpose)+V.transpose*V) := by module
        _ = 1 := last
    exact ⟨hs,hsv,by rw [← hlast]; abel⟩
  · rintro ⟨hS,hSV,hVV⟩
    exact joint_left_orthogonal a p R S V h hS hSV hVV

theorem joint_transpose (a p : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ) :
    (joint a p R S V).transpose=joint a (-p) S R V.transpose := by
  simp [joint,archiveBlock,Matrix.fromBlocks_transpose]

theorem joint_right_orthogonal (a p : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (hU : (joint a p R S V).transpose*joint a p R S V=1) :
    joint a p R S V*(joint a p R S V).transpose=1 :=
  mul_eq_one_comm.mp hU

theorem all_archive_completion_constraints (a p : ℝ)
    (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (h : a^2+p^2=1) (hp : p≠0)
    (hU : (joint a p R S V).transpose*joint a p R S V=1) :
    R.transpose*R=1 ∧ S.transpose*S=1 ∧ V*R=0 ∧ S.transpose*V=0 ∧
      V.transpose*V=1-R*R.transpose ∧ V*V.transpose=1-S*S.transpose := by
  have h₁ := (joint_orthogonality_iff a p R S V h hp).mp hU
  have h₂ : (joint a (-p) S R V.transpose).transpose*joint a (-p) S R V.transpose=1 := by
    rw [← joint_transpose,Matrix.transpose_transpose]
    exact joint_right_orthogonal a p R S V hU
  have hn : a^2+(-p)^2=1 := by simpa using h
  have h₃ := (joint_orthogonality_iff a (-p) S R V.transpose hn (neg_ne_zero.mpr hp)).mp h₂
  refine ⟨h₃.1,h₁.1,?_,h₁.2.1,h₁.2.2,?_⟩
  · simpa using congrArg Matrix.transpose h₃.2.1
  · simpa using h₃.2.2

theorem archive_embedding_injective (S : Matrix m n ℝ) (hS : S.transpose*S=1) :
    Function.Injective S.mulVec := by
  have left : Function.LeftInverse S.transpose.mulVec S.mulVec := by
    intro x
    rw [Matrix.mulVec_mulVec,hS,Matrix.one_mulVec]
  exact left.injective

def activeFeedback (U : Matrix (n ⊕ m) (n ⊕ m) ℝ) : Matrix n n ℝ :=
  U.toBlocks₂₁.transpose*U.toBlocks₂₁

/-- Exact binding to P U^T Q U P on the declared active/archive split. -/
theorem feedback_owner_binding (A : Matrix n n ℝ) (B : Matrix n m ℝ)
    (C : Matrix m n ℝ) (D : Matrix m m ℝ) :
    fromBlocks (1 : Matrix n n ℝ) 0 0 (0 : Matrix m m ℝ) *
      (fromBlocks A B C D).transpose *
      fromBlocks (0 : Matrix n n ℝ) 0 0 (1 : Matrix m m ℝ) *
      fromBlocks A B C D * fromBlocks (1 : Matrix n n ℝ) 0 0 (0 : Matrix m m ℝ) =
        fromBlocks (activeFeedback (fromBlocks A B C D)) 0 0 (0 : Matrix m m ℝ) := by
  simp [activeFeedback,Matrix.fromBlocks_transpose,Matrix.fromBlocks_multiply]

theorem one_return_feedback (a p : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ)
    (hS : S.transpose*S=1) : activeFeedback (joint a p R S V)=p^2 • 1 := by
  simp [activeFeedback,joint,Matrix.smul_mul,Matrix.mul_smul,smul_smul,hS,pow_two]

theorem joint_two_step_retained (a p : ℝ) (R S : Matrix m n ℝ) (V : Matrix m m ℝ) :
    ((joint a p R S V)*(joint a p R S V)).toBlocks₁₁ =
      a^2 • 1-p^2 • (R.transpose*S) := by
  simp [joint,Matrix.fromBlocks_multiply,Matrix.smul_mul,Matrix.mul_smul,smul_smul,pow_two]
  module

theorem feedback_from_retained_block (U : Matrix (n ⊕ m) (n ⊕ m) ℝ)
    (hU : U.transpose*U=1) :
    activeFeedback U=1-U.toBlocks₁₁.transpose*U.toBlocks₁₁ := by
  have blocks := full_left_block_equations U.toBlocks₁₁ U.toBlocks₁₂ U.toBlocks₂₁ U.toBlocks₂₂
    (by simpa only [Matrix.fromBlocks_toBlocks] using hU)
  unfold activeFeedback
  rw [← blocks.1]
  abel

end JointCompletion

section MinimalArchive
variable {n : Type*} [Fintype n] [DecidableEq n]

def minimalJoint (a p : ℝ) (H : Matrix n n ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  fromBlocks (a • 1) ((-p) • 1) (p • H) (a • H)

theorem minimal_is_joint (a p : ℝ) (H : Matrix n n ℝ) :
    minimalJoint a p H=joint a p 1 H 0 := by simp [minimalJoint,joint,archiveBlock]

theorem minimal_orthogonal (a p : ℝ) (H : Matrix n n ℝ)
    (h : a^2+p^2=1) (hH : H.transpose*H=1) :
    (minimalJoint a p H).transpose*minimalJoint a p H=1 := by
  rw [minimal_is_joint]
  exact joint_left_orthogonal a p 1 H 0 h hH (by simp) (by simp)

theorem minimal_archive_tail_zero (a p : ℝ) (R S V : Matrix n n ℝ)
    (h : a^2+p^2=1) (hp : p≠0)
    (hU : (joint a p R S V).transpose*joint a p R S V=1) : V=0 := by
  have full := all_archive_completion_constraints a p R S V h hp hU
  have hr : R*R.transpose=1 := mul_eq_one_comm.mp full.1
  have hvR : V*R=0 := full.2.2.1
  calc V = V*(R*R.transpose) := by rw [hr,Matrix.mul_one]
       _ = 0 := by rw [← Matrix.mul_assoc,hvR,Matrix.zero_mul]

theorem orthogonal_composition (U W : Matrix n n ℝ)
    (hU : U.transpose*U=1) (hW : W.transpose*W=1) :
    (U*W).transpose*(U*W)=1 := by
  calc
    (U*W).transpose*(U*W)=W.transpose*(U.transpose*U)*W := by
      rw [Matrix.transpose_mul]; simp [Matrix.mul_assoc]
    _ = 1 := by rw [hU,Matrix.mul_one,hW]

theorem all_composed_histories_orthogonal (U : Matrix n n ℝ)
    (hU : U.transpose*U=1) (k : ℕ) : (U^k).transpose*(U^k)=1 := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ]
    exact orthogonal_composition (U^k) U ih hU

theorem minimal_two_step_retained (a p : ℝ) (H : Matrix n n ℝ) :
    ((minimalJoint a p H)*(minimalJoint a p H)).toBlocks₁₁ =
      a^2 • 1-p^2 • H := by
  rw [minimal_is_joint,joint_two_step_retained]
  simp

theorem two_steps_recover_full_minimal_memory (a p : ℝ) (H₁ H₂ : Matrix n n ℝ)
    (hp : p≠0)
    (he : ((minimalJoint a p H₁)*(minimalJoint a p H₁)).toBlocks₁₁ =
      ((minimalJoint a p H₂)*(minimalJoint a p H₂)).toBlocks₁₁) : H₁=H₂ := by
  rw [minimal_two_step_retained,minimal_two_step_retained] at he
  have hs : p^2 • (H₁-H₂)=0 := by
    have hh : p^2 • H₁=p^2 • H₂ := sub_right_inj.mp he
    rw [smul_sub,hh,sub_self]
  exact sub_eq_zero.mp ((smul_eq_zero.mp hs).resolve_left (pow_ne_zero _ hp))

theorem minimal_two_step_feedback (a p : ℝ) (H : Matrix n n ℝ)
    (h : a^2+p^2=1) (hH : H.transpose*H=1) :
    activeFeedback ((minimalJoint a p H)*(minimalJoint a p H)) =
      (a^2*p^2) • ((2 : ℝ) • 1+H+H.transpose) := by
  have hU := minimal_orthogonal a p H h hH
  rw [feedback_from_retained_block _ (orthogonal_composition _ _ hU hU),minimal_two_step_retained]
  simp only [Matrix.transpose_sub,Matrix.transpose_smul,Matrix.transpose_one,
    Matrix.sub_mul,Matrix.mul_sub,Matrix.smul_mul,Matrix.mul_smul,
    Matrix.one_mul,Matrix.mul_one,smul_smul,hH]
  have hc : a^2*a^2+p^2*p^2+2*(a^2*p^2)=1 := by nlinarith [sq_nonneg (a^2+p^2-1)]
  have hcM : (a^2*a^2+p^2*p^2+2*(a^2*p^2)) • (1 : Matrix n n ℝ)=1 := by
    rw [hc,one_smul]
  conv_lhs => lhs; rw [← hcM]
  module

theorem golden_two_step_feedback (a p : ℝ) (H : Matrix n n ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hH : H.transpose*H=1) :
    activeFeedback ((minimalJoint a p H)*(minimalJoint a p H)) =
      p^3 • ((2 : ℝ) • 1+H+H.transpose) := by
  have h : a^2+p^2=1 := by rw [ha]; exact hp
  rw [minimal_two_step_feedback a p H h hH,ha]
  congr 1
  ring

end MinimalArchive

section NativeProtocols
open D0.Representation.GoldenCoherentMemory D0.Representation.GoldenOrderInterferometer

def swapBit : Matrix (Fin 2) (Fin 2) ℝ := !![0,1;1,0]

/-- The already owned golden gate, acting equally on both record coordinates. -/
def directStep (a p : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![gate a p 0 0,0,gate a p 0 1,0;
     0,gate a p 0 0,0,gate a p 0 1;
     gate a p 1 0,0,gate a p 1 1,0;
     0,gate a p 1 0,0,gate a p 1 1]

def asBlocks (U : Matrix (Fin 4) (Fin 4) ℝ) :
    Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ :=
  U.submatrix finSumFinEquiv finSumFinEquiv

theorem swapBit_orthogonal : swapBit.transpose*swapBit=1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [swapBit,Matrix.mul_apply,Fin.sum_univ_succ]

theorem directStep_owned_blocks (a p : ℝ) :
    asBlocks (directStep a p)=minimalJoint a p (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j
  rcases i with i|i <;> rcases j with j|j <;>
    fin_cases i <;> fin_cases j <;>
    simp [asBlocks,directStep,gate,minimalJoint,Matrix.submatrix,finSumFinEquiv,Matrix.fromBlocks]

theorem recordedStep_owned_blocks (a p : ℝ) :
    asBlocks (fullStep a p)=minimalJoint a p swapBit := by
  ext i j
  rcases i with i|i <;> rcases j with j|j <;>
    fin_cases i <;> fin_cases j <;>
    simp [asBlocks,fullStep,swapBit,minimalJoint,Matrix.submatrix,finSumFinEquiv,Matrix.fromBlocks]

theorem actual_composition_binding (U W : Matrix (Fin 4) (Fin 4) ℝ) :
    asBlocks (U*W)=asBlocks U*asBlocks W := by
  let e : Fin 2 ⊕ Fin 2 ≃ Fin 4 := finSumFinEquiv
  exact (Matrix.submatrix_mul_equiv U W e e e).symm

theorem same_native_single_return (a p : ℝ) :
    activeFeedback (asBlocks (directStep a p))=p^2 • 1 ∧
    activeFeedback (asBlocks (fullStep a p))=p^2 • 1 := by
  rw [directStep_owned_blocks,recordedStep_owned_blocks,minimal_is_joint,minimal_is_joint]
  exact ⟨one_return_feedback a p 1 1 0 (by simp),
    one_return_feedback a p 1 swapBit 0 swapBit_orthogonal⟩

theorem direct_two_feedback (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    activeFeedback (asBlocks (directStep a p*directStep a p))=
      (4*p^3) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  rw [actual_composition_binding,directStep_owned_blocks,
    golden_two_step_feedback a p 1 ha hp (by simp)]
  simp only [Matrix.transpose_one]
  module

theorem recorded_two_feedback (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    activeFeedback (asBlocks (fullStep a p*fullStep a p))=
      (2*p^3) • (1+swapBit) := by
  rw [actual_composition_binding,recordedStep_owned_blocks,
    golden_two_step_feedback a p swapBit ha hp swapBit_orthogonal]
  have hs : swapBit.transpose=swapBit := by ext i j; fin_cases i <;> fin_cases j <;> rfl
  rw [hs]
  module

def feedbackAction {n : Type*} [Fintype n] [DecidableEq n] (z : ℝ) (F : Matrix n n ℝ) : ℝ :=
  -Real.log (1-z • F).det

theorem direct_two_determinant (a p z : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (1-z • activeFeedback (asBlocks (directStep a p*directStep a p))).det =
      (1-4*z*p^3)^2 := by
  rw [direct_two_feedback a p ha hp]
  simp [Matrix.det_fin_two]
  ring

theorem recorded_two_determinant (a p z : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (1-z • activeFeedback (asBlocks (fullStep a p*fullStep a p))).det =
      1-4*z*p^3 := by
  rw [recorded_two_feedback a p ha hp]
  simp [Matrix.det_fin_two,swapBit]
  ring

theorem native_composed_action_gap (a p z : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    feedbackAction z (activeFeedback (asBlocks (directStep a p*directStep a p))) -
      feedbackAction z (activeFeedback (asBlocks (fullStep a p*fullStep a p))) =
      -Real.log (1-4*z*p^3) := by
  unfold feedbackAction
  rw [direct_two_determinant a p z ha hp,recorded_two_determinant a p z ha hp,
    Real.log_pow]
  ring

theorem native_composed_action_gap_positive (p z : ℝ)
    (hp : 0<p) (hz : 0<z) (hd : 0<1-4*z*p^3) :
    0 < -Real.log (1-4*z*p^3) := by
  have hprod : 0<4*z*p^3 := by positivity
  exact neg_pos.mpr (Real.log_neg hd (by linarith))

end NativeProtocols

section GenuineSource

def cayleyAxis (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  (1/(1+t^2)) • !![1-t^2,-2*t;2*t,1-t^2]

theorem cayleyAxis_orthogonal (t : ℝ) : (cayleyAxis t).transpose*cayleyAxis t=1 := by
  have hn : 1+t^2≠0 := ne_of_gt (by positivity)
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [cayleyAxis,Matrix.mul_apply,Fin.sum_univ_succ]
  all_goals field_simp
  all_goals ring

theorem cayley_two_feedback (a p t : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    activeFeedback ((minimalJoint a p (cayleyAxis t))*(minimalJoint a p (cayleyAxis t))) =
      (4*p^3/(1+t^2)) • 1 := by
  rw [golden_two_step_feedback a p (cayleyAxis t) ha hp (cayleyAxis_orthogonal t)]
  have hn : 1+t^2≠0 := ne_of_gt (by positivity)
  ext i j
  fin_cases i <;> fin_cases j <;> simp [cayleyAxis]
  all_goals field_simp
  all_goals ring

def cayleyComposedAction (p z t : ℝ) : ℝ := -2*Real.log (1-z*(4*p^3/(1+t^2)))

theorem genuine_cayley_composed_source (p z t : ℝ) (hd : 1+t^2-4*z*p^3≠0) :
    HasDerivAt (cayleyComposedAction p z)
      (-16*p^3*z*t/((1+t^2)*(1+t^2-4*z*p^3))) t := by
  have hn : 1+t^2≠0 := ne_of_gt (by positivity)
  have hq : HasDerivAt (fun s : ℝ => 1+s^2) (2*t) t := by
    simpa using ((hasDerivAt_id t).pow 2).const_add 1
  have hf := (hasDerivAt_const t (4*p^3)).div hq hn
  have hh : 1-z*(4*p^3/(1+t^2))≠0 := by
    intro he
    apply hd
    field_simp at he
    nlinarith [he]
  have hs := (((hf.const_mul z).const_sub 1).log hh).const_mul (-2)
  convert hs using 1
  simp only [Pi.div_apply]
  field_simp
  ring

theorem actual_cayley_action_binding (a p z t : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    feedbackAction z (activeFeedback
      ((minimalJoint a p (cayleyAxis t))*(minimalJoint a p (cayleyAxis t)))) =
        cayleyComposedAction p z t := by
  rw [cayley_two_feedback a p t ha hp]
  unfold feedbackAction cayleyComposedAction
  have hd : (1-z • ((4*p^3/(1+t^2)) • (1 : Matrix (Fin 2) (Fin 2) ℝ))).det =
      (1-z*(4*p^3/(1+t^2)))^2 := by simp [Matrix.det_fin_two]; ring
  rw [hd,Real.log_pow]
  ring

theorem actual_cayley_source (a p z t : ℝ) (ha : a^2=p) (hp : p+p^2=1)
    (hd : 1+t^2-4*z*p^3≠0) :
    HasDerivAt (fun s => feedbackAction z (activeFeedback
      ((minimalJoint a p (cayleyAxis s))*(minimalJoint a p (cayleyAxis s)))))
        (-16*p^3*z*t/((1+t^2)*(1+t^2-4*z*p^3))) t := by
  simpa only [actual_cayley_action_binding a p z _ ha hp] using
    genuine_cayley_composed_source p z t hd

theorem composed_source_nonzero (p z : ℝ) (hp : 0<p) (hz : 0<z)
    (hd : 0<2-4*z*p^3) : -16*p^3*z/(2*(2-4*z*p^3))≠0 := by
  apply div_ne_zero
  · have h : 0<16*p^3*z := by positivity
    nlinarith
  · exact ne_of_gt (by positivity)

end GenuineSource

section CoherentRefinement
variable {n : Type*} [Fintype n] [DecidableEq n]

def liftOperator (A : Matrix n n ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  fromBlocks A 0 0 A

/-- Same golden cylinder inclusion in the explicit sum-coordinate basis. -/
def goldenInclusion (a p : ℝ) (x : n → ℝ) : n ⊕ n → ℝ :=
  Sum.elim (a • x) (p • x)

theorem golden_lift_intertwines (A : Matrix n n ℝ) (a p : ℝ) (x : n → ℝ) :
    (liftOperator A).mulVec (goldenInclusion a p x)=
      goldenInclusion a p (A.mulVec x) := by
  simp [liftOperator,goldenInclusion,Matrix.fromBlocks_mulVec,Matrix.mulVec_smul]

theorem golden_inclusion_preserves_pairing (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1)
    (x y : n → ℝ) :
    dotProduct (goldenInclusion a p x) (goldenInclusion a p y)=dotProduct x y := by
  simp only [dotProduct,Fintype.sum_sum_type,goldenInclusion,Sum.elim_inl,Sum.elim_inr,
    Pi.smul_apply,smul_eq_mul]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i hi
  have h : a^2+p^2=1 := by rw [ha]; exact hp
  calc (a*x i)*(a*y i)+(p*x i)*(p*y i) = (a^2+p^2)*(x i*y i) := by ring
       _ = x i*y i := by rw [h,one_mul]

theorem lift_mul (A B : Matrix n n ℝ) :
    liftOperator (A*B)=liftOperator A*liftOperator B := by
  simp [liftOperator,Matrix.fromBlocks_multiply]

theorem lift_one : liftOperator (1 : Matrix n n ℝ)=1 := Matrix.fromBlocks_one

theorem lift_transpose (A : Matrix n n ℝ) :
    liftOperator A.transpose=(liftOperator A).transpose := by
  simp [liftOperator,Matrix.fromBlocks_transpose]

theorem lift_sub (A B : Matrix n n ℝ) :
    liftOperator (A-B)=liftOperator A-liftOperator B := by
  ext i j
  rcases i with i|i <;> rcases j with j|j <;> simp [liftOperator,Matrix.fromBlocks]

theorem lift_smul (a : ℝ) (A : Matrix n n ℝ) : liftOperator (a • A)=a • liftOperator A := by
  simp [liftOperator,Matrix.fromBlocks_smul]

theorem lift_every_power (U : Matrix n n ℝ) (k : ℕ) :
    liftOperator (U^k)=(liftOperator U)^k := by
  induction k with
  | zero => simp [lift_one]
  | succ k ih => rw [pow_succ,lift_mul,ih,pow_succ]

def fullFeedback (P U : Matrix n n ℝ) := P*U.transpose*(1-P)*U*P

/-- Both the operator and its retained/archive split refine together. -/
theorem full_feedback_refines (P U : Matrix n n ℝ) :
    fullFeedback (liftOperator P) (liftOperator U)=liftOperator (fullFeedback P U) := by
  simp only [fullFeedback,lift_mul,lift_transpose,lift_sub,lift_one]

theorem every_history_feedback_refines (P U : Matrix n n ℝ) (k : ℕ) :
    fullFeedback (liftOperator P) ((liftOperator U)^k)=liftOperator (fullFeedback P (U^k)) := by
  rw [← lift_every_power,full_feedback_refines]

theorem lifted_determinant (A : Matrix n n ℝ) : (liftOperator A).det=A.det^2 := by
  rw [liftOperator,Matrix.det_fromBlocks_zero₂₁,pow_two]

theorem actual_feedback_action_refinement (z : ℝ) (F : Matrix n n ℝ) :
    feedbackAction z (liftOperator F)=2*feedbackAction z F := by
  unfold feedbackAction
  rw [← lift_smul,← lift_one,← lift_sub,lifted_determinant,Real.log_pow]
  ring

theorem composed_feedback_action_refinement (z : ℝ) (P U : Matrix n n ℝ) (k : ℕ) :
    feedbackAction z (fullFeedback (liftOperator P) ((liftOperator U)^k)) =
      2*feedbackAction z (fullFeedback P (U^k)) := by
  rw [every_history_feedback_refines,actual_feedback_action_refinement]

theorem genuine_refined_source (F : ℝ → Matrix n n ℝ) (z t source : ℝ)
    (h : HasDerivAt (fun s => feedbackAction z (F s)) source t) :
    HasDerivAt (fun s => feedbackAction z (liftOperator (F s))) (2*source) t := by
  simpa only [actual_feedback_action_refinement] using h.const_mul 2

end CoherentRefinement

section PreparedReadout
variable {n m : Type*} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]

/-- Compression to a specified complete preparation, without assuming autonomy. -/
def preparedReturn (J : Matrix m n ℝ) (U : Matrix m m ℝ) : Matrix n n ℝ :=
  J.transpose*U*J

def transportReadout (J : Matrix m n ℝ) (P : Matrix n n ℝ) : Matrix m m ℝ :=
  J*P*J.transpose

def preparationLeak (J : Matrix m n ℝ) (U : Matrix m m ℝ) : Matrix m n ℝ :=
  U*J-J*preparedReturn J U

def returnFeedback (P C : Matrix n n ℝ) : Matrix n n ℝ :=
  fullFeedback P C+P*(1-C.transpose*C)*P

theorem prepared_readout_intertwines (J : Matrix m n ℝ) (P : Matrix n n ℝ)
    (hJ : J.transpose*J=1) : transportReadout J P*J=J*P := by
  simp [transportReadout,Matrix.mul_assoc,hJ]

theorem prepared_readout_projector (J : Matrix m n ℝ) (P : Matrix n n ℝ)
    (hJ : J.transpose*J=1) (hP : P*P=P) :
    transportReadout J P*transportReadout J P=transportReadout J P := by
  calc
    transportReadout J P*transportReadout J P = J*P*(J.transpose*J)*P*J.transpose := by
      simp [transportReadout,Matrix.mul_assoc]
    _ = transportReadout J P := by rw [hJ,Matrix.mul_one]; simp [transportReadout,Matrix.mul_assoc,hP]

theorem prepared_readout_symmetric (J : Matrix m n ℝ) (P : Matrix n n ℝ)
    (hP : P.transpose=P) : (transportReadout J P).transpose=transportReadout J P := by
  simp [transportReadout,Matrix.transpose_mul,hP,Matrix.mul_assoc]

/-- This uniqueness has the explicit condition of no additional fine active range. -/
theorem prepared_readout_unique (J : Matrix m n ℝ) (P : Matrix n n ℝ)
    (Q : Matrix m m ℝ) (hQ : Q*J=J*P) (hSupport : Q*(J*J.transpose)=Q) :
    Q=transportReadout J P := by
  rw [← hSupport,← Matrix.mul_assoc,hQ]
  rfl

theorem leak_is_orthogonal (J : Matrix m n ℝ) (U : Matrix m m ℝ)
    (hJ : J.transpose*J=1) : J.transpose*preparationLeak J U=0 := by
  simp [preparationLeak,preparedReturn,Matrix.mul_sub,← Matrix.mul_assoc,hJ]

/-- Exact missing norm; no reset or fresh zero archive is inserted. -/
theorem full_preparation_defect (J : Matrix m n ℝ) (U : Matrix m m ℝ)
    (hJ : J.transpose*J=1) (hU : U.transpose*U=1) :
    (preparationLeak J U).transpose*preparationLeak J U =
      1-(preparedReturn J U).transpose*preparedReturn J U := by
  let C := preparedReturn J U
  have h₁ : (U*J).transpose*(U*J)=1 := by
    calc (U*J).transpose*(U*J) = J.transpose*(U.transpose*U)*J := by simp [Matrix.mul_assoc]
         _ = 1 := by rw [hU,Matrix.mul_one,hJ]
  have h₂ : (U*J).transpose*J=C.transpose := by simp [C,preparedReturn,Matrix.mul_assoc]
  have h₃ : J.transpose*(U*J)=C := by simp [C,preparedReturn,Matrix.mul_assoc]
  change (U*J-J*C).transpose*(U*J-J*C)=1-C.transpose*C
  simp only [Matrix.transpose_sub,Matrix.sub_mul,Matrix.mul_sub]
  have h₄ : (U*J).transpose*(J*C)=C.transpose*C := by rw [← Matrix.mul_assoc,h₂]
  have h₅ : (J*C).transpose*(U*J)=C.transpose*C := by
    rw [Matrix.transpose_mul,Matrix.mul_assoc,h₃]
  have h₆ : (J*C).transpose*(J*C)=C.transpose*C := by
    calc (J*C).transpose*(J*C)=C.transpose*(J.transpose*J)*C := by simp [Matrix.mul_assoc]
         _ = C.transpose*C := by rw [hJ,Matrix.mul_one]
  rw [h₁,h₄,h₅,h₆]
  abel

theorem return_feedback_expanded (P C : Matrix n n ℝ) :
    returnFeedback P C=P*P-P*C.transpose*P*C*P := by
  simp only [returnFeedback,fullFeedback,Matrix.mul_sub,Matrix.sub_mul,
    Matrix.mul_one,Matrix.mul_assoc]
  abel

/-- Full fine feedback of the transported experiment depends on the compressed
whole history and its norm defect, not a chosen extension off the preparation. -/
theorem full_prepared_feedback (J : Matrix m n ℝ) (U : Matrix m m ℝ)
    (P : Matrix n n ℝ) (hJ : J.transpose*J=1) (hU : U.transpose*U=1) :
    fullFeedback (transportReadout J P) U=
      transportReadout J (returnFeedback P (preparedReturn J U)) := by
  let C := preparedReturn J U
  have h₁ : J.transpose*(U.transpose*U)*J=1 := by rw [hU,Matrix.mul_one,hJ]
  have h₂ : J.transpose*U.transpose*J=C.transpose := by simp [C,preparedReturn,Matrix.mul_assoc]
  have h₃ : J.transpose*U*J=C := rfl
  rw [return_feedback_expanded]
  simp only [fullFeedback,transportReadout,Matrix.mul_sub,Matrix.sub_mul]
  have term₁ : J*P*J.transpose*U.transpose*1*U*(J*P*J.transpose) = J*(P*P)*J.transpose := by
    calc
      _ = J*P*(J.transpose*(U.transpose*U)*J)*P*J.transpose := by simp [Matrix.mul_assoc]
      _ = _ := by rw [h₁,Matrix.mul_one]; simp [Matrix.mul_assoc]
  have term₂ : J*P*J.transpose*U.transpose*(J*P*J.transpose)*U*(J*P*J.transpose) =
      J*(P*C.transpose*P*C*P)*J.transpose := by
    calc
      _ = J*P*(J.transpose*U.transpose*J)*P*(J.transpose*U*J)*P*J.transpose := by
        simp [Matrix.mul_assoc]
      _ = _ := by rw [h₂,h₃]; simp [Matrix.mul_assoc]
  change J*P*J.transpose*U.transpose*1*U*(J*P*J.transpose) -
      J*P*J.transpose*U.transpose*(J*P*J.transpose)*U*(J*P*J.transpose) = _
  rw [term₁,term₂]

theorem transported_feedback_determinant (J : Matrix m n ℝ) (F : Matrix n n ℝ)
    (z : ℝ) (hJ : J.transpose*J=1) :
    (1-z • transportReadout J F).det=(1-z • F).det := by
  have h := Matrix.det_one_sub_mul_comm (z • J) (F*J.transpose)
  simpa [transportReadout,Matrix.smul_mul,Matrix.mul_smul,Matrix.mul_assoc,hJ] using h

theorem transported_feedback_action (J : Matrix m n ℝ) (F : Matrix n n ℝ)
    (z : ℝ) (hJ : J.transpose*J=1) :
    feedbackAction z (transportReadout J F)=feedbackAction z F := by
  unfold feedbackAction
  rw [transported_feedback_determinant J F z hJ]

/-- The exact action uses the full return and its leakage correction. -/
theorem full_prepared_action (J : Matrix m n ℝ) (U : Matrix m m ℝ)
    (P : Matrix n n ℝ) (z : ℝ) (hJ : J.transpose*J=1) (hU : U.transpose*U=1) :
    feedbackAction z (fullFeedback (transportReadout J P) U)=
      feedbackAction z (returnFeedback P (preparedReturn J U)) := by
  rw [full_prepared_feedback J U P hJ hU,transported_feedback_action J _ z hJ]

theorem every_prepared_history_action (J : Matrix m n ℝ) (U : Matrix m m ℝ)
    (P : Matrix n n ℝ) (z : ℝ) (k : ℕ)
    (hJ : J.transpose*J=1) (hU : U.transpose*U=1) :
    feedbackAction z (fullFeedback (transportReadout J P) (U^k))=
      feedbackAction z (returnFeedback P (preparedReturn J (U^k))) :=
  full_prepared_action J (U^k) P z hJ (all_composed_histories_orthogonal U hU k)

/-- Equality of the full compressed word, not the first compressed operator. -/
theorem full_return_determines_prepared_action
    (J K : Matrix m n ℝ) (U V : Matrix m m ℝ) (P : Matrix n n ℝ) (z : ℝ)
    (hJ : J.transpose*J=1) (hK : K.transpose*K=1)
    (hU : U.transpose*U=1) (hV : V.transpose*V=1)
    (hReturn : preparedReturn J U=preparedReturn K V) :
    feedbackAction z (fullFeedback (transportReadout J P) U)=
      feedbackAction z (fullFeedback (transportReadout K P) V) := by
  rw [full_prepared_action J U P z hJ hU,full_prepared_action K V P z hK hV,hReturn]

/-- Moving preparation, split and joint dynamics are all included. The derivative
is transported from a proved scalar identity, not postulated to vanish. -/
theorem full_prepared_source (J : ℝ → Matrix m n ℝ) (U : ℝ → Matrix m m ℝ)
    (P : ℝ → Matrix n n ℝ) (z t source : ℝ)
    (hJ : ∀ s, (J s).transpose*J s=1) (hU : ∀ s, (U s).transpose*U s=1)
    (h : HasDerivAt (fun s => feedbackAction z
      (returnFeedback (P s) (preparedReturn (J s) (U s)))) source t) :
    HasDerivAt (fun s => feedbackAction z
      (fullFeedback (transportReadout (J s) (P s)) (U s))) source t := by
  have he : (fun s => feedbackAction z (fullFeedback (transportReadout (J s) (P s)) (U s))) =
      (fun s => feedbackAction z (returnFeedback (P s) (preparedReturn (J s) (U s)))) := by
    funext s
    exact full_prepared_action (J s) (U s) (P s) z (hJ s) (hU s)
  rw [he]
  exact h

/-- The scalar golden active compression itself supplies its archive feedback. -/
theorem golden_prepared_return_feedback (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    returnFeedback (1 : Matrix n n ℝ) (a • 1)=p^2 • 1 := by
  rw [return_feedback_expanded]
  simp only [Matrix.one_mul,Matrix.mul_one,Matrix.transpose_smul,Matrix.transpose_one,
    Matrix.smul_mul,Matrix.mul_smul,smul_smul]
  have h : 1-a*a=p^2 := by nlinarith
  calc
    1-(a*a) • (1 : Matrix n n ℝ)=(1-a*a) • 1 := by module
    _ = p^2 • 1 := by rw [h]

/-- Complete additional active range: matching the old prepared experiment
permits precisely an orthogonal projector on the preparation complement. -/
theorem compatible_readout_complement (J : Matrix m n ℝ) (P : Matrix n n ℝ)
    (R : Matrix m m ℝ) (hJ : J.transpose*J=1)
    (hP : P*P=P) (hsP : P.transpose=P)
    (hR : R*R=R) (hsR : R.transpose=R) (hRJ : R*J=J*P) :
    ∃ S : Matrix m m ℝ, R=transportReadout J P+S ∧ S*J=0 ∧
      J.transpose*S=0 ∧ S.transpose=S ∧ S*S=S := by
  let A := transportReadout J P
  have hA : A*A=A := prepared_readout_projector J P hJ hP
  have hsA : A.transpose=A := prepared_readout_symmetric J P hsP
  have hRA : R*A=A := by
    calc R*A = R*J*P*J.transpose := by simp [A,transportReadout,Matrix.mul_assoc]
         _ = A := by rw [hRJ]; simp [A,transportReadout,Matrix.mul_assoc,hP]
  have hAR : A*R=A := by simpa [hsA,hsR] using congrArg Matrix.transpose hRA
  have hSJ : (R-A)*J=0 := by
    rw [Matrix.sub_mul,hRJ,prepared_readout_intertwines J P hJ,sub_self]
  have hsS : (R-A).transpose=R-A := by rw [Matrix.transpose_sub,hsR,hsA]
  refine ⟨R-A,by dsimp [A]; abel,hSJ,?_,hsS,?_⟩
  · simpa [hsS] using congrArg Matrix.transpose hSJ
  · simp only [Matrix.sub_mul,Matrix.mul_sub,hR,hRA,hAR,hA]
    abel

theorem compatible_readout_complement_sufficient (J : Matrix m n ℝ) (P : Matrix n n ℝ)
    (S : Matrix m m ℝ) (hJ : J.transpose*J=1)
    (hP : P*P=P) (hsP : P.transpose=P)
    (hS : S*S=S) (hsS : S.transpose=S) (hSJ : S*J=0) :
    let R := transportReadout J P+S
    R*R=R ∧ R.transpose=R ∧ R*J=J*P := by
  have hJS : J.transpose*S=0 := by simpa [hsS] using congrArg Matrix.transpose hSJ
  have hAS : transportReadout J P*S=0 := by simp [transportReadout,Matrix.mul_assoc,hJS]
  have hSA : S*transportReadout J P=0 := by simp [transportReadout,← Matrix.mul_assoc,hSJ]
  dsimp only
  refine ⟨?_,?_,?_⟩
  · simp only [Matrix.add_mul,Matrix.mul_add,
      prepared_readout_projector J P hJ hP,hS,hAS,hSA,add_zero,zero_add]
  · rw [Matrix.transpose_add,prepared_readout_symmetric J P hsP,hsS]
  · rw [Matrix.add_mul,prepared_readout_intertwines J P hJ,hSJ,add_zero]

end PreparedReadout

section OwnedPreparedEmbedding
variable {n : Type*} [Fintype n] [DecidableEq n]
open D0.Representation.GoldenOrderInterferometer

/-- The first column of the already owned gate on the new factor. -/
def ownedGoldenEmbedding (a p : ℝ) : Matrix (n ⊕ n) n ℝ :=
  fun i j => Sum.elim (fun k => gate a p 0 0*(1 : Matrix n n ℝ) k j)
    (fun k => gate a p 1 0*(1 : Matrix n n ℝ) k j) i

theorem owned_golden_embedding_isometric (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (ownedGoldenEmbedding (n:=n) a p).transpose*ownedGoldenEmbedding (n:=n) a p=1 := by
  ext i j
  by_cases hij : i=j
  · subst j
    simp [ownedGoldenEmbedding,gate,Matrix.mul_apply,Fintype.sum_sum_type,Matrix.one_apply]
    nlinarith
  · simp [ownedGoldenEmbedding,gate,Matrix.mul_apply,Fintype.sum_sum_type,Matrix.one_apply,hij,Ne.symm hij]

theorem owned_golden_embedding_realizes_inclusion (a p : ℝ) (x : n → ℝ) :
    (ownedGoldenEmbedding a p).mulVec x=goldenInclusion a p x := by
  ext i
  rcases i with i|i <;>
    simp [ownedGoldenEmbedding,gate,Matrix.mulVec,dotProduct,Matrix.one_apply,goldenInclusion]

/-- Literal pullback of a cylinder value repeats its multiplication operator on
both child branches. It is not the image-supported coherent preparation test. -/
theorem literal_cylinder_observable_pullback (f : n → ℝ) :
    Matrix.diagonal (Sum.elim f f)=liftOperator (Matrix.diagonal f) := by
  ext i j
  rcases i with i|i <;> rcases j with j|j <;>
    simp [Matrix.diagonal,liftOperator,Matrix.fromBlocks]

end OwnedPreparedEmbedding

section GoldenTwoPreparations
variable {n : Type*} [Fintype n] [DecidableEq n]
open D0.Representation.GoldenOrderInterferometer

/-- The owned gate acting on the new factor, with every old coordinate retained. -/
def ownedGoldenFactor (a p : ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  fromBlocks (gate a p 0 0 • 1) (gate a p 0 1 • 1)
    (gate a p 1 0 • 1) (gate a p 1 1 • 1)

def preparationCoordinates (a p : ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  fromBlocks 1 (a • 1) 0 (p • 1)

def preparationCoordinatesInverse (a p : ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  fromBlocks 1 ((-a/p) • 1) 0 (p⁻¹ • 1)

/-- Columns are J and GJ: two complete native histories, not powers of JᵀGJ. -/
def nativePreparationFrame (a p : ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  ownedGoldenFactor a p * preparationCoordinates a p

/-- The four full cross-return operators, bundled without discarding their blocks. -/
def nativeCrossReturns (a p : ℝ) (U : Matrix (n ⊕ n) (n ⊕ n) ℝ) :=
  (nativePreparationFrame a p).transpose * U * nativePreparationFrame a p

def recoverGoldenCoordinates (a p : ℝ) (R : Matrix (n ⊕ n) (n ⊕ n) ℝ) :=
  (preparationCoordinatesInverse a p).transpose * R * preparationCoordinatesInverse a p

theorem golden_factor_owned_blocks (a p : ℝ) :
    ownedGoldenFactor (n:=n) a p = minimalJoint a p 1 := by
  simp [ownedGoldenFactor,gate,minimalJoint]

theorem golden_factor_orthogonal (a p : ℝ) (h : a^2+p^2=1) :
    (ownedGoldenFactor (n:=n) a p).transpose*ownedGoldenFactor a p=1 := by
  rw [golden_factor_owned_blocks]
  exact minimal_orthogonal a p 1 h (by simp)

theorem two_native_preparation_columns (a p : ℝ) :
    (∀ i j, nativePreparationFrame (n:=n) a p i (Sum.inl j)=ownedGoldenEmbedding a p i j) ∧
    (∀ i j, nativePreparationFrame (n:=n) a p i (Sum.inr j)=
      (ownedGoldenFactor (n:=n) a p*ownedGoldenEmbedding (n:=n) a p) i j) := by
  constructor
  · intro i j
    rcases i with i|i <;>
      simp [nativePreparationFrame,ownedGoldenFactor,preparationCoordinates,
        ownedGoldenEmbedding,gate,Matrix.mul_apply,Fintype.sum_sum_type,Matrix.one_apply]
  · intro i j
    rcases i with i|i <;>
      simp [nativePreparationFrame,ownedGoldenFactor,preparationCoordinates,
        ownedGoldenEmbedding,gate,Matrix.mul_apply,Fintype.sum_sum_type,Matrix.one_apply]

theorem preparation_coordinates_inverse (a p : ℝ) (hp : p≠0) :
    preparationCoordinates (n:=n) a p*preparationCoordinatesInverse a p=1 ∧
    preparationCoordinatesInverse (n:=n) a p*preparationCoordinates a p=1 := by
  have first : preparationCoordinates (n:=n) a p*preparationCoordinatesInverse a p=1 := by
    rw [preparationCoordinates,preparationCoordinatesInverse,Matrix.fromBlocks_multiply,
      ← Matrix.fromBlocks_one (l:=n) (m:=n)]
    apply Matrix.fromBlocks_inj.mpr
    simp [Matrix.mul_smul,Matrix.smul_mul,smul_smul,hp]
    field_simp
    module
  exact ⟨first,mul_eq_one_comm.mp first⟩

theorem all_four_returns_reconstruct_coordinates (a p : ℝ)
    (U : Matrix (n ⊕ n) (n ⊕ n) ℝ) (hp : p≠0) :
    recoverGoldenCoordinates a p (nativeCrossReturns a p U)=
      (ownedGoldenFactor a p).transpose*U*ownedGoldenFactor a p := by
  have hi := (preparation_coordinates_inverse (n:=n) a p hp).1
  have ht : (preparationCoordinatesInverse (n:=n) a p).transpose*
      (preparationCoordinates a p).transpose=1 := by
    simpa only [Matrix.transpose_mul,Matrix.transpose_one] using congrArg Matrix.transpose hi
  simp only [recoverGoldenCoordinates,nativeCrossReturns,nativePreparationFrame,Matrix.transpose_mul]
  calc
    _ = ((preparationCoordinatesInverse a p).transpose*(preparationCoordinates a p).transpose)*
      ((ownedGoldenFactor a p).transpose*U*ownedGoldenFactor a p)*
      (preparationCoordinates a p*preparationCoordinatesInverse a p) := by
        simp [Matrix.mul_assoc]
    _ = _ := by rw [hi,ht,Matrix.one_mul,Matrix.mul_one]

theorem all_four_returns_reconstruct_full_operator (a p : ℝ)
    (U : Matrix (n ⊕ n) (n ⊕ n) ℝ) (hp : p≠0) (h : a^2+p^2=1) :
    ownedGoldenFactor a p*recoverGoldenCoordinates a p (nativeCrossReturns a p U)*
      (ownedGoldenFactor a p).transpose=U := by
  have hg := mul_eq_one_comm.mp (golden_factor_orthogonal (n:=n) a p h)
  rw [all_four_returns_reconstruct_coordinates a p U hp]
  calc
    _ = (ownedGoldenFactor a p*(ownedGoldenFactor a p).transpose)*U*
      (ownedGoldenFactor a p*(ownedGoldenFactor a p).transpose) := by simp [Matrix.mul_assoc]
    _ = U := by rw [hg,Matrix.one_mul,Matrix.mul_one]

theorem native_cross_returns_injective (a p : ℝ) (hp : p≠0) (h : a^2+p^2=1) :
    Function.Injective (nativeCrossReturns (n:=n) a p) := by
  intro U V he
  have eq := congrArg (fun R => ownedGoldenFactor a p*recoverGoldenCoordinates a p R*
    (ownedGoldenFactor a p).transpose) he
  simpa only [all_four_returns_reconstruct_full_operator a p _ hp h] using eq

theorem golden_factor_commutes_literal_readout (a p : ℝ) (P : Matrix n n ℝ) :
    ownedGoldenFactor a p*liftOperator P=liftOperator P*ownedGoldenFactor a p := by
  simp only [ownedGoldenFactor,liftOperator,Matrix.fromBlocks_multiply,
    Matrix.mul_smul,Matrix.smul_mul,Matrix.mul_one,Matrix.one_mul,
    Matrix.mul_zero,Matrix.zero_mul,smul_zero,add_zero,zero_add]

theorem full_literal_feedback_coordinates (a p : ℝ) (P : Matrix n n ℝ)
    (U : Matrix (n ⊕ n) (n ⊕ n) ℝ) (h : a^2+p^2=1) :
    fullFeedback (liftOperator P) ((ownedGoldenFactor a p).transpose*U*ownedGoldenFactor a p)=
      (ownedGoldenFactor a p).transpose*fullFeedback (liftOperator P) U*ownedGoldenFactor a p := by
  let G : Matrix (n ⊕ n) (n ⊕ n) ℝ := ownedGoldenFactor a p
  let R := liftOperator P
  have hgl : G.transpose*G=1 := golden_factor_orthogonal a p h
  have hg : G*G.transpose=1 := mul_eq_one_comm.mp hgl
  have hc : G*R=R*G := golden_factor_commutes_literal_readout a p P
  have hct : R*G.transpose=G.transpose*R := by
    calc
      R*G.transpose = (G.transpose*G)*R*G.transpose := by rw [hgl,Matrix.one_mul]
      _ = G.transpose*(G*R)*G.transpose := by simp [Matrix.mul_assoc]
      _ = G.transpose*(R*G)*G.transpose := by rw [hc]
      _ = G.transpose*R := by
        calc
          _ = G.transpose*R*(G*G.transpose) := by simp [Matrix.mul_assoc]
          _ = _ := by rw [hg,Matrix.mul_one]
  have hcq : G*(1-R)*G.transpose=1-R := by
    rw [Matrix.mul_sub,Matrix.mul_one,Matrix.sub_mul,hg,hc]
    simp [Matrix.mul_assoc,hg]
  change fullFeedback R (G.transpose*U*G)=G.transpose*fullFeedback R U*G
  simp only [fullFeedback,Matrix.transpose_mul,Matrix.transpose_transpose]
  calc
    _ = (R*G.transpose)*U.transpose*(G*(1-R)*G.transpose)*U*(G*R) := by
      simp [Matrix.mul_assoc]
    _ = (G.transpose*R)*U.transpose*(1-R)*U*(R*G) := by rw [hct,hcq,hc]
    _ = _ := by simp [Matrix.mul_assoc]

theorem literal_action_from_all_four_returns (a p z : ℝ) (P : Matrix n n ℝ)
    (U : Matrix (n ⊕ n) (n ⊕ n) ℝ) (hp : p≠0) (h : a^2+p^2=1) :
    feedbackAction z (fullFeedback (liftOperator P) U)=
      feedbackAction z (fullFeedback (liftOperator P)
        (recoverGoldenCoordinates a p (nativeCrossReturns a p U))) := by
  rw [all_four_returns_reconstruct_coordinates a p U hp,full_literal_feedback_coordinates a p P U h]
  have hg := mul_eq_one_comm.mp (golden_factor_orthogonal (n:=n) a p h)
  exact (transported_feedback_action (ownedGoldenFactor a p).transpose _ z (by simpa using hg)).symm

theorem genuine_two_preparation_source (a p z t source : ℝ)
    (P : ℝ → Matrix n n ℝ) (U : ℝ → Matrix (n ⊕ n) (n ⊕ n) ℝ)
    (hp : p≠0) (h : a^2+p^2=1)
    (hd : HasDerivAt (fun s => feedbackAction z (fullFeedback (liftOperator (P s))
      (recoverGoldenCoordinates a p (nativeCrossReturns a p (U s))))) source t) :
    HasDerivAt (fun s => feedbackAction z (fullFeedback (liftOperator (P s)) (U s))) source t := by
  have he : (fun s => feedbackAction z (fullFeedback (liftOperator (P s)) (U s))) =
      (fun s => feedbackAction z (fullFeedback (liftOperator (P s))
        (recoverGoldenCoordinates a p (nativeCrossReturns a p (U s))))) := by
    funext s
    exact literal_action_from_all_four_returns a p z (P s) (U s) hp h
  rw [he]
  exact hd

end GoldenTwoPreparations

section RecordedQuadraticFeedback
variable {n : Type*} [Fintype n] [DecidableEq n]
open D0.Representation.GoldenCoherentMemory

def responseNormSq (x : n → ℝ) : ℝ := ∑ i, x i*x i
def responsePairing (x y : n → ℝ) : ℝ := ∑ i, x i*y i
def quadraticResponse (A : Matrix n n ℝ) (x : n → ℝ) := responseNormSq (A.mulVec x)

/-- Pointwise expression of the owned fullStep, with both output records retained. -/
def recordedResponseState (a p : ℝ) (x y : n → ℝ) : Fin 4 → n → ℝ :=
  fun c i => (fullStep a p).mulVec ![x i,0,y i,0] c

def firstRecordedResponse (a p : ℝ) (A : Matrix n n ℝ) (x y : n → ℝ) :=
  responseNormSq (recordedResponseState a p (A.mulVec x) (A.mulVec y) 0)

def recoverRecordedPairing (a p qx qy mixed : ℝ) :=
  (a^2*qx+p^2*qy-mixed)/(2*a*p)

def probeVector (i : n) : n → ℝ := fun j => if j=i then 1 else 0

def recordedQuadraticKernel (a p : ℝ) (A : Matrix n n ℝ) : Matrix n n ℝ :=
  fun i j => recoverRecordedPairing a p
    (quadraticResponse A (probeVector i)) (quadraticResponse A (probeVector j))
    (firstRecordedResponse a p A (probeVector i) (probeVector j))

theorem norm_of_native_mix (a p : ℝ) (x y : n → ℝ) :
    responseNormSq (fun i => a*x i-p*y i)=
      a^2*responseNormSq x+p^2*responseNormSq y-2*a*p*responsePairing x y := by
  unfold responseNormSq responsePairing
  simp only [Finset.mul_sum]
  rw [← Finset.sum_add_distrib,← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem owned_recorded_response_coordinates (a p : ℝ) (x y : n → ℝ) :
    recordedResponseState a p x y =
      ![(fun i => a*x i-p*y i),0,0,(fun i => p*x i+a*y i)] := by
  funext c i
  have h := congrFun (blank_record_evolution a p (x i) (y i)) c
  fin_cases c <;> simpa [recordedResponseState] using h

theorem native_recorded_response_balance (a p : ℝ) (x y : n → ℝ)
    (h : a^2+p^2=1) :
    responseNormSq (recordedResponseState a p x y 0)+
      responseNormSq (recordedResponseState a p x y 3)=responseNormSq x+responseNormSq y := by
  rw [owned_recorded_response_coordinates]
  unfold responseNormSq
  simp only [Matrix.cons_val_zero,Matrix.cons_val_three,Matrix.head_cons,Matrix.tail_cons]
  rw [← Finset.sum_add_distrib,← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  dsimp
  calc
    _ = (a^2+p^2)*(x i*x i+y i*y i) := by ring
    _ = _ := by rw [h,one_mul]

theorem native_recorded_mixed_response (a p : ℝ) (A : Matrix n n ℝ) (x y : n → ℝ) :
    firstRecordedResponse a p A x y=
      a^2*quadraticResponse A x+p^2*quadraticResponse A y-
        2*a*p*responsePairing (A.mulVec x) (A.mulVec y) := by
  unfold firstRecordedResponse
  rw [owned_recorded_response_coordinates]
  exact norm_of_native_mix a p _ _

theorem recorded_response_recovers_pairing (a p : ℝ) (A : Matrix n n ℝ) (x y : n → ℝ)
    (ha : a≠0) (hp : p≠0) :
    recoverRecordedPairing a p (quadraticResponse A x) (quadraticResponse A y)
      (firstRecordedResponse a p A x y)=responsePairing (A.mulVec x) (A.mulVec y) := by
  rw [native_recorded_mixed_response]
  unfold recoverRecordedPairing
  field_simp
  ring

theorem probe_pairing_reads_gram (A : Matrix n n ℝ) (i j : n) :
    responsePairing (A.mulVec (probeVector i)) (A.mulVec (probeVector j))=
      (A.transpose*A) i j := by
  simp [responsePairing,probeVector,Matrix.mulVec,Matrix.mul_apply,dotProduct,
    Matrix.transpose_apply]

theorem native_quadratic_readings_reconstruct_gram (a p : ℝ) (A : Matrix n n ℝ)
    (ha : a≠0) (hp : p≠0) : recordedQuadraticKernel a p A=A.transpose*A := by
  ext i j
  rw [recordedQuadraticKernel,recorded_response_recovers_pairing a p A _ _ ha hp,
    probe_pairing_reads_gram]

/-- Coherent preparation stores the entire complementary branch in its flag. -/
def flaggedPreparation (P : Matrix n n ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  fromBlocks P (1-P) (1-P) P

theorem flagged_preparation_square (P : Matrix n n ℝ) (hP : P*P=P) :
    flaggedPreparation P*flaggedPreparation P=1 := by
  rw [flaggedPreparation,Matrix.fromBlocks_multiply,← Matrix.fromBlocks_one (l:=n) (m:=n)]
  apply Matrix.fromBlocks_inj.mpr
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one,Matrix.one_mul,hP]
  constructor
  · abel
  constructor
  · abel
  constructor <;> abel

theorem flagged_preparation_orthogonal (P : Matrix n n ℝ)
    (hP : P*P=P) (hsP : P.transpose=P) :
    (flaggedPreparation P).transpose*flaggedPreparation P=1 := by
  have ht : (flaggedPreparation P).transpose=flaggedPreparation P := by
    simp [flaggedPreparation,Matrix.fromBlocks_transpose,hsP]
  rw [ht,flagged_preparation_square P hP]

theorem flagged_blank_preparation (P : Matrix n n ℝ) (x : n → ℝ) :
    (flaggedPreparation P).mulVec (Sum.elim x 0)=
      Sum.elim (P.mulVec x) ((1-P).mulVec x) := by
  ext i
  rcases i with i|i <;>
    simp [flaggedPreparation,Matrix.mulVec,Matrix.mul_apply,dotProduct,Fintype.sum_sum_type]

/-- The literal cylinder flag uses the already owned reversible basis registration. -/
def registerCylinder (f : n → Bool) : (n × Bool) ≃ (n × Bool) where
  toFun x := (x.1, (D0.Representation.FiniteProtocolClock.register (!f x.1,x.2)).2)
  invFun x := (x.1, (D0.Representation.FiniteProtocolClock.register (!f x.1,x.2)).2)
  left_inv := by intro ⟨i,b⟩; cases hf : f i <;> cases b <;> simp [D0.Representation.FiniteProtocolClock.register,hf]
  right_inv := by intro ⟨i,b⟩; cases hf : f i <;> cases b <;> simp [D0.Representation.FiniteProtocolClock.register,hf]

theorem literal_cylinder_registration (f : n → Bool) (i : n) :
    registerCylinder f (i,false)=(i,!f i) ∧ Function.Injective (registerCylinder f) := by
  constructor
  · simp [registerCylinder,D0.Representation.FiniteProtocolClock.register]
  · exact (registerCylinder f).injective

def feedbackReadingOperator (P U : Matrix n n ℝ) := (1-P)*U*P

theorem actual_feedback_is_response_gram (P U : Matrix n n ℝ)
    (hP : P*P=P) (hsP : P.transpose=P) :
    (feedbackReadingOperator P U).transpose*feedbackReadingOperator P U=fullFeedback P U := by
  have hQ : (1-P)*(1-P)=1-P := by
    simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one,Matrix.one_mul,hP]
    abel
  simp only [feedbackReadingOperator,Matrix.transpose_mul,Matrix.transpose_sub,
    Matrix.transpose_one,hsP]
  calc
    _ = P*U.transpose*((1-P)*(1-P))*U*P := by simp [Matrix.mul_assoc]
    _ = fullFeedback P U := by rw [hQ]; rfl

theorem recorded_readings_reconstruct_full_feedback (a p : ℝ) (P U : Matrix n n ℝ)
    (ha : a≠0) (hp : p≠0) (hP : P*P=P) (hsP : P.transpose=P) :
    recordedQuadraticKernel a p (feedbackReadingOperator P U)=fullFeedback P U := by
  rw [native_quadratic_readings_reconstruct_gram a p _ ha hp,actual_feedback_is_response_gram P U hP hsP]

theorem native_preparation_quadratic_gram (a p : ℝ) (P : Matrix n n ℝ)
    (U : Matrix (n ⊕ n) (n ⊕ n) ℝ) (ha : a≠0) (hp : p≠0)
    (hP : P*P=P) (hsP : P.transpose=P) :
    recordedQuadraticKernel a p (feedbackReadingOperator (liftOperator P) U*nativePreparationFrame a p)=
      nativeCrossReturns a p (fullFeedback (liftOperator P) U) := by
  have hlp : liftOperator P*liftOperator P=liftOperator P := by rw [← lift_mul,hP]
  have hlsp : (liftOperator P).transpose=liftOperator P := by rw [← lift_transpose,hsP]
  rw [native_quadratic_readings_reconstruct_gram a p _ ha hp]
  simp only [Matrix.transpose_mul]
  calc
    _ = (nativePreparationFrame a p).transpose*
      ((feedbackReadingOperator (liftOperator P) U).transpose*feedbackReadingOperator (liftOperator P) U)*
      nativePreparationFrame a p := by simp [Matrix.mul_assoc]
    _ = _ := by rw [actual_feedback_is_response_gram _ _ hlp hlsp]; rfl

theorem native_recorded_feedback_action (a p z : ℝ) (P : Matrix n n ℝ)
    (U : Matrix (n ⊕ n) (n ⊕ n) ℝ) (ha : a≠0) (hp : p≠0)
    (h : a^2+p^2=1) (hP : P*P=P) (hsP : P.transpose=P) :
    feedbackAction z (fullFeedback (liftOperator P) U)=
      feedbackAction z (recoverGoldenCoordinates a p (recordedQuadraticKernel a p
        (feedbackReadingOperator (liftOperator P) U*nativePreparationFrame a p))) := by
  rw [native_preparation_quadratic_gram a p P U ha hp hP hsP,
    all_four_returns_reconstruct_coordinates a p _ hp]
  have hg := mul_eq_one_comm.mp (golden_factor_orthogonal (n:=n) a p h)
  exact (transported_feedback_action (ownedGoldenFactor a p).transpose _ z (by simpa using hg)).symm

theorem genuine_recorded_feedback_source (a p z t source : ℝ)
    (P : ℝ → Matrix n n ℝ) (U : ℝ → Matrix (n ⊕ n) (n ⊕ n) ℝ)
    (ha : a≠0) (hp : p≠0) (h : a^2+p^2=1)
    (hP : ∀ s, P s*P s=P s) (hsP : ∀ s, (P s).transpose=P s)
    (hd : HasDerivAt (fun s => feedbackAction z (recoverGoldenCoordinates a p
      (recordedQuadraticKernel a p (feedbackReadingOperator (liftOperator (P s)) (U s)*
        nativePreparationFrame a p)))) source t) :
    HasDerivAt (fun s => feedbackAction z (fullFeedback (liftOperator (P s)) (U s))) source t := by
  have he : (fun s => feedbackAction z (fullFeedback (liftOperator (P s)) (U s))) =
      (fun s => feedbackAction z (recoverGoldenCoordinates a p
        (recordedQuadraticKernel a p (feedbackReadingOperator (liftOperator (P s)) (U s)*
          nativePreparationFrame a p)))) := by
    funext s
    exact native_recorded_feedback_action a p z (P s) (U s) ha hp h (hP s) (hsP s)
  rw [he]
  exact hd


open scoped Kronecker

/-- The comparison record is new; x,y each include the entire old target record. -/
def comparisonBlank (x y : n → ℝ) : Fin 4 × n → ℝ :=
  fun ci => (![x,0,y,0] ci.1) ci.2

def jointRecordedComparison (a p : ℝ) (C : Matrix n n ℝ) :=
  (fullStep a p) ⊗ₖ C

theorem owned_comparison_factors (a p : ℝ) (C : Matrix n n ℝ) :
    jointRecordedComparison a p C=
      ((fullStep a p) ⊗ₖ (1 : Matrix n n ℝ))*
        ((1 : Matrix (Fin 4) (Fin 4) ℝ) ⊗ₖ C) := by
  rw [← Matrix.mul_kronecker_mul]
  simp [jointRecordedComparison]

theorem tensor_orthogonal {m : Type*} [Fintype m] [DecidableEq m]
    (W : Matrix m m ℝ) (C : Matrix n n ℝ)
    (hW : W.transpose*W=1) (hC : C.transpose*C=1) :
    (W ⊗ₖ C).transpose*(W ⊗ₖ C)=1 := by
  rw [← Matrix.kroneckerMap_transpose,← Matrix.mul_kronecker_mul,hW,hC]
  exact Matrix.one_kronecker_one

theorem owned_comparison_orthogonal (a p : ℝ) (C : Matrix n n ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hC : C.transpose*C=1) :
    (jointRecordedComparison a p C).transpose*jointRecordedComparison a p C=1 :=
  tensor_orthogonal _ _ (fullStep_orthogonal a p ha hp) hC

theorem tensor_reads_complete_blank_pair (W : Matrix (Fin 4) (Fin 4) ℝ)
    (C : Matrix n n ℝ) (x y : n → ℝ) (c : Fin 4) (i : n) :
    (W ⊗ₖ C).mulVec (comparisonBlank x y) (c,i)=
      W.mulVec ![C.mulVec x i,0,C.mulVec y i,0] c := by
  simp [comparisonBlank,Matrix.mulVec,dotProduct,Fintype.sum_prod_type,
    Fin.sum_univ_succ,Finset.mul_sum,mul_assoc]

theorem complete_owned_comparison_reading (a p : ℝ) (C : Matrix n n ℝ)
    (x y : n → ℝ) (c : Fin 4) (i : n) :
    (jointRecordedComparison a p C).mulVec (comparisonBlank x y) (c,i)=
      recordedResponseState a p (C.mulVec x) (C.mulVec y) c i := by
  exact tensor_reads_complete_blank_pair _ _ _ _ _ _

theorem blank_pair_has_fixed_norm (x y : n → ℝ) :
    responseNormSq (comparisonBlank x y)=responseNormSq x+responseNormSq y := by
  simp [responseNormSq,comparisonBlank,Fintype.sum_prod_type,Fin.sum_univ_succ]

/-- Preparation flag and comparison record stay in the complete joint operator. -/
def fullFlaggedComparison (a p : ℝ) (P U : Matrix n n ℝ) :=
  jointRecordedComparison a p (liftOperator U*flaggedPreparation P)

theorem full_flagged_comparison_orthogonal (a p : ℝ) (P U : Matrix n n ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hP : P*P=P) (hsP : P.transpose=P)
    (hU : U.transpose*U=1) :
    (fullFlaggedComparison a p P U).transpose*fullFlaggedComparison a p P U=1 := by
  apply owned_comparison_orthogonal a p _ ha hp
  have hlu : (liftOperator U).transpose*liftOperator U=1 := by
    rw [← lift_transpose,← lift_mul,hU,lift_one]
  exact orthogonal_composition _ _ hlu (flagged_preparation_orthogonal P hP hsP)

theorem common_word_after_flag (P U : Matrix n n ℝ) (x : n → ℝ) :
    (liftOperator U*flaggedPreparation P).mulVec (Sum.elim x 0)=
      Sum.elim ((U*P).mulVec x) ((U*(1-P)).mulVec x) := by
  rw [← Matrix.mulVec_mulVec,flagged_blank_preparation]
  simp [liftOperator,Matrix.fromBlocks_mulVec,Matrix.mulVec_mulVec]

theorem complete_flagged_detector_amplitude (a p : ℝ) (P U : Matrix n n ℝ)
    (x y : n → ℝ) (i : n) :
    (fullFlaggedComparison a p P U).mulVec
      (comparisonBlank (Sum.elim x 0) (Sum.elim y 0)) (0,Sum.inl i)=
      a*((U*P).mulVec x i)-p*((U*P).mulVec y i) := by
  unfold fullFlaggedComparison
  rw [complete_owned_comparison_reading,common_word_after_flag,common_word_after_flag,
    owned_recorded_response_coordinates]
  rfl

theorem retained_flag_detector_is_feedback_reading (a p : ℝ) (P U : Matrix n n ℝ)
    (x y : n → ℝ) :
    responseNormSq ((1-P).mulVec (fun i =>
      (fullFlaggedComparison a p P U).mulVec
        (comparisonBlank (Sum.elim x 0) (Sum.elim y 0)) (0,Sum.inl i)))=
      firstRecordedResponse a p (feedbackReadingOperator P U) x y := by
  simp_rw [complete_flagged_detector_amplitude]
  unfold firstRecordedResponse
  rw [owned_recorded_response_coordinates]
  congr 1
  change (1-P).mulVec (a • ((U*P).mulVec x)-p • ((U*P).mulVec y))=
    a • ((feedbackReadingOperator P U).mulVec x)-p • ((feedbackReadingOperator P U).mulVec y)
  rw [Matrix.mulVec_sub,Matrix.mulVec_smul,Matrix.mulVec_smul,
    Matrix.mulVec_mulVec,Matrix.mulVec_mulVec]
  simp [feedbackReadingOperator,Matrix.mul_assoc]

/-- An orthogonal stage has a reversible state map on the complete carrier. -/
def orthogonalStateEquiv (M : Matrix n n ℝ) (hM : M.transpose*M=1) :
    (n → ℝ) ≃ (n → ℝ) where
  toFun := M.mulVec
  invFun := M.transpose.mulVec
  left_inv x := by rw [Matrix.mulVec_mulVec,hM,Matrix.one_mulVec]
  right_inv x := by rw [Matrix.mulVec_mulVec,mul_eq_one_comm.mp hM,Matrix.one_mulVec]

/-- Stage selection is stored in the owned internal clock. -/
def threeInternalStages {S : Type*} (A B C : S ≃ S) :
    D0.Representation.FiniteProtocolClock.Clock → S ≃ S :=
  fun c => if c=0 then A else if c=1 then B else if c=2 then C else Equiv.refl S

theorem three_stage_run_is_internal {S : Type*} (A B C : S ≃ S) (x : S) :
    D0.Representation.FiniteProtocolClock.run (threeInternalStages A B C) x 3=
      (3,C (B (A x))) := by
  have h10 : (1 : D0.Representation.FiniteProtocolClock.Clock)≠0 := by decide
  have h20 : (2 : D0.Representation.FiniteProtocolClock.Clock)≠0 := by decide
  have h21 : (2 : D0.Representation.FiniteProtocolClock.Clock)≠1 := by decide
  norm_num [D0.Representation.FiniteProtocolClock.run,D0.Representation.FiniteProtocolClock.step,
    threeInternalStages,h10,h20,h21]

/-- Explicit stage program: flag, identical old-word execution, then owned recording. -/
def flaggedComparisonProgram (a p : ℝ) (P U : Matrix n n ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hP : P*P=P) (hsP : P.transpose=P)
    (hU : U.transpose*U=1) :
    D0.Representation.FiniteProtocolClock.Clock →
      (Fin 4 × (n ⊕ n) → ℝ) ≃ (Fin 4 × (n ⊕ n) → ℝ) := by
  have hA := tensor_orthogonal (1 : Matrix (Fin 4) (Fin 4) ℝ) _
    (by simp) (flagged_preparation_orthogonal P hP hsP)
  have hLU : (liftOperator U).transpose*liftOperator U=1 := by
    rw [← lift_transpose,← lift_mul,hU,lift_one]
  have hB := tensor_orthogonal (1 : Matrix (Fin 4) (Fin 4) ℝ) _ (by simp) hLU
  have hC := tensor_orthogonal (fullStep a p) (1 : Matrix (n ⊕ n) (n ⊕ n) ℝ)
    (fullStep_orthogonal a p ha hp) (by simp)
  exact threeInternalStages (orthogonalStateEquiv _ hA)
    (orthogonalStateEquiv _ hB) (orthogonalStateEquiv _ hC)

theorem complete_comparison_has_internal_program (a p : ℝ) (P U : Matrix n n ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hP : P*P=P) (hsP : P.transpose=P)
    (hU : U.transpose*U=1) (x : Fin 4 × (n ⊕ n) → ℝ) :
    D0.Representation.FiniteProtocolClock.run (flaggedComparisonProgram a p P U ha hp hP hsP hU) x 3=
      (3,(fullFlaggedComparison a p P U).mulVec x) ∧
    Function.Injective (D0.Representation.FiniteProtocolClock.step
      (flaggedComparisonProgram a p P U ha hp hP hsP hU)) := by
  constructor
  · unfold flaggedComparisonProgram
    rw [three_stage_run_is_internal]
    congr 1
    change (((fullStep a p) ⊗ₖ 1).mulVec
      (((1 : Matrix (Fin 4) (Fin 4) ℝ) ⊗ₖ liftOperator U).mulVec
        (((1 : Matrix (Fin 4) (Fin 4) ℝ) ⊗ₖ flaggedPreparation P).mulVec x)))=
          (fullFlaggedComparison a p P U).mulVec x
    rw [Matrix.mulVec_mulVec,Matrix.mulVec_mulVec,← Matrix.mul_kronecker_mul,
      ← Matrix.mul_kronecker_mul]
    simp [fullFlaggedComparison,jointRecordedComparison]
  · exact D0.Representation.FiniteProtocolClock.step_loses_no_state _

end RecordedQuadraticFeedback

section JointBootstrap
variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

def thermalPartition (beta : ℝ) (lambda : n → ℝ) :=
  ∑ i, Real.exp (-beta*lambda i)

def heatContribution (beta : ℝ) (lambda : n → ℝ) :=
  beta⁻¹*Real.log (thermalPartition beta lambda)

def thermalSource (beta : ℝ) (lambda v : n → ℝ) :=
  -(∑ i, Real.exp (-beta*lambda i)*v i)/thermalPartition beta lambda

def replicatedSpectrum (lambda : n → ℝ) : n ⊕ n → ℝ := Sum.elim lambda lambda

/-- Real coefficient extension of the actual rational scene heat readout. -/
def sceneZoneHeatReal (z : Fin 3) (x : ℝ) :=
  (D0.Synthesis.SceneHeatKernel.nzN z : ℝ)/33+
    (1-(D0.Synthesis.SceneHeatKernel.nzN z : ℝ)/33)*x^33+
    ((D0.Synthesis.SceneHeatKernel.nzN z : ℝ)-1)*x^(D0.Synthesis.SceneHeatKernel.dzN z)

theorem actual_scene_zone_heat_real_extension (z : Fin 3) (x : ℚ) :
    sceneZoneHeatReal z (x : ℝ)=(D0.Synthesis.SceneHeatKernel.zoneHeat z x : ℝ) := by
  simp [sceneZoneHeatReal,D0.Synthesis.SceneHeatKernel.zoneHeat,
    D0.Synthesis.SceneHeatKernel.nz]

theorem actual_scene_heat_polynomial (x : ℝ) :
    sceneZoneHeatReal 0 x+sceneZoneHeatReal 1 x+sceneZoneHeatReal 2 x=
      1+12*x^20+10*x^22+8*x^24+2*x^33 := by
  norm_num [sceneZoneHeatReal,D0.Synthesis.SceneHeatKernel.nzN,
    D0.Synthesis.SceneHeatKernel.dzN,Fin.ext_iff]
  ring

theorem thermal_partition_positive (beta : ℝ) (lambda : n → ℝ) :
    0<thermalPartition beta lambda := by
  unfold thermalPartition
  exact Finset.sum_pos (fun i _ => Real.exp_pos _) Finset.univ_nonempty

theorem replicated_thermal_partition (beta : ℝ) (lambda : n → ℝ) :
    thermalPartition beta (replicatedSpectrum lambda)=2*thermalPartition beta lambda := by
  simp [thermalPartition,replicatedSpectrum,Fintype.sum_sum_type,two_mul]

theorem replicated_heat_contribution (beta : ℝ) (lambda : n → ℝ) :
    heatContribution beta (replicatedSpectrum lambda)=
      heatContribution beta lambda+beta⁻¹*Real.log 2 := by
  unfold heatContribution
  rw [replicated_thermal_partition,Real.log_mul (by norm_num)
    (ne_of_gt (thermal_partition_positive beta lambda))]
  ring

theorem thermal_partition_uniform_shift (beta t : ℝ) (lambda : n → ℝ) :
    thermalPartition beta (fun i => lambda i+t)=
      Real.exp (-beta*t)*thermalPartition beta lambda := by
  simp only [thermalPartition,mul_add,neg_add_rev,Real.exp_add,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem thermal_heat_uniform_shift (beta t : ℝ) (lambda : n → ℝ) (hb : beta≠0) :
    heatContribution beta (fun i => lambda i+t)=heatContribution beta lambda-t := by
  unfold heatContribution
  rw [thermal_partition_uniform_shift,Real.log_mul
    (ne_of_gt (Real.exp_pos _)) (ne_of_gt (thermal_partition_positive beta lambda)),Real.log_exp]
  field_simp
  ring

theorem genuine_thermal_source (beta t : ℝ) (lambda : ℝ → n → ℝ) (v : n → ℝ)
    (hb : beta≠0) (h : ∀ i, HasDerivAt (fun s => lambda s i) (v i) t) :
    HasDerivAt (fun s => heatContribution beta (lambda s)) (thermalSource beta (lambda t) v) t := by
  have hz : HasDerivAt (fun s => thermalPartition beta (lambda s))
      (∑ i,Real.exp (-beta*lambda t i)*(-beta*v i)) t := by
    exact HasDerivAt.fun_sum (fun i _ => (h i |>.const_mul (-beta)).exp)
  have hp := (hz.log (ne_of_gt (thermal_partition_positive beta (lambda t)))).const_mul beta⁻¹
  convert hp using 1
  unfold thermalSource
  rw [show (∑ i,Real.exp (-beta*lambda t i)*(-beta*v i))=
      (-beta)*(∑ i,Real.exp (-beta*lambda t i)*v i) by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring]
  field_simp

theorem replicated_thermal_source (beta : ℝ) (lambda v : n → ℝ) :
    thermalSource beta (replicatedSpectrum lambda) (replicatedSpectrum v)=thermalSource beta lambda v := by
  unfold thermalSource
  rw [replicated_thermal_partition]
  simp only [replicatedSpectrum,Fintype.sum_sum_type,Sum.elim_inl,Sum.elim_inr]
  ring

def bootstrapAction (beta z : ℝ) (lambda : n → ℝ) (P U : Matrix n n ℝ) :=
  heatContribution beta lambda+feedbackAction z (fullFeedback P U)

theorem bootstrap_replication (beta z : ℝ) (lambda : n → ℝ) (P U : Matrix n n ℝ) :
    bootstrapAction beta z (replicatedSpectrum lambda) (liftOperator P) (liftOperator U)=
      heatContribution beta lambda+beta⁻¹*Real.log 2+2*feedbackAction z (fullFeedback P U) := by
  rw [bootstrapAction,replicated_heat_contribution,full_feedback_refines,actual_feedback_action_refinement]

theorem genuine_bootstrap_source (beta z t source : ℝ)
    (lambda : ℝ → n → ℝ) (v : n → ℝ) (P U : ℝ → Matrix n n ℝ)
    (hb : beta≠0) (h : ∀ i, HasDerivAt (fun s => lambda s i) (v i) t)
    (hf : HasDerivAt (fun s => feedbackAction z (fullFeedback (P s) (U s))) source t) :
    HasDerivAt (fun s => bootstrapAction beta z (lambda s) (P s) (U s))
      (thermalSource beta (lambda t) v+source) t :=
  (genuine_thermal_source beta t lambda v hb h).add hf

theorem genuine_replicated_bootstrap_source (beta z t source : ℝ)
    (lambda : ℝ → n → ℝ) (v : n → ℝ) (P U : ℝ → Matrix n n ℝ)
    (hb : beta≠0) (h : ∀ i, HasDerivAt (fun s => lambda s i) (v i) t)
    (hf : HasDerivAt (fun s => feedbackAction z (fullFeedback (P s) (U s))) source t) :
    HasDerivAt (fun s => bootstrapAction beta z (replicatedSpectrum (lambda s))
      (liftOperator (P s)) (liftOperator (U s)))
      (thermalSource beta (lambda t) v+2*source) t := by
  have hh := (genuine_thermal_source beta t lambda v hb h).add_const (beta⁻¹*Real.log 2)
  simpa only [bootstrap_replication] using hh.add (hf.const_mul 2)

theorem joint_stationarity_transfer_iff (heat feedback : ℝ) :
    (heat+feedback=0 ∧ heat+2*feedback=0) ↔ (heat=0 ∧ feedback=0) := by
  constructor
  · rintro ⟨h0,h1⟩
    constructor <;> linarith
  · rintro ⟨rfl,rfl⟩
    norm_num

theorem coarse_onshell_refined_residual (heat feedback : ℝ) (h : heat+feedback=0) :
    heat+2*feedback=feedback := by linarith

theorem compatible_refined_thermal_source_iff (heat feedback fineHeat : ℝ)
    (h : heat+feedback=0) :
    fineHeat+2*feedback=0 ↔ fineHeat=2*heat := by constructor <;> intro hh <;> linarith

theorem universal_single_calibration_obstruction (copies calibration : ℝ) :
    (∀ heat feedback : ℝ, heat+copies*feedback=calibration*(heat+feedback)) ↔
      (copies=1 ∧ calibration=1) := by
  constructor
  · intro h
    have hH := h 1 0
    have hF := h 0 1
    constructor <;> norm_num at hH hF ⊢ <;> linarith
  · rintro ⟨rfl,rfl⟩
    intro heat feedback
    ring

theorem bootstrap_uniform_spectral_shift (beta z t : ℝ) (lambda : n → ℝ)
    (P U : Matrix n n ℝ) (hb : beta≠0) :
    bootstrapAction beta z (fun i => lambda i+t) P U=
      bootstrapAction beta z lambda P U-t := by
  rw [bootstrapAction,thermal_heat_uniform_shift beta t lambda hb,bootstrapAction]
  ring

theorem genuine_bootstrap_uniform_shift_source (beta z t : ℝ) (lambda : n → ℝ)
    (P U : Matrix n n ℝ) (hb : beta≠0) :
    HasDerivAt (fun s => bootstrapAction beta z (fun i => lambda i+s) P U) (-1) t := by
  simpa only [bootstrap_uniform_spectral_shift beta z _ lambda P U hb] using
    (hasDerivAt_id t).const_sub (bootstrapAction beta z lambda P U)

theorem uniform_spectral_shift_cannot_be_stationary (beta z t : ℝ) (lambda : n → ℝ)
    (P U : Matrix n n ℝ) (hb : beta≠0) :
    ¬ HasDerivAt (fun s => bootstrapAction beta z (fun i => lambda i+s) P U) 0 t := by
  intro h
  have he := (genuine_bootstrap_uniform_shift_source beta z t lambda P U hb).unique h
  norm_num at he

/-- An independent finite control. Its coupled one-parameter variation is not
    asserted to be the physical scene variation, or the whole joint root gate. -/
def controlProjection : Matrix (Fin 2) (Fin 2) ℝ := Matrix.diagonal ![1,0]
def controlLaplacian (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := t • !![1,-1;-1,1]
def controlSpectrum (t : ℝ) : Fin 2 → ℝ := ![0,2*t]
def controlFeedbackAction (t : ℝ) := 2*Real.log (1+t^2)-Real.log (1+t^4)
def controlFeedbackSource (t : ℝ) := 4*t*(1-t^2)/((1+t^2)*(1+t^4))
def controlHeatSource (t : ℝ) := -(2*Real.exp (-2*t))/(1+Real.exp (-2*t))
def controlJointSource (t : ℝ) := controlHeatSource t+controlFeedbackSource t

theorem control_projection_is_orthogonal :
    controlProjection.transpose=controlProjection ∧ controlProjection*controlProjection=controlProjection := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [controlProjection,Matrix.mul_apply,Fin.sum_univ_succ]

theorem control_laplacian_has_declared_spectrum (t : ℝ) :
    (controlLaplacian t).mulVec ![1,1]=0 ∧
      (controlLaplacian t).mulVec ![1,-1]=(2*t) • ![1,-1] := by
  constructor <;> ext i <;> fin_cases i <;>
    simp [controlLaplacian,Matrix.mulVec,Fin.sum_univ_succ,Matrix.vecHead,Matrix.vecTail] <;> ring

theorem control_feedback_determinant (t : ℝ) :
    (1-(1/2 : ℝ) • fullFeedback controlProjection (cayleyAxis t)).det=
      (1+t^4)/(1+t^2)^2 := by
  have hn : 1+t^2≠0 := ne_of_gt (by positivity)
  simp [fullFeedback,controlProjection,cayleyAxis,Matrix.det_fin_two,
    Matrix.mul_apply,Fin.sum_univ_succ]
  field_simp
  ring

theorem control_feedback_pencil_positive (t : ℝ) :
    0<(1-(1/2 : ℝ) • fullFeedback controlProjection (cayleyAxis t)).det := by
  rw [control_feedback_determinant]
  positivity

theorem control_actual_feedback_action (t : ℝ) :
    feedbackAction (1/2) (fullFeedback controlProjection (cayleyAxis t))=controlFeedbackAction t := by
  unfold feedbackAction controlFeedbackAction
  rw [control_feedback_determinant,Real.log_div
    (ne_of_gt (by positivity : 0<(1+t^4 : ℝ)))
    (pow_ne_zero 2 (ne_of_gt (by positivity : 0<(1+t^2 : ℝ)))),Real.log_pow]
  ring

theorem control_genuine_feedback_source (t : ℝ) :
    HasDerivAt (fun s => feedbackAction (1/2) (fullFeedback controlProjection (cayleyAxis s)))
      (controlFeedbackSource t) t := by
  have h2 := (((hasDerivAt_id t).pow 2).const_add 1).log
    (ne_of_gt (by positivity : 0<(1+t^2 : ℝ)))
  have h4 := (((hasDerivAt_id t).pow 4).const_add 1).log
    (ne_of_gt (by positivity : 0<(1+t^4 : ℝ)))
  have h := (h2.const_mul 2).sub h4
  simp only [control_actual_feedback_action]
  convert h using 1
  unfold controlFeedbackSource
  simp only [Pi.pow_apply,id_eq,Nat.reduceSub,Nat.cast_ofNat,one_mul,mul_one]
  field_simp
  ring

theorem control_actual_heat_source (t : ℝ) :
    thermalSource 1 (controlSpectrum t) ![0,2]=controlHeatSource t := by
  simp [thermalSource,thermalPartition,controlSpectrum,controlHeatSource,Fin.sum_univ_succ]
  ring

theorem control_spectrum_derivative (t : ℝ) (i : Fin 2) :
    HasDerivAt (fun s => controlSpectrum s i) (![0,2] i) t := by
  fin_cases i
  · simpa [controlSpectrum] using hasDerivAt_const t (0 : ℝ)
  · simpa [controlSpectrum] using (hasDerivAt_id t).const_mul (2 : ℝ)

theorem control_genuine_joint_source (t : ℝ) :
    HasDerivAt (fun s => bootstrapAction 1 (1/2) (controlSpectrum s)
      controlProjection (cayleyAxis s)) (controlJointSource t) t := by
  simpa only [control_actual_heat_source,controlJointSource] using
    genuine_bootstrap_source 1 (1/2) t (controlFeedbackSource t)
      controlSpectrum ![0,2] (fun _ => controlProjection) cayleyAxis
      (by norm_num) (control_spectrum_derivative t) (control_genuine_feedback_source t)

theorem control_genuine_refined_source (t : ℝ) :
    HasDerivAt (fun s => bootstrapAction 1 (1/2) (replicatedSpectrum (controlSpectrum s))
      (liftOperator controlProjection) (liftOperator (cayleyAxis s)))
      (controlHeatSource t+2*controlFeedbackSource t) t := by
  simpa only [control_actual_heat_source] using
    genuine_replicated_bootstrap_source 1 (1/2) t (controlFeedbackSource t)
      controlSpectrum ![0,2] (fun _ => controlProjection) cayleyAxis
      (by norm_num) (control_spectrum_derivative t) (control_genuine_feedback_source t)

theorem control_joint_source_continuous : Continuous controlJointSource := by
  unfold controlJointSource controlHeatSource controlFeedbackSource
  have he : ∀ t : ℝ, 1+Real.exp (-2*t)≠0 := fun t => ne_of_gt (by positivity)
  have hq : ∀ t : ℝ, (1+t^2)*(1+t^4)≠0 := fun t => ne_of_gt (by positivity)
  fun_prop

theorem control_feedback_source_positive (t : ℝ) (ht : 0<t) (hb : t<1/2) :
    0<controlFeedbackSource t := by
  unfold controlFeedbackSource
  have h : 0<1-t^2 := by nlinarith
  positivity

theorem control_slice_stationary_refinement_failure :
    ∃ t : ℝ, 0<t ∧ t<1/2 ∧
      HasDerivAt (fun s => bootstrapAction 1 (1/2) (controlSpectrum s)
        controlProjection (cayleyAxis s)) 0 t ∧
      HasDerivAt (fun s => bootstrapAction 1 (1/2) (replicatedSpectrum (controlSpectrum s))
        (liftOperator controlProjection) (liftOperator (cayleyAxis s)))
        (controlFeedbackSource t) t ∧ 0<controlFeedbackSource t := by
  have h0 : controlJointSource 0=-1 := by
    norm_num [controlJointSource,controlHeatSource,controlFeedbackSource]
  have h1 : 0<controlJointSource (1/2) := by
    have he : Real.exp (-1 : ℝ)≤1 := Real.exp_le_one_iff.mpr (by norm_num)
    have hp : 0<1+Real.exp (-1 : ℝ) := by positivity
    have hheat : -(2*Real.exp (-1 : ℝ))/(1+Real.exp (-1 : ℝ))≥-1 := by
      apply (le_div_iff₀ hp).2
      linarith
    have hf : controlFeedbackSource (1/2)=96/85 := by norm_num [controlFeedbackSource]
    have hh : controlHeatSource (1/2)=-(2*Real.exp (-1 : ℝ))/(1+Real.exp (-1 : ℝ)) := by
      norm_num [controlHeatSource]
    unfold controlJointSource
    rw [hh,hf]
    linarith
  obtain ⟨t,ht,hroot⟩ := intermediate_value_Icc (by norm_num : (0 : ℝ)≤1/2)
    control_joint_source_continuous.continuousOn (show (0 : ℝ) ∈ Set.Icc
      (controlJointSource 0) (controlJointSource (1/2)) from by
        constructor <;> linarith)
  have hleft : 0<t := lt_of_le_of_ne ht.1 (by intro he; subst t; rw [h0] at hroot; norm_num at hroot)
  have hright : t<1/2 := lt_of_le_of_ne ht.2 (by
    intro he
    rw [he] at hroot
    linarith)
  have hcoarse := control_genuine_joint_source t
  rw [hroot] at hcoarse
  have hbalance : controlHeatSource t+controlFeedbackSource t=0 := hroot
  have hfine := control_genuine_refined_source t
  rw [coarse_onshell_refined_residual _ _ hbalance] at hfine
  exact ⟨t,hleft,hright,hcoarse,hfine,control_feedback_source_positive t hleft hright⟩

end JointBootstrap

section CoupledSourceAlgebra
open scoped Kronecker
variable {n : Type*} [Fintype n] [DecidableEq n]
variable {k : Type*} [Field k]

def sourceConj (T : (Matrix n n k)ˣ) (A : Matrix n n k) :=
  (T : Matrix n n k)*A*(↑T⁻¹ : Matrix n n k)
def matrixBracket (A B : Matrix n n k) := A*B-B*A
def sourceActive (D A : Matrix n n k) :=
  (-1/2840 : k) • (matrixBracket D A * matrixBracket D A)
def sourceDegree (D : Matrix n n k) :=
  (1/8 : k) • ((D-(22 : k) • 1)*(D-(20 : k) • 1))
def sourceCompression (D P : Matrix n n k) := P*sourceDegree D*P
def sourcePort (D P : Matrix n n k) :=
  (sourceCompression D P).trace⁻¹ • sourceCompression D P
def sourceInput (D P : Matrix n n k) := P-sourcePort D P
def sourceCoupled (R : Matrix n n k) (L : Matrix (Fin 4) (Fin 4) k) :=
  (1-R) ⊗ₖ 1+R ⊗ₖ L

theorem source_conj_mul (T : (Matrix n n k)ˣ) (A B : Matrix n n k) :
    sourceConj T (A*B)=sourceConj T A*sourceConj T B := by
  simp [sourceConj,Matrix.mul_assoc]

theorem source_conj_one (T : (Matrix n n k)ˣ) : sourceConj T 1=1 := by
  simp [sourceConj]

theorem source_conj_sub (T : (Matrix n n k)ˣ) (A B : Matrix n n k) :
    sourceConj T (A-B)=sourceConj T A-sourceConj T B := by
  simp [sourceConj,Matrix.mul_sub,Matrix.sub_mul]

theorem source_conj_smul (T : (Matrix n n k)ˣ) (c : k) (A : Matrix n n k) :
    sourceConj T (c • A)=c • sourceConj T A := by
  simp [sourceConj,Matrix.mul_smul,Matrix.smul_mul]

theorem source_conj_trace (T : (Matrix n n k)ˣ) (A : Matrix n n k) :
    (sourceConj T A).trace=A.trace := by
  rw [sourceConj,Matrix.trace_mul_cycle]
  simp

theorem source_conj_det (T : (Matrix n n k)ˣ) (A : Matrix n n k) :
    (sourceConj T A).det=A.det := by
  rw [sourceConj,Matrix.det_mul,Matrix.det_mul]
  calc
    _ = A.det*((T : Matrix n n k)*(↑T⁻¹ : Matrix n n k)).det := by
      rw [Matrix.det_mul]; ring
    _ = A.det := by simp

theorem source_commutator_covariant (T : (Matrix n n k)ˣ) (D A : Matrix n n k) :
    matrixBracket (sourceConj T D) (sourceConj T A)=sourceConj T (matrixBracket D A) := by
  simp [matrixBracket,source_conj_sub,source_conj_mul]

theorem source_active_covariant (T : (Matrix n n k)ˣ) (D A : Matrix n n k) :
    sourceActive (sourceConj T D) (sourceConj T A)=sourceConj T (sourceActive D A) := by
  simp [sourceActive,source_commutator_covariant,source_conj_smul,source_conj_mul]

theorem source_degree_covariant (T : (Matrix n n k)ˣ) (D : Matrix n n k) :
    sourceDegree (sourceConj T D)=sourceConj T (sourceDegree D) := by
  simp [sourceDegree,source_conj_smul,source_conj_mul,source_conj_sub,source_conj_one]

theorem source_compression_covariant (T : (Matrix n n k)ˣ) (D P : Matrix n n k) :
    sourceCompression (sourceConj T D) (sourceConj T P)=sourceConj T (sourceCompression D P) := by
  simp [sourceCompression,source_degree_covariant,source_conj_mul]

theorem source_port_covariant (T : (Matrix n n k)ˣ) (D P : Matrix n n k) :
    sourcePort (sourceConj T D) (sourceConj T P)=sourceConj T (sourcePort D P) := by
  simp [sourcePort,source_compression_covariant,source_conj_trace,source_conj_smul]

theorem source_input_covariant (T : (Matrix n n k)ˣ) (D P : Matrix n n k) :
    sourceInput (sourceConj T D) (sourceConj T P)=sourceConj T (sourceInput D P) := by
  simp [sourceInput,source_port_covariant,source_conj_sub]

def sourceJointUnits (T : (Matrix n n k)ˣ) : (Matrix (n × Fin 4) (n × Fin 4) k)ˣ where
  val := (T : Matrix n n k) ⊗ₖ 1
  inv := (↑T⁻¹ : Matrix n n k) ⊗ₖ 1
  val_inv := by rw [← Matrix.mul_kronecker_mul]; simp
  inv_val := by rw [← Matrix.mul_kronecker_mul]; simp

theorem source_coupled_covariant (T : (Matrix n n k)ˣ) (R : Matrix n n k)
    (L : Matrix (Fin 4) (Fin 4) k) :
    sourceCoupled (sourceConj T R) L=sourceConj (sourceJointUnits T) (sourceCoupled R L) := by
  unfold sourceCoupled sourceConj sourceJointUnits
  simp only [Units.val_mk,Units.inv_mk,Matrix.mul_add,Matrix.add_mul]
  rw [← Matrix.mul_kronecker_mul,← Matrix.mul_kronecker_mul,
    ← Matrix.mul_kronecker_mul,← Matrix.mul_kronecker_mul]
  simp [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_assoc]

def operatorWord : List (Matrix n n k) → Matrix n n k
  | [] => 1
  | U::word => operatorWord word*U

theorem whole_source_word_covariant (T : (Matrix n n k)ˣ) (word : List (Matrix n n k)) :
    operatorWord (word.map (sourceConj T))=sourceConj T (operatorWord word) := by
  induction word with
  | nil => simp [operatorWord,source_conj_one]
  | cons U word ih => simp [operatorWord,ih,source_conj_mul]

def weightedAdjoint (G GI U : Matrix n n k) := GI*U.transpose*G
def movedMetric (T : (Matrix n n k)ˣ) (G : Matrix n n k) :=
  (↑T⁻¹ : Matrix n n k).transpose*G*(↑T⁻¹ : Matrix n n k)
def movedInverseMetric (T : (Matrix n n k)ˣ) (GI : Matrix n n k) :=
  (T : Matrix n n k)*GI*(T : Matrix n n k).transpose
def weightedFeedback (G GI P U : Matrix n n k) := P*weightedAdjoint G GI U*(1-P)*U*P

theorem weighted_adjoint_covariant (T : (Matrix n n k)ˣ) (G GI U : Matrix n n k) :
    weightedAdjoint (movedMetric T G) (movedInverseMetric T GI) (sourceConj T U)=
      sourceConj T (weightedAdjoint G GI U) := by
  unfold weightedAdjoint movedMetric movedInverseMetric sourceConj
  simp only [Matrix.transpose_mul]
  have h : (T : Matrix n n k).transpose*(↑T⁻¹ : Matrix n n k).transpose=1 := by
    rw [← Matrix.transpose_mul]; simp
  calc
    _ = (T : Matrix n n k)*GI*((T : Matrix n n k).transpose*(↑T⁻¹ : Matrix n n k).transpose)*
      U.transpose*((T : Matrix n n k).transpose*(↑T⁻¹ : Matrix n n k).transpose)*G*(↑T⁻¹ : Matrix n n k) := by
        noncomm_ring
    _ = _ := by rw [h]; simp [Matrix.mul_assoc]

theorem weighted_feedback_covariant (T : (Matrix n n k)ˣ) (G GI P U : Matrix n n k) :
    weightedFeedback (movedMetric T G) (movedInverseMetric T GI)
      (sourceConj T P) (sourceConj T U)=sourceConj T (weightedFeedback G GI P U) := by
  have hc : 1-sourceConj T P=sourceConj T (1-P) := by
    rw [source_conj_sub,source_conj_one]
  unfold weightedFeedback
  rw [weighted_adjoint_covariant,hc,← source_conj_mul,← source_conj_mul,
    ← source_conj_mul,← source_conj_mul]

theorem weighted_feedback_euclidean (P U : Matrix n n ℝ) :
    weightedFeedback 1 1 P U=fullFeedback P U := by
  simp [weightedFeedback,weightedAdjoint,fullFeedback]

def compressionJet (D P dD dP : Matrix n n k) :=
  dP*sourceDegree D*P+P*((1/8 : k) • (dD*(D-(20 : k) • 1)+(D-(22 : k) • 1)*dD))*P+
    P*sourceDegree D*dP
def portJet (M dM : Matrix n n k) := M.trace⁻¹ • dM-((M.trace^2)⁻¹*dM.trace) • M

theorem source_commutator_first_jet (D A dD dA : Matrix n n k) :
    (dD*A+D*dA)-(dA*D+A*dD)=matrixBracket dD A+matrixBracket D dA := by
  unfold matrixBracket
  noncomm_ring

theorem source_compression_frame_jet (D P O : Matrix n n k) :
    compressionJet D P (matrixBracket O D) (matrixBracket O P)=
      matrixBracket O (sourceCompression D P) := by
  unfold compressionJet sourceCompression sourceDegree matrixBracket
  simp only [Matrix.smul_mul,Matrix.mul_smul]
  rw [← smul_add,← smul_add,← smul_sub]
  congr 1
  simp only [← Algebra.algebraMap_eq_smul_one,map_ofNat]
  noncomm_ring

theorem trace_frame_jet_zero (O M : Matrix n n k) : (matrixBracket O M).trace=0 := by
  rw [matrixBracket,Matrix.trace_sub,Matrix.trace_mul_comm O M]
  simp

theorem source_port_frame_jet (M O : Matrix n n k) :
    portJet M (matrixBracket O M)=matrixBracket O (M.trace⁻¹ • M) := by
  rw [portJet,trace_frame_jet_zero]
  simp [matrixBracket,Matrix.mul_smul,Matrix.smul_mul,smul_sub]

end CoupledSourceAlgebra

section OperatorBootstrapWard
variable {n : Type*} [Fintype n] [DecidableEq n]

def matrixHeat (beta : ℝ) (Delta : Matrix n n ℝ) :=
  beta⁻¹*Real.log (NormedSpace.exp ((-beta) • Delta)).trace
def matrixBootstrap (beta z : ℝ) (Delta G GI P U : Matrix n n ℝ) :=
  matrixHeat beta Delta+feedbackAction z (weightedFeedback G GI P U)

theorem matrix_heat_similarity (beta : ℝ) (T : (Matrix n n ℝ)ˣ) (Delta : Matrix n n ℝ) :
    matrixHeat beta (sourceConj T Delta)=matrixHeat beta Delta := by
  unfold matrixHeat
  rw [← source_conj_smul T (-beta) Delta]
  have he : NormedSpace.exp (sourceConj T ((-beta) • Delta))=
      sourceConj T (NormedSpace.exp ((-beta) • Delta)) := by
    exact Matrix.exp_units_conj T _
  rw [he,source_conj_trace]

theorem matrix_heat_diagonal (beta : ℝ) (lambda : n → ℝ) :
    matrixHeat beta (Matrix.diagonal lambda)=heatContribution beta lambda := by
  unfold matrixHeat heatContribution thermalPartition
  rw [← Matrix.diagonal_smul,Matrix.exp_diagonal]
  simp [Matrix.trace,← Real.exp_eq_exp_ℝ]

theorem actual_matrix_heat_derivative (beta t : ℝ) (lambda : ℝ → n → ℝ)
    (frame : ℝ → (Matrix n n ℝ)ˣ) (v : n → ℝ) [Nonempty n]
    (hb : beta≠0) (h : ∀ i, HasDerivAt (fun s => lambda s i) (v i) t) :
    HasDerivAt (fun s => matrixHeat beta (sourceConj (frame s) (Matrix.diagonal (lambda s))))
      (thermalSource beta (lambda t) v) t := by
  simpa only [matrix_heat_similarity,matrix_heat_diagonal] using
    genuine_thermal_source beta t lambda v hb h

theorem feedback_action_similarity (z : ℝ) (T : (Matrix n n ℝ)ˣ) (F : Matrix n n ℝ) :
    feedbackAction z (sourceConj T F)=feedbackAction z F := by
  unfold feedbackAction
  have hc : 1-z • sourceConj T F=sourceConj T (1-z • F) := by
    rw [source_conj_sub,source_conj_one,source_conj_smul]
  rw [hc,source_conj_det]

theorem whole_operator_bootstrap_covariant (beta z : ℝ) (T : (Matrix n n ℝ)ˣ)
    (Delta G GI P U : Matrix n n ℝ) :
    matrixBootstrap beta z (sourceConj T Delta) (movedMetric T G) (movedInverseMetric T GI)
      (sourceConj T P) (sourceConj T U)=matrixBootstrap beta z Delta G GI P U := by
  simp [matrixBootstrap,matrix_heat_similarity,weighted_feedback_covariant,feedback_action_similarity]

theorem genuine_whole_basis_ward (beta z t : ℝ) (T : ℝ → (Matrix n n ℝ)ˣ)
    (Delta G GI P U : Matrix n n ℝ) :
    HasDerivAt (fun s => matrixBootstrap beta z (sourceConj (T s) Delta)
      (movedMetric (T s) G) (movedInverseMetric (T s) GI)
      (sourceConj (T s) P) (sourceConj (T s) U)) 0 t := by
  simpa only [whole_operator_bootstrap_covariant] using
    hasDerivAt_const t (matrixBootstrap beta z Delta G GI P U)

end OperatorBootstrapWard

section NativeSourceBinding
open D0.Representation.SourcePortPreparation
open D0.Integration.V15.RawZone (DW AW Pact)

theorem actual_source_active_binding :
    sourceActive (DW.map (fun z : ℤ => (z : ℚ))) (AW.map (fun z : ℤ => (z : ℚ)))=Pact := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [sourceActive,matrixBracket,DW,AW,Pact,Matrix.mul_apply,Fin.sum_univ_succ]

theorem actual_source_degree_binding : sourceDegree D=degreePort := rfl

theorem actual_source_compression_binding : sourceCompression D Pact=compressed := rfl

theorem actual_source_compression_positive : (sourceCompression D Pact).trace=567/710 := by
  have hD : D=(!![24,0,0;0,22,0;0,0,20] : Matrix (Fin 3) (Fin 3) ℚ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [D,DW]
  have hI : (1 : Matrix (Fin 3) (Fin 3) ℚ)=!![1,0,0;0,1,0;0,0,1] := by
    ext i j
    fin_cases i <;> fin_cases j <;> rfl
  have hE : sourceDegree D=(!![1,0,0;0,0,0;0,0,0] : Matrix (Fin 3) (Fin 3) ℚ) := by
    rw [sourceDegree,hD,hI]
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [Matrix.mul_apply,Fin.sum_univ_succ]
  rw [sourceCompression,hE]
  norm_num [Pact,Matrix.trace,Matrix.mul_apply,Fin.sum_univ_succ]

theorem actual_source_signal_binding : sourcePort D Pact=signalPort := by
  rw [sourcePort,actual_source_compression_positive]
  norm_num [signalPort,actual_source_compression_binding]

theorem actual_source_input_binding : sourceInput D Pact=inputPort := by
  rw [sourceInput,actual_source_signal_binding]
  rfl

theorem actual_source_interaction_binding :
    sourceCoupled signalPort (D0.Representation.OrderMemoryReadout.spin 2)=coupled := rfl

end NativeSourceBinding

section NativeOperatorDifferentiation
open scoped Matrix.Norms.Operator
variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

def matrixPowerJet (A V : Matrix n n ℝ) : ℕ → Matrix n n ℝ
  | 0 => 0
  | m+1 => matrixPowerJet A V m*A+A^m*V

theorem genuine_matrix_power_derivative (A : ℝ → Matrix n n ℝ) (V : Matrix n n ℝ) (t : ℝ)
    (h : HasDerivAt A V t) (m : ℕ) :
    HasDerivAt (fun s => A s^m) (matrixPowerJet (A t) V m) t := by
  induction m with
  | zero => simpa [matrixPowerJet] using hasDerivAt_const t (1 : Matrix n n ℝ)
  | succ m ih => simpa only [pow_succ,matrixPowerJet] using ih.mul h

theorem matrix_power_jet_trace (A V : Matrix n n ℝ) (m q : ℕ) :
    (matrixPowerJet A V m*A^q).trace=(m : ℝ)*(A^(m+q-1)*V).trace := by
  induction m generalizing q with
  | zero => simp [matrixPowerJet]
  | succ m ih =>
    have hc : (A^m*V*A^q).trace=(A^(m+q)*V).trace := by
      rw [Matrix.trace_mul_cycle,← pow_add,Nat.add_comm]
    simp only [matrixPowerJet,Matrix.add_mul,Matrix.trace_add,Matrix.mul_assoc]
    rw [← pow_succ',ih,← Matrix.mul_assoc (A^m) V (A^q),hc]
    have he : m+(q+1)-1=m+q := by omega
    have he2 : m+1+q-1=m+q := by omega
    rw [he,he2]
    push_cast
    ring

theorem genuine_trace_derivative (A : ℝ → Matrix n n ℝ) (V : Matrix n n ℝ) (t : ℝ)
    (h : HasDerivAt A V t) : HasDerivAt (fun s => (A s).trace) V.trace t := by
  let tr : Matrix n n ℝ →L[ℝ] ℝ := (Matrix.traceLinearMap n ℝ ℝ).toContinuousLinearMap
  exact tr.hasFDerivAt.comp_hasDerivAt t h

theorem genuine_source_compression_derivative (D P : ℝ → Matrix n n ℝ)
    (dD dP : Matrix n n ℝ) (t : ℝ)
    (hD : HasDerivAt D dD t) (hP : HasDerivAt P dP t) :
    HasDerivAt (fun s => sourceCompression (D s) (P s))
      (compressionJet (D t) (P t) dD dP) t := by
  have hE := ((hD.sub_const ((22 : ℝ) • (1 : Matrix n n ℝ))).mul
    (hD.sub_const ((20 : ℝ) • (1 : Matrix n n ℝ)))).const_smul (1/8 : ℝ)
  have h := (hP.mul hE).mul hP
  convert h using 1 <;> dsimp [sourceCompression,compressionJet,sourceDegree] <;> noncomm_ring

theorem genuine_source_port_derivative (D P : ℝ → Matrix n n ℝ)
    (dD dP : Matrix n n ℝ) (t : ℝ)
    (hD : HasDerivAt D dD t) (hP : HasDerivAt P dP t)
    (hn : (sourceCompression (D t) (P t)).trace≠0) :
    HasDerivAt (fun s => sourcePort (D s) (P s))
      (portJet (sourceCompression (D t) (P t)) (compressionJet (D t) (P t) dD dP)) t := by
  have hM := genuine_source_compression_derivative D P dD dP t hD hP
  have ht := genuine_trace_derivative _ _ t hM
  have h := (ht.inv hn).smul hM
  convert h using 1
  unfold portJet
  module

def wordJet : List (Matrix n n ℝ × Matrix n n ℝ) → Matrix n n ℝ
  | [] => 0
  | (U,V)::word => wordJet word*U+operatorWord (word.map Prod.fst)*V

theorem genuine_whole_native_word_derivative
    (stages : List ((ℝ → Matrix n n ℝ) × Matrix n n ℝ)) (t : ℝ)
    (h : ∀ stage ∈ stages, HasDerivAt stage.1 stage.2 t) :
    HasDerivAt (fun s => operatorWord (stages.map (fun stage => stage.1 s)))
      (wordJet (stages.map (fun stage => (stage.1 t,stage.2)))) t := by
  induction stages with
  | nil => simpa [operatorWord,wordJet] using hasDerivAt_const t (1 : Matrix n n ℝ)
  | cons stage stages ih =>
    have hs := h stage (by simp)
    have hr := ih (fun x hx => h x (by simp [hx]))
    simpa [operatorWord,wordJet,List.map_map,Function.comp_def] using hr.mul hs


def activeJet (D A dD dA : Matrix n n ℝ) :=
  let K := matrixBracket D A
  let dK := matrixBracket dD A+matrixBracket D dA
  (-1/2840 : ℝ) • (dK*K+K*dK)

theorem genuine_native_commutator_derivative (D A : ℝ → Matrix n n ℝ)
    (dD dA : Matrix n n ℝ) (t : ℝ) (hD : HasDerivAt D dD t) (hA : HasDerivAt A dA t) :
    HasDerivAt (fun s => matrixBracket (D s) (A s))
      (matrixBracket dD (A t)+matrixBracket (D t) dA) t := by
  convert (hD.mul hA).sub (hA.mul hD) using 1
  dsimp [matrixBracket]
  noncomm_ring

theorem genuine_native_active_derivative (D A : ℝ → Matrix n n ℝ)
    (dD dA : Matrix n n ℝ) (t : ℝ) (hD : HasDerivAt D dD t) (hA : HasDerivAt A dA t) :
    HasDerivAt (fun s => sourceActive (D s) (A s)) (activeJet (D t) (A t) dD dA) t := by
  have hK := genuine_native_commutator_derivative D A dD dA t hD hA
  exact (hK.mul hK).const_smul (-1/2840 : ℝ)

theorem genuine_native_port_from_primitives (D A : ℝ → Matrix n n ℝ)
    (dD dA : Matrix n n ℝ) (t : ℝ) (hD : HasDerivAt D dD t) (hA : HasDerivAt A dA t)
    (hn : (sourceCompression (D t) (sourceActive (D t) (A t))).trace≠0) :
    HasDerivAt (fun s => sourcePort (D s) (sourceActive (D s) (A s)))
      (portJet (sourceCompression (D t) (sourceActive (D t) (A t)))
        (compressionJet (D t) (sourceActive (D t) (A t)) dD (activeJet (D t) (A t) dD dA))) t := by
  exact genuine_source_port_derivative D (fun s => sourceActive (D s) (A s)) dD
    (activeJet (D t) (A t) dD dA) t hD (genuine_native_active_derivative D A dD dA t hD hA) hn

theorem native_active_frame_jet (D A O : Matrix n n ℝ) :
    activeJet D A (matrixBracket O D) (matrixBracket O A)=matrixBracket O (sourceActive D A) := by
  unfold activeJet sourceActive matrixBracket
  dsimp
  simp only [Matrix.smul_mul,Matrix.mul_smul]
  rw [← smul_sub]
  congr 1
  noncomm_ring

theorem genuine_transpose_derivative (U : ℝ → Matrix n n ℝ)
    (dU : Matrix n n ℝ) (t : ℝ) (hU : HasDerivAt U dU t) :
    HasDerivAt (fun s => (U s).transpose) dU.transpose t := by
  let tr : Matrix n n ℝ →L[ℝ] Matrix n n ℝ :=
    (Matrix.transposeLinearEquiv n n ℝ ℝ).toLinearMap.toContinuousLinearMap
  exact tr.hasFDerivAt.comp_hasDerivAt t hU

def weightedFeedbackJet (G GI P U dG dGI dP dU : Matrix n n ℝ) :=
  dP*GI*U.transpose*G*(1-P)*U*P+
  P*dGI*U.transpose*G*(1-P)*U*P+
  P*GI*dU.transpose*G*(1-P)*U*P+
  P*GI*U.transpose*dG*(1-P)*U*P-
  P*GI*U.transpose*G*dP*U*P+
  P*GI*U.transpose*G*(1-P)*dU*P+
  P*GI*U.transpose*G*(1-P)*U*dP

theorem genuine_weighted_feedback_derivative (G GI P U : ℝ → Matrix n n ℝ)
    (dG dGI dP dU : Matrix n n ℝ) (t : ℝ)
    (hG : HasDerivAt G dG t) (hGI : HasDerivAt GI dGI t)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t) :
    HasDerivAt (fun s => weightedFeedback (G s) (GI s) (P s) (U s))
      (weightedFeedbackJet (G t) (GI t) (P t) (U t) dG dGI dP dU) t := by
  have ht := genuine_transpose_derivative U dU t hU
  have h := ((((((hP.mul hGI).mul ht).mul hG).mul
    ((hasDerivAt_const t (1 : Matrix n n ℝ)).sub hP)).mul hU).mul hP)
  convert h using 1
  · funext s
    dsimp [weightedFeedback,weightedAdjoint]
    noncomm_ring
  · dsimp [weightedFeedbackJet]
    noncomm_ring

theorem genuine_inverse_metric_jet (G GI : ℝ → Matrix n n ℝ)
    (dG dGI : Matrix n n ℝ) (t : ℝ) (hG : HasDerivAt G dG t) (hGI : HasDerivAt GI dGI t)
    (h : ∀ s, G s*GI s=1) (hleft : GI t*G t=1) : dGI= -GI t*dG*GI t := by
  have hf : G*GI=(fun _ => (1 : Matrix n n ℝ)) := by
    funext s
    exact h s
  have hz : dG*GI t+G t*dGI=0 :=
    (hG.mul hGI).unique (by rw [hf]; exact hasDerivAt_const t (1 : Matrix n n ℝ))
  have hz' := congrArg (fun X => GI t*X) hz
  simp only [Matrix.mul_add,← Matrix.mul_assoc,hleft,one_mul,mul_zero] at hz'
  have he : dGI= -(GI t*dG*GI t) := eq_neg_iff_add_eq_zero.mpr (by simpa [add_comm] using hz')
  simpa only [Matrix.neg_mul] using he

theorem whole_weighted_feedback_frame_jet (G GI P U O : Matrix n n ℝ) :
    weightedFeedbackJet G GI P U (-(O.transpose*G+G*O))
      (O*GI+GI*O.transpose) (matrixBracket O P) (matrixBracket O U)=
      matrixBracket O (weightedFeedback G GI P U) := by
  unfold weightedFeedbackJet weightedFeedback weightedAdjoint matrixBracket
  simp only [Matrix.transpose_sub,Matrix.transpose_mul,Matrix.transpose_transpose]
  noncomm_ring


theorem genuine_kronecker_right_derivative (R : ℝ → Matrix n n ℝ)
    (L : Matrix (Fin 4) (Fin 4) ℝ) (dR : Matrix n n ℝ) (t : ℝ) (hR : HasDerivAt R dR t) :
    HasDerivAt (fun s => Matrix.kronecker (R s) L) (Matrix.kronecker dR L) t := by
  let lin : Matrix n n ℝ →ₗ[ℝ] Matrix (n × Fin 4) (n × Fin 4) ℝ :=
    { toFun := fun X => Matrix.kronecker X L
      map_add' := fun X Y => Matrix.add_kronecker X Y L
      map_smul' := fun c X => Matrix.smul_kronecker c X L }
  let cl : Matrix n n ℝ →L[ℝ] Matrix (n × Fin 4) (n × Fin 4) ℝ := lin.toContinuousLinearMap
  exact cl.hasFDerivAt.comp_hasDerivAt t hR

theorem genuine_native_coupled_derivative (R : ℝ → Matrix n n ℝ)
    (L : Matrix (Fin 4) (Fin 4) ℝ) (dR : Matrix n n ℝ) (t : ℝ) (hR : HasDerivAt R dR t) :
    HasDerivAt (fun s => sourceCoupled (R s) L) (Matrix.kronecker dR (L-1)) t := by
  have hleft := genuine_kronecker_right_derivative (fun s => 1-R s) 1 (-dR) t
    (by simpa using (hasDerivAt_const t (1 : Matrix n n ℝ)).sub hR)
  have hright := genuine_kronecker_right_derivative R L dR t hR
  have he : Matrix.kronecker dR (L-1)=Matrix.kronecker (-dR) 1+Matrix.kronecker dR L := by
    ext i j
    simp [Matrix.kroneckerMap,Matrix.kronecker]
    ring
  rw [he]
  exact hleft.add hright

theorem genuine_native_input_from_primitives (D A : ℝ → Matrix n n ℝ)
    (dD dA : Matrix n n ℝ) (t : ℝ) (hD : HasDerivAt D dD t) (hA : HasDerivAt A dA t)
    (hn : (sourceCompression (D t) (sourceActive (D t) (A t))).trace≠0) :
    HasDerivAt (fun s => sourceInput (D s) (sourceActive (D s) (A s)))
      (activeJet (D t) (A t) dD dA-
        portJet (sourceCompression (D t) (sourceActive (D t) (A t)))
          (compressionJet (D t) (sourceActive (D t) (A t)) dD (activeJet (D t) (A t) dD dA))) t := by
  exact (genuine_native_active_derivative D A dD dA t hD hA).sub
    (genuine_native_port_from_primitives D A dD dA t hD hA hn)

theorem genuine_native_interaction_from_primitives (D A : ℝ → Matrix n n ℝ)
    (L : Matrix (Fin 4) (Fin 4) ℝ) (dD dA : Matrix n n ℝ) (t : ℝ)
    (hD : HasDerivAt D dD t) (hA : HasDerivAt A dA t)
    (hn : (sourceCompression (D t) (sourceActive (D t) (A t))).trace≠0) :
    HasDerivAt (fun s => sourceCoupled (sourcePort (D s) (sourceActive (D s) (A s))) L)
      (Matrix.kronecker
        (portJet (sourceCompression (D t) (sourceActive (D t) (A t)))
          (compressionJet (D t) (sourceActive (D t) (A t)) dD (activeJet (D t) (A t) dD dA))) (L-1)) t := by
  exact genuine_native_coupled_derivative _ L _ t
    (genuine_native_port_from_primitives D A dD dA t hD hA hn)

end NativeOperatorDifferentiation

end
noncomputable section HistorySpectralNaturality
variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Complete native preparation frame inverse, with its two histories retained. -/
def nativePreparationFrameInverse (a p : ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  preparationCoordinatesInverse (n:=n) a p*(ownedGoldenFactor (n:=n) a p).transpose

/-- Both directions of the exact inverse, not a supplied inverse oracle. -/
theorem native_preparation_frame_inverse (a p : ℝ) (hp : p≠0) (hg : a^2+p^2=1) :
    nativePreparationFrame (n:=n) a p*nativePreparationFrameInverse (n:=n) a p=1 ∧
    nativePreparationFrameInverse (n:=n) a p*nativePreparationFrame (n:=n) a p=1 := by
  have ht := preparation_coordinates_inverse (n:=n) a p hp
  have ho := golden_factor_orthogonal (n:=n) a p hg
  have hor := mul_eq_one_comm.mp ho
  constructor
  · change (ownedGoldenFactor (n:=n) a p*preparationCoordinates (n:=n) a p)*
      (preparationCoordinatesInverse (n:=n) a p*(ownedGoldenFactor (n:=n) a p).transpose)=1
    calc
      _ = ownedGoldenFactor (n:=n) a p*
          (preparationCoordinates (n:=n) a p*preparationCoordinatesInverse (n:=n) a p)*
          (ownedGoldenFactor (n:=n) a p).transpose := by simp [Matrix.mul_assoc]
      _ = 1 := by rw [ht.1,Matrix.mul_one,hor]
  · change (preparationCoordinatesInverse (n:=n) a p*(ownedGoldenFactor (n:=n) a p).transpose)*
      (ownedGoldenFactor (n:=n) a p*preparationCoordinates (n:=n) a p)=1
    calc
      _ = preparationCoordinatesInverse (n:=n) a p*
          ((ownedGoldenFactor (n:=n) a p).transpose*ownedGoldenFactor (n:=n) a p)*
          preparationCoordinates (n:=n) a p := by simp [Matrix.mul_assoc]
      _ = 1 := by rw [ho,Matrix.mul_one,ht.2]

/-- Scalar golden preparation coordinates commute with every literal cylinder operator. -/
theorem preparation_coordinates_commute_lift (a p : ℝ) (D : Matrix n n ℝ) :
    preparationCoordinates a p*liftOperator D=liftOperator D*preparationCoordinates a p := by
  simp only [preparationCoordinates,liftOperator,Matrix.fromBlocks_multiply,
    Matrix.mul_smul,Matrix.smul_mul,Matrix.mul_one,Matrix.one_mul,
    Matrix.mul_zero,Matrix.zero_mul,smul_zero,add_zero,zero_add]

/-- The complete frame commutes with the old scene operator lifted to both children. -/
theorem native_preparation_frame_commutes_lift (a p : ℝ) (D : Matrix n n ℝ) :
    nativePreparationFrame (n:=n) a p*liftOperator D=liftOperator D*nativePreparationFrame (n:=n) a p := by
  simp only [nativePreparationFrame,Matrix.mul_assoc]
  rw [preparation_coordinates_commute_lift,← Matrix.mul_assoc,
      golden_factor_commutes_literal_readout,Matrix.mul_assoc]

/-- Bundled defect for both actual preparations J and GJ. Its columns are the two
history intertwining defects; no stationarity is inserted in its definition. -/
def historySpectralDefect (a p : ℝ) (fine : Matrix (n ⊕ n) (n ⊕ n) ℝ)
    (coarse : Matrix n n ℝ) :=
  fine*nativePreparationFrame (n:=n) a p-nativePreparationFrame (n:=n) a p*liftOperator coarse

/-- The full spectral change is reconstructed from the two history defects. -/
theorem history_spectral_defect_reconstructs (a p : ℝ)
    (fine : Matrix (n ⊕ n) (n ⊕ n) ℝ) (coarse : Matrix n n ℝ)
    (hp : p≠0) (hg : a^2+p^2=1) :
    historySpectralDefect a p fine coarse*nativePreparationFrameInverse (n:=n) a p=
      fine-liftOperator coarse := by
  have hi := (native_preparation_frame_inverse (n:=n) a p hp hg).1
  unfold historySpectralDefect
  rw [native_preparation_frame_commutes_lift,Matrix.sub_mul]
  simp [Matrix.mul_assoc,hi]

/-- Complete classification of all finite operators preserving both actual history
intertwinings. No self-adjointness, positivity, or physical admission is assumed. -/
theorem history_spectral_zero_defect_iff (a p : ℝ)
    (fine : Matrix (n ⊕ n) (n ⊕ n) ℝ) (coarse : Matrix n n ℝ)
    (hp : p≠0) (hg : a^2+p^2=1) :
    historySpectralDefect a p fine coarse=0 ↔ fine=liftOperator coarse := by
  constructor
  · intro he
    have hr := history_spectral_defect_reconstructs a p fine coarse hp hg
    rw [he,Matrix.zero_mul] at hr
    exact sub_eq_zero.mp hr.symm
  · rintro rfl
    simp [historySpectralDefect,native_preparation_frame_commutes_lift]

/-- Explicit column-level naturality on J and the next retained golden history GJ. -/
theorem two_history_spectral_naturality_iff (a p : ℝ)
    (fine : Matrix (n ⊕ n) (n ⊕ n) ℝ) (coarse : Matrix n n ℝ)
    (hp : p≠0) (hg : a^2+p^2=1) :
    (fine*ownedGoldenEmbedding (n:=n) a p=ownedGoldenEmbedding (n:=n) a p*coarse ∧
     fine*(ownedGoldenFactor (n:=n) a p*ownedGoldenEmbedding (n:=n) a p)=
       (ownedGoldenFactor (n:=n) a p*ownedGoldenEmbedding (n:=n) a p)*coarse) ↔
      fine=liftOperator coarse := by
  have hc := two_native_preparation_columns (n:=n) a p
  have heq : historySpectralDefect a p fine coarse=0 ↔
      (fine*ownedGoldenEmbedding (n:=n) a p=ownedGoldenEmbedding (n:=n) a p*coarse ∧
       fine*(ownedGoldenFactor (n:=n) a p*ownedGoldenEmbedding (n:=n) a p)=
         (ownedGoldenFactor (n:=n) a p*ownedGoldenEmbedding (n:=n) a p)*coarse) := by
    rw [historySpectralDefect,sub_eq_zero]
    constructor
    · intro he
      constructor
      · ext i j
        have hx := congrArg (fun M => M i (Sum.inl j)) he
        simpa [Matrix.mul_apply,Fintype.sum_sum_type,liftOperator,hc.1] using hx
      · ext i j
        have hx := congrArg (fun M => M i (Sum.inr j)) he
        simpa [Matrix.mul_apply,Fintype.sum_sum_type,liftOperator,hc.2] using hx
    · rintro ⟨h0,h1⟩
      ext i j
      rcases j with j|j
      · have hx := congrArg (fun M => M i j) h0
        simpa [Matrix.mul_apply,Fintype.sum_sum_type,liftOperator,hc.1] using hx
      · have hx := congrArg (fun M => M i j) h1
        simpa [Matrix.mul_apply,Fintype.sum_sum_type,liftOperator,hc.2] using hx
  exact heq.symm.trans (history_spectral_zero_defect_iff a p fine coarse hp hg)

/-- With first-history naturality, the second defect is exactly the clock/scene
commutator observed on the actual prepared carrier. -/
theorem second_history_defect_is_commutator (a p : ℝ)
    (fine : Matrix (n ⊕ n) (n ⊕ n) ℝ) (coarse : Matrix n n ℝ)
    (h0 : fine*ownedGoldenEmbedding (n:=n) a p=ownedGoldenEmbedding (n:=n) a p*coarse) :
    (fine*ownedGoldenFactor (n:=n) a p-ownedGoldenFactor (n:=n) a p*fine)*ownedGoldenEmbedding (n:=n) a p=
      fine*(ownedGoldenFactor (n:=n) a p*ownedGoldenEmbedding (n:=n) a p)-
        (ownedGoldenFactor (n:=n) a p*ownedGoldenEmbedding (n:=n) a p)*coarse := by
  rw [Matrix.sub_mul]
  simp only [Matrix.mul_assoc,h0]

/-- A scene commuting with the new golden tick and preserving J necessarily
replicates; such passivity is a hypothesis to check, not a consequence of M1. -/
theorem commuting_scene_history_forces_replication (a p : ℝ)
    (fine : Matrix (n ⊕ n) (n ⊕ n) ℝ) (coarse : Matrix n n ℝ)
    (hp : p≠0) (hg : a^2+p^2=1)
    (h0 : fine*ownedGoldenEmbedding (n:=n) a p=ownedGoldenEmbedding (n:=n) a p*coarse)
    (hcomm : fine*ownedGoldenFactor (n:=n) a p=ownedGoldenFactor (n:=n) a p*fine) :
    fine=liftOperator coarse := by
  apply (two_history_spectral_naturality_iff a p fine coarse hp hg).mp
  refine ⟨h0,?_⟩
  rw [← Matrix.mul_assoc,hcomm,Matrix.mul_assoc,h0,← Matrix.mul_assoc]

/-- Actual matrix exponential on a replicated diagonal scene, not a trace proxy. -/
theorem matrix_heat_replicated_diagonal (beta : ℝ) (lambda : n → ℝ) [Nonempty n]
    :
    matrixHeat beta (liftOperator (Matrix.diagonal lambda))=
      heatContribution beta lambda+beta⁻¹*Real.log 2 := by
  rw [← literal_cylinder_observable_pullback,matrix_heat_diagonal]
  exact replicated_heat_contribution beta lambda

/-- A complete history-preserving fine scene curve has the genuine unchanged
thermal covector. This transports declared native inputs; it does not establish their physical admissibility. -/
theorem genuine_two_history_thermal_source (a p beta t : ℝ)
    (lambda : ℝ → n → ℝ) (v : n → ℝ)
    (fine : ℝ → Matrix (n ⊕ n) (n ⊕ n) ℝ) [Nonempty n]
    (hp : p≠0) (hg : a^2+p^2=1) (hb : beta≠0)
    (hl : ∀ i, HasDerivAt (fun s => lambda s i) (v i) t)
    (hn : ∀ s, historySpectralDefect a p (fine s) (Matrix.diagonal (lambda s))=0) :
    HasDerivAt (fun s => matrixHeat beta (fine s)) (thermalSource beta (lambda t) v) t := by
  have he : (fun s => matrixHeat beta (fine s))=
      (fun s => heatContribution beta (lambda s)+beta⁻¹*Real.log 2) := by
    funext s
    rw [(history_spectral_zero_defect_iff a p (fine s) _ hp hg).mp (hn s)]
    exact matrix_heat_replicated_diagonal beta (lambda s)
  rw [he]
  exact (genuine_thermal_source beta t lambda v hb hl).add_const _

/-- Genuine whole bootstrap derivative when both actual scene histories preserve
geometry and the full feedback process follows the literal cylinder lift. -/
theorem genuine_two_history_bootstrap_source (a p beta z t source : ℝ)
    (lambda : ℝ → n → ℝ) (v : n → ℝ)
    (fine : ℝ → Matrix (n ⊕ n) (n ⊕ n) ℝ) (P U : ℝ → Matrix n n ℝ) [Nonempty n]
    (hp : p≠0) (hg : a^2+p^2=1) (hb : beta≠0)
    (hl : ∀ i, HasDerivAt (fun s => lambda s i) (v i) t)
    (hn : ∀ s, historySpectralDefect a p (fine s) (Matrix.diagonal (lambda s))=0)
    (hf : HasDerivAt (fun s => feedbackAction z (fullFeedback (P s) (U s))) source t) :
    HasDerivAt (fun s => matrixHeat beta (fine s)+
      feedbackAction z (fullFeedback (liftOperator (P s)) (liftOperator (U s))))
      (thermalSource beta (lambda t) v+2*source) t := by
  have hh := genuine_two_history_thermal_source a p beta t lambda v fine hp hg hb hl hn
  have hff : HasDerivAt (fun s => feedbackAction z
      (fullFeedback (liftOperator (P s)) (liftOperator (U s)))) (2*source) t := by
    simpa only [full_feedback_refines,actual_feedback_action_refinement] using hf.const_mul 2
  exact hh.add hff

/-- Both genuine stationary derivatives force heat and feedback to vanish separately
on this declared tangent. These premises are not supplied as a native admission gate. -/
theorem two_history_stationarity_forces_separate_sources_zero (a p beta z t source : ℝ)
    (lambda : ℝ → n → ℝ) (v : n → ℝ)
    (fine : ℝ → Matrix (n ⊕ n) (n ⊕ n) ℝ) (P U : ℝ → Matrix n n ℝ) [Nonempty n]
    (hp : p≠0) (hg : a^2+p^2=1) (hb : beta≠0)
    (hl : ∀ i, HasDerivAt (fun s => lambda s i) (v i) t)
    (hn : ∀ s, historySpectralDefect a p (fine s) (Matrix.diagonal (lambda s))=0)
    (hf : HasDerivAt (fun s => feedbackAction z (fullFeedback (P s) (U s))) source t)
    (hc : HasDerivAt (fun s => bootstrapAction beta z (lambda s) (P s) (U s)) 0 t)
    (hplus : HasDerivAt (fun s => matrixHeat beta (fine s)+
      feedbackAction z (fullFeedback (liftOperator (P s)) (liftOperator (U s)))) 0 t) :
    thermalSource beta (lambda t) v=0 ∧ source=0 := by
  have h0 := (genuine_bootstrap_source beta z t source lambda v P U hb hl hf).unique hc
  have h1 := (genuine_two_history_bootstrap_source a p beta z t source lambda v fine P U
    hp hg hb hl hn hf).unique hplus
  exact (joint_stationarity_transfer_iff (thermalSource beta (lambda t) v) source).mp ⟨h0,h1⟩

/-- Literal ordinary trace, retaining both child sectors. -/
theorem lifted_ordinary_trace (A : Matrix n n ℝ) :
    (liftOperator A).trace=2*A.trace := by
  simp [liftOperator,Matrix.trace,Matrix.diag,Fintype.sum_sum_type,two_mul]

/-- At a replicated spectral value rho_plus=L(rho)/2, this exact pairing isolates
all missing spectral-variation directions. General heat differentiation is §6.7. -/
theorem fine_thermal_source_defect_identity (rho dD : Matrix n n ℝ)
    (dFine : Matrix (n ⊕ n) (n ⊕ n) ℝ) :
    -(((1/2:ℝ) • liftOperator rho)*dFine).trace=
      -(rho*dD).trace-(1/2:ℝ)*(liftOperator rho*(dFine-liftOperator dD)).trace := by
  have ht : (liftOperator rho*liftOperator dD).trace=2*(rho*dD).trace := by
    rw [← lift_mul,lifted_ordinary_trace]
  rw [Matrix.mul_sub,Matrix.trace_sub,ht,Matrix.smul_mul,Matrix.trace_smul]
  ring

/-- The required doubled thermal source fixes one exact spectral contraction,
not a complete physical law and not a criterion used to define allowed states. -/
theorem doubled_thermal_source_defect_iff (rho dD : Matrix n n ℝ)
    (dFine : Matrix (n ⊕ n) (n ⊕ n) ℝ) :
    -(((1/2:ℝ) • liftOperator rho)*dFine).trace=2*(-(rho*dD).trace) ↔
      (liftOperator rho*(dFine-liftOperator dD)).trace=2*(rho*dD).trace := by
  rw [fine_thermal_source_defect_identity rho dD dFine]
  constructor <;> intro h <;> linarith

/-- Nonzero spectral defects in the contraction kernel remain response-null.
Their vanishing is not inferred or promoted to physical gauge. -/
theorem thermal_response_null_defect_iff (rho dD : Matrix n n ℝ)
    (dFine : Matrix (n ⊕ n) (n ⊕ n) ℝ) :
    -(((1/2:ℝ) • liftOperator rho)*dFine).trace=-(rho*dD).trace ↔
      (liftOperator rho*(dFine-liftOperator dD)).trace=0 := by
  rw [fine_thermal_source_defect_identity rho dD dFine]
  constructor <;> intro h <;> linarith

end HistorySpectralNaturality

end D0.Research.NativeComposedFeedbackDynamics

/-! Actual theorem types and transitive proof dependencies. -/
#check D0.Research.NativeComposedFeedbackDynamics.archive_on_incoming
#print axioms D0.Research.NativeComposedFeedbackDynamics.archive_on_incoming
#check D0.Research.NativeComposedFeedbackDynamics.archive_transpose_on_outgoing
#print axioms D0.Research.NativeComposedFeedbackDynamics.archive_transpose_on_outgoing
#check D0.Research.NativeComposedFeedbackDynamics.archive_left_gram
#print axioms D0.Research.NativeComposedFeedbackDynamics.archive_left_gram
#check D0.Research.NativeComposedFeedbackDynamics.archive_right_gram
#print axioms D0.Research.NativeComposedFeedbackDynamics.archive_right_gram
#check D0.Research.NativeComposedFeedbackDynamics.joint_left_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.joint_left_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.full_left_block_equations
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_left_block_equations
#check D0.Research.NativeComposedFeedbackDynamics.reconstruct_all_raw_blocks
#print axioms D0.Research.NativeComposedFeedbackDynamics.reconstruct_all_raw_blocks
#check D0.Research.NativeComposedFeedbackDynamics.joint_orthogonality_iff
#print axioms D0.Research.NativeComposedFeedbackDynamics.joint_orthogonality_iff
#check D0.Research.NativeComposedFeedbackDynamics.joint_transpose
#print axioms D0.Research.NativeComposedFeedbackDynamics.joint_transpose
#check D0.Research.NativeComposedFeedbackDynamics.joint_right_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.joint_right_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.all_archive_completion_constraints
#print axioms D0.Research.NativeComposedFeedbackDynamics.all_archive_completion_constraints
#check D0.Research.NativeComposedFeedbackDynamics.archive_embedding_injective
#print axioms D0.Research.NativeComposedFeedbackDynamics.archive_embedding_injective
#check D0.Research.NativeComposedFeedbackDynamics.feedback_owner_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.feedback_owner_binding
#check D0.Research.NativeComposedFeedbackDynamics.one_return_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.one_return_feedback
#check D0.Research.NativeComposedFeedbackDynamics.joint_two_step_retained
#print axioms D0.Research.NativeComposedFeedbackDynamics.joint_two_step_retained
#check D0.Research.NativeComposedFeedbackDynamics.feedback_from_retained_block
#print axioms D0.Research.NativeComposedFeedbackDynamics.feedback_from_retained_block
#check D0.Research.NativeComposedFeedbackDynamics.minimal_is_joint
#print axioms D0.Research.NativeComposedFeedbackDynamics.minimal_is_joint
#check D0.Research.NativeComposedFeedbackDynamics.minimal_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.minimal_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.minimal_archive_tail_zero
#print axioms D0.Research.NativeComposedFeedbackDynamics.minimal_archive_tail_zero
#check D0.Research.NativeComposedFeedbackDynamics.orthogonal_composition
#print axioms D0.Research.NativeComposedFeedbackDynamics.orthogonal_composition
#check D0.Research.NativeComposedFeedbackDynamics.all_composed_histories_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.all_composed_histories_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.minimal_two_step_retained
#print axioms D0.Research.NativeComposedFeedbackDynamics.minimal_two_step_retained
#check D0.Research.NativeComposedFeedbackDynamics.two_steps_recover_full_minimal_memory
#print axioms D0.Research.NativeComposedFeedbackDynamics.two_steps_recover_full_minimal_memory
#check D0.Research.NativeComposedFeedbackDynamics.minimal_two_step_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.minimal_two_step_feedback
#check D0.Research.NativeComposedFeedbackDynamics.golden_two_step_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.golden_two_step_feedback
#check D0.Research.NativeComposedFeedbackDynamics.swapBit_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.swapBit_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.directStep_owned_blocks
#print axioms D0.Research.NativeComposedFeedbackDynamics.directStep_owned_blocks
#check D0.Research.NativeComposedFeedbackDynamics.recordedStep_owned_blocks
#print axioms D0.Research.NativeComposedFeedbackDynamics.recordedStep_owned_blocks
#check D0.Research.NativeComposedFeedbackDynamics.actual_composition_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_composition_binding
#check D0.Research.NativeComposedFeedbackDynamics.same_native_single_return
#print axioms D0.Research.NativeComposedFeedbackDynamics.same_native_single_return
#check D0.Research.NativeComposedFeedbackDynamics.direct_two_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.direct_two_feedback
#check D0.Research.NativeComposedFeedbackDynamics.recorded_two_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.recorded_two_feedback
#check D0.Research.NativeComposedFeedbackDynamics.direct_two_determinant
#print axioms D0.Research.NativeComposedFeedbackDynamics.direct_two_determinant
#check D0.Research.NativeComposedFeedbackDynamics.recorded_two_determinant
#print axioms D0.Research.NativeComposedFeedbackDynamics.recorded_two_determinant
#check D0.Research.NativeComposedFeedbackDynamics.native_composed_action_gap
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_composed_action_gap
#check D0.Research.NativeComposedFeedbackDynamics.native_composed_action_gap_positive
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_composed_action_gap_positive
#check D0.Research.NativeComposedFeedbackDynamics.cayleyAxis_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.cayleyAxis_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.cayley_two_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.cayley_two_feedback
#check D0.Research.NativeComposedFeedbackDynamics.genuine_cayley_composed_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_cayley_composed_source
#check D0.Research.NativeComposedFeedbackDynamics.actual_cayley_action_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_cayley_action_binding
#check D0.Research.NativeComposedFeedbackDynamics.actual_cayley_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_cayley_source
#check D0.Research.NativeComposedFeedbackDynamics.composed_source_nonzero
#print axioms D0.Research.NativeComposedFeedbackDynamics.composed_source_nonzero
#check D0.Research.NativeComposedFeedbackDynamics.golden_lift_intertwines
#print axioms D0.Research.NativeComposedFeedbackDynamics.golden_lift_intertwines
#check D0.Research.NativeComposedFeedbackDynamics.golden_inclusion_preserves_pairing
#print axioms D0.Research.NativeComposedFeedbackDynamics.golden_inclusion_preserves_pairing
#check D0.Research.NativeComposedFeedbackDynamics.lift_mul
#print axioms D0.Research.NativeComposedFeedbackDynamics.lift_mul
#check D0.Research.NativeComposedFeedbackDynamics.lift_one
#print axioms D0.Research.NativeComposedFeedbackDynamics.lift_one
#check D0.Research.NativeComposedFeedbackDynamics.lift_transpose
#print axioms D0.Research.NativeComposedFeedbackDynamics.lift_transpose
#check D0.Research.NativeComposedFeedbackDynamics.lift_sub
#print axioms D0.Research.NativeComposedFeedbackDynamics.lift_sub
#check D0.Research.NativeComposedFeedbackDynamics.lift_smul
#print axioms D0.Research.NativeComposedFeedbackDynamics.lift_smul
#check D0.Research.NativeComposedFeedbackDynamics.lift_every_power
#print axioms D0.Research.NativeComposedFeedbackDynamics.lift_every_power
#check D0.Research.NativeComposedFeedbackDynamics.full_feedback_refines
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_feedback_refines
#check D0.Research.NativeComposedFeedbackDynamics.every_history_feedback_refines
#print axioms D0.Research.NativeComposedFeedbackDynamics.every_history_feedback_refines
#check D0.Research.NativeComposedFeedbackDynamics.lifted_determinant
#print axioms D0.Research.NativeComposedFeedbackDynamics.lifted_determinant
#check D0.Research.NativeComposedFeedbackDynamics.actual_feedback_action_refinement
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_feedback_action_refinement
#check D0.Research.NativeComposedFeedbackDynamics.composed_feedback_action_refinement
#print axioms D0.Research.NativeComposedFeedbackDynamics.composed_feedback_action_refinement
#check D0.Research.NativeComposedFeedbackDynamics.genuine_refined_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_refined_source
#check D0.Research.NativeComposedFeedbackDynamics.prepared_readout_intertwines
#print axioms D0.Research.NativeComposedFeedbackDynamics.prepared_readout_intertwines
#check D0.Research.NativeComposedFeedbackDynamics.prepared_readout_projector
#print axioms D0.Research.NativeComposedFeedbackDynamics.prepared_readout_projector
#check D0.Research.NativeComposedFeedbackDynamics.prepared_readout_symmetric
#print axioms D0.Research.NativeComposedFeedbackDynamics.prepared_readout_symmetric
#check D0.Research.NativeComposedFeedbackDynamics.prepared_readout_unique
#print axioms D0.Research.NativeComposedFeedbackDynamics.prepared_readout_unique
#check D0.Research.NativeComposedFeedbackDynamics.leak_is_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.leak_is_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.full_preparation_defect
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_preparation_defect
#check D0.Research.NativeComposedFeedbackDynamics.return_feedback_expanded
#print axioms D0.Research.NativeComposedFeedbackDynamics.return_feedback_expanded
#check D0.Research.NativeComposedFeedbackDynamics.full_prepared_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_prepared_feedback
#check D0.Research.NativeComposedFeedbackDynamics.transported_feedback_determinant
#print axioms D0.Research.NativeComposedFeedbackDynamics.transported_feedback_determinant
#check D0.Research.NativeComposedFeedbackDynamics.transported_feedback_action
#print axioms D0.Research.NativeComposedFeedbackDynamics.transported_feedback_action
#check D0.Research.NativeComposedFeedbackDynamics.full_prepared_action
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_prepared_action
#check D0.Research.NativeComposedFeedbackDynamics.every_prepared_history_action
#print axioms D0.Research.NativeComposedFeedbackDynamics.every_prepared_history_action
#check D0.Research.NativeComposedFeedbackDynamics.full_return_determines_prepared_action
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_return_determines_prepared_action
#check D0.Research.NativeComposedFeedbackDynamics.full_prepared_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_prepared_source
#check D0.Research.NativeComposedFeedbackDynamics.golden_prepared_return_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.golden_prepared_return_feedback
#check D0.Research.NativeComposedFeedbackDynamics.compatible_readout_complement
#print axioms D0.Research.NativeComposedFeedbackDynamics.compatible_readout_complement
#check D0.Research.NativeComposedFeedbackDynamics.compatible_readout_complement_sufficient
#print axioms D0.Research.NativeComposedFeedbackDynamics.compatible_readout_complement_sufficient
#check D0.Research.NativeComposedFeedbackDynamics.owned_golden_embedding_isometric
#print axioms D0.Research.NativeComposedFeedbackDynamics.owned_golden_embedding_isometric
#check D0.Research.NativeComposedFeedbackDynamics.owned_golden_embedding_realizes_inclusion
#print axioms D0.Research.NativeComposedFeedbackDynamics.owned_golden_embedding_realizes_inclusion
#check D0.Research.NativeComposedFeedbackDynamics.literal_cylinder_observable_pullback
#print axioms D0.Research.NativeComposedFeedbackDynamics.literal_cylinder_observable_pullback
#check D0.Research.NativeComposedFeedbackDynamics.golden_factor_owned_blocks
#print axioms D0.Research.NativeComposedFeedbackDynamics.golden_factor_owned_blocks
#check D0.Research.NativeComposedFeedbackDynamics.golden_factor_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.golden_factor_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.two_native_preparation_columns
#print axioms D0.Research.NativeComposedFeedbackDynamics.two_native_preparation_columns
#check D0.Research.NativeComposedFeedbackDynamics.preparation_coordinates_inverse
#print axioms D0.Research.NativeComposedFeedbackDynamics.preparation_coordinates_inverse
#check D0.Research.NativeComposedFeedbackDynamics.all_four_returns_reconstruct_coordinates
#print axioms D0.Research.NativeComposedFeedbackDynamics.all_four_returns_reconstruct_coordinates
#check D0.Research.NativeComposedFeedbackDynamics.all_four_returns_reconstruct_full_operator
#print axioms D0.Research.NativeComposedFeedbackDynamics.all_four_returns_reconstruct_full_operator
#check D0.Research.NativeComposedFeedbackDynamics.native_cross_returns_injective
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_cross_returns_injective
#check D0.Research.NativeComposedFeedbackDynamics.golden_factor_commutes_literal_readout
#print axioms D0.Research.NativeComposedFeedbackDynamics.golden_factor_commutes_literal_readout
#check D0.Research.NativeComposedFeedbackDynamics.full_literal_feedback_coordinates
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_literal_feedback_coordinates
#check D0.Research.NativeComposedFeedbackDynamics.literal_action_from_all_four_returns
#print axioms D0.Research.NativeComposedFeedbackDynamics.literal_action_from_all_four_returns
#check D0.Research.NativeComposedFeedbackDynamics.genuine_two_preparation_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_two_preparation_source
#check D0.Research.NativeComposedFeedbackDynamics.norm_of_native_mix
#print axioms D0.Research.NativeComposedFeedbackDynamics.norm_of_native_mix
#check D0.Research.NativeComposedFeedbackDynamics.owned_recorded_response_coordinates
#print axioms D0.Research.NativeComposedFeedbackDynamics.owned_recorded_response_coordinates
#check D0.Research.NativeComposedFeedbackDynamics.native_recorded_response_balance
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_recorded_response_balance
#check D0.Research.NativeComposedFeedbackDynamics.native_recorded_mixed_response
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_recorded_mixed_response
#check D0.Research.NativeComposedFeedbackDynamics.recorded_response_recovers_pairing
#print axioms D0.Research.NativeComposedFeedbackDynamics.recorded_response_recovers_pairing
#check D0.Research.NativeComposedFeedbackDynamics.probe_pairing_reads_gram
#print axioms D0.Research.NativeComposedFeedbackDynamics.probe_pairing_reads_gram
#check D0.Research.NativeComposedFeedbackDynamics.native_quadratic_readings_reconstruct_gram
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_quadratic_readings_reconstruct_gram
#check D0.Research.NativeComposedFeedbackDynamics.flagged_preparation_square
#print axioms D0.Research.NativeComposedFeedbackDynamics.flagged_preparation_square
#check D0.Research.NativeComposedFeedbackDynamics.flagged_preparation_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.flagged_preparation_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.flagged_blank_preparation
#print axioms D0.Research.NativeComposedFeedbackDynamics.flagged_blank_preparation
#check D0.Research.NativeComposedFeedbackDynamics.literal_cylinder_registration
#print axioms D0.Research.NativeComposedFeedbackDynamics.literal_cylinder_registration
#check D0.Research.NativeComposedFeedbackDynamics.actual_feedback_is_response_gram
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_feedback_is_response_gram
#check D0.Research.NativeComposedFeedbackDynamics.recorded_readings_reconstruct_full_feedback
#print axioms D0.Research.NativeComposedFeedbackDynamics.recorded_readings_reconstruct_full_feedback
#check D0.Research.NativeComposedFeedbackDynamics.native_preparation_quadratic_gram
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_preparation_quadratic_gram
#check D0.Research.NativeComposedFeedbackDynamics.native_recorded_feedback_action
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_recorded_feedback_action
#check D0.Research.NativeComposedFeedbackDynamics.genuine_recorded_feedback_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_recorded_feedback_source
#check D0.Research.NativeComposedFeedbackDynamics.owned_comparison_factors
#print axioms D0.Research.NativeComposedFeedbackDynamics.owned_comparison_factors
#check D0.Research.NativeComposedFeedbackDynamics.tensor_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.tensor_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.owned_comparison_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.owned_comparison_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.tensor_reads_complete_blank_pair
#print axioms D0.Research.NativeComposedFeedbackDynamics.tensor_reads_complete_blank_pair
#check D0.Research.NativeComposedFeedbackDynamics.complete_owned_comparison_reading
#print axioms D0.Research.NativeComposedFeedbackDynamics.complete_owned_comparison_reading
#check D0.Research.NativeComposedFeedbackDynamics.blank_pair_has_fixed_norm
#print axioms D0.Research.NativeComposedFeedbackDynamics.blank_pair_has_fixed_norm
#check D0.Research.NativeComposedFeedbackDynamics.full_flagged_comparison_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.full_flagged_comparison_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.common_word_after_flag
#print axioms D0.Research.NativeComposedFeedbackDynamics.common_word_after_flag
#check D0.Research.NativeComposedFeedbackDynamics.complete_flagged_detector_amplitude
#print axioms D0.Research.NativeComposedFeedbackDynamics.complete_flagged_detector_amplitude
#check D0.Research.NativeComposedFeedbackDynamics.retained_flag_detector_is_feedback_reading
#print axioms D0.Research.NativeComposedFeedbackDynamics.retained_flag_detector_is_feedback_reading
#check D0.Research.NativeComposedFeedbackDynamics.three_stage_run_is_internal
#print axioms D0.Research.NativeComposedFeedbackDynamics.three_stage_run_is_internal
#check D0.Research.NativeComposedFeedbackDynamics.complete_comparison_has_internal_program
#print axioms D0.Research.NativeComposedFeedbackDynamics.complete_comparison_has_internal_program
#check D0.Research.NativeComposedFeedbackDynamics.actual_scene_zone_heat_real_extension
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_scene_zone_heat_real_extension
#check D0.Research.NativeComposedFeedbackDynamics.actual_scene_heat_polynomial
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_scene_heat_polynomial
#check D0.Research.NativeComposedFeedbackDynamics.thermal_partition_positive
#print axioms D0.Research.NativeComposedFeedbackDynamics.thermal_partition_positive
#check D0.Research.NativeComposedFeedbackDynamics.replicated_thermal_partition
#print axioms D0.Research.NativeComposedFeedbackDynamics.replicated_thermal_partition
#check D0.Research.NativeComposedFeedbackDynamics.replicated_heat_contribution
#print axioms D0.Research.NativeComposedFeedbackDynamics.replicated_heat_contribution
#check D0.Research.NativeComposedFeedbackDynamics.thermal_partition_uniform_shift
#print axioms D0.Research.NativeComposedFeedbackDynamics.thermal_partition_uniform_shift
#check D0.Research.NativeComposedFeedbackDynamics.thermal_heat_uniform_shift
#print axioms D0.Research.NativeComposedFeedbackDynamics.thermal_heat_uniform_shift
#check D0.Research.NativeComposedFeedbackDynamics.genuine_thermal_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_thermal_source
#check D0.Research.NativeComposedFeedbackDynamics.replicated_thermal_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.replicated_thermal_source
#check D0.Research.NativeComposedFeedbackDynamics.bootstrap_replication
#print axioms D0.Research.NativeComposedFeedbackDynamics.bootstrap_replication
#check D0.Research.NativeComposedFeedbackDynamics.genuine_bootstrap_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_bootstrap_source
#check D0.Research.NativeComposedFeedbackDynamics.genuine_replicated_bootstrap_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_replicated_bootstrap_source
#check D0.Research.NativeComposedFeedbackDynamics.joint_stationarity_transfer_iff
#print axioms D0.Research.NativeComposedFeedbackDynamics.joint_stationarity_transfer_iff
#check D0.Research.NativeComposedFeedbackDynamics.coarse_onshell_refined_residual
#print axioms D0.Research.NativeComposedFeedbackDynamics.coarse_onshell_refined_residual
#check D0.Research.NativeComposedFeedbackDynamics.compatible_refined_thermal_source_iff
#print axioms D0.Research.NativeComposedFeedbackDynamics.compatible_refined_thermal_source_iff
#check D0.Research.NativeComposedFeedbackDynamics.universal_single_calibration_obstruction
#print axioms D0.Research.NativeComposedFeedbackDynamics.universal_single_calibration_obstruction
#check D0.Research.NativeComposedFeedbackDynamics.bootstrap_uniform_spectral_shift
#print axioms D0.Research.NativeComposedFeedbackDynamics.bootstrap_uniform_spectral_shift
#check D0.Research.NativeComposedFeedbackDynamics.genuine_bootstrap_uniform_shift_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_bootstrap_uniform_shift_source
#check D0.Research.NativeComposedFeedbackDynamics.uniform_spectral_shift_cannot_be_stationary
#print axioms D0.Research.NativeComposedFeedbackDynamics.uniform_spectral_shift_cannot_be_stationary
#check D0.Research.NativeComposedFeedbackDynamics.control_projection_is_orthogonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_projection_is_orthogonal
#check D0.Research.NativeComposedFeedbackDynamics.control_laplacian_has_declared_spectrum
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_laplacian_has_declared_spectrum
#check D0.Research.NativeComposedFeedbackDynamics.control_feedback_determinant
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_feedback_determinant
#check D0.Research.NativeComposedFeedbackDynamics.control_feedback_pencil_positive
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_feedback_pencil_positive
#check D0.Research.NativeComposedFeedbackDynamics.control_actual_feedback_action
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_actual_feedback_action
#check D0.Research.NativeComposedFeedbackDynamics.control_genuine_feedback_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_genuine_feedback_source
#check D0.Research.NativeComposedFeedbackDynamics.control_actual_heat_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_actual_heat_source
#check D0.Research.NativeComposedFeedbackDynamics.control_spectrum_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_spectrum_derivative
#check D0.Research.NativeComposedFeedbackDynamics.control_genuine_joint_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_genuine_joint_source
#check D0.Research.NativeComposedFeedbackDynamics.control_genuine_refined_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_genuine_refined_source
#check D0.Research.NativeComposedFeedbackDynamics.control_joint_source_continuous
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_joint_source_continuous
#check D0.Research.NativeComposedFeedbackDynamics.control_feedback_source_positive
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_feedback_source_positive
#check D0.Research.NativeComposedFeedbackDynamics.control_slice_stationary_refinement_failure
#print axioms D0.Research.NativeComposedFeedbackDynamics.control_slice_stationary_refinement_failure
#check D0.Research.NativeComposedFeedbackDynamics.source_conj_mul
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_conj_mul
#check D0.Research.NativeComposedFeedbackDynamics.source_conj_one
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_conj_one
#check D0.Research.NativeComposedFeedbackDynamics.source_conj_sub
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_conj_sub
#check D0.Research.NativeComposedFeedbackDynamics.source_conj_smul
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_conj_smul
#check D0.Research.NativeComposedFeedbackDynamics.source_conj_trace
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_conj_trace
#check D0.Research.NativeComposedFeedbackDynamics.source_conj_det
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_conj_det
#check D0.Research.NativeComposedFeedbackDynamics.source_commutator_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_commutator_covariant
#check D0.Research.NativeComposedFeedbackDynamics.source_active_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_active_covariant
#check D0.Research.NativeComposedFeedbackDynamics.source_degree_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_degree_covariant
#check D0.Research.NativeComposedFeedbackDynamics.source_compression_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_compression_covariant
#check D0.Research.NativeComposedFeedbackDynamics.source_port_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_port_covariant
#check D0.Research.NativeComposedFeedbackDynamics.source_input_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_input_covariant
#check D0.Research.NativeComposedFeedbackDynamics.source_coupled_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_coupled_covariant
#check D0.Research.NativeComposedFeedbackDynamics.whole_source_word_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.whole_source_word_covariant
#check D0.Research.NativeComposedFeedbackDynamics.weighted_adjoint_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.weighted_adjoint_covariant
#check D0.Research.NativeComposedFeedbackDynamics.weighted_feedback_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.weighted_feedback_covariant
#check D0.Research.NativeComposedFeedbackDynamics.weighted_feedback_euclidean
#print axioms D0.Research.NativeComposedFeedbackDynamics.weighted_feedback_euclidean
#check D0.Research.NativeComposedFeedbackDynamics.source_commutator_first_jet
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_commutator_first_jet
#check D0.Research.NativeComposedFeedbackDynamics.source_compression_frame_jet
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_compression_frame_jet
#check D0.Research.NativeComposedFeedbackDynamics.trace_frame_jet_zero
#print axioms D0.Research.NativeComposedFeedbackDynamics.trace_frame_jet_zero
#check D0.Research.NativeComposedFeedbackDynamics.source_port_frame_jet
#print axioms D0.Research.NativeComposedFeedbackDynamics.source_port_frame_jet
#check D0.Research.NativeComposedFeedbackDynamics.matrix_heat_similarity
#print axioms D0.Research.NativeComposedFeedbackDynamics.matrix_heat_similarity
#check D0.Research.NativeComposedFeedbackDynamics.matrix_heat_diagonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.matrix_heat_diagonal
#check D0.Research.NativeComposedFeedbackDynamics.actual_matrix_heat_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_matrix_heat_derivative
#check D0.Research.NativeComposedFeedbackDynamics.feedback_action_similarity
#print axioms D0.Research.NativeComposedFeedbackDynamics.feedback_action_similarity
#check D0.Research.NativeComposedFeedbackDynamics.whole_operator_bootstrap_covariant
#print axioms D0.Research.NativeComposedFeedbackDynamics.whole_operator_bootstrap_covariant
#check D0.Research.NativeComposedFeedbackDynamics.genuine_whole_basis_ward
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_whole_basis_ward
#check D0.Research.NativeComposedFeedbackDynamics.actual_source_active_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_source_active_binding
#check D0.Research.NativeComposedFeedbackDynamics.actual_source_degree_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_source_degree_binding
#check D0.Research.NativeComposedFeedbackDynamics.actual_source_compression_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_source_compression_binding
#check D0.Research.NativeComposedFeedbackDynamics.actual_source_compression_positive
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_source_compression_positive
#check D0.Research.NativeComposedFeedbackDynamics.actual_source_signal_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_source_signal_binding
#check D0.Research.NativeComposedFeedbackDynamics.actual_source_input_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_source_input_binding
#check D0.Research.NativeComposedFeedbackDynamics.actual_source_interaction_binding
#print axioms D0.Research.NativeComposedFeedbackDynamics.actual_source_interaction_binding
#check D0.Research.NativeComposedFeedbackDynamics.genuine_matrix_power_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_matrix_power_derivative
#check D0.Research.NativeComposedFeedbackDynamics.matrix_power_jet_trace
#print axioms D0.Research.NativeComposedFeedbackDynamics.matrix_power_jet_trace
#check D0.Research.NativeComposedFeedbackDynamics.genuine_trace_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_trace_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_source_compression_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_source_compression_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_source_port_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_source_port_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_whole_native_word_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_whole_native_word_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_native_commutator_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_native_commutator_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_native_active_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_native_active_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_native_port_from_primitives
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_native_port_from_primitives
#check D0.Research.NativeComposedFeedbackDynamics.native_active_frame_jet
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_active_frame_jet
#check D0.Research.NativeComposedFeedbackDynamics.genuine_transpose_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_transpose_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_weighted_feedback_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_weighted_feedback_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_inverse_metric_jet
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_inverse_metric_jet
#check D0.Research.NativeComposedFeedbackDynamics.whole_weighted_feedback_frame_jet
#print axioms D0.Research.NativeComposedFeedbackDynamics.whole_weighted_feedback_frame_jet
#check D0.Research.NativeComposedFeedbackDynamics.genuine_kronecker_right_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_kronecker_right_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_native_coupled_derivative
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_native_coupled_derivative
#check D0.Research.NativeComposedFeedbackDynamics.genuine_native_input_from_primitives
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_native_input_from_primitives
#check D0.Research.NativeComposedFeedbackDynamics.genuine_native_interaction_from_primitives
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_native_interaction_from_primitives

#check D0.Research.NativeComposedFeedbackDynamics.native_preparation_frame_inverse
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_preparation_frame_inverse

#check D0.Research.NativeComposedFeedbackDynamics.preparation_coordinates_commute_lift
#print axioms D0.Research.NativeComposedFeedbackDynamics.preparation_coordinates_commute_lift

#check D0.Research.NativeComposedFeedbackDynamics.native_preparation_frame_commutes_lift
#print axioms D0.Research.NativeComposedFeedbackDynamics.native_preparation_frame_commutes_lift

#check D0.Research.NativeComposedFeedbackDynamics.history_spectral_defect_reconstructs
#print axioms D0.Research.NativeComposedFeedbackDynamics.history_spectral_defect_reconstructs

#check D0.Research.NativeComposedFeedbackDynamics.history_spectral_zero_defect_iff
#print axioms D0.Research.NativeComposedFeedbackDynamics.history_spectral_zero_defect_iff

#check D0.Research.NativeComposedFeedbackDynamics.two_history_spectral_naturality_iff
#print axioms D0.Research.NativeComposedFeedbackDynamics.two_history_spectral_naturality_iff

#check D0.Research.NativeComposedFeedbackDynamics.second_history_defect_is_commutator
#print axioms D0.Research.NativeComposedFeedbackDynamics.second_history_defect_is_commutator

#check D0.Research.NativeComposedFeedbackDynamics.commuting_scene_history_forces_replication
#print axioms D0.Research.NativeComposedFeedbackDynamics.commuting_scene_history_forces_replication

#check D0.Research.NativeComposedFeedbackDynamics.matrix_heat_replicated_diagonal
#print axioms D0.Research.NativeComposedFeedbackDynamics.matrix_heat_replicated_diagonal

#check D0.Research.NativeComposedFeedbackDynamics.genuine_two_history_thermal_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_two_history_thermal_source

#check D0.Research.NativeComposedFeedbackDynamics.genuine_two_history_bootstrap_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_two_history_bootstrap_source

#check D0.Research.NativeComposedFeedbackDynamics.two_history_stationarity_forces_separate_sources_zero
#print axioms D0.Research.NativeComposedFeedbackDynamics.two_history_stationarity_forces_separate_sources_zero

#check D0.Research.NativeComposedFeedbackDynamics.lifted_ordinary_trace
#print axioms D0.Research.NativeComposedFeedbackDynamics.lifted_ordinary_trace

#check D0.Research.NativeComposedFeedbackDynamics.fine_thermal_source_defect_identity
#print axioms D0.Research.NativeComposedFeedbackDynamics.fine_thermal_source_defect_identity

#check D0.Research.NativeComposedFeedbackDynamics.doubled_thermal_source_defect_iff
#print axioms D0.Research.NativeComposedFeedbackDynamics.doubled_thermal_source_defect_iff

#check D0.Research.NativeComposedFeedbackDynamics.thermal_response_null_defect_iff
#print axioms D0.Research.NativeComposedFeedbackDynamics.thermal_response_null_defect_iff
