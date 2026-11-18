"""Diagonal H.1 tariff certificate. Python 3 standard library, deterministic JSON."""
from fractions import Fraction as Q
from math import comb, factorial, isqrt
import json


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def leaf_derivative(m, ones, t):
    """Derivative of the probability of a single ordered word of Hamming weight ones."""
    return t**ones * (1-t)**(m-ones) * (ones/t - (m-ones)/(1-t))


def ordered_charge(word):
    index = int(word, 2)
    # Intentionally depends on addresses and interactions, not just Hamming weight.
    return 7 + (31*index*index + 17*index + 23) % 101


def tariff_check(m):
    step = Q(1, 100)
    nodes = [Q(2, 5) + k*step for k in range(m+1)]
    upper = nodes[-1]
    differences = [(-1)**(m-k) * comb(m, k) for k in range(m+1)]
    require(sum(differences) == 0, "annihilate constant and parsed slope")
    require(Q(2, 5)**2 - 3*Q(2, 5) + 1 < 0 and upper < Q(1, 2), "golden collar")

    matrix = [[leaf_derivative(m, bin(index).count("1"), t)
               for index in range(2**m)] for t in nodes]
    for index in range(2**m):
        require(sum(c*row[index] for c, row in zip(differences, matrix)) == 0,
                "ordered basis tariff was not annihilated")
    words = [format(i, "0{}b".format(m)) for i in range(2**m)]
    charges = [ordered_charge(word) for word in words]
    if m >= 2:
        require(charges[1] != charges[2], "need unequal charges for 01 and 10")
    slopes = [sum(a*b for a, b in zip(charges, row)) for row in matrix]
    require(sum(c*d for c, d in zip(differences, slopes)) == 0, "addressed table contrast")

    # The actual entropy contrast times ell is -m*log(odds_product).
    # Taking integer powers of rational odds gives its sign exactly.
    odds_product = Q(1)
    for t, c in zip(nodes, differences):
        odds_product *= ((1-t)/t)**c
    sign = (odds_product < 1) - (odds_product > 1)
    require(sign == (-1)**(m+1), "contrast orientation")
    ratio = max(odds_product, 1 / odds_product)
    log_modulus_lower = 2*m*(ratio-1)/(ratio+1)  # log(x) >= 2(x-1)/(x+1)
    gap_times_ell = (Q(factorial(m), 2**m) * step**m *
                     (upper**(-m) - (1-upper)**(-m)))
    require(log_modulus_lower > 2**m * gap_times_ell > 0, "uniform lower gap")
    return {"M": m, "basis_tables": len(words), "nodes": [str(t) for t in nodes],
            "entropy_difference_sign": sign, "ell_times_max_abs_slope_lower": str(gap_times_ell)}


def combine(values, weights):
    return tuple(sum(w*v[i] for w, v in zip(weights, values)) for i in range(3))


def second_order_contact():
    # Vectors represent coefficients of (1, ell, L_s), where L_s=log((1-s)/s).
    s = Q(33, 80)
    variance = s*(1-s)
    costs, first, second = [], [], []
    for x, y in ((0, 0), (0, 1), (1, 0), (1, 1)):
        z = Q(x+y, 2) - s
        costs.append((12 + (x-y) - (x-s)*(y-s)/variance, -2*z, 2*z))
        n = x+y
        first.append(leaf_derivative(2, n, s))
        second.append(2 if x == y else -2)
    # 0 < ell, L_s < 1, so even the negative coefficients at unit value
    # certify that all four fixed monetary amounts ell*T_xy are positive.
    require(all(c+min(e, 0)+min(l, 0) > 0 for c, e, l in costs), "positive tariffs")
    require(costs[1] != costs[2], "distinct ordered charges")
    d_cost = combine(costs, first)
    dd_cost = combine(costs, second)
    require(d_cost == (0, -2, 2), "cancel two parsed/entropy slopes")
    require(dd_cost == (-2/variance, 0, 0), "cancel two entropy curvatures")
    third = -2*(1-2*s)/variance**2  # ell*S'''(s); the quadratic tariff has zero third jet.
    require(third < 0, "nonzero third derivative")
    return {"q_contact": str(s), "basis_for_ell_times_tariffs": ["1", "log(phi)", "log((1-q_contact)/q_contact)"],
            "ell_times_T_00_01_10_11": [[str(k) for k in v] for v in costs],
            "S_prime": 0, "S_double_prime": 0, "ell_times_S_triple_prime": str(third),
            "costs": "fixed positive real tariffs; coefficients use the stated reference calibration"}


# Closed intervals on a fixed rational mesh for the literal pointer rotations.
GRID = 10**80


def point(q):
    q = Q(q)*GRID
    return q.__floor__(), q.__ceil__()


def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def sub(x, y):
    return x[0]-y[1], x[1]-y[0]


def mul(x, y):
    values = [a*b for a in x for b in y]
    return min(values)//GRID, -((-max(values))//GRID)


def sqrt_interval(x):
    require(x[0] >= 0, "sqrt domain")
    return isqrt(x[0]*GRID), isqrt(x[1]*GRID)+1


def power(x, n):
    answer = point(1)
    for _ in range(n):
        answer = mul(answer, x)
    return answer


def cmul(x, y):
    return sub(mul(x[0], y[0]), mul(x[1], y[1])), add(mul(x[0], y[1]), mul(x[1], y[0]))


def outward_decimal(x, places=9):
    unit = GRID//10**places
    def render(n):
        whole, frac = divmod(n, 10**places)
        return "{}.{:0{}d}".format(whole, frac, places)
    return [render(x[0]//unit), render(-((-x[1])//unit))]


def native_probability_settings():
    one, two, half = point(1), point(2), point(Q(1, 2))
    p = mul(half, sub(sqrt_interval(point(5)), one))
    a = sqrt_interval(p)
    p2 = power(p, 2)
    c512 = power(p, 3)  # cos(2 theta_G)=p^3
    for _ in range(9):
        c512 = sub(mul(two, mul(c512, c512)), one)
    q0 = add(p2, mul(mul(two, power(p, 10)), sub(one, c512)))
    g2 = cmul((a, p), (a, p))
    g4 = cmul(g2, g2)
    cs = (one, point(0))
    selected = (0, 26, 33, 59, 66, 92, 99)
    enclosures, settings = [], []
    for n in range(max(selected)+1):
        if n in selected:
            c, sn = cs
            q = add(half, add(mul(sub(q0, half), c), mul(mul(a, p), sn)))
            require(p2[1] < q[0] <= q[1] < half[0], "native point in open collar")
            require(c[0] > point(Q(98, 100))[1], "nonzero geometric Jacobian")
            enclosures.append(q)
            settings.append({"n": n, "q": outward_decimal(q), "Dq_multiplier": outward_decimal(c)})
        cs = cmul(cs, g4)
    ordered = sorted(enclosures)
    require(all(x[1] < y[0] for x, y in zip(ordered, ordered[1:])), "distinct native points")
    return {"base_q": outward_decimal(q0), "settings": settings, "width_N": 99,
            "rotation": "G^(N+n) Z G^(N-n) Z = G^(2n), before the final code",
            "scope": "Distinct modified pointer effects. Transfer uses one table and a common admissible field chart; the unmodified LC1 task fixes its effect."}


def main():
    print(json.dumps({"status": "PASS", "diagonal_checks": [tariff_check(m) for m in range(1, 7)],
                      "two_reader_flat_jet": second_order_contact(),
                      "distinct_native_probability_comparisons": native_probability_settings(),
                      "physical_full_price_selected": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
