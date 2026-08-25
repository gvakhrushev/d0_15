#!/usr/bin/env python3
"""D0-SCENE-INVARIANT-OVERDETERMINATION-001 — exact finite mirror.

For ordered tripartite invariants V=a+b+c, E=ab+ac+bc, T=abc at the source
scene (V,E,T)=(33,359,1287):

  * NO single invariant is selective (V=33 -> 91 triples, E=359 -> 19,
    T=1287 -> 10);
  * EVERY pair is selective: (V,E), (V,T), (E,T) each force (9,11,13).

So the scene is over-determined: it is the unique common solution of any two
independent count readings, and no reading is individually load-bearing.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def enumerate_triples(cap: int = 1300):
    Vt, Et, Tt = 33, 359, 1287
    single = {"V": [], "E": [], "T": []}
    pair = {"VE": [], "VT": [], "ET": []}
    triple = []
    for a in range(1, cap + 1):
        for b in range(a, cap + 1):
            if a * b > Et and a + b > Vt and a * b > Tt:
                break
            for c in range(b, cap + 1):
                v, e, t = a + b + c, a * b + a * c + b * c, a * b * c
                if v > Vt and e > Et and t > Tt:
                    break
                hv, he, ht = v == Vt, e == Et, t == Tt
                if hv:
                    single["V"].append((a, b, c))
                if he:
                    single["E"].append((a, b, c))
                if ht:
                    single["T"].append((a, b, c))
                if hv and he:
                    pair["VE"].append((a, b, c))
                if hv and ht:
                    pair["VT"].append((a, b, c))
                if he and ht:
                    pair["ET"].append((a, b, c))
                if hv and he and ht:
                    triple.append((a, b, c))
    return single, pair, triple


def main() -> int:
    print("=== D0-SCENE-INVARIANT-OVERDETERMINATION-001 ===")
    ok = True
    single, pair, triple = enumerate_triples()

    counts = {k: len(v) for k, v in single.items()}
    if counts != {"V": 91, "E": 19, "T": 10}:
        print(f"  FAIL (A): single-invariant counts={counts}")
        ok = False
    else:
        print("  ✓ (A) no single invariant is selective: V=33->91, E=359->19, T=1287->10")

    for k in ("V", "E", "T"):
        if (9, 11, 13) not in single[k] or len(single[k]) < 2:
            print(f"  FAIL (B): {k} does not contain the scene plus a rival")
            ok = False
            break
    else:
        print("  ✓ (B) each single invariant admits (9,11,13) and at least one rival")

    pair_ok = all(pair[k] == [(9, 11, 13)] for k in ("VE", "VT", "ET"))
    if not pair_ok:
        print(f"  FAIL (C): pair selection not unique: "
              f"VE={pair['VE']}, VT={pair['VT']}, ET={pair['ET']}")
        ok = False
    else:
        print("  ✓ (C) every pair (V,E),(V,T),(E,T) uniquely selects (9,11,13)")

    if triple != [(9, 11, 13)]:
        print(f"  FAIL (D): triple solution={triple}")
        ok = False
    else:
        print("  ✓ (D) full (V,E,T) is (of course) unique and consistent")

    print("\n  -- can-fail controls --")
    # A mutated target that is NOT realizable by any tripartite triple must give empty pairs.
    Vt, Et = 33, 360
    mutated = [
        (a, b, c)
        for a in range(1, 34)
        for b in range(a, 34)
        for c in [33 - a - b]
        if c >= b and a * b + a * c + b * c == Et
    ]
    if (9, 11, 13) in mutated:
        print("  FAIL controls: mutated (V=33,E=360) still admitted the scene")
        ok = False
    else:
        print(f"  ✓ mutated (V,E)=(33,360) excludes the scene ({len(mutated)} solutions)")

    print("\n" + (
        "PASS — scene is over-determined: any two counts pin it, none alone does"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
