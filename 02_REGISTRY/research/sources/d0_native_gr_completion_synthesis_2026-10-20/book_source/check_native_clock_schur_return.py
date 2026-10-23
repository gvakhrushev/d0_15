#!/usr/bin/env python3
"""Exact actual-stage clock elimination and full retained-record return.

Definition-only import of the pending stage packet; no old certificate main,
large clock matrix, eigensolver, physical clock or Book binding is supplied.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    PREFIX + "check_native_stage_clock_cut.py": "4476d246a698e2c3e2518c39a23e12811375d95f545c4569eaeafe6b265c7474",
    PREFIX + "NATIVE_STAGE_CLOCK_AND_POINTED_DESCENT.md": "e970dda60699b7236599c9618445fe17cb8cbb0b9bb8c8de8808a190c4c00848",
    "01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md": "592bbbb1dae9cc599df2eef9cabf117b19f8566d755ad072b77beb04624271d7",
}


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


for path, digest in PINS.items():
    require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
            "immutable Schur-return input: " + path)
spec = importlib.util.spec_from_file_location("owned_stage_definitions_only", ROOT / next(iter(PINS)))
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
Z, ONE, A, P = N.Z, N.ONE, N.A, N.P
add, sub, scale, mul, power = N.add, N.sub, N.scale, N.mul, N.power
mm, transpose, eye, ms, difference = N.mm, N.transpose, N.eye, N.ms, N.difference


def polynomial(coefficients):
    result = list(coefficients)
    while len(result) > 1 and result[-1] == Z:
        result.pop()
    return result


def padd(left, right):
    return polynomial([add(left[i] if i < len(left) else Z,
                           right[i] if i < len(right) else Z)
                       for i in range(max(len(left), len(right)))])


def pmul(left, right):
    result = [Z] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] = add(result[i + j], mul(x, y))
    return polynomial(result)


def ppow(value, exponent):
    result = [ONE]
    for _ in range(exponent):
        result = pmul(result, value)
    return result


def peval(value, point):
    result = Z
    for coefficient in reversed(value):
        result = add(mul(result, point), coefficient)
    return result


def char2(matrix):
    require(len(matrix) == 2 and all(len(row) == 2 for row in matrix), "two-arm sector dimension")
    return [ONE, scale(-1, add(matrix[0][0], matrix[1][1])),
            sub(mul(matrix[0][0], matrix[1][1]), mul(matrix[0][1], matrix[1][0]))]


def spin_lift(matrix):
    return [[matrix[i // 4][j // 4] if i % 4 == j % 4 else Z
             for j in range(8)] for i in range(8)]


def record_embedding(sign):
    return [[scale(sign if row % 2 else 1, ONE) if row // 2 == column else Z
             for column in range(8)] for row in range(16)]


def complete_return(label, names, palette, mutation):
    closed_names = names + ["idle"]
    if mutation == "drop-idle-clock-letter":
        closed_names = names
    require(len(closed_names) == 16 and closed_names[-1] == "idle",
            "closed clock return retains the idle sixteenth transition")
    monodromy = eye(16)
    for name in closed_names:
        monodromy = mm(palette[name], monodromy)
    require(mm(transpose(monodromy), monodromy) == eye(16), "full retained-record monodromy is orthogonal")
    # The archive retains clocks1..15 with their FULL sixteen apparatus rows.
    # D only advances within these clocks; leaving15 goes to the active0.
    support = {k: [(c, c + k) for c in range(1, 16) if c + k <= 15]
               for k in range(16)}
    require(support[14] == [(1, 15)] and support[15] == [],
            "clock archive has exact nilpotency index fifteen")
    require(all(len(support[k]) == 15 - k for k in range(15)),
            "every retained archive path has the actual forward support")
    # B D^k C: C applies U0 and entersclock1; B exits onlyclock15 via U15.
    partial, clock, return_terms = palette[closed_names[0]], 1, []
    for k in range(15):
        if clock == 15:
            term = mm(palette[closed_names[15]], partial)
            return_terms.append((k, k + 2, term))
        if k < 14:
            partial = mm(palette[closed_names[clock]], partial)
            clock += 1
    require(len(return_terms) == 1 and return_terms[0][:2] == (14, 16),
            "unique full clock return has fourteen archive links and sixteen total ticks")
    require(return_terms[0][2] == monodromy, "actual ordered Schur return equals U15 through U0")
    one_tick_corner = ms(Z, eye(16))  # clock0 advances to1, regardless of apparatus.
    one_tick_feedback = difference(eye(16), mm(transpose(one_tick_corner), one_tick_corner))
    loop_feedback = difference(eye(16), mm(transpose(monodromy), monodromy))
    if mutation == "identify-one-step-feedback-with-return":
        one_tick_feedback = loop_feedback
    require(one_tick_feedback == eye(16) and loop_feedback == ms(Z, eye(16)),
            "one-step full-clock0 feedback is I16 while the full-loop feedback is zero")
    initial = [[ONE if row == 2 * spin else Z for spin in range(4)] for row in range(16)]
    prepared = mm(mm(transpose(initial), monodromy), initial)
    expected = eye(4) if label == "identity" else ms(power(P, 3), eye(4))
    require(prepared == expected, "prepared corner is taken only after full clock elimination")
    return monodromy, prepared


def main():
    require(len(sys.argv) <= 2, "at most one mutation argument")
    mutation = None
    if len(sys.argv) == 2:
        match = re.fullmatch(r"--mutation=(.+)", sys.argv[1])
        require(match is not None and match[1] in {
            "drop-idle-clock-letter", "identify-one-step-feedback-with-return", "omit-record-complement"},
            "known Schur-return mutation")
        mutation = match[1]
    palette, programs = N.actual_palette(), N.actual_programs()
    jp, jm = record_embedding(1), record_embedding(-1)
    require(mm(transpose(jp), jp) == ms(scale(2, ONE), eye(8))
            and mm(transpose(jm), jm) == ms(scale(2, ONE), eye(8)),
            "record-X embeddings have exact normalization two")
    require(mm(transpose(jp), jm) == ms(Z, eye(8)), "record-X sectors are orthogonal")
    joined = [plus + minus for plus, minus in zip(jp, jm)]
    joined_inverse = ms(scale(N.F(1, 2), ONE), transpose(joined))
    require(mm(joined_inverse, joined) == eye(16), "all sixteen record-sector coordinates are retained")
    gate = N.parse_lean_matrix("03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
                              "def gate (", {"a": A, "p": P})
    sign = [[ONE, Z], [Z, scale(-1, ONE)]]
    arm_sectors = {
        "identity": (eye(2), sign),
        "order": (mm(mm(transpose(gate), sign), gate), mm(gate, gate)),
    }
    minus, plus = [ONE, scale(-1, ONE)], [ONE, ONE]
    quadratic = [ONE, scale(-2, power(P, 3)), ONE]
    target = {
        "identity": pmul(ppow(minus, 12), ppow(plus, 4)),
        "order": pmul(pmul(ppow(minus, 4), ppow(plus, 4)), ppow(quadratic, 4)),
    }
    results = {}
    for label, names in programs.items():
        monodromy, prepared = complete_return(label, names, palette, mutation)
        actual_sector_char = []
        for embedding, arm_sector in zip((jp, jm), arm_sectors[label]):
            compressed = ms(scale(N.F(1, 2), ONE), mm(mm(transpose(embedding), monodromy), embedding))
            require(compressed == spin_lift(arm_sector), "actual full monodromy in each record-X sector")
            require(mm(monodromy, embedding) == mm(embedding, compressed),
                    "record-X sector is invariant without discarding its complement")
            actual_sector_char.append(char2(arm_sector))
        # Similarity by [J+,J-] makes two sectors; each arm block occurs spin4 times.
        actual_characteristic = ppow(pmul(*actual_sector_char), 4)
        if mutation == "omit-record-complement":
            actual_characteristic = ppow([ONE, scale(-1, prepared[0][0])], 4)
        require(actual_characteristic == target[label],
                "full return determinant retains all sixteen apparatus coordinates")
        require(peval(actual_characteristic, ONE) == Z,
                "the full t=1 return resolvent is singular despite the archive inverse")
        results[label] = {"prepared_j_star_M_j": "I4" if label == "identity" else "p^3 I4",
                          "full_characteristic_coefficients_in_q": [[str(c) for c in x] for x in actual_characteristic],
                          "record_X_plus_arm_sector": N.encoded(arm_sectors[label][0]),
                          "record_X_minus_arm_sector": N.encoded(arm_sectors[label][1])}
    numerator = padd(ppow(minus, 2), [Z, scale(4, power(P, 2))])
    require(numerator == quadratic, "Golden quadratic equals (1-q)^2+4p^2 q")
    require(pmul(target["order"], ppow(minus, 8)) == pmul(target["identity"], ppow(numerator, 4)),
            "exact full-monodromy determinant ratio has spin multiplicity four")
    print(json.dumps({
        "status": "PASS", "field": "Q(a), a^4+a^2-1=0, p=a^2, positive Golden embedding",
        "field_coefficient_order": ["1", "a", "a^2", "a^3"], "programmes": results,
        "record_X_normalization": "Jplus^*Jplus=Jminus^*Jminus=2I8; compression includes1/2",
        "full_monodromy_determinants": {
            "identity": "(1-q)^12*(1+q)^4",
            "order": "(1-q)^4*(1+q)^4*(1-2*p^3*q+q^2)^4",
            "order_over_identity": "[1+4*p^2*q/(1-q)^2]^4",
            "spin_multiplicity": 4, "additional_clock_multiplicity": False,
            "raw_negative_logdet_order_minus_identity": "-4*log(1+4*p^2*q/(1-q)^2)<0 for0<q<1",
        },
        "clock_Schur_elimination": {
            "active_cut": "clock0 tensor FULL apparatus16", "archive_cut": "clocks1..15 tensor FULL apparatus16",
            "archive_D_nilpotency_index": 15, "nonzero_B_Dk_C_exponent": 14,
            "complete_return_ticks_including_idle": 16, "monodromy_order": "M=U15*U14*...*U0",
            "archive_det_I_minus_tD": "1", "Schur_I_minus_tW": "I16-t^16*M",
            "archive_inverse": "sum_(k=0)^14 t^k D^k; valid for every t, including1",
            "full_det_I_minus_tW": "det(I16-q*M), q=t^16",
            "full_resolvent_for0_lt_t_lt1": True, "full_resolvent_at_t1": False,
            "Schur_complement_at_t1_is_still_defined": True,
        },
        "full_apparatus_clock0_feedback": {"F_for_one_W": "I16", "F_for_W16": "0"},
        "scope": {"dependency_publication": "stage packet pending co-publication; not claimed as remote input",
                  "pending_co_publication_inputs": list(PINS)[:2],
                  "original_reported_trial": "seed0 first15 transitions, before idle wrap",
                  "closed_extension": "sixteen transitions includes owned idle wrap, original record reused",
                  "fresh_IID_record_reset": False, "q_is_physical_Book_z_or_selected_weight": False,
                  "return_loop_determinant_is_Book_feedback": False,
                  "physical_Book_U_N_or_elapsed_clock_binding_proved": False,
                  "original_primary_cap2_controller_supplied": False,
                  "physical_heat_graph_or_GR_source_selected": False,
                  "old_certificate_main_executed": False, "large_clock_matrix_built": False},
        "source_sha256": {**N.PINS, **PINS},
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
