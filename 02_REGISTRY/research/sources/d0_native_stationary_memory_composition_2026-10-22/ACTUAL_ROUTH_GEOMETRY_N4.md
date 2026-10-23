# Original N1 n4: actual full-geometry Routh–Schur pivots and the two-current border

22 October 2026 · scientific owner #334 / `constitutive/native-programme-v1`.

**Status: new numerical application of an already-owned exact theorem.** The actual original coframe/proper-Lorentz source at the existing four-interval nonflat root gives nonsingular numerical geometric pivots and a nonsingular two-current border. This is not an interval root or inverse certificate, a new action, compulsory Book03 selection, or GR closure. `GR_closed=false`.

## 1. What is consumed and what is new

The exact reduction, including block locality, the rank-at-most-two correction and the Woodbury/bordered inverse, is already proved in [A4D_NATIVE_N1_TWO_CAR_RANK2_BORDER_GEOMETRIC_SCHUR_2026_10_22.md](../../A4D_NATIVE_N1_TWO_CAR_RANK2_BORDER_GEOMETRIC_SCHUR_2026_10_22.md), Git blob `a4a77ea01f9f9146458174902228c07e1424a486`. The original gauge-reduced n3/n4/n5 roots and reconstruction of omitted Lorentz rows are also prior results, consumed through [check_full42_temporal_gauge_deflation.py](../d0_star_rank2_seam_2026-10-21/check_full42_temporal_gauge_deflation.py).

The earlier rank-two check used independent local curvature/source coordinates `f,k` to isolate the material identity. **This application differentiates the actual six-face curvature `f(e,U)` through every admitted coframe and proper-Lorentz coordinate**, including predecessor-face dependence. It computes the real geometric `34/34/40` Schur pivots and the real final `2x2` border on the original n4 root. No source coordinate is fitted or made independently variable.

The executed input blobs are:

| Input in `sources/d0_star_rank2_seam_2026-10-21/`, unless otherwise stated | Git blob |
|---|---|
| `check_full42_temporal_gauge_deflation.py` | `3a0915231e9700aefa35335584c51f53dd2292e6` |
| `check_full42_n1_single_internal.py` | `da83e40379867f71b598fecd8430444ea027a4da` |
| `full_n1_euler_analytic.py` | `7ea28c981826c96b01bbdda67a92010dc7221095` |
| `check_star_rank2_seam.py` | `a57f0e3e845290923c2ac88d39ba5c08af4f6fd6` |
| `check_diagonal_coframe_cauchy_recurrence.py` | `487705f27a32ca1ee65348c5ddb2e4f4d32f5b55` |
| `sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py` | `525b257ec671500bd02c4791f9579dbde2439f21` |

The new checker verifies all six hashes before importing the owners. No pinned input was modified.

## 2. Actual root and the correct variational normalization

The run uses the original configured N1 CQ field price, fixed time weights `(1,1,1,1)`, both original end collars, and

\[
n=4,\qquad h=0.09190076232908961.
\]

The original system has 126 free-field Euler components. The owned temporal Lorentz quotient removes 12 redundant directions, leaving 114 solve coordinates. The existing nonlinear solver converged in 46 evaluations. **All 126 original components were evaluated afterward**, including the 12 omitted temporal-link rows:

| Root check | Maximum absolute value |
|---|---:|
| Original solver's scaled 126-row covector | `2.089581410680003e-14` |
| Its 12 omitted temporal-link rows | `8.195040014531532e-15` |
| Actual geometric price rows | `2.089581410680003e-14` |
| Actual scalar price rows, with the extra solver scaling removed | `7.406684686481336e-14` |

The distinction in the last line is necessary: the original `euler()` returns `h * s['psi']` for scalar rows, while the derivative with respect to the actual interior scalar value is `s['psi']`. Their zeros agree; they are not interchangeable as Hessian rows. The present velocity source is the true `D_u S=2J`, and its Dirichlet incidence matrix includes `1/h`.

For geometry, the new Hessian chart is centered at the computed root, with additive coframe increments and actual link increments

\[
U(\delta X)=\exp(h\,\delta X)U_*.
\]

At the stationary point the derivative of the left-generator source gives the coordinate Hessian; source-proportional moving-frame corrections vanish there. Raw finite-difference asymmetry is reported before symmetrization.

The retained original cell operands are genuinely off-null:

| Cell | `f` | `q` |
|---|---:|---:|
| 0 | `-0.030944898288904343` | `-0.0001374893766238408` |
| 1 | `-0.002763411246768488` | `-0.00011796134225076915` |
| 2 | `-0.000984493061920666` | `-0.000042036476666793346` |
| 3 | `0.00012461819433812193` | `0.000005321935012157081` |

## 3. Matrix conventions and the factor of two

Let `G` denote the 108 gauge-reduced geometric coordinates and `u` the eight independently varied two-CAR cell velocities. The checker forms the actual Hessian blocks

\[
P=S_{GG},\qquad Q=S_{Gu},\qquad W=S_{uu},\qquad
N=\mathbf1_4\otimes I_2.
\]

With `D` the fixed-endpoint scalar incidence matrix, `D^T N=0`. It evaluates

\[
K_{\rm local}=P-QW^{-1}Q^T,\quad
B=QW^{-1}N,\quad K=N^TW^{-1}N,
\]

\[
H_{\rm eff}=K_{\rm local}+BK^{-1}B^T
=P-QD(D^TWD)^{-1}D^TQ^T.
\]

In the parent theorem's notation, `H_j=D_u J_j`, so **the present `W=2 diag(H_j)`**. Consequently `B=C^T`, `K=(sum H_j^{-1})/2`, and the present terminal border

\[
K+B^TK_{\rm local}^{-1}B
\]

is **one half** of the parent's `G2`. This normalization preserves exactly the same effective Hessian and inverse.

## 4. New actual geometric results

At central-difference step `5e-6`:

| Actual matrix | Minimum absolute eigenvalue | Negative / positive |
|---|---:|---:|
| Independent velocity Hessian `W`, dimension 8 | `76.5129633014` | `0 / 8` |
| `K_local`, dimension 108 | `0.0002393222450` | `45 / 63` |
| First geometric block pivot, dimension 34 | `0.0004798421666` | `14 / 20` |
| Second geometric block pivot, dimension 34 | `0.0013038785662` | `14 / 20` |
| Last geometric block pivot, dimension 40 | `0.0016604251057` | `17 / 23` |
| Effective geometric Hessian, dimension 108 | `0.0005275584266` | `44 / 64` |

All entries of `K_local` outside the nearest-neighbor time blocks are zero in the computed matrix. The two singular values of the actual `B` are `0.5076553889` and `0.2810473834`: the border really has rank two on this original root.

The terminal matrix is

\[
\begin{pmatrix}
-0.1308192825&0.0187974054\\
0.0187974054&78.4204614031
\end{pmatrix},
\]

with eigenvalues `-0.1308237807` and `78.4204659013`. It is nonsingular and indefinite. No positivity penalty was inserted into the original stationary field action.

The actual low-rank formula agrees with the full constrained Schur expression to `1.4210854715202004e-14` in maximum entry norm. The Woodbury inverse residual is `7.753711713139602e-13`.

The complete Hessian calculation was repeated at step `2e-6`. All reported inertias and pivot nonvanishing persist. The maximum change of the full Hessian is `1.1979010838825133e-8`; the effective Hessian changes by `1.1816768230588082e-8`. Raw asymmetry is `6.31259940500617e-9` and `2.481948813137791e-8` respectively. The second effective minimum absolute eigenvalue is `0.0005275584113`; its inverse residual is `5.546948745510106e-13`.

These step comparisons are numerical diagnostics, **not certified error bounds**. Original total runtime was about 237 seconds, including the 205-second nonlinear solve.

## 5. Reproduction without resolving the root

Files in this packet:

- `check_actual_routh_geometry.py`: portable consumer; auto-detects the repository from its location or accepts `--source-dir`.
- `ROOT_N4.json`: UTF-8 coordinates plus mesh, weights, source hashes and original residual; no binary file is required for replay.
- `RESULT_ACTUAL_ROUTH_N4.json`: the original executed two-step numerical receipt.

From the repository root, with NumPy, SciPy, SymPy and mpmath installed:

```bash
python3 02_REGISTRY/research/sources/d0_native_stationary_memory_composition_2026-10-22/check_actual_routh_geometry.py \
  --root-json 02_REGISTRY/research/sources/d0_native_stationary_memory_composition_2026-10-22/ROOT_N4.json \
  --json /tmp/routh_n4_replay.json
```

The saved root is checked against all 126 original Euler rows before Hessian use. `--root-only` checks only this provenance/row replay. `--source-dir PATH` supports a separate checkout; `--save-root-json PATH` records a newly solved root; omitting `--root-json` performs the original solve. Optional `--matrix-npz PATH` saves both full and effective Hessians for further analysis. Progress goes to stderr, JSON results to stdout and the optional output file. There is no implicit `/tmp` root cache.

The portable CLI was checked by converting the original saved coordinates and revalidating all original rows. This packaging check does not claim a second execution of the expensive nonlinear solve.

## 6. Exact remaining boundary

The new application resolves the earlier **numerical carrier gap** between the independent `f,k` demonstration and the actual full geometric curvature/source matrix. It supplies concrete nonzero pivot values on the original nonlinear root.

The next mathematical acceptance test is an interval or analytic enclosure of these actual indefinite geometric pivots and the terminal two-current border, together with validated root existence. The current decimal separations alone do not prove those claims. Physical Book03 heat/cut/Info/input/clock selection, actual AF/PF descendant identification, unrestricted four-dimensional spatial variations, and uniform continuum transport remain separate open obligations. `GR_closed=false`.
