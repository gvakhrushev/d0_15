import D0.VNext2.ScenePathHistoryCanonicity
import Mathlib.Tactic

/-! Exact boundary accounting for Book 03's edge-cost / vertex-information
formula on the actual D0 scene path carrier. This is a research certificate;
it does not install a physical Cost/Info readout or field map. -/

namespace D0.Research.NativeCostInfoBoundary

open D0.Claims D0.VNext2.ScenePathHistoryCanonicity
open D0.SelfReading.TypedIncidenceCarriers
noncomputable section

abbrev Vertex := Fin 33
abbrev Edge := LevelOneSceneHistory

def pathSum (w : Vertex → Vertex → ℝ) : List Vertex → ℝ
  | u :: v :: rest => w u v + pathSum w (v :: rest)
  | _ => 0

def edgeReading (w : Edge → ℝ) (u v : Vertex) : ℝ :=
  if h : SceneStep u v then w ⟨(u, v), h⟩ else 0

theorem rest_composable {u v : Vertex} {w q : List Vertex}
    (h : Composable (u :: v :: w) q) : Composable (v :: w) q := by
  rcases h with ⟨x, hx, hy⟩
  refine ⟨x, ?_, hy⟩
  simpa [pathFinish] using hx

theorem path_sum_composition (w : Vertex → Vertex → ℝ)
    {p q : List Vertex} (hp : IsSceneWalk p) (h : Composable p q) :
    pathSum w (composePath p q) = pathSum w p + pathSum w q := by
  induction hp with
  | single v =>
    rcases h with ⟨x, hx, hy⟩
    have hxv : v = x := by simpa [pathFinish] using hx
    subst x
    cases q with
    | nil => simp [pathStart] at hy
    | cons a rest =>
      have ha : a = v := by simpa [pathStart] using hy
      subst a
      simp [composePath, pathSum]
  | cons u v rest hs hr ih =>
    have hi := ih (rest_composable h)
    change w u v + pathSum w ((v :: rest) ++ q.tail) =
      (w u v + pathSum w (v :: rest)) + pathSum w q
    rw [show pathSum w ((v :: rest) ++ q.tail) =
      pathSum w (v :: rest) + pathSum w q from hi]
    ring

def allocatedWeight (cost : Edge → ℝ) (info : Vertex → ℝ)
    (theta : ℝ) (e : Edge) : ℝ :=
  cost e - theta * info e.val.1 - (1 - theta) * info e.val.2

def allocatedAction (cost : Edge → ℝ) (info : Vertex → ℝ)
    (theta : ℝ) (p : List Vertex) : ℝ :=
  pathSum (edgeReading (allocatedWeight cost info theta)) p

theorem allocatedAction_additive (cost : Edge → ℝ) (info : Vertex → ℝ)
    (theta : ℝ) {p q : List Vertex} (hp : IsSceneWalk p)
    (h : Composable p q) :
    allocatedAction cost info theta (composePath p q) =
      allocatedAction cost info theta p + allocatedAction cost info theta q :=
  path_sum_composition _ hp h

def vertexInfoSum (info : Vertex → ℝ) (p : List Vertex) : ℝ :=
  (p.map info).sum

def literalPathAction (cost : Edge → ℝ) (info : Vertex → ℝ)
    (p : List Vertex) : ℝ :=
  pathSum (edgeReading cost) p - vertexInfoSum info p

theorem literal_singleton_value (cost : Edge → ℝ) (info : Vertex → ℝ)
    (v : Vertex) : literalPathAction cost info [v] = -info v := by
  simp [literalPathAction, vertexInfoSum, pathSum]

theorem literal_two_step_defect (cost : Edge → ℝ) (info : Vertex → ℝ)
    (u v w : Vertex) (huv : SceneStep u v) (hvw : SceneStep v w) :
    literalPathAction cost info [u, v, w] =
      literalPathAction cost info [u, v] +
        literalPathAction cost info [v, w] + info v := by
  simp [literalPathAction, vertexInfoSum, pathSum, edgeReading, huv, hvw]
  ring

theorem literal_additivity_forces_info_at_join (cost : Edge → ℝ)
    (info : Vertex → ℝ) (u v w : Vertex)
    (huv : SceneStep u v) (hvw : SceneStep v w)
    (hadd : literalPathAction cost info [u, v, w] =
      literalPathAction cost info [u, v] + literalPathAction cost info [v, w]) :
    info v = 0 := by
  have hdef := literal_two_step_defect cost info u v w huv hvw
  rw [hadd] at hdef
  linarith

theorem sceneStep_has_neighbor (v : Vertex) : ∃ u, SceneStep v u := by
  by_cases hz : zone31 v = 0
  · refine ⟨9, ?_⟩
    change (if zone31 v = zone31 (9 : Fin 33) then (0 : ℚ) else 1) = 1
    have h9 : zone31 (9 : Fin 33) = 1 := by norm_num [zone31]
    simp [hz, h9]
  · refine ⟨0, ?_⟩
    change (if zone31 v = zone31 (0 : Fin 33) then (0 : ℚ) else 1) = 1
    have h0 : zone31 (0 : Fin 33) = 0 := by norm_num [zone31]
    simp [hz, h0]

theorem every_scene_vertex_has_a_join (v : Vertex) :
    ∃ u w, SceneStep u v ∧ SceneStep v w := by
  obtain ⟨w, hw⟩ := sceneStep_has_neighbor v
  exact ⟨w, w, sceneStep_symm hw, hw⟩

theorem literal_additivity_forces_all_info_zero (cost : Edge → ℝ)
    (info : Vertex → ℝ)
    (hadd : ∀ u v w, SceneStep u v → SceneStep v w →
      literalPathAction cost info [u, v, w] =
        literalPathAction cost info [u, v] + literalPathAction cost info [v, w]) :
    ∀ v, info v = 0 := by
  intro v
  obtain ⟨u, w, huv, hvw⟩ := every_scene_vertex_has_a_join v
  exact literal_additivity_forces_info_at_join cost info u v w huv hvw
    (hadd u v w huv hvw)

def coboundary (b : Vertex → ℝ) (u v : Vertex) : ℝ := b v - b u

theorem allocated_weight_difference (cost : Edge → ℝ) (info : Vertex → ℝ)
    (theta eta : ℝ) (e : Edge) :
    allocatedWeight cost info theta e - allocatedWeight cost info eta e =
      coboundary (fun v => (theta - eta) * info v) e.val.1 e.val.2 := by
  simp [allocatedWeight, coboundary]
  ring

theorem edge_reading_sub (a b : Edge → ℝ) (u v : Vertex) :
    edgeReading (fun e => a e - b e) u v =
      edgeReading a u v - edgeReading b u v := by
  by_cases h : SceneStep u v <;> simp [edgeReading, h]

theorem path_sum_sub (a b : Vertex → Vertex → ℝ) (p : List Vertex) :
    pathSum (fun u v => a u v - b u v) p = pathSum a p - pathSum b p := by
  induction p with
  | nil => simp [pathSum]
  | cons u rest ih =>
    cases rest with
    | nil => simp [pathSum]
    | cons v tail =>
      simp only [pathSum] at ih ⊢
      rw [ih]
      ring

theorem allocated_difference_reading (cost : Edge → ℝ) (info : Vertex → ℝ)
    (theta eta : ℝ) (u v : Vertex) :
    edgeReading (fun e => allocatedWeight cost info theta e -
        allocatedWeight cost info eta e) u v =
      edgeReading (fun e => coboundary (fun x => (theta - eta) * info x)
        e.val.1 e.val.2) u v := by
  by_cases h : SceneStep u v
  · simp only [edgeReading, dif_pos h]
    simpa [coboundary] using
      (allocated_weight_difference cost info theta eta ⟨(u, v), h⟩)
  · simp [edgeReading, h]

theorem edge_coboundary_path_sum (b : Vertex → ℝ) {p : List Vertex}
    (hp : IsSceneWalk p) :
    pathSum (edgeReading (fun e => coboundary b e.val.1 e.val.2)) p =
      pathSum (coboundary b) p := by
  induction hp with
  | single v => rfl
  | cons u v rest hs hr ih =>
    simp [pathSum, edgeReading, hs, ih]

theorem coboundary_telescopes (b : Vertex → ℝ) (u : Vertex)
    (rest : List Vertex) :
    pathSum (coboundary b) (u :: rest) =
      b ((u :: rest).getLast (by simp)) - b u := by
  induction rest generalizing u with
  | nil => simp [pathSum]
  | cons v tail ih =>
    simp only [pathSum, coboundary]
    rw [ih]
    simp only [List.getLast_cons_cons]
    ring

theorem allocated_action_parameter_difference (cost : Edge → ℝ)
    (info : Vertex → ℝ) (theta eta : ℝ) (u : Vertex)
    (rest : List Vertex) (hp : IsSceneWalk (u :: rest)) :
    allocatedAction cost info theta (u :: rest) -
      allocatedAction cost info eta (u :: rest) =
        coboundary (fun v => (theta - eta) * info v) u
          ((u :: rest).getLast (by simp)) := by
  have hread : edgeReading
      (fun e => allocatedWeight cost info theta e - allocatedWeight cost info eta e) =
        edgeReading (fun e => coboundary (fun v => (theta - eta) * info v)
          e.val.1 e.val.2) := by
    funext a b
    exact allocated_difference_reading cost info theta eta a b
  calc
    _ = pathSum (fun a b =>
        edgeReading (allocatedWeight cost info theta) a b -
          edgeReading (allocatedWeight cost info eta) a b) (u :: rest) := by
      exact (path_sum_sub _ _ _).symm
    _ = pathSum (edgeReading (fun e =>
        allocatedWeight cost info theta e - allocatedWeight cost info eta e))
          (u :: rest) := by
      congr 1
      funext a b
      exact (edge_reading_sub _ _ _ _).symm
    _ = pathSum (edgeReading (fun e => coboundary
        (fun v => (theta - eta) * info v) e.val.1 e.val.2)) (u :: rest) := by
      rw [hread]
    _ = pathSum (coboundary (fun v => (theta - eta) * info v))
          (u :: rest) := edge_coboundary_path_sum _ hp
    _ = coboundary (fun v => (theta - eta) * info v) u
          ((u :: rest).getLast (by simp)) := by
      simpa [coboundary] using
        (coboundary_telescopes (fun v => (theta - eta) * info v) u rest)

#check literal_two_step_defect
#check literal_additivity_forces_all_info_zero
#check allocatedAction_additive
#check allocated_action_parameter_difference
#print axioms literal_two_step_defect
#print axioms literal_additivity_forces_all_info_zero
#print axioms allocatedAction_additive
#print axioms allocated_action_parameter_difference

end
end D0.Research.NativeCostInfoBoundary
