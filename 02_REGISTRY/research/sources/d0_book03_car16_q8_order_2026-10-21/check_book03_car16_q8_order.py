#!/usr/bin/env python3
"""Exact Book 03 order comparator on the original CAR16 Spin/Q8 carrier.

This composes the pinned Q8 word and Golden two-port with the existing
four-mode Jordan-Wigner CAR16 representation.  The arm and retained record
are explicit apparatus factors.  The result is conditional representation
evidence, not physical G0 admission, full-price selection, or GR closure.
"""

from pathlib import Path
import hashlib
import json
import re
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PINS = json.loads((HERE / "SOURCE_PINS.json").read_text())

a, p = sp.symbols("a p")
relations = sp.groebner([a**2 - p, p**2 + p - 1], a, p)


def reduce_expr(value):
    return relations.reduce(sp.expand(value))[1]


def sparse_reduced(matrix):
    matrix = sp.SparseMatrix(matrix)
    entries = {}
    for key, value in matrix.todok().items():
        result = reduce_expr(value)
        if result != 0:
            entries[key] = result
    return sp.SparseMatrix(matrix.rows, matrix.cols, entries)


def matrix_equal(left, right):
    left = sp.SparseMatrix(left)
    right = sp.SparseMatrix(right)
    difference = left - right
    return all(reduce_expr(value) == 0 for value in difference.todok().values())


checks = []


def check(label, condition):
    if not bool(condition):
        raise AssertionError(label)
    checks.append(label)


def source_matrix(source, marker):
    block = source.split(marker, 1)[1].split("!![", 1)[1].split("]", 1)[0]
    return sp.Matrix(
        [[sp.sympify(value) for value in row.split(",")] for row in block.split(";")]
    )


# Pin and read the actual formal and Book owners consumed by this replay.
inputs = {}
source_text = {}
for item in PINS["files"]:
    path = item["path"]
    data = (ROOT / path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    check(f"pinned input bytes: {path}", digest == item["sha256"])
    source_text[path] = data.decode("utf-8")
    inputs[path] = {"sha256": digest, "git_blob": item["git_blob"]}

BOOK = "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md"
VERIFY = "04_CERTIFICATES/order_memory_control_verify.py"
GOLDEN = "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean"
CONTROL = "03_FORMALIZATION/D0/Representation/OrderMemoryControl.lean"
READOUT = "03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean"
CLOCK = "03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean"
SPIN_CHECK = (
    "02_REGISTRY/research/sources/d0_native_spin_q8_car16_2026-10-20/"
    "check_original_car16_clifford_spin_golden.py"
)
CAR_RELATIONS = "03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean"
CAR_DIRAC = "03_FORMALIZATION/D0/Geometry/ArchiveCARDirac.lean"

book = source_text[BOOK]
verify = source_text[VERIFY]
golden = source_text[GOLDEN]
control = source_text[CONTROL]
readout = source_text[READOUT]
clock_source = source_text[CLOCK]
spin_check = source_text[SPIN_CHECK]
car_relations = source_text[CAR_RELATIONS]
car_dirac = source_text[CAR_DIRAC]

check("Book03 states the exact two chronological comparator words",
      "`X X X X Y Y Y Y` and `X Y X X X Y Y Y`" in book)
check("Book03 retains the relative-sign and Golden readout boundary",
      "physical port addressability, initial apparatus preparation" in book
      and "M1-admissible" in book)
check("formal Q8 controller uses the owned local i and common j matrices",
      "def localIQ : M8Q := fromBlocks 1 0 0 (spin 2)" in control
      and "def commonJQ : M8Q := fromBlocks (spin 4) 0 0 (spin 4)" in control)
check("formal forward words have the pinned order/identity group products",
      "commonJQ ^ 3 * localIQ ^ 3 * commonJQ * localIQ = relativeSignQ" in control
      and "commonJQ ^ 4 * localIQ ^ 4 = 1" in control)
control_compact = re.sub(r"\s+", " ", control)
check("the Book03 controller mixer equals its Golden two-port gate",
      "def mixer (a p : ℝ) : M8R := fromBlocks (a • (1 : M4R)) ((-p) • (1 : M4R)) (p • (1 : M4R)) (a • (1 : M4R))" in control_compact)
check("formal 16-stage clock is a supplied reversible schedule",
      "abbrev Clock := ZMod 16" in clock_source
      and "theorem completed_stage" in clock_source)
check("CAR16 source is the original four-mode Jordan-Wigner construction",
      "ArchiveFockState" in car_relations
      and "fockGamma" in car_dirac
      and "Jordan-Wigner" in spin_check)

# Reconstruct the exact original four-mode CAR matrices on the existing
# ArchiveFockState = Role -> Bool carrier (integer basis 0,...,15).
identity16 = sp.eye(16)
zero16 = sp.zeros(16)
creation = []
for mode in range(4):
    matrix = sp.zeros(16)
    for state in range(16):
        if not (state & (1 << mode)):
            sign = (-1) ** bin(state & ((1 << mode) - 1)).count("1")
            matrix[state | (1 << mode), state] = sign
    creation.append(matrix)
annihilation = [matrix.T for matrix in creation]

for left in range(4):
    for right in range(4):
        check(
            f"original CAR anticommutators ({left},{right})",
            creation[left] * creation[right]
            + creation[right] * creation[left] == zero16
            and annihilation[left] * annihilation[right]
            + annihilation[right] * annihilation[left] == zero16
            and annihilation[left] * creation[right]
            + creation[right] * annihilation[left]
            == (identity16 if left == right else zero16),
        )

gamma = [annihilation[0] + creation[0]] + [
    creation[mode] - annihilation[mode] for mode in (1, 2, 3)
]
signature = (1, -1, -1, -1)
parity = sp.diag(*[(-1) ** bin(state).count("1") for state in range(16)])
for mu in range(4):
    for nu in range(4):
        target = 2 * signature[mu] * identity16 if mu == nu else zero16
        check(f"CAR16 real Cl(1,3) relation ({mu},{nu})",
              gamma[mu] * gamma[nu] + gamma[nu] * gamma[mu] == target)
    check(f"CAR16 generator {mu} is parity-odd",
          parity * gamma[mu] == -gamma[mu] * parity)

q_i = gamma[2] * gamma[3]
q_j = gamma[3] * gamma[1]
q_k = gamma[1] * gamma[2]
check("CAR16 Q8 squares and oriented product",
      q_i**2 == -identity16 and q_j**2 == -identity16
      and q_k == q_i * q_j == -q_j * q_i)
check("CAR16 Q8 generators are parity-even and orthogonal",
      all(q * parity == parity * q and q.T * q == identity16
          for q in (q_i, q_j, q_k)))
q8_car16 = [identity16, -identity16, q_i, -q_i, q_j, -q_j, q_k, -q_k]
check("the CAR16 Q8 representation is faithful",
      len({tuple(matrix) for matrix in q8_car16}) == 8)

# Compare all 64 products to the exact Fin-8 Q8 ordering used by Book03's
# OrderMemoryReadout.spin, not merely to an independently chosen convention.
q_a, q_b, q_c, q_d = sp.symbols("a b c d")
left_template = source_matrix(readout, "def left")


def left_quaternion(aa, bb, cc, dd):
    return left_template.subs(
        {q_a: aa, q_b: bb, q_c: cc, q_d: dd}, simultaneous=True
    )


q8_book = [
    left_quaternion(1, 0, 0, 0),
    left_quaternion(-1, 0, 0, 0),
    left_quaternion(0, 1, 0, 0),
    left_quaternion(0, -1, 0, 0),
    left_quaternion(0, 0, 1, 0),
    left_quaternion(0, 0, -1, 0),
    left_quaternion(0, 0, 0, 1),
    left_quaternion(0, 0, 0, -1),
]
readout_compact = re.sub(r"\s+", " ", readout)
check("Q8 label order matches the existing Fin-8 spin table",
      "def spin : Fin 8 → M4 := ![left 1 0 0 0, left (-1) 0 0 0, left 0 1 0 0, left 0 (-1) 0 0, left 0 0 1 0, left 0 0 (-1) 0, left 0 0 0 1, left 0 0 0 (-1)]" in readout_compact)


def matrix_key(matrix):
    return tuple(sp.simplify(value) for value in matrix)


book_product_to_label = {matrix_key(matrix): label
                         for label, matrix in enumerate(q8_book)}
check("Book03 Q8 matrices enumerate eight distinct group elements",
      len(book_product_to_label) == 8)
for left_label, left_matrix in enumerate(q8_book):
    for right_label, right_matrix in enumerate(q8_book):
        product_label = book_product_to_label[matrix_key(left_matrix * right_matrix)]
        check(
            f"CAR16 intertwines Book03 Q8 product ({left_label},{right_label})",
            q8_car16[product_label] == q8_car16[left_label] * q8_car16[right_label],
        )

# The book's Golden gate is parsed from its Lean definition. The quotient
# Q[a,p]/(a^2-p, p^2+p-1) supplies exact orthogonality, with p=phi^-1>0.
golden_gate = source_matrix(golden, "def gate")
check("parsed Golden gate is exactly the Book03 two-port map",
      golden_gate == sp.Matrix([[a, -p], [p, a]]))
identity2 = sp.eye(2)
arm_splitter = sp.SparseMatrix(golden_gate)
arm_spin_gate = sp.kronecker_product(arm_splitter, sp.SparseMatrix(identity16))
arm_spin_gate = sp.SparseMatrix(arm_spin_gate)

local_i = sp.SparseMatrix(sp.diag(identity16, q_i))
common_j = sp.SparseMatrix(sp.diag(q_j, q_j))
record_identity = sp.SparseMatrix(identity2)

def with_record(gate):
    return sp.SparseMatrix(sp.kronecker_product(gate, record_identity))


gates = {
    "G": with_record(arm_spin_gate),
    "X": with_record(local_i),
    "Y": with_record(common_j),
}

write = sp.SparseMatrix(64, 64, {})
for arm in range(2):
    for spin in range(16):
        for bit in range(2):
            old = 32 * arm + 2 * spin + bit
            new = 32 * arm + 2 * spin + (bit ^ arm)
            write[new, old] = 1
gates["WRITE"] = write
gates["idle"] = sp.SparseMatrix(sp.eye(64))

for name, gate in gates.items():
    check(f"64-coordinate apparatus primitive {name} is orthogonal",
          matrix_equal(gate.T * gate, sp.SparseMatrix(sp.eye(64))))
check("record operation is its own reversible inverse", write * write == sp.eye(64))

identity_word = ["X"] * 4 + ["Y"] * 4
order_word = ["X", "Y"] + ["X"] * 3 + ["Y"] * 3


def program(word):
    # Chronological list; X^2 G X^2 is the forward implementation of G^T.
    return ["G"] + word + ["X"] * 2 + ["G"] + ["X"] * 2 + ["WRITE"]


programs = {
    "identity": program(identity_word),
    "order": program(order_word),
}
check("both Book03 trials have the same 15 chronological stages",
      len(programs["identity"]) == len(programs["order"]) == 15)
check("identity and order words match the pinned exact checker",
      "order_word = [\"local_i\", \"common_j\"] + [\"local_i\"]*3 + [\"common_j\"]*3" in verify
      and "identity_word = [\"local_i\"]*4 + [\"common_j\"]*4" in verify)
check("both clock schedules append the same reversible idle stage",
      all(names[-1] == "WRITE" and len(names + ["idle"]) == 16
          for names in programs.values()))

initial = sp.SparseMatrix(64, 16, {})
for spin in range(16):
    initial[2 * spin, spin] = 1  # arm 0, any CAR16 input, record 0.
record_one = sp.SparseMatrix(sp.kronecker_product(sp.eye(32), sp.diag(0, 1)))
record_zero = sp.SparseMatrix(sp.kronecker_product(sp.eye(32), sp.diag(1, 0)))
arm_one = sp.SparseMatrix(sp.diag(*([0] * 32 + [1] * 32)))

traces = {}
effects = {}
for label, names in programs.items():
    state = initial
    trace = [state]
    for stage, name in enumerate(names, start=1):
        state = sparse_reduced(gates[name] * state)
        trace.append(state)
        check(f"{label} preserves every CAR16 input norm at stage {stage}",
              matrix_equal(state.T * state, sp.eye(16)))
    traces[label] = trace

    effect_one = sparse_reduced(state.T * record_one * state)
    effect_zero = sparse_reduced(state.T * record_zero * state)
    expected_one = sp.zeros(16) if label == "identity" else 4 * p**3 * identity16
    expected_zero = identity16 if label == "identity" else p**6 * identity16
    check(f"{label} record-one effect on all CAR16 inputs",
          matrix_equal(effect_one, expected_one))
    check(f"{label} record-zero effect on all CAR16 inputs",
          matrix_equal(effect_zero, expected_zero))
    check(f"{label} record is exactly the output arm",
          matrix_equal(record_one * state, arm_one * state))
    check(f"{label} complete record effects normalize to identity",
          matrix_equal(effect_one + effect_zero, identity16))
    effects[label] = {
        "record_one": "0*I16" if label == "identity" else "4*p^3*I16",
        "record_zero": "1*I16" if label == "identity" else "p^6*I16",
    }

# Build the exact 16-stage reversible clock on clock x arm x CAR16 x record.
# The final idle wraps the finite clock but is not among the first 15 operations.
def clock_operator(names):
    dimension = 16 * 64
    entries = {}
    for stage, name in enumerate(names + ["idle"]):
        for (row, column), value in gates[name].todok().items():
            entries[(64 * ((stage + 1) % 16) + row,
                     64 * stage + column)] = value
    return sp.SparseMatrix(dimension, dimension, entries)


clock_machines = {label: clock_operator(names) for label, names in programs.items()}
clock_identity = sp.SparseMatrix(1024, 1024,
                                 {(index, index): 1 for index in range(1024)})
for label, machine in clock_machines.items():
    check(f"{label} 16-stage clock transition is reversible",
          matrix_equal(machine.T * machine, clock_identity))
    state = sp.SparseMatrix(1024, 16,
                            {(row, col): value
                             for (row, col), value in initial.todok().items()})
    for stage in range(1, 16):
        state = sparse_reduced(machine * state)
        expected = sp.SparseMatrix(
            1024, 16,
            {(64 * stage + row, col): value
             for (row, col), value in traces[label][stage].todok().items()},
        )
        check(f"{label} internal clock realizes CAR16 stage {stage}",
              matrix_equal(state, expected))

# One fixed device retains the program choice as a basis label. This is a
# mathematical reversible construction; its physical admission remains open.
fixed_machine = sp.diag(clock_machines["identity"], clock_machines["order"])
fixed_machine = sp.SparseMatrix(fixed_machine)
fixed_identity = sp.SparseMatrix(2048, 2048,
                                 {(index, index): 1 for index in range(2048)})
check("one 2048-coordinate fixed programmed clock is reversible",
      matrix_equal(fixed_machine.T * fixed_machine, fixed_identity))
for program_bit, label in enumerate(("identity", "order")):
    state = sp.SparseMatrix(
        2048, 16,
        {(1024 * program_bit + row, col): value
         for (row, col), value in initial.todok().items()},
    )
    for _stage in range(1, 16):
        state = sparse_reduced(fixed_machine * state)
    expected = sp.SparseMatrix(
        2048, 16,
        {(1024 * program_bit + 64 * 15 + row, col): value
         for (row, col), value in traces[label][15].todok().items()},
    )
    check(f"stored program label {program_bit} keeps the exact CAR16 result",
          matrix_equal(state, expected))

# Hostile control: replacing only-arm X by common X removes the distinction.
global_i = sp.SparseMatrix(sp.diag(q_i, q_i))
negative_gates = dict(gates, X=with_record(global_i))
negative_effects = {}
for label, names in programs.items():
    state = initial
    for name in names:
        state = sparse_reduced(negative_gates[name] * state)
    negative_effects[label] = sparse_reduced(state.T * record_one * state)
check("global-i negative control erases the order contrast",
      matrix_equal(negative_effects["identity"], negative_effects["order"]))

result = {
    "status": "PASS",
    "source_checkpoint": PINS["source_checkpoint"],
    "checks_passed": len(checks),
    "checks": checks,
    "representation": {
        "carrier": "original four-mode CAR16 Fock space",
        "q8_generators": ["Gamma^2 Gamma^3", "Gamma^3 Gamma^1", "Gamma^1 Gamma^2"],
        "faithful": True,
        "parity_even": True,
        "arm_times_car16_times_record_dimension": 64,
        "programmed_16_stage_clock_dimension": 2048,
    },
    "exact_ring": ["a^2=p", "p^2+p=1"],
    "chronological_operations": 15,
    "clock_labels_including_idle": 16,
    "record_effects": effects,
    "hostile_control": "common-i on both arms gives identical record effects",
    "scope": {
        "physical_G0_admission": False,
        "physical_port_addressability": False,
        "physical_paid_actuation": False,
        "field_to_Q8_pullback": False,
        "full_Book03_Cost_Info": False,
        "GR_closed": False,
    },
    "input_pins": inputs,
}
(HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: value for key, value in result.items() if key != "checks"},
                 ensure_ascii=False, indent=2))
