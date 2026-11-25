"""Exact two-record comparison on the validated Parry support of #334, §7fx."""
from sympy import Rational, S, diff, exp, expand_log, log, simplify, sqrt, symbols


def equal(actual, expected, label):
    if simplify(actual - expected) != 0:
        raise ArithmeticError(label)


def main():
    p = (sqrt(5) - 1) / 2
    ell = -log(p)
    support = ((0, 0), (0, 1), (1, 0))
    lengths = tuple(sum(1 + mark for mark in word) for word in support)

    # Use independent positive factors while splitting the logarithms. Then
    # restrict to the interior of the two probability simplices.
    b0, b1, u0, u1 = symbols("b0 b1 u0 u1", positive=True)
    probabilities = (b0 * u0, b0 * u1, b1)
    q, u = symbols("q u", positive=True)
    normalize = {b0: 1 - q, b1: q, u0: 1 - u, u1: u}
    equal(sum(probabilities).subs(normalize), 1, "mass on the three valid leaves")

    # Old report costs and new report costs are each charged once. Valuation
    # under test: classical surprisal on both records and a scalar Born mean.
    scores = [length + expand_log(log(prob)) / ell
              for prob, length in zip(probabilities, lengths)]
    mean = sum(mass * score for mass, score in zip(probabilities, scores)).subs(normalize)
    moment = sum(mass * exp(-ell * score)
                 for mass, score in zip(probabilities, scores)).subs(normalize)

    def code_price(x):
        return 1 + x + (x * log(x) + (1 - x) * log(1 - x)) / ell

    expected_mean = code_price(q) + (1 - q) * code_price(u) + q
    equal(mean, expected_mean, "complete two-report mean, including coarse information")
    equal(moment, p**2 + 2 * p**3, "complete three-leaf scalar moment")
    equal(moment, 1 - p**4, "existing two-tick Golden mass")
    pressure = -log(moment) / ell
    for direction in (q, u):
        equal(diff(pressure, direction), 0, "fixed-support scalar covector")

    # PX5 selects u=p². At that point (1-u,u)=(p,p²).
    # Reduce its two logs with p+p²=1 and positivity, before simplifying
    # expressions containing log of algebraic numbers.
    def at_parry(expression):
        return expression.subs({log(u): -2 * ell, log(1 - u): -ell}).subs(u, p**2)

    equal(1 - p**2, p, "Parry bright probabilities")
    equal(at_parry(code_price(u)), 0, "stationary conditional bright price")
    equal(at_parry(diff(mean, q)), 1 + diff(code_price(q), q), "coarse source")
    equal(at_parry(diff(mean, u)), 0, "independent bright redistribution source")

    # Apply surprisal only to the second token as in PX1/PX5. This is a
    # different statistic of the same leaves and detects omission of token 1.
    new_probabilities = (u0, u1, S.One)
    aux_moment = sum(mass * p**(1 + word[1]) / cond
                     for word, mass, cond in zip(support, probabilities, new_probabilities))
    equal(aux_moment.subs(normalize), 1 - p**2 * q, "second-token-only moment")
    equal(diff(aux_moment.subs(normalize), q), -p**2, "second-token-only variation")
    equal((moment - aux_moment.subs(normalize)).subs(q, Rational(1, 2)),
          p**2 * (Rational(1, 2) - p**2), "two-token and one-token differ on the collar")

    # If leaf tariffs really move on a family, the constant-mass result
    # applies only to fixed code lengths. Differentiate ALL three additions.
    extra = symbols("w00 w01 w10", real=True)
    terms = [mass * exp(-ell * (score + w))
             for mass, score, w in zip(probabilities, scores, extra)]
    varied_moment = sum(terms)
    weights = [p**length * exp(-ell * w) for length, w in zip(lengths, extra)]
    equal(varied_moment, sum(weights), "scalar sum with moving leaf work")
    for w, weight in zip(extra, weights):
        equal(diff(-log(varied_moment) / ell, w), weight / sum(weights),
              "normalized reaction to each independent moving tariff")

    print("support=00,01,10  lengths=2,3,3")
    print("both records: Z=1-p^4  D(-log_phi Z)=0  Gamma_scalar=0")
    print("both records at u=p^2: D(mean)=(1+f'(q))Dq  partial_u=0")
    print("second record alone: Z_aux=1-p^2*q")
    print("moving leaf work: D(-log_phi Z)=sum_i tau_i Dw_i")
    print("full physical CD13: unavailable from the specified record valuations")


if __name__ == "__main__":
    main()
