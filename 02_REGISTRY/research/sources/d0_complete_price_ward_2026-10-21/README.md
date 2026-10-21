# Complete-price density rigidity: reproduction

Existing PR #334, input `086fab99d8aaed7f712e9a3d2858c516b61901fc`.

Read the [new proof](../../A4D_COMPLETE_PRICE_ONSHELL_DENSITY_RIGIDITY_2026_10_21.md). It consumes the already supplied fixed-measure continuum action, the stationary two-density normal form, and the native all-cap radial branch; it does not introduce a new detector or price.

The coupled Euler equations imply both the local coframe trace `x F_x-y F_y=0` and the fixed-volume consistency integral `d(F-x F_x)=0`. Their density Jacobian is invertible near zero. On the literal native radial branch the already-owned logarithmic derivative bound makes this rigidity uniform for every fixed finite cap. The full regular field critical sets, and their local Jacobi kernels with the same boundary conditions, are therefore cap-independent. The aligned timelike branch is exactly the volume-adapted irrotational Einstein-dust class. The checker includes a genuinely inhomogeneous arbitrary-function LTB representative, with nonzero scalar curvature and Weyl tensor, and all 16+24+2 continuum source equations.

Run from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_complete_price_ward_2026-10-21/check_complete_price_ward.py
```

The script writes `RESULT.json` beside itself. Its exact expected byte digest, the executed code/proof digests and source Git blobs are pinned in `AUTHOR_RECEIPT.json`. The imported archive now includes `PROOF.md`, `RESULT.json`, both execution logs, `README_RU.md`, `PUBLICATION.json`, and `SHA256SUMS.json`; `IMPORT_NOTE.md` records the archive hash and mapping. The proof copy is byte-identical to the published root artifact. The normal and optimized executions agreed byte for byte. The numerical branch samples are 85-digit diagnostics, not the analytic proof for all caps. Symbolic tensor identities hold for arbitrary smooth `b(s)` on the displayed open chart.

No native moving-query admission, complete absolute Book03 valuation, finite-lattice lift, independent upstream stationary state, new Lean or remote CI acceptance is asserted. Fixed-volume spurion consistency is not full off-shell Diff naturality. Nonuniform actual ledger sources are retained explicitly in proof section 5.2. `GR_closed=false`.
