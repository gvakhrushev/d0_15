#!/usr/bin/env python3
"""Outward interval certificate for the actual primary full128 pointer jet.

Only the static D0 needed by the small-matter linear coefficient is built.
The complete literal Julia/Walsh rows, both ports, CAR16 and RIGHT128 are
retained. This computes an entropy observable and the known port payment;
it does not choose Shannon as physical Book Info or select a full label code.
"""

import hashlib
import importlib.util
import json
import math
import os
from fractions import Fraction as Q
from pathlib import Path
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True
import numpy as np


PINS = {
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_primary_car_preparation_source.py":
        "889053f6da84501769d23ab84186c2189e6c026414db623919f4934098fb6c34",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py":
        "c67285c7469db49ff61f3e52597d0bcc6aad991ec1f7af025d6daeb065a43edf",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/RESULT.md":
        "290772fb869cfa73ed0cc419d3182048d80ea9b02312be0b9d56ad558f5c47be",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/RESULT.md":
        "9a441405c455adda9651f88c21fcda4d9383673a3718e88a93aeb50467133e71",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md":
        "2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79",
}
NEG_INF, POS_INF = -np.inf, np.inf
UNIT = Q(1, 2 ** 53)
TINY = np.nextafter(0., 1.)


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


def down(value):
    return np.nextafter(value, NEG_INF)


def up(value):
    return np.nextafter(value, POS_INF)


def rational_bounds(value):
    value = Q(value)
    lower = upper = float(value)
    if Q.from_float(lower) > value:
        lower = float(down(lower))
    if Q.from_float(upper) < value:
        upper = float(up(upper))
    require(Q.from_float(lower) <= value <= Q.from_float(upper),
            "exact rational-to-binary64 enclosure")
    return lower, upper


class I:
    """Local interval arrays; each basic operation rounds outwards."""

    def __init__(self, lower, upper=None):
        self.lo = np.asarray(lower, dtype=np.float64)
        self.hi = np.asarray(lower if upper is None else upper, dtype=np.float64)
        require(np.all(np.isfinite(self.lo)) and np.all(np.isfinite(self.hi))
                and np.all(self.lo <= self.hi), "finite ordered interval endpoints")

    @classmethod
    def rational(cls, value):
        return cls(*rational_bounds(value))

    def __getitem__(self, item):
        return I(self.lo[item], self.hi[item])

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __add__(self, other):
        if not isinstance(other, I):
            other = I.rational(other)
        lo, hi = down(self.lo + other.lo), up(self.hi + other.hi)
        exact_zero = (self.lo == 0) & (self.hi == 0) & (other.lo == 0) & (other.hi == 0)
        return I(np.where(exact_zero, 0., lo), np.where(exact_zero, 0., hi))

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other if isinstance(other, I) else -I.rational(other))

    def __mul__(self, other):
        if not isinstance(other, I):
            other = I.rational(other)
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        lo = down(np.minimum.reduce(products))
        hi = up(np.maximum.reduce(products))
        exact_zero = ((self.lo == 0) & (self.hi == 0)) | ((other.lo == 0) & (other.hi == 0))
        return I(np.where(exact_zero, 0., lo), np.where(exact_zero, 0., hi))

    __rmul__ = __mul__

    def reciprocal(self):
        require(np.all((self.lo > 0) | (self.hi < 0)), "reciprocal excludes zero")
        return I(down(1. / self.hi), up(1. / self.lo))

    def __truediv__(self, other):
        return self * (other if isinstance(other, I) else I.rational(other)).reciprocal()

    def square(self):
        lo = np.minimum(self.lo * self.lo, self.hi * self.hi)
        lo = np.where((self.lo <= 0) & (self.hi >= 0), 0., down(lo))
        hi = up(np.maximum(self.lo * self.lo, self.hi * self.hi))
        zero = (self.lo == 0) & (self.hi == 0)
        return I(np.where(zero, 0., lo), np.where(zero, 0., hi))

    def sqrt(self):
        require(np.all(self.lo >= 0), "nonnegative square-root argument")
        lower, upper = [], []
        for lo, hi in zip(self.lo.flat, self.hi.flat):
            a, b = math.sqrt(float(lo)), math.sqrt(float(hi))
            # Exact dyadic squaring certifies endpoints independently of
            # any correct-rounding claim for the library square root.
            while Q.from_float(a) ** 2 > Q.from_float(float(lo)):
                a = float(down(a))
            while Q.from_float(b) ** 2 < Q.from_float(float(hi)):
                b = float(up(b))
            lower.append(a)
            upper.append(b)
        return I(np.array(lower).reshape(self.lo.shape), np.array(upper).reshape(self.hi.shape))

    def contains(self, value):
        return bool(np.all(self.lo <= value) and np.all(value <= self.hi))


def reduce_sum(value):
    """Any binary reduction tree: gamma_(n-1)*sum(abs(x)) plus underflow.

    No BLAS dot-product or undocumented pairwise-summation accuracy is
    assumed. Basic binary64 operations use rounding to nearest, then one
    nextafter step supplies directed endpoints. The gamma bound permits
    the worst possible depth n-1 of NumPy's finite addition tree.
    """
    n = value.lo.size
    if n == 0:
        return I(0.)
    require((n - 1) * UNIT < 1, "finite gamma_n reduction bound")
    gamma = I.rational((n - 1) * UNIT / (1 - (n - 1) * UNIT)).hi
    require(float(gamma) < 1, "positive denominator in absolute reduction bound")
    def endpoint(array, lower):
        total = np.sum(array, dtype=np.float64)
        absolute = np.sum(np.abs(array), dtype=np.float64)
        absolute_upper = up(up(absolute + up(n * TINY)) / down(1 - gamma))
        error = up(up(gamma * absolute_upper) + up(n * TINY))
        return down(total - error) if lower else up(total + error)
    return I(endpoint(value.lo, True), endpoint(value.hi, False))


def log_rational(value, terms=36):
    """Exact rational atanh series with a proved positive geometric tail."""
    value = Q(value)
    require(value > 0, "positive logarithm endpoint")
    exponent = 0
    while value < 1:
        value *= 2
        exponent -= 1
    while value >= 2:
        value /= 2
        exponent += 1
    def series(x):
        z = (x - 1) / (x + 1)
        require(0 <= z <= Q(1, 3), "atanh range reduction")
        power, total = z, Q(0)
        for j in range(terms):
            total += 2 * power / (2 * j + 1)
            power *= z * z
        remainder = 2 * power / ((2 * terms + 1) * (1 - z * z))
        return total, total + remainder
    low, high = series(value)
    low2, high2 = series(Q(2))
    if exponent >= 0:
        return low + exponent * low2, high + exponent * high2
    return low + exponent * high2, high + exponent * low2


def logarithm(value):
    require(np.all(value.lo > 0), "actual probability has positive lower bound")
    low, _ = log_rational(Q.from_float(float(value.lo)))
    _, high = log_rational(Q.from_float(float(value.hi)))
    return I(rational_bounds(low)[0], rational_bounds(high)[1])


def const_matrix_action(matrix, state):
    shape = state.lo.shape
    lo, hi = np.zeros(shape), np.zeros(shape)
    for row in range(16):
        total = I(np.zeros((shape[0], shape[2])))
        for column in range(16):
            if matrix[row][column]:
                total = total + state[:, column, :] * matrix[row][column]
        lo[:, row, :], hi[:, row, :] = total.lo, total.hi
    return I(lo, hi)


def shifted(state, indices):
    return I(state.lo[indices], state.hi[indices])


def broadcast_site(value):
    return I(value.lo[:, None, None], value.hi[:, None, None])


def fwht(values):
    values = list(values)
    size = 1
    while size < len(values):
        for base in range(0, len(values), 2 * size):
            for offset in range(size):
                a, b = values[base + offset], values[base + size + offset]
                values[base + offset], values[base + size + offset] = a + b, a - b
        size *= 2
    return [value * Q(1, 16) for value in values]


def bounds(value):
    return [float(value.lo), float(value.hi)]


def main():
    require(np.finfo(np.float64).nmant == 52 and np.finfo(np.float64).maxexp == 1024,
            "binary64 arithmetic format")
    require(np.float64(1.) + np.float64(2. ** -53) == np.float64(1.)
            and np.float64(1.) + np.float64(3 * 2. ** -53) == np.float64(1. + 2. ** -51),
            "round-to-nearest ties-to-even runtime canaries")
    require(np.float64(TINY) * np.float64(1.) == TINY
            and np.float64(TINY) + np.float64(TINY) > TINY,
            "subnormal multiplication/addition runtime canaries; no flush to zero")
    root = Path(__file__).resolve().parents[5]
    for path, expected in PINS.items():
        require(hashlib.sha256((root / path).read_bytes()).hexdigest() == expected,
                "pinned source changed: " + path)
    path = root / next(iter(PINS))
    spec = importlib.util.spec_from_file_location("owned_preparation_definitions_only", path)
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    counts = owned.actual_counts(root)
    f = np.array(owned.fourier_numerators(), dtype=np.int64)
    for label in range(32):
        for word in range(16):
            first = (-1) ** (label & (2 * word)).bit_count()
            second = (-1) ** (label & (2 * word + 1)).bit_count()
            expected = 0 if label % 2 else 2 * (-1) ** ((label // 2) & word).bit_count()
            require(first + second == expected,
                    "exact original duplicated-Walsh cancellation and row routing")
    for column in range(16):
        basis_output = fwht([Q(row == column) for row in range(16)])
        require(basis_output == [Q((-1) ** (row & column).bit_count(), 16)
                                 for row in range(16)],
                "exact16 by16 transform basis agrees with literal original Walsh rows")
    sites, right, w = 256, 128, owned.site_index(owned.W)
    indices = np.array(owned.SITES_LIST)
    forward = [np.array([owned.site_index(owned.step(site, r, 1))
                         for site in owned.SITES_LIST]) for r in range(4)]
    backward = [np.array([owned.site_index(owned.step(site, r, -1))
                          for site in owned.SITES_LIST]) for r in range(4)]
    p = (I.rational(5).sqrt() - 1) * Q(1, 2)
    sqrt_p = p.sqrt()
    sigma = p * p * p
    rho_intervals = [I.rational(Q(sites * count, sum(counts))) for count in counts]
    rho = I([float(x.lo) for x in rho_intervals], [float(x.hi) for x in rho_intervals])
    a = sigma * rho.sqrt()
    weight = broadcast_site(a)
    h = Q(1, 4)
    state_lo, state_hi = np.zeros((sites, 16, right + 2)), np.zeros((sites, 16, right + 2))
    clock = sqrt_p * I(f / 128.)
    slack = p * I(f / 128.)
    state_lo[:, 1, :right], state_hi[:, 1, :right] = clock.lo, clock.hi
    state_lo[:, 14, :right], state_hi[:, 14, :right] = slack.lo, slack.hi
    # C_B contracted against the complete RIGHT row f(w)/sqrt128.
    # Integer kernel /128/128 retains all128 original real columns.
    numerator = f @ f[w]
    for site_index, site in enumerate(owned.SITES_LIST):
        entry = I.rational(owned.B(site) * Q(int(numerator[site_index]), 128 ** 2))
        state_lo[site_index, 15, right], state_hi[site_index, 15, right] = entry.lo, entry.hi
    state_lo[w, 15, right + 1] = state_hi[w, 15, right + 1] = 1.
    state = I(state_lo, state_hi)
    creation = owned.ROLE_CREATION
    adjoints = tuple(owned.transpose(c) for c in creation)
    gamma = (Q(1, 2), Q(2), Q(1), Q(1))
    dstate = I(np.zeros_like(state_lo))
    for role in range(4):
        dstate = dstate + weight * const_matrix_action(creation[role], shifted(state, forward[role]))
        dstate = dstate - weight * const_matrix_action(creation[role], state)
        dstate = dstate + shifted(weight * const_matrix_action(adjoints[role], state), backward[role])
        dstate = dstate - weight * const_matrix_action(adjoints[role], state)
    astate = dstate * Q(1, 16)  # A=hD/16; dstate above equals hD state.
    primitives = [[], []]
    minimum_radicand = 1.
    for role in range(4):
        cr, ct = creation[role], adjoints[role]
        radicand = I.rational(1) - a.square() * gamma[role]
        minimum_radicand = min(minimum_radicand, float(np.min(radicand.lo)))
        require(np.min(radicand.lo) > Q(1, 2), "strict actual analytic Julia domain")
        root_delta = radicand.sqrt() - 1
        left_projector = owned.mscale(owned.mmul(cr, ct), 1 / gamma[role])
        right_projector = owned.mscale(owned.mmul(ct, cr), 1 / gamma[role])
        require(owned.mmul(left_projector, left_projector) == left_projector
                and owned.mmul(right_projector, right_projector) == right_projector,
                "exact CAR defect projectors")
        left_root_action = astate + broadcast_site(root_delta) * const_matrix_action(left_projector, astate)
        right_root_action = astate + broadcast_site(root_delta) * const_matrix_action(right_projector, astate)
        shifted_right_action = astate + broadcast_site(shifted(root_delta, backward[role])) * const_matrix_action(right_projector, astate)
        primitives[0].extend((shifted(weight * const_matrix_action(ct, astate), backward[role]),
                              weight * const_matrix_action(cr, shifted(astate, forward[role])),
                              -(weight * const_matrix_action(ct, astate)),
                              -(weight * const_matrix_action(cr, astate))))
        primitives[1].extend((left_root_action, shifted_right_action,
                              -left_root_action, -right_root_action))
    transformed = [fwht(part) for part in primitives]
    del primitives
    q, r = [I(0.) for _ in range(128)], [I(0.) for _ in range(128)]
    for label in range(0, 32, 2):
        for coefficient in range(2):
            n_action = transformed[coefficient][label // 2]
            for port in range(2):
                amplitude = n_action * (-2 * (p * p if port == 0 else p * sqrt_p))
                if label == coefficient == port == 0:
                    amplitude = amplitude + state
                physical_index = 4 * label + 2 * coefficient + port
                q[physical_index] = reduce_sum(amplitude[:, :, :right].square())
                r[physical_index] = 2 * p * reduce_sum(amplitude[:, :, right] * amplitude[:, :, right + 1])
    active = [4 * label + 2 * coefficient + port for label in range(0, 32, 2)
              for coefficient in range(2) for port in range(2)]
    inactive = sorted(set(range(128)) - set(active))
    require(len(active) == len(inactive) == 64 and all(q[i].contains(0) and r[i].contains(0) for i in inactive),
            "exact structural Walsh dark labels retained")
    require(all(float(q[i].lo) > 0 for i in active), "all64 remaining base probabilities certified positive")
    qsum, rsum, cost = I(0.), I(0.), I(0.)
    entropy_natural = I(0.)
    for i in active:
        qsum, rsum = qsum + q[i], rsum + r[i]
        cost = cost + (1 + i % 2) * r[i]
        entropy_natural = entropy_natural - r[i] * logarithm(q[i])
    require(qsum.contains(1) and rsum.contains(0), "complete probability and first-jet normalization enclosures")
    log_phi = -logarithm(p)
    entropy = entropy_natural / log_phi
    net = cost - entropy
    require(float(entropy.hi) < 0 < float(net.lo), "strict full-pointer and known-net coefficient signs")
    port_q, port_r = [I(0.), I(0.)], [I(0.), I(0.)]
    for i in active:
        port_q[i % 2] = port_q[i % 2] + q[i]
        port_r[i % 2] = port_r[i % 2] + r[i]
    port_entropy = I(0.)
    for port in range(2):
        port_entropy = port_entropy - port_r[port] * logarithm(port_q[port]) / log_phi
    label_conditional = entropy - port_entropy
    require(float(port_entropy.hi) < 0 and float(label_conditional.hi) < 0,
            "strict conditional-label source; port entropy cannot replace full pointer entropy")
    rho_w, rho_plus = rho[w], rho[forward[0][w]]
    rayleigh = -(7 * p * sigma * sigma * (rho_w * rho_plus).sqrt()) * Q(1, 2048)
    epsilon = p * p * h * h * Q(1, 64)
    expected_cost = p * epsilon * rayleigh
    require(float(cost.lo) <= float(expected_cost.hi) and float(expected_cost.lo) <= float(cost.hi),
            "known port source equals independently certified Rayleigh coefficient")
    wrong_right_normalization = expected_cost * 128
    require(float(wrong_right_normalization.hi) < float(cost.lo),
            "hostile omitted-RIGHT normalization gives a disjoint port source")
    # Optional fixed-blank DATA compression type gate; no auxiliary
    # physical re-encoding or new word class is inferred from this entry.
    pair = tuple(sorted((owned.W, owned.step(owned.W, 0, 1))))
    entry = owned.column_inner(owned.flat_column(owned.W, 15),
                               owned.flat_column(owned.step(owned.W, 0, 1), 15))
    require(entry == {pair: Q(-8)}, "exact parity type-gate top neighbour entry")
    report = {
        "status": "PASS", "arithmetic": "outward binary64 interval arrays; exact rational sqrt brackets and log tails",
        "carrier": {"L": 4, "CAR": 16, "oldRIGHT": 128, "FR_words": sum(counts),
                    "count_w": counts[w], "count_next_u": counts[forward[0][w]], "sigma": "p^3"},
        "source_scope": "coefficient of the angle derivative at small matter t; D(t)=D0+O(t^2)",
        "normalization": {"sum_q0": bounds(qsum), "sum_r": bounds(rsum),
                          "structural_zero_labels": 64, "certified_positive_labels": 64,
                          "exact_duplicated_Walsh_and_transform_basis_checks": True,
                          "minimum_positive_q0_lower": min(float(q[i].lo) for i in active),
                          "minimum_Julia_radicand_lower": minimum_radicand},
        "linear_coefficients": {"Rayleigh": bounds(rayleigh), "known_port_cost": bounds(cost),
                                "port_cost_from_Rayleigh": bounds(expected_cost),
                                "full_pointer_entropy_phi": bounds(entropy),
                                "port_marginal_entropy_phi": bounds(port_entropy),
                                "conditional_label_entropy_phi": bounds(label_conditional),
                                "known_port_minus_pointer_phi": bounds(net)},
        "full_label_code": "not selected by owner; fixed uniform mu_(b,k)=p^(1+b)/64 would add only constant log_phi64",
        "physical_Book_Info_selected": False,
        "finite_positive_t_or_native_word_bound_certified": False,
        "fixed_blank_DATA_type_gate": "rotated Delta entry (w14,(w+u)15)=sin(theta)*8*a_w*a_next; any fixed-CAR-parity geometric Delta has zero there",
        "no_probability_floor_or_support_deletion": True,
        "interval_assumptions": "IEEE binary64 round-to-nearest without flush-to-zero; format/rounding/subnormal canaries pass; no BLAS reduction, eigensolver or libm logarithm accuracy premise",
        "hostile_controls": ["port-marginal entropy has a strictly different source", "omitting RIGHT128 gives a disjoint port source", "all structural zeros are exact Walsh cancellations rather than a numerical support floor"],
        "source_sha256": PINS,
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
