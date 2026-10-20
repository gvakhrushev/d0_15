# Bounded independent main-intake review

20 October 2026. Reviewer: relational_history_bridge.

This review verifies the bounded transfer into main and preservation of
the already reviewed scientific scope. It does not replace the independent
analytical reviews in INTEGRATION_REVIEW.md, repeat the author's own
mathematics as an independent proof, or claim physical GR closure.

## Exact base and source

- Main base: 257fd52fe37889be3e020b3bc1a002330ae67539.
- Intake branch: control/native-gr-source-synthesis-intake-2026-10-20.
- Scientific source commit: 00ba40744b377c30eb2c03d03bb2106fc121ff02.
- The source worktree was at 2300da098f3c5d35a857247e48d765f7f374c42f
  during the copy. Every copied file was independently compared with
  the named scientific source commit; subsequent unrelated native
  changes were not included.

Native publication provenance and the integrating CONTROL PR are recorded
separately by the integrator. This local intake review does not assert
that either this branch or the source commit has been published.

## Exact transfer and entrypoint boundary

PASS: 43 files were copied byte-for-byte from the source worktree and
matched the exact source-commit blobs:

- the main A4D_CAUSAL_BOOK_SOURCE_TO_EXACT_GR_SYNTHESIS_2026_10_20.md;
- all 41 files of d0_native_gr_completion_synthesis_2026-10-20;
- a4d_native_gr_completion_synthesis_check.py.

The four existing main documents contain only the insertion blocks from
that source commit. Removing those blocks restores the original main
bytes exactly:

| Maintained document | Inserted lines |
|---|---:|
| AGENTS.md | 10 |
| README.md | 2 |
| D0_GR_PRIMARY_POSITIVE_CASE.md | 12 |
| MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md | 28 |

No existing line was removed or replaced. The current main route and its
prior accepted material remain intact. The copied main synthesis section 7
and REFERENCE_COMPOSITION_REVIEW.md retain the precise reference-cocycle
qualification; the concurrent canonical reference-cocycle note was not
imported.

The intended final scope at this handoff is 48 files: the 43 exact copies,
four insertion-only maintained documents, and this intake review. The
integrator may add the separately authorized main provenance metadata.
No queue, task brief, assembly contract, acceptance, claim, canonical book,
Lean, tooling, CI or other native research file was changed.

## Structural and metadata evidence

The following commands ran in this intake worktree. Each returned 0:

| Command | Actual result |
|---|---|
| python3 tools/validate_repo.py | PASS; warnings=0 |
| python3 tools/validate_work.py | PASS; active work plane clean |
| python3 tools/validate_agent_protocol.py | PASS; cold-start metadata enforced |
| python3 tools/gr_assembly.py check | valid=true; discharged=5, obligations=22; scientific_promotion=false |
| python3 tools/gr_assembly.py render --check | generated assembly view current |
| python3 tools/render_work_status.py --check | PASS; stale=0 |

A read-only comparison verified every copied byte against both the
source worktree and the named commit. A separate static AST read of the
copied certificate verified its complete declared input set and all
36 immutable SHA256 pins without importing or executing the checker.

The bounded Markdown check covered the four maintained entrypoints, new
synthesis and packet metadata, causal proof, and three new scientific
proofs: 13 documents, 149 links, including 120 local targets and heading
anchors. No missing target or anchor was found. Frozen historical input
bodies were not traversed for link repair and their bytes were unchanged.
This review adds no Markdown links.

No mathematical suite, new certificate replay, historical replay or Lean
build was run for this identical-byte transfer. The source packet retains
the integrator's frozen FINAL_REPLAY.json and all checker/receipt pairs;
these are preserved source evidence, not a new intake execution claim.

## Scientific and lifecycle scope retained

The known CAR reporting source is a component of the complete price on
the supplied coherent interface. The full absolute Book Info/work effect,
native primitive admission, genuine upstream preparation sources, matter
coefficients and prospective selection remain obligations.

The causal proof preserves all 16+24+2 source rows and the actual
coefficient ratio required by the same midpoint representative. It does
not infer global minimal selection from stationarity. The actual return,
cost marker, relative statistic and complete physical price are not
identified without their proved same-execution binding.

This is a bounded CONTROL intake of the existing PR #334 research result.
It creates no new lifecycle task, retires no existing research owner and
promotes neither GR, positive_gr, raw216 nor assembly acceptance.
No commit, push, PR creation or merge was performed by this reviewer.

**Decision: PASS for bounded main integration at the stated source and
base, with no intake blocker found.** Publication and final remote/CI
verification remain with the integrator.
