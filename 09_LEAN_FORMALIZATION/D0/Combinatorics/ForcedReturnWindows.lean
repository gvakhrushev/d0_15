import D0.Combinatorics.PhaseUnfolding

namespace D0

theorem forced_return_window_summary :
    qT = 44 ∧ d13 = 20 ∧ qEW = 710 ∧ DEW = 35 := by
  exact ⟨lcm_abcd_v11, d13_from_return_window, qEW_forced, ew_depth_from_omega8⟩

theorem half_window_355_fails_full_orientation : 355 ≠ qEW := by
  rw [qEW_forced]
  norm_num

theorem window_568_fails_pointed_requirement : 568 ≠ qEW := by
  rw [qEW_forced]
  norm_num

end D0
