# DESI/BAO S_DE Failure Diagnostics

- result: FAIL_DESI_BAO_SDE_REAL_DATA
- diagnostic_result: PASS_DESI_BAO_SDE_FAILURE_DIAGNOSTICS
- dominant_failure_modes: ['LOW_Z_FAILURE', 'MID_Z_FAILURE', 'AMPLITUDE_TOO_LOW']
- shape_diagnostic: AMPLITUDE_ONLY
- recommendation: Frozen finite-window S_DE transfer fails BAO shape; next admissible operator must diagnose transfer geometry without refitting roots or window centers.
- largest_pull_rows:
  - {'tracer': 'ELG', 'z_eff': 1.1, 'pull_d0': -26.23, 'failure_direction': 'AMPLITUDE_TOO_LOW'}
  - {'tracer': 'LRG', 'z_eff': 0.7, 'pull_d0': -17.97, 'failure_direction': 'MID_Z_FAILURE'}
  - {'tracer': 'BGS', 'z_eff': 0.3, 'pull_d0': -7.72, 'failure_direction': 'LOW_Z_FAILURE'}
