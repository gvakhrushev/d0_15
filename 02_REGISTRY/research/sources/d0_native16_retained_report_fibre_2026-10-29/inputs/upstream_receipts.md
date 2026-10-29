<!-- BEGIN 7dq ARCHIVE SEED QUERY RECEIPT -->
```json
{
  "archive": {
    "fixed_raw_tick_archive_claim": false,
    "full_endpoint_commutation": true,
    "same_original_A0_and_full_Spin_oldRIGHT_algebra": true,
    "unused_left_padding_arbitrary": true
  },
  "boundary": {
    "active": [
      0,
      6,
      11,
      12,
      13,
      14
    ],
    "active_dimension": 64,
    "blanks": 12,
    "full_dimension": 65536,
    "input_rank": 16,
    "input_spectator": 2,
    "oldRIGHT": 15,
    "thermal_spectator": 1024,
    "total_wires": 16,
    "unknown": [
      6,
      13,
      14,
      15
    ]
  },
  "checker_sha256": "764ffcab31407770f56a843c5b53e9ee0da30f95d01632ea05e50ce67be21b82",
  "checks": 434,
  "corners": {
    "A": "diag(p^3 I8,0_8)",
    "B": "diag(I8,0_8)",
    "C": "diag((2p^6-1) I8,0_8)",
    "seed": "diag(I8,0_8)"
  },
  "incoming_nonscalar_input_commit": "d37bd1ecf9550034586f32426fac84aecaf43be0",
  "input_commit": "185ab21cb165cbf420291a6d8a2056dc366e5275",
  "input_pins": {
    "d0_canonical_stationary_family_2026-10-28/PROOF_RU.md": "fe4b8e9033098ced52299fbc0481ab2ddecceed69c6f4392988803ab0abfa005",
    "d0_canonical_stationary_family_2026-10-28/check_canonical_seed.py": "21744ce3ea2e55dbd48a74393fd627b209d49b391e9367330858c519eab6ca94",
    "d0_clock_winding_source_2026-10-28/PROOF_RU.md": "ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418",
    "d0_native_stationary_seed_2026-10-28/check_seed.py": "9bd41ca8b58fb364fa00cedf9aee493d0fe03963c5b3fda92583def1fd192120",
    "d0_task_faithful_source_2026-10-28/check_task_source.py": "ac1b5af37e848782060b8f686852729d401d7b48d7c1f7bff459075d59f0f180"
  },
  "inventories": {
    "A": {
      "CX": 25,
      "G": 4,
      "SourceI": 14
    },
    "B": {
      "CX": 25,
      "G": 4,
      "SourceI": 14
    },
    "C": {
      "CX": 23,
      "G": 4,
      "SourceI": 14
    },
    "short": {
      "CX": 19,
      "G": 2,
      "SourceI": 10
    }
  },
  "literal_words": {
    "A": [
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
        "op": "G",
        "wires": [
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
    ],
    "B": [
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
          0
        ]
      }
    ],
    "C": [
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
          6,
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
          0
        ]
      },
      {
        "op": "CX",
        "wires": [
          6,
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
          6,
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
          6,
          11
        ]
      }
    ],
    "short": [
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
  "nonscalar_future": {
    "actual_cold_product": true,
    "all_five_prefix_sources_exact_zero": true,
    "all_stages": [
      {
        "coefficients_over_g": [],
        "op": "CX",
        "operator_norm_dual_over_g": 0,
        "stage": 1,
        "wires": [
          6,
          12
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 2,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 3,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 4,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 5,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 6,
        "wires": [
          6,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 7,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 8,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 9,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "-4"
          ],
          [
            1,
            4,
            "4"
          ],
          [
            2,
            7,
            "-4"
          ],
          [
            3,
            6,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 10,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "4"
          ],
          [
            1,
            5,
            "4"
          ],
          [
            2,
            6,
            "4"
          ],
          [
            3,
            7,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 11,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 12,
        "wires": [
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "4"
          ],
          [
            1,
            4,
            "-4"
          ],
          [
            2,
            7,
            "4"
          ],
          [
            3,
            6,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 13,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "-4"
          ],
          [
            1,
            5,
            "-4"
          ],
          [
            2,
            6,
            "-4"
          ],
          [
            3,
            7,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 14,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 15,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 16,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 17,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 18,
        "wires": [
          6,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 19,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 20,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 21,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "-4"
          ],
          [
            1,
            4,
            "4"
          ],
          [
            2,
            7,
            "-4"
          ],
          [
            3,
            6,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 22,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "4"
          ],
          [
            1,
            5,
            "4"
          ],
          [
            2,
            6,
            "4"
          ],
          [
            3,
            7,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 23,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 24,
        "wires": [
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "4"
          ],
          [
            1,
            4,
            "-4"
          ],
          [
            2,
            7,
            "4"
          ],
          [
            3,
            6,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 25,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "-4"
          ],
          [
            1,
            5,
            "-4"
          ],
          [
            2,
            6,
            "-4"
          ],
          [
            3,
            7,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 26,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 27,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 28,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 29,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 30,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 31,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 32,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "-4"
          ],
          [
            1,
            4,
            "4"
          ],
          [
            2,
            7,
            "-4"
          ],
          [
            3,
            6,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 33,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "4"
          ],
          [
            1,
            5,
            "4"
          ],
          [
            2,
            6,
            "4"
          ],
          [
            3,
            7,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 34,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 35,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 36,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 37,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 38,
        "wires": [
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 39,
        "wires": [
          6,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 40,
        "wires": [
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 41,
        "wires": [
          6,
          11
        ]
      }
    ],
    "commutes_with_return_projector": true,
    "full_B_interval": [
      "27.188969808801702414046933399179414398483862067",
      "27.188969808801702414046933399179434528268335222"
    ],
    "full_heat_interval": [
      "27.188960573493033079606540214264102673644554290",
      "27.188960573493033079606540214264122803429027446"
    ],
    "full_modes": 1141964800,
    "full_raw_stage_max_dual_over_abs_g": 576,
    "full_return_interval": [
      "0.000009235308669334440393184915311724839307775",
      "0.000009235308669334440393184915311724839307778"
    ],
    "future_effect": "diag((2p^6-1)^2 I8,I8)",
    "future_gain_interval": [
      "0.000006023485401478137596096245153867810104761",
      "0.000006023485401478137596096245153867810104764"
    ],
    "future_stages": 36,
    "g_signed_interval": [
      "-0.000000388771692006215587090309017621782164264",
      "-0.000000388771692006215587090309017621782164261"
    ],
    "native_reentry_negative_control": "S_word;CX(6,12) has K=I, unlike K_CX K_seed=diag(I8,0_8); retention of the new right12 record is not claimed for this control",
    "nonzero_real_components": 66,
    "raw_stages": 41,
    "real_axis_components": 534
  },
  "physical_limits": {
    "GR_closed": false,
    "all42_map_not_proved": true,
    "fixed_finite_word_alternatives_executed": true,
    "no_continuous_native_gate_claim": true,
    "selected_full_Cost_Info_not_identified": true,
    "single_autonomous_controller_not_proved": true
  },
  "price43": {
    "A_full_B_interval": [
      "27.251321332653249109755279560072556945630233176",
      "27.251321332653249109755279560072577075414706332"
    ],
    "A_minus_B_interval": [
      "0.000007204226189964287779304299645565884614332",
      "0.000007204226189964287779304299645565884614335"
    ],
    "A_return_interval": [
      "0.000014833624359195407837306249535799190639668",
      "0.000014833624359195407837306249535799190639671"
    ],
    "B_full_B_interval": [
      "27.251314128427059145467500255772911379745618843",
      "27.251314128427059145467500255772931509530091999"
    ],
    "B_return_interval": [
      "0.000007629398169231120058001949890233306025335",
      "0.000007629398169231120058001949890233306025338"
    ],
    "H0_modes": 92995584,
    "balanced_plus_minus_multiplicity": 32768,
    "full_H_interval": [
      "27.251306499028889914347442253823021146439593507",
      "27.251306499028889914347442253823041276224066662"
    ],
    "full_modes": 1197670400,
    "harmonic_modes": 1011679232,
    "heat_row_exact_zero_at_both_words": true,
    "paired_H1_modes": 1104674816
  },
  "runtime": {
    "mpmath": "1.3.0",
    "python": "3.9.6",
    "sympy": "1.14.0"
  },
  "scope": "actual fixed-boundary archive-preserving seed plus query; full fixed INTERNAL Book price; not physical X_N or GR closure",
  "source43": {
    "A_all_stages": [
      {
        "coefficients_over_g": [],
        "op": "CX",
        "operator_norm_dual_over_g": 0,
        "stage": 1,
        "wires": [
          6,
          12
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 2,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 3,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 4,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [],
        "op": "SourceI",
        "operator_norm_dual_over_g": 0,
        "stage": 5,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 6,
        "wires": [
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 7,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 8,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 9,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "-4"
          ],
          [
            1,
            4,
            "4"
          ],
          [
            2,
            7,
            "-4"
          ],
          [
            3,
            6,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 10,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "4"
          ],
          [
            1,
            5,
            "4"
          ],
          [
            2,
            6,
            "4"
          ],
          [
            3,
            7,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 11,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 12,
        "wires": [
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "4"
          ],
          [
            1,
            4,
            "-4"
          ],
          [
            2,
            7,
            "4"
          ],
          [
            3,
            6,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 13,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "-4"
          ],
          [
            1,
            5,
            "-4"
          ],
          [
            2,
            6,
            "-4"
          ],
          [
            3,
            7,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 14,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 15,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 16,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 17,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 18,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 19,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 20,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "-4"
          ],
          [
            1,
            4,
            "4"
          ],
          [
            2,
            7,
            "-4"
          ],
          [
            3,
            6,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 21,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "4"
          ],
          [
            1,
            5,
            "4"
          ],
          [
            2,
            6,
            "4"
          ],
          [
            3,
            7,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 22,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 23,
        "wires": [
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "4"
          ],
          [
            1,
            4,
            "-4"
          ],
          [
            2,
            7,
            "4"
          ],
          [
            3,
            6,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 24,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "-4"
          ],
          [
            1,
            5,
            "-4"
          ],
          [
            2,
            6,
            "-4"
          ],
          [
            3,
            7,
            "-4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 25,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 26,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 27,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 28,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 29,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 30,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "-16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 31,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            5,
            "-4"
          ],
          [
            1,
            4,
            "4"
          ],
          [
            2,
            7,
            "-4"
          ],
          [
            3,
            6,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 32,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            4,
            "4"
          ],
          [
            1,
            5,
            "4"
          ],
          [
            2,
            6,
            "4"
          ],
          [
            3,
            7,
            "4"
          ]
        ],
        "op": "SourceI",
        "operator_norm_dual_over_g": 16,
        "stage": 33,
        "wires": [
          0,
          13,
          14
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 34,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 35,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 36,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 37,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 38,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 39,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "G",
        "operator_norm_dual_over_g": 16,
        "stage": 40,
        "wires": [
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            3,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 41,
        "wires": [
          0,
          11
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            2,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 42,
        "wires": [
          11,
          0
        ]
      },
      {
        "coefficients_over_g": [
          [
            0,
            1,
            "16"
          ]
        ],
        "op": "CX",
        "operator_norm_dual_over_g": 16,
        "stage": 43,
        "wires": [
          0,
          11
        ]
      }
    ],
    "A_nonzero_real_components": 68,
    "B_nonzero_real_components": 0,
    "full_local_complex_dimensions": 1312,
    "full_raw_stage_max_dual_interval": [
      "0.000133011647164318196959510273111586671738308",
      "0.000133011647164318196959510273111586671738311"
    ],
    "full_raw_stage_max_dual_over_w_interval": [
      "312.841996145266822048941119232228464028286975150",
      "312.841996145266822048941119232228464028286975153"
    ],
    "g_definition": "zeta*c*sqrt(1-c^2)/(1-zeta+zeta*c^2), c=p^3",
    "g_interval": [
      "0.000000218769156520260192367615580775635973252",
      "0.000000218769156520260192367615580775635973255"
    ],
    "imaginary_symmetric_axes_exact_zero": true,
    "one_sided_row_interval": [
      "0.000003500306504324163077881849292410175572059",
      "0.000003500306504324163077881849292410175572062"
    ],
    "query_conjugacy_row_interval": [
      "0.000007000613008648326155763698584820351144120",
      "0.000007000613008648326155763698584820351144123"
    ],
    "real_axis_components_per_word": 546,
    "seed_five_occurrences_exact_zero": true,
    "true_w_interval": [
      "0.000000425171967968631731746184594007985738018",
      "0.000000425171967968631731746184594007985738021"
    ],
    "whole_matrix_source_fd_max_error": "2.333540635646586277411043806635267e-30"
  },
  "status": "PASS",
  "word_sha256": {
    "A": "4ac8481e3282befb84d5f8004e738a26dae6ea5a12874373adba611082f7eed8",
    "B": "fbb6a6f0b718b4e5ebb4e726f62ed6429441eb561747e11a6f61b8976894e5eb",
    "C": "213e905b80cfa19eeb36299b91308533be126ee4663bae41a21463d5800c7b21",
    "short": "407e7556ea2de04c28db866b313013b4185dae88ff6b2adf607ba6db28eb74a0"
  }
}
```
<!-- END 7dq ARCHIVE SEED QUERY RECEIPT -->

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
