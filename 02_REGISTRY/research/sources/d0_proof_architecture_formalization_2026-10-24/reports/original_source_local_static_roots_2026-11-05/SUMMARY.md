# Static Julia roots in the local radical algebra

`D0.Algebra.OriginalBookLocalStaticRoots` builds local representatives for
the baseline left/right Julia roots for all four source roles and the actual
phased live left/right roots for roles other than D. Their complex images are
the previously proved positive source roots; both modular evaluations are
proved with conjugation performed before evaluation. The correct source
`1/5` and the order of `c c†` versus `c† c` are retained. The moving D roots
are not covered by this module.

Narrow Lean and axiom checks passed on blob `48cdf3e8e3e3cabd146e6f400950106573201ef0`
(the committed Lean file removes two trailing blank lines only), with `propext`,
`Classical.choice`, `Quot.sound`; independent read-only review checked the
source roles, left/right order and both evaluations. Existing dependency cache
was used; final provenance-guarded integration remains required.

Local representatives of moving D, Walsh, source effects and their matrix
entries, modular determinant transfer and the complex lower rank remain open.
Physical admission, clock/work and owner #334 remain unchanged;
`GR_closed=false`.
