#!/usr/bin/env python3
"""Exact local checks for the H.1 code-tail/weighted-history witness.

No claim of a Book03 physical price, actual admission of the added reader, or
GR closure. All matrix equalities use the copied original native executor and
its algebraic field Q(sqrt(phi^-1)). Run with python3 -B and python3 -B -O.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as sp

HERE = Path(__file__).resolve().parent
NATIVE_PATH = HERE / "inputs" / "native_execution.py"
NATIVE_SHA256 = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
if hashlib.sha256(NATIVE_PATH.read_bytes()).hexdigest() != NATIVE_SHA256:
    raise RuntimeError("the copied native executor differs from the pinned input")
spec = importlib.util.spec_from_file_location("open_h1_native", NATIVE_PATH)
native = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = native
spec.loader.exec_module(native)

P, A, G, F = native.P, native.A, native.G_LOCAL, native.GOLDEN_FIELD
V = sp.Matrix([A, P])
ZERO = sp.Matrix([1, 0])
ONE = sp.Matrix([0, 1])
I2 = sp.eye(2)
KET = [ZERO, ONE]
PROJ = [v * v.T for v in KET]
checks = []

# Every copied excerpt is checked against the original start-package receipt.
receipt = json.loads((HERE / "inputs" / "receipt.json").read_text())
for row in receipt["sources"]:
    copied = HERE / "inputs" / Path(row["output"]).name
    if copied.exists():
        if hashlib.sha256(copied.read_bytes()).hexdigest() != row["export_sha256"]:
            raise RuntimeError("input hash mismatch: " + row["id"])
        checks.append("receipt SHA-256 " + row["id"])


def require(ok, name):
    if not bool(ok):
        raise AssertionError(name)
    checks.append(name)


def scalar_eq(x, y):
    return F.from_sympy(sp.expand(x - y)) == F.zero


def matrix_eq(x, y):
    x, y = sp.Matrix(x), sp.Matrix(y)
    return x.shape == y.shape and all(scalar_eq(z, 0) for z in x - y)


def exact(condition, name):
    require(condition, name)


def gate(op, *wires):
    return native.Gate(op, tuple(wires))


def matrix(n, word, profile=native.G_CX, port=None, spin=None):
    execution = native.Execution(n, (), (), tuple(word), profile, port, spin)
    return native.word_matrix(execution, max_qubits=n, max_expanded_stages=100)


def qexecution(n, word):
    return native.Execution(n, (), (), tuple(word), native.G_CX)


def one_gate(n, item):
    execution = qexecution(n, [item])
    return native.gate_matrix(execution, item, max_qubits=n, max_expanded_stages=100)


exact(scalar_eq(P + P**2, 1), "Golden normalization")
exact(matrix_eq(G.T * G, I2), "native G is orthogonal")
exact(matrix_eq(G * ZERO, V), "actual canonical birth v equals G|0>")
exact(matrix_eq(G.T * V, ZERO), "one paid inverse prepares zero from v")
exact(scalar_eq(P - P**2, P**3), "actual golden contrast p-p^2=p^3")

# Actual E0, its L0 (two CXs) with two more CXs for a seven-call layout,
# and the exact L1. Both have the same wires and no births in these seven calls.
r, t = 0, 1
C = gate("CX", r, t)
Gt = gate("G", t)
E0 = (C, Gt, C)
L0 = (C, C)
L1 = (Gt, C, Gt, C)
word0 = E0 + L0 + (C, C)
word1 = E0 + L1
exact(len(word0) == len(word1) == 7, "both honest prefix layouts have seven calls")
exact(tuple(g.op for g in word0).count("G") == 1 and
      tuple(g.op for g in word0).count("CX") == 6, "prefix 0 inventory 1G 6CX")
exact(tuple(g.op for g in word1).count("G") == 3 and
      tuple(g.op for g in word1).count("CX") == 4, "prefix 1 inventory 3G 4CX")
U0, U1 = matrix(2, word0), matrix(2, word1)
J = sp.kronecker_product(I2, V)
P0 = sp.diag(1, 1, 0, 0)
P1 = sp.diag(0, 0, 1, 0)
PBAD = sp.diag(0, 0, 0, 1)
for name, U, tail0 in (("0", U0, G * V), ("1", U1, G**3 * V)):
    expected = sp.Matrix.hstack(sp.kronecker_product(ZERO, tail0),
                                sp.kronecker_product(ONE, ZERO))
    exact(matrix_eq(U * J, expected), "initialized output on every r column " + name)
    for label, projector, target in (("0", P0, PROJ[0]),
                                     ("1", P1, PROJ[1]),
                                     ("invalid", PBAD, sp.zeros(2))):
        exact(matrix_eq(J.T * U.T * projector * U * J, target),
              "exact original effect " + label + " prefix " + name)

# Two mathematical paths through the actual born tail. No extra path record is
# postulated; the path split is just a resolution of the original amplitude.
v0, v1 = sp.Matrix([A, 0]), sp.Matrix([0, P])
in0, in1 = sp.kronecker_product(ONE, v0), sp.kronecker_product(ONE, v1)
unit_bad = sp.kronecker_product(ONE, ONE)
path0, path1 = PBAD * U0 * in0, PBAD * U0 * in1
exact(matrix_eq(path0, -A * P * unit_bad), "invalid path 0 is -ap")
exact(matrix_eq(path1, A * P * unit_bad), "invalid path 1 is +ap")
exact(matrix_eq(path0 + path1, sp.zeros(4, 1)), "actual invalid path cancellation")
exact(scalar_eq(A**2 * P**2, P**3), "invalid mismatch coefficient is p^3")
# Hostile illustrative scalar reweighting, not an admitted price or law.
exact(scalar_eq((path0 + P * path1).dot(path0 + P * path1), P**7),
      "unequal illustrative path weights create p^7 invalid mass")
zeta = sp.symbols("zeta", real=True)
invalid_tilt = P**3 * (1 - sp.exp(-zeta))**2
exact(sp.diff(invalid_tilt, zeta).subs(zeta, 0) == 0,
      "invalid probability has zero first derivative at a dark point")
exact(scalar_eq(sp.diff(invalid_tilt, zeta, 2).subs(zeta, 0), 2*P**3),
      "invalid probability detects a relative tilt at second order")

# Exact paid inverse compiler from the already admitted SourceI profile.
# PORT=0, opaque Spin=(1,2), the live target wire is 3. No extra source-spin gate.
def inverse_route(n):
    swap = (gate("CX", 0, 3), gate("CX", 3, 0), gate("CX", 0, 3))
    source = gate("SourceI", 0, 1, 2)
    return swap + (source, source) + (gate("G", 0),) * n + (source, source) + swap

for n in (1, 2):
    word = inverse_route(n)
    exact(len(word) == n + 10, "paid inverse length n=" + str(n))
    actual = matrix(4, word, native.G_CX_SOURCE_I, 0, (1, 2))
    target = sp.kronecker_product(sp.eye(8), G.T**n)
    exact(matrix_eq(actual, target), "routed inverse on every port/Spin/target column n=" + str(n))

# The flag is born at v, not at zero. CX(t,f) gives this exact effect on t.
Ctflag = matrix(2, (gate("CX", 0, 1),))
Jflag = sp.kronecker_product(I2, V)
flag_effect = Jflag.T * Ctflag.T * sp.kronecker_product(I2, PROJ[1]) * Ctflag * Jflag
exact(matrix_eq(flag_effect, sp.diag(P**2, P)), "v-born flag has effect diag(p^2,p)")
exact(not matrix_eq(flag_effect, PROJ[1]), "hostile zero-blank substitution rejected")

# The same E0 adds a legal 0/10 report to an arbitrary (possibly entangled)
# copied pointer; this independently verifies both additional output encoders.
Uenc = matrix(2, E0)
exact(matrix_eq(J.T * Uenc.T * P1 * Uenc * J, PROJ[1]), "new encoder preserves all pointer columns")
exact(matrix_eq(J.T * Uenc.T * PBAD * Uenc * J, sp.zeros(2)), "new encoder has no initialized 11")

# Entire nontrivial test, with a born-then-paid-zero archive c and a born flag f.
# The two new code tails factor out by the verified E0 identity just above.
# r,t,c,f order; the controlled archive is copied before t is touched.
J4 = sp.kronecker_product(I2, V, ZERO, V)
inv_t = sp.kronecker_product(I2, G.T**2, I2, I2)
copy_r_c = gate("CX", 0, 2)
copy_t_f = gate("CX", 1, 3)
flag_copy = one_gate(4, copy_t_f)
qq = sp.symbols("q", real=True)
d = 4 * P**6
s = P**2 + d
probabilities = []
for which, word in ((0, word0), (1, word1)):
    Upre = matrix(4, word + (copy_r_c,))
    W = flag_copy * inv_t * Upre * J4
    s0, s1 = ((P**2, s) if which == 0 else (s, s))
    for b in (0, 1):
        for f in (0, 1):
            event = sp.kronecker_product(I2, I2, PROJ[b], PROJ[f])
            effect = W.T * event * W
            sb = s0 if b == 0 else s1
            factor = sb if f == 1 else 1 - sb
            expected = factor * PROJ[b]
            exact(matrix_eq(effect, expected),
                  "joint original/new marked effect k%d b%d f%d" % (which, b, f))
    r = (1 - qq) * s0 + qq * s1
    probabilities.append(r)

# Same prefixes must give the same effects, not a manufactured contrast.
exact(scalar_eq(probabilities[0].subs(qq, 0), P**2), "branch zero of k0 uses actual v-born flag")
exact(scalar_eq(probabilities[1].subs(qq, 0), s), "branch zero of k1 changes the future mark")
exact(sp.simplify(sp.diff(probabilities[0], qq) - d) == 0, "future source k0 is 4p^6 Dq")
exact(sp.simplify(sp.diff(probabilities[1], qq)) == 0, "future source k1 vanishes")
exact(scalar_eq(probabilities[1].subs(qq, 0) - probabilities[0].subs(qq, 0), d),
      "same-prefix negative control and distinct-tail positive contrast")
exact(scalar_eq((G * V).dot(G**3 * V), P**3), "conditional unread-tail overlap is p^3")
exact(scalar_eq((G * V).dot(G * V), 1) and scalar_eq((G**3 * V).dot(G**3 * V), 1),
      "both conditional tails are normalized")
exact(scalar_eq((G.T**2 * ZERO)[0]**2, P**6), "without archive old 10 support drops to p^6")
exact(scalar_eq((G.T**2 * ZERO)[1]**2, 4 * P**3), "without archive invalid 11 mass becomes 4p^3")

# General pair E0;L_k and E0;L_(k+n), after equal-count CX^2
# padding of the shorter word. The suffix uses the actual inverse G^[-2(k+1)].
# These exact examples validate the all-k,n symbolic derivation in the note.
def echo(k):
    return (Gt,) * k + (C,) + (Gt,) * k + (C,)

def sm(m):
    return P**2 + P**3 * (G**(2*m) * ZERO)[1]**2

for k, n in ((1, 1), (1, 2), (2, 1)):
    lower = E0 + echo(k) + (C,) * (2*n)
    upper = E0 + echo(k+n)
    exact(len(lower) == len(upper) == 2*(k+n)+5,
          "general equal-count prefix k%d n%d" % (k, n))
    test_inverse = sp.kronecker_product(I2, G.T**(2*(k+1)), I2, I2)
    for which, word in enumerate((lower, upper)):
        W = flag_copy * test_inverse * matrix(4, word + (copy_r_c,)) * J4
        s0 = P**2 if which == 0 else sm(n)
        s1 = sm(k+1)
        for b in (0, 1):
            for f in (0, 1):
                event = sp.kronecker_product(I2, I2, PROJ[b], PROJ[f])
                sb = s0 if b == 0 else s1
                expected = (sb if f else 1-sb) * PROJ[b]
                exact(matrix_eq(W.T * event * W, expected),
                      "general joint effect k%d n%d version%d b%d f%d" %
                      (k, n, which, b, f))
    exact(not scalar_eq(sm(n), P**2), "general future mark really separates n%d" % n)

# Actual additional finite layout (not counting any physical reader).
# c born + inverse G + copy; d born + original E0; f born + inverse G^2
# on old tail + CX; u born + original E0. The 4-qubit spectator proof above
# and the all-column inverse/E0 checks cover this compositional programme.
def route_for(target, n):
    swap = (gate("CX", 0, target), gate("CX", target, 0), gate("CX", 0, target))
    source = gate("SourceI", 0, 1, 2)
    return swap + (source, source) + (gate("G", 0),) * n + (source, source) + swap

def encode_for(pointer, tail):
    return (gate("CX", pointer, tail), gate("G", tail), gate("CX", pointer, tail))

# Ten-wire syntax validation includes a protected old-right spectator on wire 9.
# The initial live set has the original port, opaque Spin, pointer and direct tail.
# Sequence items ("birth", wire) are checked locally, not mislabelled native gates.
layout = [("birth", 5)] + list(route_for(5, 1)) + [gate("CX", 3, 5)]
layout += [("birth", 6)] + list(encode_for(5, 6))
layout += [("birth", 7)] + list(route_for(4, 2)) + [gate("CX", 4, 7)]
layout += [("birth", 8)] + list(encode_for(7, 8))
live = {0, 1, 2, 3, 4, 9}
actual_gates = []
births = []
for item in layout:
    if isinstance(item, tuple) and item[0] == "birth":
        require(item[1] not in live, "fresh born wire " + str(item[1]))
        live.add(item[1])
        births.append(item[1])
    else:
        require(set(item.wires) <= live, "only live gate operands %02d" % len(actual_gates))
        actual_gates.append(item)
execution = native.Execution(10, (), (9,), tuple(actual_gates),
                             native.G_CX_SOURCE_I, 0, (1, 2), (5, 7))
native.validate_execution(execution, max_qubits=10, max_expanded_stages=31)
counts = {"births": len(births), **{op: sum(g.op == op for g in actual_gates)
                                    for op in ("G", "CX", "SourceI")}}
exact(counts == {"births": 4, "G": 5, "CX": 18, "SourceI": 8},
      "literal added layout counts 4 births and 31 primitive calls")
exact(len(layout) == 35, "added layout contains 35 real pre-reader stages")

# Numerical checks are diagnostics only; the argument uses strict concavity
# and the closed-form Golden identities, not these floating-point values.
p = float(sp.N(P, 30))
ell = math.log(1.0 / p)
DD = 4 * p**6
ss = p**2 + DD
binary_h = lambda x: -x * math.log(x) - (1-x) * math.log(1-x)
score = lambda x: 1 + x - binary_h(x) / ell
q_sample = 0.45
sample_marginal = p**2 + DD*q_sample
mi = binary_h(sample_marginal) - ((1-q_sample)*binary_h(p**2) + q_sample*binary_h(ss))
require(0 < p**2 < ss < 1, "strict positive flag collar")
require(abs(score(p**2)) < 1e-12 and score(ss) > 0, "strict positive extra CQ/code contrast")
require(mi > 1e-6, "hostile marginal entropy loses record correlation")

print(json.dumps({
    "status": "PASS",
    "checks": len(checks),
    "check_names": checks,
    "native_sha256": NATIVE_SHA256,
    "p": p,
    "future_probability_delta": DD,
    "second_flag_high_s": ss,
    "specified_incremental_CQ_code_gain": score(ss),
    "conditional_tail_overlap": p**3,
    "conditional_tail_trace_distance": math.sqrt(1-p**6),
    "sample_q_is_only_a_diagnostic": q_sample,
    "sample_classical_mutual_information_nats": mi,
    "additional_layout_before_readers": counts,
    "complete_physical_cost_info_bound_proved": False,
    "added_reader_admission_proved": False,
    "GR_closed": False,
}, sort_keys=True, indent=2))
