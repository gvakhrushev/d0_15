#!/usr/bin/env python3
"""Force-map certificate for the three normalized CAR sources.

J(t) is the memo's B(t): sum_r t_r gamma(a_r) kappa(u_r).
It is not kappa0 B(t) and not a new operator.
The check certifies rank, the nuclear-norm identity, the support
criterion, and a real density of rank at most 2.
It does not continue a nonlinear branch and does not assign a source.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import sympy as s


PIN = "ec45c8cc4085e7bce888d97439251be9e578d4ff"
MEMO = "02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md"
PARENT = "02_REGISTRY/research/sources/d0_native_memory_source_2026-10-16/check_memory_source.py"
MEMO_SHA256 = "8ec54e4838aaa579469896eeaf369e16a24d6a6f0f67824ede6fa88f5cb9b622"
PARENT_SHA256 = "dbffbc21bd1e7d4f194eca4dbc0f9819b0839d6b233a2a74460155d8ba7de26b"

ROOT = Path(__file__).resolve().parents[4]


def require(name, condition, checks):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)


def popcount(mask):
    return bin(int(mask)).count("1")


def creator_matrices():
    creators = []
    for mode in range(4):
        matrix = s.zeros(16)
        for mask in range(16):
            if mask & (1 << mode):
                continue
            sign = (-1) ** popcount(mask & ((1 << mode) - 1))
            matrix[mask | (1 << mode), mask] = sign
        creators.append(matrix)
    return creators


def git_bytes(pin, path):
    return subprocess.check_output(["git", "show", "%s:%s" % (pin, path)], cwd=ROOT)


def load_parent_namespace():
    raw = git_bytes(PIN, PARENT)
    text = raw.decode("utf-8")
    text = text.replace(
        "(mask&((1<<r)-1)).bit_count()",
        "bin(mask&((1<<r)-1)).count('1')",
    )
    text = text.replace("(mask>>1).bit_count()", "bin(mask>>1).count('1')")
    text = text.replace("mask.bit_count()", "bin(mask).count('1')")
    if "bit_count" in text:
        raise AssertionError("parent_bit_count_rewrite_incomplete")
    namespace = {"__name__": "pinned_memory_source"}
    exec(compile(text, PARENT, "exec"), namespace, namespace)
    return hashlib.sha256(raw).hexdigest(), namespace


def lin(vector, operators):
    total = s.zeros(16)
    for index in range(4):
        total += vector[index] * operators[index]
    return total


def gamma(vector, creators, annihilators):
    return lin(vector, creators) + lin(vector, annihilators)


def kappa(vector, creators, annihilators):
    return lin(vector, creators) - lin(vector, annihilators)


def frame_rows(frame_a, frame_b):
    frame = (frame_a - frame_b) * s.eye(4) + frame_b * s.ones(4)
    return [frame.row(index).T for index in range(4)]


def coefficient_vectors():
    return [
        s.Matrix([0, 0, -1, 1]),
        s.Matrix([0, 1, 0, -1]),
        s.Matrix([0, -1, 1, 0]),
    ]


def coefficient_matrix(weights, rows, vectors):
    total = s.zeros(4)
    for index in range(3):
        total += weights[index] * vectors[index] * rows[index + 1].T
    return total


def source_operators(frame_a, frame_b, creators, annihilators):
    rows = frame_rows(frame_a, frame_b)
    vectors = coefficient_vectors()
    operators = []
    for index in range(3):
        operators.append(
            gamma(vectors[index], creators, annihilators)
            * kappa(rows[index + 1], creators, annihilators)
        )
    return rows, vectors, operators


def pencil(weights, operators):
    total = s.zeros(16)
    for index in range(3):
        total += weights[index] * operators[index]
    return total


def gram_invariants(coeff):
    gram = s.expand(coeff * coeff.T)
    trace = s.expand(s.trace(gram))
    discriminant = s.expand((trace ** 2 - s.trace(s.expand(gram * gram))) / 2)
    return trace, discriminant


def plane_coordinates(vector):
    # a1=(0,0,-1,1), a2=(0,1,0,-1), so c1=-x2 and c2=x1.
    return s.Matrix([-vector[2], vector[1]])


def is_zero_matrix(matrix):
    expanded = s.expand(matrix)
    return expanded == s.zeros(*expanded.shape)


def blank_state():
    state = s.zeros(16, 1)
    state[1] = 1 / s.sqrt(2)
    state[15] = -1 / s.sqrt(2)
    return state


def run():
    checks = []
    memo_raw = git_bytes(PIN, MEMO)
    require(
        "memo_pin_sha256",
        hashlib.sha256(memo_raw).hexdigest() == MEMO_SHA256,
        checks,
    )
    parent_sha, parent = load_parent_namespace()
    require("parent_car_pin_sha256", parent_sha == PARENT_SHA256, checks)

    creators = creator_matrices()
    annihilators = [matrix.T for matrix in creators]
    require(
        "creators_match_pinned_parent",
        all(creators[index] == parent["C"][index] for index in range(4)),
        checks,
    )
    eye4 = s.eye(4)
    for index in range(4):
        basis = eye4[:, index]
        require(
            "gamma_matches_parent_%s" % index,
            gamma(basis, creators, annihilators) == parent["gamma"](basis),
            checks,
        )
        require(
            "kappa_matches_parent_%s" % index,
            kappa(basis, creators, annihilators) == parent["kappa"](basis),
            checks,
        )

    frame_a, frame_b = s.symbols("A B", real=True)
    weights = s.Matrix(s.symbols("t1:4", real=True))
    rows, vectors, operators = source_operators(
        frame_a, frame_b, creators, annihilators
    )
    coeff = s.expand(coefficient_matrix(weights, rows, vectors))
    source = s.expand(pencil(weights, operators))

    require("time_component_of_each_a_r_is_zero", all(vectors[i][0] == 0 for i in range(3)), checks)
    require("a1_plus_a2_plus_a3_is_zero", vectors[0] + vectors[1] + vectors[2] == s.zeros(4, 1), checks)
    require("coefficient_time_row_is_zero", coeff.row(0) == s.zeros(1, 4), checks)
    require(
        "coefficient_spatial_rows_sum_to_zero",
        is_zero_matrix(coeff.row(1) + coeff.row(2) + coeff.row(3)),
        checks,
    )
    # Four rows are spanned by two of them, for every real specialization.
    require(
        "rank_at_most_two_by_two_row_span",
        is_zero_matrix(coeff.row(3) + coeff.row(1) + coeff.row(2)) and is_zero_matrix(coeff.row(0)),
        checks,
    )

    basis = s.Matrix.hstack(vectors[0], vectors[1])
    plane_gram = s.expand(basis.T * basis)
    require("plane_gram", plane_gram == s.Matrix([[2, -1], [-1, 2]]), checks)
    coordinate_x, coordinate_y = s.symbols("c1 c2", real=True)
    quadratic = s.expand(
        (s.Matrix([coordinate_x, coordinate_y]).T * plane_gram * s.Matrix([coordinate_x, coordinate_y]))[0]
    )
    squares = s.expand(
        coordinate_x ** 2 + coordinate_y ** 2 + (coordinate_x - coordinate_y) ** 2
    )
    require("plane_gram_is_sum_of_squares", s.expand(quadratic - squares) == 0, checks)
    reduced = s.zeros(2, 4)
    for column in range(4):
        coords = plane_coordinates(coeff[:, column])
        reduced[:, column] = coords
        restored = s.expand(coords[0] * vectors[0] + coords[1] * vectors[1])
        require(
            "column_lies_in_the_plane_%s" % column,
            is_zero_matrix(restored - coeff[:, column]),
            checks,
        )
    reduced_gram = s.expand(plane_gram * reduced * reduced.T)
    trace, discriminant = gram_invariants(coeff)
    require("trace_matches_reduced_gram", s.expand(s.trace(reduced_gram) - trace) == 0, checks)
    require("discriminant_matches_reduced_determinant", s.expand(reduced_gram.det() - discriminant) == 0, checks)

    clifford = s.zeros(16)
    for left in range(4):
        for right in range(4):
            clifford += coeff[left, right] * gamma(eye4[:, left], creators, annihilators) * kappa(
                eye4[:, right], creators, annihilators
            )
    require("pencil_is_the_clifford_compression", is_zero_matrix(source - s.expand(clifford)), checks)
    for index, operator in enumerate(operators):
        require("source_is_real_symmetric_%s" % index, s.expand(operator - operator.T) == s.zeros(16), checks)
    require("pencil_trace_is_zero", s.expand(s.trace(source)) == 0, checks)

    square = s.expand(source * source)
    trace_square = s.expand(s.trace(square))
    require("frobenius_identity", s.expand(trace_square - 16 * trace) == 0, checks)
    quartic_gap = s.expand((square - trace * s.eye(16)) ** 2 - 4 * discriminant * s.eye(16))
    require("squared_shift_is_four_discriminant", is_zero_matrix(quartic_gap), checks)

    gammas = [gamma(eye4[:, index], creators, annihilators) for index in range(4)]
    volume = gammas[0] * gammas[1] * gammas[2] * gammas[3]
    require("volume_squares_to_identity", is_zero_matrix(s.expand(volume * volume - s.eye(16))), checks)
    require("volume_flips_pencil", is_zero_matrix(s.expand(volume * source + source * volume)), checks)

    # Spectral symmetry gives m(a)=m(-a) and m(b)=m(-b). Dimension 16 then
    # says m_a+m_b=8. Tr(J^2)=16 T says the larger and smaller squares share
    # multiplicity 4 whenever D2>0. Here delta stands for sqrt(D2).
    singular_gap = s.symbols("delta", positive=True)
    multiplicity_large, multiplicity_small = s.symbols("m_plus m_minus")
    power_sum = s.expand(
        (multiplicity_large + multiplicity_small) * trace
        + 2 * singular_gap * (multiplicity_large - multiplicity_small)
        - 8 * trace
    )
    solved = s.solve(
        [multiplicity_large + multiplicity_small - 8, power_sum],
        [multiplicity_large, multiplicity_small],
        dict=True,
    )
    require(
        "open_multiplicities_are_four",
        solved == [{multiplicity_large: 4, multiplicity_small: 4}],
        checks,
    )

    blank = blank_state()
    require("blank_is_normalized", s.expand((blank.T * blank)[0] - 1) == 0, checks)
    for index, operator in enumerate(operators):
        moment = s.expand((blank.T * operator * blank)[0])
        require("blank_expectation_zero_%s" % index, moment == 0, checks)

    covariance = s.zeros(3)
    for left in range(3):
        for right in range(3):
            covariance[left, right] = s.expand((blank.T * operators[left] * operators[right] * blank)[0])
    scale = frame_a ** 2 + 3 * frame_b ** 2
    off = frame_a ** 2 - 4 * frame_a * frame_b - frame_b ** 2
    covariance_formula = (2 * scale - off) * s.eye(3) + off * s.ones(3)
    require("blank_covariance_formula", is_zero_matrix(covariance - covariance_formula), checks)

    # Rational witnesses. A>B>0 is the declared root regime, not a new root.
    frame_fix = {frame_a: s.Rational(3, 5), frame_b: s.Rational(1, 10)}
    transverse = {weights[0]: 1, weights[1]: -1, weights[2]: 0}
    rank_one_direction = {weights[0]: 1, weights[1]: 0, weights[2]: 0}
    zero_direction = {weights[0]: 0, weights[1]: 0, weights[2]: 0}
    require("zero_direction_has_rank_zero", coeff.subs(zero_direction).rank() == 0, checks)
    require(
        "axis_direction_has_rank_one",
        coeff.subs(frame_fix).subs(rank_one_direction).rank() == 1,
        checks,
    )
    transverse_coeff = s.expand(coeff.subs(frame_fix).subs(transverse))
    require("transverse_direction_has_rank_two", transverse_coeff.rank() == 2, checks)

    transverse_source = s.expand(source.subs(frame_fix).subs(transverse))
    transverse_trace = s.together(trace.subs(frame_fix).subs(transverse))
    transverse_discriminant = s.together(discriminant.subs(frame_fix).subs(transverse))
    require("transverse_discriminant_positive", transverse_discriminant > 0, checks)
    require(
        "frobenius_is_strictly_smaller_than_nuclear_square",
        s.simplify(transverse_trace - (transverse_trace + 2 * s.sqrt(transverse_discriminant))) != 0,
        checks,
    )
    lam = (5 + s.sqrt(159)) / 10
    z = s.symbols("z")
    got = s.Poly(s.expand(transverse_source.charpoly(z).as_expr()), z)
    expect_roots = (
        (z - (5 + s.sqrt(159)) / 10)
        * (z - (-5 + s.sqrt(159)) / 10)
        * (z - (5 - s.sqrt(159)) / 10)
        * (z - (-5 - s.sqrt(159)) / 10)
    ) ** 4
    expect = s.Poly(s.expand(expect_roots), z)
    require("transverse_spectrum_multiplicities", got == expect, checks)
    require(
        "largest_eigenvalue_is_nuclear_norm",
        s.simplify(lam ** 2 - (transverse_trace + 2 * s.sqrt(transverse_discriminant))) == 0,
        checks,
    )

    kernel = s.simplify(transverse_source - lam * s.eye(16)).nullspace()
    require("max_eigenspace_dimension_four", len(kernel) == 4, checks)
    fixed_operators = [s.expand(operator.subs(frame_fix)) for operator in operators]
    expectations = []
    for vector in kernel:
        norm = s.simplify((vector.T * vector)[0])
        moment = s.Matrix(
            [
                s.simplify((vector.T * fixed_operators[index] * vector)[0] / norm)
                for index in range(3)
            ]
        )
        expectations.append(moment)
    for index in range(1, 4):
        require(
            "max_face_expectation_constant_%s" % index,
            is_zero_matrix(s.simplify(expectations[index] - expectations[0])),
            checks,
        )
    superposition = s.simplify(kernel[0] + 2 * kernel[1] + kernel[2])
    super_norm = s.simplify((superposition.T * superposition)[0])
    super_moment = s.Matrix(
        [
            s.simplify((superposition.T * fixed_operators[index] * superposition)[0] / super_norm)
            for index in range(3)
        ]
    )
    require(
        "max_face_superposition_same_expectation",
        is_zero_matrix(s.simplify(super_moment - expectations[0])),
        checks,
    )
    boundary = expectations[0]
    exposing = s.Matrix([1, -1, 0])
    require(
        "boundary_saturates_support",
        s.simplify((exposing.T * boundary)[0] - lam) == 0,
        checks,
    )
    fixed_covariance = s.simplify(covariance.subs(frame_fix))
    ellipsoid_form = s.simplify((boundary.T * fixed_covariance.inv() * boundary)[0])
    require("boundary_lies_outside_blank_ellipsoid", s.simplify(ellipsoid_form - 1) > 0, checks)

    vector = s.simplify(kernel[0])
    vector_norm = s.simplify((vector.T * vector)[0])
    rank_one = s.simplify(vector * vector.T / vector_norm)
    require("rank_one_density_trace", s.simplify(s.trace(rank_one) - 1) == 0, checks)
    require("rank_one_density_rank", rank_one.rank() == 1, checks)
    rank_one_moment = s.Matrix(
        [s.simplify(s.trace(rank_one * fixed_operators[index])) for index in range(3)]
    )
    require("rank_one_density_matches_boundary", is_zero_matrix(s.simplify(rank_one_moment - boundary)), checks)

    blank_fixed = blank
    mix_columns = s.Matrix.hstack(blank_fixed, s.simplify(vector / s.sqrt(vector_norm)))
    require("blank_and_boundary_vector_independent", mix_columns.rank() == 2, checks)
    rank_two = s.simplify(s.Rational(1, 2) * blank_fixed * blank_fixed.T + s.Rational(1, 2) * rank_one)
    require("rank_two_density_trace", s.simplify(s.trace(rank_two) - 1) == 0, checks)
    require("rank_two_density_rank", rank_two.rank() == 2, checks)
    rank_two_moment = s.Matrix(
        [s.simplify(s.trace(rank_two * fixed_operators[index])) for index in range(3)]
    )
    require(
        "rank_two_density_is_half_boundary",
        is_zero_matrix(s.simplify(rank_two_moment - boundary / 2)),
        checks,
    )
    half_form = s.simplify((rank_two_moment.T * fixed_covariance.inv() * rank_two_moment)[0])
    require("half_boundary_inside_blank_ellipsoid", s.simplify(1 - half_form).is_positive is True, checks)
    # Half of this exposed point falls back into the blank ellipsoid.
    # The rank-2 witness below stays outside that ellipsoid.
    outside_theta = s.Rational(9, 10)
    outside = s.simplify(
        outside_theta * rank_one + (1 - outside_theta) * blank_fixed * blank_fixed.T
    )
    outside_moment = s.Matrix(
        [s.simplify(s.trace(outside * fixed_operators[index])) for index in range(3)]
    )
    outside_form = s.simplify((outside_moment.T * fixed_covariance.inv() * outside_moment)[0])
    require(
        "nine_tenths_matches_scaled_boundary",
        is_zero_matrix(s.simplify(outside_moment - outside_theta * boundary)),
        checks,
    )
    require("nine_tenths_trace", s.simplify(s.trace(outside) - 1) == 0, checks)
    require("nine_tenths_rank_two", outside.rank() == 2, checks)
    require("nine_tenths_outside_blank_ellipsoid", s.simplify(outside_form - 1).is_positive is True, checks)

    # Inadmissible control: twice the exposed point is separated by the same t.
    too_large = 2 * boundary
    require(
        "inadmissible_point_violates_support",
        s.simplify((exposing.T * too_large)[0] - lam) > 0,
        checks,
    )

    # Pure state on the blank ellipsoid, rank one, inside K but not the whole of K.
    hop = s.Matrix([s.Rational(1, 11), s.Rational(-1, 13), s.Rational(2, 17)])
    prepared = blank_fixed
    for index in range(3):
        prepared += hop[index] * fixed_operators[index] * blank_fixed
    prepared = s.simplify(prepared)
    prepared_norm = s.simplify((prepared.T * prepared)[0])
    pure = s.simplify(prepared / s.sqrt(prepared_norm))
    pure_moment = s.Matrix(
        [s.simplify((pure.T * fixed_operators[index] * pure)[0]) for index in range(3)]
    )
    want = s.simplify(2 * fixed_covariance * hop / (1 + (hop.T * fixed_covariance * hop)[0]))
    require("ellipsoid_pure_state_matches_formula", is_zero_matrix(s.simplify(pure_moment - want)), checks)
    pure_form = s.simplify((pure_moment.T * fixed_covariance.inv() * pure_moment)[0])
    require("ellipsoid_pure_state_inside", s.simplify(1 - pure_form) > 0, checks)
    require("ellipsoid_pure_state_rank_one", s.simplify(pure * pure.T).rank() == 1, checks)

    # Real-part lemma used to pass from a Hermitian density to a real one.
    symmetric = s.Matrix([[s.symbols("s1", real=True), s.symbols("a", real=True)],
                          [s.symbols("a", real=True), s.symbols("s2", real=True)]])
    skew = s.Matrix([[0, s.symbols("b", real=True)], [-s.symbols("b", real=True), 0]])
    require("skew_pairs_to_zero_with_symmetric", s.expand(s.trace(skew * symmetric)) == 0, checks)

    for rank in range(0, 6):
        freedom = rank * (rank + 1) // 2
        if rank <= 2:
            require("extreme_rank_room_%s" % rank, freedom <= 4, checks)
        else:
            require("extreme_rank_blocked_%s" % rank, freedom > 4, checks)

    axis_trace = s.together(trace.subs(frame_fix).subs(rank_one_direction))
    axis_discriminant = s.together(discriminant.subs(frame_fix).subs(rank_one_direction))
    axis_source = s.expand(source.subs(frame_fix).subs(rank_one_direction))
    require("rank_one_discriminant_zero", axis_discriminant == 0, checks)
    require(
        "rank_one_square_equals_trace_times_identity",
        is_zero_matrix(s.expand(axis_source * axis_source - axis_trace * s.eye(16))),
        checks,
    )

    return {
        "schema": "d0-rank-force-map/1",
        "pin": PIN,
        "memo_sha256": MEMO_SHA256,
        "parent_sha256": PARENT_SHA256,
        "normalized_operator": "J(t)=memo B(t)",
        "physical_kappa0_units_not_reopened": True,
        "exact_checks": len(checks),
        "checks": checks,
        "rank_bound": "rank C(t)<=2 for every real t,A,B",
        "norm_identity": "||J(t)||_op=||C(t)||_*",
        "support_criterion": "|t·y|<=||C(t)||_* for every real t",
        "rank_two_density": "extreme point has rank<=2; explicit witnesses below",
        "witnesses": {
            "frame": {"A": "3/5", "B": "1/10"},
            "blank_expectation": [0, 0, 0],
            "blank_rank": 1,
            "boundary_t": [1, -1, 0],
            "boundary_y": [str(s.simplify(boundary[i])) for i in range(3)],
            "boundary_nuclear_norm": str(s.simplify(lam)),
            "boundary_ellipsoid_form": str(s.simplify(ellipsoid_form)),
            "boundary_rank": 1,
            "half_boundary_y": [str(s.simplify(rank_two_moment[i])) for i in range(3)],
            "half_boundary_rank": 2,
            "half_boundary_ellipsoid_form": str(s.simplify(half_form)),
            "nine_tenths_y": [str(s.simplify(outside_moment[i])) for i in range(3)],
            "nine_tenths_rank": 2,
            "nine_tenths_ellipsoid_form": str(s.simplify(outside_form)),
            "ellipsoid_pure_y": [str(s.simplify(pure_moment[i])) for i in range(3)],
            "ellipsoid_pure_form": str(s.simplify(pure_form)),
            "inadmissible_separated_by": [1, -1, 0],
        },
        "nonlinear_branch_continued": False,
        "geometric_source_assigned": False,
        "pr_334_merged": False,
        "gr_closed": False,
        "claims_csv_changed": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
