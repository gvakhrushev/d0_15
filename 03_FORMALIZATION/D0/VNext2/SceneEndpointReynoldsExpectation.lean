import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Claims.Signature31Split
import D0.Synthesis.SceneNormalizedQuotientDescent
import D0.VNext2.ScenePathHistoryCanonicity

/-!
# D0.VNext2.SceneEndpointReynoldsExpectation

Theoretical owner: `D0-SCENE-ONE-STEP-HISTORY-TRANSPORT-001`.

Formalization of the canonical endpoint conditional expectation on 1-step scene histories:
1. `source` and `endpoint` maps on `LevelOneSceneHistory`.
2. Endpoint lift $J_t$ and source lift $J_s$ as matrices.
3. Canonical endpoint conditional expectation / Reynolds average $C_1$:
   $$C_1(v, \gamma) = \frac{1}{\operatorname{deg}(v)} \quad \text{if } \operatorname{end}(\gamma) = v \text{ else } 0.$$
4. Exact left-inverse identity: $C_1 J_t = 1$.
5. Idempotence of the Reynolds projector: $(J_t C_1)^2 = J_t C_1$.
6. Projection property: $(J_t C_1) J_t = J_t$.
7. Crucial forgetting identity connecting 1-step history to the random walk transport:
   $$C_1 J_s = \operatorname{fullTransport}.$$
8. Fiber cardinality equal to degree, pushforward counting weights $(216, 242, 260)$,
   and edge-reversal detailed balance.
-/

namespace D0.VNext2.SceneEndpointReynoldsExpectation

open D0.Claims
open D0.Synthesis.SceneNormalizedQuotientDescent
open D0.VNext2.ScenePathHistoryCanonicity

/-- Source vertex of a level-1 history. -/
def source (γ : LevelOneSceneHistory) : Fin 33 :=
  γ.val.1

/-- Endpoint vertex of a level-1 history. -/
def endpoint (γ : LevelOneSceneHistory) : Fin 33 :=
  γ.val.2

/-- Endpoint lift matrix $J_t$: pulls vertex functions to endpoint-evaluated history functions. -/
def Jt : Matrix LevelOneSceneHistory (Fin 33) ℚ :=
  Matrix.of fun γ v => if endpoint γ = v then 1 else 0

/-- Source lift matrix $J_s$: pulls vertex functions to source-evaluated history functions. -/
def Js : Matrix LevelOneSceneHistory (Fin 33) ℚ :=
  Matrix.of fun γ u => if source γ = u then 1 else 0

/-- Canonical endpoint average matrix $C_1$: averages history data over the fiber of paths
ending at vertex $v$. -/
def C1 : Matrix (Fin 33) LevelOneSceneHistory ℚ :=
  Matrix.of fun v γ => if endpoint γ = v then (fullDegreeValue v)⁻¹ else 0

/-- Reversal of a directed step: $(u, v) \mapsto (v, u)$. -/
def reverseEdge (γ : LevelOneSceneHistory) : LevelOneSceneHistory :=
  ⟨(γ.val.2, γ.val.1), sceneStep_symm γ.property⟩

theorem reverseEdge_involutive (γ : LevelOneSceneHistory) :
    reverseEdge (reverseEdge γ) = γ := by
  cases γ
  rfl

/-- Vertex degree is strictly positive on the connected scene graph. -/
theorem fullDegreeValue_pos (v : Fin 33) : 0 < fullDegreeValue v := by
  revert v
  native_decide

theorem fullDegreeValue_ne_zero (v : Fin 33) : fullDegreeValue v ≠ 0 :=
  ne_of_gt (fullDegreeValue_pos v)

/-- The fiber of level-1 histories ending at $v$ has cardinality equal to $\operatorname{deg}(v)$. -/
theorem endpoint_counting_mass_eq_degree (v : Fin 33) :
    (∑ γ : LevelOneSceneHistory, if endpoint γ = v then (1 : ℚ) else 0) = fullDegreeValue v := by
  revert v
  native_decide

/-- **Theorem 1: Canonical Left-Inverse.**
The endpoint averaging operator $C_1$ is a strict left inverse to the endpoint lift $J_t$:
$$C_1 J_t = 1.$$ -/
theorem endpoint_average_left_inverse :
    C1 * Jt = 1 := by
  native_decide

/-- **Theorem 2: Idempotence of the Endpoint Reynolds Projector.**
$$(J_t C_1)^2 = J_t C_1.$$ -/
theorem endpoint_reynolds_idempotent :
    (Jt * C1) * (Jt * C1) = Jt * C1 := by
  have h : (Jt * C1) * (Jt * C1) = Jt * (C1 * Jt) * C1 := by
    simp only [Matrix.mul_assoc]
  rw [h, endpoint_average_left_inverse, Matrix.mul_one]

/-- **Theorem 3: Reynolds Projection Fixes Endpoint Functions.**
$$(J_t C_1) J_t = J_t.$$ -/
theorem endpoint_reynolds_fixes_endpoint_functions :
    (Jt * C1) * Jt = Jt := by
  rw [Matrix.mul_assoc, endpoint_average_left_inverse, Matrix.mul_one]

/-- **Theorem 4: Key Forgetting Stitch.**
Averaging the source lift $J_s$ over the endpoint fiber yields exactly the full random-walk
transport matrix:
$$C_1 J_s = \operatorname{fullTransport}.$$ -/
theorem one_step_history_forgetting_eq_fullTransport :
    C1 * Js = fullTransport := by
  native_decide

/-- Pushforward counting weights partitioned by zone sum to $(216, 242, 260)$. -/
theorem oriented_edge_pushforward_eq_stationary_weight :
    (∑ v : Fin 33, if zone31 v = 0 then fullDegreeValue v else 0) = 216 ∧
    (∑ v : Fin 33, if zone31 v = 1 then fullDegreeValue v else 0) = 242 ∧
    (∑ v : Fin 33, if zone31 v = 2 then fullDegreeValue v else 0) = 260 := by
  native_decide

/-- Edge reversal detailed balance at the level of generating arrows. -/
theorem edge_reversal_detailed_balance (u v : Fin 33) :
    fullDegreeValue u * fullTransport u v = fullDegreeValue v * fullTransport v u := by
  revert u v
  native_decide

/-- **D0-SCENE-ONE-STEP-HISTORY-TRANSPORT-001 (CORE-FORMALIZED).**
The canonical 1-step endpoint conditional expectation satisfies the left-inverse identity,
idempotence, projectivity, and descent to the full random walk transport. -/
theorem scene_one_step_history_transport_owner :
    C1 * Jt = 1 ∧
    (Jt * C1) * (Jt * C1) = Jt * C1 ∧
    (Jt * C1) * Jt = Jt ∧
    C1 * Js = fullTransport :=
  ⟨endpoint_average_left_inverse,
   endpoint_reynolds_idempotent,
   endpoint_reynolds_fixes_endpoint_functions,
   one_step_history_forgetting_eq_fullTransport⟩

end D0.VNext2.SceneEndpointReynoldsExpectation
