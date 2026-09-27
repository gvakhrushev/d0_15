# A4D FUGU v5 operator audit

**Disposition:** the v5 rank table is a frozen-vector numerical diagnostic, not
a new joint-response or physical anomaly owner. The exact carrier-transport
identity is already owned by [PR #270](https://github.com/gvakhrushev/d0_15/pull/270).
No claim or BOOK promotion follows.

## Repository baseline and owner map

This audit was refreshed against `main` at
`1fc6ff1a75bce9ad45744ac796316350076255df`, after the exact #270, #290, and
#292 owners and the #295 formalization registrations were integrated.

- [PR #232](https://github.com/gvakhrushev/d0_15/pull/232) refutes local joint
  Palatini uniqueness with an exact curved, nongauge vacuum family. It does not
  refute the designated low-frequency metric response.
- [PR #270](https://github.com/gvakhrushev/d0_15/pull/270) owns the polarized
  metric-null line and its exact transport under character detuning.
- [PR #290](https://github.com/gvakhrushev/d0_15/pull/290) owns the exact
  physical cross-character cokernel residuals and same-carrier transport
  witnesses.
- [PR #292](https://github.com/gvakhrushev/d0_15/pull/292) expands the #270
  identity coefficientwise over `Q`, with all 480 scalar coefficient checks
  and the direct Laurent substitution certified; see
  [the coefficientwise audit](A4D_HAQ_COEFFICIENTWISE_IDENTITY.md) for the
  exact `C(d)=\sum_r d_r C_r` decomposition and coordinate convention.
- [PR #240](https://github.com/gvakhrushev/d0_15/pull/240) remains the open
  broader research task for normalized metric response of the #232
  microstructure on a smooth nonconstant background. Its task contract forbids
  downstream task creation from that lane.
- [PR #273](https://github.com/gvakhrushev/d0_15/pull/273) independently
  identifies the flat linear Schur symbol with the linearized Einstein symbol.
  It does not prove a nonlinear continuum Einstein equation.
- [PR #275](https://github.com/gvakhrushev/d0_15/pull/275) is the live,
  narrower Y-family follow-up: continue the #259 connection-stationary lift
  through the next order and test the corrected normalized metric response.
  Its collision fence explicitly retires FUGU fixed-q detune tables.

## What the supplied scout reports

The v5 synthesis reports the nine-orbit rank profile

```text
[0, 1, 2, 2, 0, 3, 2, 1, 0]
```

for a map assembled by differentiating the mixed symbol at a fixed null vector
and projecting the result to `ker A†`, where `A` is the connection Hessian.
The code uses central finite differences and SVD thresholds, so rank zero means
“below this numerical threshold,” not an exact membership theorem. The
reported rank sum is 11. This is the output recorded by the supplied scripts
and logs; it is not reproduced here as an exact theorem.

The map's actual type is

```text
character-detuning direction δz in C^4
  ↦ P_(ker A†) (D_(δz) C) q_n in C^24,
```

with a chosen null vector `q_n` held fixed at the base character. Its domain is
the four character-detuning coordinates, not the metric-only amplitude space
itself. It is a frozen-vector, connection-only solvability diagnostic. At the
reported tolerance, rank zero says that the four sampled first-order sources
are numerically resolved inside `im A` for this frozen section. It does not by
itself establish an exact solvability statement or a nonlinear
implicit-function branch. Positive rank shows failure of this frozen-section
test; it does not show failure of the full joint equations.

## Exact carrier correction already owned by #270

The accepted mixed symbol is `C(z)=H_AQ(z)`. For every nontrivial character,
the exact owner gives

```text
q_null(z) = vec_sym(d(z) d(z)^T),   d_r(z) = z_r^(-1) - 1,
C(z) q_null(z) = 0.
```

The coefficientwise #292 audit establishes the polynomial identity before
the Laurent substitution; it does not rerun the #270 rank or kernel proof.
At `z=(1,1,1,1)`, `d=q_0=0`, so this does not supply a nonzero infrared germ.
Differentiating the identity in any character direction
`D_j=z_j∂_(z_j)` gives

```text
(D_j C) q_null = - C (D_j q_null).
```

Thus, for the same-character holomorphic chart `[A(z) | C(z)]`, the raw
fixed-vector derivative is canceled by the metric motion `C(z)D_jq_0(z)`.
This is a joint-kernel transport identity, not a statement about the physical
conjugate-paired symbol. The explicit derivative is

```text
D_j q_0 = -z_j^-1 (e_j d^T + d e_j^T).
```

The sign follows from `D_j d=-z_j^-1 e_j`; the displayed shear is generally
not in `ker C(z)`. The coefficientwise identity and its derivative do not
transfer to `C(conj(z))` by substitution.

The physical torus instead uses the conjugate-paired table row
`[A(zeta) | C(conj(zeta))]`. Merged #290 reports rank 23 and a one-dimensional
cokernel on orbit types 5 and 7, with distinct exact cross-character
membership patterns and residuals. It also proves that the same-carrier
moving-germ forcing lies in the physical row image. These are separate facts:
the physical cokernel is nonzero, while that particular transport forcing has
zero cokernel class. Neither fact follows by applying the holomorphic
coefficient identity to the conjugated slot.

The scalar control confirms the distinction: the holomorphic unpaired chart
`[A(z)|C(z)]` has rank 24 on orbit types 5 and 7, while the physical
conjugate-paired operator has rank 23 on those types. A rank-24 value for these
physical cases is therefore a phase-convention error, not a refutation of the
holomorphic kernel section.

The projection to `ker A†` can still be meaningful for the deliberately frozen
`q_n` question. It is not invariant under replacing that frozen section by the
owned moving null line in the same-character chart, and it cannot decide the
separate physical cross-character cokernel question by itself.

## Audit of the stronger interpretations

- **Radial and phase profiles are not independent confirmations.** For the
  holomorphic symbol, radial differentiation is `D_j`; phase differentiation
  is `iD_j`. The residual projection is complex-linear, so the two derivative
  matrices differ by the same scalar `i` and have identical ranks and singular
  values. Their agreement is expected from the symbol type.
- **The rank sum 11 is not the scene parameter 11.** It sums ranks over nine
  selected representatives. The packet supplies no canonical direct-sum
  carrier or typed/natural map from this sum to a part-size or other parameter
  of `K(9,11,13)`. Treat the numerical equality as an untyped coincidence.
- **The common phase is not yet physical time or a proved U(1) action.** The
  files specify a simultaneous character tangent. They do not supply the
  required typed identification with the archive time axis or a physical
  action.
- **The reported `F_4` overlap is convention-sensitive.** The v5 prose writes
  `A+iCC^T`, while `deep_analysis.py` computes `A+iCC†`. The script measures
  the top left-singular residual line against `ker F_4`; a later discussion
  compares `ker G` with `ker F_4`, which are in different typed spaces unless
  another map is supplied. Neither is a current owner-level bridge.
- **The reported rational singular-value squares are numerical fits.**
  `final_synth.py` applies `Fraction.limit_denominator(200)` to floating-point
  SVD output. That does not prove exact rationality. The later discussion
  retracts `15/116` and `1/21` as denominator-limit artifacts; the claimed
  exactness of the remaining `1/26` still needs an exact symbolic derivation.
- **The later random-tangent check is not an independent invariant test.**
  For a linear map `M`, composing with a full-rank change of coordinates
  preserves `rank M`. The supplied bundle has no separate random-tangent
  checker, and such a check would not replace the moving-kernel transport.
- **The small-residual absorption statements remain numerical.** The later
  discussion reports residuals near `10^-15` on three orbits, but the supplied
  scripts do not provide exact correction vectors or a symbolic identity.

## Reproducibility boundary

The supplied derivative scripts load `a4d_fugu_p1p2_check.py`, but that source
file is absent from the supplied bundle and from the pinned repository tree.
The v5 pin resolves to the merge commit for PR #262; that commit does not
contain the FUGU source script. The `num_*.npz` files contain sampled `A`, `C`,
and orbit IDs, but not symbolic derivatives. The supplied
`sym_symbolic.npy.npz` archive contains no arrays. The logs preserve reported
outputs, not an exact reproducibility path. In addition, the scripts use
central finite differences (`h=10^-5` or `10^-6`) and SVD rank thresholds.

The later discussion also proposes that the rank sum 11 be linked to the
middle part of `K(9,11,13)` and calls for another task to find that map. Since
the summed statistic is not yet a typed invariant of the moving carrier, that
proposed task is not registered. First-order null-line transport is already
closed by #270. The specific corrected Y-profile question is already assigned
to #275; the wider normalized-response question remains in #240.

## Roadmap consequence

Do not register a second FUGU census task or derive a physical stress/Einstein
term from this rank table. The follow-up already has two nonduplicative scopes:
#275 tests the next exact stationary correction for the named Y slow profile;
#240 tests the wider normalized response question for exact joint-critical
microstructure. Weak-field or empirical tests come only after the
corresponding typed continuum observable exists.
