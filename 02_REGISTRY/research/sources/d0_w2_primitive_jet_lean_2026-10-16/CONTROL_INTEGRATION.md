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

Prepared integration dependency: the published #353 checkpoint
`16b8b0b749dc49554ee521ca0aa97c6bc06bb5c4`, which contains main
`e9d81e07deff2c51c17a312332fa5260a0a833b3`. This is an explicitly prepared
dependency while #353 awaits final acceptance/merge. CONTROL permits this
prepared branch to reach Ready against actual main
`e9d81e07deff2c51c17a312332fa5260a0a833b3` so its combined formal closure can
compile independently while #353 is reviewed. This does not permit merging
#342 before #353: before merge, refresh with final main containing #353's
acceptance and update the PR baseline. The original formal inputs are already
present through the prepared dependency; acceptance/provenance updates alone
do not assert a new mathematical build result.

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

The application is submitted as `proposed`. The original bounded task can be
self-retired as a complete scoped submission; independent pinned acceptance
of this exact application remains necessary for scientific delivery. Neither
a green build nor the task's retirement accepts a physical parent premise.

## CONTROL changes and validation boundary

- Register the unchanged module as `EXPLICIT_SUPPORT` and regenerate `D0.All`.
- Preserve the prepared dependency's strategy and queue; retire only the
  original #342 task through the lifecycle helper and regenerate work views.
- Add one typed result and its scoped application pinned to the original
  published source. Use the second of the two capacity places explicitly
  reserved by #353: 52 active results under the unchanged limit of 52.
- Retain all evidence, hypothesis and acceptance gates.

The original published report records a narrow Lean build with 1475 jobs and
standard axioms, without `sorryAx`. This integration environment has neither
`lake` nor `lean` nor a populated `.lake` cache; no new local Lean success is
claimed and no toolchain is installed. Exact-head Ready GitHub CI must check
the imported `D0.All` closure before merge. Local validation covers the
affected structural, assembly, lifecycle and generated-view gates.

Local checks passed on this prepared integration tree:

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
