"""A strict finite code domain for the concrete retained native apparatus.

This defines an operational sector, not universal physical admissibility or a
Cost-minus-Info law.  The source-I profile explicitly uses the owned selective
active-port x quaternion-spin interface (Book03 03.26.1-2; memo 7j).  Its physical
availability is not inferred from membership in a matrix algebra.  Every gate
acts on all columns; there is no reset, measurement, postselection, arbitrary
matrix or uncharged inverse primitive in the grammar.

Wire 0 is the most significant computational bit.  Source-spin coordinates
00,01,10,11 are the original quaternion coordinates (1,i,j,k).  Gates are listed
chronologically, hence the last gate multiplies on the left.  All nonblank
input wires remain arbitrary, possibly entangled unknown inputs; old_right is
the smaller, explicitly immutable subset on which no gate may act.
"""

from dataclasses import dataclass
import json
from typing import Optional

import sympy as sp
from sympy.polys.matrices import DomainMatrix


G_CX = "G_CX"
G_CX_SOURCE_I = "G_CX_SOURCE_I"
SCHEMA = "d0.native-execution/1"

# Positive real embedding of Q(a), a^4+a^2-1=0, p=a^2=phi^-1.
P = (sp.sqrt(5) - 1) / 2
A = sp.sqrt(P)
GOLDEN_FIELD = sp.QQ.algebraic_field(A)
G_LOCAL = sp.ImmutableMatrix([[A, -P], [P, A]])
L_I = sp.ImmutableMatrix([[0, -1, 0, 0], [1, 0, 0, 0],
                          [0, 0, 0, -1], [0, 0, 1, 0]])
SOURCE_I_LOCAL = sp.ImmutableMatrix(sp.diag(sp.eye(4), L_I))


class DomainError(ValueError):
    """A code is outside the declared finite apparatus domain."""


@dataclass(frozen=True)
class Gate:
    op: str
    wires: tuple[int, ...]


@dataclass(frozen=True)
class Execution:
    qubits: int
    blank_wires: tuple[int, ...]
    old_right: tuple[int, ...]
    gates: tuple[Gate, ...]
    profile: str = G_CX
    source_port: Optional[int] = None
    source_spin: Optional[tuple[int, int]] = None
    # Readout metadata only: this adds no physical measurement operation.
    report_bits: tuple[int, ...] = ()


@dataclass(frozen=True)
class Inventory:
    qubits: int
    blank_count: int
    unknown_wires: tuple[int, ...]
    gate_count: int
    g_count: int
    cx_count: int
    source_i_count: int
    full_dimension: int
    input_dimension: int
    cut_rank: int

    @property
    def expanded_stages(self) -> int:
        """Raw gate stages only; a closing/clock operation is not inserted."""
        return self.gate_count


def _nat(value, label: str) -> int:
    if type(value) is not int or value < 0:
        raise DomainError(f"{label} must be a nonnegative integer")
    return value


def _sequence(value, label: str):
    if type(value) not in (tuple, list):
        raise DomainError(f"{label} must be a finite tuple/list")
    return value


def _wires(value, qubits: int, label: str) -> tuple[int, ...]:
    values = tuple(_sequence(value, label))
    for wire in values:
        if _nat(wire, label) >= qubits:
            raise DomainError(f"{label} contains an out-of-range wire")
    if len(set(values)) != len(values):
        raise DomainError(f"{label} repeats a wire")
    return values


def _validate_gate(execution: Execution, gate: Gate) -> None:
    if type(gate) is not Gate or type(gate.op) is not str:
        raise DomainError("every stage must be a Gate with a primitive name")
    arities = {"G": 1, "CX": 2, "SourceI": 3}
    if gate.op not in arities:
        raise DomainError(f"unknown primitive: {gate.op!r}")
    wires = _wires(gate.wires, execution.qubits, "gate wires")
    if len(wires) != arities[gate.op]:
        raise DomainError(f"wrong arity for {gate.op}")
    if set(wires).intersection(execution.old_right):
        raise DomainError("a gate touches immutable old_right")
    if gate.op == "SourceI":
        if execution.profile != G_CX_SOURCE_I:
            raise DomainError("SourceI requires the explicit source-I profile")
        if wires != (execution.source_port, *execution.source_spin):
            raise DomainError("SourceI must use the declared port/spin frame")
    elif execution.source_spin is not None:
        if set(wires).intersection(execution.source_spin):
            raise DomainError("source spin has no individual G/CX addressing")


def validate_execution(execution: Execution, *, max_qubits: int,
                       max_expanded_stages: int) -> None:
    """Decide the bounded syntactic domain; reject malformed data exactly.

    Bounds are explicit integer inputs.  No matrix approximation or tolerance
    enters membership.  Lists and tuples are both accepted; bools are not ints.
    """
    _nat(max_qubits, "max_qubits")
    _nat(max_expanded_stages, "max_expanded_stages")
    if type(execution) is not Execution:
        raise DomainError("expected an Execution")
    n = _nat(execution.qubits, "qubits")
    if n > max_qubits:
        raise DomainError("qubit bound exceeded")
    blanks = _wires(execution.blank_wires, n, "blank_wires")
    old = _wires(execution.old_right, n, "old_right")
    _wires(execution.report_bits, n, "report_bits")
    if set(blanks).intersection(old):
        raise DomainError("old_right is an unknown input, not a fresh blank")
    if type(execution.profile) is not str or execution.profile not in (
            G_CX, G_CX_SOURCE_I):
        raise DomainError("unknown apparatus profile")
    if execution.profile == G_CX:
        if execution.source_port is not None or execution.source_spin is not None:
            raise DomainError("G_CX profile has no source-I capability")
    else:
        port = _wires((execution.source_port,), n, "source_port")
        spin = _wires(execution.source_spin, n, "source_spin")
        if len(spin) != 2 or set(port).intersection(spin):
            raise DomainError("source-I requires one port and two distinct spin wires")
        if set(port + spin).intersection(old):
            raise DomainError("source-I apparatus cannot be immutable old_right")
    gates = _sequence(execution.gates, "gates")
    if len(gates) > max_expanded_stages:
        raise DomainError("expanded-stage bound exceeded")
    for gate in gates:
        _validate_gate(execution, gate)


def is_member(execution: Execution, *, max_qubits: int,
              max_expanded_stages: int) -> bool:
    try:
        validate_execution(execution, max_qubits=max_qubits,
                           max_expanded_stages=max_expanded_stages)
        return True
    except DomainError:
        return False


def _object_fields(value, required: set[str], optional: set[str], label: str):
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise DomainError(f"{label} must be a JSON object with string keys")
    keys = set(value)
    if not required.issubset(keys):
        raise DomainError(f"{label} is missing required fields")
    if not keys.issubset(required | optional):
        raise DomainError(f"{label} has unknown fields")
    return value


def _json_list(value, label: str):
    if type(value) is not list:
        raise DomainError(f"{label} must be a JSON list")
    return value


def execution_from_dict(value, *, max_qubits: int,
                        max_expanded_stages: int) -> Execution:
    """Parse the fixed finite-code schema, then validate the bounded execution.

    Required fields are schema, qubits, blank_wires, old_right, gates, profile.
    Source apparatus fields default to None and report_bits defaults to []; the
    source-I profile still requires a complete valid port/spin declaration.
    """
    obj = _object_fields(value,
                         {"schema", "qubits", "blank_wires", "old_right",
                          "gates", "profile"},
                         {"source_port", "source_spin", "report_bits"},
                         "execution")
    if type(obj["schema"]) is not str or obj["schema"] != SCHEMA:
        raise DomainError("unsupported execution schema")
    blanks = _json_list(obj["blank_wires"], "blank_wires")
    old = _json_list(obj["old_right"], "old_right")
    raw_gates = _json_list(obj["gates"], "gates")
    # Reject an oversized code before constructing its expanded gate objects.
    _nat(max_expanded_stages, "max_expanded_stages")
    if len(raw_gates) > max_expanded_stages:
        raise DomainError("expanded-stage bound exceeded")
    gates = []
    for raw_gate in raw_gates:
        gate = _object_fields(raw_gate, {"op", "wires"}, set(), "gate")
        wires = _json_list(gate["wires"], "gate wires")
        gates.append(Gate(gate["op"], tuple(wires)))
    spin = obj.get("source_spin")
    if spin is not None:
        spin = tuple(_json_list(spin, "source_spin"))
    report = _json_list(obj.get("report_bits", []), "report_bits")
    execution = Execution(obj["qubits"], tuple(blanks), tuple(old), tuple(gates),
                          obj["profile"], obj.get("source_port"), spin,
                          tuple(report))
    validate_execution(execution, max_qubits=max_qubits,
                       max_expanded_stages=max_expanded_stages)
    return execution


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DomainError("duplicate JSON object key")
        result[key] = value
    return result


def _reject_json_constant(_value):
    raise DomainError("nonfinite JSON numbers are not permitted")


def execution_from_json(code, *, max_qubits: int,
                        max_expanded_stages: int) -> Execution:
    """Membership on finite UTF-8 JSON codes; no references or evaluation.

    Multiple whitespace presentations may describe one finite object.  This
    does not assert a finite set of all such presentations or free physical
    storage of the programme bytes.  canonical_json chooses one presentation.
    """
    try:
        if type(code) is bytes:
            text = code.decode("utf-8", errors="strict")
        elif type(code) is str:
            code.encode("utf-8", errors="strict")
            text = code
        else:
            raise DomainError("execution code must be str or UTF-8 bytes")
        obj = json.loads(text, object_pairs_hook=_unique_json_object,
                         parse_constant=_reject_json_constant)
        return execution_from_dict(obj, max_qubits=max_qubits,
                                   max_expanded_stages=max_expanded_stages)
    except DomainError:
        raise
    except (UnicodeError, ValueError, TypeError, RecursionError) as error:
        raise DomainError("malformed UTF-8 execution JSON") from error


def execution_to_dict(execution: Execution) -> dict:
    """Serialize a structurally valid execution, including all optional fields."""
    if type(execution) is not Execution:
        raise DomainError("expected an Execution")
    n = _nat(execution.qubits, "qubits")
    gates = _sequence(execution.gates, "gates")
    validate_execution(execution, max_qubits=n,
                       max_expanded_stages=len(gates))
    return {"schema": SCHEMA, "qubits": n,
            "blank_wires": list(execution.blank_wires),
            "old_right": list(execution.old_right),
            "gates": [{"op": gate.op, "wires": list(gate.wires)}
                      for gate in gates],
            "profile": execution.profile,
            "source_port": execution.source_port,
            "source_spin": (None if execution.source_spin is None
                            else list(execution.source_spin)),
            "report_bits": list(execution.report_bits)}


def canonical_json(execution: Execution) -> str:
    """Deterministic compact UTF-8-compatible JSON; tuples/lists become lists."""
    return json.dumps(execution_to_dict(execution), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def inventory(execution: Execution, *, max_qubits: int,
              max_expanded_stages: int) -> Inventory:
    validate_execution(execution, max_qubits=max_qubits,
                       max_expanded_stages=max_expanded_stages)
    unknown = tuple(q for q in range(execution.qubits)
                    if q not in execution.blank_wires)
    rank = 2 ** len(unknown)
    return Inventory(execution.qubits, len(execution.blank_wires), unknown,
                     len(execution.gates),
                     sum(g.op == "G" for g in execution.gates),
                     sum(g.op == "CX" for g in execution.gates),
                     sum(g.op == "SourceI" for g in execution.gates),
                     2 ** execution.qubits, rank, rank)


def _swap(a: int, b: int) -> tuple[Gate, ...]:
    return (Gate("CX", (a, b)), Gate("CX", (b, a)), Gate("CX", (a, b)))


def inverse_word(execution: Execution, *, max_qubits: int,
                 max_expanded_stages: int) -> tuple[Gate, ...]:
    """Expand a full-column inverse using the declared source-I interface.

    The same supplied stage bound applies to both input and expanded output.
    G_CX does not receive an unproved inverse macro, even on a READY sector.
    """
    validate_execution(execution, max_qubits=max_qubits,
                       max_expanded_stages=max_expanded_stages)
    if execution.profile != G_CX_SOURCE_I:
        raise DomainError("the exact inverse compiler requires source-I")
    port = execution.source_port
    source = Gate("SourceI", (port, *execution.source_spin))
    result = []
    for gate in reversed(execution.gates):
        if gate.op == "CX":
            block = (gate,)
        elif gate.op == "SourceI":
            block = (source,) * 3
        else:
            q = gate.wires[0]
            core = (source, source, Gate("G", (port,)), source, source)
            routing = () if q == port else _swap(q, port)
            block = routing + core + routing
        if len(result) + len(block) > max_expanded_stages:
            raise DomainError("expanded inverse exceeds the stage bound")
        result.extend(block)
    return tuple(result)


def _matrix_validate(execution: Execution, max_qubits: int,
                     max_expanded_stages: int) -> None:
    validate_execution(execution, max_qubits=max_qubits,
                       max_expanded_stages=max_expanded_stages)


def gate_matrix(execution: Execution, gate: Gate, *, max_qubits: int = 6,
                max_expanded_stages: int = 10000) -> sp.ImmutableMatrix:
    """Exact full-column matrix, for bounded small fixtures only."""
    _matrix_validate(execution, max_qubits, max_expanded_stages)
    _validate_gate(execution, gate)
    wires = tuple(gate.wires)
    if gate.op == "G":
        local = G_LOCAL
    elif gate.op == "CX":
        local = sp.zeros(4)
        for control in range(2):
            for target in range(2):
                local[2 * control + (target ^ control), 2 * control + target] = 1
    else:
        local = SOURCE_I_LOCAL
    dimension = 2 ** execution.qubits
    result = sp.zeros(dimension)
    shifts = tuple(execution.qubits - 1 - q for q in wires)
    for column in range(dimension):
        local_in = 0
        for shift in shifts:
            local_in = 2 * local_in + ((column >> shift) & 1)
        for local_out in range(2 ** len(wires)):
            value = local[local_out, local_in]
            if value == 0:
                continue
            row = column
            for pos, shift in enumerate(shifts):
                bit = (local_out >> (len(wires) - 1 - pos)) & 1
                row = (row & ~(1 << shift)) | (bit << shift)
            result[row, column] = value
    return sp.ImmutableMatrix(result)


def word_matrix(execution: Execution, *, max_qubits: int = 6,
                max_expanded_stages: int = 10000) -> sp.ImmutableMatrix:
    """Chronological product computed in the exact algebraic number field."""
    _matrix_validate(execution, max_qubits, max_expanded_stages)
    dimension = 2 ** execution.qubits
    result = DomainMatrix.eye((dimension, dimension), GOLDEN_FIELD)
    cache = {}
    for gate in execution.gates:
        key = (gate.op, tuple(gate.wires))
        if key not in cache:
            matrix = gate_matrix(execution, gate, max_qubits=max_qubits,
                                 max_expanded_stages=max_expanded_stages)
            cache[key] = DomainMatrix.from_Matrix(matrix).convert_to(GOLDEN_FIELD)
        result = cache[key].matmul(result)
    return sp.ImmutableMatrix(result.to_Matrix())


def input_isometry(execution: Execution, *, max_qubits: int = 6,
                   max_expanded_stages: int = 10000) -> sp.ImmutableMatrix:
    """Insert zero blanks; retain every nonblank basis input independently."""
    _matrix_validate(execution, max_qubits, max_expanded_stages)
    unknown = tuple(q for q in range(execution.qubits)
                    if q not in execution.blank_wires)
    result = sp.zeros(2 ** execution.qubits, 2 ** len(unknown))
    for column in range(2 ** len(unknown)):
        row = 0
        for pos, wire in enumerate(unknown):
            bit = (column >> (len(unknown) - 1 - pos)) & 1
            row |= bit << (execution.qubits - 1 - wire)
        result[row, column] = 1
    return sp.ImmutableMatrix(result)


def cut_projector(execution: Execution, *, max_qubits: int = 6,
                  max_expanded_stages: int = 10000) -> sp.ImmutableMatrix:
    """The source cut P0=J J^T; rank includes all unknown/protected modes."""
    injection = input_isometry(execution, max_qubits=max_qubits,
                               max_expanded_stages=max_expanded_stages)
    return sp.ImmutableMatrix(injection * injection.T)


def exact_matrix_equal(left: sp.MatrixBase, right: sp.MatrixBase) -> bool:
    """Exact algebraic equality, used only for matrices over the owned field."""
    return left.shape == right.shape and all(
        GOLDEN_FIELD.from_sympy(value) == GOLDEN_FIELD.zero
        for value in left - right)
