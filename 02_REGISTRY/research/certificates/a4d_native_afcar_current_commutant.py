#!/usr/bin/env python3
"""Exact commutant boundary for the complete CAR current and AF record step."""
import importlib.util
import sys
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
CERT = Path("02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant")


def load(stem):
    path = ROOT / "02_REGISTRY/research/certificates" / (stem + ".py")
    spec = importlib.util.spec_from_file_location(stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CAR = load("a4d_native_correlated_current_transition")
FRAME = load("a4d_native_reference_memory_preparation")
AF = load("a4d_native_fibonacci_record_activation")
JONES = load("a4d_native_jones_record_transport")
P_MOD, A_MOD = CAR.p, CAR.a
MODULUS = 11
I16 = s.eye(16)


def operators():
    u4, p4, b4, t = FRAME.literal_tuple()
    frame = FRAME.mat(
        FRAME.C.B0 * s.kronecker_product(t.T, s.eye(4))
    )
    record = [
        FRAME.mat(s.kronecker_product(x, s.eye(4)))
        for x in (u4, p4, b4)
    ]
    current = [
        FRAME.mat(frame.T * alpha * frame)
        for alpha in CAR.car_operators()[3]
    ]
    return record + current, frame, current


def matrix_action(blocks, coordinates, *, right=False):
    """Literal left/right multiplication on normalized matrix-unit coordinates."""
    index = {coordinate: i for i, coordinate in enumerate(coordinates)}
    result = s.zeros(len(coordinates))
    for column, (block, row, col) in enumerate(coordinates):
        for inner in range(blocks[block].rows):
            coefficient = (
                blocks[block][col, inner]
                if right else blocks[block][inner, row]
            )
            if coefficient:
                target = (
                    (block, row, inner)
                    if right else (block, inner, col)
                )
                result[index[target], column] = coefficient
    return result


def include(blocks, steps):
    for _ in range(steps):
        blocks = [s.diag(*blocks), blocks[0]]
    return blocks


def commutator_map(matrices):
    return s.Matrix.vstack(*(
        s.kronecker_product(matrix.T, I16)
        - s.kronecker_product(I16, matrix)
        for matrix in matrices
    ))


def reduce_mod11(matrix):
    result = matrix.subs(
        {
            CAR.a: 5,
            CAR.p: 3,
            FRAME.a: 5,
            FRAME.p: 3,
        },
        simultaneous=True,
    ).applyfunc(s.radsimp)
    converted = []
    for entry in result:
        if getattr(s.sympify(entry), "free_symbols", set()):
            raise AssertionError("UNREDUCED_SYMBOL_IN_MODULAR_MATRIX")
        value = s.Rational(entry)
        denominator = int(value.q) % MODULUS
        if denominator == 0:
            raise AssertionError("NONINVERTIBLE_MODULAR_DENOMINATOR")
        converted.append(
            (int(value.p) * pow(denominator, -1, MODULUS)) % MODULUS
        )
    return s.Matrix(result.rows, result.cols, converted)


def coefficients_are_integer_polynomials(matrices):
    for matrix in matrices:
        for entry in matrix:
            numerator, denominator = s.fraction(s.cancel(entry))
            if denominator != 1:
                return False
            try:
                polynomial = s.Poly(numerator, CAR.a, CAR.p, domain="QQ")
            except s.PolynomialError:
                return False
            if any(coefficient.q != 1 for coefficient in polynomial.coeffs()):
                return False
    return True


def modular_rank(matrices):
    from sympy.polys.domains import GF
    from sympy.polys.matrices import DomainMatrix

    reduced = reduce_mod11(commutator_map(matrices))
    return DomainMatrix.from_Matrix(reduced).convert_to(GF(MODULUS)).rank()


def certificate_data():
    from sympy.polys.domains import GF
    from sympy.polys.matrices import DomainMatrix

    ops, frame, current = operators()
    checks = []

    def check(name, proposition):
        if not bool(proposition):
            raise AssertionError(name)
        checks.append(name)

    check("adapted_frame_is_orthogonal", FRAME.mat(frame.T * frame - s.eye(16)) == s.zeros(16))
    check("record_step_is_unitary", FRAME.mat(ops[0].T * ops[0] - I16) == s.zeros(16))
    check("price_cut_is_projection", FRAME.mat(ops[1] * ops[1] - ops[1]) == s.zeros(16))
    check("blank_cut_is_projection", FRAME.mat(ops[2] * ops[2] - ops[2]) == s.zeros(16))
    check("price_and_blank_cuts_differ", ops[1] != ops[2])
    check(
        "adapted_coefficients_are_integer_polynomials",
        coefficients_are_integer_polynomials(ops),
    )
    for i, alpha in enumerate(current):
        check(f"current_{i+1}_selfadjoint", FRAME.mat(alpha.T - alpha) == s.zeros(16))
        for j, other in enumerate(current):
            check(
                f"current_clifford_{i+1}_{j+1}",
                FRAME.mat(alpha * other + other * alpha - 2 * int(i == j) * I16)
                == s.zeros(16),
            )
    check(
        "identity_in_common_kernel",
        all(FRAME.mat(I16 * x - x * I16) == s.zeros(16) for x in ops),
    )

    comm = reduce_mod11(commutator_map(ops))
    domain = DomainMatrix.from_Matrix(comm).convert_to(GF(MODULUS))
    reduced, pivot_columns = domain.rref()
    rank = domain.rank()
    check("modular_common_commutant_rank_255", rank == 255)
    check("modular_pivot_column_count", len(pivot_columns) == 255)

    restricted = domain.extract(range(domain.shape[0]), pivot_columns)
    _, pivot_rows = restricted.transpose().rref()
    minor = domain.extract(pivot_rows, pivot_columns)
    determinant = int(minor.det())
    check("pivot_row_count", len(pivot_rows) == 255)
    check("pivot_minor_rank", minor.rank() == 255)
    check("pivot_minor_determinant_mod11", determinant == 6)

    current_rank = modular_rank(current)
    record_rank = modular_rank(ops[:3])
    without_record_step_rank = modular_rank(ops[1:])
    check("current_only_commutant_dimension_32", 256 - current_rank == 32)
    check("record_only_commutant_dimension_16", 256 - record_rank == 16)
    check("omit_record_step_commutant_dimension_2", 256 - without_record_step_rank == 2)

    def matrix_unit(i, j):
        result = s.zeros(2)
        result[i, j] = 1
        return result

    doubled = [s.kronecker_product(matrix, s.eye(2)) for matrix in ops]
    right_units = {
        (i, j): s.kronecker_product(I16, matrix_unit(j, i))
        for i in range(2)
        for j in range(2)
    }
    check(
        "two_copy_right_M2_commutes_with_fixed_tuple",
        all(
            FRAME.mat(operator * action - action * operator) == s.zeros(32)
            for operator in doubled
            for action in right_units.values()
        ),
    )
    check(
        "two_copy_right_M2_op_matrix_unit_relations",
        all(
            FRAME.mat(
                right_units[(i, j)] * right_units[(k, ell)]
                - int(i == ell) * right_units[(k, j)]
            )
            == s.zeros(32)
            for i in range(2)
            for j in range(2)
            for k in range(2)
            for ell in range(2)
        ),
    )
    af_right = AF.right_frames(1)
    check(
        "level1_AF_path_module_right_multiplicity_34_21",
        AF.counts(1) == (2, 1)
        and AF.counts(4) == (8, 5)
        and [frame["dimension"] for frame in af_right] == [34, 21],
    )
    data1 = AF.frame(1)
    d1 = data1["old_dimension"]
    _, Paf1, _, _ = AF.full_operators(data1["V"], d1)
    Pdouble = s.kronecker_product(ops[1], s.eye(2))
    check(
        "level1_two_copy_price_rank_obstruction",
        d1 == 5
        and AF.zero(data1["V"].T * data1["V"] - s.eye(4 * d1))
        and AF.zero(Paf1 * Paf1 - Paf1)
        and s.trace(Paf1) == 2 * d1 == 10
        and Pdouble * Pdouble == Pdouble
        and s.trace(Pdouble) == 16
        and s.trace(Pdouble) > s.trace(Paf1),
    )

    # At AF input level 2, the old A_1=M_2+C algebra has exactly two
    # canonical M_2--M_2 corners in A_2=M_3+M_2: the upper-left M_2 in M_3
    # and the full M_2 block. Their normalized matrix units give four right
    # M_2 copies, or an 8-dimensional spectator module. Split the CAR
    # spectator label s=2*left_row+path and retain the right matrix column as
    # the external two-copy factor.
    data2 = AF.frame(2)
    d2 = data2["old_dimension"]
    coordinates2 = data2["old_coordinates"]
    index2 = {coordinate: i for i, coordinate in enumerate(coordinates2)}
    V2 = data2["V"]
    corner_coordinates = [
        coordinate
        for coordinate in coordinates2
        if (coordinate[0] == 0 and coordinate[1] < 2 and coordinate[2] < 2)
        or coordinate[0] == 1
    ]
    check(
        "level2_old_M2_bimodule_has_two_canonical_path_corners",
        data2["old_sizes"] == (3, 2)
        and d2 == 13
        and len(corner_coordinates) == 8,
    )
    corner_projection = s.diag(*[
        int(coordinate in set(corner_coordinates))
        for coordinate in coordinates2
    ])
    old_m2_units = []
    for i in range(2):
        for j in range(2):
            x = s.zeros(2)
            x[i, j] = 1
            blocks = [s.zeros(3), s.zeros(2)]
            blocks[0][:2, :2] = x
            blocks[1] = x
            old_m2_units.append((i, j, blocks))
            check(
                "level2_old_M2_corner_is_left_and_right_invariant",
                matrix_action(blocks, coordinates2) * corner_projection
                == corner_projection * matrix_action(blocks, coordinates2)
                and matrix_action(blocks, coordinates2, right=True)
                * corner_projection
                == corner_projection
                * matrix_action(blocks, coordinates2, right=True),
            )

    weld = s.zeros(4 * d2, 32)
    for apparatus in range(4):
        for left_row in range(2):
            for path in range(2):
                for right_column in range(2):
                    spectator = 2 * left_row + path
                    source_column = (apparatus * 4 + spectator) * 2 + right_column
                    target_row = apparatus * d2 + index2[(path, left_row, right_column)]
                    weld[target_row, source_column] = 1
    check("level2_two_copy_AF_weld_isometry", weld.T * weld == s.eye(32))
    check(
        "level2_two_copy_AF_weld_uses_only_canonical_M2_corners",
        all(
            (target % d2) in {index2[c] for c in corner_coordinates}
            for target in range(weld.rows)
            for source in range(weld.cols)
            if weld[target, source]
        ),
    )

    U2, P2, B2, _ = FRAME.literal_tuple()
    for name, source_operator, target_operator in zip(
        ("record", "price", "blank"), ops[:3], (U2, P2, B2)
    ):
        check(
            f"level2_two_copy_{name}_intertwiner",
            AF.zero(
                s.kronecker_product(target_operator, s.eye(d2)) * weld
                - weld * s.kronecker_product(source_operator, s.eye(2))
            ),
        )

    # Check the same intertwiners after the actual four-row AF frame is
    # included into the full A_5 GNS carrier; all AF complement modes stay.
    Waf2, Paf2, Baf2, _ = AF.full_operators(V2, d2)
    weld_fine = V2 * weld
    for name, source_operator, target_operator in zip(
        ("record", "price", "blank"), ops[:3], (Waf2, Paf2, Baf2)
    ):
        check(
            f"level2_full_A5_{name}_intertwiner",
            AF.zero(
                target_operator * weld_fine
                - weld_fine * s.kronecker_product(source_operator, s.eye(2))
            ),
        )

    # The right action is the actual old A_1 M_2 action included into A_2 and
    # then into A_5. The CAR copy factor is exactly its matrix-column index.
    right_intertwiners = []
    for i, j, blocks in old_m2_units:
        right_coarse = matrix_action(blocks, coordinates2, right=True)
        source_right = s.zeros(2)
        source_right[j, i] = 1
        right_intertwiners.append(source_right)
        check(
            "level2_two_copy_old_right_M2_intertwiner",
            s.kronecker_product(s.eye(4), right_coarse) * weld
            == weld * s.kronecker_product(s.eye(16), source_right),
        )
        fine_blocks = include(blocks, 3)
        right_fine = matrix_action(fine_blocks, data2["fine_coordinates"], right=True)
        check(
            "level2_actual_A5_right_M2_bond_intertwiner",
            AF.zero(
                right_fine * V2
                - V2 * s.kronecker_product(s.eye(4), right_coarse)
            ),
        )
    for alpha in current:
        for right_unit in right_intertwiners:
            check(
                "level2_two_copy_current_commutes_with_old_right_M2",
                s.kronecker_product(alpha, s.eye(2))
                * s.kronecker_product(s.eye(16), right_unit)
                == s.kronecker_product(s.eye(16), right_unit)
                * s.kronecker_product(alpha, s.eye(2)),
            )

    # The fixed K_2 path label is also the simple-summand label of A_2.
    # Every AF-left observable commutes with the old A_2 right action, in
    # particular its right central projection (1,0). The CAR current must
    # therefore preserve the corresponding path projection if it is to be
    # represented by an AF-left observable on this same weld.
    center0_blocks = [s.eye(3), s.zeros(2)]
    center0_coarse = matrix_action(center0_blocks, coordinates2, right=True)
    center0_fine = matrix_action(
        include(center0_blocks, 3), data2["fine_coordinates"], right=True
    )
    center0_working = s.kronecker_product(s.eye(4), center0_coarse)
    center0_source = s.diag(*[
        int((index % 4) % 2 == 0) for index in range(16)
    ])
    center0_weld = s.kronecker_product(center0_source, s.eye(2))
    check(
        "level2_weld_intertwines_old_A2_right_center",
        center0_working * weld == weld * center0_weld,
    )
    check(
        "level2_actual_A5_weld_intertwines_old_A2_right_center",
        center0_fine * weld_fine == weld_fine * center0_weld,
    )
    current_center_commutators = [
        FRAME.mat(
            center0_weld * s.kronecker_product(alpha, s.eye(2))
            - s.kronecker_product(alpha, s.eye(2)) * center0_weld
        )
        for alpha in current
    ]
    current_center_commutator_ranks = [
        value.rank() for value in current_center_commutators
    ]
    check(
        "level2_fixed_weld_CAR_current_center_commutator_ranks_32_0_32",
        current_center_commutator_ranks == [32, 0, 32],
    )
    check(
        "level2_fixed_weld_CAR_current_1_crosses_A2_center_paths",
        current_center_commutators[0] != s.zeros(32),
    )
    check(
        "level2_fixed_weld_CAR_current_2_preserves_A2_center_paths",
        current_center_commutators[1] == s.zeros(32),
    )
    check(
        "level2_fixed_weld_CAR_current_3_crosses_A2_center_paths",
        current_center_commutators[2] != s.zeros(32),
    )
    check(
        "level2_fixed_weld_no_full_AF_left_current_extension",
        weld.T * weld == s.eye(32)
        and center0_working * weld == weld * center0_weld
        and any(value != s.zeros(32) for value in current_center_commutators),
    )

    # At A_3=M_5+C_3, put both old-M_2 copies inside the same M_5 block.
    # The path is then a left-row multiplicity label; the old right-M_2
    # matrix column is the same (0,1) pair on both copies.
    data3 = AF.frame(3)
    d3 = data3["old_dimension"]
    coordinates3 = data3["old_coordinates"]
    index3 = {coordinate: i for i, coordinate in enumerate(coordinates3)}
    weld3 = s.zeros(4 * d3, 32)
    for apparatus in range(4):
        for left_row in range(2):
            for path in range(2):
                for right_column in range(2):
                    spectator = 2 * left_row + path
                    af_row = left_row + 3 * path
                    source_column = (apparatus * 4 + spectator) * 2 + right_column
                    target_row = apparatus * d3 + index3[(0, af_row, right_column)]
                    weld3[target_row, source_column] = 1
    check(
        "level3_same_simple_two_copy_weld_isometry",
        data3["old_sizes"] == (5, 3)
        and d3 == 34
        and len([c for c in coordinates3 if c[0] == 0 and c[1] in (0, 1, 3, 4) and c[2] in (0, 1)]) == 8
        and weld3.T * weld3 == s.eye(32),
    )
    for i, j, blocks in old_m2_units:
        x = blocks[1]
        included_A3 = include(blocks, 1)
        left_A3 = matrix_action(included_A3, coordinates3)
        right_A3 = matrix_action(included_A3, coordinates3, right=True)
        source_left = s.kronecker_product(
            s.eye(4), s.kronecker_product(s.kronecker_product(x, s.eye(2)), s.eye(2))
        )
        source_right = s.kronecker_product(s.eye(16), x.T)
        check(
            "level3_same_simple_old_left_M2_bimodule_intertwiner",
            s.kronecker_product(s.eye(4), left_A3) * weld3 == weld3 * source_left,
        )
        check(
            "level3_same_simple_common_right_M2_column_intertwiner",
            s.kronecker_product(s.eye(4), right_A3) * weld3 == weld3 * source_right,
        )

    U3, P3, B3, _ = FRAME.literal_tuple()
    for name, source_operator, target_operator in zip(
        ("record", "price", "blank"), ops[:3], (AF.record(), P3, B3)
    ):
        check(
            f"level3_same_simple_{name}_intertwiner",
            AF.zero(
                s.kronecker_product(target_operator, s.eye(d3)) * weld3
                - weld3 * s.kronecker_product(source_operator, s.eye(2))
            ),
        )

    # Use the CAR current only on the left-module closure of the selected
    # rows. Its canonical support projection is zero on row 2 and on the
    # other simple summand; no extra current is assigned to that complement.
    current_support_plus = s.zeros(20)
    for apparatus in range(4):
        for row in (0, 1, 3, 4):
            current_support_plus[apparatus * 5 + row, apparatus * 5 + row] = 1
    current_support_minus = s.zeros(12)
    level3_current_support_multiplicity = [current_support_plus, current_support_minus]
    level3_current_multiplicity = []
    level3_current_on_weld = []
    for component, alpha in enumerate(current):
        plus = s.zeros(20)
        minus = s.zeros(12)
        for source in range(16):
            app_in, spectator_in = divmod(source, 4)
            row_in = spectator_in // 2 + 3 * (spectator_in % 2)
            for target in range(16):
                app_out, spectator_out = divmod(target, 4)
                row_out = spectator_out // 2 + 3 * (spectator_out % 2)
                plus[app_out * 5 + row_out, app_in * 5 + row_in] = alpha[target, source]
        level3_current_multiplicity.append([plus, minus])

        on_weld = s.zeros(4 * d3, 32)
        for source_column in range(32):
            app_in = source_column // 8
            spectator_in = (source_column // 2) % 4
            right_column = source_column % 2
            row_in = spectator_in // 2 + 3 * (spectator_in % 2)
            for app_out in range(4):
                for spectator_out in range(4):
                    row_out = spectator_out // 2 + 3 * (spectator_out % 2)
                    coefficient = plus[
                        app_out * 5 + row_out, app_in * 5 + row_in
                    ]
                    if coefficient:
                        target_row = app_out * d3 + index3[(0, row_out, right_column)]
                        on_weld[target_row, source_column] = coefficient
        check(
            f"level3_same_simple_CAR_current_{component + 1}_intertwiner",
            AF.zero(
                on_weld
                - weld3 * s.kronecker_product(alpha, s.eye(2))
            ),
        )
        level3_current_on_weld.append(on_weld)

    seed3 = FRAME.mat(frame.T * CAR.blank_code() * s.Matrix([A_MOD, P_MOD]))
    seed3_two_copy = s.kronecker_product(seed3, s.eye(2)[:, 0])
    expected_blank3 = s.zeros(4 * d3, 1)
    expected_blank3[index3[(0, 0, 0)]] = A_MOD
    expected_blank3[2 * d3 + index3[(0, 3, 0)]] = P_MOD
    check(
        "level3_same_simple_actual_CAR_blank_binds_to_two_M5_row_copies",
        weld3 * seed3_two_copy == expected_blank3,
    )
    recorded_seed3 = s.kronecker_product(ops[0], s.eye(2)) * seed3_two_copy
    level3_prepared_current = [
        s.Integer(1),
        *[
            FRAME.red(
                (
                    recorded_seed3.T
                    * s.kronecker_product(alpha, s.eye(2))
                    * recorded_seed3
                )[0]
            )
            for alpha in current
        ],
    ]
    check(
        "level3_same_simple_recorded_blank_has_source_current_and_feedback_norm",
        level3_prepared_current == [s.Integer(1), 2 * A_MOD * P_MOD, 0, 0]
        and FRAME.red(1 - (2 * A_MOD * P_MOD) ** 2 - P_MOD**6) == 0,
    )
    check(
        "level3_native_current_reads_the_same_prepared_source",
        all(
            FRAME.red(
                (
                    recorded_seed3.T
                    * weld3.T
                    * level3_current_on_weld[component]
                    * recorded_seed3
                )[0]
            )
            == level3_prepared_current[component + 1]
            for component in range(3)
        ),
    )

    check(
        "level3_same_simple_current_is_corner_Clifford_without_complement_selector",
        all(
            AF.zero(
                level3_current_multiplicity[i][block]
                * level3_current_multiplicity[j][block]
                + level3_current_multiplicity[j][block]
                * level3_current_multiplicity[i][block]
                - (2 * level3_current_support_multiplicity[block]
                   if i == j else s.zeros(level3_current_multiplicity[i][block].rows))
            )
            for block in range(2)
            for i in range(3)
            for j in range(3)
        ),
    )

    # The existing six-step path frames identify these right-A_3 module
    # endomorphisms with literal matrix blocks of A_9, of sizes 89 and 55.
    level3_right_frames = AF.right_frames(3)
    path_matrix = ((1, 1), (1, 0))
    level3_path_bijections = []
    level3_paths_legal = True
    for part in level3_right_frames:
        old_type = part["old_type"]
        native_paths = AF.segments(*data3["old_sizes"], 6)[old_type]
        expected_paths = {
            (kind, path, row)
            for kind, path, _offset in native_paths
            for row in range(data3["old_sizes"][kind])
        }
        folded_paths = []
        for final_type, segment_index, row in part["labels"]:
            column_type, column_path, _column_offset = data3["segments"][final_type][segment_index]
            row_type, row_path, row_offset = next(
                segment
                for segment in data3["segments"][final_type]
                if segment[2] <= row < segment[2] + data3["old_sizes"][segment[0]]
            )
            full_column_path = (old_type,) + column_path
            path = row_path + tuple(reversed(full_column_path[:-1]))
            level3_paths_legal = level3_paths_legal and (
                len(path) == 6
                and path[-1] == old_type
                and all(path_matrix[y][x] == 1 for x, y in zip((row_type,) + path, path))
            )
            folded_paths.append((row_type, path, row - row_offset))
        level3_path_bijections.append(
            len(set(folded_paths)) == len(folded_paths) == part["dimension"]
            and set(folded_paths) == expected_paths
        )
    check(
        "level3_A9_right_frames_are_native_six_path_bijections",
        level3_paths_legal and level3_path_bijections == [True, True],
    )
    level3_native_current = [[None, None] for _ in range(3)]
    level3_native_support = []
    level3_native_current_support = []
    level3_native_record = []
    level3_native_price = []
    level3_native_blank = []
    for part in level3_right_frames:
        block = part["old_type"]
        multiplicity = part["spectator_dimension"]
        native_size = part["dimension"]
        path_frame = part["V"]
        support = FRAME.mat(path_frame * path_frame.T)
        check(
            f"level3_A9_path_frame_{block}_isometry",
            native_size == AF.counts(9)[block]
            and path_frame.shape == (native_size, 4 * multiplicity)
            and AF.zero(path_frame.T * path_frame - s.eye(4 * multiplicity)),
        )
        level3_native_support.append(support)
        current_support = FRAME.mat(
            path_frame * level3_current_support_multiplicity[block] * path_frame.T
        )
        level3_native_current_support.append(current_support)
        level3_native_record.append(
            FRAME.mat(
                path_frame * s.kronecker_product(AF.record(), s.eye(multiplicity)) * path_frame.T
                + s.eye(native_size) - support
            )
        )
        level3_native_price.append(
            FRAME.mat(
                path_frame * s.kronecker_product(P3, s.eye(multiplicity)) * path_frame.T
            )
        )
        level3_native_blank.append(
            FRAME.mat(
                path_frame * s.kronecker_product(B3, s.eye(multiplicity)) * path_frame.T
            )
        )
        for component in range(3):
            current_block = level3_current_multiplicity[component][block]
            native_current = FRAME.mat(path_frame * current_block * path_frame.T)
            level3_native_current[component][block] = native_current
            check(
                f"level3_A9_native_current_{component + 1}_block_{block}_corner_Clifford",
                AF.zero(native_current.T - native_current)
                and AF.zero(native_current * native_current - current_support)
                and AF.zero(native_current * current_support - native_current)
                and AF.zero(native_current * support - native_current),
            )
            check(
                f"level3_A9_native_current_{component + 1}_block_{block}_path_action",
                AF.zero(native_current * path_frame - path_frame * current_block),
            )

    # Bind the recorded CAR blank to the regular A_9 GNS space using the
    # owned right-module row frame and the blank's existing right column 0.
    # Compare that vector state with the canonical Jones conditional vector
    # e/p^3 for the six-step A_3 -> A_9 inclusion.
    field_to_af = {
        CAR.a: AF.a,
        CAR.p: AF.p,
        FRAME.a: AF.a,
        FRAME.p: AF.p,
    }
    recorded_native3 = AF.mat(
        (weld3 * recorded_seed3).subs(field_to_af, simultaneous=True)
    )
    source_row3 = s.zeros(20, 1)
    source_row3_lift = s.zeros(4 * d3, 1)
    for apparatus in range(4):
        for row in range(5):
            value = recorded_native3[apparatus * d3 + index3[(0, row, 0)]]
            source_row3[apparatus * 5 + row] = value
            source_row3_lift[apparatus * d3 + index3[(0, row, 0)]] = value
    check(
        "level3_recorded_blank_is_the_owned_single_right_column_seed",
        AF.zero(recorded_native3 - source_row3_lift)
        and AF.zero(source_row3.T * source_row3 - s.ones(1, 1)),
    )
    source_path_frame = level3_right_frames[0]["V"]
    source_row9 = AF.mat(source_path_frame * source_row3)
    jones_frames9 = [
        AF.mat(
            part.subs(
                {JONES.E.a: AF.a, JONES.E.p: AF.p}, simultaneous=True
            )
        )
        for part in JONES.corner_frames(3)
    ]
    jones_corners9 = [AF.mat(part * part.T) for part in jones_frames9]
    jones_right_column9 = jones_frames9[0][:, 0]
    prepared_gns_matrix9 = AF.mat(source_row9 * jones_right_column9.T)
    prepared_gns_weights9 = [AF.p**10, AF.p**11]
    prepared_gns_norm9 = AF.red(
        sum(
            prepared_gns_weights9[block] * s.trace(value.T * value)
            for block, value in enumerate(
                [prepared_gns_matrix9, s.zeros(55, 55)]
            )
        )
    )
    jones_corner_trace9 = AF.red(
        sum(
            prepared_gns_weights9[block] * s.trace(value)
            for block, value in enumerate(jones_corners9)
        )
    )
    prepared_gns_leakage9 = AF.red(
        (source_row9.T * (s.eye(89) - jones_corners9[0]) * source_row9)[0]
    )
    prepared_gns_current = [s.Integer(1)]
    jones_conditional_current = [s.Integer(1)]
    for component in range(3):
        source_native_current = AF.mat(
            level3_native_current[component][0].subs(
                field_to_af, simultaneous=True
            )
        )
        source_gns_readout = AF.red(
            (source_row9.T * source_native_current * source_row9)[0]
        )
        conditional_trace = AF.red(
            prepared_gns_weights9[0]
            * s.trace(
                jones_corners9[0]
                * source_native_current
                * jones_corners9[0]
            )
            / AF.p**6
        )
        prepared_gns_current.append(source_gns_readout)
        jones_conditional_current.append(conditional_trace)
        check(
            f"level3_regular_GNS_source_current_{component + 1}_matches_native_seed",
            AF.red(
                source_gns_readout
                - level3_prepared_current[component + 1].subs(
                    field_to_af, simultaneous=True
                )
            )
            == 0,
        )
        check(
            f"level3_Jones_conditional_GNS_current_{component + 1}_matches_exact_trace",
            conditional_trace == 0
            and (
                source_gns_readout != 0
                if component == 0
                else source_gns_readout == 0
            ),
        )
    golden_substitution = {
        AF.p: (s.sqrt(5) - 1) / 2,
        AF.a: s.sqrt((s.sqrt(5) - 1) / 2),
    }
    leakage_real = s.simplify(
        prepared_gns_leakage9.subs(golden_substitution, simultaneous=True)
    )
    check(
        "level3_prepared_GNS_vector_is_not_in_Jones_conditional_corner",
        AF.zero(source_row9.T * source_row9 - s.ones(1, 1))
        and AF.zero(jones_frames9[0].T * jones_frames9[0] - s.eye(5))
        and AF.zero(jones_frames9[1].T * jones_frames9[1] - s.eye(3))
        and AF.zero(jones_corners9[0] * jones_corners9[0] - jones_corners9[0])
        and AF.zero(jones_corners9[1] * jones_corners9[1] - jones_corners9[1])
        and AF.red(prepared_gns_norm9 - AF.p**10) == 0
        and AF.red(jones_corner_trace9 - AF.p**6) == 0
        and AF.red(
            prepared_gns_leakage9
            + (source_row9.T * jones_corners9[0] * source_row9)[0]
            - 1
        )
        == 0
        and AF.zero(prepared_gns_matrix9 * jones_corners9[0] - prepared_gns_matrix9)
        and leakage_real.is_positive is True,
    )

    check(
        "level3_A9_native_current_pairwise_anticommutation",
        all(
            AF.zero(
                level3_native_current[i][block] * level3_native_current[j][block]
                + level3_native_current[j][block] * level3_native_current[i][block]
            )
            for block in range(2)
            for i in range(3)
            for j in range(i)
        ),
    )
    check(
        "level3_A9_record_cuts_are_owned_corner_operators",
        all(
            AF.zero(level3_native_record[b].T * level3_native_record[b] - s.eye(level3_native_record[b].rows))
            and AF.zero(level3_native_price[b] ** 2 - level3_native_price[b])
            and AF.zero(level3_native_blank[b] ** 2 - level3_native_blank[b])
            and AF.zero(level3_native_price[b] * level3_native_blank[b] - level3_native_blank[b] * level3_native_price[b])
            and level3_native_price[b] != level3_native_blank[b]
            for b in range(2)
        ),
    )

    # Bind the actual CAR whole-blank column to two normalized AF matrix units
    # with the same old left row and right column, and then through one record
    # step to the positive current already owned on the full CAR carrier.
    seed = FRAME.mat(frame.T * CAR.blank_code() * s.Matrix([A_MOD, P_MOD]))
    seed_two_copy = s.kronecker_product(seed, s.eye(2)[:, 0])
    expected_blank = s.zeros(4 * d2, 1)
    expected_blank[index2[(0, 0, 0)]] = A_MOD
    expected_blank[2 * d2 + index2[(1, 0, 0)]] = P_MOD
    check(
        "level2_whole_blank_maps_to_two_actual_M2_path_units",
        weld * seed_two_copy == expected_blank,
    )
    check(
        "level2_blank_is_in_owned_full_AF_blank_cut",
        AF.zero(Baf2 * weld_fine * seed_two_copy - weld_fine * seed_two_copy),
    )
    recorded_source = s.kronecker_product(ops[0], s.eye(2)) * seed_two_copy
    recorded_fine = Waf2 * weld_fine * seed_two_copy
    check(
        "level2_full_record_step_sends_preparation_to_source_state",
        AF.zero(recorded_fine - weld_fine * recorded_source),
    )
    source_current = [
        s.Integer(1),
        *[
            FRAME.red(
                (recorded_source.T * s.kronecker_product(alpha, s.eye(2))
                 * recorded_source)[0]
            )
            for alpha in current
        ],
    ]
    check(
        "level2_recorded_native_current_is_source_active",
        source_current == [s.Integer(1), 2 * A_MOD * P_MOD, 0, 0],
    )
    check(
        "level2_source_lorentz_norm_matches_feedback_corner",
        FRAME.red(1 - (2 * A_MOD * P_MOD) ** 2 - P_MOD ** 6) == 0,
    )

    return {
        "status": "PASS",
        "proof": "02_REGISTRY/research/A4D_NATIVE_AFCAR_CURRENT_COMMUTANT_BOUNDARY.md",
        "source_commit": "3e512e599f3cf69571b1cacb63972e5c315d9a2c",
        "field": {
            "generator": "a",
            "relations": ["p=a^2", "p^2+p=1", "a^4+a^2-1=0"],
            "specialization": {"prime": 11, "a": 5, "p": 3},
            "polynomial_residue": (5**4 + 5**2 - 1) % 11,
        },
        "commutant": {
            "coefficient_matrix_shape": list(commutator_map(ops).shape),
            "modular_rank": rank,
            "complex_rank_by_minor_and_identity": 255,
            "complex_dimension": 1,
            "pivot_rows": list(map(int, pivot_rows)),
            "pivot_columns": list(map(int, pivot_columns)),
            "minor_determinant_mod11": determinant,
        },
        "controls": {
            "current_only_commutant_dimension": 256 - current_rank,
            "record_only_commutant_dimension": 256 - record_rank,
            "without_record_step_commutant_dimension": 256 - without_record_step_rank,
        },
        "single_copy_right_M2_extension_excluded": True,
        "two_copy_abstract_right_M2_extension_realized": True,
        "two_copy_commutant_dimension_by_block_argument": 4,
        "two_copy_AF_path_binding_established": True,
        "two_copy_AF_all_level_refinement_established": False,
        "level1_two_copy_price_rank_obstruction": {
            "AF_owned_price_rank": 10,
            "doubled_CAR_price_rank": 16,
            "isometric_intertwiner_exists": False,
        },
        "level2_two_copy_record_current_weld": {
            "input_level": 2,
            "input_AF_sizes": list(data2["old_sizes"]),
            "working_dimension": 4 * d2,
            "full_AF_level": 5,
            "full_AF_dimension": V2.rows,
            "canonical_old_M2_bimodule_dimension": len(corner_coordinates),
            "weld_dimension": weld.cols,
            "retained_full_AF_complement_dimension": V2.rows - weld.cols,
            "prepared_current": ["1", "2*a*p", "0", "0"],
            "source_lorentz_norm": "p^6",
            "physical_admission_established": False,
            "all_level_refinement_established": False,
        },
        "level2_fixed_weld_AF_left_current_extension": {
            "old_A2_right_center_intertwining_at_A5": True,
            "CAR_current_components_preserving_path_center": [
                value == s.zeros(32) for value in current_center_commutators
            ],
            "CAR_current_path_center_commutator_ranks": current_center_commutator_ranks,
            "full_AF_left_current_extension_exists": False,
            "scope": "fixed_K2_path_binding_and_AF_left_observable_owner",
        },
        "level3_same_simple_path_current_weld": {
            "input_level": 3,
            "input_AF_sizes": list(data3["old_sizes"]),
            "working_dimension": 4 * d3,
            "canonical_same_simple_M2_rows": [0, 1, 3, 4],
            "common_right_M2_columns": [0, 1],
            "active_weld_dimension": weld3.cols,
            "native_AF_algebra_level": 9,
            "native_AF_block_sizes": list(AF.counts(9)),
            "native_six_path_bijections_checked": level3_path_bijections,
            "native_current_corner_support_ranks": [
                int(s.trace(support)) for support in level3_native_current_support
            ],
            "prepared_source_current": [str(value) for value in level3_prepared_current],
            "prepared_source_lorentz_norm": "p^6",
            "prepared_GNS_source_current": [str(value) for value in prepared_gns_current],
            "canonical_Jones_conditional_GNS_current": [
                str(value) for value in jones_conditional_current
            ],
            "canonical_Jones_conditional_corner_trace": str(jones_corner_trace9),
            "prepared_GNS_vector_norm": str(prepared_gns_norm9),
            "prepared_GNS_vector_off_corner_mass_squared": str(prepared_gns_leakage9),
            "prepared_GNS_vector_off_corner_mass_squared_decimal": str(
                s.N(leakage_real, 16)
            ),
            "prepared_GNS_vector_matches_canonical_Jones_conditional_state": False,
            "fixed_state_binding_scope": "level3_A9_same_simple_path_and_canonical_Jones_conditional_vector",
            "full_CAR_current_extension_in_native_AF_corner": True,
            "current_corner_unit_is_path_generated_active_projection": True,
            "all_level_Jones_operator_transport_follows_from_owned_homomorphism": True,
            "prepared_state_Jones_GNS_binding_established": False,
            "physical_admission_established": False,
        },
        "AF_right_module_capacity": {
            "input_level": 1,
            "input_simple_sizes": [2, 1],
            "working_level": 4,
            "working_simple_sizes": [8, 5],
            "old_right_multiplicities": [34, 21],
            "two_copy_slots_required": 16,
            "M2_branch_has_capacity": True,
            "path_specific_carrier_established": True,
        },
        "larger_multiplicity_or_covariant_current_excluded": False,
        "whole_core_no_go": False,
        "exact_controls": len(checks),
        "check_names": checks,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(certificate_data(), indent=2, sort_keys=True))
