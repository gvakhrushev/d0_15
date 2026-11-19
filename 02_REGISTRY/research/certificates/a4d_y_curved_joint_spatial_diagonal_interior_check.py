#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=600
"""Characteristic-zero interior rank locus on the spatial-diagonal ratio line.

For lambda=(1,r,r,r), r in C*, the 68 phase-1/2 joint rows have rank 68
except at r=1 (rank 65) and r=4/21 (rank 67). Two exact 68x68 minors
have gcd r**45*(r-1)**3*(r-4/21) after clearing Laurent powers. The full
136x96 joint operator has rank 96 at r=4/21: boundary rows rescue the
additional interior rank drop. This is only a one-dimensional stratum.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_joint_rational_stencil as S

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_curved_joint_spatial_diagonal_interior_results.json"
r = sp.symbols("r")
INTERIOR = list(range(24, 72)) + list(range(106, 126))
COLUMNS = [
    (list(range(18)) + list(range(24, 53)) + list(range(54, 59)) +
     list(range(60, 63)) + list(range(72, 77)) + list(range(78, 86))),
    (list(range(17)) + [18] + list(range(24, 68)) +
     [78, 79, 80, 81, 82, 84]),
]


def ck(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


# For lambda0=1 and lambda1=lambda2=lambda3=r, every Laurent monomial is
# r**k with k in {-1,0,1}. Multiplication of the entire operator by r is
# invertible on C*, and gives a polynomial matrix of entry degree <=2.
Qpoly = sp.zeros(136, 96)
degree_ok = True
for terms, offset in ((S.ATERMS, 0), (S.QTERMS, 96)):
    for shift, entries in terms.items():
        exponent = sum(shift[1:])
        degree_ok &= exponent in (-1, 0, 1)
        for (row, col), value in entries.items():
            Qpoly[offset + row, col] += (
                sp.Rational(value.numerator, value.denominator)
                * r**(exponent + 1)
            )
ck("LAURENT_CLEARING_DEGREE_TWO", degree_ok)
I = Qpoly.extract(INTERIOR, range(96))
ck("INTERIOR_SHAPE", I.shape == (68, 96))

minors = []
records = []
for j, columns in enumerate(COLUMNS):
    ck("CHART_" + str(j) + "_COLUMNS", len(columns) == len(set(columns)) == 68)
    D = sp.Poly(I.extract(range(68), columns).det(method="domain-ge"), r, domain=QQ)
    ck("CHART_" + str(j) + "_NONZERO", not D.is_zero and D.eval(2) != 0)
    minors.append(D)
    denominator, integral = D.clear_denoms(convert=True)
    content, primitive = integral.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    ledger = ",".join(str(c) for c in primitive.all_coeffs()).encode()
    records.append({
        "columns": columns,
        "degree": D.degree(),
        "lowest_exponent": min(power for (power,), coefficient in D.terms() if coefficient),
        "primitive_integer_coefficients_sha256": hashlib.sha256(ledger).hexdigest(),
    })

common = sp.gcd(minors[0], minors[1]).monic()
expected = sp.Poly(r**45*(r-1)**3*(r-sp.Rational(4, 21)), r, domain=QQ)
ck("EXACT_CHARACTERISTIC_ZERO_GCD", common == expected)
ck("INTERIOR_RANK_AT_ONE", DomainMatrix.from_Matrix(I.subs(r, 1)).convert_to(QQ).rank() == 65)
exception = sp.Rational(4, 21)
ck("INTERIOR_RANK_AT_FOUR_OVER_21",
   DomainMatrix.from_Matrix(I.subs(r, exception)).convert_to(QQ).rank() == 67)
ck("BOUNDARY_RESCUES_FOUR_OVER_21",
   DomainMatrix.from_Matrix(Qpoly.subs(r, exception)).convert_to(QQ).rank() == 96)
ck("FULL_JOINT_FOLDED_RANK95",
   DomainMatrix.from_Matrix(Qpoly.subs(r, 1)).convert_to(QQ).rank() == 95)

result = {
    "schema": "a4d-y-curved-joint-spatial-diagonal-interior-v1",
    "terminal": "A4D-Y-CURVED-JOINT-SPATIAL-DIAGONAL-INTERIOR-LOCUS-CERTIFIED",
    "stratum": "lambda=(1,r,r,r), r in C*",
    "interior_shape": [68, 96],
    "cleared_polynomial_entry_degree_upper": 2,
    "minor_records": records,
    "exact_monic_gcd": "r^45*(r-1)^3*(r-4/21)",
    "interior_rank_generic": 68,
    "interior_rank_at_r_eq_one": 65,
    "interior_rank_at_r_eq_four_over_21": 67,
    "full_joint_rank_at_r_eq_four_over_21": 96,
    "full_joint_rank_at_r_eq_one": 95,
    "unit_circle_implication": "the only interior rank drop on this line with |r|=1 is r=1",
    "scope_fence": [
        "one spatial-diagonal ratio line, not all three ratios",
        "4/21 is a nonphysical complex-torus interior rank drop rescued by boundary rows",
        "no all-Bloch or nonlinear response terminal",
    ],
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
print("TERMINAL", result["terminal"])
