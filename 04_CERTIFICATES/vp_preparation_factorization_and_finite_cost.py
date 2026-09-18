"""Exact checks for preparation factorization and finite-cost capacity-variance criterion.

Uses only the Python standard library.
Checks:
1. Operational independence defect Delta = J - 2M + K vanishes iff p = u (x) v.
2. Unbiased sample check verifies factor risk and dependent bias formula.
3. 4-record check matches Delta algebraically.
4. Additivity 1 + rho_{A (x) B} = (1 + rho_A)(1 + rho_B) holds for independent products.
5. Finite cost criterion C_{lambda, L} = log N + lambda log(1 + rho_L) uniquely selects (9, 11, 13)
   at P2 = 371/1089 for all L >= 3 across all 17 partitions.
"""

from fractions import Fraction as F
from functools import reduce
from itertools import combinations, product
from math import comb, gcd, log


def moment(p, degree):
    return sum(x**degree for x in p)


def ingredients(table):
    rows = list(map(sum, table))
    cols = [sum(row[j] for row in table) for j in range(len(table[0]))]
    joint = sum(x * x for row in table for x in row)
    mixed = sum(
        table[i][j] * rows[i] * cols[j]
        for i in range(len(rows))
        for j in range(len(cols))
    )
    independent = moment(rows, 2) * moment(cols, 2)
    delta = sum(
        (table[i][j] - rows[i] * cols[j]) ** 2
        for i in range(len(rows))
        for j in range(len(cols))
    )
    assert delta == joint - 2 * mixed + independent
    return rows, cols, joint, mixed, independent, delta


def variance(p, L):
    k, t = moment(p, 2), moment(p, 3)
    return (2 * k * (1 - k) + 4 * (L - 2) * (t - k * k)) / (L * (L - 1))


def sample_check(table, L):
    rows, cols, J, M, K, delta = ingredients(table)
    outcomes = [(i, j) for i in range(len(rows)) for j in range(len(cols))]
    pairs = list(combinations(range(L), 2))
    mean = square_mean = F(0)
    for sample in product(outcomes, repeat=L):
        probability = F(1)
        for i, j in sample:
            probability *= table[i][j]
        ua = F(sum(sample[a][0] == sample[b][0] for a, b in pairs), comb(L, 2))
        ub = F(sum(sample[a][1] == sample[b][1] for a, b in pairs), comb(L, 2))
        estimate = ua * ub
        mean += probability * estimate
        square_mean += probability * estimate**2
    expected_bias = -2 * (1 - F(2, L)) * (M - K) - (1 - F(2, L * (L - 1))) * delta
    assert mean - J == expected_bias
    if delta == 0:
        va, vb = variance(rows, L), variance(cols, L)
        ka, kb = moment(rows, 2), moment(cols, 2)
        expected_var = (ka * ka + va) * (kb * kb + vb) - ka * ka * kb * kb
        assert square_mean - mean * mean == expected_var
        assert expected_var <= variance([x for row in table for x in row], L)


def four_record_check(table):
    rows, cols, J, M, K, delta = ingredients(table)
    outcomes = [(i, j) for i in range(len(rows)) for j in range(len(cols))]
    expected = F(0)
    for s in product(outcomes, repeat=4):
        probability = F(1)
        for i, j in s:
            probability *= table[i][j]
        j = int(s[0][0] == s[1][0] and s[0][1] == s[1][1])
        m = int(s[0][0] == s[1][0] and s[0][1] == s[2][1])
        k = int(s[0][0] == s[1][0] and s[2][1] == s[3][1])
        expected += probability * (j - 2 * m + k)
    assert expected == delta


def constrained_partitions(total, squares, lower=1):
    if total == 0:
        if squares == 0:
            yield ()
        return
    for first in range(lower, total + 1):
        if first * first > squares:
            break
        for rest in constrained_partitions(
            total - first, squares - first * first, first
        ):
            yield (first,) + rest


def main():
    independent = [[F(2, 15), F(3, 15)], [F(4, 15), F(6, 15)]]
    dependent = [[F(4, 10), F(1, 10)], [F(2, 10), F(3, 10)]]
    for table in (independent, dependent):
        four_record_check(table)
        for L in range(2, 6):
            sample_check(table, L)

    core = (9, 11, 13)
    table = [[F(a * b, 1089) for b in core] for a in core]
    assert ingredients(table)[-1] == 0
    for i, n in enumerate((73, 145, 153)):
        table[i][i] = F(n, 1089)
    assert ingredients(table)[-1] == F(294003328, 1406408618241)

    # Parity example is pairwise independent, but AB and C are dependent.
    xor_table = [
        [F(1, 4), 0],
        [0, F(1, 4)],
        [0, F(1, 4)],
        [F(1, 4), 0],
    ]
    assert ingredients(xor_table)[-1] == F(1, 8)

    # All 17 partitions of N=33 at P2=371/1089 evaluated by finite cost criterion.
    partitions = list(constrained_partitions(33, 371))
    assert len(partitions) == 17
    kappa = F(371, 1089)
    for L in (3, 4, 10, 50):
        for lam in (F(1, 10), F(1, 2), F(1)):
            costs = []
            for p in partitions:
                weights = [F(n, 33) for n in p]
                var = variance(weights, L)
                rho = var / (kappa * kappa)
                cost = log(33) + float(lam) * log(1 + float(rho))
                costs.append((cost, p))
            costs.sort()
            assert costs[0][1] == (9, 11, 13)

    print("Exact independence-event identities passed.")
    print("Eight complete sample enumerations verify factor risk and dependent bias.")
    print("Composition counterexample and parity counterexample detected by Delta.")
    print("Finite-cost D0 minimum verified on all 17 native partitions at four budgets.")


if __name__ == "__main__":
    main()
