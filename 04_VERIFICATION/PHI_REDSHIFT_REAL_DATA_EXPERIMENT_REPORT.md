# PHI-P_DESI_01 — real-data experiment report

Date: 2026-08-31  
Verdict: the recovered catalogue-level phi claim is not reproduced, and the direct physical
step-H interpretation is decisively rejected.

## What was tested

The recovered draft contained two different observational statements:

\[
z_n=\varphi^n-1
\]

as a possible excess of object redshifts near fixed levels, and

\[
H(z)=H_0\varphi^{-\lfloor\log_\varphi(1+z)\rfloor}
\]

as a stepwise expansion history.  The first requires a QSO object catalogue.  The second requires
the radial BAO observable \(D_H/r_d=c/[H(z)r_d]\).  Treating DESI BAO bins as catalogue redshift
peaks would mix the two experiments and is forbidden by the frozen protocol.

The exact protocol is in `08_PASSPORTS/DESI/PHI_P_DESI_01_PROTOCOL.md`.  The old “~10%” and
“3.2 sigma” statements were not found with supporting data, code, or a hash manifest in the current
repository or its searched git history, so they were treated as unverified historical notes.

## A. DESI DR1 QSO object-level test

Official input: `QSO_cat_iron_cumulative_v0.fits`, 816,203,520 bytes, official and local SHA-256

`a65604303cc29af8865db9193a23934b2540591b16c5afd2a4bea2d61464aef4`.

The protocol was frozen before the QSO redshift values were read.  Selection used finite positive
final Z, `ZWARN=0`, MAIN/DARK, followed by deterministic `TARGETID` deduplication by minimum finite
`ZERR`.  This left 1,497,382 unique quasars from 2,182,309 catalogue rows.

For \(x=\log_\varphi(1+z)\), fixed levels \(n=1,2,3\), and pre-fixed half-width
\(\delta=0.01\), the equal-width local core/sideband result was:

| level | predicted z | core | side control | core fraction | one-sided p |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.618033989 | 3,687 | 3,521 | 0.511515 | 0.02598 |
| 2 | 1.618033989 | 20,961 | 20,721 | 0.502879 | 0.12086 |
| 3 | 3.236067977 | 4,435 | 4,307 | 0.507321 | 0.08719 |
| pooled | — | 29,083 | 28,549 | 0.504633 | **0.01320** |

Frozen decision threshold: one-sided p < 0.001 with the same positive sign at all three levels.
The DESI final-redshift result therefore is
`NO_DESI_LEVEL_EXCESS_AT_FROZEN_PRIMARY_SCALE` (about 2.22 sigma one-sided, not a detection).

The apparent effect is not scale-stable: at \(\delta=0.005\), pooled p is about 0.0567; at
\(\delta=0.02\), the core becomes a deficit (57,632 versus 59,950).  These widths are diagnostics,
not alternative primary tests.

### Redshift-estimator control

On the same selected spectra:

| estimator | core | side | core fraction | one-sided p | reading |
|---|---:|---:|---:|---:|---|
| final `Z` | 29,083 | 28,549 | 0.504633 | 0.01320 | below frozen threshold |
| `Z_RR` | 29,274 | 28,906 | 0.503163 | 0.06406 | no excess |
| `Z_QN` | 28,779 | 27,888 | 0.507862 | 0.00009245 | estimator-only formal excess |

The `Z_QN` pooled value corresponds to about 3.74 sigma one-sided, but it is not a common
three-level effect: level 1 is a deficit (3,109 core versus 3,419 side), while levels 2 and 3 drive
the statistic.  The feature weakens in the final adopted redshift and in Redrock.  It therefore
has the signature of estimator/selection structure, not two independent detections of a physical
phi lattice.  It may explain how an exploratory “~3.2 sigma” statement could arise without being
a robust physical result.

## A2. Independent-survey replication: SDSS DR16Q

The identical frozen statistic was run without refitting on the SDSS DR16Q quasar-only catalogue,
obtained as the two-column best-redshift table from CDS/VizieR VII/289.  It contains 750,414 unique
quasars; the pinned response SHA-256 is

`996c167c6469b0dc01670d6b2d9de4241ea396ce50e2b1cdbb430effc901769e`.

| level | predicted z | core | side control | core fraction | one-sided p |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.618033989 | 2,593 | 2,639 | 0.495604 | 0.7422 |
| 2 | 1.618033989 | 9,441 | 9,429 | 0.500318 | 0.4689 |
| 3 | 3.236067977 | 2,628 | 2,561 | 0.506456 | 0.1798 |
| pooled | — | 14,662 | 14,629 | 0.500563 | **0.42584** |

Verdict: `NO_INDEPENDENT_SDSS_LEVEL_EXCESS_REPLICATION`.  SDSS uses a different survey,
instrument history, target selection, and redshift pipeline.  Exact object overlap with DESI was
not removed, so even a positive result would still require a dedicated overlap/selection audit;
the observed null needs no such promotion.

## B. DESI DR2 BAO direct step-H test

Official input: the DESI-linked Cobaya Gaussian DR2 BAO likelihood, all-tracer mean vector and full
covariance.  Both files were downloaded, hash-pinned, and marked `sample_data=false`.

Since DESI reports \(D_H/r_d=c/[H(z)r_d]\), the recovered law predicts

\[
(D_H/r_d)_i=C\varphi^{k_i},\qquad
k_i=\lfloor\log_\varphi(1+z_i)\rfloor.
\]

Only the positive normalization C was fitted.  Phi, phase origin, steps, bins, and covariance were
not fitted.  The six radial BAO points have frozen step assignment `[0,1,1,1,1,2]`.

- best-fit \(C=4.66112346\);
- \(\chi^2=7631.137391\) for 5 degrees of freedom;
- p = \(1.47381734624\times10^{-1652}\);
- verdict: `REJECT_DIRECT_PHYSICAL_STEP_H`.

The direction-reversed ladder is much less bad but still has \(\chi^2=449.37\).  A fitted smooth
power-law diagnostic gives \(\chi^2=26.00\).  Therefore the failure is not a rounding issue at a
single phi boundary: the recovered physical step law has the wrong global behavior and forces four
widely separated BAO points inside one constant step.

## Theory consequence

This is a useful negative closure, not a failure of the internal formalization.

1. The Lean-proved internal depth/frequency cocycle remains exactly what it was: a conditional
   internal/bridge theorem.
2. The stronger astronomical identification “QSO redshifts have phi-level excesses” is not
   independently detected under the frozen local statistic.
3. The direct identification of the recovered step function with conventional Hubble \(H(z)\) is
   empirically false and must not be used as a D0 prediction.
4. The `Z_QN` control demonstrates why the project requires two independent detections: a
   catalogue algorithm can manufacture a formally impressive sigma without the final estimator or
   an independent survey reproducing it.

The next live red point should therefore be a bridge-derived relation whose apparatus mapping is
specified before data — most naturally a calibrated redshift-drift relation — rather than another
search for peaks at phi-labelled catalogue coordinates.

