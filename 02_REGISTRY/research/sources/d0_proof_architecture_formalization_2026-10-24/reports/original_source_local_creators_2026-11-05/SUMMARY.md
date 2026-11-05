# Original creators in the localized radical model

`D0.Algebra.OriginalBookLocalCreators` constructs all four actual source
creator matrices over the established local algebra. Their complex images
equal the existing `sourceCreatorComplex`; both modular evaluations equal
the original integer creator entries in `ZMod 1009`. For every matrix over
the local algebra, local conjugate transpose maps to the complex dagger;
its first modular evaluation equals the transpose of the second evaluation.
This explicitly performs conjugation before specializing `i`, rather than
postulating a complex star on a single finite field.

The exact source passed narrow Lean and axiom checks with `propext`,
`Classical.choice`, `Quot.sound`. Independent read-only review checked the
source entries, both evaluations and generic dagger correspondence. Existing
dependency cache was used; final provenance-guarded integration remains due.

This is the creator and generic dagger interface only: actual Julia roots,
Walsh rows, reduced effects and determinant are not yet shown to arise from
local matrices, and no complex lower-rank bound or physical admission follows.
Clock/work and owner #334 remain open; `GR_closed=false`.
