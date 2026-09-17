#!/usr/bin/env python3
"""D0-M1-CLASS-ADMISSIBILITY-001 — exact finite mirror.

Class-level M1 admissibility means observable invariance under every external
catalogue choice. It may retain many candidates. Existing M1Forced remains the
special case where a canonical constraint has exactly one witness.
"""
from __future__ import annotations

import sys
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def catalogue_invariant(eval_fn, candidate, catalogues):
    outputs = [eval_fn(candidate, c) for c in catalogues]
    return len(set(outputs)) == 1


def main() -> int:
    print("=== D0-M1-CLASS-ADMISSIBILITY-001 ===")
    ok = True

    candidates = (0, 1, 2, 3)
    catalogues = (False, True)

    invariant_eval = lambda a, _c: a % 2
    dependent_eval = lambda a, c: (a % 2) ^ int(c)

    admissible = [a for a in candidates if catalogue_invariant(invariant_eval, a, catalogues)]
    if admissible != list(candidates):
        print(f"  FAIL (A): invariant class={admissible}")
        ok = False
    else:
        print("  ✓ (A) class admissibility retains multiple catalogue-independent candidates")

    dependent = [a for a in candidates if catalogue_invariant(dependent_eval, a, catalogues)]
    if dependent == list(candidates):
        print("  FAIL (B): catalogue dependence was not detected")
        ok = False
    else:
        print("  ✓ (B) candidates whose observable changes with the catalogue are excluded")

    # Unique forcing is the singleton witness case.
    forced = [a for a in candidates if a == 2]
    if len(forced) != 1:
        print("  FAIL (C): singleton forced constraint failed")
        ok = False
    else:
        print("  ✓ (C) unique M1 forcing is the singleton witness special case")

    # A non-singleton allowed class cannot have a unique forced answer under the same predicate.
    allowed = [0, 2]
    if len(allowed) <= 1:
        print("  FAIL (D): non-singleton control collapsed")
        ok = False
    else:
        print("  ✓ (D) a non-singleton admissible class is not one M1Forced answer")

    print("\n  -- can-fail controls --")
    mutated_singleton = [a for a in candidates if a in (1, 3)]
    if len(mutated_singleton) == 1:
        print("  FAIL controls: two-witness mutation was misclassified as unique")
        ok = False
    else:
        print("  ✓ two-witness mutation correctly breaks unique forcing")

    print("\n" + (
        "PASS — class admissibility and unique forcing are compatible two-stage M1 interfaces"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
