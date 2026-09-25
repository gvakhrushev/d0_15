# WRK-A4D-QUOTIENT-SATURATION-PASSPORT

## Class

WORKER

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Objective

Lean-own the finite linear-algebra passport in research PR #128 / memo
`02_REGISTRY/research/MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md` §11:

same-fibre quotient graph criterion (11.1), quotient transport and labelled-loop
endpoint criterion (11.2), finite saturation recursion (11.3), minimality of the
fixed point `W*`, and the exact witness (11.4) in which a one-dimensional
initial vertical defect saturates to the whole fibre.

The point of the witness is algebraic: quotient by the old vertical defect `M`
alone is not a fixed point of (11.3), so it is not an admissible universal
repair of the same-fibre relation. A zero quotient always exists and is not a
classical-limit theorem.

## Read first

- `02_REGISTRY/research/MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md` §11,
  including the exact checker block under `Finite simultaneous quotient saturation`.
- Vocabulary only from §2–§3: `B`, `S`, `K = ker B`, `M = S(K)`, graph `G`.
- Do not import a physical readout, observer, or quotient.

## Preferred modules

- `03_FORMALIZATION/D0/Geometry/A4DQuotientSaturationPassport.lean`
- `03_FORMALIZATION/D0/Geometry/A4DQuotientSaturationWitness.lean`

## Mandatory theorem package

### 1. Same-fibre graph criterion (11.1)

For a supplied surjection `q` with kernel `W`,

`im(q ∘ B, q ∘ S)` is a graph iff `S(B⁻¹ W) ⊆ W`.

Forgetting only the solder output is the weaker test `M ⊆ W`.

### 2. Transport compatibility (11.2)

Quotient transport along an invertible `P` exists in both directions iff
`P W' = W`. It is the identity on the quotient, hence endpoint-independent on
loops, iff `(P - I) V ⊆ W`.

Record the fundamental-loop reduction: images of `(PQ - I)` sit in the sum of
the factors, and inverses add no new image. Both parallel edges of an `L = 2`
pair must be retained: dropping one can strictly shrink the coinvariant.

### 3. Finite saturation and minimality (11.3, Theorem 4)

`H` is the coinvariant sum of `(Pγ - I) V`, not PR #120's common fixed space.
`W⁰ = H` and

`Wᵏ⁺¹ = Wᵏ + ∑_y S_y ((B_y)⁻¹ Wᵏ)`

in basepoint coordinates. The sequence is monotone and stabilizes after at most
`finrank` strict increases (four on the Role fibre). Equal dimension means the
step is already a fixed point. `W*` is the least subspace containing `H` for
which the same-fibre relation is a graph and quotient transport is
endpoint-independent. Path replacement by a loop, and a change of basepoint,
do not change the construction.

### 4. Exact collapse witness (11.4)

At identity transport,

`B = (e_A, e_B, e_C, 0)`, `S = (e_B, e_C, e_D, e_A)`.

Initially `M = ℚ e_A`. The iterates are `ℚ e_A`, `span(e_A, e_B)`,
`span(e_A, e_B, e_C)`, then the whole fibre. The maximal simultaneous quotient
is zero-dimensional. Quotient by `M` alone fails (11.1).

### 5. Hostile controls named in §11

- Nyquist, flat transport: saturation kills the `e_A` line, including the
  mandated `4 e_A` response.
- Boost holonomy: the coinvariant contains the whole A/B plane.
- `W = V` is always a fixed point. That zero quotient is not a physical
  classical limit.

## Firewalls (HARD)

- No physical observer, readout, or physical quotient.
- No constitutive star, `C_N`, nonlinear `Q(e)`, `H(e)`, stress, Einstein,
  continuum, GR, QFT, physical time, or golden refinement.
- Do not identify `n = e_A` or `U_A` with physical time.
- Do not modify located `J`.
- Coinvariant `H` stays distinct from PR #120's common fixed space.
- No `sorry`, `sorryAx`, new axioms, or `lake clean`.
- No self-merge.

## Exit condition

Lean owns (11.1), (11.2), the saturation recursion, minimality of `W*`, and the
exact one-dimensional collapse to the whole fibre, with the Nyquist and boost
controls; wired into `D0.All` / `formal_support.csv`; narrow builds and one
final `D0.All` pass; axioms of the capstones are among `propext`,
`Classical.choice`, `Quot.sound`; task self-retired; PR Ready; do not merge.
