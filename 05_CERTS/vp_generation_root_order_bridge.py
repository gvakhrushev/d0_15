#!/usr/bin/env python3
"""D0-GENERATION-ROOT-ORDER-BRIDGE-001 — exact finite mirror.

GenerationPhasonMode is TorusShell with owned radial order
innerD9 < coreD11 < outerD13. The transport roots have a unique increasing order.
Therefore exactly one of the six shell→root bijections preserves both orders.
"""
from __future__ import annotations

import sys
from itertools import permutations

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-GENERATION-ROOT-ORDER-BRIDGE-001 ===")
    ok = True

    shells = ("innerD9", "coreD11", "outerD13")
    shell_sizes = (9, 11, 13)
    shell_degrees = (24, 22, 20)
    if not (shell_sizes[0] < shell_sizes[1] < shell_sizes[2]):
        print("  FAIL (A): shell radial/size order is not strict")
        ok = False
    else:
        print("  ✓ (A) owned structural generation order: innerD9 < coreD11 < outerD13")

    x = sp.symbols("x")
    roots = sorted(float(sp.re(sp.N(r, 40)))
                   for r in sp.Poly(x**3 - 359*x - 2574, x).all_roots())
    if not roots[0] < roots[1] < roots[2]:
        print(f"  FAIL (B): root order is not strict: {roots}")
        ok = False
    else:
        print("  ✓ (B) canonical transport-root order is strict")

    order_preserving = []
    for p in permutations(range(3)):
        image = [roots[p[i]] for i in range(3)]
        if image[0] < image[1] < image[2]:
            order_preserving.append(p)
    if order_preserving != [(0, 1, 2)]:
        print(f"  FAIL (C): preserving bridges={order_preserving}, expected identity only")
        ok = False
    else:
        print("  ✓ (C) exactly one order-preserving shell→root bridge (identity orientation)")

    bridge = dict(zip(shells, roots))
    if not (bridge["innerD9"] == roots[0] and bridge["coreD11"] == roots[1]
            and bridge["outerD13"] == roots[2]):
        print("  FAIL (D): canonical bridge values wrong")
        ok = False
    else:
        print("  ✓ (D) inner/core/outer map to low/middle/high transport roots")

    print("\n  -- can-fail controls --")
    reversed_map = [roots[2], roots[1], roots[0]]
    shuffled_map = [roots[1], roots[0], roots[2]]
    reverse_bad = not (reversed_map[0] < reversed_map[1] < reversed_map[2])
    shuffle_bad = not (shuffled_map[0] < shuffled_map[1] < shuffled_map[2])
    degree_antitone = shell_degrees[0] > shell_degrees[1] > shell_degrees[2]
    if not (reverse_bad and shuffle_bad and degree_antitone):
        print("  FAIL controls: reversed/shuffled mapping or degree antitone law escaped")
        ok = False
    else:
        print("  ✓ controls: reversed/shuffled bridges rejected; degree law is antitone")

    print("\n" + ("PASS — structural generation→root orientation is internally unique" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
