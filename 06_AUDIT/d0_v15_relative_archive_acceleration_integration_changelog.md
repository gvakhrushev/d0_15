# D0 v15 Relative Archive Acceleration Integration Changelog

## 1. Relative archive ratio added
New observable \(R_n = B_n / A_n\) (and continuum \(R(s)\)) derived from the fractal tick recurrence in Informational Mechanics. Discrete second difference \(\Delta^2 R_n = \varphi^{n-2} > 0\); continuum \(R''(s) > 0\).

## 2. Discrete acceleration proof added
Executable verification in `vp_relative_archive_acceleration_cosmology_bridge.py` and updated `vp_fractal_continuum_predictions.py` (distinguishes \(\Delta^2 B_n < 0\) absolute deceleration from \(\Delta^2 R_n > 0\) relative acceleration; required PASS tokens emitted).

## 3. Continuum acceleration proof added
\(R(s) = e^{s \log \varphi} - 1\), \(R''(s) = (\log \varphi)^2 e^{s \log \varphi} > 0\) for \(s \ge 0\). Verified symbolically and numerically. Internal only.

## 4. Book 08 patched
Replaced loose "archive pressure explains acceleration" with exact statement:
"The core proves internal relative archive acceleration. The absolute archive increment decelerates, while the relative archive/active ratio \(R_n = B_n / A_n\) accelerates. This supplies the finite internal mechanism feeding the archive-pressure term \(\mathsf P_{fb} = \beta^{-1} \partial_V \log Z_N\). Survey comparison remains passport-layer."

Equations for \(R_n\), \(\Delta^2 R_n\), \(R(s)\), \(R''(s)\) inserted. Normalized observable requirement stated.

## 5. Passport boundary preserved
All survey data (DESI, SPARC, H0, etc.) and numerical fits explicitly excluded from core definitions. New closure class and forbidden shortcuts added in Book 05. No H0 claim from topology.

## 6. Runner updated
`run_all_v15_closure_certs.py` now includes `vp_relative_archive_acceleration_cosmology_bridge.py`. Full run emits `PASS_RUN_ALL_V15_CLOSURE_CERTS`.

## 7. Maps and status
- New claim `D0-IM-COSMO-001` added to `theory_status_map.csv` and `CLAIM_TO_LEAN_MAP.csv` with `RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED` (CERT_ONLY for Lean).
- Book 05: `RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED` definition + forbidden shortcuts (H0 from topology, survey fits without passport, absolute/relative confusion).

Theory document `D0_v15_RELATIVE_ARCHIVE_ACCELERATION_TO_COSMOLOGY_BRIDGE.md` created with full equations and strict passport boundary statement.

All per executable cert evidence. No survey data used. No .lake / __pycache__ introduced.
