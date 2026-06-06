#!/usr/bin/env python3
"""D0 information-quasicrystal phase-unfolding integration certificate."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


PASS_TOKEN = "PASS_INFORMATION_QUASICRYSTAL_PHASE_UNFOLDING"


def euler_phi(n: int) -> int:
    result = n
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1
    if x > 1:
        result -= result // x
    return result


def continued_fraction(x: float, terms: int) -> list[int]:
    out: list[int] = []
    y = x
    for _ in range(terms):
        a = math.floor(y)
        out.append(a)
        y -= a
        if abs(y) < 1e-15:
            break
        y = 1.0 / y
    return out


def convergent_from_cf(cf: list[int]) -> Fraction:
    value = Fraction(cf[-1], 1)
    for a in reversed(cf[:-1]):
        value = Fraction(a, 1) + Fraction(1, value)
    return value


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def distance_to_integer(x: float) -> float:
    return abs(x - round(x))


def locking_score(alpha: float, q_max: int) -> float:
    return min(q * distance_to_integer(q * alpha) for q in range(1, q_max + 1))


def has_small_period(seq: list[int], max_period: int) -> bool:
    n = len(seq)
    for p in range(1, max_period + 1):
        if all(seq[i] == seq[i + p] for i in range(n - p)):
            return True
    return False


def phase_residue_distribution(alpha: float, q: int, samples: int) -> dict[int, int]:
    counts = {i: 0 for i in range(q)}
    for n in range(samples):
        residue = math.floor(q * ((n * alpha) % 1.0))
        counts[residue] += 1
    return counts


def main() -> dict:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    alpha = 1.0 / (phi * phi)
    cf = continued_fraction(alpha, 18)
    convergents = [convergent_from_cf(cf[: i + 1]) for i in range(len(cf))]

    fib_checks = []
    for n in range(1, 12):
        conv = convergents[n]
        fib_checks.append(
            {
                "n": n,
                "convergent": f"{conv.numerator}/{conv.denominator}",
                "expected": f"{fibonacci(n)}/{fibonacci(n + 2)}",
                "matches": conv == Fraction(fibonacci(n), fibonacci(n + 2)),
                "q2_error": float(
                    conv.denominator
                    * conv.denominator
                    * abs(alpha - conv.numerator / conv.denominator)
                ),
            }
        )

    q_max = 2500
    rotations = {
        "phi_minus_2": alpha,
        "sqrt2_minus_1": math.sqrt(2.0) - 1.0,
        "sqrt3_minus_1": math.sqrt(3.0) - 1.0,
        "pi_minus_3": math.pi - 3.0,
        "e_minus_2": math.e - 2.0,
        "one_seventh": 1.0 / 7.0,
        "one_third": 1.0 / 3.0,
    }
    locking_scores = {
        name: locking_score(value, q_max) for name, value in rotations.items()
    }
    best_rotation = max(locking_scores, key=locking_scores.get)

    ABCD = 4
    V11 = 11
    V13 = 13
    Omega8 = 8
    V = 9 + 11 + 13
    branchB = ABCD + 1
    qT = math.lcm(ABCD, V11)
    mT = ABCD + 3
    d13 = euler_phi(qT)
    qEW = 2 * branchB * (2 * V + branchB)
    mEW = branchB * d13 + V13
    phi_qEW = euler_phi(qEW)

    terminal_orbit = [(n * mT) % qT for n in range(qT)]
    ew_orbit_prefix = [(n * mEW) % qEW for n in range(256)]
    irrational_residues = [
        math.floor(qT * ((n * alpha) % 1.0)) for n in range(512)
    ]
    distribution = phase_residue_distribution(alpha, qT, 2048)

    checks = {
        "alpha_cf_prefix": cf[:12] == [0, 2] + [1] * 10,
        "fibonacci_convergents": all(row["matches"] for row in fib_checks),
        "hurwitz_tail_close": abs(fib_checks[-1]["q2_error"] - 1 / math.sqrt(5)) < 0.02,
        "phi_minus_2_best_low_denominator_locking": best_rotation == "phi_minus_2",
        "qT": qT == 44,
        "mT": mT == 7,
        "gcd_qT_mT": math.gcd(qT, mT) == 1,
        "phi_qT": d13 == 20,
        "qEW": qEW == 710,
        "mEW": mEW == 113,
        "gcd_qEW_mEW": math.gcd(qEW, mEW) == 1,
        "phi_qEW": phi_qEW == 280,
        "ew_depth": phi_qEW == Omega8 * 35,
        "terminal_residues_full_orbit": len(set(terminal_orbit)) == qT,
        "ew_prefix_has_no_short_period": not has_small_period(ew_orbit_prefix, 32),
        "irrational_phase_no_short_period": not has_small_period(irrational_residues, 64),
        "irrational_residues_all_bins_seen": all(v > 0 for v in distribution.values()),
        "irrational_residue_distribution_not_constant": len(set(distribution.values())) > 1,
    }

    status = PASS_TOKEN if all(checks.values()) else "FAIL"
    result = {
        "status": status,
        "phi": phi,
        "alpha_phi_minus_2": alpha,
        "continued_fraction_alpha": cf,
        "fibonacci_convergents": fib_checks,
        "locking_q_max": q_max,
        "locking_scores": locking_scores,
        "best_rotation": best_rotation,
        "return_windows": {
            "qT": qT,
            "mT": mT,
            "phi_Euler_44": d13,
            "qEW": qEW,
            "mEW": mEW,
            "phi_Euler_710": phi_qEW,
            "ew_depth": phi_qEW // Omega8,
        },
        "phase_residue_distribution_mod_44": distribution,
        "checks": checks,
    }
    return result


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_information_quasicrystal_phase_unfolding_results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
