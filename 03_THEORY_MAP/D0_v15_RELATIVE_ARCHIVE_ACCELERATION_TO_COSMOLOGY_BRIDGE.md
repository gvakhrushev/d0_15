# D0 v15 Relative Archive Acceleration to Cosmology Bridge

**Status:** RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED

This document integrates the relative archive acceleration bridge derived from the fractal tick recurrence in Informational Mechanics. It supplies the finite internal mechanism for apparent cosmological expansion under active-sector readout. Survey comparison (DESI, SPARC, H0, etc.) remains strictly PASSPORT-LAYER.

## Core Identities (Discrete)

The retained/active substrate and archive trace obey the exact recurrence from the stable detector tick:

\[
A_{n+1} = \varphi^{-1} A_n, \qquad B_{n+1} = B_n + \varphi^{-2} A_n.
\]

Closed-form solutions (with \(A_0\) initial retained substrate):

\[
A_n = A_0 \varphi^{-n}, \qquad B_n = A_0 (1 - \varphi^{-n}).
\]

The relative archive/active ratio is:

\[
R_n = \frac{B_n}{A_n} = \varphi^n - 1.
\]

Finite differences:

\[
\Delta R_n = \varphi^n (\varphi - 1), \qquad \Delta^2 R_n = \varphi^{n-2} > 0.
\]

## Continuum Envelope

The continuous limit (semigroup envelope) is:

\[
R(s) = e^{s \log \varphi} - 1.
\]

Second derivative (strictly positive acceleration):

\[
R''(s) = (\log \varphi)^2 e^{s \log \varphi} > 0 \quad (s \ge 0).
\]

## Link to Archive Pressure

The internal relative acceleration feeds the archive-pressure term in the finite thermodynamics:

\[
\mathsf P_{fb} = \beta^{-1} \partial_V \log Z_N.
\]

The core proves the existence and sign of the relative acceleration observable. It does not derive or fit external survey parameters (H0, w, etc.). Those remain passport-layer operations after the finite object is frozen.

## Negative Controls / Guardrails

- No H0 value is extracted from topology or recurrence alone.
- No DESI/SPARC/H0 numerical fit is performed or claimed inside the core.
- Absolute archive increment deceleration (\(\Delta^2 B_n < 0\)) is distinct from relative ratio acceleration (\(\Delta^2 R_n > 0\)).
- Survey data never enters the definition or choice of the finite recurrence or the ratio \(R_n\).

## Cert Support

Executable verification is provided by:

- `05_CERTS/vp_relative_archive_acceleration_cosmology_bridge.py`
- `05_CERTS/vp_fractal_continuum_predictions.py` (distinguishes absolute vs. relative second differences)

See also the fractal tick substrate in `D0_v15_INFORMATIONAL_MECHANICS_FRACTAL_TICK.md` and the prior continuum envelope work.

## Relation to Book 08

The bridge supplies the finite origin of the archive-pressure contribution to cosmological expansion. External likelihood comparisons remain separate passport protocols (see `08_PASSPORTS/` manifests and the empirical passport matrix).

## Passport Boundary (Strict)

This layer is INTERNAL and CERT-CLOSED at the level of the finite observable \(R_n\) and its continuum envelope. All numerical cosmology (BAO, supernovae, CMB, H0 tension, etc.) is PASSPORT-LAYER only. The core never selects, tunes, or claims agreement with external survey values.
