#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact full-joint rank theorem on the spatial-equal physical two-torus.

The S3 module owner reduces the literal 136x96 symbol at
lambda=(mu,mu*r,mu*r,mu*r) to trivial/sign/standard-swap-minus blocks of
16/16/32 columns. Two exact determinant charts per block, one univariate
resultant, reciprocal-polynomial gcds, and three exact line-gcd controls
prove rank 96 on |mu|=|r|=1 except the four folded points of rank 95.
No finite character grid, floating singular value, or complex-surface
extrapolation is used.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from flint import fmpz_poly
import numpy as np
import sympy as sp
from sympy.polys.domains import QQ, QQ_I, ZZ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_joint_spatial_equal_s3_check as S3
import a4d_y_curved_joint_rational_stencil as S

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_curved_joint_spatial_equal_torus_results.json"
MU, R = sp.symbols("mu r")
COEFF = S3.coeff
BASES = S3.bases

SMALL_CONNECTION = [0, 3, 6, 7, 8, 9, 10, 11,
                    24, 27, 30, 31, 32, 33, 34, 35]
SMALL_METRIC = [96, 97, 100, 101, 106, 107, 110, 111,
                3, 6, 7, 8, 9, 10, 30, 31]
STANDARD_CONNECTION = [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13,
                       14, 15, 16, 17, 24, 25, 27, 28, 30, 31,
                       32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
STANDARD_METRIC = [97, 98, 100, 101, 102, 103, 107, 108, 110, 111,
                   112, 113, 0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13,
                   14, 15, 16, 17, 24, 25, 27, 28]


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def block_coeff(name):
    return np.einsum("abij,jk->abik", COEFF, BASES[name], optimize=True)


def determinant(block, rows):
    width = block.shape[-1]
    ck("DET_ROWSET_%d" % width, len(rows) == width and len(set(rows)) == width)
    matrix = sp.Matrix([
        [sum(int(block[a, b, row, col]) * MU**a * R**b
             for a in range(3) for b in range(3))
         for col in range(width)] for row in rows
    ])
    return DomainMatrix.from_Matrix(matrix).convert_to(
        ZZ.poly_ring(MU, R)).det().as_expr()


def primitive_reciprocal_gcd_degree(poly, x):
    polynomial = sp.Poly(poly, x).primitive()[1]
    coeff = [int(polynomial.nth(j)) for j in range(polynomial.degree() + 1)]
    return fmpz_poly(coeff).gcd(fmpz_poly(list(reversed(coeff)))).degree()


sign = block_coeff("sign")
trivial = block_coeff("trivial")
standard = block_coeff("standard_swap_minus")

# The two 16-column charts. An exact common quarter-phase rotation
# interchanges the trivial and sign determinant charts.
sign_connection = determinant(sign, SMALL_CONNECTION)
sign_metric = determinant(sign, SMALL_METRIC)
trivial_connection = determinant(trivial, SMALL_CONNECTION)
trivial_metric = determinant(trivial, SMALL_METRIC)
ck("TRIVIAL_CONNECTION_QUARTER_ROTATION",
   sp.Poly(trivial_connection - sign_connection.subs(MU, sp.I*MU),
           MU, R).is_zero)
ck("TRIVIAL_METRIC_QUARTER_ROTATION",
   sp.Poly(trivial_metric + sign_metric.subs(MU, sp.I*MU),
           MU, R).is_zero)

connection_factors = sp.factor_list(sign_connection)[1]
large = sorted(
    [f for f, multiplicity in connection_factors
     if sp.Poly(f, MU, R).degree(MU) == 8],
    key=lambda f: int(sp.Poly(f, MU, R).coeff_monomial(MU**8*R**4)))
ck("SIGN_CONNECTION_TWO_DEGREE_8_4_FACTORS",
   len(large) == 2 and all(
       sp.Poly(f, MU, R).degree(R) == 4 for f in large)
   and [int(sp.Poly(f, MU, R).coeff_monomial(MU**8*R**4))
        for f in large] == [9, 49])
F = large[0]
F_reverse = large[1]
ck("SIGN_CONNECTION_RECIPROCAL_FACTORS",
   sp.Poly(F_reverse - MU**8 * R**4 * F.subs(
       {MU: 1/MU, R: 1/R}), MU, R).is_zero)
ck("SIGN_CONNECTION_COMPLETE_FACTOR",
   sp.Poly(sign_connection - 377801998336 * MU**8 * R**12
           * F * F_reverse, MU, R).is_zero)

metric_factors = (MU**12 * R**13 * (MU**2 + 1)
                  * (3*MU**2*R + R + 2)
                  * (8*MU**2*R - MU**2 + 7)
                  * (R-1)**2 * (MU**2*R**2 + 1))
ck("SIGN_METRIC_COMPLETE_FACTOR",
   sp.Poly(sign_metric + 9139785943744512 * metric_factors,
           MU, R).is_zero)

# On the unit torus, the two nontrivial metric factors above vanish only
# at (MU^2,R)=(-1,1): |3u+1|=2 and |u-7|=8 with |u|=1 both force u=-1.
x = sp.symbols("x", real=True)
ck("SIGN_METRIC_FIRST_UNIT_MODULUS_GATE",
   sp.solve(10+6*x-4, x) == [-1])
ck("SIGN_METRIC_SECOND_UNIT_MODULUS_GATE",
   sp.solve(50-14*x-64, x) == [-1])
ck("SIGN_METRIC_EXCEPTIONAL_R_ONE",
   3*(-1)+1+2 == 0 and 8*(-1)-(-1)+7 == 0)

# If MU^2+1=0, the connection factor restricts to (r-1) times a real
# cubic with no unit root (reciprocal gcd one).
at_i = sp.Poly(F.subs(MU, sp.I), R)
quotient_i, remainder_i = sp.div(at_i, sp.Poly(R-1, R))
ck("SIGN_CONNECTION_AT_I_DIVIDES_R_MINUS_ONE", remainder_i.is_zero)
ck("SIGN_CONNECTION_CUBIC_NO_UNIT_ROOT",
   quotient_i.degree() == 3
   and primitive_reciprocal_gcd_degree(quotient_i, R) == 0
   and sp.Poly(F.subs(MU, -sp.I), R) == at_i)

# If r=1, the remaining quartic factor has no unit root: for |MU|=1,
# |MU^4-1|<=2 whereas |16 MU^2|=16.
at_r_one = sp.Poly(F.subs(R, 1), MU)
quotient_r, remainder_r = sp.div(at_r_one, sp.Poly(MU**4-1, MU))
ck("SIGN_CONNECTION_AT_R_ONE_FOLDED_ONLY",
   remainder_r.is_zero and quotient_r.degree() == 4
   and primitive_reciprocal_gcd_degree(quotient_r, MU) == 0)

# The remaining unit-torus metric factor is MU^2*r^2+1. Its resultant
# with F has only MU=+/-i as possible unit roots; the cubic gate then
# forces r=1. The quotient of the resultant has no reciprocal root.
resultant_sign = sp.Poly(sp.resultant(F, MU**2*R**2+1, R), MU)
quotient_resultant, remainder_resultant = sp.div(
    resultant_sign, sp.Poly(MU**2+1, MU))
ck("SIGN_QUADRATIC_RESULTANT_UNIT_ROOTS",
   remainder_resultant.is_zero and quotient_resultant.degree() == 14
   and primitive_reciprocal_gcd_degree(quotient_resultant, MU) == 0)

# Exact full block ranks at all four folded characters. The quarter
# rotation swaps the trivial and sign center assignment.
folded_ranks = {}
for name, block in (("trivial", trivial), ("sign", sign),
                    ("standard", standard)):
    ranks = []
    for mu in (1, sp.I, -1, -sp.I):
        matrix = sp.zeros(136, block.shape[-1])
        for a in range(3):
            for b in range(3):
                matrix += mu**a * sp.Matrix(block[a, b].tolist())
        ranks.append(DomainMatrix.from_Matrix(matrix).convert_to(QQ_I).rank())
    folded_ranks[name] = ranks
ck("FOLDED_TRIVIAL_SIGN_STANDARD_RANKS",
   folded_ranks == {"trivial": [15, 16, 15, 16],
                    "sign": [16, 15, 16, 15],
                    "standard": [32, 32, 32, 32]})

# The 32-column standard block has one large connection factor F32 and a
# metric factor G12 plus simple lines. Both full determinants are formed
# over Z[mu,r], with no specialization used for their factorization.
standard_connection = determinant(standard, STANDARD_CONNECTION)
standard_metric = determinant(standard, STANDARD_METRIC)
factors_connection = sp.factor_list(standard_connection)[1]
factors_metric = sp.factor_list(standard_metric)[1]
F32s = [f for f, multiplicity in factors_connection
        if sp.Poly(f, MU, R).degree(MU) == 32]
G12s = [f for f, multiplicity in factors_metric
        if sp.Poly(f, MU, R).degree(MU) == 12]
ck("STANDARD_LARGE_FACTOR_DEGREES",
   len(F32s) == len(G12s) == 1
   and sp.Poly(F32s[0], MU, R).degree(R) == 32
   and sp.Poly(G12s[0], MU, R).degree(R) == 12)
F32, G12 = F32s[0], G12s[0]
ck("STANDARD_CONNECTION_COMPLETE_FACTOR",
   sp.Poly(standard_connection - 4593933734501238773365407744
           * MU**16 * R**16 * F32, MU, R).is_zero)
simple_standard = (MU**26 * R**20 * (MU*R-1) * (MU*R+1)
                   * (R+1)**2 * (R-1)**6 * (MU**2*R**2+1))
ck("STANDARD_METRIC_COMPLETE_FACTOR",
   sp.Poly(standard_metric - 2801805344278863070480704979813269504
           * simple_standard * G12, MU, R).is_zero)

# Eliminate r from the two large factors. After removing the excluded
# monomial MU^144, the resultant is P(MU^4), deg P=120. If P has a
# root on the unit circle, its real-coefficient reversal has the same
# root. Their exact integer gcd is one, so this cannot happen.
H = sp.Poly(sp.resultant(F32, G12, R), MU).primitive()[1]
nonzero_terms = {power[0]: int(value) for power, value in H.terms()}
valuation = min(nonzero_terms)
ck("STANDARD_RESULTANT_VALUATION_AND_FOURTH_POWERS",
   valuation == 144 and H.degree() == 624
   and all((power-valuation) % 4 == 0 for power in nonzero_terms))
P_coeff = [nonzero_terms.get(valuation+4*j, 0) for j in range(121)]
P = fmpz_poly(P_coeff)
ck("STANDARD_LARGE_FACTORS_NO_UNIT_INTERSECTION",
   P.degree() == 120
   and P.gcd(fmpz_poly(list(reversed(P_coeff)))).degree() == 0)


def one_variable_line(label, substitution):
    """Two exact standard-block minor charts on a simple complex line."""
    variable = sp.symbols("x")
    orderings = (list(range(136)), list(range(96, 136))+list(range(96)))
    determinants = []
    records = []
    for value, order in zip((2, 3), orderings):
        if substitution == "r=1":
            mu_value, r_value = sp.Rational(value), sp.Integer(1)
            def entry(row, col):
                return sum(int(standard[a, b, row, col]) * variable**a
                           for a in range(3) for b in range(3))
        elif substitution == "r=-1":
            mu_value, r_value = sp.Rational(value), sp.Integer(-1)
            def entry(row, col):
                return sum(int(standard[a, b, row, col]) * (-1)**b
                           * variable**a for a in range(3) for b in range(3))
        else:
            mu_value, r_value = sp.Rational(value), sp.Rational(1, value)
            def entry(row, col):
                return sum(int(standard[a, b, row, col])
                           * variable**(a-b+2)
                           for a in range(3) for b in range(3))
        evaluated = sp.Matrix([
            [sum(int(standard[a, b, row, col])
                 * mu_value**a * r_value**b
                 for a in range(3) for b in range(3))
             for row in order] for col in range(32)
        ])
        _, pivot_columns = DomainMatrix.from_Matrix(
            evaluated).convert_to(QQ).rref()
        ck("LINE_%s_CHART_RANK_%d" % (label, value),
           len(pivot_columns) == 32)
        rows = [order[j] for j in pivot_columns]
        matrix = sp.Matrix([
            [entry(row, col) for col in range(32)] for row in rows
        ])
        determinant_poly = sp.Poly(
            DomainMatrix.from_Matrix(matrix).convert_to(
                ZZ.poly_ring(variable)).det().as_expr(), variable)
        determinants.append(determinant_poly)
        records.append({"rows": rows, "degree": determinant_poly.degree()})
    gcd = sp.gcd(determinants[0], determinants[1]).monic()
    expected_valuation = {"r=1": 12, "r=-1": 16,
                          "mu*r=1": 48}[substitution]
    ck("LINE_%s_EXACT_COMPLEX_GCD_MONOMIAL" % label,
       gcd.degree() == expected_valuation and len(gcd.terms()) == 1
       and gcd.LC() == 1)
    return {"line": substitution, "charts": records,
            "gcd": "x^%d" % expected_valuation}


line_records = [one_variable_line("R_PLUS", "r=1"),
                one_variable_line("R_MINUS", "r=-1"),
                one_variable_line("SPATIAL_ONE", "mu*r=1")]

# Common quarter-phase covariance is coefficientwise exact. The common
# phase diagonal commutes with the 3-cycle, hence preserves the entire
# standard isotypic subspace. It transports the mu*r=1 theorem to all
# four lines mu*r in mu_4, even when it exchanges swap eigenspaces.
for owner, offset in ((S.ATERMS, 0), (S.QTERMS, 96)):
    for shift, entries in owner.items():
        for (row, col), value in entries.items():
            if not value:
                continue
            row_phase = row // 24 if offset == 0 else row // 10
            col_phase = S.LABELS[col][0]
            if (sum(shift) - col_phase + row_phase) % 4:
                raise AssertionError("COMMON_QUARTER_PHASE_COVARIANCE")
ck("COMMON_QUARTER_PHASE_COVARIANCE", True)
ck("QUARTER_PHASE_PRESERVES_STANDARD_ISOTYPIC",
   all(S.LABELS[row][0] == S.LABELS[col][0]
       for row, col in zip(*np.nonzero(S3.cycle))))

result = {
    "schema": "a4d-y-curved-joint-spatial-equal-torus-v1",
    "terminal": "A4D-Y-CURVED-JOINT-SPATIAL-EQUAL-PHYSICAL-TORUS-LOCUS-CERTIFIED",
    "surface": "lambda=(mu,mu*r,mu*r,mu*r), |mu|=|r|=1",
    "rank_off_four_folds": 96,
    "rank_at_four_folds": 95,
    "folded_block_ranks_mu_1_i_minus1_minusi": folded_ranks,
    "sign_connection_factor_bidegree": [8, 4],
    "sign_cubic_reciprocal_gcd_degree": 0,
    "sign_quadratic_resultant_degree": resultant_sign.degree(),
    "standard_connection_factor_bidegree": [32, 32],
    "standard_metric_factor_bidegree": [12, 12],
    "standard_resultant_mu_valuation": valuation,
    "standard_resultant_reduced_w_degree": P.degree(),
    "standard_resultant_reduced_w_coefficients_sha256": hashlib.sha256(
        ",".join(str(value) for value in P_coeff).encode()).hexdigest(),
    "standard_resultant_reciprocal_gcd_degree": 0,
    "standard_simple_line_records": line_records,
    "scope_fence": [
        "continuous two-real-dimensional physical spatial-equal torus",
        "not all three independent spatial ratios or the full four-torus",
        "uniform inverse and nonlinear consequences require a separate argument",
        "no fixed-curved-background normalized response terminal",
    ],
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT, flush=True)
else:
    ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
print("TERMINAL", result["terminal"])
