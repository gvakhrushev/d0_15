# A4D joint resonance linear kernel census

**Task:** `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Certificate:** `02_REGISTRY/research/certificates/a4d_joint_resonance_linear_kernel_check.py`
**Machine-readable output:** `02_REGISTRY/research/certificates/a4d_joint_resonance_kernel_census.json`

## 0. Terminal

```text
J2-JOINT-LINEAR-RESONANCE-KERNEL-CENSUS-CERTIFIED
```

## 0.1 Corrections to the first revision of this memo

An earlier revision contained two errors. Both were found in review and are
fixed here. They are recorded because the corrected numbers differ from the
earlier ones, and the earlier ones must not be reused.

**Error 1 — the joint kernel was computed on the transposed block.**
The census computed

```python
N0 = sp.Matrix.vstack(H.T, Q).nullspace()
```

which is `ker H_AA^T ∩ ker H_AQ`, not the declared `ker H_AA ∩ ker H_AQ`.
The certificate simultaneously asserted `H_AA != H_AA^T`, so these are
different subspaces. The accompanying check `H * N0 == 0` only showed that
the returned vectors happened to lie in the right kernel as well; it could not
show completeness. **The correct computation is `vstack(H, Q)`, and it gives
exactly the dimensions the brief predicted.**

**Error 2 — the joint Hessian mixed two different column layouts.**
The earlier matrix placed `H_AA` in the first 24 columns of the lower block,
so the metric rows and the connection rows indexed the columns differently.
The array was 34 x 34 but was not the Hessian of any single quadratic form.

**Correction.** With variables ordered `(q, x) = (metric, connection)`,
`dim q = 10`, `dim x = 24`, the stationarity system of

```text
f(x, q) = 1/2 <A x, x> + <B x, q>
```

is `d/dq : B^T x = 0` and `d/dx : A x + B q = 0`, so the carrier is

```text
        [[ 0_10x10 , H_QA ],        H_QA = B^T  (10 x 24)
H_J  =  [ H_AQ     , A     ]].       H_AQ = B    (24 x 10)
```

with `A = H_AA + H_AA^T`. The certificate now verifies on **every** null vector
that `H_QA x = 0` and `H_AQ q + A x = 0`. Using `H_AA` as-is gives six
violations on the diagonal orbit; using `H_AA + H_AA^T` gives none.

## 1. Objects and conventions

| Block | Shape | Meaning |
|---|---|---|
| `H_AA` | 24 x 24 | polarized connection bilinear, **not symmetric** |
| `A = H_AA + H_AA^T` | 24 x 24 | genuine quadratic connection action |
| `H_QA = (H_AQ)^T` | 10 x 24 | metric response of a connection direction |
| `H_AQ` | 24 x 10 | the transpose partner of `H_QA` |

`H_QA` and `H_AQ` form a genuine transpose pair, so the KKT carrier is a
legitimate non-symmetric saddle-point matrix. The antisymmetric remainder
`H_AA - H_AA^T` is an exact 2-form on the connection sector and is a separate
channel; it is not part of the symmetric carrier.

## 2. Orbit inventory (reproduced)

All 56 singular L=4 characters and all 9 orbit types are reproduced exactly,
with multiplicities `6, 6, 6, 12, 2, 6, 6, 6, 6`.

## 3. Joint kernel census (corrected)

`dim N_0 = dim ker H_AA ∩ ker H_AQ`, exact over `Q(i)`:

| # | phase ids | (r_H, r_A, d) | dim N | rank(H_AQ on N) | dim N_0 | brief |
|---|---|---|---|---|---|---|
| 0 | (0,0,1,1) | (22,23,1) | 2 | 1 | **1** | 1 |
| 1 | (0,0,1,3) | (22,24,2) | 2 | 2 | 0 | 0 |
| 2 | (0,1,1,2) | (20,24,4) | 4 | 4 | 0 | 0 |
| 3 | (1,0,1,2) | (20,24,4) | 4 | 4 | 0 | 0 |
| 4 | (1,1,1,1) | (16,20,4) | 8 | 4 | **4** | 4 |
| 5 | (1,1,3,3) | (20,23,3) | 4 | 3 | **1** | 1 |
| 6 | (2,0,1,1) | (20,24,4) | 4 | 4 | 0 | 0 |
| 7 | (2,1,1,2) | (22,23,1) | 2 | 1 | **1** | 1 |
| 8 | (2,1,2,3) | (22,24,2) | 2 | 2 | 0 | 0 |

**The brief's prediction `dim N_0 = r_A - r_H` is reproduced on all nine orbit
types.** The earlier `4 + 1` result was an artefact of the transpose error.
The nonzero joint kernels are `4 + 1 + 1` on orbits 4, 0 and 5/7.

Total source-invisible connection dimension over the singular characters:

```text
orbit 0 : 6 * 1 =  6
orbit 4 : 2 * 4 =  8
orbit 5 : 6 * 1 =  6
orbit 7 : 6 * 1 =  6
total              = 26
```

## 4. Exact bases for the nonzero N_0

Orbit 0, `ids = (0,0,1,1)`, `dim 1`:

```text
(0,-1), (6,-1), (12,1), (14,-1), (16,1), (18,1), (19,-1), (21,1)
```

Orbit 4, `ids = (1,1,1,1)`, `dim 4` (diagonal quarter-wave):

```text
v0 : (3,1), (4,-1), (5,1)
v1 : (7,1), (8,-1), (11,1)
v2 : (12,1), (14,-1), (16,1)
v3 : (18,1), (19,-1), (21,1)
```

Orbit 5, `ids = (1,1,3,3)`, `dim 1`:

```text
(0,-1+i), (6,-1+i), (12,1), (14,-1), (16,1), (18,1), (19,-1), (21,1)
```

Orbit 7, `ids = (2,1,1,2)`, `dim 1`:

```text
(2,1), (7,-i), (8,i), (11,-i), (12,-i), (14,i), (16,-i), (20,1)
```

Orbits 0 and 4 are rational; orbits 5 and 7 genuinely need `i`.

## 5. First linearized curvature

| orbit | basis | link support | curvature |
|---|---|---|---|
| 0 | v0 | all four links | **NONZERO** |
| 4 | v0..v3 | one link each | **ZERO** (flat candidates) |
| 5 | v0 | all four links | **NONZERO** |
| 7 | v0 | all four links | **NONZERO** |

Only the four diagonal-quarter-wave vectors are curvature-flat. They are flat
**candidates**; no vector is labelled gauge, since that requires the actual
Lorentz/metric quotient.

## 6. The joint KKT Hessian

`H_J = [[0, H_QA], [H_AQ, A]]` on `(q, x)`:

| # | ids | rank H_AA | rank A (sym) | rank H_J | nullity | H_AA pure skew |
|---|---|---|---|---|---|---|
| 0 | (0,0,1,1) | 22 | 8 | 22 | 12 | no |
| 1 | (0,0,1,3) | 22 | 16 | 24 | 10 | no |
| 2 | (0,1,1,2) | 20 | 12 | 28 | 6 | no |
| 3 | (1,0,1,2) | 20 | 12 | 28 | 6 | no |
| 4 | (1,1,1,1) | 16 | **0** | 18 | 16 | **yes** |
| 5 | (1,1,3,3) | 20 | 16 | 32 | 2 | no |
| 6 | (2,0,1,1) | 20 | 12 | 28 | 6 | no |
| 7 | (2,1,1,2) | 22 | 20 | 32 | 2 | no |
| 8 | (2,1,2,3) | 22 | 24 | 28 | 6 | no |

**Structural finding.** On the diagonal quarter-wave the symmetrized
connection action `A = H_AA + H_AA^T` is **identically zero**: `H_AA` is a pure
exact 2-form there. Consequently there is **no non-degenerate symmetric
connection metric** on that orbit, and no Schur complement of `A` is available
there. This is a certified fact, not a numerical artefact.

Because `A` is degenerate on at least one orbit, the earlier additive
metric-only / connection-only / mixed decomposition of `ker H_J` is **not
asserted**; the nullity is reported by exact rank only. The symmetric radical
form of the general non-symmetric quotient-Schur decomposition must not be
applied to this carrier until a genuinely conjugate-paired symmetric carrier is
built. That carrier is **not** built here.

## 7. `E_Q(Q, I) == 0`

`rank(H_AQ) = 9` of 10 on every orbit, so exactly one metric direction is never
produced by the connection. It coincides with the pure trace on six of the
nine orbit types and is a Role-dependent character direction on the other
three; no stronger claim is made. The direction for every orbit is recorded in
the JSON.

## 8. The #227 tangent

| direction | in `ker H_AA` | in `ker H_AQ` | source-visible |
|---|---|---|---|
| `lambda_0` | yes | **no** | yes |
| `w` | no | no | yes |
| `B = K_1 + K_2 + K_3` | no | no | yes |

`B` is excluded from `N_0` and is visible to the metric equation at the first
connection valuation.

## 9. Boundaries

No nonlinear branch search. No torsion-free constraint. No new action term. No
#202 edits. No global Einstein claim. The nine orbit types are the *singular*
characters; regular characters are untouched.

## 10. Reproduction

```bash
python 02_REGISTRY/research/certificates/a4d_joint_resonance_linear_kernel_check.py
```

Exit 0, terminal `J2-JOINT-LINEAR-RESONANCE-KERNEL-CENSUS-CERTIFIED`.
