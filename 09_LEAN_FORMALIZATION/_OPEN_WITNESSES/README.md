# Open Lean witnesses (carry `sorry`)

These modules are **open proof obligations**, not part of the D0 release graph.
They sit OUTSIDE `D0/` so the core tree stays `sorry`-free under
`check_no_sorry_in_core.py --all`. Nothing imports them and no claim row in
`CLAIM_TO_LEAN_MAP.csv` references them.

- `FiniteBianchiEinsteinTensor.lean` — finite Bianchi -> Einstein-tensor response
  (gravity); theorem `ricci_or_scalar_only_not_full_gravity_response` has a `sorry`.
- `BlackHoleA4EntropyWitness.lean` — A/4 entropy from the ABCD boundary cell
  capacity; theorem `a4_entropy_from_abcd_boundary_cell_capacity` has a `sorry`.

To close either: complete the proof, move the file back under `D0/<Domain>/`,
register a claim row (status climbs PROOF-TARGET -> ... -> CORE-FORMALIZED), and
the scoreboard strength rises. Tracked as gravity-sector work in Phase 8.

## Build-hygiene quarantine (2026-06-15)

The first full `lake build D0.All` (CI never ran it) surfaced 12 **orphan** modules
that never compiled — broken since `base-v14`, no `CLAIM_TO_LEAN_MAP.csv` row
references them. Moved here (out of `D0/`) so `D0.All` is green. None is a `sorry`
witness; each fails to elaborate. To revive: define the missing API / fix the proof,
move back under `D0/<Domain>/`, regenerate `All.lean`.

Higgs/Book04 cluster — depend on a `ConstructiveScalarProjectorClosure` /
`FiniteMatterTransferCarrier` / `FiniteScalarProjector` / `finiteEWMatterTransferCarrier`
API that was **never defined** (reference-only phantoms; `git log -S` shows no defining
commit; `HiggsScalarProjectorConstructive.lean` is a `True`-stub):
- `HiggsScalarProjectorDecision.lean` — `ConstructiveScalarProjectorClosure`, `.witness`.
- `HiggsScalarProjectorPositive.lean` — `FiniteScalarProjector`, `finite_scalar_projector_rank_one_no_go`.
- `Book04OperatorBoundary.lean` — `ConstructiveScalarProjectorClosure` (meson rows are real, Higgs row is not).
- `SMActionTermEmergence.lean` — field `projector : HiggsScalarProjectorCertificate`.
- `SMScalarActionCompletion.lean` — `minimalPositiveHiggsScalarProjectorCertificate`.

Missing-module / missing-def imports:
- `FiniteHorizonCapacity.lean`, `FiniteHolographicEntropy.lean` — import the absent
  `D0.Matter.TerminalAlphabetABCD` (file never existed).
- `FiniteMinCutEntropy.lean` — uses undefined `minCutValue`; `cutCapacity` also missing a
  `[DecidableEq V]` instance.
- `FiniteA2EinsteinResponse.lean` — imports absent `D0.Geometry.FiniteWeakFieldQuotient` /
  `GradedBianchiClosure` modules (the `FiniteWeakFieldQuotient` *structure* is real, in
  `FiniteSpin2.lean`, but the module file is not); its main theorem also used a false
  identity-matrix witness for a divergence-free claim.

Broken-theorem scaffold:
- `EchoCapacityHorizon.lean` — `self_similar_horizon_is_capacity_null_boundary` tries to use
  the `Prop`-typed struct fields `B.horizon.null_boundary` / `terminal_capacity_boundary` as
  *proofs* of themselves (unprovable for a generic `B`); also carried a `_ -> Prop := fun _ =>
  True` placeholder. Its dependency `CriticalCollapseDSS` was repaired (stale `Mathlib.Data.Rat.Basic`
  import -> `Mathlib.Tactic`; dead `: Prop := True` placeholder removed) and stays in the build.

Placeholder / scaffold modules (declarations were `theorem _ : Prop := True`/`by exact True`,
rejected as "type of theorem is not a proposition"; bodies prove nothing):
- `VacuumFeedbackEquationOfState.lean` — broken struct field + 5 `: Prop := True` placeholders;
  duplicated `finite_pvt_equation_of_state` with the real `FiniteFeedbackEquationOfState`.
- `TickS3BaryonAsymmetry.lean` — `: Prop := True` placeholder + `rfl`-after-`simp` (no goals).
- `HodgeMatterGravityArchiveIndex.lean` — all 4 declarations are vacuous `: Prop := by exact True`.
