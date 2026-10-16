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
