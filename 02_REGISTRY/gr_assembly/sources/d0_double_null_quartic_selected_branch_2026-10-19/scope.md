# Selected cubic representative: quartic-order chart obstruction

For the perpendicular crossed-null chart `H=a*x`, `J=b*y` at `h=1`, this
checker takes the explicit degree-at-most-three particular solutions in the
adjacent `degree3_output.txt`. In each `[a^2*b]` and `[a*b^2]` system, the 134
free parameters are set to zero, as in that output. It then evaluates the
`[a^2*b^2]` coefficient of all 40 original six-plaquette Euler rows at
symbolic transverse coordinates `x,y`.

The checker allows independent spatial polynomials of total degree at most
five for every one of the 24 Lorentz-link corrections and all 16 coframe
corrections at quartic amplitude order. Their linear response gives 840 exact
rational coefficient equations for 840 unknown coefficients. Fraction-free
exact reduction yields coefficient rank 580 and augmented rank 581, so no
quartic correction exists in this chart around this particular cubic
representative.

This does not exclude other cubic representatives: the 134 free parameters
in each cubic system were not varied, and the quartic obstruction may depend
on them. It also does not exclude non-polynomial or higher-spatial-degree
quartic corrections, a different lower-order branch, an all-order finite
root, a refinement family, sourced matter, or physical D0 selection. It is a
single exact finite perturbative chart result at `h=1`, not a general
obstruction to crossed-null solutions or a positive D0-to-GR derivation.
