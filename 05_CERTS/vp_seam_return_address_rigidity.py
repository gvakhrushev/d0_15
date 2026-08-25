#!/usr/bin/env python3
"""D0-SEAM-RETURN-ADDRESS-RIGIDITY-001 — deterministic exact mirror.

The certificate checks the arithmetic content of the Lean owner:

  ReturnAddress(m,n) := n > 0, m/n = 12/5, m+n = 17.

It verifies that the unique positive integer address is (12,5), that the pair is
reduced, and that the fifth/twelfth return defects compose to the seventeenth
return in Q(phi), where phi^2 = phi + 1.

CAN-FAIL CONTROLS:
  * dropping m+n=17 leaves the infinite scale family (12k,5k);
  * changing the total depth to 16 rejects (12,5) and has no compatible address;
  * changing the ratio to 11/5 rejects (12,5).

HONEST SCOPE: this mirrors arithmetic address rigidity only. It does not assert
the remaining physical/semantic primitive that the seam transport must use this
reduced-angle/depth address.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from math import gcd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class QPhi:
    """Exact element a + b*phi of Q(phi), reduced by phi^2 = phi + 1."""

    a: Fraction
    b: Fraction

    def __add__(self, other: "QPhi") -> "QPhi":
        return QPhi(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "QPhi") -> "QPhi":
        return QPhi(self.a - other.a, self.b - other.b)

    def __mul__(self, other: "QPhi") -> "QPhi":
        # (a+bφ)(c+dφ) = (ac+bd) + (ad+bc+bd)φ.
        return QPhi(
            self.a * other.a + self.b * other.b,
            self.a * other.b + self.b * other.a + self.b * other.b,
        )

    def __pow__(self, exponent: int) -> "QPhi":
        if exponent < 0:
            raise ValueError("use the exact phi inverse for negative powers")
        result = ONE
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result


def qphi(a: int, b: int = 0) -> QPhi:
    return QPhi(Fraction(a), Fraction(b))


ZERO = qphi(0)
ONE = qphi(1)
PHI = qphi(0, 1)
PHI_INV = qphi(-1, 1)  # φ - 1; exactly φ⁻¹ because φ(φ-1)=1.


def addresses(depth: int, ratio_num: int = 12, ratio_den: int = 5, bound: int = 100):
    """Positive integer solutions of ratio_den*m = ratio_num*n and m+n=depth."""
    return [
        (m, n)
        for m in range(1, bound + 1)
        for n in range(1, bound + 1)
        if ratio_den * m == ratio_num * n and m + n == depth
    ]


def main() -> int:
    print("=== D0-SEAM-RETURN-ADDRESS-RIGIDITY-001 ===")
    ok = True

    exact = addresses(depth=17)
    if exact != [(12, 5)]:
        print(f"  FAIL (A): compatible addresses = {exact}, expected [(12, 5)]")
        ok = False
    else:
        print("  ✓ (A) m/n=12/5 and m+n=17 force the unique address (m,n)=(12,5)")

    if gcd(12, 5) != 1:
        print("  FAIL (B): gcd(12,5) ≠ 1")
        ok = False
    else:
        print("  ✓ (B) gcd(12,5)=1: the address ratio is reduced")

    seam_lhs = PHI_INV**5
    seam_rhs = PHI**5 - qphi(11)
    transport_lhs = PHI_INV**12
    transport_rhs = qphi(322) - PHI**12
    total_lhs = PHI_INV**17
    total_rhs = seam_rhs * transport_rhs

    identities = [
        ("φ⁻⁵ = φ⁵ − 11", seam_lhs == seam_rhs),
        ("φ⁻¹² = 322 − φ¹²", transport_lhs == transport_rhs),
        ("φ⁻¹⁷ = (φ⁵−11)(322−φ¹²)", total_lhs == total_rhs),
        ("φ⁻¹⁷ = φ⁻⁵ φ⁻¹²", total_lhs == seam_lhs * transport_lhs),
    ]
    for label, passed in identities:
        if not passed:
            print(f"  FAIL (C): {label}")
            ok = False
        else:
            print(f"  ✓ (C) exact in ℚ(φ): {label}")

    print("\n  -- can-fail controls --")
    ratio_only = [
        (m, n)
        for m in range(1, 101)
        for n in range(1, 101)
        if 5 * m == 12 * n
    ]
    expected_ratio_prefix = [(12 * k, 5 * k) for k in range(1, 9)]
    if ratio_only != expected_ratio_prefix:
        print(f"  FAIL control-no-depth: got {ratio_only}, expected {expected_ratio_prefix}")
        ok = False
    else:
        print("  ✓ control-no-depth: dropping m+n=17 leaves 8 scaled pairs in 1..100")

    depth16 = addresses(depth=16)
    if (12, 5) in depth16 or depth16:
        print(f"  FAIL control-depth: mutated depth 16 accepted {depth16}")
        ok = False
    else:
        print("  ✓ control-depth: replacing 17 by 16 destroys the address")

    ratio11 = addresses(depth=17, ratio_num=11, ratio_den=5)
    original_passes_mutated_ratio = 5 * 12 == 11 * 5
    if original_passes_mutated_ratio or (12, 5) in ratio11:
        print(f"  FAIL control-ratio: mutated ratio 11/5 accepted (12,5); solutions={ratio11}")
        ok = False
    else:
        print("  ✓ control-ratio: replacing 12/5 by 11/5 rejects (12,5)")

    print("\n" + ("PASS — seam-return address rigidity verified" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
