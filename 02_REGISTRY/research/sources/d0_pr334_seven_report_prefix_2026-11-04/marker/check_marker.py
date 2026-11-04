#!/usr/bin/env python3
"""Exact port-routed marker, Born cut and positive seven-report prefix margin.

Only the small marker is executed on all 64 native columns. The H.1 application
consumes its existing selector/report identities; no giant H.1 bank, full heat,
or physical task selection is claimed. Guards survive python -O.
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


def require(condition, name: str) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    source = args.repo / SOURCE
    require(sha(source) == PIN, "pinned actual native execution owner")
    spec = importlib.util.spec_from_file_location("native_routed_marker_owner", source)
    require(spec is not None and spec.loader is not None, "native owner import specification")
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    field = native.GOLDEN_FIELD

    def eq(left, right, name: str) -> None:
        difference = left - right
        entries = difference if isinstance(difference, sp.MatrixBase) else (difference,)
        require(all(field.from_sympy(entry) == field.zero for entry in entries), name)

    def mm(*matrices):
        out = DomainMatrix.from_Matrix(matrices[0]).convert_to(field)
        for matrix in matrices[1:]:
            out = out.matmul(DomainMatrix.from_Matrix(matrix).convert_to(field))
        return sp.ImmutableMatrix(out.to_Matrix())

    # P0, opaque Spin1/2, actual report bit q3, fresh record R4, oldRIGHT5.
    Gate = native.Gate
    port, report, record = 0, 3, 4
    source_i = Gate("SourceI", (port, 1, 2))
    g = Gate("G", (port,))
    inverse_g = (source_i, source_i, g, source_i, source_i)
    swap = (Gate("CX", (port, record)), Gate("CX", (record, port)), Gate("CX", (port, record)))
    # Central CX changes target when the two inner SWAPs are fused.
    fused = swap + inverse_g + (Gate("CX", (report, port)), g) + swap
    unfused = swap + inverse_g + swap + (Gate("CX", (report, record)),) + swap + (g,) + swap

    def execution(word):
        return native.Execution(6, (), (5,), word, native.G_CX_SOURCE_I, port, (1, 2), (record,))

    ex = execution(fused)
    native.validate_execution(ex, max_qubits=6, max_expanded_stages=19)
    require(len(fused) == 13 and len(unfused) == 19,
            "fully routed fused13 and unfused19 call counts")
    inv = native.inventory(ex, max_qubits=6, max_expanded_stages=19)
    require((inv.g_count, inv.source_i_count, inv.cx_count) == (2, 4, 7),
            "fused actual inventory2G4SourceI7CX")
    require(all(gate.wires == (port,) for gate in fused if gate.op == "G"),
            "every executed Golden G acts on the designated physical port")
    require(all(5 not in gate.wires for gate in fused), "immutable oldRIGHT never addressed")
    require(all(not set(gate.wires).intersection((1, 2)) for gate in fused if gate.op != "SourceI"),
            "source Spin never individually addressed")
    require(all(port in gate.wires for gate in fused if gate.op == "CX"),
            "all seven executed CX operations include the designated port")
    require(fused[8] == Gate("CX", (report, port)),
            "the fused central CX is incoming report-to-port, not report-to-record")
    actual = native.word_matrix(ex, max_qubits=6, max_expanded_stages=19)
    ordinary = native.word_matrix(execution(unfused), max_qubits=6, max_expanded_stages=19)
    eq(actual, ordinary, "fused and unfused marker endpoints agree on all64columns")
    # These matrices describe the target identity, not uncharged executed G_R.
    gr = native.gate_matrix(ex, Gate("G", (record,)), max_qubits=6, max_expanded_stages=19)
    copy = native.gate_matrix(ex, Gate("CX", (report, record)), max_qubits=6, max_expanded_stages=19)
    eq(actual, mm(gr, copy, gr.T), "all64columns implement G_R CX(q,R) G_R inverse")
    eq(mm(actual.T, actual), sp.eye(64), "complete marker is orthogonal on every input column")
    eq(actual, actual.T, "complete marker is a reflection")

    p, a = native.P, native.A
    v = sp.Matrix([a, p])
    vperp = sp.Matrix([-p, a])
    # The record is inserted before immutable oldRIGHT; no unknown state reset.
    birth = sp.kronecker_product(sp.eye(16), v, sp.eye(2))
    birth_perp = sp.kronecker_product(sp.eye(16), vperp, sp.eye(2))
    q0 = sp.kronecker_product(sp.eye(8), sp.diag(1, 0), sp.eye(2))
    q1 = sp.eye(32) - q0
    eq(mm(birth.T, birth), sp.eye(32), "actual32-to64 Born embedding is isometric")
    eq(mm(birth.T, birth_perp), sp.zeros(32), "full orthogonal birth detail retained")
    eq(mm(actual, birth), mm(birth, q0) + mm(birth_perp, q1),
       "actual report0 writes v and report1 writes vperp for all32inputcolumns")
    eq(mm(birth.T, actual, birth), q0,
       "true Born cold compression of marker is the report-zero projector")
    record_one = mm(birth_perp, birth_perp.T)
    eq(mm(birth.T, actual.T, record_one, actual, birth), q1,
       "Born-frame terminal record reads the actual report-one effect")
    eq(sp.trace(q0), 16, "no restriction of the original source Spin/oldRIGHT input columns")

    # Owned comparator: eight weight-two words, five genuine v births.
    words = ("00011", "00101", "00110", "01001", "01010", "01100", "10001", "10010")
    require(len(set(words)) == 8 and all(len(word) == 5 and word.count("1") == 2 for word in words),
            "owned eight disjoint selector words all have five bits and weight two")
    for word in words:
        eq(p**(5-word.count("1")) * p**(2*word.count("1")), p**7,
           "actual Born selector weight p7 for " + word)
    # Each event is a projector: product of two composite READY-and-REPORT
    # bits or its complement. There are eight, so 0 <= n_omega <= 8 exactly.
    yp, ym, f, baseline, xp, xm, material = symbols = sp.symbols("yp ym f baseline xp xm material")
    events = (yp*f, ym*baseline, 1-yp*baseline, 1-ym*f,
              xp*material, xm*baseline, 1-xp*baseline, 1-xm*material)

    def boolean_reduce(poly):
        result = 0
        for exponents, coefficient in sp.Poly(sp.expand(poly), *symbols).terms():
            monomial = coefficient
            for symbol, exponent in zip(symbols, exponents):
                if exponent:
                    monomial *= symbol
            result += monomial
        return sp.expand(result)

    require(all(boolean_reduce(event**2-event) == 0 for event in events),
            "all eight owned branch events are Boolean projections; their sum lies between0and8")
    require(sp.expand(sum(events) - (4+(yp-ym)*(f-baseline)+(xp-xm)*(material-baseline))) == 0,
            "actual eight-event sum equals the original cross-reference polynomial")
    require(25*5 > 121 and 16*5 < 81, "exact square certificates for3/5<p<5/8")
    margin = 1 - 16*sp.Rational(5, 8)**7
    require(margin == sp.Rational(52947, 131072) and margin > 0,
            "c_omega=1-2kappa9 p7 n_omega exceeds52947/131072 using0<=kappa9<=1")

    # Pick the actual REPORT BIT of the fixed BASELINE (x,y)=(0,0) call.
    # This avoids silently assuming a lower bound for every geometric operand.
    z0 = sp.Rational(1, 2**20)
    b0 = 4*p**3
    a0 = 2*b0-b0**2
    r0 = z0*(a0+b0)-z0**2*a0*b0
    eq(b0, 8*p-4, "baseline b0=4p3=8p-4, hence4/5<b0<1")
    eq(a0-b0, b0*(1-b0), "baseline A0>=b0 on the proved interval")
    eq(1-a0, (1-b0)**2, "baseline0<A0<1 and0<A0b0<1")
    eq(r0/z0, a0+b0-z0*a0*b0, "unchanged original baseline reporter polynomial")
    require(z0 < sp.Rational(1, 2) and sp.Rational(8, 5)-sp.Rational(1, 2) == sp.Rational(11, 10),
            "strict rational proof r0/z0>11/10>1")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    word_path = args.output_dir / "native_word.json"
    write_json(word_path, {
        "schema": "d0.native-born-report-marker/1",
        "source_owner": str(SOURCE), "source_sha256": PIN,
        "wire_roles": {"P": 0, "Spin": [1, 2], "actual_report_bit": 3, "born_record": 4, "immutable_oldRIGHT": 5},
        "birth": {"new_wire": 4, "vector": ["sqrt(p)", "p"], "from_dim": 32, "to_dim": 64},
        "native_word": json.loads(native.canonical_json(ex)),
        "chronology": "SWAP(P,R); InvG_P; CX(q,P); G_P; SWAP(P,R)",
    })
    receipt = {
        "schema": "d0.native-born-report-marker-receipt/1",
        "status": "PASS", "check_count": len(CHECKS), "checks": CHECKS,
        "checker_sha256": sha(Path(__file__).resolve()), "source_sha256": PIN,
        "native_word_sha256": sha(word_path),
        "inventory": {"G_on_port": 2, "SourceI": 4, "CX_including_port": 7, "calls": 13,
                      "unfused_calls": 19, "births": 1, "full_columns": 64, "initial_columns": 32},
        "born_cut": "j_R* C_q j_R=Pi_(q=0)",
        "selector_margin": {"n_omega_bounds": [0, 8], "cmin": "1-16 kappa9 p^7",
                            "rational_strict_lower_bound": "52947/131072"},
        "baseline_report": {"bit_is_composite_READY_REPORT": False,
                            "actual_bit": "REPORT bit of baseline (0,0) call",
                            "r0_over_z0_strict_lower_bound": "11/10",
                            "effect_implication": "E_REPORT>=E_READY_AND_REPORT=alpha_h r0 I>alpha_h z0 I"},
        "H1_application": {
            "consumed": ["7ec(1146)", "7ef SC6-SC7", "7eh.H.2 T3", "SOURCE_PROOF_RU(1)"],
            "identity": "C_old-C_keep=sum_(omega:q=1) c_omega E_omega",
            "strict_bound": "C_old-C_keep>=cmin E_REPORT>cmin alpha_h z0 I",
            "exact_hypotheses": "fixed actual comparator; independent born selector/port factors; original baseline report law",
            "approximation_boundary": "full marked-prefix isometry error eta adds at most2eta to the corner-difference norm",
        },
        "scope": {"giant_H1_word_executed": False, "full_heat_claimed": False,
                  "equal_price_unfused_and_fused_claimed": False,
                  "physical_task_admission_forced": False, "GR_closed": False},
    }
    write_json(args.output_dir / "receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
