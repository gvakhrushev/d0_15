# PHI-P_DESI_01 — redshift-ladder empirical protocol

Status: frozen analysis protocol, 2026-08-31.

This protocol separates two observables that the old draft had combined:

1. an object-catalogue test of excess density at the fixed redshift levels
   \(z_n=\varphi^n-1\);
2. a compressed-BAO test of the direct physical reading
   \(H(z)=H_0\varphi^{-\lfloor\log_\varphi(1+z)\rfloor}\).

They are not interchangeable.  DESI BAO points are distance/expansion measurements in broad
redshift bins; they are not peaks in the catalogue of individual object redshifts.

## Leg A — DESI DR1 QSO level-excess test

This leg is frozen before downloading or reading the values in
`QSO_cat_iron_cumulative_v0.fits`.

- Source: official DESI DR1 QSO catalogue,
  `https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/QSO/iron/QSO_cat_iron_cumulative_v0.fits`.
- Fixed levels: \(n=1,2,3\), hence \(z\approx0.618034,1.618034,3.236068\).  No level, origin,
  base, or phase may be fitted.
- Primary coordinate: \(x=\log_\varphi(1+z)\).
- Primary half-width: \(\delta=0.01\) in x.  The core is \(|x-n|\le\delta\); the equal-width
  local control is \(\delta<|x-n|\le2\delta\).
- Primary statistic: the pooled conditional one-sided binomial test of core counts against the
  equal-width local controls, with null probability 1/2.  The per-level counts and effects must
  also be reported; pooling may not hide a sign reversal at any level.  The frozen decision
  threshold is one-sided p < 0.001.
- Robustness widths: 0.005 and 0.02 are diagnostics only.  They cannot replace the primary result.
- Quality selection: finite positive final redshift, `ZWARN == 0` when present, MAIN survey when
  present, DARK program when present, and one deterministic record per `TARGETID` (minimum
  `ZERR`, then first file order).  The exact available columns and every applied/fallback cut are
  emitted by the runner.
- A DESI-only p-value is not an independent physical confirmation: targeting and redshift-pipeline
  structure can create features in n(z).  A positive DESI result remains `DESI_ONLY_SIGNAL` until
  the same frozen statistic and levels reproduce in an independently reduced survey (reserved
  confirmation owner: SDSS DR16Q) and in the future DESI DR2 catalogue without refitting.
- Negative controls: half-phase levels \(n+1/2\), width mutations, and removal of each level in
  turn.  Controls diagnose selection artifacts; they do not redefine the primary test.
- Pipeline diagnostics: repeat the frozen count statistic on `Z_RR` and `Z_QN` where finite.  These
  are not independent astronomical detections, but disagreement with final `Z` flags a redshift
  estimator artifact.

Because the catalogue was already public when this protocol was written, this is a frozen
prospective *analysis* but not a historically pre-data prediction.  The older claims “~10%” and
“3.2 sigma” have no located data/code provenance in the current repository and are not carried
forward as results.

## Leg B — DESI DR2 BAO step-H test

This is a retrospective, parameter-frozen falsification test: the DESI values were public and
inspected while the executable passport was being prepared, but the tested formula and phi were
already fixed by the recovered draft.

- Source: official DESI DR2 Gaussian BAO likelihood linked by the DESI DR2 results page:
  `CobayaSampler/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_{mean,cov}.txt`.
- Observable: only rows labelled `DH_over_rs`, since \(D_H/r_d=c/[H(z)r_d]\).
- Frozen model vector:
  \[
  (D_H/r_d)_i=C\,\varphi^{\lfloor\log_\varphi(1+z_i)\rfloor}.
  \]
- The only fitted nuisance parameter is the positive common scale C.  Phi, the phase origin,
  step boundaries, redshift bins, and covariance are not fitted.
- Test statistic: generalized least-squares chi-square with the published covariance; degrees of
  freedom = number of `DH_over_rs` points minus one.
- Decision: p < 0.001 rejects the direct physical step-H reading; otherwise it is merely not
  rejected.  No outcome can promote the internal D0 redshift construction to an astronomical
  identification.
- Mutation controls: reverse-sign ladder \(C\varphi^{-k}\), a smooth power law, and leave-one-bin-out
  diagnostics.  They cannot rescue or replace the frozen primary model.

## Scope

A rejection of Leg B says that the symbol H in the recovered formula cannot be the conventional
Hubble expansion rate under the stated bridge.  It does not reject the Lean-proved internal
depth/frequency relations.  A Leg A excess, if any, is an empirical catalogue feature until a
second independent survey and instrument-specific selection audit reproduce it.
