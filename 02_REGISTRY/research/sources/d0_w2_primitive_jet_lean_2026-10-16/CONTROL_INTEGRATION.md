# CONTROL integration of ordered primitive words and first jets

Date: 2026-10-20. Execution: existing PR #342,
`WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION`.

This intake registers the completed bounded algebraic theorem. The original
Lean module, `RESULT_RU.md` and candidate note are preserved unchanged. Their
historical statement that CONTROL registration remains outstanding is resolved
by this integration, without rewriting the original report.

## Exact inputs and preserved result

Original published worker head:
`9e3073851e9fa59d3564caeb02a8a5cb4d6d936b`.

Initial prepared dependency: the published #353 checkpoint
`16b8b0b749dc49554ee521ca0aa97c6bc06bb5c4`, containing then-main
`e9d81e07deff2c51c17a312332fa5260a0a833b3`. CONTROL allowed the combined
formal closure to compile while #353 awaited acceptance and merge.

Actual main integration parent:
`cf25e1dd18d3de5f259b7b9041bf778b8254e96a`, after #353 was accepted and
merged. The refresh preserves that accepted application and its independent
decision. All formal inputs, including the generated `D0.All`, are unchanged
from the published Ready build head
`7dad5382aff9a80d3fea2daa293739679034f8c4`; the refreshed assembly and
provenance metadata do not introduce a new mathematical build result.

The Lean owner is
`03_FORMALIZATION/D0/Research/PrimitiveJetComposition.lean`, SHA-256
`4e93661bd8d4f4a8402b9f177fbe0e1e2f8e635adb9622f541ad84abe1499731`.
`RESULT_RU.md` has SHA-256
`3135758a3573bd6949f526fde90a0d664e798afd597f9c55445aa43458b10a41`.
Both are byte-identical to the published worker head. No proof, expected
scientific result or claim statement is changed.

For any finite ordered word in one ring, `wordResidual_eq_orderedSum` gives
the exact ordered telescoping identity. The distinct-vertex version is
`movingWordResidual_eq_orderedSum`, for the endpoint residual
`V_w I_m - I_0 U_w` and one-step terms `V_k I_(k+1) - I_k U_k`.
`jet_movingWordResidual_eq_orderedSum` applies this identity in the first-jet
ring; `movingStepResidual_deriv` keeps both adjacent derivatives. The fixed
family remains a separate, explicitly proved specialization.

The proof preserves noncommutative factor order. Its existing 2-by-2 controls
distinguish reversed factors, a frozen derivative, a shared intertwiner and
different vertex intertwiners. No new primitive catalogue is introduced.

## Precise norm and comparison scope

With the supplied `NormedRing`/`NormOneClass`, contraction and one-step
residual bounds, `movingWordResidual_norm_le` gives the moving-vertex value
estimate. The numerical derivative estimate `jet_wordDeriv_norm_le` concerns
one shared parameter-dependent intertwiner. An estimate for the derivatives
of arbitrary unequal vertex intertwiners is not claimed; their exact jet
identity is proved.

`BranchAgreement` and `ComparisonHypothesis` expose separately supplied
propositions. Their fields do not prove an actual physical instrument or a
comparison map. Labels, preparations, tests, adjacent carriers, endpoint
readings and postselection normalization are not inferred from a zero word
residual. The theorem covers an ordered word in one ring, without asserting
a general tensor/parallel-program theorem or transport across different
physical carriers.

## Parent substitution and acceptance boundary

Phase: interpretation and generic transfer.

The exact submitted slot is `primitive_jet_composition`, on `word-jet-v1`,
using its existing `direct` method. The application
`lean-primitive-jet-composition-to-word-slot` maps the algebraic domain,
supplied norm bounds and branch/comparison hypotheses to the named domain of
that same scoped obligation. The original task statement, work key and
completion premise are unchanged.

This supplies the generic ordered-word and first-jet composition theorem for
the current route. Its intended physical consumer remains `native_sector`:
the actual typed native maps, their physical admission and their instrument
agreement must still be supplied and applied. No v8 primitive, native action,
physical source or GR closure is obtained by this intake.

The application is now `accepted` for `primitive_jet_composition` only. The
independent [decision](../../../gr_assembly/reviews/lean-primitive-jet-composition-to-word-slot.md)
is pinned at `8a49edff2a32810d6fc16379f1efba2ea85b3998` and binds the exact
application digest
`2fd27f22e6d5da240a116a56a372d01d9605bc03fcd070654fbeacceebe74e2d`.
Activation followed the separate successful actual Lean integration build
recorded below. Queue retirement and this accepted substitution complete the
original bounded worker; the physical consumer and its native maps remain open.

## CONTROL changes and validation boundary

- Register the unchanged module as `EXPLICIT_SUPPORT` and regenerate `D0.All`.
- Preserve current main's strategy and queue; retire only the
  original #342 task through the lifecycle helper and regenerate work views.
- Add one typed result and its scoped application pinned to the original
  published source. Use the second of the two capacity places explicitly
  reserved by #353: 52 active results under the unchanged limit of 52.
- Retain all evidence, hypothesis and acceptance gates.

The original published report records a narrow Lean build with 1475 jobs and
standard axioms, without `sorryAx`. This integration environment has neither
`lake` nor `lean` nor a populated `.lake` cache; no new local Lean success is
claimed and no toolchain is installed.

The actual Ready GitHub CI build passed in
[run 39408876490](https://github.com/gvakhrushev/d0_15/actions/runs/39408876490),
associated with published head
`7dad5382aff9a80d3fea2daa293739679034f8c4`. The completed log records
compilation of `D0.Research.PrimitiveJetComposition` and a successful `D0.All`
build with 4552 jobs. Job `118581429089` and its actual
`Build release proof closure` step both succeeded; the build step completed
at 2026-10-20 11:18:17 UTC and the run at 11:18:20 UTC.

The full `03_FORMALIZATION` tree, formal-support registration and Lean build
workflow are byte-identical to that Ready head. The subsequent changes are
assembly acceptance, independent review and integration provenance only.
This records actual compilation on unchanged formal inputs; a skipped metadata
check is not used as build evidence. Local validation covers the affected
structural, assembly, lifecycle and generated-view gates.

Local checks passed on the initial prepared integration tree:

- `python3 tools/validate_repo.py` — 889 claims, 174 formal-support entries,
  909-module closure, zero errors and warnings.
- `python3 tools/validate_work.py` and `python3 tools/validate_agent_protocol.py`.
- `python3 tools/gr_assembly.py check` — 52/52 active results; the proposed
  applications do not change the accepted/discharged set.
- `python3 tools/gr_assembly.py render --check`,
  `python3 tools/render_work_status.py --check` and
  `python3 tools/generate_lean_views.py --check`.
- `git diff --check` against the prepared dependency, and exact byte comparison
  of the module, original RESULT and candidate note with the worker head.

After the actual-main refresh and scoped acceptance, the affected repository,
work, agent, assembly and generated-view checks passed again. The assembly
contains 52/52 active results and three discharged scoped obligations; this
activation adds only `primitive_jet_composition`. The exact application digest
is unchanged. `native_sector` and all physical GR obligations remain open.
