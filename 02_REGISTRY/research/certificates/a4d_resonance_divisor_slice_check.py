#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=1200
"""Exact exploratory slices of the owned four-character connection Hessian.

This certificate rebuilds the same 24x24 A(Z) convention as
`a4d_resonance_divisor_counterexample_check.py`. It does not claim a global
factorization or complete rank stratification.
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
    inversions = sum(sequence[i] > sequence[j]
                     for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def mul4(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[2] * right[0],
        left[0] * right[3] + left[1] * right[2]
        + left[2] * right[1] + left[3] * right[0],
    )


def exp4(left, right, phase_left=1, phase_right=1, inverse=False):
    sign = -1 if inverse else 1
    return (
        sp.eye(4),
        sign * phase_left * left,
        sign * phase_right * right,
        sp.Rational(1, 2) * phase_left * phase_right
        * (left * right + right * left),
    )


def curvature_mixed(plaquette):
    return plaquette[3] - sp.Rational(1, 2) * (
        plaquette[1] * plaquette[2] + plaquette[2] * plaquette[1]
    )


def connection_hessian(characters: tuple[sp.Expr, ...]) -> sp.Matrix:
    action = sp.Integer(0)
    for r, s in PAIR:
        plaquette = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
        plaquette = mul4(plaquette, exp4(A_LINKS[r], B_LINKS[r]))
        plaquette = mul4(plaquette, exp4(A_LINKS[s], B_LINKS[s], characters[r], 1 / characters[r]))
        plaquette = mul4(plaquette, exp4(A_LINKS[r], B_LINKS[r], characters[s], 1 / characters[s], True))
        plaquette = mul4(plaquette, exp4(A_LINKS[s], B_LINKS[s], inverse=True))
        u, v = [j for j in range(4) if j not in (r, s)]
        area = wedge(BASIS[u], BASIS[v])
        action += orientation((r, s)) * (
            area.T * G2 * STAR * bivector(curvature_mixed(plaquette))
        )[0]
    action = sp.expand(action)
    return sp.Matrix(24, 24, lambda i, j: sp.diff(sp.diff(action, AV[i]), BV[j]))


def exact_rank(matrix: sp.Matrix, domain) -> int:
    return int(matrix.to_DM().convert_to(domain).rank())


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print("PASS_" + label, flush=True)


z = sp.symbols("z0:4")
A = connection_hessian(z)
check("OWNER_SHAPE_24x24", A.shape == (24, 24))
check("OWNER_NONZERO_COUNT_96", sum(value != 0 for value in A) == 96)


def coordinate_change(sigma: tuple[int, int, int, int]) -> sp.Matrix:
    """Lift a coordinate permutation to the owned 24 link-generator basis."""
    q = sp.zeros(4)
    for old, new in enumerate(sigma):
        q[new, old] = 1
    generator_change = sp.zeros(6)
    for j, generator in enumerate(GEN):
        transformed = q * generator * q.T
        for k, basis_generator in enumerate(GEN):
            denominator = sum(basis_generator[a, b] ** 2 for a in range(4) for b in range(4))
            generator_change[k, j] = sum(
                transformed[a, b] * basis_generator[a, b]
                for a in range(4) for b in range(4)
            ) / denominator
    lifted = sp.zeros(24)
    for new_role in range(4):
        old_role = sigma.index(new_role)
        for new_generator in range(6):
            for old_generator in range(6):
                lifted[6 * new_role + new_generator, 6 * old_role + old_generator] = (
                    generator_change[new_generator, old_generator]
                )
    return lifted


spatial_transpositions = ((0, 2, 1, 3), (0, 1, 3, 2))
for index, sigma in enumerate(spatial_transpositions):
    character_map = {z[r]: z[sigma.index(r)] for r in range(4)}
    permuted_A = A.subs(character_map, simultaneous=True)
    change = coordinate_change(sigma)
    check(f"SPATIAL_S3_GENERATOR_{index}_CONGRUENCE", change.T * permuted_A * change == A)
    check(f"SPATIAL_S3_GENERATOR_{index}_UNIT_DETERMINANT", change.det() == 1)
inverse_A = A.subs({z[r]: 1 / z[r] for r in range(4)}, simultaneous=True)
check("GLOBAL_CHARACTER_INVERSION_TRANSPOSE", inverse_A == A.T)

# Entrywise Laurent complexity after exact cancellation.
entry_terms = []
entry_degrees = []
entry_denominators = set()
for value in A:
    numerator, denominator = sp.fraction(sp.cancel(value))
    numerator_poly = sp.Poly(numerator, *z)
    entry_terms.append(len(numerator_poly.terms()))
    entry_degrees.append(numerator_poly.total_degree())
    entry_denominators.add(str(sp.factor(denominator)))
check("ENTRY_TERMS_AT_MOST_4", max(entry_terms) <= 4)
check("ENTRY_NUMERATOR_TOTAL_DEGREE_AT_MOST_2", max(entry_degrees) <= 2)
check("ENTRY_DENOMINATORS_OWNED", entry_denominators <= {"1", *(f"2*{zj}" for zj in z)})

# Each 6x6 role-to-role block has rank four over Q(z0,z1,z2,z3).
function_field = sp.QQ.frac_field(*z)
block_ranks = []
for r in range(4):
    row = []
    for s in range(4):
        block = A.extract(range(6 * r, 6 * r + 6), range(6 * s, 6 * s + 6))
        row.append(int(block.to_DM().convert_to(function_field).rank()))
    block_ranks.append(row)
check("ALL_ROLE_BLOCK_GENERIC_RANK_4", block_ranks == [[4] * 4 for _ in range(4)])

x = sp.symbols("x")
one, minus_one = sp.Integer(1), sp.Integer(-1)
slices = {
    "(x,1,1,1)": ((x, one, one, one), (3 * x**4 - 22 * x**2 + 3)**2 / x**4),
    "(x,x,1,1)": ((x, x, one, one), sp.Integer(256)),
    "(x,1/x,1,1)": ((x, 1 / x, one, one), (x**4 - 2 * x**3 - 2 * x**2 - 2 * x + 1)**4 / x**8),
    "(x,x,x,1)": ((x, x, x, one), (x**8 + 6 * x**6 + 18 * x**4 + 6 * x**2 + 1)**2 / (4 * x**8)),
    "(x,-1,1,1)": ((x, minus_one, one, one), (x**6 - 3 * x**5 - x**4 - 10 * x**3 - x**2 - 3 * x + 1)**2 / x**6),
}
slice_results = {}
for label, (characters, expected) in slices.items():
    determinant = sp.factor(sp.cancel(connection_hessian(characters).det(method="domain-ge")))
    check("SLICE_" + label.replace(" ", "").replace(",", "_").replace("(", "").replace(")", "").replace("/", "over"),
          sp.simplify(determinant - expected) == 0)
    slice_results[label] = str(determinant)

y = sp.symbols("y")
f_xy = x * y - x + y + 1
f_yx = x * y + x - y + 1
h_xy = (
    3 * x**8 * y**2 - x**6 * y**4 + 8 * x**6 * y**2 - x**6
    + 4 * x**5 * y**3 - 4 * x**5 * y - 4 * x**4 * y**4
    + 22 * x**4 * y**2 - 4 * x**4 - 4 * x**3 * y**3
    + 4 * x**3 * y - x**2 * y**4 + 8 * x**2 * y**2 - x**2 + 3 * y**2
)
spatial_diagonal_expected = f_xy**2 * f_yx**2 * h_xy**2 / (64 * x**10 * y**6)
spatial_diagonal_det = sp.factor(sp.cancel(
    connection_hessian((y, x, x, x)).det(method="domain-ge")
))
check("SPATIAL_DIAGONAL_TWO_VARIABLE_FACTORIZATION",
      sp.simplify(spatial_diagonal_det - spatial_diagonal_expected) == 0)
slice_results["(y,x,x,x)"] = str(spatial_diagonal_det)

# Exact negative controls inherited from the merged phase-count-law refutation.
A_generic = connection_hessian((one, one, one, one))
A_counterexample = connection_hessian((minus_one, minus_one, I, I))
field_i = sp.QQ.algebraic_field(I)
rank_generic = exact_rank(A_generic, field_i)
rank_counterexample = exact_rank(A_counterexample, field_i)
check("NEGATIVE_CONTROL_FULL_RANK_AT_ONE", rank_generic == 24)
check("NEGATIVE_CONTROL_COUNT_LAW_COUNTEREXAMPLE", rank_counterexample == 22)

# A global square up to a Laurent unit would have a fixed square-class on
# every point whose four character coordinates are rational squares. Ratios
# of two such determinant values would therefore be rational squares.
square_points = {
    "(4,9,16,25)": (sp.Integer(4), sp.Integer(9), sp.Integer(16), sp.Integer(25)),
    "(1,4,9,16)": (sp.Integer(1), sp.Integer(4), sp.Integer(9), sp.Integer(16)),
    "(4,1,25,9)": (sp.Integer(4), sp.Integer(1), sp.Integer(25), sp.Integer(9)),
}
specialized_determinants = {
    label: sp.Rational(connection_hessian(characters).det(method="domain-ge"))
    for label, characters in square_points.items()
}


def is_rational_square(value: sp.Expr) -> bool:
    numerator, denominator = sp.fraction(sp.cancel(value))
    numerator_root, numerator_is_square = sp.integer_nthroot(abs(int(numerator)), 2)
    denominator_root, denominator_is_square = sp.integer_nthroot(int(denominator), 2)
    return numerator_is_square and denominator_is_square and int(numerator) >= 0


square_class_ratios = {}
labels = list(specialized_determinants)
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        ratio = sp.factor(specialized_determinants[labels[i]] / specialized_determinants[labels[j]])
        square_class_ratios[f"{labels[i]} / {labels[j]}"] = str(ratio)
check("GLOBAL_DETERMINANT_NOT_LAURENT_UNIT_TIMES_SQUARE",
      all(not is_rational_square(
          specialized_determinants[labels[i]] / specialized_determinants[labels[j]]
      ) for i in range(len(labels)) for j in range(i + 1, len(labels))))

# Exact Hodge/chiral decomposition.  This is a global norm representation,
# not an irreducible factorization of the rational Laurent determinant.
Biv = sp.Matrix.hstack(*(bivector(generator) for generator in GEN))
Hodge = Biv.inv() * STAR * Biv
plus_basis = Hodge - I * sp.eye(6)
minus_basis = Hodge + I * sp.eye(6)
plus_eigenspace = plus_basis.nullspace()
minus_eigenspace = minus_basis.nullspace()
T6 = sp.Matrix.hstack(*plus_eigenspace, *minus_eigenspace)
T = sp.diag(T6, T6, T6, T6)
ip = [6 * role + j for role in range(4) for j in range(3)]
im = [6 * role + j for role in range(4) for j in range(3, 6)]
Qchiral = T.T * A * T
cross_pm = Qchiral.extract(ip, im).applyfunc(sp.cancel)
cross_mp = Qchiral.extract(im, ip).applyfunc(sp.cancel)
check("CHIRAL_CROSS_BLOCKS_IDENTICALLY_ZERO",
      all(value == 0 for value in cross_pm) and all(value == 0 for value in cross_mp))
Aplus = Qchiral.extract(ip, ip).applyfunc(sp.cancel)
Aminus = Qchiral.extract(im, im).applyfunc(sp.cancel)
check("CHIRAL_BLOCKS_ARE_CONJUGATES",
      Aminus == Aplus.xreplace({I: -I}))
det_T = sp.factor(T.det())
check("CHIRAL_CHANGE_BASIS_DETERMINANT_4096", det_T == 4096)

# Compute det(Aplus) by sparse fraction-free Bareiss elimination over Q(i).
# Multiplication by z0*z1*z2*z3 clears the entry denominators first.
K = sp.QQ.algebraic_field(I)
monomial = sp.prod(z)
size = 12
bareiss = [
    [sp.Poly(sp.cancel(Aplus[row, col] * monomial), *z, domain=K)
     for col in range(size)]
    for row in range(size)
]
previous = sp.Poly(1, *z, domain=K)
permutation_sign = 1
for pivot_index in range(size - 1):
    best = None
    for row in range(pivot_index, size):
        row_nnz = sum(not bareiss[row][col].is_zero
                      for col in range(pivot_index, size))
        if not row_nnz:
            continue
        for col in range(pivot_index, size):
            if bareiss[row][col].is_zero:
                continue
            col_nnz = sum(not bareiss[r][col].is_zero
                          for r in range(pivot_index, size))
            score = (row_nnz * col_nnz, bareiss[row][col].length(),
                     bareiss[row][col].total_degree(), row, col)
            if best is None or score < best:
                best = score
    if best is None:
        raise AssertionError("chiral plus block is singular over Q(i)(z)")
    _, _, _, pivot_row, pivot_col = best
    if pivot_row != pivot_index:
        bareiss[pivot_index], bareiss[pivot_row] = bareiss[pivot_row], bareiss[pivot_index]
        permutation_sign = -permutation_sign
    if pivot_col != pivot_index:
        for row in bareiss:
            row[pivot_index], row[pivot_col] = row[pivot_col], row[pivot_index]
        permutation_sign = -permutation_sign
    pivot = bareiss[pivot_index][pivot_index]
    for row in range(pivot_index + 1, size):
        left = bareiss[row][pivot_index]
        for col in range(pivot_index + 1, size):
            if bareiss[row][col].is_zero and (left.is_zero or bareiss[pivot_index][col].is_zero):
                continue
            numerator = pivot * bareiss[row][col] - left * bareiss[pivot_index][col]
            bareiss[row][col] = numerator.exquo(previous)
        bareiss[row][pivot_index] = sp.Poly(0, *z, domain=K)
    for col in range(pivot_index + 1, size):
        bareiss[pivot_index][col] = sp.Poly(0, *z, domain=K)
    previous = pivot
    print(f"CHIRAL_BAREISS_STEP_{pivot_index + 1}_OF_{size - 1}", flush=True)

det_Aplus_polynomial = permutation_sign * bareiss[size - 1][size - 1]
det_Aplus = sp.cancel(det_Aplus_polynomial.as_expr() / monomial**size)
plus_numerator, plus_denominator = sp.together(det_Aplus).as_numer_denom()
Pplus = sp.Poly(plus_numerator, *z, extension=I)
check("CHIRAL_PLUS_DENOMINATOR_PRODUCT_Z_CUBED",
      sp.cancel(plus_denominator - monomial**3) == 0)
check("CHIRAL_PLUS_NUMERATOR_671_TERMS_DEGREE_18",
      Pplus.length() == 671 and Pplus.total_degree() == 18)

chiral_terms = [
    [*powers, str(sp.simplify(coefficient))]
    for powers, coefficient in Pplus.terms()
]
chiral_expected_path = Path(__file__).with_name(
    "a4d_resonance_divisor_chiral_numerator.json"
)
chiral_expected = json.loads(chiral_expected_path.read_text())
check("CHIRAL_PLUS_NUMERATOR_COEFFICIENT_LEDGER_EXACT",
      chiral_expected == {
          "variables": [str(variable) for variable in z],
          "denominator": str(plus_denominator),
          "degree": Pplus.total_degree(),
          "term_count": Pplus.length(),
          "field": "Q(i)",
          "terms": chiral_terms,
      })

# The basis determinant contributes det(T)^2.  The three exact controls also
# compare the compact norm formula with fresh full 24x24 determinants.
Pplus_expr = Pplus.as_expr()
chiral_controls = {}
for label, point_values in square_points.items():
    point = tuple(sp.Integer(value) for value in point_values)
    point_substitution = dict(zip(z, point))
    p_value = sp.cancel(Pplus_expr.subs(point_substitution))
    norm_value = sp.cancel(
        p_value * p_value.xreplace({I: -I})
        / (sp.prod(point)**6 * sp.Integer(det_T)**2)
    )
    direct_value = sp.cancel(connection_hessian(point).det(method="domain-ge"))
    check("CHIRAL_NORM_CONTROL_" + label.replace(",", "_"),
          sp.cancel(norm_value - direct_value) == 0)
    chiral_controls[label] = str(norm_value)

chiral_norm = {
    "basis_change_determinant": str(det_T),
    "plus_block": "Pplus(z0,z1,z2,z3)/(z0*z1*z2*z3)^3",
    "minus_block": "conjugate(Pplus)(z0,z1,z2,z3)/(z0*z1*z2*z3)^3",
    "full_determinant": "Pplus*conjugate(Pplus)/(4096^2*(z0*z1*z2*z3)^6)",
    "plus_numerator_field": "Q(i)",
    "plus_numerator_degree": Pplus.total_degree(),
    "plus_numerator_term_count": Pplus.length(),
    "plus_numerator_ledger": chiral_expected_path.name,
    "exact_full_determinant_controls": chiral_controls,
    "irreducible_factorization": "OPEN",
}

result = {
    "owner": "a4d_resonance_divisor_counterexample_check.py connection_hessian convention",
    "symbol_shape": [24, 24],
    "nonzero_entries": 96,
    "max_entry_numerator_terms": max(entry_terms),
    "max_entry_numerator_total_degree": max(entry_degrees),
    "entry_denominators": sorted(entry_denominators),
    "exact_determinant_symmetries": [
        "permutation symmetry on spatial coordinates z1,z2,z3 (two exact generators)",
        "simultaneous inversion z_r -> z_r^-1 for all four characters",
    ],
    "role_block_generic_ranks_over_Q(z)": block_ranks,
    "exact_slice_determinants": slice_results,
    "negative_controls": {
        "rank_at_(1,1,1,1)": rank_generic,
        "rank_at_(-1,-1,i,i)_over_Q(i)": rank_counterexample,
    },
    "square_character_specializations": {
        "determinants": {label: str(value) for label, value in specialized_determinants.items()},
        "ratios": square_class_ratios,
        "conclusion": "global determinant is not a rational Laurent unit times a square",
    },
    "chiral_determinant_norm": chiral_norm,
    "global_multivariable_factorization": "OPEN",
    "complete_rank_stratification": "OPEN",
}
output = Path(__file__).with_name("a4d_resonance_divisor_slice_results.json")
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print("TERMINAL A4D_RESONANCE_DIVISOR_EXACT_SLICES_CERTIFIED", flush=True)
print("RESULT_JSON", output, flush=True)
