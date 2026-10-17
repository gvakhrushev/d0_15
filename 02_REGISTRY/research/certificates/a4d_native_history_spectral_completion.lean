import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import D0.VNext2.SceneEndpointReynoldsExpectation
import D0.Spectral.DarkArchiveStructure
import Mathlib.LinearAlgebra.Matrix.SchurComplement
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false

namespace D0.Research.NativeSceneHistoryFeedback
noncomputable section
open Matrix
open scoped BigOperators

section GenericGraph
variable {v : Type*} [Fintype v] [DecidableEq v]
variable (r : v → v → Prop) [DecidableRel r]

abbrev Edge := {e : v × v // r e.1 e.2}

def edgeDegree (b : v) : ℚ := ∑ a, if r a b then 1 else 0
def endpointLift : Matrix (Edge r) v ℚ := fun e b => if e.val.2=b then 1 else 0
def sourceLift : Matrix (Edge r) v ℚ := fun e b => if e.val.1=b then 1 else 0
def endpointAverage : Matrix v (Edge r) ℚ :=
  fun b e => if e.val.2=b then (edgeDegree r b)⁻¹ else 0
def graphAdjacency : Matrix v v ℚ := fun a b => if r a b then 1 else 0
def graphTransport : Matrix v v ℚ :=
  diagonal (fun b => (edgeDegree r b)⁻¹)*graphAdjacency r

theorem sum_over_actual_edges (f : v × v → ℚ) :
    (∑ e : Edge r, f e.val)=∑ a, ∑ b, if r a b then f (a,b) else 0 := by
  rw [← Finset.sum_subtype (Finset.univ.filter (fun e : v × v => r e.1 e.2))
    (by simp) f, Finset.sum_filter, Fintype.sum_prod_type]

theorem endpoint_lift_gram :
    (endpointLift r).transpose*endpointLift r=diagonal (edgeDegree r) := by
  ext a b
  simp only [Matrix.mul_apply, Matrix.transpose_apply, endpointLift]
  rw [sum_over_actual_edges r (fun e => (if e.2=a then 1 else 0)*(if e.2=b then 1 else 0))]
  by_cases hab : a=b
  · subst b
    have h : ∀ x y : v,
        (if r x y then (if y=a then (1:ℚ) else 0)*(if y=a then 1 else 0) else 0)=
          if y=a then (if r x a then (1:ℚ) else 0) else 0 := by
      intro x y
      by_cases hy : y=a <;> by_cases hr : r x y <;> simp_all
    simp only [h,Finset.sum_ite_eq',Finset.mem_univ,if_true,Matrix.diagonal_apply_eq]
    rfl
  · have h : ∀ x y : v,
        (if r x y then (if y=a then (1:ℚ) else 0)*(if y=b then 1 else 0) else 0)=0 := by
      intro x y
      by_cases hy : y=a <;> by_cases hz : y=b <;> by_cases hr : r x y <;> simp_all
    simp only [h,Finset.sum_const_zero,Matrix.diagonal_apply_ne _ hab]

theorem endpoint_average_is_weighted_adjoint :
    endpointAverage r=diagonal (fun b => (edgeDegree r b)⁻¹)*(endpointLift r).transpose := by
  ext b e
  simp only [Matrix.diagonal_mul, Matrix.transpose_apply, endpointAverage, endpointLift]
  split_ifs <;> simp

theorem endpoint_average_exact_left_inverse (hn : ∀ b, edgeDegree r b≠0) :
    endpointAverage r*endpointLift r=1 := by
  rw [endpoint_average_is_weighted_adjoint,Matrix.mul_assoc,endpoint_lift_gram]
  ext a b
  by_cases hab : a=b
  · subst b; simp [Matrix.diagonal_apply,Matrix.one_apply,hn]
  · simp [Matrix.diagonal_apply,Matrix.one_apply,hab]

theorem endpoint_reynolds_is_selfadjoint :
    (endpointLift r*endpointAverage r).transpose=endpointLift r*endpointAverage r := by
  rw [endpoint_average_is_weighted_adjoint]
  simp [Matrix.transpose_mul,Matrix.diagonal_transpose,Matrix.mul_assoc]

theorem endpoint_source_average (hs : ∀ a b, r a b ↔ r b a) :
    endpointAverage r*sourceLift r=graphTransport r := by
  ext a b
  simp only [Matrix.mul_apply, endpointAverage, sourceLift]
  rw [sum_over_actual_edges r (fun e => (if e.2=a then (edgeDegree r a)⁻¹ else 0)*
    (if e.1=b then 1 else 0))]
  have h : ∀ x y : v,
      (if r x y then (if y=a then (edgeDegree r a)⁻¹ else 0)*(if x=b then 1 else 0) else 0)=
        if x=b then (if y=a then (if r b a then (edgeDegree r a)⁻¹ else 0) else 0) else 0 := by
    intro x y
    by_cases hx : x=b <;> by_cases hy : y=a <;> by_cases hr : r x y <;> simp_all
  simp only [h,Finset.sum_ite_eq',Finset.mem_univ,if_true]
  simp [graphTransport,graphAdjacency,Matrix.diagonal_mul,hs b a]

def reverseEquiv (hs : ∀ a b, r a b ↔ r b a) : Equiv.Perm (Edge r) where
  toFun e := ⟨(e.val.2,e.val.1),(hs _ _).mp e.property⟩
  invFun e := ⟨(e.val.2,e.val.1),(hs _ _).mp e.property⟩
  left_inv e := by cases e; rfl
  right_inv e := by cases e; rfl

def reverseOperator (hs : ∀ a b, r a b ↔ r b a) : Matrix (Edge r) (Edge r) ℚ :=
  fun e f => if f=reverseEquiv r hs e then 1 else 0

theorem history_reverse_is_involution (hs : ∀ a b, r a b ↔ r b a) :
    reverseOperator r hs*reverseOperator r hs=1 := by
  ext e f
  simp only [Matrix.mul_apply,reverseOperator,ite_mul,one_mul,zero_mul,
    Finset.sum_ite_eq',Finset.mem_univ,if_true]
  simp [reverseEquiv,Matrix.one_apply,eq_comm]

theorem history_reverse_is_selfadjoint (hs : ∀ a b, r a b ↔ r b a) :
    (reverseOperator r hs).transpose=reverseOperator r hs := by
  ext e f
  simp only [reverseOperator,Matrix.transpose_apply]
  have he : e=reverseEquiv r hs f ↔ f=reverseEquiv r hs e := by
    constructor <;> intro h <;> subst_vars <;> rfl
  simp only [he]

theorem history_reverse_is_orthogonal (hs : ∀ a b, r a b ↔ r b a) :
    (reverseOperator r hs).transpose*reverseOperator r hs=1 := by
  rw [history_reverse_is_selfadjoint,history_reverse_is_involution]

theorem history_reverse_recovers_source (hs : ∀ a b, r a b ↔ r b a) :
    reverseOperator r hs*endpointLift r=sourceLift r := by
  ext e b
  simp only [Matrix.mul_apply,reverseOperator,ite_mul,one_mul,zero_mul,
    Finset.sum_ite_eq',Finset.mem_univ,if_true]
  simp [endpointLift,sourceLift,reverseEquiv]

def historyRelabel (σ : Equiv.Perm v) (hp : ∀ a b, r (σ a) (σ b) ↔ r a b) :
    Equiv.Perm (Edge r) where
  toFun e := ⟨(σ e.val.1,σ e.val.2),(hp _ _).mpr e.property⟩
  invFun e := ⟨(σ.symm e.val.1,σ.symm e.val.2),by
    apply (hp _ _).mp
    simpa using e.property⟩
  left_inv e := by apply Subtype.ext; simp
  right_inv e := by apply Subtype.ext; simp

theorem complete_history_relabel_reverse_naturality (hs : ∀ a b, r a b ↔ r b a)
    (σ : Equiv.Perm v) (hp : ∀ a b, r (σ a) (σ b) ↔ r a b) (e : Edge r) :
    reverseEquiv r hs (historyRelabel r σ hp e)=
      historyRelabel r σ hp (reverseEquiv r hs e) := rfl

theorem complete_history_relabel_keeps_both_readouts (σ : Equiv.Perm v)
    (hp : ∀ a b, r (σ a) (σ b) ↔ r a b) (e : Edge r) :
    (historyRelabel r σ hp e).val.1=σ e.val.1 ∧
      (historyRelabel r σ hp e).val.2=σ e.val.2 := ⟨rfl,rfl⟩

end GenericGraph

section CompleteReturn
variable {v e : Type*} [Fintype v] [Fintype e] [DecidableEq v] [DecidableEq e]

def historyProjection (J : Matrix e v ℚ) (C : Matrix v e ℚ) := J*C
def historyFeedback (P U : Matrix e e ℚ) := P*U.transpose*(1-P)*U*P
def historyCompression (J : Matrix e v ℚ) (C : Matrix v e ℚ) (U : Matrix e e ℚ) := C*U*J

theorem complete_history_projection_idempotent (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (hc : C*J=1) : historyProjection J C*historyProjection J C=historyProjection J C := by
  change (J*C)*(J*C)=J*C
  calc
    _ = J*(C*J)*C := by simp [Matrix.mul_assoc]
    _ = J*C := by rw [hc,Matrix.mul_one]

theorem involutive_history_exact_feedback (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (hc : C*J=1) (hu : U*U=1) (ht : U.transpose=U) :
    historyFeedback (historyProjection J C) U=
      J*(1-historyCompression J C U*historyCompression J C U)*C := by
  simp only [historyFeedback,historyProjection,historyCompression,ht,Matrix.mul_sub,
    Matrix.sub_mul,Matrix.mul_one]
  have hCJ : C*(J*C)=C := by rw [← Matrix.mul_assoc,hc,Matrix.one_mul]
  simp only [Matrix.mul_assoc,hc,hCJ,hu,Matrix.one_mul,Matrix.mul_one]

theorem history_feedback_retains_whole_vertex_response (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (hc : C*J=1) (hu : U*U=1) (ht : U.transpose=U) :
    C*historyFeedback (historyProjection J C) U*J=
      1-historyCompression J C U*historyCompression J C U := by
  rw [involutive_history_exact_feedback J C U hc hu ht]
  simp only [← Matrix.mul_assoc,hc,Matrix.one_mul,Matrix.mul_one]
  rw [Matrix.mul_assoc,hc,Matrix.mul_one]

theorem history_feedback_determinant_exact (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (z : ℚ) (hc : C*J=1) (hu : U*U=1) (ht : U.transpose=U) :
    (1-z • historyFeedback (historyProjection J C) U).det=
      (1-z • (1-historyCompression J C U*historyCompression J C U)).det := by
  rw [involutive_history_exact_feedback J C U hc hu ht]
  have h := Matrix.det_one_sub_mul_comm (z • J)
    ((1-historyCompression J C U*historyCompression J C U)*C)
  have htail : (1-historyCompression J C U*historyCompression J C U)*C*J=
      1-historyCompression J C U*historyCompression J C U := by
    rw [Matrix.mul_assoc,hc,Matrix.mul_one]
  simpa [Matrix.smul_mul,Matrix.mul_smul,← Matrix.mul_assoc,htail] using h

theorem every_native_even_history_returns (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (k : ℕ) (hc : C*J=1) (hu : U*U=1) :
    historyCompression J C (U^(2*k))=1 := by
  have hk : U^(2*k)=1 := by rw [pow_mul,pow_two,hu]; simp
  simp [historyCompression,hk,hc]

theorem every_native_odd_history_returns (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (k : ℕ) (hu : U*U=1) :
    historyCompression J C (U^(2*k+1))=historyCompression J C U := by
  have hk : U^(2*k)=1 := by rw [pow_mul,pow_two,hu]; simp
  simp [historyCompression,pow_succ,hk]

theorem every_even_history_feedback_zero (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (k : ℕ) (hc : C*J=1) (hu : U*U=1) :
    historyFeedback (historyProjection J C) (U^(2*k))=0 := by
  have hk : U^(2*k)=1 := by rw [pow_mul,pow_two,hu]; simp
  have hp := complete_history_projection_idempotent J C hc
  simp only [historyFeedback,hk,Matrix.transpose_one,Matrix.mul_one,Matrix.mul_sub,
    Matrix.sub_mul,hp]
  simp

theorem history_kernel_is_fully_retained (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (x : v → ℚ) (hc : C*J=1) (hu : U*U=1)
    (ht : U.transpose=U) (hx : (historyCompression J C U).mulVec x=0) :
    (historyFeedback (historyProjection J C) U*J).mulVec x=J.mulVec x := by
  rw [involutive_history_exact_feedback J C U hc hu ht]
  simp only [Matrix.mul_assoc,hc,Matrix.mul_one]
  rw [← Matrix.mulVec_mulVec,Matrix.sub_mulVec,Matrix.one_mulVec,
    ← Matrix.mulVec_mulVec,hx,Matrix.mulVec_zero,sub_zero]

theorem exact_full_history_resolvent (U : Matrix e e ℚ) (z : ℚ)
    (hu : U*U=1) (hz : 1-z^2≠0) :
    (1-z • U)*((1-z^2)⁻¹ • (1+z • U))=1 ∧
    ((1-z^2)⁻¹ • (1+z • U))*(1-z • U)=1 := by
  have hr : (1-z • U)*(1+z • U)=(1-z^2) • (1 : Matrix e e ℚ) := by
    simp only [Matrix.sub_mul,Matrix.mul_add,Matrix.one_mul,Matrix.mul_one,
      Matrix.smul_mul,Matrix.mul_smul,smul_smul,hu]
    module
  have hl : (1+z • U)*(1-z • U)=(1-z^2) • (1 : Matrix e e ℚ) := by
    simp only [Matrix.mul_sub,Matrix.add_mul,Matrix.one_mul,Matrix.mul_one,
      Matrix.smul_mul,Matrix.mul_smul,smul_smul,hu]
    module
  constructor <;> simp only [Matrix.mul_smul,Matrix.smul_mul,hr,hl,smul_smul,
    inv_mul_cancel₀ hz,one_smul]

theorem exact_full_history_resolvent_compression (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (z : ℚ) (hc : C*J=1) :
    C*((1-z^2)⁻¹ • (1+z • U))*J=
      (1-z^2)⁻¹ • (1+z • historyCompression J C U) := by
  simp [historyCompression,Matrix.mul_add,Matrix.add_mul,Matrix.mul_smul,
    Matrix.smul_mul,Matrix.mul_assoc,hc]

def historyComplement (J : Matrix e v ℚ) (C : Matrix v e ℚ) := 1-J*C
def historyIncoming (J : Matrix e v ℚ) (C : Matrix v e ℚ) (U : Matrix e e ℚ) :=
  historyComplement J C*U*J
def historyArchive (J : Matrix e v ℚ) (C : Matrix v e ℚ) (U : Matrix e e ℚ) :=
  historyComplement J C*U*historyComplement J C
def historyOutgoing (J : Matrix e v ℚ) (C : Matrix v e ℚ) (U : Matrix e e ℚ) :=
  C*U*historyComplement J C

theorem full_history_complement_idempotent (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (hc : C*J=1) : historyComplement J C*historyComplement J C=historyComplement J C := by
  have hp := complete_history_projection_idempotent J C hc
  unfold historyComplement
  change (1-historyProjection J C)*(1-historyProjection J C)=1-historyProjection J C
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.one_mul,Matrix.mul_one,hp]
  abel

theorem full_history_incoming_delay (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (hc : C*J=1) (hu : U*U=1) :
    historyArchive J C U*historyIncoming J C U=
      -(historyIncoming J C U*historyCompression J C U) := by
  have hq := full_history_complement_idempotent J C hc
  have hqJ : historyComplement J C*J=0 := by
    simp [historyComplement,Matrix.sub_mul,Matrix.one_mul,Matrix.mul_assoc,hc]
  have hE : historyIncoming J C U=U*J-J*historyCompression J C U := by
    simp [historyIncoming,historyComplement,historyCompression,Matrix.sub_mul,Matrix.mul_assoc]
  calc
    _ = historyComplement J C*U*historyIncoming J C U := by
      simp only [historyArchive,historyIncoming,Matrix.mul_assoc] at hq ⊢
      rw [← Matrix.mul_assoc (historyComplement J C) (historyComplement J C),hq]
    _ = historyComplement J C*U*(U*J-J*historyCompression J C U) := by rw [hE]
    _ = -(historyIncoming J C U*historyCompression J C U) := by
      simp [Matrix.mul_sub,← Matrix.mul_assoc,hu,hqJ,historyIncoming]
      rw [Matrix.mul_assoc (historyComplement J C) U U,hu,Matrix.mul_one,hqJ]

theorem all_native_archive_delays_reconstructed (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (k : ℕ) (hc : C*J=1) (hu : U*U=1) :
    (historyArchive J C U)^k*historyIncoming J C U=
      historyIncoming J C U*(-historyCompression J C U)^k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ,Matrix.mul_assoc,full_history_incoming_delay J C U hc hu,
      Matrix.mul_neg,← Matrix.mul_assoc,ih]
    simp [pow_succ,Matrix.mul_assoc]

theorem full_history_outgoing_incoming (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (hc : C*J=1) (hu : U*U=1) :
    historyOutgoing J C U*historyIncoming J C U=
      1-historyCompression J C U*historyCompression J C U := by
  have hq := full_history_complement_idempotent J C hc
  calc
    _ = C*U*historyComplement J C*U*J := by
      simp only [historyOutgoing,historyIncoming,Matrix.mul_assoc] at hq ⊢
      rw [← Matrix.mul_assoc (historyComplement J C) (historyComplement J C),hq]
    _ = 1-historyCompression J C U*historyCompression J C U := by
      unfold historyComplement historyCompression
      simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one]
      simp [Matrix.mul_assoc,hu,hc]

theorem complete_native_archive_return_kernel (J : Matrix e v ℚ) (C : Matrix v e ℚ)
    (U : Matrix e e ℚ) (k : ℕ) (hc : C*J=1) (hu : U*U=1) :
    historyOutgoing J C U*(historyArchive J C U)^k*historyIncoming J C U=
      (1-historyCompression J C U*historyCompression J C U)*(-historyCompression J C U)^k := by
  rw [Matrix.mul_assoc,all_native_archive_delays_reconstructed J C U k hc hu,
    ← Matrix.mul_assoc,full_history_outgoing_incoming J C U hc hu]

end CompleteReturn

section ActualScene
open D0.VNext2.ScenePathHistoryCanonicity
open D0.VNext2.SceneEndpointReynoldsExpectation
open D0.Synthesis.SceneNormalizedQuotientDescent
local instance : DecidableEq LevelOneSceneHistory :=
  inferInstanceAs (DecidableEq {p : Fin 33 × Fin 33 // SceneStep p.1 p.2})

theorem actual_scene_relation_symmetric (a b : Fin 33) :
    SceneStep a b ↔ SceneStep b a := ⟨sceneStep_symm,sceneStep_symm⟩

theorem actual_scene_relation_iff (a b : Fin 33) :
    SceneStep a b ↔ D0.Claims.zone31 a≠D0.Claims.zone31 b := by
  unfold SceneStep D0.Claims.Adj31
  simp only [Matrix.of_apply]
  split_ifs <;> simp_all

theorem actual_scene_adjacency_binding : graphAdjacency SceneStep=D0.Claims.Adj31 := by
  ext a b
  simp only [graphAdjacency,D0.Claims.Adj31,Matrix.of_apply,actual_scene_relation_iff]
  by_cases h : D0.Claims.zone31 a=D0.Claims.zone31 b <;> simp [h]

theorem actual_endpoint_degree_binding (b : Fin 33) : edgeDegree SceneStep b=fullDegreeValue b := by
  unfold edgeDegree fullDegreeValue
  apply Finset.sum_congr rfl
  intro a _
  rw [← actual_scene_adjacency_binding]
  simp [graphAdjacency,actual_scene_relation_symmetric a b]

theorem graph_endpoint_degree_nonzero {v : Type*} [Fintype v] [DecidableEq v]
    (r : v → v → Prop) [DecidableRel r] (b : v) (hn : ∃ a, r a b) : edgeDegree r b≠0 := by
  obtain ⟨a,ha⟩ := hn
  have hsum : (1 : ℚ)≤edgeDegree r b := by
    have h := Finset.single_le_sum (f:=fun a => if r a b then (1:ℚ) else 0)
      (fun a _ => by dsimp; split_ifs <;> norm_num) (Finset.mem_univ a)
    simpa [edgeDegree,ha] using h
  linarith

theorem actual_endpoint_degree_nonzero (b : Fin 33) : edgeDegree SceneStep b≠0 := by
  apply graph_endpoint_degree_nonzero SceneStep b
  have h0 : D0.Claims.zone31 0=0 := by decide
  have h9 : D0.Claims.zone31 9=1 := by decide
  by_cases hb : D0.Claims.zone31 b=0
  · refine ⟨9,(actual_scene_relation_iff 9 b).mpr ?_⟩
    rw [h9,hb]; decide
  · refine ⟨0,(actual_scene_relation_iff 0 b).mpr ?_⟩
    rw [h0]; exact Ne.symm hb

theorem actual_endpoint_lift_binding : endpointLift SceneStep=Jt := rfl
theorem actual_source_lift_binding : sourceLift SceneStep=Js := rfl

theorem actual_endpoint_average_binding : endpointAverage SceneStep=C1 := by
  ext b e
  simp [endpointAverage,C1,endpoint,actual_endpoint_degree_binding]

theorem actual_transport_binding : graphTransport SceneStep=fullTransport := by
  simp [graphTransport,fullTransport,fullDegreeInv,actual_endpoint_degree_binding,
    actual_scene_adjacency_binding]

theorem actual_history_average_left_inverse : C1*Jt=1 := by
  rw [← actual_endpoint_average_binding,← actual_endpoint_lift_binding]
  exact endpoint_average_exact_left_inverse SceneStep actual_endpoint_degree_nonzero

theorem actual_history_average_source : C1*Js=fullTransport := by
  rw [← actual_endpoint_average_binding,← actual_source_lift_binding,
    ← actual_transport_binding]
  exact endpoint_source_average SceneStep actual_scene_relation_symmetric

def nativeHistoryReverse : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ :=
  reverseOperator SceneStep actual_scene_relation_symmetric

theorem actual_history_reverse_owner_binding (e : LevelOneSceneHistory) :
    reverseEquiv SceneStep actual_scene_relation_symmetric e=reverseEdge e := by
  cases e; rfl

theorem actual_native_history_reverse_involution : nativeHistoryReverse*nativeHistoryReverse=1 :=
  history_reverse_is_involution SceneStep actual_scene_relation_symmetric

theorem actual_native_history_reverse_selfadjoint : nativeHistoryReverse.transpose=nativeHistoryReverse :=
  history_reverse_is_selfadjoint SceneStep actual_scene_relation_symmetric

theorem actual_native_history_projection_selfadjoint :
    (historyProjection Jt C1).transpose=historyProjection Jt C1 := by
  rw [historyProjection,← actual_endpoint_average_binding,← actual_endpoint_lift_binding]
  exact endpoint_reynolds_is_selfadjoint SceneStep

theorem actual_native_history_reverse_reads_source : nativeHistoryReverse*Jt=Js :=
  history_reverse_recovers_source SceneStep actual_scene_relation_symmetric

theorem actual_native_history_compression : historyCompression Jt C1 nativeHistoryReverse=fullTransport := by
  unfold historyCompression
  rw [Matrix.mul_assoc,actual_native_history_reverse_reads_source,actual_history_average_source]

theorem normalized_scene_return_feedback_polynomial :
    1-fullTransport*fullTransport=
      2 • fullNormalizedLaplacian-fullNormalizedLaplacian*fullNormalizedLaplacian := by
  unfold fullNormalizedLaplacian
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.one_mul,Matrix.mul_one]
  module

theorem actual_native_history_feedback :
    historyFeedback (historyProjection Jt C1) nativeHistoryReverse=
      Jt*(1-fullTransport*fullTransport)*C1 := by
  rw [involutive_history_exact_feedback Jt C1 nativeHistoryReverse
    actual_history_average_left_inverse actual_native_history_reverse_involution
    actual_native_history_reverse_selfadjoint,actual_native_history_compression]

theorem actual_native_history_feedback_determinant (z : ℚ) :
    (1-z • historyFeedback (historyProjection Jt C1) nativeHistoryReverse).det=
      (1-z • (1-fullTransport*fullTransport)).det := by
  rw [history_feedback_determinant_exact Jt C1 nativeHistoryReverse z
    actual_history_average_left_inverse actual_native_history_reverse_involution
    actual_native_history_reverse_selfadjoint,actual_native_history_compression]

theorem actual_native_all_archive_return_kernels (k : ℕ) :
    historyOutgoing Jt C1 nativeHistoryReverse*(historyArchive Jt C1 nativeHistoryReverse)^k*
      historyIncoming Jt C1 nativeHistoryReverse=
        (1-fullTransport*fullTransport)*(-fullTransport)^k := by
  rw [complete_native_archive_return_kernel Jt C1 nativeHistoryReverse k
    actual_history_average_left_inverse actual_native_history_reverse_involution,
    actual_native_history_compression]

theorem actual_native_full_resolvent_compression (z : ℚ) :
    C1*((1-z^2)⁻¹ • (1+z • nativeHistoryReverse))*Jt=
      (1-z^2)⁻¹ • (1+z • fullTransport) := by
  rw [exact_full_history_resolvent_compression Jt C1 nativeHistoryReverse z
    actual_history_average_left_inverse,actual_native_history_compression]

theorem actual_native_two_returns_recover_all_vertices :
    historyCompression Jt C1 (nativeHistoryReverse^2)=1 := by
  exact every_native_even_history_returns Jt C1 nativeHistoryReverse 1
    actual_history_average_left_inverse actual_native_history_reverse_involution

theorem actual_native_two_return_feedback_zero :
    historyFeedback (historyProjection Jt C1) (nativeHistoryReverse^2)=0 := by
  exact every_even_history_feedback_zero Jt C1 nativeHistoryReverse 1
    actual_history_average_left_inverse actual_native_history_reverse_involution

theorem actual_archive_adjacency_binding :
    D0.Claims.Adj31=D0.Spectral.DarkArchiveStructure.adj := by
  ext a b
  simp [D0.Claims.Adj31,D0.Spectral.DarkArchiveStructure.adj,
    D0.Claims.zone31,D0.Spectral.DarkArchiveStructure.zone,eq_comm]

theorem actual_balanced_archive_transport_zero (x : Fin 33 → ℚ)
    (hx : ∀ z, D0.Spectral.DarkArchiveStructure.zoneSum x z=0) :
    fullTransport.mulVec x=0 := by
  have hA : D0.Claims.Adj31.mulVec x=0 := by
    rw [actual_archive_adjacency_binding]
    ext u
    exact D0.Spectral.DarkArchiveStructure.balanced_mem_ker x hx u
  simp [fullTransport,← Matrix.mulVec_mulVec,hA]

theorem actual_balanced_archive_full_history_feedback (x : Fin 33 → ℚ)
    (hx : ∀ z, D0.Spectral.DarkArchiveStructure.zoneSum x z=0) :
    (historyFeedback (historyProjection Jt C1) nativeHistoryReverse*Jt).mulVec x=Jt.mulVec x := by
  apply history_kernel_is_fully_retained Jt C1 nativeHistoryReverse x
    actual_history_average_left_inverse actual_native_history_reverse_involution
    actual_native_history_reverse_selfadjoint
  rw [actual_native_history_compression]
  exact actual_balanced_archive_transport_zero x hx

theorem actual_balanced_archive_two_history_return (x : Fin 33 → ℚ)
    (hx : ∀ z, D0.Spectral.DarkArchiveStructure.zoneSum x z=0) :
    (C1*nativeHistoryReverse*Jt).mulVec x=0 ∧
      (C1*(nativeHistoryReverse^2)*Jt).mulVec x=x := by
  constructor
  · change (historyCompression Jt C1 nativeHistoryReverse).mulVec x=0
    rw [actual_native_history_compression]
    exact actual_balanced_archive_transport_zero x hx
  · change (historyCompression Jt C1 (nativeHistoryReverse^2)).mulVec x=x
    rw [actual_native_two_returns_recover_all_vertices]
    exact Matrix.one_mulVec x

def archiveWitness : Fin 33 → ℚ := Pi.single 0 1-Pi.single 1 1

theorem actual_archive_witness_balanced :
    ∀ z, D0.Spectral.DarkArchiveStructure.zoneSum archiveWitness z=0 := by
  intro z
  unfold D0.Spectral.DarkArchiveStructure.zoneSum archiveWitness
  rw [Finset.sum_filter]
  have h : ∀ w : Fin 33,
      (if D0.Spectral.DarkArchiveStructure.zone w=z then Pi.single 0 (1:ℚ) w-Pi.single 1 1 w else 0)=
      (if w=0 then (if (0:Fin 3)=z then (1:ℚ) else 0) else 0)-
      (if w=1 then (if (0:Fin 3)=z then (1:ℚ) else 0) else 0) := by
    intro w
    by_cases h0 : w=0 <;> by_cases h1 : w=1 <;>
      simp_all [Pi.single_apply,D0.Spectral.DarkArchiveStructure.zone] <;>
      split_ifs <;> norm_num
  simp only [Pi.sub_apply,h,Finset.sum_sub_distrib,Finset.sum_ite_eq',Finset.mem_univ,if_true,sub_self]

theorem actual_archive_witness_nonzero : archiveWitness≠0 := by
  intro h
  have h0 := congrFun h 0
  norm_num [archiveWitness,Pi.single_apply] at h0

theorem actual_native_history_feedback_nonzero :
    historyFeedback (historyProjection Jt C1) nativeHistoryReverse≠0 := by
  intro h
  have hret := actual_balanced_archive_full_history_feedback archiveWitness actual_archive_witness_balanced
  rw [h,Matrix.zero_mul,Matrix.zero_mulVec] at hret
  have hrec := congrArg (fun y => C1.mulVec y) hret
  dsimp only at hrec
  rw [Matrix.mulVec_zero,Matrix.mulVec_mulVec,actual_history_average_left_inverse,Matrix.one_mulVec] at hrec
  exact actual_archive_witness_nonzero hrec.symm

theorem actual_no_repeated_forgetting_return :
    historyCompression Jt C1 (nativeHistoryReverse^2)≠fullTransport*fullTransport := by
  intro h
  rw [actual_native_two_returns_recover_all_vertices] at h
  have hx := congrArg (fun M => M.mulVec archiveWitness) h
  dsimp only at hx
  rw [Matrix.one_mulVec,← Matrix.mulVec_mulVec,
    actual_balanced_archive_transport_zero archiveWitness actual_archive_witness_balanced,
    Matrix.mulVec_zero] at hx
  exact actual_archive_witness_nonzero hx

end ActualScene
end
end D0.Research.NativeSceneHistoryFeedback

namespace D0.Research.NativeSceneHistoryFeedback
noncomputable section
open Matrix
open scoped BigOperators

section FullSpectralFrame
variable {e v : Type*} [Fintype e] [Fintype v] [DecidableEq e] [DecidableEq v]

def fullHistoryProjection (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (HI : Matrix v v ℚ) : Matrix e e ℚ := J*C+E*HI*B

def generatedHistoryHeat (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (HI delta : Matrix v v ℚ) : Matrix e e ℚ := J*delta*C+E*delta*HI*B

def completeHistoryHeat (A K W : Matrix e e ℚ) : Matrix e e ℚ :=
  A+(1-K)*W*(1-K)

theorem full_constant_inverse (H HI Pc : Matrix v v ℚ)
    (h : HI*H=1) (hc : H*Pc=Pc) : HI*Pc=Pc := by
  calc HI*Pc = HI*(H*Pc) := by rw [hc]
       _ = Pc := by rw [← Matrix.mul_assoc,h,Matrix.one_mul]

theorem full_spectral_projection_endpoint (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (HI : Matrix v v ℚ) (hc : C*J=1) (hb : B*J=0) :
    fullHistoryProjection J E C B HI*J=J := by
  simp [fullHistoryProjection,Matrix.add_mul,Matrix.mul_assoc,hc,hb]

theorem full_spectral_projection_incoming (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (H HI Pc : Matrix v v ℚ) (hc : C*E=0) (hb : B*E=H-Pc)
    (hi : HI*H=1) (hip : HI*Pc=Pc) (he : E*Pc=0) :
    fullHistoryProjection J E C B HI*E=E := by
  simp [fullHistoryProjection,Matrix.add_mul,Matrix.mul_assoc,hc,hb,Matrix.mul_sub,hi,hip,he]

theorem full_spectral_projection_idempotent (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (HI : Matrix v v ℚ)
    (hj : fullHistoryProjection J E C B HI*J=J)
    (he : fullHistoryProjection J E C B HI*E=E) :
    fullHistoryProjection J E C B HI*fullHistoryProjection J E C B HI =
      fullHistoryProjection J E C B HI := by
  conv_lhs => rhs; unfold fullHistoryProjection
  rw [Matrix.mul_add,← Matrix.mul_assoc _ J C,hj]
  simp [← Matrix.mul_assoc,he]
  rfl

theorem generated_spectral_endpoint (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (HI delta : Matrix v v ℚ) (hc : C*J=1) (hb : B*J=0) :
    generatedHistoryHeat J E C B HI delta*J=J*delta := by
  simp [generatedHistoryHeat,Matrix.add_mul,Matrix.mul_assoc,hc,hb]

theorem generated_spectral_incoming (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (H HI Pc delta : Matrix v v ℚ) (hc : C*E=0) (hb : B*E=H-Pc)
    (hi : HI*H=1) (hip : HI*Pc=Pc) (hd : delta*Pc=0) :
    generatedHistoryHeat J E C B HI delta*E=E*delta := by
  simp [generatedHistoryHeat,Matrix.add_mul,Matrix.mul_assoc,hc,hb,Matrix.mul_sub,hi,hip,hd]

theorem two_retained_readouts_determine_generated_block
    (A : Matrix e e ℚ) (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (HI delta : Matrix v v ℚ) (hj : A*J=J*delta) (he : A*E=E*delta) :
    A*fullHistoryProjection J E C B HI=generatedHistoryHeat J E C B HI delta := by
  unfold fullHistoryProjection generatedHistoryHeat
  rw [Matrix.mul_add,← Matrix.mul_assoc _ J C,hj]
  rw [← Matrix.mul_assoc _ (E*HI) B,← Matrix.mul_assoc _ E HI,he]

theorem full_projector_selfadjoint (J E : Matrix e v ℚ) (C B : Matrix v e ℚ)
    (HI : Matrix v v ℚ) (hp : (J*C).transpose=J*C)
    (hq : (E*HI*B).transpose=E*HI*B) :
    (fullHistoryProjection J E C B HI).transpose=fullHistoryProjection J E C B HI := by
  simp [fullHistoryProjection,Matrix.transpose_add,hp,hq]

theorem complete_symmetric_history_extension (A K W : Matrix e e ℚ)
    (hA : A.transpose=A) (hK : K.transpose=K) (hW : W.transpose=W) :
    (completeHistoryHeat A K W).transpose=completeHistoryHeat A K W := by
  simp [completeHistoryHeat,Matrix.transpose_add,Matrix.transpose_mul,Matrix.transpose_sub,hA,hK,hW,Matrix.mul_assoc]

theorem complete_history_readout_extension (A K W : Matrix e e ℚ) (J : Matrix e v ℚ)
    (delta : Matrix v v ℚ) (hk : K*J=J) (ha : A*J=J*delta) :
    completeHistoryHeat A K W*J=J*delta := by
  have hq : (1-K)*J=0 := by simp [Matrix.sub_mul,hk]
  simp [completeHistoryHeat,Matrix.add_mul,Matrix.mul_assoc,hq,ha]

theorem all_symmetric_history_extensions (A A0 K : Matrix e e ℚ)
    (ha : A.transpose=A) (h0 : A0.transpose=A0) (hk : K.transpose=K)
    (hkk : K*K=K) (h : A*K=A0) : A=completeHistoryHeat A0 K A := by
  have hl : K*A=A0 := by
    have ht := congrArg Matrix.transpose h
    simpa [Matrix.transpose_mul,ha,h0,hk] using ht
  have h0k : A0*K=A0 := by
    calc A0*K = A*(K*K) := by rw [← h,Matrix.mul_assoc]
         _ = A0 := by rw [hkk,h]
  have hk0 : K*A0=A0 := by
    have ht := congrArg Matrix.transpose h0k
    simpa [Matrix.transpose_mul,h0,hk] using ht
  unfold completeHistoryHeat
  simp only [Matrix.sub_mul,Matrix.mul_sub,Matrix.one_mul,Matrix.mul_one]
  rw [h,hl,h0k]
  abel

theorem complete_supported_symmetric_extension_iff (A A0 K : Matrix e e ℚ)
    (h0 : A0.transpose=A0) (hk : K.transpose=K) (h0k : A0*K=A0) :
    (A.transpose=A ∧ A*K=A0) ↔
    ∃ B : Matrix e e ℚ, B.transpose=B ∧ B*K=0 ∧ K*B=0 ∧ A=A0+B := by
  have hk0 : K*A0=A0 := by
    have ht := congrArg Matrix.transpose h0k
    simpa [Matrix.transpose_mul,h0,hk] using ht
  constructor
  · rintro ⟨ha,h⟩
    have hl : K*A=A0 := by
      have ht := congrArg Matrix.transpose h
      simpa [Matrix.transpose_mul,ha,h0,hk] using ht
    refine ⟨A-A0,?_,?_,?_,?_⟩
    · simp [Matrix.transpose_sub,ha,h0]
    · simp [Matrix.sub_mul,h,h0k]
    · simp [Matrix.mul_sub,hl,hk0]
    · abel
  · rintro ⟨B,hb,hbr,hbl,rfl⟩
    exact ⟨by simp [Matrix.transpose_add,h0,hb],by simp [Matrix.add_mul,h0k,hbr]⟩

theorem complete_supported_extension_parameter_unique (A0 B1 B2 : Matrix e e ℚ) :
    A0+B1=A0+B2 ↔ B1=B2 := add_left_cancel_iff

theorem complete_extension_endpoint_invisible (K : Matrix e e ℚ) (J : Matrix e v ℚ)
    (B : Matrix e e ℚ) (hk : K*J=J) (hb : B*K=0) : B*J=0 := by
  calc B*J = B*(K*J) := by rw [hk]
       _ = 0 := by rw [← Matrix.mul_assoc,hb,Matrix.zero_mul]

end FullSpectralFrame

section LowRankInverse
variable {v z : Type*} [Fintype v] [Fintype z] [DecidableEq v] [DecidableEq z]

theorem exact_zone_inverse_lift (L : Matrix v z ℚ) (C : Matrix z v ℚ)
    (H HI : Matrix z z ℚ) (hc : C*L=1) (h : H*HI=1) :
    (1+L*(H-1)*C)*(1+L*(HI-1)*C)=1 := by
  have hx : (L*(H-1)*C)*(L*(HI-1)*C)=L*((H-1)*(HI-1))*C := by
    simp only [Matrix.mul_assoc]
    rw [← Matrix.mul_assoc C L _,hc,Matrix.one_mul]
  rw [Matrix.add_mul,Matrix.mul_add,Matrix.mul_add,Matrix.one_mul,Matrix.one_mul,
    Matrix.mul_one,hx]
  calc
    _ = 1+L*(H*HI-1)*C := by
      simp only [Matrix.sub_mul,Matrix.mul_sub,Matrix.mul_one,Matrix.one_mul,
        Matrix.mul_add,Matrix.mul_sub,Matrix.add_mul,Matrix.sub_mul]
      abel
    _ = 1 := by rw [h]; simp

end LowRankInverse

section WeightedSymmetry
variable {v e : Type*} [Fintype v] [Fintype e] [DecidableEq v] [DecidableEq e]

theorem weighted_commuting_product_selfadjoint (X Y D : Matrix v v ℚ)
    (hd : D.transpose=D) (hx : (X*D).transpose=X*D) (hy : (Y*D).transpose=Y*D)
    (hc : X*Y=Y*X) : (X*Y*D).transpose=X*Y*D := by
  have hxt : D*X.transpose=X*D := by simpa [Matrix.transpose_mul,hd] using hx
  have hyt : D*Y.transpose=Y*D := by simpa [Matrix.transpose_mul,hd] using hy
  simp only [Matrix.transpose_mul,hd]
  rw [← Matrix.mul_assoc,hyt,Matrix.mul_assoc,hxt,← Matrix.mul_assoc,← hc]

theorem weighted_inverse_selfadjoint (H HI D : Matrix v v ℚ)
    (hd : D.transpose=D) (hh : (H*D).transpose=H*D)
    (hil : HI*H=1) : (HI*D).transpose=HI*D := by
  have ht : D*H.transpose=H*D := by simpa [Matrix.transpose_mul,hd] using hh
  have hinvt : H.transpose*HI.transpose=1 := by
    have h := congrArg Matrix.transpose hil
    simpa [Matrix.transpose_mul] using h
  simp only [Matrix.transpose_mul,hd]
  calc
    D*HI.transpose = HI*(H*D)*HI.transpose := by simp [← Matrix.mul_assoc,hil]
    _ = HI*(D*H.transpose)*HI.transpose := by rw [ht]
    _ = HI*D := by simp [Matrix.mul_assoc,hinvt]

theorem paired_block_selfadjoint (E : Matrix e v ℚ) (B : Matrix v e ℚ)
    (X D : Matrix v v ℚ) (hb : B=D*E.transpose) (hx : (X*D).transpose=X*D) :
    (E*X*B).transpose=E*X*B := by
  rw [hb]
  have he : E*X*(D*E.transpose)=E*(X*D)*E.transpose := by simp [Matrix.mul_assoc]
  rw [he]
  rw [Matrix.transpose_mul,Matrix.transpose_mul,Matrix.transpose_transpose,hx]
  simp [Matrix.mul_assoc]

end WeightedSymmetry

section ProjectionCovariance
variable {v e : Type*} [Fintype v] [Fintype e] [DecidableEq v] [DecidableEq e]

theorem generated_projector_commutes_preserving_reverse (J E : Matrix e v ℚ)
    (C B : Matrix v e ℚ) (HI : Matrix v v ℚ) (R : Matrix e e ℚ)
    (hk : (fullHistoryProjection J E C B HI).transpose=fullHistoryProjection J E C B HI)
    (hr : R.transpose=R)
    (hj : fullHistoryProjection J E C B HI*(R*J)=R*J)
    (he : fullHistoryProjection J E C B HI*(R*E)=R*E) :
    fullHistoryProjection J E C B HI*R=R*fullHistoryProjection J E C B HI := by
  let K := fullHistoryProjection J E C B HI
  have hj' : K*R*J=R*J := by simpa only [Matrix.mul_assoc,K] using hj
  have he' : K*R*E=R*E := by simpa only [Matrix.mul_assoc,K] using he
  have hkrk : K*R*K=R*K := by
    conv_lhs => rhs; unfold K fullHistoryProjection
    conv_rhs => rhs; unfold K fullHistoryProjection
    simp only [Matrix.mul_add,← Matrix.mul_assoc,hj',he']
  have ht := congrArg Matrix.transpose hkrk
  have hkl : K*R*K=K*R := by
    simpa only [Matrix.transpose_mul,hk,hr,Matrix.mul_assoc,K] using ht
  exact hkl.symm.trans hkrk

end ProjectionCovariance
end
end D0.Research.NativeSceneHistoryFeedback

namespace D0.Research.NativeSceneHistoryFeedback
noncomputable section
open Matrix
open scoped BigOperators
open D0.Claims D0.Synthesis.SceneNormalizedQuotientDescent
open D0.VNext2.SceneEndpointReynoldsExpectation D0.VNext2.ScenePathHistoryCanonicity
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000

 def nativeZoneSize : Fin 3 → ℚ := ![9,11,13]
 def nativeZoneDegree : Fin 3 → ℚ := ![24,22,20]
 def nativeZoneTransport : Matrix (Fin 3) (Fin 3) ℚ :=
   !![0,11/24,13/24; 9/22,0,13/22; 9/20,11/20,0]
 def nativeZoneAverage : Matrix (Fin 3) (Fin 33) ℚ :=
   fun z i => if zone31 i=z then (nativeZoneSize z)⁻¹ else 0
 def nativeZoneConstant : Matrix (Fin 3) (Fin 3) ℚ :=
   fun _ z => nativeZoneSize z*nativeZoneDegree z/718
 def nativeConstant : Matrix (Fin 33) (Fin 33) ℚ :=
   fun _ j => nativeZoneDegree (zone31 j)/718
 def nativeCoarseH : Matrix (Fin 33) (Fin 33) ℚ :=
   1-fullTransport*fullTransport+nativeConstant
 def nativeZoneH : Matrix (Fin 3) (Fin 3) ℚ :=
   1-nativeZoneTransport*nativeZoneTransport+nativeZoneConstant
 def nativeZoneHI : Matrix (Fin 3) (Fin 3) ℚ :=
   !![1947716/1675453,-526757/15079077,-147970/1159929;
      -574644/18429983,6276841/5026359,-925490/4253073;
      -177564/1675453,-1018039/5026359,505930/386643]
 def nativeCoarseHI : Matrix (Fin 33) (Fin 33) ℚ :=
   1+Cind31*(nativeZoneHI-1)*nativeZoneAverage

 theorem native_zone_counts_kernel (z : Fin 3) :
     (∑ i : Fin 33, Cind31 i z)=nativeZoneSize z := by
   fin_cases z <;>
     simp only [Fin.sum_univ_succ,Cind31,Matrix.of_apply] <;>
     norm_num [zone31,nativeZoneSize,Fin.ext_iff]

 theorem native_zone_size_nonzero (z : Fin 3) : nativeZoneSize z≠0 := by
   fin_cases z <;> norm_num [nativeZoneSize]

 theorem native_zone_average_left_inverse : nativeZoneAverage*Cind31=1 := by
   ext a b
   simp only [Matrix.mul_apply,nativeZoneAverage,Cind31,Matrix.of_apply]
   by_cases h : a=b
   · subst b
     have he : ∀ i : Fin 33,
         (if zone31 i=a then (nativeZoneSize a)⁻¹ else 0)*(if zone31 i=a then (1:ℚ) else 0)=
         (nativeZoneSize a)⁻¹*Cind31 i a := by
       intro i; by_cases h : zone31 i=a <;> simp [h,Cind31]
     simp only [he,← Finset.mul_sum,native_zone_counts_kernel]
     simp [native_zone_size_nonzero]
   · have he : ∀ i : Fin 33,
         (if zone31 i=a then (nativeZoneSize a)⁻¹ else 0)*(if zone31 i=b then (1:ℚ) else 0)=0 := by
       intro i; by_cases ha : zone31 i=a <;> by_cases hb : zone31 i=b <;> simp_all
     simp [he,Matrix.one_apply,h]

 theorem native_full_degree_by_zone (i : Fin 33) :
     fullDegreeValue i=nativeZoneDegree (zone31 i) := by
   unfold fullDegreeValue
   have he : ∀ j : Fin 33, Adj31 i j=1-Cind31 j (zone31 i) := by
     intro j
     simp only [Adj31,Cind31,Matrix.of_apply]
     by_cases h : zone31 i=zone31 j
     · simp only [h,ne_self_iff_false,if_false,if_true]; norm_num
     · simp only [h,Ne.symm h,if_true,if_false]; norm_num
   simp only [he,Finset.sum_sub_distrib,Finset.sum_const,Finset.card_univ,Fintype.card_fin,nsmul_eq_mul,mul_one,native_zone_counts_kernel]
   generalize zone31 i=z
   fin_cases z <;> norm_num [nativeZoneSize,nativeZoneDegree]

 theorem native_transport_entry (i j : Fin 33) :
     fullTransport i j = if zone31 i=zone31 j then 0 else (nativeZoneDegree (zone31 i))⁻¹ := by
   simp [fullTransport,fullDegreeInv,Matrix.diagonal_mul,Adj31,native_full_degree_by_zone]

 theorem native_transport_zone_factorization :
     fullTransport=Cind31*nativeZoneTransport*nativeZoneAverage := by
   ext i j
   rw [native_transport_entry]
   have hrow (z : Fin 3) : (Cind31*nativeZoneTransport) i z=nativeZoneTransport (zone31 i) z := by
     simp [Matrix.mul_apply,Cind31,Finset.sum_ite_eq']
   simp only [Matrix.mul_apply,hrow,nativeZoneAverage]
   have hs : (∑ z : Fin 3, nativeZoneTransport (zone31 i) z *
       (if zone31 j=z then (nativeZoneSize z)⁻¹ else 0)) =
       nativeZoneTransport (zone31 i) (zone31 j)*(nativeZoneSize (zone31 j))⁻¹ := by
     simp [mul_ite,eq_comm,Finset.sum_ite_eq']
   rw [hs]
   generalize zone31 i=zi, zone31 j=zj
   fin_cases zi <;> fin_cases zj <;>
     norm_num [nativeZoneTransport,nativeZoneSize,nativeZoneDegree]

 theorem native_constant_zone_factorization :
     nativeConstant=Cind31*nativeZoneConstant*nativeZoneAverage := by
   ext i j
   have hrow (z : Fin 3) : (Cind31*nativeZoneConstant) i z=nativeZoneConstant (zone31 i) z := by
     simp [Matrix.mul_apply,Cind31,Finset.sum_ite_eq']
   simp only [Matrix.mul_apply,hrow,nativeZoneAverage,nativeZoneConstant,nativeConstant]
   simp only [mul_ite,mul_zero,eq_comm,Finset.sum_ite_eq',Finset.mem_univ,if_true]
   field_simp [native_zone_size_nonzero]

 theorem native_zone_constant_transport_left :
     nativeZoneTransport*nativeZoneConstant=nativeZoneConstant := by
   ext a b; fin_cases a <;> fin_cases b <;>
     norm_num [nativeZoneTransport,nativeZoneConstant,nativeZoneSize,nativeZoneDegree,
       Matrix.mul_apply,Fin.sum_univ_succ]

 theorem native_zone_constant_transport_right :
     nativeZoneConstant*nativeZoneTransport=nativeZoneConstant := by
   ext a b; fin_cases a <;> fin_cases b <;>
     norm_num [nativeZoneTransport,nativeZoneConstant,nativeZoneSize,nativeZoneDegree,
       Matrix.mul_apply,Fin.sum_univ_succ]

 theorem native_zone_constant_idempotent : nativeZoneConstant*nativeZoneConstant=nativeZoneConstant := by
   ext a b; fin_cases a <;> fin_cases b <;>
     norm_num [nativeZoneConstant,nativeZoneSize,nativeZoneDegree,Matrix.mul_apply,Fin.sum_univ_succ]

 theorem native_zone_inverse_exact : nativeZoneH*nativeZoneHI=1 ∧ nativeZoneHI*nativeZoneH=1 := by
   have hh : nativeZoneH=!![49949/57440,6743/172320,1573/17232;
       5517/157960,23681/28720,8879/63184;1089/14360,7513/57440,45571/57440] := by
     ext a b; fin_cases a <;> fin_cases b <;>
       norm_num [nativeZoneH,nativeZoneTransport,nativeZoneConstant,nativeZoneSize,
         nativeZoneDegree,Matrix.mul_apply,Matrix.one_apply,Fin.ext_iff,Fin.sum_univ_succ]
   rw [hh]
   constructor <;> ext a b <;> fin_cases a <;> fin_cases b <;>
     norm_num [nativeZoneHI,Matrix.mul_apply,Matrix.one_apply,Fin.ext_iff,Fin.sum_univ_succ]

 theorem native_coarse_h_zone_lift :
     nativeCoarseH=1+Cind31*(nativeZoneH-1)*nativeZoneAverage := by
   unfold nativeCoarseH nativeZoneH
   rw [native_transport_zone_factorization,native_constant_zone_factorization]
   have hx : (Cind31*nativeZoneTransport*nativeZoneAverage)*
       (Cind31*nativeZoneTransport*nativeZoneAverage)=
       Cind31*(nativeZoneTransport*nativeZoneTransport)*nativeZoneAverage := by
     simp only [Matrix.mul_assoc]
     rw [← Matrix.mul_assoc nativeZoneAverage Cind31 _,native_zone_average_left_inverse,
       Matrix.one_mul]
   rw [hx]
   simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_add,Matrix.add_mul]
   abel

 theorem native_coarse_inverse_exact : nativeCoarseH*nativeCoarseHI=1 ∧ nativeCoarseHI*nativeCoarseH=1 := by
   rw [native_coarse_h_zone_lift]
   unfold nativeCoarseHI
   exact ⟨exact_zone_inverse_lift Cind31 nativeZoneAverage nativeZoneH nativeZoneHI
      native_zone_average_left_inverse native_zone_inverse_exact.1,
     exact_zone_inverse_lift Cind31 nativeZoneAverage nativeZoneHI nativeZoneH
      native_zone_average_left_inverse native_zone_inverse_exact.2⟩

 theorem native_constant_transport_left : fullTransport*nativeConstant=nativeConstant := by
   rw [native_transport_zone_factorization,native_constant_zone_factorization]
   simp only [Matrix.mul_assoc]
   rw [← Matrix.mul_assoc nativeZoneAverage Cind31 _,native_zone_average_left_inverse,Matrix.one_mul,
     ← Matrix.mul_assoc nativeZoneTransport nativeZoneConstant _,native_zone_constant_transport_left]

 theorem native_constant_transport_right : nativeConstant*fullTransport=nativeConstant := by
   rw [native_transport_zone_factorization,native_constant_zone_factorization]
   simp only [Matrix.mul_assoc]
   rw [← Matrix.mul_assoc nativeZoneAverage Cind31 _,native_zone_average_left_inverse,Matrix.one_mul,
     ← Matrix.mul_assoc nativeZoneConstant nativeZoneTransport _,native_zone_constant_transport_right]

 theorem native_constant_idempotent : nativeConstant*nativeConstant=nativeConstant := by
   rw [native_constant_zone_factorization]
   simp only [Matrix.mul_assoc]
   rw [← Matrix.mul_assoc nativeZoneAverage Cind31 _,native_zone_average_left_inverse,Matrix.one_mul,
     ← Matrix.mul_assoc nativeZoneConstant nativeZoneConstant _,native_zone_constant_idempotent]

 theorem native_constant_h_fixed : nativeCoarseH*nativeConstant=nativeConstant := by
   simp [nativeCoarseH,Matrix.add_mul,Matrix.sub_mul,Matrix.mul_assoc,
     native_constant_transport_left,native_constant_idempotent]

 theorem native_constant_hi_fixed : nativeCoarseHI*nativeConstant=nativeConstant :=
   full_constant_inverse nativeCoarseH nativeCoarseHI nativeConstant
     native_coarse_inverse_exact.2 native_constant_h_fixed

 theorem native_normalized_constant_zero : fullNormalizedLaplacian*nativeConstant=0 := by
   simp [fullNormalizedLaplacian,Matrix.sub_mul,native_constant_transport_left]

 local instance : DecidableEq LevelOneSceneHistory :=
   inferInstanceAs (DecidableEq {p : Fin 33 × Fin 33 // SceneStep p.1 p.2})

 def nativeIncoming : Matrix LevelOneSceneHistory (Fin 33) ℚ :=
   historyIncoming Jt C1 nativeHistoryReverse
 def nativeOutgoing : Matrix (Fin 33) LevelOneSceneHistory ℚ :=
   historyOutgoing Jt C1 nativeHistoryReverse
 def nativeFullProjection : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ :=
   fullHistoryProjection Jt nativeIncoming C1 nativeOutgoing nativeCoarseHI
 def nativeGeneratedHeat : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ :=
   generatedHistoryHeat Jt nativeIncoming C1 nativeOutgoing nativeCoarseHI fullNormalizedLaplacian

 theorem native_incoming_from_both_readouts : nativeIncoming=Js-Jt*fullTransport := by
   simp [nativeIncoming,historyIncoming,historyComplement,Matrix.sub_mul,Matrix.mul_assoc,
     actual_native_history_reverse_reads_source,actual_history_average_source]

 theorem native_endpoint_average_incoming_zero : C1*nativeIncoming=0 := by
   rw [native_incoming_from_both_readouts]
   simp [Matrix.mul_sub,← Matrix.mul_assoc,actual_history_average_left_inverse,
     actual_history_average_source]

 theorem native_outgoing_endpoint_zero : nativeOutgoing*Jt=0 := by
   have hq : historyComplement Jt C1*Jt=0 := by
     simp [historyComplement,Matrix.sub_mul,Matrix.mul_assoc,actual_history_average_left_inverse]
   simp [nativeOutgoing,historyOutgoing,Matrix.mul_assoc,hq]

 theorem native_outgoing_incoming_h : nativeOutgoing*nativeIncoming=nativeCoarseH-nativeConstant := by
   change historyOutgoing Jt C1 nativeHistoryReverse*historyIncoming Jt C1 nativeHistoryReverse=_
   have he := full_history_outgoing_incoming Jt C1 nativeHistoryReverse
     actual_history_average_left_inverse actual_native_history_reverse_involution
   rw [actual_native_history_compression] at he
   simpa [nativeCoarseH] using he

 theorem native_two_constant_readouts : Js*nativeConstant=Jt*nativeConstant := by
   ext e j
   change (∑ k : Fin 33, (if e.val.1=k then (1:ℚ) else 0)*(nativeZoneDegree (zone31 j)/718))=
     (∑ k : Fin 33, (if e.val.2=k then (1:ℚ) else 0)*(nativeZoneDegree (zone31 j)/718))
   simp only [ite_mul,eq_comm,
     one_mul,zero_mul,Finset.sum_ite_eq',Finset.mem_univ,if_true]

 theorem native_incoming_constant_zero : nativeIncoming*nativeConstant=0 := by
   rw [native_incoming_from_both_readouts]
   simp [Matrix.sub_mul,Matrix.mul_assoc,native_constant_transport_left,native_two_constant_readouts]

 theorem native_full_projector_endpoint : nativeFullProjection*Jt=Jt :=
   full_spectral_projection_endpoint Jt nativeIncoming C1 nativeOutgoing nativeCoarseHI
     actual_history_average_left_inverse native_outgoing_endpoint_zero

 theorem native_full_projector_incoming : nativeFullProjection*nativeIncoming=nativeIncoming :=
   full_spectral_projection_incoming Jt nativeIncoming C1 nativeOutgoing nativeCoarseH nativeCoarseHI
     nativeConstant native_endpoint_average_incoming_zero native_outgoing_incoming_h
     native_coarse_inverse_exact.2 native_constant_hi_fixed native_incoming_constant_zero

 theorem native_full_projector_idempotent : nativeFullProjection*nativeFullProjection=nativeFullProjection :=
   full_spectral_projection_idempotent Jt nativeIncoming C1 nativeOutgoing nativeCoarseHI
     native_full_projector_endpoint native_full_projector_incoming

 theorem native_generated_endpoint : nativeGeneratedHeat*Jt=Jt*fullNormalizedLaplacian :=
   generated_spectral_endpoint Jt nativeIncoming C1 nativeOutgoing nativeCoarseHI fullNormalizedLaplacian
     actual_history_average_left_inverse native_outgoing_endpoint_zero

 theorem native_generated_incoming : nativeGeneratedHeat*nativeIncoming=nativeIncoming*fullNormalizedLaplacian :=
   generated_spectral_incoming Jt nativeIncoming C1 nativeOutgoing nativeCoarseH nativeCoarseHI
     nativeConstant fullNormalizedLaplacian native_endpoint_average_incoming_zero native_outgoing_incoming_h
     native_coarse_inverse_exact.2 native_constant_hi_fixed native_normalized_constant_zero

 theorem native_transport_normalized_commute : fullTransport*fullNormalizedLaplacian=
     fullNormalizedLaplacian*fullTransport := by
   simp [fullNormalizedLaplacian,Matrix.mul_sub,Matrix.sub_mul]

 theorem native_both_readouts_determine_incoming (A : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ)
     (ht : A*Jt=Jt*fullNormalizedLaplacian) (hs : A*Js=Js*fullNormalizedLaplacian) :
     A*nativeIncoming=nativeIncoming*fullNormalizedLaplacian := by
   rw [native_incoming_from_both_readouts]
   simp only [Matrix.mul_sub,Matrix.sub_mul,← Matrix.mul_assoc,ht,hs]
   rw [Matrix.mul_assoc Jt fullTransport _,native_transport_normalized_commute]
   rw [← Matrix.mul_assoc]

 theorem native_generated_source : nativeGeneratedHeat*Js=Js*fullNormalizedLaplacian := by
   have hj : Js=nativeIncoming+Jt*fullTransport := by rw [native_incoming_from_both_readouts]; abel
   rw [hj,Matrix.mul_add,← Matrix.mul_assoc,native_generated_endpoint,native_generated_incoming]
   simp only [Matrix.add_mul]
   rw [Matrix.mul_assoc Jt fullNormalizedLaplacian _,← native_transport_normalized_commute,
     ← Matrix.mul_assoc]

 theorem native_full_projector_source : nativeFullProjection*Js=Js := by
   have hj : Js=nativeIncoming+Jt*fullTransport := by rw [native_incoming_from_both_readouts]; abel
   rw [hj,Matrix.mul_add,← Matrix.mul_assoc,native_full_projector_endpoint,native_full_projector_incoming]

 theorem native_all_joint_readouts_determine_generated_heat
     (A : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ)
     (ht : A*Jt=Jt*fullNormalizedLaplacian) (hs : A*Js=Js*fullNormalizedLaplacian) :
     A*nativeFullProjection=nativeGeneratedHeat :=
   two_retained_readouts_determine_generated_block A Jt nativeIncoming C1 nativeOutgoing
     nativeCoarseHI fullNormalizedLaplacian ht (native_both_readouts_determine_incoming A ht hs)

 theorem native_degree_inverse_selfadjoint : fullDegreeInv.transpose=fullDegreeInv := by
   simp [fullDegreeInv]

 theorem native_adjacency_selfadjoint : Adj31.transpose=Adj31 := by
   ext i j; simp [Adj31,eq_comm]

 theorem native_transport_weighted_selfadjoint : (fullTransport*fullDegreeInv).transpose=
     fullTransport*fullDegreeInv := by
   simp [fullTransport,Matrix.transpose_mul,native_degree_inverse_selfadjoint,
     native_adjacency_selfadjoint,Matrix.mul_assoc]

 theorem native_constant_weighted_entry (i j : Fin 33) :
     (nativeConstant*fullDegreeInv) i j=1/718 := by
   simp only [fullDegreeInv,Matrix.mul_diagonal,nativeConstant,native_full_degree_by_zone]
   have hn : nativeZoneDegree (zone31 j)≠0 := by
     generalize zone31 j=z
     fin_cases z <;> norm_num [nativeZoneDegree]
   field_simp

 theorem native_constant_weighted_selfadjoint : (nativeConstant*fullDegreeInv).transpose=
     nativeConstant*fullDegreeInv := by
   ext i j; simp only [Matrix.transpose_apply,native_constant_weighted_entry]

 theorem native_coarse_h_weighted_selfadjoint : (nativeCoarseH*fullDegreeInv).transpose=
     nativeCoarseH*fullDegreeInv := by
   have ht := weighted_commuting_product_selfadjoint fullTransport fullTransport fullDegreeInv
     native_degree_inverse_selfadjoint native_transport_weighted_selfadjoint
     native_transport_weighted_selfadjoint rfl
   have hp : fullDegreeInv*nativeConstant.transpose=nativeConstant*fullDegreeInv := by
     simpa only [Matrix.transpose_mul,native_degree_inverse_selfadjoint] using native_constant_weighted_selfadjoint
   simp [nativeCoarseH,Matrix.add_mul,Matrix.sub_mul,Matrix.transpose_add,Matrix.transpose_sub,
     native_degree_inverse_selfadjoint,ht,hp]

 theorem native_coarse_hi_weighted_selfadjoint : (nativeCoarseHI*fullDegreeInv).transpose=
     nativeCoarseHI*fullDegreeInv :=
   weighted_inverse_selfadjoint nativeCoarseH nativeCoarseHI fullDegreeInv
     native_degree_inverse_selfadjoint native_coarse_h_weighted_selfadjoint
     native_coarse_inverse_exact.2

 theorem native_normalized_weighted_selfadjoint : (fullNormalizedLaplacian*fullDegreeInv).transpose=
     fullNormalizedLaplacian*fullDegreeInv := by
   have ht : fullDegreeInv*fullTransport.transpose=fullTransport*fullDegreeInv := by
     simpa only [Matrix.transpose_mul,native_degree_inverse_selfadjoint] using native_transport_weighted_selfadjoint
   simp [fullNormalizedLaplacian,Matrix.sub_mul,Matrix.transpose_sub,native_degree_inverse_selfadjoint,
     ht]

 theorem native_h_normalized_commute : nativeCoarseH*fullNormalizedLaplacian=
     fullNormalizedLaplacian*nativeCoarseH := by
   unfold nativeCoarseH fullNormalizedLaplacian
   simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_add,Matrix.add_mul,Matrix.one_mul,
     Matrix.mul_one,Matrix.mul_assoc,native_constant_transport_left,native_constant_transport_right]
   abel

 theorem native_hi_normalized_commute : nativeCoarseHI*fullNormalizedLaplacian=
     fullNormalizedLaplacian*nativeCoarseHI := by
   calc
     _ = nativeCoarseHI*(fullNormalizedLaplacian*nativeCoarseH)*nativeCoarseHI := by
       simp [Matrix.mul_assoc,native_coarse_inverse_exact.1]
     _ = nativeCoarseHI*(nativeCoarseH*fullNormalizedLaplacian)*nativeCoarseHI := by
       rw [native_h_normalized_commute]
     _ = _ := by simp [← Matrix.mul_assoc,native_coarse_inverse_exact.2]

 theorem native_history_average_weighted_adjoint : C1=fullDegreeInv*Jt.transpose := by
   rw [← actual_endpoint_average_binding,← actual_endpoint_lift_binding]
   simpa [fullDegreeInv,actual_endpoint_degree_binding] using endpoint_average_is_weighted_adjoint SceneStep

 theorem native_history_complement_selfadjoint : (historyComplement Jt C1).transpose=
     historyComplement Jt C1 := by
   change (1-historyProjection Jt C1).transpose=1-historyProjection Jt C1
   simp [Matrix.transpose_sub,actual_native_history_projection_selfadjoint]

 theorem native_outgoing_weighted_adjoint : nativeOutgoing=fullDegreeInv*nativeIncoming.transpose := by
   unfold nativeOutgoing nativeIncoming historyOutgoing historyIncoming
   rw [Matrix.transpose_mul,Matrix.transpose_mul,actual_native_history_reverse_selfadjoint,
     native_history_complement_selfadjoint,native_history_average_weighted_adjoint]
   simp only [Matrix.mul_assoc]

 theorem native_full_projector_selfadjoint : nativeFullProjection.transpose=nativeFullProjection :=
   full_projector_selfadjoint Jt nativeIncoming C1 nativeOutgoing nativeCoarseHI
     actual_native_history_projection_selfadjoint
     (paired_block_selfadjoint nativeIncoming nativeOutgoing nativeCoarseHI fullDegreeInv
       native_outgoing_weighted_adjoint native_coarse_hi_weighted_selfadjoint)

 theorem native_generated_heat_selfadjoint : nativeGeneratedHeat.transpose=nativeGeneratedHeat := by
   have hj : (Jt*fullNormalizedLaplacian*C1).transpose=Jt*fullNormalizedLaplacian*C1 :=
     paired_block_selfadjoint Jt C1 fullNormalizedLaplacian fullDegreeInv
       native_history_average_weighted_adjoint native_normalized_weighted_selfadjoint
   have hx : ((fullNormalizedLaplacian*nativeCoarseHI)*fullDegreeInv).transpose=
       (fullNormalizedLaplacian*nativeCoarseHI)*fullDegreeInv :=
     weighted_commuting_product_selfadjoint fullNormalizedLaplacian nativeCoarseHI fullDegreeInv
       native_degree_inverse_selfadjoint native_normalized_weighted_selfadjoint
       native_coarse_hi_weighted_selfadjoint native_hi_normalized_commute.symm
   have he := paired_block_selfadjoint nativeIncoming nativeOutgoing
     (fullNormalizedLaplacian*nativeCoarseHI) fullDegreeInv native_outgoing_weighted_adjoint hx
   unfold nativeGeneratedHeat generatedHistoryHeat
   simp only [Matrix.transpose_add,hj]
   simpa only [Matrix.mul_assoc] using congrArg (fun X => Jt*fullNormalizedLaplacian*C1+X) he

 theorem native_generated_heat_supported : nativeGeneratedHeat*nativeFullProjection=nativeGeneratedHeat :=
   native_all_joint_readouts_determine_generated_heat nativeGeneratedHeat native_generated_endpoint native_generated_source

 theorem native_complete_symmetric_joint_history_extensions
     (A : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ) :
     (A.transpose=A ∧ A*Jt=Jt*fullNormalizedLaplacian ∧ A*Js=Js*fullNormalizedLaplacian) ↔
     ∃ B : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ,
       B.transpose=B ∧ B*nativeFullProjection=0 ∧ nativeFullProjection*B=0 ∧ A=nativeGeneratedHeat+B := by
   have he := complete_supported_symmetric_extension_iff A nativeGeneratedHeat nativeFullProjection
     native_generated_heat_selfadjoint native_full_projector_selfadjoint
     native_generated_heat_supported
   constructor
   · rintro ⟨ha,ht,hs⟩
     exact he.mp ⟨ha,native_all_joint_readouts_determine_generated_heat A ht hs⟩
   · intro h
     obtain ⟨B,hb,hbk,hkb,hA⟩ := h
     have hbt := complete_extension_endpoint_invisible nativeFullProjection Jt B native_full_projector_endpoint hbk
     have hbs := complete_extension_endpoint_invisible nativeFullProjection Js B native_full_projector_source hbk
     rw [hA]
     exact ⟨by simp [Matrix.transpose_add,native_generated_heat_selfadjoint,hb],
       by simp [Matrix.add_mul,native_generated_endpoint,hbt],
       by simp [Matrix.add_mul,native_generated_source,hbs]⟩

 theorem native_complete_joint_parameter_unique (B1 B2 : Matrix LevelOneSceneHistory LevelOneSceneHistory ℚ) :
     nativeGeneratedHeat+B1=nativeGeneratedHeat+B2 ↔ B1=B2 :=
   complete_supported_extension_parameter_unique nativeGeneratedHeat B1 B2

 theorem native_full_complement_supported : (1-nativeFullProjection)*nativeFullProjection=0 ∧
     nativeFullProjection*(1-nativeFullProjection)=0 := by
   simp [Matrix.sub_mul,Matrix.mul_sub,native_full_projector_idempotent]

 theorem native_scalar_complement_keeps_both_readouts (s : ℚ) :
     (nativeGeneratedHeat+s • (1-nativeFullProjection)).transpose=nativeGeneratedHeat+s • (1-nativeFullProjection) ∧
     (nativeGeneratedHeat+s • (1-nativeFullProjection))*Jt=Jt*fullNormalizedLaplacian ∧
     (nativeGeneratedHeat+s • (1-nativeFullProjection))*Js=Js*fullNormalizedLaplacian := by
   apply (native_complete_symmetric_joint_history_extensions _).mpr
   refine ⟨s • (1-nativeFullProjection),?_,?_,?_,rfl⟩
   · simp [Matrix.transpose_smul,Matrix.transpose_sub,native_full_projector_selfadjoint]
   · simp [Matrix.smul_mul,native_full_complement_supported.1]
   · simp [Matrix.mul_smul,native_full_complement_supported.2]

 def nativeRectangleEdge (u v : Fin 33) (h : SceneStep u v) : LevelOneSceneHistory := ⟨(u,v),h⟩
 def edge09 : LevelOneSceneHistory := nativeRectangleEdge 0 9 (by decide)
 def edge19 : LevelOneSceneHistory := nativeRectangleEdge 1 9 (by decide)
 def edge010 : LevelOneSceneHistory := nativeRectangleEdge 0 10 (by decide)
 def edge110 : LevelOneSceneHistory := nativeRectangleEdge 1 10 (by decide)
 def nativeArchiveRectangle : LevelOneSceneHistory → ℚ :=
   Pi.single edge09 1-Pi.single edge19 1-Pi.single edge010 1+Pi.single edge110 1

 theorem native_archive_rectangle_endpoint_zero : C1.mulVec nativeArchiveRectangle=0 := by
   ext v
   simp only [nativeArchiveRectangle,Matrix.mulVec_add,Matrix.mulVec_sub,Matrix.mulVec_single,
     Pi.add_apply,Pi.sub_apply,smul_eq_mul,C1,Matrix.of_apply,endpoint,
     edge09,edge19,edge010,edge110,nativeRectangleEdge]
   simp

 theorem native_archive_rectangle_reversed_endpoint_zero : (C1*nativeHistoryReverse).mulVec nativeArchiveRectangle=0 := by
   have hr : C1*nativeHistoryReverse=fullDegreeInv*Js.transpose := by
     rw [native_history_average_weighted_adjoint]
     have hs : Jt.transpose*nativeHistoryReverse=Js.transpose := by
       have h := congrArg Matrix.transpose actual_native_history_reverse_reads_source
       simpa [Matrix.transpose_mul,actual_native_history_reverse_selfadjoint] using h
     rw [Matrix.mul_assoc,hs]
   rw [hr,← Matrix.mulVec_mulVec]
   have hs : Js.transpose.mulVec nativeArchiveRectangle=0 := by
     ext v
     simp only [nativeArchiveRectangle,Matrix.mulVec_add,Matrix.mulVec_sub,Matrix.mulVec_single,
       Pi.add_apply,Pi.sub_apply,smul_eq_mul,Matrix.transpose_apply,Js,Matrix.of_apply,
       D0.VNext2.SceneEndpointReynoldsExpectation.source,
       edge09,edge19,edge010,edge110,nativeRectangleEdge]
     simp
   rw [hs,Matrix.mulVec_zero]

 theorem native_archive_rectangle_outgoing_zero : nativeOutgoing.mulVec nativeArchiveRectangle=0 := by
   have hq : (historyComplement Jt C1).mulVec nativeArchiveRectangle=nativeArchiveRectangle := by
     simp [historyComplement,Matrix.sub_mulVec,← Matrix.mulVec_mulVec,native_archive_rectangle_endpoint_zero]
   unfold nativeOutgoing historyOutgoing
   rw [← Matrix.mulVec_mulVec,hq]
   exact native_archive_rectangle_reversed_endpoint_zero

 theorem native_archive_rectangle_projected_zero : nativeFullProjection.mulVec nativeArchiveRectangle=0 := by
   simp [nativeFullProjection,fullHistoryProjection,Matrix.add_mulVec,← Matrix.mulVec_mulVec,
     native_archive_rectangle_endpoint_zero,native_archive_rectangle_outgoing_zero]

 theorem native_archive_rectangle_nonzero : nativeArchiveRectangle≠0 := by
   have h1 : edge09≠edge19 := by
     intro h; have hv := congrArg (fun e : LevelOneSceneHistory => e.val) h
     norm_num [edge09,edge19,nativeRectangleEdge,Prod.mk.injEq,Fin.ext_iff] at hv
   have h2 : edge09≠edge010 := by
     intro h; have hv := congrArg (fun e : LevelOneSceneHistory => e.val) h
     norm_num [edge09,edge010,nativeRectangleEdge,Prod.mk.injEq,Fin.ext_iff] at hv
   have h3 : edge09≠edge110 := by
     intro h; have hv := congrArg (fun e : LevelOneSceneHistory => e.val) h
     norm_num [edge09,edge110,nativeRectangleEdge,Prod.mk.injEq,Fin.ext_iff] at hv
   intro h
   have h0 := congrFun h edge09
   norm_num [nativeArchiveRectangle,Pi.single_apply,h1,h2,h3] at h0

 theorem native_full_complement_nonzero : 1-nativeFullProjection≠0 := by
   intro h
   have hw := congrArg (fun M => M.mulVec nativeArchiveRectangle) h
   simp only [Matrix.sub_mulVec,Matrix.one_mulVec,native_archive_rectangle_projected_zero,
     sub_zero,Matrix.zero_mulVec] at hw
   exact native_archive_rectangle_nonzero hw

 theorem native_zone_constant_trace : nativeZoneConstant.trace=1 := by
   norm_num [Matrix.trace,nativeZoneConstant,nativeZoneSize,nativeZoneDegree,Fin.sum_univ_succ]

 theorem native_constant_trace : nativeConstant.trace=1 := by
   rw [native_constant_zone_factorization,Matrix.trace_mul_cycle]
   rw [native_zone_average_left_inverse,Matrix.one_mul,native_zone_constant_trace]

 theorem native_full_projector_trace : nativeFullProjection.trace=65 := by
   unfold nativeFullProjection fullHistoryProjection
   rw [Matrix.trace_add,Matrix.trace_mul_comm,actual_history_average_left_inverse,
     Matrix.trace_mul_cycle]
   rw [native_outgoing_incoming_h,Matrix.trace_mul_comm,Matrix.mul_sub,
     native_coarse_inverse_exact.2,native_constant_hi_fixed,Matrix.trace_sub,native_constant_trace]
   norm_num [Matrix.trace_one]

 theorem native_history_cardinality_in_kernel : (Fintype.card LevelOneSceneHistory : ℚ)=718 := by
   have h : (Fintype.card LevelOneSceneHistory : ℚ)=∑ a : Fin 33, fullDegreeValue a := by
     have he := sum_over_actual_edges SceneStep (fun _ => (1:ℚ))
     simpa [Edge,LevelOneSceneHistory,actual_scene_relation_iff,fullDegreeValue,Adj31] using he
   rw [h]
   simp only [native_full_degree_by_zone,Fin.sum_univ_succ]
   norm_num [nativeZoneDegree,zone31,Matrix.cons_val_two]

 theorem native_full_complement_trace : (1-nativeFullProjection).trace=653 := by
   rw [Matrix.trace_sub,native_full_projector_trace,Matrix.trace_one,native_history_cardinality_in_kernel]
   norm_num

 theorem native_reverse_reads_endpoint : nativeHistoryReverse*Js=Jt := by
   rw [← actual_native_history_reverse_reads_source,← Matrix.mul_assoc,
     actual_native_history_reverse_involution,Matrix.one_mul]

 theorem native_reverse_incoming : nativeHistoryReverse*nativeIncoming=Jt-Js*fullTransport := by
   rw [native_incoming_from_both_readouts,Matrix.mul_sub,← Matrix.mul_assoc,
     native_reverse_reads_endpoint,actual_native_history_reverse_reads_source]

 theorem native_full_projector_preserves_reversed_incoming :
     nativeFullProjection*(nativeHistoryReverse*nativeIncoming)=nativeHistoryReverse*nativeIncoming := by
   rw [native_reverse_incoming,Matrix.mul_sub,← Matrix.mul_assoc,native_full_projector_endpoint,
     native_full_projector_source]

 theorem native_full_projector_reverse_commute : nativeFullProjection*nativeHistoryReverse=
     nativeHistoryReverse*nativeFullProjection :=
   generated_projector_commutes_preserving_reverse Jt nativeIncoming C1 nativeOutgoing nativeCoarseHI
     nativeHistoryReverse native_full_projector_selfadjoint actual_native_history_reverse_selfadjoint
     (by rw [actual_native_history_reverse_reads_source]; exact native_full_projector_source)
     native_full_projector_preserves_reversed_incoming

 theorem native_generated_reverse_joint_readouts :
     (nativeGeneratedHeat*nativeHistoryReverse)*Jt=(nativeHistoryReverse*nativeGeneratedHeat)*Jt ∧
     (nativeGeneratedHeat*nativeHistoryReverse)*nativeIncoming=
       (nativeHistoryReverse*nativeGeneratedHeat)*nativeIncoming := by
   constructor
   · calc
       _ = nativeGeneratedHeat*(nativeHistoryReverse*Jt) := by rw [Matrix.mul_assoc]
       _ = Js*fullNormalizedLaplacian := by rw [actual_native_history_reverse_reads_source,native_generated_source]
       _ = nativeHistoryReverse*(nativeGeneratedHeat*Jt) := by
         rw [native_generated_endpoint,← Matrix.mul_assoc,actual_native_history_reverse_reads_source]
       _ = _ := by rw [Matrix.mul_assoc]
   · rw [Matrix.mul_assoc,native_reverse_incoming,Matrix.mul_sub,
       ← Matrix.mul_assoc,native_generated_endpoint,native_generated_source]
     rw [Matrix.mul_assoc _ nativeGeneratedHeat _,native_generated_incoming,← Matrix.mul_assoc,
       native_reverse_incoming,Matrix.sub_mul]
     rw [Matrix.mul_assoc Js fullNormalizedLaplacian _,← native_transport_normalized_commute,
       ← Matrix.mul_assoc]

 theorem native_generated_reverse_commute : nativeGeneratedHeat*nativeHistoryReverse=
     nativeHistoryReverse*nativeGeneratedHeat := by
   have hblock : (nativeGeneratedHeat*nativeHistoryReverse)*nativeFullProjection=
       (nativeHistoryReverse*nativeGeneratedHeat)*nativeFullProjection := by
     unfold nativeFullProjection fullHistoryProjection
     simp only [Matrix.mul_add,← Matrix.mul_assoc,
       native_generated_reverse_joint_readouts.1,native_generated_reverse_joint_readouts.2]
   have hl : (nativeGeneratedHeat*nativeHistoryReverse)*nativeFullProjection=
       nativeGeneratedHeat*nativeHistoryReverse := by
     rw [Matrix.mul_assoc,← native_full_projector_reverse_commute,← Matrix.mul_assoc,
       native_generated_heat_supported]
   have hr : (nativeHistoryReverse*nativeGeneratedHeat)*nativeFullProjection=
       nativeHistoryReverse*nativeGeneratedHeat := by
     rw [Matrix.mul_assoc,native_generated_heat_supported]
   simpa only [hl,hr] using hblock

 theorem native_scalar_complement_reverse_commute (s : ℚ) :
     (nativeGeneratedHeat+s • (1-nativeFullProjection))*nativeHistoryReverse=
       nativeHistoryReverse*(nativeGeneratedHeat+s • (1-nativeFullProjection)) := by
   simp [Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,Matrix.mul_smul,Matrix.sub_mul,
     Matrix.mul_sub,native_generated_reverse_commute,native_full_projector_reverse_commute]

 theorem native_scalar_complement_parameter_distinct (s t : ℚ) :
     nativeGeneratedHeat+s • (1-nativeFullProjection)=nativeGeneratedHeat+t • (1-nativeFullProjection) ↔ s=t := by
   rw [add_left_cancel_iff]
   exact (smul_left_injective ℚ native_full_complement_nonzero).eq_iff

end
end D0.Research.NativeSceneHistoryFeedback

namespace D0.Research.NativeSceneHistoryFeedback
noncomputable section
open Real

def scalarCompletedHeat (generated beta s : ℝ) : ℝ := generated+653*Real.exp (-beta*s)
def scalarCompletedAction (generated beta feedback s : ℝ) : ℝ :=
  beta⁻¹*Real.log (scalarCompletedHeat generated beta s)-feedback

theorem scalar_completed_heat_positive (g beta s : ℝ) (hg : 0<g) :
    0<scalarCompletedHeat g beta s := by
  unfold scalarCompletedHeat
  positivity

theorem scalar_completed_heat_genuine_derivative (g beta s : ℝ) :
    HasDerivAt (scalarCompletedHeat g beta) (-653*beta*Real.exp (-beta*s)) s := by
  have h := ((hasDerivAt_const s (-beta)).mul (hasDerivAt_id s)).exp
  have he := (h.const_mul 653).const_add g
  convert he using 1 <;> simp [scalarCompletedHeat] <;> ring

theorem scalar_completed_action_genuine_derivative (g beta f s : ℝ)
    (hg : 0<g) (hb : beta≠0) :
    HasDerivAt (scalarCompletedAction g beta f)
      (-653*Real.exp (-beta*s)/scalarCompletedHeat g beta s) s := by
  have hz : scalarCompletedHeat g beta s≠0 := ne_of_gt (scalar_completed_heat_positive g beta s hg)
  have h := ((scalar_completed_heat_genuine_derivative g beta s).log hz).const_mul beta⁻¹
  have hf := h.sub_const f
  convert hf using 1 <;> field_simp

theorem scalar_completed_action_derivative_nonzero (g beta f s : ℝ)
    (hg : 0<g) (hb : beta≠0) :
    deriv (scalarCompletedAction g beta f) s≠0 := by
  rw [(scalar_completed_action_genuine_derivative g beta f s hg hb).deriv]
  have hz := scalar_completed_heat_positive g beta s hg
  have he := Real.exp_pos (-beta*s)
  apply ne_of_lt
  exact div_neg_of_neg_of_pos (by nlinarith) hz

theorem full_and_scene_heat_source_agree_iff (x y xp yp : ℝ) (hx : x≠0) (ht : 2*x-1+y≠0) :
    (2*xp+yp)/(2*x-1+y)=xp/x ↔ x*yp=(y-1)*xp := by
  constructor
  · intro h
    have hm : (2*xp+yp)*x=xp*(2*x-1+y) := (div_eq_div_iff ht hx).mp h
    nlinarith
  · intro h
    apply (div_eq_div_iff ht hx).mpr
    nlinarith

end
end D0.Research.NativeSceneHistoryFeedback

#check D0.Research.NativeSceneHistoryFeedback.sum_over_actual_edges
#print axioms D0.Research.NativeSceneHistoryFeedback.sum_over_actual_edges
#check D0.Research.NativeSceneHistoryFeedback.endpoint_lift_gram
#print axioms D0.Research.NativeSceneHistoryFeedback.endpoint_lift_gram
#check D0.Research.NativeSceneHistoryFeedback.endpoint_average_is_weighted_adjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.endpoint_average_is_weighted_adjoint
#check D0.Research.NativeSceneHistoryFeedback.endpoint_average_exact_left_inverse
#print axioms D0.Research.NativeSceneHistoryFeedback.endpoint_average_exact_left_inverse
#check D0.Research.NativeSceneHistoryFeedback.endpoint_reynolds_is_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.endpoint_reynolds_is_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.endpoint_source_average
#print axioms D0.Research.NativeSceneHistoryFeedback.endpoint_source_average
#check D0.Research.NativeSceneHistoryFeedback.history_reverse_is_involution
#print axioms D0.Research.NativeSceneHistoryFeedback.history_reverse_is_involution
#check D0.Research.NativeSceneHistoryFeedback.history_reverse_is_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.history_reverse_is_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.history_reverse_is_orthogonal
#print axioms D0.Research.NativeSceneHistoryFeedback.history_reverse_is_orthogonal
#check D0.Research.NativeSceneHistoryFeedback.history_reverse_recovers_source
#print axioms D0.Research.NativeSceneHistoryFeedback.history_reverse_recovers_source
#check D0.Research.NativeSceneHistoryFeedback.complete_history_relabel_reverse_naturality
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_history_relabel_reverse_naturality
#check D0.Research.NativeSceneHistoryFeedback.complete_history_relabel_keeps_both_readouts
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_history_relabel_keeps_both_readouts
#check D0.Research.NativeSceneHistoryFeedback.complete_history_projection_idempotent
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_history_projection_idempotent
#check D0.Research.NativeSceneHistoryFeedback.involutive_history_exact_feedback
#print axioms D0.Research.NativeSceneHistoryFeedback.involutive_history_exact_feedback
#check D0.Research.NativeSceneHistoryFeedback.history_feedback_retains_whole_vertex_response
#print axioms D0.Research.NativeSceneHistoryFeedback.history_feedback_retains_whole_vertex_response
#check D0.Research.NativeSceneHistoryFeedback.history_feedback_determinant_exact
#print axioms D0.Research.NativeSceneHistoryFeedback.history_feedback_determinant_exact
#check D0.Research.NativeSceneHistoryFeedback.every_native_even_history_returns
#print axioms D0.Research.NativeSceneHistoryFeedback.every_native_even_history_returns
#check D0.Research.NativeSceneHistoryFeedback.every_native_odd_history_returns
#print axioms D0.Research.NativeSceneHistoryFeedback.every_native_odd_history_returns
#check D0.Research.NativeSceneHistoryFeedback.every_even_history_feedback_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.every_even_history_feedback_zero
#check D0.Research.NativeSceneHistoryFeedback.history_kernel_is_fully_retained
#print axioms D0.Research.NativeSceneHistoryFeedback.history_kernel_is_fully_retained
#check D0.Research.NativeSceneHistoryFeedback.exact_full_history_resolvent
#print axioms D0.Research.NativeSceneHistoryFeedback.exact_full_history_resolvent
#check D0.Research.NativeSceneHistoryFeedback.exact_full_history_resolvent_compression
#print axioms D0.Research.NativeSceneHistoryFeedback.exact_full_history_resolvent_compression
#check D0.Research.NativeSceneHistoryFeedback.full_history_complement_idempotent
#print axioms D0.Research.NativeSceneHistoryFeedback.full_history_complement_idempotent
#check D0.Research.NativeSceneHistoryFeedback.full_history_incoming_delay
#print axioms D0.Research.NativeSceneHistoryFeedback.full_history_incoming_delay
#check D0.Research.NativeSceneHistoryFeedback.all_native_archive_delays_reconstructed
#print axioms D0.Research.NativeSceneHistoryFeedback.all_native_archive_delays_reconstructed
#check D0.Research.NativeSceneHistoryFeedback.full_history_outgoing_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.full_history_outgoing_incoming
#check D0.Research.NativeSceneHistoryFeedback.complete_native_archive_return_kernel
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_native_archive_return_kernel
#check D0.Research.NativeSceneHistoryFeedback.actual_scene_relation_symmetric
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_scene_relation_symmetric
#check D0.Research.NativeSceneHistoryFeedback.actual_scene_relation_iff
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_scene_relation_iff
#check D0.Research.NativeSceneHistoryFeedback.actual_scene_adjacency_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_scene_adjacency_binding
#check D0.Research.NativeSceneHistoryFeedback.actual_endpoint_degree_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_endpoint_degree_binding
#check D0.Research.NativeSceneHistoryFeedback.graph_endpoint_degree_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.graph_endpoint_degree_nonzero
#check D0.Research.NativeSceneHistoryFeedback.actual_endpoint_degree_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_endpoint_degree_nonzero
#check D0.Research.NativeSceneHistoryFeedback.actual_endpoint_lift_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_endpoint_lift_binding
#check D0.Research.NativeSceneHistoryFeedback.actual_source_lift_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_source_lift_binding
#check D0.Research.NativeSceneHistoryFeedback.actual_endpoint_average_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_endpoint_average_binding
#check D0.Research.NativeSceneHistoryFeedback.actual_transport_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_transport_binding
#check D0.Research.NativeSceneHistoryFeedback.actual_history_average_left_inverse
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_history_average_left_inverse
#check D0.Research.NativeSceneHistoryFeedback.actual_history_average_source
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_history_average_source
#check D0.Research.NativeSceneHistoryFeedback.actual_history_reverse_owner_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_history_reverse_owner_binding
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_reverse_involution
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_reverse_involution
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_reverse_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_reverse_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_projection_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_projection_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_reverse_reads_source
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_reverse_reads_source
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_compression
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_compression
#check D0.Research.NativeSceneHistoryFeedback.normalized_scene_return_feedback_polynomial
#print axioms D0.Research.NativeSceneHistoryFeedback.normalized_scene_return_feedback_polynomial
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_feedback
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_feedback
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_feedback_determinant
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_feedback_determinant
#check D0.Research.NativeSceneHistoryFeedback.actual_native_all_archive_return_kernels
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_all_archive_return_kernels
#check D0.Research.NativeSceneHistoryFeedback.actual_native_full_resolvent_compression
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_full_resolvent_compression
#check D0.Research.NativeSceneHistoryFeedback.actual_native_two_returns_recover_all_vertices
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_two_returns_recover_all_vertices
#check D0.Research.NativeSceneHistoryFeedback.actual_native_two_return_feedback_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_two_return_feedback_zero
#check D0.Research.NativeSceneHistoryFeedback.actual_archive_adjacency_binding
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_archive_adjacency_binding
#check D0.Research.NativeSceneHistoryFeedback.actual_balanced_archive_transport_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_balanced_archive_transport_zero
#check D0.Research.NativeSceneHistoryFeedback.actual_balanced_archive_full_history_feedback
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_balanced_archive_full_history_feedback
#check D0.Research.NativeSceneHistoryFeedback.actual_balanced_archive_two_history_return
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_balanced_archive_two_history_return
#check D0.Research.NativeSceneHistoryFeedback.actual_archive_witness_balanced
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_archive_witness_balanced
#check D0.Research.NativeSceneHistoryFeedback.actual_archive_witness_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_archive_witness_nonzero
#check D0.Research.NativeSceneHistoryFeedback.actual_native_history_feedback_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_native_history_feedback_nonzero
#check D0.Research.NativeSceneHistoryFeedback.actual_no_repeated_forgetting_return
#print axioms D0.Research.NativeSceneHistoryFeedback.actual_no_repeated_forgetting_return
#check D0.Research.NativeSceneHistoryFeedback.full_constant_inverse
#print axioms D0.Research.NativeSceneHistoryFeedback.full_constant_inverse
#check D0.Research.NativeSceneHistoryFeedback.full_spectral_projection_endpoint
#print axioms D0.Research.NativeSceneHistoryFeedback.full_spectral_projection_endpoint
#check D0.Research.NativeSceneHistoryFeedback.full_spectral_projection_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.full_spectral_projection_incoming
#check D0.Research.NativeSceneHistoryFeedback.full_spectral_projection_idempotent
#print axioms D0.Research.NativeSceneHistoryFeedback.full_spectral_projection_idempotent
#check D0.Research.NativeSceneHistoryFeedback.generated_spectral_endpoint
#print axioms D0.Research.NativeSceneHistoryFeedback.generated_spectral_endpoint
#check D0.Research.NativeSceneHistoryFeedback.generated_spectral_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.generated_spectral_incoming
#check D0.Research.NativeSceneHistoryFeedback.two_retained_readouts_determine_generated_block
#print axioms D0.Research.NativeSceneHistoryFeedback.two_retained_readouts_determine_generated_block
#check D0.Research.NativeSceneHistoryFeedback.full_projector_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.full_projector_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.complete_symmetric_history_extension
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_symmetric_history_extension
#check D0.Research.NativeSceneHistoryFeedback.complete_history_readout_extension
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_history_readout_extension
#check D0.Research.NativeSceneHistoryFeedback.all_symmetric_history_extensions
#print axioms D0.Research.NativeSceneHistoryFeedback.all_symmetric_history_extensions
#check D0.Research.NativeSceneHistoryFeedback.complete_supported_symmetric_extension_iff
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_supported_symmetric_extension_iff
#check D0.Research.NativeSceneHistoryFeedback.complete_supported_extension_parameter_unique
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_supported_extension_parameter_unique
#check D0.Research.NativeSceneHistoryFeedback.complete_extension_endpoint_invisible
#print axioms D0.Research.NativeSceneHistoryFeedback.complete_extension_endpoint_invisible
#check D0.Research.NativeSceneHistoryFeedback.exact_zone_inverse_lift
#print axioms D0.Research.NativeSceneHistoryFeedback.exact_zone_inverse_lift
#check D0.Research.NativeSceneHistoryFeedback.weighted_commuting_product_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.weighted_commuting_product_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.weighted_inverse_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.weighted_inverse_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.paired_block_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.paired_block_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.generated_projector_commutes_preserving_reverse
#print axioms D0.Research.NativeSceneHistoryFeedback.generated_projector_commutes_preserving_reverse
#check D0.Research.NativeSceneHistoryFeedback.native_zone_counts_kernel
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_counts_kernel
#check D0.Research.NativeSceneHistoryFeedback.native_zone_size_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_size_nonzero
#check D0.Research.NativeSceneHistoryFeedback.native_zone_average_left_inverse
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_average_left_inverse
#check D0.Research.NativeSceneHistoryFeedback.native_full_degree_by_zone
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_degree_by_zone
#check D0.Research.NativeSceneHistoryFeedback.native_transport_entry
#print axioms D0.Research.NativeSceneHistoryFeedback.native_transport_entry
#check D0.Research.NativeSceneHistoryFeedback.native_transport_zone_factorization
#print axioms D0.Research.NativeSceneHistoryFeedback.native_transport_zone_factorization
#check D0.Research.NativeSceneHistoryFeedback.native_constant_zone_factorization
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_zone_factorization
#check D0.Research.NativeSceneHistoryFeedback.native_zone_constant_transport_left
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_constant_transport_left
#check D0.Research.NativeSceneHistoryFeedback.native_zone_constant_transport_right
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_constant_transport_right
#check D0.Research.NativeSceneHistoryFeedback.native_zone_constant_idempotent
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_constant_idempotent
#check D0.Research.NativeSceneHistoryFeedback.native_zone_inverse_exact
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_inverse_exact
#check D0.Research.NativeSceneHistoryFeedback.native_coarse_h_zone_lift
#print axioms D0.Research.NativeSceneHistoryFeedback.native_coarse_h_zone_lift
#check D0.Research.NativeSceneHistoryFeedback.native_coarse_inverse_exact
#print axioms D0.Research.NativeSceneHistoryFeedback.native_coarse_inverse_exact
#check D0.Research.NativeSceneHistoryFeedback.native_constant_transport_left
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_transport_left
#check D0.Research.NativeSceneHistoryFeedback.native_constant_transport_right
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_transport_right
#check D0.Research.NativeSceneHistoryFeedback.native_constant_idempotent
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_idempotent
#check D0.Research.NativeSceneHistoryFeedback.native_constant_h_fixed
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_h_fixed
#check D0.Research.NativeSceneHistoryFeedback.native_constant_hi_fixed
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_hi_fixed
#check D0.Research.NativeSceneHistoryFeedback.native_normalized_constant_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_normalized_constant_zero
#check D0.Research.NativeSceneHistoryFeedback.native_incoming_from_both_readouts
#print axioms D0.Research.NativeSceneHistoryFeedback.native_incoming_from_both_readouts
#check D0.Research.NativeSceneHistoryFeedback.native_endpoint_average_incoming_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_endpoint_average_incoming_zero
#check D0.Research.NativeSceneHistoryFeedback.native_outgoing_endpoint_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_outgoing_endpoint_zero
#check D0.Research.NativeSceneHistoryFeedback.native_outgoing_incoming_h
#print axioms D0.Research.NativeSceneHistoryFeedback.native_outgoing_incoming_h
#check D0.Research.NativeSceneHistoryFeedback.native_two_constant_readouts
#print axioms D0.Research.NativeSceneHistoryFeedback.native_two_constant_readouts
#check D0.Research.NativeSceneHistoryFeedback.native_incoming_constant_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_incoming_constant_zero
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_endpoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_endpoint
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_incoming
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_idempotent
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_idempotent
#check D0.Research.NativeSceneHistoryFeedback.native_generated_endpoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_generated_endpoint
#check D0.Research.NativeSceneHistoryFeedback.native_generated_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.native_generated_incoming
#check D0.Research.NativeSceneHistoryFeedback.native_transport_normalized_commute
#print axioms D0.Research.NativeSceneHistoryFeedback.native_transport_normalized_commute
#check D0.Research.NativeSceneHistoryFeedback.native_both_readouts_determine_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.native_both_readouts_determine_incoming
#check D0.Research.NativeSceneHistoryFeedback.native_generated_source
#print axioms D0.Research.NativeSceneHistoryFeedback.native_generated_source
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_source
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_source
#check D0.Research.NativeSceneHistoryFeedback.native_all_joint_readouts_determine_generated_heat
#print axioms D0.Research.NativeSceneHistoryFeedback.native_all_joint_readouts_determine_generated_heat
#check D0.Research.NativeSceneHistoryFeedback.native_degree_inverse_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_degree_inverse_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_adjacency_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_adjacency_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_transport_weighted_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_transport_weighted_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_constant_weighted_entry
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_weighted_entry
#check D0.Research.NativeSceneHistoryFeedback.native_constant_weighted_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_weighted_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_coarse_h_weighted_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_coarse_h_weighted_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_coarse_hi_weighted_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_coarse_hi_weighted_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_normalized_weighted_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_normalized_weighted_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_h_normalized_commute
#print axioms D0.Research.NativeSceneHistoryFeedback.native_h_normalized_commute
#check D0.Research.NativeSceneHistoryFeedback.native_hi_normalized_commute
#print axioms D0.Research.NativeSceneHistoryFeedback.native_hi_normalized_commute
#check D0.Research.NativeSceneHistoryFeedback.native_history_average_weighted_adjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_history_average_weighted_adjoint
#check D0.Research.NativeSceneHistoryFeedback.native_history_complement_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_history_complement_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_outgoing_weighted_adjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_outgoing_weighted_adjoint
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_generated_heat_selfadjoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_generated_heat_selfadjoint
#check D0.Research.NativeSceneHistoryFeedback.native_generated_heat_supported
#print axioms D0.Research.NativeSceneHistoryFeedback.native_generated_heat_supported
#check D0.Research.NativeSceneHistoryFeedback.native_complete_symmetric_joint_history_extensions
#print axioms D0.Research.NativeSceneHistoryFeedback.native_complete_symmetric_joint_history_extensions
#check D0.Research.NativeSceneHistoryFeedback.native_complete_joint_parameter_unique
#print axioms D0.Research.NativeSceneHistoryFeedback.native_complete_joint_parameter_unique
#check D0.Research.NativeSceneHistoryFeedback.native_full_complement_supported
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_complement_supported
#check D0.Research.NativeSceneHistoryFeedback.native_scalar_complement_keeps_both_readouts
#print axioms D0.Research.NativeSceneHistoryFeedback.native_scalar_complement_keeps_both_readouts
#check D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_endpoint_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_endpoint_zero
#check D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_reversed_endpoint_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_reversed_endpoint_zero
#check D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_outgoing_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_outgoing_zero
#check D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_projected_zero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_projected_zero
#check D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_archive_rectangle_nonzero
#check D0.Research.NativeSceneHistoryFeedback.native_full_complement_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_complement_nonzero
#check D0.Research.NativeSceneHistoryFeedback.native_zone_constant_trace
#print axioms D0.Research.NativeSceneHistoryFeedback.native_zone_constant_trace
#check D0.Research.NativeSceneHistoryFeedback.native_constant_trace
#print axioms D0.Research.NativeSceneHistoryFeedback.native_constant_trace
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_trace
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_trace
#check D0.Research.NativeSceneHistoryFeedback.native_history_cardinality_in_kernel
#print axioms D0.Research.NativeSceneHistoryFeedback.native_history_cardinality_in_kernel
#check D0.Research.NativeSceneHistoryFeedback.native_full_complement_trace
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_complement_trace
#check D0.Research.NativeSceneHistoryFeedback.native_reverse_reads_endpoint
#print axioms D0.Research.NativeSceneHistoryFeedback.native_reverse_reads_endpoint
#check D0.Research.NativeSceneHistoryFeedback.native_reverse_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.native_reverse_incoming
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_preserves_reversed_incoming
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_preserves_reversed_incoming
#check D0.Research.NativeSceneHistoryFeedback.native_full_projector_reverse_commute
#print axioms D0.Research.NativeSceneHistoryFeedback.native_full_projector_reverse_commute
#check D0.Research.NativeSceneHistoryFeedback.native_generated_reverse_joint_readouts
#print axioms D0.Research.NativeSceneHistoryFeedback.native_generated_reverse_joint_readouts
#check D0.Research.NativeSceneHistoryFeedback.native_generated_reverse_commute
#print axioms D0.Research.NativeSceneHistoryFeedback.native_generated_reverse_commute
#check D0.Research.NativeSceneHistoryFeedback.native_scalar_complement_reverse_commute
#print axioms D0.Research.NativeSceneHistoryFeedback.native_scalar_complement_reverse_commute
#check D0.Research.NativeSceneHistoryFeedback.native_scalar_complement_parameter_distinct
#print axioms D0.Research.NativeSceneHistoryFeedback.native_scalar_complement_parameter_distinct
#check D0.Research.NativeSceneHistoryFeedback.scalar_completed_heat_positive
#print axioms D0.Research.NativeSceneHistoryFeedback.scalar_completed_heat_positive
#check D0.Research.NativeSceneHistoryFeedback.scalar_completed_heat_genuine_derivative
#print axioms D0.Research.NativeSceneHistoryFeedback.scalar_completed_heat_genuine_derivative
#check D0.Research.NativeSceneHistoryFeedback.scalar_completed_action_genuine_derivative
#print axioms D0.Research.NativeSceneHistoryFeedback.scalar_completed_action_genuine_derivative
#check D0.Research.NativeSceneHistoryFeedback.scalar_completed_action_derivative_nonzero
#print axioms D0.Research.NativeSceneHistoryFeedback.scalar_completed_action_derivative_nonzero
#check D0.Research.NativeSceneHistoryFeedback.full_and_scene_heat_source_agree_iff
#print axioms D0.Research.NativeSceneHistoryFeedback.full_and_scene_heat_source_agree_iff
