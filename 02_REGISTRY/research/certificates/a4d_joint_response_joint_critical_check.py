#!/usr/bin/env python3
"""The joint-critical replacement for (NF) is obstructed at linear order.

Memo section 9 names the single missing identity: a joint-critical replacement
for (NF), meaning every amplitude admitted by

    E_K = 0        and        E_Q = h^2 tau

at every character and solder must have vanishing tested moment.  This
certificate asks the prior question first: does such an amplitude exist at
all on the resonant joint kernel, already at the order where the connection
equation is linear?

The first step is bookkeeping, not a theorem: a kernel direction b of
J = [H ; C] satisfies H b = 0 BY CONSTRUCTION, so the linear part of the
connection equation is automatically satisfied on the whole joint kernel. The
obstruction cannot live at order u.

It lives one order later.  On a single kernel direction the connection Euler
expands as

    E_K(u b) = u^2 * S,      S the quadratic self-interaction,

and the metric Euler as

    E_Q(u b) = u * 0 + u^2 * M(b),   M(b) the content-one response moment.

A joint-critical amplitude therefore needs S = 0.  The order-u^5 certificate
of this branch already computes S: on both defect carriers the witness
projection of the order-u^5 connection Euler is -432, a nonzero multiple of the
normalised amplitude, so S != 0 and u^2 S = 0 forces u = 0.  This certificate
makes the bookkeeping explicit and records that the two obstructions are
distinct, rather than asserting a new linear-order no-go that is false.
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
    print("  automatically, since it lies in ker H by construction.  The")
    print("  obstruction is therefore NOT at linear order.")
    print()
    print("  The obstruction is the quadratic self-interaction S.  The order-u^5")
    print("  certificate of this branch already certifies S != 0 on both defect")
    print("  carriers: the witness projection is -432, a nonzero multiple of")
    print("  the normalised amplitude, so u^2 S = 0 forces u = 0.")
    print()
    print("CONSEQUENCE: a joint-critical amplitude cannot start on these two")
    print("  carriers, and the reason is the quadratic term, not the linear")
    print("  one.  No claim is made here about other characters or solders.")
    print("TERMINAL: JOINT-CRITICAL-OBSTRUCTION-IS-QUADRATIC-NOT-LINEAR")
    print("BOUNDARY: an accessibility statement about the exact joint kernels")
    print("  of the two certified defect carriers.  It is NOT a")
    print("  smooth-background metric-response NOGO: no joint-critical sequence")
    print("  is produced, no #216 comparator gap is computed, and no response")
    print("  terminal is claimed.")


if __name__ == "__main__":
    main()
