# Native checkpoint: preserved inputs and current compatibility

This is the bounded integration of #322 with main
`e9d81e07deff2c51c17a312332fa5260a0a833b3`. It changes replay provenance, not
the scientific scope of the results. Native physical selection, source, joint
dynamics, refinement, G0 and GR retain their existing open obligations.

## Why this source has a version

Published #322 head `64cbac8d17028376ba2e5324da5014ebcfa053b1` contains compiled
receipts for an earlier `EndogenousActionQuantum.lean`. Main #375 adds explicit
action underdetermination and homogeneity boundaries. Those additions remain
on main; the older receipts retain the exact source they actually certified.

| Input | Exact identity |
|---|---|
| Historical source commit | `64cbac8d17028376ba2e5324da5014ebcfa053b1` |
| Historical Git blob | `dab5b67300a70768e0211159deb2ac6e53fa7b29` |
| Historical SHA256 | `692f2b5929b001361a2f22d7dc224fba46a80738036f26a1ff7bdd5175fc80c4` |
| Maintained SHA256 at integration | `5ca12d6190aca5f75a898e1e7a5c1296a71ed1ff04b963bd3df32f34e8569e94` |

The [snapshot](EndogenousActionQuantum.lean) is byte-identical to the published
blob. Its source-time prose is historical; #375's narrower current interpretation
remains in the maintained owner. The [manifest](HISTORICAL_INPUT.json) binds
seventeen source receipts, eleven entrypoints, ten current-compatibility
Lean capsules and the two report headers below. The only changed receipt is the new field-coupling relocation
record described below; older receipts and checker bytes remain unchanged.

Two receipts also pin the earlier
[common-action report](APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md).
This 1,767-byte snapshot has Git blob
`dc59c6cdcdd3d2d1d1e4460ec74e456918359abc` at the same published #322 head and
SHA256 `b95d5f631fb9c5936fe61964e73c3f373ea3f9deefb0fae037c7a760d6535ff5`.
It is a historical input, never the current scientific route. Main's maintained
report (integration SHA256
`645fb50cb991c1e590a752354837bc6db9d14db2c2c5168045c2da0bbf0844e3`)
retains #375's clarified boundaries and its added owner references. Only
`a4d_native_history_action_check.py` and
`a4d_native_dynamical_ownership_check.py` use this second overlay; their original
`_certificate.json` headers remain byte-identical. The fixed report source,
two-entry map and two receipt hashes are validated before either overlay.

The last #322 commit also appended section 7 to a memo pinned by five earlier
certificates. That section is now in
[its own owner](../../A4D_NATIVE_HISTORY_FIELD_COUPLING_BOUNDARY.md). The earlier
memo and five certificates are restored/preserved byte-for-byte. Only the new
field-coupling checker's report path and its own relocation receipt changed,
with original source hashes retained in its provenance.

## Bounded historical replay

The existing isolated runner has one explicitly scoped binding for:

- `a4d_native_addressed_third_role_check.py`
- `a4d_native_archive_apparatus_realization_check.py`
- `a4d_native_code_price_resolution_check.py`
- `a4d_native_dynamical_ownership_check.py`
- `a4d_native_history_action_check.py`
- `a4d_native_history_field_coupling_check.py`
- `a4d_native_prepared_action_check.py`
- `a4d_native_scene_payload_action_check.py`
- `a4d_native_uniform_memory_actuation_check.py`
- `a4d_native_verified_archive_actuation_check.py`
- `d0_native_tangent_source_preflight_check.py`

The retained-record certificate is the seventeenth receipt. Its entrypoint
remains ordinary and receives no overlay: its default finite replay passed
on main, whereas the eleven entries above failed historical source/header
checks after #375. All seventeen recorded historical receipts remain bound.

Before execution the runner verifies the snapshot, entrypoint, every bound
receipt and capsule. It changes one source path inside a disposable worktree,
plus the explicitly bound report only for the two entries just named. It
logs both source hashes and source commit in `historical-input.json`, and labels
the run `HISTORICAL_COMPILED_INPUT_REPLAY_NOT_CURRENT_SOURCE_PROOF`; the report
record is labelled `HISTORICAL_REPORT_INPUT_NOT_CURRENT_ROUTE`. It restores
the maintained bytes before ordinary mutation checks. If the checker changes
the overlay, that is a mutation failure; restoration cannot hide it. No main
file or old expected receipt is overwritten.

A changed snapshot, entrypoint, bound receipt, capsule, undeclared target path
or changed original action declaration fails the binding. Other consumers use
normal replay. Other shared inputs retain their original checks. Binding
changes add all eleven entries to normal changed-input selection and never
remove existing selected consumers; report-only changes additionally select
the two report consumers. Direct execution against a different
maintained source can still report the original mismatch; use declared
isolated replay for historical receipts and the separate compilation below.

## Maintained-source compatibility

Before overlay, a conservative text check verifies all eleven original
declaration bodies, disregarding comments, whitespace and the added
extensionality attributes. These include `ActionProtocol` and its fields,
`S_min = 1`, the canonical unit action, the action-floor theorem, calibration
and distinction lemmas. #375 adds declarations and an extensionality attribute
without replacing those original definitions or proofs.

That check is separate from compilation. The Lean workflow must build
`D0.All`, then execute:

```sh
python tools/check_native_checkpoint_compatibility.py
```

The command builds actual imports and compiles all ten unchanged research
capsules against maintained sources, with no overlay. It checks compiler exits
and printed axiom dependencies and rejects source changes during execution.
The preflight entry has no Lean capsule. `--interface-only` explicitly reports
a text check; it cannot count as Lean compilation. Historical replay does not
satisfy current compatibility, and neither check promotes a physical claim.

## Acceptance evidence

Acceptance requires scoped historical replay, affected structural/generated
checks and successful current-source Lean CI on the published final head.
Local commits are not publication. The ordinary current-source provenance audit
may still expose the intentional historical difference; the runner's separate
input record states exactly what was replayed, without claiming a proof about
another source version. All original scientific parents remain open.
