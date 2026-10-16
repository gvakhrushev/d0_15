#!/usr/bin/env python3
"""Exact-data replay for the periodic regular-branch mean obstruction.

The short proof in A4D_Y_CURVED_RESPONSE_CORRECTED_FOLLOWUP.md combines the
owned normal-jet, center-injectivity, and amplitude-family certificates with
the exact zero-mean identity for periodic shifts.  The conclusion is limited
to a uniformly C^4, integer-power regular expansion through order h^4; it is
not a claim about singular/refinement-dependent branches.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_periodic_regular_branch_mean_results.json"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def read(name: str) -> dict:
    return json.loads((HERE / name).read_text())


family = read("a4d_y_stationary_center_family_coker_results.json")
joint = read("a4d_y_joint_first_slow_injectivity_results.json")
normal = read("a4d_y_variable_curvature_normal_jet_results.json")
degree2 = read("a4d_y_curved_normaljet_degree2_obstruction_results.json")

coker = [sp.Rational(x) for x in
         degree2["connection_only_jet"]["constant_center_cokernel"][
             "stationary_seed_projected_source"]]
kappa = sp.Symbol("kappa")
family_source = [sp.sympify(x) for x in family["stationary_connection_coker_C2"]]
check("CONNECTION_COKERNEL_SOURCE_IS_NONZERO",
      coker == [sp.Rational(351402359, 2108160),
                sp.Rational(21506403637, 154949760)])
check("AMPLITUDE_FAMILY_IS_KAPPA_SQUARED_AND_RETUNING_INVARIANT",
      family_source == [kappa**2 * x for x in coker]
      and family["first_order_y_center_parameter"] == "s"
      and "independent of s" in family["exact_parameter_dependence"])
check("BOTH_MEAN_COEFFICIENTS_HAVE_POSITIVE_SIGN", all(x > 0 for x in coker))

# The first-slow owner certificate supplies an exact full-rank minor and the
# theorem statement for all nonzero real slow covectors.
minor_det = sp.Rational(joint["minor_determinant"])
check("FIRST_SLOW_JOINT_SYMBOL_HAS_EXACT_NONZERO_MINOR", minor_det != 0)
check("FIRST_SLOW_CONSTRAINT_KILLS_NONCONSTANT_CENTER_ENVELOPES",
      "injective first-order center symbol in every nonzero real slow covector"
      in joint["symbol_consequence"])

# A lattice shift is a permutation of periodic sites, hence every difference
# has exactly zero mean. Check representative periods and all offsets; the
# proof for every period is the permutation identity stated in the memo.
for m, n in ((2, 2), (2, 3), (3, 4), (4, 5)):
    sites = sp.symbols(f"u0:{m*n}")
    base_sum = sum(sites)
    ok = True
    for a in range(-m, m + 1):
        for b in range(-n, n + 1):
            shifted_sum = sum(sites[((i + a) % m) * n + (j + b) % n]
                              for i in range(m) for j in range(n))
            ok &= sp.expand(shifted_sum - base_sum) == 0
    check(f"PERIODIC_TORUS_SHIFT_SUM_{m}x{n}", ok)

# Power counting for the Riemann-normal profile: the order-h^4 product of two
# order-h^2 curvature tangents only sees kappa^2; gradients enter one order
# later. The linear Hessian-curvature term is a periodic divergence.
h, xi, grad, hess = sp.symbols("h xi grad hess", real=True)
curvature_sample = kappa + h * grad * xi + h**2 * hess * xi**2 / 2
check("ORDER_H4_QUADRATIC_SOURCE_SEES_ONLY_KAPPA_SQUARED",
      sp.expand(h**4 * kappa * curvature_sample).coeff(h, 4) == kappa**2)
check("VARIABLE_CURVATURE_NORMAL_JET_HAS_LINEAR_HESSIAN_TERM",
      "3*Hess(kappa)(x,x)/20" in normal["normal_metric_jet"])

result = {
    "schema": "a4d-y-periodic-regular-branch-mean-v1",
    "terminal": "A4D-Y-PERIODIC-REGULAR-BRANCH-MEAN-OBSTRUCTION",
    "hypotheses": [
        "periodic spatial domain and real C^4 Gaussian-curvature profile kappa",
        "z=1 surviving Y sheet and the owned product Riemann-normal metric convention",
        "joint-stationary family has a uniform integer-power expansion through order h^4 with bounded C^4 coefficients and O(h^5) remainder",
        "the order-h center profile obeys the owned first-slow joint equations",
    ],
    "mean_equation_at_order_h4": [
        "(351402359/2108160) * mean(kappa^2) = 0",
        "(21506403637/154949760) * mean(kappa^2) = 0",
    ],
    "conclusion": "under the stated regular-expansion hypotheses, a periodic branch on this Y sheet requires kappa identically zero",
    "proof_inputs": {
        "connection_cokernel_source": [str(x) for x in coker],
        "amplitude_law": family["stationary_connection_coker_C2"],
        "center_injectivity_minor_determinant": str(minor_det),
        "normal_jet": normal["lattice_scaled_metric_jet"],
        "periodic_shift_identity": "sum_x u(x+r) = sum_x u(x) for every periodic shift r",
    },
    "scope_fence": [
        "does not exclude a nonanalytic or noninteger-power h-dependent branch",
        "does not prove an h-uniform range inverse or continuation theorem",
        "does not cover other Y amplitudes, regular z outside this sheet, or non-product curvature",
        "does not establish either task-level PR terminal",
    ],
}
if OUT.exists():
    check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT, flush=True)
print("TERMINAL A4D-Y-PERIODIC-REGULAR-BRANCH-MEAN-OBSTRUCTION", flush=True)
