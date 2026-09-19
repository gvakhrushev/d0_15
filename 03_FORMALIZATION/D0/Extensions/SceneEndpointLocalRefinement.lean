import Mathlib.Tactic

/-!
# D0.Extensions.SceneEndpointLocalRefinement

Theoretical owner: `D0-SCENE-ENDPOINT-LOCAL-REFINEMENT-001`.

Investigation of the history refinement ambiguity (all-walks `W` vs non-backtracking `NB`).
The reason for multiple admissible completions in `SceneHistoryRefinementExtension`
is that admissibility previously allowed history-dependent transition extension rules.

Here we formulate the precise structural boundary:
1. Histories are sequences of vertices in `V` (with at least one element: `head :: rest`).
2. An extension rule `R : NonemptyHistory V → V → Bool` determines whether a history `h`
   can be extended by vertex `w`.
3. `EndpointLocal`: the rule depends only on the current state (endpoint of the history),
   not on past trajectory memory.
4. `SceneFaithful`: on single-vertex histories (`[v]`), `R [v] w` coincides with the
   scene graph adjacency `Adj v w`.

Main Results:
* `allWalksRule` is endpoint-local.
* `nonBacktrackingRule` is NOT endpoint-local (counterexample: distinct pasts arriving
  at the same vertex produce conflicting extension decisions).
* **Uniqueness Theorem**: Any endpoint-local and scene-faithful extension rule is
  IDENTICALLY equal to `allWalksRule`.

Epistemological Status:
This is a conditional theorem: IF archive/history is passive (Markovian / endpoint-local),
the all-walks free path tower is canonical. However, because D0 allows internal history
memory, endpoint locality is not yet derived from M1; hence the two-completion no-go
for `PRIM-SCENE-HISTORY-REFINEMENT-RULE` remains active until an owner for passive-archive
locality is established.
-/

namespace D0.Extensions.SceneEndpointLocalRefinement

/-- Nonempty history: a list of vertices with at least one vertex. -/
structure NonemptyHistory (V : Type) where
  head : V
  rest : List V

/-- The current state (endpoint) of a history. -/
def endpoint {V : Type} (h : NonemptyHistory V) : V :=
  match h.rest.getLast? with
  | none => h.head
  | some v => v

/-- Singleton history containing just vertex `v`. -/
def singleton {V : Type} (v : V) : NonemptyHistory V :=
  ⟨v, []⟩

/-- Endpoint locality: extension decisions depend strictly on the current endpoint. -/
def EndpointLocal {V : Type} (R : NonemptyHistory V → V → Bool) : Prop :=
  ∀ h₁ h₂ w, endpoint h₁ = endpoint h₂ → R h₁ w = R h₂ w

/-- Scene faithfulness: on single-vertex histories, extension coincides with scene adjacency. -/
def SceneFaithful {V : Type} (Adj : V → V → Bool) (R : NonemptyHistory V → V → Bool) : Prop :=
  ∀ v w, R (singleton v) w = Adj v w

/-- The all-walks extension rule: allows transition whenever `w` is adjacent to the endpoint. -/
def allWalksRule {V : Type} (Adj : V → V → Bool) (h : NonemptyHistory V) (w : V) : Bool :=
  Adj (endpoint h) w

/-- The all-walks rule is endpoint-local. -/
theorem all_walks_endpoint_local {V : Type} (Adj : V → V → Bool) :
    EndpointLocal (allWalksRule Adj) := by
  intro h₁ h₂ w heq
  unfold allWalksRule
  rw [heq]

/-- The all-walks rule is scene-faithful. -/
theorem all_walks_scene_faithful {V : Type} (Adj : V → V → Bool) :
    SceneFaithful Adj (allWalksRule Adj) := by
  intro v w
  unfold allWalksRule singleton endpoint
  rfl

/-- **Uniqueness Theorem**: Any endpoint-local and scene-faithful extension rule
is uniquely forced to be the all-walks rule. -/
theorem endpoint_local_scene_faithful_unique
    {V : Type} (Adj : V → V → Bool) (R : NonemptyHistory V → V → Bool)
    (h_local : EndpointLocal R)
    (h_faithful : SceneFaithful Adj R) :
    R = allWalksRule Adj := by
  ext h w
  have h_end : endpoint h = endpoint (singleton (endpoint h)) := by
    unfold singleton endpoint
    rfl
  have h_step1 : R h w = R (singleton (endpoint h)) w := by
    apply h_local
    exact h_end
  have h_step2 : R (singleton (endpoint h)) w = Adj (endpoint h) w := by
    apply h_faithful
  rw [h_step1, h_step2]
  rfl

/-- Non-backtracking previous vertex extractor (if history length ≥ 2). -/
def previous {V : Type} (h : NonemptyHistory V) : Option V :=
  match h.rest with
  | [] => none
  | [_] => some h.head
  | _ :: _ => (h.head :: h.rest).drop (h.rest.length - 1) |>.head?

/-- Non-backtracking extension rule: adjacent to endpoint AND $w \neq \mathrm{previous}(h)$. -/
def nonBacktrackingRule {V : Type} [DecidableEq V] (Adj : V → V → Bool) (h : NonemptyHistory V) (w : V) : Bool :=
  Adj (endpoint h) w && (match previous h with
                         | none => true
                         | some prev => decide (w ≠ prev))

/-- Explicit non-locality witness for non-backtracking on any graph with at least two distinct vertices $a \neq c$
both adjacent to a common vertex $b$. -/
theorem non_backtracking_not_endpoint_local
    {V : Type} [DecidableEq V] (Adj : V → V → Bool)
    (a b c : V) (_hab : a ≠ b) (_hbc : b ≠ c) (hac : a ≠ c)
    (h_adj_ba : Adj b a = true) (_h_adj_bc : Adj b c = true) :
    ¬ EndpointLocal (nonBacktrackingRule Adj) := by
  intro h_local
  let h₁ : NonemptyHistory V := ⟨a, [b]⟩
  let h₂ : NonemptyHistory V := ⟨c, [b]⟩
  have heq_end : endpoint h₁ = endpoint h₂ := by
    unfold endpoint h₁ h₂
    rfl
  have h_same := h_local h₁ h₂ a heq_end
  -- Evaluate R_NB on h₁ and a: previous is a, so w = a is backtrack (false)
  have h_r1 : nonBacktrackingRule Adj h₁ a = false := by
    unfold nonBacktrackingRule previous endpoint h₁
    simp
  -- Evaluate R_NB on h₂ and a: previous is c, so w = a ≠ c is allowed (true)
  have h_r2 : nonBacktrackingRule Adj h₂ a = true := by
    unfold nonBacktrackingRule previous endpoint h₂
    simp [h_adj_ba]
    exact hac
  rw [h_r1, h_r2] at h_same
  contradiction

/-- Summary owner for `D0-SCENE-ENDPOINT-LOCAL-REFINEMENT-001`. -/
theorem scene_endpoint_local_refinement_owner
    {V : Type} (Adj : V → V → Bool) :
    EndpointLocal (allWalksRule Adj) ∧
    SceneFaithful Adj (allWalksRule Adj) ∧
    (∀ R : NonemptyHistory V → V → Bool,
      EndpointLocal R → SceneFaithful Adj R → R = allWalksRule Adj) := by
  refine ⟨all_walks_endpoint_local Adj,
          all_walks_scene_faithful Adj,
          fun R h_loc h_faith => endpoint_local_scene_faithful_unique Adj R h_loc h_faith⟩

end D0.Extensions.SceneEndpointLocalRefinement
