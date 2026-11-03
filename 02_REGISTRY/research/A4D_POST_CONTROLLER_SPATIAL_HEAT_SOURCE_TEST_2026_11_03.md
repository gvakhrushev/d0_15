# After shared-controller elimination: actual spatial heat and the h^-2 source test

3 November 2026, existing research PR #334 in `gvakhrushev/d0_15`.
Input `c6e647c4271a7058048e27c650c5b27c042ac63f`.

[Full Russian proof](sources/d0_spatial_heat_source_2026-11-03/PROOF_RU.md),
[executed checker](sources/d0_spatial_heat_source_2026-11-03/check_spatial_source.py),
[observed result](sources/d0_spatial_heat_source_2026-11-03/result.json).

## The attempted missing parent substitution

The October31 [joint thermal/shared-source result](A4D_JOINT_THERMAL_STATIONARITY_AND_SHARED_SOURCE_LOSS_2026_10_31.md)
proves that eliminating an independent scalar controller also removes a field
source carried by that same scalar. Its suggested independent spatial-Dirac
escape is tested here using the EXISTING full16 operator and actual finite
stencil of [the coframe owner](A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md) and
[fixed-time source theorem](A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md).
No new action, report table, source-defined stress or pure flag is introduced.

## Complete continuum source test, not another heat coefficient

For n=e0, eta=diag(1,-1,-1,-1), s=1/4 and a rotation O_theta(y) in the time/x
plane, take e=s^-1 O_theta and the actual independent Lorentz connection
restricted to its Levi-Civita graph. Then

    G=e^T e=s^-2 I,     g=e^T eta e,
    R_g=-2s^2 theta_y^2,     f_star=ER_g/2=-s^-2 theta_y^2.

Counting measure differs from dVol_G only by a constant. On ALL16 exterior
components the true original differential and its positive adjoint are
unitarily equivalent to s times the flat Hodge-Dirac. Its ENTIRE continuum
spectrum and every fixed-positive-time heat trace are theta-independent.
This is not Lorentz gauge: g is curved when theta_y is nonzero. The old general
positive/Lorentz mismatch is credited to its existing owner; the present
application tests the complete operator and its normalized finite residual.

For theta=epsilon sin(2pi m y), constant original scalars and the SAME nonlinear
r(tau f_star,tau q), tau=p^2, the exact field Hessian is

    I_tau''(0,m)=-tau s^-2 r_x(0,0)(2pi m)^2,
    r_x(0,0)=(-52167499+23331193 sqrt5)/137438953472>0.

The m2/m1 ratio is therefore exactly4. Small actual operands remain in the
old report collar; no desired field equation is put into a new decoder.
Physical admission of this mathematical coframe/current family is NOT inferred.

## The shrinking-gain loophole was explicitly tested

An unscaled zero continuum source does NOT rule out amplification of finite
errors. On the SAME full lattice stencil, exact proper links exp(h omega),
shifted adjoint and every Nyquist mode are retained. Full Kubo-Mori differentiation
and exact symbolic CAR coefficients give, at fixed beta=2p^2,s=1/4,

    H_h''(0,m)=h^2 Q_m+o(h^2).

The proof supplies an explicit convergent Gaussian series for Q_m, derived from
the actual finite Fourier response, not a continuum operator substituted at
finite h. An analytic all-tail bound plus80-digit interval arithmetic gives

    42.6276 < Q1 < 42.6278,
    109.2735 < Q2 < 109.2738,
    2.563 < Q2/Q1 < 2.565 != 4.

Thus no ONE nonzero scalar normalization of this spatial heat matches the two
original Lorentz field linear-response directions. Both positive and negative
normalizations are covered. This statement concerns C2/linearized source
matching at the common flat point; it is not a theorem against arbitrary C1-only
limits, different beta_h/s_h regimes or other genuinely selected source terms.
It does not close or alter the older exact raw216/h^-2 contract.

## Actual execution and scope

58 checks executed; ordinary, python -O and repeat ordinary JSON outputs are
byte-identical. Exact Christoffel/Ricci, all torsion/so(1,3) conditions, full16
intertwining and symbol coefficients are checked. Finite matrix derivatives at
two m/L controls agree with the separate exact Fourier Hessian within3.50e-10.

The all-mode h^-2 Hessians at L8,16,32,64 are:

    m1:44.43493634,42.82027931,42.66412707,42.63610459;
    m2:124.32805570,112.06763581,109.93091875,109.43553355.

At L64 all268435456 spin/Fourier modes are summed analytically by blocks; the
huge square matrix is not formed. Infinite-coefficient intervals are certified
separately by a Gaussian tail bound, not inferred from this convergence table.
The genuine small-amplitude finite links stay in the strict Julia norm window.

Checker SHA256: `e66f1d28cc7ab651fa0eb778cecc244ad02f9712565f47c8ec53526f93a45a97`.
Proof SHA256: `bbb440382c9bbbce06804ceaa1f54a5a48689c0fedda16cf5bf8dfb1e25bf4cc`.
Result SHA256: `6d7c086d9d652db69f0b0bef3410b8d67399e86dd7c13b1c26f741ce442fc4a7`.

This particular spatial-only rescue of shared-controller source loss fails at
the stated scope. The positive nonlinear reporter, record-completion and
canonical source maps are NOT refuted. Actual independent matter/observer,
feedback, Cost-Info or other coupled sources could change the result, but have
not been computed by this packet and cannot be assigned from the Einstein
residual. Likewise no physical exclusion of this family is assumed.

No native programme, new physical all42 root, full Cost-Info source, finite
record-depth error, Lean or repository CI has been supplied. No universal D0
impossibility, task selection, main merge or scientific promotion.
`GR_closed=false`.
