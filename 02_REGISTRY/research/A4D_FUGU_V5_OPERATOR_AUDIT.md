# A4D FUGU v5 operator audit

**Disposition:** the v5 rank table is a frozen-vector numerical diagnostic, not
a new joint-response or physical anomaly owner. The exact carrier-transport
identity is already owned by [PR #270](https://github.com/gvakhrushev/d0_15/pull/270).
No claim or BOOK promotion follows.

## Repository baseline and owner map

This audit was prepared against `main` at
`420cf140adabacadd73e6fd8da556b4f36f7c6e1`, after PRs #270 and #273 merged
and the Y slow-continuation task was registered.

- [PR #232](https://github.com/gvakhrushev/d0_15/pull/232) refutes local joint
  Palatini uniqueness with an exact curved, nongauge vacuum family. It does not
  refute the designated low-frequency metric response.
- [PR #270](https://github.com/gvakhrushev/d0_15/pull/270) owns the polarized
  metric-null line and its exact transport under character detuning.
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

Differentiating this identity in any character direction `D_j=z_j∂_(z_j)`
gives

```text
(D_j C) q_null = - C (D_j q_null).
```

Thus the raw fixed-vector detune belongs to `im C`. In the full joint
linearization, the metric-null vector moves with the character; its `C δq`
term cancels the raw derivative before a connection-cokernel obstruction is
asserted. PR #270 verifies the exact identity on all 36 detunes of the nine
owned L=4 orbit representatives. This is the relevant carrier-covariant
reading of the v5 calculation.

The projection to `ker A†` can still be meaningful for the deliberately frozen
`q_n` question. It is not invariant under replacing that frozen section by the
owned moving null line, so it does not define a joint anomaly operator by
itself.

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
