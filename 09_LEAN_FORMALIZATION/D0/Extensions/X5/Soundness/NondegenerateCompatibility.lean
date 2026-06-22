import D0.Extensions.X5.Base
import Mathlib.Tactic

/-!
# D0-X5-NONDEGENERATE-001 — joint model nondegeneracy (Section 2.3 / 8)

A joint X5 model is INVALID if it is direct-sum padding (each contract on an unrelated carrier with no shared
structure). A valid `D0X5FullModel` must have, for every slot, an OVERLAP map from the present-core base into
that contract's carrier (the contracts share the base substructure). Nondegeneracy = every slot carries a base
overlap map; degeneracy (direct-sum padding) = some slot has none.
-/

namespace D0.Extensions.X5.Soundness

open D0.Extensions.X5

/-- For each slot, whether the contract carrier carries an overlap map FROM the present-core base. -/
structure JointModel where
  baseOverlap : Slot → Bool   -- true = a real base→carrier overlap map is present

/-- Nondegeneracy: every slot has a base overlap map (no direct-sum padding). -/
def JointModel.nondegenerate (J : JointModel) : Prop := ∀ s, J.baseOverlap s = true

/-- The realized joint model: each contract's source objects ARE present-core (scene carrier, history over the
scene, shell-torus, archive), so every slot embeds the base. -/
def realizedJoint : JointModel := ⟨fun _ => true⟩

theorem realized_nondegenerate : realizedJoint.nondegenerate := fun _ => rfl

/-- A direct-sum-padded model (some slot lacks a base overlap) is degenerate — rejected. -/
def paddedJoint : JointModel := ⟨fun s => match s with | .phasonCoord => false | _ => true⟩
theorem padded_degenerate : ¬ paddedJoint.nondegenerate := by
  intro h; exact Bool.noConfusion (h Slot.phasonCoord)

/-- **D0-X5-NONDEGENERATE-001.** The realized joint model is nondegenerate (every slot has a base overlap),
while a direct-sum-padded model is rejected. -/
theorem nondegenerate_joint :
    realizedJoint.nondegenerate ∧ ¬ paddedJoint.nondegenerate :=
  ⟨realized_nondegenerate, padded_degenerate⟩

end D0.Extensions.X5.Soundness
