# A4D joint real-carrier quotient decomposition

**Task:** `WRK-A4D-JOINT-REAL-CARRIER-QUOTIENT-DECOMPOSITION`
**Class:** `WORKER`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Baseline:** `8bd7a5c9` (current `main` at branch creation)

## 0. Terminal

```text
J2-JOINT-REAL-CARRIER-QUOTIENT-DECOMPOSITION-NO-REGISTERED-GAUGE-MAP
```

The brief's positive terminal is **not** reached. The exact carrier, its ranks
and its pre-quotient decomposition are certified below; the gauge quotient is
**impossible** because no registered map connects the carrier to the
repository's gauge image. That failure is named precisely rather than papered
over.

## 1. Consumed owners (pinned)

| Owner | What is consumed |
|---|---|
| `A4DGaugeImageResolution.lean` (merged #188/#193) | the only registered gauge image `U = range D₀` |
| merged #252 polarized census | nine-orbit inventory, exact `N_0`, curvature |
| merged #249 | canonical `E_Q(Q,I) = 0` |

## 2. Step 1 — the character conversion is exact

The brief asks for the conversion between table character `zeta`, physical
input character `chi = zeta^{-1}`, conjugate pairing, and the real carrier.
For L = 4 every phase is a fourth root of unity, hence `|zeta| = 1` and

```text
chi = zeta^{-1} = conj(zeta)
```

holds exactly on all four roots, checked symbolically. The conjugate pairing
the real carrier uses is therefore the physical input pairing, not a
convention.

The owned symbol satisfies

```text
H(conj z) = conj(H(z))      on all nine orbit representatives
```

so it is real on the real torus, as required.

## 3. Steps 2-3 — the real carrier and its ranks

The conjugate-doubled carrier is

```text
A_real = [[Re H, -Im H],        C_real = [[Re S, -Im S],
          [Im H,  Re H]]                 [Im S,  Re S]]
H_J^real = [[0_20x20, C_real^T], [C_real, A_real]]   (68 x 68)
```

Exact ranks, and their invariance under `zeta -> chi`:

| # | ids | rank `A_real` | rank `H_J^real` | invariant under `zeta -> chi` |
|---|---|---|---|---|
| 0 | (0,0,1,1) | 44 | 56 | yes |
| 1 | (0,0,1,3) | 44 | 62 | yes |
| 2 | (0,1,1,2) | 40 | 60 | yes |
| 3 | (1,0,1,2) | 40 | 60 | yes |
| 4 | (1,1,1,1) | 32 | 48 | yes |
| 5 | (1,1,3,3) | 40 | 64 | yes |
| 6 | (2,0,1,1) | 40 | 60 | yes |
| 7 | (2,1,1,2) | 44 | 64 | yes |
| 8 | (2,1,2,3) | 44 | 62 | yes |

`rank(A_real) = 2 rank(H_AA)` everywhere. The invariance is the point a real
torus forces, and it holds.

**A caveat that matters.** The complex operators at `zeta` and at
`chi = conj(zeta)` are *not* equal, even though they are conjugate and have
equal rank. A real torus must therefore keep both characters as independent
sectors; collapsing the pair to a single character is not legitimate. All ranks
reported here are rank-stable, so the census is unaffected, but any *basis*
transported naively from `zeta` to `chi` would be wrong.

## 4. Step 4 — pre-quotient decomposition

A null vector `(q, x)` of `H_J^real` satisfies `C_real^T q = 0` and
`C_real q + A_real x = 0`. Projecting onto the two slots gives an exact split
whose counts add up on every orbit:

| # | ids | nullity | metric-only | connection-only | mixed |
|---|---|---|---|---|---|
| 0 | (0,0,1,1) | 12 | 2 | 0 | 10 |
| 1 | (0,0,1,3) | 6 | 2 | 0 | 4 |
| 2 | (0,1,1,2) | 8 | 2 | 0 | 6 |
| 3 | (1,0,1,2) | 8 | 2 | 0 | 6 |
| 4 | (1,1,1,1) | 20 | 2 | 6 | 12 |
| 5 | (1,1,3,3) | 4 | 2 | 0 | 2 |
| 6 | (2,0,1,1) | 8 | 2 | 0 | 6 |
| 7 | (2,1,1,2) | 4 | 2 | 0 | 2 |
| 8 | (2,1,2,3) | 6 | 2 | 0 | 4 |

The **metric-only block is uniformly 2-dimensional** and is exactly
`ker C_real^T`, i.e. the `E_Q(Q,I)` directions. The split is **not** the naive
`dim ker C_real^T + dim ker A_real`: a connection vector in both kernels gives
one direction, not two. Only the diagonal quarter-wave has connection-only
directions; the other eight orbits are entirely metric-only plus mixed.

## 5. Hostile control: the auxiliary carrier is not the physical one

The brief requires an explicit demonstration that the fixed-character
`H + H^T` auxiliary carrier is not the physical quotient result. On the
diagonal quarter-wave,

```text
rank(H + H^T)      = 0     (identically zero)
rank(A_real)       = 32    (non-degenerate)
```

The auxiliary carrier annihilates every connection direction, so it cannot
carry the physical quotient: it would declare the whole connection sector
gauge. This is certified, not asserted.

The second required control also holds: the conjugate-paired carrier is
non-degenerate on all nine orbits while the auxiliary symmetrization changes
rank across orbits (0, 8, 12, 12, 16, 16, 12, 20, 24).

## 6. Step 5 — the gauge quotient fails, and why

The brief requires mapping "the repository's actual infinitesimal
local-Lorentz/gauge image" into the carrier and quotienting exactly. **This
map does not exist in the repository.**

| | Carrier of the gauge owner | Carrier here |
|---|---|---|
| owner | `D0.Geometry.A4DGaugeImageResolution` | this census |
| space | `LocalCoframeField 0`, finrank **256** | `R^20 (+) R^48`, dim **68** |
| period | `N = 0` (L = 2 torus) | `L = 4` characters |
| gauge image | `U = range D₀`, rank 60, codim 196 | not defined |
| kernel | `dim ker D₀ = 4` | not defined |

The owner carries no `L = 4` content and no map into a metric/connection
split. Nothing in `main` supplies such a map, so

```text
physical null dimensions after gauge quotient : NOT COMPUTABLE
```

is the honest statement. Claiming a gauge count here would require inventing
exactly the bridge the brief forbids inventing.

## 7. Reconciliation with #252

The `N_0` dimensions of merged #252 (1, 4, 1, 1 on orbits 0, 4, 5, 7) are
**not** identified with the metric-only block here (uniformly 2). They live in
the 24-dimensional complex connection sector of the polarized census; the
metric-only block lives in the 20-dimensional real metric sector. No exact map
relating the two is constructed, and none is claimed.

## 8. Scope fences respected

No nonlinear germ search, no #202 edits, no new action density, no torsion or
Holst term, no selector, no continuum Einstein claim, no claim-status
promotion, no BOOK edits.
