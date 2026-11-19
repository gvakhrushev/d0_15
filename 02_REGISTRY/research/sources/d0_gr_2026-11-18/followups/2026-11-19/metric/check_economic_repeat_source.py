"""Exact positive economic-mixture source and native LIVE repetition checks.

This consumes the published LIVE_PARSER probabilities/lengths; it does not
re-run its circuit or assert that one candidate Cost-Info is selected by D0.
General derivatives use rational arithmetic.  Native branch arithmetic is
in Q(p), p**2=1-p. Decimal numbers illustrate the analytic theorem.
No scientific check relies on Python assertions; -O has the same result.
"""
from decimal import Decimal, getcontext
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
getcontext().prec = 90


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


class Golden:
    """Exact a+b*p, with p positive root of p*p+p-1=0."""
    def __init__(self, a=0, b=0):
        if isinstance(a, Golden):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = F(a), F(b)

    def __add__(self, other):
        other = Golden(other)
        return Golden(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Golden(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-Golden(other))

    def __rsub__(self, other):
        return Golden(other) - self

    def __mul__(self, other):
        other = Golden(other)
        return Golden(self.a * other.a + self.b * other.b,
                      self.a * other.b + self.b * other.a - self.b * other.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a * self.a - self.a * self.b - self.b * self.b
        need(norm != 0, 'nonzero golden inverse')
        return Golden((self.a - self.b) / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * Golden(other).inverse()

    def __rtruediv__(self, other):
        return Golden(other) / self

    def __pow__(self, n):
        need(isinstance(n, int), 'integer golden power')
        if n < 0:
            return self.inverse() ** (-n)
        out, base = Golden(1), self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n //= 2
        return out

    def __eq__(self, other):
        other = Golden(other)
        return self.a == other.a and self.b == other.b


def exact_full_source():
    # Four true old leaves; continuations differ within BOTH T sectors.
    weights = [F(2), F(3), F(5), F(7)]
    tails = [F(1, 2), F(7, 3), F(2, 5), F(11, 7)]
    tags = [0, 0, 1, 1]
    directions = []
    for i in range(8):
        d = [F(0)] * 8
        d[i] = F(1)
        directions.append(d)
    directions.append([F(2, 3), F(-3, 5), F(7, 11), F(-1, 2),
                       F(3, 7), F(-5, 13), F(2, 9), F(-7, 17)])
    hidden_within_sector_nonzero = False
    for d in directions:
        dw, dh = d[:4], d[4:]
        old = sum(weights)
        dold = sum(dw)
        mass, dmass, factor, dfactor = [], [], [], []
        for t in (0, 1):
            ids = [i for i in range(4) if tags[i] == t]
            m = sum(weights[i] for i in ids)
            dm = sum(dw[i] for i in ids)
            n = sum(weights[i] * tails[i] for i in ids)
            dn = sum(dw[i] * tails[i] + weights[i] * dh[i] for i in ids)
            mass.append(m)
            dmass.append(dm)
            factor.append(n / m)
            dfactor.append((dn * m - n * dm) / (m * m))
        nu = mass[1] / old
        dnu = (dmass[1] * old - mass[1] * dold) / (old * old)
        a, b = factor
        da, db = dfactor
        mix = (1 - nu) * a + nu * b
        post = nu * b / mix
        z = sum(weights[i] * tails[i] for i in range(4))
        dz = sum(dw[i] * tails[i] + weights[i] * dh[i] for i in range(4))
        need(z == old * mix, 'exact complete two-sector factorization')
        direct = -dz / z  # ell * D A_N
        formula = -dold / old + (a - b) * dnu / mix
        formula -= (1 - post) * da / a + post * db / b
        need(direct == formula, 'all old and conditional source rows ER3')
        if any(dw) and not any(dh) and (da or db):
            hidden_within_sector_nonzero = True
    need(hidden_within_sector_nonzero, 'old conditional correlations retained')
    return len(directions)


def exact_gain_bounds():
    count = 0
    for nu in (F(1, 100), F(1, 3), F(1, 2), F(7, 8), F(99, 100)):
        for ratio in (F(1, 10**60), F(1, 100), F(2, 3), F(1),
                      F(3, 2), F(100), F(10**60)):
            # a=1, b=ratio, ell*s is exact and rational.
            g = (1 - ratio) / (1 - nu + nu * ratio)
            need(-1 / nu < g < 1 / (1 - nu), 'strict sharp oriented bounds')
            need(abs(g) < 1 / min(nu, 1 - nu), 'two-sided collar bound')
            count += 1
    return count


def native_live_paths():
    p = Golden(0, 1)
    need(p + p**2 == 1, 'native golden law')
    tested = 0
    for n in range(1, 9):
        for t in (0, 1):
            born_sum, expected_factor, count_factor = Golden(), Golden(), Golden()
            mean_length = Golden()
            for error_path in product((0, 1), repeat=n):
                e = sum(error_path)
                probability = p ** (n + e)
                length = 5 * n + n * t + e
                scalar_factor = (p ** length) / probability
                need(scalar_factor == p ** (n * (4 + t)),
                     'actual canonical path net is N(4+T)')
                born_sum += probability
                mean_length += probability * length
                expected_factor += probability * scalar_factor
                count_factor += scalar_factor
                tested += 1
            need(born_sum == 1, 'all canonical errors retained')
            need(mean_length - n * (1 + p**2) == n * (4 + t),
                 'mean printed length minus full conditional entropy')
            need(expected_factor == p ** (n * (4 + t)),
                 'Born-expectation conditional factor')
            need(count_factor == (2**n) * expected_factor,
                 'counting partition has its actual multiplicity')
    for xi in (Golden(F(3, 8)), p**2, Golden(F(2, 5))):
        z0 = p**5 / (1 - xi) + p**6 / xi
        z1 = p**7 / xi + p**6 / (1 - xi)
        need(z1 == p * z0, 'complete LIVE conditional ratio at moving noise')
    xi = p**2
    z0 = p**5 / (1 - xi) + p**6 / xi
    dz0 = p**5 / (1 - xi)**2 - p**6 / xi**2
    need(-dz0 / z0 == F(1, 2), 'independent literal noise source ell*dA=N/2')
    return tested


def fresh_vs_shared_exact():
    nu, a, b = F(1, 3), F(3, 4), F(1, 4)
    single = (1 - nu) * a + nu * b
    checks = 0
    for n in range(2, 9):
        fresh = single ** n
        shared = (1 - nu) * a ** n + nu * b ** n
        need(fresh != shared, 'fresh full queries differ from shared-T rereads')
        independent_gradient = (a - b) / single
        shared_gradient = (a**n - b**n) / shared
        need(shared_gradient < 1 / (1 - nu), 'shared source saturates')
        # Differentiate all N actual factors, not a conditional repeated bit.
        product_derivative = sum((b - a) * single**(n - 1) for _ in range(n))
        need(-product_derivative / fresh == n * independent_gradient,
             'exact full product derivative')
        checks += 1
    return checks


def decimal_examples():
    p = (Decimal(5).sqrt() - 1) / 2
    ell = (1 / p).ln()
    nu = Decimal(1) / 2
    rows = []
    previous = Decimal(0)
    for n in (1, 2, 4, 8, 16, 64, 256):
        ratio = p ** n
        gain = (1 - ratio) / (ell * (1 - nu + nu * ratio))
        need(previous < gain < 2 / ell, 'native positive gain increases to finite limit')
        previous = gain
        rows.append({'N': n, 'shared_marker_gain': format(gain, '.18f'),
                     'mean_code_cq_gain': n})
    need(abs(previous - 2 / ell) < Decimal('1e-50'), 'native gain saturation')
    # Hostile control: discarding the fixed old collar can make the gain grow.
    rare = []
    for n in (8, 16, 32):
        ratio = p ** n
        nu_rare = 1 - ratio**2
        gain = (1 - ratio) / (ell * (1 - nu_rare + nu_rare * ratio))
        need(gain > 2 / ell, 'no bound from a silently discarded fixed collar')
        need(gain < 1 / (ell * (1 - nu_rare)), 'rare-sector true oriented bound')
        rare.append({'N': n, 'nu': format(nu_rare, '.30f'),
                     'gain': format(gain, '.18f')})
    # Native finite endpoint comparison; positivity covers the whole segment.
    low, high = p**2, Decimal(1) / 2
    n = 16
    ratio = p ** n
    action_difference = -((1 - high + high * ratio) /
                         (1 - low + low * ratio)).ln() / ell
    upper = (high - low) * 2 / ell
    need(0 < action_difference < upper, 'native two-end full-log source bound')
    return {
        'at_economic_nu_half': rows,
        'limit_gain_at_nu_half': format(2 / ell, '.18f'),
        'literal_noise_source_per_copy': format(1 / (2 * ell), '.18f'),
        'rare_collar_controls': rare,
        'native_endpoint_N16_action_difference': format(action_difference, '.18f'),
        'native_endpoint_N16_bound': format(upper, '.18f'),
    }


def main():
    receipt = json.loads((HERE / 'live_parser_result.json').read_text())
    need(receipt['status'] == 'PASS', 'existing literal parser receipt')
    need(receipt['births'] == 6 and receipt['primitive_square_calls'] == 28
         and receipt['raw_stages'] == 34, 'existing actual 34-stage word')
    inputs = ['LIVE_PARSER_RU.md', 'check_live_parser.py', 'live_parser_result.json',
              'GUARDED_NOISE_RU.md', 'COMPLETE_WORK_SOURCE_RU.md',
              'SAME_HISTORY_BINDING_RU.md']
    result = {
        'status': 'PASS',
        'scope': 'positive complete economic mixtures; no selected physical Cost-Info asserted',
        'input_sha256': {name: sha256((HERE / name).read_bytes()).hexdigest()
                         for name in inputs},
        'exact_full_source_directions': exact_full_source(),
        'exact_positive_gain_bound_cases': exact_gain_bounds(),
        'native_complete_noise_paths_checked': native_live_paths(),
        'fresh_vs_shared_checks': fresh_vs_shared_exact(),
        'native_stages_per_live': receipt['raw_stages'],
        'decimal_diagnostics': decimal_examples(),
        'native_cost_info_selection_proved': False,
        'GR_closed': False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
