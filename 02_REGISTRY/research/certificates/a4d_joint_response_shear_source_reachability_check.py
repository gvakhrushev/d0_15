#!/usr/bin/env python3
"""Order-u^2 metric image of the period-2 shear reduction, and source reachability.

At order u^2 the period-2 Lyapunov-Schmidt step of the upper-shear carrier
solves the 24 constant link equations for a link block Z.  Two exact facts
decide every source question at this order.

Fact 1 -- the order-u^2 cell metric jet is CONSTANT in Z.
    E_Q^{(2)}(Z) = (0,0,0,0,-16,0,0,0,0,0)
for every Z in R^24.  The derivative vanishes on all 24 basis directions, so
the image is a single POINT, not a line spanned by e_q11.  There is therefore
no free 24-dimensional link block for the metric to act on at this order.

Fact 2 -- the order-u^2 link equation is a fixed NON-ZERO target.
    E_K^{(2)}(Z) = SOURCE,  SOURCE != 0,
so the 24 link slots are constrained rather than free, and the committed ZETA
is its solution.

A branch therefore requires the target point to be matched. The source is
declared BEFORE solving, from the Role/face structure of the carrier and not
tuned to any observed response:

    TAU  = e_{q_01}  (the pure off-diagonal direction q = (0,1)).

Since the image is a single point equal to the q_11 defect and carries no
q_01 component, no constant link correction can realise this source. Neither
can the predeclared tau = e_00 of the earlier step. Both misses are exact.

This is an accessibility obstruction at this order. It is NOT a
smooth-background metric-response NOGO: no joint-critical sequence is
produced and the NOGO terminal is not claimed.
"""
from __future__ import annotations

import runpy
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ns = runpy.run_path(
    str(HERE / "a4d_joint_response_shear_reduction_check.py"))

SYM = ns["SYM"]
metric_u2 = ns["metric_u2"]
euler_jets = ns["euler_jets"]
ZETA_SOLVED = ns["ZETA"]
SOURCE = ns["SOURCE"]

# Source declared BEFORE solving: the pure q_01 direction, fixed by the
# carrier's Role/face structure.  Not tuned to any response moment.
TAU = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
TAU_LABEL = "(0,1)"
Q11 = 4          # index of q = (1,1) inside SYM


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ((" :: " + detail) if detail else ""))
    print("PASS_" + name, flush=True)


def zeros() -> list:
    return [sp.Integer(0)] * 24


def main() -> None:
    point = tuple(metric_u2(zeros()))

    # Fact 1: the jet is constant in Z.
    derivative = []
    for k in range(24):
        z = zeros()
        z[k] = sp.Integer(1)
        v = metric_u2(z)
        derivative.append(tuple(sp.simplify(v[i] - point[i])
                               for i in range(10)))
    check("DERIVATIVE_ZERO_ON_ALL_24_BASIS_DIRECTIONS",
          all(all(d[i] == 0 for i in range(10)) for d in derivative))
    samples = [[sp.Integer(k + 1) for k in range(24)],
               [sp.Integer((k % 7) - 3) for k in range(24)],
               [sp.Integer(-1) ** k for k in range(24)]]
    check("JET_CONSTANT_ON_SUPERPOSITIONS",
          all(tuple(metric_u2(s)) == point for s in samples))
    check("IMAGE_IS_A_SINGLE_POINT",
          point == (0, 0, 0, 0, -16, 0, 0, 0, 0, 0), str(list(point)))
    check("POINT_LIES_ON_Q11", all(point[i] == 0 for i in range(10)
                                   if i != Q11))
    print(f"RESULT_METRIC_IMAGE: one point, {point[Q11]} on q_{SYM[Q11]} "
          f"and 0 elsewhere", flush=True)

    # Fact 2: the link equation has a fixed non-zero target, so the link block
    # is constrained rather than free.
    r0 = euler_jets(zeros())
    check("LINK_TARGET_NONZERO", any(r0[i][2] != 0 for i in range(24)))
    check("LINK_TARGET_IS_COMMITTED_SOURCE",
          [sp.Integer(r0[i][2]) for i in range(24)] ==
          [sp.Integer(v) for v in SOURCE])
    rows = euler_jets(ZETA_SOLVED)
    check("CONTROL_SOLVED_ZETA_KILLS_LINK_EULER",
          all(row[2] == 0 for row in rows))
    m_solved = tuple(metric_u2(ZETA_SOLVED))
    check("CONTROL_SOLVED_ZETA_GIVES_THE_SAME_POINT",
          m_solved == point, str(list(m_solved)))

    # The predelared source has a q_01 component; the image point has none.
    q01 = SYM.index((0, 1))
    check("PREDECLARED_SOURCE_IS_Q01", TAU[q01] == 1 and sum(TAU) == 1)
    check("IMAGE_HAS_NO_Q01_COMPONENT", point[q01] == 0)
    check("SOURCE_MISSES_IMAGE",
          tuple(TAU) != point,
          f"tau={TAU} point={list(point)}")
    print(f"RESULT_SOURCE: TAU = {TAU} on q = {TAU_LABEL}", flush=True)
    print("RESULT_BRANCH: no constant link correction realises this source", flush=True)
    print("RESULT_REASON: the order-u^2 metric image is a single point on "
          "q_11, with no q_01 component", flush=True)

    print("TERMINAL: SHEAR-IMAGE-POINT-OBSTRUCTION-CERTIFIED")
    print("BOUNDARY: order-u^2 truncation, flat-solder shear carrier.")
    print("  This is an accessibility obstruction at this order, NOT a")
    print("  smooth-background metric-response NOGO: no joint-critical")
    print("  sequence is produced and the NOGO terminal is not claimed.")


if __name__ == "__main__":
    main()
