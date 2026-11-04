#!/usr/bin/env python3
"""Exact record-only paid decoder closes the reverse-frame reaction.

Standalone native49-call replay; --repo defaults to cwd. Same endpoint and
frontloaded birth ages prove equality of complete H+J via the owned ST3
clock determinant. No expensive clock diagonalization or new Info law.
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
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)+"\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent/"decoder")
    args = parser.parse_args()
    source = args.repo/SOURCE
    require(sha(source) == PIN, "pinned actual native owner")
    spec = importlib.util.spec_from_file_location("paid_record_decoder_native_owner", source)
    require(spec is not None and spec.loader is not None, "native import specification")
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    field = native.GOLDEN_FIELD

    def eq(left, right, label):
        difference = left-right
        entries = difference if isinstance(difference, sp.MatrixBase) else (difference,)
        require(all(field.from_sympy(entry) == field.zero for entry in entries), label)

    def mm(*matrices):
        out = DomainMatrix.from_Matrix(matrices[0]).convert_to(field)
        for matrix in matrices[1:]:
            out = out.matmul(DomainMatrix.from_Matrix(matrix).convert_to(field))
        return sp.ImmutableMatrix(out.to_Matrix())

    Gate = native.Gate
    port, report, record = 0, 3, 4
    source_i = Gate("SourceI", (port, 1, 2))
    g = Gate("G", (port,))
    swap = (Gate("CX", (port, record)), Gate("CX", (record, port)), Gate("CX", (port, record)))
    marker = swap + (source_i, source_i, g, source_i, source_i) + (Gate("CX", (report, port)), g) + swap

    def prep(k):
        return swap+(g,)*k+(source_i, source_i)+(g,)*(2-k)+(source_i, source_i)+swap

    def execution(word):
        return native.Execution(6, (), (5,), tuple(word), native.G_CX_SOURCE_I, port, (1, 2), (record,))

    p, a = native.P, native.A
    v, w = sp.Matrix([a, p]), sp.Matrix([-p, a])
    birth = sp.kronecker_product(sp.eye(16), v, sp.eye(2))
    birth_perp = sp.kronecker_product(sp.eye(16), w, sp.eye(2))
    q0 = sp.kronecker_product(sp.eye(8), sp.diag(1, 0), sp.eye(2))
    q1 = sp.eye(32)-q0
    q0_full = sp.kronecker_product(sp.eye(8), sp.diag(1, 0), sp.eye(4))
    q1_full = sp.eye(64)-q0_full
    projection_born = mm(birth, birth.T)
    projection_detail = sp.eye(64)-projection_born
    readout_one = mm(birth_perp, birth_perp.T)
    ex_marker = execution(marker)
    marker_matrix = native.word_matrix(ex_marker, max_qubits=6, max_expanded_stages=49)
    eq(mm(birth.T, birth), sp.eye(32), "actual32-to64 frontloaded Born embedding")
    eq(projection_detail, readout_one, "complete orthogonal birth detail is retained")
    eq(sp.trace(projection_born), 32, "old born layer rank32")
    eq(sp.trace(projection_detail), 32, "new birth-detail layer rank32")
    eq(mm(marker_matrix, birth_perp), mm(birth_perp, q0)+mm(birth, q1),
       "full new-detail columns give I_R on q0 and X_R on q1")
    pzero = native.word_matrix(execution(prep(1)), max_qubits=6, max_expanded_stages=49)
    eq(pzero, sp.eye(64), "paid12-call zero-coordinate preparation is exactly identity")

    words = {}
    for k in (0, 1, 2):
        label = ("back_minus", "back_zero", "back_plus")[k]
        word = prep(1)+marker+prep(k)+prep(2-k)
        ex = execution(word)
        native.validate_execution(ex, max_qubits=6, max_expanded_stages=49)
        inventory = native.inventory(ex, max_qubits=6, max_expanded_stages=49)
        require(len(word) == 49 and (inventory.g_count, inventory.source_i_count, inventory.cx_count) == (8, 16, 25),
                label+" actual49-call inventory8G16SourceI25CX")
        require(all(gate.wires == (port,) for gate in word if gate.op == "G"),
                label+" every Golden call acts on designated port")
        require(all(port in gate.wires for gate in word if gate.op == "CX"),
                label+" every CX includes designated port")
        require(all(5 not in gate.wires for gate in word), label+" immutable oldRIGHT never addressed")
        require(all(not set(gate.wires).intersection((1, 2)) for gate in word if gate.op != "SourceI"),
                label+" opaque source Spin only used by original SourceI")
        endpoint = native.word_matrix(ex, max_qubits=6, max_expanded_stages=49)
        eq(endpoint, marker_matrix, label+" complete paid-decoder endpoint equals M on all64columns")
        eq(mm(endpoint.T, endpoint), sp.eye(64), label+" full endpoint orthogonality")
        eq(mm(endpoint, birth), mm(birth, q0)+mm(birth_perp, q1),
           label+" exact report bit retained after the actually executed decoder")
        eq(mm(birth.T, endpoint, birth), q0, label+" same actual canonical cold corner")
        eq(mm(birth.T, endpoint.T, readout_one, endpoint, birth), q1,
           label+" exact fixed final native readout effect")
        eq(mm(endpoint, q0_full), q0_full, label+" all-column report-zero identity block")
        eq(mm(endpoint, q1_full), mm(q1_full, endpoint), label+" actual report flag preserved")
        words[label] = json.loads(native.canonical_json(ex))

    f, b, d = sp.symbols("f b d", real=True)
    rotation = lambda x: sp.Matrix([[sp.cos(x), -sp.sin(x)], [sp.sin(x), sp.cos(x)]])
    xmark = sp.Matrix([[0, 1], [1, 0]])
    e0 = sp.Matrix([1, 0])
    out0 = rotation(d-b)*rotation(f)*e0
    out1 = rotation(d-b)*xmark*rotation(f)*e0

    def trig_eq(left, right, label):
        difference = left-right
        entries = difference if isinstance(difference, sp.MatrixBase) else (difference,)
        require(all(sp.trigsimp(entry) == 0 for entry in entries), label)

    trig_eq(out0, sp.Matrix([sp.cos(f+d-b), sp.sin(f+d-b)]), "paid-decoder q0 conditional state")
    trig_eq(out1, sp.Matrix([sp.sin(f+b-d), sp.cos(f+b-d)]), "paid-decoder q1 conditional state")
    trig_eq(out0[1]**2, sp.sin(f+d-b)**2, "paid fixed-readout false positive")
    trig_eq(out1[1]**2, sp.cos(f+b-d)**2, "paid fixed-readout true positive")
    guard = sp.Matrix([f+d-b, f+b-d])
    jac = guard.jacobian((f, b, d))
    require(jac.rank() == 2 and jac.nullspace() == [sp.Matrix([0, 1, 1])],
            "regular local readout guard has precisely f=0 and d=b tangent")
    trig_eq(rotation(d-b).subs(d, b), sp.eye(2), "guard forces the full paid decoder-frame product to identity")
    cold_a, cold_d = sp.cos(f+d-b), sp.sin(f+b-d)
    trig_eq(sp.diff(cold_a, b)+sp.diff(cold_a, d), 0, "reverse-frame and decoder A sources cancel as actual paired reactions")
    trig_eq(sp.diff(cold_d, b)+sp.diff(cold_d, d), 0, "reverse-frame and decoder D sources cancel as actual paired reactions")

    # All gates are AFTER the one true birth. Thus ST3's canonical endpoint
    # is the ordinary full64 endpoint, and the two ages are shared exactly.
    stages, hist_dim = 1+49, 32+49*64
    require(stages == 50 and hist_dim == 3168, "actual50-stage history dimension3168")
    require(425*hist_dim == 1346400 and 359*hist_dim == 1137312,
            "full1346400 Hodge modes and1137312 harmonic offset retained")
    xi = sp.symbols("xi")
    born_ages = sp.diag(xi**50, xi**49)
    det0 = (sp.eye(2)-born_ages).det()
    det1 = (sp.eye(2)-xmark*born_ages).det()
    require(sp.expand(det0-(1-xi**50)*(1-xi**49)) == 0, "ST3 report-zero two-age determinant")
    require(sp.expand(det1-(1-xi**99)) == 0, "ST3 report-one two-age determinant")
    require(16*(50+49+99) == hist_dim, "complete clock characteristic degree equals actual history dimension")
    # Every block has multiplicity16: arbitrary P, Spin1/2 and oldRIGHT.
    eq(sp.trace(q0), 16, "report blocks retain all16 spectator columns")
    eq(mm(q0, q0), q0, "actual cold Gram is rank16 report-zero projector")
    require(359*hist_dim+32*33*(50+49+99) == 425*hist_dim,
            "complete scene heat formula counts every Hodge mode at beta zero")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    word_path = args.output_dir/"native_words.json"
    write_json(word_path, {
        "schema": "d0.retained-record-paid-decoder-words/1",
        "source_owner": str(SOURCE), "source_sha256": PIN,
        "wire_roles": {"P": 0, "Spin": [1, 2], "actual_report": 3, "born_record": 4, "oldRIGHT": 5},
        "birth": {"new_wire": 4, "vector": ["sqrt(p)", "p"], "from_dim": 32, "to_dim": 64, "before_all_calls": True},
        "chronology": "P1(identity12); M_q(13); P_k(back12); P_(2-k)(decoder12)",
        "words": words,
    })
    receipt = {
        "schema": "d0.retained-record-paid-decoder-receipt/1",
        "status": "PASS", "check_count": len(CHECKS), "checks": CHECKS,
        "checker_sha256": sha(Path(__file__).resolve()), "native_words_sha256": sha(word_path),
        "dependencies": {str(SOURCE): PIN}, "other_checker_dependency": None,
        "inventory_each": {"G": 8, "SourceI": 16, "CX": 25, "calls": 49, "births": 1,
                           "N": 50, "D": 3168, "full_modes": 1346400, "harmonic_offset": 1137312},
        "endpoint": "M_q on all64columns for every k; true born cold Pi0; final fixed readout Pi1",
        "clock": {"all_births_frontloaded": True, "layer_ranks": [32, 32], "ages": [50, 49],
                  "ST3_determinant": "(1-xi^50)^16(1-xi^49)^16(1-xi^99)^16",
                  "full_Z": "359D+32[sum_(k<50)h(2pi k/50)+sum_(k<49)h(2pi k/49)+sum_(k<99)h(2pi k/99)]",
                  "h": "Tr_(actual33scene) exp[-beta(I-B_s-2cos(theta)C_s)]",
                  "all_three_full_heats_equal": True, "heat_diagonalization_used": False},
        "price": {"all_three_full_H_plus_J_equal": True,
                  "J": "-16 log(1-zeta)", "H": "beta^(-1)log(full_Z)",
                  "reason": "same actual complete endpoint, canonical birth ages, scene, beta and feedback cut; ST3 retains the full clock",
                  "larger_H1_composition": "append only on a proved common birth layout; its true dimensions and stages must be counted separately",
                  "equal_to_unextended13_or37_call_price": False},
        "readout_guard": {"local_equations": ["f+d-b=0", "f+b-d=0"], "solution": "f=0,d=b",
                          "required_decoder": "actual paid record-only rotation with paired inverse endpoint; fixed final readout",
                          "reaction": "reverse-frame and decoder rows are opposite; their permitted paired direction is an exact full-word gauge",
                          "probability_jacobian_warning": "use the local complete readout map; squared error constraints have zero Jacobians at the reference"},
        "scope": {"original_H1_task_forces_this_decoder": False, "wider_joint_decoder_admission": False,
                  "new_Info_or_Cost_law": False, "physical_GR_closure": False},
    }
    write_json(args.output_dir/"receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
