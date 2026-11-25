# D0 Lean formalization

This package is the v12 Lean formalization workspace for the D0 corpus.  The
release core is theorem-bearing Lean code; bridge files expose assumptions
explicitly instead of promoting external physics or empirical pipelines into
core theorems.

## Check a change

Use the Lean toolchain and Lake manifest checked into this directory. The Python
checks below use the CI baseline, Python 3.11. From the repository root:

```bash
python 03_FORMALIZATION/tools/check_no_sorry_in_core.py --all
python 03_FORMALIZATION/tools/check_claim_map_coverage.py
python tools/generate_lean_views.py --check
```

On Unix, use the project's build helper to serialize access to the Lake cache:

```bash
python tools/lean_task_build.py narrow D0.Algebra.AlbertJordan
python tools/lean_task_build.py final
```

For a direct Lake invocation, including native Windows:

```bash
cd 03_FORMALIZATION
lake exe cache get  # optional Mathlib cache
lake build D0.All
```

## Build-cache policy

For a proof edit, build the affected module while iterating. Run the incremental
`D0.All` build once after narrow checks pass. GitHub's D0 Lean workflow supplies
the independent integration build when the formalization changes. The
[validation budget](../00_WORK/README.md#validation-budget) defines the checks
for other surfaces.

Keep the pinned manifest and reuse the Lake and Mathlib caches. A fresh build
is useful when toolchain or dependency inputs change or cache corruption has
been confirmed. Keep generated Lake artifacts and certificate outputs outside
version control.

## v12.17 Branch-Defect Projective Generation

The generation index is now represented by the projective closure of the minimal two-branch defect plane over `F₂`.  The Lean core proves that the nonzero projective branch-defect rays are exactly three and that the canonical companion/defect action cycles them with order three.

Core theorem layer:

- `D0.Spectrum.BranchDefectProjectiveGeneration.branchRay_card`
- `D0.Spectrum.BranchDefectProjectiveGeneration.exactly_three_projective_branch_defect_generations`
- `D0.Spectrum.BranchDefectProjectiveGeneration.defectAction_order_three`
- `D0.Spectrum.BranchDefectProjectiveGeneration.defect_generation_card`
- `D0.Spectrum.BranchDefectProjectiveControls.branch_defect_projective_proof_closed`

Scope boundary: the index `3` is core; mass hierarchy, Yukawa structure and empirical generation clustering remain outside this theorem.
