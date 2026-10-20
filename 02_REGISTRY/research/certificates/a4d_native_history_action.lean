import D0.VNext2.ScenePathHistoryCanonicity
import D0.VNext2.ScenePerronTraceCanonicity
import D0.VNext2.SceneHistoryPerronTrace
import D0.Foundation.EndogenousActionQuantum
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-! Complete additive scalar valuations on the literal scene path carrier.
Additivity and logarithmic reading are explicit comparison hypotheses, not
new native field laws. No coframe/link/matter map is supplied by this capsule. -/
namespace D0.Research.NativeHistoryAction
open D0.Claims D0.VNext2.ScenePathHistoryCanonicity
open D0.VNext2.ScenePerronTraceCanonicity
open D0.Foundation.VerifiabilityNecessity D0.Foundation.EndogenousActionQuantum
noncomputable section

abbrev Path := {p : List Vertex33 // IsSceneWalk p}
abbrev Edge := LevelOneSceneHistory

def edgePath (e : Edge) : Path :=
  ⟨[e.val.1,e.val.2],IsSceneWalk.cons _ _ [] e.property (IsSceneWalk.single _)⟩

def singlePath (v : Vertex33) : Path := ⟨[v],IsSceneWalk.single v⟩

def comp (p q : Path) (h : Composable p.val q.val) : Path :=
  ⟨composePath p.val q.val,isSceneWalk_compose p.property q.property h⟩

structure AdditiveAction where
  value : Path → ℝ
  identity : ∀ v, value (singlePath v)=0
  additive : ∀ p q h, value (comp p q h)=value p+value q

def pathSum (w : Vertex33 → Vertex33 → ℝ) : List Vertex33 → ℝ
  | u::v::rest => w u v + pathSum w (v::rest)
  | _ => 0

def edgeReading (w : Edge → ℝ) (u v : Vertex33) : ℝ :=
  if h : SceneStep u v then w ⟨(u,v),h⟩ else 0

theorem rest_composable {u v : Vertex33} {w q : List Vertex33}
    (h : Composable (u::v::w) q) : Composable (v::w) q := by
  rcases h with ⟨x,hx,hy⟩
  refine ⟨x,?_,hy⟩
  simpa [pathFinish] using hx

theorem path_sum_composition (w : Vertex33 → Vertex33 → ℝ)
    {p q : List Vertex33} (hp : IsSceneWalk p) (h : Composable p q) :
    pathSum w (composePath p q)=pathSum w p+pathSum w q := by
  induction hp with
  | single v =>
    rcases h with ⟨x,hx,hy⟩
    have hxv : v=x := by simpa [pathFinish] using hx
    subst x
    cases q with
    | nil => simp [pathStart] at hy
    | cons a rest =>
      have ha : a=v := by simpa [pathStart] using hy
      subst a
      simp [composePath,pathSum]
  | cons u v rest hs hr ih =>
    have hi := ih (rest_composable h)
    change w u v + pathSum w ((v::rest)++q.tail) =
      (w u v + pathSum w (v::rest))+pathSum w q
    rw [show pathSum w ((v::rest)++q.tail)=pathSum w (v::rest)+pathSum w q from hi]
    ring

def fromEdges (w : Edge → ℝ) : AdditiveAction where
  value p := pathSum (edgeReading w) p.val
  identity _ := rfl
  additive p _q h := path_sum_composition _ p.property h

def toEdges (S : AdditiveAction) (e : Edge) : ℝ := S.value (edgePath e)

theorem edges_of_extension (w : Edge → ℝ) : toEdges (fromEdges w)=w := by
  funext e
  simp [toEdges,fromEdges,edgePath,pathSum,edgeReading,e.property]

theorem additive_value_forced (S : AdditiveAction) (p : Path) :
    S.value p=pathSum (edgeReading (toEdges S)) p.val := by
  rcases p with ⟨p,hp⟩
  induction hp with
  | single v => exact S.identity v
  | cons u v rest hs hr ih =>
    have hc : Composable [u,v] (v::rest) := ⟨v,rfl,rfl⟩
    have ha := S.additive (edgePath ⟨(u,v),hs⟩) ⟨v::rest,hr⟩ hc
    change S.value ⟨u::v::rest, _⟩ = _ at ha
    rw [ha,ih]
    simp [pathSum,edgeReading,hs,toEdges]

theorem additive_ext (S T : AdditiveAction) (h : S.value=T.value) : S=T := by
  cases S
  cases T
  cases h
  rfl

theorem extension_of_edges (S : AdditiveAction) : fromEdges (toEdges S)=S := by
  apply additive_ext
  funext p
  exact (additive_value_forced S p).symm

/-- Completeness is over every scalar valuation satisfying the displayed
identity and concatenation law, on every valid native scene walk. -/
def completeAdditiveFiber : AdditiveAction ≃ (Edge → ℝ) where
  toFun := toEdges
  invFun := fromEdges
  left_inv := extension_of_edges
  right_inv := edges_of_extension

theorem native_history_family_domain (F : SceneHistoryFamily) (p : List Vertex33) :
    F.mem p ↔ IsSceneWalk p := composition_complete_eq_all_walks F p

theorem scene_edge_distinct (e : Edge) : e.val.1≠e.val.2 := by
  intro h
  have he := e.property
  simp [SceneStep,Adj31,h] at he

abbrev sceneProtocol : VerificationProtocol where
  State := Vertex33
  Record := Vertex33
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ u v => decide (u≠v)

theorem scene_protocol_verified : VerificationContract sceneProtocol where
  state_nontrivial := inferInstance
  line_nontrivial := inferInstance
  catalogue_nonempty := inferInstance
  correct := by intro _ _ _ _; rfl

def protocolFromEdges (w : Edge → ℝ) (hw : ∀ e,1≤w e) : ActionProtocol sceneProtocol where
  action u v := if u=v then 0 else if h : SceneStep u v then w ⟨(u,v),h⟩ else 1
  action_refl := by intro u; simp
  action_nontrivial := by
    intro u v h
    simp only [if_neg h]
    split_ifs with hs
    · exact hw ⟨(u,v),hs⟩
    · exact le_rfl

theorem protocol_edges_exact (w : Edge → ℝ) (hw : ∀ e,1≤w e) (e : Edge) :
    (protocolFromEdges w hw).action e.val.1 e.val.2=w e := by
  simp [protocolFromEdges,scene_edge_distinct e,e.property]

theorem full_positive_edge_fiber (w : Edge → ℝ) :
    (∃ A : ActionProtocol sceneProtocol, ∀ e,A.action e.val.1 e.val.2=w e) ↔
      ∀ e,1≤w e := by
  constructor
  · rintro ⟨A,h⟩ e
    rw [← h e]
    exact A.action_nontrivial _ _ (scene_edge_distinct e)
  · intro h
    exact ⟨protocolFromEdges w h,protocol_edges_exact w h⟩

theorem canonical_scene_edge_cost (e : Edge) :
    (canonicalActionProtocol sceneProtocol).action e.val.1 e.val.2=1 := by
  simp [canonicalActionProtocol,scene_edge_distinct e]

theorem primitive_cost_cannot_forget_return {P : VerificationProtocol}
    (A : ActionProtocol P) (u v : P.State) (h : u≠v) :
    A.action u v+A.action v u≠A.action u u := by
  rw [A.action_refl]
  have h1 := A.action_nontrivial u v h
  have h2 := A.action_nontrivial v u h.symm
  linarith

theorem unit_path_sum (p : List Vertex33) :
    pathSum (fun _ _ => 1) p=((p.length-1 : ℕ) : ℝ) := by
  induction p with
  | nil => simp [pathSum]
  | cons u rest ih =>
    cases rest with
    | nil => simp [pathSum]
    | cons v tail =>
      simp only [pathSum] at ih ⊢
      change 1+pathSum (fun _ _ => 1) (v::tail)=_
      rw [show pathSum (fun _ _ => 1) (v::tail)=((List.length (v::tail)-1 : ℕ):ℝ) from ih]
      simp
      ring

theorem unit_edge_action_eq_length (p : Path) :
    (fromEdges (fun _ => 1)).value p=((p.val.length-1 : ℕ):ℝ) := by
  have he : pathSum (edgeReading (fun _ => 1)) p.val=pathSum (fun _ _ => 1) p.val := by
    rcases p with ⟨p,hp⟩
    induction hp with
    | single v => rfl
    | cons u v tail hs hr ih => simp [pathSum,edgeReading,hs,ih]
  exact he.trans (unit_path_sum p.val)

def coboundary (b : Vertex33 → ℝ) (u v : Vertex33) : ℝ := b v-b u

theorem coboundary_telescopes (b : Vertex33 → ℝ) (u : Vertex33) (rest : List Vertex33) :
    pathSum (coboundary b) (u::rest)=b ((u::rest).getLast (by simp))-b u := by
  induction rest generalizing u with
  | nil => simp [pathSum]
  | cons v tail ih =>
    simp only [pathSum,coboundary]
    rw [ih]
    simp only [List.getLast_cons_cons]
    ring

def conditionalEdge (u v : Vertex33) : ℝ :=
  fullScenePerronVector v/(sceneRho*fullScenePerronVector u)

def logEdge (u v : Vertex33) : ℝ := -Real.log (conditionalEdge u v)

theorem conditional_edge_pos (u v : Vertex33) : 0<conditionalEdge u v := by
  exact div_pos (fullScenePerronVector_pos v)
    (mul_pos sceneRho_pos (fullScenePerronVector_pos u))

theorem perron_log_edge_is_length_plus_boundary (u v : Vertex33) :
    logEdge u v=Real.log sceneRho+Real.log (fullScenePerronVector u)-Real.log (fullScenePerronVector v) := by
  unfold logEdge conditionalEdge
  rw [Real.log_div (ne_of_gt (fullScenePerronVector_pos v))
      (ne_of_gt (mul_pos sceneRho_pos (fullScenePerronVector_pos u))),
    Real.log_mul (ne_of_gt sceneRho_pos) (ne_of_gt (fullScenePerronVector_pos u))]
  ring

theorem path_sum_add (a b : Vertex33 → Vertex33 → ℝ) (p : List Vertex33) :
    pathSum (fun u v => a u v+b u v) p=pathSum a p+pathSum b p := by
  induction p with
  | nil => simp [pathSum]
  | cons u tail ih =>
    cases tail with
    | nil => simp [pathSum]
    | cons v rest => simp only [pathSum] at ih ⊢; rw [ih]; ring

theorem constant_path_sum (c : ℝ) (p : List Vertex33) :
    pathSum (fun _ _ => c) p=((p.length-1 : ℕ):ℝ)*c := by
  induction p with
  | nil => simp [pathSum]
  | cons u tail ih =>
    cases tail with
    | nil => simp [pathSum]
    | cons v rest =>
      change c+pathSum (fun _ _ => c) (v::rest)=_
      rw [ih]
      simp
      ring

theorem perron_path_log_telescopes (u : Vertex33) (rest : List Vertex33) :
    pathSum logEdge (u::rest)=(rest.length:ℝ)*Real.log sceneRho+
      Real.log (fullScenePerronVector u)-
      Real.log (fullScenePerronVector ((u::rest).getLast (by simp))) := by
  have hf : logEdge=fun u v => Real.log sceneRho+
      coboundary (fun z => -Real.log (fullScenePerronVector z)) u v := by
    funext u v
    rw [perron_log_edge_is_length_plus_boundary]
    simp [coboundary]
    ring
  rw [hf,path_sum_add,constant_path_sum,coboundary_telescopes]
  simp
  ring

theorem equal_length_endpoints_have_equal_log (u : Vertex33)
    (p q : List Vertex33) (hn : p.length=q.length)
    (ht : (u::p).getLast (by simp)=(u::q).getLast (by simp)) :
    pathSum logEdge (u::p)=pathSum logEdge (u::q) := by
  rw [perron_path_log_telescopes,perron_path_log_telescopes,hn,ht]

theorem positive_symmetric_coboundary_zero (b : Vertex33 → ℝ) (u v : Vertex33)
    (hu : 0≤coboundary b u v) (hv : 0≤coboundary b v u) :
    coboundary b u v=0 := by
  unfold coboundary at *
  linarith

theorem perron_root_bounds : 20<sceneRho ∧ sceneRho<24 := by
  have h20 : 20<sceneRho := by
    by_contra h
    have hn := scene_cubic_no_positive_root_le_20 sceneRho sceneRho_pos (le_of_not_gt h)
    rw [sceneRho_cubic] at hn
    exact (lt_irrefl 0) hn
  refine ⟨h20,?_⟩
  by_contra h
  have h24 : 0<sceneTransportCubic 24 := by norm_num [sceneTransportCubic]
  rcases eq_or_lt_of_le (le_of_not_gt h) with he|hl
  · rw [he,sceneRho_cubic] at h24
    exact (lt_irrefl 0) h24
  · have hm := scene_cubic_strictMono_ge_20 (by norm_num : (20:ℝ)≤24) hl
    rw [sceneRho_cubic] at hm
    linarith

theorem perron_uniform_two_step_lower_arithmetic (rho : ℝ)
    (h20 : 20<rho) (h24 : rho<24) :
    (1:ℝ)/100 < 9*(rho+9)/(rho^2*(rho+13)) := by
  have hd : 0<rho^2*(rho+13) := mul_pos (sq_pos_of_pos (by linarith)) (by linarith)
  have hs : rho^2<576 := by nlinarith
  have ht : rho^2*(rho+13)<576*37 := by
    have := mul_lt_mul_of_pos_right hs (show 0<rho+13 by linarith)
    nlinarith
  apply (lt_div_iff₀ hd).mpr
  nlinarith

theorem normalized_constant_reading {I : Type*} [Fintype I]
    (weights : I → ℝ) (h : ∑ i, weights i=1) (c : ℝ) :
    (∑ i, weights i*c)=c := by rw [← Finset.sum_mul,h,one_mul]

end
end D0.Research.NativeHistoryAction

#check D0.Research.NativeHistoryAction.completeAdditiveFiber
#check D0.VNext2.SceneHistoryPerronTrace.scene_history_perron_trace_owner

#print axioms D0.Research.NativeHistoryAction.edges_of_extension
#print axioms D0.Research.NativeHistoryAction.additive_value_forced
#print axioms D0.Research.NativeHistoryAction.extension_of_edges
#print axioms D0.Research.NativeHistoryAction.completeAdditiveFiber
#print axioms D0.Research.NativeHistoryAction.native_history_family_domain
#print axioms D0.Research.NativeHistoryAction.scene_protocol_verified
#print axioms D0.Research.NativeHistoryAction.protocol_edges_exact
#print axioms D0.Research.NativeHistoryAction.full_positive_edge_fiber
#print axioms D0.Research.NativeHistoryAction.primitive_cost_cannot_forget_return
#print axioms D0.Research.NativeHistoryAction.unit_edge_action_eq_length
#print axioms D0.Research.NativeHistoryAction.coboundary_telescopes
#print axioms D0.Research.NativeHistoryAction.conditional_edge_pos
#print axioms D0.Research.NativeHistoryAction.perron_log_edge_is_length_plus_boundary
#print axioms D0.Research.NativeHistoryAction.perron_path_log_telescopes
#print axioms D0.Research.NativeHistoryAction.equal_length_endpoints_have_equal_log
#print axioms D0.Research.NativeHistoryAction.positive_symmetric_coboundary_zero

#print axioms D0.Research.NativeHistoryAction.canonical_scene_edge_cost
#print axioms D0.Research.NativeHistoryAction.perron_root_bounds
#print axioms D0.Research.NativeHistoryAction.perron_uniform_two_step_lower_arithmetic
#print axioms D0.Research.NativeHistoryAction.normalized_constant_reading
