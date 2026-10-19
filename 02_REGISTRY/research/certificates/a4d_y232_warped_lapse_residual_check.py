#!/usr/bin/env python3
"""Exact #232 warped-lapse control and all-order first-variation obstruction."""
from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import sympy as sp
import numpy as np
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


OWNER_PATH = Path(__file__).with_name("a4d_y_slow_exact_plane_check.py")
SPEC = spec_from_file_location("a4d_y_slow_exact_plane_owner", OWNER_PATH)
assert SPEC is not None and SPEC.loader is not None
OWNER = module_from_spec(SPEC)
SPEC.loader.exec_module(OWNER)
STENCIL_PATH = Path(__file__).with_name("a4d_y_curved_joint_rational_stencil.py")
STENCIL_SPEC = spec_from_file_location("a4d_y_curved_joint_rational_stencil_owner", STENCIL_PATH)
assert STENCIL_SPEC is not None and STENCIL_SPEC.loader is not None
STENCIL = module_from_spec(STENCIL_SPEC)
STENCIL_SPEC.loader.exec_module(STENCIL)


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print(f"PASS_{name}", flush=True)


def exact_rank(matrix: sp.MatrixBase) -> int:
    return len(DomainMatrix.from_Matrix(sp.Matrix(matrix)).convert_to(QQ).rref()[1])


def stencil_matrix(terms, row_count: int, moment_axis: int | None = None) -> sp.Matrix:
    result = sp.zeros(row_count, 96)
    for shift, entries in terms.items():
        weight = 1 if moment_axis is None else shift[moment_axis]
        if not weight:
            continue
        for (row, col), value in entries.items():
            result[row, col] += weight * sp.Rational(value.numerator, value.denominator)
    return result


def first_order_joint_gate() -> None:
    # The exact z=1 Laurent owner supplies the period-four connection and
    # phase-resolved metric Jacobians. Its first shift moment is the slow
    # derivative in lattice direction x^1.
    A0 = stencil_matrix(STENCIL.ATERMS, 96)
    A1 = stencil_matrix(STENCIL.ATERMS, 96, moment_axis=1)
    Q0 = stencil_matrix(STENCIL.QTERMS, 40)
    Q1 = stencil_matrix(STENCIL.QTERMS, 40, moment_axis=1)

    Y = OWNER.GEN[3] - OWNER.GEN[4] + OWNER.GEN[5]
    z = sp.symbols("z", real=True)
    U_z = OWNER.cayley_simple(Y, 3, z)
    y_right_log = (OWNER.linv(U_z) * sp.diff(U_z, z)).subs(z, 1).applyfunc(sp.factor)
    y_tangent = sp.zeros(96, 1)
    for generator_index, (a, b) in enumerate(OWNER.PAIRS):
        y_tangent[STENCIL.IDX[(0, 0, generator_index)]] = y_right_log[a, b]
        y_tangent[STENCIL.IDX[(2, 0, generator_index)]] = -y_right_log[a, b]

    # The independent boost-dual center is the exact d-derivative of
    # U*Cayley(B,-d), U^-1*Cayley(B,+d), B=K_01+K_02+K_03.
    boost_dual = OWNER.GEN[0] + OWNER.GEN[1] + OWNER.GEN[2]
    dual_tangent = sp.zeros(96, 1)
    for generator_index, (a, b) in enumerate(OWNER.PAIRS):
        dual_tangent[STENCIL.IDX[(0, 0, generator_index)]] = -boost_dual[a, b]
        dual_tangent[STENCIL.IDX[(2, 0, generator_index)]] = boost_dual[a, b]
    centers = sp.Matrix.hstack(y_tangent, dual_tangent)

    check("FLAT_CONNECTION_RANK_94", exact_rank(A0) == 94)
    check("TWO_EXACT_CENTER_TANGENTS", exact_rank(centers) == 2 and A0 * centers == sp.zeros(96, 2))

    # The direct warped-lapse replay above gives these two connection rows at
    # each phase, with coefficient N_(n-1)-N_n. The sign/scale is immaterial
    # to the compatibility test, so normalize that coefficient to one.
    lapse_forcing = sp.zeros(96, 1)
    for phase in range(4):
        lapse_forcing[STENCIL.IDX[(phase, 2, 3)]] = 1
        lapse_forcing[STENCIL.IDX[(phase, 3, 4)]] = 1

    # Three phase differences per Gram component must vanish for any source
    # that is smooth and phase-common on this four-cell control.
    phase_difference = sp.zeros(30, 40)
    for component in range(10):
        for phase in (1, 2, 3):
            row = 10 * (phase - 1) + component
            phase_difference[row, 10 * phase + component] = 1
            phase_difference[row, component] = -1

    base = A0.col_join(phase_difference * Q0)
    slow_center = (A1 * centers).col_join(phase_difference * Q1 * centers)
    augmented = base.row_join(slow_center)
    rhs = (-lapse_forcing).col_join(sp.zeros(30, 1))
    rank_base = exact_rank(base)
    rank_with_centers = exact_rank(augmented)
    rank_with_forcing = exact_rank(augmented.row_join(rhs))
    check("JOINT_ZERO_SLOW_RANK_95", rank_base == 95)
    check("JOINT_WITH_BOTH_CENTER_SLOPES_RANK_97", rank_with_centers == 97)
    check("LAPSE_FORCING_RAISES_RANK_TO_98", rank_with_forcing == 98)

    # Produce an exact left-null witness for the rank obstruction, rather
    # than relying only on two separately reported ranks.
    reduced, pivots = DomainMatrix.from_Matrix(augmented.T).convert_to(QQ).rref()
    reduced = reduced.to_Matrix()
    pivot_set = set(pivots)
    witness = None
    for free_col in range(augmented.rows):
        if free_col in pivot_set:
            continue
        candidate = sp.zeros(augmented.rows, 1)
        candidate[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            candidate[pivot_col] = -reduced[row, free_col]
        pairing = sp.factor((candidate.T * rhs)[0])
        if pairing != 0:
            witness = candidate
            break
    check("LEFT_NULL_WITNESS_ANNIHILATES_ALL_CORRECTORS", witness is not None and augmented.T * witness == sp.zeros(98, 1))
    pairing = sp.factor((witness.T * rhs)[0]) if witness is not None else 0
    check("LEFT_NULL_WITNESS_SEES_LAPSE_FORCING", pairing != 0)
    print(f"FIRST_ORDER_RANKS: base={rank_base}, with_centers={rank_with_centers}, with_forcing={rank_with_forcing}")
    print(f"FIRST_ORDER_LEFT_NULL_PAIRING: {pairing}")


def modular_rank(matrix: np.ndarray, prime: int) -> int:
    """Exact Gaussian rank over a prime field; products stay below int64 range."""
    work = np.array(matrix, dtype=np.int64, copy=True) % prime
    row_count, col_count = work.shape
    rank = 0
    for col in range(col_count):
        if rank == row_count:
            break
        nonzero = np.flatnonzero(work[rank:, col])
        if len(nonzero) == 0:
            continue
        pivot = rank + int(nonzero[0])
        if pivot != rank:
            work[[rank, pivot]] = work[[pivot, rank]]
        inverse = pow(int(work[rank, col]), prime - 2, prime)
        work[rank, :] = (work[rank, :] * inverse) % prime
        affected = np.flatnonzero(work[rank + 1:, col]) + rank + 1
        if len(affected):
            multipliers = work[affected, col].copy()
            work[affected, :] = (
                work[affected, :] - multipliers[:, None] * work[rank, :][None, :]
            ) % prime
        rank += 1
    return rank


def finite_character_gate() -> None:
    # Exact reduction of the linearized source problem at roots of unity.
    # A full-rank augmented matrix modulo a good prime proves inconsistency
    # over the corresponding characteristic-zero cyclotomic field.
    prime = 1_000_033
    generator = 5
    orders = (4, 8, 12, 16, 24, 32, 44, 48, 88, 96, 132, 176, 264, 352, 528, 1056)
    check("FINITE_FIELD_PRIME", sp.isprime(prime) and prime % 14 != 0)
    check("FINITE_FIELD_GENERATOR", all(
        pow(generator, (prime - 1) // q, prime) != 1
        for q in sp.factorint(prime - 1)
    ))

    phase_difference = np.zeros((30, 40), dtype=np.int64)
    for component in range(10):
        for phase in (1, 2, 3):
            row = 10 * (phase - 1) + component
            phase_difference[row, 10 * phase + component] = 1
            phase_difference[row, component] = -1
    forcing = np.zeros(96, dtype=np.int64)
    for phase in range(4):
        forcing[STENCIL.IDX[(phase, 2, 3)]] = 1
        forcing[STENCIL.IDX[(phase, 3, 4)]] = 1

    records = []
    for order in orders:
        check(f"ORDER_DIVIDES_FIELD_{order}", (prime - 1) % order == 0)
        root = pow(generator, (prime - 1) // order, prime)
        check(f"ROOT_HAS_EXACT_ORDER_{order}", pow(root, order, prime) == 1 and all(
            pow(root, order // q, prime) != 1 for q in sp.factorint(order)
        ))

        connection = np.zeros((96, 96), dtype=np.int64)
        metric = np.zeros((40, 96), dtype=np.int64)
        denominators_clear = True
        for shift, entries in STENCIL.ATERMS.items():
            phase_factor = pow(root, shift[1], prime)
            for (row, col), value in entries.items():
                cleared = 14 * value
                denominators_clear = denominators_clear and cleared.denominator == 1
                connection[row, col] += cleared.numerator * phase_factor
        for shift, entries in STENCIL.QTERMS.items():
            phase_factor = pow(root, shift[1], prime)
            for (row, col), value in entries.items():
                cleared = 14 * value
                denominators_clear = denominators_clear and cleared.denominator == 1
                metric[row, col] += cleared.numerator * phase_factor
        check(f"DENOMINATORS_CLEARED_{order}", denominators_clear)
        connection %= prime
        metric %= prime
        system = np.vstack((connection, phase_difference @ metric % prime)) % prime
        rhs = np.zeros(126, dtype=np.int64)
        rhs[:96] = (14 * (1 - pow(root, -1, prime)) * forcing) % prime
        rank_system = modular_rank(system, prime)
        rank_augmented = modular_rank(np.column_stack((system, rhs)), prime)
        check(f"SOURCE_INCOMPATIBLE_AT_ORDER_{order}", rank_system == 96 and rank_augmented == 97)
        records.append((order, rank_system, rank_augmented))
    print("FINITE_CYCLOTOMIC_RANKS:", records)


def all_root_of_unity_gate() -> None:
    """Certify first-order incompatibility at every nonconstant periodic mode.

    A fixed 97-by-97 minor has degree at most 141 after clearing Laurent
    powers row by row. Thus any root-of-unity zero has order n with
    phi(n) <= 141, hence n <= 2*141^2. Two integer minors cover every such
    order by exact reductions at primitive roots in suitable prime fields.
    """
    prime = 1_000_033
    terms: dict[tuple[int, int, int], int] = {}
    denominators_clear = True

    def add(row: int, col: int, exponent: int, value: int) -> None:
        if value:
            key = (row, col, exponent)
            terms[key] = terms.get(key, 0) + int(value)

    # Integerize the exact Laurent stencil. The last column is the lapse
    # forcing; the first 96 are connection corrections.
    for shift, entries in STENCIL.ATERMS.items():
        for (row, col), value in entries.items():
            scaled = 14 * sp.Rational(value.numerator, value.denominator)
            denominators_clear = denominators_clear and scaled.q == 1
            add(row, col, shift[1], scaled.p)

    # Append the 30 equations requiring phase-independent metric output:
    # Q(phase)-Q(phase 0)=0, three rows for each of ten packed components.
    for shift, entries in STENCIL.QTERMS.items():
        for (metric_row, col), value in entries.items():
            scaled = 14 * sp.Rational(value.numerator, value.denominator)
            denominators_clear = denominators_clear and scaled.q == 1
            phase, component = divmod(metric_row, 10)
            if phase:
                add(96 + 10 * (phase - 1) + component, col, shift[1], scaled.p)
            else:
                for target_phase in (1, 2, 3):
                    add(96 + 10 * (target_phase - 1) + component, col, shift[1], -scaled.p)

    forcing = sp.zeros(96, 1)
    for phase in range(4):
        forcing[STENCIL.IDX[(phase, 2, 3)]] = 1
        forcing[STENCIL.IDX[(phase, 3, 4)]] = 1
    for row in range(96):
        if forcing[row]:
            add(row, 96, 0, 14)
            add(row, 96, -1, -14)

    terms = {key: value for key, value in terms.items() if value}
    check("ALL_ORDER_STENCIL_DENOMINATORS_CLEAR", denominators_clear)
    row_min: list[int | None] = [None] * 126
    row_max: list[int | None] = [None] * 126
    for (row, _col, exponent), _value in terms.items():
        row_min[row] = exponent if row_min[row] is None else min(row_min[row], exponent)
        row_max[row] = exponent if row_max[row] is None else max(row_max[row], exponent)
    require_rows = tuple(range(97))
    check(
        "ALL_ORDER_MINOR_ROWS_NONEMPTY",
        all(row_min[row] is not None and row_max[row] is not None for row in require_rows),
    )
    row_degree = [int(row_max[row] - row_min[row]) for row in require_rows]
    degree_bound = sum(row_degree)
    check("ALL_ORDER_FIRST_MINOR_DEGREE_BOUND_141", degree_bound == 141)

    # The second minor is selected by exact rank at the two orders where the
    # first minor did not certify nonvanishing. Both row sets are fixed here.
    minor_rows = (tuple(range(97)), tuple(range(95)) + (96, 97))

    def minor_at(root: int, field: int, rows: tuple[int, ...]) -> np.ndarray:
        positions = {row: index for index, row in enumerate(rows)}
        matrix = np.zeros((97, 97), dtype=np.int64)
        for (row, col, exponent), value in terms.items():
            if row in positions and col < 97:
                power = exponent - int(row_min[row])
                matrix[positions[row], col] = (
                    matrix[positions[row], col] + value * pow(root, power, field)
                ) % field
        return matrix

    def prime_for_order(order: int) -> int:
        multiplier = max(1, 15 // order)
        while True:
            candidate = multiplier * order + 1
            if candidate > 14 and sp.isprime(candidate):
                return int(candidate)
            multiplier += 1

    def smallest_primitive_root(field: int) -> int:
        factors = tuple(sp.factorint(field - 1))
        for candidate in range(2, field):
            if all(pow(candidate, (field - 1) // factor, field) != 1 for factor in factors):
                return candidate
        raise AssertionError("prime field has no primitive root")

    # Show that the first minor is a nonzero integer polynomial.
    check("ALL_ORDER_BASE_FIELD_PRIME", sp.isprime(prime) and prime > 14)
    check(
        "ALL_ORDER_FIRST_MINOR_NONZERO_POLYNOMIAL",
        modular_rank(minor_at(2, prime, minor_rows[0]), prime) == 97,
    )

    # phi(n) >= sqrt(n/2), so only this finite set can divide the first
    # minor. A common root of unity would make every maximal minor vanish.
    order_limit = 2 * degree_bound * degree_bound
    totients = list(range(order_limit + 1))
    for candidate in range(2, order_limit + 1):
        if totients[candidate] == candidate:
            for multiple in range(candidate, order_limit + 1, candidate):
                totients[multiple] -= totients[multiple] // candidate
    orders = [order for order in range(2, order_limit + 1) if totients[order] <= degree_bound]
    check("ALL_ORDER_CANDIDATE_SET_268", len(orders) == 268 and max(orders) == 510)

    rank_deficient_residues = [[], []]
    uncovered = []
    fields_valid = True
    roots_valid = True
    for order in orders:
        field = prime_for_order(order)
        fields_valid = fields_valid and sp.isprime(field) and field > 14 and (field - 1) % order == 0
        generator = smallest_primitive_root(field)
        root = pow(generator, (field - 1) // order, field)
        exact_order = pow(root, order, field) == 1 and all(
            pow(root, order // factor, field) != 1 for factor in sp.factorint(order)
        )
        roots_valid = roots_valid and exact_order
        minor_ranks = [
            modular_rank(minor_at(root, field, rows), field) for rows in minor_rows
        ]
        for index, rank in enumerate(minor_ranks):
            if rank < 97:
                rank_deficient_residues[index].append(order)
        if max(minor_ranks) < 97:
            uncovered.append(order)

    check("ALL_NONCONSTANT_ROOTS_OF_UNITY_COVERED", not uncovered)
    check("ALL_ORDER_PRIME_ROOT_REDUCTIONS_VALID", fields_valid and roots_valid)
    print(
        "ALL_ORDER_CYCLOTOMIC_CERTIFICATE:",
        {
            "degree_bound": degree_bound,
            "candidate_orders": len(orders),
            "max_candidate_order": max(orders),
            "minor_1_rank_deficient_residues": rank_deficient_residues[0],
            "minor_2_rank_deficient_residues": rank_deficient_residues[1],
            "uncovered_orders": uncovered,
        },
    )


def main() -> None:
    # This is the literal #232 generator and its pinned Cayley point.
    Y = OWNER.GEN[3] - OWNER.GEN[4] + OWNER.GEN[5]
    U = OWNER.I4 + sp.Rational(4, 7) * Y + sp.Rational(2, 7) * (Y * Y)
    check("Y_CAYLEY_LORENTZ", OWNER.reduced(U * OWNER.linv(U)) == OWNER.I4)

    wave = [U, OWNER.I4, OWNER.linv(U), OWNER.I4]

    def link(site, role):
        return wave[sum(site) % 4] if role == 0 else OWNER.I4

    # First replay the mandatory flat #232 joint vacuum control.
    flat_solder = lambda _site: OWNER.I4
    for phase in range(4):
        site = (phase, 0, 0, 0)
        check(f"FLAT_PHASE_{phase}_SOLDER", OWNER.solder_euler(flat_solder, link, site) == sp.zeros(4))
        check(
            f"FLAT_PHASE_{phase}_CONNECTION",
            all(OWNER.edge_euler(flat_solder, link, site, role, generator) == 0
                for role in range(4) for generator in OWNER.GEN),
        )

    # Hold the transverse coordinate fixed and vary only the smooth lapse
    # samples N_n in e^0=N(x^1)e^0_flat.  All four fast phases are represented
    # by changing x^0, not by changing the slow x^1 coordinate.
    N = {n: sp.symbols(f"N_{n}", real=True) for n in range(-4, 5)}

    def solder(site):
        result = OWNER.I4.copy()
        result[0, 0] = N[site[1]]
        return result

    expected = {
        (2, 3): N[-1] - N[0],  # role 2, internal J_12
        (3, 4): N[-1] - N[0],  # role 3, internal J_13
    }
    for phase in range(4):
        site = (phase, 0, 0, 0)
        check(f"WARPED_PHASE_{phase}_ALL_16_SOLDER_ROWS", OWNER.solder_euler(solder, link, site) == sp.zeros(4))
        actual = {}
        for role in range(4):
            for generator_index, generator in enumerate(OWNER.GEN):
                value = sp.factor(OWNER.edge_euler(solder, link, site, role, generator))
                if value != 0:
                    actual[(role, generator_index)] = value
        check(f"WARPED_PHASE_{phase}_EXACT_CONNECTION_ROWS", actual == expected)

    # A constant lapse is still the exact #232 root; only its spatial
    # variation creates the two displayed connection residuals.
    constant_profile = {value: sp.Integer(1) for value in N.values()}
    check("CONSTANT_LAPSE_RESIDUAL_ZERO", all(
        value.subs(constant_profile) == 0 for value in expected.values()))
    print("RESULT: only E_omega(role 2,J_12)=E_omega(role 3,J_13)=N_{-1}-N_0 remain.")
    first_order_joint_gate()
    finite_character_gate()
    all_root_of_unity_gate()
    print("SCOPE: no regular phase-common first-order lift; nonregular exact roots and response gaps remain open.")


if __name__ == "__main__":
    main()
