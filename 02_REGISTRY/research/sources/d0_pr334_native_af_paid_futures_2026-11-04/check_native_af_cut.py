#!/usr/bin/env python3
"""Exact bounded application of the owned coherent-AF instrument to native words.

No physical Info selection, Einstein-source identification or full-price equality
is claimed. The 0/10 output code cost and the actual 34-stage execution differ.
Run normally and with python3 -O -Werror; all guards use require, not assert.
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


SOURCE = Path("02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py")
SOURCE_SHA256 = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
DEFAULT_REPO = Path.cwd()
CHECKS: list[str] = []


def require(condition, description: str) -> None:
    if not bool(condition):
        raise ArithmeticError(description)
    CHECKS.append(description)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    source = args.repo / SOURCE
    require(sha(source) == SOURCE_SHA256, "actual native execution owner SHA256")
    spec = importlib.util.spec_from_file_location("coherent_native_cut_owner", source)
    require(spec is not None and spec.loader is not None, "native owner import specification")
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    field = native.GOLDEN_FIELD

    def zero(expression) -> bool:
        return field.from_sympy(expression) == field.zero

    def eq(left, right, description: str) -> None:
        difference = left - right
        if isinstance(difference, sp.MatrixBase):
            require(all(zero(x) for x in difference), description)
        else:
            require(zero(difference), description)

    a, p = native.A, native.P
    v = sp.Matrix([a, p])
    v_perp = sp.Matrix([-p, a])
    eq(v.T * v, sp.ones(1), "actual Golden born vector is normalized")
    eq(v.T * v_perp, sp.zeros(1), "entire orthogonal birth detail is retained")

    # Wire order: P=0, arbitrary source Spin=(1,2), immutable oldRIGHT=3,
    # born controls o1=4 and o2=5. Every source call uses exactly that frame.
    Gate = native.Gate
    src = Gate("SourceI", (0, 1, 2))
    g = Gate("G", (0,))
    inv_g = (src, src, g, src, src)
    c1 = Gate("CX", (4, 0))
    c2 = Gate("CX", (5, 0))
    echo = (c1,) + inv_g + (c1, g)
    first = echo + echo
    mux = (g, c2) + inv_g + (c1,) + inv_g + (c2, g, c1)
    word = first + mux
    execution = native.Execution(
        qubits=6, blank_wires=(), old_right=(3,), gates=word,
        profile=native.G_CX_SOURCE_I, source_port=0, source_spin=(1, 2),
        report_bits=(4, 5),
    )
    native.validate_execution(execution, max_qubits=6, max_expanded_stages=32)
    require(len(word) == 32, "exact 32-call native syntax with protected oldRIGHT")
    require(word[-1] == c1, "last real stage is CX; no closing identity was inserted")
    inventory = native.inventory(execution, max_qubits=6, max_expanded_stages=32)
    require((inventory.g_count, inventory.source_i_count, inventory.cx_count) == (8, 16, 8),
            "actual inventory 8G + 16SourceI + 8CX")
    require(inventory.full_dimension == 64 and inventory.blank_count == 0,
            "all 64 native columns retained; no fictional computational blanks")
    require(all(3 not in gate.wires for gate in word), "no primitive touches immutable oldRIGHT")

    unitary = native.word_matrix(execution, max_qubits=6, max_expanded_stages=32)
    rotation = native.G_LOCAL ** 4
    rotation16 = sp.kronecker_product(rotation, sp.eye(8))
    q00 = sp.diag(1, 0, 0, 0)
    target = sp.kronecker_product(sp.eye(16), q00) + sp.kronecker_product(rotation16, sp.eye(4) - q00)
    eq(unitary, target, "full 64-column endpoint: control00 I, all other controls G4; Spin/RIGHT identity")
    eq(unitary.T * unitary, sp.eye(64), "full endpoint orthogonality")
    require(len(set((gate.op, gate.wires) for gate in word)) == 4,
            "only G, SourceI, and the two declared CX address tuples occur")
    for index, gate in enumerate(dict.fromkeys(word)):
        matrix = native.gate_matrix(execution, gate, max_qubits=6, max_expanded_stages=32)
        eq(matrix.T * matrix, sp.eye(64), f"actual primitive {index} full-column orthogonality")

    # The two real birth stages precede all 32 calls. Both orthogonal details
    # stay in the clock; the native fixed-carrier input metadata is not the cut.
    birth0 = sp.kronecker_product(sp.eye(16), v)
    birth1 = sp.kronecker_product(sp.eye(32), v)
    birth = birth1 * birth0
    require(birth0.shape == (32, 16) and birth1.shape == (64, 32),
            "actual births 16 -> 32 -> 64 in the requested order")
    eq(birth.T * birth, sp.eye(16), "complete initial 16-column birth embedding")
    detail1 = sp.eye(32) - birth0 * birth0.T
    detail2 = sp.eye(64) - birth1 * birth1.T
    layer0 = birth * birth.T
    layer1 = birth1 * detail1 * birth1.T
    layer2 = detail2
    eq(layer0 + layer1 + layer2, sp.eye(64), "complete chronological birth-layer partition")
    for i, layer in enumerate((layer0, layer1, layer2)):
        eq(layer * layer, layer, f"actual birth layer {i} is a projector")
        eq(sp.trace(layer), (16, 16, 32)[i], f"actual birth layer {i} full dimension")
    eq(layer0 * layer1 + layer0 * layer2 + layer1 * layer2, sp.zeros(64),
       "chronological birth details are mutually orthogonal")

    # Original Fibonacci cut: A=(00,1), B=(01). Record 1 includes the untouched
    # second born factor; its orthogonal partner remains a physical dark column.
    r00 = sp.Matrix([1, 0, 0, 0])
    r1 = sp.kronecker_product(sp.Matrix([0, 1]), v)
    r01 = sp.Matrix([0, 1, 0, 0])
    rdark = sp.kronecker_product(sp.Matrix([0, 1]), v_perp)
    frame = sp.Matrix.hstack(r00, r1, r01, rdark)
    eq(frame.T * frame, sp.eye(4), "ready/pending/dark record frame is a complete orthonormal basis")
    expected_born = (sp.kronecker_product(p * sp.eye(16), r00)
                     + sp.kronecker_product(p * rotation16, r1)
                     + sp.kronecker_product(a * p * rotation16, r01))
    eq(unitary * birth, expected_born, "exact AF N1 amplitudes pI, pG4, apG4 on the actual born input")
    eq(sp.kronecker_product(sp.eye(16), rdark.T) * unitary * birth, sp.zeros(16),
       "dark output has zero amplitude on actual input, not a deleted thermal column")
    dark_inclusion = sp.kronecker_product(sp.eye(16), rdark)
    eq(unitary * dark_inclusion, dark_inclusion * rotation16,
       "full dark complement executes G4 and remains in the complete endpoint")
    eq(p**2 + p**2 + p**3, 1, "AF ready/pending probabilities normalize")

    # Full Bloch state, including its imaginary coherence. Tensor spectators can
    # be arbitrary: all K_v^* K_u are operators on P tensor identity_8.
    x, y, z = sp.symbols("bloch_x bloch_y bloch_z", real=True)
    rho = sp.Matrix([[1 + z, x - sp.I*y], [x + sp.I*y, 1 - z]]) / 2
    k00, k1, k01 = p * sp.eye(2), p * rotation, a * p * rotation
    gram_a = sp.Matrix([[sp.trace(ku * rho * kv.T) for kv in (k00, k1)]
                        for ku in (k00, k1)])
    gram_b = sp.trace(k01 * rho * k01.T)
    cosine = sp.simplify(rotation[0, 0])
    sine = sp.simplify(rotation[1, 0])
    expected_gram = p**2 * sp.Matrix([[1, cosine + sp.I*sine*y],
                                     [cosine - sp.I*sine*y, 1]])
    require(all(sp.simplify(entry) == 0 for entry in gram_a - expected_gram),
            "entire Bloch Gram formula including imaginary +/- i sin(theta) bloch_y")
    require(sp.simplify(gram_b - p**3) == 0, "full pending Bloch trace equals p3")
    require(all(sp.simplify(sp.diff(entry, coordinate)) == 0
                for coordinate in (x, z) for entry in gram_a),
            "Bloch x/z terms cancel by actual rotation; y coherence remains")
    require(sp.simplify(sp.diff(gram_a[0, 1], y)) != 0, "imaginary Bloch coherence is genuinely retained")
    eq(cosine, 17 - 8*sp.sqrt(5), "exact native angle cosine at G4")
    eq(cosine**2 + sine**2, 1, "native angle sine/cosine identity")
    eq((v.T * rotation * v)[0], cosine, "real born target supplies the y=0 coherent example without mixed-state preparation")

    # Cold return uses the physical born cut, not the three readout projectors.
    cold = birth.T * unitary * birth
    cold2 = p**2 * sp.eye(2) + p * rotation
    eq(cold, sp.kronecker_product(cold2, sp.eye(8)), "actual cold C=(p2 I+p G4) tensor I8")
    h = sp.simplify(p**4 + p**2 + 2*p**3*cosine)
    eq(cold.T * cold, h * sp.eye(16), "full physical C* C is h I16")
    eq(h, 64*sp.sqrt(5) - 143, "exact radical form of the cold scalar h")
    require(143**2 < 64**2 * 5 < 144**2,
            "rational-square certificate proves 0<h=64sqrt5-143<1")
    eq(sp.trace(cold.T * cold), 16*h, "true input rank and determinant multiplicity are 16")
    # This is the original rank-one scene cut. No scene multiplicity is added
    # to J; all 425D scene/Hodge modes are nevertheless retained in H.
    stage_dimensions = [16, 32] + [64] * 32
    stage_count = len(stage_dimensions)
    hist_dimension = sum(stage_dimensions)
    require(stage_count == 34 and hist_dimension == 2096,
            "actual 34-stage growing history dimension is 2096")
    modes = 425 * hist_dimension
    harmonic_offset = 359 * hist_dimension
    require(modes == 890800 and harmonic_offset == 752464,
            "full Hodge carrier 890800; harmonic dimension offset 752464")
    # For eigenvalue 1, all birth details add to I before the first square call,
    # so fixed clock vectors correspond to fixed endpoint vectors. Only control
    # 00 is fixed: det(G4-I)!=0. Thus ker Delta0 has dimension 16 on this scene.
    eq(sp.det(rotation - sp.eye(2)), 2 - 2*cosine, "nonidentity G4 block has no fixed vector")
    require(not zero(2 - 2*cosine), "exact field certificate: no G4 eigenvalue equals one")
    eq(birth0 * birth.T + detail1 * birth1.T, birth1.T,
       "clock eigenvalue-one birth recurrence reconstructs the penultimate birth fibre")
    eq(birth1 * birth1.T + detail2, sp.eye(64),
       "clock eigenvalue-one birth recurrence reconstructs the full endpoint input")
    fixed_clock_dimension = 16
    full_harmonic_modes = harmonic_offset + 2 * fixed_clock_dimension
    require(full_harmonic_modes == 752496,
            "total Hodge harmonic modes include 2*ker Delta0: 752496, not merely 752464")
    code_cost = sp.simplify(2*(2*p**2) + 3*p**3)
    eq(code_cost, 2 + p**3, "owned 0/10 AF output code cost is 2+p3")
    require(1**2 < 5 < 3**2 and 3 < stage_count,
            "0<p<1 gives output code cost 2+p3<3<34 actual stages")

    native_json = json.loads(native.canonical_json(execution))
    history = {
        "schema": "d0.coherent-native-af-cut/1",
        "source_owner": str(SOURCE), "source_sha256": SOURCE_SHA256,
        "wire_roles": {"P": 0, "Spin": [1, 2], "immutable_oldRIGHT": 3,
                       "born_o1": 4, "born_o2": 5},
        "births_before_word": [
            {"stage": 0, "new_wire": 4, "vector": ["sqrt(p)", "p"], "from_dim": 16, "to_dim": 32},
            {"stage": 1, "new_wire": 5, "vector": ["sqrt(p)", "p"], "from_dim": 32, "to_dim": 64},
        ],
        "native_word": native_json,
        "clock_stage_dimensions": stage_dimensions,
        "input_cut_rank": 16,
        "record_frame": {"ready00": "|00>", "ready1": "|1> tensor (a|0>+p|1>)",
                         "pending01": "|01>", "dark": "|1> tensor (-p|0>+a|1>)"},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    word_path = args.output_dir / "native_word.json"
    dump(word_path, history)
    receipt = {
        "schema": "d0.coherent-native-af-cut-receipt/1",
        "checker_sha256": sha(Path(__file__).resolve()),
        "source_sha256": SOURCE_SHA256,
        "native_word_sha256": sha(word_path),
        "checks": CHECKS, "check_count": len(CHECKS), "status": "PASS",
        "inventory": {"G": 8, "SourceI": 16, "CX": 8, "primitive_calls": 32,
                      "birth_stages": 2, "total_stages": stage_count,
                      "endpoint_dimension": 64, "physical_initial_cut_rank": 16},
        "angle": {"cosine": str(cosine), "sine": str(sine)},
        "cold": {"C": "(p^2 I2+p G^4) tensor I8", "h": str(h),
                 "h_numeric": str(sp.N(h, 30)),
                 "J": "-16 log(1-z+z h)"},
        "clock": {"D": hist_dimension, "full_modes": modes,
                  "harmonic_offset": harmonic_offset, "ker_Delta0": fixed_clock_dimension,
                  "total_harmonic_modes": full_harmonic_modes,
                  "Z01": "359D+2 Tr_(33D) exp(-beta Delta0(T))"},
        "record_gram": {"A": "p^2 [[1,c+i s bloch_y],[c-i s bloch_y,1]]", "B": "p^3"},
        "output_code_cost": "2+p^3",
        "scope": {"physical_Info_selected": False, "output_code_cost_equals_raw_cost": False,
                  "full_price_equals_AF_relative_entropy": False,
                  "smooth_theta_is_native_control": False, "GR_closed": False},
    }
    dump(args.output_dir / "receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
