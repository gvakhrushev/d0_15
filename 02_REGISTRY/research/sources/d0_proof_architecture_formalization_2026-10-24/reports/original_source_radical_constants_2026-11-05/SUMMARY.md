# Source constants in the local radical algebra

`D0.Algebra.OriginalBookRadicalSourceConstants` constructs actual elements
`p=(s−1)/2` and `q=t/200` in the localized source algebra, explicitly using
the invertibility of 8810. Their images under the proven complex embedding
are the existing `goldenP` and positive Julia coefficient, respectively.
Both elements are fixed by source star; paired reduction maps them to
`(626,626)` and `(278,278)` in `ZMod 1009 × ZMod 1009`. This connects the
scalar values used by the real source construction to the local model, rather
than merely checking unrelated quadratic roots.

Exact narrow Lean and four axiom checks passed with `propext`,
`Classical.choice`, `Quot.sound`; independent read-only review checked the
denominators, actual complex targets, finite-field images and star. Existing
dependency cache was used; a final provenance-guarded integration build for
this added module remains required.

Only these two scalar constants are covered. Membership of actual source
matrices and effects, determinant verification and complex rank lower bound
remain open; `sqrt(p)` is not claimed as a local algebra element. Physical
admission, clock/work and owner #334 are unchanged, and `GR_closed=false`.
