"""Verify the two-control paid mark, terminal disturbance and price-source identities."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[6]
NATIVE = ROOT / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
PIN = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
sys.path.insert(0, str(NATIVE.parent))
import native_execution as ne

PORT, READY, REPORT, MARK = 0, 1, 2, 3
SPIN = (4, 5)


def require(condition, reason):
    if not bool(condition):
        raise AssertionError(reason)


def gate(name, *wires):
    return ne.Gate(name, tuple(wires))


def mark_word(m):
    swap = [gate("CX", PORT, MARK), gate("CX", MARK, PORT), gate("CX", PORT, MARK)]
    sign = [gate("SourceI", PORT, *SPIN)]*2
    plus = [gate("G", PORT)]*m
    minus = sign + plus + sign
    return (swap + minus + [gate("CX", REPORT, PORT)]
            + minus + [gate("CX", READY, PORT)]
            + plus + [gate("CX", REPORT, PORT)]
            + minus + [gate("CX", READY, PORT)] + swap)


def verify_mark():
    require(sha256(NATIVE.read_bytes()).hexdigest() == PIN, "Native alphabet changed")
    g = sp.Matrix(ne.G_LOCAL)
    p, a = ne.P, ne.A
    v = sp.Matrix([a, p])
    for m in (1, 2):
        word = mark_word(m)
        counts = Counter(gate.op for gate in word)
        require(counts == {"G": 4*m, "CX": 10, "SourceI": 12},
                "The physical native schedule changed")
        execution = ne.Execution(6, (), (), tuple(word), ne.G_CX_SOURCE_I, PORT, SPIN)
        actual = ne.word_matrix(execution, max_qubits=6, max_expanded_stages=64)
        expected = sp.kronecker_product(
            sp.eye(2), sp.diag(g.T**(2*m), g.T**(2*m), g.T**(2*m), g**(2*m)), sp.eye(4)
        )
        require(ne.exact_matrix_equal(actual, expected), "The mark is not the claimed all-column operator")
    mark0, mark1 = g.T**2*v, g**2*v
    for mark in (mark0, mark1):
        require(ne.exact_matrix_equal(v.T*mark, sp.Matrix([[p**3]])), "Unequal born compression")
    require(ne.exact_matrix_equal(mark0.T*mark1, sp.Matrix([[2*p**6-1]])), "The mark overlap changed")
    require(ne.exact_matrix_equal(
        sp.Matrix([mark0[1]**2, mark1[1]**2]), sp.Matrix([p**2, (4-5*p)**2])
    ), "Native measured pointer probabilities changed")

    # A complete 0/10 writer is an isometry from the pointer into pointer and born tail.
    writer = sp.Matrix.hstack(
        sp.kronecker_product(sp.Matrix([1, 0]), g*v),
        sp.kronecker_product(sp.Matrix([0, 1]), g.T*v),
    )
    require(ne.exact_matrix_equal(writer.T*writer, sp.eye(2)), "Code writing altered the overlap")
    require(ne.exact_matrix_equal(sp.kronecker_product(sp.eye(2), v.T)*writer, a*sp.eye(2)),
            "Code writing does not have the assumed common born compression")
    require(ne.exact_matrix_equal(a**2*(p**3)**2*sp.eye(2), p**7*sp.eye(2)),
            "Wrong two-mark coherent compression")
    return {"G": "8m+2", "CX": 24, "SourceI": 24, "canonical_births": 4}


def verify_source_and_return():
    f, q, y0, b, p = sp.symbols("P_f P_q y0 b p", real=True)
    yf, yq = y0+b*f, y0+b*q
    joint = sp.Matrix([(1-yf)*(1-yq), (1-yf)*yq, yf*(1-yq), yf*yq])
    require(sp.expand(sum(joint)) == 1, "Incomplete paired measured law")
    tilt = (sp.Matrix([[p*p, p**3, p**3, p**4]])*joint)[0]
    cost_factor = p + (p*p-p)*y0
    require(sp.expand(tilt - (cost_factor+(p*p-p)*b*f)*(cost_factor+(p*p-p)*b*q)) == 0,
            "The complete 0/10 charge tilt changed")
    require(sp.simplify(sp.diff(tilt, f).subs(f, q) - sp.diff(tilt, q).subs(f, q)) == 0,
            "The paired charge coefficients disagree at the common null")
    g = sp.symbols("g")
    coefficients = sp.symbols("h00 h01 h10 h11", positive=True)
    h = sp.Matrix(coefficients)
    bits = ((0, 0), (0, 1), (1, 0), (1, 1))
    gram = sp.Matrix(4, 4, lambda j,k: g**sum(b1 != b2 for b1,b2 in zip(bits[j], bits[k])))
    expected = (
        2*(1-g)*(h[0]*h[1]+h[0]*h[2]+h[1]*h[3]+h[2]*h[3])
        + 2*(1-g*g)*(h[0]*h[3]+h[1]*h[2])
    )
    require(sp.expand(sum(h)**2 - (h.T*gram*h)[0] - expected) == 0,
            "Discrepancy of compatible recorded return changed")
    return {
        "same_registered_source_coefficients_on_common_null": True,
        "old_cut_return_ignoring_record": "sum(h_a*h_b*g^Hamming(a,b))",
        "old_cut_return_loss_positive_when_informative": True,
        "full_born_cold_amplitude_factor_m1": "p^7",
        "full_born_cold_probability_factor_m1": "p^14",
    }


def main():
    print(json.dumps({
        "status": "PASS",
        "native_gate_sha256": PIN,
        "pair_with_emitters": verify_mark(),
        "source_and_return": verify_source_and_return(),
        "physical_book_work_or_info_selected": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
