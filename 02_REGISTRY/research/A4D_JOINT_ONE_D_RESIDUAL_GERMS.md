# A4D joint one-dimensional residual germs

**Task:** `WRK-A4D-JOINT-ONE-D-RESIDUAL-GERMS`  
**Prerequisite:** PR [#231](https://github.com/gvakhrushev/d0_15/pull/231), stacked at `2d4b8f4773521afb516ad631512df04a432c1e26`  
**Certificate:** `02_REGISTRY/research/certificates/a4d_joint_one_d_residual_germs_check.py`

## Terminal

```text
J2-JOINT-ONE-D-RESIDUAL-ORBITS-ISOLATED
```

The exact prerequisite census refines the task's predicted orbit count under
the conjugate-character Euler convention of the owned star action: only the
`(22,23,1)` representative has a one-dimensional joint kernel. The
`(20,23,3)` representative has no joint-kernel direction and is already cut
at the linear level. The actual one-dimensional germ is locally isolated by
its quadratic metric response.

## 1. Exact orbit correction and basis

Use the rank labels and representatives of #231. Since the polarized block is
non-symmetric, the direct connection Euler operator on the selected Fourier
coefficient is `H_AA^T`; the metric Euler operator is `H_QA`. Accordingly,
for the coefficient convention below,
`N_0 = ker(H_AA^T) ∩ ker(H_QA)`. The auxiliary inventory rank
`rank([H_AA^T | H_AQ])` is not a substitute for this column-kernel test.

| Orbit | Phase IDs | `(r_H,r_A,d)` | `dim ker(H_AA^T)` | `rank(H_QA on that kernel)` | `dim N_0` |
|---|---|---:|---:|---:|---:|
| 0 | `(0,0,1,1)` | `(22,23,1)` | 2 | 1 | **1** |
| 5 | `(1,1,3,3)` | `(20,23,3)` | 4 | 4 | **0** |

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

For orbit 5, the direct connection Euler kernel `ker H_AA^T` has dimension 4,
and the exact metric map has rank 4 on it. Thus `dim N_0=0`; there is no
one-dimensional germ on this orbit. The rank-3 statistic in the census is
the metric map on the distinct right kernel `ker H_AA`; it does not classify
the direct conjugate-character Euler system. This is a linear exclusion, not
a nonlinear conclusion.

## 2. Connection range elimination

Write the real connection perturbation as

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

Analytic higher-order terms preserve a local estimate
`||E_Q^red(u)|| >= c |u|^2` for some `c>0`. Hence the joint zero is locally
isolated at `u=0`; the quintic connection equation cannot restore a branch.
The finite Hölder exponent is `1/2`: under smooth forcing of size
`O(h^infinity)`, this estimate gives `u=O(h^infinity)`.

Orbit 5 is cut at first connection valuation because its exact `N_0` is zero.
Together these close both rank types named by the original brief, with one
nonlinear germ and one corrected linear exclusion. This is only the two
finite L=4 orbit controls; it is not a full smooth-continuum theorem.

## 4. Reproduction

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_one_d_residual_germs_check.py
```

The certificate checks the #231 basis and orbit correction, direct Euler
orientation, exact range equations, the quintic connection coefficient, and
the coercive metric quadratic. Repository validation results are recorded in
the Draft PR.

## Boundaries

No diagonal four-dimensional sector, all-sheet rescue, torsion constraint,
new action term, boundary selector, #202 edits, or global Einstein claim.
Do not self-merge.
