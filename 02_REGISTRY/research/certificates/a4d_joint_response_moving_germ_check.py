#!/usr/bin/env python3
"""Exact moving metric-germ identity and physical block audit for PR #240.

This is a symbolic identity, not a new frequency census or a nonlinear
response-decoupling certificate.  It reuses the owned #216 Fourier symbols.
"""
from __future__ import annotations

import a4d_joint_response_nf_l4_check as nf
import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def simplify(matrix):
    return matrix.applyfunc(lambda entry: sp.cancel(sp.expand(entry)))


def main():
    z = nf.z_owner
    d = sp.Matrix([1 / t - 1 for t in z])
    q0 = d * d.T
    g = sp.Matrix([q0[a, b] for a, b in nf.QPAIRS])
    # B(z)=HAQ(z) is the owned 24x10 block.  With physical character z,
    # the connection block is HAB(z)^T, and the metric block is B(z^-1)^T.
    b = nf.metric_owner
    check("ALL_PHASE_MOVING_GERM", simplify(b * g) == sp.zeros(24, 1))
    for j in range(4):
        w = b.diff(z[j]) * g
        correction = g.diff(z[j])
        check(f"ALL_PHASE_JET_{j}",
              simplify(w + b * correction) == sp.zeros(24, 1))
    # The same exterior-algebra identity holds at these nonstandard solders.
    # The accompanying memo supplies the proof for every nondegenerate E.
    samples = {
        "DIAGONAL": sp.diag(2, 3, 5, 7),
        "SHEAR": sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0],
                            [0, 0, 1, 0], [0, 0, 0, 1]]),
        "RATIONAL": sp.Matrix([[2, 1, 0, 1], [0, 1, 1, 0],
                               [1, 0, 1, 0], [0, 0, 0, 1]]),
    }
    for label, solder in samples.items():
        row = nf.metric_symbol(solder, [1 / t for t in z], q0)
        check(label + "_ALL_PHASE_GERM", simplify(row) == sp.zeros(1, 24))

    orbits = [
        (0, 0, 1, 1), (0, 0, 1, 3), (0, 1, 1, 2),
        (1, 0, 1, 2), (1, 1, 1, 1), (1, 1, 3, 3),
        (2, 0, 1, 1), (2, 1, 1, 2), (2, 1, 2, 3),
    ]
    expected_physical = [23, 24, 24, 24, 20, 23, 24, 23, 24]
    expected_unpaired = [23, 24, 24, 24, 20, 24, 24, 24, 24]
    ranks = []
    for n, ids in enumerate(orbits):
        point = dict(zip(z, [sp.I ** j for j in ids]))
        h_table = nf.connection_owner.subs(point)
        b_here = b.subs(point)
        h_physical = h_table.T
        full = sp.BlockMatrix([
            [sp.zeros(10), sp.conjugate(b_here).T],
            [b_here, h_physical],
        ]).as_explicit()
        check(f"ORBIT_{n}_PHYSICAL_HERMITIAN",
              full == sp.conjugate(full).T)
        check(f"ORBIT_{n}_METRIC_KERNEL_LINE", nf.exact_rank(b_here) == 9)
        germ = g.subs(point).col_join(sp.zeros(24, 1))
        check(f"ORBIT_{n}_FULL_JOINT_GERM",
              simplify(full * germ) == sp.zeros(34, 1))
        physical_rank = nf.exact_rank(h_physical.row_join(b_here))
        wrong_rank = nf.exact_rank(h_table.row_join(b_here))
        check(f"ORBIT_{n}_PHYSICAL_ROW_RANK",
              physical_rank == expected_physical[n])
        check(f"ORBIT_{n}_UNPAIRED_ROW_CONTROL",
              wrong_rank == expected_unpaired[n])
        # F detects the common connection kernel, not a metric stress.
        f = h_physical + sp.I * b_here * sp.conjugate(b_here).T
        check(f"ORBIT_{n}_F_KERNEL_IDENTITY",
              nf.exact_rank(f.applyfunc(sp.expand)) == physical_rank)
        ranks.append(physical_rank)
    print("PHYSICAL_ROW_RANKS", ranks, flush=True)
    print("PHYSICAL_COKERNEL_DIMS", [24 - r for r in ranks], flush=True)
    print("RESULT: C(z) q0(z)=0 and dC q0 + C dq0=0 identically.")
    print("BOUNDARY: constant-solder linear symbols; no nonlinear NOGO or CLOSED.")


if __name__ == "__main__":
    main()
