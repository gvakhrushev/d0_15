# Local phased D operand

The local ring now contains the actual phased D operand `i * (3/5) * c_D * U`. Its complex embedding is the previously verified source analytic operand, and its two finite-field images use the distinct phases 469 and 540. Dagger is evaluated by the opposite branch before transposition. Independent review checked the phase, factor and source order.

Narrow Lean and axiom checks passed on blob `3e16d5b830e26c768289abc4405a7217fb0f4127` using existing dependency cache; the declared footprint is `propext`, `Classical.choice`, `Quot.sound`. The committed source may differ only by trailing blank-line normalization. Final provenance-guarded integration remains pending.

The equality of the evaluated operand Gram with the previously reduced source Gram is not yet proved; no full source-effect correspondence, complex rank or physical admission follows. Owner #334 and `GR_closed=false` remain unchanged.
