import D0.Representation.GoldenCoherentMemory
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
end
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
