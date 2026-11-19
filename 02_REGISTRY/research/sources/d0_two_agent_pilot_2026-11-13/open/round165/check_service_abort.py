"""Audit A80's native detector and the kept-service-abort RC3 on the exact leaf tree."""
from collections import Counter
from fractions import Fraction as Fr
from hashlib import sha256
import importlib.util
from itertools import combinations
from pathlib import Path
from sys import argv
import json

import numpy as np
import sympy as sp

A80_PIN = "2b59138c88987a2159474b3f167ab755f83ddb74"
PR334_PIN = "65753c972b4ad1e528a29b0343e30c3ecc9b9670"
A80_DETECTOR_SHA = "fdc0d988a48073b862f92dbe1e3f945f529c32fb3e907421c2f611dbcdea739c"


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def import_owner(repo):
    relative = (
        "02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13"
        "/direct/round80/native/check_return_work.py"
    )
    path = repo / relative
    require(sha256(path.read_bytes()).hexdigest() == A80_DETECTOR_SHA, "pinned A80 detector")
    spec = importlib.util.spec_from_file_location("a80_return_work", path)
    owner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owner)
    return owner


def times_a(state):
    x0, x1, x2, x3 = state
    return np.stack((x3, x0, x1-x3, x2))


def times_p(state):
    x0, x1, x2, x3 = state
    return np.stack((x2, x3, x0-x2, x1-x3))


def verify_exact_detector(owner):
    # Coefficients in Z[a] with a^4=1-a^2. The four components here
    # are ordered by powers 0,1,2,3 and p=a^2.
    rows, old = np.arange(256), np.arange(64)
    state = np.zeros((4,256,64), dtype=np.int64)
    state[2,4*old,old] = 1
    state[3,4*old+1,old] = 1
    state[3,4*old+2,old] = 1
    state[0,4*old+3,old] = 1
    state[2,4*old+3,old] = -1

    context = owner.native.Execution(8, (), (), (), owner.native.G_CX_SOURCE_I, 2, (0,1))
    algebraic_source = owner.native.gate_matrix(context, owner.src, max_qubits=8)
    integer_source = np.asarray(algebraic_source,dtype=np.int64)
    if (algebraic_source != sp.Matrix(integer_source.tolist())
            or not np.all(np.isin(integer_source,(-1,0,1)))
            or not np.all(np.count_nonzero(integer_source,axis=0)==1)
            or not np.all(np.count_nonzero(integer_source,axis=1)==1)):
        raise ArithmeticError("invalid signed SourceI permutation")
    source_input = np.argmax(np.abs(integer_source),axis=1)
    source_sign = integer_source[rows,source_input]

    maximum = 1
    for gate in owner.measure_word():
        masks = tuple(1 << (7-wire) for wire in gate.wires)
        if gate.op == "CX":
            control,target = masks
            state = state[:,rows ^ np.where((rows&control)!=0,target,0),:]
        elif gate.op == "G":
            target, = masks
            if maximum > 2**60:
                raise ArithmeticError("no exact int64 bound for the next rotation")
            signs = np.where((rows&target)!=0,1,-1)
            state = times_a(state) + times_p(state[:,rows^target,:])*signs[None,:,None]
            maximum = max(maximum,int(np.max(np.abs(state))))
        elif gate == owner.src:
            state = state[:,source_input,:]*source_sign[None,:,None]
        else:
            raise ArithmeticError("unexpected literal gate")

    cosine,sine = np.array([1,0,0,0]),np.array([0,0,0,0])
    for _ in range(16):
        cosine,sine = times_a(cosine)-times_p(sine),times_p(cosine)+times_a(sine)
    coeffs = [sine]
    for _ in range(16):
        coeffs.append(times_a(coeffs[-1]))
    projection = np.zeros((4,64,64),dtype=np.int64)
    for row in range(64):
        for column in range(64):
            if row//16 == column//16:
                degree = 8 + bin(row%16).count("1") + bin(column%16).count("1")
                projection[:,row,column] = coeffs[degree]
    identity = np.eye(64,dtype=np.int64)
    expected = (cosine[:,None,None]*identity, sine[:,None,None]*identity-projection,
                projection,np.zeros_like(projection))
    for mark,kraus in enumerate(expected):
        if not np.array_equal(state[:,mark::4,:],kraus):
            raise ArithmeticError(f"exact endpoint mismatch on mark {mark}")
    return maximum


def check_exact_tree(field, golden_p, service_failure, outer_cap, service_cap, pair):
    cosine, sine = pair
    require(cosine * cosine + sine * sine == 1, "old two-plane reflection")
    u = cosine * cosine
    q = (1 - cosine) / 2
    p_no_service = service_failure**service_cap
    one = field.one
    mark_mass = {"00": golden_p**2, "10": golden_p**3, "01": golden_p**3}
    leaves = []

    def scalar(x):
        return field.convert(sp.Rational(x.numerator, x.denominator))

    def reflection(vec):
        return cosine * vec[0] + sine * vec[1], sine * vec[0] - cosine * vec[1]

    def measure(vec, passive_weight, actual_scale, outer_index, service_index):
        # The 00 event has a nonzero scalar Kraus and leaves the old vector
        # unchanged. The two informative answers project onto old P or B.
        next_weight = passive_weight * mark_mass["00"]
        next_scale = actual_scale * service_failure
        if service_index + 1 == service_cap:
            leaves.append(("service_abort", vec, next_weight, next_scale))
        else:
            measure(vec, next_weight, next_scale, outer_index, service_index + 1)
        yes = (vec[0], Fr(0))
        no = (Fr(0), vec[1])
        leaves.append(("success", yes, passive_weight * mark_mass["10"],
                       actual_scale * (one - service_failure)))
        if outer_index + 1 == outer_cap:
            leaves.append(("outer_abort", no, passive_weight * mark_mass["01"],
                           actual_scale * (one - service_failure)))
        else:
            measure(reflection(no), passive_weight * mark_mass["01"],
                    actual_scale * (one - service_failure), outer_index + 1, 0)

    measure(reflection((Fr(1), Fr(0))), one, one, 0, 0)
    h_sum = field.zero
    all_born = field.zero
    total_fail = field.zero
    counts = Counter()
    for kind, vec, passive_weight, actual_scale in leaves:
        counts[kind] += 1
        total = vec[0] ** 2 + vec[1] ** 2
        require(total > 0, "fixed legal leaf rank")
        h_sum += passive_weight * scalar(vec[0] ** 2 / total)
        born = actual_scale * scalar(total)
        all_born += born
        if kind != "success":
            total_fail += born

    a = golden_p ** (2 * service_cap)
    ell = golden_p**2 * (one - a)
    later = sum((ell**j for j in range(1, outer_cap)), field.zero)
    h_formula = ell * (one + later) + a * (scalar(u) + scalar(1 - u) * later)
    require(h_sum == h_formula, "exact full RC3 occupied subspaces")
    require(all_born == one, "exact full Born normalization")
    expect_count = {
        "success": sum(service_cap**j for j in range(1, outer_cap + 1)),
        "service_abort": sum(service_cap**j for j in range(outer_cap)),
        "outer_abort": service_cap**outer_cap,
    }
    require(dict(counts) == expect_count, "full retained leaf ranks")

    w = (one - p_no_service) * scalar(u)
    expected_fail = (
        p_no_service
        + p_no_service * (one - p_no_service) * scalar(1 - u)
        * sum((w**j for j in range(outer_cap - 1)), field.zero)
        + (one - p_no_service)**outer_cap * scalar((1 - u) * u**(outer_cap - 1))
    )
    require(expected_fail == total_fail, "exact service and outer failure probability")
    return q, h_sum, a * (one - later)


def certified_service_recovery_ratio():
    p_lower = Fr(6180339887498948482, 10**19)
    p_upper = Fr(6180339887498948483, 10**19)
    require(p_lower + p_lower**2 < 1 < p_upper + p_upper**2, "rational Golden bracket")

    def square_interval(lower, upper):
        endpoints = lower * lower, upper * upper
        return (min(endpoints) if lower * upper > 0 else Fr(0)), max(endpoints)

    # cos(2 theta)=2p-1; three doublings give cos(16 theta).
    lo, hi = 2 * p_lower - 1, 2 * p_upper - 1
    for _ in range(3):
        lo, hi = square_interval(lo, hi)
        lo, hi = 2 * lo - 1, 2 * hi - 1
    lo, hi = square_interval(lo, hi)
    ratio = lo / p_upper**2, hi / p_lower**2
    require(Fr(28419, 100000) < ratio[0] < ratio[1] < Fr(28420, 100000), "strict native ratio enclosure")
    return tuple(float(endpoint) for endpoint in ratio)


def verify_operator_and_independent_variations():
    eye = sp.eye(6)
    root, failure = eye[:, :2], eye[:, 2:4]
    old_cut = root * root.T
    failure_cut = failure * failure.T
    complement = eye - old_cut
    cosine = sp.diag(sp.Rational(7, 25), sp.Rational(5, 13))
    sine = sp.diag(sp.Rational(24, 25), sp.Rational(12, 13))
    reflection = sp.diag(cosine.row_join(sine).col_join(sine.row_join(-cosine)), -sp.eye(2))
    require(reflection.T == reflection and reflection**2 == eye, "nonscalar reflection")
    require((complement - failure_cut) * reflection * root == sp.zeros(6, 2), "zero occupied-range defect")

    def occupied_cold(columns):
        compressed = root.T * columns
        return compressed * (columns.T * columns).inv() * compressed.T

    require(occupied_cold(reflection * root) == cosine**2, "first service abort range")
    require(occupied_cold(reflection * failure) == sp.eye(2) - cosine**2, "late service abort range")
    require(occupied_cold(failure) == sp.zeros(2), "ordinary abort range")
    preceding_failure = root
    for _ in range(5):
        before_measurement = reflection * preceding_failure
        require(occupied_cold(old_cut * before_measurement) == sp.eye(2), "success range")
        preceding_failure = complement * before_measurement

    def skew_basis(lo, hi):
        for row, col in combinations(range(lo, hi), 2):
            basis = sp.zeros(6)
            basis[row, col], basis[col, row] = 1, -1
            yield basis

    for generator in skew_basis(0, 6):
        moved = generator * reflection
        dcosine = root.T * moved * root
        predicted = dcosine * cosine.T + cosine * dcosine.T
        later = root.T * (moved * failure_cut * reflection.T + reflection * failure_cut * moved.T) * root
        require(later == -predicted, "later service abort derivative at fixed incoming range")
    for generator in skew_basis(2, 6):
        moved_range = generator * failure_cut - failure_cut * generator
        later = root.T * reflection * moved_range * reflection.T * root
        require(later == sp.zeros(2), "earlier variation of the incoming occupied range")
    return 21


def main(repo):
    g = (sp.sqrt(5) - 1) / 2
    field = sp.QQ.algebraic_field(sp.sqrt(g))
    a = field.convert(sp.sqrt(g))
    p = a * a
    require(p + p * p == field.one, "Golden equality")
    owner = import_owner(repo)
    inventory = Counter(gate.op for gate in owner.measure_word())
    require(inventory == {"CX": 254, "SourceI": 88, "G": 58}, "actual 400-gate detector")
    peak = verify_exact_detector(owner)
    cosine, sine = field.one, field.zero
    for _ in range(16):
        cosine, sine = a * cosine - p * sine, p * cosine + a * sine
    service_failure = cosine * cosine
    require(cosine * cosine + sine * sine == field.one, "native detector normalization")
    exact_tangents = verify_operator_and_independent_variations()

    # All comparison formulas are exact in Q(sqrt(p)); use 65 digit displays
    # only for explanatory magnitudes. The analytical sign inequalities are
    # derived from p²<1/2 and ell/(1-ell) <= p.
    r = field.to_sympy(service_failure / (p * p))
    ratio = float(r.evalf(65))
    ratio_bounds = certified_service_recovery_ratio()
    require(ratio_bounds[0] <= ratio <= ratio_bounds[1], "exact field ratio replay")
    cases = 0
    for n in range(1, 5):
        for m in range(0, 5):
            prev_q = None
            prev_h = None
            slope = None
            for pair in ((Fr(7, 25), Fr(24, 25)), (Fr(5, 13), Fr(12, 13))):
                q, h, du = check_exact_tree(field, p, service_failure, m + 1, n, pair)
                require(float(field.to_sympy(du).evalf(65)) > 0, "signed h response")
                if prev_q is not None:
                    u = (1 - 2 * q)**2
                    prev_u = (1 - 2 * prev_q)**2
                    delta = field.convert(sp.Rational((u - prev_u).numerator, (u - prev_u).denominator))
                    require(du == slope and (h - prev_h) / delta == du, "exact cold secant")
                prev_q, prev_h, slope = q, h, du
                cases += 1

    print(json.dumps({
        "status": "PASS",
        "A80_commit": A80_PIN,
        "PR334_commit": PR334_PIN,
        "A80_detector_sha256": A80_DETECTOR_SHA,
        "native_gate_inventory": dict(inventory),
        "exact_native_input_columns": 64,
        "exact_native_output_rows": 256,
        "peak_exact_integer_gate_coefficient": peak,
        "exact_stopped_trees": cases,
        "exact_nonscalar_tangent_directions": exact_tangents,
        "enumeration_q_samples": [str((1 - Fr(5, 13)) / 2), str((1 - Fr(7, 25)) / 2)],
        "native_service_failure_ratio_to_p_squared": ratio,
        "native_service_failure_ratio_rounded_enclosure": [0.28419, 0.28420],
        "graph_history_APPLICABILITY": "fixed old root, actual retained pointer marks, fixed closure and heat budget",
        "microscopic_path_Cost_minus_Info_identified": False,
        "GR_closed": False
    }, indent=2))


if __name__ == "__main__":
    main(Path(argv[1] if len(argv) > 1 else ".").resolve())
