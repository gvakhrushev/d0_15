#!/usr/bin/env python3
"""Literal equal-inventory record preparations and their fixed-readout guard.

Runs the actual native owner on all 64 columns. No complete H.1 word, heat
value, physical admission, continuous native angle or GR closure is claimed.
Use --repo for a checkout other than the current working directory.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as sp
from sympy.polys.matrices import DomainMatrix

SOURCE = Path("02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py")
PIN = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
CHECKS: list[str] = []


def require(value, label: str) -> None:
    if not bool(value):
        raise ArithmeticError(label)
    CHECKS.append(label)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    path = args.repo / SOURCE
    require(sha(path) == PIN, "actual native owner SHA256 pin")
    spec = importlib.util.spec_from_file_location("record_preparation_native_owner", path)
    require(spec is not None and spec.loader is not None, "native import specification")
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    field = native.GOLDEN_FIELD

    def eq(left, right, label: str) -> None:
        difference = left - right
        entries = difference if isinstance(difference, sp.MatrixBase) else (difference,)
        require(all(field.from_sympy(entry) == field.zero for entry in entries), label)

    def mm(*matrices):
        result = DomainMatrix.from_Matrix(matrices[0]).convert_to(field)
        for matrix in matrices[1:]:
            result = result.matmul(DomainMatrix.from_Matrix(matrix).convert_to(field))
        return sp.ImmutableMatrix(result.to_Matrix())

    Gate = native.Gate
    port, report, record = 0, 3, 4
    source_i = Gate("SourceI", (port, 1, 2))
    g = Gate("G", (port,))
    swap = (Gate("CX", (port, record)), Gate("CX", (record, port)), Gate("CX", (port, record)))
    inverse_g = (source_i, source_i, g, source_i, source_i)
    marker = swap + inverse_g + (Gate("CX", (report, port)), g) + swap

    def execution(word):
        return native.Execution(6, (), (5,), tuple(word), native.G_CX_SOURCE_I,
                                port, (1, 2), (record,))

    def prep(k: int):
        return swap + (g,)*k + (source_i, source_i) + (g,)*(2-k) + (source_i, source_i) + swap

    p, a = native.P, native.A
    v, w = sp.Matrix([a, p]), sp.Matrix([-p, a])
    birth = sp.kronecker_product(sp.eye(16), v, sp.eye(2))
    birth_perp = sp.kronecker_product(sp.eye(16), w, sp.eye(2))
    q0 = sp.kronecker_product(sp.eye(8), sp.diag(1, 0), sp.eye(2))
    q1 = sp.eye(32)-q0
    q0_full = sp.kronecker_product(sp.eye(8), sp.diag(1, 0), sp.eye(4))
    q1_full = sp.eye(64)-q0_full
    record_readout = mm(birth_perp, birth_perp.T)
    eq(mm(birth.T, birth), sp.eye(32), "same actual32-to64 Born embedding")
    eq(mm(birth.T, birth_perp), sp.zeros(32), "retained orthogonal birth detail")

    base_execution = execution(marker)
    marker_matrix = native.word_matrix(base_execution, max_qubits=6, max_expanded_stages=37)
    gr = native.gate_matrix(base_execution, Gate("G", (record,)), max_qubits=6, max_expanded_stages=37)
    sin4 = 4*a*p**4
    cos4 = 1-8*p**3
    eq(sin4**2+cos4**2, 1, "exact Golden sin4theta and cos4theta")
    require(25*5 > 121 and 16*5 < 81, "rational square bounds3/5<p<5/8")
    eq(cos4, 9-16*p, "actual cos4theta is negative on the proved p interval")
    require(sp.Rational(9)-16*sp.Rational(3, 5) < 0, "cos4theta<0")
    # sin4=4*sqrt(p)*p^4>0 and cos4 != 0, so 0<sin4<1.
    require(sp.Rational(3, 5) > 0, "positive p proves positive sin4theta")

    words = {}
    for k in (0, 1, 2):
        label = ("minus", "zero", "plus")[k]
        pword = prep(k)
        pex = execution(pword)
        native.validate_execution(pex, max_qubits=6, max_expanded_stages=37)
        pinv = native.inventory(pex, max_qubits=6, max_expanded_stages=37)
        require(len(pword) == 12 and (pinv.g_count, pinv.source_i_count, pinv.cx_count) == (2, 4, 6),
                label + " actual12-call routed preparation inventory")
        pmat = native.word_matrix(pex, max_qubits=6, max_expanded_stages=37)
        target = (mm(gr.T, gr.T), sp.eye(64), mm(gr, gr))[k]
        eq(pmat, target, label + " preparation equals G_R^(2k-2) on all64columns")

        word = pword + marker + prep(2-k)
        ex = execution(word)
        native.validate_execution(ex, max_qubits=6, max_expanded_stages=37)
        inventory = native.inventory(ex, max_qubits=6, max_expanded_stages=37)
        require(len(word) == 37 and (inventory.g_count, inventory.source_i_count, inventory.cx_count) == (6, 12, 19),
                label + " common37-call inventory6G12SourceI19CX")
        require(all(gate.wires == (port,) for gate in word if gate.op == "G"),
                label + " every Golden call acts on designated port")
        require(all(port in gate.wires for gate in word if gate.op == "CX"),
                label + " every CX includes designated port")
        require(all(5 not in gate.wires for gate in word), label + " immutable oldRIGHT never addressed")
        require(all(not set(gate.wires).intersection((1, 2)) for gate in word if gate.op != "SourceI"),
                label + " source Spin never independently addressed")
        actual = native.word_matrix(ex, max_qubits=6, max_expanded_stages=37)
        eq(actual, mm(target.T, marker_matrix, target),
           label + " complete37-call endpoint on all64columns")
        eq(mm(actual.T, actual), sp.eye(64), label + " full endpoint orthogonality")
        eq(actual, actual.T, label + " full endpoint remains a reflection")
        eq(mm(actual, q0_full), q0_full, label + " report-zero full-column block is identity")
        eq(mm(actual, q1_full), mm(q1_full, actual), label + " actual report flag projector preserved")
        sine = (-sin4, sp.Integer(0), sin4)[k]
        cosine = sp.Integer(1) if k == 1 else cos4
        eq(mm(actual, birth), mm(birth, q0+sine*q1)+cosine*mm(birth_perp, q1),
           label + " exact conditional record states for all32 Born columns")
        eq(mm(birth.T, actual, birth), q0+sine*q1, label + " actual canonical cold corner")
        eq(mm(birth.T, actual.T, record_readout, actual, birth), cosine**2*q1,
           label + " actual fixed Born readout effect including false negatives")
        words[label] = json.loads(native.canonical_json(ex))

    # This is a coordinate identity for genuinely admitted real preparations,
    # not a claim that a continuously variable rotation is a native instruction.
    f, b = sp.symbols("f b", real=True)
    rotation = lambda x: sp.Matrix([[sp.cos(x), -sp.sin(x)], [sp.sin(x), sp.cos(x)]])
    xmark = sp.Matrix([[0, 1], [1, 0]])
    e0 = sp.Matrix([1, 0])
    out0 = rotation(-b)*rotation(f)*e0
    out1 = rotation(-b)*xmark*rotation(f)*e0

    def trig_eq(left, right, label):
        difference = left-right
        entries = difference if isinstance(difference, sp.MatrixBase) else (difference,)
        require(all(sp.trigsimp(entry) == 0 for entry in entries), label)

    trig_eq(out0, sp.Matrix([sp.cos(f-b), sp.sin(f-b)]), "independent q0 state R(f-b)v")
    trig_eq(out1, sp.Matrix([sp.sin(f+b), sp.cos(f+b)]), "independent q1 state R(-b)X R(f)v")
    trig_eq(out0[1]**2, sp.sin(f-b)**2, "fixed readout false positive sin²(f-b)")
    trig_eq(out1[1]**2, sp.cos(f+b)**2, "fixed readout true positive cos²(f+b)")
    trig_eq((out0.T*out1)[0], sp.sin(2*f), "conditional record overlap independent of reverse frame b")
    fp, fn = sp.sin(f-b)**2, sp.sin(f+b)**2
    require(all(sp.diff(error, coordinate).subs({f: 0, b: 0}) == 0
                for error in (fp, fn) for coordinate in (f, b)),
            "both probability-constraint Jacobians vanish at reference")
    require(sp.hessian(fp+fn, (f, b)).subs({f: 0, b: 0}) == 4*sp.eye(2),
            "sum of readout-error Hessians is positive definite4I")
    require(sp.Matrix([[1, -1], [1, 1]]).det() == 2,
            "local exact guard f-b=f+b=0 forces f=b=0")
    trig_eq(out0[0].subs(b, 0), sp.cos(f), "canonical fixed-reference cold coefficient of A")
    trig_eq(out1[0].subs(b, 0), sp.sin(f), "canonical fixed-reference cold coefficient of D")
    trig_eq(out0[0].subs(b, f), 1, "generated input-reference cold coefficient of A")
    trig_eq(out1[0].subs(b, f), sp.sin(2*f), "generated input-reference cold coefficient of D")

    # If both readout errors <=e and |f±b|<pi/2, write
    # t=sqrt(1-e) in [0,1]. Then 1-cos(f-b)<=1-t,
    # |sin(f+b)|<=sqrt(e), and apply the operator norm triangle law.
    t = sp.symbols("t", nonnegative=True)
    require(sp.expand(1-(1-t**2)-t**2) == 0,
            "approximate guard algebra e=1-t² with t=sqrt(1-e)")
    require(sp.expand((1-t)*(1+t)-(1-t**2)) == 0,
            "approximate A coefficient1-sqrt(1-e)=e/(1+sqrt(1-e))")
    # Moving readout basis can absorb reverse rotation b when f=0.
    projector_one = sp.diag(0, 1)
    moved = rotation(-b)*projector_one*rotation(b)
    trig_eq((out0.T*moved*out0)[0].subs(f, 0), 0,
            "moving Born readout absorbs arbitrary b for report zero at f=0")
    trig_eq((out1.T*moved*out1)[0].subs(f, 0), 1,
            "moving Born readout absorbs arbitrary b for report one at f=0")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    word_path = args.output_dir/"native_words.json"
    write_json(word_path, {
        "schema": "d0.retained-record-native-preparations/1",
        "source_owner": str(SOURCE), "source_sha256": PIN,
        "wire_roles": {"P": 0, "Spin": [1, 2], "actual_report": 3, "born_record": 4, "oldRIGHT": 5},
        "birth": {"new_wire": 4, "vector": ["sqrt(p)", "p"], "from_dim": 32, "to_dim": 64},
        "preparation": "SWAP(P,R); G^k; SourceI²; G^(2-k); SourceI²; SWAP(P,R)",
        "chronology": "P_k; fixed fused13-call M_q; P_(2-k)",
        "words": words,
    })
    receipt = {
        "schema": "d0.retained-record-native-preparations-receipt/1",
        "status": "PASS", "check_count": len(CHECKS), "checks": CHECKS,
        "checker_sha256": sha(Path(__file__).resolve()),
        "source_owner": str(SOURCE), "source_sha256": PIN,
        "native_words_sha256": sha(word_path),
        "inventory_each": {"G": 6, "SourceI": 12, "CX": 19, "calls": 37,
                           "births": 1, "stages": 38, "full_columns": 64, "initial_columns": 32},
        "cold": {"minus": "Pi0-sin(4theta)Pi1", "zero": "Pi0", "plus": "Pi0+sin(4theta)Pi1",
                 "sin4theta": "4sqrt(p)p^4", "cos4theta": "1-8p^3=9-16p",
                 "sin4theta_numeric": str(sp.N(sin4, 30))},
        "independent_preparations": {
            "C": "cos(f-b)A+sin(f+b)D", "one_leg_reference_derivative": "D",
            "paired_reference_derivative": "2D", "fixed_reference": "cos(f)A+sin(f)D",
            "input_generated_reference": "A+sin(2f)D",
        },
        "fixed_readout_guard": {
            "false_positive": "sin²(f-b)", "true_positive": "cos²(f+b)",
            "local_domain": "|f-b|<pi/2 and |f+b|<pi/2",
            "exact_feasible_set_locally": "f=b=0",
            "probability_constraint_jacobians_at_zero": "both zero; tangent kernel is not the feasible tangent",
            "sum_error_hessian_at_zero": "4I2",
            "approximation": "both errors<=e,0<=e<1 imply ||C-A||<=(1-sqrt(1-e))||A||+sqrt(e)||D||",
            "moving_basis_pitfall": "if the paid readout basis may co-rotate, f=0 and arbitrary b preserve perfect reading; conditional overlap sin(2f) still prevents perfect separation for generic f",
        },
        "scope": {"full_H1_word_executed": False, "full_heat_computed": False,
                  "zero_heat_claimed": False, "full_price_contrast_claimed": False,
                  "physical_task_admission_proved": False, "continuous_native_angle_claimed": False,
                  "GR_closed": False},
    }
    write_json(args.output_dir/"receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
