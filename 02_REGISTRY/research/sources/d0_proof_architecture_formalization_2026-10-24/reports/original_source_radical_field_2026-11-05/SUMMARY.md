# Rational radical field for the original source

`D0.Algebra.OriginalBookRadicalField` constructs the rational field tower
`ℚ(√5)(√24142)(i)` via quadratic algebras and proves an injective field
homomorphism to `ℂ`. It proves the required nonsquare obligations instead of
assuming them: 5 modulo 3; 24142 and 120710 modulo 4; the second extension by
coordinate analysis; and −1 via the real embedding. The images of all three
generators are the actual positive real square roots and `Complex.I`; the
source constants satisfy `p=(√5−1)/2` and
`q=√(12071/20000)=√24142/200`.

The exact file passed narrow Lean and four axiom checks; independent read-only
review checked the nonsquares, field instances, injectivity and source p/q.
Checked results use only `propext`, `Classical.choice`, `Quot.sound`. The
checks used an existing dependency cache; full provenance-guarded integration
for this module remains required.

This is not a localized integral coefficient ring, a modular homomorphism,
proof that the actual reduced effects belong to such a ring, a determinant
certificate or a complex rank lower bound. No field homomorphism from all of
`ℂ` to `GF(1009)` is asserted. The original eight finite-field controls retain
their scope. Physical admission, clock/work and scientific owner #334 remain
open, with `GR_closed=false`.
