# #334 post-8da source intake

This packet preserves the seven-commit range
`8daed32d560df18837bcc69458a8fa538a9cf135..523d2cbcc0a9771ea40faa4a2eac84cc78704b0e`
from open Draft PR #334. The seven changed paths are stored byte-for-byte under
`upstream/`; `UPSTREAM_SOURCES.zip` also includes the exact original constructor
input from commit `1e6420f319d714be53363a77823f76ec620a6473`. The full binary
patch and ordered commit list are retained separately.

## Replay

`replay/work/check_prefix_recovery.py` and its `inputs/check_history_source.py`
are exact source copies. The checker was run locally in normal and optimized
Python modes. Both runs report `PASS_COMPLETE_FIXED_PREFIX_COVECTOR_RECOVERY`
with 69 checks, and their JSON output files are byte-identical. The local
runtime was Python 3.9.6, NumPy 2.0.2, SciPy 1.13.1, SymPy 1.14.0, and mpmath
1.3.0. The owner receipt records Python 3.13.5, NumPy 2.3.5, and SymPy 1.14.0.
Owner and local JSON are therefore not byte-identical: environment labels
differ, and 15 floating fields differ at most `1.5543122344752192e-15` in
absolute value (the finite-difference error changes by `7.0586961263845085e-19`).

Each local run also emitted 120 NumPy `RuntimeWarning` records at 40 matrix
multiplication sites, for divide-by-zero, overflow, and invalid-value flags.
The exact stderr is retained in `replay/normal_stderr.txt` and
`replay/optimized_stderr.txt`; the warnings were not suppressed. The checker
completed with its recorded status, but these diagnostics remain a replay
caveat and are not labeled harmless by this intake.

Replay from the repository root with:

```sh
cd 02_REGISTRY/research/sources/d0_334_post_8da_delta_2026-10-28/replay/work
python3 check_prefix_recovery.py > ../normal_output.json 2> ../normal_stderr.txt
python3 -O check_prefix_recovery.py > ../optimized_output.json 2> ../optimized_stderr.txt
```

The `explore_original_full_source.py` exploration was preserved but not rerun
locally because PyTorch is unavailable in this runtime. Its seven-scale
candidate is not a full root; the recorded unrestricted all-280-row solve
failed and left the positive-orientation chart. The original exploration JSON
and failed-solve receipt remain unchanged under `replay/` and `upstream/`.

## Scope

The result extends the inherited cumulative source-limit theorem to all
directions of one arbitrary regular finite original prefix. It keeps that
prefix's source rows and shows their normalized dual norm is bounded by
`C_xi/Lambda`; repeated genuinely paid blocks make this fixed-prefix term and
the full internal-heat term vanish along the stated cumulative sequence.
It does not eliminate a non-Einstein field source or new independently free
apparatus rows in each block. It proves no exact finite stationary word and
does not establish physical admission, the full original 42-field execution,
or GR closure. `GR_closed=false`.

`verify_source_delta.py --verify-source-objects` checks the manifest, all
source and replay bytes, the pinned Git commits and blobs, and the exact patch.
The intake remains supporting research; it adds no Lean theorem, claim,
formal-support row, assembly acceptance, or lifecycle promotion.
