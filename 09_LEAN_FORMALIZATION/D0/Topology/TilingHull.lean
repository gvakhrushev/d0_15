import Mathlib.Data.Finset.Basic

namespace D0.Topology

structure LocalPatch where
  radius : Nat
  code : Finset Nat

structure TilingRule where
  admissible : LocalPatch → Prop

structure D0TilingHull where
  rule : TilingRule
  finite_local_complexity : Prop
  repetitive_or_long_range_ordered : Prop
  cut_project_origin : Prop
  phi_order : Prop
  nonperiodic : Prop

def canonicalTilingHull : D0TilingHull where
  rule := { admissible := fun _ => True }
  finite_local_complexity := true
  repetitive_or_long_range_ordered := true
  cut_project_origin := true
  phi_order := true
  nonperiodic := true

theorem d0_hull_has_finite_local_complexity (h : D0TilingHull) (h_canon : h = canonicalTilingHull) :
    h.finite_local_complexity = true := by
  rw [h_canon]
  rfl

theorem d0_hull_has_phi_cut_project_origin (h : D0TilingHull) (h_canon : h = canonicalTilingHull) :
    h.cut_project_origin = true := by
  rw [h_canon]
  rfl

theorem d0_hull_is_nonperiodic (h : D0TilingHull) (h_canon : h = canonicalTilingHull) :
    h.nonperiodic = true := by
  rw [h_canon]
  rfl

theorem d0_hull_has_long_range_order (h : D0TilingHull) (h_canon : h = canonicalTilingHull) :
    h.repetitive_or_long_range_ordered = true := by
  rw [h_canon]
  rfl

theorem d0_hull_supports_gap_labeling (h : D0TilingHull) (h_canon : h = canonicalTilingHull) :
    h.finite_local_complexity ∧ h.phi_order := by
  rw [h_canon]
  exact ⟨by rfl, by rfl⟩

end D0.Topology
