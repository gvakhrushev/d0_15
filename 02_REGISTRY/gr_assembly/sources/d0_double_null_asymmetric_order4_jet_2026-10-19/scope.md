# Selected crossed-null branch: pure cubic and asymmetric quartic coefficients

Starting from the registered mixed-quartic solution, this checker raises the
amplitude cap to three and tests four previously omitted coefficients on the
same `h=1`, `H=a*x`, `J=b*y` branch. The pure `[a^3]` and `[b^3]` sources are
identically zero, so zero corrections are selected. For `[a^3*b]` and
`[a*b^3]`, independent degree-at-most-five spatial polynomials are allowed
for all 24 Lorentz-link and 16 coframe corrections. Each 840-equation system
has exact coefficient rank 580; the augmented RHS is not a pivot. The RREF
solutions have four nonzero field coefficients per asymmetric quartic order.

After adding both corrections to the prior cubic and `[a^2*b^2]` fields, a
combined symbolic replay verifies all 40 original Euler rows identically in
`x,y` at 13 retained amplitude coefficients: the six lower coefficients,
`[a^2*b]`, `[a*b^2]`, `[a^2*b^2]`, `[a^3]`, `[b^3]`, `[a^3*b]`, and
`[a*b^3]`.

This is not a complete fourth-order jet: `[a^4]`, `[b^4]`, `[a^3*b^2]`,
`[a^2*b^3]`, and `[a^3*b^3]` are not checked. It also gives no arbitrary-slope
family, refinement or boundary limit, sourced solution, all-order root, or
physical D0-to-GR selection.
