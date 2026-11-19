#!/usr/bin/env python3
"""Exact native recombiner/complement, clock-cut and amplitude type controls.

Consume the owned full controlled word. New finite Golden-query fixture
checks its actual output complement and a noncommuting determinant transport.
No old suite, full primary matrix, eigensolver or physical cut selection.
"""
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
    PREFIX + "check_native_coherent_choice_source.py": "f5422b5ed923daab8bf7ed8eda89046fee6abe987fce2e93fe2094eac9e6943a",
    PREFIX + "NATIVE_COHERENT_CHOICE_SOURCE.md": "2e906213861d0c4d1812e1ec8608aec571aeb18230fce8f791fb4cce6b4c2c1b",
    PREFIX + "PRIMARY_STOPPED_PORT_PRICE_AND_PREPARATION_EULER.md": "66108133dc615593e50e634274005a5d904b533f3a2f3fd7861a57b2557b8b50",
    PREFIX + "PRIMARY_CAR_PAID_RETURN_PRICE.md": "2fdf545aa33e3c85f9ef81398fe604a4770c0af76ee872845beefd4f365cfcc1",
    PREFIX + "BOOK_SOURCE_BINDING.md": "2b26bf2f4c1b128731ccf14a17437ba654c046e82b5e42e55113a8b6053494ea",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md": "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
    "02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/paired_feedback.md": "72e241a39b0142a157693e575aaa86fcfadcfba698cadaddf0db274b81a68b62",
    "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md": "73bf64d8c05b2624e092d851cab5f11019fd886c74d6b332ed97f4d4f4d4d434",
    "02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md": "75845813d20ecf7b585fb7b7a7bef8b8170a711e94a56bb0df0cc3546622a036",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


for path, digest in PINS.items():
    require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, "immutable complement input: " + path)
spec = importlib.util.spec_from_file_location("owned_coherent_definitions_only", ROOT / next(iter(PINS)))
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
Z, ONE, A, P = N.Z, N.ONE, N.A, N.P
add, sub, mul, scale, power = N.add, N.sub, N.mul, N.scale, N.power
field = lambda x: scale(Q(x), ONE)


def rot(value, bit, inverse=False):
    result = list(value)
    for j in range(len(value)):
        if not (j >> bit) & 1:
            k = j ^ (1 << bit)
            off = scale(-1 if inverse else 1, P)
            result[j] = sub(mul(A, value[j]), mul(off, value[k]))
            result[k] = add(mul(off, value[j]), mul(A, value[k]))
    return result


def cx(value, control, target):
    result = [Z] * len(value)
    for j, x in enumerate(value):
        result[j ^ (1 << target) if (j >> control) & 1 else j] = x
    return result


def recombine(value):
    return cx(rot(cx(value, 5, 6), 6), 5, 6)


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[N.sum_field(mul(a[i][k], b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def ma(a, b):
    return [[add(x, y) for x, y in zip(r, s)] for r, s in zip(a, b)]


def ms(c, a):
    return [[mul(c, x) for x in row] for row in a]


def eye(n):
    return [[ONE if i == j else Z for j in range(n)] for i in range(n)]


def inverse_field(x):
    columns = [mul(x, tuple(Q(i == j) for i in range(4))) for j in range(4)]
    rows = [[columns[j][i] for j in range(4)] + [Q(i == 0)] for i in range(4)]
    for j in range(4):
        pivot = next(i for i in range(j, 4) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        q = rows[j][j]
        rows[j] = [a / q for a in rows[j]]
        for i in range(4):
            if i != j:
                q = rows[i][j]
                rows[i] = [a - q * b for a, b in zip(rows[i], rows[j])]
    result = tuple(row[-1] for row in rows)
    require(mul(x, result) == ONE, "exact field inverse")
    return result


def inverse(a):
    n = len(a)
    rows = [list(row) + e for row, e in zip(a, eye(n))]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j] != Z)
        rows[j], rows[pivot] = rows[pivot], rows[j]
        q = inverse_field(rows[j][j])
        rows[j] = [mul(q, x) for x in rows[j]]
        for i in range(n):
            if i != j:
                q = rows[i][j]
                rows[i] = [sub(x, mul(q, y)) for x, y in zip(rows[i], rows[j])]
    result = [row[n:] for row in rows]
    require(mm(a, result) == eye(n), "actual matrix inverse")
    return result


def determinant(a):
    result = Z
    for perm in permutations(range(len(a))):
        term = ONE
        for i, j in enumerate(perm):
            term = mul(term, a[i][j])
        inv = sum(perm[i] > perm[j] for i in range(len(a)) for j in range(i + 1, len(a)))
        result = add(result, scale((-1) ** inv, term))
    return result


def native_complement():
    basis = N.O.owned["basis"]
    for c in range(2):
        for flag in range(2):
            e = basis(128, 32 * c + 64 * flag)
            require(recombine(e) == rot(e, 6, inverse=bool(c)), "full c0/c1 recombiner complement")
    native_u = []
    for j in range(16):
        e = basis(16, j)
        u = e
        for _ in range(4):
            u = rot(u, 0)
        native_u.append(u if (j >> 1).bit_count() >= 2 else e)
    u = transpose(native_u)
    high = [j for j in range(16) if (j >> 1).bit_count() >= 2]
    g = scale(16, power(P, 6))
    h = ma(ms(P, eye(16)), ms(power(P, 2), u))
    for closed in (False, True):
        blocks = []
        for word in (N.BASEWORD, N.QWORD):
            columns = []
            for j in range(16):
                value = N.execute(rot(basis(256, 32 + j), 6), word)
                value = rot(value, 7)  # actual one-Golden-query test, not the primary D instrument.
                if closed and "--mutation=omit-recombiner" not in sys.argv:
                    value = recombine(value)
                columns.append(value)
            active = [[column[32 + i] for column in columns] for i in range(16)]
            expected = ms(A, h if word == N.QWORD else eye(16)) if closed else ms(P, eye(16))
            require(active == expected, "literal closed active block and common baseline")
            feedback = ma(eye(16), ms(field(-1), mm(transpose(active), active)))
            if "--mutation=abort-as-complement" in sys.argv:
                event_columns = [[x for i, x in enumerate(column) if not (i >> 7) & 1] for column in columns]
                feedback = [[N.O.owned["dot"](x, y) for y in event_columns] for x in event_columns]
            pi = [[ONE if i == j and i in high else Z for j in range(16)] for i in range(16)]
            if "--mutation=rank-two-generator" in sys.argv:
                pi = [[ONE if i == j and i in (14, 15) else Z for j in range(16)] for i in range(16)]
            target = ms(power(P, 2) if closed else P, eye(16))
            if closed and word == N.QWORD:
                target = ma(target, ms(mul(P, g), pi))
            require(feedback == target, "true full complement retains all eight high CAR directions")
            blocks.append(feedback)
        require((blocks[0] == blocks[1]) == (not closed), "forward blindness versus recombined feedback sensitivity")
    # Explicit one-bit encoded-stage shift/corner, not physical time transport.
    clock_shift, clock_input = [[Z, ONE], [ONE, Z]], [[ONE], [Z]]
    require(mm(transpose(clock_shift), clock_shift) == eye(2), "complete encoded-clock shift retained")
    actual_t = mm(mm(transpose(clock_input), clock_shift), clock_input)[0][0]
    require(actual_t == Z, "advanced encoded clock is orthogonal to the active start")
    used_t = ONE if "--mutation=reset-clock" in sys.argv else actual_t
    clock_feedback = sub(ONE, mul(mul(used_t, used_t), P))
    require(clock_feedback == ONE, "advanced retained clock is not silently reset to the active start")
    return {"new_common_recombiner_forward_letters": 3, "c1": "G_P^-1", "c0": "G_P",
            "full_local_generator_rank": len(high), "nonquery_common_stages": "4+14k plus actual query/control/clock transport",
            "unrecombined_true_feedback": "I-p*R_clk tensor B^4; R_clk=T_clk^*T_clk",
            "recombined_true_feedback": "I-R_clk tensor H^*B^4H",
            "advanced_start_only_clock_feedback": "I", "clock_reset_inferred": False,
            "clock_fixture_is_physical_elapsed_clock_transport": False}


def noncommuting_determinant():
    u2 = eye(2)
    for _ in range(4):
        u2 = transpose([rot(col, 0) for col in transpose(u2)])
    u = [[u2[0][0], u2[0][1], Z], [u2[1][0], u2[1][1], Z], [Z, Z, ONE]]
    pi = [[ONE, Z, Z], [Z, ONE, Z], [Z, Z, Z]]
    f = [[field(Q(1, 2)), field(Q(1, 16)), field(Q(1, 16))],
         [field(Q(1, 16)), field(Q(1, 3)), Z], [field(Q(1, 16)), Z, field(Q(1, 4))]]
    require(mm(f, pi) != mm(pi, f), "noncommuting full-carrier determinant fixture")
    z, g = field(Q(1, 8)), scale(16, power(P, 6))
    h = ma(ms(P, eye(3)), ms(power(P, 2), u))
    require(mm(h, transpose(h)) == ma(eye(3), ms(scale(-1, g), pi)), "native full-generator contraction identity")
    m0 = ma(ms(sub(ONE, z), eye(3)), ms(z, f))
    actual = ma(ms(sub(ONE, z), eye(3)), ms(z, mm(mm(transpose(h), f), h)))
    kernel = mm(f, inverse(m0))
    small = [[sub(ONE if i == j else Z, mul(mul(z, g), kernel[i][j])) for j in range(2)] for i in range(2)]
    require(determinant(actual) == mul(determinant(m0), determinant(small)), "rank-reduced determinant with noncommuting input")
    return {"fixture_DATA_dimension": 3, "projector_rank": 2, "commuting_projector_assumed": False,
            "source_first_derivative": 0, "source_second_derivative": "2*r*z*p^3*Tr(K_reduced)>0 when clock return is nonzero"}


def bound_and_amplitude():
    # Current counting/port central gain has scalar net gap-1, not amplitude gap-1/2.
    actual_probability_ratio = P
    squared_scalar_ratio = power(P, 2)
    require(actual_probability_ratio != squared_scalar_ratio, "scalar gain trial is not the Book amplitude binding")
    if "--mutation=scalar-as-amplitude" in sys.argv:
        require(actual_probability_ratio == squared_scalar_ratio, "literal amplitude route rejects squared scalar port weights")
    lo, hi = Q(3, 5), Q(5, 8)
    for _ in range(80):
        midpoint = (lo + hi) / 2
        if midpoint * midpoint + midpoint < 1:
            lo = midpoint
        else:
            hi = midpoint
    # p^6=5-8p; r=128, rank8, z=2^-20 and B>11/12.
    lower, upper = (Q(14641, 1327104) * (5 - 8 * x) for x in (hi, lo))
    require(0 < lower < upper, "strict original native feedback penalty lower-bound coefficient")
    return {"k1_natural_log_feedback_lower_bound": {"rational_lower": str(lower), "rational_upper": str(upper)},
            "exact_bound": "14641*p^6/1327104 times Tr(R_clk), R_clk=T_clk^*T_clk",
            "continuous_g_window": "0<=g<=4p^3<1", "oldRIGHT_multiplicity": 128,
            "counting_port_gain_difference": 2, "required_absolute_amplitude_gain_difference": "3/2",
            "common_normalizer_repairs_relative_gap": False}


def main():
    print(json.dumps({"status": "PASS", "native_complement": native_complement(),
                      "determinant_transport": noncommuting_determinant(), "bound_and_type": bound_and_amplitude(),
                      "source_sha256": {**{PREFIX + n: h for n, h in N.O.PINS.items()}, **N.PINS, **PINS},
                      "physical_clock_cut_or_full_Book_selected": False, "new_primary_spectral_replay": False}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
