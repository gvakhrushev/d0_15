# Independent review: original P3 gluing defect and actual Schur reduction

20 October 2026. Reviewer: `record_recovery_source`. **ACCEPT** as an exact
composition on the old finite P3 model; no physical GR claim.

Inspected `03_FORMALIZATION/D0/Claims/GluingAnomalyTime.lean`. Its actual
declarations supply exactly the stated L, B, `Ln=I2`, the Galerkin identity
`B^T L B=I2`, and the nonzero operator defect `C=L B-B Ln`.

Independent exact symbolic calculation confirms

    B^T B = [[2,1],[1,2]],
    C = [[-1,-1],[0,0],[-1,-1]],
    n=(1,-1,1),  B^T n=0,  n^T L n=8,
    F=B^T L n=(-2,-2)^T.

Here n is the complementary archive coordinate, not an additional retained
column of B. No normalized/isometric inclusion is presumed: B is not an
isometry. The full coordinate map `[B,n]` has determinant 3, so the joint
variation covers the complete original three-dimensional space.

The actual full energy is

    E(x,y)=(x1^2+x2^2)/2 - 2(x1+x2)y + 4y^2.

Its archive equation is `8y-2(x1+x2)=0`, with unique minimizing solution
`y*=(x1+x2)/4`. Direct substitution, including its derivative, gives

    E_reduced=(x1-x2)^2/4,
    dE_reduced=((x1-x2)/2,(x2-x1)/2),
    Hess E_reduced=I2-F F^T/8=[[1/2,-1/2],[-1/2,1/2]].

Thus restriction at y=0 and stationary elimination are different operations.
For `x=(a,a), y=a/2`, the full state is `(3a/2)(1,1,1)` and L annihilates
it. All full Euler equations vanish although the operator C is nonzero.
The energy is nonnegative, so these are actual full minima in this fixture.

The intended conclusions follow: this owned operator intertwining defect
does not constitute a scalar DeltaAlpha, a state-independent nonzero force,
or a missing physical stationary law. The Lean finite matrix theorem remains
valid; stronger generative/physical prose is not supplied by this calculation.

Narrow SymPy replay passed in approximately 0.3 seconds, checking the matrices,
archive Euler equation, reduced Hessian/source and complete stationary state.
No repository file or existing certificate was modified.
