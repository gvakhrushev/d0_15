#!/usr/bin/env python3
"""Exact forward program, internal clock and detector-record construction.

All arithmetic is reduced modulo a^2=p, p^2+p=1; numerical interpretation
chooses p=phi^-1>0 and a=sqrt(p)>0. No simulation samples or external data.
"""
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
paths = [
    "09_LEAN_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean",
    "09_LEAN_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
    "09_LEAN_FORMALIZATION/D0/Representation/OrderMemoryControl.lean",
    "09_LEAN_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean",
]
source = [(ROOT / p).read_text() for p in paths]


def matrix_after(text, marker):
    body = text.split(marker, 1)[1].split("!![", 1)[1].split("]", 1)[0]
    return S.Matrix([[S.sympify(x) for x in row.split(",")] for row in body.split(";")])


a, p = S.symbols("a p")
relations = S.groebner([a*a-p, p*p+p-1], a, p)


def reduce(x):
    return relations.reduce(S.expand(x))[1]


def reduced(M):
    return M.applyfunc(reduce)


checks = []


def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)


def eq(A, B):
    return all(reduce(v) == 0 for v in S.SparseMatrix(A-B).todok().values())


left = matrix_after(source[0], "def left")
qa, qb, qc, qd = S.symbols("a b c d")
Li = left.subs({qa: 0, qb: 1, qc: 0, qd: 0})
Lj = left.subs({qa: 0, qb: 0, qc: 1, qd: 0})
B2 = matrix_after(source[1], "def gate")
Ci8 = S.diag(S.eye(4), Li)
Gj8 = S.diag(Lj, Lj)
Z8 = S.diag(S.eye(4), -S.eye(4))
B8 = S.kronecker_product(B2, S.eye(4))
turn8 = S.kronecker_product(S.Matrix([[0,-1],[1,0]]), S.eye(4))
check("source-controlled i produces relative sign", Ci8*Ci8 == Z8)
check("source-global j fourth power", Gj8**4 == S.eye(8))
check("forward order loop produces relative sign", Gj8**3*Ci8**3*Gj8*Ci8 == Z8)
check("inverse splitter synthesized", eq(Z8*B8*Z8, B8.T))
check("mixer commutes with arm turn", B8*turn8 == turn8*B8)
check("common j commutes with arm turn", Gj8*turn8 == turn8*Gj8)
check("relative sign violates common invariant", Z8*turn8 != turn8*Z8)

# Basis of the apparatus: arm (2) x spin coordinate (4) x record bit (2).
gates = {
    "B": S.kronecker_product(B8, S.eye(2)),
    "local_i": S.kronecker_product(Ci8, S.eye(2)),
    "common_j": S.kronecker_product(Gj8, S.eye(2)),
    "idle": S.eye(16),
}
write = S.zeros(16)
for arm in range(2):
    for spin in range(4):
        for bit in range(2):
            old = 8*arm+2*spin+bit
            new = 8*arm+2*spin+(bit ^ arm)
            write[new, old] = 1
gates["write"] = write
check("record write is reversible", write*write == S.eye(16))
for name, gate in gates.items():
    check(f"primitive norm conservation: {name}", eq(gate.T*gate, S.eye(16)))

order_word = ["local_i", "common_j"] + ["local_i"]*3 + ["common_j"]*3
identity_word = ["local_i"]*4 + ["common_j"]*4


def program(word):
    # Chronological list. The final local_i^2, B, local_i^2 implements B^T.
    return ["B"] + word + ["local_i"]*2 + ["B"] + ["local_i"]*2 + ["write"]


initial = S.zeros(16, 4)
for spin in range(4):
    initial[2*spin, spin] = 1  # arm 0, record 0; arbitrary four-coordinate input.
record1 = S.diag(*[idx % 2 for idx in range(16)])
arm1 = S.diag(*[int(idx >= 8) for idx in range(16)])
results = {}
transitions = []
completed_states = []


def execute(names, palette=gates):
    state = initial
    trajectory = [state]
    for name in names:
        state = reduced(palette[name]*state)
        trajectory.append(state)
    return state, trajectory


for label, word in (("identity", identity_word), ("order", order_word)):
    names = program(word)
    check(f"{label}: fifteen forward operations", len(names) == 15)
    final, trace = execute(names)
    for stage, state in enumerate(trace):
        check(f"{label}: arbitrary-input norm at stage {stage}", eq(state.T*state, S.eye(4)))
    weight = 0 if label == "identity" else 4*p**3
    check(f"{label}: final record weight", eq(final.T*record1*final, weight*S.eye(4)))
    check(f"{label}: record equals output arm", eq(record1*final, arm1*final))

    # Autonomous transition on clock (16) x apparatus (16) = 256 coordinates.
    # U = sum_c |c+1><c| tensor G_c; the last slot is a reversible idle wrap.
    # Only the first fifteen transitions belong to this finite protocol.
    entries = {}
    for stage, name in enumerate(names+["idle"]):
        for (row, col), value in S.SparseMatrix(gates[name]).todok().items():
            entries[(16*((stage+1) % 16)+row, 16*stage+col)] = value
    U = S.SparseMatrix(256, 256, entries)
    transitions.append(U)
    check(f"{label}: full autonomous transition orthogonal", eq(U.T*U, S.eye(256)))
    state = S.SparseMatrix(256, 4, {(row,col): value for (row,col),value in S.SparseMatrix(initial).todok().items()})
    for stage in range(1, 16):
        state = reduced(U*state)
        expected = S.SparseMatrix(256, 4, {(16*stage+row,col): value for (row,col),value in S.SparseMatrix(trace[stage]).todok().items()})
        check(f"{label}: internal stage and complete state {stage}", eq(state, expected))
    completed_states.append(state)
    results[label] = {"program": names, "record_one_exact": str(S.expand(weight)), "autonomous_nonzero_entries": len(entries)}

# A single fixed device for BOTH trials: the program label is an internal bit,
# conserved by diag(U_identity,U_order), rather than an external per-step switch.
fixed = S.SparseMatrix(S.diag(*transitions))
check("one device with stored program: orthogonal", eq(fixed.T*fixed, S.eye(512)))
for program_bit, expected_small in enumerate(completed_states):
    state = S.SparseMatrix(512, 4, {(256*program_bit+row,col): val for (row,col),val in S.SparseMatrix(initial).todok().items()})
    for _ in range(15):
        state = reduced(fixed*state)
    expected = S.SparseMatrix(512, 4, {(256*program_bit+row,col): val for (row,col),val in expected_small.todok().items()})
    check(f"stored program {program_bit}: full machine produces the same result", eq(state, expected))

# Negative control: use global i instead of the only local action everywhere.
# The hardware remains norm-preserving but the two output distributions coincide.
common_i = S.kronecker_product(S.diag(Li, Li), S.eye(2))
uncontrolled = dict(gates, local_i=common_i)
f_identity, _ = execute(program(identity_word), uncontrolled)
f_order, _ = execute(program(order_word), uncontrolled)
check("no local control: record distributions coincide", eq(f_identity.T*record1*f_identity, f_order.T*record1*f_order))
check("no local control: common weight is 4p^3", eq(f_identity.T*record1*f_identity, 4*p**3*S.eye(4)))

result = {
    "status": "PASS",
    "scope": "Constructive finite apparatus conditional on supplied local routing and initial record. Not M1 physical-realization closure.",
    "checks_passed": len(checks),
    "checks": checks,
    "source_sha256": {path: hashlib.sha256(text.encode()).hexdigest() for path,text in zip(paths,source)},
    "exact_relations": ["a^2=p", "p^2+p=1"],
    "positive_embedding": {"p": "phi^-1", "a": "sqrt(p)"},
    "resources": {"forward_comparison_operations": 14, "record_operations": 1, "clock_labels": 16, "arm_labels": 2, "spin_coordinates": 4, "record_labels": 2, "fixed_program_real_dimension": 256, "stored_program_labels": 2, "two_program_real_dimension": 512},
    "protocols": results,
    "uncontrolled_negative_control": "Both record weights are 4*p^3; contrast is zero.",
}
(HERE / "control_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in ("checks", "source_sha256", "protocols")}, ensure_ascii=False, indent=2))
