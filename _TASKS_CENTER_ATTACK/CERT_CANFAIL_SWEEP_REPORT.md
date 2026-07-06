# CERT CAN-FAIL SWEEP — Tier-0 integrity audit of the 05_CERTS corpus

**Date:** 2026-07-05 · **Tool:** `_TASKS_CENTER_ATTACK/cert_canfail_sweep.py` · **Scope:** all top-level `05_CERTS/vp_*.py` (601 files) · **Registry:** `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (538 rows, 417 with `python_cert`, 429 cert references)

**Question audited, per cert:** does a designed, computation-dependent path to a non-zero exit code exist? A verification certificate that cannot fail verifies nothing (the SPECTRAL-EINSTEIN print-only-stub incident showed at least one such cert shipped).

Reproduce:

```
python3 _TASKS_CENTER_ATTACK/cert_canfail_sweep.py --json out.json                # static + cross-ref
python3 _TASKS_CENTER_ATTACK/cert_canfail_sweep.py --dynamic --mutate --top 15    # + runs + mutation probes
```

No cert files and no registry files were modified. Mutation probes ran on copies under scratch only. Certs that statically write files were **not executed** (the repo is not a git repo; no restore path).

---

## 1. Headline counts

| Class | Count | % | Backing ≥1 CERT-CLOSED / NO-GO / NO_GO_PROVED claim |
|---|---|---|---|
| **SOLID** (computed checks + executed negative control) | 398 | 66.2% | 173 |
| **WEAK** (computed checks, no real negative control) | 152 | 25.3% | 39 |
| **STUB-SUSPECT** (no computation-dependent failure path) | 51 | 8.5% | **5** |

- STUB-SUSPECT breakdown: 30 print-only PASS lines, 17 all-asserts-constant, 4 no failure path at all.
- WEAK breakdown: 147 no negative control, **5 with negative controls that are PRINTED but never executed** (Finding F2).
- 12 registry claim-rows cite a STUB-SUSPECT cert (7 of them CERT-CLOSED/NO-GO); 2 further CERT-CLOSED claims rest **solely** on printed-not-executed-control certs.
- Corpus hygiene: 3,036 asserts total, 96 of them constant-expression (can never respond to computation); exit discipline: 489 `SystemExit(main())`, 9 module-level gate, 88 top-level checks, **15 none**; 227 certs read files, 82 write files.
- 13 registry `python_cert` references have **no file** in `05_CERTS/` top level (Section 6).

---

## 2. Finding F1 — 5 stub-suspect certs back 7 CERT-CLOSED/NO-GO claims

All five are in the VNEXT2 family. Their asserts are arithmetic on integer literals (e.g. `assert (9*24**2 + 11*22**2 + 13*20**2) - (...) == 2*359`) — true at write time, forever, independent of any computed object. Dynamic runs confirm: each exits 0 in 0.01 s, and several **print `FAIL_*` lines (one ends its transcript with a bare `FAIL`) while still exiting 0** — transcripts cannot be machine-audited.

| Cert | Dependent claim (release_status) | Lean side | Mutation probe |
|---|---|---|---|
| `vp_vnext2_scene_native_input_audit.py` | D0-VNEXT2-SCENE-FINGERPRINT-OWNER-001 (**CERT-CLOSED**) | LEAN_PROVED | caught (flip hit an asserted literal) |
| `vp_vnext2_tripartite_path_tower_classification.py` | D0-VNEXT2-TRIPARTITE-PATH-TOWER-OWNER-001 (**NO-GO**), D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 (**NO-GO**) | LEAN_PROVED | **SURVIVED** |
| `vp_vnext2_tripartite_scene_xi_intertwiner.py` | D0-VNEXT2-SCENE-XI-INTERTWINER-OWNER-001 (**NO-GO**), D0-VNEXT2-XI-MAXIMALITY-NOGO-001 (**NO-GO**) | LEAN_PROVED | **SURVIVED** |
| `vp_vnext2_scene_native_refinement_category.py` | D0-VNEXT2-SCENE-NATIVE-REFINEMENT-OWNER-001 (**NO-GO**) | LEAN_PROVED | caught (asserted literal) |
| `vp_vnext2_scene_native_scale_cocycles.py` | D0-VNEXT2-DIRAC-COVARIANCE-MAXIMALITY-NOGO-001 (**NO-GO**) | LEAN_PROVED | **SURVIVED** |

Mitigation: all seven claims carry `LEAN_PROVED` on the Lean side, so the claims are not *solely* backed by these certs — but the `python_cert` column currently offers **corroboration theater**, and this matches the previously recorded VNEXT2 content-free-cert desync.

## 3. Finding F2 — negative controls claimed in output but never executed (worst finding)

Five certs print `NEGATIVE_CONTROL_CAUGHT FAIL_*` **unconditionally inside the success branch** — no control computation exists anywhere in the file. A transcript reader sees a control "caught"; nothing was run. Four of them are the **entire formal backing** of two CERT-CLOSED claims whose `lean_status` is `PYTHON_CERTIFIED` (no Lean module at all):

| Cert | Claim | Exposure |
|---|---|---|
| `vp_cvft_boundary_channel_rank.py` | D0-CVFT-F7 (CERT-CLOSED) | **sole backing** (no Lean) |
| `vp_cvft_refined_logdet_rank_bound.py` | D0-CVFT-F7 (CERT-CLOSED) | second leg, same defect |
| `vp_cvft_ueff_pole_discipline.py` | D0-CVFT-F4 (CERT-CLOSED) | **sole backing** (no Lean) |
| `vp_cvft_uv_feedback_tail_bound_refined.py` | D0-CVFT-F4 (CERT-CLOSED) | second leg, same defect |
| `vp_sde_exceptional_point_algebra.py` | (no registry claim) | — |

Smoking gun (`vp_cvft_ueff_pole_discipline.py`, all inputs hardcoded literals):

```python
if contraction and pole_ok and bare_f_real_nonnegative:
    print("PASS_UEFF_CONTRACTION_POLE_DISCIPLINE")
    print("PASS_UEFF_POLE_DISCIPLINE")
    print("NEGATIVE_CONTROL_CAUGHT FAIL_COMPLEX_POLES_FROM_BARE_POSITIVE_F")  # nothing was run
    print("NEGATIVE_CONTROL_CAUGHT FAIL_COMPLEX_POLES_FROM_BARE_F")           # nothing was run
    return 0
```

These four DO have a genuine failure path (`return 1` fall-through), so they are classed WEAK, not STUB — but the checks are tautologies over their own hardcoded inputs (e.g. verifying that `abs(0.8·e^{0.3i}) ≤ 1`), and the control claims in the transcript are fabricated. **D0-CVFT-F7 and D0-CVFT-F4 are CERT-CLOSED on this evidence alone.** Related: the three unreferenced siblings `vp_cvft_boundary_rank_bound.py`, `vp_cvft_logdet_rank_bound.py`, `vp_cvft_uv_feedback_tail_bound.py` have **no failure path whatsoever** (STUB-SUSPECT, `no_failure_path`).

## 4. Finding F3 — dynamic spot-check of the top 15 stub-suspects

Selection: all STUB-SUSPECTs ranked by load-bearing claim count, then total claims, then name; top 15. Runs: `python3 <cert>`, cwd `05_CERTS`, 60 s timeout. Mutation probe (self-contained certs only): copy to scratch, flip the first int literal ≥2 outside prints/f-strings, rerun — a copy that still exits 0 proves no check constrains the computation.

| # | Cert | Run | Mutation (flip → result) |
|---|---|---|---|
| 1 | `vp_vnext2_tripartite_path_tower_classification.py` | rc=0, 0.01s — transcript ends `FAIL` | line 9: 9→10 → rc=0 **SURVIVED** |
| 2 | `vp_vnext2_tripartite_scene_xi_intertwiner.py` | rc=0, 0.01s | line 9: 9→10 → rc=0 **SURVIVED** |
| 3 | `vp_vnext2_scene_native_input_audit.py` | rc=0, 0.01s | line 9: 9→10 → rc=1 caught (asserted literal) |
| 4 | `vp_vnext2_scene_native_refinement_category.py` | rc=0, 0.01s | line 9: 9→10 → rc=1 caught (asserted literal) |
| 5 | `vp_vnext2_scene_native_scale_cocycles.py` | rc=0, 0.01s | line 9: 9→10 → rc=0 **SURVIVED** |
| 6 | `vp_neutrino_phason_decoherence_passport.py` | SKIPPED-WRITES (would modify repo outputs) | SKIPPED (file I/O) |
| 7 | `vp_vnext2_endpoint_conditional_expectation.py` | rc=0, 0.01s | line 9: 9→10 → rc=0 **SURVIVED** |
| 8 | `vp_vnext2_scene_dirac_covariance_selection.py` | rc=0, 0.01s | line 9: 9→10 → rc=0 **SURVIVED** |
| 9 | `vp_vnext2_scene_native_feshbach_lift.py` | rc=0, 0.01s | line 9: 9→10 → rc=0 **SURVIVED** |
| 10 | `vp_vnext2_scene_spectral_intertwining.py` | rc=0, 0.01s | line 9: 9→10 → rc=0 **SURVIVED** |
| 11 | `vp_archive_phason_halo_passport.py` | SKIPPED-WRITES | SKIPPED (file I/O) |
| 12 | `vp_bao_sde_phason_flip_passport.py` | SKIPPED-WRITES | SKIPPED (file I/O) |
| 13 | `vp_baryon_s3_symmetrizer.py` | rc=0, 0.06s — **`RuntimeWarning: invalid value encountered in matmul` yet exits 0** | SKIPPED (no int constant ≥2) |
| 14 | `vp_book02_synthesis_renumbering.py` | SKIPPED-WRITES | SKIPPED (file I/O) |
| 15 | `vp_ckm_holonomy_external_convention_passport.py` | SKIPPED-WRITES | SKIPPED (file I/O) |

Summary: 10/15 executed — **all exit 0**; 9 mutation-probed — **7 survived** (confirmed: nothing in the cert constrains its computation), 2 "caught" only because the flipped literal sat inside a constant assert (the tautology broke — still no computed check). Row 13 is the print-only pathology in its purest form: the linear algebra produced invalid values (NaNs) at runtime and the cert still reported success.

## 5. Full STUB-SUSPECT list (51)

| Cert | Reason | Dependent claims [release_status] |
|---|---|---|
| `vp_vnext2_tripartite_path_tower_classification.py` | all_asserts_constant | D0-VNEXT2-TRIPARTITE-PATH-TOWER-OWNER-001 [NO-GO]; D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 [NO-GO] |
| `vp_vnext2_tripartite_scene_xi_intertwiner.py` | all_asserts_constant | D0-VNEXT2-SCENE-XI-INTERTWINER-OWNER-001 [NO-GO]; D0-VNEXT2-XI-MAXIMALITY-NOGO-001 [NO-GO] |
| `vp_vnext2_scene_native_input_audit.py` | all_asserts_constant | D0-VNEXT2-SCENE-FINGERPRINT-OWNER-001 [CERT-CLOSED] |
| `vp_vnext2_scene_native_refinement_category.py` | all_asserts_constant | D0-VNEXT2-SCENE-NATIVE-REFINEMENT-OWNER-001 [NO-GO] |
| `vp_vnext2_scene_native_scale_cocycles.py` | all_asserts_constant | D0-VNEXT2-DIRAC-COVARIANCE-MAXIMALITY-NOGO-001 [NO-GO] |
| `vp_neutrino_phason_decoherence_passport.py` | print_only_pass_lines | D0-ICECUBE-001 [EMPIRICAL-PASSPORT] |
| `vp_vnext2_endpoint_conditional_expectation.py` | all_asserts_constant | D0-VNEXT2-ENDPOINT-CONDITIONAL-EXPECTATION-OWNER-001 [PROOF-TARGET] |
| `vp_vnext2_scene_dirac_covariance_selection.py` | all_asserts_constant | D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001 [PROOF-TARGET] |
| `vp_vnext2_scene_native_feshbach_lift.py` | all_asserts_constant | D0-VNEXT2-SCENE-FESHBACH-LIFT-OWNER-001 [PROOF-TARGET] |
| `vp_vnext2_scene_spectral_intertwining.py` | all_asserts_constant | D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001 [PROOF-TARGET] |
| `vp_archive_phason_halo_passport.py` | print_only_pass_lines | — |
| `vp_bao_sde_phason_flip_passport.py` | print_only_pass_lines | — |
| `vp_baryon_s3_symmetrizer.py` | print_only_pass_lines | — |
| `vp_book02_synthesis_renumbering.py` | no_failure_path | — |
| `vp_ckm_holonomy_external_convention_passport.py` | print_only_pass_lines | — |
| `vp_cmb_phason_flip_entropy_passport.py` | print_only_pass_lines | — |
| `vp_cvft_boundary_rank_bound.py` | no_failure_path | — |
| `vp_cvft_logdet_rank_bound.py` | no_failure_path | — |
| `vp_cvft_uv_feedback_tail_bound.py` | no_failure_path | — |
| `vp_desi_bao_sde_real_data.py` | print_only_pass_lines | — |
| `vp_edge_alpha_ramification_puiseux.py` | print_only_pass_lines | — |
| `vp_edge_alpha_trace.py` | print_only_pass_lines | — |
| `vp_edge_sector_alpha_trace_target.py` | print_only_pass_lines | — |
| `vp_finite_spin2_wave_operator.py` | print_only_pass_lines | — |
| `vp_higgs_scalar_projector_positive.py` | print_only_pass_lines | — |
| `vp_internal_feedback_resolvent.py` | print_only_pass_lines | — |
| `vp_master_bootstrap_variation.py` | print_only_pass_lines | — |
| `vp_meson_domain_wall_pdg_passport.py` | print_only_pass_lines | — |
| `vp_readout306_proof_cell_v1113.py` | print_only_pass_lines | — |
| `vp_sde_feedback_pressure_reinterpretation.py` | print_only_pass_lines | — |
| `vp_sparc_phason_halo_failure_diagnostics.py` | print_only_pass_lines | — |
| `vp_tick_s3_baryon_asymmetry_scaffold.py` | print_only_pass_lines | — |
| `vp_torus_ramification_indices.py` | print_only_pass_lines | — |
| `vp_torus_ramification_indices_target.py` | print_only_pass_lines | — |
| `vp_v1124_open_sector_closure.py` | print_only_pass_lines | — |
| `vp_v1125_hadron_meson_transfer.py` | print_only_pass_lines | — |
| `vp_v1133_bao_sde_reproducible_passport.py` | print_only_pass_lines | — |
| `vp_v1133_high_gain_full_atlas.py` | print_only_pass_lines | — |
| `vp_v1133_qft_rg_scheme_passports.py` | print_only_pass_lines | — |
| `vp_v1139_phase_unfolding_theorem.py` | print_only_pass_lines | — |
| `vp_v1140_phase_unfolding_master_chain.py` | print_only_pass_lines | — |
| `vp_v1141_abcd_omega8_v9_phi_capacity.py` | print_only_pass_lines | — |
| `vp_vacuum_feedback_equation_of_state.py` | print_only_pass_lines | — |
| `vp_vnext2_endpoint_measure_classification.py` | all_asserts_constant | — |
| `vp_vnext2_scene_native_history_operators.py` | all_asserts_constant | — |
| `vp_vnext2_scene_native_history_tick.py` | all_asserts_constant | — |
| `vp_vnext2_scene_native_retained_archive_lift.py` | all_asserts_constant | — |
| `vp_vnext2_scene_spectral_fingerprint_lift.py` | all_asserts_constant | — |
| `vp_vnext_anchored_dirac_scale_family.py` | all_asserts_constant | — |
| `vp_vnext_canonical_anchor_feshbach_compression.py` | all_asserts_constant | — |
| `vp_vnext_refined_xi_tower_compatibility.py` | all_asserts_constant | — |

Notable near-misses kept out of this class by the audit's own honesty rules: `vp_a2_hypercharge_u1_mass_kernel.py`, `vp_pi0_branch_defect_generation.py`, `vp_alpha_edge_moment_witness.py`, `vp_spectral_action_eh_coefficient.py`, `vp_dm_classicality_guardrail.py` and others initially flagged were confirmed to have live accumulator/fall-through failure paths after fixing two analyzer bugs (sentinel and fall-through-return detection) — they are WEAK or SOLID, not stubs.

## 6. Registry hygiene — 13 dangling `python_cert` references

These are cited by registry rows but have no file at `05_CERTS/` top level (some exist elsewhere, e.g. subdirectories or repo root — not in the audited scope; some may be genuinely missing):

`d0_branch_row_minimal_extension_verify.py`, `d0_ckm_mismatch_bound_verify.py`, `verify_unified_backbone.py`, `verify_unified_feedback.py`, `vp_boundary_dark_survey_driver_kernel.py`, `vp_calibration_dag_and_lambda_section_rigidity_20260522.py`, `vp_final_survey_likelihood_and_baryon_form_factor_closure_20260522.py`, `vp_ftheory_lw2016_chiral_recombination_layer.py`, `vp_ftheory_lw2016_d0_filter.py`, `vp_higgs_anchor_projector.py`, `vp_neutron_lifetime_rate_closure.py`, `vp_proton_terminal_destructive_readout.py`, `vp_single_section_gravity_completion.py`

## 7. Top-10 priority repairs

Ranked by claim exposure (sole formal backing first), then status weight:

1. **`vp_cvft_boundary_channel_rank.py`** — D0-CVFT-F7 is CERT-CLOSED with *no Lean backing*; replace the fake control print with an executed control (e.g. a rank-4 QUP that must be rejected) and derive the QUP matrix from a source object, not a literal.
2. **`vp_cvft_ueff_pole_discipline.py`** — D0-CVFT-F4, same situation: execute a control (a bare positive F whose poles must come out real), compute the eigenvalues from a constructed operator.
3. **`vp_cvft_refined_logdet_rank_bound.py`** — second leg of D0-CVFT-F7, same printed-control defect.
4. **`vp_cvft_uv_feedback_tail_bound_refined.py`** — second leg of D0-CVFT-F4, same defect.
5. **`vp_vnext2_scene_native_input_audit.py`** — the only CERT-CLOSED claim resting on a constant-assert stub (D0-VNEXT2-SCENE-FINGERPRINT-OWNER-001; Lean-proved, so downgrade or repair the Python leg — currently corroboration theater).
6. **`vp_vnext2_tripartite_path_tower_classification.py`** — 2 NO-GO claims; mutation survivor; transcript ends `FAIL` with rc 0. Recompute the path-tower objects and gate the exit on them.
7. **`vp_vnext2_tripartite_scene_xi_intertwiner.py`** — 2 NO-GO claims; mutation survivor.
8. **`vp_vnext2_scene_native_scale_cocycles.py`** — NO-GO claim; mutation survivor.
9. **`vp_vnext2_scene_native_refinement_category.py`** — NO-GO claim; constant asserts only.
10. **`vp_neutrino_phason_decoherence_passport.py`** — D0-ICECUBE-001 empirical passport is print-only AND writes outputs into the repo on every run; add computed gates and move outputs out of band.

Corpus-level repairs: (a) adopt a lint gate = this sweep's STUB test in CI (a cert must possess ≥1 computation-dependent failure path and ≥1 *executed* negative control); (b) fix the 13 dangling registry references; (c) triage the remaining 41 unreferenced suspects — either promote them to real certs or mark them explicitly as non-load-bearing demos.

## 8. Method limits (honest)

- **Static heuristics.** "Can fail" means a designed failure mechanism exists — it does **not** prove the checks are non-vacuous. Tautologies over hardcoded inputs (the CVFT pattern) still count as WEAK-can-fail; whole-program constant propagation was out of scope. Conversely, asserts inside never-called functions would be over-credited (none observed in spot checks).
- **Negative-control detection is lexical + one structural pattern.** A genuinely executed control without the standard vocabulary (CONTROL/REJECTED/planted/…) reads as WEAK; fabricated vocabulary is only caught in the specific success-path-print shape (F2). Other fabrication shapes would pass as SOLID.
- **File-reading certs (227) were not mutation-tested**; file-writing certs (82) were not even executed by the dynamic layer, because the repo is not under git and runs would overwrite tracked outputs. Their dynamic behavior is unverified here.
- **Dynamic coverage is top-15 only.** The 36 remaining suspects are static-only findings. Exit-0-despite-FAIL-prints can only be seen dynamically.
- **Single mutation per cert, first-eligible-constant strategy.** A survivor is damning; a "caught" is weak evidence (twice it was a constant-assert tautology breaking, not a computed check firing).
- **Registry reading is python_cert-column-only.** Claims may carry independent Lean backing (`lean_status` was consulted for the affected claims and is reported above); this audit does not evaluate the Lean side.
- **Analyzer calibration.** Two classifier bugs (non-constant-return sentinel; fall-through `return 1` after in-branch `return 0`) were found and fixed during validation against 8 hand-verified ground-truth certs; final classifications post-fix. False positives/negatives beyond the validated idioms remain possible — the tool errs toward flagging, and every load-bearing flag above was verified by eye.
