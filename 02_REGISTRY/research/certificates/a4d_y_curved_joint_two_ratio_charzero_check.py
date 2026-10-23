#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Characteristic-zero elimination for the four owned two-ratio minors.

Consume the exact integer coefficient ledger reconstructed by the separate
integer-minors owner.  Do not infer a characteristic-zero gcd from agreement
at several primes.  Instead certify an exact structural divisor, preserve the
degree of one resultant, and apply the primitive-gcd reduction lemma proved in
A4D_Y_CURVED_JOINT_TWO_RATIO_CHARACTERISTIC_ZERO.md.

The full, large integer resultants need not be reconstructed: local rational
Schur jets prove their x=1 orders, assignment bounds prove their x=0 orders,
and a rational null pairing at infinity bounds the first resultant degree.
One exact finite-field resultant/gcd then supplies the degree upper bound for
the common characteristic-zero gcd.  All arithmetic is exact.
"""
from __future__ import annotations

import hashlib
import json
import math
from math import comb
from pathlib import Path

from flint import fmpq_mat, fmpq_poly, fmpz_mpoly_ctx, fmpz_poly, nmod_mpoly_ctx
import sympy as sp

import a4d_y_curved_joint_rational_stencil as S

HERE = Path(__file__).resolve().parent
INPUT = HERE / "a4d_y_curved_joint_two_ratio_integer_minors_results.json"
OUT = HERE / "a4d_y_curved_joint_two_ratio_charzero_results.json"
PRIME = 664448401
LEDGER_HASHES = (
    "dfa19c5fe9b8d64b0275e250d05200867b682940ca2bf8d7f3fe2134fc8331d6",
    "8b59dbe61d56795b3e6db6a8c5130b89766f048dd16aa201c99486b7d8cccadb",
    "a901545b12fe72e0f78e13adff65e8c8ab247763040161374129666de5baf0e2",
    "e57acee20376a49d4be68292b81bf6ea4349f0b4ed5fc4e06e9f847b21eb47fd",
)


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def assignment_dual(cost):
    """Integer Hungarian duals; every used inequality is replayed below."""
    n = len(cost)
    infinity = 10**12
    u, v, p, way = ([0] * (n + 1) for _ in range(4))
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv, used = [infinity] * (n + 1), [False] * (n + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], infinity, 0
            for j in range(1, n + 1):
                if used[j]:
                    continue
                cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                if cur < minv[j]:
                    minv[j], way[j] = cur, j0
                if minv[j] < delta:
                    delta, j1 = minv[j], j
            if delta >= infinity:
                raise AssertionError("NO_PERFECT_MATCHING")
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if not p[j0]:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if not j0:
                break
    return u[1:], v[1:]


def sylvester_entries(A, B):
    """Fixed y degrees; entries are sparse integer polynomials in x."""
    m, n = int(A.degrees()[1]), int(B.degrees()[1])
    size = m + n
    entries = [[{} for _ in range(size)] for _ in range(size)]
    for offset, count, P, degree in ((0, n, A, m), (n, m, B, n)):
        coeffs = [dict() for _ in range(degree + 1)]
        for (a, b), c in P.to_dict().items():
            coeffs[degree - int(b)][int(a)] = int(c)
        for row in range(count):
            for col, C in enumerate(coeffs):
                entries[offset + row][row + col] = C
    return entries


def entry_dual(entries):
    cost = [[min(C) if C else 10**6 for C in row] for row in entries]
    u, v = assignment_dual(cost)
    ck("INTEGER_DUAL_INEQUALITIES", all(
        a >= u[r] + v[c]
        for r, row in enumerate(entries) for c, C in enumerate(row) for a in C
    ))
    return u, v


def pivot_columns(M):
    R, rank = M.rref()
    return [next(c for c in range(M.ncols()) if R[r, c]) for r in range(rank)]


def submatrix(M, rows, cols):
    return fmpq_mat([[M[r, c] for c in cols] for r in rows])


def series_inverse(P, precision):
    Q = fmpq_poly([1 / P[0]])
    size = 1
    while size < precision:
        size = min(2 * size, precision)
        Q = Q.mul_low(fmpq_poly([2]) - P.mul_low(Q, size), size)
    if P.mul_low(Q, precision) != fmpq_poly([1]):
        raise AssertionError("SERIES_INVERSE_REPLAY")
    return Q


def series_pivot_orders(M, precision):
    """Exact local determinant order when every pivot order is < precision.

    Pick a minimum-valuation pivot t^v U.  The elimination ratio is known
    mod t^(precision-v), and every pivot-row entry has valuation >= v, so
    each updated entry remains correct mod t^precision.  Nonzero leading
    pivot coefficients then determine the exact determinant valuation.
    """
    size = len(M)
    orders = []
    for k in range(size):
        def valuation(P):
            return next((j for j in range(len(P)) if P[j]), precision)
        v, row, col = min(
            (valuation(M[r][c]), r, c)
            for r in range(k, size) for c in range(k, size)
        )
        if v == precision:
            raise AssertionError("INSUFFICIENT_LOCAL_PRECISION")
        M[k], M[row] = M[row], M[k]
        if col != k:
            for r in range(size):
                M[r][k], M[r][col] = M[r][col], M[r][k]
        orders.append(v)
        inverse = series_inverse(M[k][k].right_shift(v), precision - v)
        for r in range(k + 1, size):
            if not M[r][k]:
                continue
            ratio = M[r][k].right_shift(v).mul_low(inverse, precision - v)
            for c in range(k + 1, size):
                M[r][c] = (M[r][c] - ratio.mul_low(M[k][c], precision)).truncate(precision)
            M[r][k] = fmpq_poly([])
    return orders


def local_schur_orders(entries, precision=9):
    """Schur complement over Q[[t]], x=1+t, of a constant invertible block."""
    size = len(entries)
    matrices = [fmpq_mat([
        [sum(value * comb(a, k) for a, value in C.items() if a >= k) for C in row]
        for row in entries
    ]) for k in range(precision)]
    cols = pivot_columns(matrices[0])
    rows = pivot_columns(matrices[0].transpose())
    rank = len(cols)
    rest_cols = [c for c in range(size) if c not in cols]
    rest_rows = [r for r in range(size) if r not in rows]
    aa = [submatrix(M, rows, cols) for M in matrices]
    bb = [submatrix(M, rows, rest_cols) for M in matrices]
    cc = [submatrix(M, rest_rows, cols) for M in matrices]
    dd = [submatrix(M, rest_rows, rest_cols) for M in matrices]
    inverse = aa[0].inv()
    solutions, reduced = [], []
    for k in range(precision):
        rhs = bb[k]
        for j in range(1, k + 1):
            rhs = rhs - aa[j] * solutions[k - j]
        solutions.append(inverse * rhs)
        # Independent coefficient replay of A(t) X(t)=B(t).
        replay = fmpq_mat(rank, size - rank)
        for j in range(k + 1):
            replay = replay + aa[j] * solutions[k - j]
        if replay != bb[k]:
            raise AssertionError("SCHUR_SOLVE_REPLAY")
        E = dd[k]
        for j in range(k + 1):
            E = E - cc[j] * solutions[k - j]
        reduced.append(E)
    ck("SCHUR_CONSTANT_ZERO", not any(reduced[0].entries()))
    small = [[fmpq_poly([E[r, c] for E in reduced])
              for c in range(size - rank)] for r in range(size - rank)]
    return rank, series_pivot_orders(small, precision)


def one_dimensional_null(M):
    R, rank = M.rref()
    size = M.ncols()
    ck("NULLITY_ONE", rank == size - 1)
    pivots = [next(c for c in range(size) if R[r, c]) for r in range(rank)]
    free = next(c for c in range(size) if c not in pivots)
    out = [0] * size
    out[free] = 1
    for r, c in enumerate(pivots):
        out[c] = -R[r, free]
    ck("NULL_VECTOR_REPLAY", not any((M * fmpq_mat([[z] for z in out])).entries()))
    return out


def first_resultant_degree_bound(A, B, entries):
    m, n = int(A.degrees()[1]), int(B.degrees()[1])
    size = m + n
    row_degrees = [int(A.degrees()[0])] * n + [int(B.degrees()[0])] * m
    reversed_entries = [[{row_degrees[r] - a: value for a, value in C.items()}
                         for C in row] for r, row in enumerate(entries)]
    u, v = entry_dual(reversed_entries)
    constant = fmpq_mat([[C.get(u[r] + v[c], 0) for c, C in enumerate(row)]
                         for r, row in enumerate(reversed_entries)])
    derivative = fmpq_mat([[C.get(u[r] + v[c] + 1, 0) for c, C in enumerate(row)]
                           for r, row in enumerate(reversed_entries)])
    left = one_dimensional_null(constant.transpose())
    right = one_dimensional_null(constant)
    pairing = (fmpq_mat([left]) * derivative * fmpq_mat([[z] for z in right]))[0, 0]
    ck("INFINITY_FIRST_DERIVATIVE_ZERO", pairing == 0)
    # Rank size-1 makes adj(constant) a nonzero multiple of right*left.
    # Thus det(constant+t*derivative+...) has zero constant and linear terms.
    bound = sum(row_degrees) - sum(u) - sum(v) - 2
    return bound, {
        "row_degree_sum": sum(row_degrees),
        "assignment_dual_sum": sum(u) + sum(v),
        "constant_rank": constant.rank(),
        "first_derivative_pairing": "0",
        "resultant_degree_upper_bound": bound,
    }


def certify(data):
    ck("LITERAL_STENCIL_HASH", hashlib.sha256(Path(S.__file__).read_bytes()).hexdigest()
       == "d4cf844b027f8cc34540c385b48922f3a5bcfc42cbedf08d5a704cfb7adb0daa")
    ck("INPUT_TERMINAL", data["terminal"] in {
        "A4D-Y-CURVED-JOINT-TWO-RATIO-INTEGER-MINORS-CERTIFIED",
        "A4D-Y-CURVED-JOINT-TWO-RATIO-CHARZERO-LOCUS-CERTIFIED",
    })
    ck("INPUT_FOUR_CHARTS", len(data["records"]) == len(data["charts"]) == 4)
    ctx = fmpz_mpoly_ctx.get(("x", "y"), "lex")
    polys = []
    contents = []
    for i, record in enumerate(data["records"]):
        ledger = record["coefficient_ledger"]
        payload = ";".join(f"{a},{b},{c}" for a, b, c in ledger)
        h = hashlib.sha256(payload.encode()).hexdigest()
        ck("EXACT_LEDGER_HASH_" + str(i), h == record["coefficient_ledger_sha256"] == LEDGER_HASHES[i])
        ck("CRT_MODULUS_" + str(i),
           math.prod(record["crt_primes"]) == int(record["crt_modulus"]) > 2 * int(record["coefficient_bound"]))
        ax = min(a for a, b, c in ledger)
        bx = min(b for a, b, c in ledger)
        content, P = ctx.from_dict({(a - ax, b - bx): c for a, b, c in ledger}).primitive()
        contents.append(int(content))
        polys.append(P)
    ck("EXACT_CHART_DEGREES", [P.degrees() for P in polys] == [(40, 34), (38, 38), (43, 40), (37, 36)])

    # The two specializations are independent exact univariate Z-gcd controls.
    fiber_gcds = {}
    for fixed_axis, variable in ((0, "y"), (1, "x")):
        common = None
        for P in polys:
            degree = P.degrees()[1 - fixed_axis]
            coeffs = [0] * (degree + 1)
            for ab, value in P.to_dict().items():
                coeffs[ab[1 - fixed_axis]] += int(value)
            F = fmpz_poly(coeffs)
            common = F if common is None else common.gcd(F)
        common = common / common.leading_coefficient()
        ck("EXACT_FIBER_" + variable.upper(), common == fmpq_poly([-1, 3, -3, 1]))
        fiber_gcds["x_equals_1" if fixed_axis == 0 else "y_equals_1"] = f"({variable}-1)^3"

    entries = [sylvester_entries(polys[i], polys[j]) for i, j in ((0, 1), (2, 3))]
    pair_records = []
    for index, E in enumerate(entries):
        u, v = entry_dual(E)
        order_zero_lower = sum(u) + sum(v)
        ck("X_ZERO_ORDER_" + str(index), order_zero_lower == (229, 259)[index])
        rank, orders = local_schur_orders(E)
        ck("EXACT_LOCAL_PIVOTS_" + str(index), orders == ([1, 2, 3, 5], [3, 5, 7])[index])
        ck("STRUCTURAL_DIVISOR_" + str(index), order_zero_lower >= 229 and sum(orders) >= 11)
        pair_records.append({
            "pair": [[0, 1], [2, 3]][index],
            "sylvester_size": len(E),
            "x_zero_order_lower_bound": order_zero_lower,
            "x_one_constant_rank": rank,
            "x_one_schur_pivot_orders": orders,
            "x_one_resultant_order": sum(orders),
        })

    degree_bound, infinity_record = first_resultant_degree_bound(polys[0], polys[1], entries[0])
    ck("EXACT_FIRST_RESULTANT_DEGREE_BOUND", degree_bound == 2576)
    ck("GOOD_PRIME", sp.isprime(PRIME) and all(content % PRIME for content in contents))
    modctx = nmod_mpoly_ctx.get(names=("x", "y"), ordering="lex", modulus=PRIME)
    modpolys = [modctx.from_dict({ab: int(c) % PRIME for ab, c in P.to_dict().items()}) for P in polys]
    ck("Y_DEGREES_PRESERVED", [P.degrees() for P in modpolys] == [P.degrees() for P in polys])
    resultants = [modpolys[i].resultant(modpolys[j], "y") for i, j in ((0, 1), (2, 3))]
    ck("MODULAR_RESULTANT_DEGREES", [R.degrees()[0] for R in resultants] == [2576, 2742])
    ck("FIRST_RESULTANT_DEGREE_PRESERVED", resultants[0].degrees()[0] == degree_bound)
    x, _ = modctx.gens()
    D = x**229 * (x - 1)**11
    ck("MODULAR_GCD_EXACT_STRUCTURAL_DIVISOR", resultants[0].gcd(resultants[1]) == D)
    ck("MODULAR_RESIDUAL_COPRIMENESS", (resultants[0] // D).gcd(resultants[1] // D).is_one())

    # The actual 68-row interior operator, rather than only the four selected
    # minors, has rank 65 at the surviving point.
    center = [[0 for _ in range(96)] for _ in range(68)]
    for E in S.ATERMS.values():
        for (row, col), value in E.items():
            if 24 <= row < 72:
                center[row - 24][col] += value
    for E in S.QTERMS.values():
        for (row, col), value in E.items():
            if 10 <= row < 30:
                center[row + 38][col] += value
    center_rank = fmpq_mat([[str(value) for value in row] for row in center]).rank()
    ck("EXACT_INTERIOR_CENTER_RANK_65", center_rank == 65)

    # Hostile controls: degree preservation does not identify the factor unless
    # the proposed structural divisor is proved over Z; and missing degree
    # preservation can hide a nonconstant common factor completely.
    xx = sp.symbols("xx")
    primes = (664448401, 996672601, 1328896801)
    bad = sp.Poly(xx - 1 - math.prod(primes), xx)
    bad2 = bad * sp.Poly(xx + 2, xx)
    ck("THREE_PRIME_AGREEMENT_NEGATIVE_CONTROL", all(
        sp.gcd(sp.Poly(bad.as_expr(), xx, modulus=p),
               sp.Poly(bad2.as_expr(), xx, modulus=p)).monic() == sp.Poly(xx - 1, xx, modulus=p)
        for p in primes
    ) and bad.eval(1) != 0)
    hidden = sp.Poly(PRIME * xx + 1, xx)
    ck("MISSING_DEGREE_PRESERVATION_NEGATIVE_CONTROL",
       hidden.degree() == 1 and sp.Poly(hidden.as_expr(), xx, modulus=PRIME).degree() == 0)
    ck("LOCAL_SERIES_CANCELLATION_CONTROL", series_pivot_orders([
        [fmpq_poly([0, 0, 1]), fmpq_poly([0, 0, 0, 1])],
        [fmpq_poly([0, 0, 0, 0, 1]), fmpq_poly([0, 0, 0, 0, 0, 1, 0, 1])],
    ], 9) == [2, 7])
    try:
        series_pivot_orders([[fmpq_poly([])]], 9)
    except AssertionError as error:
        ck("LOCAL_SERIES_INSUFFICIENT_PRECISION_CONTROL",
           str(error) == "INSUFFICIENT_LOCAL_PRECISION")
    else:
        raise AssertionError("UNOBSERVED_LOCAL_PIVOT_ACCEPTED")

    result = {
        "schema": "a4d-y-curved-joint-two-ratio-charzero-v1",
        "terminal": "A4D-Y-CURVED-JOINT-TWO-RATIO-CHARACTERISTIC-ZERO-ELIMINATION-CERTIFIED",
        "ratio_plane": "rho0=1, rho1=x, rho2=y, rho3=1",
        "integer_minor_owner": INPUT.name,
        "literal_stencil_sha256": "d4cf844b027f8cc34540c385b48922f3a5bcfc42cbedf08d5a704cfb7adb0daa",
        "coefficient_ledger_sha256": list(LEDGER_HASHES),
        "primitive_chart_degrees": [[int(d) for d in P.degrees()] for P in polys],
        "resultant_local_data": pair_records,
        "first_resultant_infinity_certificate": infinity_record,
        "good_prime": PRIME,
        "modular_resultant_degrees": [int(R.degrees()[0]) for R in resultants],
        "characteristic_zero_monic_resultant_gcd": "x^229*(x-1)^11",
        "exact_coordinate_fibers": fiber_gcds,
        "four_minors_common_zero_set_in_complex_torus": "(x,y)=(1,1)",
        "interior_rank_at_center": center_rank,
        "interior_rank_elsewhere_on_plane": 68,
        "scope_fence": [
            "exact characteristic-zero theorem on this representative two-ratio plane",
            "does not classify the genuine three-ratio interior locus",
            "does not close the remaining boundary rows or all-Bloch gap",
            "does not prove nonlinear reduced-center solvability or normalized response convergence",
        ],
    }
    return result


if __name__ == "__main__":
    result = certify(json.loads(INPUT.read_text()))
    if "--write" in __import__("sys").argv:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT)
    elif OUT.exists():
        ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
    print("TERMINAL", result["terminal"])
