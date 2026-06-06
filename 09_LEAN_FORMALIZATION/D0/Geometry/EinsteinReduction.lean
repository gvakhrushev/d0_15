import D0.Geometry.HeatTraceConditions

namespace D0

def EinsteinReductionClosedFromD0 : Prop := False

theorem Einstein_reduction_not_closed_from_current_D0_objects :
    ¬ EinsteinReductionClosedFromD0 := by
  intro h
  exact h

theorem Einstein_sample_window_no_go :
    ∃ A B : WindowTower,
      sampleWindowEvidence A ∧ sampleWindowEvidence B ∧ A 2 ≠ B 2 :=
  sample_windows_do_not_determine_infinite_tower

end D0

