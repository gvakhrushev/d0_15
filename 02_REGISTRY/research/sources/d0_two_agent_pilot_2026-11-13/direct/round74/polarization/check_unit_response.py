"""Check both CNOTs, the unit response, and the distinction between two information ledgers."""
from itertools import product
from pathlib import Path

import sympy as sp


def check(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    p = (sp.sqrt(5) - 1) / 2
    phi = 1/p
    m, q, energy = sp.symbols("M q R", positive=True)
    alpha = p**3/m
    # The original port1 is a complete positive effect, acting also on mixed inputs.
    source = Path(__file__).resolve().parents[7] / "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source"
    check("full port1 effect is p epsilon Delta" in (source/"PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE.md").read_text(),
          "original port equation")
    check("Cost_port=1+p epsilon R" in (source/"PRIMARY_CAR_RECORD_PRICE_SOURCE.md").read_text(),
          "original recorded port charge")
    h = p+2*p**2  # -sum Pr log_phi Pr in either orientation
    charge = 0
    mean_flips = 0
    for port, selector, raw in product((0, 1), repeat=3):
        probability = (q if port else 1-q) * (p if selector else p**2) * (p**2 if raw else p)
        first = raw ^ 1 ^ port
        second = raw ^ selector ^ port
        charge += probability * m * (17*(1+first) + 4*(1+second))
        mean_flips += probability * m * (17*(1 ^ port) + 4*(selector ^ port))
    newly_paid = sp.expand(charge - 21*m*h)
    check(sp.simplify(newly_paid - p**3 * mean_flips) == 0, "actual mean code")
    at_effect = sp.expand(newly_paid.subs(q, alpha*energy))
    check(sp.simplify(sp.diff(at_effect, energy) + 1) == 0, "unit cancellation")
    constant = m*p**3*(17+4*p)
    check(sp.simplify(at_effect - constant + energy) == 0, "absolute intercept")
    check(sp.simplify(p**6*(17+4*(2*p-1))-1) == 0, "integer Golden schedule")
    # Alternate fixed circuit with no known-one control. Selector j has
    # amplitudes G^j |0>; D_j is its signed difference of flip counts.
    gate = sp.Matrix([[sp.sqrt(p), -p], [p, sp.sqrt(p)]])
    counts = [6, 1, 1194, 143]
    differences = []
    for j in range(4):
        probability_one = (gate**j)[1, 0]**2
        difference = -sp.chebyshevt(j, 2*p-1)
        check(sp.simplify(2*probability_one - 1 - difference) == 0, "native selector probability")
        differences.append(difference)
    check(sum(counts) == 21*64, "fixed slots without constant control")
    check(sp.simplify(sum(n*d for n, d in zip(counts, differences))*p**6-64) == 0,
          "exact signed count difference without constant control")
    extra = [3, 6, 9, 1]
    check(sum(extra) == 19 and sp.simplify(sum(n*d for n, d in zip(extra, differences))*p**3 - 1) == 0,
          "optional exact cancellation of the original mandatory port code")
    # The result is an operator identity, not tied to a diagonal input tangent.
    t = sp.symbols("t", real=True)
    effect = sp.Matrix([[sp.Rational(1,4), t], [t, sp.Rational(1,3)]])
    rho = sp.Matrix([[sp.Rational(2,3)+t, sp.Rational(1,9)], [sp.Rational(1,9), sp.Rational(1,3)-t]])
    port = sp.trace(rho*effect)
    net = (newly_paid + q/alpha).subs(q, port)
    check(sp.simplify(sp.diff(net, t)) == 0, "moving state and noncommuting moving operand")
    # Distinct actual leaf responses when Info means conditional self-information.
    check(sp.simplify(p**2 * phi + p / phi - 1) == 0, "exponential Born moment")
    check(sp.simplify(phi + 1/phi - sp.sqrt(5)) == 0, "counting moment")
    check(sp.simplify((2*p+p**2)-h-p**3) == 0, "conditional mean")
    print("PASS exact unit response on all port effects; fixed binary circuit and conditional record price")


if __name__ == "__main__":
    main()
