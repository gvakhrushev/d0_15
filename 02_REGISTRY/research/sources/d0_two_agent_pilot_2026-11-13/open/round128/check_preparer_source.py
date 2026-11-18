"""Check the original clock conflict, early effects, and preparer marginal identity."""

import json
from hashlib import sha256
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round122"))
from check_preparer_crossover import (
    REPO, actual_words, exact, ne, require, stage_matrix,
)


def verify_words():
    words = actual_words()
    plain = words["CX_18"]
    echo = words["G_Z_G_Z"]
    require(len(plain) == len(echo) == 18, "The words changed length")
    clock_size = 16
    first, wrapped = 1, 17
    require((first - 1) % clock_size == (wrapped - 1) % clock_size,
            "The two ticks do not use the same original clock address")
    require(echo[first - 1].op == "G" and echo[wrapped - 1].op == "CX",
            "The actual wrap witness changed")
    require(not ne.exact_matrix_equal(stage_matrix(echo[first - 1]), stage_matrix(echo[wrapped - 1])),
            "The wrapped stages demand the same matrix")
    for word in (plain, echo):
        execution = ne.Execution(4, (), (), word, ne.G_CX_SOURCE_I, 0, (2, 3))
        full = ne.word_matrix(execution, max_qubits=4, max_expanded_stages=18)
        require(ne.exact_matrix_equal(full, sp.eye(16)), "The full-word endpoint changed")
    p, a = ne.P, ne.A
    spin = sp.eye(4)[:, 0]
    zero = sp.kronecker_product(sp.Matrix([1, 0, 0, 0]), spin)
    golden = sp.kronecker_product(sp.Matrix([a, p, 0, 0]), spin)
    marked = sp.diag(*[int(bool((column // 4) % 2)) for column in range(16)])
    for vector, expected in ((zero, (0, p**2)), (golden, (1-p, 1-p**6))):
        for word, value in zip((plain, echo), expected):
            state = stage_matrix(word[0]) * vector
            require(exact((state.T * marked * state)[0], value),
                    "First fine mark probability changed")
    return {
        "clock_labels": clock_size,
        "contradictory_ticks": [first, wrapped],
        "conflicting_operations": [echo[first - 1].op, echo[wrapped - 1].op],
        "both_full_endpoints": "I_16",
        "target_zero_after_first_tick_on_golden_input": ["p", "p^6"],
    }


def verify_preparer():
    r, dr, a, d, b = sp.symbols("r dr A d b", positive=True)
    even = sp.Matrix([[1, 1], [1, 1]]) / 2
    odd = sp.eye(2) - even
    rho = r * even + (1-r) * odd
    rho_sqrt = sp.sqrt(r) * even + sp.sqrt(1-r) * odd
    inv = even / sp.sqrt(r) + odd / sp.sqrt(1-r)
    derivative = dr * (even - odd)
    effect0 = b**2 * sp.eye(2)
    effect1 = a**2 * sp.eye(2) + 4*d**2*even
    mass0, mass1 = [sp.simplify(sp.trace(rho * e)) for e in (effect0, effect1)]
    ref0, ref1 = [(rho_sqrt * e * rho_sqrt).T / m
                  for e, m in ((effect0, mass0), (effect1, mass1))]
    diff = (ref1 - ref0).applyfunc(sp.simplify)
    score = (inv * derivative * inv).T
    pairing = sp.simplify(sp.trace(score * diff))
    wanted = 4*d**2*dr / (a**2 + 4*d**2*r)
    require(sp.simplify(pairing - wanted) == 0, "Wrong marginal pairing")
    # The spectral extrema of score in the two sectors give the sharp bound.
    eig_even = sp.simplify(sp.trace(even * diff))
    eig_odd = sp.simplify(sp.trace(odd * diff))
    require(sp.simplify(eig_even + eig_odd) == 0, "Reference difference is not traceless")
    require(sp.simplify(eig_even - 4*d**2*r*(1-r)/mass1) == 0,
            "Wrong reference spectrum")
    osc_score = dr/r + dr/(1-r)
    require(sp.simplify(osc_score*eig_even - wanted) == 0, "Sharp bound is not attained")
    return {
        "preparer_pairing": "4*d^2*Dr/(A^2+4*d^2*r)",
        "reference_trace_norm": "8*d^2*r*(1-r)/(A^2+4*d^2*r)",
        "trace_norm_bound_is_sharp": True,
    }


def main():
    paths = [
        "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
        "03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean",
        "04_CERTIFICATES/order_memory_control_verify.py",
        str((HERE.parent / "round121" / "check_book03_identity_pair.py").relative_to(REPO)),
        str((HERE.parent / "round122" / "check_preparer_crossover.py").relative_to(REPO)),
    ]
    print(json.dumps({
        "status": "PASS",
        "source_sha256": {path: sha256((REPO / path).read_bytes()).hexdigest() for path in paths},
        "words": verify_words(),
        "preparation": verify_preparer(),
        "absolute_book_preparation_response_determined": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
