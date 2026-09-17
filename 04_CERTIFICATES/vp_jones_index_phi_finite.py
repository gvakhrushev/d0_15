#!/usr/bin/env python3
"""D0-JONES-INDEX-PHI-001 — φ is forced as the n=5 Jones index value (finite shadow).

Finite-core reduction owning the previously BARE assertion "why φ as a quantum dimension".
Jones' subfactor index theorem (Invent. Math. 72, 1983) quantizes the index [M:N] of a type-II₁
subfactor: in the interval [1,4) the ONLY admissible values are the discrete series
`4cos²(π/n)`, n=3,4,5,…  The n=5 value is `4cos²(π/5) = φ²` — the first irrational ("golden")
member, and the squared quantum dimension `d_τ = φ` of the Fibonacci category (the unique
unitary modular tensor category with one non-trivial simple object of dimension > 1).

WHAT IS PROVED (exact, able to FAIL):
  * VALUE.  `φ² = 4cos²(π/5) = (3+√5)/2` — checked both as an exact element of Z[√5]
    (squaring the surd φ = ½+½√5) and numerically against the trig value to 1e-12.
  * SERIES.  the quantized series `4cos²(π/n)` for n=3,4,5,6 is `1, 2, φ², 3` — n=5 is the
    FIRST non-integer (n=3,4 give integers 1,2; n=6 gives integer 3), i.e. φ² is the first
    genuinely "golden" quantized index.
  * FUSION.  `d_τ = φ` is the positive root of the Fibonacci fusion relation `x² = x + 1`
    (`τ⊗τ = 1 ⊕ τ`); the other root ψ = (1−√5)/2 < 0 is rejected (a quantum dimension is ≥ 1).

HONESTY BOUNDARY (printed, not hidden):
  * This closes the n=5 VALUE = φ² exactly. The Jones quantization OBSTRUCTION itself (that no
    index value in the open interval (1,4) exists OTHER than the 4cos²(π/n) series) is the
    external classical theorem — owner ASSUMP-JONES-INDEX — and stays EXTERNAL. We do not
    re-prove Jones; we certify that the D0-forced φ sits exactly at its forced n=5 slot.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Surd:
    """Exact element a + b·√5 with rational a, b (ring Z[√5] ⊗ Q)."""

    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a + o.a, self.b + o.b)

    def __mul__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        # (a+b√5)(c+d√5) = (ac+5bd) + (ad+bc)√5
        return Surd(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    def __eq__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return self.a == o.a and self.b == o.b

    def __repr__(self):
        return f"{self.a}+{self.b}√5"

    def float(self):
        return float(self.a) + float(self.b) * math.sqrt(5.0)


def jones_value(n: int) -> float:
    """The Jones index value 4cos²(π/n) (the admissible value in [1,4) for integer n≥3)."""
    return 4.0 * math.cos(math.pi / n) ** 2


def main() -> int:
    print("=== D0-JONES-INDEX-PHI-001  φ forced as the n=5 Jones index value ===")

    phi = Surd(F(1, 2), F(1, 2))             # (1+√5)/2
    psi = Surd(F(1, 2), F(-1, 2))            # (1−√5)/2
    phi_sq = phi * phi
    golden = Surd(F(3, 2), F(1, 2))          # (3+√5)/2

    # ---- VALUE: φ² = (3+√5)/2 exactly, and = 4cos²(π/5) numerically ----------------
    assert phi_sq == golden, f"φ² != (3+√5)/2 exactly: {phi_sq}"
    assert phi_sq == phi + 1, f"φ² != φ+1 (golden relation): {phi_sq} vs {phi + Surd(1)}"
    assert abs(phi_sq.float() - jones_value(5)) < 1e-12, "φ² != 4cos²(π/5) numerically"
    print(f"PASS_N5_VALUE_IS_PHI_SQ  4cos²(π/5) = φ² = (3+√5)/2 = {phi_sq.float():.12f}")

    # ---- SERIES: 4cos²(π/n) for n=3,4,5,6 = 1,2,φ²,3; n=5 first non-integer ---------
    series = {n: jones_value(n) for n in (3, 4, 5, 6)}
    assert abs(series[3] - 1.0) < 1e-12, "n=3 should give 1"
    assert abs(series[4] - 2.0) < 1e-12, "n=4 should give 2"
    assert abs(series[6] - 3.0) < 1e-12, "n=6 should give 3"
    assert abs(series[5] - phi_sq.float()) < 1e-12, "n=5 should give φ²"
    # n=5 is the FIRST non-integer member
    assert abs(series[3] - round(series[3])) < 1e-12 and abs(series[4] - round(series[4])) < 1e-12, \
        "n=3,4 must be integers"
    assert abs(series[5] - round(series[5])) > 1e-3, "n=5 must be NON-integer (the golden slot)"
    print("PASS_QUANTIZED_SERIES  4cos²(π/n)|n=3..6 = 1, 2, φ², 3 (n=5 = first golden non-integer)")

    # ---- FUSION: d_τ=φ is the positive root of x²=x+1; ψ<0 rejected -----------------
    assert phi_sq == phi + 1, "fusion relation d_τ²=d_τ+1 fails for φ"
    assert (psi * psi) == psi + 1, "ψ should also satisfy x²=x+1 (the conjugate root)"
    assert phi.float() > 1.0 > psi.float() and psi.float() < 0.0, "φ>1>ψ, ψ<0"
    print("PASS_FIBONACCI_FUSION  d_τ=φ positive root of x²=x+1 (τ⊗τ=1⊕τ); ψ<0 rejected")

    # ---- negative controls (must differ) -------------------------------------------
    assert abs(jones_value(3) - phi_sq.float()) > 0.5, "control: n=3 value (1) != φ²"
    assert abs(jones_value(7) - phi_sq.float()) > 1e-3, "control: n=7 value != φ²"
    assert (psi * psi) != golden or psi.float() < 0, "control: the rejected root ψ is negative"
    # a quantum dimension must be >= 1 — ψ cannot be a quantum dimension
    assert psi.float() < 1.0, "control: ψ < 1 cannot be a quantum dimension"
    print("FAIL_N3_VALUE_1_IS_NOT_PHI_SQ")
    print("FAIL_N7_VALUE_IS_NOT_PHI_SQ")
    print("FAIL_PSI_NEGATIVE_NOT_A_QUANTUM_DIMENSION")
    print("PASS_JONES_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_PROVES_N5_VALUE_IS_PHI_SQ_NOT_THE_JONES_QUANTIZATION_OBSTRUCTION")
    print("HONEST_JONES_NO_INDEX_IN_(1,4)_OTHER_THAN_4COS2_PI_N_STAYS_EXTERNAL_ASSUMP_JONES_INDEX")

    print("PASS_JONES_INDEX_PHI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
