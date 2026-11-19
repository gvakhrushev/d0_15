# Unconditional first-success tape and the archive radial remainder

**Status:** research candidate after two skeptic passes. Skeptic #1 wounded the
flat monomial sentence and the mixed thermal pairing `2(1/3-1)`. Both repairs
were accepted and re-read. Skeptic #2 returned SURVIVES on the repaired text.
No registry row edited. Not a CORE/BOOK/Lean claim and not a GR statement.
Pre-flight on `ad0a7a230338`:
`unconditional`, `first-success`, `q^{M-1}` and `S_select` have no owner of this
tape. Unrelated hits are `A4D_NATIVE_GOLDEN_FIXED_CALIBRATION.md:80`
("complete unconditional outputs") and closure-packet symbols `B_M1`, `B_MINKOWSKI`.
Cross-refs used below are the heat radial law, the chronological price, the
one-way record class and the seam edge gradient.

Calculation base: `ad0a7a230338152e93e2921bfefb2e0620d6ea7e`. Parent task remains
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310. The v4 files
named in the 2026-10-14 PR note are not in this tree. This note recomputes the
load-bearing identities; it does not replay the absent L=8 receipt. The later
tip `13e94346` certifies a feedback-only stationary interval on which the
full-CAR current norm in the updated metric is strictly negative. That witness
is not an input to the arithmetic below and is not re-certified here.

## Claim A (DEF-0.2.2 form)

Let each attempt be an independent pair `(flag, data)`. Success has probability
`b=s_0 s_A`, `q=1-b`, and conditional data energy `E_A`. The unconditional
one-attempt data energy is `E_0`. The output slot is attempt 0 after the
involution that swaps attempt-data 0 with attempt-data 1 when flag 0 is the
failure bit, and does nothing when flag 0 is success. Then for every integer
`M>=1` the output energy equals

    (1-q^{M-1}) E_A + q^{M-1} E_0.

The all-fail probability is `q^M`. It equals the output weight `q^{M-1}`
exactly when `q=1`, and also when `q=0` and `M>1`. For every other pair
with `M>=1` and `q` in `[0,1]`, including `M=1` at `q=0`, the two monomials
differ. At `M=1` the output energy is `E_0`.

## Claim B

On the four-bit carrier `(F0,D0,F1,D1)` that involution is a symmetric
permutation of order 2, preserves `D0+D1` on every basis vector, and does not
commute with translation of `F0`. Both tested one-way generators do commute
with that translation. The permutation is not linear over `F_2`.

## Claim C

Let `c=q^{M-1}` and let `s_0` be constant. Differentiating the mixture energy
`R_M=(1-c)R_A+c R_0` gives

    δR_M = (1-c) δR_A + c δR_0 + (R_A-R_0)(M-1) q^{M-2} s_0 δs_A.

The two-term expression that drops `c δR_0` agrees with this on the subclass
`δR_0=0` and disagrees on a witness with `δR_0≠0`. On that subclass, with
`R_A≠R_0`, the controller weight is still nonzero.

## Claim D

For spectrum `{0,1}`, `β=log 2`, and the success/failure ensemble
`b=1/2`, `E_A=1`, `E_0=1/2`, one register has thermal energy `1/3`.
The output slot has energy `3/4`, so its pullback is `2(1/3-3/4)=-5/6`.
The sum of the two data registers has energy `1` and thermal energy `2/3`,
so its pullback is `2(2/3-1)=-2/3`. The substitution `2(1/3-1)=-4/3` pairs
one register's thermal energy with the two-register energy and is not this
pullback.

For spectrum `{0,4}` and the same `β`, four trace-state registers have
pullback `-240/17`. The normalized conformal cosine of frozen vectors is
invariant, so the owned rule `dot J=j(c) dot c` contributes 0 on that
tangent. The sum is still `-240/17`. The integer `6` is not this value.
The cold state of energy 0 on the same spectrum has pullback
`2(4/17-0)=8/17` per copy, opposite in sign to the trace-state value
`-60/17`. Nonconstant spectrum and `β>0` do not by themselves force a
negative sign.

## Owned pre-facts

Heat radial law, `A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md:120-140`:

```text
H'(0)=2E_β,  E_β=sum λ_i e^{-βλ_i} / sum e^{-βλ_i} >0,
B'(0)=2E_β+R'(0).
Consequently full stationarity requires R'(0)=-2E_β.
```

The next sentences do not extend vanishing of one golden feedback to every
coupled price. The same memo, lines 423-426:

```text
Its thermal derivative is 2/3 and its feedback derivative
is -2/3. This cancels one radial derivative. It is not an admitted D0
preparation or a full joint stationary solution; it prevents promotion of
(3) to a no-go for every coupled price.
```

Chronological price, `A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md:210-212`:

```text
dot J = j(c) dot c,
j(c)=2z l'/A+2(z t'-z^2 d')/B+(z t0'-z^2 d0')/C,
dot c=dot n^T G n_plus+n^T dot G n_plus+n^T G dot n_plus.
```

The factor-curve evaluation in the same memo, lines 294-300, is a different
tangent: `d/dt[β^{-1} log Tr exp(-βΔ_{Q_t})+J_t]=2(E_1-E_2)>1/10000`, and a
constraint multiplier cannot cancel that number. This note does not replace
that statement. It uses only `dot J=j(c) dot c` on the pure conformal tangent.

One-way class, `A4D_NATIVE_RETAINED_RECORD_ADMISSION.md:37-47`:

```text
every complete orthogonal U_A on the active carrier, acting as U_A tensor I_R;
every one-way reversible recording C_f:(a,r)->(a,r+f(a));
The generators do not include an old record controlling the active
computation, coherent rotation of that old record, or arbitrary nonlinear
archive permutations.
```

Seam edge, `A4D_NATIVE_SEAM_ACTION_GATE_BOUNDARY.md:61`: `dS[E_{01}]=6` for the
canonical unit-conductance cycle and the variation `E_{01}=(e_0-e_1)(e_0-e_1)^T`.
That is one integer on that carrier. It is not a radial compensator for the
attempt tape.

## Argument

The output formula is the finite history sum. For `j=0,...,M-2` the first
success at `j` has probability `q^j b` and contributes `E_A`. The remaining
probability `q^{M-1}` contributes the untouched last attempt `E_0`. These
probabilities add to 1. Replacing the tail exponent by `M` leaves out the
successful last attempt and fails at `M=1`, where no earlier failure exists
and the output is the single unconditional attempt.

The four-bit involution is the `M=2` case of that routing: failure of flag 0
swaps the two data bits; success leaves them. Applying it twice restores the
bits. It is a product of disjoint transpositions, hence a symmetric permutation
matrix. Swapping data bits preserves their sum. Translation of flag 0 changes
whether the swap fires, so the operators do not commute. The commutator on
this 16-dimensional basis has squared Frobenius norm 16. An unconditional data
swap, and a recording CNOT that XORs flag 0 by data 0, both commute with the
same translation. The selector sends `(F0,D0)=(0,1)` to a swapped pair and
fixes `(1,0)`; their `F_2` sum is not preserved. A CNOT circuit is affine over
`F_2`, so this permutation is not one.

The mixture derivative is the product rule. `c=q^{M-1}` and `q=1-s_0 s_A`
give `δc=-(M-1)q^{M-2} s_0 δs_A` when `s_0` is fixed. The cross term
`(R_0-R_A)δc` is the displayed controller weight. The diagonal term `c δR_0`
is present whenever the unconditional attempt energy depends on the error
eigenvalues. A two-mode witness with `f(e)=1-e`, `s_0=2/3`, `λ=(0,4)` and
nonselective energy linear in those eigenvalues makes `c δR_0` change the
partial derivative. Freezing `R_0` removes that partial and leaves a nonzero
weight, because `R_A≠R_0` at the sample point `e=(1/5,1/2)`.

The radial pullback at fixed state is `2(E_β(H)-E(H))` for the operator
`H` actually being scaled. On the bit ensemble the output operator has
`E_β=1/3` and energy `3/4`, hence `-5/6`. The sum operator has thermal
energy `2/3` and energy `1`, hence `-2/3`. Using `1/3` against energy `1`
produces `-4/3`, which is a different pairing. On four trace registers with
spectrum `{0,4}`, each copy has `E_β=4/17` and energy `2`, so each
contributes `2(4/17-34/17)=-60/17` and four contribute `-240/17`.

For `G(t)=e^{-2t} I` the normalized cosine
`v^T G w / sqrt(v^T G v · w^T G w)` cancels `e^{-2t}`. The owned chain rule
then gives `dot J=0` at every fixed `c` where `j(c)` is defined. The bare
matrix element `v^T G w` still moves. A frozen-vector boost
`F=diag(e^t,e^{-t},1,1)` also moves the inverse-metric cosine, while
transporting both vectors by `F` makes that cosine constant. The pencil at
`c=1` reproduces `(1-4 z p^3)^4`. At `c=3/5`, `z=1/2`, the `c`-derivative
of `-2 log A-2 log B-log C` is the nonzero element

    -108236496255820/21915981199427 + 57454120467900 sqrt(5)/21915981199427

of `Q(sqrt(5))`. A metric-only reading can therefore look like a source.
The transported conformal reading cannot: its `dot c` is 0, so this nonzero
`j(c)` multiplies zero and does not cancel `-240/17`.

## Verification

`02_REGISTRY/research/certificates/a4d_native_unconditional_archive_action_check.py`

88/88 checks passed under `python3` after the repair. The repaired predicates
are the monomial endpoint, the two-register thermal pairing, the CNOT
population, and `j(3/5)` times the conformal slope. Receipt:
`a4d_native_unconditional_archive_action_results.json`.

Negative controls, each rejecting a stated conclusion rather than a technique:

- output weight `q^M` instead of `q^{M-1}` disagrees on the open interval
  and at `(q,M)=(0,1)`, and the two monomials do agree at `q=1`;
- one classical CNOT copies the data bit into the flag, and the second
  write on that same register restores the flag; the data population stays
  `1/5` through four writes, while the first-success formula at that `b`
  does not;
- dropping `c δR_0` changes a partial derivative on the two-mode witness;
- the bare conformal matrix element moves, so scale invariance is not the
  un-normalized contraction;
- the frozen boost cosine moves, so transport is not optional;
- cold energy 0 and trace energy 2 have opposite pullback signs;
- seam value 6 is not the additive inverse of `-240/17`.

## Named risks and pre-registered attack surface

The strongest self-attack is the missing `c δR_0` term. A note that copies
only `(1-c)δR_A` plus the controller weight is false as soon as the
unconditional attempt energy depends on the error eigenvalues. Claim C keeps
the term and isolates the subclass on which it vanishes.

Next attacks, in the order a skeptic should try them:

1. Carrier mismatch. `M` attempt registers are not the `L^4` site multiplicity
   of the chronology memo, and `dS[E_01]=6` is not `-240/17`. The note never
   adds those integers.
2. Tautological cosine. The normalized conformal cosine does contain
   `e^{-2t}` before simplification. The un-normalized contraction is the
   control that still moves.
3. Universal sign. `2M(E_β-E_τ)<0` for every nonconstant spectrum is false.
   The cold witness reverses it. The trace witness is negative. Both are
   computed.
4. Palette overclaim. Failure of the one-way class and of `F_2`-affine CNOT
   circuits does not forbid an approximate addressed `G`/`CNOT` word in the
   sense of the external Shi theorem already cited by the compilation memo.
   No such word is constructed or excluded here.
5. Other prices can cancel a radial derivative. The heat memo's four-coordinate
   control cancels `2/3` with `-2/3` and is explicitly not admitted. This note
   does not promote the conformal vanishing of this `J` into a no-go for every
   coupled price.
6. A future owned map from the count eigenvalue `e` to the chronology angle
   `c` would add `j(c) ∂c/∂e`. No such map is in the quoted owners. Inventing
   one would be an import. The product calculation has no cross term.
7. Off-by-one routing and same-register QND repetition are the two discarded
   readings of "several attempts". Both fail the explicit ensemble.

## What this does not show

It does not compile the involution from the owned golden matrix `G`, admit it
as a native operation, or supply address and budget. It does not replay the
L=8 interval receipt. It does not place `π_0`, derive a Ward identity, or
produce a ten-component source. It does not identify the attempt tape with the
curvature pairing whose absence is recorded as the missing variational package
in `MEMO_A4D_CURVATURE_ACTION_GRAVITY_GATE.md` §12. The radial remainder is one
scalar contraction. Owned `J` does not cancel it on the transported conformal
tangent. That is a boundary on this tape, not an Einstein equation.
