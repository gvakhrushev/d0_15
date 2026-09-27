# A4D q0 germ-tower collapse: exact typed certificate

**Task:** `WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT`  
**Terminal:** `A4D-Q0-GERM-TOWER-COLLAPSE-EXACT`  
**Certificate:** `certificates/a4d_q0_germ_tower_collapse_check.py`

## Owned inputs and naming

The exact coefficient matrices are `K_r = [d_r] C(d)` from the merged #270
owner, pinned by source SHA-256
`d7707248af8a30beb14591991d5a78f37cd73c9fef2ac7c29aae0e8b2003f0b7`. They
are checked entrywise against the merged #292 coefficient ledger (480 exact
zero scalar coefficients, with the ten-coordinate `SYM` convention and no
off-diagonal `sqrt(2)`). The physical carrier comes from merged #290; the
full Gram-lift coefficient comes from merged #296. The certificate pins and
reconstructs these owners rather than using the archived FUGU or J2 operator.

Write `x_r=d_r=z_r^{-1}-1`, `q0(x)=vec_sym(xx^T)`, and

```text
M_k(x) = sum_r x_r^k K_r q0(x)
B_n(x) = C(d(z^n)) q0(x)
G_n(x) = 2 binom(1/2,n) sigma(x)^(n-1) B_n(x)
sigma(x) = x^T eta x.
```

`B_n` is the **bare** harmonic operator. `G_n` is the **full** #296 Gram-lift
coefficient (called `F_n` in that owner). They are different objects.

## Exact harmonic algebra

The accepted polynomial identity gives

```text
M_1 = sum_r x_r K_r q0(x) = C(x) q0(x) = 0.
```

Since `d_r(z^n)=(1+x_r)^n-1`, linearity of `C` and the finite binomial
theorem give, for every integer `n>=2`,

```text
B_n = sum_{k=1}^n binom(n,k) M_k
    = sum_{k=2}^n binom(n,k) M_k.
```

Each `K_r` is constant and `q0` is quadratic, so `M_k` is homogeneous of
degree `k+2`. The exact polynomial `M_2` is nonzero and homogeneous of degree
four. Thus, for every fixed `n>=2`,

```text
B_n = binom(n,2) M_2 + terms of degree at least 5
    = binom(n,2) M_2 + O(||x||^5).
```

The leading-weight generating function follows by differentiating the
geometric series twice:

```text
sum_{n>=2} binom(n,2) s^(n-1) = (s/2) d^2/ds^2 (1/(1-s)) = s/(1-s)^3.
```

The #296 prefactor restores the fixed-harmonic order. Since `sigma` has
degree two and `B_n` has first possible degree four, `G_n` has generic first
degree `2(n-1)+4=2n+2`. This is a polynomial-order statement near `x=0`;
special rays can cancel the leading coefficient. It is not a metric-stress
or stationary-sheet theorem.

## Exact physical-cokernel scope for `M_k`

On the exact physical carriers `P=[H_AA(zeta) | H_AQ(conj(zeta))]` of merged
#290, the physical left cokernel has dimension one on orbit types 5 and 7.
Normalize its exact vector `ell` so its first nonzero coordinate is one and
put `a_r=ell^* K_r q0(x)`. The certificate obtains these weights from the
owned matrices and proves the grouping identities below:

| Carrier | `x=d(zeta)` | `(a_0,a_1,a_2,a_3)` | Equal-coordinate groups |
|---|---|---|---|
| orbit 5: `(i,i,-i,-i)` | `(-1-i,-1-i,-1+i,-1+i)` | `(-2+2i, 2-2i, 0, 0)` | both group sums are zero |
| orbit 7: `(-1,i,i,-1)` | `(-2,-1-i,-1-i,-2)` | `(-4i, 0, 0, 4i)` | both group sums are zero |

For every integer `k>=0`, coordinates with the same `x_r` have the same
`x_r^k`; the grouped weights therefore give

```text
alpha_5(k) = (-2+2i + 2-2i)(-1-i)^k + 0*(-1+i)^k = 0
alpha_7(k) = (-4i + 4i)(-2)^k + (0+0)(-1-i)^k = 0
ell^* M_k = sum_r x_r^k a_r = alpha_orbit(k) = 0.
```

Together with the exact one-dimensional left cokernel, this proves
`M_k in im(P)` for every `k>=0` on these two carriers. In particular, it
applies to every `M_k` entering the finite binomial expansion of `B_n`. This
is an all-`k` result only for the two listed exact physical carriers; it is
not an all-character or continuum theorem. It says image membership, not that
the vectors `M_k` vanish.

## Hostile carrier control

The frozen/cross-character source `w_j(zeta)` is paired against the physical
matrix whose mixed block is at `chi=conj(zeta)`. The certificate reproduces
the #290 raw squared residuals `[8/5,8/5,0,0]` on orbit 5 and `[2,0,0,2]` on
orbit 7 (unit-`q0` values `[1/25,1/25,0,0]` and `[1/46,0,0,1/46]`). Thus the
nonzero cross-character cokernel class remains exact on its listed
directions.

For the same-carrier source, the differentiated owner identity is instead

```text
w_j(chi) + H_AQ(chi) D_j q0(chi) = 0.
```

All eight exact transport checks vanish. The cross-character residual is a
carrier-mismatch diagnostic, not a same-carrier moving-germ obstruction.

## Reproduce and scope

Run:

```sh
python3 02_REGISTRY/research/certificates/a4d_q0_germ_tower_collapse_check.py
```

The certificate uses exact rational/Gaussian-rational/symbolic arithmetic.
It makes no SVD, floating-point, finite-difference, or numerical-fit
decisions. It does not prove stationary-sheet stress, nonlinear Einstein,
continuum convergence, or any N0 odd correction, and it changes no BOOK,
ClaimMap, or release status.
