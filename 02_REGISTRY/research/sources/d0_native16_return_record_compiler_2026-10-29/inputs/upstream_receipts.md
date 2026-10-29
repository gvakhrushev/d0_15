### 9. Frozen changed code and actual receipt
<!-- BEGIN 7dr RETAINED REPORT FIBRE RECEIPT -->
```json
{
  "approximate_graph": {
    "noncommuting_rational_control": true,
    "operator_gradient_defect_bound": "(zeta/a)*(1/2+2mu)*(1+2zeta/a)*epsilon",
    "trace_direction_bound": "r times operator-gradient bound times ||D C||op; r is actual protected input rank"
  },
  "boundary": {
    "active_dimension": 128,
    "active_wires": [
      0,
      6,
      10,
      11,
      12,
      13,
      14
    ],
    "actual_blanks": 12,
    "full_dimension": 65536,
    "full_wires": 16,
    "input_spectator": 2,
    "live_query_wire": 11,
    "old_copy_wire": 12,
    "rank_input": 16,
    "retained_new_report_wire": 10,
    "thermal_spectator": 512,
    "unknown": [
      6,
      13,
      14,
      15
    ]
  },
  "checker_sha256": "d5c987f4cec9d1de7aa2b3d35bc6bed9d0d7fa1e8ff56ceb49a9a5164954d99f",
  "checks": 288,
  "exact_fixed_report_B_high_minus_low_interval": [
    "0.000004452457504183996824985687210400961068",
    "0.000004452457504183996824985687210400961071"
  ],
  "input_commit": "b728d85246c6bcf75b84dadaef294e91f5f50b15",
  "input_pins": {
    "d0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md": "1db9ebd3d24b57a45b1a3a00a2c2553c2e08019cecc34d18e2e2a94d19b45254",
    "d0_canonical_stationary_family_2026-10-28/PROOF_RU.md": "fe4b8e9033098ced52299fbc0481ab2ddecceed69c6f4392988803ab0abfa005",
    "d0_clock_winding_source_2026-10-28/PROOF_RU.md": "ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418",
    "d0_task_faithful_source_2026-10-28/PROOF_RU.md": "9f2354817860f9024a597dba4bd14c0580cc021de5c473925740b46b0e8f96e5"
  },
  "inventories": {
    "completed16": {
      "CX": 9,
      "G": 1,
      "SourceI": 6
    },
    "high27": {
      "CX": 14,
      "G": 3,
      "SourceI": 10
    },
    "low27": {
      "CX": 14,
      "G": 3,
      "SourceI": 10
    },
    "recorded32": {
      "CX": 20,
      "G": 2,
      "SourceI": 10
    },
    "unrecorded31": {
      "CX": 19,
      "G": 2,
      "SourceI": 10
    }
  },
  "literal_words": {
    "completed16": [
      {
        "op": "CX",
        "wires": [
          6,
          12
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          10
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "G",
        "wires": [
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          10
        ]
      }
    ],
    "high27": [
      {
        "op": "CX",
        "wires": [
          6,
          12
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "G",
        "wires": [
          0
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          10
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "G",
        "wires": [
          11
        ]
      },
      {
        "op": "G",
        "wires": [
          11
        ]
      }
    ],
    "low27": [
      {
        "op": "CX",
        "wires": [
          6,
          12
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "G",
        "wires": [
          0
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          10
        ]
      },
      {
        "op": "G",
        "wires": [
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "G",
        "wires": [
          11
        ]
      }
    ],
    "recorded32": [
      {
        "op": "CX",
        "wires": [
          6,
          12
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "G",
        "wires": [
          0
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          10
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "G",
        "wires": [
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      }
    ],
    "unrecorded31": [
      {
        "op": "CX",
        "wires": [
          6,
          12
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "G",
        "wires": [
          0
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "SourceI",
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "G",
        "wires": [
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      },
      {
        "op": "CX",
        "wires": [
          11,
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          0,
          11
        ]
      }
    ]
  },
  "native_full_source_completion": {
    "actual_generated_prefix_cuts_verified": true,
    "actual_joint_effect": "p Q_return",
    "actual_native_G_source_interval": [
      "0.000007413764171516666215979814570577698644",
      "0.000007413764171516666215979814570577698647"
    ],
    "all16_occurrence_sources_equal_observable_pullback": true,
    "all_endpoint_source_equals_observable_pullback": true,
    "full_B_global_minimum_not_proved": true,
    "full_H_first_source_zero_on_every_endpoint_unitary_tangent": true,
    "full_signature": {
      "+1": 32768,
      "-1": 32768
    },
    "joint_observable": "record10=0 AND seed-copy12=0",
    "literal_word": "completed16",
    "native_G_stage": 15,
    "positive_return_gap_exact_zero": true,
    "recorded32_unsaturated_gap": "p^3 Q_return",
    "return_minimum_at_fixed_joint_effect": true,
    "same_clock_as_low27": false,
    "same_entire_initialized_work_isometry_as": "low27",
    "same_joint_effect_as_recorded32": true,
    "source_equivalent_positive_ratio_interval": [
      "1.059016426469788682156510786578844100404686",
      "1.059016426469788682156510786578844100404689"
    ],
    "stationarity_does_not_require_linked_inverse_legs": true,
    "stationary_on_every_fixed_joint_record_effect_tangent": true,
    "unrestricted_source_not_zero": true
  },
  "nonscalar_recording": {
    "new_prefix_criterion": "[C,Q_return]=0 for Hermitian contraction C",
    "old_C_squared_criterion_alone_insufficient": true
  },
  "pair_future_charpoly": "(lambda^2-1)(lambda^2-2sqrt(p)lambda+1)",
  "price_comparison_heat_exact_equal": true,
  "recorded32_signature": {
    "+1": 40960,
    "-1": 24576
  },
  "remaining": {
    "GR_closed": false,
    "all42_physical_source_and_refinement": false,
    "autonomous_controller_admission": false,
    "full_physical_variation_domain": false,
    "full_selected_Cost_Info_binding": false
  },
  "retained_report": {
    "all64_SOURCE_columns_with_actual_record_blank_match_middle_test": true,
    "all_initial16_event_effect": "p^2 I16",
    "new_memory_not_erased": true,
    "same_entire_other15_wire_output_channel_for_27_pair": true,
    "same_every_possible_future_context": false
  },
  "runtime": {
    "mpmath": "1.3.0",
    "python": "3.9.6",
    "sympy": "1.14.0"
  },
  "scope": "same actual retained report and full old archive, full fixed INTERNAL Book H+J; no unconditional physical X_N or GR closure",
  "source": {
    "actual_recorded_w_interval": [
      "0.000002914171114976538947145560430803361082",
      "0.000002914171114976538947145560430803361085"
    ],
    "exact_graph_gain_ratio_interval": [
      "1.309016587107152976983759489433395872021148",
      "1.309016587107152976983759489433395872021151"
    ],
    "finite_difference_error": "3.0546388785485305263510796912999557e-34",
    "new_gain": "8 zeta ((1+c)/2)^2/(1-zeta+zeta ((1+c)/2)^2)",
    "nonzero_readback_source_interval": [
      "0.000004581959274119384956134264232057826308",
      "0.000004581959274119384956134264232057826311"
    ],
    "old_five_rows_exact_zero": [
      1,
      2,
      3,
      4,
      5
    ],
    "old_gain": "8 zeta c^2/(1-zeta+zeta c^2)",
    "old_w_interval": [
      "0.000000425171967968631731746184594007985737",
      "0.000000425171967968631731746184594007985740"
    ],
    "paid_final_G_stage": 29,
    "same_all_other15_wire_task_tangent": true,
    "whole_heat_first_row_zero_at_recorded32": true
  },
  "status": "PASS",
  "whole_book": {
    "completed16": {
      "B_interval": [
        "25.957207927733290053290929316678906624665135",
        "25.957207927733290053290929316678926754888222"
      ],
      "H_interval": [
        "25.957197384165192693158973083714237681473207",
        "25.957197384165192693158973083714257811696295"
      ],
      "J_interval": [
        "0.000010543568097360131956232964668943191926",
        "0.000010543568097360131956232964668943191929"
      ],
      "N": 16,
      "all_modes": 445644800,
      "unpaired_harmonic_modes": 376438784
    },
    "high27": {
      "B_interval": [
        "26.642153092653733033685012440914836077292507",
        "26.642153092653733033685012440914856207076983"
      ],
      "H_interval": [
        "26.642138096628131489556231222262956733139510",
        "26.642138096628131489556231222262976862923986"
      ],
      "J_interval": [
        "0.000014996025601544128781218651879344152995",
        "0.000014996025601544128781218651879344152998"
      ],
      "N": 27,
      "all_modes": 752025600,
      "unpaired_harmonic_modes": 635240448
    },
    "low27": {
      "B_interval": [
        "26.642148640196228849688187455227625676331437",
        "26.642148640196228849688187455227645806115914"
      ],
      "H_interval": [
        "26.642138096628131489556231222262956733139510",
        "26.642138096628131489556231222262976862923986"
      ],
      "J_interval": [
        "0.000010543568097360131956232964668943191926",
        "0.000010543568097360131956232964668943191929"
      ],
      "N": 27,
      "all_modes": 752025600,
      "unpaired_harmonic_modes": 635240448
    },
    "recorded32": {
      "B_interval": [
        "26.864551167745933999763248200820458123626354",
        "26.864551167745933999763248200820478253410830"
      ],
      "H_interval": [
        "26.864538823121241288771436932202650288941689",
        "26.864538823121241288771436932202670418726165"
      ],
      "J_interval": [
        "0.000012344624692710991811268617807834684664",
        "0.000012344624692710991811268617807834684667"
      ],
      "N": 32,
      "all_modes": 891289600,
      "unpaired_harmonic_modes": 752877568
    },
    "unrecorded31": {
      "B_interval": [
        "26.822994071102531619335475533937872207246315",
        "26.822994071102531619335475533937892337030791"
      ],
      "H_interval": [
        "26.822979237478172423927638227688336408055675",
        "26.822979237478172423927638227688356537840151"
      ],
      "J_interval": [
        "0.000014833624359195407837306249535799190638",
        "0.000014833624359195407837306249535799190641"
      ],
      "N": 31,
      "all_modes": 863436800,
      "unpaired_harmonic_modes": 729350144
    }
  },
  "word_sha256": {
    "completed16": "22a52553e0f6ffe294a5f52bd3b6ee15999db9d2d9cc9aa2ba58bc34438bc97d",
    "high27": "486284df113400ba1c9b3248eb08f45f76c124d4aab0b208f317a5b462dbe5ac",
    "low27": "249e1d54e7240eb730c728291b11fc1b26371de88bc236ed5a104b87764c19de",
    "recorded32": "d70d6bee5dc82137058d64e351eabc37eb292b02f723f6cd5c0574ded6efa691",
    "unrecorded31": "407e7556ea2de04c28db866b313013b4185dae88ff6b2adf607ba6db28eb74a0"
  }
}
```
<!-- END 7dr RETAINED REPORT FIBRE RECEIPT -->

<!-- BEGIN 7do PAID BINARY INPUT RECEIPT -->
```json
{
  "status": "PASS_PAID_BINARY_INPUT_SAME_EXECUTION_SOURCE",
  "checks": 441,
  "compiler_sha256": "07c40e179d0446c52650e7a148c82ef33cd03d0349b0875b5b6af5acd7d9f3a5",
  "owned_result_sha256": "bc2addf30982c3c8ba219358d63f7913485c6877763c3e65dd824766b3620f1a",
  "input": {
    "qubits": 16,
    "unknown_wires": [
      6,
      13,
      14,
      15
    ],
    "blank_wires": [
      0,
      1,
      2,
      3,
      4,
      5,
      7,
      8,
      9,
      10,
      11,
      12
    ],
    "Spin": [
      13,
      14
    ],
    "oldRIGHT": [
      15
    ],
    "input_rank": 16,
    "full_work_dimension": 65536
  },
  "preparation": {
    "initial_CX": [
      6,
      12
    ],
    "planes": [
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 130,
        "target_probability_power": 8,
        "positive_G_run": 313440,
        "certified_operator_error_upper": "0.000003816016436500034694250473"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 195,
        "target_probability_power": 8,
        "positive_G_run": 182264,
        "certified_operator_error_upper": "0.000006840421768914821277561372"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 325,
        "target_probability_power": 8,
        "positive_G_run": 20706,
        "certified_operator_error_upper": "0.000008824865508195203723557076"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 455,
        "target_probability_power": 8,
        "positive_G_run": 7842,
        "certified_operator_error_upper": "0.000007969562366160676628797347"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 520,
        "target_probability_power": 8,
        "positive_G_run": 1066218,
        "certified_operator_error_upper": "0.000003179130413726837961119785"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 650,
        "target_probability_power": 8,
        "positive_G_run": 367432,
        "certified_operator_error_upper": "0.000006911046108447952968962757"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 715,
        "target_probability_power": 8,
        "positive_G_run": 591192,
        "certified_operator_error_upper": "0.000007276483576300049783801712"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 845,
        "target_probability_power": 8,
        "positive_G_run": 159412,
        "certified_operator_error_upper": "0.000000101136272534760229961463"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 975,
        "target_probability_power": 8,
        "positive_G_run": 798872,
        "certified_operator_error_upper": "0.000004661292938204207310874709"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1040,
        "target_probability_power": 8,
        "positive_G_run": 306328,
        "certified_operator_error_upper": "0.000000066285148410197655303516"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1170,
        "target_probability_power": 8,
        "positive_G_run": 408560,
        "certified_operator_error_upper": "0.000004694140449086814774598745"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1300,
        "target_probability_power": 8,
        "positive_G_run": 3946,
        "certified_operator_error_upper": "0.000004587682762589310236727143"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1365,
        "target_probability_power": 8,
        "positive_G_run": 194108,
        "certified_operator_error_upper": "0.000001072198781338810261245348"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1495,
        "target_probability_power": 8,
        "positive_G_run": 26118,
        "certified_operator_error_upper": "0.000002789765779879009152761265"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1560,
        "target_probability_power": 8,
        "positive_G_run": 601598,
        "certified_operator_error_upper": "0.000009604742295565298773139767"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1690,
        "target_probability_power": 8,
        "positive_G_run": 818926,
        "certified_operator_error_upper": "0.000004608531951728107992226588"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1820,
        "target_probability_power": 8,
        "positive_G_run": 350332,
        "certified_operator_error_upper": "0.000009677398574111852244668571"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 1885,
        "target_probability_power": 8,
        "positive_G_run": 148744,
        "certified_operator_error_upper": "0.000002283355673708100139477480"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2015,
        "target_probability_power": 8,
        "positive_G_run": 511550,
        "certified_operator_error_upper": "0.000003996251472418701460116033"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2080,
        "target_probability_power": 8,
        "positive_G_run": 337128,
        "certified_operator_error_upper": "0.000006500510756541542193301163"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2210,
        "target_probability_power": 8,
        "positive_G_run": 250636,
        "certified_operator_error_upper": "0.000005238644749017651959483759"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2340,
        "target_probability_power": 8,
        "positive_G_run": 400768,
        "certified_operator_error_upper": "0.000006040032996883340407252237"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2405,
        "target_probability_power": 8,
        "positive_G_run": 311060,
        "certified_operator_error_upper": "0.000003721547431659655238559709"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2535,
        "target_probability_power": 8,
        "positive_G_run": 278900,
        "certified_operator_error_upper": "0.000000108852083354462210903507"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2665,
        "target_probability_power": 8,
        "positive_G_run": 304288,
        "certified_operator_error_upper": "0.000009700958377550938174945381"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2730,
        "target_probability_power": 8,
        "positive_G_run": 208148,
        "certified_operator_error_upper": "0.000008996720485749870891713745"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2860,
        "target_probability_power": 8,
        "positive_G_run": 764332,
        "certified_operator_error_upper": "0.000005134257559892494251973246"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 2925,
        "target_probability_power": 8,
        "positive_G_run": 1019912,
        "certified_operator_error_upper": "0.000005248508176388528668597462"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3055,
        "target_probability_power": 8,
        "positive_G_run": 319348,
        "certified_operator_error_upper": "0.000003626457349812923004454633"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3185,
        "target_probability_power": 8,
        "positive_G_run": 61650,
        "certified_operator_error_upper": "0.000005529051574425619638397339"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3250,
        "target_probability_power": 8,
        "positive_G_run": 365130,
        "certified_operator_error_upper": "0.000007019163399417587324187629"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3380,
        "target_probability_power": 8,
        "positive_G_run": 425554,
        "certified_operator_error_upper": "0.000009570268899186235193020506"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3510,
        "target_probability_power": 8,
        "positive_G_run": 182158,
        "certified_operator_error_upper": "0.000008063841368788347671165442"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3520,
        "target_probability_power": 9,
        "positive_G_run": 440118,
        "certified_operator_error_upper": "0.000008039354457499323517633398"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3650,
        "target_probability_power": 9,
        "positive_G_run": 462290,
        "certified_operator_error_upper": "0.000007572783791095608156777272"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3715,
        "target_probability_power": 9,
        "positive_G_run": 183858,
        "certified_operator_error_upper": "0.000008641791277045843718161057"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3845,
        "target_probability_power": 9,
        "positive_G_run": 378674,
        "certified_operator_error_upper": "0.000001456007017489252395436570"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 3975,
        "target_probability_power": 9,
        "positive_G_run": 242504,
        "certified_operator_error_upper": "0.000000992259543376051475895583"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4040,
        "target_probability_power": 9,
        "positive_G_run": 221430,
        "certified_operator_error_upper": "0.000001357104897633638401700214"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4170,
        "target_probability_power": 9,
        "positive_G_run": 285070,
        "certified_operator_error_upper": "0.000002634219514609219358124719"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4235,
        "target_probability_power": 9,
        "positive_G_run": 75272,
        "certified_operator_error_upper": "0.000008950538039920359443469764"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4365,
        "target_probability_power": 9,
        "positive_G_run": 186812,
        "certified_operator_error_upper": "0.000007637527089430013620789765"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4495,
        "target_probability_power": 9,
        "positive_G_run": 82462,
        "certified_operator_error_upper": "0.000007894052546146226181836054"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4560,
        "target_probability_power": 9,
        "positive_G_run": 951774,
        "certified_operator_error_upper": "0.000005243632380884005800655291"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4690,
        "target_probability_power": 9,
        "positive_G_run": 172588,
        "certified_operator_error_upper": "0.000000595145341859377508463247"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4820,
        "target_probability_power": 9,
        "positive_G_run": 451778,
        "certified_operator_error_upper": "0.000000384112874443591634637429"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 4885,
        "target_probability_power": 9,
        "positive_G_run": 981894,
        "certified_operator_error_upper": "0.000004091799813326811679659129"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 5015,
        "target_probability_power": 9,
        "positive_G_run": 566952,
        "certified_operator_error_upper": "0.000005114867076259050288564611"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 5080,
        "target_probability_power": 9,
        "positive_G_run": 420454,
        "certified_operator_error_upper": "0.000008001404252591376919497770"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 5210,
        "target_probability_power": 9,
        "positive_G_run": 590300,
        "certified_operator_error_upper": "0.000002616426276857026118181994"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 5340,
        "target_probability_power": 9,
        "positive_G_run": 313724,
        "certified_operator_error_upper": "0.000000651072814883507360544986"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 5405,
        "target_probability_power": 9,
        "positive_G_run": 122960,
        "certified_operator_error_upper": "0.000002177283267035247483460043"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 5535,
        "target_probability_power": 9,
        "positive_G_run": 99166,
        "certified_operator_error_upper": "0.000007326968259845471033756106"
      },
      {
        "old_input": 0,
        "anchor": 0,
        "leaf": 5600,
        "target_probability_power": 9,
        "positive_G_run": 193422,
        "certified_operator_error_upper": "0.000003271559579103269780814153"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 260,
        "target_probability_power": 7,
        "positive_G_run": 423620,
        "certified_operator_error_upper": "0.000002365056397031962356952421"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 390,
        "target_probability_power": 7,
        "positive_G_run": 100504,
        "certified_operator_error_upper": "0.000009086899544862298949837677"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 585,
        "target_probability_power": 7,
        "positive_G_run": 14012,
        "certified_operator_error_upper": "0.000000521201606292603603572498"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 780,
        "target_probability_power": 7,
        "positive_G_run": 640608,
        "certified_operator_error_upper": "0.000005290004886999977334500689"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 910,
        "target_probability_power": 7,
        "positive_G_run": 550900,
        "certified_operator_error_upper": "0.000008690005023020358516001449"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 1105,
        "target_probability_power": 7,
        "positive_G_run": 370046,
        "certified_operator_error_upper": "0.000003200730820209605140091351"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 1235,
        "target_probability_power": 7,
        "positive_G_run": 395434,
        "certified_operator_error_upper": "0.000009582270422921587631090750"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 1430,
        "target_probability_power": 7,
        "positive_G_run": 150600,
        "certified_operator_error_upper": "0.000004481561225723482865688998"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 1625,
        "target_probability_power": 7,
        "positive_G_run": 409396,
        "certified_operator_error_upper": "0.000008864626633095427124729252"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 1755,
        "target_probability_power": 7,
        "positive_G_run": 39818,
        "certified_operator_error_upper": "0.000001755970401681662020904158"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 1950,
        "target_probability_power": 7,
        "positive_G_run": 292182,
        "certified_operator_error_upper": "0.000006697855935636458757378435"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 2145,
        "target_probability_power": 7,
        "positive_G_run": 362254,
        "certified_operator_error_upper": "0.000004561065046634040992035751"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 2275,
        "target_probability_power": 7,
        "positive_G_run": 368346,
        "certified_operator_error_upper": "0.000005498883127066731979738913"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 2470,
        "target_probability_power": 7,
        "positive_G_run": 280076,
        "certified_operator_error_upper": "0.000006126485948456546470306149"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 2600,
        "target_probability_power": 7,
        "positive_G_run": 840914,
        "certified_operator_error_upper": "0.000002310638818498605045211231"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 2795,
        "target_probability_power": 7,
        "positive_G_run": 114622,
        "certified_operator_error_upper": "0.000007190575576363796586958737"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 2990,
        "target_probability_power": 7,
        "positive_G_run": 1017532,
        "certified_operator_error_upper": "0.000004243387021372049179665225"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 3120,
        "target_probability_power": 7,
        "positive_G_run": 4938,
        "certified_operator_error_upper": "0.000000043381748853599125605914"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 3315,
        "target_probability_power": 7,
        "positive_G_run": 111484,
        "certified_operator_error_upper": "0.000002555409316403628127735645"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 3445,
        "target_probability_power": 7,
        "positive_G_run": 232332,
        "certified_operator_error_upper": "0.000003416144570353190495758419"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 3585,
        "target_probability_power": 8,
        "positive_G_run": 186812,
        "certified_operator_error_upper": "0.000007637527089430013620789765"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 3780,
        "target_probability_power": 8,
        "positive_G_run": 82462,
        "certified_operator_error_upper": "0.000007894052546146226181836054"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 3910,
        "target_probability_power": 8,
        "positive_G_run": 951774,
        "certified_operator_error_upper": "0.000005243632380884005800655291"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 4105,
        "target_probability_power": 8,
        "positive_G_run": 172588,
        "certified_operator_error_upper": "0.000000595145341859377508463247"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 4300,
        "target_probability_power": 8,
        "positive_G_run": 451778,
        "certified_operator_error_upper": "0.000000384112874443591634637429"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 4430,
        "target_probability_power": 8,
        "positive_G_run": 981894,
        "certified_operator_error_upper": "0.000004091799813326811679659129"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 4625,
        "target_probability_power": 8,
        "positive_G_run": 566952,
        "certified_operator_error_upper": "0.000005114867076259050288564611"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 4755,
        "target_probability_power": 8,
        "positive_G_run": 420454,
        "certified_operator_error_upper": "0.000008001404252591376919497770"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 4950,
        "target_probability_power": 8,
        "positive_G_run": 590300,
        "certified_operator_error_upper": "0.000002616426276857026118181994"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 5145,
        "target_probability_power": 8,
        "positive_G_run": 313724,
        "certified_operator_error_upper": "0.000000651072814883507360544986"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 5275,
        "target_probability_power": 8,
        "positive_G_run": 122960,
        "certified_operator_error_upper": "0.000002177283267035247483460043"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 5470,
        "target_probability_power": 8,
        "positive_G_run": 99166,
        "certified_operator_error_upper": "0.000007326968259845471033756106"
      },
      {
        "old_input": 1,
        "anchor": 65,
        "leaf": 5665,
        "target_probability_power": 8,
        "positive_G_run": 193422,
        "certified_operator_error_upper": "0.000003271559579103269780814153"
      }
    ],
    "plane_count": 87,
    "rle_records": 5333825,
    "rle_stream_sha256": "852ac77ff1ba6465cd5f7f4f24b63b8358f7223a0be14ffb2b6b495ea5f0b30c",
    "direct_inventory": {
      "G": 128548888576,
      "CX": 4842305,
      "SourceI": 270336
    },
    "positive_inverse_inventory": {
      "G": 128548888576,
      "CX": 7889729,
      "SourceI": 2236416
    },
    "actual_input_operator_error": 2.9741099043748848e-05,
    "certified_input_operator_error_upper": "0.000423597039241966803689790303",
    "input_error_budget_exact_rational": [
      423597039241966803689790303,
      1000000000000000000000000000000
    ],
    "primitive_stages_executed_individually": false,
    "all_preparation_16_input_columns_evaluated": true
  },
  "whole_word_recipe": {
    "generator": "whole_word_runs(preparation_side, loop_side), each side in {-1,0,1}",
    "chronological_sections": [
      "preparation_runs(side)",
      "byte-matched owned loop",
      "inverse_preparation_runs(side)",
      "two paid G^r SourceI^2 blocks"
    ],
    "owned_loop_word_sha256": "22ea825f6103a8987403e605d803c19657a2e387d4e8421a1114a3218ea5745d",
    "all_owned_loop_word_hashes": {
      "0": "22ea825f6103a8987403e605d803c19657a2e387d4e8421a1114a3218ea5745d",
      "-1": "534f087d490870d4d640aacfc72ed0c8e3bfa2dd732faf0a99fceb288f78da09",
      "1": "27901c3a695a3ba71b214f70d25c209aeae219871917aa1de34371f5988515d7"
    },
    "all_inverse_and_padding_calls_positive_native_primitives": true
  },
  "variation": {
    "changed_plane": 0,
    "run_delta": 1098,
    "decoded_angle_step": "0.0115782681309647539968259678974167696",
    "run_values": {
      "-1": 312342,
      "0": 313440,
      "1": 314538
    },
    "same_native_initial_boundary": true,
    "same_full_inventory": {
      "G": 257214301184,
      "CX": 12733188,
      "SourceI": 2506888
    },
    "whole_stages": 257229541260,
    "u": {
      "-1": [
        "0.018073553115520330234127705733",
        "0.018073553115520330234127705736"
      ],
      "0": [
        "0.021287337849896284664708918772",
        "0.021287337849896284664708918775"
      ],
      "1": [
        "0.024757808893258857066994120694",
        "0.024757808893258857066994120697"
      ]
    },
    "actual_corner": {
      "-1": [
        "0.95126227613134270844893220466458848",
        "0.94737447477230462033447724320081851"
      ],
      "0": [
        "0.947376196611555384829102493062225951",
        "0.94737447477230462033447724320081851"
      ],
      "1": [
        "0.943179734321667440287824074955461936",
        "0.94737447477230462033447724320081851"
      ]
    }
  },
  "complete_book": {
    "beta": "2p^2",
    "zeta": "2^-20",
    "full_thermal_modes": 7164562966806528000,
    "a0_interval": [
      "15.586588649889302436781848065773",
      "15.586588649889302436781848065776"
    ],
    "heat_interval": [
      "56.719942321489786426506268275296",
      "56.719942321489786426506268275299"
    ],
    "winding_tail_bound": "4*10^(-N)",
    "return_price_intervals": {
      "-1": [
        "0.000001507428710020580098418399",
        "0.000001507428710020580098418402"
      ],
      "0": [
        "0.000001563720372462082335261637",
        "0.000001563720372462082335261640"
      ],
      "1": [
        "0.000001624249299131864734232498",
        "0.000001624249299131864734232501"
      ]
    },
    "absolute_price_intervals": {
      "-1": [
        "56.719943828918496447086366693696",
        "56.719943828918496447086366693699"
      ],
      "0": [
        "56.719943885210158888588603536934",
        "56.719943885210158888588603536937"
      ],
      "1": [
        "56.719943945739085558371002507795",
        "56.719943945739085558371002507798"
      ]
    },
    "finite_difference_interval": [
      "0.000000116820589111284635814098",
      "0.000000116820589111284635814101"
    ],
    "preparation_secant_interval": [
      "0.000017476977691420472827244052",
      "0.000017476977691420472827244055"
    ],
    "preparation_derivative_interval": [
      "0.000017479841090748204477372140",
      "0.000017479841090748204477372143"
    ],
    "heat_difference_exactly_zero": true
  },
  "two_axis_same_execution": {
    "coordinates": [
      "actual preparation probability u",
      "actual decoded loop angle phi"
    ],
    "absolute_price_grid": {
      "(-1, -1)": [
        "56.719943792704095630605280691068",
        "56.719943792704095630605280691071"
      ],
      "(-1, 0)": [
        "56.719943828918496447086366693696",
        "56.719943828918496447086366693699"
      ],
      "(-1, 1)": [
        "56.719943864811887355973246242159",
        "56.719943864811887355973246242162"
      ],
      "(0, -1)": [
        "56.719943847680421316489679460446",
        "56.719943847680421316489679460449"
      ],
      "(0, 0)": [
        "56.719943885210158888588603536934",
        "56.719943885210158888588603536937"
      ],
      "(0, 1)": [
        "56.719943922405329387919659771561",
        "56.719943922405329387919659771564"
      ],
      "(1, -1)": [
        "56.719943906801555062272406151674",
        "56.719943906801555062272406151677"
      ],
      "(1, 0)": [
        "56.719943945739085558371002507795",
        "56.719943945739085558371002507798"
      ],
      "(1, 1)": [
        "56.719943984327193366581972147835",
        "56.719943984327193366581972147838"
      ]
    },
    "actual_loop_gain_interval": [
      "0.000002392185063590529478050760",
      "0.000002392185063590529478050763"
    ],
    "loop_angle_step_interval": [
      "0.015621006860749434265203121832",
      "0.015621006860749434265203121835"
    ],
    "actual_loop_normalized_contrast_interval": [
      "0.999842506920919443437590048560",
      "0.999842506920919443437590048563"
    ],
    "preparation_source_over_actual_loop_gain_interval": [
      "7.307060543431363206607526004528",
      "7.307060543431363206607526004531"
    ]
  },
  "scope": "One explicitly prepared source-I binary execution sector and actual finite code comparisons, with generated cuts and full homogeneous INTERNAL Book functional. Not physical admission of the binary primitives/initial blanks, all independent physical prices or variations, an emitted giant field compiler, or GR closure."
}
```
<!-- END 7do PAID BINARY INPUT RECEIPT -->
