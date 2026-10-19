#!/usr/bin/env python3
"""Exact first-order commutator response of one original full128 pointer event."""
from functools import lru_cache
from pathlib import Path
import ast
import hashlib
import json

import numpy as np
import sympy as s
from scipy.linalg import qr
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[4]
CREATORS = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
PINS = {
    "02_REGISTRY/research/A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md":
        "d7f8498e30e788af43edeb2bfd6e763d429e221cea76b622198687bbf4af21db",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md":
        "2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79",
    "02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md":
        "577cbc909f766468fbef8ab38a5986ae761d348b075c2f38b2e1a88b704d4b3e",
    "02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md":
        "a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915",
    "02_REGISTRY/research/sources/d0_opposite_null_julia_order_memory_2026-10-19/check_lorentz_order_memory.py":
        "48a9692675fbe46c68c4d902d3069ac2c717e2370761508983db2e3245497cb8",
    "02_REGISTRY/research/sources/d0_complete_record_channel_2026-10-17/check_record_channel.py":
        "dee7ada5cf04bf961701206f65b216e1ab9c6f45ef9f9ed3258e70bed9cb13a2",
}


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(ok, name):
        if not bool(ok):
            raise ArithmeticError("full128_order_readout:" + name)
        checks.append(name)

    def eq(left, right, name):
        diff = left - right
        values = list(diff) if isinstance(diff, s.MatrixBase) else [diff]
        require(all(s.simplify(v) == 0 for v in values), name)

    for relpath, digest in PINS.items():
        actual = hashlib.sha256((repo / relpath).read_bytes()).hexdigest()
        require(actual == digest, "pin_" + Path(relpath).name)

    tree = ast.parse((repo / CREATORS).read_text())
    nodes = [
        node for node in tree.body
        if (isinstance(node, ast.FunctionDef) and node.name == "creator")
        or (isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name)
                    and target.id == "EXTERIOR_ORDER" for target in node.targets))
    ]
    require(len(nodes) == 2, "only_owned_CAR_creator_and_order_loaded")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, "exec"), scope)
    C = [scope["creator"](r) for r in range(4)]
    I16 = s.eye(16)

    def unit(i, j):
        M = s.zeros(4)
        M[i, j] = 1
        return M

    N2 = unit(1, 2) + unit(2, 0)
    N3 = unit(1, 3) + unit(3, 0)
    Nbar2 = unit(0, 2) + unit(2, 1)
    Nbar3 = unit(0, 3) + unit(3, 1)
    J23 = unit(2, 3) - unit(3, 2)
    B = unit(1, 1) - unit(0, 0)
    lorentz_generators = [N2, N3, Nbar2, Nbar3, J23, B]
    eta = s.Matrix([
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ])
    eq(N2 * Nbar3 - Nbar3 * N2, J23, "opposite_null_commutator_is_J23")
    for name, generator in zip(
        ("N2", "N3", "Nbar2", "Nbar3", "J23", "B"),
        lorentz_generators,
    ):
        eq(generator.T * eta + eta * generator, s.zeros(4),
           "proper_lorentz_tangent_" + name)
    require(s.Matrix.vstack(*(G.reshape(1, 16) for G in lorentz_generators)).rank() == 6,
            "six_independent_proper_lorentz_generators")

    for r in range(4):
        eq(C[r] * C[r].H + C[r].H * C[r], I16,
           "CAR_single_mode_" + str(r))
        require(C[r] != s.zeros(16), "nonzero_CAR_mode_" + str(r))
    GJ = sum(
        (J23[i, j] * C[i] * C[j].H
         for i in range(4) for j in range(4)),
        s.zeros(16),
    )
    for k in range(4):
        expected = sum((J23[i, k] * C[i] for i in range(4)), s.zeros(16))
        eq(GJ * C[k] - C[k] * GJ, expected,
           "full16_exterior_lift_generator_" + str(k))

    # L=4 first-shell Fourier phases: k=(0,0,0,1), so shift_3=i.
    h = s.Rational(1, 4)
    nu = s.Rational(3, 5)
    z = [s.Integer(1), s.Integer(1), s.Integer(1), s.I]
    d_h = s.zeros(16)
    for r in range(4):
        P_r = nu * C[r] * z[r]  # M_r=I at the base configuration
        d_h += (P_r - nu * C[r]) / h
    D_h = d_h + d_h.H
    A = h * D_h / 16
    require(D_h == D_h.H, "actual_true_adjoint_Dh_is_selfadjoint")
    require(A == A.H, "blank_SELECT_block_A_is_selfadjoint")
    require(nu < 1, "strict_contraction_weight")
    for r in range(4):
        projector = C[r] * C[r].H
        right_projector = C[r].H * C[r]
        eq(projector * projector, projector, "CAR_projection_" + str(r))
        eq(right_projector * right_projector, right_projector,
           "CAR_right_projection_" + str(r))

    # Vary only the proper Lorentz link M_2 by exp(t J23).
    dP = nu * C[2] * GJ * z[2]
    d_dh = dP / h
    dD_h = d_dh + d_dh.H
    dA = h * dD_h / 16

    p = (s.sqrt(5) - 1) / 2
    require(s.simplify(p + p**2 - 1) == 0, "golden_weight_normalization")
    # The original full128 port-0, blank-label Kraus block is
    # p I + p^2 (I - 2 A* A) = I - 2 p^2 A^2.
    K00 = I16 - 2 * p**2 * A**2
    dK00 = -2 * p**2 * (dA * A + A * dA)
    q0_source = s.simplify(s.trace(K00 * dK00) / 8)
    expected_source = (
        s.Rational(42633, 5120000)
        - s.Rational(14157, 5120000) * s.sqrt(5)
    )
    eq(q0_source, expected_source, "exact_full128_pointer_J23_source")
    require(q0_source.is_positive is True, "strictly_positive_order_source")

    # At zero Fourier momentum A=0, hence this same pointer has zero first jet.
    d0 = s.zeros(16)
    for r in range(4):
        d0 += (nu * C[r] - nu * C[r]
               + (nu * C[r] - nu * C[r]).H) / h
    A0 = h * d0 / 16
    dP0 = nu * C[2] * GJ
    dD0 = (dP0 + dP0.H) / h
    dA0 = h * dD0 / 16
    K000 = I16 - 2 * p**2 * A0**2
    dK000 = -2 * p**2 * (dA0 * A0 + A0 * dA0)
    q0_zero_mode_source = s.simplify(s.trace(K000 * dK000) / 8)
    eq(q0_zero_mode_source, 0, "zero_mode_order_source_control")
    eq(A0, s.zeros(16), "zero_mode_blank_SELECT_block_is_zero")

    # A well-typed algebraic diagnostic for naive same-flag Julia composition.
    # The relative unitary V(M)=J(P0)^* J(P(M)) is normalized to V(I)=I.
    # This tests that specific candidate map; it does not assume D0 executes V.
    r_link = 2
    Qleft = C[r_link] * C[r_link].H
    Qright = C[r_link].H * C[r_link]
    Pstar = nu * C[r_link]  # shift_2=1 on the mode used above
    Lstar = I16 - s.Rational(1, 5) * Qleft
    Rstar = I16 - s.Rational(1, 5) * Qright
    Jstar = Pstar.row_join(Lstar).col_join(Rstar.row_join(-Pstar.H))
    eq(Jstar.H * Jstar, s.eye(32), "base_Julia_word_is_unitary")

    def sylvester_at_base(projector, rhs):
        pieces = (
            (I16 - projector, s.Integer(1)),
            (projector, s.Rational(4, 5)),
        )
        return sum(
            (left * rhs * right / (lam_left + lam_right)
             for left, lam_left in pieces
             for right, lam_right in pieces),
            s.zeros(16),
        )

    def relative_julia_tangent(generator):
        G = sum(
            (generator[i, j] * C[i] * C[j].H
             for i in range(4) for j in range(4)),
            s.zeros(16),
        )
        dP_link = nu * C[r_link] * G
        rhs_left = -dP_link * Pstar.H - Pstar * dP_link.H
        rhs_right = -dP_link.H * Pstar - Pstar.H * dP_link
        dL_link = sylvester_at_base(Qleft, rhs_left)
        dR_link = sylvester_at_base(Qright, rhs_right)
        eq(Lstar * dL_link + dL_link * Lstar, rhs_left,
           "left_Julia_defect_root_Sylvester")
        eq(Rstar * dR_link + dR_link * Rstar, rhs_right,
           "right_Julia_defect_root_Sylvester")
        dJ_link = dP_link.row_join(dL_link).col_join(
            dR_link.row_join(-dP_link.H)
        )
        tangent = Jstar.H * dJ_link
        eq(tangent.H + tangent, s.zeros(32),
           "relative_Julia_tangent_is_skew")
        return tangent

    XN = relative_julia_tangent(N2)
    Xbar = relative_julia_tangent(Nbar3)
    XJ = relative_julia_tangent(J23)
    julia_lie_defect = s.simplify(XN * Xbar - Xbar * XN - XJ)
    eq(julia_lie_defect.H + julia_lie_defect, s.zeros(32),
       "relative_Julia_Lie_defect_is_skew")
    julia_lie_defect_norm2 = s.simplify(
        s.trace(julia_lie_defect.H * julia_lie_defect)
    )
    eq(julia_lie_defect_norm2, s.Rational(1789, 500),
       "exact_same_flag_Julia_composition_defect_norm")
    require(julia_lie_defect_norm2 > 0,
            "relative_Julia_map_is_not_a_Lorentz_representation")
    julia_lie_defect_rank = julia_lie_defect.rank()
    require(julia_lie_defect_rank == 10,
            "same_flag_Julia_defect_rank_10")
    julia_anti_defect = s.simplify(XN * Xbar - Xbar * XN + XJ)
    julia_anti_defect_norm2 = s.simplify(
        s.trace(julia_anti_defect.H * julia_anti_defect)
    )
    eq(julia_anti_defect_norm2, s.Rational(1789, 500),
       "exact_reversed_order_Julia_defect_norm")
    require(julia_anti_defect_norm2 > 0,
            "reversed_order_does_not_restore_representation")

    # Reapply the same original full128 Kraus instrument at two assigned
    # Lorentz increments, retaining the fresh outcome after each round.
    # This is a matrix-program history test, not a claim that D0 physically
    # compiles either increment into an onsite memory word.
    def full128_kraus_and_tangent(generator, varying_role=2):
        G = sum(
            (generator[i, j] * C[i] * C[j].H
             for i in range(4) for j in range(4)),
            s.zeros(16),
        )
        words = []
        dwords = []
        for role in range(4):
            Qleft = C[role] * C[role].H
            Qright = C[role].H * C[role]
            P = nu * C[role] * z[role]
            L = I16 - s.Rational(1, 5) * Qleft
            R = I16 - s.Rational(1, 5) * Qright
            dP_role = (nu * C[role] * G * z[role]
                       if role == varying_role else s.zeros(16))
            if role == varying_role:
                rhs_left = -dP_role * P.H - P * dP_role.H
                rhs_right = -dP_role.H * P - P.H * dP_role
                dL_role = sylvester_at_base(Qleft, rhs_left)
                dR_role = sylvester_at_base(Qright, rhs_right)
                eq(L * dL_role + dL_role * L, rhs_left,
                   "sequential_left_Julia_root_tangent")
                eq(R * dR_role + dR_role * R, rhs_right,
                   "sequential_right_Julia_root_tangent")
            else:
                dL_role = s.zeros(16)
                dR_role = s.zeros(16)
            fixed_left = I16 - s.Rational(1, 5) * Qleft
            fixed_right = I16 - s.Rational(1, 5) * Qright
            items = (
                ((P, L), (dP_role, dL_role)),
                ((P.H, R), (dP_role.H, dR_role)),
                ((-nu * C[role], -fixed_left),
                 (s.zeros(16), s.zeros(16))),
                ((-nu * C[role].H, -fixed_right),
                 (s.zeros(16), s.zeros(16))),
            )
            for item, derivative in items:
                for _ in range(2):
                    words.append(item)
                    dwords.append(derivative)

        rows = []
        drows = []
        for label in range(32):
            signs = [s.Rational((-1) ** bin(label & j).count("1"), 32)
                     for j in range(32)]
            for coefficient in range(2):
                rows.append(sum(
                    (signs[j] * words[j][coefficient]
                     for j in range(32)), s.zeros(16)))
                drows.append(sum(
                    (signs[j] * dwords[j][coefficient]
                     for j in range(32)), s.zeros(16)))

        eq(rows[0], A, "sequential_blank_row_matches_owned_full128_A")
        base_kraus = []
        tangent = []
        dA_role = drows[0]
        a = s.sqrt(p)
        for row, drow in zip(rows, drows):
            port0 = (I16 if not base_kraus else s.zeros(16)) \
                - 2 * p**2 * row.H * A
            dport0 = -2 * p**2 * (drow.H * A + row.H * dA_role)
            port1 = -2 * a * p * row.H * A
            dport1 = -2 * a * p * (drow.H * A + row.H * dA_role)
            base_kraus.extend((port0, port1))
            tangent.extend((dport0, dport1))
        completeness = sum(
            (K.H * K for K in base_kraus), s.zeros(16))
        eq(completeness, I16, "sequential_original_full128_complete")
        return base_kraus, tangent

    seq_kraus, dseq_N2 = full128_kraus_and_tangent(N2)
    seq_kraus_bar, dseq_Nbar3 = full128_kraus_and_tangent(Nbar3)
    for index, (left, right) in enumerate(zip(seq_kraus, seq_kraus_bar)):
        eq(left, right, "sequential_shared_base_kraus_" + str(index))

    def selected_history_mixed_jet(first_tangent, second_tangent):
        # Event 0 = blank-label/coefficient-0/port-0. Event 19 is
        # label-4/coefficient-1/port-1 in the original 128-output round.
        first_base = seq_kraus[0]
        second_base = seq_kraus[19]
        first_derivative = first_tangent[0]
        second_derivative = second_tangent[19]
        total = second_base * first_base
        total_a = second_base * first_derivative
        total_b = second_derivative * first_base
        total_ab = second_derivative * first_derivative
        real = lambda value: s.simplify(
            (value + s.conjugate(value)) / 2)
        return s.simplify((
            real(s.trace(total.H * total_ab))
            + real(s.trace(total_a.H * total_b))
        ) / 8)

    sequential_AB_jet = selected_history_mixed_jet(
        dseq_N2, dseq_Nbar3)
    sequential_BA_jet = selected_history_mixed_jet(
        dseq_Nbar3, dseq_N2)
    sequential_order_jet = s.simplify(
        sequential_AB_jet - sequential_BA_jet)
    expected_sequential_BA = (
        -s.Rational(12640131, 3276800000000)
        + s.Rational(5746707, 3276800000000) * s.sqrt(5)
    )
    expected_sequential_order = (
        s.Rational(12640131, 3276800000000)
        - s.Rational(5746707, 3276800000000) * s.sqrt(5)
    )
    eq(sequential_AB_jet, 0,
       "fresh_record_selected_history_AB_mixed_jet")
    eq(sequential_BA_jet, expected_sequential_BA,
       "fresh_record_selected_history_BA_mixed_jet")
    eq(sequential_order_jet, expected_sequential_order,
       "fresh_record_selected_history_order_jet")
    require(sequential_order_jet.is_zero is False,
            "fresh_record_selected_history_reads_increment_order")

    # Use every original full128 outcome as a probability readout and vary all
    # four links independently along a full proper-Lorentz basis.  The matrix
    # below is exact over Q(sqrt(5)); it is not a floating-point rank test.
    probability_columns = []
    output_state_columns = []
    all24_tangent_kraus = []
    common_base_checked = False
    for role in range(4):
        for generator in lorentz_generators:
            base_kraus, tangent = full128_kraus_and_tangent(
                generator, varying_role=role)
            all24_tangent_kraus.append(tangent)
            tangent_completeness = sum(
                (K.H * dK + dK.H * K
                 for K, dK in zip(base_kraus, tangent)),
                s.zeros(16),
            )
            eq(tangent_completeness, s.zeros(16),
               "all24_full128_tangent_completeness")
            if not common_base_checked:
                require(all(
                    s.simplify(left - right) == s.zeros(16)
                    for left, right in zip(seq_kraus, base_kraus)
                ), "all24_shared_full128_base_kraus")
                common_base_checked = True
            probability_columns.append([
                s.simplify((s.trace(K.H * dK) + s.trace(dK.H * K)) / 16)
                for K, dK in zip(base_kraus, tangent)
            ])
            state_coordinates = []
            for K, dK in zip(base_kraus, tangent):
                d_state = (dK * K.H + K * dK.H) / 16
                state_coordinates.extend(
                    s.re(d_state[i, i]) for i in range(16)
                )
                for i in range(16):
                    for j in range(i + 1, 16):
                        entry = d_state[i, j]
                        state_coordinates.extend((
                            s.re(entry),
                            s.im(entry),
                        ))
            output_state_columns.append(state_coordinates)
    probability_jacobian = s.Matrix(
        128, 24,
        lambda row, column: probability_columns[column][row],
    )
    require(all(
        s.simplify(sum(probability_jacobian[row, column]
                       for row in range(128))) == 0
        for column in range(24)
    ), "all24_probability_tangents_conserve_total_probability")
    eq(
        probability_jacobian[0, 2 * 6 + 4],
        expected_source,
        "all24_jacobian_reproduces_existing_J23_pointer_source",
    )
    probability_rank = DomainMatrix.from_Matrix(probability_jacobian).convert_to(
        QQ.algebraic_field(s.sqrt(5))
    ).rank()
    require(probability_rank == 6,
            "all128_outcome_probability_jacobian_exact_rank_6_of_24")

    # Retaining each unnormalized conditional CAR output state contains more
    # than its scalar probability. Use a floating pivot only to select rows;
    # prove the resulting 24x24 minor exactly over Q(sqrt(5)) below.
    state_coordinate_count = 128 * 16 * 16
    require(all(len(column) == state_coordinate_count
                for column in output_state_columns),
            "all128_conditional_state_coordinates_complete")
    state_numeric = np.asarray([
        [float(s.N(value, 16)) for value in column]
        for column in output_state_columns
    ], dtype=np.float64).T
    _, triangular, pivot_rows = qr(
        state_numeric.T, mode="economic", pivoting=True, check_finite=False
    )
    pivot_rows = [int(index) for index in pivot_rows[:24]]
    state_minor = s.Matrix(
        24, 24,
        lambda row, column: s.simplify(
            output_state_columns[column][pivot_rows[row]]
        ),
    )
    output_state_rank = DomainMatrix.from_Matrix(state_minor).convert_to(
        QQ.algebraic_field(s.sqrt(5))
    ).rank()
    require(output_state_rank == 24,
            "all128_retained_conditional_states_exact_minor_rank_24_of_24")

    # Read the same 24 link directions through the ordinary classical record
    # after two fresh applications of the existing full128 instrument.  Each
    # link tangent is shared between the two rounds, as for one stationary
    # background; no state tomography or new effect is used.  QR only chooses
    # candidate history rows, whose 24x24 derivative minor is checked exactly.
    K_numeric = np.asarray([
        [[complex(s.N(value, 16)) for value in row] for row in K.tolist()]
        for K in base_kraus
    ], dtype=np.complex128)
    dK_numeric = np.asarray([
        [[[complex(s.N(value, 16)) for value in row] for row in dK.tolist()]
         for dK in tangent]
        for tangent in all24_tangent_kraus
    ], dtype=np.complex128)
    history_base = np.einsum(
        "kac,jcb->jkab", K_numeric, K_numeric, optimize=True
    )
    history_numeric = np.empty((128 * 128, 24), dtype=np.float64)
    for column, dK_column in enumerate(dK_numeric):
        history_tangent = (
            np.einsum("kac,jcb->jkab", dK_column, K_numeric,
                      optimize=True)
            + np.einsum("kac,jcb->jkab", K_numeric, dK_column,
                        optimize=True)
        )
        history_numeric[:, column] = (
            np.einsum("jkab,jkab->jk", history_base.conj(),
                      history_tangent, optimize=True).real / 8
        ).reshape(-1)
        del history_tangent
    _, history_triangular, history_pivot_rows = qr(
        history_numeric.T, mode="economic", pivoting=True,
        check_finite=False
    )
    history_pivot_rows = [int(index) for index in history_pivot_rows[:24]]

    def history_probability_derivative(flat_index, base_operators,
                                       tangent_operators):
        first, second = divmod(flat_index, 128)
        total = base_operators[second] * base_operators[first]
        dtotal = (
            tangent_operators[second] * base_operators[first]
            + base_operators[second] * tangent_operators[first]
        )
        contraction = s.trace(total.H * dtotal)
        return s.simplify(
            (contraction + s.conjugate(contraction)) / 16
        )

    history_minor = s.Matrix(
        24, 24,
        lambda row, column: history_probability_derivative(
            history_pivot_rows[row], base_kraus,
            all24_tangent_kraus[column]
        ),
    )
    history_rank = DomainMatrix.from_Matrix(history_minor).convert_to(
        QQ.algebraic_field(s.sqrt(5))
    ).rank()
    require(history_rank > 0,
            "two_round_full128_selected_history_minor_has_nonzero_rank")

    return {
        "status": "PASS",
        "exact_checks": len(checks),
        "checks": checks,
        "carrier": {
            "CAR": "all16 exterior components",
            "record": "original128 outcomes; selected scalar is port0/blank label",
            "reference": "reference128 retained as an untouched tensor factor",
            "preparation": "fixed system marginal I16/16",
        },
        "fixture": {
            "lattice": "L=4",
            "h": str(h),
            "Fourier_mode": "(0,0,0,1), phase i on role3",
            "moving_link": "role2: exp(a N2) exp(b Nbar3) versus reverse",
            "other_links": "identity",
            "coframe_weight": str(nu),
            "source": "full128 port0/blank-label probability",
        },
        "mixed_order_jet": str(q0_source),
        "mixed_order_jet_decimal": str(s.N(q0_source, 16)),
        "zero_mode_control": str(q0_zero_mode_source),
        "same_flag_Julia_lie_defect_norm_squared": str(julia_lie_defect_norm2),
        "same_flag_Julia_lie_defect_rank": julia_lie_defect_rank,
        "reversed_order_Julia_defect_norm_squared": str(
            julia_anti_defect_norm2
        ),
        "fresh_record_history": {
            "round_1_outcome_index": 0,
            "round_2_outcome_index": 19,
            "AB_mixed_jet": str(sequential_AB_jet),
            "BA_mixed_jet": str(sequential_BA_jet),
            "AB_minus_BA_mixed_jet": str(sequential_order_jet),
            "AB_minus_BA_decimal": str(s.N(sequential_order_jet, 16)),
        },
        "all24_link_probability_jacobian": {
            "directions": "four independent links times six proper-Lorentz generators",
            "outcomes": 128,
            "exact_rank_over_Q_sqrt5": probability_rank,
            "nullity": 24 - probability_rank,
            "background": "L=4; Fourier phases (1,1,1,i)",
            "preparation": "I16/16 with the original reference128 as spectator",
        },
        "all128_conditional_output_state_jacobian": {
            "directions": 24,
            "real_coordinates": state_coordinate_count,
            "exact_rank_over_Q_sqrt5": output_state_rank,
            "nullity": 24 - output_state_rank,
            "exact_minor_coordinate_rows": pivot_rows,
            "numeric_pivot_min_diagonal": float(min(
                abs(triangular[i, i]) for i in range(24)
            )),
            "retained_object": "all 128 unnormalized conditional CAR16 states",
        },
        "two_round_full128_probability_jacobian": {
            "directions": "four shared link roles times six proper-Lorentz generators",
            "outcome_histories": 128 * 128,
            "selected_minor_dimension": 24,
            "selected_minor_exact_rank_over_Q_sqrt5": history_rank,
            "verified_full_jacobian_rank_lower_bound": history_rank,
            "numeric_rank": int(np.linalg.matrix_rank(history_numeric)),
            "exact_minor_history_rows": history_pivot_rows,
            "numeric_pivot_min_diagonal": float(
                min(abs(history_triangular[i, i]) for i in range(24))
            ),
            "preparation": "I16/16 with the original reference128 as spectator",
            "retained_object": "all ordered pairs of original full128 outcomes",
        },
        "scope": {
            "endpoint_link_order_readout": True,
            "chosen_two_round_full128_history_order_readout": True,
            "relative_same_flag_Julia_map_is_a_representation": False,
            "physical_admission_of_this_probe": False,
            "sequential_memory_word_execution": False,
            "Julia_dilation_composition_compatibility": False,
            "native_Cost_Info_selection": False,
            "positive_GR_closure": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
