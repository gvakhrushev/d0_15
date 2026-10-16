# Exact full-shell first-jet obstruction on the sampled cone

17 October 2026. This result sharpens the [actual first-corrector calculation](A4D_CONE_PREPARATION_FIRST_CORRECTOR.md) on the same period-`2pi` cone `theta=y`, `G=s^2 I4`, exact proper Levi-Civita links, and unchanged first geometry/link jets. It uses the already-owned full16 CAR operator and adds no action, source, or preparation selector.

## First projected equation

Let `A_s=P{D0,D1}P` be the first coefficient of the actual sampled matter operator, compressed to the full first shell

```text
Omega={-e0,+e0,-e1,+e1,-e2,+e2,-e3,+e3},   dim(P)=8*16=128.
```

If `C_h=C0+h C1+o(h)` and `R_h=s^-2+h epsilon1+o(h)`, projection of the first amplitude Euler equation gives the necessary condition

```text
(A_s-epsilon1 P) C0=0.                                  (1)
```

The `C1` term vanishes after projection because `Delta0=s^-2 I` on this shell. Thus off-shell amplitude directions cannot repair a failure of (1).

## Exact spectrum and support

An exact replay of the pinned full128 assembly gives the following invariant blocks at `s=1`; for general `s`, multiply every listed eigenvalue by `s^-2`.

| Shell support | Eigenvalues | Multiplicity of each |
|---|---|---:|
| `{-e0,+e0}` | `±(1+sqrt(2))/2`, `±(sqrt(2)-1)/2` | 8 |
| `{-e1,+e1}` | `±(1+sqrt(2))/2`, `±(sqrt(2)-1)/2` | 8 |
| `{-e2,+e2}` | `±sqrt(2)/4` | 16 |
| `{-e3}` | `0` | 16 |
| `{+e3}` | `0` | 16 |

The e0/e1 blocks have identical eigenvalues but are uncoupled, so a corresponding eigenspace may use both axes 0 and 1. It still has no support on axes 2 or 3. The zero eigenspace is exactly the two e3 momenta, dimension32. The smallest nonzero absolute eigenvalue at `s=1` is `(sqrt(2)-1)/2`; in particular no other shell block is silently part of the kernel.

It follows that **no eigenspace has support on all four coordinate-axis pairs**. Every nonzero solution of (1) is confined to one of three sectors: the e0/e1 sector, e2, or e3. Therefore no leading amplitude whose density is supported on the entire `Omega` shell can satisfy (1), at any rank. In particular, for the existing conditional memory-source family

```text
rho_sigma=(P_Omega/8) tensor sigma,   sigma>=0, Tr sigma=1,
```
reducing the internal Schmidt rank of `sigma` does not solve the first-corrector obstruction: this family retains nonzero support on all four momentum axes.

## Boundary

This is a no-go for one explicit nonflat sampled cone with the first geometric and link jets held fixed. It does **not** exclude a first field/link jet obtained from its own Euler equation, a preparation with momentum support confined to one spectral sector, another cone or shell, or any other native branch. It does not establish physical admission, refinement/recovery, or Einstein dynamics. The next physical test is to derive the actual first field/link jets from the complete coupled equations and re-evaluate (1); assigning a compensating jet by hand would not count.

The exact checker replays only the pinned finite first-shell owner, verifies all five invariant block spectra, and applies negative controls against dropping the `+/-` coupling or replacing the operator by its scalar trace. The recorded result is finite-dimensional evidence, not a continuum or GR claim: [checker and result](sources/d0_cone_full_shell_first_jet_2026-10-17/README.md).
