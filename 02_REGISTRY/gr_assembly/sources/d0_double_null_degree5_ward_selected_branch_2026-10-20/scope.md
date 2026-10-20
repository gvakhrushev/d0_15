# Fifth-order Ward compatibility on one selected crossed-null branch

The checker first replays the registered exact mixed-quartic and asymmetric
quartic calculations for `H=a*x`, `J=b*y`, `h=1` on the original
six-plaquette action. That selected RREF representative satisfies all 40
Euler rows at the 13 amplitude coefficients recorded by the prior checkers.
The Lorentz exponential is then extended through degree five and the four
adjoint coframe-gradient Ward projections are evaluated at `[a^3*b^2]` and
`[a^2*b^3]`.

The exact projections are nonzero:

* `[a^3*b^2]`, internal component 0: `3*x/32 - 3/128`;
* `[a^2*b^3]`, internal component 1: `-x/128 + 11*y/128 + 13/256`.

The coefficientwise flat-symbol certificate verifies the four backward
coframe-gradient null directions and the variational adjoint identities. At
fifth amplitude degree, any new field coefficient enters through that flat
linearized Euler operator, so a nonzero adjoint Ward projection rules out a
fifth-order extension of this exact lower-order representative, even if the
new correction is allowed arbitrary site dependence.

This is scoped to the one RREF-selected representative. The homogeneous
degrees of freedom left by the joint mixed-quartic solve and by both
asymmetric-quartic solves were set to zero; changing those lower-order modes
may change the fifth-order Ward source and remains the next compatibility
question. This result does not establish a general obstruction to crossed-null
solutions, an all-order root, a refinement limit, matter coupling, native
physical admission or GR closure.
