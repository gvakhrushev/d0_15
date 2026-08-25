#!/usr/bin/env python3
"""D0-TRANSPORT-SPLITTING-FIELD-NOGO-001 — no golden content in the FULL splitting field of
the transport cubic lambda^3 - 359*lambda - 2574: the discriminant obstruction.

Owner-edge structure: the arithmetic legs (discriminant value, factorization, two modular
non-squareness certificates, the kernel positive control) are exact and Lean-owned
(D0.Synthesis.TransportSplittingFieldObstruction, clean axioms). The classification step —
irreducible cubic + non-square disc => Gal = S3 => the splitting field K has EXACTLY ONE
quadratic subfield Q(sqrt(disc)) — is the named EXTERNAL owner edge (standard Galois theory
of cubics; Dummit-Foote, Abstract Algebra 3e, sec. 14.6-14.7; Cox, Galois Theory, ch. 7).
Irreducibility itself is Lean-owned (TransportFieldNoGolden.Pcubic_irreducible).

Conclusion at maximal scope: sqrt(5) not in K, hence phi not in K — NO rational-coefficient
rational function of ALL THREE transport eigenvalues jointly produces any golden quantity.
The class is exhausted BY CONSTRUCTION (every such function lies in K). Upgrades
D0-TRANSPORT-FIELD-NO-GOLDEN-001 (single-eigenvalue fields) to the joint closure, discharging
its own named next step ("the splitting-field statement is a possible further step, not
claimed").
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

P, Q = -359, -2574  # x^3 + P x + Q


def disc_cubic(p: int, q: int) -> int:
    return -4 * p ** 3 - 27 * q ** 2


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def squarefree_kernel(n: int) -> int:
    k, d, m = 1, 2, abs(n)
    while d * d <= m:
        e = 0
        while m % d == 0:
            m //= d
            e += 1
        if e % 2:
            k *= d
        d += 1
    return k * m * (1 if n >= 0 else -1)


def has_rational_root(p: int, q: int) -> bool:
    # rational root theorem for monic integer cubic: any rational root is an integer divisor of q
    if q == 0:
        return True
    for d in range(1, abs(q) + 1):
        if abs(q) % d == 0:
            for s in (d, -d):
                if s ** 3 + p * s + q == 0:
                    return True
    return False


def main() -> int:
    print("=== D0-TRANSPORT-SPLITTING-FIELD-NOGO-001  discriminant obstruction: no golden content in K ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: criterion fixed first — irreducible cubic + nonsquare disc "
          "=> Gal = S3 => unique quadratic subfield Q(sqrt(disc)); Q(sqrt(disc)) = Q(sqrt(5)) iff "
          "5*disc is a rational square; all arithmetic exact, controls on both sides")

    disc = disc_cubic(P, Q)
    assert disc == 6185264 == -4 * P ** 3 - 27 * Q ** 2
    print(f"PASS_DISC_VALUE  disc(x^3 {P:+d}x {Q:+d}) = {disc}  (matches the owned "
          "discriminant_positive value at D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001)")

    assert not has_rational_root(P, Q)
    print("PASS_IRREDUCIBLE  no rational root (full divisor sweep of 2574, both signs) — "
          "Lean owner: TransportFieldNoGolden.Pcubic_irreducible")

    assert disc == 2 ** 4 * 193 * 2003
    for pr in (193, 2003):
        assert all(pr % d for d in range(2, math.isqrt(pr) + 1))
    kern = squarefree_kernel(disc)
    assert kern == 386579 == 193 * 2003
    print(f"PASS_FACTORIZATION  disc = 2^4 * 193 * 2003; squarefree kernel = {kern} = 193*2003 "
          "(both prime)")

    assert not is_square(disc)
    assert disc % 9 == 5 and sorted({(i * i) % 9 for i in range(9)}) == [0, 1, 4, 7]
    print("PASS_DISC_NOT_SQUARE  disc = 5 mod 9, squares mod 9 = {0,1,4,7} -> Gal = S3, [K:Q] = 6, "
          "K has EXACTLY ONE quadratic subfield Q(sqrt(disc)) [external owner edge]")

    assert not is_square(5 * disc)
    assert (5 * disc) % 7 == 5 and sorted({(i * i) % 7 for i in range(7)}) == [0, 1, 2, 4]
    print("PASS_FIVE_DISC_NOT_SQUARE  5*disc = 5 mod 7, squares mod 7 = {0,1,2,4} -> "
          "Q(sqrt(disc)) != Q(sqrt(5)) -> sqrt(5) not in K -> phi not in K")

    # ---- POSITIVE CONTROL: the same test CONFIRMS the kernel that IS in K -------------------
    assert is_square(disc * kern) and disc * kern == 1546316 ** 2
    print("FAIL_KERNEL_CONFIRMED  disc * 386579 = 1546316^2 IS a square: the machinery confirms "
          "sqrt(386579) in K (as sqrt(disc) always is) while refusing sqrt(5) — it distinguishes, "
          "not blanket-rejects")

    # ---- NEGATIVE CONTROLS (the criterion can fail the CONCLUSION) --------------------------
    # control 1: a cubic where the S3 step FAILS — x^3 - 3x - 1 has disc 81 = 9^2 (cyclic A3,
    # no quadratic subfield at all); the criterion correctly does NOT fire its S3 branch.
    c1 = disc_cubic(-3, -1)
    assert c1 == 81 and is_square(c1) and not has_rational_root(-3, -1)
    print("FAIL_A3_CONTROL  x^3-3x-1: disc = 81 = 9^2 (square) -> A3 route, S3 classification "
          "does NOT apply — the disc test can fail")

    # control 2: a cubic whose splitting field DOES contain sqrt(5) — search the coefficient box
    # for an irreducible monic cubic with squarefree kernel exactly 5; the 5*disc test must PASS
    # there (i.e. 5*disc a square), showing the field-distinction step can fail.
    found = None
    for p in range(-60, 61):
        for q in range(-60, 61):
            if q == 0:
                continue
            d = disc_cubic(p, q)
            if d != 0 and not has_rational_root(p, q) and squarefree_kernel(d) == 5:
                found = (p, q, d)
                break
        if found:
            break
    assert found is not None, "no golden-subfield control cubic found in the search box"
    fp, fq, fd = found
    assert is_square(5 * fd)
    print(f"FAIL_GOLDEN_SUBFIELD_CONTROL  x^3 {fp:+d}x {fq:+d}: disc = {fd}, kernel 5, "
          "5*disc IS a square -> that splitting field CONTAINS Q(sqrt(5)) — the distinction "
          "test can fail; the transport cubic is on the other side")

    print("HONEST_OWNER_EDGE  classification steps (S3 from nonsquare disc; unique quadratic "
          "subfield) are the named external owner edge (Dummit-Foote 14.6-14.7 / Cox ch.7); "
          "irreducibility + all arithmetic Lean-owned; scope: rational-coefficient functions of "
          "the transport eigenvalues (exhausted by K); other operator families untouched; no "
          "door adjudicated; (gamma) not owned")
    print("PASS_TRANSPORT_SPLITTING_FIELD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
