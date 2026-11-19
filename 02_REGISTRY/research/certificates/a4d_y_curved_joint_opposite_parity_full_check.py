#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact full-joint rank on lambda=(mu,-mu,-mu,-mu), mu in C*.

Two 96-row charts of the literal 136x96 rational Laurent symbol are made
integer-polynomial by multiplying every entry by 14*mu.  Their determinants
have degree at most 192.  A 256-point NTT over several exact prime fields
recovers each determinant modulo the product of the primes.  The integer
coefficient bound from the Leibniz expansion makes the signed CRT lift unique.
The first prime bounds the characteristic-zero gcd from above; exact division
supplies the matching lower bound.  This line is the opposite-spatial-parity
coset of the common-phase line, not an all-Bloch theorem.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from flint import nmod_mat, nmod_poly
import sympy as sp
from sympy.polys.domains import QQ, ZZ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_joint_rational_stencil as S

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_curved_joint_opposite_parity_full_results.json"
SIZE = 256
FIRST_PRIME = 998244353
R = sp.symbols("mu")


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


# Coefficients of 14*mu*Q(mu,-mu,-mu,-mu), indexed by degree, row, column.
coeff = [[[0] * 96 for _ in range(136)] for _ in range(3)]
for owner, offset in ((S.ATERMS, 0), (S.QTERMS, 96)):
    for shift, entries in owner.items():
        degree = 1 + sum(shift)
        ck("LAURENT_DEGREE_" + str(shift), 0 <= degree <= 2)
        sign = -1 if sum(shift[1:]) % 2 else 1
        for (row, col), value in entries.items():
            scaled = 14 * value * sign
            if scaled.denominator != 1:
                raise AssertionError("DENOMINATOR_14")
            coeff[degree][offset + row][col] += scaled.numerator
ck("INTEGER_POLYNOMIAL_MATRIX", len(coeff) == 3)


def chart_rows(value, order):
    # Rational row reduction only selects a chart.  No rank theorem is
    # inferred from this specialization; both determinants are reconstructed.
    mat = sp.Matrix([
        [sum(coeff[k][row][col] * value**k for k in range(3))
         for row in order]
        for col in range(96)
    ])
    _, pivots = DomainMatrix.from_Matrix(mat).convert_to(QQ).rref()
    ck("CHART_RANK_AT_" + str(value), len(pivots) == 96)
    return [order[j] for j in pivots]


charts = [
    chart_rows(2, list(range(136))),
    chart_rows(3, list(range(96, 136)) + list(range(96))),
]
ck("CHARTS_DISTINCT", charts[0] != charts[1])
ck("FIRST_CHART_CONNECTION_ONLY", charts[0] == list(range(96)))


def row_bound(rows):
    # The coefficient l1 norm of det M is at most
    # product_i sum_j ||M_ij||_1 by the Leibniz formula.
    bound = 1
    for row in rows:
        bound *= sum(sum(abs(coeff[k][row][col]) for k in range(3))
                     for col in range(96))
    return bound


bounds = [row_bound(rows) for rows in charts]
ck("FINITE_EXACT_COEFFICIENT_BOUNDS", all(x > 0 for x in bounds))


def primes():
    yield FIRST_PRIME
    candidate = FIRST_PRIME + SIZE
    while True:
        if sp.isprime(candidate):
            yield candidate
        candidate += SIZE


def root_of_order_256(p):
    ck("PRIME_CONGRUENCE_" + str(p), (p - 1) % SIZE == 0)
    for base in range(2, p):
        root = pow(base, (p - 1) // SIZE, p)
        if pow(root, SIZE // 2, p) != 1:
            ck("ROOT_ORDER_" + str(p), pow(root, SIZE, p) == 1)
            return root
    raise AssertionError("NO_PRIMITIVE_ROOT")


def modular_determinant(rows, p, omega):
    matrices = [
        [coeff[k][row][col] % p for row in rows for col in range(96)]
        for k in range(3)
    ]
    values = []
    point = 1
    for _ in range(SIZE):
        point2 = point * point % p
        entries = [(a + point*b + point2*c) % p
                   for a, b, c in zip(*matrices)]
        values.append(int(nmod_mat(96, 96, entries, p).det()))
        point = point * omega % p
    ck("FULL_NTT_ORBIT_" + str(p), point == 1)
    inv_size = pow(SIZE, -1, p)
    result = []
    for degree in range(SIZE):
        step = pow(omega, (-degree) % SIZE, p)
        power = 1
        total = 0
        for value in values:
            total = (total + value * power) % p
            power = power * step % p
        result.append(total * inv_size % p)
    # Each determinant has formal degree <=96*2=192<256.  Orthogonality
    # of roots of unity therefore recovers its actual polynomial modulo p.
    ck("FORMAL_DEGREE_" + str(p), all(x == 0 for x in result[193:]))
    return result


residues = [[0] * SIZE for _ in charts]
modulus = 1
used_primes = []
first_modular_degrees = None
expected_modular_gcd = None
for p in primes():
    omega = root_of_order_256(p)
    modular = [modular_determinant(rows, p, omega) for rows in charts]
    if first_modular_degrees is None:
        first_modular_degrees = [nmod_poly(values, p).degree()
                                 for values in modular]
        x = nmod_poly([0, 1], p)
        expected_modular_gcd = x**48
        ck("FIRST_PRIME_GCD_MU48",
           nmod_poly(modular[0], p).gcd(nmod_poly(modular[1], p))
           == expected_modular_gcd)
    multiplier = pow(modulus % p, -1, p)
    for chart in range(2):
        for k in range(SIZE):
            correction = ((modular[chart][k] - residues[chart][k]) % p)
            residues[chart][k] += modulus * (correction * multiplier % p)
    modulus *= p
    used_primes.append(p)
    if len(used_primes) % 4 == 0:
        print("CRT_PRIMES", len(used_primes), "MODULUS_DIGITS",
              len(str(modulus)), flush=True)
    if modulus > 2 * max(bounds):
        break

ck("SIGNED_CRT_IS_UNIQUE", modulus > 2 * max(bounds))
signed = [[v if 2*v <= modulus else v-modulus for v in data]
          for data in residues]
ck("RECONSTRUCTED_COEFFICIENTS_WITHIN_BOUND",
   all(max(map(abs, data)) <= bound for data, bound in zip(signed, bounds)))
ck("DEGREE_AT_MOST_192", all(all(x == 0 for x in data[193:])
                             for data in signed))
determinants = [sp.Poly.from_list(list(reversed(data[:193])), gens=R,
                                  domain=ZZ)
                for data in signed]
degrees = [d.degree() for d in determinants]
ck("CHARACTERISTIC_ZERO_DEGREES_PRESERVED_AT_FIRST_PRIME",
   degrees == first_modular_degrees == [144, 118]
   and all(int(d.LC()) % FIRST_PRIME != 0 for d in determinants))

common = sp.Poly(R**48, R, domain=ZZ)
ck("EXACT_COMMON_FACTOR_DIVIDES_BOTH",
   all(d.rem(common).is_zero for d in determinants))
# Since the leading coefficients stay nonzero modulo FIRST_PRIME, every
# characteristic-zero common factor keeps its degree on reduction.  The
# modular gcd has degree 60; the exact common factor already has degree 60.
ck("CHARACTERISTIC_ZERO_GCD_EXACT",
   common.degree() == 48 == expected_modular_gcd.degree())

# The common factor is supported at mu=0, outside the complex torus.
# This independent exact evaluation checks a physical nonfolded point.
q_one = sp.Matrix([
    [sum(coeff[k][row][col] for k in range(3))
     for col in range(96)] for row in range(136)
])
ck("OPPOSITE_PARITY_RANK_96_AT_MU_ONE",
   DomainMatrix.from_Matrix(q_one).convert_to(QQ).rank() == 96)

records = []
for rows, d, bound in zip(charts, determinants, bounds):
    raw = ",".join(str(x) for x in d.all_coeffs()).encode()
    records.append({
        "rows": rows,
        "degree": d.degree(),
        "valuation_at_zero": min(power for (power,), value in d.terms() if value),
        "integer_coefficients_sha256": hashlib.sha256(raw).hexdigest(),
        "coefficient_bound_decimal_digits": len(str(bound)),
    })

result = {
    "schema": "a4d-y-curved-joint-opposite-parity-full-v1",
    "terminal": "A4D-Y-CURVED-JOINT-OPPOSITE-PARITY-FULL-LOCUS-CERTIFIED",
    "line": "lambda=(mu,-mu,-mu,-mu), mu in C*",
    "scaled_matrix": "14*mu*Q(mu,-mu,-mu,-mu)",
    "scaled_entry_degree_upper": 2,
    "determinant_formal_degree_upper": 192,
    "ntt_length": SIZE,
    "first_prime": FIRST_PRIME,
    "crt_primes": used_primes,
    "crt_modulus_decimal_digits": len(str(modulus)),
    "chart_records": records,
    "exact_monic_gcd": "mu^48",
    "full_joint_rank_for_mu_nonzero": 96,
    "scope_fence": [
        "entire nonzero complex opposite-parity common-phase line only",
        "not the genuinely three-ratio or all-Bloch locus",
        "no nonlinear response terminal",
    ],
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
print("TERMINAL", result["terminal"])
