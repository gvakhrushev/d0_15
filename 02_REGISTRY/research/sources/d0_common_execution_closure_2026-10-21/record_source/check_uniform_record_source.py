#!/usr/bin/env python3
"""Narrow exact controls of the complete-record source theorem; no circuit replay."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def moment(xs, k):
    return sum((x ** k for x in xs), F(0))


def gradient(xs, kind):
    if isinstance(kind, int):
        return [kind * x ** (kind - 1) for x in xs]
    if kind == "square_of_purity":
        return [4 * moment(xs, 2) * x for x in xs]
    if kind == "purity_times_third_moment":
        a, b = moment(xs, 2), moment(xs, 3)
        return [2 * x * b + 3 * x * x * a for x in xs]
    raise ValueError(kind)


def dot(xs, ys):
    return sum((x * y for x, y in zip(xs, ys)), F(0))


def local_vector(m, r, dp, dr):
    p = F(1, m)
    q, dq = [], []
    for t in range(m):
        q.extend([p * (1 - r), p * r])
        dq.extend([dp[t] * (1 - r) - p * dr[t], dp[t] * r + p * dr[t]])
    require(sum(q) == 1 and sum(dq) == 0, "normalized probability tangent")
    return q, dq


def product_vector(qs, dqs):
    indices = list(itertools.product(*(range(len(q)) for q in qs)))
    q, dq = [], []
    for idx in indices:
        value = F(1)
        for a, i in enumerate(idx):
            value *= qs[a][i]
        delta = F(0)
        for a, i in enumerate(idx):
            term = dqs[a][i]
            for b, j in enumerate(idx):
                if b != a:
                    term *= qs[b][j]
            delta += term
        q.append(value)
        dq.append(delta)
    require(sum(q) == 1 and sum(dq) == 0, "normalized product tangent")
    return indices, q, dq


def run():
    checks = []
    r = F(1, 7)
    kinds = [2, 3, 4, "square_of_purity", "purity_times_third_moment"]
    for m in [2, 4]:
        dp = [F(t + 1, 13) for t in range(m - 1)]
        dp.append(-sum(dp))
        dr = [F(2 * t - 1, 19) for t in range(m)]
        q, dq = local_vector(m, r, dp, dr)
        report_delta = sum(dq[1::2])
        require(report_delta == sum(dr) / m, "matched report removes label normals")
        for kind in kinds:
            g = gradient(q, kind)
            coeff = g[1] - g[0]
            require(dot(g, dq) == coeff * report_delta, f"local spectral source {m},{kind}")
            checks.append(f"local M={m}: {kind}")

    # Genuine nonadditive valuation on the entire three-cell product spectrum.
    qs, dqs, report_deltas = [], [], []
    for a in range(3):
        dp = [F(a + 1, 17), -F(a + 1, 17)]
        dr = [F(a - 1, 11), F(2 - a, 23)]
        q, dq = local_vector(2, r, dp, dr)
        qs.append(q)
        dqs.append(dq)
        report_deltas.append(sum(dq[1::2]))
    idxs, qprod, dqprod = product_vector(qs, dqs)
    require(len(set(qprod)) == 4, "three report factors have four Hamming strata, not two")
    for kind in kinds:
        g = gradient(qprod, kind)
        coefficients = []
        for a in range(3):
            marginal = [F(0) for _ in qs[a]]
            for idx, grad in zip(idxs, g):
                weight = F(1)
                for b, j in enumerate(idx):
                    if b != a:
                        weight *= qs[b][j]
                marginal[idx[a]] += grad * weight
            require(marginal[0] == marginal[2] and marginal[1] == marginal[3], "marginal label symmetry")
            coefficients.append(marginal[1] - marginal[0])
        require(len(set(coefficients)) == 1, "identical cell profiles share source coefficient")
        require(dot(g, dqprod) == coefficients[0] * sum(report_deltas), "global product source")
        checks.append(f"nonadditive whole-product source: {kind}")

    # Uniform measured permutation block: first-order averaging without
    # asserting equality of the complete off-diagonal nonadditive prices.
    q0, d0 = local_vector(2, r, [F(1, 5), F(-1, 5)], [F(1, 3), F(1, 7)])
    _, d1 = local_vector(2, r, [F(-1, 11), F(1, 11)], [F(-1, 2), F(1, 13)])
    q = [x / 2 for x in q0] * 2
    dq = [x / 2 for x in d0] + [x / 2 for x in d1]
    for kind in kinds:
        g = gradient(q, kind)
        mean_delta = [(x + y) / 2 for x, y in zip(d0, d1)]
        require(dot(g, dq) == dot(g[:len(q0)], mean_delta), "actual measured permutation differential")
        checks.append(f"measured permutation first source: {kind}")

    q, dq = local_vector(2, r, [F(1, 3), F(-1, 3)], [F(0), F(0)])
    require(sum(dq[1::2]) == 0, "control has no report source")
    unequal_label_charge = F(2, 5) * sum(dq[:2])
    require(unequal_label_charge != 0, "unequal physical label charge must survive")

    # Different cell coefficients invalidate cancellation of opposite report tangents.
    c = 2 * (2 * r - 1)
    unequal_cell_source = c * (F(1) * F(1, 9) + F(2) * F(-1, 9))
    require(unequal_cell_source != 0, "unequal cell price control")

    # At one-half readiness, a pure failed report instead of matched r0
    # gives a nonzero source for the full spectral purity.
    readiness_source = r * r + (1 - r) ** 2 - 1
    require(readiness_source != 0, "unmatched abort source survives")
    require(dot([F(1)] * len(q), dq) == 0, "trace has zero response")

    checks.extend([
        "unequal paid label charge survives with zero report source",
        "unequal cell coefficients destroy opposite-source cancellation",
        "unmatched abort leaves a readiness source",
        "trace symmetry alone gives no nonzero gravitational response",
    ])
    return {
        "status": "PASS_EXACT_UNIFORM_RECORD_SOURCE_CONTROLS",
        "method": "exact Fraction arithmetic; analytic proof supplies the general theorem",
        "checks": checks,
        "negative_controls": {
            "unequal_label_source": str(unequal_label_charge),
            "unequal_cell_source": str(unequal_cell_source),
            "unmatched_abort_purity_source": str(readiness_source),
        },
        "scope": {
            "local_spectral_first_source": True,
            "actual_product_spectrum_not_binary": True,
            "measured_permutation_first_order_only": True,
            "Book03_spectral_binding_proved": False,
            "general_valuation_Hessians_identified": False,
            "physical_GR_selection": False,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = run()
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(output)
    else:
        print(output, end="")
