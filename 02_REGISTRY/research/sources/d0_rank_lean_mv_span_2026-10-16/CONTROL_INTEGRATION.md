# CONTROL integration of the generic Hermitian tangent-span theorem

Date: 2026-10-20. Execution: existing PR #353,
`WRK-A4D-LEAN-MV-TANGENT-SPAN`.

This intake integrates the completed bounded theorem into the current formal
closure. It preserves the original result and Lean source; the candidate note receives
one editorial cleanup of stale directory-name prose, described below.
The blocker recorded in `RESULT_RU.md` was the remaining CONTROL registration;
that historical report is retained unchanged.

## Exact inputs and result

Original published worker head:
`304a6dd3c53b7cf3c35353fbdc40aa0444fc77ec`.

Integration main parent:
`e9d81e07deff2c51c17a312332fa5260a0a833b3`.

The Lean owner is
`03_FORMALIZATION/D0/Research/MemoryTangentSpan.lean`, SHA-256
`c7b8ac25b6dbc20752e95ebe6d5220fb82170d0c6baccf51bc5416f8f47f78fa`.
Its bytes are identical to the published worker head. `RESULT_RU.md` is also
byte-identical, with SHA-256
`1fb8745e7674ac534695cbc1fc6aa00ca9d761853cafb0d3b88e73d4d6e29150`.
No proof, expected scientific result or claim statement is rewritten by this
integration. The first paragraph of `CANDIDATE_NOTE.md` no longer repeats three
obsolete directory-path tokens from another layout: it says that those paths
were absent and that the current registries were searched. All mathematical
content is unchanged; the exact original note remains at the published worker
head. The architecture firewall is unchanged.

For any fixed finite index type and Hermitian complex matrices
`J1`, `J2`, `J3`, `M`, the theorem states that `Tr(S M)=0` for every
Hermitian traceless source-neutral `S` if and only if
`M` is in `span_R{I,J1,J2,J3}`. No independence of the source triple is
assumed. The real vector space in `mv-span-v1` is the Hermitian matrix space
over real scalars; the interface now spells out that convention explicitly.

The main theorem is `trace_vanishes_iff_memRealSpan`; its two directions are
`memRealSpan_of_admissible_trace_vanishes` and
`admissible_trace_vanishes_of_memRealSpan`. The existing controls distinguish
source neutrality from mere tracelessness and a full matrix identity from a
single-ray identity. The proof uses the real trace pairing and its
nondegeneracy on Hermitian matrices.

## Parent substitution and acceptance boundary

Phase: interpretation and generic transfer.

The exact submitted slot is `mv_tangent_span`, on `mv-span-v1`, using its
existing `direct` method. Application
`lean-memory-tangent-span-to-mv-slot` maps both finite-index and Hermitian-data
hypotheses to the named mathematical domain of that same scoped obligation.
It does not introduce an external physical assumption. The original task's
statement, work key and completion premise are unchanged.

This supplies the generic algebraic test available to the source and dynamical
compatibility step in the current route. Its intended physical consumer remains
`matter_source_ward`. Substituting actual native `M_v` and source matrices,
establishing the physical tangent class and proving the source/Ward map remain
separate work. This application does not discharge `matter_source_ward`,
`native_sector`, the original raw terminal or GR.

The application is now `accepted` for `mv_tangent_span` only. The independent
[decision](../../../gr_assembly/reviews/lean-memory-tangent-span-to-mv-slot.md)
is pinned at `16b07f9fb6abae4369e2457e28f9a0e20254b992` and binds the exact
application digest. The separate actual Lean integration build also passed,
as recorded below. Queue retirement and this accepted substitution complete
the original bounded worker; physical instantiation remains open.

## CONTROL changes

- Register the existing module as `EXPLICIT_SUPPORT` and regenerate `D0.All`.
- Preserve current main's strategy and queue when resolving the three generated
  work/status conflicts; retire only this original bounded worker task through
  the lifecycle helper.
- Add one typed result and its scoped application with immutable evidence pinned
  to the original published worker head.
- Increase the active-result capacity explicitly from 50 to 52 for delivery of
  the two already registered, completed bounded Lean tasks #353 and #342.
  This PR uses one place; the other remains available for #342. No unrelated
  result is removed, and all hypothesis, evidence and acceptance gates remain.

## Validation boundary

The original published `RESULT_RU.md` records the narrow Lean build with 2949
jobs and standard axioms, without `sorryAx`. The integration environment has
neither `lake` nor `lean` nor a populated `.lake` cache. No new local Lean
success is claimed, and no toolchain is installed for a repeated proof build.
The unchanged theorem must be checked in the final imported closure by the
exact-head GitHub Ready CI before merge. Local verification covers the affected
structural, assembly, lifecycle and generated-view gates.

Local checks passed on the integration tree:

- `python3 tools/validate_repo.py` — 889 claims, 173 formal-support entries,
  908-module closure, zero errors and warnings.
- `python3 tools/validate_work.py` and `python3 tools/validate_agent_protocol.py`.
- `python3 tools/gr_assembly.py check` — 51/52 active results; the existing one
  discharged obligation is unchanged because this new application is proposed.
- `python3 tools/gr_assembly.py render --check`,
  `python3 tools/render_work_status.py --check` and
  `python3 tools/generate_lean_views.py --check`.
- `git diff --check` and exact byte comparison of the Lean module and
  `RESULT_RU.md` against the published worker head.

The first repository check exposed obsolete-directory prose in the candidate
note; the one-sentence editorial repair above resolved it without changing the
validator or any mathematical assertion.

## Final integration acceptance

Actual GitHub Ready run [39407194430](https://github.com/gvakhrushev/d0_15/actions/runs/39407194430/job/118575884394)
compiled the release closure on published head
`16b8b0b749dc49554ee521ca0aa97c6bc06bb5c4`. The build step completed
successfully on 2026-10-20 at 10:51:50 UTC; its log records `D0.All`
and `Build completed successfully (4551 jobs)`. This was an executed build,
not a skipped workflow step. Ready guards on that head also passed.

The later acceptance commit changes only the pinned review, application review
block and generated/documentation views; all formalization inputs remain
byte-identical to that compiled head. The accepted application discharges
`mv_tangent_span`; the previously accepted C2 obligation stays accepted.
`matter_source_ward`, native dynamics and GR retain their existing open scope.
