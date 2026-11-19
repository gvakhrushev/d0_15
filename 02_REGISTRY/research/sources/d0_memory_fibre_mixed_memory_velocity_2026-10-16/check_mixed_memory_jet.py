#!/usr/bin/env python3
"""Exact quotient-jet lemma for memory-only mixed first velocities."""
from pathlib import Path
import hashlib
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
checks = []

def require(name, condition):
    if not bool(condition):
        raise ArithmeticError(name)
    checks.append(name)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def evaluate():
    pins = json.loads((HERE / "INPUTS.json").read_text())["sha256"]
    for rel, expected in pins.items():
        require("input_pin:" + rel, sha(ROOT / rel) == expected)

    old = json.loads((ROOT / "02_REGISTRY/research/sources/d0_memory_fibre_crossing_2026-10-16/RESULT.json").read_text())
    lo, hi = old["crossing_interval"]
    require("owned_interior_crossing_segment", 0 < lo < hi < 1)
    require("unique_simple_crossing", old["unique_crossing_for_each_root_box_parameter_pair"] and old["complex_fourier_kernel_dimension"] == 1)
    require("full_rank_memory_segment", old["preparation_rank_on_crossing_segment"] == 16)
    pair_bound = old["center"]["all_kernel_memory_tangent_pairings_upper"]
    require("strict_owned_cokernel_pairing", pair_bound < -0.8441)

    # Exact translation-support check in (Z/8)^4.
    L = 8
    omega = set()
    for r in range(4):
        for sign in (-1, 1):
            q = [0] * 4
            q[r] = sign % L
            omega.add(tuple(q))
    difference = {tuple((a[j] - b[j]) % L for j in range(4))
                  for a in omega for b in omega}
    q_original = (3, 3, 0, 0)
    q_representative = (3, 0, 0, 3)
    require("omega_has_eight_shell_modes", len(omega) == 8)
    require("omega_difference_has_33_modes", len(difference) == 33)
    require("original_q_outside_omega_difference", q_original not in difference)
    require("s3_q_representative_outside_difference", q_representative not in difference)
    require("q_and_representative_are_spatial_permutations", q_original[0] == q_representative[0] and sorted(q_original[1:]) == sorted(q_representative[1:]))
    require("negative_q_outside_omega_difference", tuple((-x) % L for x in q_representative) not in difference)

    # The owned reduced eigenvalue is the quotient Tr(sigma K)/Tr(sigma G).
    # On this q sector K_0=eps0 G_0 and K_1=eps0 G_1 (the shell compression
    # of E_1 vanishes). Its order-two numerator correction M is affine in
    # sigma, while both the order-one denominator and its memory variation
    # are retained. This exact jet models the full quotient, not a frozen
    # denominator.
    t, w, z = sp.symbols("t w z", real=True)
    eps0 = sp.symbols("eps0", real=True)
    g10, g11, g12, g20, g21, g22 = sp.symbols("g10 g11 g12 g20 g21 g22", real=True)
    m0, mw, mz = sp.symbols("m0 mw mz", real=True)
    G = 1 + t * (g10 + w*g11 + z*g12) + t**2 * (g20 + w*g21 + z*g22) / 2
    M = m0 + w*mw + z*mz
    epsilon_hat = eps0 + t**2 * M / (2*G)
    at_base = {t: 0, w: 0, z: 0}
    def at(expr):
        return sp.simplify(expr.subs(at_base))
    require("q_first_eigenvalue_jet_zero", at(sp.diff(epsilon_hat, t)) == 0)
    require("first_q_derivative_zero_over_memory_fibre", at(sp.diff(epsilon_hat, t, w)) == 0)
    require("two_memory_one_q_derivative_zero", at(sp.diff(epsilon_hat, t, w, z)) == 0)
    require("three_memory_derivative_zero", at(sp.diff(epsilon_hat, w, w, z)) == 0)
    require("field_field_memory_term_is_owned_M", at(sp.diff(epsilon_hat, t, t, z)) == mz)
    total = (sp.diff(epsilon_hat, t, t, z)
             + 2*sp.diff(epsilon_hat, t, w, z)
             + sp.diff(epsilon_hat, w, w, z))
    require("full_mixed_jet_independent_of_memory_velocity", at(total - mz) == 0)
    # Hostile control: without the q-compression identity, mixed density
    # derivatives need not vanish, so the theorem is not overgeneralized.
    outside_support = eps0 + t * (w + z) / (1 + z)
    require("nonzero_mixed_term_without_q_support_hypothesis",
            at(sp.diff(outside_support, t, w, z)) == -1)

    return {
        "schema": "d0-memory-only-mixed-velocity-jet/1",
        "exact_checks": len(checks),
        "checks": checks,
        "fourier": {
            "L": 8, "omega_size": len(omega), "omega_difference_size": len(difference),
            "q_original": list(q_original), "q_representative": list(q_representative),
            "both_outside_omega_difference": True, "shell_compression_of_first_q_jet": "zero"
        },
        "reduced_jet": {
            "functional": "Phi(x,sigma)=F_price(Delta(x))+epsilon_hat(x,sigma)",
            "quotient_denominator_variations_retained": True,
            "pure_memory_cubic_term": "zero",
            "q_memory_memory_cubic_term": "zero",
            "q_q_memory_cubic_term": "Tr(zeta M_v)",
            "sum_for_xi=(v,w)": "Tr(zeta M_v), independent of w"
        },
        "consumed_crossing": {
            "result_sha256": pins["02_REGISTRY/research/sources/d0_memory_fibre_crossing_2026-10-16/RESULT.json"],
            "crossing_interval": [lo, hi],
            "complex_kernel_dimension": old["complex_fourier_kernel_dimension"],
            "unit_pairing_upper": pair_bound,
            "real_q_minus_q_kernel_dimension": old["real_q_minus_q_kernel_dimension_before_orbit_quotient"]
        },
        "conclusion": {
            "no_second_order_jet_for_nonzero_crossing_pair_plus_any_memory_fibre_tangent": True,
            "requires_no_zero_first_order_memory_assumption": True,
            "additional_field_modes_classified": False,
            "nonlinear_branch_or_physical_GR_closed": False
        },
        "input_sha256": pins
    }

if __name__ == "__main__":
    result = evaluate()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
