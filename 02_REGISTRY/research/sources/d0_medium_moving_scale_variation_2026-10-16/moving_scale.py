"""Candidate slots for the moving-scale variation.

The metric Euler tensor of a field-dependent E4 coefficient is recorded only
on the diagonal one-variable family. No scale, preparation, or observer law
is selected.
"""

from __future__ import annotations


def volume_source_factor(k):
    """Coefficient of q^{μν} for the unnormalized integrand k dVol."""
    return k / 2


def volume_source_frobenius_square(k, dimension=4):
    """S^{μν}=(k/2) q^{μν} has S_{αβ} S^{αβ} = (k/2)^2 * dimension."""
    return (k * k * dimension) / 4


def e4_family_contravariant(b, c, d, b1, c1, d1, b2, c2, d2, f1, f2):
    """Raised diagonal components of the metric Euler density on g=diag(1,b,c,d).

    Returns (E^{yy}, E^{zz}, E^{ww}) for the coefficient f(x). The yy slot does
    not use (b1, b2); zz does not use the c-jet; ww does not use the d-jet.
    """
    ey = (
        2 * c * c1 * d * d1 * f2
        + f1 * (2 * c * c1 * d * d2 - c * c1 * d1**2 + 2 * c * c2 * d * d1 - c1**2 * d * d1)
    ) / (2 * b * c**2 * d**2)
    ez = (
        2 * b * b1 * d * d1 * f2
        + f1 * (2 * b * b1 * d * d2 - b * b1 * d1**2 + 2 * b * b2 * d * d1 - b1**2 * d * d1)
    ) / (2 * b**2 * c * d**2)
    ew = (
        2 * b * b1 * c * c1 * f2
        + f1 * (2 * b * b1 * c * c2 - b * b1 * c1**2 + 2 * b * b2 * c * c1 - b1**2 * c * c1)
    ) / (2 * b**2 * c**2 * d)
    return ey, ez, ew


def chain_coefficient(gamma, alpha, t):
    return gamma * alpha * t**2 / 2


def chain_differential(gamma, alpha, t, d_alpha, d_t):
    return (gamma * t**2 / 2) * d_alpha + (gamma * alpha * t) * d_t


def finite_alpha_step(p, x_n, y_n, f0_prime, f1_prime):
    """One cut step of alpha_n. n is not a coordinate."""
    x_next = p * x_n + y_n
    y_next = (p**2) * x_n
    alpha = (p**2) * (x_n * f0_prime + y_n * f1_prime)
    alpha_next = (p**2) * (x_next * f0_prime + y_next * f1_prime)
    return alpha_next - alpha, x_next, y_next


def centered_directional(weights, prices, d_weights, d_prices):
    """D(M/Z) = (DM - A DZ) / Z for one common normalizer Z=Σ weights."""
    total_z = sum(weights)
    total_m = sum(w * price for w, price in zip(weights, prices))
    average = total_m / total_z
    d_m = sum(
        dw * price + w * dp
        for w, price, dw, dp in zip(weights, prices, d_weights, d_prices)
    )
    d_z = sum(d_weights)
    return (d_m - average * d_z) / total_z, average


def preparation_directional(d_z, z_value, g0):
    """Faithful-optimum source -d log Z(E) / g0. g0 is not the metric."""
    return -d_z / (g0 * z_value)


def quotient_t_derivatives(t):
    """Full d/dt of t^2/(1+t^2), freezing Z, and freezing the numerator."""
    numerator = t**2
    zone = 1 + t**2
    full = (2 * t * zone - numerator * 2 * t) / zone**2
    freeze_zone = (2 * t) / zone
    freeze_numerator = numerator * (-2 * t) / zone**2
    return full, freeze_zone, freeze_numerator


def flat_partial_freeze_yy(kappa):
    """yy component of κ(∇∇(t^2) - g □(t^2)) for t=x on flat R^4.

    The xx component of the same tensor is zero. Dropping the Hessian only
    inside -c G leaves this yy source.
    """
    return -2 * kappa


def measure_slot(pi_n, error=None, d_error=None):
    """M06 scalar slot. It is not a summand of G^{μν}."""
    if pi_n is None:
        return {
            "status": "unevaluated",
            "reason": "pi_N(X) missing",
            "absorbed_into_G": False,
            "error": None,
            "d_error": None,
        }
    return {
        "status": "supplied",
        "reason": "arrow supplied by the caller",
        "absorbed_into_G": False,
        "error": error,
        "d_error": d_error,
    }
