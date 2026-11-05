# Local integral radical model and complex embedding

`D0.Algebra.OriginalBookRadicalLocal` constructs `Z[1/8810]` and three
quadratic-algebra stages with `s²=5`, `t²=24142`, `z²=−1`. It constructs the
coordinatewise maps into the previously proved rational field tower and
proves each map injective, starting from localization injectivity. Composing
with the established rational-tower embedding yields an injective map of the
local integral model into `ℂ`; this injectivity is not an assumption.

Exact-file narrow Lean and axiom checks passed using the existing dependency
cache. Independent read-only review checked the localization, coefficients and
all injection steps. The checked results use `propext`, `Classical.choice`,
`Quot.sound`; a final provenance-guarded integration build remains required.

The module does not yet construct the finite-field specialization, prove
that actual reduced effect coefficients belong to this model, verify a
determinant or supply a rank lower bound. Complex conjugation before modular
specialization requires a separate paired-evaluation adapter. Physical
admission, clock/work and #334 remain open; `GR_closed=false`.
