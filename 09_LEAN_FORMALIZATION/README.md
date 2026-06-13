# D0 Lean formalization

This package is the v12 Lean formalization workspace for the D0 corpus.  The
release core is theorem-bearing Lean code; bridge files expose assumptions
explicitly instead of promoting external physics or empirical pipelines into
core theorems.

Required checks:

```bash
../tools/lean_dev.ps1 build
../tools/lean_dev.ps1 build D0
../tools/lean_dev.ps1 build D0.All
python tools/check_no_sorry_in_core.py
python tools/check_claim_map_coverage.py
```

Optional acceleration:

```bash
../tools/lean_dev.ps1 exe cache get
```

Known Windows cache issue: `lake exe cache get` may fail when the global
mathlib cache under `~/.cache/mathlib` is inconsistent.  This is a
precompiled-cache download/decompression issue, not a D0 proof-checking
failure, if `lake build`, `lake build D0`, and `lake build D0.All` pass.
Recommended repair is to remove the global mathlib cache, run `lake update`,
run `lake exe cache get`, then run `lake build`.
# Local Lake Storage

This project keeps heavy Lake dependency and build artifacts outside the
repository by default. Lake manages its cache (usually under `~/.lake` or a
location controlled by the `LAKE_HOME` / `LAKE_CACHE_DIR` environment variables).

The committed files are: sources, `lean-toolchain`, `lakefile.lean`, and
`lake-manifest.json`.  A small `.lake/config` directory may appear during
configuration; the full `.lake/` tree is git-ignored and disposable.

Rebuild from a clean checkout:

```bash
cd 09_LEAN_FORMALIZATION
../tools/lean_dev.ps1 update
../tools/lean_dev.ps1 exe cache get   # optional, speeds up mathlib
../tools/lean_dev.ps1 build
../tools/lean_dev.ps1 build D0
../tools/lean_dev.ps1 build D0.All
```

Do not commit `.lake/` or generated cert result files. On Windows, the repo
runner keeps `.lake` as a junction to an external cache root:
`$HOME/.d0_lean_cache/D0_v14/09_LEAN_FORMALIZATION/.lake`. Set
`D0_LEAN_CACHE_ROOT` to override that location.

If you previously used a custom absolute path in `lakefile.lean`, remove it
before sharing or cloning on another machine. The portable default is strongly
recommended.


## v12.17 Branch-Defect Projective Generation

The generation index is now represented by the projective closure of the minimal two-branch defect plane over `F₂`.  The Lean core proves that the nonzero projective branch-defect rays are exactly three and that the canonical companion/defect action cycles them with order three.

Core theorem layer:

- `D0.Spectrum.BranchDefectProjectiveGeneration.branchRay_card`
- `D0.Spectrum.BranchDefectProjectiveGeneration.exactly_three_projective_branch_defect_generations`
- `D0.Spectrum.BranchDefectProjectiveGeneration.defectAction_order_three`
- `D0.Spectrum.BranchDefectProjectiveGeneration.defect_generation_card`
- `D0.Spectrum.BranchDefectProjectiveControls.branch_defect_projective_proof_closed`

Scope boundary: the index `3` is core; mass hierarchy, Yukawa structure and empirical generation clustering remain outside this theorem.
