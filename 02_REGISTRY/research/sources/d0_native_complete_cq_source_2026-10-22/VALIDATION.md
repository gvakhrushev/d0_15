# Frozen packet validation and integration record

22 October 2026. Existing Draft #334. This file reports execution evidence;
it is not a new numerical expected receipt or a physical acceptance claim.

## Final affected replay

The repository's `run_research_certs.replay` runner executed **only**
`a4d_native_complete_source_reduction_check.py` in its own detached worktree.
The local committed scientific snapshot was
`20a524ad2b54dc7c4ee45f235d212f1a9e71107a`, tree
`7f54b8038a6c2657818b7e067980c124ca8ec470`. This is the local verification
snapshot, not a claim that its commit ID is the published remote head.
The durable exact scientific input identities are in `SOURCE_PINS.json`;
the separately committed integration notes do not change them.

Result: **PASS**, return code 0, **173 scoped checks**, 32.948 seconds.
The runner reported `tracked_mutation=false`, with the detached HEAD
unchanged. The wrapper verified all 35 declared inputs before and after
execution, including the immutable expected receipts and source manifest.

```text
PASS check_cut_source_equivalence.py: 100 scoped checks
PASS check_maximum_entropy_preparation.py: 23 scoped checks
PASS check_complete_history_source.py: 50 scoped checks
PASS 173 bounded checks; exact input provenance; immutable receipts
SCOPE: actual cut / marginal / complete history; physical Book03 selection and GR remain open.
```

The runner's complete stdout file has SHA256
`de48742c8ac365f56cf6596d28c025ea395850f91d161541bd8c91355b6a6a97`.
The arithmetic environment was Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0.
The wrapper restricts BLAS/OpenMP worker counts to one for these small
matrices. Mathematical and replay tolerances are separately documented
in the proof files, checkers and README.

Author-level ordinary and optimized runs, and the independent affected
replays, are recorded in the three corresponding review files. The final
integration review is [INTEGRATION_INDEPENDENT_REVIEW.md](INTEGRATION_INDEPENDENT_REVIEW.md),
SHA256 `fdcd3a26a475b89255d7a61f12df9f3e331c04c014bff8fb3397db1ddf3a735a`.
It is an external review record, not a self-referential manifest input.

## Hostile replay and structural controls

Four in-memory receipt controls under optimized Python each raised an
explicit failure as required: changed `GR_closed`, changed check count,
a nonfinite numerical source, and changed regularization eta. No expected
receipt was modified to perform these controls.

The affected structural checks passed:

- `python tools/validate_repo.py`: zero warnings.
- `python tools/validate_work.py`: work plane valid.
- `python tools/validate_agent_protocol.py`: task/assembly protocol valid.
- `python tools/gr_assembly.py render --check`: generated view current.
- Python AST parsing of the four new entrypoints and the new Markdown
  files' relative links passed.
- `git diff --check` passed for the committed packet.

The shallow local checkout initially lacked existing assembly evidence
commits. Their exact published objects were retrieved from the other local
checkout; the validator then passed without changing any evidence pin or
assembly contract.

The concurrent branch had three manually added navigation entries in the
generated `gr_assembly/SYNTHESIS.md`. Canonical rendering removed those
out-of-model entries so that the generated-view gate passed. All three
source documents remain unchanged; their navigation and source distinctions
are preserved in the primary scientific memo and the later intake here.
No scientific result, assembly status, queue state or claim was retired.

The later stopped-source intake also identified one narrow wording error
in the concurrent KL source note: its reference-gradient cancellation is
pointwise at a stationary base state and therefore also holds for tangents
leaving the stationary family. The source of the separate price-defect
term need not vanish on those tangents. That sentence in the live KL note
was corrected explicitly; its occupation, price-defect formulas and
numerical checker were not changed or rerun.

No previous geometric root, interval certificate, all42 calculation,
full research suite or Lean build was rerun. The separate concurrently
published calculations are consumed at their stated refs and scopes.
`GR_closed=false`.
