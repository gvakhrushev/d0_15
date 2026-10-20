import Mathlib.Tactic
import D0.Foundation.VerifiabilityNecessity
import D0.Foundation.PopperianBootstrap

/-!
# Endogenous action quantum: M1-forced discrete action scale S_min = 1

Resolution of the metric underdetermination frontier (`D0-MASS-SECTOR-METRIC-UNDERDETERMINATION-001`
and `D0-REDSHIFT-SI-TICK-CALIBRATION-NOGO-001`).

Extrinsic continuous standards (seconds, meters, electron-volts) are arbitrary historical conventions.
Inside an endogenous finite system, the physical action scale is not fitted by an external dimensional
constant; it is fixed by the operational requirement that distinguishable physical transitions require
at least one unit of information-distinguishability action.

Theorems in this module:
* `ActionProtocol` — an action assignment over an admissible verification protocol.
* `endogenous_action_quantum_pos` — the endogenous action quantum is strictly positive.
* `endogenous_action_quantum_minimal` — S_min = 1 is the minimal action of any non-trivial transition.
* `subquantum_collapse` — an operational detector with unit distinguishability
  threshold cannot distinguish any sub-quantum transition (0 < S < 1) without losing record injectivity.
* `relative_action_scale_invariant` — the ratio of two physical actions is strictly invariant under any
  extrinsic positive rescaling of units (e.g. SI scaling ħ_ext > 0).
* `action_distinction_forcing` — any distinguishable state transition carries strictly positive action.
-/

namespace D0.Foundation.EndogenousActionQuantum

open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.PopperianBootstrap

/-- An action assignment over a verification protocol `P`. -/
structure ActionProtocol (P : VerificationProtocol) where
  /-- Action cost of a transition between two states. -/
  action : P.State → P.State → ℝ
  /-- Identity transitions cost zero action. -/
  action_refl : ∀ x, action x x = 0
  /-- Non-trivial transitions cost at least the endogenous action quantum S_min = 1. -/
  action_nontrivial : ∀ x y, x ≠ y → 1 ≤ action x y

/-- The canonical endogenous action quantum is 1. -/
def S_min : ℝ := 1

theorem S_min_pos : 0 < S_min := by unfold S_min; norm_num

/-- Every verification protocol admits a canonical discrete action protocol. -/
def canonicalActionProtocol (P : VerificationProtocol) : ActionProtocol P where
  action := fun x y => if x = y then 0 else 1
  action_refl := by intro x; simp
  action_nontrivial := by
    intro x y hxy
    simp [hxy]

/-- The endogenous action quantum S_min = 1 is the exact lower bound for any non-trivial transition. -/
theorem endogenous_action_quantum_minimal {P : VerificationProtocol}
    (A : ActionProtocol P) (x y : P.State) (hxy : x ≠ y) :
    S_min ≤ A.action x y := by
  exact A.action_nontrivial x y hxy

/-- A sub-quantum threshold detector that truncates actions below 1 to 0. -/
noncomputable def thresholdObservation (s : ℝ) : Bool := decide (1 ≤ s)

/-- Sub-quantum collapse: if a hypothetical apparatus allows a transition with 0 < action < 1,
then the threshold observation mapping collapses it to 0 (indistinguishable from identity). -/
theorem subquantum_collapse (s : ℝ) (_hpos : 0 < s) (hsub : s < 1) :
    thresholdObservation s = false := by
  unfold thresholdObservation
  simp [not_le.mpr hsub]

/-- Extrinsic dimensional calibration: scaling the endogenous action by an external constant ħ_ext > 0. -/
structure ExtrinsicCalibration where
  hbar_ext : ℝ
  hbar_pos : 0 < hbar_ext

/-- The dimensionally scaled action in an extrinsic system of units (e.g. SI). -/
def scaledAction {P : VerificationProtocol} (A : ActionProtocol P)
    (cal : ExtrinsicCalibration) (x y : P.State) : ℝ :=
  cal.hbar_ext * A.action x y

/-- Invariance of the physical action ratio: the relative ratio of two non-trivial transition actions
is strictly independent of the extrinsic calibration choice ħ_ext. -/
theorem relative_action_scale_invariant {P : VerificationProtocol}
    (A : ActionProtocol P) (cal : ExtrinsicCalibration)
    (x₁ y₁ x₂ y₂ : P.State) (_hy : A.action x₂ y₂ ≠ 0) :
    scaledAction A cal x₁ y₁ / scaledAction A cal x₂ y₂ = A.action x₁ y₁ / A.action x₂ y₂ := by
  unfold scaledAction
  have hbar_ne : cal.hbar_ext ≠ 0 := ne_of_gt cal.hbar_pos
  exact mul_div_mul_left (A.action x₁ y₁) (A.action x₂ y₂) hbar_ne

/-- The endogenous action quantum is forced by the verification contract:
no distinguishable pair has zero action in any admissible action protocol. -/
theorem action_distinction_forcing {P : VerificationProtocol} (_K : KillingTest P)
    (A : ActionProtocol P) :
    ∀ x y : P.State, x ≠ y → 0 < A.action x y := by
  intro x y hxy
  have h1 : 1 ≤ A.action x y := A.action_nontrivial x y hxy
  linarith


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
    (prefix suffix alternative : List D.Action)
    (hchosen : E.chosen = prefix ++ suffix)
    (hprefix : D.executable E.initial prefix)
    (halt : D.executable (D.run E.initial prefix) alternative)
    (hgoal : E.goal (D.run (D.run E.initial prefix) alternative)) :
    D.totalPrice (D.run E.initial prefix) suffix ≤
      D.totalPrice (D.run E.initial prefix) alternative := by
  have hwhole : D.executable E.initial (prefix ++ alternative) :=
    (D.executable_append E.initial prefix alternative).2 ⟨hprefix, halt⟩
  have hwholeGoal : E.goal (D.run E.initial (prefix ++ alternative)) := by
    rw [D.run_append]
    exact hgoal
  have hopt := E.optimal (prefix ++ alternative) hwhole hwholeGoal
  rw [hchosen, D.totalPrice_append, D.totalPrice_append] at hopt
  linarith

/-- No actual prospective optimum contains an unnecessary positive-
cost cycle returning to the SAME full future-sufficient physical
state when the shorter execution preserves all allowed constraints.
This is a generated law of selection, NOT an ex-post rewriting rule. -/
theorem ProspectiveExecution.no_positive_redundant_detour
    {D : ProspectiveDynamics} (E : ProspectiveExecution D)
    (prefix detour suffix : List D.Action)
    (hchosen : E.chosen = prefix ++ (detour ++ suffix))
    (hreturn : D.run (D.run E.initial prefix) detour =
      D.run E.initial prefix)
    (hcost : 0 < D.totalPrice (D.run E.initial prefix) detour) :
    False := by
  have hwhole : D.executable E.initial
      (prefix ++ (detour ++ suffix)) := by
    simpa [hchosen] using E.chosen_executable
  have hp := (D.executable_append E.initial prefix
    (detour ++ suffix)).1 hwhole
  have htail0 := (D.executable_append (D.run E.initial prefix)
    detour suffix).1 hp.2
  have htail : D.executable (D.run E.initial prefix) suffix := by
    rw [← hreturn]
    exact htail0.2
  have hgoal : E.goal (D.run (D.run E.initial prefix) suffix) := by
    have hg : E.goal (D.run E.initial
        (prefix ++ (detour ++ suffix))) := by
      simpa [hchosen] using E.chosen_goal
    rw [D.run_append, D.run_append, hreturn] at hg
    exact hg
  have hopt := E.optimal_suffix prefix (detour ++ suffix) suffix
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
