# D0 v15 Strong Log-Det Pressure Coupling

**Status:** LOGDET-PRESSURE-COUPLING-CERT-CLOSED

This document provides the strong internal derivation of positive loop-pressure response from the explicit volume dependence of the finite feedback operator \(F_N(V)\). It supersedes weaker bridge-law statements while preserving the passport boundary.

## Finite Identities (Clock Sector)

The relative archive/active ratio and normalized trace are:

\[
R(V) = e^{\kappa V} - 1, \qquad r_N(V) = \frac{R(V)}{1 + R(V)} = 1 - e^{-\kappa V}, \qquad \kappa = \log \varphi.
\]

Derivative:

\[
\partial_V r_N(V) = \kappa e^{-\kappa V} > 0.
\]

Clock-sector model of the feedback operator:

\[
F_N(V) = r_N(V) \Pi_{\rm clock} + F_\perp(V), \qquad \operatorname{rank} \Pi_{\rm clock} = d_\tau.
\]

## Loop Term and Derivative

The loop contribution to the partition function is:

\[
-\log\det(I - z F_N(V)) = -d_\tau \log(1 - z r_N(V)) + \text{orthogonal terms}.
\]

Pressure response (derivative w.r.t. normalized volume):

\[
\partial_V [-\log\det(I - z F_N(V))] = d_\tau \frac{z \kappa e^{-\kappa V}}{1 - z (1 - e^{-\kappa V})} > 0.
\]

## Resolvent Domain

The expression is defined on the resolvent domain:

\[
0 < z < 1 / \rho(F_N(V)).
\]

A globally safe sufficient condition (independent of the specific spectrum) is:

\[
0 < z < 1.
\]

## Guardrail (Strict)

This proves a dimensionless internal positive loop-pressure response derived from the volume dependence of \(F_N(V)\). It does not derive an H0 value, DESI likelihood, SPARC fit, or a physical FLRW scale factor. Survey comparison remains PASSPORT-LAYER only.

The weak bridge law (relative-pressure term \(\mathsf P_{rel} = c_R \Delta R_n\)) remains as historical support but is not the primary statement. The direct log-det derivation is the strong theorem.

## Relation to Prior Work

See `D0_v15_ARCHIVE_PRESSURE_COUPLING_FROM_RELATIVE_ACCELERATION.md` (weak bridge, status RELATIVE-PRESSURE-BRIDGE-LAW-CERT-CLOSED) and `D0_v15_RELATIVE_ARCHIVE_ACCELERATION_TO_COSMOLOGY_BRIDGE.md` for the upstream acceleration observable.

Executable verification is in `05_CERTS/vp_strong_logdet_pressure_coupling.py`.

## First and Second Response (Sign Corrected)

The log-det loop pressure term has positive first derivative \(L'(V)>0\) and negative second derivative \(L''(V)<0\) in the safe resolvent domain \(0<z<1\). Thus the finite feedback response is positive but bounded and saturating (decelerating).

For \(0<z<1\):

\[
\lim_{V\to\infty} L(V) = -d_\tau \log(1-z), \qquad \lim_{V\to\infty} L'(V) = 0.
\]

The second response is saturating/decelerating in the safe domain, not accelerating.

## Relation to Relative Archive Acceleration (No Contradiction)

Relative archive ratio \(R(V)=e^{\kappa V}-1\) has \(R''(V)=\kappa^2 e^{\kappa V}>0\) (accelerating geometry).

The log-det loop response saturates while relative geometry accelerates. These are distinct observables. The core proves a bounded pressure-response mechanism plus accelerating relative geometry.

## Statuses

- LOGDET-FIRST-PRESSURE-RESPONSE-CERT-CLOSED
- LOGDET-SECOND-RESPONSE-STABILITY-CERT-CLOSED (positive first, negative second, bounded saturation for 0<z<1; domain derived)

## Negative Controls (Extended)

- No H0 value extracted from topology or recurrence.
- No survey data (DESI, SPARC, IceCube, LIGO, etc.) enters the definition or the choice of \(z\) or the clock projector.
- Wrong derivative for \(r(V)\) (e.g., treating \(r(V)\) as constant) is forbidden.
- Confusing the relative archive ratio with a physical FLRW scale factor is forbidden.
- Using the expression outside the resolvent domain is forbidden.
- Claiming L'' >0 for safe 0<z<1 is forbidden.
- Confusing relative R acceleration with logdet L acceleration is forbidden.

## Passport Boundary

All numerical cosmology (BAO, CMB, H0 tension, survey likelihoods) is external comparison only. The core owns only the finite operator, the clock-sector decomposition, and the signs of the volume derivatives of the loop term on the declared domain.

Executable verification in `05_CERTS/vp_logdet_second_response_and_stability.py` (sign correction) and `vp_strong_logdet_pressure_coupling.py`.
