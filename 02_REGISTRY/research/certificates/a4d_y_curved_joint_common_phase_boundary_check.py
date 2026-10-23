#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact full-joint rank on the entire nonzero common-phase character line.

Use the literal rational Laurent stencil and zone folding
lambda_j=mu, w=mu**4. The phase-1/2 rows are independent of w and have
rank 65. Their 31-dimensional right kernel reduces the remaining rows to
a one-variable polynomial matrix. Two exact 31x31 minors have gcd
w**23*(w-1), so the only rank drop for mu in C* is mu**4=1.
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
OUT = HERE / "a4d_y_curved_joint_common_phase_boundary_results.json"


def ck(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def row_phase(row: int) -> int:
    return row // 24 if row < 96 else (row - 96) // 10


w = sp.symbols("w")
T = {k: sp.zeros(136, 96) for k in (-1, 0, 1)}
zone_integral = True
wrap_in_range = True
for terms, offset in ((S.ATERMS, 0), (S.QTERMS, 96)):
    for d, entries in terms.items():
        for (r, c), value in entries.items():
            row = offset + r
            exponent = row_phase(row) - c // 24 + sum(d)
            zone_integral &= exponent % 4 == 0
            k = exponent // 4
            wrap_in_range &= k in T
            if k not in T:
                raise AssertionError(("ZONE_WRAP_OUT_OF_RANGE", d, row, c, k))
            T[k][row, c] += sp.Rational(value.numerator, value.denominator)
ck("ZONE_EXPONENT_DIVISIBLE_BY_FOUR", zone_integral)
ck("ZONE_WRAP_IN_RANGE", wrap_in_range)

interior = list(range(24, 72)) + list(range(106, 126))
boundary = [r for r in range(136) if r not in interior]
ck("PHASE_INTERIOR_HAS_NO_WRAP",
   T[-1].extract(interior, range(96)) == sp.zeros(68, 96) and
   T[1].extract(interior, range(96)) == sp.zeros(68, 96))
I = T[0].extract(interior, range(96))
IDM = DomainMatrix.from_Matrix(I).convert_to(QQ)
ck("INTERIOR_RANK65", IDM.rank() == 65)
N = IDM.nullspace().to_Matrix().T
ck("INTERIOR_KERNEL_DIM31", N.shape == (96, 31) and I*N == sp.zeros(68, 31))

# Q_hat(w) = w^-1 T[-1] + T[0] + w T[1]. On C* we multiply it by w,
# leaving the common zero-set unchanged. The matrices below are the boundary
# rows of w Q_hat(w) restricted to ker I.
P = (T[-1] + w*T[0] + w*w*T[1]).extract(boundary, range(96))*N
ck("BOUNDARY_REDUCTION_SHAPE", P.shape == (68, 31))

ROWSETS = [
    (0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
     72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88),
    (72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
     87, 88, 89, 90, 91, 92, 93, 94, 97, 98, 100, 101, 102, 103, 6, 7),
]
records = []
minors = []
for index, rows in enumerate(ROWSETS):
    ck("BOUNDARY_ROWSET_" + str(index), len(rows) == len(set(rows)) == 31 and
       set(rows).issubset(boundary))
    sub = P.extract([boundary.index(r) for r in rows], range(31))
    polynomial = sp.Poly(sub.det(method="domain-ge"), w, domain=QQ)
    ck("NONZERO_BOUNDARY_MINOR_" + str(index), not polynomial.is_zero and
       polynomial.eval(2) != 0)
    minors.append(polynomial)
    denom, integral = polynomial.clear_denoms(convert=True)
    content, primitive = integral.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    coefficient_bytes = ",".join(str(c) for c in primitive.all_coeffs()).encode()
    records.append({
        "boundary_rows": list(rows),
        "degree": polynomial.degree(),
        "lowest_exponent": min(k for (k,), v in polynomial.terms() if v),
        "primitive_integer_coefficients_sha256": hashlib.sha256(coefficient_bytes).hexdigest(),
    })

gcd = sp.gcd(minors[0], minors[1]).monic()
expected = sp.Poly(w**23*(w-1), w, domain=QQ)
ck("EXACT_CHARACTERISTIC_ZERO_GCD", gcd == expected)

# At w=1 the reduced boundary kernel is one-dimensional, hence total rank
# 65+30=95; elsewhere on C* one of the two minors is nonzero, so the total
# rank is 65+31=96. The row/column phase rescalings by mu are invertible.
boundary_at_fold = P.subs(w, 1)
ck("FOLDED_BOUNDARY_RANK30",
   DomainMatrix.from_Matrix(boundary_at_fold).convert_to(QQ).rank() == 30)
ck("FOLDED_FULL_JOINT_RANK95",
   DomainMatrix.from_Matrix(T[-1]+T[0]+T[1]).convert_to(QQ).rank() == 95)

result = {
    "schema": "a4d-y-curved-joint-common-phase-boundary-v1",
    "terminal": "A4D-Y-CURVED-JOINT-COMMON-PHASE-BOUNDARY-CERTIFIED",
    "line": "lambda0=lambda1=lambda2=lambda3=mu in C*",
    "folded_variable": "w=mu^4",
    "interior_rows": 68,
    "interior_rank": 65,
    "interior_kernel_dimension": 31,
    "boundary_reduced_shape": [68, 31],
    "minor_records": records,
    "exact_monic_gcd": "w^23*(w-1)",
    "rank_at_mu4_eq_one": 95,
    "rank_at_mu4_ne_one": 96,
    "scope_fence": [
        "entire nonzero common-phase complex line only",
        "not a genuinely three-ratio or all-Bloch locus theorem",
        "no nonlinear reduced-center or uniform response conclusion",
    ],
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
print("TERMINAL", result["terminal"])
