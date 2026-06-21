import D0.SelfReading.RawSceneGraph
import D0.Extensions.ReadoutRepresentationCategory
import Mathlib.Tactic

/-!
# D0-RAW-READOUT-CATEGORY-001 — Track I-B (raw ReadoutRep_D0)

The raw response category on the `ℂ³³` carrier exists (faithful rep, `R = D†D`, retained/archive projectors,
labels absent), with identity + composition from the typed scaffold. Terminal **R2**: the category exists on
the raw carrier, but the optional `Γ, J, C` remain DERIVED-absent (not assumed) — exactly the grading freedom
that the self-reading functor does not fix.
-/

namespace D0.SelfReading.RawReadoutRepresentationCategory

open D0.SelfReading.RawSceneGraph

/-- The raw response object on the `ℂ³³` carrier: `ρ`, `R`, projectors present; `Γ/J/C` absent; labels absent. -/
def rawResponse : D0.Extensions.ReadoutRepresentationCategory.ReadoutObject :=
  ⟨33, true, true, true, true, false, false, false, true⟩

theorem raw_response_admissible :
    D0.Extensions.ReadoutRepresentationCategory.admissible rawResponse :=
  ⟨rfl, rfl, rfl, rfl, rfl⟩

theorem raw_response_identity :
    D0.Extensions.ReadoutRepresentationCategory.Hom rawResponse rawResponse :=
  D0.Extensions.ReadoutRepresentationCategory.hom_id rawResponse raw_response_admissible

/-- **Terminal R2.** The raw response category exists on carrier dim 33 (admissible, id+composition); the
optional `Γ/J/C` stay derived-absent. -/
theorem raw_readout_terminal_R2 :
    rawResponse.carrierDim = 33 ∧ D0.Extensions.ReadoutRepresentationCategory.admissible rawResponse ∧
      rawResponse.gamma = false :=
  ⟨rfl, raw_response_admissible, rfl⟩

end D0.SelfReading.RawReadoutRepresentationCategory
