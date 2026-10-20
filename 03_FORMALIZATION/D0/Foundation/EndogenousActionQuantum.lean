import Mathlib.Tactic
import D0.Foundation.VerifiabilityNecessity
import D0.Foundation.PopperianBootstrap

/-!
# Endogenous action quantum: M1-forced discrete action scale S_min = 1

Formalizes the abstract transition-action threshold and its remaining interface boundary for the
metric underdetermination frontier (`D0-MASS-SECTOR-METRIC-UNDERDETERMINATION-001` and
`D0-REDSHIFT-SI-TICK-CALIBRATION-NOGO-001`).

Extrinsic continuous standards (seconds, meters, electron-volts) are arbitrary historical conventions.
Inside the abstract verification protocol, the action threshold is fixed by the operational requirement
that distinguishable state transitions require at least one unit of information-distinguishability
action. Its realization on native D0 field histories remains a separate, unproved bridge.

Theorems in this module:
* `ActionProtocol` — an action assignment over an admissible verification protocol.
* `endogenous_action_quantum_pos` — the endogenous action quantum is strictly positive.
* `endogenous_action_quantum_minimal` — S_min = 1 is the lower bound for every non-trivial transition
  admitted by `ActionProtocol`.
* `action_protocol_has_nonscaling_completions` — the protocol constraints do not determine a
  transition-cost profile, even modulo one overall positive scale, on a three-state carrier.
* `no_degree_two_homogeneous_action_protocol` — a degree-two homogeneous cost on any nontrivial
  real vector carrier cannot obey the protocol's unit lower bound on every nonzero transition.
* `subquantum_collapse` — an operational detector with unit distinguishability
  threshold cannot distinguish any sub-quantum transition (0 < S < 1) without losing record injectivity.
* `relative_action_scale_invariant` — the ratio of two physical actions is strictly invariant under any
  extrinsic positive rescaling of units (e.g. SI scaling ħ_ext > 0).
* `action_distinction_forcing` — any distinguishable state transition carries strictly positive action.
-/

namespace D0.Foundation.EndogenousActionQuantum

open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.PopperianBootstrap

/-- The canonical endogenous action quantum is 1. -/
def S_min : ℝ := 1

/-- An action assignment over a verification protocol `P`. -/
@[ext]
structure ActionProtocol (P : VerificationProtocol) where
  /-- Action cost of a transition between two states. -/
  action : P.State → P.State → ℝ
  /-- Identity transitions cost zero action. -/
  action_refl : ∀ x, action x x = 0
  /-- Non-trivial transitions cost at least the endogenous action quantum S_min = 1. -/
  action_nontrivial : ∀ x y, x ≠ y → 1 ≤ action x y

/-- The exact free data left by `ActionProtocol`: an independent nonnegative excess on
each ordered non-identity transition. -/
@[ext]
structure ActionExcessProfile (P : VerificationProtocol) where
  excess : P.State → P.State → ℝ
  excess_refl : ∀ x, excess x x = 0
  excess_nontrivial : ∀ x y, x ≠ y → 0 ≤ excess x y

/-- Extract the amount above the forced unit floor on every non-identity transition. -/
def actionExcessOf {P : VerificationProtocol} (A : ActionProtocol P) :
    ActionExcessProfile P where
  excess x y := if x = y then 0 else A.action x y - S_min
  excess_refl := by intro x; simp
  excess_nontrivial := by
    intro x y hxy
    simp [hxy]
    have h := A.action_nontrivial x y hxy
    unfold S_min at h ⊢
    linarith

/-- Reconstruct an action protocol from an arbitrary admissible excess profile. -/
def actionProtocolOfExcess {P : VerificationProtocol} (E : ActionExcessProfile P) :
    ActionProtocol P where
  action x y := if x = y then 0 else S_min + E.excess x y
  action_refl := by intro x; simp
  action_nontrivial := by
    intro x y hxy
    simp [hxy, S_min]
    exact E.excess_nontrivial x y hxy

/-- Every protocol is exactly its unit floor plus its extracted excess profile. -/
theorem actionProtocol_excess_reconstruction {P : VerificationProtocol}
    (A : ActionProtocol P) (x y : P.State) :
    (actionProtocolOfExcess (actionExcessOf A)).action x y = A.action x y := by
  by_cases hxy : x = y
  · subst y
    simp [actionProtocolOfExcess, actionExcessOf, S_min, A.action_refl]
  · simp [actionProtocolOfExcess, actionExcessOf, S_min, hxy]

/-- Every admissible excess profile is recovered after reconstruction. -/
theorem actionExcessOf_reconstruction {P : VerificationProtocol}
    (E : ActionExcessProfile P) (x y : P.State) :
    (actionExcessOf (actionProtocolOfExcess E)).excess x y = E.excess x y := by
  by_cases hxy : x = y
  · subst y
    simp [actionExcessOf, actionProtocolOfExcess, E.excess_refl]
  · simp [actionExcessOf, actionProtocolOfExcess, S_min, hxy]

/-- Exact classification of the full `ActionProtocol` fiber. It has no symmetry,
composition, refinement, or field-source constraint beyond the unit floor. -/
def actionProtocolExcessEquiv {P : VerificationProtocol} :
    ActionProtocol P ≃ ActionExcessProfile P where
  toFun := actionExcessOf
  invFun := actionProtocolOfExcess
  left_inv := by
    intro A
    ext x y
    exact actionProtocol_excess_reconstruction A x y
  right_inv := by
    intro E
    ext x y
    exact actionExcessOf_reconstruction E x y

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

/-- A second symmetric completion that raises the cost of every transition incident to `a`.
The protocol itself has no axiom forbidding this state dependence. -/
def markedActionProtocol (P : VerificationProtocol) (a : P.State) : ActionProtocol P where
  action := fun x y => if x = y then 0 else if x = a ∨ y = a then 2 else 1
  action_refl := by intro x; simp
  action_nontrivial := by
    intro x y hxy
    by_cases hmark : x = a ∨ y = a <;> simp [hxy, hmark]

/-- On any protocol with three distinct states, the two admissible costs above cannot be
identified by an overall action-scale calibration. Thus the `ActionProtocol` fields alone do not
determine transition-cost ratios uniquely; this is an interface result, not a physical admission
theorem for a D0 carrier. -/
theorem action_protocol_has_nonscaling_completions {P : VerificationProtocol}
    (a b c : P.State) (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    ¬ ∃ s : ℝ, 0 < s ∧
      ∀ x y : P.State,
        (markedActionProtocol P a).action x y = s * (canonicalActionProtocol P).action x y := by
  rintro ⟨s, _hs, hsame⟩
  have hbase : (1 : ℝ) = s := by
    simpa [markedActionProtocol, canonicalActionProtocol, hbc,
      Ne.symm hab, Ne.symm hac] using hsame b c
  have hmarked : (2 : ℝ) = s := by
    simpa [markedActionProtocol, canonicalActionProtocol, hab] using hsame a b
  linarith

/-- A uniformly doubled admissible completion shows that the lower bound `S_min = 1` need not
be attained by every action protocol. Attainment is witnessed by `canonicalActionProtocol`, not
forced for an arbitrary inhabitant of `ActionProtocol`. -/
def doubledActionProtocol (P : VerificationProtocol) : ActionProtocol P where
  action := fun x y => if x = y then 0 else 2
  action_refl := by intro x; simp
  action_nontrivial := by intro x y hxy; simp [hxy]

theorem doubledActionProtocol_never_attains_S_min {P : VerificationProtocol}
    (x y : P.State) (hxy : x ≠ y) :
    (doubledActionProtocol P).action x y ≠ S_min := by
  simp [doubledActionProtocol, S_min, hxy]

/-- A degree-two homogeneous cost on a divisible real vector carrier cannot satisfy the unit
lower bound on every nonzero transition. Starting from any nonzero direction `v`, the rescaling
`v ↦ v / (Q(v) + 1)` remains nonzero and has cost below one. Thus the abstract `ActionProtocol`
cannot be applied directly to all pointwise field variations with their quadratic action; a
discrete event-to-field map is required. This is a scope theorem, not a no-go for discrete native
histories. -/
theorem no_degree_two_homogeneous_action_protocol
    {V : Type*} [AddCommGroup V] [Module ℝ V]
    (Q : V → ℝ) (hQ : ∀ t v, Q (t • v) = t ^ 2 * Q v)
    (v₀ : V) (hv₀ : v₀ ≠ 0) :
    ¬ ∀ v : V, v ≠ 0 → 1 ≤ Q v := by
  intro hfloor
  have hbase : 1 ≤ Q v₀ := hfloor v₀ hv₀
  let t : ℝ := 1 / (Q v₀ + 1)
  have htpos : 0 < t := by
    dsimp [t]
    positivity
  have htne : t ≠ 0 := ne_of_gt htpos
  have hscaled_ne : t • v₀ ≠ 0 := smul_ne_zero htne hv₀
  have hsmall : Q (t • v₀) < 1 := by
    rw [hQ]
    dsimp [t]
    have hden : Q v₀ + 1 ≠ 0 := by linarith
    field_simp [hden]
    nlinarith [sq_nonneg (Q v₀)]
  have hlarge : 1 ≤ Q (t • v₀) := hfloor (t • v₀) hscaled_ne
  linarith

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

end D0.Foundation.EndogenousActionQuantum
