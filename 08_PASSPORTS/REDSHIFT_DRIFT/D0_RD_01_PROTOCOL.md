# D0-RD-01 — direct redshift-drift passport

Status: frozen before running the local statistic, 2026-09-03.

The publications and their headline central values were already public and inspected when this
file was written.  This is therefore a retrospective, form-frozen confrontation, not a historically
prospective preregistration.  The stringent `alpha=0.001` rule is inherited from PHI-P_DESI_01 and
was fixed before the local cross-block aggregation was evaluated; the exact p-values are reported
so the conclusion does not depend on hiding a conventional threshold.

## Question

Does the already-proved D0 one-tick relation

\[
\Delta z_{D0}=(\varphi-1)(1+z_{D0})
\]

survive a direct astronomical redshift-drift confrontation?  This passport does not reconstruct
drift from BAO or from an assumed FLRW expansion history.  It uses repeated spectra of the same
absorbers.

## Data frozen before the computation

1. **Low-redshift block:** the ten bold-face H I 21-cm absorbers used in Table 1 of Darling (2012),
   arXiv:1211.4585.  The observations use primarily digital Green Bank Telescope spectra and span
   0.09 <= z <= 0.69.
2. **Independent high-redshift holdout:** the pixel-by-pixel result for the three ESPRESSO epochs
   of QSO J052915.80-435152.0 in Trost et al. (2026), arXiv:2603.02318, at the mean Lyman-alpha
   forest redshift z=3.57.
3. The likelihood-correlation result from the same ESPRESSO spectra is a correlated analysis
   control.  It is never counted as an additional independent measurement.

The downloaded arXiv source archives are pinned by SHA-256 in the manifest.  The runner verifies
the transcribed table against exact tokens in those sources.  This is a confrontation with
published measurement-level data, not a new reduction of raw telescope exposures.

## Leg A — literal discrete-tick test

For each primary absorber, convert the reported drift and uncertainty to the full registered
baseline.  Define the conservative observed envelope

\[
B_i=(|\dot z_i|+5\sigma_i)\Delta t_i.
\]

The smallest nonzero forward D0 change is

\[
J_i=(\varphi-1)(1+z_i).
\]

No Gaussian tail extrapolation is used.  The literal bridge “at least one D0 refinement tick
occurred between these two registered epochs” is excluded for a row when J_i>B_i.  If every row
passes, the bridge is rejected on both independent observing technologies.  This verdict does not
reject the internal Lean theorem because that theorem supplies no SI duration for a tick.

## Leg B — minimal continuous SI bridge

For sensitivity only, add one explicit bridge parameter rho >= 0 (ticks/year) and the unique smooth
constant-rate interpolation

\[
1+z(t)=(1+z_0)\varphi^{\rho t}.
\]

Eliminating z gives one common velocity drift for every target,

\[
A := c\,\dot z/(1+z)=c\rho\ln\varphi.
\]

No redshift-dependent coefficient is fitted.  Fit A by inverse-variance weighting to the ten GBT
measurements plus the single independent ESPRESSO pixel result.  Report:

- the unrestricted common-A fit and goodness of fit;
- GBT calibration followed by prediction of the ESPRESSO holdout;
- the one-sided positive-signal p-value;
- the boundary p-value for excluding the composite A>=0 family;
- the 99.9% one-sided upper limit on A and rho.

The frozen threshold is alpha=0.001.  A negative point estimate is not a detection of reverse D0
time.  If the positive family is not excluded at alpha, the result is a sensitivity bound, not a
confirmation or rejection of the internal law.

## Controls and scope

- The two ESPRESSO analysis methods must not be pooled as independent.
- The high-z holdout is evaluated against the low-z fit before the joint fit is interpreted.
- Leg A is parameter-free but conditional on a literal physical tick occurring in the registered
  interval.
- Leg B adds an external SI interpolation and therefore can only be an empirical bridge passport.
- Neither leg may promote an astronomical identification to Lean core.
