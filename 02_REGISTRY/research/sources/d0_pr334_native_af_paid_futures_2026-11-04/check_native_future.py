#!/usr/bin/env python3
"""Actual future undo/born-reader tests the owned AF cut's algebra boundary.

Conditional on admission of these words and continuation on mutable controls,
two same-inventory native histories have identical AF states and different future
readout probabilities. A separate pinching comparison remains mathematical only.
No unrestricted H.1-task admission or physical Info law is thereby selected.
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
SOURCE_SHA = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
CHECKS: list[str] = []


def require(condition, description: str) -> None:
    if not bool(condition):
        raise ArithmeticError(description)
    CHECKS.append(description)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    source = args.repo / SOURCE
    require(sha(source) == SOURCE_SHA, "pinned actual native execution owner")
    spec = importlib.util.spec_from_file_location("native_future_reader_owner", source)
    require(spec is not None and spec.loader is not None, "native owner import specification")
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    field = native.GOLDEN_FIELD

    def mm(*matrices):
        result = DomainMatrix.from_Matrix(matrices[0]).convert_to(field)
        for factor in matrices[1:]:
            result = result.matmul(DomainMatrix.from_Matrix(factor).convert_to(field))
        return sp.ImmutableMatrix(result.to_Matrix())

    def zero(value) -> bool:
        return field.from_sympy(value) == field.zero

    def eq(left, right, description: str) -> None:
        difference = left - right
        if isinstance(difference, sp.MatrixBase):
            require(all(zero(x) for x in difference), description)
        else:
            require(zero(difference), description)

    p, a, Gate = native.P, native.A, native.Gate
    v = sp.Matrix([a, p])
    v_perp = sp.Matrix([-p, a])
    source_i = Gate("SourceI", (0, 1, 2))
    g = Gate("G", (0,))
    inverse_g = (source_i, source_i, g, source_i, source_i)
    cx1 = Gate("CX", (4, 0))
    cx2 = Gate("CX", (5, 0))

    def macro_pattern(positive: tuple, negative: tuple) -> tuple:
        echo = (cx1,) + negative + (cx1,) + positive
        mux = positive + (cx2,) + negative + (cx1,) + negative + (cx2,) + positive + (cx1,)
        return echo + echo + mux

    original = macro_pattern((g,), inverse_g)
    cheap_inverse = macro_pattern(inverse_g, (g,))

    def swap(first: int, second: int) -> tuple:
        return (Gate("CX", (first, second)), Gate("CX", (second, first)), Gate("CX", (first, second)))

    def read_born(control: int) -> tuple:
        routing = swap(0, control)
        return routing + inverse_g + routing

    reader4, reader5 = read_born(4), read_born(5)
    future = cheap_inverse + reader4 + reader5
    complete = original + future

    def gamma(control: int, power: int) -> tuple:
        routing = swap(0, control)
        return routing + (source_i,) * power + routing

    cx45 = Gate("CX", (4, 5))
    # L_I has order four. a+b-(a XOR b)=2ab implements CZ, with Spin restored.
    phase33 = (gamma(4, 1) + gamma(5, 1) + (cx45,)
               + gamma(5, 3) + (cx45,) + gamma(5, 2))
    phase35 = phase33 + (cx1, cx1)

    # Same-inventory identity: sum of the seven nonzero GF2 linear forms is
    # zero at 000 and four elsewhere, so their common L_I power is identity.
    routes = (
        (), swap(0, 4), swap(0, 5), (cx1,), (cx2,),
        swap(0, 4) + (cx2,), (cx1, cx2),
    )
    identity_blocks = tuple(route + (source_i,) + tuple(reversed(route)) for route in routes)
    identity35 = tuple(gate for block in identity_blocks for gate in block)
    paired0 = original + identity35
    paired1 = original + phase35

    def execution(word: tuple):
        return native.Execution(6, (), (3,), word, native.G_CX_SOURCE_I, 0, (1, 2), (4, 5))

    def matrix(word: tuple):
        current = execution(word)
        native.validate_execution(current, max_qubits=6, max_expanded_stages=121)
        return native.word_matrix(current, max_qubits=6, max_expanded_stages=121)

    require(len(original) == len(cheap_inverse) == 32, "original and cheap literal inverse have 32 calls each")
    require(len(reader4) == len(reader5) == 11, "each routed Born reader has 11 actual calls")
    require(len(future) == 54 and len(complete) == 86, "actual future54 and complete86 square-call lengths")
    inventories = {}
    for name, word, expected in (
        ("original", original, (8, 16, 8)),
        ("inverse", cheap_inverse, (8, 16, 8)),
        ("future", future, (10, 24, 20)),
        ("complete", complete, (18, 40, 28)),
        ("identity35", identity35, (0, 7, 28)),
        ("pending_phase35", phase35, (0, 7, 28)),
        ("paired_history0", paired0, (8, 23, 36)),
        ("paired_history1", paired1, (8, 23, 36)),
    ):
        inv = native.inventory(execution(word), max_qubits=6, max_expanded_stages=121)
        triple = (inv.g_count, inv.source_i_count, inv.cx_count)
        require(triple == expected, f"{name} actual inventory G/SourceI/CX={expected}")
        inventories[name] = {"G": triple[0], "SourceI": triple[1], "CX": triple[2], "calls": len(word)}
    require(all(3 not in gate.wires for gate in complete), "immutable oldRIGHT never addressed")
    require(all(not set(gate.wires).intersection((1, 2)) for gate in complete if gate.op != "SourceI"),
            "source Spin never individually addressed by G or CX")
    require(all(gate.wires == (0, 1, 2) for gate in complete if gate.op == "SourceI"),
            "every SourceI uses the one original physical source frame")

    original_u = matrix(original)
    inverse_u = matrix(cheap_inverse)
    reader_u = matrix(reader4 + reader5)
    future_u = matrix(future)
    complete_u = matrix(complete)
    rotation16 = sp.kronecker_product(native.G_LOCAL**4, sp.eye(8))
    q00 = sp.diag(1, 0, 0, 0)
    original_target = (sp.kronecker_product(sp.eye(16), q00)
                       + sp.kronecker_product(rotation16, sp.eye(4) - q00))
    eq(original_u, original_target, "original cut endpoint on all64 columns")
    eq(inverse_u, original_u.T, "cheap32call inverse is the exact full-column inverse")
    eq(mm(inverse_u, original_u), sp.eye(64), "actual original and cheap inverse compose to I64")
    reader_target = sp.kronecker_product(sp.eye(16), native.G_LOCAL.T, native.G_LOCAL.T)
    eq(reader_u, reader_target, "routed readers implement InvG4 InvG5 with original source Spin restored")
    eq(future_u, mm(reader_u, inverse_u), "actual chronological future map")
    eq(complete_u, reader_target, "all86calls have full endpoint InvG4 InvG5")
    eq(mm(complete_u.T, complete_u), sp.eye(64), "complete word retains every input column")

    birth0 = sp.kronecker_product(sp.eye(16), v)
    birth1 = sp.kronecker_product(sp.eye(32), v)
    birth = mm(birth1, birth0)
    eq(mm(birth.T, birth), sp.eye(16), "actual two-birth cut has all16 initial columns")
    actual_v = mm(original_u, birth)
    eq(mm(actual_v.T, actual_v), sp.eye(16), "V=U_paid j is an isometry")
    final_pointer = sp.kronecker_product(sp.eye(16), q00)
    future_effect = mm(future_u.T, final_pointer, future_u)
    eq(future_effect, mm(actual_v, actual_v.T), "actual future computational00 effect equals V V* on all64columns")
    eq(mm(future_effect, future_effect), future_effect, "actual future effect is a projector")
    eq(sp.trace(future_effect), 16, "actual future-test rank is16")
    eq(mm(actual_v.T, future_effect, actual_v), sp.eye(16),
       "future accepts original history with probability1 for arbitrary16input")

    r00 = sp.Matrix([1, 0, 0, 0])
    r1 = sp.kronecker_product(sp.Matrix([0, 1]), v)
    r01 = sp.Matrix([0, 1, 0, 0])
    rdark = sp.kronecker_product(sp.Matrix([0, 1]), v_perp)
    pa = sp.kronecker_product(sp.eye(16), r00*r00.T + r1*r1.T)
    pb = sp.kronecker_product(sp.eye(16), r01*r01.T)
    pdark = sp.kronecker_product(sp.eye(16), rdark*rdark.T)
    projections = (pa, pb, pdark)
    eq(pa + pb + pdark, sp.eye(64), "AF ready/pending/dark projections exhaust full carrier")
    for index, (projection, mass) in enumerate(zip(projections, (2*p**2, p**3, 0))):
        eq(mm(projection, projection), projection, f"AF sector{index} actual orthogonal projection")
        eq(mm(actual_v.T, projection, actual_v), mass * sp.eye(16),
           f"complete all-input AF sector{index} compression")
    eq(mm(pa,pb) + mm(pa,pdark) + mm(pb,pdark), sp.zeros(64), "AF sector projections are mutually orthogonal")
    pinched_effect = sum((mm(projection, future_effect, projection) for projection in projections), sp.zeros(64))
    acceptance = sp.simplify(4*p**4 + p**6)
    eq(mm(actual_v.T, pinched_effect, actual_v), acceptance * sp.eye(16),
       "mathematically pinched state acceptance is4p4+p6 for every16input")
    gap = sp.simplify(1 - acceptance)
    eq(gap, 4*p**5, "exact original-versus-pinched probability gap4p5")
    require(1 < 5, "p=(sqrt5-1)/2>0 makes4p5 strictly positive")
    eq(mm(actual_v.T, future_effect - pinched_effect, actual_v), 4*p**5 * sp.eye(16),
       "actual future observable is outside AF pinching's fixed algebra")
    require(any(not zero(value) for value in future_effect - pinched_effect),
            "AF algebra mismatch is nonzero on the actual full carrier")

    # Mathematical E_AF comparison is NOT inserted into this chronological word.
    cold = mm(birth.T, complete_u, birth)
    eq(cold, p * sp.eye(16), "actual entire-history cold return is p I16")
    eq(mm(cold.T, cold), p**2 * sp.eye(16), "entire-history feedback uses p2 I16")
    stage_dimensions = [16, 32] + [64] * len(complete)
    require(len(stage_dimensions) == 88 and sum(stage_dimensions) == 5552,
            "complete physical growing clock N88 D5552, including both births")
    require(complete[-1] == Gate("CX", (0, 5)), "last actual CX closes the clock without an added identity")

    require(tuple(map(len, identity_blocks)) == (1, 7, 7, 3, 3, 9, 5),
            "seven actual parity-source blocks have lengths1,7,7,3,3,9,5")
    require(len(identity35) == len(phase35) == 35 and len(paired0) == len(paired1) == 67,
            "two actual histories have one common67call inventory")
    for bits in range(8):
        pbit, b1, b2 = (bits >> 2) & 1, (bits >> 1) & 1, bits & 1
        forms = (pbit, b1, b2, pbit ^ b1, pbit ^ b2, b1 ^ b2, pbit ^ b1 ^ b2)
        require(sum(forms) == (0 if bits == 0 else 4), f"actual parity exponent sum at input{bits:03b}")
    identity_u = matrix(identity35)
    phase_u = matrix(phase35)
    eq(identity_u, sp.eye(64), "all64columns of actual35call same-inventory identity")
    eq(phase_u, sp.eye(64) - 2*pb, "actual35call word changes only pendingAFsector sign; Spin/oldRIGHT restored")
    paired0_u, paired1_u = matrix(paired0), matrix(paired1)
    eq(paired0_u, original_u, "first actual67call history endpoint")
    eq(paired1_u, mm(phase_u, original_u), "second actual67call history endpoint")
    paired0_v, paired1_v = mm(paired0_u, birth), mm(paired1_u, birth)
    paired_cold0 = mm(birth.T, paired0_v)
    paired_cold1 = mm(birth.T, paired1_v)
    eq(paired_cold0, p**2*sp.eye(16) + p*rotation16,
       "actual history0 cold corner is p2I+pG4")
    eq(paired_cold1, p**2*sp.eye(16) + p**4*rotation16,
       "actual history1 cold corner is p2I+p4G4")
    cosine = sp.simplify((native.G_LOCAL**4)[0, 0])
    h0 = sp.simplify(p**4 + p**2 + 2*p**3*cosine)
    h1 = sp.simplify(p**4 + p**8 + 2*p**6*cosine)
    eq(mm(paired_cold0.T, paired_cold0), h0*sp.eye(16), "actual history0 complete compression Gram")
    eq(mm(paired_cold1.T, paired_cold1), h1*sp.eye(16), "actual history1 complete compression Gram")
    eq(h0 - h1, 8*p**11, "exact entire16input return difference h0-h1=8p11")
    for index, (projection, sign) in enumerate(zip(projections, (1, -1, 1))):
        eq(mm(projection, paired1_v), sign*mm(projection, paired0_v),
           f"paired actual histories have identical AF sector{index} state for every complex input")
    eq(mm(paired0_v.T, future_effect, paired0_v), sp.eye(16),
       "same native54call future accepts actual paired history0 with probability1")
    actual_pair_acceptance = (1 - 2*p**3)**2
    eq(mm(paired1_v.T, future_effect, paired1_v), actual_pair_acceptance*sp.eye(16),
       "same native54call future accepts actual paired history1 with probability(1-2p3)^2")
    eq(1 - actual_pair_acceptance, 8*p**5, "two actual same-inventory history separation is8p5")
    pair_dimensions = [16, 32] + [64] * 67
    queried_pair_dimensions = [16, 32] + [64] * 121
    require(len(pair_dimensions) == 69 and sum(pair_dimensions) == 4336,
            "paired histories use common growing clockN69D4336")
    require(len(queried_pair_dimensions) == 123 and sum(queried_pair_dimensions) == 7792,
            "each paired history plus the same future has clockN123D7792")
    require(all(3 not in gate.wires for gate in paired0 + paired1),
            "both actual paired histories protect immutable oldRIGHT")
    require(all(not set(gate.wires).intersection((1, 2)) for gate in paired0 + paired1 if gate.op != "SourceI"),
            "paired strengthening never individually addresses source Spin")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    word_path = args.output_dir / "native_word.json"
    word_object = {
        "schema": "d0.coherent-af-native-future-test/1",
        "source_owner": str(SOURCE), "source_sha256": SOURCE_SHA,
        "wire_roles": {"P": 0, "Spin": [1, 2], "immutable_oldRIGHT": 3, "born_controls": [4, 5]},
        "births_before_word": [
            {"stage": 0, "wire": 4, "vector": ["sqrt(p)", "p"], "from_dim": 16, "to_dim": 32},
            {"stage": 1, "wire": 5, "vector": ["sqrt(p)", "p"], "from_dim": 32, "to_dim": 64}],
        "call_boundaries": {"original": [0, 32], "cheap_inverse": [32, 64], "reader4": [64, 75], "reader5": [75, 86]},
        "native_word": json.loads(native.canonical_json(execution(complete))),
        "clock_stage_dimensions": stage_dimensions,
        "terminal_test": "computational control4=0 and control5=0; all other columns retained",
        "mathematical_pinching_is_executed": False,
        "paired_actual_histories": {
            "history0": json.loads(native.canonical_json(execution(paired0))),
            "history1": json.loads(native.canonical_json(execution(paired1))),
            "common_future": json.loads(native.canonical_json(execution(future))),
            "clock_stage_dimensions": pair_dimensions,
            "queried_clock_stage_dimensions": queried_pair_dimensions,
        },
    }
    write_json(word_path, word_object)
    receipt = {
        "schema": "d0.coherent-af-native-future-test-receipt/1",
        "checker_sha256": sha(Path(__file__).resolve()),
        "source_sha256": SOURCE_SHA, "native_word_sha256": sha(word_path),
        "status": "PASS", "check_count": len(CHECKS), "checks": CHECKS,
        "inventory": inventories,
        "test": {"effect": "V V*", "rank": 16, "original_acceptance": "1",
                 "mathematical_pinched_acceptance": "4p^4+p^6",
                 "gap": "4p^5", "gap_exact": str(gap), "gap_numeric": str(sp.N(gap, 30))},
        "whole_execution": {"N": 88, "D": 5552, "endpoint": "InvG_4 InvG_5 tensor I_PSpinRIGHT",
                            "C": "p I16", "J": "-16 log(1-z+z p^2)",
                            "full_modes": 425*5552, "harmonic_offset": 359*5552},
        "actual_paired_witness": {"history_calls": 67, "N": 69, "D": 4336,
                                  "future_calls": 54, "queried_N": 123, "queried_D": 7792,
                                  "AF_states_identical_for_every_input": True,
                                  "acceptance0": "1", "acceptance1": "(1-2p^3)^2",
                                  "gap": "8p^5", "equal_full_Book_prices_claimed": False,
                                  "h0": str(h0), "h1": str(h1), "h0_minus_h1": "8p^11",
                                  "Jj": "-16 log(1-z+z hj)"},
        "scope": {"countertest_requires_mutable_control_future_admission": True,
                  "AF_algebra_contains_actual_future_effect": False,
                  "physical_dephasing_admitted": False,
                  "pinched_state_is_second_admitted_history": False,
                  "restricted_VrhoVstar_image_sufficiency_refuted": False,
                  "actual_finite_grammar_pair_separated_by_actual_future": True,
                  "same_original_H1_task_admission_proved": False,
                  "physical_Info_selected": False, "GR_closed": False},
    }
    write_json(args.output_dir / "receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
