# D0-RD-01 — direct redshift-drift real-data report

Date: 2026-09-03

## Verdict

The experiment closes two different questions and does not merge their scopes.

1. **Literal discrete physical tick: rejected.**  Assigning one or more forward D0 refinement
   ticks to any registered observing baseline predicts a minimum change
   `Delta z=(phi-1)(1+z)`.  For all ten GBT H I absorbers and the independent ESPRESSO Lyman-alpha
   sightline this is outside the conservative `|measured change|+5 sigma` envelope.  The weakest
   separation is still `5.1023e4`.
2. **Continuous SI-rate bridge: no detection, not rejected at the frozen alpha=0.001.**  The
   one-parameter interpolation `1+z(t)=(1+z0)phi^(rho t)` eliminates redshift and predicts a common
   velocity drift `A=c rho ln(phi) >= 0`.  The unrestricted joint fit is
   `A=-4.9321 +/- 1.8889 m/s/yr`; the positive-signal p-value is `0.99549`.  The boundary p-value
   against the whole nonnegative family is `0.004513` (about `2.61 sigma` one-sided), above the
   inherited project-wide rejection threshold.
   Hence this is a null/sensitivity result, not evidence for reverse time and not a confirmation.

At 99.9% one-sided confidence the continuous bridge is bounded by

`A < 0.90514 m/s/yr`, `rho < 6.2742e-9 tick/yr`,

or, equivalently within this external interpolation only, more than `1.5938e8 yr` per
multiplicative phi tick.

## Independent-observable check

The ten-object GBT calibration gives `A=-5.5207 +/- 2.2285 m/s/yr`.  Without refitting it predicts
the independent high-redshift ESPRESSO measurement `-3.43 +/- 3.56 m/s/yr` with a holdout residual
of only `0.498 sigma`.  This agreement is not a detection: both blocks are consistent with a signal
far below their present sensitivity and their central values have the wrong sign for `rho>0`.

The second ESPRESSO likelihood-correlation estimate (`-3.63 +/- 3.65 m/s/yr`) uses the same spectra.
It is retained as a correlated analysis control and is explicitly prohibited from entering the
joint inverse-variance fit.  Counting it would spuriously reduce the uncertainty from `1.889` to
`1.678 m/s/yr`.

## Data and reproducibility

- Low-z primary source: Darling, *Toward a Direct Measurement of the Cosmic Acceleration*,
  arXiv:1211.4585, Table 1.
- High-z primary source: Trost et al., *The ESPRESSO Redshift Drift Experiment III*,
  arXiv:2603.02318, three epochs and two analysis methods.
- Both arXiv source archives are locally pinned by SHA-256.  The runner verifies exact source
  tokens and the hash of the transcribed measurement table before computing a statistic.
- Protocol: `08_PASSPORTS/REDSHIFT_DRIFT/D0_RD_01_PROTOCOL.md`.
- Manifest: `08_PASSPORTS/REDSHIFT_DRIFT/d0_rd_01_manifest.json`.
- Measurements: `08_PASSPORTS/REDSHIFT_DRIFT/direct_redshift_drift_measurements.csv`.
- Verdict: `08_PASSPORTS/REDSHIFT_DRIFT/d0_rd_01_verdict.json`.
- Certificate: `05_CERTS/vp_d0_redshift_drift_direct.py`.

This is a published-measurement-level confrontation, not a new reduction of raw telescope
exposures.  The official VizieR record for ESPRESSO Paper I supplies fitted metal-line parameters,
not the three-epoch pixel spectra required to reproduce Paper III's full spectral likelihood.
The headline values were public and inspected before the protocol was written, so this is also a
retrospective form-frozen test, not a prospective discovery claim.

## Exact theory boundary

The Lean theorem `internal_redshift_drift_relation` is discrete and supplies no conversion from a
refinement tick to years.  Therefore Leg A rejects the *literal astronomical representation* that
places a nonzero tick in the measured interval, not the internal theorem.  Leg B deliberately adds
the missing SI map as one visible parameter and stays `EMPIRICAL-PASSPORT`; its rate bound must not
be promoted to `CORE-FORMALIZED`.

The useful conclusion is structural: current direct observations already rule out a naive
one-observation-step equals one-D0-tick reading by at least four orders of magnitude, while their
precision is still insufficient to decide a sufficiently slow continuous physical realization at
the frozen threshold.
