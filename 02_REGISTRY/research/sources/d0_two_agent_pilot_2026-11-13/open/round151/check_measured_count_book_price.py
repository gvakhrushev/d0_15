"""Finite proof controls for the measured-count and scalar price theorems."""

from collections import Counter, defaultdict
from functools import reduce
from hashlib import sha256
from itertools import product
import json
from math import exp, log, pi, sqrt
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
RESEARCH = "02_REGISTRY/research/"
PILOT = RESEARCH + "sources/d0_two_agent_pilot_2026-11-13/"
SOURCES = (
    RESEARCH + "A4D_NATIVE_BOOK03_BORN_ENTROPY_BELLMAN_VERTEX_INFORMATION_WELD_2026_10_22.md",
    PILOT + "open/round150/RESULT.json",
    PILOT + "direct/round76/geometry/INVISIBLE_GEOMETRY_RU.md",
    PILOT + "direct/round76/record/COMPLETE_RECORD_PRICE_RU.md",
    PILOT + "direct/round76/history/STOPPED_HISTORY_RU.md",
)
sys.path.insert(0, str(HERE.parent / "round149"))
from check_full_book_memory_return import multiply


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def equal(actual, expected, message):
    require(sp.simplify(actual-expected) == 0, message)


def check_bernstein():
    n = sp.Symbol("n", positive=True, integer=True)
    t = sp.Symbol("t", positive=True)
    means = (n*(n-1)*(n-2)*t**3 + 3*n*(n-1)*t**2 + n*t)/n**3
    diffusion = t*(1-t)*sp.diff(t**3, t, 2)/2
    expected_residual = t*(1-t)*(1-2*t)/n**2
    equal(means - t**3 - diffusion/n, expected_residual, "Cubic first Bernstein bias")
    p1, p2, unit = sp.symbols("p1 p2 ell", positive=True)
    prob = sp.Matrix([p1, p2])
    p3 = 1-p1-p2
    cov = sp.diag(p1, p2)-prob*prob.T
    hess = 2*(sp.diag(1/p1, 1/p2)+sp.ones(2)/p3)/unit
    equal(sp.trace(cov*hess)/2, 2/unit, "Constant finite-alphabet entropy bias")


def check_fine_prefixes():
    leaves = {"00": sp.Rational(1, 5), "01": sp.Rational(2, 5),
              "1": sp.Rational(2, 5)}
    raw_price = {"00": 2, "01": 11, "1": 4}
    effective_cost = {leaf: -2*sp.log(pr) for leaf, pr in leaves.items()}
    tail = {leaf: effective_cost[leaf]-raw_price[leaf] for leaf in leaves}
    def conditional(prefix):
        support = [key for key in leaves if key.startswith(prefix)]
        mass = sum(leaves[key] for key in support)
        entropy = -sum(leaves[key]/mass*sp.log(leaves[key]/mass) for key in support)
        cost = sum(leaves[key]/mass*(raw_price[key]+tail[key]) for key in support)
        return mass, entropy, cost

    edges = (("", "0"), ("", "1"), ("0", "00"), ("0", "01"))
    for u, child in edges:
        mass, entropy, cost = conditional(u)
        child_mass, child_entropy, child_cost = conditional(child)
        q = child_mass/mass
        gain = sp.log(q) + 2*(entropy-child_entropy) + child_cost-cost
        equal(gain, -sp.log(q), "True Shannon gain on a fine asymmetric prefix")


def check_local_surprise():
    t = sp.Symbol("t", positive=True)
    stops = ((2, 0, 1), (3, 1, 2), (4, 3, 5), (5, 5, 7))
    weights = [coef*(1+t)**count/t**success for count, success, coef in stops]
    total = sum(weights)
    scores = [count*t/(1+t)-success for count, success, _ in stops]
    mean = sum(weight*score for weight, score in zip(weights, scores))/total
    covariance = sum(weight*(score-mean)**2
                     for weight, score in zip(weights, scores))/total
    counts = sum(weight*count for weight, (count, _, _) in zip(weights, stops))/total
    derivative = t*sp.diff(t*sp.diff(sp.log(total), t), t)
    equal(derivative, counts*t/(1+t)**2+covariance, "Adaptive local-surprise curvature")


def check_a76_output_rows():
    constraints = []
    for block in range(4):
        row = [0]*32
        row[16+4*block], row[16+4*block+1] = 1, -1
        constraints.append(row)
    for label in (1, 3):
        constraints.append([(-1)**bin(label & k).count("1") for k in range(16)] + [0]*16)
    tangent = sp.Matrix.hstack(*sp.Matrix(constraints).nullspace())
    require(tangent.cols == 26, "A76 finite affine dimension")
    require(all(any(coefficient for coefficient in row) for row in tangent.tolist()),
            "Every ordinary positive Walsh outcome is nonconstant")
    p = (sp.sqrt(5)-1)/2
    blank = 4*p**4*tangent[0, :] - 4*p**2*sp.ones(1, 32)*tangent
    require(any(sp.simplify(entry) != 0 for entry in blank), "Blank outcome also moves")


def check_ordered_classes():
    labels = (2, 3, 1)
    by_count = defaultdict(Counter)
    cancelled = 0
    for word in product(range(len(labels)), repeat=8):
        sign = reduce(multiply, (labels[item] for item in word), 1)
        counts = tuple(word.count(item) for item in range(3))
        by_count[counts][sign] += 1
        pair = next((j for j in range(0, 8, 2) if {word[j], word[j+1]} == {0, 1}), None)
        if pair is not None:
            swapped = list(word)
            swapped[pair:pair+2] = reversed(swapped[pair:pair+2])
            other = reduce(multiply, (labels[item] for item in swapped), 1)
            require(other == -sign, "Adjacent same-count swap flips central class")
            cancelled += 1
    for counts, signs in by_count.items():
        if counts[0] and counts[1] and counts[0] % 2 == counts[1] % 2 == 0:
            require(set(signs) == {1, -1}, "Interior central count admits both signs")
    return cancelled


def saddle_control(n, theta, tariff_error=0):
    ell = log((1+sqrt(5))/2)
    center = 0.5+theta
    weights = []
    for k in range(n+1):
        x = k/n-center
        f = (k/n-0.5)**2/4+(k/n-0.5)/5
        error = tariff_error * (1 if x > 0 else -1)
        weights.append((exp(-n*x*x/2-ell*(f+error)), n*x))
    total = sum(weight for weight, _ in weights)/sqrt(2*pi*n)
    score = sum(weight*derivative for weight, derivative in weights)
    mean = sum(weight for weight, _ in weights)
    return -log(total)/ell, -score/(ell*mean)


def check_saddle():
    # Diagnostic instance only. g=theta/2+theta²/2, so the physical
    # auxiliary scalar factor a=exp(L-g) is nonconstant.
    errors = {}
    for n in (64, 128, 256, 512, 1024):
        values = []
        for theta in (-0.15, 0.0, 0.15):
            free, derivative = saddle_control(n, theta)
            values.extend((abs(free-(theta**2/4+theta/5)), abs(derivative-(theta/2+0.2))))
        errors[str(n)] = max(values)
    require(errors["1024"] < errors["128"]/6, "Unscaled numerical saddle convergence")
    _, baseline = saddle_control(1024, 0)
    _, disturbed = saddle_control(1024, 0, 1/sqrt(1024))
    require(0.7 < abs(disturbed-baseline) < 0.9, "Arbitrary tariff errors can leave finite drift")
    return errors, abs(disturbed-baseline)


def main():
    check_bernstein()
    check_fine_prefixes()
    check_local_surprise()
    check_a76_output_rows()
    ordered_leaves = check_ordered_classes()
    convergence, drift = check_saddle()
    print(json.dumps({
        "GR_closed": False,
        "actual_full_economic_weight_and_admission_proved": False,
        "nonconstant_active_A76_affine_rows": 64,
        "A76_affine_dimension": 26,
        "symmetry_paired_ordered_leaves_of_3_to_8": ordered_leaves,
        "unscaled_lattice_control_max_errors": convergence,
        "diagnostic_sqrt_n_tariff_error_derivative_drift": drift,
        "source_sha256": {path: sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in SOURCES},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
