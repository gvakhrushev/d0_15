# Mixed quartic crossed-null jet with free cubic modes

For the perpendicular crossed-null profile `H=a*x`, `J=b*y` at `h=1`, this
checker parameterizes both complete cubic correction families for the original
six-plaquette action. Each 400-equation cubic system has exact rank 266 and
134 free parameters. It then allows all 268 cubic free parameters to vary
jointly with independent degree-at-most-five quartic spatial polynomials for
all 24 Lorentz-link and 16 coframe corrections.

The joint system has 840 equations and 1108 unknowns. Its exact RREF has rank
582 and the appended right-hand side is not a pivot, so the system is
consistent. The selected solution uses two nonzero free cubic coframe modes
in the `[a^2*b]` coefficient: `e_2_1_1_0_1_2 = 1/64` and
`e_2_1_1_0_0_3 = -1/64`; all other cubic free modes are zero in the selected
RREF solution. It uses 166 nonzero quartic correction coefficients. A final
combined replay verifies all 40 original Euler rows identically in `x,y` at
the checked lower coefficients and at `[a^2*b^2]`.

This is a finite mixed-amplitude jet in the truncated ring
`Q[a,b]/(a^3,b^3)`, at one spacing and one perpendicular-slope chart. It does
not establish the pure cubic coefficients `[a^3]` or `[b^3]`, an all-order
finite root, arbitrary slopes, refinement or boundary control, a matter
source, or physical D0-to-GR selection.
