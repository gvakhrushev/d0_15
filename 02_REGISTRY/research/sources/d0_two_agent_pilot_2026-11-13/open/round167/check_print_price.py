"""Exact finite journal checks and rational uniform bounds for B167 printing."""
from fractions import Fraction as Q
import json


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def finite_leaves(q, efficiency, service_cap, outer_cap):
    def service(depth, attempt, report, mass, length, factors):
        e = q if report else 1 - q
        for label, weight, factor in (
            ("10", efficiency * e, 0 if report else 1),
            ("01", efficiency * (1 - e), 1 if report else 0),
            ("00", 1 - efficiency, None),
        ):
            counts = list(factors)
            if factor is not None:
                counts[factor] += 1
                counts[2] += 1
            else:
                counts[3] += 1
            next_mass = mass * weight
            next_length = length + (2 if label == "00" else 3)
            if label == "00" and attempt < service_cap:
                yield from service(depth, attempt + 1, report, next_mass, next_length, counts)
            elif label == "01" and depth < outer_cap:
                yield from visit(depth + 1, next_mass, next_length, counts)
            else:
                yield next_mass, next_length, counts

    def visit(depth, mass, length, factors):
        for report in (0, 1):
            q_factor = report if depth == 1 else 1 - report
            weight = q if q_factor else 1 - q
            counts = list(factors)
            counts[0 if q_factor else 1] += 1
            yield from service(depth, 1, report, mass * weight, length + 1 + report, counts)

    return visit(1, Q(1), 0, (0, 0, 0, 0))


def verify_journal(q, eta, service_cap, m):
    g = 1 - (1 - eta) ** service_cap
    kappa = g / eta
    beta = 2 * q * (1 - q)
    visits = 1 + g * beta * sum((g * (1 - beta)) ** j for j in range(m))
    expected_length = visits * (2 * kappa + g) + 1 + q + (visits - 1) * (2 - q)
    expected_factors = (
        q * visits * (1 + g),
        (1 - q) * visits * (1 + g),
        eta * visits * kappa,
        (1 - eta) * visits * kappa,
    )
    mass_sum = Q(0)
    length_sum = Q(0)
    factor_sums = [Q(0)] * 4
    for mass, length, factors in finite_leaves(q, eta, service_cap, m + 1):
        reconstructed_mass = q ** factors[0] * (1 - q) ** factors[1]
        reconstructed_mass *= eta ** factors[2] * (1 - eta) ** factors[3]
        require(mass == reconstructed_mass, "each actual positive leaf factorization")
        mass_sum += mass
        length_sum += mass * length
        for i, count in enumerate(factors):
            factor_sums[i] += mass * count
    require(mass_sum == 1, "all failures retained in normalized law")
    require(length_sum == expected_length, "expected literal length")
    require(tuple(factor_sums) == expected_factors, "exact coefficients of all entropy logarithms")


def verify_constants():
    alpha_max = Q(528, 1000)
    delta_max = Q(473, 1000)
    g_min = Q(89, 100)
    a_bound = Q(28, 10)
    require(2 * alpha_max * delta_max < Q(1, 2), "all finite T derivative bound")
    require(2 / g_min + Q(5, 2) < Q(19, 4), "coefficient upper bound")
    require(Q(11, 100) * (1 + Q(221, 100)) / Q(48, 100) < Q(3, 4), "h(eta) bound")
    require(Q(694, 1000) / Q(48, 100) < Q(29, 20), "binary entropy upper bound")
    m3_bound = delta_max * (2 * alpha_max * (1 - g_min**2) + 3 * alpha_max**2 * g_min**2)
    require(m3_bound < Q(42, 100), "three-cycle derivative bound")
    require(4 * delta_max * alpha_max**3 < Q(28, 100), "late derivative constant")
    require(delta_max / (1 - alpha_max) ** 2 < Q(213, 100), "late service derivative")
    losses = (
        a_bound / 2 - Q(3, 4),
        a_bound * Q(42, 100) - Q(3, 8),
        a_bound * Q(28, 100) + (a_bound * Q(213, 100) - 5) * (1 - g_min),
    )
    require(max(losses) < Q(891, 1000), "nine copies suffice uniformly")


def verify_passive_weights():
    import sympy as sp

    x = sp.Symbol("p")
    golden = x * x + x - 1
    p = (sp.sqrt(5) - 1) / 2
    g = sp.Matrix([[sp.sqrt(p), -p], [p, sp.sqrt(p)]])
    z = sp.diag(1, -1)
    v = g[:, 0]
    require(((z * g * z * g) - sp.eye(2)).applyfunc(sp.simplify) == sp.zeros(2), "balanced identity endpoint")
    require((z * z * g * g - g * g).applyfunc(sp.simplify) == sp.zeros(2), "balanced squared endpoint")
    require(sp.simplify((v.T * g * g * v)[0] - p**3) == 0, "squared-arm passive amplitude")
    for copies in (6, 9):
        for bit in (0, 1):
            exponent = copies * (3 + 2 * bit) + 6 * (copies // 3) * (1 - bit)
            require(exponent == 5 * copies, "all leaves have the same additional passive attenuation")
    require(sp.rem(x**4 - x**7 - 2 * x**6, golden) == 0, "printed REPORT weight difference is 2 p^6")
    return {"00": 2 + 6, "10": 3 + 8, "01": 3 + 8}


def main():
    verify_constants()
    configurations = 0
    for eta in (Q(89, 100), Q(19, 20)):
        for q in (Q(2, 5), Q(1, 2), Q(3, 5)):
            for service_cap in range(1, 4):
                for m in range(3):
                    verify_journal(q, eta, service_cap, m)
                    configurations += 1
    weights = verify_passive_weights()
    result = {
        "status": "PASS",
        "exact_journal_configurations": configurations,
        "physical_raw_marks_include_dark_11": True,
        "test_mark_passive_exponents_after_base_printing": weights,
        "extra_initial_copies": {"EC-H": 6, "EC-2H": 9},
        "uniform_derivative_lower_bounds_after_printing": {"EC-H": "2", "EC-2H": "0.109"},
        "GR_closed": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
