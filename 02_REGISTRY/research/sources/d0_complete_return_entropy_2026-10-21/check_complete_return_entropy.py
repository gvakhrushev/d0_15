#!/usr/bin/env python3
"""New complete-return entropy/source certificate; Python standard library only.

The analytic tail proof is in PROOF.md. The infinite native source sign is
certified by outward Decimal interval arithmetic plus an exact Fraction tail.
The independent noncommuting matrix/finite-difference check is numerical only.
No old gate, all128, geometry or Lean suite is invoked; no receipts are rewritten.
"""
from decimal import Decimal as D, getcontext, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import sys

getcontext().prec = 180


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


class Interval:
    def __init__(self, low, high=None):
        self.lo = D(low)
        self.hi = D(low if high is None else high)
        require(self.lo <= self.hi, "interval ordering")

    def __add__(self, other):
        other = interval(other)
        return Interval((self.lo + other.lo).next_minus(),
                        (self.hi + other.hi).next_plus())

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -interval(other)

    def __rsub__(self, other):
        return interval(other) + -self

    def __mul__(self, other):
        other = interval(other)
        products = [self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi]
        return Interval(min(products).next_minus(), max(products).next_plus())

    __rmul__ = __mul__

    def inverse(self):
        require(self.lo * self.hi > 0, "inverse interval excludes zero")
        return Interval((D(1) / self.hi).next_minus(),
                        (D(1) / self.lo).next_plus())

    def __truediv__(self, other):
        return self * interval(other).inverse()

    def __rtruediv__(self, other):
        return interval(other) * self.inverse()

    def square(self):
        if self.lo <= 0 <= self.hi:
            return Interval(0, max(self.lo * self.lo, self.hi * self.hi).next_plus())
        squares = [self.lo * self.lo, self.hi * self.hi]
        return Interval(min(squares).next_minus(), max(squares).next_plus())

    def sqrt(self):
        require(self.lo >= 0, "square root domain")
        # Decimal sqrt/ln are correctly rounded. Enlarge by one adjacent
        # representable value to obtain directed enclosures.
        return Interval(max(D(0), self.lo.sqrt().next_minus()),
                        self.hi.sqrt().next_plus())

    def log(self):
        require(self.lo > 0, "logarithm domain")
        return Interval(self.lo.ln().next_minus(), self.hi.ln().next_plus())


def interval(value):
    return value if isinstance(value, Interval) else Interval(value)


def fraction_interval(value):
    return Interval(value.numerator) / Interval(value.denominator)


def endpoints(value, digits=45):
    # Render a shorter interval with outward rounding as well. Assertions use
    # the full 180-digit enclosure, never these presentation endpoints.
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_FLOOR
        low = +value.lo
        context.rounding = ROUND_CEILING
        high = +value.hi
    return [str(low), str(high)]


def tails(n):
    r = F(31, 32)
    rr = r * r
    t0 = rr ** (n + 1) / (1 - rr)
    t1 = rr ** (n + 1) * (F(n + 1) / (1 - rr) + rr / (1 - rr) ** 2)
    t2 = rr ** (n + 1) * (F((n + 1) ** 2) / (1 - rr)
                          + 2 * (n + 1) * rr / (1 - rr) ** 2
                          + rr * (1 + rr) / (1 - rr) ** 3)
    return t0, t1, t2


def native_interval_certificate():
    n_cap = 320
    r = F(31, 32)
    rr = r * r
    const = F(7, 6)
    velocity = F(16, 15)
    require(r ** 8 > F(3, 4), "power-majorant rational inequality")
    require(const * r ** 3 > 1, "remainder-class rational inequality")
    require(const * r ** 5 < 1, "amplitude logarithm regime n>=6")
    require(const ** 2 * rr ** 16 < F(1, 2), "coherent large-eigenvalue regime")
    require(velocity ** 2 > F(16, 15), "native derivative norm budget")

    root5 = Interval(5).sqrt()
    c = root5 - 2
    logphi = ((root5 + 1) / 2).log()
    require(D('0.23') < c.lo < c.hi < D('0.25'), "native point in c chart")
    require(logphi.lo > D(2) / 5, "Golden log lower bound")
    logr = fraction_interval(r).log()
    require((-logr).hi < D(1) / 31, "r logarithm upper bound")

    amplitudes = [Interval(0), c, Interval(0), c * c * c - c,
                  (1 - c * c).square()]
    jets = [Interval(0), Interval(1), Interval(0), 3 * c * c - 1,
            -4 * c * (1 - c * c)]
    for n in range(5, n_cap + 1):
        amplitudes.append(c * amplitudes[n - 1] + c * c * amplitudes[n - 2]
                          - c * amplitudes[n - 3])
        jets.append(amplitudes[n - 1] + c * jets[n - 1]
                    + 2 * c * amplitudes[n - 2] + c * c * jets[n - 2]
                    - amplitudes[n - 3] - c * jets[n - 3])

    entropy = Interval(0)
    source = Interval(0)
    mass = Interval(0)
    mass_source = Interval(0)
    mean = Interval(0)
    mean_source = Interval(0)
    for n in range(1, n_cap + 1):
        if n == 2:
            # a_2(c)=0 identically; its entropy and first source are exactly 0.
            continue
        probability = amplitudes[n].square()
        probability_source = 2 * amplitudes[n] * jets[n]
        require(probability.lo > 0, "resolved interval does not straddle dark branch")
        entropy -= probability * probability.log() / logphi
        source -= probability_source * (probability.log() + 1) / logphi
        mass += probability
        mass_source += probability_source
        mean += n * probability
        mean_source += n * probability_source

    survival = 1 - mass
    survival_source = -mass_source
    require(0 < survival.lo < survival.hi < D('0.5'), "actual cap unresolved mass")
    cap_entropy = entropy - survival * survival.log() / logphi
    cap_source = source - survival_source * (survival.log() + 1) / logphi
    cap_mean = mean + n_cap * survival
    cap_mean_source = mean_source + n_cap * survival_source

    t0, t1, t2 = tails(n_cap)
    omitted_source = 10 * const ** 3 * velocity * r ** -3 * (t1 + t2 / 31)
    abort_source = (10 * const ** 3 * velocity * r ** -1
                    * (n_cap + F(n_cap * n_cap, 31)) * rr ** n_cap)
    cap_error = omitted_source + abort_source
    omitted_value = F(5, 2) * const ** 2 * r ** -2 * (t0 + F(2, 31) * t1)
    e = fraction_interval(omitted_source)
    ec = fraction_interval(cap_error)
    ev = fraction_interval(omitted_value)
    infinite_source = Interval((source.lo - e.hi).next_minus(),
                               (source.hi + e.hi).next_plus())
    from_cap = Interval((cap_source.lo - ec.hi).next_minus(),
                        (cap_source.hi + ec.hi).next_plus())
    infinite_value = Interval(cap_entropy.lo,
                              (cap_entropy.hi + ev.hi).next_plus())
    require(infinite_source.lo > D('10.61') and infinite_source.hi < D('10.62'),
            "infinite source strict interval 10.61..10.62")
    require(from_cap.lo > D('10.61') and from_cap.hi < D('10.62'),
            "complete cap source strict interval 10.61..10.62")
    require(source.hi - source.lo < D('1e-150'), "interval arithmetic width")
    require(infinite_value.lo > D('1.79') and infinite_value.hi < D('1.80'),
            "infinite entropy value enclosure")

    return {
        'native_parameter': 'sqrt(5)-2',
        'cap': n_cap,
        'decimal_precision': getcontext().prec,
        'finite_resolved_entropy': endpoints(entropy),
        'finite_resolved_source': endpoints(source),
        'finite_source_arithmetic_width': str(source.hi - source.lo),
        'unresolved_mass': [str(survival.lo), str(survival.hi)],
        'complete_cap_entropy': endpoints(cap_entropy),
        'complete_cap_source': endpoints(cap_source),
        'complete_cap_mean_cycles': endpoints(cap_mean),
        'complete_cap_mean_cycles_source': endpoints(cap_mean_source),
        'infinite_source_interval': endpoints(infinite_source),
        'infinite_source_from_complete_cap': endpoints(from_cap),
        'infinite_entropy_interval': endpoints(infinite_value),
        'omitted_source_rational_bound': str(omitted_source),
        'omitted_source_bound_float': float(omitted_source),
        'complete_cap_source_bound_float': float(cap_error),
        'infinite_source_sign': '10.61 < H_phi_prime(sqrt(5)-2) < 10.62',
        'physical_gate_variation_admitted': False,
    }


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(4))
             for j in range(4)] for i in range(4)]


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def vecadd(left, right):
    return [x + y for x, y in zip(left, right)]


def matrix_entropy_jet(matrix, jet, n_cap):
    v = [1., 0., 0., 0.]
    dv = [0.] * 4
    blank = [list(row) for row in matrix]
    blank_jet = [list(row) for row in jet]
    blank[0] = [0.] * 4
    blank_jet[0] = [0.] * 4
    entropy = source = mean = mean_source = 0.
    logphi = math.log((1 + math.sqrt(5)) / 2)
    for n in range(1, n_cap + 1):
        amplitude = matvec(matrix, v)[0]
        amplitude_jet = vecadd(matvec(jet, v), matvec(matrix, dv))[0]
        probability = amplitude * amplitude
        probability_jet = 2 * amplitude * amplitude_jet
        if probability:
            entropy -= probability * math.log(probability) / logphi
            source -= probability_jet * (math.log(probability) + 1) / logphi
        mean += n * probability
        mean_source += n * probability_jet
        dv, v = vecadd(matvec(blank_jet, v), matvec(blank, dv)), matvec(blank, v)
    survival = sum(x * x for x in v)
    survival_jet = 2 * sum(x * y for x, y in zip(v, dv))
    if survival:
        entropy -= survival * math.log(survival) / logphi
        source -= survival_jet * (math.log(survival) + 1) / logphi
    return (entropy, source, mean + n_cap * survival,
            mean_source + n_cap * survival_jet)


def noncommuting_control():
    c = math.sqrt(5) - 2
    k = math.sqrt(1 - c * c)
    matrix = [[c, 0., -k, 0.], [0., c, 0., -k],
              [0., -k, 0., -c], [-k, 0., -c, 0.]]
    generator = [[0.] * 4 for _ in range(4)]
    generator[0][1] = 1.
    generator[1][0] = -1.
    left = matmul(generator, matrix)
    right = matmul(matrix, generator)
    commutator_max = max(abs(left[i][j] - right[i][j])
                         for i in range(4) for j in range(4))
    require(commutator_max > .1, "independent control is noncommuting")
    zero_jet = [[0.] * 4 for _ in range(4)]

    def perturbed(t):
        rotation = [[float(i == j) for j in range(4)] for i in range(4)]
        rotation[0][0] = rotation[1][1] = math.cos(t)
        rotation[0][1] = math.sin(t)
        rotation[1][0] = -math.sin(t)
        return matmul(rotation, matrix)

    exact_jet = matrix_entropy_jet(matrix, left, 80)
    step = 1e-5
    plus = matrix_entropy_jet(perturbed(step), zero_jet, 80)
    minus = matrix_entropy_jet(perturbed(-step), zero_jet, 80)
    finite_difference = (plus[0] - minus[0]) / (2 * step)
    discrepancy = abs(finite_difference - exact_jet[1])
    require(discrepancy < 2e-6, "noncommuting complete-cap entropy derivative")
    require(abs(exact_jet[2] - 4) < 1e-12, "constant mean return control")
    require(abs(exact_jet[3]) < 1e-12, "zero mean-clock source control")
    require(abs(exact_jet[1]) > .5, "nonzero full entropy source control")
    return {'cap': 80, 'commutator_max_entry': commutator_max,
            'complete_entropy_source': exact_jet[1],
            'centered_finite_difference': finite_difference,
            'discrepancy': discrepancy, 'mean_cycles': exact_jet[2],
            'mean_cycles_source': exact_jet[3],
            'physical_gate_variation_admitted': False,
            'status': 'floating control; not the interval sign certificate'}


def verify_pins(repository_root):
    pins_path = Path(__file__).with_name('SOURCE_PINS.json')
    pins = json.loads(pins_path.read_text())
    for entry in pins['inputs']:
        path = repository_root / entry['path']
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == entry['sha256'], 'immutable source changed: ' + entry['path'])
    return {'input_commit': pins['input_commit'], 'verified_inputs': len(pins['inputs'])}


def main():
    output = {'status': 'PASS_COMPLETE_RETURN_ENTROPY_C1',
              'native_interval': native_interval_certificate(),
              'noncommuting_control': noncommuting_control(),
              'uniform_neighborhood': 'U(4), fixed P=jj*, ||V^4||^2<=3/4',
              'probability_floor_required': False,
              'uniform_C2_claimed': False,
              'full_D0_price_selected': False, 'GR_closed': False}
    if len(sys.argv) == 2:
        output['source_pins'] = verify_pins(Path(sys.argv[1]))
    elif len(sys.argv) > 2:
        raise RuntimeError('usage: check_complete_return_entropy.py [repository_root]')
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
