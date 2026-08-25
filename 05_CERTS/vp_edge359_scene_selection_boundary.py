#!/usr/bin/env python3
"""D0-EDGE359-SCENE-SELECTION-NOGO-001 — exact finite mirror.

Audit question: does the edge count 359 independently select K(9,11,13)?

Answer:
  * NO: there are exactly 19 positive ordered triples a<=b<=c with
    ab+ac+bc=359, including the distinct rival (7,10,17).
  * YES after one independent repair coordinate: adding a+b+c=33 leaves the
    unique triple (9,11,13).

Therefore an alpha/edge expression that only reuses E=359 cannot independently
validate or select the scene. It is a downstream shared invariant. The pair
(V,E) is scene-selective; E alone is not.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def edge(a: int, b: int, c: int) -> int:
    return a * b + a * c + b * c


def triangle(a: int, b: int, c: int) -> int:
    return a * b * c


def edge_solutions(target: int) -> list[tuple[int, int, int]]:
    # If a<=b<=c and a,b,c>=1, then a*b < target and
    # c=(target-a*b)/(a+b); this is a complete finite enumeration.
    out: list[tuple[int, int, int]] = []
    for a in range(1, target + 1):
        for b in range(a, target + 1):
            numerator = target - a * b
            if numerator < 0:
                break
            denominator = a + b
            if numerator % denominator:
                continue
            c = numerator // denominator
            if c >= b and c >= 1:
                out.append((a, b, c))
    return out


def main() -> int:
    print("=== D0-EDGE359-SCENE-SELECTION-NOGO-001 ===")
    ok = True

    expected = [
        (1, 1, 179), (1, 2, 119), (1, 3, 89), (1, 4, 71),
        (1, 5, 59), (1, 7, 44), (1, 8, 39), (1, 9, 35),
        (1, 11, 29), (1, 14, 23), (1, 17, 19), (2, 9, 31),
        (3, 5, 43), (3, 13, 20), (4, 11, 21), (5, 7, 27),
        (5, 11, 19), (7, 10, 17), (9, 11, 13),
    ]
    solutions = edge_solutions(359)
    if solutions != expected:
        print(f"  FAIL (A): edge-359 solutions={solutions}")
        ok = False
    else:
        print("  ✓ (A) exact classification: E=359 has 19 positive ordered triples")

    source = (9, 11, 13)
    rival = (7, 10, 17)
    if edge(*source) != 359 or edge(*rival) != 359 or source == rival:
        print("  FAIL (B): source/rival edge collision not realized")
        ok = False
    else:
        print("  ✓ (B) source (9,11,13) and rival (7,10,17) both have E=359")

    if sum(source) == sum(rival) or triangle(*source) == triangle(*rival):
        print("  FAIL (C): rival failed to differ in V/T")
        ok = False
    else:
        print(f"  ✓ (C) rival differs: V={sum(rival)} vs 33; "
              f"T={triangle(*rival)} vs {triangle(*source)}")

    ve = [x for x in solutions if sum(x) == 33]
    if ve != [source]:
        print(f"  FAIL (D): (V,E)=(33,359) solutions={ve}")
        ok = False
    else:
        print("  ✓ (D) adding independent V=33 repairs uniqueness: only (9,11,13)")

    # The alpha-top structural form depends on the scene only through E:
    # fingerprint (coefficient of phi^-2, coefficient of phi^-5).
    alpha_fingerprints = {(edge(*x), -1) for x in solutions}
    if alpha_fingerprints != {(359, -1)}:
        print(f"  FAIL (E): edge-alpha fingerprints vary={alpha_fingerprints}")
        ok = False
    else:
        print("  ✓ (E) every E=359 rival has the same edge-alpha structural fingerprint")

    print("\n  -- can-fail controls --")
    mutated = edge_solutions(360)
    mutated_ve = [x for x in mutated if sum(x) == 33]
    if mutated == expected or mutated_ve == [source]:
        print("  FAIL controls: edge-target mutation was not detected")
        ok = False
    else:
        print(f"  ✓ changing target to E=360 changes the fibre ({len(mutated)} solutions)")
        print("  ✓ the source no longer passes the mutated (V,E) selector")

    print("\n" + (
        "PASS — 359 is a shared downstream invariant, not an independent scene selector"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
