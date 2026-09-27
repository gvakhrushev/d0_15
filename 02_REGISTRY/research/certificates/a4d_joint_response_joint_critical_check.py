#!/usr/bin/env python3
"""Linear joint-kernel bookkeeping for the two finite NF defects.

This file checks H b = C b = 0 on the joint kernel. It computes no nonlinear
Euler coefficient and proves no amplitude cutoff. The separate period-two
order-five certificates must retain their actual order and ansatz scope.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "sup", HERE / "a4d_joint_response_shear_l4_support_check.py"
)
sup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sup)

SHEAR = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0],
                   [0, 0, 1, 0], [0, 0, 0, 1]])
CHAIN = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 1],
                  [0, 0, 1, 0], [0, 0, 0, 1]])
CASES = (
    ("upper_shear", SHEAR, (sp.Integer(-1), sp.Integer(1),
                           sp.Integer(-1), sp.Integer(1))),
    ("chain", CHAIN, (sp.Integer(-1), sp.Integer(1),
                      sp.Integer(1), sp.Integer(-1))),
)


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ((" :: " + detail) if detail else ""))
    print("PASS_" + name, flush=True)


def main() -> None:
    print("  case           char                 dJ  dim ker  rank(H|ker)  O(u) E_K")
    rows = []
    for label, S, phase in CASES:
        stored = sup.brackets(S)
        units = sup.metric_units(S)
        h = sup.connection(stored, phase)
        c = sup.metric(units, [1 / z for z in phase])
        J = h.col_join(c)
        ns = J.nullspace()
        d = len(ns)
        if d == 0:
            check(f"{label.upper()}_HAS_KERNEL", False, "nullity 0")
            continue
        B = sp.Matrix.hstack(*ns)
        lin = h * B
        r = lin.rank()
        # Linear bookkeeping: the joint kernel lies in ker H by construction,
        # so the order-u connection equation is auto-satisfied.  Recording it
        # prevents the false claim that the obstruction is at linear order.
        check(f"{label.upper()}_LINEAR_EK_AUTOMATIC", r == 0,
              f"rank(H|ker) = {r}, expected 0")
        check(f"{label.upper()}_KERNEL_IN_KER_H", (h * B).is_zero_matrix)
        # The metric linearisation is recorded but not used as a terminal.
        met = c * B
        rows.append({"case": label, "character": [str(x) for x in phase],
                     "joint_nullity": d, "rank_H_on_kernel": r,
                     "linear_EK_automatic": True,
                     "rank_metric_on_kernel": met.rank()})
        print(f"  {label:<14} {str(phase):<20} {J.rank():>3} {d:>8} "
              f"{r:>13}  auto (kernel in ker H)", flush=True)

    check("BOTH_KERNELS_SATISFY_LINEAR_EK_AUTOMATICALLY",
          all(r["linear_EK_automatic"] for r in rows) and len(rows) == 2)

    print()
    print("RESULT: the joint kernel satisfies the order-u connection equation")
    print("  automatically, since it lies in ker H by construction.")
    print("TERMINAL: JOINT-KERNEL-LINEAR-EULER-IDENTITY")
    print("BOUNDARY: no nonlinear Euler coefficient is computed in this file.")
    print("  In particular an order-u^5 obstruction is not a quadratic one.")
    print("  See the separate certificates for their precise period-two scope.")


if __name__ == "__main__":
    main()
