# REDSHIFT-DRIFT / EXPANSION COUPLED OWNER — CLOSURE REPORT

Status: uncommitted working-tree result, 2026-09-03.

Lean modules:

- `D0.Bridge.RedshiftSITickCalibrationNoGo`
- `D0.Bridge.RedshiftExpansionArchiveCoupling`

Executable passport:

- `04_CERTIFICATES/vp_redshift_drift_expansion_coupled.py`
- protocol `05_EXPERIMENTS/COUPLED_REDSHIFT_EXPANSION/D0_RDEC_01_PROTOCOL.md`
- verdict `05_EXPERIMENTS/COUPLED_REDSHIFT_EXPANSION/d0_rdec_01_verdict.json`

## 1. SI rho is not internally identifiable

The result is a parametric scale-gauge NO-GO, not a list of clocks.  For every positive rate
`rho` Lean constructs the reciprocal positive SI tick calibration.  Rescaling the SI duration
preserves every internal depth/redshift comparison and changes `rho` inversely.  Consequently two
calibrations with distinct SI rates are observationally identical to the dimensionless internal
protocol, and no real rate can be common to every admissible calibration.

Therefore an SI value of `rho` requires either:

- an external clock section; or
- a derived dimensionless ratio between the cosmological refinement tick and an already calibrated
  physical cycle.

The internal phi generator fixes the ratio of adjacent readouts, not seconds per refinement tick.

## 2. Eliminating rho gives a hard coupled relation

Under the explicit constant-rate interpolation

`dot(z)=rho*ln(phi)*(1+z)`

and the standard FLRW redshift-drift bridge

`dot(z)=(1+z)H0-H(z)`,

Lean proves

`H(z)/(1+z)=H0-rho*ln(phi)=constant`.

Thus the DESI radial-BAO observable must obey

`DH(z)/rd=C/(1+z)`.

Phi and rho cancel from the tested shape.  A nonconstant measured `H(z)/(1+z)` cannot be repaired
by changing one scalar rate: Lean proves by contradiction that a variable-rate representation must
have `rho(z1) != rho(z2)` wherever the two normalized expansion measurements differ.  The reopening
cost is therefore an outcome-affecting function (or abandonment of one physical bridge), not a
renamed value of the old scalar.

## 3. Real-data verdict

The runner verifies the pinned D0-RD-01 verdict and the official DESI DR2 Gaussian BAO mean and
covariance hashes.  On the six `DH_over_rs` measurements:

- best-fit `C = 31.7844087 +/- 0.1992190`;
- `chi2 = 132.0131594` for 5 dof;
- `p = 8.8978e-27`;
- verdict: `REJECT_CONSTANT_RATE_D0_FLRW_COUPLED_BRIDGE` at the frozen `alpha=0.001`.

The direct redshift-drift block by itself had an acceptable constant-shape fit
(`p=0.35617`) and only a null-level bound.  The independent DESI expansion observable is what kills
the shared constant-rate physical bridge.  This is the desired two-observable knife: the same
interpolation cannot be tuned independently in drift and expansion.

Controls:

- freeing one exponent gives `alpha=-1.221896`, but still has `chi2=26.0000/4`,
  `p=3.1644e-5`, below the same goodness-of-fit threshold;
- fixing the coupled exponent `-1` costs `Delta chi2=106.0131` relative to that free exponent
  (`p=7.3248e-25` for one nested degree of freedom);
- the first five galaxy-tracer radial points alone do not reject (`p=0.17896`), while their
  prediction for the DESI `z=2.33` Lyman-alpha point misses by `-11.21 sigma` including calibration
  uncertainty;
- leave-one-out rejection disappears only when the `z=2.33` point is removed.  This dependence is
  reported explicitly; the Lyman-alpha point is not called an independent survey.

The result rejects the coupled constant-rate FLRW application, not the internal Lean redshift
cocycle.  It is also broader than phi: after elimination the same failure applies to any constant
exponential redshift-rate bridge of this form.

## 4. The existing electron section cannot be the cosmological tick

The repository's single SI action section gives

`tau_e=h/(38*m_e*c^2)=2.1298157e-22 s`,

hence `rho_e=1.4817056e29 tick/year` if one refinement tick is identified with that terminal cycle.
The direct-drift 99.9% limit is `rho<6.2741697e-9 tick/year`.  The identification is excluded by a
minimum dimensionless separation factor

`tau_cosmological/tau_e > 2.3615964e37`.

This rejects the cross-scale identification, not the coefficient 38.  Saving a single SI section
requires D0 to derive a dimensionless clock ratio larger than this bound; no such owner is currently
wired into the redshift protocol.

## 5. Dark-response boundary

Combining the internal relation `f_archive=z/(1+z)` with the radial shape gives the exact conditional
law

`DH/rd=C*(1-f_archive)`.

Lean types the missing physical datum as `MeasuredDarkResponseRepresentation`; it does not assert an
inhabitant.  The current run supplies no independently measured dark-response representation, so
its verdict is deliberately `NOT_TESTED_NO_INDEPENDENT_DARK_RESPONSE_REPRESENTATION`.  BAO residuals
are not relabelled as dark response, and the existing phason-magnitude NO-GO is not bypassed.

## Net result

- SI `rho` from dimensionless self-unfolding alone: structurally impossible (scale-gauge NO-GO).
- Constant-rate redshift + FLRW expansion bridge: rejected by real DESI DR2 radial BAO.
- Electron terminal tick = cosmological tick: rejected; required scale separation exceeds `2.36e37`.
- Measured dark-response coupling: exact conditional form exists, but the independent
  representation/data leg is still absent and is not claimed closed.

