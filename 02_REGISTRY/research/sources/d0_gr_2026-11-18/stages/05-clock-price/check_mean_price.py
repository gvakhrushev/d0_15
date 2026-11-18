"""Check the paid harmonic counter and the cold return of its native writer."""
import json
from decimal import Decimal, localcontext
from pathlib import Path

import sympy as sp


def writer():
    p = (sp.sqrt(5) - 1) / 2
    v = sp.Matrix([sp.sqrt(p), p])
    gate = sp.Matrix([[sp.sqrt(p), -p], [p, sp.sqrt(p)]])
    z = sp.diag(1, -1)
    assert (z * gate * z - gate.T).applyfunc(sp.simplify) == sp.zeros(2)
    initial = sp.kronecker_product(v, v)
    cx = sp.eye(4)[:, [0, 1, 3, 2]]
    nc1 = cx * sp.kronecker_product(sp.eye(2), gate) * cx
    actual = nc1 * sp.kronecker_product(gate.T, sp.eye(2)) * initial
    expected = sp.kronecker_product(sp.Matrix([1, 0]), gate * v)
    assert (actual - expected).applyfunc(sp.simplify) == sp.zeros(4, 1)
    assert sp.simplify(initial.dot(actual) - p) == 0
    assert sp.simplify(actual.dot(actual) - 1) == 0
    for count in range(1, 6):
        born = sp.kronecker_product(*([v] * count)) if count > 1 else v
        zero_amplitude = born[0]
        assert sp.simplify(zero_amplitude**2 - p**count) == 0


def check_counter(prob, dimension, beta, a, reference=None):
    one = Decimal(1)
    x = one - prob
    action = ((a * dimension).ln() - prob.ln()) / beta
    if reference is not None:
        assert abs(reference - action) < Decimal("3e-14")
    caps = {}
    for limit in (1, 2, 8, 16, 64):
        value = (a * dimension).ln() / beta
        slope = Decimal(0)
        for j in range(1, limit + 1):
            unit = one / (beta * j)
            integral = int(unit)
            frac = unit - integral
            randomized_count = integral * (one - frac) + (integral + 1) * frac
            value += x**j * randomized_count
            slope += j * x**(j-1) * beta * prob * randomized_count
        # Independent enumeration by terminal time including its timeout.
        payouts = [(a * dimension).ln() / beta]
        for j in range(1, limit + 1):
            payouts.append(payouts[-1] + one / (beta * j))
        complete_mean = sum(prob * x**j * payouts[j] for j in range(limit))
        complete_mean += x**limit * payouts[limit]
        assert abs(value - complete_mean) < Decimal("1e-75")
        assert abs(slope - (1 - x**limit)) < Decimal("1e-75")
        bound = x**(limit+1) / (beta * (limit+1) * prob)
        assert -Decimal("1e-78") < action - value < bound + Decimal("1e-78")
        caps[limit] = dict(tail_bound=float(bound), slope_loss=float(x**limit))
    p = (Decimal(5).sqrt() - one) / 2
    ell = -p.ln()
    q = x / (1 - p)
    assert 0 < q < 1
    gains = {}
    step = Decimal("1e-18")
    for theta in (Decimal("0.01"), ell, one, Decimal(5)):
        jump = 1 - (-theta).exp()
        moment = 1 - jump*q
        gain = beta * prob * jump / (theta * (1-p) * moment)
        def price(action_shift):
            shifted_q = (1 - prob * (-beta*action_shift).exp()) / (1-p)
            return -(1 - jump*shifted_q).ln() / theta
        secant = (price(step) - price(-step)) / (2*step)
        assert gain > 0 and abs(gain - secant) < Decimal("1e-31")
        if theta == ell:
            assert abs(moment - prob) < Decimal("1e-80")
        gains[str(round(theta, 6))] = float(gain)
    floor = int(action)
    frac = action - floor
    min_integer_moment = p**floor * (1-frac+p*frac)
    if frac:
        assert min_integer_moment > (-ell*action).exp()
    return dict(target=float(action), probability=float(prob),
                mean_external_trials=float(one / prob), caps=caps,
                binary_report_gains=gains,
                lattice_Jensen_relative_excess=float(min_integer_moment/(-ell*action).exp()-1))


def main():
    writer()
    with localcontext() as ctx:
        ctx.prec = 90
        one = Decimal(1)
        p = (Decimal(5).sqrt() - one) / 2
        beta = 2 * p**2
        a = 359 - 66 * (beta / 5).exp()
        models = json.loads(Path(__file__).with_name("master_mark_result.json").read_text())
        results = {}
        for row in models["models"]:
            results[row["native_word"]] = check_counter(
                Decimal(str(row["marked_probability_identity"])),
                row["clock_dimension"], beta, a, Decimal(str(row["B"])))
        for dim in (4, 108, 100000):
            for prob in ("0.66", "0.725", "0.8"):
                check_counter(Decimal(prob), dim, beta, a)
        worst_gain_loss = Decimal("0.34")**16
        assert worst_gain_loss < Decimal("3.2e-8")
        assert 1 / Decimal("0.66") < Decimal("1.52")
        z = one / (2**20)
        sealed_widths = {}
        for count in (1, 8, 16, 64):
            width = 4 * (1 + z*p**count/(1-z)).ln()
            basic_bound = 4 * z*p**count/(1-z)
            assert 0 < width <= basic_bound
            for old_return in (Decimal(0), p, one):
                new_effect = p**(2*count)*old_return
                distance = 4 * (1 + z*new_effect/(1-z)).ln()
                assert 0 <= distance <= width
            sealed_widths[count] = float(width)
        return dict(result="PASS", models=results, writer_cold_amplitude="1/phi",
                    writer_parsed_length=1, writer_conditional_information=0,
                    sealed_feedback_width=sealed_widths,
                    uniform_cap16_relative_loss=float(worst_gain_loss),
                    physical_full_action_identified=False, GR_closed=False)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
