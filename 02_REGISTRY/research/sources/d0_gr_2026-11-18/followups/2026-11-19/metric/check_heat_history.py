"""Exact growing-clock moments on native words, plus positive-clock truncation bounds."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import factorial
import json


def need(value, name):
    if not value:
        raise ArithmeticError(name)


@dataclass(frozen=True)
class Golden:
    """Integer power basis 1,a,a²,a³ with a=√p and a⁴+a²=1."""
    c: tuple

    def __add__(self, other):
        return Golden(tuple(x + y for x, y in zip(self.c, other.c)))

    def __neg__(self):
        return Golden(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if self == ZERO or other == ZERO:
            return ZERO
        coeff = [0] * 7
        for i, x in enumerate(self.c):
            for j, y in enumerate(other.c):
                coeff[i + j] += x * y
        for degree in (6, 5, 4):
            coeff[degree - 4] += coeff[degree]
            coeff[degree - 2] -= coeff[degree]
        return Golden(tuple(coeff[:4]))

    def __pow__(self, exponent):
        out = ONE
        for _ in range(exponent):
            out = out * self
        return out


def const(n):
    return Golden((n, 0, 0, 0))


ZERO, ONE, A = const(0), const(1), Golden((0, 1, 0, 0))
P = A * A


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def transpose(x):
    return [list(row) for row in zip(*x)]


def mul(x, y):
    return [[sum((a * b for a, b in zip(row, col)), ZERO)
             for col in zip(*y)] for row in x]


def sub(x, y):
    return [[a - b for a, b in zip(rx, ry)] for rx, ry in zip(x, y)]


def scale(s, x):
    return [[s * a for a in row] for row in x]


def trace(x):
    return sum((row[i] for i, row in enumerate(x)), ZERO)


def kron(x, y):
    return [[a * b for a in row_x for b in row_y] for row_x in x for row_y in y]


def zero_matrix(n, m):
    return [[ZERO] * m for _ in range(n)]


def place(x, block, i0, j0):
    for i, row in enumerate(block, i0):
        for j, v in enumerate(row, j0):
            x[i][j] = x[i][j] + v


V = [[A], [P]]
G = [[A, -P], [P, A]]
G0, G1 = kron(G, eye(2)), kron(eye(2), G)
CX = [eye(4)[i] for i in (0, 1, 3, 2)]
J0, J1 = V, kron(eye(2), V)
PASSIVE = [J0, J1, eye(4)]
DIMS = (1, 2, 4, 4)
OFFSETS = (0, 1, 3, 7)
D = sum(DIMS)
N = 425 * D


def fixture(name, g0, g1):
    # Sec. 7fs: passive maps close the complements of successive birth images.
    back = [None, None, None, eye(4)]
    for i in range(2, -1, -1):
        back[i] = mul(back[i + 1], PASSIVE[i])
    detail = [eye(1)] + [sub(eye(n), mul(j, transpose(j)))
                         for n, j in zip(DIMS[1:], PASSIVE)]
    closing = []
    for d, b in zip(detail, back):
        closing.extend(mul(d, transpose(b)))
    need(mul(transpose(closing), closing) == eye(4), "closing isometry")

    time = zero_matrix(D, D)
    cut = zero_matrix(D, D)
    prefix = eye(1)
    place(cut, eye(1), 0, 0)
    for i, op in enumerate((J0, J1, g0)):
        place(time, op, OFFSETS[i + 1], OFFSETS[i])
        prefix = mul(op, prefix)
        place(cut, mul(prefix, transpose(prefix)), OFFSETS[i + 1], OFFSETS[i + 1])
    place(time, mul(closing, g1), 0, OFFSETS[-1])
    need(mul(transpose(time), time) == eye(D), "complete clock orthogonal")
    need(mul(cut, cut) == cut and trace(cut) == const(4), "generated cut")
    leak = mul(sub(eye(D), cut), mul(time, cut))
    feedback = mul(transpose(leak), leak)
    cold = mul(transpose(back[0]), mul(g1, prefix))[0][0]
    f = ONE - cold**2
    need(trace(feedback) == f and mul(feedback, feedback) == scale(f, feedback),
         "actual complete leak has determinant 1-z(1-c²)")
    need(trace(time) == ZERO, "no length-one time loop")
    t2 = trace(mul(time, time))
    need(t2 == const(2) * trace(mul(g0, mul(detail[2], g1))), "two-step return")
    return dict(word=name, cold=cold.c, leak=f.c, trace_T2=t2.c), cold, t2, time


def positive_clock_checks():
    # Exact integer count: given k labelled independent B-bit strings, exactly
    # binom(2**B,k) strictly increasing assignments exist, even for biased bits.
    k = 3
    prefixes = list(product((0, 1), repeat=2))
    sorted_mass, distinct_mass = ZERO, ZERO
    for group in product(prefixes, repeat=k):
        if len(set(group)) < k:
            continue
        n1 = sum(sum(bits) for bits in group)
        weight = P**(2*k + n1)
        distinct_mass = distinct_mass + weight
        if tuple(sorted(group)) == group:
            sorted_mass = sorted_mass + weight
    need(const(factorial(k)) * sorted_mass == distinct_mass and sorted_mass != ZERO,
         "unequal golden atom masses still give factorial by exchangeability")
    for n in range(9):
        coefficient = sum((Fraction(1, factorial(i)*factorial(j)*factorial(h)*
                                    factorial(n-i-j-h))
                           for i in range(n+1) for j in range(n-i+1)
                           for h in range(n-i-j+1)), Fraction())
        need(coefficient == Fraction(4**n, factorial(n)), "four-count series")
    need(P + P**2 == ONE and (P**2 + P**4) + const(2) * P**3 == ONE,
         "geometric/sorting origins")
    # p<0.619 by x²+x−1>0 there. ρ=1−2p³<0.53 from p>0.618.
    lo, hi = Fraction(618, 1000), Fraction(619, 1000)
    need(lo**2 + lo < 1 < hi**2 + hi and 1-2*lo**3 < Fraction(53, 100),
         "certified rational tail envelopes")
    L, t, R = 40, 80, 3
    bound = 4 * hi**(2*L) + 4 * hi**2 * Fraction(53, 100)**t + Fraction(1, 2**(20*R))
    need(bound < Fraction(1, 10**15), "finite cutoff error below 10^-15")
    u, pair_cap = 80, 128
    finite = bound + 2 * Fraction(1, 2**u) + (20*R+2*u)*Fraction(53, 100)**pair_cap
    need(finite < Fraction(1, 10**15), "all classical fair bits and comparisons finitely capped")
    return dict(k_sort_test=k, exact_sorted_mass_power_basis=sorted_mass.c,
                L=L, stream_prefix_bits=t, return_cap=R,
                upper_bound_rational=str(bound), certified_less_than="1e-15",
                classical_threshold_bits=u, raw_pairs_per_fair_bit=pair_cap,
                classical_all_caps_upper_bound=str(finite),
                statistical_scope="absolute event error; full capped classical comparison of algebraic marks is included")


def scene_moment_coefficients(order):
    """Return Tr_scene (B_s+x C_s)^n, scaled by 3432^n, as polynomials."""
    sizes = (9, 11, 13)
    lcm = 3432
    c = [lcm//(35-n) for n in sizes]
    power = [[[(i==j)] for j in range(3)] for i in range(3)]
    coefficients = []
    for n in range(order+1):
        traced = [sum(power[i][i][j] for i in range(3)) for j in range(n+1)]
        traced[n] += sum((m-1)*factor**n for m, factor in zip(sizes, c))
        coefficients.append(traced)
        nxt = [[[0]*(n+2) for j in range(3)] for i in range(3)]
        for i, j, k in product(range(3), repeat=3):
            for d, value in enumerate(power[i][j]):
                if j == k:
                    nxt[i][k][d+1] += value*c[k]
                else:
                    nxt[i][k][d] += value*sizes[k]*c[k]
        power = nxt
    return coefficients, lcm


def algebraic_bounds(z):
    # Positive unique root of a^4+a^2−1. Enclose the linear combination term by term.
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(192):
        mid = (lo+hi)/2
        if mid**4 + mid**2 < 1:
            lo = mid
        else:
            hi = mid
    low, high = 0, 0
    for deg, coeff in enumerate(z.c):
        ends = (coeff*lo**deg, coeff*hi**deg)
        low += min(ends)
        high += max(ends)
    return low, high


def scaled_heat_bounds(time, coefficients, lcm):
    # This is e^beta Z_H, hence its same-budget ratio is exactly Z_H,+ / Z_H,-.
    x = [[a+b for a,b in zip(rx, ry)] for rx, ry in zip(time, transpose(time))]
    moments = []
    mat = eye(D)
    total = ZERO
    beta = const(2) * P**2
    for degree, coeff in enumerate(coefficients):
        moments.append(trace(mat))
        moment = sum((const(c)*t for c,t in zip(coeff, moments)), ZERO)
        full = const(359*D) + const(Fraction(2, lcm**degree))*moment
        total = total + const(Fraction(1,factorial(degree))) * beta**degree * full
        mat = mul(mat, x)
    lo, hi = algebraic_bounds(total)
    # ||I−Delta||≤1, beta<1 and exp(beta)<3. All zero modes are counted.
    error = Fraction(3*N, factorial(len(coefficients)))
    return lo-error, hi+error


def decimal_enclosure(interval, places=18):
    scale10 = 10**places
    a,b = interval
    m = (a*scale10).__floor__()
    n = (b*scale10).__ceil__()
    def fixed(k):
        return f"{k//scale10}.{k%scale10:0{places}d}"
    return [fixed(m), fixed(n)]


def positive_ratio_interval(t1, t2, c1, c2):
    order = 19
    coeff, lcm = scene_moment_coefficients(order)
    h1, h2 = (scaled_heat_bounds(time, coeff, lcm) for time in (t1,t2))
    z = const(Fraction(1, 2**20))
    den1, den2 = (algebraic_bounds(ONE-z*(ONE-c**2)) for c in (c1,c2))
    heat = (h1[0]/h2[1], h1[1]/h2[0])
    full = (heat[0]*den2[0]/den1[1], heat[1]*den2[1]/den1[0])
    need(0 < full[0] <= full[1] < 1 and 0 < heat[0] <= heat[1] < 1,
         "strict exact sign of both matched ratios")
    return dict(order=order, scaled_heat_absolute_taylor_error=str(Fraction(3*N,factorial(order+1))),
                heat_ratio=decimal_enclosure(heat), original_partition_ratio=decimal_enclosure(full))


def main():
    rows = []
    for name, g0, g1 in (("G0;G1", G0, G1), ("CX01;CX01", CX, CX),
                         ("G1;CX01", G1, CX), ("CX01;G1", CX, G1)):
        rows.append(fixture(name, g0, g1))
    (_, c_gg, t_gg, _), (_, c_cc, t_cc, _), (_, c_plus, t_plus, t1), (_, c_minus, t_minus, t2) = rows
    need(c_gg == P and c_cc == ONE, "old comparator true cuts")
    need(t_gg - t_cc == const(4)*(P-ONE), "old certified spectral contrast")
    centre = A * P + const(2) * P**4
    need(c_plus == centre + P**6 and c_minus == centre - P**6, "matched true cuts")
    need(t_plus - t_minus == -const(4) * P**4, "matched spectral contrast")
    scene_factor = sum((Fraction(n, (33-n+2)**2) for n in (9, 11, 13)), Fraction())
    need(scene_factor > 0, "all 33 scene vertices retained")
    return dict(schema="d0.heat-history-comparator/1", status="PASS",
                power_basis="1,a,a²,a³; a=√p; a⁴=1−a²", D=D, grades=(33*D,392*D),
                total_modes=N, fixtures=[r[0] for r in rows],
                tr_Cs_squared=str(scene_factor),
                matched_delta_full_second_moment_over_tr_Cs_squared=(-const(16)*P**4).c,
                matched_ratio=positive_ratio_interval(t1,t2,c_plus,c_minus),
                positive_clock=positive_clock_checks(),
                scope="same genuine finite words and spectral partition; a cost/Info identification and native heat measurement are additional inputs")


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
