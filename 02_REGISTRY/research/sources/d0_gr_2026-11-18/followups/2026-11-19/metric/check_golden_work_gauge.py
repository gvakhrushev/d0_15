#!/usr/bin/env python3
"""Native H.1 port words and exact first-order identification of a scalar amplitude model."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp


def load_owner():
    path = Path("02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py")
    owner = next(folder / path for folder in Path(__file__).resolve().parents if (folder / path).is_file())
    digest = hashlib.sha256(owner.read_bytes()).hexdigest()
    assert digest == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
    spec = importlib.util.spec_from_file_location("golden_work_gate_owner", owner)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, digest


def native_words(owner):
    S = owner.Gate("SourceI", (2, 0, 1))
    G = owner.Gate("G", (2,))
    X = owner.Gate("CX", (2, 3))
    T = owner.Gate("G", (3,))
    z = sp.diag(1, -1)
    g = sp.Matrix(owner.G_LOCAL)
    v = sp.Matrix([owner.A, owner.P])
    kron = sp.kronecker_product
    eq = owner.exact_matrix_equal

    def execution(bits, gates, reports):
        return owner.Execution(bits, (), (), gates, profile=owner.G_CX_SOURCE_I,
                               source_port=2, source_spin=(0, 1), report_bits=reports)

    def native_matrix(word):
        gates = tuple(gate for letter in word for gate in ((G,) if letter == "G" else (S, S)))
        ex = execution(3, gates, ())
        counts = owner.inventory(ex, max_qubits=3, max_expanded_stages=11)
        assert counts.g_count == word.count("G") and counts.source_i_count == 2 * word.count("Z")
        return owner.word_matrix(ex), counts.gate_count

    assert eq(native_matrix("Z")[0], kron(sp.eye(4), z))
    assert eq(native_matrix("ZGZ")[0] * kron(sp.eye(4), v), kron(sp.eye(4), sp.Matrix([1, 0])))
    encoder = owner.word_matrix(execution(4, (X, T, X), (2, 3)))
    e0, e1 = sp.eye(2)[:, 0], sp.eye(2)[:, 1]
    assert eq(encoder * kron(sp.eye(4), e0, v), kron(sp.eye(4), e0, g * v))
    assert eq(encoder * kron(sp.eye(4), e1, v), kron(sp.eye(4), e1, e0))
    result = {}
    for m in (1, 3):
        dark = "G" + "Z" * m + "G"
        bright_a, bright_b = dark + "ZG", dark + "GZ"
        records = []
        for word, expected in ((dark, z), (bright_a, g), (bright_b, z * g * z)):
            matrix, count = native_matrix(word)
            assert eq(matrix, kron(sp.eye(4), expected))
            records.append({"chronological_macros": word, "body_raw_calls": count})
        result[str(m)] = records
    return result


def algebra():
    A, B, C, D, u, v = sp.symbols("A B C D u v", positive=True)
    al, be, ga, de, up, vp = sp.symbols("a b c d i j", real=True)
    W, Z = sp.Matrix([[A, -B], [C, D]]), sp.diag(u, -v)
    dW, dZ = sp.Matrix([[A*al, -B*be], [C*ga, D*de]]), sp.diag(u*up, -v*vp)
    forms = {"G": (W, dW), "Z": (Z, dZ)}
    centre = {D: A, v: u}
    def jet(word, index=0):
        y, dy = sp.eye(2)[:, index], sp.zeros(2, 1)
        for letter in word:
            M, dM = forms[letter]
            dy, y = dM*y + M*dy, M*y
            dy = dy.applyfunc(lambda t: sp.factor(t.subs(centre)))
            y = y.applyfunc(lambda t: sp.factor(t.subs(centre)))
        return y, dy

    def signed_log_amplitude_odds(word):
        y, dy = jet(word)
        return sp.factor(dy[1]/y[1] - dy[0]/y[0])

    results = []
    for m in (1, 3):
        dark = "G" + "Z"*m + "G"
        K = W * Z**m * W
        assert sp.expand(K[1, 0] - C*(A*u**m-D*v**m)) == 0
        y, dy = jet(dark)
        assert y[1] == 0 and sp.simplify(2*y[1]*dy[1]) == 0
        left = signed_log_amplitude_odds(dark + "ZG")
        right = signed_log_amplitude_odds(dark + "GZ")
        ratio = sp.factor(right - left)
        assert sp.expand(ratio - 2*(al-de) - (2*m-1)*(up-vp)) == 0
        results.append(ratio)
    X, U = al-de, up-vp
    assert sp.simplify((5*results[0]-results[1])/8-X) == 0
    assert sp.simplify((results[1]-results[0])/4-U) == 0
    y0, dy0 = jet("G", 0)
    y1, dy1 = jet("G", 1)
    odds_cross = sp.factor((y0[1]/y0[0])**2 / (y1[1]/y1[0])**2)
    def dlog(y, dy):
        return dy[1]/y[1] - dy[0]/y[0]
    assert sp.factor(dlog(y0, dy0)-dlog(y1, dy1) - (be+ga-al-de)) == 0
    assert sp.factor(odds_cross - (B*C/A**2)**2) == 0
    # Geometric significance is conditional. Verify precisely the surviving group.
    a, p, k, s, c = sp.symbols("a p k s c", positive=True)
    H = sp.diag(1, k)
    G0, Z0 = sp.Matrix([[a, -p], [p, a]]), sp.diag(1, -1)
    physical = {"G": s*H.inv()*G0*H, "Z": c*Z0}
    for word in ("G", "ZGZ", "GZZZGGZ", "ZGGGZGZ"):
        lhs, rhs = sp.eye(2), sp.eye(2)
        for letter in word:
            lhs = physical[letter]*lhs
            rhs = {"G": G0, "Z": Z0}[letter]*rhs
        expected = s**word.count("G") * c**word.count("Z") * H.inv()*rhs*H
        assert all(sp.expand(t) == 0 for t in lhs - expected)
    return {"half_log_bright_odds_derivatives": ["2X+U", "2X+5U"],
            "one_gate_half_cross_log_odds": "d log(BC/(AD))",
            "determinant_first_two_rows": 8,
            "dark_intensity_first_derivative_at_exact_zero": 0,
            "word_gauge": "s^#G c^#Z H^-1 U(word) H, H=diag(1,k)"}


if __name__ == "__main__":
    owner, sha = load_owner()
    print(json.dumps({"owner_sha256": sha, "eight_column_body_checks": native_words(owner),
                      "NC1_encoder_on_real_born_tail": "verified on both labels times all four Spin columns",
                      "exact_positive_amplitude_model": algebra(),
                      "identification_with_complete_physical_Cost_minus_Info": False},
                     ensure_ascii=False, indent=2))
