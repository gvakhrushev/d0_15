import Mathlib.Tactic
import D0.Claims.Signature31Split
import D0.SelfReading.TypedIncidenceCarriers
import D0.VNext2.SceneNativeRefinementClassification

/-!
# D0.VNext2.ScenePathHistoryCanonicity

Theoretical owners:
- `D0-SCENE-PATH-COMPOSITION-CANONICITY-001`
- `D0-NONBACKTRACKING-NOT-SCENE-HISTORY-COMPLETION-001`
- `D0-IMMEDIATE-RETURN-ORIENTED-EDGE-EQUIV-001`
- `D0-DIRECTED-EDGE-AS-LEVEL1-HISTORY-001`

Root reinterpretation of the Lane A history refinement problem:
1. `runtime` in D0 is defined as ordered finite evolution, i.e., composition of finite
   tick maps, where `tick` is an evolution endomorphism.
2. A faithful history refinement of the base scene dynamics must record compositions of
   permitted 1-step scene transitions.
3. Every family of histories that contains the elementary scene transitions, contains only
   valid scene walks, and is closed under concatenation of composable paths is IDENTICALLY
   the free path category (all-walks).
4. Non-backtracking (NB) is NOT closed under composition of paths on vertex objects:
   for adjacent vertices `0` and `9`, `[0, 9]` and `[9, 0]` are NB, but their composition
   `[0, 9, 0]` is not NB. Thus NB is not a composition-closed history completion of the
   vertex-object scene tick.
5. The 718 difference `15708 - 14990 = 718` at depth 2 is in canonical 1-to-1 bijection
   with the 718 oriented edges: `(u, v) ↔ (u, v, u)` (immediate direct-return walks).
6. The dimension `718` is not a rival state dimension to `33`; it is the cardinality of
   the level-1 generating arrow carrier `LevelOneSceneHistory ≃ DirectedEdgeSupport`.
-/

namespace D0.VNext2.ScenePathHistoryCanonicity

open D0.Claims
open D0.SelfReading.TypedIncidenceCarriers
open D0.VNext2.SceneNativeRefinementClassification

abbrev Vertex33 := Fin 33

/-- Step relation in the scene graph: adjacency in `Adj31`. -/
def SceneStep (u v : Vertex33) : Prop :=
  Adj31 u v = 1

instance (u v : Vertex33) : Decidable (SceneStep u v) :=
  inferInstanceAs (Decidable (Adj31 u v = 1))

/-- Inductive predicate defining valid walks in the scene graph. -/
inductive IsSceneWalk : List Vertex33 → Prop where
  | single (v : Vertex33) : IsSceneWalk [v]
  | cons (u v : Vertex33) (w : List Vertex33)
      (hstep : SceneStep u v) (hrest : IsSceneWalk (v :: w)) :
      IsSceneWalk (u :: v :: w)

/-- A walk has a well-defined start (head). -/
def pathStart (p : List Vertex33) : Option Vertex33 :=
  p.head?

/-- A walk has a well-defined finish (last vertex). -/
def pathFinish (p : List Vertex33) : Option Vertex33 :=
  p.getLast?

/-- Two non-empty path sequences are composable if the finish of the first
coincides with the start of the second. -/
def Composable (p q : List Vertex33) : Prop :=
  ∃ v : Vertex33, pathFinish p = some v ∧ pathStart q = some v

/-- Composition of two composable paths by concatenating and dropping the duplicate junction vertex. -/
def composePath (p q : List Vertex33) : List Vertex33 :=
  p ++ q.tail

/-- An admissible complete scene history family on vertex objects:
contains all singletons, all 1-step edges, only valid scene walks, and is
closed under composition of composable paths. -/
structure SceneHistoryFamily where
  mem : List Vertex33 → Prop
  sceneOnly : ∀ p, mem p → IsSceneWalk p
  identities : ∀ v, mem [v]
  containsEdges : ∀ u v, SceneStep u v → mem [u, v]
  compClosed : ∀ p q, mem p → mem q → Composable p q → mem (composePath p q)

/-- Step is symmetric for undirected graph K(9,11,13). -/
theorem sceneStep_symm {u v : Vertex33} (h : SceneStep u v) : SceneStep v u := by
  unfold SceneStep Adj31 at h ⊢
  simp only [Matrix.of_apply] at h ⊢
  by_cases hzone : zone31 u = zone31 v
  · simp [hzone] at h
  · have hzone' : ¬ zone31 v = zone31 u := fun heq => hzone heq.symm
    simp [hzone']

/-- Walk concatenation preserves `IsSceneWalk`. -/
theorem isSceneWalk_compose {p q : List Vertex33}
    (hp : IsSceneWalk p) (hq : IsSceneWalk q) (hcomp : Composable p q) :
    IsSceneWalk (composePath p q) := by
  induction hp with
  | single v =>
    rcases hcomp with ⟨v', hlast, hhead⟩
    unfold pathFinish at hlast
    simp at hlast
    subst v'
    unfold composePath
    simp
    unfold pathStart at hhead
    cases q with
    | nil => contradiction
    | cons w rest =>
      simp at hhead
      subst w
      exact hq
  | cons u v w hstep hrest ih =>
    unfold composePath
    dsimp
    have hcomp' : Composable (v :: w) q := by
      rcases hcomp with ⟨x, hlast, hhead⟩
      use x
      refine ⟨?_, hhead⟩
      unfold pathFinish at hlast ⊢
      cases w with
      | nil =>
        simp at hlast ⊢
        exact hlast
      | cons y ys =>
        simp at hlast ⊢
        exact hlast
    have := ih hcomp'
    unfold composePath at this
    cases w with
    | nil =>
      dsimp at this ⊢
      exact IsSceneWalk.cons u v (q.tail) hstep this
    | cons y ys =>
      dsimp at this ⊢
      exact IsSceneWalk.cons u v (y :: ys ++ q.tail) hstep this

/-- **Theorem A: Universal property of the free path category.**
Any complete, scene-faithful, composition-closed history family on vertex objects
coincides identically with the all-walks path category `IsSceneWalk`. -/
theorem composition_complete_eq_all_walks (F : SceneHistoryFamily) (p : List Vertex33) :
    F.mem p ↔ IsSceneWalk p := by
  constructor
  · exact F.sceneOnly p
  · intro hp
    induction hp with
    | single v => exact F.identities v
    | cons u v w hstep hrest ih =>
      cases w with
      | nil =>
        exact F.containsEdges u v hstep
      | cons y ys =>
        have h_edge : F.mem [u, v] := F.containsEdges u v hstep
        have h_comp : Composable [u, v] (v :: y :: ys) := by
          use v
          refine ⟨rfl, rfl⟩
        have h_composed := F.compClosed [u, v] (v :: y :: ys) h_edge ih h_comp
        unfold composePath at h_composed
        dsimp at h_composed
        exact h_composed

/-- Non-backtracking predicate on paths: adjacent steps without immediate returns `v_{i} = v_{i+2}`. -/
def IsNonBacktracking (p : List Vertex33) : Prop :=
  IsSceneWalk p ∧
  match p with
  | [] => True
  | [_] => True
  | [_, _] => True
  | u :: v :: w :: rest =>
      u ≠ w ∧
      -- recursive condition on remainder
      let rec no_backtrack : List Vertex33 → Prop
        | a :: b :: c :: tl => a ≠ c ∧ no_backtrack (b :: c :: tl)
        | _ => True
      no_backtrack (v :: w :: rest)

/-- Composition closed predicate for a path property. -/
def CompositionClosed (P : List Vertex33 → Prop) : Prop :=
  ∀ p q, P p → P q → Composable p q → P (composePath p q)

/-- Scene step between vertex 0 (in part 9) and vertex 9 (in part 11). -/
theorem edge_0_9 : SceneStep 0 9 := by
  unfold SceneStep Adj31 zone31
  native_decide

/-- Scene step between vertex 9 (in part 11) and vertex 0 (in part 9). -/
theorem edge_9_0 : SceneStep 9 0 := by
  unfold SceneStep Adj31 zone31
  native_decide

/-- Path `[0, 9]` is non-backtracking. -/
theorem nb_0_9 : IsNonBacktracking [0, 9] := by
  refine ⟨IsSceneWalk.cons 0 9 [] edge_0_9 (IsSceneWalk.single 9), trivial⟩

/-- Path `[9, 0]` is non-backtracking. -/
theorem nb_9_0 : IsNonBacktracking [9, 0] := by
  refine ⟨IsSceneWalk.cons 9 0 [] edge_9_0 (IsSceneWalk.single 0), trivial⟩

/-- `[0, 9]` and `[9, 0]` are composable. -/
theorem comp_0_9_0 : Composable [0, 9] [9, 0] := by
  use 9
  refine ⟨rfl, rfl⟩

/-- Composite path of `[0, 9]` and `[9, 0]` is `[0, 9, 0]`. -/
theorem compose_0_9_0_eq : composePath [0, 9] [9, 0] = [0, 9, 0] := by
  unfold composePath
  rfl

/-- **Theorem B: Non-backtracking is NOT composition-closed on vertex objects.**
The paths `[0, 9]` and `[9, 0]` are both non-backtracking, but their concatenation
`[0, 9, 0]` backtracks immediately. Hence non-backtracking is not a composition-closed
history completion of the vertex-object scene tick. -/
theorem nonBacktracking_not_composition_closed :
    ¬ CompositionClosed IsNonBacktracking := by
  intro h_closed
  have h_comp := h_closed [0, 9] [9, 0] nb_0_9 nb_9_0 comp_0_9_0
  rw [compose_0_9_0_eq] at h_comp
  rcases h_comp with ⟨_hwalk, hnb⟩
  dsimp [IsNonBacktracking] at hnb
  have h00 : (0 : Vertex33) ≠ 0 := hnb.1
  exact h00 rfl

/-- Depth-2 scene walks: triples `(u, v, w)` with `SceneStep u v` and `SceneStep v w`. -/
def Depth2Walk := { trip : Vertex33 × Vertex33 × Vertex33 // SceneStep trip.1 trip.2.1 ∧ SceneStep trip.2.1 trip.2.2 }

instance : Fintype Depth2Walk :=
  inferInstanceAs (Fintype { trip : Vertex33 × Vertex33 × Vertex33 // SceneStep trip.1 trip.2.1 ∧ SceneStep trip.2.1 trip.2.2 })

/-- Immediate return walks: depth-2 walks with `u = w`. -/
def ImmediateReturn := { trip : Depth2Walk // trip.val.1 = trip.val.2.2 }

instance : Fintype ImmediateReturn :=
  inferInstanceAs (Fintype { trip : Depth2Walk // trip.val.1 = trip.val.2.2 })

/-- Level-1 scene history: an ordered adjacent pair of vertices. -/
def LevelOneSceneHistory := { p : Vertex33 × Vertex33 // SceneStep p.1 p.2 }

instance : Fintype LevelOneSceneHistory :=
  inferInstanceAs (Fintype { p : Vertex33 × Vertex33 // SceneStep p.1 p.2 })

/-- Canonical bijection between `ImmediateReturn` and `LevelOneSceneHistory`:
`(u, v, u) ↔ (u, v)`. -/
def immediateReturnEquivLevelOne : ImmediateReturn ≃ LevelOneSceneHistory where
  toFun ret := ⟨(ret.val.val.1, ret.val.val.2.1), ret.val.property.1⟩
  invFun edge := ⟨⟨(edge.val.1, edge.val.2, edge.val.1), ⟨edge.property, sceneStep_symm edge.property⟩⟩, rfl⟩
  left_inv := by
    rintro ⟨⟨⟨u, v, w⟩, ⟨h1, h2⟩⟩, heq⟩
    dsimp at heq
    subst w
    rfl
  right_inv := by
    rintro ⟨⟨u, v⟩, h⟩
    rfl

/-- The number of level-1 scene histories is exactly 718. -/
theorem level_one_card_eq_718 : Fintype.card LevelOneSceneHistory = 718 := by
  native_decide

/-- **Theorem C: Exactly 718 immediate returns, matching the difference 15708 - 14990.** -/
theorem immediate_return_cardinality :
    Fintype.card ImmediateReturn = 718 := by
  rw [Fintype.card_congr immediateReturnEquivLevelOne]
  exact level_one_card_eq_718

/-- Arithmetic resolution of the depth-2 carrier split: 15708 = 14990 + 718. -/
theorem depth2_carrier_decomposition :
    allWalksDepth2 = nonBacktrackingDepth2 + Fintype.card ImmediateReturn := by
  rw [immediate_return_cardinality]
  unfold allWalksDepth2 nonBacktrackingDepth2
  decide

/-- **Theorem D: Directed edges are precisely level-1 histories.**
The dimension 718 is the cardinality of the 1-step generating arrow space,
not a rival state dimension to 33. -/
theorem directed_edges_are_level_one_histories :
    Fintype.card LevelOneSceneHistory = 2 * numEdges := by
  rw [level_one_card_eq_718]
  rfl

/-- Complete theoretical owner for `D0-SCENE-PATH-COMPOSITION-CANONICITY-001`. -/
theorem scene_path_composition_canonicity_owner :
    (∀ F : SceneHistoryFamily, ∀ p, F.mem p ↔ IsSceneWalk p) ∧
    (¬ CompositionClosed IsNonBacktracking) ∧
    (Fintype.card ImmediateReturn = 718) ∧
    (allWalksDepth2 = nonBacktrackingDepth2 + 718) ∧
    (Fintype.card LevelOneSceneHistory = 718) := by
  refine ⟨composition_complete_eq_all_walks,
          nonBacktracking_not_composition_closed,
          immediate_return_cardinality,
          by unfold allWalksDepth2 nonBacktrackingDepth2; decide,
          level_one_card_eq_718⟩

end D0.VNext2.ScenePathHistoryCanonicity
