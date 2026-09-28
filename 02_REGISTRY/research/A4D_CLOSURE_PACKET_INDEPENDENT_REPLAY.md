# A4D Closure Packet: Independent Replay

This note records an exact replay of four supplied files. The original Python
sources and their result JSON files are retained byte-for-byte under
`02_REGISTRY/research/sources/a4d_closure_packet_2026-09-28/`. The integrated
checker is
`02_REGISTRY/research/certificates/a4d_closure_packet_integration_check.py`;
its pinned result is
`02_REGISTRY/research/certificates/a4d_closure_packet_integration_results.json`.

Reproduce from the repository root with:

```bash
python3 02_REGISTRY/research/certificates/a4d_closure_packet_integration_check.py
```

The checker verifies all four attachment SHA-256 values and the exact
coefficient-table input SHA, then reruns both supplied programs. It runs the
closure calculation in a temporary directory so CI does not mutate the
repository. `--write-results` is only for intentional result regeneration.

## #260: selected degree-three obstruction

The independent Fraction-arithmetic Hessian gives the four Fourier ranks
`(0, 0, 16, 0)`, joint rank `16`, and augmented rank `17` for each of the two
selected real dressings. The checker explicitly substitutes
`ell = (1, 1, 1, 0, ..., 0)` into all 96 columns and the degree-three vector:
`ell^T J = 0`, with pairing `+64` for COS and `-64` for SIN.

The supplied closure JSON serializes `ell` as the scalar `1`. The integrated
result corrects that lossy field by storing and checking all 24 entries of the
witness. The attached Hessian checker itself does not load the claimed owner
file by SHA. The historical packet pin `cdb357ca...` differs from the current
open #260 owner checker (`d3a2c377...` at intake); the current owner checker
contains its own degree-three rank and coker assertions. This replay is an
independent selected-ray confirmation, not a SHA-pinned execution of that
owner and not a classification of the full complex `N0` support.

## D2: all powers on the two named orbits

For each listed orbit, every coordinate `x_r` takes one of two distinct values
`a,b`. On those values,

```text
x_r^(k-1) = rho_k*x_r + c_k,
rho_k = (a^(k-1)-b^(k-1))/(a-b).
```

Multiplying by the `x_r`-weighted coefficient contribution and summing gives
`M_k = rho_k*M_2 + c_k*M_1`. The exact check gives `M_1=0`, hence
`M_k=rho_k*M_2` for every integer `k>=1`. The coefficient map has complex rank
9 on each tested carrier. In addition to the source's rank checks, this replay
solves `C*q_2=M_2` over Gaussian rationals and verifies all 24 equations
exactly. Thus `q_k=rho_k*q_2` is an explicit image witness for every `k>=1`.

The `q_2` vectors below use the coefficient table's declared `sym_order` and
are stored as `[real, imaginary]` rational pairs in the result JSON:

| Orbit | Carrier | `q_2` |
|---|---|---|
| 5 | `C(x)` | `(-8, -8, 4i, 4i, -8, 4i, 4i, 0, 0, 0)` |
| 5 | `C(conj x)` | `(0, 0, 4, 4, 0, 4, 4, 0, 0, 0)` |
| 7 | `C(x)` | `(0, -4, -4, 0, -4-4i, -4-4i, -4, -4-4i, -4, 0)` |
| 7 | `C(conj x)` | `(0, -4, -4, 0, -4, -4, -4, -4, -4, 0)` |

The replay also checks `k=1..12` for all four orbit/carrier pairs: 48 exact
identity checks, explicit `q_k` image checks, and augmented-rank checks, with
zero failures. The all-`k` statement follows from the displayed two-value
identity, not from extrapolating that finite scan. Its scope remains the two
named orbits and the pinned coefficient table.

## #275: reconstructed slow-lift cross-check

The supplied SymPy reconstruction passes its exact lift equation and residual,
all four phase checks through order `h^2`, the two normalized substitutions
`z=h` and `z=h^2`, and all 96 flat-limit connection-Euler components. The
committed replay checks its terminal and output counts. It remains a separate
reconstruction of the selected #232 `Y` carrier; it does not widen the class
proved by the existing #275 owner and does not close the full joint-critical
uniform limit #240.

## Ownership and claim boundaries

This is a supplemental audit artifact for three distinct owners, not a
replacement owner for #260, #275, or the D2 coefficient-table result. It does
not change their task lifecycle or claim status. In particular, the two
selected real #260 rays do not classify general complex `N0`; the D2 theorem
does not cover other orbits; and this slow-lift reconstruction does not prove
the uniform #240 limit.
