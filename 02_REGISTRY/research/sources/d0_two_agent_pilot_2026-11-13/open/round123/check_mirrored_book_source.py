"""Exact A67 mirror controls and source identities in the declared price class."""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round121"))
from check_book03_identity_pair import NATIVE, REPO, exact, ne


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def polynomial_zero(value):
    return sp.cancel(value) == 0


def verify_words():
    A, B, U = "A", "B", "U"
    Z = (A, B, A, U, U, A, B, A)
    P = Z + Z + (A, A)
    K = Z + (A,) + Z + (A,)
    words = {"P_plus": P + (A, A), "P_minus": (A,) + P + (A,), "K_ref": K + (A, A)}
    gates = {
        A: ne.Gate("CX", (2, 3)),
        B: ne.Gate("CX", (3, 2)),
        U: ne.Gate("SourceI", (2, 0, 1)),
    }
    counts = Counter(words["K_ref"])

    def full_matrix(word):
        program = ne.Execution(6, (), (), tuple(gates[name] for name in word),
                               ne.G_CX_SOURCE_I, 2, (0, 1))
        return ne.word_matrix(program, max_qubits=6, max_expanded_stages=20)

    def tariff(word, start):
        state = start
        result = Counter()
        for label in word:
            result[label, state] += 1
            # A stationary vertex Info contributes independently at that address.
            result["visited", state] += 1
            e, y = state
            if label == A:
                state = (e, y ^ e)
            elif label == B:
                state = (e ^ y, y)
        require(state == start, "A complete comparison changed its WORK address")
        return result

    for title, word in words.items():
        require(len(word) == 20 and Counter(word) == counts, "Inventory mismatch")
        expected = full_matrix((U, U)) if title == "K_ref" else sp.eye(64)
        require(ne.exact_matrix_equal(full_matrix(word), expected), "Native endpoint")
    def field(matrix):
        return DomainMatrix.from_Matrix(matrix).convert_to(ne.GOLDEN_FIELD).to_dense()

    p, a = ne.P, ne.A
    v = sp.Matrix([a, p])
    incoming = field(sp.kronecker_product(sp.eye(4), v, v, v, v))
    reports = [field(sp.kronecker_product(sp.eye(16), sp.diag(*mask)))
               for mask in ((1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))]
    report_copy = ne.Gate("CX", (2, 4))
    target_copy = ne.Gate("CX", (4, 5))
    G = ne.Gate("G", (5,))
    for active, Q in ((gates[B], 2*p**3), (gates[A], p**2)):
        q = p**2 + p**3*Q
        expected = [field((1-q)*sp.eye(4)), field(q*sp.eye(4)), field(sp.zeros(4))]
        for word in words.values():
            actual = (active, report_copy, gates[U], gates[U],
                      *(gates[name] for name in word),
                      active, target_copy, G, target_copy)
            program = ne.Execution(6, (), (), actual, ne.G_CX_SOURCE_I, 2, (0, 1))
            final = field(ne.word_matrix(program, max_qubits=6, max_expanded_stages=28)) * incoming
            for report, gram in zip(reports, expected):
                reached = report * final
                require(reached.transpose() * reached == gram, "Original noisy readout changed")

    for x in product((0, 1), repeat=2):
        plus, minus, ref = (tariff(words[key], x) for key in ("P_plus", "P_minus", "K_ref"))
        e, y = x
        require(plus + minus == Counter({k: 2*v for k, v in ref.items()}),
                "Midpoint identity failed on the addressed path")
        require(minus == tariff(words["P_plus"], (e, y ^ e)), "Mirror identity failed")
        if e == 0:
            require(plus == minus == ref, "Reference sector changed cost")
    return {"addressed_stage_inventory": dict(counts), "stages_per_body": 20,
            "full_columns": 64, "native_output": ["I", "I", "Z_e"],
            "original_readout_gram_checks": 18,
            "stationary_WORK_tariff_midpoint_on_all_addresses": True}


def verify_odds():
    m0, a, b, s = sp.symbols("m0 a b s", positive=True)
    Q = (a+b)/(m0+a+b)
    Qplus = (s*a+b/s)/(m0+s*a+b/s)
    Qminus = (a/s+s*b)/(m0+a/s+s*b)
    odds = lambda q: q/(1-q)
    Tplus, Tminus = odds(Qplus)/odds(Q), odds(Qminus)/odds(Q)
    z = (a-b)/(a+b)
    ch, sh = (s+1/s)/2, (s-1/s)/2
    require(polynomial_zero(Tplus - ch - z*sh), "First mirrored odds")
    require(polynomial_zero(Tminus - ch + z*sh), "Second mirrored odds")
    require(polynomial_zero((Tplus+Tminus)/2 - ch), "Prepared imbalance did not cancel")
    require(polynomial_zero((m0+s*a+b/s)/(m0+a+b) - 1 - Q*(Tplus-1)),
            "Raw mass ratio")
    det = sp.det(sp.Matrix([[s-1, 1/s-1], [1/s-1, s-1]]))
    require(polynomial_zero(det - (s-1)**3*(s+1)/s**2), "Blindness determinant")
    return {"unknown_preparer_imbalance_cancels": True,
            "cosh_is_the_mean_of_normalized_odds_ratios": True,
            "recovers_relative_total_mass_from_normalized_sector_masses": True,
            "unchanged_marginals_force_blindness_or_zero_tilt": True}


def verify_E0():
    p, a = ne.P, ne.A
    identity = sp.eye(2)
    Rz = sp.Matrix([[0, 1], [1, 0]])
    gate = sp.BlockMatrix([[a*identity, p*Rz], [p*identity, a*identity]]).as_explicit()
    flip = sp.kronecker_product(Rz, identity)
    fresh = sp.Matrix.vstack(a*identity, p*identity)
    tail = flip * gate * flip * fresh
    require(ne.exact_matrix_equal(tail, sp.Matrix.vstack(identity, a*p*(identity + Rz))),
            "Original E0 regular lift")
    left_tail = gate * fresh
    expected_left = sp.Matrix.vstack(p*identity + p**2*Rz, 2*a*p*identity)
    require(ne.exact_matrix_equal(left_tail, expected_left), "Original E0 left mark")
    proof_gram = identity + 2*p**3*(identity+Rz)
    for reached in (left_tail, tail):
        require(ne.exact_matrix_equal(reached.T*reached, proof_gram), "Original E0 full Gram")

    q, c, u0, u1 = sp.symbols("q c u0 u1", positive=True)
    mean = (1-q)*u0 + q*u1
    normalizer = 1+c*mean
    post = q*(1+c*u1)/normalizer
    dark = c*q*u1/normalizer
    require(polynomial_zero((q-post+dark)/(c*(post-dark)) - mean),
            "Mean even mass recovered from original readout")
    return {"right_mark_on_original_E0": 1, "regular_conditional_dark_mass": "4p^3*u",
            "regular_conditional_error": "4p^3*u/(1+4p^3*u)",
            "identical_Gram_on_both_marks": "I + 4p^3*P_plus",
            "measured_even_mass": "(q_before-q_after+P_11)/(4p^3*(q_after-P_11))"}


def main():
    print(json.dumps({
        "native_sha256": sha256(NATIVE.read_bytes()).hexdigest(),
        "mirror_words": verify_words(),
        "odds": verify_odds(),
        "E0": verify_E0(),
        "book03_stationary_class_blind_weight_binding_proved": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
