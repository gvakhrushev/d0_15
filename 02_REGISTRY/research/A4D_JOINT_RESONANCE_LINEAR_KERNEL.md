# A4D joint resonance linear kernel census

**Task:** `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Certificate:** `02_REGISTRY/research/certificates/a4d_joint_resonance_linear_kernel_check.py`
**Machine-readable output:** `a4d_joint_resonance_kernel_census.json`

## 0. Terminal

```text
J2-JOINT-LINEAR-RESONANCE-KERNEL-CENSUS-CERTIFIED
```

with one certified refinement of the brief's predicted residual dimensions,
stated exactly in section 4.

## 1. Objects and conventions

The polarized star connection symbol is rebuilt from the owned finite star
formula, structurally as in merged #208/#216. On one L=4 character the
connection sector carries 24 real components and the symmetric metric sector
carries 10, related by the genuine symmetric lift `q -> H = (1/2) q eta`:

| Block | Shape | Meaning |
|---|---|---|
| `H_AA` | 24 x 24 | polarized connection bilinear |
| `H_AQ` | 10 x 24 | metric response of a connection direction |

Two conventions were ambiguous in the brief and are now pinned by the
certificate:

1. **`H_AA` is not symmetric.** It is a *polarized* block, not a Hessian of a
   quadratic form in the link variable. The joint Hessian is therefore built
   with the owned block as-is; symmetrizing it would silently change the
   operator. The certificate asserts `HAB != HAB.T` as a guard.

2. **`N_0` is the nullspace of the 34 x 24 matrix `[H_AA^T ; H_AQ]`**, i.e.
   exactly `{ x : H_AA x = 0 and H_AQ x = 0 }`. This is the joint kernel and
   is *not* the same system as the `r_A` inventory quantity below.

## 2. Orbit inventory (reproduced)

All 56 singular L=4 characters and all 9 orbit types are reproduced exactly,
with multiplicities `6, 6, 6, 12, 2, 6, 6, 6, 6`.

## 3. Joint kernel census

`dim N`, `rank(H_AQ|_N)`, and `dim N_0`, all exact over `Q(i)`:

| # | phase ids | (r_H, r_A, d) | dim N | rank(H_AQ on N) | dim N_0 | brief |
|---|---|---|---|---|---|---|
| 0 | (0,0,1,1) | (22,23,1) | 2 | 1 | **1** | 1 |
| 1 | (0,0,1,3) | (22,24,2) | 2 | 2 | 0 | 0 |
| 2 | (0,1,1,2) | (20,24,4) | 4 | 4 | 0 | 0 |
| 3 | (1,0,1,2) | (20,24,4) | 4 | 4 | 0 | 0 |
| 4 | (1,1,1,1) | (16,20,4) | 8 | 4 | **4** | 4 |
| 5 | (1,1,3,3) | (20,23,3) | 4 | 3 | **0** | 1 |
| 6 | (2,0,1,1) | (20,24,4) | 4 | 4 | 0 | 0 |
| 7 | (2,1,1,2) | (22,23,1) | 2 | 1 | **0** | 1 |
| 8 | (2,1,2,3) | (22,24,2) | 2 | 2 | 0 | 0 |

## 4. Certified refinement of the brief

The brief predicted `dim N_0 = r_A - r_H`. That is reproduced on **seven** of
the nine orbit types, and it is **wrong on two**:

```text
orbit 5 = (1,(1,3,3),20,23)   predicted 1, exact 0
orbit 7 = (2,(1,1,2),22,23)   predicted 1, exact 0
```

The cause is structural, not numerical. The quantity `r_A` used in the #208/#216
inventory is the rank of the **row** system `[H_AA^T | H_AQ]`, whose kernel
lives in the joint space `R^24 (+) R^10`. The quantity `N_0` is instead the
kernel of the **column** system `[H_AA^T ; H_AQ]` on the connection sector
alone. These are different systems, and

```text
im(H_AQ|_N)  is  NOT  contained in  ker([H_AA^T | H_AQ])
```

exactly on orbits 5 and 7. On the other seven types the containment happens to
hold, which is why `r_A - r_H` coincides with `dim N_0` there.

**Consequence.** The predicted "1" on two orbit types does not exist. The only
genuine nonzero joint kernels are

```text
orbit 0 : dim 1, multiplicity 6
orbit 4 (diagonal quarter-wave) : dim 4, multiplicity 2
```

so the total source-invisible connection dimension over the singular L=4
characters is

```text
6*1 + 2*4 = 14
```

rather than the `16` implied by the brief. Equivalently, the refinement removes
exactly `6*1 + 6*1 = 12` dimensions from orbit 5 (mult 6) and orbit 7 (mult 6).

## 5. Exact bases for the nonzero N_0

All bases are **rational** (hence in `Q(i)`); no extension is needed.

Orbit 0, `ids = (0,0,1,1)`, `dim N_0 = 1`, one vector, nonzero slots:

```text
(0, -1), (6, -1), (12, 1), (14, -1), (16, 1), (18, 1), (19, -1), (21, 1)
```

Orbit 4, `ids = (1,1,1,1)`, `dim N_0 = 4` (the diagonal quarter-wave):

```text
v0 : (3, 1), (4, -1), (5, 1)
v1 : (7, 1), (8, -1), (11, 1)
v2 : (12, 1), (14, -1), (16, 1)
v3 : (18, 1), (19, -1), (21, 1)
```

Each of these four is supported on a **single link**, so its first linearized
plaquette curvature vanishes: they are flat/gauge **candidates**, not
certified gauge directions. The orbit-0 vector is supported on all four links
and therefore has **nonzero** first-order curvature, so it is *not* a flat
candidate.

No vector is labelled gauge here. Doing so requires checking the repository's
actual Lorentz/metric quotient, which this task does not do.

## 6. Full mixed joint Hessian

`H_J = [[0, H_AQ], [H_AA, 0]]` on the joint space `R^24 (+) R^10`:

| # | ids | rank | nullity | connection-only | metric-only | mixed |
|---|---|---|---|---|---|---|
| 0 | (0,0,1,1) | 29 | 5 | 2 | 1 | 2 |
| 1 | (0,0,1,3) | 29 | 5 | 2 | 1 | 2 |
| 2 | (0,1,1,2) | 29 | 5 | 4 | 1 | 0 |
| 3 | (1,0,1,2) | 29 | 5 | 4 | 1 | 0 |
| 4 | (1,1,1,1) | 25 | 9 | 8 | 1 | 0 |
| 5 | (1,1,3,3) | 29 | 5 | 4 | 1 | 0 |
| 6 | (2,0,1,1) | 29 | 5 | 4 | 1 | 0 |
| 7 | (2,1,1,2) | 31 | 3 | 2 | 1 | 0 |
| 8 | (2,1,2,3) | 31 | 3 | 2 | 1 | 0 |

The decomposition is canonical: a null vector `(c, m)` satisfies
`H_AQ m = 0` and `H_AA c = 0`, so

```text
metric-only     = ker H_AQ          (dimension 10 - rank H_AQ = 1)
connection-only = ker H_AA          (dimension 24 - rank H_AA)
mixed          = the remainder
```

## 7. `E_Q(Q, I) == 0` and the tangent-cone consequence

`rank(H_AQ) = 9` on **every** orbit. So there is exactly one metric direction
that the connection never produces, and it is exactly the single metric-only
null vector of `H_J`. This is the exact content of `E_Q(Q, I) == 0`: at the
first connection valuation the joint tangent cone contains no branch along
that metric direction.

The direction is **not** the pure trace on all orbits. It coincides with the
trace on six of the nine orbit types and is a Role-dependent character
direction on the other three. The certificate records the direction for every
orbit in the JSON, so no stronger claim is made than the computation supports.

## 8. The #227 tangent is source-visible and not in N_0

The three owned quarter-wave directions, evaluated on the diagonal orbit:

| direction | in `ker H_AA` | in `ker H_AQ` | source-visible |
|---|---|---|---|
| `lambda_0` | yes | **no** | yes |
| `w` | no | no | yes |
| `B = K_1 + K_2 + K_3` | no | no | yes |

`B` is therefore **excluded from `N_0`** and is visible to the metric equation
at the first connection valuation. The #227 curved germ is not a joint-kernel
direction and cannot be produced by the source-invisible mechanism catalogued
here.

## 9. Boundaries

No nonlinear branch search. No torsion-free constraint. No new action term. No
#202 edits. No global Einstein claim. The nine orbit types are the *singular*
ones; regular characters are untouched by this census.

## 10. Reproduction

```bash
python 02_REGISTRY/research/certificates/a4d_joint_resonance_linear_kernel_check.py
```

Exit 0, terminal
`J2-JOINT-LINEAR-RESONANCE-KERNEL-CENSUS-CERTIFIED`.
