import Mathlib.Tactic

/-!
# D0-X5-SOUNDNESS-SCHEMA-001 — claim-mode + relative-theorem discipline (Section 1)

A postulated primitive is NOT a CERT-CLOSED owner: it carries `claim_mode = X5_POSTULATED_CONTRACT` and
`present_core_derived = false`. Only interface/model/deletion/compatibility META-facts are CERT-CLOSED. An
X5-relative theorem must declare a NON-EMPTY `dependsOn`; a theorem with empty `dependsOn` is present-core (and
an X5 consequence claimed with empty deps must fail validation).
-/

namespace D0.Extensions.X5.Soundness

/-- Claim modes (the controlled set used by the X5 registry). -/
inductive ClaimMode
  | X5_POSTULATED_CONTRACT   -- the primitive itself (HYP-intent)
  | X5_INTERFACE_CERT        -- interface/model/deletion/compatibility (CERT-CLOSED-eligible)
  | X5_RELATIVE_THEOREM      -- THE relative to named contracts
  | PRESENT_CORE             -- frozen present-core (no X5 dependency)
  deriving DecidableEq, Repr

/-- A relative theorem: an id + the contracts it consumes. -/
structure RelativeTheorem where
  id : String
  dependsOn : List String
  deriving Repr

/-- A theorem is X5-relative iff it declares at least one consumed contract. -/
abbrev RelativeTheorem.isX5Relative (t : RelativeTheorem) : Prop := t.dependsOn ≠ []

/-- A postulated contract is never `present_core_derived`. -/
def ClaimMode.presentCoreDerived : ClaimMode → Bool
  | .PRESENT_CORE => true
  | _ => false

theorem postulate_not_present_core :
    ClaimMode.presentCoreDerived ClaimMode.X5_POSTULATED_CONTRACT = false := rfl

/-- **A theorem with empty `dependsOn` is NOT X5-relative** (it would be present-core). -/
theorem empty_deps_not_relative (t : RelativeTheorem) (h : t.dependsOn = []) :
    ¬ t.isX5Relative := by simp [RelativeTheorem.isX5Relative, h]

/-- An example X5-relative theorem (`N_active` candidate-sector dim depends on `X5-G`). -/
def exampleRelative : RelativeTheorem := ⟨"X5-G-candidate-sector-dim", ["X5-G"]⟩
theorem example_is_relative : exampleRelative.isX5Relative := by decide

end D0.Extensions.X5.Soundness
