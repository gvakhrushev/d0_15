import D0.Foundation.EndogenousActionQuantum

/-!
# Prospective execution and exact paid-history boundaries — preserved proof intake

The declarations below were initially copied byte-for-byte from
`03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean`
at `bf82fb54c63bbe95aee5e459a30f17a27f576519`.
The reserved binder spelling `prefix` is now renamed consistently to
`initialSegment`; the mathematical statements and assumptions are unchanged.
See `02_REGISTRY/research/D0_FOUNDATION_MAIN_INTAKE_2026_10_20.md` for
provenance, exact scope and the continuing physical consumers.
-/

namespace D0.Foundation.EndogenousActionQuantum

open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.PopperianBootstrap

/-! ## Fundamental M1/MDL source: paid reversible history is not endpoint cost

The original endogenous action quantum forces every actually
distinguishable nonidentity physical transition to cost at least one
unit. A reversible two-transition RETURN to exactly the SAME
registered state is therefore NOT equivalent, as a fully paid
history, to the null-history identity transition. No gravitational
action or arbitrary quantum coupling enters this theorem.

The proof is purely foundational; it is conditional on a REAL
source admitting both x→y and y→x, which the ActionProtocol
price assignment by itself does not guarantee. One must never
erase actual intermediate record/provenance on the basis of equal
endpoints, nor claim the theorem selects complete Book03 work.
-/

/-- One truly distinguishable forward transition AND its returning
reverse pay at least two original endogenous action quanta. -/
theorem original_roundtrip_forces_paid_history
    {P : VerificationProtocol} (A : ActionProtocol P)
    (x y : P.State) (h : x ≠ y) :
    2 ≤ A.action x y + A.action y x := by
  have hforward := A.action_nontrivial x y h
  have hback := A.action_nontrivial y x h.symm
  linarith

/-- A complete source-path Cost that counts the two genuinely executed
primitive transitions CANNOT be a function of the final state alone,
with the original empty history assigned zero. The endpoint x is
identical in both executions. -/
theorem original_roundtrip_no_endpoint_only_paid_action
    {P : VerificationProtocol} (A : ActionProtocol P)
    (x y : P.State) (h : x ≠ y) :
    ¬ ∃ costOfEndpoint : P.State → ℝ,
        costOfEndpoint x = 0 ∧
        costOfEndpoint x = A.action x y + A.action y x := by
  rintro ⟨f, hblank, hpaid⟩
  have hmin := original_roundtrip_forces_paid_history A x y h
  rw [hblank] at hpaid
  linarith



/-! ## Research frontier: PROSPECTIVE MDL SELECTION, not after-the-fact compression

The original Tome I definition of D_min compares equivalent DESCRIPTIONS;
the existing ActionProtocol assigns a lower bound to actual transition
COST. Neither definition alone states that the physical world SELECTS
its next feasible execution by minimizing cumulative action. The
following explicit separate DYNAMICAL SELECTION PREMISE formalizes the
strong prospective-MDL hypothesis without smuggling it into M1.

A prospective execution includes the COMPLETE state (including all
currently relevant retained archive, clock, momentum and preparation),
allowed actions, a goal/boundary predicate and full transition costs.
If the selected whole trajectory really minimizes the given FULL price
among all physically allowed alternatives with the SAME initial state
and SAME goal, it cannot contain an avoidable positive-cost detour
that returns to the SAME COMPLETE state. No retroactive rewriting is
involved. Uniqueness under ties, actual Book H+J+R selection and GR
do not follow from this structural principle-of-optimality theorem.
-/

/-- Physical-type finite state machine with ORIGINAL enabled actions,
full state-dependent execution price and NO extrinsic future oracle. -/
structure ProspectiveDynamics where
  State : Type
  Action : Type
  step : State → Action → State
  allowed : State → Action → Prop
  price : State → Action → ℝ

/-- Execute a list of original admitted operations chronologically. -/
def ProspectiveDynamics.run (D : ProspectiveDynamics) (s : D.State) :
    List D.Action → D.State
  | [] => s
  | a :: tail => D.run (D.step s a) tail

/-- Accumulate the FULL actual state-dependent step price. -/
def ProspectiveDynamics.totalPrice (D : ProspectiveDynamics) (s : D.State) :
    List D.Action → ℝ
  | [] => 0
  | a :: tail => D.price s a + D.totalPrice (D.step s a) tail

/-- Admissibility is evaluated at EVERY actual intermediate state,
not inferred from a mere shared endpoint. -/
def ProspectiveDynamics.executable (D : ProspectiveDynamics) (s : D.State) :
    List D.Action → Prop
  | [] => True
  | a :: tail => D.allowed s a ∧ D.executable (D.step s a) tail

theorem ProspectiveDynamics.run_append (D : ProspectiveDynamics)
    (s : D.State) (head tail : List D.Action) :
    D.run s (head ++ tail) = D.run (D.run s head) tail := by
  induction head generalizing s with
  | nil => rfl
  | cons a rest ih =>
      exact ih (D.step s a)

theorem ProspectiveDynamics.totalPrice_append (D : ProspectiveDynamics)
    (s : D.State) (head tail : List D.Action) :
    D.totalPrice s (head ++ tail) =
      D.totalPrice s head + D.totalPrice (D.run s head) tail := by
  induction head generalizing s with
  | nil => simp [ProspectiveDynamics.totalPrice, ProspectiveDynamics.run]
  | cons a rest ih =>
      simp only [List.cons_append, ProspectiveDynamics.totalPrice,
        ProspectiveDynamics.run]
      rw [ih]
      ring

theorem ProspectiveDynamics.executable_append (D : ProspectiveDynamics)
    (s : D.State) (head tail : List D.Action) :
    D.executable s (head ++ tail) ↔
      D.executable s head ∧ D.executable (D.run s head) tail := by
  induction head generalizing s with
  | nil =>
      simp [ProspectiveDynamics.executable, ProspectiveDynamics.run]
  | cons a rest ih =>
      simp only [List.cons_append, ProspectiveDynamics.executable,
        ProspectiveDynamics.run]
      rw [ih]
      tauto

/-- An explicit PROSPECTIVE physical selection rule.
Its optimality is a PREMISE to be DERIVED from full native M1/Book
Cost-Info, NOT an already proved theorem of the original D_min definition. -/
structure ProspectiveExecution (D : ProspectiveDynamics) where
  initial : D.State
  goal : D.State → Prop
  chosen : List D.Action
  chosen_executable : D.executable initial chosen
  chosen_goal : goal (D.run initial chosen)
  optimal : ∀ alternative : List D.Action,
    D.executable initial alternative →
    goal (D.run initial alternative) →
    D.totalPrice initial chosen ≤ D.totalPrice initial alternative

/-- Prospective, not retrospective: a strictly cheaper genuinely
feasible alternative with the SAME initial FULL state and terminal
goal excludes the selected history before it occurs. -/
theorem ProspectiveExecution.reject_strictly_dominated
    {D : ProspectiveDynamics} (E : ProspectiveExecution D)
    (alternative : List D.Action)
    (hvalid : D.executable E.initial alternative)
    (hgoal : E.goal (D.run E.initial alternative)) :
    ¬ D.totalPrice E.initial alternative <
        D.totalPrice E.initial E.chosen := by
  exact not_lt.mpr (E.optimal alternative hvalid hgoal)

/-- The finite Bellman principle follows from prospective global
choice, complete state and additive true history price. Replacing
a selected suffix by an allowed cheaper suffix reaching the SAME
goal is impossible. -/
theorem ProspectiveExecution.optimal_suffix
    {D : ProspectiveDynamics} (E : ProspectiveExecution D)
    (initialSegment suffix alternative : List D.Action)
    (hchosen : E.chosen = initialSegment ++ suffix)
    (hprefix : D.executable E.initial initialSegment)
    (halt : D.executable (D.run E.initial initialSegment) alternative)
    (hgoal : E.goal (D.run (D.run E.initial initialSegment) alternative)) :
    D.totalPrice (D.run E.initial initialSegment) suffix ≤
      D.totalPrice (D.run E.initial initialSegment) alternative := by
  have hwhole : D.executable E.initial (initialSegment ++ alternative) :=
    (D.executable_append E.initial initialSegment alternative).2 ⟨hprefix, halt⟩
  have hwholeGoal : E.goal (D.run E.initial (initialSegment ++ alternative)) := by
    rw [D.run_append]
    exact hgoal
  have hopt := E.optimal (initialSegment ++ alternative) hwhole hwholeGoal
  rw [hchosen, D.totalPrice_append, D.totalPrice_append] at hopt
  linarith

/-- No actual prospective optimum contains an unnecessary positive-
cost cycle returning to the SAME full future-sufficient physical
state when the shorter execution preserves all allowed constraints.
This is a generated law of selection, NOT an ex-post rewriting rule. -/
theorem ProspectiveExecution.no_positive_redundant_detour
    {D : ProspectiveDynamics} (E : ProspectiveExecution D)
    (initialSegment detour suffix : List D.Action)
    (hchosen : E.chosen = initialSegment ++ (detour ++ suffix))
    (hreturn : D.run (D.run E.initial initialSegment) detour =
      D.run E.initial initialSegment)
    (hcost : 0 < D.totalPrice (D.run E.initial initialSegment) detour) :
    False := by
  have hwhole : D.executable E.initial
      (initialSegment ++ (detour ++ suffix)) := by
    simpa [hchosen] using E.chosen_executable
  have hp := (D.executable_append E.initial initialSegment
    (detour ++ suffix)).1 hwhole
  have htail0 := (D.executable_append (D.run E.initial initialSegment)
    detour suffix).1 hp.2
  have htail : D.executable (D.run E.initial initialSegment) suffix := by
    rw [← hreturn]
    exact htail0.2
  have hgoal : E.goal (D.run (D.run E.initial initialSegment) suffix) := by
    have hg : E.goal (D.run E.initial
        (initialSegment ++ (detour ++ suffix))) := by
      simpa [hchosen] using E.chosen_goal
    rw [D.run_append, D.run_append, hreturn] at hg
    exact hg
  have hopt := E.optimal_suffix initialSegment (detour ++ suffix) suffix
    hchosen hp.1 htail hgoal
  rw [D.totalPrice_append, hreturn] at hopt
  linarith



/-! ## Nontrivial D_min dynamics needs a REQUIRED verification task

If the physical goal is already met at the initial complete state,
the empty history is allowed and has zero execution price. When
every actual primitive costs STRICTLY more than zero, any prospective
global minimizer must choose this empty history. Therefore primitive
Cost>=S_min=1 plus a prospective minimizing law, by themselves,
CANNOT force a falling apple, any tick, or real change. The original
M1/D_min must provide a genuinely obligatory test/closure condition,
or the actual complete Cost-minus-Info objective must make idle
nonoptimal. No external ad hoc physical destination is assumed here.
-/

theorem ProspectiveDynamics.totalPrice_nonneg
    (D : ProspectiveDynamics) (hprice : ∀ s a, 0 ≤ D.price s a)
    (s : D.State) (word : List D.Action) :
    0 ≤ D.totalPrice s word := by
  induction word generalizing s with
  | nil => simp [ProspectiveDynamics.totalPrice]
  | cons a tail ih =>
      change 0 ≤ D.price s a + D.totalPrice (D.step s a) tail
      exact add_nonneg (hprice s a) (ih (D.step s a))

theorem ProspectiveExecution.no_motion_without_a_required_distinction
    {D : ProspectiveDynamics} (E : ProspectiveExecution D)
    (goal_already_met : E.goal E.initial)
    (hpositive : ∀ s a, 0 < D.price s a) :
    E.chosen = [] := by
  cases hchosen : E.chosen with
  | nil => rfl
  | cons a tail =>
      have hzeroLegal : D.executable E.initial
          ([] : List D.Action) := by
        simp [ProspectiveDynamics.executable]
      have hzeroGoal : E.goal (D.run E.initial
          ([] : List D.Action)) := by
        simpa [ProspectiveDynamics.run] using goal_already_met
      have hopt := E.optimal [] hzeroLegal hzeroGoal
      rw [hchosen] at hopt
      have htail := D.totalPrice_nonneg
        (fun s a => le_of_lt (hpositive s a))
        (D.step E.initial a) tail
      have hbound : D.price E.initial a +
          D.totalPrice (D.step E.initial a) tail ≤ 0 := by
        simpa [ProspectiveDynamics.totalPrice] using hopt
      linarith [hpositive E.initial a]

theorem ProspectiveExecution.nonempty_forces_unsatisfied_initial_goal
    {D : ProspectiveDynamics} (E : ProspectiveExecution D)
    (hpositive : ∀ s a, 0 < D.price s a)
    (hword : E.chosen ≠ []) : ¬ E.goal E.initial := by
  intro hgoal
  exact hword (E.no_motion_without_a_required_distinction hgoal hpositive)

end D0.Foundation.EndogenousActionQuantum
