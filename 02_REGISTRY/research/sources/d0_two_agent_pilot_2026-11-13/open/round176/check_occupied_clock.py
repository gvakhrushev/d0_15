"""Exact occupied-input obstruction and marked Book03 cyclic invariant."""

from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from runpy import run_path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round121"))
from check_book03_identity_pair import BOOK03, REPO, actual_words, ne, require

OWNER = REPO / "04_CERTIFICATES" / "order_memory_control_verify.py"
sys.path.insert(0, str(OWNER.parent))


def occupied_test():
    words = actual_words()
    echo = words["G_Z_G_Z"]
    plain = words["CX_18"]
    p, a = ne.P, ne.A
    spin = sp.eye(4)
    initial = sp.kronecker_product(sp.Matrix([1, 0]), sp.Matrix([a, p]), spin)

    def execute(word):
        state = initial
        prefixes = [initial]
        for gate in word:
            execution = ne.Execution(4, (), (), (gate,), ne.G_CX_SOURCE_I, 0, (2, 3))
            matrix = ne.word_matrix(execution, max_qubits=4, max_expanded_stages=1)
            state = matrix * state
            prefixes.append(state)
        return prefixes

    require(len(echo) == 18 and len(plain) == 18, "Words changed length")
    require((echo[0].op, echo[0].wires) == ("G", (1,)), "First letter changed")
    require(
        [(gate.op, gate.wires) for gate in echo[16:]] == [("CX", (1, 0)), ("CX", (0, 1))],
        "Closing CX letters changed",
    )
    states = execute(echo)
    for actual, expected in (
        (states[16], sp.kronecker_product(sp.Matrix([a, 0, 0, p]), spin)),
        (states[17], initial),
        (states[18], initial),
        (execute(plain)[18], initial),
        (states[0].T * states[16], p * spin),
        (states[1].T * states[17], a * spin),
    ):
        require(ne.exact_matrix_equal(actual, expected), "Wrong occupied prefix or Gram matrix")

    wrapped = execute(echo[:16] + echo[:2])[18]
    port_one = sp.diag(sp.zeros(8), sp.eye(8))
    require(ne.exact_matrix_equal(wrapped.T * port_one * wrapped, p**2 * spin),
            "Reloaded 16-slot clock must leak into PORT=1")
    require(ne.exact_matrix_equal(states[18].T * port_one * states[18], sp.zeros(4)),
            "Literal endpoint must retain PORT=0")

    epsilon = 2 * sp.sin((sp.acos(p) - sp.acos(a)) / 6)
    return {
        "occupied_spin_dimension": 4,
        "clock_address_collision": [1, 17],
        "gram_before": "p I4",
        "gram_after": "sqrt(p) I4",
        "canonical_fibre_prefix_error_lower_bound": "2 sin((acos(p)-acos(sqrt(p)))/6)",
        "canonical_fibre_prefix_error_lower_bound_approx": str(epsilon.evalf(16)),
        "clean_unchanged_lap_tags_must_be_orthogonal": True,
        "changed_lap_tags_squared_overlap_ratio": "p (output / input)",
        "literal_reload_port_one_probability": "p^2",
        "required_port_one_probability": "0",
    }


def marked_clock_test():
    with redirect_stdout(StringIO()):
        owner = run_path(str(OWNER))
    p = owner["p"]
    gates, program = owner["gates"], owner["program"]
    reduce, reduced = owner["reduce"], owner["reduced"]

    def monodromy(word):
        product = sp.eye(16)
        for name in program(word) + ["idle"]:
            product = reduced(gates[name] * product)
        return product

    identity = monodromy(owner["identity_word"])
    order = monodromy(owner["order_word"])
    lam = sp.Symbol("lambda")
    char_identity = (lam - 1)**12 * (lam + 1)**4
    char_order = (lam - 1)**4 * (lam + 1)**4 * (lam**2 - 2*p**3*lam + 1)**4
    for matrix, expected in ((identity, char_identity), (order, char_order)):
        difference = sp.Poly(matrix.charpoly(lam).as_expr() - expected, lam)
        require(all(reduce(coefficient) == 0 for coefficient in difference.all_coeffs()),
                "Charpoly of the original marked cycle changed")
    require(sp.trace(identity) == 8, "Incorrect identity cycle trace")
    require(reduce(sp.trace(order) - 8*p**3) == 0, "Incorrect order cycle trace")
    return {
        "executed_stages_before_terminal": 15,
        "formal_idle_wrap_stage": 16,
        "marked_trace_of_W_power_16": ["128", "128 p^3"],
        "marked_monodromy_characteristic_polynomials": [
            "(lambda-1)^12 (lambda+1)^4",
            "(lambda-1)^4 (lambda+1)^4 (lambda^2-2 p^3 lambda+1)^4",
        ],
    }


def main():
    word_owner = HERE.parent / "round121" / "check_book03_identity_pair.py"
    result = {
        "status": "PASS",
        "source_sha256": {
            str(path.relative_to(REPO)): sha256(path.read_bytes()).hexdigest()
            for path in (BOOK03, OWNER, word_owner)
        },
        "B121_occupied_test": occupied_test(),
        "original_X_Y_marked_cycle": marked_clock_test(),
        "absolute_book_preparation_response_determined_by_exchange": False,
        "GR_closed": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
