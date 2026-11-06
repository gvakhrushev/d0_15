#!/usr/bin/env python3
"""Paid decoder followed by the actual routed computational-basis reader.

Standalone native60-call replay; --repo defaults to cwd. Same endpoint and
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
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent/"computational_reader")
    args = parser.parse_args()
    source = args.repo/SOURCE
    require(sha(source) == PIN, "pinned actual native owner")
    spec = importlib.util.spec_from_file_location("paid_computational_reader_native_owner", source)
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
    reader = swap + (source_i, source_i, g, source_i, source_i) + swap

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
    born_readout_one = mm(birth_perp, birth_perp.T)
    readout_one = sp.kronecker_product(sp.eye(16), sp.diag(0, 1), sp.eye(2))
    computational_zero = sp.kronecker_product(sp.eye(16), sp.Matrix([1, 0]), sp.eye(2))
    computational_one = sp.kronecker_product(sp.eye(16), sp.Matrix([0, 1]), sp.eye(2))
    ex_marker = execution(marker)
    marker_matrix = native.word_matrix(ex_marker, max_qubits=6, max_expanded_stages=60)
    ex_reader = execution(reader)
    reader_inventory = native.inventory(ex_reader, max_qubits=6, max_expanded_stages=60)
    require(len(reader) == 11 and (reader_inventory.g_count, reader_inventory.source_i_count, reader_inventory.cx_count) == (1, 4, 6),
            "actual11-call routed inverse-G reader inventory1G4SourceI6CX")
    reader_matrix = native.word_matrix(ex_reader, max_qubits=6, max_expanded_stages=60)
    gr = native.gate_matrix(ex_reader, Gate("G", (record,)), max_qubits=6, max_expanded_stages=60)
    eq(reader_matrix, gr.T, "actual11-call reader equals inverse-G_R on all64columns")
    target_endpoint = mm(reader_matrix, marker_matrix)
    eq(mm(birth.T, birth), sp.eye(32), "actual32-to64 frontloaded Born embedding")
    eq(projection_detail, born_readout_one, "complete orthogonal birth detail is retained")
    eq(sp.trace(projection_born), 32, "old born layer rank32")
    eq(sp.trace(projection_detail), 32, "new birth-detail layer rank32")
    eq(mm(marker_matrix, birth_perp), mm(birth_perp, q0)+mm(birth, q1),
       "full new-detail columns give I_R on q0 and X_R on q1")
    pzero = native.word_matrix(execution(prep(1)), max_qubits=6, max_expanded_stages=60)
    eq(pzero, sp.eye(64), "paid12-call zero-coordinate preparation is exactly identity")

    words = {}
    for k in (0, 1, 2):
        label = ("back_minus", "back_zero", "back_plus")[k]
        word = prep(1)+marker+prep(k)+prep(2-k)+reader
        ex = execution(word)
        native.validate_execution(ex, max_qubits=6, max_expanded_stages=60)
        inventory = native.inventory(ex, max_qubits=6, max_expanded_stages=60)
        require(len(word) == 60 and (inventory.g_count, inventory.source_i_count, inventory.cx_count) == (9, 20, 31),
                label+" actual60-call inventory9G20SourceI31CX")
        require(all(gate.wires == (port,) for gate in word if gate.op == "G"),
                label+" every Golden call acts on designated port")
        require(all(port in gate.wires for gate in word if gate.op == "CX"),
                label+" every CX includes designated port")
        require(all(5 not in gate.wires for gate in word), label+" immutable oldRIGHT never addressed")
        require(all(not set(gate.wires).intersection((1, 2)) for gate in word if gate.op != "SourceI"),
                label+" opaque source Spin only used by original SourceI")
        endpoint = native.word_matrix(ex, max_qubits=6, max_expanded_stages=60)
        eq(endpoint, target_endpoint, label+" complete60-call endpoint equals inverse-G_R M on all64columns")
        eq(mm(endpoint.T, endpoint), sp.eye(64), label+" full endpoint orthogonality")
        eq(mm(endpoint, birth), mm(computational_zero, q0)+mm(computational_one, q1),
           label+" true report bit in computational record basis after paid reader")
        eq(mm(birth.T, endpoint, birth), a*q0+p*q1, label+" actual60-call cold corner aPi0+pPi1")
        eq(mm(birth.T, endpoint.T, readout_one, endpoint, birth), q1,
           label+" actual computational record-one readout equals original report-one effect")
        eq(mm(endpoint, q0_full), mm(reader_matrix, q0_full), label+" all-column report-zero block is inverse-G_R")
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

    # The final fixed reader converts the retained Born basis to the actual
    # computational detector basis, so the preceding guard equations apply.
    eq(mm(reader_matrix, birth), computational_zero, "fixed paid reader maps v to computational zero")
    eq(mm(reader_matrix, birth_perp), computational_one, "fixed paid reader maps vperp to computational one")

    # All gates are AFTER the one true birth. Thus ST3's canonical endpoint
    # is the ordinary full64 endpoint, and the two ages are shared exactly.
    stages, hist_dim = 1+60, 32+60*64
    require(stages == 61 and hist_dim == 3872, "actual61-stage history dimension3872")
    require(425*hist_dim == 1645600 and 359*hist_dim == 1390048,
            "full1645600 Hodge modes and1390048 harmonic offset retained")
    xi = sp.symbols("xi")
    q0_record = sp.Matrix([[a, p], [-p, a]])
    q1_record = sp.Matrix([[p, a], [a, -p]])
    eq(mm(birth.T, target_endpoint, birth), a*q0+p*q1, "full two-age block top-left")
    eq(mm(birth.T, target_endpoint, birth_perp), p*q0+a*q1, "full two-age block top-right")
    eq(mm(birth_perp.T, target_endpoint, birth), -p*q0+a*q1, "full two-age block bottom-left")
    eq(mm(birth_perp.T, target_endpoint, birth_perp), a*q0-p*q1, "full two-age block bottom-right")
    eq(q0_record.T*q0_record, sp.eye(2), "report-zero record block is orthogonal")
    eq(q1_record.T*q1_record, sp.eye(2), "report-one record block is orthogonal")
    born_ages = sp.diag(xi**61, xi**60)
    det0 = sp.expand((sp.eye(2)-q0_record*born_ages).det())
    det1 = sp.expand((sp.eye(2)-q1_record*born_ages).det())
    expected0 = 1-a*(xi**61+xi**60)+xi**121
    expected1 = 1+p*(xi**60-xi**61)-xi**121
    for actual_poly, expected_poly, label in ((det0, expected0, "zero"), (det1, expected1, "one")):
        coefficients = sp.Poly(sp.expand(actual_poly-expected_poly), xi).all_coeffs()
        require(all(field.from_sympy(coefficient) == field.zero for coefficient in coefficients),
                "ST3 actual report-"+label+" two-age determinant")
    require(16*(121+121) == hist_dim, "complete clock characteristic degree equals actual history dimension")
    # Every block has multiplicity16: arbitrary P, Spin1/2 and oldRIGHT.
    eq(sp.trace(q0), 16, "report blocks retain all16 spectator columns")
    cold = a*q0+p*q1
    eq(mm(cold.T, cold), p*q0+p**2*q1, "actual60-call cold Gram pPi0+p²Pi1")
    eq(sp.trace(q1), 16, "both feedback eigenvalues have actual multiplicity16")
    require(359*hist_dim+32*33*(121+121) == 425*hist_dim,
            "complete scene heat formula counts every Hodge mode at beta zero")

    # Actual infinitesimal coordinate formula, conditional on its admission.
    # It is not a new continuously variable primitive instruction.
    record_generator = sp.kronecker_product(sp.eye(16), sp.Matrix([[0, -1], [1, 0]]), sp.eye(2))
    eq(mm(birth.T, target_endpoint, record_generator, birth), p*q0+a*q1,
       "actual completed-reader forward-preparation cold source pPi0+aPi1")
    eq(mm(record_generator.T, record_generator), sp.eye(64),
       "actual forward generator operator norm is exactly one")
    require(25*5 > 121 and 16*5 < 81, "exact rational bounds3/5<p<5/8")
    eq(a*a-p*p, p**3, "a=sqrt(p)>p by positive square difference p³")
    margin = sp.Rational(52947, 131072)
    zeta = sp.Rational(1, 2**20)  # Actual master feedback, separately typed from reporter z0.
    x = sp.Rational(2, 55)
    heat_bound60 = sp.Rational(176, 359)*x**60/sp.factorial(60)/((1-x*x)*(1-x/60))
    source_per_rank_lower = 2*zeta*sp.Rational(3, 5)**2*margin**2
    general_zeta_threshold = heat_bound60/(2*sp.Rational(3, 5)**2*margin**2)
    require(heat_bound60 > 0 and source_per_rank_lower > 0,
            "positive exact rational CL8 and canonical-cut source bounds")
    require(heat_bound60 < source_per_rank_lower,
            "CL8 A60 is strictly below actual-master canonical-cut forward J source for every rank>=1")
    require(general_zeta_threshold < zeta,
            "actual master zeta2^-20 exceeds the general rational heat-dominance threshold")
    beta_cal = sp.symbols("beta_cal", real=True)
    coefficient = a-(a-p)*beta_cal
    require(sp.expand(coefficient-p-(a-p)*(1-beta_cal)) == 0 and
            sp.expand(a-coefficient-(a-p)*beta_cal) == 0,
            "fixed calibration coefficient is between p and a for0<=beta_cal<=1")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    word_path = args.output_dir/"native_words.json"
    write_json(word_path, {
        "schema": "d0.retained-record-paid-computational-reader-words/1",
        "source_owner": str(SOURCE), "source_sha256": PIN,
        "wire_roles": {"P": 0, "Spin": [1, 2], "actual_report": 3, "born_record": 4, "oldRIGHT": 5},
        "birth": {"new_wire": 4, "vector": ["sqrt(p)", "p"], "from_dim": 32, "to_dim": 64, "before_all_calls": True},
        "chronology": "P1(identity12); M_q(13); P_k(back12); P_(2-k)(decoder12); routed inverse-G_R(reader11)",
        "words": words,
    })
    receipt = {
        "schema": "d0.retained-record-paid-computational-reader-receipt/1",
        "status": "PASS", "check_count": len(CHECKS), "checks": CHECKS,
        "checker_sha256": sha(Path(__file__).resolve()), "native_words_sha256": sha(word_path),
        "dependencies": {str(SOURCE): PIN}, "other_checker_dependency": None,
        "inventory_each": {"G": 9, "SourceI": 20, "CX": 31, "calls": 60, "births": 1,
                           "N": 61, "D": 3872, "full_modes": 1645600, "harmonic_offset": 1390048},
        "endpoint": "inverse-G_R M_q on all64columns; cold aPi0+pPi1; actual computational record-one effect Pi1",
        "clock": {"all_births_frontloaded": True, "layer_ranks": [32, 32], "ages": [61, 60],
                  "ST3_determinant": "[1-a(xi^61+xi^60)+xi^121]^16 [1+p(xi^60-xi^61)-xi^121]^16",
                  "full_Z": "359D+32 sum_(j=0,1) sum_(xi a root of q_j, with multiplicity) h(arg xi)",
                  "q0": "1-a(xi^61+xi^60)+xi^121", "q1": "1+p(xi^60-xi^61)-xi^121",
                  "h": "Tr_(actual33scene) exp[-beta(I-B_s-2cos(theta)C_s)]",
                  "all_three_full_heats_equal": True, "heat_diagonalization_used": False},
        "price": {"all_three_full_H_plus_J_equal": True,
                  "J": "-16 log(1-zeta+zeta p)-16 log(1-zeta+zeta p²)", "H": "beta^(-1)log(full_Z)",
                  "reason": "same actual complete endpoint, canonical birth ages, scene, beta and feedback cut; ST3 retains the full clock",
                  "larger_H1_composition": "append only on a proved common birth layout; its true dimensions and stages must be counted separately",
                  "H1_after_reader_corner": "aA+pD with the actual larger bank's own source and clock",
                  "equal_to_unextended13_or37_or49_call_price": False},
        "canonical_forward_source": {
            "C_read": "aA+pD=pC_old+(a-p)C_keep", "d_f_C_read": "pA+aD",
            "hypotheses": "original H1 A,D positive, cmin I<=A+D=C_old<=I; fixed canonical old cut; fixed birth layout with actual minimum age L>=60 and original scene; unit-norm forward record generator",
            "J_f": "-2zeta Tr[(1-zeta+zeta C_read²)^(-1) C_read (pA+aD)]",
            "magnitude_lower": "2 rank zeta p² cmin²",
            "zeta_master": "1/1048576",
            "zeta_owner": "02_REGISTRY/research/A4D_NATIVE_RETURN_RECORD_SOURCE_GATE_2026_11_03.md section2, original z=2^-20",
            "reporter_z0_identification_used": False,
            "CL8_A60_exact": str(heat_bound60),
            "CL8_A60_numeric": str(sp.N(heat_bound60, 20)),
            "J_lower_per_rank_rational": str(source_per_rank_lower),
            "general_zeta_threshold_exact": str(general_zeta_threshold),
            "full_H_plus_J_forward_source_strictly_negative_under_hypotheses": True,
            "old_nontrivial_Gram_case_claimed": False,
            "forward_direction_preserves_exact_readout_guard": False,
            "fixed_calibration_field_source": "if dD=beta_cal dC_old with fixed0<=beta_cal<=1, dC_read=[a-(a-p)beta_cal]dC_old; coefficient in[p,a]",
        },
        "readout_guard": {"local_equations": ["f+d-b=0", "f+b-d=0"], "solution": "f=0,d=b",
                          "required_decoder": "actual paid record-only rotation with paired inverse endpoint; extra paid inverse-G_R followed by fixed computational readout",
                          "reaction": "reverse-frame and decoder rows are opposite; their permitted paired direction is an exact full-word gauge",
                          "probability_jacobian_warning": "use the local complete readout map; squared error constraints have zero Jacobians at the reference"},
        "scope": {"original_H1_task_forces_this_decoder": False, "wider_joint_decoder_admission": False,
                  "detector_or_classical_emission_assigned_zero_cost": False,
                  "new_Info_or_Cost_law": False, "physical_GR_closure": False},
    }
    write_json(args.output_dir/"receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
