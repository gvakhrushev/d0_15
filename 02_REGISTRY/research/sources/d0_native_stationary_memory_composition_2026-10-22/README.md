# Native finite age-clock and preparation-source composition

Existing research owner: Draft PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, slot `constitutive`, carrier `native-programme-v1`. Date: 22 October 2026. `Book03_selected=false`; `GR_closed=false`.

The [integration note](../../A4D_NATIVE_FINITE_AGE_CLOCK_AND_PREPARATION_SOURCE_COMPOSITION_2026_10_22.md) explains the new source composition and its exact remaining consumer. This packet keeps three different evidence levels explicit: finite analytical identities, exact rational bounds, and floating numerical diagnostics.

## Proofs and consumers

| File | Content and scientific scope |
|---|---|
| [AGE_CLOCK_SOURCE.md](AGE_CLOCK_SOURCE.md) | The actual finite no-reset blank-age channel; exact entropy, functional derivative and finite Gibbs representation; real full-window and suffix costs; controlled native spectral source |
| [SPECTATOR_POISSON.md](SPECTATOR_POISSON.md) | New ambient **gain** factorization and same-age boundary/Poisson source transport, consuming the existing oldRIGHT Fredholm theorem |
| [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) | Independent analytical audit, ownership correction, input-versus-output entropy correction and exact scope of the rational/numerical checks |
| [FINE_ARCHIVE_SOURCE.md](FINE_ARCHIVE_SOURCE.md) | Actual same-K fine-minus-age source; all-K proportional-port correction; known native tariff yields an exact whole port-CQ-gain price reduction with paired net weight phi^-3 |
| [FINE_ARCHIVE_SPECTRAL_AUDIT.md](FINE_ARCHIVE_SPECTRAL_AUDIT.md) | Eight exact native row-spectrum classes and an independent outward rational certificate for the original K1 source sign |
| [ACTUAL_ROUTH_GEOMETRY_N4.md](ACTUAL_ROUTH_GEOMETRY_N4.md) | New actual full-geometry application of the existing N1 rank-two Schur theorem at the original nonlinear n4 root; numerical, not interval-certified |
| [PROVENANCE.json](PROVENANCE.json) | Frozen original input paths/blobs, research and publication parents, runtime, evidence scopes |

The stationary oldRIGHT fixed algebra, general Fredholm criterion, raw-CQ uniform-RIGHT solution and rank-at-most-two Routh identity were already proved by their named owners. They are not new claims in this packet. The full128 clock/spectral fixture, rational DATA2×RIGHT2 control, and configured N1 geometry are distinct carriers. No unproved physical source equality between them is asserted.

## Reproduction

Run from a repository checkout. Python 3, NumPy and SciPy suffice for the small matrix controls. The original N1 imports additionally require SymPy and mpmath. The executed environment used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 and mpmath 1.3.0.

```bash
D0_MEMORY_PACKET=02_REGISTRY/research/sources/d0_native_stationary_memory_composition_2026-10-22
python3 "$D0_MEMORY_PACKET/check_age_clock_source.py"
python3 "$D0_MEMORY_PACKET/check_age_clock_rational_bound.py"
python3 "$D0_MEMORY_PACKET/check_spectator_full_poisson.py"
python3 "$D0_MEMORY_PACKET/check_age_spectator_poisson_weld.py"
OPENBLAS_NUM_THREADS=1 python3 "$D0_MEMORY_PACKET/check_fine_archive_source.py"
python3 "$D0_MEMORY_PACKET/check_fine_archive_spectral.py"
```

The first two checks need only the standard library. They consume the original pinned spectral values and first jets rather than rerunning the original full128 matrix instrument. `Decimal` evaluations are nominal high-precision numbers; the `Fraction` check proves strict inequalities with rationally enclosed square roots. The all-order coefficient and moment bounds are analytical proofs in the age note, not finite-sample extrapolation.

The matrix controls use the inherited rational **noncommuting two-Kraus** example. One verifies the gain/Fredholm ambient equations and hostile correlation controls. The other enumerates actual finite-window words, groups them by trailing-blank age, and checks the corrected input score and full source. Neither claims an original full128 tensor replay.

The two `check_fine_archive_*` scripts are a separate **original native CAR16/128-label** application. The first reads the three pinned existing repository inputs and enumerates all K1/K2 actual words, with analytic source jets and inherited entropy-smoothing bounds. It supports `--repo-root` or `--input-dir` and optional `--json`. The second independently constructs the exact original CAR/Walsh/Julia matrices and row spectra; SymPy and outward `Fraction` root/log intervals prove the K1 source sign without SVD. Its optional `--json` writes the same receipt as stdout. This is not a full spatial DATA128/full42 replay or a K4096 enumeration. The all-K paired-bit and literal-port-price reductions are analytical channel identities.

For the actual configured N1 geometry, validate the saved root without solving again:

```bash
python3 "$D0_MEMORY_PACKET/check_actual_routh_geometry.py" \
  --root-json "$D0_MEMORY_PACKET/ROOT_N4.json" --root-only
```

Reproduce both true geometric Hessians and the 2×2 border:

```bash
python3 "$D0_MEMORY_PACKET/check_actual_routh_geometry.py" \
  --root-json "$D0_MEMORY_PACKET/ROOT_N4.json" \
  --json /tmp/routh_n4_replay.json
```

The original nonlinear solve took about 205 seconds; both Hessian passes about 32 seconds. Saved-root replay avoids the solve. `--source-dir PATH` supports a separately located checkout. The checker verifies all six actual input Git-blob hashes and all 126 original Euler rows before using a saved root. It does not alter those inputs or silently reuse an untyped cache. Omitting `--root-json` performs the original nonlinear solve. `--matrix-npz PATH` optionally saves the Hessians.

## Preserved receipts

| Receipt | Meaning |
|---|---|
| [RESULT_AGE_CLOCK_SOURCE.txt](RESULT_AGE_CLOCK_SOURCE.txt) | 80-digit analytic derivative evaluation; finite entropy/Gibbs identities |
| [RESULT_AGE_CLOCK_RATIONAL_BOUND.json](RESULT_AGE_CLOCK_RATIONAL_BOUND.json) | 29 exact rational inequalities for spectral, sign, source, cap and positive-tail bounds |
| [RESULT_SPECTATOR_POISSON.json](RESULT_SPECTATOR_POISSON.json) | 36 floating controls, including gain/raw-CQ distinction and full correlated input variations |
| [RESULT_AGE_SPECTATOR_WELD.json](RESULT_AGE_SPECTATOR_WELD.json) | 54 finite-age normal/source checks at caps 1, 2, 3, 6 |
| [RESULT_FINE_ARCHIVE_SOURCE.json](RESULT_FINE_ARCHIVE_SOURCE.json) | 55 actual original K1/K2 fine/age/merged source checks and exact rational K4096 paired-information bounds |
| [RESULT_FINE_ARCHIVE_SPECTRAL.json](RESULT_FINE_ARCHIVE_SPECTRAL.json) | 659 exact matrix/spectral and outward rational interval controls; strict original K1 source signs |
| [RESULT_ACTUAL_ROUTH_N4.json](RESULT_ACTUAL_ROUTH_N4.json) | Original n4 nonlinear solve plus both full-geometric Hessian passes |
| [ROOT_N4.json](ROOT_N4.json) | Actual root coordinates, mesh, weights and input hashes for reproducible replay |

The numerical N1 receipt is the original executed calculation. Its portability update was checked by importing the pinned sources and revalidating the saved root; an unchanged expensive solve was not repeated. Finite-difference step stability is not an interval error enclosure.

## Exact physical boundary

The finite age clock has an exact mathematical Gibbs representation. This does not prove the compulsory Book03 scene Hodge operator equals that logarithmic age operator, or that its energy is an already paid R term. Full fine-history conditional information, retained oldRIGHT/prefix correlations, actual clock/work/preparation costs and the physical field writer remain in the source. A stationary mixed product is not a finite pure Choi preparation. The roughly 9000-fold reduction is a comparison of two explicitly declared candidate entropy/feedback expressions on one named native tangent, not a bound on the complete physical Euler residual.

Continuing to the same finite fullfine archive proves why this distinction is material: at K1 its missing conditional source reverses the age-only gain source sign. The known K4096 paired-bit contribution exceeds 56.5 nats, but its derivative alone does not fix the remaining merged-history source. The original full128 port-report owner explicitly fixes `(c0,c1)=(1,2)`, so the exact paired net contribution is phi^-3; reversing the tariff to cancel the entropy would change the given price. The complete declared port-cost-minus-CQ-gain equality holds before stationarity and for correlated retained references, but actual further factory/stage/preparation/clock work is still additional physical input.

The separate N1 application computes the true original geometric pivots that were left unevaluated by the earlier local-coordinate check. Strict root/inverse certification, physical Book03 selection, unrestricted four-dimensional spatial dynamics and a uniform continuum limit remain open.
