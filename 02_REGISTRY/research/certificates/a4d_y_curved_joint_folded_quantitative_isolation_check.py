#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""An explicit zero-free radius and linear gap around every folded Y point.

This lightweight consequence of the exact folded graph-chart owner uses its
two pinned inverse-Frobenius bounds and the literal Laurent stencil. All
constant comparisons below are rational. The radius is deliberately
conservative; it does not cover the rest of the unit torus.
"""
from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path

import a4d_y_curved_joint_rational_stencil as S

HERE = Path(__file__).resolve().parent
CHART = json.loads((HERE / "a4d_y_curved_joint_folded_isolation_results.json").read_text())
LIP = json.loads((HERE / "a4d_y_curved_joint_torus_lipschitz_results.json").read_text())
OUT = HERE / "a4d_y_curved_joint_folded_quantitative_isolation_results.json"


def ck(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def phase(row: int) -> int:
    return row // 24 if row < 96 else (row - 96) // 10


ck("OWNED_FOLDED_GRAPH_CHART", CHART["terminal"] == "A4D-Y-CURVED-FOLDED-JOINT-LOCALLY-ISOLATED")
ck("OWNED_LIPSCHITZ_CERTIFICATE", LIP["terminal"] == "A4D-Y-CURVED-JOINT-TORUS-LIPSCHITZ-CERTIFIED")
rows = CHART["square_graph_rows"]
frows = CHART["reduced_residual_rows"]
drop = S.LABELS.index((0, 0, 3))
ck("GRAPH_COORDINATES", len(rows) == len(set(rows)) == 95 and
   len(frows) == len(set(frows)) == 4 and not set(rows).intersection(frows) and
   CHART["deleted_coordinate"] == "phase0:role0:J12")
ck("INVERSE_BOUNDS", F(CHART["square_inverse_frobenius_squared"]) < 40**2 and
   F(CHART["reduced_J4_inverse_frobenius_squared"]) < 5**2 and
   F(CHART["reduced_J4_determinant"]) != 0)
ck("DERIVATIVE_ENVELOPE", all(F(b["operator_upper_bound"]) == F(22, 7)
                              for b in LIP["coordinate_bounds"]))

# Every exponent component is -1, 0, or 1. Thus the existing entrywise
# first-derivative envelope also dominates each mixed second derivative.
aterms, qterms = S.ATERMS, S.QTERMS
ck("MIXED_DERIVATIVE_ENVELOPE", all(all(abs(v) <= 1 for v in d)
                                          for d in set(aterms) | set(qterms)))

# The coefficientwise fourth-root phase law transports the same 95-row
# chart, four residual rows, kernel vector and derivative singular values to
# all four folded characters by diagonal unitary matrices.
covariant = True
for terms, offset in ((aterms, 0), (qterms, 96)):
    for d, coeffs in terms.items():
        for (r, c), v in coeffs.items():
            if v and (phase(offset + r) - c // 24 + sum(d)) % 4:
                covariant = False
ck("FOUR_FOLDED_COPIES_UNITARILY_EQUIVALENT", covariant)

q0 = {}
for terms, offset in ((aterms, 0), (qterms, 96)):
    for coeffs in terms.values():
        for (r, c), v in coeffs.items():
            key = (offset + r, c)
            q0[key] = q0.get(key, F(0)) + v
q0 = {key: v for key, v in q0.items() if v}

v0 = [F(0)] * 96
for p, sgn in ((0, 1), (2, -1)):
    for g, val in ((3, 1), (4, -1), (5, 1)):
        v0[S.LABELS.index((p, 0, g))] = F(sgn * val)
ck("NORMALIZED_Y_KERNEL", v0[drop] == 1 and sum(x*x for x in v0) == 6 and
   all(sum(val*v0[c] for (rr, c), val in q0.items() if rr == r) == 0
       for r in range(136)))
r_frob2 = sum(val*val for (r, _c), val in q0.items() if r in frows)
ck("FOUR_RESIDUAL_ROWS_NORM_LT3", r_frob2 == F(340, 49) and r_frob2 < 9)

# Write delta = sum |theta_j-theta_j^*|. From the owned ||S0^-1||<40,
# ||J0^-1||<5 and ||d_j Q||,||d_j d_k Q||<4:
#   ||S(theta)^-1||<50, ||x(theta)-x0||<800 delta, ||x(theta)||<4;
#   ||x'_k(0)||<640, ||x'_k(theta)-x'_k(0)||<289000 delta;
#   ||F'_k(theta)-F'_k(0)||<1200000 delta.
# Here x=-S^-1 q and F is the four-row reduced graph residual. Direct
# rational checks retain every slack used in this norm calculation.
radius = F(1, 100_000_000)
ck("NEUMANN_INVERSE_50", radius <= F(1, 1000) and
   F(40) / (1 - F(40)*4*radius) < 50)
ck("GRAPH_AMPLITUDE_4", 3 + 800*radius < 4)
ck("RESIDUAL_ROW_BOUND_4", 3 + 4*radius < 4)
inverse_change = 50*4*40
graph_change = 50*4*(1 + 3)
graph_derivative_at_zero = 40*4*(1 + 3)
derivative_change = inverse_change*16 + 50*(4 + 4*3 + 4*graph_change)
residual_derivative_change = (4*3 + 4*graph_change +
                              4*graph_derivative_at_zero + 4*derivative_change)
ck("DERIVATIVE_CHAIN", graph_change == 800 and
   graph_derivative_at_zero == 640 and derivative_change == 288800 and
   residual_derivative_change == 1_160_972 and
   residual_derivative_change < 1_200_000)

# ||J0 a|| >= ||a||_1/10. Along the segment from zero to a the derivative
# error is at most 1,200,000*delta, so ||F(theta)|| > delta/20.
ck("EXPLICIT_REDUCED_GAP", F(1, 10) - 1_200_000*radius > F(1, 20))
# For u=(x,a), set e=x-x(theta)*a. Selected chart rows give
# ||e||<50||Q u||; four residual rows give
# |a|<4020*||Q u||/delta. As ||(x(theta),1)||<5,
# ||u||<(50+20100/delta)||Q u|| <=20150||Q u||/delta.
ck("EXPLICIT_FULL_JOINT_GAP", 20*(1 + 4*50) == 4020 and
   50 + 5*4020/radius <= 20150/radius)

result = {
    "schema": "a4d-y-curved-joint-folded-quantitative-isolation-v1",
    "terminal": "A4D-Y-CURVED-JOINT-FOLDED-EXPLICIT-LOCAL-GAP",
    "input_owners": [
        "a4d_y_curved_joint_rational_stencil.py",
        "a4d_y_curved_joint_torus_lipschitz_results.json",
        "a4d_y_curved_joint_folded_isolation_results.json",
    ],
    "folded_characters": ["1", "i", "-1", "-i"],
    "angular_metric": "delta=sum_j |theta_j-theta_j^*| with a local real lift",
    "radius": str(radius),
    "reduced_residual_bound": "||F(theta)||_2 > delta/20 for 0<delta<=radius",
    "full_joint_bound": "sigma_min Q(theta) > delta/20150 for 0<delta<=radius",
    "derivative_change_bound": str(residual_derivative_change),
    "residual_row_frobenius_squared_at_center": str(r_frob2),
    "scope_fence": [
        "the four explicit local neighborhoods only",
        "not an all-torus rank classification or a compact-complement gap",
        "not a nonlinear reduced-center equation or refinement-uniform response theorem",
    ],
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
print("TERMINAL", result["terminal"])
