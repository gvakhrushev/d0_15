#!/usr/bin/env python3
"""Exact coherent controlled-return composition and inherited primary source.

No old suite or eigensolver is run. Check full128 forward words, the real
quantum flag/RIGHT Gram, rank-birth and capacity controls, and exact source
compression. Consume the pinned original cap2 source and owned C1 theorem.
"""
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    PREFIX + "check_native_retained_choice_dispatch.py": "4c0cfe7af38ca3d768bb29b47b1b7300504ebdaa90a3bdae0f3a5910ec72bc67",
    PREFIX + "NATIVE_RETAINED_CHOICE_DISPATCH.md": "6f4289d101d2b3cd70f33a14828e2f6da43bfec4b7e58765b8aad1278f61c065",
    PREFIX + "GOLDEN_EXACT_DETECTOR.md": "d33c9c2cb2322e381723f481eb1fcf58058fd05ad88eda92c5597c026d02eb77",
    PREFIX + "PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE.md": "f45c6b301aad0d5601fc771b20550072ad8eeb579c8a701ec51c91b249d64f89",
    PREFIX + "PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_CERTIFICATE.json": "9c910c2e28d02af5fd3a8642d98d01b8c58aeb0a9a55ccf3612a5bc80e397785",
    PREFIX + "PRIMARY_RIGHT_COMPLETE_CODE_SOURCE.md": "7a38155f37b98fabdd358271be52ad4919a0b28963a5fb952d91da049eba4424",
    "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/RESULT.md":
        "9a441405c455adda9651f88c21fcda4d9383673a3718e88a93aeb50467133e71",
    "02_REGISTRY/research/A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md":
        "f09c24bb7b8ef5f512555257dcd9a335571c052b452482d2c31a3b8e586efdc5",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


for path, digest in PINS.items():
    require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
            "immutable coherent-source input: " + path)
spec = importlib.util.spec_from_file_location("owned_dispatch_definitions_only", ROOT / next(iter(PINS)))
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
Z, ONE, A, P = O.Z, O.ONE, O.A, O.P
add, sub, mul, scale, power = O.add, O.sub, O.mul, O.scale, O.power

# All are chronological FORWARD primitives. Rminus is an inverse only
# on c1; its full c0 blocks are retained and explicitly checked below.
RPLUS = ("XP", "XC", "G", "XC", "XP", "G")
RMINUS = ("XC", "G", "XC", "XP", "G", "XP")
QWORD = ("K",) + RMINUS + ("K",) + RPLUS
BASEWORD = ("K", "K") + RMINUS + RPLUS


def cnot(value, control):
    result = [Z] * len(value)
    for n, entry in enumerate(value):
        result[n ^ 1 if (n >> control) & 1 else n] = entry
    return result


def execute(value, word):
    for letter in word:
        if letter == "K":
            value = O.owned["k_gate"](value)
        elif letter == "G":
            value = O.owned["g"](value)
        else:
            value = cnot(value, 6 if letter == "XP" else 5)
    return value


def word_checks():
    profile = Counter({"K": 2, "G": 4, "XC": 4, "XP": 4})
    require(Counter(QWORD) == Counter(BASEWORD) == profile, "same actual addressed primitive multiset")
    columns, pads = [], []
    for j in range(128):
        e = O.owned["basis"](128, j)
        fourth = e
        for _ in range(4):
            fourth = O.owned["g"](fourth)
        c, flag = (j >> 5) & 1, (j >> 6) & 1
        actual, baseline = execute(e, QWORD), execute(e, BASEWORD)
        if "--mutation=delete-c0" in sys.argv and not c:
            actual = e
        expected = [fourth[n] if ((c == flag == 1 and ((n % 16) >> 1).bit_count() >= 2)
                                  or (c == flag == 0 and ((n % 16) >> 1).bit_count() < 2))
                    else e[n] for n in range(128)]
        require(actual == expected, "actual coherent word keeps all c0/P complements")
        expected_pad = fourth if c == flag == 0 else e
        require(baseline == expected_pad, "matched baseline has its actual full complement")
        require(all(x == Z or n // 16 == j // 16 for n, x in enumerate(actual)),
                "quantum P,c and orientation f are retained")
        columns.append(actual)
        pads.append(baseline)
    for i in range(128):
        for j in range(i + 1):
            require(O.owned["dot"](columns[i], columns[j]) == (ONE if i == j else Z),
                    "full128 candidate orthogonal")
            require(O.owned["dot"](pads[i], pads[j]) == (ONE if i == j else Z),
                    "full128 baseline orthogonal")
    return {"dimension": 128, "forward_letters_each_prefix": 14,
            "primitive_inventory": dict(profile),
            "c1_P0": "I", "c1_P1": "I_low+G^4_high",
            "c0_P0": "G^4_low+I_high", "c0_P1": "I",
            "baseline_c0_P0": "G^4_all", "baseline_other_blocks": "I",
            "unmeasured_common_selector_preparation": "G(P)|0> on BOTH programmes"}


def msum(left, right):
    return [[add(a, b) for a, b in zip(x, y)] for x, y in zip(left, right)]


def mmul(left, right):
    return [[sum_field(mul(left[i][k], right[k][j]) for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def sum_field(values):
    result = Z
    for value in values:
        result = add(result, value)
    return result


def determinant(matrix):
    total = Z
    for perm in permutations(range(len(matrix))):
        inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
        term = ONE
        for i, j in enumerate(perm):
            term = mul(term, matrix[i][j])
        total = add(total, scale((-1) ** inversions, term))
    return total


def coherent_fixture():
    # C=I2/sqrt2, U0=I,U1=Z, K+/-=X projectors. Each full PR block
    # is rank one of mass1/2, whereas the RIGHT posterior has eigen p,p².
    vectors = ((A, A, P, scale(-1, P)), (A, scale(-1, A), P, P))
    blocks = [[[scale(Q(1, 4), mul(x, y)) for y in v] for x in v] for v in vectors]
    total = [[Z] * 4 for _ in range(4)]
    for block in blocks:
        physical = [list(row) for row in zip(*block)]  # FULL P⊗R transpose.
        partial = [[block[2 * (i // 2) + j % 2][2 * (j // 2) + i % 2]
                    for j in range(4)] for i in range(4)]
        require(determinant(partial) == scale(Q(-1, 16), power(P, 6)),
                "partial-R transpose has strictly negative determinant")
        if "--mutation=partial-R-transpose" in sys.argv:
            physical = partial
        require(mmul(physical, physical) == [[scale(Q(1, 2), x) for x in row] for row in physical],
                "physical full Gram is positive rank one with mass1/2")
        require(sum_field(physical[i][i] for i in range(4)) == O.scalar(Q(1, 2)),
                "actual complete leaf mass is1/2")
        posterior = [[scale(2, add(physical[i][j], physical[2 + i][2 + j]))
                      for j in range(2)] for i in range(2)]
        require(add(posterior[0][0], posterior[1][1]) == ONE
                and determinant(posterior) == power(P, 3),
                "conditional RIGHT posterior has actual eigenvalues p,p²")
        total = msum(total, physical)
    prior = [[add(total[i][j], total[2 + i][2 + j]) for j in range(2)] for i in range(2)]
    require(prior == [[O.scalar(Q(1, 2)), Z], [Z, O.scalar(Q(1, 2))]], "original RIGHT prior unchanged")
    require(total[0][2] != Z, "true PR prior contains coherent cross-arm terms")
    require([[scale(4, x) for x in row] for row in total]
            != [[ONE if i == j else Z for j in range(4)] for i in range(4)],
            "uniform PR likelihood completeness is NOT inherited")
    # Actual nonzero spectra: full YPR has1/2,1/2, so Acoh=0.
    # Conditional PR leaves pure, conditional R spectrum p,p²:
    # H(P|YR)=-(2-p), H(Y|R)=2-p, which cancel on the whole tape.
    log2 = {"log_phi2": ONE}
    golden_entropy = {"1": sub(O.scalar(2), P)}
    full_entropy = log2  # two nonzero eigenvalues1/2 of the full cut.
    yr_entropy = O.vadd(log2, golden_entropy)
    conditional_p = O.vadd(full_entropy, O.vscale(O.scalar(-1), yr_entropy))
    conditional_y = O.vadd(yr_entropy, O.vscale(O.scalar(-1), log2))
    require(O.vequal(O.vadd(conditional_p, conditional_y), {}),
            "negative postselected term is compensated by retained Y")
    # Full supplied reference has eight eigenvalues1/8. Omitting P
    # would use the false capacity4 and change the declared label net.
    reference_cross_entropy = {"log_phi2": O.scalar(2 if "--mutation=drop-P-capacity" in sys.argv else 3)}
    gain = O.vadd(reference_cross_entropy, O.vscale(O.scalar(-1), full_entropy))
    source_net = O.vadd(log2, O.vscale(O.scalar(-1), gain))
    require(O.vequal(source_net, O.vscale(O.scalar(-1), log2)),
            "label cost minus central gain retains the common P-capacity offset")
    return {"complete_conditional_entropy": 0, "each_leaf_H_P_given_R": "-(2-p)",
            "H_Y_given_R": "2-p", "full_transpose_required": True,
            "actual_PR_prior_is_uniform": False,
            "central_label_cost_minus_gain": "A_coh-log_phi2",
            "initial_pure_flag_capacity_is_executed_work": False}


def source_fixture():
    v = (A, P)
    single, coherent = {}, {}
    for c, dc in ((Q(3, 5), Q(-4, 5)), (Q(4, 5), Q(3, 5))):
        cross = scale(c * dc, mul(A, P))
        jet = [[Z, cross], [cross, scale(2 * c * dc, mul(P, P))]]
        compression = sum_field(mul(mul(v[i], jet[i][j]), v[j]) for i in range(2) for j in range(2))
        old_jet = O.scalar(2 * c * dc)
        require(compression == mul(mul(P, P), old_jet), "occupied-support derivative has exact selector weight p²")
        single = O.vadd(single, O.vscale(scale(-1, old_jet), O.logq(c * c)))
        coherent = O.vadd(coherent, O.vscale(scale(-1, compression), O.logq(c * c)))
    if "--mutation=omit-selector-weight" in sys.argv:
        coherent = single
    require(O.vequal(coherent, O.vscale(mul(P, P), single)), "coherent source equals p² times single-arm source")
    require(Q(9, 16) < 1, "fixture single-arm entropy source (24/25)log_phi(9/16) is negative")
    # A genuine rank-birth model, C=|0>, queryI, other armG|0>:
    # det[p|0><0|+p²G|0><0|G*]=p^5>0, born from rank1 at angle0.
    rho = [[add(P, power(P, 3)), mul(A, power(P, 3))],
           [mul(A, power(P, 3)), power(P, 4)]]
    require(determinant(rho) == power(P, 5), "actual coherent rank-birth determinant")
    return {"exact_angle_source_factor": "p^2", "rank_birth_model_determinant_at_G": "p^5",
            "rank_birth_remainder_may_include": "alpha^2 log|alpha|",
            "new_full_Gram_inversion_used": False}


def scaled_decimal(integer, digits):
    sign = "-" if integer < 0 else ""
    integer = abs(integer)
    return sign + str(integer // 10 ** digits) + "." + str(integer % 10 ** digits).zfill(digits)


def decimal_lower(value, digits=30):
    integer = (value.numerator * 10 ** digits) // value.denominator
    return scaled_decimal(integer, digits)


def decimal_upper(value, digits=30):
    integer = -((-value.numerator * 10 ** digits) // value.denominator)
    return scaled_decimal(integer, digits)


def inherited_source():
    saved = json.loads((ROOT / (PREFIX + "PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_CERTIFICATE.json")).read_bytes())
    lo, hi = Q(3, 5), Q(5, 8)
    for _ in range(80):
        midpoint = (lo + hi) / 2
        if midpoint * midpoint + midpoint < 1:
            lo = midpoint
        else:
            hi = midpoint
    weights = (1 - hi, 1 - lo)  # p²=1-p.
    result = {}
    for name, interval in (("coherent_cap2_entropy_angle", saved["linear_coefficients"]["conditional_entropy_cap2"]),
                           ("coherent_cap2_abort_angle", saved["actual_abort"]["angle_source_linear_coefficient"])):
        a, b = map(Q.from_float, interval)
        products = [x * y for x in (a, b) for y in weights]
        lower, upper = min(products), max(products)
        require(upper < 0 if "entropy" in name else lower > 0, "inherited strict coherent source sign")
        require(Q(decimal_lower(lower)) <= lower <= upper <= Q(decimal_upper(upper)),
                "displayed decimal endpoints outwardly enclose exact rational source")
        result[name] = {"rational_lower": str(lower), "rational_upper": str(upper),
                        "decimal_lower": decimal_lower(lower),
                        "decimal_upper": decimal_upper(upper)}
    return result


def main():
    word, fixture, source = word_checks(), coherent_fixture(), source_fixture()
    print(json.dumps({"status": "PASS", "full_word": word, "quantum_cut_control": fixture,
                      "source_compression": source, "inherited_primary_sources": inherited_source(),
                      "source_sha256": {**{PREFIX + n: h for n, h in O.PINS.items()}, **PINS},
                      "new_256_eigensystem_replayed": False,
                      "physical_Book_Info_or_work_selected": False,
                      "physical_oldRIGHT_spectral_test_admission_inferred": False,
                      "task_abort_constraint_removed": False}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
