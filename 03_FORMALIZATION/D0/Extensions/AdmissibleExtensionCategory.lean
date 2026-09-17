import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic

/-!
# D0AdmissibleExtension — the typed beyond-present-core extension category (Section 1)

An extension object is a PARTIAL tuple over the five components `(R_rep, H_ref, P_arch, B_branch, A_res)`
(each may be absent), together with the inadmissibility flags. The category supports partial objects (any of
the `2⁵ = 32` component-configurations), admissibility is `no-manual-data ∧ no-post-hoc-choice`, and morphisms
are component-inclusions of admissible objects (a refinement order with identity + composition). An object is
rejected if it uses a manual basis/labels/window/redshift-anchor/scale, any PDG/Planck/DESI/LIGO datum, or a
post-hoc choice after seeing an observable.
-/

namespace D0.Extensions.AdmissibleExtensionCategory

/-- The five extension components. -/
inductive Component
  | R_rep      -- finite representation / readout extension      (E1)
  | H_ref      -- history / refinement functor                   (E2)
  | P_arch     -- archive pressure-energy observable             (E3)
  | B_branch   -- branch-sensitive selector                      (E4)
  | A_res      -- profinite analytic residue realization         (E5)
  deriving DecidableEq, Repr, Fintype

/-- A (partial) extension object: a subset of the five components plus the inadmissibility flags. -/
structure ExtObject where
  components : Finset Component
  usesManualData : Bool   -- manual basis/labels/window/anchor/scale OR PDG/Planck/DESI/LIGO
  postHocChoice : Bool    -- a choice made after seeing an observable

/-- Admissibility: no manual data and no post-hoc choice. -/
def ExtObject.admissible (E : ExtObject) : Prop := E.usesManualData = false ∧ E.postHocChoice = false

/-- Morphism: a component-inclusion (refinement) between admissible objects. -/
def Hom (E F : ExtObject) : Prop := E.admissible ∧ F.admissible ∧ E.components ⊆ F.components

/-- Exactly five component types. -/
theorem five_components : Fintype.card Component = 5 := by decide

/-- Partial-object support: exactly `2⁵ = 32` component-configurations. -/
theorem partial_object_configs : (Finset.univ : Finset Component).powerset.card = 32 := by decide

/-- The empty extension is admissible. -/
theorem empty_admissible : ExtObject.admissible ⟨∅, false, false⟩ := ⟨rfl, rfl⟩

/-- A manual-data object is never admissible (rejected). -/
theorem manual_data_rejected (c : Finset Component) (ph : Bool) :
    ¬ ExtObject.admissible ⟨c, true, ph⟩ := by
  rintro ⟨h, _⟩; exact Bool.noConfusion h

/-- A post-hoc-choice object is never admissible (rejected). -/
theorem post_hoc_rejected (c : Finset Component) (md : Bool) :
    ¬ ExtObject.admissible ⟨c, md, true⟩ := by
  rintro ⟨_, h⟩; exact Bool.noConfusion h

/-- `Hom` is reflexive on admissible objects (identity morphism). -/
theorem hom_id (E : ExtObject) (h : E.admissible) : Hom E E := ⟨h, h, Finset.Subset.refl _⟩

/-- `Hom` composes (the refinement order is transitive). -/
theorem hom_comp {E F G : ExtObject} (h₁ : Hom E F) (h₂ : Hom F G) : Hom E G :=
  ⟨h₁.1, h₂.2.1, Finset.Subset.trans h₁.2.2 h₂.2.2⟩

/-- **D0AdmissibleExtension is a well-formed partial-object category**: 5 components, 32 partial
configurations, admissibility rejects manual data and post-hoc choice, and `Hom` has identity + composition. -/
theorem admissible_extension_category :
    Fintype.card Component = 5 ∧
    (Finset.univ : Finset Component).powerset.card = 32 ∧
    ExtObject.admissible ⟨∅, false, false⟩ ∧
    (∀ c ph, ¬ ExtObject.admissible ⟨c, true, ph⟩) :=
  ⟨five_components, partial_object_configs, empty_admissible, manual_data_rejected⟩

end D0.Extensions.AdmissibleExtensionCategory
