# Physical redshift detection passport — closure report

Date: 2026-08-26

## Verdict

The next edge after the internal self-unfolding redshift relation is closed at its maximal honest
scope.  There are two simultaneous results:

1. `D0-PHYSICAL-REDSHIFT-DETECTION-PASSPORT-001` — conditional `BRIDGE-ASSUMPTIONS-EXPLICIT` theorem from a
   preregistered self-return-covariant positive frequency detector to the standard ratio
   `nu_em/nu_obs` and its drift;
2. `D0-RAW-DOUBLE-DETECTION-REDSHIFT-NOGO-001` — unconditional structural NO-GO showing that two raw
   positive registrations alone are ratio-surjective and cannot select the golden redshift law.

Bridge owner: `D0.Bridge.PhysicalRedshiftDetection`.

Internal protocol theorems: `D0.Cosmology.PhysicalRedshiftDetectionPassport`.

Certificate:
`05_CERTS/vp_physical_redshift_detection_passport.py`.

## Positive forcing chain

The preregistered protocol contains a positive constant one-step multiplier `p`, one common
one-step covariance law, and the already-owned self-return closure `p+p^2=1` on `0<p<1`.

Lean proves:

- `p=phi^-1` (`protocol_tickMultiplier_eq_phi_inv`);
- `nu(n)=nu(0)phi^-n` (`protocol_readout_closed_form`);
- the relative calibration is constant (`protocol_relativeCalibration_constant`);
- division-free transport `nu_obs * phi^(o-e)=nu_em`;
- `nu_em/nu_obs=phi^(o-e)=1+zD0`;
- `Delta z_phys=(phi-1)(1+z_phys)` for a repeated observation.

The absolute normalization is present but cancels.  No second redshift or drift coefficient exists.

## Structural reductio and exact extra datum

For every raw positive detector define

`C_n = nu(n) / phi^-n`.

Lean proves universally

`nu_em/nu_obs = (C_em/C_obs) * phi^(o-e)`.

Therefore a rival ratio at the same depths implies `C_em != C_obs`.  This is the precise additional
outcome-affecting information required by the rival.  The theorem quantifies over every raw protocol;
it is not a finite search or an exhaustion claim about named cosmologies.

The raw layer is shown maximally non-selective by a parametric family: for every `r>0`, a positive
protocol at depths `0,1` realizes `nu_em/nu_obs=r`.  Removing the preregistered covariance therefore
destroys the conclusion.

## Mutation controls

The executable certificate rejects:

- post-data registration;
- fitting the tick/redshift generator;
- dropping the forbidden `depth_gap` fit guard;
- replacing the named frequency-ratio readout by an arbitrary detector number;
- a free multiplier `1/2`, which fails self-return closure;
- the negative second algebraic root, which fails positivity;
- a constant raw readout, which yields ratio `1` rather than `phi`;
- unequal emitter/observer calibrations hidden inside the raw ratio.

## Exact boundary

No empirical detection is claimed.  A concrete light/spectroscopy pipeline must still instantiate
`PreregisteredSelfReturnFrequencyProtocol`: it must expose positive readouts, freeze the readout and
fit policy before comparison, and establish the common self-return covariance.  If it cannot, the
NO-GO applies and `zD0` must not be called measured astronomical redshift.

No SI scale, Hubble parameter, FLRW model, DESI datum, or spectral-line catalogue enters the Lean
theorem.  Those belong to a later empirical application passport.
