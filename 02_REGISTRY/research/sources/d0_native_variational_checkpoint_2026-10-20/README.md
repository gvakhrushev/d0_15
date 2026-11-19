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
Lean capsules and the three report headers below. The only changed receipt is the new field-coupling relocation
record described below; older receipts and checker bytes remain unchanged.

Three receipts also pin the earlier
[common-action report](APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md).
This 1,767-byte snapshot has Git blob
`dc59c6cdcdd3d2d1d1e4460ec74e456918359abc` at the same published #322 head and
SHA256 `b95d5f631fb9c5936fe61964e73c3f373ea3f9deefb0fae037c7a760d6535ff5`.
It is a historical input, never the current scientific route. Main's maintained
report (integration SHA256
`645fb50cb991c1e590a752354837bc6db9d14db2c2c5168045c2da0bbf0844e3`)
retains #375's clarified boundaries and its added owner references.
`a4d_native_history_action_check.py` and
`a4d_native_dynamical_ownership_check.py` use this report with the source overlay.
`a4d_native_time_field_intertwiner_check.py` uses only the report overlay: its
binding does not read, validate or replace `EndogenousActionQuantum.lean` and
adds no source premise. All three original `_certificate.json` headers remain
byte-identical. The fixed report source, three-entry map, checker hashes and
three receipt hashes are validated before the report overlay.

The third binding addresses the one failure in Ready run
[`39410232456`](https://github.com/gvakhrushev/d0_15/actions/runs/39410232456).
The unchanged time-field checker passed all 163 controls on maintained inputs;
its payload differed from the old ledger only at `input_sha256` for this report
(`b95d5f...` versus maintained `645fb5...`). Its proof, checker, compiler receipt,
remaining six input pins and all result/scope fields were unchanged. It reuses
the exact existing report snapshot; neither the checker nor its expected ledger
is rewritten.

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
plus the explicitly bound report for the two source consumers named above. It
logs both source hashes and source commit in `historical-input.json`, and labels
the run `HISTORICAL_COMPILED_INPUT_REPLAY_NOT_CURRENT_SOURCE_PROOF`; the report
record is labelled `HISTORICAL_REPORT_INPUT_NOT_CURRENT_ROUTE`.
The third consumer has a separate report-only path, validates only the report
binding and logs that report mode directly. Its replay does not require the
historical Quantum source or the ten compatibility capsules. The runner restores
the maintained bytes before ordinary mutation checks. If the checker changes
the overlay, that is a mutation failure; restoration cannot hide it. No main
file or old expected receipt is overwritten.

A changed snapshot, entrypoint, bound receipt, capsule, undeclared target path
or changed original action declaration fails the binding. Other consumers use
normal replay. Other shared inputs retain their original checks. Binding
changes add all eleven entries to normal changed-input selection and never
remove existing selected consumers; report-only changes additionally select
the three report consumers. Manifest and helper changes also select the
report-only consumer without adding it to the eleven source consumers.
Direct execution against a different
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


## Native #334 support-source compatibility — 20 October 2026

The main checkpoint above remains byte-for-byte pinned by
`HISTORICAL_INPUT.json`. Integration with native head
`07f2f2b15b7050a612d0075aa73db8dc46087a95` retains two additional
shift-irrelevance lemmas in the maintained `ArchiveAffineExteriorLink.lean`.
Its source SHA256 is
`2ccca18cf8ca66b9e1aa020301ce0d84d6fcd12563e913323482ce139928e5fe`.
The accepted main exterior definitions are unchanged; the maintained source is
compiled with those additions, without replay overlays.

Three of the already listed historical consumers additionally bind the older
exterior bytes. The [separate support manifest](SUPPORT_INPUT.json) pins exactly
two published inputs from main
`b6a339c303451b18a3ff8c6c42113290fe98307c`:

| Historical consumer | Extra input restored only inside its isolated replay |
|---|---|
| `a4d_native_history_field_coupling_check.py` | `ArchiveAffineExteriorLink.lean` |
| `a4d_native_scene_payload_action_check.py` | `ArchiveAffineExteriorLink.lean` |
| `a4d_native_prepared_action_check.py` | `ArchiveAffineExteriorLink.lean` and its original joint-field-quotient certificate |

The snapshot SHA256 and Git blob identities are fixed in the support manifest
and helper. The original seventeen receipt expectations, eleven checkers and
ten current-compatibility capsules remain unchanged. A text compatibility check
rejects changes to any original exterior declaration; it allows the two added
lemmas and does not replace their current-source Lean compilation. Support
snapshot/manifest/target changes select exactly these three additional bindings.
Other consumers retain their ordinary maintained inputs. Each replay records
the exact historical and maintained input hashes; a mutation of either nested
overlay remains an explicit failure and is not hidden by restoration.

Older main snapshots predate this support bundle. They can replay without it
only when both target files already have exactly the pinned published bytes.
An evolved target with a missing bundle fails instead of silently skipping the
binding. The original ten-capsule compatibility command never applies either
support input.

Native #334 also extended the history-action capsule from 20 to 29 declarations.
Those exact extended source, checker, compiler output and receipts are preserved
in [their versioned native owner](../d0_native_history_action_extension_2026-10-20/README.md).
The associated current mathematical statements and the corrected original-Book
complement convention are in
[the interface extension note](../../A4D_NATIVE_ACTION_INTERFACE_EXTENSIONS_2026_10_20.md).
No older certificate is re-labelled as evidence for the extended capsule.
