# WRK-A4D-SOLDER-METRIC-HISTORY-SPATIAL-SPLIT

## Class
WORKER

## Parent
`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State
REVIEW

## Baseline
`c44af0ffbbd1b3bf31ce20ef6be92f038e6e2483` (`origin/main`, fetched 2026-09-23).

## Scope
Formalize the exact soldered Lorentz Gram completion of the existing centered coframe readout, its flat tangent and finite right-frame invariance. Construct the literal A-phase/spatial phase equivalence, A-invariant function/cochain factorization, spatial difference compatibility and the existing Hodge-square intertwiner. Provide a separate history/spatial carrier using the Feshbach tick index.

## Boundaries
Preserve `CAUSAL-TIME-ROLE-INTERTWINER-MISSING`, `SOLDERED-OBSERVER-REPRESENTATION-NOT-YET-OWNED`, `PHYSICAL-CARTAN-LIFT-STILL-MISSING`, and `HODGE-CONSTITUTIVE-PRIMITIVE-REQUIRED`. No cyclic-phase/history identification, physical time vector, continuum claim, nonlinear Cartan closure, Einstein equation, constitutive selector or Nyquist deletion. Sitewise Lorentz matrices alone do not commute with directional centering.

## Affected Claims
- `D0-HODGE-LINKS-001`

## Exit Condition
Two source modules pass narrow builds, `D0.All`, repository/work/no-sorry/generated-view guards and capstone axiom inspection. One PR against main, task in REVIEW; coordinator owns CI and merge.

## Result
- `SOLDER-METRIC-FLAT-TANGENT-OWNED` / `COFRAME-READOUT-IS-SOLDER-METRIC-FLAT-TANGENT`.
- `ARCHIVE-SPATIAL-FACTOR-OWNED`.
- `ARCHIVE-A-PHASE-NOT-USED-AS-HISTORY-COORDINATE`.

The existing readout is the exact linear coefficient of the nonlinear Gram candidate, with an explicit quadratic remainder. The Lorentz tangent space is structurally equivalent to six independent RolePair coordinates. Its sitewise field carrier has finrank `6 * archiveModes N`. Constant pre-centered Lorentz directions are readout-null; variable directions require an explicit centered lift. No equality with the pre-centered readout kernel is asserted.

The archive split and generic A-invariant factorization are explicit equivalences. Cochains factor by a linear equivalence preserving the existing Fock fibre. Both spatial differences intertwine; the existing Hodge square becomes the spatial Laplacian, also proved equal to minus the sum of backward-after-forward differences. The history/spatial product reads `FeshbachSchurTimeDelayOwner.tickIndex` without any tick-to-A-phase map.

The requested spatial shell owner is named `ArchiveHodgeCARDiracShell.lean` in this baseline. Both new modules are registered as explicit support for existing `D0-HODGE-LINKS-001`; no claim ID or frozen claim status is changed.

## Exact capstones
All declarations below are in namespace `D0.Geometry`.

`A4DSolderMetricCompletion.lean`:
- `solderMetric_expand`
- `solderMetric_minus_background`
- `solderMetric_smul_expand`
- `solderMetric_flat_tangent`
- `solderMetric_forwardGauge_flat_tangent`
- `solderGram_right_lorentz_invariant`
- `lorentzTangent_right_condition`
- `lorentzTangent_centeredReadout_zero`
- `lorentzTangent_centeredLift_readout_zero`
- `rolePairsEquivLorentzTangent`
- `roleLorentzTangent_finrank`
- `localLorentzTangentField_finrank`

`ArchiveSpatialHistorySplit.lean`:
- `spatialRole_card_three`
- `spatialArchivePhaseGroup_card`
- `archiveRolePhase_timeSpatialEquiv`
- `axisInvariant_eq_of_same_spatialProjection`
- `axisInvariantFunctionEquiv`
- `axisInvariantCochainEquivSpatial`
- `spatial_forwardDifference_intertwine`
- `spatial_backwardDifference_intertwine`
- `spatialArchiveLaplacian_eq_backward_forward`
- `axisInvariant_hodgeSquare_equiv_spatialLaplacian`
- `historySpatialReading_history`
- `roleA_is_unique_positive_internal_role`

## Local validation
Passed on 2026-09-23:
- Narrow builds of both new modules.
- `lake build D0.All` (4423 jobs).
- `python3 tools/validate_repo.py`: PASS, zero warnings.
- `python3 tools/validate_work.py` and `--self-test`: PASS.
- `python3 tools/generate_lean_views.py --check`: PASS, zero stale views.
- `python3 03_FORMALIZATION/tools/check_no_sorry_in_core.py --all-modules`: PASS.
- `git diff --check`: PASS.
- Capstone `#print axioms`: no `sorryAx`, no newly introduced axioms.

Final fetch retained baseline `c44af0ffbbd1b3bf31ce20ef6be92f038e6e2483`; no rebase was necessary. Local validation is supporting evidence; CONTROL owns remote CI acceptance and merge.

## Axiom report
The matrix, equivalence, difference and history capstones use subsets of `propext`, `Classical.choice`, `Quot.sound`.

The two finrank capstones additionally inherit the existing finite RolePair enumeration dependency:
- `rolePair_card._native.native_decide.ax_1_1`

The Hodge-square intertwiner additionally inherits the existing finite CAR checks:
- `car_annihilate_anticommutator_int._native.native_decide.ax_1_1`
- `car_create_anticommutator_int._native.native_decide.ax_1_1`
- `car_mixed_anticommutator_int._native.native_decide.ax_1_1`

Neither new module introduces `native_decide`, `axiom`, `sorry` or `admit`. Matrix identities and carrier equivalences have structural proofs.
