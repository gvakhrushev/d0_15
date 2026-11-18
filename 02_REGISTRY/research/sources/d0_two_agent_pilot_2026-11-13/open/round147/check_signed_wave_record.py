"""Verify the signed wave statistic and its exact native code calibration."""

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import sympy as sp


RESEARCH = Path(__file__).resolve().parents[4]
SOURCES = (
    "sources/d0_two_agent_pilot_2026-11-13/direct/round73/matter/check_matter_root.py",
    "sources/d0_two_agent_pilot_2026-11-13/direct/round74/polarization/"
    "UNIT_MATERIAL_RESPONSE_RU.md",
    "sources/d0_paid_moment_field_writer_2026-10-21/moments/"
    "EXACT_MOMENT_SOURCE_CONSTRUCTION.md",
    "sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
    "NATIVE_FOUR_COPY_MATTER_RESPONSE.md",
    "A4D_NATIVE_BOOK03_BORN_ENTROPY_BELLMAN_VERTEX_INFORMATION_WELD_2026_10_22.md",
)
ZERO = (0, 0, 0, 0)
U, V, X, Y = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(offset):
    return tuple(-a for a in offset)


def derivative(offset, forward):
    return {offset: 1, ZERO: -1} if forward else {ZERO: 1, neg(offset): -1}


def wave_stencil():
    stencil = defaultdict(int)
    for left, right, sign in ((U, V, 1), (V, U, 1), (X, X, -1), (Y, Y, -1)):
        for a, v1 in derivative(left, False).items():
            for b, v2 in derivative(right, True).items():
                stencil[add(a, b)] += sign * v1 * v2
    return {shift: coefficient for shift, coefficient in stencil.items() if coefficient}


def overlaps():
    pairs = [k for k in product(range(4), repeat=4)
             if k < tuple(-value % 4 for value in k)][:64]
    cos = (1, 0, -1, 0)
    return {d: Q(sum(cos[sum(a * b for a, b in zip(d, k)) % 4] for k in pairs), 64)
            for d in (U, V, X, Y, add(U, neg(V)))}


def compare_statistic_and_action(length, stencil, p):
    h = Q(1, length)
    size = length**4
    sites = list(product(range(length), repeat=4))
    a, b, c = (1, 0, 1, 1), (1, 0, 1, 2), (2, length - 1, 1, 1)
    fields = ({a: Q(1, 12), b: Q(-1, 10)}, {a: Q(1, 8), b: Q(1, 7), c: Q(1, 9)})

    def at_offset(site, shift):
        return tuple(value % length for value in add(site, shift))

    stencil_sum = Q(0)
    differences_sum = Q(0)
    for field in fields:
        for site in sites:
            origin = field.get(site, 0)
            du, dv, dx, dy = [field.get(at_offset(site, step), 0) - origin
                              for step in (U, V, X, Y)]
            differences_sum += -2 * du * dv + dx**2 + dy**2
            for shift, weight in stencil.items():
                stencil_sum += weight * origin * field.get(at_offset(site, shift), 0)
    require(stencil_sum == differences_sum and stencil_sum != 0,
            "Finite wave form and mixed differences agree")
    # Bernoulli J padding decoded by the two fair outcome bits (counts of plus).
    plus_counts = {2: 4, 1: 3, 0: 2, -1: 1}
    for weight, count in plus_counts.items():
        require(Q(2 * count - 4, 4) == Q(weight, 2), "Implemented mean of J")
    # Two full site outcomes, one common fair polarisation, then the parity read.
    offset_mean_sum = sum(Q(2 * plus_counts[weight] - 4, 4)
                          * origin * field.get(at_offset(site, shift), 0)
                          for field in fields for site, origin in field.items()
                          for shift, weight in stencil.items())
    q_shift = p * offset_mean_sum / size**2
    wave_action = p**12 * stencil_sum / (2 * size * h**2)
    gain = p * h**2 / (p**12 * size)
    require(sp.simplify(q_shift - gain * wave_action) == 0, "Born calibration of Q_h")
    require(Q(-1, 2) < offset_mean_sum / size**2 < Q(1, 2), "Regular test probability")
    # The y-link contributes with the intended sign to the relative sign witness.
    require(stencil[Y] == -1 and stencil[neg(Y)] == -1, "Transverse y link")
    return {
        "gain_in_units_p_inverse_11": str(Q(1, length**6)),
        "printed_bits": 13 * length**6,
        "cx_suffix": 47 * length**6 // 2,
    }


def check_refining_gap():
    h = sp.symbols("h", positive=True)
    s = sp.sin(2 * sp.pi * h)
    w = sp.sin(4 * sp.pi * h)
    without_cancellation = (-4*s**2 - 4*s*sp.sin(8*sp.pi*h) + 4*s**2 + 4*w**2) / h**2
    eigenvalue = 8*w*s*(sp.cos(2*sp.pi*h) - sp.cos(4*sp.pi*h)) / h**2
    require(sp.trigsimp(without_cancellation - eigenvalue) == 0, "Refining eigenmode")
    require(sp.limit(eigenvalue / h**2, h, 0, dir="+") == 384 * sp.pi**4,
            "Refining eigenvalue coefficient")


def main():
    stencil = wave_stencil()
    expected = {ZERO: 2}
    for shift, sign in ((U, 1), (V, 1), (add(U, neg(V)), -1), (X, -1), (Y, -1)):
        expected[shift] = expected[neg(shift)] = sign
    require(stencil == expected, "Eleven finite operator coefficients")
    gram = overlaps()
    require(tuple(gram.values()) == (Q(7, 16), Q(3, 16), Q(1, 16), Q(0), Q(1, 4)),
            "Actual retained Fourier overlaps")
    p = (sp.sqrt(5) - 1) / 2
    slope = p**3 * (5 + 21*(1 - 2*p)) / 2
    require(sp.simplify(slope - p**11) == 0, "Unit cost response")
    require(3*Q(3, 8) - 1 > 0, "Positive flipped-bit Info from p < 5/8")
    require(Q(25, 2) * Q(5, 8)**9 < Q(1, 4), "A74 old port bound")
    require(Q(8, 5)**9 > 64, "64 old leaves have entropy less than 9 Golden units")
    tests = {str(n): compare_statistic_and_action(n, stencil, p) for n in (4, 8)}
    check_refining_gap()
    print(json.dumps({
        "GR_closed": False,
        "supported_displacements_with_center": len(stencil),
        "retained_Fourier128_y_neighbour_overlap": str(gram[Y]),
        "unit_signed_wave_source_on_incremental_code_minus_CQ": True,
        "scalar_Born_Shannon_partition_requires_ancestor_Info_update": True,
        "absolute_native_history_admitted_and_priced": False,
        "dyadic_eigenvalue_limit_divided_by_h_squared": "384*pi^4",
        "statistics_and_code": tests,
        "source_sha256": {path: sha256((RESEARCH / path).read_bytes()).hexdigest()
                          for path in SOURCES},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
