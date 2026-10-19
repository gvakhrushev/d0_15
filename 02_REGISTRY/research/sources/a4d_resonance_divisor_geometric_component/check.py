#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Candidate geometric components of the owned resonance divisor.

Status of the claim checked here: CANDIDATE. This is not a closure of the
higher-codimension rank stratification.

Owner. The 24x24 matrix A(z) is the connection Hessian rebuilt by the same
face-orientation, generator order, and exp4 second-jet convention as
certificates/a4d_resonance_divisor_counterexample_check.py. The chiral
blocks come from the constant Hodge eigenbasis T on each role, with
det T = 4096 and with both cross-chiral blocks identically zero.

Object. Clearing denominators is unnecessary for the plus block as a
matrix over the Laurent ring: direct expansion of det(A+) over the 2304
support matchings produces a Laurent polynomial whose numerator
P+ = (z0 z1 z2 z3)^3 det(A+) lies in Z[i][z0,z1,z2,z3], has 671 terms,
and has degree at most 6 in each variable. The conjugate block is the
coefficient conjugate. On (C*)^4,
    det A(z) = P+(z) * conjugate(P+)(z) / (4096**2 * (z0 z1 z2 z3)**6).
The coordinate hyperplanes are units on the torus, so the codimension-one
zero set is V(P+) union V(conjugate(P+)).

Absolute irreducibility. The unimodular substitution
z0=u, z1=u+y1, z2=u+y2, z3=u+y3 has leading u^18 coefficient -1024,
independent of the y's. The specialization y2=1, y3=4 therefore preserves
u-degree. Its image H is square-free and the Ruppert/Gao solution space
    f (g_y - h_u) + h f_u - g f_y = 0,
deg_u g <= 17, deg_y g <= deg_y H, deg_u h <= 18, deg_y h <= deg_y H - 1,
has dimension 1 over F_p for two primes p > (2*18-1)*deg_y H with i in F_p.
A nontrivial factor over an algebraic closure would produce a solution
linearly independent from (H_u, H_y), and field extension does not change
matrix rank, so H and hence P+ are absolutely irreducible. Coefficient
conjugation preserves that property and the two factors are nonassociate.
Generic Smith valuation of det(A+) along V(P+) is 1, so the generic rank
of A on that geometric component is 23. The same holds on the conjugate
component.

The refuted count law nullity = 2 max(n_+i, n_-i) predicts 4 at
(-1,-1,i,i) and the exact rank there is 22. That point lies on both
components; it is not a generic point of either.

The nullity >= 2 locus is not settled by this file. stratum_check.py is the
candidate partial certificate: the conjugate intersection is pure dimension 2,
and generic rank 22 is checked on the equal-spatial components and on every
component through (-1,-1,i,i). Still unseen there: the generic rank of every
residual component of V(R, Q), and any Fitting component where one chiral
block has rank at most 10 and avoids (-1,-1,i,i).
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import sympy as sp

PAIR = list(combinations(range(4), 2))
PAIR_INDEX = {pair: i for i, pair in enumerate(PAIR)}
I = sp.I
ETA = sp.diag(1, -1, -1, -1)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIR))
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PAIR_INDEX[dst], PAIR_INDEX[src]] = sign


def boost(j: int) -> sp.Matrix:
    out = sp.zeros(4)
    out[0, j] = out[j, 0] = 1
    return out


def rotation(i: int, j: int) -> sp.Matrix:
    out = sp.zeros(4)
    out[i, j], out[j, i] = 1, -1
    return out


GEN = [boost(1), boost(2), boost(3), rotation(1, 2), rotation(1, 3), rotation(2, 3)]
BASIS = [sp.eye(4)[:, j] for j in range(4)]
AV = sp.symbols("a0:24")
BV = sp.symbols("b0:24")
A_LINKS = [sum((AV[6 * r + j] * GEN[j] for j in range(6)), sp.zeros(4)) for r in range(4)]
B_LINKS = [sum((BV[6 * r + j] * GEN[j] for j in range(6)), sp.zeros(4)) for r in range(4)]


def wedge(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[a] * right[b] - left[b] * right[a] for a, b in PAIR])


def bivector(matrix: sp.Matrix) -> sp.Matrix:
    lowered = matrix * ETA
    return sp.Matrix([lowered[a, b] for a, b in PAIR])


def orientation(face: tuple[int, int]) -> int:
    complement = [j for j in range(4) if j not in face]
    sequence = list(face) + complement
    inversions = sum(sequence[i] > sequence[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def mul4(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[2] * right[0],
        left[0] * right[3] + left[1] * right[2] + left[2] * right[1] + left[3] * right[0],
    )


def exp4(left, right, phase_left=1, phase_right=1, inverse=False):
    sign = -1 if inverse else 1
    return (
        sp.eye(4),
        sign * phase_left * left,
        sign * phase_right * right,
        sp.Rational(1, 2) * phase_left * phase_right * (left * right + right * left),
    )


def curvature_mixed(plaquette):
    return plaquette[3] - sp.Rational(1, 2) * (
        plaquette[1] * plaquette[2] + plaquette[2] * plaquette[1]
    )


def connection_hessian(characters) -> sp.Matrix:
    action = sp.Integer(0)
    for r, s in PAIR:
        plaquette = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
        plaquette = mul4(plaquette, exp4(A_LINKS[r], B_LINKS[r]))
        plaquette = mul4(plaquette, exp4(A_LINKS[s], B_LINKS[s], characters[r], 1 / characters[r]))
        plaquette = mul4(
            plaquette, exp4(A_LINKS[r], B_LINKS[r], characters[s], 1 / characters[s], True)
        )
        plaquette = mul4(plaquette, exp4(A_LINKS[s], B_LINKS[s], inverse=True))
        u, v = [j for j in range(4) if j not in (r, s)]
        area = wedge(BASIS[u], BASIS[v])
        action += orientation((r, s)) * (area.T * G2 * STAR * bivector(curvature_mixed(plaquette)))[0]
    action = sp.expand(action)
    return sp.Matrix(24, 24, lambda i, j: sp.diff(sp.diff(action, AV[i]), BV[j]))


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print("PASS_" + label, flush=True)


def mul_poly(left, right):
    out = {}
    for e1, c1 in left.items():
        for e2, c2 in right.items():
            exp = (e1[0] + e2[0], e1[1] + e2[1], e1[2] + e2[2], e1[3] + e2[3])
            re = c1[0] * c2[0] - c1[1] * c2[1]
            im = c1[0] * c2[1] + c1[1] * c2[0]
            prev = out.get(exp)
            if prev is None:
                if re or im:
                    out[exp] = (re, im)
            else:
                re += prev[0]
                im += prev[1]
                if re or im:
                    out[exp] = (re, im)
                else:
                    del out[exp]
    return out


def gauss_nullity(rows, prime: int) -> int:
    if not rows:
        return 0
    matrix = [row[:] for row in rows]
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    row = 0
    pivots = 0
    for col in range(n_cols):
        pivot = None
        for i in range(row, n_rows):
            if matrix[i][col] % prime:
                pivot = i
                break
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][col], -1, prime)
        matrix[row] = [(value * inverse) % prime for value in matrix[row]]
        for i in range(n_rows):
            factor = matrix[i][col] % prime
            if i != row and factor:
                matrix[i] = [(matrix[i][j] - factor * matrix[row][j]) % prime for j in range(n_cols)]
        pivots += 1
        row += 1
        if row == n_rows:
            break
    return n_cols - pivots


def gao_dimension(polynomial, prime: int) -> tuple[int, int, int]:
    """Dimension of the relaxed Ruppert system over F_prime.

    A factorization over the algebraic closure with both factors of positive
    u-degree and one factor having nonzero u-derivative produces a solution
    independent of (f_u, f_y). Rank is invariant under field extension, so
    dimension 1 forbids such a factorization. Proper powers are excluded
    separately by gcd(f, f_u)=1.
    """
    m = max(exp[0] for exp in polynomial)
    n = max(exp[1] for exp in polynomial)
    f_u = {}
    f_y = {}
    for (eu, ey), coeff in polynomial.items():
        if eu:
            f_u[(eu - 1, ey)] = (f_u.get((eu - 1, ey), 0) + eu * coeff) % prime
        if ey:
            f_y[(eu, ey - 1)] = (f_y.get((eu, ey - 1), 0) + ey * coeff) % prime
    f_u = {key: value for key, value in f_u.items() if value}
    f_y = {key: value for key, value in f_y.items() if value}
    g_keys = [(eu, ey) for eu in range(m) for ey in range(n + 1)]
    h_keys = [(eu, ey) for eu in range(m + 1) for ey in range(n)]
    u_max = 2 * m - 1
    y_max = 2 * n - 1
    monomials = [(eu, ey) for eu in range(u_max + 1) for ey in range(y_max + 1)]
    index = {key: i for i, key in enumerate(monomials)}
    columns = []

    def column_of(term):
        column = [0] * len(monomials)
        for key, value in term.items():
            column[index[key]] = value % prime
        return column

    for eu, ey in g_keys:
        term = {}
        if ey:
            factor = ey % prime
            for (fu, fy), coeff in polynomial.items():
                key = (fu + eu, fy + ey - 1)
                term[key] = (term.get(key, 0) + coeff * factor) % prime
        for (fu, fy), coeff in f_y.items():
            key = (fu + eu, fy + ey)
            term[key] = (term.get(key, 0) - coeff) % prime
        columns.append(column_of(term))
    for eu, ey in h_keys:
        term = {}
        for (fu, fy), coeff in f_u.items():
            key = (fu + eu, fy + ey)
            term[key] = (term.get(key, 0) + coeff) % prime
        if eu:
            factor = eu % prime
            for (fu, fy), coeff in polynomial.items():
                key = (fu + eu - 1, fy + ey)
                term[key] = (term.get(key, 0) - coeff * factor) % prime
        columns.append(column_of(term))
    system = [[columns[col][row] for col in range(len(columns))] for row in range(len(monomials))]
    system = [row for row in system if any(row)]
    return m, n, gauss_nullity(system, prime)


def sqrt_minus_one(prime: int) -> int:
    for base in range(2, prime):
        root = pow(base, (prime - 1) // 4, prime)
        if (root * root) % prime == prime - 1:
            return root
    raise AssertionError("no square root of -1")


def reduce_bivariate(polynomial, prime: int, root: int) -> dict:
    reduced = {}
    for (eu, ey), (re, im) in polynomial.items():
        value = (re + im * root) % prime
        if value:
            reduced[(eu, ey)] = value
    return reduced


def bivariate_from_chart(numerator, y2: int, y3: int) -> dict:
    """Specialize z0=u, z1=u+y, z2=u+y2, z3=u+y3."""
    out = {}

    def add(exp, value):
        if value == (0, 0):
            return
        prev = out.get(exp)
        if prev is None:
            out[exp] = value
            return
        summed = (prev[0] + value[0], prev[1] + value[1])
        if summed == (0, 0):
            del out[exp]
        else:
            out[exp] = summed

    for (a0, a1, a2, a3), (re, im) in numerator.items():
        # u^a0 * (u+y)^a1 * (u+y2)^a2 * (u+y3)^a3
        for i in range(a1 + 1):
            ci = sp.binomial(a1, i)
            for j in range(a2 + 1):
                cj = sp.binomial(a2, j) * (y2 ** j)
                for k in range(a3 + 1):
                    ck = int(ci * cj * sp.binomial(a3, k) * (y3 ** k))
                    eu = a0 + (a1 - i) + (a2 - j) + (a3 - k)
                    add((eu, i), (ck * re, ck * im))
    return out


def chart_leading_coefficient(numerator) -> tuple[int, tuple[int, int]]:
    """Coefficient of u^18 after z=(u, u+y1, u+y2, u+y3), and the max u-degree."""
    coeff = {}
    max_degree = 0
    for (a0, a1, a2, a3), (re, im) in numerator.items():
        degree = a0 + a1 + a2 + a3
        max_degree = max(max_degree, degree)
        # Leading term of each monomial is u^{a0+a1+a2+a3}; y's do not enter it.
        prev = coeff.get(degree)
        if prev is None:
            coeff[degree] = (re, im)
        else:
            coeff[degree] = (prev[0] + re, prev[1] + im)
    coeff = {deg: value for deg, value in coeff.items() if value != (0, 0)}
    top = max(coeff)
    return top, coeff[top]


def main() -> None:
    z = sp.symbols("z0:4")
    owned = connection_hessian(z)
    check("OWNER_SHAPE_AND_96_NONZERO", owned.shape == (24, 24) and sum(value != 0 for value in owned) == 96)

    bivector_matrix = sp.Matrix.hstack(*(bivector(generator) for generator in GEN))
    hodge = bivector_matrix.inv() * STAR * bivector_matrix
    plus_space = (hodge - I * sp.eye(6)).nullspace()
    minus_space = (hodge + I * sp.eye(6)).nullspace()
    t6 = sp.Matrix.hstack(*plus_space, *minus_space)
    change = sp.diag(t6, t6, t6, t6)
    check("CHIRAL_CHANGE_DET_4096", sp.factor(change.det()) == 4096)
    plus_index = [6 * role + j for role in range(4) for j in range(3)]
    minus_index = [6 * role + j for role in range(4) for j in range(3, 6)]
    congruent = change.T * owned * change
    cross = congruent.extract(plus_index, minus_index).applyfunc(sp.cancel)
    check("CHIRAL_CROSS_BLOCKS_ZERO", all(value == 0 for value in cross))
    plus = congruent.extract(plus_index, plus_index).applyfunc(sp.cancel)
    minus = congruent.extract(minus_index, minus_index).applyfunc(sp.cancel)
    check("MINUS_IS_COEFFICIENT_CONJUGATE", minus == plus.xreplace({I: -I}))

    support = []
    parsed = []
    for row in range(12):
        row_support = []
        row_entries = []
        for col in range(12):
            value = sp.together(sp.cancel(plus[row, col]))
            if value == 0:
                row_entries.append(None)
                continue
            numerator, denominator = sp.fraction(value)
            numerator = sp.expand(numerator)
            denominator = sp.expand(denominator)
            num_poly = sp.Poly(numerator, *z, extension=I)
            den_poly = sp.Poly(denominator, *z, extension=I)
            num_dict = {}
            for exp, coeff in num_poly.terms():
                real, imag = sp.expand(coeff).as_real_imag()
                num_dict[tuple(int(part) for part in exp)] = (int(real), int(imag))
            den_monomials = den_poly.monoms()
            check(f"DENOMINATOR_MONOMIAL_{row}_{col}", len(den_monomials) == 1)
            den_leading = sp.expand(den_poly.LC()).as_real_imag()
            check(
                f"DENOMINATOR_UNIT_{row}_{col}",
                int(den_leading[0]) == 1 and int(den_leading[1]) == 0,
            )
            row_support.append(col)
            row_entries.append((num_dict, tuple(int(part) for part in den_monomials[0])))
        support.append(row_support)
        parsed.append(row_entries)
    check("PLUS_SUPPORT_HAS_48_NONZERO", sum(len(cols) for cols in support) == 48)

    accumulated = {}
    matching_count = [0]

    def accumulate(perm, poly, denominator):
        inversions = sum(perm[a] > perm[b] for a in range(12) for b in range(a + 1, 12))
        sign = 1 if inversions % 2 == 0 else -1
        for exp, coeff in poly.items():
            key = tuple(exp[t] - denominator[t] for t in range(4))
            signed = (sign * coeff[0], sign * coeff[1])
            prev = accumulated.get(key)
            if prev is None:
                accumulated[key] = signed
            else:
                summed = (prev[0] + signed[0], prev[1] + signed[1])
                if summed == (0, 0):
                    del accumulated[key]
                else:
                    accumulated[key] = summed
        matching_count[0] += 1

    def walk(row, perm, poly, denominator):
        if row == 12:
            accumulate(perm, poly, denominator)
            return
        used = set(perm)
        for col in support[row]:
            if col in used:
                continue
            num_dict, den_exp = parsed[row][col]
            walk(
                row + 1,
                perm + [col],
                mul_poly(poly, num_dict),
                tuple(denominator[t] + den_exp[t] for t in range(4)),
            )

    walk(0, [], {(0, 0, 0, 0): (1, 0)}, (0, 0, 0, 0))
    check("PLUS_SUPPORT_MATCHING_COUNT_2304", matching_count[0] == 2304)
    min_exp = [min(key[t] for key in accumulated) for t in range(4)]
    max_exp = [max(key[t] for key in accumulated) for t in range(4)]
    check("PLUS_DET_LAURENT_WINDOW", min_exp == [-3, -3, -3, -3] and max_exp == [3, 3, 3, 3])
    numerator = {
        tuple(exp[t] + 3 for t in range(4)): coeff
        for exp, coeff in accumulated.items()
    }
    check("NUMERATOR_671_TERMS_DEGREE_AT_MOST_6", len(numerator) == 671 and max(max_exp) + 3 == 6)
    check(
        "NUMERATOR_HAS_A_TERM_FREE_OF_EACH_VARIABLE",
        all(any(exp[t] == 0 and coeff != (0, 0) for exp, coeff in numerator.items()) for t in range(4)),
    )
    real_witness = numerator[(6, 4, 4, 4)]
    imag_witness = numerator[(6, 4, 3, 2)]
    check("CONJUGATE_NONASSOCIATE_WITNESSES", real_witness == (512, 0) and imag_witness == (0, -512))

    ledger_path = Path(__file__).resolve().parents[2] / "certificates" / "a4d_resonance_divisor_chiral_numerator.json"
    ledger = json.loads(ledger_path.read_text())
    ledger_dict = {}
    for a0, a1, a2, a3, coeff_text in ledger["terms"]:
        coeff = sp.sympify(coeff_text)
        real, imag = coeff.as_real_imag()
        ledger_dict[(a0, a1, a2, a3)] = (int(real), int(imag))
    check("NUMERATOR_MATCHES_PRIOR_BAREISS_LEDGER", ledger_dict == numerator)

    sample = {z[0]: 2, z[1]: 3, z[2]: 5, z[3]: 7}
    direct_plus = sp.Matrix(12, 12, lambda i, j: sp.simplify(plus[i, j].subs(sample))).det()
    series_plus = 0
    point = (2, 3, 5, 7)
    for exp, (re, im) in accumulated.items():
        monomial = sp.Integer(1)
        for t in range(4):
            monomial *= sp.Integer(point[t]) ** exp[t]
        series_plus += (re + im * I) * monomial
    check("PLUS_EXPANSION_MATCHES_NUMERIC_DET", sp.expand(direct_plus - series_plus) == 0)
    direct_full = sp.Matrix(24, 24, lambda i, j: sp.simplify(owned[i, j].subs(sample))).det()
    direct_minus = sp.Matrix(12, 12, lambda i, j: sp.simplify(minus[i, j].subs(sample))).det()
    check(
        "DET_SPLITS_AS_CHIRAL_NORM",
        sp.expand(direct_full * (4096 ** 2) - direct_plus * direct_minus) == 0,
    )

    top_degree, top_coeff = chart_leading_coefficient(numerator)
    check("CHART_LEADING_U18_IS_CONSTANT_-1024", top_degree == 18 and top_coeff == (-1024, 0))
    specialized = bivariate_from_chart(numerator, 1, 4)
    check(
        "SPECIALIZATION_PRESERVES_U_DEGREE",
        max(exp[0] for exp in specialized) == 18 and specialized.get((18, 0)) == (-1024, 0),
    )

    def derivative_gcd_is_one(reduced, prime: int) -> bool:
        u, y = sp.symbols("u y")
        expression = sum(coeff * u ** eu * y ** ey for (eu, ey), coeff in reduced.items())
        poly = sp.Poly(sp.expand(expression), u, y, modulus=prime)
        return sp.gcd(poly, sp.diff(poly, u)).degree() == 0

    primes = (1009, 1021)
    gao_reports = []
    for prime in primes:
        check(f"PRIME_{prime}_SPLITS_I_AND_CLEARS_BOUND", prime % 4 == 1 and prime > (2 * 18 - 1) * 6)
        root = sqrt_minus_one(prime)
        reduced = reduce_bivariate(specialized, prime, root)
        m_deg, n_deg, dimension = gao_dimension(reduced, prime)
        check(f"GAO_HYPOTHESES_{prime}", m_deg == 18 and prime > (2 * m_deg - 1) * n_deg)
        check(f"GAO_DIMENSION_ONE_{prime}", dimension == 1)
        check(f"SPECIALIZATION_SQUAREFREE_{prime}", derivative_gcd_is_one(reduced, prime))
        gao_reports.append({"prime": prime, "y_degree": n_deg, "dimension": dimension})

    # The same linear system must be able to fail absolute irreducibility.
    sum_of_squares = {(2, 0): 1, (0, 2): 1}
    inert = 1031  # 1031 ≡ 3 (mod 4), so u^2+y^2 is irreducible over F_p and reducible over F_p bar.
    circle = {(2, 0): 1, (0, 2): 1, (0, 0): inert - 1}
    check("CONTROL_SUM_OF_SQUARES_ABSOLUTELY_REDUCIBLE", gao_dimension(sum_of_squares, inert)[2] == 2)
    check("CONTROL_CIRCLE_ABSOLUTELY_IRREDUCIBLE", gao_dimension(circle, inert)[2] == 1)

    field = sp.QQ.algebraic_field(I)
    rank_one = int(connection_hessian((1, 1, 1, 1)).to_DM().convert_to(field).rank())
    counter = (sp.Integer(-1), sp.Integer(-1), I, I)
    rank_counter = int(connection_hessian(counter).to_DM().convert_to(field).rank())
    check("RANK_24_OFF_DIVISOR", rank_one == 24)
    check("COUNTEREXAMPLE_RANK_22", rank_counter == 22)
    n_plus_i = sum(value == I for value in counter)
    n_minus_i = sum(value == -I for value in counter)
    predicted = 2 * max(n_plus_i, n_minus_i)
    check("PHASE_COUNT_LAW_PREDICTS_4_AND_IS_FALSE", predicted == 4 and 24 - rank_counter == 2)
    substitution = dict(zip(z, counter))
    plus_value = 0
    minus_value = 0
    for exp, (re, im) in numerator.items():
        monomial = sp.Integer(1)
        for variable, power in zip(z, exp):
            monomial *= substitution[variable] ** power
        plus_value += (re + im * I) * monomial
        minus_value += (re - im * I) * monomial
    check(
        "COUNTEREXAMPLE_LIES_ON_BOTH_GEOMETRIC_COMPONENTS",
        sp.expand(plus_value) == 0 and sp.expand(minus_value) == 0,
    )

    result = {
        "status": "CANDIDATE",
        "carrier": "owned holomorphic connection Hessian A(z) on (C*)^4",
        "object": "geometric hypersurface components V(P+) and V(conjugate(P+))",
        "numerator_term_count": len(numerator),
        "chart_u_degree": top_degree,
        "chart_leading_coefficient": list(top_coeff),
        "specialization": {"y2": 1, "y3": 4},
        "gao": gao_reports,
        "generic_rank_on_each_geometric_component": 23,
        "generic_nullity_on_each_geometric_component": 1,
        "phase_count_at_(-1,-1,i,i)": {
            "predicted_nullity": predicted,
            "exact_rank": rank_counter,
            "exact_nullity": 24 - rank_counter,
        },
        "missing_stratum": (
            "nullity >= 2 locus, including the conjugate intersection "
            "V(P+) ∩ V(conjugate(P+)) and any Fitting component where one "
            "chiral block has rank <= 10; candidate partial in "
            "stratum_results.json: intersection dimension 2, generic rank 22 "
            "on equal-spatial components and on components through "
            "(-1,-1,i,i); still unseen: generic rank of residual components "
            "that avoid that point and of Fitting components that avoid it"
        ),
    }
    output = Path(__file__).with_name("results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("CANDIDATE_GEOMETRIC_COMPONENTS_CERTIFIED", flush=True)
    print("RESULT_JSON", output, flush=True)


if __name__ == "__main__":
    main()
