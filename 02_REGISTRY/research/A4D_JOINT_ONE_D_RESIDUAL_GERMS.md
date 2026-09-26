# A4D joint one-dimensional residual germs

**Task:** `WRK-A4D-JOINT-ONE-D-RESIDUAL-GERMS`  
**Prerequisite:** PR [#231](https://github.com/gvakhrushev/d0_15/pull/231), current corrected head `a16cab08463e3e6e2657d3a0161142367d4d6941`
**Certificate:** `02_REGISTRY/research/certificates/a4d_joint_one_d_residual_germs_check.py`

## Terminal

```text
J2-JOINT-ONE-D-RESIDUAL-ORBITS-ISOLATED
```

The corrected exact prerequisite census gives a one-dimensional joint kernel
on both requested orbit types. Both nonlinear joint germs are locally
isolated: orbit 0 by its quadratic metric response (exponent `1/2`), and orbit
5 by its cubic connection obstruction (exponent `1/3`).

## 1. Exact orbit correction and basis

Use the corrected right-kernel convention of #231:
`N_0 = ker(vstack(H_AA, H_AQ^T))`, using the repository's `H_AQ` 24-by-10
block. The direct nonlinear Euler checks below also evaluate
the physical input on the inverse Fourier character, as required by the
owned conjugate-mode convention. The inventory rank is not a substitute for
the joint column-kernel test.

| Orbit | Phase IDs | `(r_H,r_A,d)` | `dim ker(H_AA)` | `metric rank on that kernel` | `dim N_0` |
|---|---|---:|---:|---:|---:|
| 0 | `(0,0,1,1)` | `(22,23,1)` | 2 | 1 | **1** |
| 5 | `(1,1,3,3)` | `(20,23,3)` | 4 | 3 | **1** |

For orbit 0 the exact rational `N_0` basis is the vector with nonzero
coordinates

```text
(0,-1), (6,-1), (12,1), (14,-1),
(16,1), (18,1), (19,-1), (21,1).
```

The coefficient-symbol representative is `(1,1,i,i)`; the physical input
field uses its inverse character `(1,1,-i,-i)`, as in the #208/#216
conjugate-mode convention. The vector has nonzero first plaquette curvature,
so it is not a flat-direction candidate.

For orbit 5, the exact `N_0` basis has nonzero coordinates

```text
(0,-1+i), (6,-1+i), (12,1), (14,-1),
(16,1), (18,1), (19,-1), (21,1).
```

It has nonzero first plaquette curvature. Both requested rank types therefore
have an actual one-complex-amplitude germ to reduce.

## 2. Connection range elimination

For orbit 0, write the real connection perturbation as

```text
A_x = u chi(x) v + conjugate(u chi(x) v) + higher harmonics,
```

where `v` is the orbit-0 basis above. The direct linear connection and metric
Euler maps both vanish on `v`. The generated zero and double-character
connection blocks have exact rank 24, so their range corrections are unique.
With coordinates ordered as in the #216 certificate, the quadratic
corrections have these nonzero entries:

```text
w_0: 0,1,2,6,7,8 = 1; 3,4,9,10 = -1
w_2: 0=1/2, 1=-1/2, 2=-1/2, 3=1/2, 4=1/2,
     6=1/2, 7=-1/2, 8=-1/2, 9=1/2, 10=1/2,
     14=-i/2, 16=i/2, 17=-i/2, 19=-i/2, 21=i/2, 23=i/2.
```

The cubic resonant connection forcing lies in the regular range. Eliminating
that range gives zero reduced connection equation through cubic order. The
first nonzero connection equation is quintic. Equivalently, for the
unnormalized action summed over the `4^4` periodic sites,

```text
S_red^(4) = 0,
S_red^(6) = 512 i u conjugate(u) (u^2 + i conjugate(u)^2)^2,
```

and variation in the conjugate amplitude gives

```text
E_K^red(u) = 512 i u (u^2 + i conjugate(u)^2)
                    (u^2 + 5 i conjugate(u)^2) + O(|u|^7).
```

The checker uses exact Lie-log link products and character orthogonality; the
order-six reduced action needs the connection range correction through cubic
order. No source term or additional action channel is introduced.

For orbit 5, the center is the exact complex basis above and the physical
input character is `(−i,−i,i,i)`. The generated zero and double-character
connection blocks again have rank 24; their exact quadratic range corrections
are solved by the certificate. The resulting quadratic metric normal form has
only these nonzero entries, in the repository symmetric-coordinate order:

```text
E_Q,01^red =  2i (u^2 - conjugate(u)^2)
E_Q,02^red = -i (u^2 - conjugate(u)^2)
E_Q,03^red = -i (u^2 - conjugate(u)^2)
E_Q,11^red = -2i (u^2 - conjugate(u)^2)
E_Q,12^red =  i (u^2 - conjugate(u)^2)
E_Q,13^red =  i (u^2 - conjugate(u)^2)
```

The `uv` coefficients vanish. For `u=x+iy`, the squared norm of this leading
metric vector is `192 x^2 y^2`; it vanishes on both real coordinate axes, so
the metric quadratic alone does not isolate the origin.

After eliminating the regular zero, double-character, and cubic connection
ranges, an exact left-kernel covector gives the cubic joint obstruction

```text
E_K^red(u) = 2i u^2 conjugate(u) - (1+i) conjugate(u)^3 + O(|u|^5).
```

Its leading homogeneous term obeys the exact reverse-triangle estimate

```text
|2i u^2 conjugate(u) - (1+i) conjugate(u)^3|
  >= (2 - sqrt(2)) |u|^3.
```

The analytic higher-order remainder preserves a local bound
`||E_K^red(u)|| >= c |u|^3` for some `c>0`. Thus this joint germ is locally
isolated even on the axes where the metric quadratic vanishes, with finite
Hölder exponent `1/3`.

## 3. Joint metric normal form and isolation

From the same range-eliminated action, the only nonzero quadratic metric
components, in the repository's symmetric-coordinate order, are

```text
E_Q,00^red = (1-i)u^2 + (1+i)conjugate(u)^2 + O(|u|^3)
E_Q,01^red = -2u^2 - 2conjugate(u)^2 + O(|u|^3)
E_Q,11^red = (1+i)u^2 + (1-i)conjugate(u)^2 + O(|u|^3).
```

The other seven metric components vanish at quadratic order. For `u=x+iy`,
the squared Euclidean norm of these three leading components is exactly

```text
24 x^4 - 16 x^2 y^2 + 24 y^4
  = 8 |u|^4 + 16 (x^2-y^2)^2
  >= 8 |u|^4.
```

For orbit 0, analytic higher-order terms preserve a local estimate
`||E_Q^red(u)|| >= c |u|^2` for some `c>0`. Hence its joint zero is locally
isolated, with finite Hölder exponent `1/2`. For orbit 5 the cubic connection
bound gives `||E_K^red(u)|| >= c |u|^3` locally and exponent `1/3`.
Concretely, the reduced residual bounds have the form
`|u|^m <= C ||E_red(u)||`, with `m=2` or `m=3`. If the reduced forcing is
`O(h^N)` for every `N`, then for any target power `h^k` we choose `N >= mk`
and get `u=O(h^k)`, hence `u=O(h^infinity)`. These are the two finite
`L=4` orbit controls in the task; they are not a full smooth-continuum theorem.

## 4. Reproduction

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_one_d_residual_germs_check.py
```

The certificate checks both corrected #231 bases, direct Euler orientation,
exact range equations, the orbit-0 quintic connection coefficient and
coercive metric quadratic, and the orbit-5 cubic obstruction and its
reverse-triangle bound. Repository validation results are recorded in the
Draft PR.

## Boundaries

No diagonal four-dimensional sector, all-sheet rescue, torsion constraint,
new action term, boundary selector, #202 edits, or global Einstein claim.
Do not self-merge.
