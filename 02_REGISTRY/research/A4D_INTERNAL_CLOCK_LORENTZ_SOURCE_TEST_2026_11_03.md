# Internal material clock: full positive-heat versus Lorentz-source test

3 November 2026. Existing PR #334 in `gvakhrushev/d0_15`.
Input `17f452ff7324f2483650dd75e8a025eab3af851e`.

[Full Russian proof](sources/d0_internal_clock_source_2026-11-03/PROOF_RU.md),
[executed checker](sources/d0_internal_clock_source_2026-11-03/check_internal_clock.py),
[observed receipt](sources/d0_internal_clock_source_2026-11-03/result.json).

## Named parent application

The latest spatial full16 test distinguishes the positive heat metric G from
Lorentz g. This continuation tests the proposed removal of that mismatch by
making time a genuinely internal matter readout and imposing Frobenius.
It consumes the existing P1 matter-observer map and exact LC/exterior
intertwining; no external observer, new Hilbert factor, action or penalty.

For a=epsilon sin(x), f=cos(2x), s=1/4, use the actual coframe whose first
rows are (1,a)/[s sqrt(1+a^2)],(-a,1)/[s sqrt(1+a^2)] and transverse rows
exp(sigma f)/s,1/s. Put omega on its genuine Levi-Civita graph. The native
raw grade-one field is e0, all exterior components remain in the operator.
Its P1 current is v=s(1,a,0,0)/sqrt(1+a^2), with g(v,v)=1. It is exactly
normalized grad_g T for T=t-epsilon cos x, so the time direction is
hypersurface-orthogonal, not a freely selected external vector.

The same native observer formula gives

    G_sigma=s^-2 diag(1,1,exp(2sigma*cos(2x)),1).

At sigma=0 this is flat for every epsilon although Lorentz g is curved.
The entire counting-measure full16 heat source in the sigma direction is
EXACTLY ZERO for every beta>0: all first operator coefficients have spatial
Fourier shifts +/-2, so every heat-weighted diagonal Fourier trace vanishes.
Moving pairings, normalizers and coframe/LC transformations are included.
No heat modes are omitted. The separately selected geometric-volume version
has the same first zero, but is not silently substituted for counting measure.

## The nonlinear geometric source is strictly different

Let A=(1-epsilon^2 sin^2 x)/(1+epsilon^2 sin^2 x). Full4D curvature is

    R_g=s^2[A_xx+2sigma(A f_x)_x+2sigma^2 A f_x^2],
    det(e)=s^-4 exp(sigma f).

At sigma0 the entire Einstein tensor is diag(0,0,A_xx/2,A_xx/2) in the
unit-Jacobian time-sheared coordinates. The owned I_tau uses the same actual
r(tau ER/2,0), not a fitted Einstein residual. Its q=0 polynomial is exactly
r(X,0)=a0+a1 X+a2 X^2, with a1>0,a2<0 explicitly determined by Golden/z0.
Uniform rational estimates show its sigma first source is STRICTLY NEGATIVE
for the displayed small-epsilon family. At epsilon1/128,s1/4,tau=p^2 it is
-5.7272417652446593627e-10 per coordinate volume, versus exactly zero heat.
The strict analytical lower magnitude bound exceeds5.7234216981e-10.
All operands, including finite comparisons |sigma|<=2^-20, remain in the
original |X|<1/1024 collar. Full torus integrals multiply by the fixed
(2pi)^4, recorded explicitly; no source normalization is fitted to a zero.

This is a first-source mismatch at a nonflat field, not only a flat Hessian
or a disputed boundary coefficient. The original EH action value at sigma0
can integrate to zero while its transverse source is nonzero; testing only
that action value would miss the difference.

## Execution and scope

48 new program checks executed, normal and python -O outputs byte-identical.
Symbolic full curvature/current identities and exact sign/collar bounds are
independent of quadrature. Whole nonlinear-price finite difference error
<1.99e-29. A separate full16 weighted-coordinate finite control includes all
4096 modes and gives heat-source residual<4.36e-18. That control is NOT the
native proper-Lorentz-link finite stencil, whose artifacts remain governed
by its own owner. The continuum proof is an all-mode argument, not inference
from the finite control. No physical gate admission or emitted programme.

This rules out this fixed-positive-time continuum spatial-only scalar source
identification even after deriving the clock internally. It does NOT rule
out a genuinely different same-execution return/matter/torsion/Cost-Info source,
shrinking-gain finite corrections, other temperature/scaling regimes or a
physically derived restriction of the compared domain. The K913 phase source
from the prior chat is a different carrier; it is neither refuted nor silently
identified with the full16 geometric operator. No full-price D0 impossibility,
full42 physical root, native compiler, Lean, CI, main merge or promotion.

`GR_closed=false`. The complete Lorentz/source binding is not established by
closedness, by a scalar clock alone, or by renaming positive geometry.
