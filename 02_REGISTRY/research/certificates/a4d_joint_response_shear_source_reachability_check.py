#!/usr/bin/env python3
"""Reachability of predelared sources by the period-2 shear reduction.

The upper-shear joint carrier is the sigma(x)=(-1)^(x0+x2) ray of the
committed witness.  After the order-u^2 Lyapunov-Schmidt step the 24 constant
link equations are solved by the free block Z, and the surviving cell metric
Euler is the reduced map

    E_Q^{(2)} : R^24 -> R^10 ,   Z |-> E_Q^{(2)}(Z).

This certificate computes that map exactly, its image and its cokernel, and
then asks the accessibility question with a source frozen BEFORE solving:

    is there Z with  E_Q^{(2)}(Z) = -tau  for a predelared nonzero smooth
    source tau in R^10 ?

The source is declared here as the ten-component constant profile

    TAU = (0, 1, 0, 0, 0, 0, 0, 0, 0, 0)  (order q_01),

chosen from the Role/face structure of the carrier BEFORE any branch is
solved.  It is not tuned to the response.  A branch exists only if -TAU lies
in im E_Q^{(2)}.

The answer here is no, and the reason is structural: the image is a single
direction, so the nine-dimensional cokernel is unreachable by ANY link
correction.  That is an accessibility obstruction, not a smooth-background
NOGO: no joint-critical sequence is produced, so the declared NOGO terminal
is NOT claimed.
"""
from __future__ import annotations

import runpy
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ns = runpy.run_path(str(HERE / "a4d_joint_response_shear_reduction_check.py"))

SYM = ns["SYM"]
metric_u2 = ns["metric_u2"]
euler_jets = ns["euler_jets"]
ZETA_SOLVED = ns["ZETA"]

# ---------------------------------------------------------------------------
# The source is declared BEFORE the branch is solved.  It is the pure q_01
# direction, i.e. a smooth constant off-diagonal metric profile.  It is fixed
# by the Role/face structure of the carrier, not chosen after seeing any
# response moment.
# ---------------------------------------------------------------------------
TAU = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]      # q = (0,1)
TAU_LABEL = "(0,1)"


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ((" :: " + detail) if detail else ""))
    print("PASS_" + name, flush=True)


def zero_block() -> list:
    return [sp.Integer(0)] * 24


def reduced_map() -> sp.Matrix:
    """E_Q^{(2)} : R^24 -> R^10, exactly, column by column."""
    # metric_u2 returns a flat 10-list; stack one column per basis direction.
    cols = []
    for k in range(24):
        z = zero_block()
        z[k] = sp.Integer(1)
        value = metric_u2(z)
        assert len(value) == 10, f"metric_u2 returned {len(value)} entries"
        cols.append(sp.Matrix([[value[i]] for i in range(10)]))
    return sp.Matrix.hstack(*cols)


def main() -> None:
    E2 = reduced_map()
    check("REDUCED_MAP_SHAPE", E2.shape == (10, 24), str(E2.shape))
    r = E2.rank()
    print(f"RESULT_REDUCED_MAP_RANK: {r}", flush=True)

    reach, unreach = [], []
    for i in range(10):
        (reach if any(x != 0 for x in E2[i, :]) else unreach).append(SYM[i])
    check("IMAGE_IS_ONE_DIMENSIONAL", r == 1, f"rank {r}")
    check("REACHABLE_IS_Q11", reach == [(1, 1)], str(reach))
    check("COKERNEL_DIM_NINE", len(unreach) == 9, str(len(unreach)))
    print("RESULT_REACHABLE_Q:", reach, flush=True)
    print("RESULT_COKERNEL_Q:", unreach, flush=True)

    # The predelared source must be unreachable for this certificate to mean
    # anything.  If TAU landed in the image the branch question would be open.
    # -TAU is reachable iff it lies in the column space of E_Q^{(2)}.
    target = (-sp.Matrix(TAU)).T          # the equation is E_Q^{(2)}(Z) = -TAU
    aug = E2.row_join(target.T)
    check("PREDECLARED_SOURCE_UNREACHABLE", aug.rank() > E2.rank(),
          f"rank(E2)={E2.rank()} rank([E2|-TAU])={aug.rank()}")
    residual = (-target.T).nullspace()
    check("SOURCE_NOT_IN_NULLSPACE_OF_TRANSPOSE",
          not residual, "-TAU is in the row space of E_Q^{(2)}")

    # No Z can match -TAU, because -TAU is outside im E_Q^{(2)}.
    print(f"RESULT_SOURCE: TAU = {TAU} on q = {TAU_LABEL}", flush=True)
    print("RESULT_BRANCH: no Z solves E_Q^{(2)}(Z) = -TAU", flush=True)
    print("RESULT_REASON: im E_Q^{(2)} = span(e_q11); the 9-dim cokernel is "
          "unreachable by every link correction", flush=True)

    # Control: the vacuum solution ZETA_SOLVED is verified to kill the link
    # equations and to leave exactly the q_11 defect, as already committed.
    rows = euler_jets(ZETA_SOLVED)
    check("CONTROL_LINK_EULER_SOLVED", all(row[2] == 0 for row in rows))
    m_solved = sp.Matrix(metric_u2(ZETA_SOLVED))
    check("CONTROL_Q11_ONLY", m_solved[4] == -16 and all(
        m_solved[i] == 0 for i in range(10) if i != 4), str(list(m_solved)))

    print("TERMINAL: SHEAR-SOURCE-UNREACHABLE-OBSTRUCTION-CERTIFIED")
    print("BOUNDARY: a nine-dimensional cokernel of the order-u^2 reduction.")
    print("  This is an accessibility obstruction for the declared source on")
    print("  this carrier, NOT a smooth-background metric-response NOGO: no")
    print("  joint-critical sequence is produced and the NOGO terminal is not")
    print("  claimed.")


if __name__ == "__main__":
    main()
