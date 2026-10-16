"""Candidate finite C1 transport arithmetic for a supplied history-to-cell map.

The map is an input. Nothing in this module chooses a spatial measure,
identifies AF depth with a smooth parameter, or drops the normalizer derivative.
"""

from __future__ import annotations

from fractions import Fraction


class Quad:
    """Element a + b p of Q(p), p>0, p^2 = 1-p."""

    def __init__(self, a, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other):
        other = _quad(other)
        return Quad(self.a + other.a, self.b + other.b)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        other = _quad(other)
        return Quad(self.a - other.a, self.b - other.b)

    def __rsub__(self, other):
        return _quad(other) - self

    def __mul__(self, other):
        other = _quad(other)
        # (a+bp)(c+dp) = ac + bd(1-p) + (ad+bc)p
        return Quad(
            self.a * other.a + self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return Quad(-self.a, -self.b)

    def __truediv__(self, other):
        if isinstance(other, Quad):
            norm = other.a * other.a - other.a * other.b - other.b * other.b
            if norm == 0:
                raise ZeroDivisionError("Quad")
            conjugate = Quad(other.a - other.b, -other.b)
            return (self * conjugate) / norm
        scale = Fraction(other)
        if scale == 0:
            raise ZeroDivisionError("rational")
        return Quad(self.a / scale, self.b / scale)

    def __eq__(self, other):
        other = _quad(other)
        return self.a == other.a and self.b == other.b

    def __lt__(self, other):
        return (_quad(other) - self).is_positive()

    def __repr__(self):
        return f"Quad({self.a}, {self.b})"

    def is_zero(self):
        return self.a == 0 and self.b == 0

    def is_positive(self):
        """Strict positivity via u + v sqrt(5), doubled out of the basis."""
        u = 2 * self.a - self.b
        v = self.b
        if v == 0:
            return u > 0
        if v > 0:
            if u >= 0:
                return True
            return 5 * v * v > u * u
        if u <= 0:
            return False
        return u * u > 5 * v * v


def _quad(value):
    if isinstance(value, Quad):
        return value
    return Quad(value, 0)


P = Quad(0, 1)


def mass(weights):
    total = None
    for value in weights.values():
        total = value if total is None else total + value
    if total is None:
        raise ValueError("empty weight set")
    return total


def moment(weights, prices):
    total = None
    for key, weight in weights.items():
        term = weight * prices[key]
        total = term if total is None else total + term
    if total is None:
        raise ValueError("empty weight set")
    return total


def normalized_average(weights, prices):
    """A = M/Z. Requires Z != 0. Does not discard dZ; this is only the value."""
    return moment(weights, prices) / mass(weights)


def full_derivative(weights, dweights, prices, dprices):
    """D A = (DM - A DZ) / Z, the quotient rule with the normalizer kept."""
    z = mass(weights)
    a = moment(weights, prices) / z
    dm = None
    for key, weight in weights.items():
        term = dweights[key] * prices[key] + weight * dprices[key]
        dm = term if dm is None else dm + term
    dz = mass(dweights)
    return (dm - a * dz) / z


def deleted_z_derivative(weights, dweights, prices, dprices):
    """Illegal (DM)/Z. Equal to the full derivative iff A DZ = 0."""
    z = mass(weights)
    dm = None
    for key, weight in weights.items():
        term = dweights[key] * prices[key] + weight * dprices[key]
        dm = term if dm is None else dm + term
    return dm / z


def deletion_gap(weights, dweights, prices, dprices):
    """bad - full = A (DZ) / Z, coefficient 1."""
    z = mass(weights)
    a = moment(weights, prices) / z
    dz = mass(dweights)
    return a * dz / z


def pushforward(weights, assignment, cells):
    """Hard finite map. Cells missed by the map keep weight 0."""
    zero = None
    for value in weights.values():
        zero = value * 0
        break
    if zero is None:
        raise ValueError("empty weight set")
    pushed = {cell: zero for cell in cells}
    for cylinder, weight in weights.items():
        pushed[assignment[cylinder]] = pushed[assignment[cylinder]] + weight
    return pushed


def normalized_probability(weights):
    z = mass(weights)
    return {key: value / z for key, value in weights.items()}


def probability_derivative(weights, dweights):
    """D(w/Z) = (Z Dw - w DZ) / Z^2 on each label."""
    z = mass(weights)
    dz = mass(dweights)
    return {
        key: (z * dweights[key] - weights[key] * dz) / (z * z)
        for key in weights
    }


def l1(left, right):
    keys = set(left) | set(right)
    total = None
    for key in keys:
        term = abs(left.get(key, 0) - right.get(key, 0))
        total = term if total is None else total + term
    return 0 if total is None else total


def oscillation(prices):
    values = list(prices.values())
    return max(values) - min(values)


def weight_value_bound(theta, osc):
    """Coefficient 1/2 in front of ||p-r||_1 osc(L)."""
    return theta * osc / 2


def partition_motion_bound(reassigned_fraction, osc):
    """Coefficient 1 in front of rho * osc(L)."""
    return reassigned_fraction * osc


def reassigned_fraction(weights, assignment, other):
    z = mass(weights)
    moved = None
    for cylinder, weight in weights.items():
        if assignment[cylinder] != other[cylinder]:
            moved = weight if moved is None else moved + weight
    if moved is None:
        moved = z * 0
    return moved / z


def fiber_defect(cylinder_weights, cylinder_prices, cell_prices, assignment):
    pulled = {cylinder: cell_prices[assignment[cylinder]] for cylinder in cylinder_weights}
    return normalized_average(cylinder_weights, cylinder_prices) - normalized_average(
        cylinder_weights, pulled
    )


def fiber_derivative_bound(eps_prime, eta_star, dmu_l1, dz_abs, z):
    """Coefficient 1 on both the jet max and the weight-motion factor."""
    return eps_prime + eta_star * (dmu_l1 + dz_abs) / z


def coarse_fiber_derivative_bound(eps_prime, eps, dmu_l1, z_min):
    """Corollary coefficient 4 = 2 * 2. Not claimed sharp. Requires mu >= 0."""
    return eps_prime + 4 * eps * dmu_l1 / z_min


def weight_derivative_bound(theta1, osc, theta, max_abs_dl):
    """Coefficient 1/2 on the normalized-weight jet, coefficient 1 on theta."""
    return theta1 * osc / 2 + theta * max_abs_dl


def real_cost_children(ready, pending):
    """Ready cylinders split; pending cylinders are carried, not split."""
    parent = {}
    for cylinder in ready:
        parent[("direct", cylinder)] = cylinder
        parent[("start", cylinder)] = cylinder
    for cylinder in pending:
        parent[("complete", cylinder)] = cylinder
    return parent


def false_uniform_split(ready, pending):
    """Different refinement: every leaf, including pending, is split in two."""
    parent = {}
    for cylinder in list(ready) + list(pending):
        parent[("left", cylinder)] = cylinder
        parent[("right", cylinder)] = cylinder
    return parent


def refine_golden_weights(weights, ready, pending):
    """Factors p and p^2 on a ready split; factor 1 on a pending carry."""
    refined = {}
    for cylinder in ready:
        refined[("direct", cylinder)] = P * weights[cylinder]
        refined[("start", cylinder)] = (P * P) * weights[cylinder]
    for cylinder in pending:
        refined[("complete", cylinder)] = weights[cylinder]
    return refined


def commuting_assignment(assignment, parent):
    return {child: assignment[parent_cylinder] for child, parent_cylinder in parent.items()}
