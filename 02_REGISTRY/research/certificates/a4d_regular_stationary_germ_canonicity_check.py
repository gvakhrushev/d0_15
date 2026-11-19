#!/usr/bin/env python3
"""Finite controls for the analytic regular-stationary constitutive theorem.

Replays the existing all-solder and independent Schur owners. New controls:
translated degree-six reconstruction, the total-degree Newton simplex,
the sharp general-stencil C6/C7 raw-norm boundary, and actual native maps.
The C^R theorem itself is proved in the companion memo, not by this script.
No full-class D0 selector, exact general source lift, or parent terminal.
"""
from __future__ import annotations

import argparse
import contextlib
from fractions import Fraction as F
import hashlib
from itertools import combinations_with_replacement, product
import io
import json
import math
from pathlib import Path
import runpy

import sympy as sp

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_regular_stationary_germ_canonicity_results.json"
INPUTS = (
    "a4d_j2_fixed_realization_ir_check.py",
    "a4d_schur_einstein_direct_identification_check.py",
    "a4d_metric_null_hessian_complex_check.py",
    "a4d_warped_designated_normal_rescue_results.json",
    "a4d_warped_smooth_comparator_bias_results.json",
    "a4d_fixed_source_algebraic_stationarity_results.json",
)


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def replay_owner(name: str) -> dict:
    transcript = io.StringIO()
    with contextlib.redirect_stdout(transcript):
        owned = runpy.run_path(str(HERE / name))
    check("OWNER_REPLAY_" + name.removesuffix(".py"),
          "PASS_" in transcript.getvalue())
    return owned


def nodal_controls() -> dict:
    t, z = sp.symbols("t z")
    nodes = [j - t for j in range(7)]
    lagrange = [
        sp.prod((z - nodes[i]) / (j - i) for i in range(7) if i != j)
        for j in range(7)
    ]
    moments = 0
    bounds = []
    for derivative in range(7):
        weights = [
            sp.expand(sp.diff(p, z, derivative).subs(z, 0))
            for p in lagrange
        ]
        bounds.append(str(sum(
            sum(abs(c) for c in sp.Poly(w, t).all_coeffs()) for w in weights
        )))
        for degree in range(7):
            value = sp.expand(sum(
                w * n**degree for w, n in zip(weights, nodes)
            ))
            expected = math.factorial(degree) if degree == derivative else 0
            if value != expected:
                raise AssertionError("translated reconstruction moment")
            moments += 1
    check("ALL_49_TRANSLATED_RECONSTRUCTION_MOMENTS", moments == 49)
    vandermonde_det = math.prod(
        j - i for i in range(7) for j in range(i + 1, 7)
    )
    check("NODE_DETERMINANT_INDEPENDENT_OF_TRANSLATION",
          vandermonde_det == 24883200)

    # Independent total-degree construction. N_beta(alpha)=prod binom(alpha,beta)
    # is triangular by total degree and equals 1 on the diagonal.
    simplex = sorted(
        (a for a in product(range(7), repeat=4) if sum(a) <= 6),
        key=lambda a: (sum(a), a),
    )
    check("FOUR_DIMENSIONAL_TOTAL_DEGREE_SIX_NODES",
          len(simplex) == math.comb(10, 4) == 210)
    for i, alpha in enumerate(simplex):
        for j, beta in enumerate(simplex):
            value = math.prod(
                math.comb(a, b) if b <= a else 0
                for a, b in zip(alpha, beta)
            )
            if (i < j and value != 0) or (i == j and value != 1):
                raise AssertionError("Newton simplex unisolvence")
    check("NEWTON_SIMPLEX_UNIT_TRIANGULAR_UNISOLVENCE", True)

    missing_node_kernel = sp.prod(z - (j - t) for j in range(6))
    check("HOSTILE_SIX_NODES_LEAVE_A_DEGREE_SIX_KERNEL",
          missing_node_kernel.subs({z: 0, t: sp.Rational(1, 2)}) != 0
          and all(missing_node_kernel.subs(z, j - t) == 0 for j in range(6)))
    return {
        "translated_moments": moments,
        "tensor_coordinate_nodes": 7,
        "simplex_total_degree": 6,
        "simplex_node_count": len(simplex),
        "simplex_newton_determinant": 1,
        "one_dimensional_vandermonde_determinant": vandermonde_det,
        "derivative_weight_bounds_on_t_0_1": bounds,
    }


def uv_kernel_controls() -> dict:
    z = sp.symbols("z", nonzero=True)
    symbol = 1 + (z + 1 / z) / 2
    check("TOY_FROZEN_BLOCK_IS_INVERTIBLE", symbol.subs(z, 1) == 2)
    check("TOY_FULL_OPERATOR_HAS_A_UV_KERNEL", symbol.subs(z, -1) == 0)
    # This is the Euler stencil of
    # sum_x(a_x^2/2 + a_x a_(x+1)/2 + q_x a_x) at q=0.
    # Its scalar metric/source readout is a_x. It is not the A4D action.
    ledgers = []
    for L in (4, 8, 12, 16):
        h = F(1, L)
        for R in (6, 7):
            a = [h**R * (-1)**x for x in range(L)]
            residual = [
                a[x] + (a[(x + 1) % L] + a[(x - 1) % L]) / 2
                for x in range(L)
            ]
            check(f"TOY_EXACT_ALL_SITE_STATIONARITY_L{L}_R{R}",
                  not any(residual))
            raw = L**3 * sum(abs(x) for x in a) / h**2
            check(f"TOY_RAW_THRESHOLD_L{L}_R{R}", raw == h**(R - 6))
            ledgers.append({
                "L": L, "amplitude": str(h**R), "R": R,
                "raw_normalized_readout": str(raw),
            })
    return {
        "variational_stencil": "1+(z+z^-1)/2",
        "zero_phase_block": 2,
        "uv_character": "-1",
        "extension": "h^R*cos(pi*y1/h)",
        "derivative_scaling": "C^j scales as pi^j*h^(R-j)",
        "scope": "general-stencil inference control, not an A4D witness",
        "exact_mesh_ledgers": ledgers,
    }


def native_controls() -> dict:
    def composed(x: int, fine: int, coarse: int) -> int:
        for target in range(fine - 1, coarse - 1, -1):
            x %= target
        return x

    image = [composed(x, 8, 4) for x in range(8)]
    check("ACTUAL_CONSECUTIVE_ROLE_COMPOSITION",
          image == [0, 1, 2, 3, 0, 0, 0, 0])
    sign = lambda x: 1 if x % 4 in (0, 1) else -1
    check("PERIOD_FOUR_OPPOSITE_SIGNS_HAVE_SAME_IMAGE",
          image[0] == image[6] and sign(0) == -sign(6))
    check("EXACT_PROFILE_COHERENCE_FORCES_ZERO",
          sp.Matrix([[1, -1], [-1, -1]]).det() != 0)
    check("DISTINGUISHABLE_COHERENT_THREADS",
          all(composed(c, L, 2) == c
              for L in range(3, 25) for c in (0, 1)))

    # Fin(5^4) flat-record modulus and product-of-coordinate modulus differ.
    flat_index = 5**3
    encoded_coarse = flat_index % 4**4
    decoded = tuple((encoded_coarse // 4**j) % 4 for j in range(4))
    check("EQUAL_CARDINALITY_DOES_NOT_IDENTIFY_POINT_MAPS",
          decoded == (1, 3, 3, 1) and decoded != (0, 0, 0, 1))
    for L in (4, 8, 12):
        coarse_amplitude, fine_amplitude = F(1, L**4), F(1, (L + 1)**4)
        check(f"KAPPA_LOCAL_VS_RAW_L{L}",
              coarse_amplitude + fine_amplitude <= 2 * coarse_amplitude
              and L**4 * coarse_amplitude == 1)
    return {
        "role_composition_8_to_4": image,
        "coherent_distinct_threads": [0, 1],
        "fine_point": [0, 0, 0, 1],
        "flat_record_image_5_to_4": list(decoded),
        "role_product_image_5_to_4": [0, 0, 0, 1],
        "approximate_profile": "L^-4*sigma",
        "local_residue_bound": "2*L^-4",
        "raw_sum": 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="explicit output; default verifies immutable pinned JSON")
    args = parser.parse_args()
    ir = replay_owner(INPUTS[0])
    direct = replay_owner(INPUTS[1])
    check("OWNED_ALL_SOLDER_CONGRUENCE",
          all(sp.expand(x) == 0 for x in ir["identity"]))
    check("PHYSICAL_ZERO_PHASE_TRANSPOSE_AGREES",
          ir["h0"].T == ir["h0"] and ir["h0"].det() == 256)
    monomials = [direct["d"][a] * direct["d"][b]
                 for a, b in combinations_with_replacement(range(4), 2)]
    difference = direct["K"] + direct["K_G"] / 2
    coefficients = [
        sp.Poly(x, *direct["d"]).coeff_monomial(m)
        for x in difference for m in monomials
    ]
    check("ALL_1000_NORMAL_J2_EINSTEIN_COEFFICIENTS",
          len(coefficients) == 1000 and not any(coefficients))
    result = {
        "schema": "a4d-regular-stationary-germ-canonicity-v1",
        "input_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in INPUTS
        },
        "all_solder_zero_phase_determinant": 256,
        "normal_j2_coefficient_count": len(coefficients),
        "nodal": nodal_controls(),
        "uv_threshold": uv_kernel_controls(),
        "native_interfaces": native_controls(),
        "analytic_theorem": {
            "hypotheses": "fixed smooth nondegenerate solder; small log chart; uniform C^R extensions",
            "mesh_error": "e_h=max_x |E_K(x)|",
            "log_comparison": "C_R*(e_h+h^R)",
            "raw_response_comparison": "C_R*(h^-6*e_h+h^(R-6))",
            "exact_C7_corollary": "O(h)",
            "exact_Cinfinity_corollary": "O(h^infinity)",
            "proof_owner": "A4D_CANONICAL_CONSTITUTIVE_GERM_SYNTHESIS.md",
            "scope": "analytic proof, not inferred from finite examples",
        },
        "parent_terminal": "PARTIAL / OPEN; no native UV transfer or general exact source lift",
    }
    if args.output is not None:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", args.output, flush=True)
    else:
        check("PINNED_JSON_REPLAY", result == json.loads(OUT.read_text()))
    print("A4D-REGULAR-STATIONARY-GERM-FINITE-CONTROLS-PASS", flush=True)


if __name__ == "__main__":
    main()
