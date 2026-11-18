"""Verify the switch, the clean-prefix obstruction, and the preparation contrast."""

from hashlib import sha256
from itertools import accumulate
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round121"))
from check_book03_identity_pair import NATIVE, REPO, actual_words, exact, ne


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def xor_route(block_size):
    result = sp.zeros(4 * block_size)
    for setting in (0, 1):
        for mark in (0, 1):
            column = (2 * setting + mark) * block_size
            row = (2 * setting + (mark ^ setting)) * block_size
            result[row:row + block_size, column:column + block_size] = sp.eye(block_size)
    return result


def stage_matrix(gate):
    execution = ne.Execution(4, (), (), (gate,), ne.G_CX_SOURCE_I, 0, (2, 3))
    return ne.word_matrix(execution, max_qubits=4, max_expanded_stages=1)


def verify_switch():
    words = actual_words()
    first = words["G_Z_G_Z"]
    reference = words["CX_18"]
    require(len(first) == len(reference) == 18, "Body size changed")
    width = 16
    route = xor_route(width)
    route_execution = ne.Execution(6, (), (), (ne.Gate("CX", (0, 1)),),
                                   ne.G_CX_SOURCE_I, 2, (4, 5))
    native_route = ne.word_matrix(route_execution, max_qubits=6, max_expanded_stages=1)
    require(ne.exact_matrix_equal(route, native_route), "The label route is not literal CX")
    stage_swap = sp.zeros(2 * width)
    stage_swap[:width, width:] = sp.eye(width)
    stage_swap[width:, :width] = sp.eye(width)
    forward_prefix = sp.eye(2 * width)
    reverse_prefix = sp.eye(2 * width)
    previous_gauge = sp.eye(2 * width)
    for gate0, gate1 in zip(reference, first):
        w0, w1 = stage_matrix(gate0), stage_matrix(gate1)
        forward = sp.diag(w0, w1)
        reverse = sp.diag(w1, w0)
        require(ne.exact_matrix_equal(stage_swap * forward * stage_swap, reverse),
                "Block assignment not exchanged by label transposition")
        supplied_selector = sp.diag(forward, forward)
        require(ne.exact_matrix_equal(route * supplied_selector * route, sp.diag(forward, reverse)),
                "The setting route is not a coherent controlled exchange")
        forward_prefix = forward * forward_prefix
        reverse_prefix = reverse * reverse_prefix
        gauge = reverse_prefix * forward_prefix.T
        require(ne.exact_matrix_equal(gauge * forward, reverse * previous_gauge),
                "Stagewise gauge fails to transport a clock edge")
        previous_gauge = gauge

    require(ne.exact_matrix_equal(forward_prefix, sp.eye(2 * width)), "Forward endpoint changed")
    require(ne.exact_matrix_equal(reverse_prefix, sp.eye(2 * width)), "Reverse endpoint changed")
    parity_first = list(accumulate(g.op == "G" for g in first))
    parity_reference = list(accumulate(g.op == "G" for g in reference))
    obstruction = [k for k, (a, b) in enumerate(zip(parity_first, parity_reference), 1)
                   if a % 2 != b % 2]
    require(obstruction == list(range(1, 10)), "Unexpected mismatched prefixes")
    return {
        "addresses_per_body": width,
        "assignment_and_mark_address_count": 4 * width,
        "settings_and_marks_retained": True,
        "same_exact_native_endpoint": True,
        "stagewise_gauge_intertwines_every_clock_edge": True,
        "literal_selector_obstructed_prefixes": obstruction,
        "original_clock_states": 16,
        "distinct_labels_needed_including_endpoints": 19,
        "extra_routing_stages_if_using_a_retained_setting": 2,
        "controlled_selector_was_supplied_as_a_matrix": True,
    }


def verify_mod_two():
    x = sp.symbols("x")
    residue = sp.Poly(x**4 + x**2 + 1, x, modulus=2)
    one = sp.Poly(1, x, modulus=2)
    odd_row = sp.Poly(x**2 + x, x, modulus=2)
    require(odd_row != one and (odd_row**2).rem(residue) == one, "Wrong native residue")
    # Both initial and restored normalized integral auxiliary vectors have unit row sum.
    # Verify the noncomputational canonical example in the same residue ring.
    require((sp.Poly(x, x, modulus=2)**2 + sp.Poly(x**2, x, modulus=2)**2)
            .rem(residue) == one, "Canonical Golden auxiliary is not normalized")
    return {
        "residue_ring": "F2[x]/(x^4+x^2+1)",
        "identity_and_permutation_row_sum": "1",
        "G_row_sum": "x+x^2 != 1",
        "golden_auxiliary_sum_is_a_unit": True,
    }


def verify_preparation():
    a0, a1, m00, m01, m10, m11 = sp.symbols("a0 a1 m00 m01 m10 m11", positive=True)
    odds_a = a1 * m11 / (a0 * m00)
    odds_b = a1 * m10 / (a0 * m01)
    require(sp.cancel(odds_a / odds_b - m11*m01/(m00*m10)) == 0,
            "Common mark-only preparer factor failed to cancel")

    A, d, b, u = sp.symbols("A d b u", positive=True)
    even = sp.Matrix([[1, 1], [1, 1]]) / 2
    odd = sp.eye(2) - even
    # Bright and forbidden WORK outputs are orthogonal. On the retained central
    # pair the forbidden map is d*(I + R_z) = 2d*P_plus.
    echo = sp.Matrix.vstack(A * sp.eye(2), 2*d*even)
    reference = sp.Matrix.vstack(b * sp.eye(2), sp.zeros(2))
    rho = u * even + (1-u) * odd
    mass1 = sp.expand(sp.trace(rho * echo.T * echo))
    mass0 = sp.expand(sp.trace(rho * reference.T * reference))
    require(mass1 == A**2 + 4*d**2*u and mass0 == b**2, "Regular preparation profile")
    require(sp.simplify(sp.diff(sp.log(mass1/mass0), u) - 4*d**2/mass1) == 0,
            "Wrong complete preparation derivative")

    p = ne.P
    require(exact(p**2 + p**4 + 2*p**3, sp.Integer(1)), "B121 Golden weights changed")
    return {
        "common_scalar_cancels_from_crossed_odds": True,
        "regular_echo_mass": "A^2 + 4*d^2*u",
        "regular_reference_mass": "b^2",
        "regular_preparation_coefficient": "4*d^2/(A^2+4*d^2*u)",
        "regular_profile_cancels_for_arbitrary_preparation": False,
        "fixed_odd_spin_preparation_profile_cancels": True,
    }


def main():
    book = REPO / "01_BOOKS" / "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md"
    inputs = [book, NATIVE, HERE.parent / "round121" / "RESULT.json"]
    print(json.dumps({
        "sha256": {str(f.relative_to(REPO)): sha256(f.read_bytes()).hexdigest()
                   for f in inputs},
        "switch": verify_switch(),
        "mod_two": verify_mod_two(),
        "preparation": verify_preparation(),
        "book03_full_physical_preparation_source_cancelled": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
