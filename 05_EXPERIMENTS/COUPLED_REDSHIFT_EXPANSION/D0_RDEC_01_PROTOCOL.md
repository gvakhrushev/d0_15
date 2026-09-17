# D0-RDEC-01 — coupled redshift-drift / expansion protocol

Status: retrospective form-frozen confrontation, 2026-09-03.  The public values were already
available and inspected before this executable passport was written, so this is not presented as a
prospective preregistration.

## Question

The continuous SI interpolation used by D0-RD-01 is

\[
1+z(t)=(1+z_0)\varphi^{\rho t},\qquad
\dot z=\rho\log\varphi\,(1+z).
\]

Combining it with the standard FLRW redshift-drift identity

\[
\dot z=(1+z)H_0-H(z)
\]

eliminates the independently unobservable tick rate from the *shape*:

\[
{H(z)\over 1+z}=H_0-\rho\log\varphi=\text{constant},\qquad
{D_H(z)\over r_d}={C\over 1+z}.
\]

This is not another search for phi-spaced peaks.  Phi and rho disappear from the tested shape; the
only fitted nuisance is the common positive normalization `C`.

## Frozen inputs and statistic

- Direct-drift leg: the hash-pinned D0-RD-01 verdict.  It is used only to establish that the same
  constant-rate bridge was already confronted with GBT and ESPRESSO measurements.
- Expansion leg: the six `DH_over_rs` rows in the official DESI DR2 Gaussian BAO mean and their
  published covariance.
- Primary model: `DH_over_rs = C/(1+z)`.
- Primary statistic: generalized least-squares chi-square; dof = 6 - 1.
- Decision threshold: `p < 0.001` rejects the coupled constant-rate FLRW bridge.
- Phi, rho, redshift bins, covariance, and the exponent `-1` may not be fitted.

## Independence and controls

The direct-drift measurements (GBT H I and ESPRESSO Lyman-alpha spectroscopy) and the DESI radial
BAO expansion measurements are distinct observable/analysis blocks.  Within DESI, the first five
galaxy-tracer radial points calibrate `C` and the `z=2.33` Lyman-alpha radial point is reported as a
holdout.  It is not claimed to be a separate survey.

Controls are fixed:

- fit a free smooth exponent `C(1+z)^alpha` and compare `alpha=-1` by one nested degree of freedom;
- reverse the shape to `C(1+z)`;
- leave out each radial BAO point in turn;
- report explicitly whether rejection disappears when the Lyman-alpha point is removed.

## SI single-section collision

The existing D0 single action section supplies the candidate microscopic duration

\[
\tau_e={h\over38m_ec^2}.
\]

Identifying one cosmological refinement tick with this duration is a separate bridge and is tested
against the D0-RD-01 upper limit on rho.  Rejection of that identification does not reject the
dimensionless coefficient 38; it proves that the microscopic terminal cycle is not the astronomical
refinement clock unless an additional derived dimensionless scale-separation factor is provided.

## Dark-response boundary

Internally D0 proves `f_archive=z_D0/(1+z_D0)`, hence conditionally
`DH/rd=C(1-f_archive)`.  This passport does **not** label `f_archive` as observed dark energy,
lensing mass, or a density fraction.  No independent dark-response dataset/representation is
present in this run, so the dark leg remains an explicit application obligation rather than a
post-hoc reinterpretation of BAO.

