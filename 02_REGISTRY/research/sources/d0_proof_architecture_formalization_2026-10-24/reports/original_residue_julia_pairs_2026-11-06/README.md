# Julia endpoint images over GF(1009)

At the original split (1009, 244, 626, 226, 278, 469), both Lean residue
families agree entrywise with the pinned constructor. This comparison covers
four modes, four rows, both endpoints and every entry of each 16 by 16 matrix
in both orientations. The local source-ring mapping theorems are in
`D0.Algebra.OriginalBookResidueJuliaPairs`.

With the repository toolchain, Python and NumPy installed, run the narrow
build and the comparison from the repository root.

```sh
python3 tools/lean_task_build.py narrow D0.Algebra.OriginalBookResidueJuliaPairs
python3 02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/reports/original_residue_julia_pairs_2026-11-06/check_endpoints.py
```

The script reads the original constructor from Git at
`a358e91e764655b16082bf7e6161a79df96a24a6` and verifies its SHA-256 before
executing it. It captures the endpoint table at return and compares it with
fresh output from the compiled Lean module. The check at Lean source commit
`4ac69741ab15852bdc794510e68c2803881126d2` matched all 16,384 field entries.
The canonical CSV rows have SHA-256
`bc59ee384e3edc1b8d6419fdf5260f5a6a80303ffd599e6b0ae6020553fdee59`.

For mode D, row 1, the first endpoint at (0,2) is 324 under the first
evaluation and 685 under the conjugate evaluation. The second endpoint
at (1,2) is 188 under both. The numerical comparison ends at the Julia
endpoints. Walsh sums and chronological effects have separate checks.
