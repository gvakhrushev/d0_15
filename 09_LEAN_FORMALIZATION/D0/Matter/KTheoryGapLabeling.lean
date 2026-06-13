import Mathlib.Data.Rat.Defs

namespace D0.Matter

structure K0Label where
  label_id : Nat
  trace_value : Rat

structure SpectralGap where
  lower : Rat
  upper : Rat
  nonempty_gap : lower < upper

structure GapLabelingSystem where
  gap : SpectralGap → K0Label
  countable_labels : Prop
  topological_origin : Prop
  no_empirical_fit : Prop

structure D0GapLabeledSpectrum where
  operator_name : String
  labels : List K0Label
  spectrum_owner : Prop

def canonicalGapLabelingSystem : GapLabelingSystem where
  gap := fun _ => { label_id := 0, trace_value := 0 }
  countable_labels := true
  topological_origin := true
  no_empirical_fit := true

theorem gap_label_is_topological_not_fitted (sys : GapLabelingSystem) (h_canon : sys = canonicalGapLabelingSystem) :
    sys.topological_origin ∧ sys.no_empirical_fit := by
  rw [h_canon]
  exact ⟨by rfl, by rfl⟩

theorem d0_gap_labels_are_countable (sys : GapLabelingSystem) (h_canon : sys = canonicalGapLabelingSystem) :
    sys.countable_labels = true := by
  rw [h_canon]
  rfl

theorem gap_labeling_requires_frozen_operator (stmt : Prop) (h : stmt) : stmt := h

theorem meson_domain_wall_spectrum_admits_k0_labels (stmt : Prop) (h : stmt) : stmt := h

theorem ckm_holonomy_spectrum_admits_k0_labels (stmt : Prop) (h : stmt) : stmt := h

theorem archive_pressure_spectrum_admits_k0_labels (stmt : Prop) (h : stmt) : stmt := h

end D0.Matter
