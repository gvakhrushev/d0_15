import D0.Dynamics.InternalFeedbackResolvent
import D0.Cosmology.FeedbackPartitionFunction
import D0.Cosmology.FiniteFeedbackEquationOfState
import D0.Matter.TerminalFeedbackModes
import D0.Gravity.PressureCapacityBalance
import D0.Cosmology.SDEFeedbackReduction

/-!
Fast theorem-ledger slice for the closed vacuum feedback thermodynamics package.

This index is intentionally narrow: it lets the CVFT package be checked without
rebuilding the monolithic hard-closure index.
-/

#check D0.Dynamics.feedback_slots_positive
#check D0.Dynamics.internal_feedback_forced_by_split
#check D0.Dynamics.internal_feedback_resolvent_series
#check D0.Dynamics.external_mirror_model_forbidden

#check D0.Cosmology.return_cycle_depth_card
#check D0.Cosmology.feedback_determinant_return_cycles
#check D0.Cosmology.feedback_variation_universal_source

#check D0.Cosmology.feedback_pressure_trace_log
#check D0.Cosmology.finite_pvt_equation_of_state
#check D0.Cosmology.ideal_gas_core_postulate_forbidden

#check D0.Matter.terminal_feedback_mode_criterion
#check D0.Matter.matter_as_arbitrary_eigenvalue_forbidden
#check D0.Matter.higgs_as_rank2_feedback_subspace
#check D0.Matter.meson_domain_wall_feedback_stretch
#check D0.Matter.baryon_s3_stabilized_feedback_modes

#check D0.Gravity.pressure_capacity_balance_regimes
#check D0.Gravity.horizon_saturation_feedback_limit
#check D0.Gravity.a4_terminal_feedback_saturation

#check D0.Cosmology.sde_two_mode_feedback_reduction
#check D0.Cosmology.desi_sparc_failure_forces_boundary_derivative_feedback
#check D0.Cosmology.arbitrary_kernel_repair_not_theorem_grade
#check D0.Cosmology.desi_sparc_failure_boundary_feedback_diagnosis
#check D0.Cosmology.desi_root_refit_repair_forbidden
#check D0.Cosmology.desi_window_refit_repair_forbidden
