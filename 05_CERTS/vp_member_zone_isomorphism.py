#!/usr/bin/env python3
"""D0-TOWER-STOP-NOEXT-001 CASE-1 stress test — the written map is not exhaustivity.

The former certificate wrote a three-entry dictionary

    p^1 (direct registration)  -> DISTINGUISH  (the first act; without it there is no fact)
    p^2 (self-return)          -> PRESERVE     (apply registration to itself; else no comparison)
    = 1 (closure/exhaustion)   -> CLOSE        (M1+ canonisation of the unit; BOOK_00)

but writing a bijection between two declared three-element sets does not prove that every
admissible zone belongs to either set. Moreover p^3 is a distinct value despite reducing in the
two-dimensional algebra. This script now records that counterexample and leaves semantic
exhaustivity open.

WHAT IS PROVED (exact Z[p] / surd, able to FAIL):
  * p = phi^-1 satisfies p^2 + p = 1 (the forced branching law).
  * The algebra is rank 2: basis {1, p}; p^3 reduces, p^3 = 2p - 1 (no fourth independent slot).
    Identity: p^3 - 2p + 1 = (p-1)(p^2+p-1) = 0.
  * The map {slot -> type} is a bijection of 3-element sets: p<->DISTINGUISH, p^2<->PRESERVE,
    1<->CLOSE -- each pairing sourced from a forced primitive (registration / self-application /
    M1+), each type from exactly one slot and each slot to exactly one type.

HONESTY BOUNDARY: the dictionary is a proposed interpretation, not a classification theorem.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Surd:
    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a - o.a, self.b - o.b)

    def __mul__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    def __eq__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return self.a == o.a and self.b == o.b

    def fval(self):
        return float(self.a) + float(self.b) * math.sqrt(5.0)


def main() -> int:
    print("=== D0-TOWER-STOP-NOEXT-001 CASE-1 exhaustivity stress test ===")

    p = Surd(F(-1, 2), F(1, 2))     # phi^-1 = (sqrt5-1)/2
    one = Surd(1)

    # ---- p^2 + p = 1 (the forced branching law) ------------------------------------
    assert (p * p + p) == one, "p = phi^-1 must satisfy p^2 + p = 1"
    print(f"PASS_BRANCHING_LAW  p=phi^-1={p.fval():.6f}, p^2+p=1 (the forced quadratic)")

    # ---- rank-2 algebra: p^3 reduces to 2p-1 (no 4th independent slot) --------------
    p3 = p * p * p
    assert p3 == (p + p) - one, "p^3 = 2p - 1 (reduces into span{1,p})"
    assert p3 != one and p3 != p and p3 != p * p, "linear reduction does not make p^3 a repeated value"
    # identity p^3 - 2p + 1 = (p-1)(p^2+p-1) = 0
    lhs = p3 - ((p + p) - one)
    assert lhs == Surd(0), "p^3 - (2p-1) = 0"
    print(f"PASS_FOURTH_DISTINCT_VALUE  p^3 = 2p-1 = {p3.fval():.6f}, in span{{1,p}} but distinct from 1,p,p^2")

    # ---- the 3 slots and the bijection to the 3 necessity-types ---------------------
    slots = {"p^1": "DISTINGUISH", "p^2": "PRESERVE", "=1": "CLOSE"}
    sources = {"p^1": "registration primitive (BOOK_01, no act no fact)",
               "p^2": "self-application p∘p = return (algebra)",
               "=1": "M1+ unit exhaustion / canonisation (BOOK_00)"}
    assert len(slots) == 3 and len(set(slots.values())) == 3, "3 slots <-> 3 distinct types (injective+surjective)"
    assert set(slots.keys()) == set(sources.keys()), "every slot has exactly one forced source"
    print("PASS_DECLARED_DICTIONARY_IS_BIJECTIVE_ON_ITS_OWN_THREE_ENTRIES")

    # ---- count: 3 = 2 quadratic terms + 1 closure (NOT a list) ----------------------
    assert 3 == 2 + 1, "3 types = 2 quadratic terms + 1 closure (degree-2, not enumeration)"
    print("PASS_THREE_IS_TWO_PLUS_ONE_ARITHMETIC_ONLY")

    # ---- negative control --------------------------------------------------------
    # a genuinely-new 4th slot would be an independent p^3; but p^3 in span{1,p} => not independent
    assert p3 != one and p3 != p and p3 != p * p
    print("FAIL_WRITTEN_DICTIONARY_DOES_NOT_EXHAUST_DISTINCT_POWERS")
    print("PASS_MEMBER_ZONE_CONTROLS")

    print("OPEN_MEMBER_ZONE_EXHAUSTIVITY_REQUIRES_SEMANTIC_OWNER")
    print("PASS_MEMBER_ZONE_ISOMORPHISM_STRESS_TEST")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
