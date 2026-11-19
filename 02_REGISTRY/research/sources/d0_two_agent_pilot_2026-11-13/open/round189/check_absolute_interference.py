"""Rational checks of the B189 scale test and conditional modulus inequality."""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from math import isqrt


Z = F(1, 2**20)
SQRT_SCALE = 10**35


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True)
class Interval:
    """Closed rational enclosure. Square roots round outward on a fixed grid."""

    lo: F
    hi: F

    @staticmethod
    def cast(value):
        return value if isinstance(value, Interval) else Interval(F(value), F(value))

    def __add__(self, other):
        other = Interval.cast(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -Interval.cast(other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = Interval.cast(other)
        corners = [a * b for a, b in product((self.lo, self.hi), (other.lo, other.hi))]
        return Interval(min(corners), max(corners))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Interval.cast(other)
        require(other.lo > 0, "Positive denominator")
        return self * Interval(1 / other.hi, 1 / other.lo)

    def __pow__(self, exponent):
        answer = Interval.cast(1)
        for _ in range(exponent):
            answer = answer * self
        return answer

    def sqrt(self):
        require(self.lo >= 0, "Nonnegative radicand")

        def floor_at_scale(value):
            return isqrt(value.numerator * SQRT_SCALE**2 // value.denominator)

        return Interval(
            F(floor_at_scale(self.lo), SQRT_SCALE),
            F(floor_at_scale(self.hi) + 1, SQRT_SCALE),
        )


def check_scale():
    mass = F(11, 20)
    prefixes = (F(7, 11), F(13, 17))
    stop, go = F(5, 8), F(7, 16)
    other = F(7, 9)

    def probabilities(single, extra_go):
        raw = {}
        for depth, prefix in enumerate(prefixes, 1):
            raw[depth, 0] = prefix * stop
            raw[depth, 1] = prefix * go * single**depth * extra_go[depth - 1]
        denominator = sum(raw.values()) + other
        return ({key: weight / denominator for key, weight in raw.items()},
                other / denominator)

    p, p_other = probabilities(mass, (F(1), F(1)))
    recovered = p[2, 1] * p[1, 0] / (p[2, 0] * p[1, 1])
    kappa = F(5, 4)
    require(recovered == mass, "Unknown prefix and stop/go factors must cancel")
    require(sum(p.values()) + p_other == 1, "Other recorded histories are retained")
    require(probabilities(kappa * mass, (1/kappa, 1/kappa**2)) == (p, p_other),
            "An uncalibrated depth-specific launch must leave a gauge ambiguity")
    return str(recovered)


def check_universal_bounds():
    p_lo, p_hi = F(618, 1000), F(619, 1000)
    require(p_lo**2 + p_lo < 1 < p_hi**2 + p_hi, "Isolate the positive Golden root")
    require(1 - p_hi == F(381, 1000) and 1 - p_lo < F(383, 1000),
            "Bound p^2 using 1-p")
    require(F(383, 1000)/64 < F(6, 1000), "Bound the attenuation in B")
    require(F(612, 1000) == p_lo - F(6, 1000)
            and p_hi + F(6, 1000) == F(5, 8), "Bound the rotated w")
    require(4*(2*p_lo-1) == F(944, 1000) and 4*(2*p_hi-1) < 1, "Bound L")
    gamma = F(6, 1000)
    b = (8*p_hi*F(238, 1000)*gamma + (24*F(383, 1000)-4)*gamma**2
         + 16*p_hi*gamma**3 + 4*gamma**4)
    require(b < F(727, 100000), "Nonconstant coefficient sum of B")
    require(1 - 3*Z > 0 and F(1056, 1000)*b + Z*F(56, 1000)*b*b < F(1, 100),
            "Nonconstant coefficient sum of R divided by z")
    require(8*F(381, 1000)*F(612, 1000)*(1-2*F(5, 8)**2)*(1-Z)/64 > F(1, 200),
            "Lower bound for R' divided by z")
    a_lo, a_hi = F(786, 1000), F(787, 1000)
    require(a_lo*a_lo < p_lo and p_hi < a_hi*a_hi, "Bound sqrt(p)")
    require((a_lo-p_hi)/(a_hi+p_hi) > F(1, 10), "Lower bound for escort contrast")
    require(F(944, 1000)*F(2056, 1000) - Z > F(187, 100), "Lower bound for r_0/z")
    require(2*Z < F(1, 2) and Z < F(1, 144), "Lower bound for Phi'(r_0)")
    require(F(186, 100)**3 > F(5, 2)**2 and (1-F(201, 100)*Z)**3 > F(1, 4)
            and F(1, 10)+Z/2 < F(1, 9), "Upper bound for |Phi''|")
    require(F(1, 32000) - F(1, 90000) > 0, "Strict bound for all 0 < nu <= 1")


def multiply_polynomials(left, right):
    result = [Interval.cast(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i+j] += a*b
    return result


def report_coefficients(p):
    w = [p, p*p/64]
    w2 = multiply_polynomials(w, w)
    w4 = multiply_polynomials(w2, w2)
    b = [4*((w2[k] if k < len(w2) else 0) - w4[k]) for k in range(5)]
    b2 = multiply_polynomials(b, b)
    ell = 4*p**3
    coefficients = [-Z*Z*(1-ell)*value for value in b2]
    for k, value in enumerate(b):
        coefficients[k] += Z*(2-ell-Z*ell)*value
    coefficients[0] += Z*ell
    return coefficients


def category_masses(u):
    zero = 1-u
    twice = zero**2/4
    once = (zero**2+u**2)/4
    return twice, once, 1-twice-once


def check_fine_sum():
    p = (Interval.cast(5).sqrt() - 1)/2
    a = p.sqrt()
    coefficients = report_coefficients(p)
    p_escort = (p/(a+p), a/(a+p))
    powers = [[tuple(weight**k for k in range(9)) for weight in category_masses(u)]
              for u in p_escort]
    category_values = (F(-1), F(-1, 2), F(0))
    weight_cache = [{}, {}]
    averages = [Interval.cast(0), Interval.cast(0)]
    total = [Interval.cast(0), Interval.cast(0)]
    for labels in product(range(3), repeat=8):
        monomial = F(1)
        report = coefficients[0]
        for k, label in enumerate(labels, 1):
            monomial *= category_values[label]
            report += coefficients[k]*monomial
        require(F(186, 100)*Z < report.lo <= report.hi < F(201, 100)*Z,
                "All fine reports lie in the proved rare-report interval")
        modulus = report.sqrt()+(1-report).sqrt()
        counts = tuple(labels.count(i) for i in range(3))
        for end in range(2):
            if counts not in weight_cache[end]:
                edge = powers[end]
                weight_cache[end][counts] = edge[0][counts[0]]*edge[1][counts[1]]*edge[2][counts[2]]
            weight = weight_cache[end][counts]
            averages[end] += weight*modulus
            total[end] += weight
    require(all(value.lo <= 1 <= value.hi for value in total), "Escort laws sum to one")
    difference = averages[1]-averages[0]
    certified = Interval.cast(Z).sqrt()*(F(1, 32000)-F(1, 90000))
    require(difference.lo > certified.hi, "Fine sum satisfies the strict uniform bound at nu=1")
    return f"{float(difference.lo):.12g}"


def check_shared_site_obstruction():
    unit = ((1, 0), (0, 1), (-1, 0), (0, -1))
    local = Counter()
    for _, u, v, _ in product(range(4), repeat=4):
        d = [unit[(u+1) % 4][i] - unit[u][i] for i in range(2)]
        e = [unit[(u+v+1) % 4][i] - unit[(u+v) % 4][i] for i in range(2)]
        local[F(-sum(x*y for x, y in zip(d, e)), 2)] += 1
    require(local == {-1: 64, 0: 128, 1: 64}, "Original 00/01 local moment counts")
    mean = sum(value*n for value, n in local.items())/256
    second = sum(value**2*n for value, n in local.items())/256
    require(mean == 0 and second == F(1, 2), "Shared SITE correlates the sign inputs")
    return str(second)


def main():
    mass = check_scale()
    check_universal_bounds()
    print(json.dumps({
        "quadratic_mass_recovered": mass,
        "launch_confounds_are_not_identified": True,
        "strict_sign_for_all_nu_in_(0,1]": True,
        "checked_fine_categories_at_nu_1": 3**8,
        "display_fine_expectation_difference_at_nu_1": check_fine_sum(),
        "shared_site_second_moment": check_shared_site_obstruction(),
        "original_physical_Book_binding_proved": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
