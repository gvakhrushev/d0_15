# Paired modular specialization of the source radical algebra

`D0.Algebra.OriginalBookRadicalMod1009` constructs two ring homomorphisms
from the actual localized source algebra to `ZMod 1009`. The first maps
`s,t,i` to `244,105,469`; the second is the first after source conjugation and
maps `i` to `540`. Their pair exchanges components under source star. Source
star fixes both real radicals and negates only `i`, and the already injective
complex embedding preserves this star. The proof checks the inverse of 8810,
all quadratic relations and the exact images, plus a negative control showing
that the single first projection does not preserve star as the identity
involution on one finite field. The checked `226²=626` is only a numerical
finite-field relation; it does not put `sqrt(p)` in the source algebra.

Narrow Lean and axiom checks passed on the exact code; an independent read-only
review checked the coefficients, maps, swap law, complex conjugation and scope.
The results use `propext`, `Classical.choice`, `Quot.sound`. Existing dependency
cache was used, so final provenance-guarded integration remains required.

This supplies the previously missing paired specialization, not injectivity
of the modular map, membership of actual reduced source-effect coefficients,
verification of the selected determinant, a complex rank lower bound, or
physical admission. The other seven source primes remain independent controls.
Clock/work and owner #334 remain open; `GR_closed=false`.
