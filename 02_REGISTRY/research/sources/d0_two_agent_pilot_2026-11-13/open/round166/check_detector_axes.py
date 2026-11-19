"""Exact audit of all 58 addressed single-G angle axes of the 400-gate A80 detector."""
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

import numpy as np
import sympy as sp


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_b165():
    path = Path(__file__).resolve().parents[1] / "round165" / "check_service_abort.py"
    spec = spec_from_file_location("b165_detector", path)
    result = module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def audit_angle_axes(owner, arithmetic):
    gates = owner.measure_word()
    require(Counter(gate.op for gate in gates) == {"SourceI": 88, "CX": 254, "G": 58}, "literal A80 word")
    rows, columns = np.arange(256), np.arange(64)
    context = owner.native.Execution(8, (), (), (), owner.native.G_CX_SOURCE_I, 2, (0, 1))
    source = owner.native.gate_matrix(context, owner.src, max_qubits=8)
    signed = np.asarray(source, dtype=np.int64)
    require(source == sp.Matrix(signed.tolist()), "exact SourceI entries")
    require(np.all(np.count_nonzero(signed, axis=0) == 1) and
            np.all(np.count_nonzero(signed, axis=1) == 1) and
            np.all(np.isin(signed, (-1, 0, 1))), "signed permutation")
    source_input = np.argmax(np.abs(signed), axis=1)
    source_sign = signed[rows, source_input]
    port_mask = 1 << (7 - owner.port)
    require(np.array_equal(source_input[source_input], rows) and
            np.array_equal(source_sign * source_sign[source_input],
                           np.where((rows & port_mask) == 0, 1, -1)), "two SourceI realize physical Z")

    def apply(state, gate):
        masks = tuple(1 << (7 - wire) for wire in gate.wires)
        if gate.op == "CX":
            control, target = masks
            return state[:, rows ^ np.where((rows & control) != 0, target, 0), :]
        if gate == owner.src:
            return state[:, source_input, :] * source_sign[None, :, None]
        require(gate.op == "G", "native gate kind")
        target, = masks
        require(np.max(np.abs(state)) <= 2**60, "exact int64 range before G")
        signs = np.where((rows & target) != 0, 1, -1)
        return (arithmetic.times_a(state)
                + arithmetic.times_p(state[:, rows ^ target, :]) * signs[None, :, None])

    def old_output_axis(state, wire):
        mask = 1 << (7 - wire)
        signs = np.where((rows & mask) != 0, 1, -1)
        return state[:, rows ^ mask, :] * signs[None, :, None]

    def old_input_axis(state, wire):
        mask = 1 << (5 - wire)
        signs = np.where((columns & mask) == 0, 1, -1)
        return state[:, :, columns ^ mask] * signs[None, None, :]

    state = np.zeros((4, 256, 64), dtype=np.int64)
    state[2, 4 * columns, columns] = 1
    state[3, 4 * columns + 1, columns] = 1
    state[3, 4 * columns + 2, columns] = 1
    state[0, 4 * columns + 3, columns] = 1
    state[2, 4 * columns + 3, columns] = -1
    prefixes = {}
    for index, gate in enumerate(gates):
        state = apply(state, gate)
        if gate.op == "G":
            prefixes[index] = state
    require(not np.any(state[:, 3::4, :]), "exact dark baseline")

    def support_on_reflected_root(derivative, active_wires):
        dark = derivative[:, 3::4, :]
        # Each reflected root column has 16 entries ±a^(4+popcount(work)).
        # Multiplication by a increases the maximum integer coefficient by
        # at most two. The stated guard covers eight shifts plus sixteen sums.
        require(np.max(np.abs(dark)) <= 2**49, "exact int64 range for root projection")
        rooted = []
        for spin_column in range(4):
            output = np.zeros((4, 64), dtype=np.int64)
            for work in range(16):
                amplitude = dark[:, :, 16 * spin_column + work]
                for _ in range(4 + bin(work).count("1")):
                    amplitude = arithmetic.times_a(amplitude)
                parity = sum((work >> (5 - wire)) & 1 for wire in active_wires)
                output += (-1)**parity * amplitude
            rooted.append(output)
        if not np.any(rooted[0]):
            require(not np.any(rooted), "spin-scalar dark projection")
            return 0
        # Disjoint support and matching coefficient columns give rank four
        # without evaluating any square root numerically.
        for spin_column, output in enumerate(rooted):
            require(not np.any(output[:, :16 * spin_column]) and
                    not np.any(output[:, 16 * (spin_column + 1):]), "old Spin remains separate")
            require(np.array_equal(output[:, 16 * spin_column:16 * (spin_column + 1)],
                                   rooted[0][:, :16]), "same old work column on each Spin")
        return 4

    pre, post, lifts = {}, {}, []
    for index, prefix in prefixes.items():
        wire = gates[index].wires[0]
        delta = old_output_axis(prefix, wire)
        for gate in gates[index + 1:]:
            delta = apply(delta, gate)
        stage = index + 1
        if np.any(delta[:, 3::4, :]):
            require(support_on_reflected_root(delta, (2, 4)) == 4, "rank four on first NPS2")
            require(support_on_reflected_root(delta, (2, 3, 4)) == 4, "rank four on second NPS2")
            lifts.append(stage)
            continue
        if wire in range(2, 6) and np.array_equal(delta, old_output_axis(state, wire)):
            post[stage] = wire
            continue
        pre_wires = [j for j in range(2, 6) if np.array_equal(delta, -old_input_axis(state, j))]
        require(len(pre_wires) == 1, "finite dark input rotation")
        pre[stage] = pre_wires[0]
    require(pre == {3: 2, 11: 3, 22: 4, 33: 5}, "four exact basis-input rotations")
    require(post == {397: 2, 398: 3, 399: 4, 400: 5}, "four exact outcome-output rotations")
    require(len(lifts) == 50, "every other angle opens the dark branch")
    return pre, post, lifts


def exact_rotation_checks():
    p_exact = (sp.sqrt(5) - 1) / 2
    field = sp.QQ.algebraic_field(sp.sqrt(p_exact))
    a = field.convert(sp.sqrt(p_exact))
    p, one = a * a, field.one
    d, sin_twice = p**3, 2 * a * p
    require(a * a - p * p == d, "cosine of twice the native angle")

    def mul(left, right):
        return tuple(tuple(sum((left[j][k] * right[k][i] for k in range(2)), field.zero)
                           for i in range(2)) for j in range(2))

    z = ((one, field.zero), (field.zero, -one))
    g = ((a, -p), (p, a))
    g_squared = mul(g, g)
    forward = mul(g_squared, mul(z, z))
    backward = mul(z, mul(g_squared, z))
    require(mul(forward, backward) == ((one, field.zero), (field.zero, one)),
            "positive equal-inventory rotations are exact inverses")
    results = {}
    for active_count in (2, 3):
        cosine = d**active_count
        matrix_element = sin_twice * d**(active_count - 1)
        variations = []
        cold_values = []
        for direction, rotation in ((1, forward), (-1, backward)):
            require(rotation[0][0] == d and rotation[1][0] == direction * sin_twice,
                    "actual fixed-word angle")
            abort = cosine * rotation[0][0] + matrix_element * rotation[1][0]
            ordinary = p**3 * (
                rotation[0][0]**2
                + (matrix_element * rotation[1][0])**2 / (one - cosine**2)
            )
            cold_values.append(ordinary + p**2 * abort**2)
            variations.append(2 * p**2 * cosine * matrix_element)
        diff = cold_values[0] - cold_values[1]
        require(diff == 16 * p**5 * d**(2 * active_count), "exact cold contrast")
        results[str(active_count)] = {
            "positive_angle_cold_derivative": float(field.to_sympy(variations[0]).evalf(20)),
            "signed_finite_cold_contrast": float(field.to_sympy(diff).evalf(20)),
        }
    return results


def main():
    repo = Path(__file__).resolve().parents[6]
    arithmetic = load_b165()
    owner = arithmetic.import_owner(repo)
    pre, post, lifts = audit_angle_axes(owner, arithmetic)
    result = {
        "status": "PASS",
        "A80_commit": arithmetic.A80_PIN,
        "B165_commit": "c1fb65623",
        "PR334_commit": arithmetic.PR334_PIN,
        "native_A80_operations": 400,
        "native_single_G_angles": 58,
        "exact_old_input_columns": 64,
        "exact_output_rows": 256,
        "dark_exact_input_pre_rotation": pre,
        "dark_exact_effect_preserving_output_post_rotation": post,
        "dark_lifting_G_stages": lifts,
        "new_dark_leaf_rank_on_either_NPS2_for_each_lifting_axis": 4,
        "passive_dark_leaf_weight": "p^4",
        "lower_bound_on_J_jump": "-4 ln(1-z+z*p^4)",
        "finite_comparison_extra_native_inventory_per_word": {"G": 2, "SourceI": 4},
        "finite_contrast_formula": "16*p^5*(p^3)^(2*s)",
        "m_zero_N_one_reflection_checks": exact_rotation_checks(),
        "full_physical_Cost_minus_Info_identified": False,
        "GR_closed": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
