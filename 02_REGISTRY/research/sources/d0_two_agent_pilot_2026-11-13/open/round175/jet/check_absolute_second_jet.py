"""Exact receipts for the phase-invariant SC1 and second-jet example."""

from fractions import Fraction
from math import comb
import json


def require(condition, label):
    if not condition:
        raise ValueError(label)


def retained_harmonics(power, lattice, sigma, eccentricity):
    """Average (sigma*(1-t*cos(2x+phase)))**power over a cyclic SITE."""
    result = {}
    for count in range(power + 1):
        prefactor = sigma**power * comb(power, count) * (-eccentricity / 2)**count
        for left in range(count + 1):
            wave = 2 * left - count
            if (2 * wave) % lattice == 0:
                result[wave] = result.get(wave, 0) + prefactor * comb(count, left)
    return {wave: coefficient for wave, coefficient in result.items() if coefficient}


def covariance(vectors, weights):
    means = [
        sum(weight * vector[i] for weight, vector in zip(weights, vectors))
        for i in range(2)
    ]
    return means, [
        [
            sum(
                weight * (vector[i] - means[i]) * (vector[j] - means[j])
                for weight, vector in zip(weights, vectors)
            )
            for j in range(2)
        ]
        for i in range(2)
    ]


def main():
    sigma = Fraction(1, 64)
    eccentricity = Fraction(1, 2)
    traces = {}
    for lattice in (18, 20, 24, 32, 64):
        moments = []
        for degree in range(1, 9):
            receipt = retained_harmonics(degree, lattice, sigma, eccentricity)
            require(set(receipt) == {0}, f"phase harmonic survived, L={lattice}, k={degree}")
            moments.append(receipt[0])
        require(moments[0] == sigma, "physical mean material action")
        require(
            moments[1] == sigma**2 * (1 + eccentricity**2 / 2),
            "physical second material moment",
        )
        traces[lattice] = [str(x) for x in moments]

    # sin(pi H) <= pi H, pi < 22/7, min t0 = 1/4, min w'(Q) = 3/2.
    uniform_hessian_lower = Fraction(3, 4) * sigma / (4 * Fraction(22, 7)**2)
    require(uniform_hessian_lower > Fraction("0.00029"), "native trace Hessian lower bound")

    centers, cov = covariance(
        ((2, 1), (-2, 1), (0, -1)),
        (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)),
    )
    require(centers == [0, 0], "exact two-dimensional first compensation")
    require(cov == [[2, 0], [0, 1]], "nonzero covariance at equal first derivative")
    require(
        Fraction(1, 3) - Fraction(1, 1) / (3 + Fraction(1, 2)) == Fraction(1, 21),
        "Schur shift with the same uneliminated geometric block",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "phase_invariant_moments": traces,
                "native_hessian_lower": str(uniform_hessian_lower),
                "rank_two_work_covariance": [[int(x) for x in row] for row in cov],
                "schur_shift": "1/21",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
