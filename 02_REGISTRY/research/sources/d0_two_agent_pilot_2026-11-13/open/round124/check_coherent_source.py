"""Exact fine-label response, paid phase control, and coherent saturation checks."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round121"))
from check_book03_identity_pair import NATIVE, exact, ne


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def zero_matrix(value):
    return all(sp.expand(entry) == 0 for entry in value)


def word_matrix(gates, width, port, spin):
    execution = ne.Execution(width, (), (), gates, ne.G_CX_SOURCE_I, port, spin)
    return ne.word_matrix(execution, max_qubits=width, max_expanded_stages=len(gates))


def verify_fine_response():
    p, a = ne.P, ne.A
    v = sp.Matrix([a, p])
    cx = ne.Gate("CX", (0, 1))
    gate = word_matrix((cx, ne.Gate("G", (1,)), cx), 4, 0, (2, 3))
    born0 = sp.kronecker_product(sp.Matrix([1, 0]), v, sp.eye(4))
    born1 = sp.kronecker_product(sp.Matrix([0, 1]), v, sp.eye(4))
    target0 = sp.kronecker_product(sp.Matrix([1, 0]), sp.Matrix([p**3, 2*a*p]), sp.eye(4))
    target1 = sp.kronecker_product(sp.Matrix([0, 1]), sp.Matrix([1, 0]), sp.eye(4))
    require(ne.exact_matrix_equal(gate*born0, target0), "Wrong direct tail")
    require(ne.exact_matrix_equal(gate*born1, target1), "Wrong reported tail")

    require(exact(p**6 + 4*p**3, sp.Integer(1)), "Direct tail no longer normalized")
    require(exact(p**4 + 2*p**3, p), "Fine overlap coefficient")
    require(exact(a*(p**3 + 2*p**2), a), "Conditional Hellinger coefficient")
    require(exact(p/(1+p), p**2), "Fine gain threshold")
    q0 = p**2
    require(exact(p*a+p*a*sp.sqrt(q0), a), "Fine optimum at the threshold")
    return {
        "passive_marks_00_01_10_11": ["p^2", "p^3", "p^3", "p^4"],
        "actual_direct_tail_conditional_law": ["p^6", "4p^3"],
        "fine_optimal_cold": "p*sqrt(1-q)+p*sqrt(p)*sqrt(q)",
        "fine_stationary_threshold": "p^2",
        "informative_collar_gain_bound": "-f_fine'(q) >= p*(q-p^2)/4",
    }


def verify_paid_phase():
    # Port 0 and helper 1 are live WORK; 2 and 3 are r,t; 4 and 5 are Spin.
    swap = (ne.Gate("CX", (0, 1)), ne.Gate("CX", (1, 0)), ne.Gate("CX", (0, 1)))
    source = ne.Gate("SourceI", (0, 4, 5))
    routed = word_matrix(swap + (source,) + swap, 6, 0, (4, 5))
    reverse = word_matrix(swap + (source,) * 3 + swap, 6, 0, (4, 5))
    expected = sp.kronecker_product(sp.eye(2),
                                     sp.diag(sp.eye(16), sp.kronecker_product(sp.eye(4), ne.L_I)))
    require(ne.exact_matrix_equal(routed, expected), "Routed SourceI did not restore its frame")
    require(ne.exact_matrix_equal(reverse*routed, sp.eye(64)), "Literal phase inverse failed")

    edge = sp.Matrix([[0, 1], [-1, 0]])
    phase = sp.diag(1, sp.I)
    paired = phase * edge * phase.H
    require(paired == -sp.I * sp.Matrix([[0, 1], [1, 0]]), "Imaginary symmetric edge")
    require(edge*paired-paired*edge == sp.diag(-2*sp.I, 2*sp.I), "Imaginary diagonal difference")
    return {"literal_routed_phase_stages": 7, "literal_inverse_stages": 9,
            "all_columns": 64, "mark_bits_unchanged": True,
            "real_edge_and_phase_conjugate_generate_su2": True}


def verify_joint_terminal():
    p, a = ne.P, ne.A
    v = sp.Matrix([a, p])
    X = sp.Matrix([[0, 1], [1, 0]])
    omega = (v.T*X*v)[0]
    require(exact(omega, 2*a*p) and exact(1-omega**2, p**6), "Helper overlaps")
    # Three WORK bits r,t,eta followed by the protected Spin factor.
    CX = word_matrix((ne.Gate("CX", (0, 2)),), 5, 0, (3, 4))
    target = sp.kronecker_product(v, v, v)
    tag = sp.kronecker_product(sp.eye(4), v*v.T)
    end = target*target.T
    require(ne.exact_matrix_equal(tag*end, end), "Born return lies within helper success")
    b0 = sp.kronecker_product(sp.Matrix([1, 0]), v, v, sp.eye(4))
    b1 = sp.kronecker_product(sp.Matrix([0, 1]), sp.Matrix([1, 0]), v, sp.eye(4))
    e0, e1 = CX*b0, CX*b1
    tag_fail = sp.kronecker_product(sp.eye(8)-tag, sp.eye(4))
    require(ne.exact_matrix_equal(tag_fail*e0, sp.zeros(32, 4)), "False helper signal")
    require(ne.exact_matrix_equal(e1.T*tag_fail*e1, p**6*sp.eye(4)), "Helper signal gain")
    ret = sp.kronecker_product(target.T, sp.eye(4))
    require(ne.exact_matrix_equal(ret*e0, a*sp.eye(4)), "Coarse arm zero")
    require(ne.exact_matrix_equal(ret*e1, a*p*omega*sp.eye(4)), "Coarse arm one")
    return {
        "extra_paid_gate": "CX(r,eta)",
        "helper_born_overlap": "2p*sqrt(p)",
        "helper_failure_probability": "p^6*q",
        "cold_and_helper_commute": True,
        "coarse_tagged_cold": "sqrt(p)*sqrt(1-q)+p*sqrt(p)*omega*sqrt(q)",
        "fine_tagged_cold": "p*sqrt(1-q)+p*sqrt(p)*omega*sqrt(q)",
        "fine_tagged_collar_gain_bound": "-f'(q) >= sqrt(p)*(1-omega)/2",
    }


def verify_saturation_identities():
    v, w = sp.symbols("v w", positive=True)
    c0 = sp.Matrix([[sp.Rational(1, 3), sp.I/4], [sp.Rational(1, 5), sp.Rational(1, 2)]])
    c1 = sp.Matrix([[sp.I/3, sp.Rational(2, 3)], [sp.Rational(1, 4), -sp.I/6]])
    cold = v*c0+w*c1
    f = v+w
    ident = sp.eye(2)
    deficit = f**2*ident-cold.H*cold
    leakage = f*(v*(ident-c0.H*c0)+w*(ident-c1.H*c1))
    mismatch = v*w*(c0-c1).H*(c0-c1)
    require(zero_matrix(deficit-leakage-mismatch), "Operator deficit decomposition")

    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1", positive=True)
    common = sp.Matrix([[1, 2], [3, 4]])
    d0 = sp.Matrix([[0, 2], [1, 3]])
    d1 = sp.Matrix([[4, -1], [2, 0]])
    f = a0*b0+a1*b1
    C = f*common
    DC = a0*d0+a1*d1
    DE0 = b0*(common.T*d0+d0.T*common)
    DE1 = b1*(common.T*d1+d1.T*common)
    require(zero_matrix(DC.T*C+C.T*DC-f*(a0/b0*DE0+a1/b1*DE1)),
            "Absolute first jet at saturation")
    return {"positive_deficit_identity": True,
            "absolute_return_jet_from_absolute_mark_effect_jets": True}


def main():
    print(json.dumps({
        "native_sha256": sha256(NATIVE.read_bytes()).hexdigest(),
        "fine_coherent_response": verify_fine_response(),
        "paid_phase_control": verify_paid_phase(),
        "single_joint_terminal": verify_joint_terminal(),
        "weighted_saturation_identities": verify_saturation_identities(),
        "Book03_absolute_normalizer_bound": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
