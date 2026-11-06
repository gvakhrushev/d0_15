# Determinant consumer for the saved GF(1009) matrix

`SavedFutureMatrixDeterminant.lean` imports the exact numerical matrix module
and proves that the saved matrix A has nonzero determinant from its proved
right inverse, using `Matrix.det_mul`. The concrete 0≠1 case is checked by
kernel `decide`. This is a result about the pinned numerical matrix only.

Two earlier candidate files failed to elaborate, first with an untyped and
then a typed `zero_ne_one`; both diagnostics included `sorryAx` and neither
constituted a theorem. Each failure and the later successful run have separate
path-free receipts.

The imported module source is pinned at commit `8f5b33bd` as
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/reports/saved_future_matrix_all_rows_2026-11-05/SavedFutureMatrixAllRows.lean`,
Git blob `2d5b38b17621e1b36e490f1bcba2aedf5cbd2ac2`; no second copy is needed.

The successful run checked the exact module selected by `lean --deps`,
including its olean digest. The consumer retains the imported native-computation
axiom `D0.Algebra.SavedFutureMatrixPacked.all_rows_right_inverse._native.native_decide.ax_1_1`
alongside `propext`, `Classical.choice`, and `Quot.sound`. The cached
dependencies were not independently authenticated. There is no source-effect
equality, complex lower rank, physical admission or GR conclusion here.
Raw logs can contain local paths and are excluded; receipts carry their hashes.

The Git copies normalize CRLF to LF where applicable; `files.json` preserves
executed-byte SHA-256 alongside each stored-file hash.
