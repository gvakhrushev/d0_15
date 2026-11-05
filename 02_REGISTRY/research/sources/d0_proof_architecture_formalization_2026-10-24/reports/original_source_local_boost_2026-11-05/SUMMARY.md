# Original boost over the local radical algebra

`D0.Algebra.OriginalBookLocalBoost` builds `G=c_A c_D†+c_D c_A†` and
`U=I+G²/40+9G/40` from the actual local creator matrices. The inverse of 40 is
constructed in `Z[1/8810]`. Their complex images are the source generator and
the previously proved `exp(log(5/4) G)`; both modular images agree with the
source rational formulas because these particular creator/boost coefficients
are real. Dagger is transported through the opposite modular evaluation before
transposition, not by assuming an identity star on a single finite field.

The exact module passed narrow Lean and five axiom checks with `propext`,
`Classical.choice`, `Quot.sound`; independent read-only review verified the
coefficients, factor order and both evaluations. Existing dependency cache was
used, so final provenance-guarded integration remains required.

This connects the actual generator/boost to the local model. It does not yet
transport the Julia roots, Walsh rows or reduced effects, certify a determinant,
or establish a rank lower bound. Physical admission, clock/work and owner #334
remain open, and `GR_closed=false`.
