# A4D exact resonance divisor and rank strata

**Task:** `EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION`  
**Status:** `IN_PROGRESS / OPEN`  
**Primary certificate:** [`certificates/a4d_resonance_divisor_slice_check.py`](certificates/a4d_resonance_divisor_slice_check.py)  
**Exact output:** [`certificates/a4d_resonance_divisor_slice_results.json`](certificates/a4d_resonance_divisor_slice_results.json)

## Current exact result

The symbol is the owned 24-by-24 holomorphic connection Hessian `A(Z)` rebuilt with the face orientation, generator order, and `exp4` second-jet convention of the merged #314 certificate. It has 96 nonzero entries. After exact cancellation each entry has at most four numerator monomials, total numerator degree at most two, and denominator in `{1, 2 z_0, 2 z_1, 2 z_2, 2 z_3}`. Every one of its sixteen 6-by-6 role-to-role blocks has generic rank four over `Q(z_0,z_1,z_2,z_3)`.

Exact univariate restrictions of the full determinant are:

| Character slice | Exact determinant | Status |
|---|---|---|
| `(x,1,1,1)` | `(3 x^4 - 22 x^2 + 3)^2 / x^4` | exact identity in `Q(x)` |
| `(x,x,1,1)` | `256` | exact identity in `Q(x)` |
| `(x,x^-1,1,1)` | `(x^4 - 2 x^3 - 2 x^2 - 2 x + 1)^4 / x^8` | exact identity in `Q(x)` |
| `(x,x,x,1)` | `(x^8 + 6 x^6 + 18 x^4 + 6 x^2 + 1)^2 / (4 x^8)` | exact identity in `Q(x)` |
| `(x,-1,1,1)` | `(x^6 - 3 x^5 - x^4 - 10 x^3 - x^2 - 3 x + 1)^2 / x^6` | exact identity in `Q(x)` |

The slice identities are checked by `a4d_resonance_divisor_slice_check.py`; the certificate also reproduces the full-rank control at `(1,1,1,1)` and the exact #314 counterexample rank 22 at `(-1,-1,i,i)` over `Q(i)`. The counterexample refutes the earlier count-only nullity formula. PR #315 independently owns the diagonal specialization

\[
\det A(x,x,x,x)=\frac{(x^2+1)^{12}}{16x^{12}}
\]

and local one-variable Smith exponents `(1,1,1,1,2,2,2,2)` at `x=i`.

Although every listed one-variable determinant restriction is a square or a
higher even power, the global Laurent determinant is **not** a rational
Laurent unit times a square. At the square-character points `(4,9,16,25)` and
`(1,4,9,16)`, exact determinants are respectively

\[
\frac{55489071565690103131701193700501}{19349176320000000000},\qquad
\frac{82681547376902231521}{1761205026816}.
\]

Their ratio is
\[
\frac{443912572525520825053609549604008}{7266932874923047692275390625},
\]
which is not a rational square. If `det A = c z^m P(z)^2` for a Laurent
unit `c z^m`, then at points with square coordinates the monomial is a square
and the ratio of any two nonzero determinant values must be a rational
square. This exact contradiction rejects a global-square shortcut; it does
not identify the irreducible factors or their multiplicities.

The repeated powers in these restrictions are suggestive but do **not** establish that the global four-variable determinant is a square, nor do the slice roots identify all irreducible components. Block ranks and determinant multiplicities alone do not classify the matrix kernel on intersections.

## Exact computation boundary

The general Laurent determinant has not yet been factored. A direct generic symbolic determinant and a sparse fraction-free elimination attempt were stopped after extended computation without a result; neither contributes evidence for a factorization. The reproducible artifact currently certifies exact restrictions and structural sparsity only.

The task remains open for the global factorization over `Q[z_0^±1,z_1^±1,z_2^±1,z_3^±1]`, generic rank on every irreducible divisor component, and exact higher-codimension rank-drop ideals/strata. No finite character scan substitutes for these algebraic steps.

## Scope firewall

This is the holomorphic square symbol `A(z)`. Its results do not automatically transfer to the physical conjugated slot `[A(z)|C(bar z)]`. The memo makes no response, residue, stationary-sheet, continuum, or physical-carrier claim. The rejected phase-count law is recorded only as refuted by #314; no replacement count rule is proposed.

## Reproduction

```bash
python3 02_REGISTRY/research/certificates/a4d_resonance_divisor_slice_check.py
```
