#!/usr/bin/env python3
"""Exact bounded full-flag comparison; no full GR/native compiler is emitted."""
from __future__ import annotations
import argparse
import ast
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
SR_HASH = "b785b3f595ea130e6d0b4dc85a8dd09f4b989f59a549dae5aa806d2fd8219048"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def extract(text, marker, expected):
    section = text.split("<!-- " + marker + ":BEGIN -->", 1)[1].split("<!-- " + marker + ":END -->", 1)[0]
    match = re.search(r"^```python\r?\n(.*?)^```[ \t]*(?:\n|$)", section, re.S | re.M)
    if match is None:
        raise RuntimeError("Missing owned block " + marker)
    code = match.group(1).replace("\r\n", "\n")
    if sha(code.encode()) != expected:
        raise RuntimeError("Changed owned block " + marker + ": " + sha(code.encode()))
    return code


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    text = (root / PRIMARY).read_text(encoding="utf-8")
    rocode = extract(text, "RO-NATIVE-GOLDEN-CHECK", RO_HASH)
    srcode = extract(text, "SR-ORIGINAL-READER-CLOCK-CHECK", SR_HASH)
    ro = types.ModuleType("owned_ro_for_full_flag")
    ro.__file__ = str(root / PRIMARY) + "#RO-NATIVE-GOLDEN-CHECK"
    sys.modules[ro.__name__] = ro
    exec(compile(rocode, ro.__file__, "exec"), ro.__dict__)
    spec = importlib.util.spec_from_file_location("owned_native_for_full_flag", root / NATIVE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot import native owner")
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)

    K, zero, one, p = ro.K, ro.Z, ro.ONE, ro.p
    eye, transpose, mul, scale = ro.eye, ro.transpose, ro.mul, ro.scale
    add, kron, exact_gate, replay = ro.add, ro.kron, ro.exact_gate, ro.replay
    v = ro.v
    env = {"ro": ro, "native": native, "Fraction": Fraction, "K": K,
           "zero": zero, "one": one, "v": v, "eye": eye, "transpose": transpose,
           "mul": mul, "scale": scale, "add": add, "kron": kron, "exact_gate": exact_gate}
    srmain = next(node for node in ast.parse(srcode).body if isinstance(node, ast.FunctionDef) and node.name == "main")
    names = {"trace", "sub", "zeros", "put", "column_inner", "owner_word", "true_clock"}
    functions = [node for node in srmain.body if isinstance(node, ast.FunctionDef) and node.name in names]
    if {node.name for node in functions} != names:
        raise RuntimeError("Owned SR helper interface changed")
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(root / PRIMARY) + "#SR-owned-helpers", "exec"), env)
    trace, sub, inner = env["trace"], env["sub"], env["column_inner"]
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError("FAIL: " + name)
        checks.append(name)

    # Exact original READY calibration, including its limiting algebraic value.
    z = K(Fraction(1, 2**20))
    def report0(t):
        ell = K(4)*t*t*(one-t*t)
        aa = K(2)*ell-ell*ell
        return one-(one-z*ell)*(one-z*aa)
    r0 = z*(K(152)*p-K(92))-z*z*(K(1504)-K(2432)*p)
    check("original bare-report baseline polynomial", report0(p) == r0)
    pc = -one-p
    ainf = K(Fraction(1,5))*(K(6)*p-K(2))
    ainf_c = K(Fraction(1,5))*(K(6)*pc-K(2))
    field_trace = K(4)*(ainf*r0+ainf_c*report0(pc))-K(4)
    check("actual READY limiting field trace", field_trace == K(-4+Fraction(12976327,2**32)))
    check("limiting trace is nonintegral", Fraction(12976327,2**32).denominator != 1)
    check("all finite READY conjugates outside root interval", Fraction(4*21892*244,2**20)-2 > 2)

    X = [[zero, one], [one, zero]]
    Pplus = scale(K(Fraction(1, 2)), add(eye(2), X))
    Pminus = scale(K(Fraction(1, 2)), sub(eye(2), X))
    s = inner(v, mul(X, v))
    check("canonical flag overlap is actual golden value", s == K(2)*p*ro.a)
    check("both character sectors retained", add(Pplus, Pminus) == eye(2) and trace(Pplus) == one and trace(Pminus) == one)
    check("character projector does not commute with actual flag birth", mul(Pplus, mul(v, transpose(v))) != mul(mul(v, transpose(v)), Pplus))

    def comparator(A):
        return add(kron(A, eye(2)), kron(sub(eye(len(A)), A), X))

    def make_fixture(D, b, Zport, name):
        d = len(D)
        Pb = mul(b, transpose(b))
        Rb = sub(eye(d), scale(K(2), Pb))
        W = mul(mul(transpose(D), Zport), D)
        E = scale(K(Fraction(1, 2)), sub(eye(d), W))
        CP, CE = comparator(Pb), comparator(E)
        F = mul(CE, CP)
        u = kron(b, v)
        Q = inner(b, mul(E, b))
        char = add(kron(eye(d), Pplus), kron(mul(W, Rb), Pminus))
        check(name + ": E is the full projector", mul(E, E) == E and transpose(E) == E)
        check(name + ": both full flags are involutions", mul(CP, CP) == eye(2*d) and mul(CE, CE) == eye(2*d))
        check(name + ": full F is orthogonal", mul(transpose(F), F) == eye(2*d))
        check(name + ": full two-sector operator identity", F == char)
        check(name + ": canonical input is unchanged by CP", mul(CP, u) == u)
        check(name + ": full cold corner, no sector selection", inner(u, mul(F, u)) == s+(one-s)*Q)
        check(name + ": complete trace retains source", trace(F) == K(d)+trace(Zport)-K(2)+K(4)*Q)
        check(name + ": original report preserved", inner(mul(F, u), mul(kron(E, eye(2)), mul(F, u))) == Q)
        direct = mul(mul(mul(kron(transpose(D), eye(2)), comparator(scale(K(Fraction(1, 2)), sub(eye(d), Zport)))), kron(D, eye(2))), CP)
        check(name + ": literal complete comparison order", direct == F)
        mark = mul(kron(D, eye(2)), CP)
        check(name + ": initialized original marked geometry", mul(mark, u) == kron(mul(D, b), v))
        check(name + ": full mark is a genuine precomposition", mark != kron(D, eye(2)))
        V = kron(F, eye(2))
        check(name + ": last-spectator target is SO", mul(transpose(V), V) == eye(4*d) and ro.det(V) == one)
        repeated = eye(2*d)
        x = K(2)*Q-one
        cheb = [one, x, K(2)*x*x-one, K(4)*x*x*x-K(3)*x]
        repeated_traces = []
        for k in (1, 2, 3):
            repeated = mul(repeated, F)
            rhs = K(d)+K(2)*cheb[k]+K(d//2-1)*K(1+(-1)**k)
            check(name + ": repeated full trace Chebyshev k=" + str(k), trace(repeated) == rhs)
            repeated_traces.append(trace(repeated).encoded())
        return V, {"name": name, "original_bank_dimension": d, "Q_actual": Q.encoded(),
                   "cold_corner": inner(u, mul(F, u)).encoded(), "trace_F": trace(F).encoded(),
                   "trace_F_power_1_2_3": repeated_traces}

    bank = kron(v, v)
    Z4 = [[(one if i < 2 else -one) if i == j else zero for j in range(4)] for i in range(4)]
    words = [
        ("native_G_CX_three", [("G", (0,)), ("CX", (0, 1)), ("G", (1,))]),
        ("native_G_CX_six", [("G", (0,)), ("CX", (0, 1)), ("G", (1,)),
                            ("G", (0,)), ("CX", (1, 0)), ("G", (1,))]),
    ]
    rows = []
    for name, word in words:
        D = replay(2, word)
        check(name + ": unchanged native owner all-column match", D == env["owner_word"](word))
        _, row = make_fixture(D, bank, Z4, name)
        row["native_calls"] = len(word)
        rows.append(row)
    check("two actual native fixtures have different Q", rows[0]["Q_actual"] != rows[1]["Q_actual"])

    # Smallest true clock: one original bank bit, one flag, last spectator.
    # Use the SHA-pinned original SR G1--G6 constructor unchanged.
    Z2 = [[one, zero], [zero, -one]]
    Vsmall, smallrow = make_fixture(ro.G, v, Z2, "one_G_clock_bank")
    T, R, dims, g, prefix = env["true_clock"](Vsmall, 2)
    w = [[-p], [ro.a]]
    Plast = kron(eye(4), mul(w, transpose(w)))
    check("actual clock incidence isometry", mul(transpose(R), R) == eye(8))
    check("full growing clock unitarity", mul(transpose(T), T) == eye(len(T)))
    check("real intermediate G and final target retained", prefix != eye(8) and mul(g, prefix) == Vsmall)
    check("no shorter clock wrap", trace(T) == zero)
    check("shortest wrap reads full flag, not a character", trace(mul(T, T)) == K(2)*trace(mul(Plast, Vsmall)))
    check("shortest trace equals complete repeated source", trace(mul(Plast, Vsmall)) == K(2)+trace(Z2)-K(2)+K(4)*K(smallrow["Q_actual"]))

    receipt = {
        "schema": "full-flag-original-comparison-exact-v1", "status": "PASS",
        "field": "Q[a]/(a^4+a^2-1), a positive, p=a^2",
        "arithmetic": "exact rational polynomial reduction; no floating tolerance",
        "checks": len(checks), "check_names": checks,
        "owners": [
            {"path": PRIMARY, "block": "RO-NATIVE-GOLDEN-CHECK", "code_sha256": RO_HASH},
            {"path": PRIMARY, "block": "SR-ORIGINAL-READER-CLOCK-CHECK", "code_sha256": SR_HASH,
             "reused_functions": sorted(names)},
            {"path": NATIVE, "sha256": sha((root / NATIVE).read_bytes())},
            {"path": CLOCK, "sha256": sha((root / CLOCK).read_bytes())},
        ],
        "checker_sha256": sha(Path(__file__).read_bytes().replace(b"\r\n", b"\n")),
        "native_reader_cases": rows, "small_clock_reader": smallrow,
        "clock": {"stage_dimensions": dims, "clock_dimension": len(T), "L": 2,
                  "trace_T": trace(T).encoded(), "trace_T_squared": trace(mul(T, T)).encoded()},
        "scope": [
            "Q is the actual fixture probability; no READY factor or GR source constant is invented.",
            "Both full character sectors, canonical flag and last spectator remain in the target and clock.",
            "The clock has three separate births, a nonidentity native G stage, and one ideal final target.",
            "CP/CE and final targets are not claimed emitted exact native words; all GR compilation remains analytic.",
            "k=1,2,3 illustrates the exact Chebyshev law; it does not numerically prove an infinite classification.",
            "No old suite is rerun; only its SHA-pinned arithmetic/native/clock helper definitions are reused.",
        ],
    }
    args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "checks": len(checks), "output": str(args.out.resolve()),
                      "receipt_sha256": sha(args.out.read_bytes())}))


if __name__ == "__main__":
    main()
