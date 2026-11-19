"""Exact 406-gate positive-support coarse detector and retained stopping tree."""
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path

import numpy as np
import sympy as sp


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def b165_owner():
    path = Path(__file__).resolve().parents[1] / "round165" / "check_service_abort.py"
    spec = spec_from_file_location("b165", path)
    arithmetic = module_from_spec(spec)
    spec.loader.exec_module(arithmetic)
    return arithmetic, arithmetic.import_owner(Path(__file__).resolve().parents[6])


def exact_native_endpoint(owner, arithmetic):
    gate = owner.native.Gate
    r, s = 6, 7
    extra = (gate("CX", (r, s)), gate("G", (r,)), gate("CX", (s, r)),
             gate("G", (r,)), gate("CX", (s, r)), gate("CX", (r, s)))
    gates = owner.measure_word() + extra
    inventory = Counter(stage.op for stage in gates)
    require(inventory == {"CX": 258, "SourceI": 88, "G": 60}, "406 actual square stages")
    require([j + 1 for j, g in enumerate(gates) if j >= 400 and g.op == "G"] == [402, 404],
            "two new independently addressed rotation slots")

    rows, old = np.arange(256), np.arange(64)
    state = np.zeros((4, 256, 64), dtype=np.int64)
    state[2, 4 * old, old] = 1
    state[3, 4 * old + 1, old] = 1
    state[3, 4 * old + 2, old] = 1
    state[0, 4 * old + 3, old] = 1
    state[2, 4 * old + 3, old] = -1
    context = owner.native.Execution(8, (), (), (), owner.native.G_CX_SOURCE_I, 2, (0, 1))
    source = owner.native.gate_matrix(context, owner.src, max_qubits=8)
    signed = np.asarray(source, dtype=np.int64)
    require(source == sp.Matrix(signed.tolist()) and np.all(np.isin(signed, (-1, 0, 1)))
            and np.all(np.count_nonzero(signed, axis=0) == 1)
            and np.all(np.count_nonzero(signed, axis=1) == 1), "exact signed source action")
    source_input = np.argmax(np.abs(signed), axis=1)
    source_sign = signed[rows, source_input]
    peak = 1

    for stage in gates:
        masks = tuple(1 << (7 - q) for q in stage.wires)
        if stage.op == "CX":
            control, target = masks
            state = state[:, rows ^ np.where((rows & control) != 0, target, 0), :]
        elif stage == owner.src:
            state = state[:, source_input, :] * source_sign[None, :, None]
        else:
            require(stage.op == "G", "literal native gate")
            target, = masks
            require(peak <= 2**60, "integer product fits in signed 64 bits")
            signs = np.where((rows & target) != 0, 1, -1)
            state = (arithmetic.times_a(state)
                     + arithmetic.times_p(state[:, rows ^ target, :]) * signs[None, :, None])
            peak = max(peak, int(np.max(np.abs(state))))

    cosine, sine = np.array([1, 0, 0, 0]), np.array([0, 0, 0, 0])
    for _ in range(16):
        cosine, sine = (arithmetic.times_a(cosine) - arithmetic.times_p(sine),
                        arithmetic.times_p(cosine) + arithmetic.times_a(sine))
    powers = [sine]
    for _ in range(16):
        powers.append(arithmetic.times_a(powers[-1]))
    projected = np.zeros((4, 64, 64), dtype=np.int64)
    for row, col in product(range(64), repeat=2):
        if row // 16 == col // 16:
            degree = 8 + bin(row % 16).count("1") + bin(col % 16).count("1")
            projected[:, row, col] = powers[degree]
    identity = np.eye(64, dtype=np.int64)
    expected = (
        (2 * arithmetic.times_p(cosine) - cosine)[:, None, None] * identity,
        sine[:, None, None] * identity - projected,
        projected,
        (2 * arithmetic.times_a(arithmetic.times_p(cosine)))[:, None, None] * identity,
    )
    for mark, kraus in enumerate(expected):
        require(np.array_equal(state[:, mark::4, :], kraus), f"exact all-column Kraus {mark:02b}")
        require(np.any(kraus), f"nonempty Kraus {mark:02b}")
    return dict(inventory), peak


def independent_inner_angles():
    c1, s1, c2, s2 = sp.symbols("c1 s1 c2 s2")
    a1 = sp.Matrix([[c1, -s1], [s1, c1]])
    a2 = sp.Matrix([[c2, -s2], [s2, c2]])
    eye = sp.eye(4)
    first = eye[:, [0, 1, 3, 2]]
    second = eye[:, [0, 3, 2, 1]]
    total = first * second * sp.kronecker_product(a2, sp.eye(2)) * second * sp.kronecker_product(a1, sp.eye(2)) * first
    cp, sp_ = c1 * c2 - s1 * s2, s1 * c2 + c1 * s2
    cm, sm = c1 * c2 + s1 * s2, s1 * c2 - c1 * s2
    expected = sp.Matrix([[cp, 0, 0, -sp_], [0, cm, -sm, 0],
                          [0, sm, cm, 0], [sp_, 0, 0, cp]])
    require((total - expected).applyfunc(sp.expand) == sp.zeros(4), "separate even and odd rotations")

    t, e = sp.symbols("t e", real=True)
    A, B = 1 - e**2, e**2
    left = A * t / (A * t + B * (1 - t))
    right = B * t / (B * t + A * (1 - t))
    summed = left + right
    require(sp.factor(summed.subs(t, 1 - t) + summed - 2) == 0, "opposite report effects")
    require(sp.diff(summed, e).subs(e, 0) == 0, "zero first derivative of odd mixing")
    return "even=theta1+theta2; odd=theta1-theta2"


def exact_leaf_tree(n, m, weights, field):
    guard0, guard1, report0, report1, retry0, retry1, informative = weights
    one, zero = field.one, field.zero
    cap = (retry0 + retry1)**n
    ell = informative * sum(((retry0 + retry1)**j for j in range(n)), zero)
    old_report_weights = report0, report1
    leaves = Counter()
    constant, slope = zero, zero

    def terminates(kind, weight, report):
        nonlocal constant, slope
        leaves[kind] += 1
        if kind == "success":
            constant += weight
        if kind in ("guard", "service"):
            constant += weight if report == 0 else zero
            slope += weight if report == 1 else -weight

    def attempts(attempt, depth, report, prior):
        for retry in (retry0, retry1):
            branch = prior * retry
            if attempt + 1 == n:
                terminates("service", branch, report)
            else:
                attempts(attempt + 1, depth, report, branch)
        terminates("success", prior * informative, report)
        if depth == m:
            terminates("overflow", prior * informative, report)
        else:
            run_cycle(depth + 1, prior * informative)

    def run_cycle(depth, prior):
        for report, weight in enumerate(old_report_weights):
            terminates("guard", prior * weight * guard0, report)
            attempts(0, depth, report, prior * weight * guard1)

    run_cycle(0, one)
    raw = 2 * (2**n - 1)
    visits = sum(raw**j for j in range(m + 1))
    require(dict(leaves) == {"guard": 2 * visits, "service": (2**(n + 1)) * visits,
                            "success": raw * visits, "overflow": raw**(m + 1)}, "retained tree count")
    w = report0 + report1
    total_cont = guard1 * ell * w
    carried = sum((total_cont**j for j in range(m + 1)), zero)
    coefficient = guard0 + guard1 * cap
    require(slope == carried * coefficient * (report1 - report0), "exact report slope")
    require(constant == carried * (total_cont + coefficient * report0), "exact cold baseline")
    return sum(leaves.values())


def main():
    arithmetic, owner = b165_owner()
    inventory, peak = exact_native_endpoint(owner, arithmetic)
    inner_angles = independent_inner_angles()
    p_exact = (sp.sqrt(5) - 1) / 2
    field = sp.QQ.algebraic_field(p_exact)
    p = field.convert(p_exact)
    require(p**2 + p**4 + 2 * p**3 == field.one, "unprinted per-attempt passive normalization")
    unprinted = p, p**2, p, p**2, p**2, p**4, p**3
    printed = p**4, p**7, p**4, p**7, p**8, p**14, p**11
    total = 0
    for weights, n, m in product((unprinted, printed), (1, 2, 3), (0, 1, 2)):
        total = max(total, exact_leaf_tree(n, m, weights, field))
    info = {
        "status": "PASS",
        "A80_commit": arithmetic.A80_PIN,
        "B167_commit": "82e2486f6",
        "native_gate_inventory": inventory,
        "native_exact_old_columns": 64,
        "native_exact_output_rows": 256,
        "peak_exact_integer_coefficient": peak,
        "two_added_G_stages": [402, 404],
        "independent_angles": inner_angles,
        "born_transparent_total": "cos(beta)^2",
        "unprinted_transparent_passive_sum": "p^2+p^4",
        "printed_transparent_passive_sum": "p^8+p^14",
        "exact_guarded_stopped_trees": 18,
        "largest_explicit_terminal_count": total,
        "GR_closed": False,
    }
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
