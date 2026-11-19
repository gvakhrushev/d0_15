"""Replay both smooth elliptical DATA ends as one retained natively multiplexed word."""
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
import json
import math
from pathlib import Path
import sys

from mpmath import iv
import numpy as np


def load_owner():
    path = Path(__file__).resolve().parents[2] / "round173" / "car" / "check_car_phase_loader.py"
    spec = spec_from_file_location("b173_car", path)
    owner = module_from_spec(spec)
    sys.modules[spec.name] = owner
    spec.loader.exec_module(owner)
    return owner


def character(mask, address):
    return (-1) ** bin(mask & address).count("1")


def coeffs(angles):
    size = len(angles)
    return [sum(a * character(mask, address) for address, a in enumerate(angles)) / size
            for mask in range(size)]


def phase_plan(owner, loader, first, second, angles, search):
    size = len(angles)
    differences = [j for j in range(4) if ((first ^ second) >> (3 - j)) & 1]
    pivot = differences[0]
    target = loader.car[pivot]
    start_bit = (first >> (3 - pivot)) & 1
    route = tuple(loader.cx(target, loader.car[j]) for j in differences[1:])
    canonical = first
    if start_bit:
        for j in differences[1:]:
            canonical ^= 1 << (3 - j)
    # The CAR mask uses the low three bits, and the J/SITE mask the upper bits.
    car_conditions = [(loader.car[j], (canonical >> (3 - j)) & 1)
                      for j in range(4) if j != pivot]
    expected_car = sum(bit << j for j, (_, bit) in enumerate(car_conditions))
    controls = tuple(wire for wire, _ in car_conditions) + tuple(reversed(loader.site))
    coefficients = coeffs(angles)
    powers = [loader.nearest_power(a, 3, search) for a in coefficients]
    full_masks = 8 * size
    gray = [j ^ (j >> 1) for j in range(full_masks)]
    word = list(route)
    for mask, following in zip(gray, gray[1:] + gray[:1]):
        power = (-1) ** start_bit * character(mask & 7, expected_car) * powers[mask >> 3]
        if power:
            word.extend(loader.balanced(target, power, abs(power)))
        toggle = mask ^ following
        owner.require(toggle > 0 and toggle & (toggle - 1) == 0, "Gray transition")
        word.append(loader.cx(controls[toggle.bit_length() - 1], target))
    word.extend(reversed(route))
    units = [16 * k * loader.theta for k in powers]
    # Reducing coefficients modulo 2π is legal because each character is ±1.
    rounded_angles = [sum(u * character(mask, address) for mask, u in enumerate(units))
                      for address in range(size)]
    error_bound = sum(owner.rotation_error(u, a) for a, u in zip(coefficients, units))
    return tuple(word), rounded_angles, error_bound, powers


def replay_all_sections(owner, loader, word, register_width):
    """Drive every addressed input through the same native runs.

    J and SITE are controls only. Logical X row permutations here are CX blocks,
    while grouping consecutive identical gates only speeds up arithmetic.
    """
    n = 1 << register_width
    rows = np.arange(n)
    matrices = np.broadcast_to(np.eye(n), (1 << len(loader.site), n, n)).copy()
    local_bits = (1 << np.array([register_width - 1 - j for j in range(register_width)]))
    offset = len(loader.site)
    source = np.array(loader.native.SOURCE_I_LOCAL, dtype=float)
    source_index = np.argmax(abs(source), axis=1)
    source_sign = source[np.arange(8), source_index]
    port_mask = int(local_bits[loader.port - offset])
    owner.require(port_mask == 4, "PORT and both Spin bits are the final three wires")
    source_preimage = (rows & ~7) + source_index[rows & 7]
    source_factors = source_sign[rows & 7]
    sections = np.arange(len(matrices))
    for gate, count in word:
        if not count:
            continue
        if gate.op == "CX":
            if count % 2 == 0:
                continue
            control, target = gate.wires
            owner.require(target >= offset, "every J and SITE wire is control-only")
            t = local_bits[target - offset]
            if control < offset:
                active = (sections & (1 << (offset - 1 - control))) != 0
                matrices[active] = matrices[active][:, rows ^ t]
            else:
                c = local_bits[control - offset]
                matrices = matrices[:, rows ^ np.where(rows & c, t, 0)]
        elif gate.op == "SourceI":
            for _ in range(count % 4):
                matrices = matrices[:, source_preimage] * source_factors[None, :, None]
        else:
            owner.require(gate == loader.g_port, "active source-port G")
            angle = math.remainder(count * loader.theta, 2 * math.pi)
            sign = np.where(rows & port_mask, 1, -1)
            matrices = (math.cos(angle) * matrices
                        + math.sin(angle) * sign[None, :, None] * matrices[:, rows ^ port_mask])
    return matrices


def physical_prefix_symbols(owner, loader, full_word):
    new_head = loader.site[0]
    old_q, readout, tail = (loader.width + j for j in range(3))
    # CAR is the actual emitted original vacuum/SITE/Fourier carrier, not blank.
    blank = (new_head, tail)
    nc1 = (loader.cx(new_head, tail), (loader.native.Gate("G", (tail,)), 1),
           loader.cx(new_head, tail))
    runs = full_word + nc1
    literal = loader.literal_word(runs)
    native = loader.native
    code = native.Execution(loader.width + 3, blank, (old_q, readout), literal,
                            native.G_CX_SOURCE_I, loader.port, loader.spin)
    native.validate_execution(code, max_qubits=code.qubits, max_expanded_stages=len(literal))
    owner.require(not any(old_q in g.wires or readout in g.wires for g in literal),
                  "the old q and READOUT factors are protected")
    # Raw Execution is the complete square-gate word. The actual separate NC1
    # physical measurement is computed below, not inferred from report metadata.
    return dict(Counter(g.op for g in literal))


def nc1_actual_projectors(owner, p, theta):
    v = np.array([math.sqrt(p), p])
    native_G = np.array([[math.cos(theta), -math.sin(theta)],
                         [math.sin(theta), math.cos(theta)]])
    X = np.array([[0, 1], [1, 0]])
    zeroed = owner.compose(X, native_G, X) @ v
    owner.require(np.max(np.abs(zeroed - np.array([1, 0]))) < 2e-15, "born tail is cleared at J=1")
    prepared = np.r_[v[0] * (native_G @ v), v[1] * zeroed]
    # Head 0 keeps both tail directions. Head 1 actually reads its tail.
    projectors = (np.diag([1, 1, 0, 0]), np.diag([0, 0, 1, 0]), np.diag([0, 0, 0, 1]))
    squared_norms = [float(np.linalg.norm(P @ prepared) ** 2) for P in projectors]
    owner.require(max(abs(x - y) for x, y in zip(squared_norms, (p, p * p, 0))) < 2e-15,
                  "NC1 positive events and retained dark 11")
    return squared_norms



def certify_native_material_jet(owner, L, anchor, powers_x, powers_y):
    """Outward intervals from exact native integer powers, on the actual vacuum."""
    iv.dps = 65
    p = (iv.sqrt(5) - 1) / 2
    a = iv.sqrt(p)

    def mul(left, right):
        x, y = left
        u, v = right
        return x * u - y * v, x * v + y * u

    def rot(power):
        result = (iv.mpf(1), iv.mpf(0))
        base = (a, p if power >= 0 else -p)
        power = abs(power)
        while power:
            if power & 1:
                result = mul(result, base)
            power >>= 1
            if power:
                base = mul(base, base)
        return result

    def apply(state, i, j, power):
        c, s = rot(power)
        u, v = state[i], state[j]
        state[i], state[j] = c * u - s * v, s * u + c * v

    values = []
    for section in range(2 * L):
        dyn_x = 16 * sum(k * character(mask, section) for mask, k in enumerate(powers_x))
        dyn_y = 16 * sum(k * character(mask, section) for mask, k in enumerate(powers_y))
        state = {0: iv.mpf(0), 1: a, 14: p, 15: iv.mpf(0)}
        apply(state, 1, 14, -16 * anchor)
        apply(state, 14, 0, -dyn_x)
        apply(state, 14, 15, -dyn_y)
        apply(state, 1, 14, 16 * anchor)
        apply(state, 14, 15, dyn_y)
        apply(state, 14, 0, dyn_x)
        values.append(tuple(state[j] * state[1] / a for j in (0, 15)))

    def edge_energy(j, n):
        start = values[j * L + n]
        end = values[j * L + (n + 1) % L]
        return L**2 * sum((y - x)**2 for x, y in zip(start, end))

    # L=8: expected cos(4*pi*(n+1/2)/L) signs (+,-,-,+) repeated.
    margin = iv.mpf(1) / 1000
    for n in range(L):
        sign = 1 if n % 4 in (1, 2) else -1
        secant = 4 * (edge_energy(1, n) - edge_energy(0, n))
        owner.require((sign * secant).a > margin, "strict certified edge source on native material")
    return "1/1000"


def main():
    owner = load_owner()
    L = 8
    loader = owner.NativeLoader(owner.native_owner(), 1 + int(math.log2(L)))
    p, theta = loader.p, loader.theta
    H = 1 / L
    sigma = 1 / 64
    amplitude = H * math.sqrt(sigma) / (2 * math.sin(math.pi * H))
    center, step = 1 / 2, 1 / 8
    times = (center - step, center + step)
    psi = np.array([[amplitude * math.sqrt(1 + t) * math.cos(2 * math.pi * n / L),
                     amplitude * math.sqrt(1 - t) * math.sin(2 * math.pi * n / L)]
                    for t in times for n in range(L)])
    angles = np.array([owner.angle_pair(p, pair) for pair in psi])
    search = 8000
    T1, first, error1, indices1 = phase_plan(owner, loader, 14, 0, angles[:, 0], search)
    T2, second, error2, indices2 = phase_plan(owner, loader, 14, 15, angles[:, 1], search)
    T = T2 + T1
    anchor = loader.nearest_power(theta, 3, search)
    H_word = loader.rotation(1, 14, anchor, abs(anchor))
    B = owner.plane(1, 14, 16 * anchor * theta)
    word = loader.inverse(H_word) + loader.inverse(T) + H_word + T
    owned_B = owner.plane(1, 14, theta)
    vacuum = np.zeros(16)
    vacuum[[1, 14]] = (math.sqrt(p), p)
    vacuum_with_port_spin = np.kron(vacuum, np.eye(8)[0])
    inventory = physical_prefix_symbols(owner, loader, word)
    signed_word_replay = replay_all_sections(owner, loader, word, 7)
    max_operator_error, max_replay_error = 0.0, 0.0
    prepared_psi = []
    for js, pair in enumerate(psi):
        exact = owner.compose(owner.owned_target(p, pair), owned_B.T)
        rounded_T = owner.compose(owner.plane(14, 0, first[js]), owner.plane(14, 15, second[js]))
        approx = owner.compose(rounded_T, B, rounded_T.T, B.T)
        op_error = owner.opnorm(exact - approx)
        max_operator_error = max(max_operator_error, op_error)
        replay_error = float(np.max(np.abs(signed_word_replay[js] - np.kron(approx, np.eye(8)))))
        max_replay_error = max(max_replay_error, replay_error)
        owner.require(replay_error < 2e-9, "every positive-window section matches native full replay")
        # Original CAR moment M_A=(|1><A|+|A><1|)/(2sqrt(p)).
        column = np.einsum("ij,j->i", signed_word_replay[js], vacuum_with_port_spin)[np.arange(16) * 8]
        prepared_psi.append(column[[0, 15]] * column[1] / math.sqrt(p))
    total_bound = 2 * (error1 + error2) + 2 * owner.rotation_error(16 * anchor * theta, theta)
    owner.require(max_operator_error <= total_bound + 1e-11, "all-column value bound")

    def energy(field):
        by_j = np.reshape(field, (2, L, 2))
        return np.sum(((np.roll(by_j, -1, axis=1) - by_j) / H)**2, axis=2)

    exact = energy(psi)
    approximate = energy(prepared_psi)
    exact_jet = (exact[1] - exact[0]) / (2 * step)
    formula = -sigma * np.cos(4 * math.pi * (np.arange(L) + 0.5) / L)
    owner.require(np.max(np.abs(exact_jet - formula)) < 1e-14, "elliptical exact edge jet including seam")
    observed_jet_error = float(np.max(np.abs((approximate[1] - approximate[0]) / (2 * step) - formula)))
    moment_error = float(np.max(np.linalg.norm(np.array(prepared_psi) - psi, axis=1)))
    owner.require(moment_error <= 2 * total_bound / math.sqrt(p), "coordinate moment continuity")
    grad_bound = float(np.sqrt(np.max(exact)))
    grad_err = 2 * moment_error / H
    jet_bound = (2 * grad_bound + grad_err) * grad_err / step
    owner.require(observed_jet_error <= jet_bound + 1e-11, "forward material jet bound")

    sign_margin = certify_native_material_jet(owner, L, anchor, indices1, indices2)
    head_probs = nc1_actual_projectors(owner, p, theta)
    print(json.dumps({
        "status": "PASS",
        "PR334_commit": "2350117b469890c04b8ff5d8987b224a863e844a",
        "dyadic_L": L,
        "field_endpoints": times,
        "material_level": "1/64",
        "lattice_H": H,
        "half_secant_step": step,
        "single_literal_square_word": inventory,
        "virtual_columns_replayed_all_J_SITE_CAR_PORT_Spin": len(signed_word_replay) * 128,
        "common_gate_sequence_J_always_control": True,
        "old_q_and_READOUT_protected": True,
        "own_NC1_marks_and_norms": dict(zip(("0", "10", "11"), head_probs)),
        "max_full_replay_defect": max_replay_error,
        "illustrative_max_full_operator_error": max_operator_error,
        "illustrative_all_section_operator_error_bound": total_bound,
        "illustrative_max_CAR_moment_pair_error": moment_error,
        "certified_literal_CAR_material_jet_all_edge_signs": True,
        "certified_positive_signed_CAR_material_jet_margin": sign_margin,
        "exact_target_jet_supremum": float(np.max(np.abs(formula))),
        "illustrative_max_material_jet_error": observed_jet_error,
        "illustrative_material_jet_error_bound": jet_bound,
        "cartesian_walsh_powers": [indices1, indices2],
        "fixed_geometric_gain_missing": True,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
