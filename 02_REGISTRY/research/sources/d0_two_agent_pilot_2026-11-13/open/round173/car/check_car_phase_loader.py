"""Native CAR phase loader on dyadic SITE and its common-static finite secants."""
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
import json
import math
from pathlib import Path

import numpy as np


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def native_owner():
    research_sources = Path(__file__).resolve().parents[4]
    path = research_sources / "d0_native_execution_domain_2026-10-24" / "native_execution.py"
    spec = spec_from_file_location("car_native", path)
    native = module_from_spec(spec)
    import sys
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    return native


class NativeLoader:
    """Runs count genuine identical chronological gates; each can be expanded."""

    def __init__(self, native, site_bits):
        self.native = native
        self.site = tuple(range(site_bits))
        self.car = tuple(range(site_bits, site_bits + 4))
        self.port = site_bits + 4
        self.spin = (site_bits + 5, site_bits + 6)
        self.width = site_bits + 7
        self.p = (math.sqrt(5) - 1) / 2
        self.theta = math.asin(self.p)
        self.source = self.native.Gate("SourceI", (self.port, *self.spin))
        self.g_port = self.native.Gate("G", (self.port,))

    def cx(self, a, b):
        return (self.native.Gate("CX", (a, b)), 1)

    def swap(self, a, b):
        return (self.cx(a, b), self.cx(b, a), self.cx(a, b))

    def balanced(self, target, numerator, budget):
        require(abs(numerator) <= budget, "common nonnegative power budgets")
        move = self.swap(target, self.port)
        sign = (self.source, 2)
        return move + (sign, (self.g_port, budget - numerator),
                       sign, (self.g_port, budget + numerator)) + move

    def rotation(self, start, target, numerator, budget, extra_controls=()):
        """Maps the first listed CAR state toward the second for positive angle."""
        differing = [j for j in range(4) if ((start ^ target) >> (3 - j)) & 1]
        require(differing, "distinct CAR basis states")
        pivot = differing[0]
        target_wire = self.car[pivot]
        first_bit = (start >> (3 - pivot)) & 1
        route = tuple(self.cx(target_wire, self.car[k]) for k in differing[1:])
        canonical = start
        if first_bit:
            for bit in differing[1:]:
                canonical ^= 1 << (3 - bit)
        conditions = tuple((wire, (canonical >> (3 - j)) & 1)
                           for j, wire in enumerate(self.car) if j != pivot) + tuple(extra_controls)
        gray = [index ^ (index >> 1) for index in range(1 << len(conditions))]
        word = list(route)
        for mask, next_mask in zip(gray, gray[1:] + gray[:1]):
            sign = 1 - 2 * ((first_bit + sum(bit for j, (_, bit) in enumerate(conditions)
                                             if (mask >> j) & 1)) % 2)
            word.extend(self.balanced(target_wire, sign * numerator, budget))
            diff = mask ^ next_mask
            require(diff and diff & (diff - 1) == 0, "cyclic Gray address changes one control")
            word.append(self.cx(conditions[diff.bit_length() - 1][0], target_wire))
        return tuple(word) + tuple(reversed(route))

    def inverse(self, word):
        result = []
        for gate, n in reversed(word):
            if not n:
                continue
            if gate.op == "CX":
                result.append((gate, n))
            elif gate.op == "SourceI":
                result.append((gate, 3 * n))
            else:
                require(gate == self.g_port, "all positive rotations take place on actual PORT")
                result.extend(((self.source, 2), (gate, n), (self.source, 2)))
        return tuple(result)

    def nearest_power(self, theta, controls, search):
        unit = (1 << (controls + 1)) * self.theta
        best = min(range(-search, search + 1),
                   key=lambda n: abs(math.remainder(unit * n - theta, 2 * math.pi)))
        return best

    def operators(self, word):
        """Direct all-column replay grouping adjacent identical literal gates only."""
        size = 1 << self.width
        rows = np.arange(size)
        full = np.eye(size)
        source_index = np.argmax(abs(np.array(self.native.SOURCE_I_LOCAL, dtype=float)), axis=1)
        source_sign = np.array(self.native.SOURCE_I_LOCAL, dtype=float)[np.arange(8), source_index]
        bits = tuple(1 << (self.width - 1 - wire) for wire in (self.port, *self.spin))
        local = sum(((rows & mask) != 0) * factor for mask, factor in zip(bits, (4, 2, 1)))
        rest = rows & ~sum(bits)

        def inflate(values):
            return sum(((values & factor) != 0) * mask for mask, factor in zip(bits, (4, 2, 1)))

        source_preimage = rest + inflate(source_index[local])
        source_factors = source_sign[local]
        for gate, n in word:
            if n == 0:
                continue
            if gate.op == "CX":
                if n % 2:
                    c, target = (1 << (self.width - 1 - wire) for wire in gate.wires)
                    full = full[rows ^ np.where(rows & c, target, 0)]
            elif gate.op == "SourceI":
                for _ in range(n % 4):
                    full = full[source_preimage] * source_factors[:, None]
            else:
                require(gate == self.g_port, "replay source port")
                mask = bits[0]
                angle = math.remainder(n * self.theta, 2 * math.pi)
                sign = np.where(rows & mask, 1, -1)
                full = math.cos(angle) * full + math.sin(angle) * sign[:, None] * full[rows ^ mask]
        return full

    def literal_word(self, runs):
        return tuple(gate for gate, repetitions in runs for _ in range(repetitions))


def compose(*matrices):
    product = matrices[0]
    for matrix in matrices[1:]:
        product = np.einsum("ij,jk->ik", product, matrix)
    return product


def verify_walsh_address():
    for controls in (3, 4):
        count = 1 << controls
        for address in range(count):
            for actual in range(count):
                factor = sum((-1) ** bin((address ^ actual) & mask).count("1")
                             for mask in range(count))
                require(factor == (count if actual == address else 0),
                        "exact integer Walsh selector")


def plane(start, end, theta):
    result = np.eye(16)
    c, s = math.cos(theta), math.sin(theta)
    result[start, start] = result[end, end] = c
    result[start, end], result[end, start] = -s, s
    return result


def angle_pair(p, psi):
    a, b = psi
    return math.asin(a / math.sqrt(p * p - b * b)), math.asin(b / p)


def owned_target(p, psi):
    a, b = psi
    m = np.zeros(16)
    m[1], m[0], m[15], m[14] = math.sqrt(p), a, b, math.sqrt(p * p - a * a - b * b)
    e = np.eye(16)[:, 1]
    K = np.outer(m, e) - np.outer(e, m)
    return np.eye(16) + K + compose(K, K) / (1 + math.sqrt(p))


def rotation_error(actual, ideal):
    return 2 * abs(math.sin((actual - ideal) / 2))


def opnorm(matrix):
    return float(np.linalg.norm(matrix, 2))


def main():
    verify_walsh_address()
    native = native_owner()
    loader = NativeLoader(native, 2)
    p, theta = loader.p, loader.theta
    static_phase_angles = (math.pi, math.pi / 2)
    search = 640
    phase_powers = tuple(loader.nearest_power(angle, 4, search) for angle in static_phase_angles)
    W = tuple(g for wire, k in zip(loader.site, phase_powers)
              for g in loader.rotation(0, 15, k, abs(k), ((wire, 1),)))
    W_inv = loader.inverse(W)
    true_W = [plane(0, 15, math.pi * n / 2) for n in range(4)]
    rounded_W = [plane(0, 15, sum(32 * k * theta * ((n >> (1 - j)) & 1)
                                    for j, k in enumerate(phase_powers)))
                 for n in range(4)]
    phase_error = sum(rotation_error(32 * k * theta, ideal)
                      for k, ideal in zip(phase_powers, static_phase_angles))

    anchor_power = loader.nearest_power(theta, 3, search)
    H = loader.rotation(1, 14, anchor_power, abs(anchor_power))
    rounded_anchor = plane(1, 14, 16 * anchor_power * theta)
    anchor_error = rotation_error(16 * anchor_power * theta, theta)
    h = 1 / 4
    F_H = 16517734400 / 162621047169
    k0 = 23.4164067518840749729
    amplitude = h * math.sqrt(F_H / k0) / (2 * math.sin(math.pi * h))
    step = 1 / 64
    direction = np.array([1 / 2, -1 / 3])
    endpoints = (np.array([amplitude, 0.0]), np.array([amplitude, 0.0]) + step * direction)
    angles = tuple(angle_pair(p, psi) for psi in endpoints)
    chosen = tuple(tuple(loader.nearest_power(angle, 3, search) for angle in pair) for pair in angles)
    budgets = tuple(1 + max(abs(chosen[0][j]), abs(chosen[1][j])) for j in range(2))
    approximants, exact_targets, cores, Ts, errors, counts = [], [], [], [], [], []

    for psi, (first, second), (n1, n2) in zip(endpoints, angles, chosen):
        T_word = loader.rotation(14, 15, n2, budgets[1]) + loader.rotation(14, 0, n1, budgets[0])
        word = W_inv + loader.inverse(T_word) + H + T_word + W
        literal = loader.literal_word(word)
        run = native.Execution(loader.width, (), (), literal, native.G_CX_SOURCE_I, loader.port, loader.spin)
        native.validate_execution(run, max_qubits=loader.width, max_expanded_stages=len(literal))
        require(all(g.wires[-1] not in loader.site for g in literal), "SITE only acts as a control")
        counts.append(dict(Counter(g.op for g in literal)))

        target = owned_target(p, psi)
        t_matrix = compose(plane(14, 0, first), plane(14, 15, second))
        require(np.max(abs(compose(t_matrix, plane(1, 14, theta), t_matrix.T) - target)) < 1e-14,
                "Cartesian factorization equals whole owned Householder")
        Ts.append(t_matrix)
        cores.append(target)
        rounded_t = compose(plane(14, 0, 16 * n1 * theta), plane(14, 15, 16 * n2 * theta))
        core = compose(rounded_t, rounded_anchor, rounded_t.T)
        exact_targets.append([compose(frame, target, frame.T) for frame in true_W])
        approximants.append([compose(frame, core, frame.T) for frame in rounded_W])
        replay = loader.operators(word)
        expected = np.zeros_like(replay)
        for site in range(4):
            start = site * 128
            expected[start:start + 128, start:start + 128] = np.kron(approximants[-1][site], np.eye(8))
        require(np.max(abs(expected - replay)) < 5e-11, "native full SITE/CAR/PORT/Spin block")
        require(np.max(abs(compose(replay.T, replay) - np.eye(len(replay)))) < 5e-11,
                "orthogonal all-column completion")
        errors.append(rotation_error(16 * n1 * theta, first) + rotation_error(16 * n2 * theta, second))
    require(counts[0] == counts[1], "balanced full literal budgets")

    secant_error = max(opnorm((ap - am) - (bp - bm)) for ap, am, bp, bm in
                       zip(approximants[1], approximants[0], exact_targets[1], exact_targets[0])) / step
    static_and_dynamic_bound = (2 * sum(errors) + 2 * anchor_error * opnorm(Ts[1] - Ts[0])
                                + 2 * phase_error * opnorm(cores[1] - cores[0])) / step
    require(secant_error < static_and_dynamic_bound + 1e-11, "common-static operator secant")

    Pi = np.diag([int(j in (0, 15)) for j in range(16)])
    def projectors(matrices):
        return [compose(U.T, Pi, U) for U in matrices]

    projector_error = max(opnorm((ap - am) - (bp - bm)) for ap, am, bp, bm in
                          zip(projectors(approximants[1]), projectors(approximants[0]),
                              projectors(exact_targets[1]), projectors(exact_targets[0]))) / step
    value_errors = [2 * phase_error + anchor_error + 2 * value for value in errors]
    observed_values = [max(opnorm(a - b) for a, b in zip(rounded, exact))
                       for rounded, exact in zip(approximants, exact_targets)]
    require(all(observed <= bound + 1e-11 for observed, bound in zip(observed_values, value_errors)),
            "endpoint error")
    projector_bound = 2 * static_and_dynamic_bound + sum(value_errors) * opnorm(cores[1] - cores[0]) / step
    require(projector_error < projector_bound + 1e-11, "fixed projector secant")
    print(json.dumps({
        "status": "PASS",
        "PR334_commit": "2350117b469890c04b8ff5d8987b224a863e844a",
        "dyadic_L": 4,
        "exact_mathematical_whole_column_factorization": True,
        "exact_integer_Walsh_selector_3_and_4_controls": True,
        "native_replay_columns_including_source_work": 512,
        "RIGHT_and_other_SITE_axes_are_untouched_tensor_factors": True,
        "literal_op_inventory_both_endpoints": counts[0],
        "static_site_power_indices": phase_powers,
        "static_anchor_power_index": anchor_power,
        "two_cartesian_power_vectors": chosen,
        "cartesian_secant_step": step,
        "static_phase_error_upper_bound": phase_error,
        "static_anchor_error": anchor_error,
        "illustrative_operator_value_errors": observed_values,
        "proved_form_operator_value_bounds_at_example": value_errors,
        "illustrative_operator_secant_error": secant_error,
        "proved_form_operator_secant_bound_at_example": static_and_dynamic_bound,
        "illustrative_fixed_projector_secant_error": projector_error,
        "proved_form_fixed_projector_secant_bound_at_example": projector_bound,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
