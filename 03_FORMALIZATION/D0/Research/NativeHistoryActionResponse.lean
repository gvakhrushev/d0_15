import D0.Claims.Signature31Split
import D0.VNext2.ScenePathHistoryCanonicity
import D0.Foundation.EndogenousActionQuantum
import D0.Foundation.PopperianBootstrap
import D0.CondensedAnchor.DetectorSupportGoldenWeight
import Mathlib.Tactic

/-!
# Two-tick path-resolved response of the scene action fiber

The full K(9,11,13) history owner admits every ordered walk, including the
two-step return `[0, 9, 0]`. Two actual ActionProtocol completions on the same
33-state verification carrier give this same history different edge costs under
the explicit diagnostic identification `Cost(x,y) := ActionProtocol.action x y`.
With the path's total vertex information held fixed, Book 03's `phi^(-Cost + Info)`
coefficient changes by an exact factor of `phi`. This is a path-coefficient result,
not a variation theorem for the full `Z_D` sum. It does not identify the diagnostic
interface with a coframe/link/matter variation or prove physical admission of either
completion.
-/

open scoped goldenRatio
open Real

namespace D0.Research.NativeHistoryActionResponse

open D0.Claims
open D0.VNext2.ScenePathHistoryCanonicity
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.EndogenousActionQuantum

abbrev Vertex := Fin 33

/-- The actual K(9,11,13) vertices as the states of an exact verification protocol. -/
def sceneProtocol : VerificationProtocol where
  State := Vertex
  Record := Vertex
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ x y => decide (x ≠ y)

/-- The same carrier satisfies the owner's full verification contract. -/
theorem sceneProtocol_contract : VerificationContract sceneProtocol where
  state_nontrivial := by
    change Nontrivial Vertex
    infer_instance
  line_nontrivial := by
    change Nontrivial Bool
    infer_instance
  catalogue_nonempty := ⟨()⟩
  correct := by intro l c x y; rfl

/-- A second admissible primitive cost profile, varying only on two directed zone pairs. -/
noncomputable def historyCost (x y : Vertex) : ℝ :=
  if x = y then 0
  else if zone31 x = (0 : Fin 3) ∧ zone31 y = 1 then 3
  else if zone31 x = 2 ∧ zone31 y = 1 then 17 / 13
  else 2

/-- This cost profile is a genuine member of the actual ActionProtocol fiber. -/
noncomputable def historyAction : ActionProtocol sceneProtocol where
  action := historyCost
  action_refl := by
    intro x
    simp [historyCost]
  action_nontrivial := by
    intro x y hxy
    simp only [historyCost]
    split_ifs with hEq h01 h21
    · exact (hxy hEq).elim
    · norm_num
    · norm_num
    · norm_num

/-- The constant-cost completion, expressed on the concrete `Fin 33` state type. -/
noncomputable def uniformHistoryCost (x y : Vertex) : ℝ :=
  if x = y then 0 else 2

noncomputable def uniformHistoryAction : ActionProtocol sceneProtocol where
  action := uniformHistoryCost
  action_refl := by intro x; simp [uniformHistoryCost]
  action_nontrivial := by
    intro x y hxy
    change 1 ≤ (if x = y then (0 : ℝ) else 2)
    split_ifs with h
    · exact (hxy h).elim
    · norm_num

/-- A return history through vertex 9, the first history in the 9-zone. -/
def return090 : Depth2Walk :=
  ⟨(0, 9, 0), ⟨by decide, by decide⟩⟩

/-- A return history through vertex 20, in the 13-zone. -/
def return020 : Depth2Walk :=
  ⟨(0, 20, 0), ⟨by decide, by decide⟩⟩

theorem v0_ne_9 : (0 : Vertex) ≠ 9 := by decide
theorem v9_ne_0 : (9 : Vertex) ≠ 0 := by decide
theorem v0_ne_20 : (0 : Vertex) ≠ 20 := by decide
theorem v20_ne_0 : (20 : Vertex) ≠ 0 := by decide
theorem zone0 : zone31 (0 : Vertex) = 0 := by norm_num [zone31]
theorem zone9 : zone31 (9 : Vertex) = 1 := by norm_num [zone31]
theorem zone20 : zone31 (20 : Vertex) = 2 := by norm_num [zone31]
theorem zone2_ne_zone1 : (2 : Fin 3) ≠ 1 := by decide
theorem zone0_ne_zone2 : (0 : Fin 3) ≠ 2 := by decide
theorem zone2_ne_zone0 : (2 : Fin 3) ≠ 0 := by decide

/-- The additive edge-cost part of the Book 03 price on a two-step history. -/
def twoStepCost (A : ActionProtocol sceneProtocol) (p : Depth2Walk) : ℝ :=
  A.action p.val.1 p.val.2.1 + A.action p.val.2.1 p.val.2.2

theorem return090_valid : IsSceneWalk [0, 9, 0] := by
  exact IsSceneWalk.cons 0 9 [0] (by decide)
    (IsSceneWalk.cons 9 0 [] (by decide) (IsSceneWalk.single 0))

theorem return020_valid : IsSceneWalk [0, 20, 0] := by
  have h20 : SceneStep 0 20 := by decide
  have h02 : SceneStep 20 0 := by decide
  exact IsSceneWalk.cons 0 20 [0] h20
    (IsSceneWalk.cons 20 0 [] h02 (IsSceneWalk.single 0))

theorem return_histories_distinct : return090.val ≠ return020.val := by
  decide

theorem uniform_return090_cost : twoStepCost uniformHistoryAction return090 = 4 := by
  change uniformHistoryCost (0 : Vertex) (9 : Vertex) +
      uniformHistoryCost (9 : Vertex) (0 : Vertex) = 4
  simp [uniformHistoryCost, v0_ne_9, v9_ne_0]; norm_num

theorem history_return090_cost : twoStepCost historyAction return090 = 5 := by
  change historyAction.action (0 : Vertex) (9 : Vertex) +
    historyAction.action (9 : Vertex) (0 : Vertex) = 5
  simp [historyAction, historyCost, zone0, zone9, v0_ne_9, v9_ne_0]; norm_num

theorem uniform_return020_cost : twoStepCost uniformHistoryAction return020 = 4 := by
  change uniformHistoryCost (0 : Vertex) (20 : Vertex) +
      uniformHistoryCost (20 : Vertex) (0 : Vertex) = 4
  simp [uniformHistoryCost, v0_ne_20, v20_ne_0]; norm_num

theorem history_return020_cost : twoStepCost historyAction return020 = 4 := by
  change historyAction.action (0 : Vertex) (20 : Vertex) +
    historyAction.action (20 : Vertex) (0 : Vertex) = 4
  simp [historyAction, historyCost, zone0, zone20, zone2_ne_zone1,
    zone0_ne_zone2, zone2_ne_zone0, v0_ne_20, v20_ne_0]; norm_num

/-- Book 03's forced exponential weight for a path with a fixed total vertex-information value.
Writing it as `exp((Info-Cost) log phi)` is exactly `phi^(Info-Cost)`. -/
noncomputable def book03PathWeight (A : ActionProtocol sceneProtocol) (p : Depth2Walk)
    (info : ℝ) : ℝ :=
  Real.exp ((info - twoStepCost A p) * Real.log φ)

/-- The same complete two-tick history changes weight under two admitted primitive costs,
for every shared information term. -/
theorem same_history_weight_changes (info : ℝ) :
    book03PathWeight uniformHistoryAction return090 info >
      book03PathWeight historyAction return090 info := by
  unfold book03PathWeight
  rw [uniform_return090_cost, history_return090_cost]
  apply Real.exp_lt_exp.mpr
  have hlog : 0 < Real.log φ := Real.log_pos one_lt_goldenRatio
  nlinarith

/-- The changed path coefficient is exactly one golden factor, independently of fixed Info. -/
theorem same_history_weight_ratio (info : ℝ) :
    book03PathWeight uniformHistoryAction return090 info =
      φ * book03PathWeight historyAction return090 info := by
  unfold book03PathWeight
  rw [uniform_return090_cost, history_return090_cost]
  have hshift : (info - 4) * Real.log φ =
      (info - 5) * Real.log φ + Real.log φ := by ring
  rw [hshift, Real.exp_add, Real.exp_log (by positivity : 0 < φ)]
  ring

/-- The control return has the same path coefficient under both protocols. -/
theorem control_history_weight_unchanged (info : ℝ) :
    book03PathWeight uniformHistoryAction return020 info =
      book03PathWeight historyAction return020 info := by
  unfold book03PathWeight
  rw [uniform_return020_cost, history_return020_cost]

/-- On this fixed return fiber, the second path is unaffected; the cost change is carried by
the ordered intermediate history, not by either endpoint or the tick count. -/
theorem same_endpoints_different_history_costs :
    twoStepCost historyAction return090 = 5 ∧
    twoStepCost historyAction return020 = 4 ∧
    return090.val.1 = return020.val.1 ∧
    return090.val.2.2 = return020.val.2.2 := by
  exact ⟨history_return090_cost, history_return020_cost, rfl, rfl⟩

end D0.Research.NativeHistoryActionResponse
