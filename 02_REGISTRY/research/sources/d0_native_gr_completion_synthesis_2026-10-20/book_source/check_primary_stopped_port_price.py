#!/usr/bin/env python3
"""Compose the actual cap2 port ledger and nonlinear preparation equation.

Exact saved-dyadic interval composition, formal noncommuting operator jet,
complete supplied reference and an exact nonlinear RIGHT fixture. No old
suite, numerical matrix, eigensolver or physical Info selection is run.
"""
import ast
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    PREFIX + "check_native_car_actuated_metric.py": "72b2743f2f4c9408ceafe29dc691786c5011c4d1133d5fa6ebdb671a230bc3fa",
    PREFIX + "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json": "3fc747be8d27a7b581cfa7a2e9b58da5ff87058a4e3b76199dd2e9483a674b6a",
    PREFIX + "PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_CERTIFICATE.json": "9c910c2e28d02af5fd3a8642d98d01b8c58aeb0a9a55ccf3612a5bc80e397785",
    PREFIX + "NATIVE_COHERENT_CHOICE_SOURCE.md": "2e906213861d0c4d1812e1ec8608aec571aeb18230fce8f791fb4cce6b4c2c1b",
    PREFIX + "PRIMARY_RIGHT_COMPLETE_CODE_SOURCE.md": "7a38155f37b98fabdd358271be52ad4919a0b28963a5fb952d91da049eba4424",
    PREFIX + "BOOK_SOURCE_BINDING.md": "2b26bf2f4c1b128731ccf14a17437ba654c046e82b5e42e55113a8b6053494ea",
    "02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md": "75845813d20ecf7b585fb7b7a7bef8b8170a711e94a56bb0df0cc3546622a036",
}


def require(value, message):
    if not value:
        raise RuntimeError(message)


for path, digest in PINS.items():
    require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
            "immutable port-price input: " + path)
source = ast.parse((ROOT / next(iter(PINS))).read_text(encoding="utf8"))
names = {"add", "scale", "sub", "mul", "power"}
nodes = [n for n in source.body if
         (isinstance(n, ast.FunctionDef) and n.name in names)
         or (isinstance(n, ast.Assign) and len(n.targets) == 1
             and isinstance(n.targets[0], ast.Name) and n.targets[0].id in {"Z", "O", "A", "P"})]
owned = {"F": Q}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "pinned_field_definitions", "exec"), owned)
Z, ONE, P = (owned[n] for n in ("Z", "O", "P"))
add, scale, sub, mul, power = (owned[n] for n in ("add", "scale", "sub", "mul", "power"))


def poly_add(left, right):
    result = dict(left)
    for word, value in right.items():
        result[word] = add(result.get(word, Z), value)
    return {w: v for w, v in result.items() if v != Z}


def poly_mul(left, right):
    result = {}
    for w, a in left.items():
        for v, b in right.items():
            result = poly_add(result, {w + v: mul(a, b)})
    return result


def derivative(poly):
    result = {}
    for word, value in poly.items():
        for j, letter in enumerate(word):
            if letter == "X":
                result = poly_add(result, {word[:j] + ("Y",) + word[j + 1:]: value})
    return result


def operator_and_reference():
    identity = {(): ONE}
    blank = {(): ONE, ("X",): scale(Q(-1, 2), ONE)}
    cost = {(): ONE, ("X",): P}
    c2 = poly_add(cost, poly_mul(poly_mul(blank, cost), blank))
    expected = {(): scale(2, ONE), ("X",): sub(scale(2, P), ONE),
                ("X", "X"): sub(scale(Q(1, 4), ONE), P),
                ("X", "X", "X"): scale(Q(1, 4), P)}
    require(c2 == expected, "actual whole-operator cap2 port polynomial")
    direct_jet = poly_add(derivative(cost), poly_add(
        poly_mul(poly_mul(derivative(blank), cost), blank), poly_add(
            poly_mul(poly_mul(blank, derivative(cost)), blank),
            poly_mul(poly_mul(blank, cost), derivative(blank)))))
    require(direct_jet == derivative(expected), "ordered noncommuting full cost jet")
    require(("Y", "X") in direct_jet and ("X", "Y") in direct_jet,
            "field/source derivative does not commute X with its jet")
    # One specifically SUPPLIED reference, not an inferred native prior.
    denominator = 1 if "--mutation=drop-reference-labels" in sys.argv else 64
    reference = [scale(Q(1, denominator), power(P, 1 + b)) for k in range(64) for b in range(2)]
    total = Z
    for value in reference:
        total = add(total, value)
    require(total == ONE, "complete128 supplied reference retains all64 labels")
    stopped = [(1, 1 + b, mu) for j, (b, mu) in enumerate(
        (b, reference[2 * k + b]) for k in range(64) for b in range(2)) if j != 0]
    stopped += [(2, 2 + b, mul(reference[0], reference[2 * k + b]))
                for k in range(64) for b in range(2)]
    total = Z
    for rounds, payment, mu in stopped:
        total = add(total, mu)
        require(scale(64 ** rounds, mu) == power(P, payment), "actual prefix code retains round capacity")
    require(total == ONE and len(stopped) == 255, "complete cap2 prefix reference includes abort and dark leaves")
    return {"cap2_polynomial": "2I+(2p-1)X+(1/4-p)X^2+(p/4)X^3; X=epsilon*Delta",
            "noncommuting_jet_checked": True, "reference_declared_leaves": len(stopped),
            "reference_physically_selected": False,
            "actual_port_minus_full_gain": "A_coh-log_phi2-log_phi64*ET"}


def ia(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[1], -a[0]


def im(a, b):
    products = [x * y for x in a for y in b]
    return min(products), max(products)


def iq(value):
    return Q(value), Q(value)


def saved(value):
    return tuple(Q.from_float(x) for x in value)


def overlap(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def display(value):
    def dec(q, upper=False):
        unit = 10 ** 30
        number = -((-q.numerator * unit) // q.denominator) if upper else q.numerator * unit // q.denominator
        return ("-" if number < 0 else "") + str(abs(number) // unit) + "." + str(abs(number) % unit).zfill(30)
    lower, upper = dec(value[0]), dec(value[1], True)
    require(Q(lower) <= value[0] <= value[1] <= Q(upper), "outward displayed exact rational interval")
    return {"rational": [str(x) for x in value], "decimal": [lower, upper]}


def source_composition():
    first = json.loads((ROOT / (PREFIX + "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json")).read_bytes())
    second = json.loads((ROOT / (PREFIX + "PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_CERTIFICATE.json")).read_bytes())
    lo, hi = Q(3, 5), Q(5, 8)
    for _ in range(80):
        midpoint = (lo + hi) / 2
        if midpoint * midpoint + midpoint < 1:
            lo = midpoint
        else:
            hi = midpoint
    p, weight = (lo, hi), (1 - hi, 1 - lo)
    cases = second["new_spectral_certificates"]
    require(len(cases) == 33 and cases[0]["physical_index"] == 0
            and cases[0]["leaf_type"] == "abort_B_squared"
            and cases[1]["physical_index"] == 1
            and all(d["paired_port_zero_by_p"] and d["physical_index"] % 2 == 1 for d in cases[2:]),
            "original distinct-leaf port dictionary")
    c1 = saved(first["linear_coefficients"]["known_port_cost"])
    rb = saved(first["spectral_certificates"][0]["trace_jet"])
    ra, rs = (saved(d["trace_jet"]) for d in cases[:2])
    pair = iq(0)
    for case in cases[2:]:
        pair = ia(pair, saved(case["trace_jet"]))
    mass = ia(ia(ra, rs), im(ia(iq(1), p), pair))
    require(overlap(mass, rb), "second-round complete mass source equals actual incoming blank source")
    cost_pair = ia(iq(2), p)
    if "--mutation=equal-pair-prices" in sys.argv:
        cost_pair = im(iq(2), ia(iq(1), p))
    abort = iq(0) if "--mutation=drop-abort" in sys.argv else ra
    occupation = ia(c1, ia(abort, ia(im(iq(2), rs), im(cost_pair, pair))))
    if "--mutation=reset-blank" in sys.argv:
        occupation = im(iq(2), c1)
    port_only = ia(c1, ia(rb, ia(rs, pair)))
    full_leaves = ia(ia(c1, neg(rb)), ia(im(iq(2), ra),
                     ia(im(iq(3), rs), im(ia(iq(3), im(iq(2), p)), pair))))
    require(overlap(occupation, port_only) and overlap(occupation, full_leaves),
            "actual stopped cost agrees with independent port-only and full-leaf ledgers")
    c2 = (max(occupation[0], port_only[0], full_leaves[0]),
          min(occupation[1], port_only[1], full_leaves[1]))
    require(c2[0] <= c2[1] < 0, "actual complete cap2 port source strictly decreases")
    a2 = saved(second["linear_coefficients"]["conditional_entropy_cap2"])
    require(rb[0] > 0 and ra[0] > 0 and a2[1] < 0, "retained entropy/clock/abort signs")
    # phi^8<64<phi^9, verified using positive p bracket and phi=1+p.
    phi = ia(iq(1), p)
    def ipow(x, n):
        result = iq(1)
        for _ in range(n):
            result = im(result, x)
        return result
    require(ipow(phi, 8)[1] < 64 < ipow(phi, 9)[0], "strict8<log_phi64<9")
    trial = im(weight, ia(a2, neg(im((Q(8), Q(9)), rb))))
    require(trial[1] < 0, "actual port/full-gain source decreases for the supplied counting reference")
    ratio = im(neg(c2), (1 / ra[1], 1 / ra[0]))
    return {"single_arm_cap2_port_cost": display(c2), "coherent_cap2_port_cost": display(im(weight, c2)),
            "independent_cost_ledgers_intersect": True, "abort_multiplier_port_only": display(ratio),
            "coherent_expected_rounds_source": display(im(weight, rb)),
            "coherent_supplied_reference_price_source": display(trial),
            "supplied_reference_source_formula": "p^2*(a2-log_phi64*r_blank)",
            "port_cost_added_again_to_matched_entropy": False}


def nonlinear_fixture():
    # Formal vector coordinates: 1, log_phi2, log_phi3.
    def va(a, b):
        return tuple(x + y for x, y in zip(a, b))
    def vs(k, a):
        return tuple(Q(k) * x for x in a)
    zero = (Q(0),) * 3
    def mm(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
    def tr(a):
        return list(map(list, zip(*a)))
    e0 = [[Q(3, 4), Q(0), Q(1, 8)], [Q(0), Q(1, 4), Q(1, 8)], [Q(1, 8), Q(1, 8), Q(1, 2)]]
    e1 = [[Q(i == j) - e0[i][j] for j in range(3)] for i in range(3)]
    for e in (e0, e1):
        require(all(e[i][i] > sum(abs(e[i][j]) for j in range(3) if i != j) for i in range(3)), "actual positive complete fixture effects")
    c, dc = [[Q(1), Q(0)], [Q(0), Q(1)], [Q(0), Q(0)]], [[Q(0), Q(0)], [Q(0), Q(0)], [Q(1), Q(-1)]]
    require(mm(tr(c), dc) == [[0, 0], [0, 0]], "actual fixed-oldRIGHT Stiefel tangent")
    direct, gradient = zero, zero
    for j, e in enumerate((e0, e1)):
        b = [[x / 2 for x in row] for row in mm(mm(tr(c), e), c)]
        cross = mm(mm(tr(dc), e), c)
        jet = [[(cross[i][k] + cross[k][i]) / 2 for k in range(2)] for i in range(2)]
        require(sum(jet[i][i] for i in range(2)) == 0, "all classical leaf probability sources vanish")
        logs = [(Q(0), Q(-3), Q(b[i][i] == Q(3, 8))) for i in range(2)]
        ec = mm(e, c)
        for i in range(2):
            direct = va(direct, vs(-jet[i][i], logs[i]))
            mark = va((Q(1 + j), Q(-1), Q(0)), vs(-1, logs[i]))
            for row in range(3):
                gradient = va(gradient, vs(dc[row][i] * ec[row][i], mark))
    if "--mutation=freeze-averaged-Info" in sys.argv:
        gradient = zero
    require(direct == gradient == (Q(0), Q(0), Q(-1, 4)), "nonlinear full-RIGHT source survives zero label-probability sources")
    return {"RIGHT_dimension": 2, "both_label_probability_jets": 0,
            "actual_price_source": "-(1/4)*log_phi3", "frozen_averaged_price_source": 0,
            "correct_stationarity": "(I-r*C*C^*)*Z(C)=0 with actual Info/work derivative retained"}


def main():
    print(json.dumps({"status": "PASS", "operator_and_reference": operator_and_reference(),
                      "actual_source_composition": source_composition(), "nonlinear_preparation": nonlinear_fixture(),
                      "source_sha256": PINS, "new_spectral_replay": False,
                      "physical_Info_reference_or_work_selected": False,
                      "actual_abort_constraint_selected": False}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
