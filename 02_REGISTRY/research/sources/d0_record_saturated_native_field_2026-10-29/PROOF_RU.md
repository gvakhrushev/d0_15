# Record-saturated native field stencil: local replay intake

## Upstream source and statement

The existing [#334 owner](https://github.com/gvakhrushev/d0_15/pull/334)
added `check_record_saturated_field.py` at commit
[`418afd58c741713a60036a90f8246060d774fd56`](https://github.com/gvakhrushev/d0_15/blob/418afd58c741713a60036a90f8246060d774fd56/02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/check_record_saturated_field.py).
The file is pinned by Git blob
`81d78ce6ebcc3e9d98bceaacbd61ed0328943da9` and SHA-256
`618d1d6267739e7468fea7c0108be22cff448c8d9abac28110081854ca502b65`.
Owner source pin: `02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/check_record_saturated_field.py` commit `418afd58c741713a60036a90f8246060d774fd56` blob `81d78ce6ebcc3e9d98bceaacbd61ed0328943da9`. The checker covers fixed-Golden native source stencils with an actual retained record; all expanded calls are positive G/CX/SourceI. Large repeats are specified, not iterated or claimed run on hardware. Its 42-variable test is a local Palatini jet, not a lattice GR root or runtime quantum field decoder.
The checker fixes its input commit at `4b30fcb4dc743e7a04415c9701aae19a847e8dab`,
an ancestor of the owner commit. That owner commit adds the checker, not a
published result receipt; the JSON output preserved here is a local replay.

The exact checker first builds a 16-call positive `G/CX/SourceI` word on its
declared seven active wires. It verifies the literal endpoint identities,
the retained click law, the saturated joint record, the complete endpoint
cotangent identity and the 16 independent primitive-occurrence pullbacks.
The inactive blank multiplicity and 65,536-dimensional work carrier are
reported algebraically; the checker does not diagonalize the full clock.

It then tests 42 independent pointwise Palatini coordinates at one fixed
field point: 16 coframe, 24 connection and two matter coordinates. For each
coordinate it compares an interval-certified derivative of the full recorded
source with the two compiled field values at displacement `h=1/1000`.
The numerical words use odd powers of the original Golden rotation and a
matched primitive inventory. The checker emits 85 compact word descriptions
(the centre and the two stencil endpoints for each of 42 coordinates).
Their reported common inventory has
`11,177,567,015,642,288` positive calls per word. This is compact repetition
notation; the large words are not expanded or run on hardware.

## Local replay

The exact pinned checker was run in ordinary mode, with `-O`, and once more.
All three executions returned code zero and identical stdout, `result.json`
and `programmes.json`. They reported 867 checks,
`max_coordinate_error = 8.1894604955210760e-14`,
`dual_max_norm_error = 6.7387704951582848e-13`, and the reported
`dual_max_norm_proved_bound = 1.2147724375054815e-12`. The saved result also
retains a positive actual stage-15 `G` source (`7.413764171516666e-6`) and
the exact-inventory/zero-heat comparison used by this finite certificate.

The local environment emitted NumPy `RuntimeWarning`s for divide-by-zero,
overflow and invalid values at matrix multiplications. These stderr logs are
preserved for all three runs. The checker exited successfully, its structured
JSON contains only finite numeric values, and repeated outputs agree; however,
the cause of the warnings is unresolved, so this intake does not claim a
warning-free replay or establish that the warnings are harmless. The original
#334 commit does not contain a result receipt for comparison. See
[`replay_manifest.json`](replay_manifest.json) and
[`source_manifest.json`](source_manifest.json) for runtime versions and hashes.

## Scope and unresolved application

This is a source-verified finite calculation for the declared record-saturated
word and its 42 pointwise coordinate stencils. It is not an original 42-row
finite-mesh Euler solve, a runtime field reader/compiler, or a proof of the
physical variational domain. The checker explicitly leaves `Lean_or_CI_run`,
`same_runtime_field_compiler_proved`, `physical_variation_domain_derived`,
`new_all42_stationary_root` and `GR_closed` false. The checker’s local pass
does not bind this stencil to physical execution, selected Book03 `Cost-Info`,
clock/boundary equations, or nonlinear GR refinement.

This result supplies a potential quantitative source comparison to the
existing #334 native-word work. Before using that comparison as a parent
substitution, resolve the local NumPy warnings and prove the transport from
this fixed field point/stencil to the actual admitted source and its full
physical variation domain. The independent upstream-preparation and paid
return-record results remain scoped to their own declared executions.

No task or assembly edge is added. `WRK-D0-PROOF-ARCHITECTURE-FORMALIZATION`
remains in progress and `GR_closed=false`.
