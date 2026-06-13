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
