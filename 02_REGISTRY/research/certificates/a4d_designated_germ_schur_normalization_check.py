#!/usr/bin/env python3
"""Cross-check the #310 normal Hessian against the independent #273 Schur symbol.

This only contracts the exact flat quadratic symbols with one pinned normal
metric Hessian. It does not construct a nonlinear smooth stationary branch or
an all-order finite-lattice Einstein operator.
"""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "a4d_y_curved_normaljet_compatibility_results.json"
OWNER = HERE / "a4d_schur_einstein_direct_identification_check.py"
OUT = HERE / "a4d_designated_germ_schur_normalization_results.json"


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print("PASS_" + label, flush=True)


# The owner reconstructs K_G independently of K_Schur and verifies all 100
# entries, their index position, and the off-diagonal factor of two.
owned = runpy.run_path(str(OWNER))
k_schur, k_einstein = owned["K"], owned["K_G"]
k = owned["d"]
slots = [(int(a), int(b)) for a, b in owned["SYM"]]
check("TEN_SYMMETRIC_COORDINATES", slots == [
    (0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
    (1, 2), (1, 3), (2, 2), (2, 3), (3, 3),
])
check("OWNED_POLYNOMIAL_SCHUR_IDENTITY",
      (k_schur + k_einstein / 2).applyfunc(sp.expand) == sp.zeros(10))

source = json.loads(SOURCE.read_text())
germ = source["normalized_surviving_curvature"]
hessian = {}
for tag, components in germ["normal_metric_hessian_nonzero"].items():
    a, b = (int(x) for x in tag[1:].split("d"))
    hessian[a, b] = sp.Matrix([sp.Rational(x) for x in components])
check("NORMAL_HESSIAN_SPATIAL_SUPPORT",
      set(hessian) == {(1, 1), (1, 2), (1, 3),
                       (2, 2), (2, 3), (3, 3)})


def evaluate_on_normal_hessian(symbol: sp.Matrix) -> sp.Matrix:
    # A polynomial in k represents a constant-coefficient second derivative
    # operator. Its k_i*k_j coefficient acts on the corresponding second
    # partial derivative, whose 10 coordinates are pinned above.
    unit = []
    for i in range(4):
        unit.append(symbol.subs({k[j]: int(i == j) for j in range(4)}))
    value = sp.zeros(10, 1)
    for (i, j), jet in hessian.items():
        coefficient = unit[i] if i == j else (
            symbol.subs({k[l]: int(l == i or l == j) for l in range(4)})
            - unit[i] - unit[j]
        )
        value += coefficient * jet
    return value.applyfunc(sp.factor)


einstein_value = evaluate_on_normal_hessian(k_einstein)
schur_value = evaluate_on_normal_hessian(k_schur)
response = sp.Matrix([sp.Rational(x) for x in germ["emergent_common_response"]])
flat_control = sp.Matrix([sp.Rational(x) for x in germ["flat_einstein_control"]])
check("CURVED_RESPONSE_MATCHES_FLAT_CONTROL", response == flat_control)
check("EINSTEIN_TENSOR_IS_TWICE_RESPONSE", einstein_value == 2 * response)
check("SCHUR_IS_NEGATIVE_RESPONSE", schur_value == -response)
check("PROPOSED_UNIT_EINSTEIN_NORMALIZATION_FAILS",
      response != einstein_value and response != -2 * schur_value)

result = {
    "schema": "a4d-designated-germ-schur-normalization-v1",
    "inputs": [SOURCE.name, OWNER.name],
    "normal_hessian_curvature": "normalized -Y tensor Y at z=1",
    "coordinate_order": [f"q{a}{b}" for a, b in slots],
    "standard_linearized_einstein_on_pinned_hessian": [str(x) for x in einstein_value],
    "flat_schur_on_pinned_hessian": [str(x) for x in schur_value],
    "phase_common_metric_response": [str(x) for x in response],
    "identity_on_this_input": "E_Q = G^(1)/2 = -K_Schur[J]",
    "hostile_claim": "E_Q = G^(1) = -2*K_Schur[J] fails by a factor of two",
    "scope": "one exact normal-Hessian input and flat linear symbols; no nonlinear finite-L operator or joint selector",
}
if OUT.exists():
    check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT, flush=True)
print("A4D-DESIGNATED-GERM-SCHUR-NORMALIZATION-AUDITED", flush=True)
