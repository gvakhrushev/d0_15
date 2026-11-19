#!/usr/bin/env python3
"""Bounded checks for the flat old-v8 null-sideband equalizer.

This checks the translation-invariant CAR-only symbol and finite lattice
readouts. It does not load a curved operator, AF/RIGHT factorization, or a
whole-programme price.
"""
import json
from cmath import exp, pi
from itertools import product
from math import cos, sin, sqrt

P = (sqrt(5.0) - 1.0) / 2.0
MODE = (1, -1, -1, -1)
MODE_PRIME = (-1, 1, -1, -1)
Q = tuple(b - a for a, b in zip(MODE, MODE_PRIME))
ETA = (1.0, -1.0, -1.0, -1.0)
EXTERIOR_ORDER = (0, 2, 3, 1)
AMPLITUDE = 0.2
TOL = 2e-10
CHECK_COUNT = 0
CHECK_KINDS = set()


def require(ok, label):
    global CHECK_COUNT
    if not ok:
        raise AssertionError("null_sideband:" + label)
    if label not in CHECK_KINDS:
        CHECK_COUNT += 1
        CHECK_KINDS.add(label)


def close(a, b, label, tol=TOL):
    require(abs(a - b) <= tol, label)


def symbol_energy(mode, n, d, o):
    """z*[(d-o)I+o11*]z for h=1/n and k=2pi*mode."""
    z = [n * (exp(2j * pi * m / n) - 1.0) for m in mode]
    total = sum(z)
    gz = [(d - o) * value + o * total for value in z]
    value = sum(a.conjugate() * b for a, b in zip(z, gz))
    require(abs(value.imag) <= TOL, "real_old_v8_symbol")
    return value.real


def local_state(site, n, amplitude=AMPLITUDE):
    phase = lambda mode: 2.0 * pi * sum(m * x for m, x in zip(mode, site)) / n
    root = sqrt(1.0 - P - 2.0 * amplitude * amplitude)
    return {
        0: amplitude * exp(1j * phase(MODE_PRIME)),
        1: sqrt(P) * exp(1j * phase(MODE)),
        14: root * exp(1j * phase(MODE)),
        15: -1j * amplitude * exp(1j * phase(MODE_PRIME)),
    }


def create(i):
    matrix = [[0.0] * 16 for _ in range(16)]
    for mask in range(16):
        if mask & (1 << i):
            continue
        predecessors = EXTERIOR_ORDER[:EXTERIOR_ORDER.index(i)]
        sign = (-1.0) ** sum(bool(mask & (1 << j)) for j in predecessors)
        matrix[mask | (1 << i)][mask] = sign
    return matrix


def transpose(matrix):
    return [[matrix[j][i] for j in range(16)] for i in range(16)]


def add(a, b, sign_b=1.0):
    return [[a[i][j] + sign_b * b[i][j] for j in range(16)]
            for i in range(16)]


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(16))
             for j in range(16)] for i in range(16)]


def check_car_current_restline():
    support = (0, 1, 14, 15)
    creators = [create(i) for i in range(4)]
    for i in range(1, 4):
        alpha_i = multiply(add(creators[0], transpose(creators[0])),
                           add(creators[i], transpose(creators[i]), -1.0))
        compressed = [alpha_i[a][b] for a in support for b in support]
        require(max(abs(x) for x in compressed) == 0.0,
                "full_CAR_current_compression_i" + str(i))


def check_grid(n):
    require(2 * pi * (Q[0] ** 2 - Q[1] ** 2) == 0.0,
            "integer_null_wavevector")
    for d, o in ((1.7, 0.3), (2.3, 0.8)):
        lam = symbol_energy(MODE, n, d, o)
        lam_prime = symbol_energy(MODE_PRIME, n, d, o)
        close(lam, lam_prime, "permuted_equal_old_v8_eigenvalue_N" + str(n))
        require(lam > 0.0, "positive_test_symbol_N" + str(n))

    h = 1.0 / n
    delta = [2.0 * pi * q / n for q in Q]
    q_energy = sum(ETA[mu] * sin(delta[mu] / 2.0) ** 2 for mu in range(4))
    close(q_energy, 0.0, "exact_centered_box_null_N" + str(n))
    require(abs(sin(delta[0])) > 1e-8,
            "nonzero_finite_null_gradient_N" + str(n))

    for site in product(range(n), repeat=4):
        theta = 2.0 * pi * sum(q * x for q, x in zip(Q, site)) / n
        psi = (AMPLITUDE * cos(theta), AMPLITUDE * sin(theta))
        state = local_state(site, n)
        norm = sum(abs(value) ** 2 for value in state.values())
        close(norm, 1.0, "local_CAR_norm_N" + str(n))

        rho01 = state[0] * state[1].conjugate()
        rho151 = state[15] * state[1].conjugate()
        close(rho01.real / sqrt(P), psi[0],
              "grade0_readout_N" + str(n))
        close(rho151.real / sqrt(P), psi[1],
              "top_readout_N" + str(n))
        close(abs(state[1]) ** 2, P, "fixed_clock_density_N" + str(n))
        require(abs(state[14] * state[0].conjugate()) > 0.0,
                "additional_CAR_coherence_retained_N" + str(n))

        first = []
        for mu in range(4):
            step = delta[mu]
            forward = (
                AMPLITUDE * (cos(theta + step) - cos(theta)) / h,
                AMPLITUDE * (sin(theta + step) - sin(theta)) / h,
            )
            energy = forward[0] ** 2 + forward[1] ** 2
            expected = (2.0 * AMPLITUDE * sin(step / 2.0) / h) ** 2
            close(energy, expected,
                  "constant_forward_pair_speed_N" + str(n))
            first.append((
                -AMPLITUDE * sin(theta) * sin(step) / h,
                AMPLITUDE * cos(theta) * sin(step) / h,
            ))

            second_cos = (cos(theta + step) - 2.0 * cos(theta)
                          + cos(theta - step)) / (h * h)
            second_sin = (sin(theta + step) - 2.0 * sin(theta)
                          + sin(theta - step)) / (h * h)
            # The two fields share the same Fourier symbol. The eta-weighted
            # sum is checked below, rather than each directional term.
            if mu == 0:
                box_cos = [second_cos]
                box_sin = [second_sin]
            else:
                box_cos.append(second_cos)
                box_sin.append(second_sin)

        for field_box, label in ((box_cos, "cos"), (box_sin, "sin")):
            box = sum(ETA[mu] * field_box[mu] for mu in range(4))
            close(box, 0.0, "finite_box_" + label + "_N" + str(n))

        for mu in range(4):
            for nu in range(4):
                stress = sum(first[mu][a] * first[nu][a] for a in range(2))
                expected = (AMPLITUDE ** 2 * sin(delta[mu]) *
                            sin(delta[nu]) / (h * h))
                close(stress, expected, "central_pair_stress_N" + str(n))

        trace = sum(ETA[mu] * sum(first[mu][a] ** 2 for a in range(2))
                    for mu in range(4))
        close(trace, 0.0, "central_pair_null_trace_N" + str(n))

    check_car_current_restline()


def test():
    require(P > 0.0 and 2.0 * AMPLITUDE ** 2 < 1.0 - P,
            "nonempty_normalized_amplitude_interval")
    for n in (8, 12):
        check_grid(n)

    # Every nonzero CAR component is one of the two equal-eigenvalue modes.
    # Thus a globally normalized one-column CAR state obeys Delta C=lambda C.
    require(MODE != MODE_PRIME, "distinct_sideband_modes")
    require(Q == (-2, 2, 0, 0), "declared_null_sideband")
    return {
        "status": "PASS",
        "check_categories": CHECK_COUNT,
        "lattice_sites_checked": 8 ** 4 + 12 ** 4,
        "check_kinds": sorted(CHECK_KINDS),
        "scope": {
            "flat_old_v8_CAR_only_symbol": True,
            "curved_operator_or_full_H_plus_J_plus_R_root": False,
            "AF_RIGHT_factorization_or_canonical_reference128": False,
            "physical_query_PREP_Book_admission": False,
        },
        "interpretation": (
            "Exact flat CAR-only Rayleigh stationary candidate with a "
            "nonzero null two-field readout; not physical D0-to-GR closure."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(test(), ensure_ascii=False, sort_keys=True))
