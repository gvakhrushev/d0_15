# NO-GO: Pi0 Branch-Defect Physical Generation Clustering

The projective branch-defect generation index is Lean-proved as exactly three.

This no-go file records the remaining limitation: physical mass/Yukawa hierarchy or PDG clustering does not follow from the projective index alone.

{
  "negative_controls": {
    "perturb_6_5_changes_pi0_defect": true,
    "remove_gap_loses_third_ray": true,
    "replace_phi_by_sqrt2_breaks_branch_normalization": true,
    "replace_pi0_by_pi_kills_phase_defect": true
  },
  "projective_checks": {
    "action_eGap_to_ePlus": true,
    "action_eMinus_to_eGap": true,
    "action_ePlus_to_eMinus": true,
    "action_order_three_on_nonzero_rays": true,
    "f2_nonzero_projective_ray_count_eq_3": true,
    "gap_ray_is_sum_of_plus_and_minus": true
  },
  "real_lift_checks": {
    "branchGap_eq_two_delta0": true,
    "deltaPi_nonzero_against_smooth_pi": true,
    "pPlus_add_pMinus_eq_one": true,
    "pi0_positive": true,
    "tau0_eq_two_pi0": true
  },
  "scope_guardrail": "Core generation index is projective branch-defect cardinality. Physical masses/Yukawa hierarchy/clustering are not certified here.",
  "status": "PASS_PI0_BRANCH_DEFECT_PROJECTIVE_GENERATION",
  "values": {
    "branchGap": 0.23606797749978964,
    "delta0": 0.11803398874989482,
    "deltaPi": 4.813291008076703e-05,
    "orbit_ePlus": [
      [
        1,
        0
      ],
      [
        0,
        1
      ],
      [
        1,
        1
      ],
      [
        1,
        0
      ]
    ],
    "pMinus": 0.38196601125010515,
    "pPlus": 0.6180339887498948,
    "phi": 1.618033988749895,
    "pi0": 3.141640786499874,
    "tau0": 6.283281572999748
  }
}
