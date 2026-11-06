#!/usr/bin/env python3
"""Exact bounded original-reader/input-comparison and true-clock check.

This checks finite targets and the G1--G6 clock, not an emitted exact native
reflection, the full geometry, an asymptotic q>=3 estimate, or free ticks.
Arithmetic is Q[a]/(a^4+a^2-1), from the unchanged embedded RO owner.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import types

PRIMARY = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
NATIVE = "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
CLOCK = "02_REGISTRY/research/sources/d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md"
RO_HASH = "28af31ce262cafd8fa3ebe2b93922248961e0441fc582663f25857cccc83f99a"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    text = (root / PRIMARY).read_text(encoding="utf-8")
    begin = "<!-- RO-NATIVE-GOLDEN-CHECK:BEGIN -->"
    end = "<!-- RO-NATIVE-GOLDEN-CHECK:END -->"
    section = text.split(begin, 1)[1].split(end, 1)[0]
    match = re.search(r"```python\r?\n(.*?)```", section, re.S)
    if match is None:
        raise RuntimeError("Missing owned RO Python block")
    code = match.group(1).replace("\r\n", "\n")
    if sha(code.encode()) != RO_HASH:
        raise RuntimeError("Owned RO exact arithmetic code hash changed")
    ro = types.ModuleType("owned_ro_exact_arithmetic")
    ro.__file__ = str(root / PRIMARY) + "#RO-NATIVE-GOLDEN-CHECK"
    sys.modules[ro.__name__] = ro
    exec(compile(code, ro.__file__, "exec"), ro.__dict__)
    K, zero, one, a, p = ro.K, ro.Z, ro.ONE, ro.a, ro.p
    eye, transpose, mul, scale = ro.eye, ro.transpose, ro.mul, ro.scale
    add, kron, exact_gate, replay = ro.add, ro.kron, ro.exact_gate, ro.replay
    v = ro.v

    spec = importlib.util.spec_from_file_location("owned_native_for_input_clock", root / NATIVE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load native owner")
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError("FAIL: " + name)
        checks.append(name)

    def trace(matrix):
        return sum((matrix[j][j] for j in range(len(matrix))), zero)

    def sub(left, right):
        return add(left, scale(-one, right))

    def zeros(rows, cols):
        return [[zero for _ in range(cols)] for _ in range(rows)]

    def put(dst, block, row, col):
        for i, values in enumerate(block):
            for j, value in enumerate(values):
                dst[row+i][col+j] += value

    def column_inner(left, right):
        return mul(transpose(left), right)[0][0]

    def owner_word(word):
        gates = tuple(native.Gate(op, tuple(wires)) for op, wires in word)
        execution = native.Execution(qubits=2, blank_wires=(0, 1), old_right=(), gates=gates, profile=native.G_CX)
        native.validate_execution(execution, max_qubits=2, max_expanded_stages=100)
        actual = native.word_matrix(execution, max_qubits=2, max_expanded_stages=100)
        result = zeros(4, 4)
        for i in range(4):
            for j in range(4):
                coeff = list(reversed(native.GOLDEN_FIELD.from_sympy(actual[i, j]).to_list()))
                result[i][j] = K([Fraction(int(x.numerator), int(x.denominator)) for x in coeff])
        return result

    check("golden defining polynomial", a**4 + a*a == one)
    check("canonical birth normalized", column_inner(v, v) == one)
    b = kron(v, v)
    Pb = mul(b, transpose(b))
    Rb = sub(eye(4), scale(K(2), Pb))
    Zport = [[(one if i < 2 else -one) if i == j else zero for j in range(4)] for i in range(4)]
    check("input reflection all columns", mul(Rb, Rb) == eye(4))
    check("input reflection fixes born ray up to minus", mul(Rb, b) == scale(-one, b))
    check("input reflection determinant minus one", ro.det(Rb) == -one)
    Jbank = kron(eye(4), v)
    b3 = kron(b, v)
    Rb3 = sub(eye(8), scale(K(2), mul(b3, transpose(b3))))
    check("input comparison natural under actual birth", mul(Rb3, Jbank) == mul(Jbank, Rb))

    words = {
        "identity": [],
        "one_G": [("G", (0,))],
        "G_CX_six": [("G", (0,)), ("CX", (0, 1)), ("G", (1,)),
                     ("G", (0,)), ("CX", (1, 0)), ("G", (1,))],
    }
    wlast = [[-p], [a]]
    Plast = kron(eye(4), mul(wlast, transpose(wlast)))
    check("latest detail normalized and orthogonal", column_inner(wlast, wlast) == one and column_inner(v, wlast) == zero)
    reader_rows = []
    endpoints = {}
    for name, word in words.items():
        D = replay(2, word)
        check(name + ": native all-column replay", D == owner_word(word))
        check(name + ": orthogonal reader word", mul(transpose(D), D) == eye(4))
        W = mul(mul(transpose(D), Zport), D)
        Db = mul(D, b)
        Q = sum((Db[i][0]**2 for i in range(2, 4)), zero)
        V = kron(mul(W, Rb), eye(2))
        Vbad = kron(W, eye(2))
        expected = trace(Zport) - K(2) + K(4)*Q
        check(name + ": reflection and full trace constant", mul(W, W) == eye(4) and transpose(W) == W and trace(W) == trace(Zport))
        check(name + ": two-reflection compressed trace", trace(mul(Plast, V)) == expected)
        check(name + ": omission hostile trace constant", trace(mul(Plast, Vbad)) == trace(Zport))
        check(name + ": all initialized marks phase transport", mul(V, b3) == scale(-one, mul(Vbad, b3)))
        check(name + ": full target SO", mul(transpose(V), V) == eye(8) and ro.det(V) == one)
        endpoints[name] = V
        reader_rows.append({"word": name, "native_calls": len(word), "Q": Q.encoded(),
                            "full_trace_W": trace(W).encoded(), "latest_trace_WRb": expected.encoded()})
    check("actual report probability nonconstant", reader_rows[0]["Q"] != reader_rows[1]["Q"])
    check("two-reflection trace retains report variation", reader_rows[0]["latest_trace_WRb"] != reader_rows[1]["latest_trace_WRb"])

    V = endpoints["G_CX_six"]
    Vmix = mul(exact_gate(3, "G", (2,)), V)
    check("age-mixing target is orthogonal", mul(transpose(Vmix), Vmix) == eye(8))
    check("age-mixing target really mixes latest detail", mul(Plast, Vmix) != mul(Vmix, Plast))
    check("mixed target does not inherit two-reflection source identity", trace(mul(Plast, Vmix)) != trace(mul(Plast, V)))

    def true_clock(endpoint, L):
        # THREE separate births, L-1 nonidentity native G stages, final target.
        dims = [1, 2, 4] + [8]*L
        nstage = len(dims)
        passive = [kron(eye(1), v), kron(eye(2), v), kron(eye(4), v)]
        steps = passive.copy()
        prefix = eye(8)
        intermediate = [exact_gate(3, "G", (0,))]
        if L == 3:
            intermediate.append(exact_gate(3, "G", (2,)))
        for gate in intermediate:
            if gate == eye(8):
                raise RuntimeError("A purported literal body stage is identity")
            steps.append(gate)
            passive.append(eye(8))
            prefix = mul(gate, prefix)
        g = mul(endpoint, transpose(prefix))
        if mul(g, prefix) != endpoint:
            raise RuntimeError("Final ideal target did not give the stated endpoint")
        offsets = []
        total = 0
        for dimension in dims:
            offsets.append(total)
            total += dimension
        B = [None]*nstage
        B[-1] = eye(8)
        for j in range(nstage-2, -1, -1):
            B[j] = mul(B[j+1], passive[j])
        R = zeros(total, 8)
        for j in range(nstage):
            detail = eye(dims[j]) if j == 0 else sub(eye(dims[j]), mul(passive[j-1], transpose(passive[j-1])))
            put(R, mul(detail, transpose(B[j])), offsets[j], 0)
        T = zeros(total, total)
        for j, gate in enumerate(steps):
            put(T, gate, offsets[j+1], offsets[j])
        put(T, mul(R, g), 0, offsets[-1])
        return T, R, dims, g, prefix

    clock_rows = []
    for name, endpoint in [("WRb", V), ("age_mixing", Vmix)]:
        for L in (2, 3):
            T, R, dims, g, prefix = true_clock(endpoint, L)
            label = name + ": L=" + str(L)
            check(label + ": actual incidence isometry G4", mul(transpose(R), R) == eye(8))
            check(label + ": true growing clock unitary G6", mul(transpose(T), T) == eye(len(T)))
            check(label + ": actual final stage orthogonal", mul(transpose(g), g) == eye(8))
            check(label + ": all body stages retained in endpoint", mul(g, prefix) == endpoint)
            power = eye(len(T))
            traces = []
            for r in range(1, L+1):
                power = mul(power, T)
                tr = trace(power)
                traces.append(tr.encoded())
                if r < L:
                    check(label + ": no shorter wrap r=" + str(r), tr == zero)
                else:
                    check(label + ": shortest wrap exact coefficient", tr == K(L)*trace(mul(Plast, endpoint)))
            clock_rows.append({"target": name, "L": L, "stage_dimensions": dims,
                               "clock_dimension": len(T), "trace_powers_1_to_L": traces,
                               "latest_partial_trace": trace(mul(Plast, endpoint)).encoded()})

    receipt = {
        "schema": "original-reader-input-true-clock-exact-v1", "status": "PASS",
        "field": "Q[a]/(a^4+a^2-1), a positive, p=a^2",
        "arithmetic": "exact rational polynomial reduction; no floating tolerance",
        "checks": len(checks), "check_names": checks,
        "owners": [
            {"path": PRIMARY, "block": "RO-NATIVE-GOLDEN-CHECK", "code_sha256": RO_HASH},
            {"path": NATIVE, "sha256": sha((root / NATIVE).read_bytes())},
            {"path": CLOCK, "sha256": sha((root / CLOCK).read_bytes())},
        ],
        "checker_sha256": sha(Path(__file__).read_bytes().replace(b"\r\n", b"\n")),
        "reader_cases": reader_rows, "clock_cases": clock_rows,
        "scope": [
            "Original native G/CX D words checked on every column against unchanged native_execution.py.",
            "Rb and final closing g are ideal full real targets; no emitted exact native reflection is asserted.",
            "q=2 bounded clock fixture is not the asymptotic q>=3 source theorem or full geometry replay.",
            "Three separate births and every nontrivial intermediate G stage are retained and counted.",
            "Age mixing obeys shortest-wrap identity; invariant-age factorization is not assumed.",
            "No free identity tick, measurement, record register, erased complement, or physical inverse is introduced.",
        ],
    }
    args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "checks": len(checks), "output": str(args.out.resolve()),
                      "receipt_sha256": sha(args.out.read_bytes())}))


if __name__ == "__main__":
    main()
