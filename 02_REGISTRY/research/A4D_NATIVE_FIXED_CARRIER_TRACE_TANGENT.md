# Fixed-carrier trace tangent and level growth

Research supplement, 2026-10-14. Input SOURCE
`81d0479674cab9f8efd84b93196b76473b0c9386`.

The existing [four-level AF analysis](A4D_NATIVE_FOUR_LEVEL_SELF_SIMILAR_TAIL.md)
establishes a four-level activation threshold for its specified record class,
then an exact Fibonacci tail and all-level corner-record transport. It does
not identify those internal transitions with physical spatial expansion.
This supplement checks a useful boundary on the other side of that missing
map: a continuous idempotent readout variation cannot change its trace-volume
to first order while it remains on one finite carrier.

For finite real matrices, let `P` be idempotent and let `X` satisfy the
differentiated constraint

```text
P^2 = P,              P X + X P = X.
```

Then `P X P = 0`. Cyclicity of trace gives `tr(P X)=tr(X P)=0`, and tracing the
tangent equation yields `tr(X)=0`. The Lean theorem
`D0.Research.RankVolumeTangent.idempotent_tangent_trace_zero` proves this for
every finite index type. Its axiom report contains only Lean's standard
`propext`, `Classical.choice`, and `Quot.sound`.

The result says that an interlevel increase of this readout's trace cannot be
represented by a tangent that stays inside the same idempotent carrier. It
therefore makes the refinement map mathematically indispensable to any
physical expansion claim. It does not prove that D0's volume observable is
`tr(P)`, that its AF refinement is admitted by the native preparation, or
that an expanding curved solution exists. Those are still open arrows in the
native-to-physical path.

Reproduce the narrow proof from `03_FORMALIZATION` with:

```sh
lake env lean ../02_REGISTRY/research/certificates/a4d_rank_volume_tangent.lean
```

The accompanying result record pins the source, compiler output, Lean version,
and Mathlib revision. This is a supporting algebraic lemma; it does not close
the parent native-source or fixed-source terminal.
