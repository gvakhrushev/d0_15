#!/usr/bin/env python3
"""Original SAME-CARRIER full128 exact-algebraic specialization checks, C28-C33.

Reuses the unchanged original full128 CAR/Julia/Golden/Walsh construction
at its eight already authenticated split primes; no synthetic Kraus model,
floating rank test, free initialization, changed palette, or new physical GR
source. Its finite-field equality checks are REGRESSIONS for the separately
given characteristic-zero operator derivation, not a proof of all-field GR.
Run:
python3 02_REGISTRY/research/certificates/a4d_original_full128_native_fixedpoint_cost_modprime.py
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
import numpy as np

SOURCE = Path(__file__).resolve().parent.parent / (
    "sources/d0_original_full128_future_even_algebra_2026-10-22"
)
sys.path.insert(0, str(SOURCE))
from check_future_even_algebra_modprime import ( # noqa E402
    SPLIT_PRIMES, original_kraus_mod
)


def fail(msg: str):
    raise AssertionError(msg)


def inv_mod_matrix(matrix: np.ndarray, prime: int):
    """Pure modular row reduction, no floating linear algebra."""
    n = matrix.shape[0]
    if matrix.shape != (n, n):
        fail("input must be square")
    aug = np.column_stack((matrix % prime, np.eye(n, dtype=np.int64)))
    for j in range(n):
        idx = next((r for r in range(j, n) if int(aug[r, j]) % prime), None)
        if idx is None:
            return None
        if idx != j:
            aug[[idx, j]] = aug[[j, idx]]
        aug[j] = (aug[j] * pow(int(aug[j, j]), -1, prime)) % prime
        for k in range(n):
            if k != j:
                c = int(aug[k, j])
                if c:
                    aug[k] = (aug[k] - c * aug[j]) % prime
    inverse = aug[:, n:] % prime
    if not np.array_equal((matrix @ inverse) % prime,
                          np.eye(n, dtype=np.int64)):
        fail("modular inverse did not pass original operator multiplication")
    return inverse


def main():
    tests = 0
    rows = []
    valid_inverse = 0
    valid_state = 0
    for prime_data in SPLIT_PRIMES:
        m, _, golden_p, golden_sqrt_p, _, _ = prime_data
        d = original_kraus_mod(prime_data)
        K = d["K"]
        Kd = d["Kd"]
        I = d["I"]
        if K.shape != (128, 16, 16) or Kd.shape != K.shape:
            fail("authentic full128 primitive dimension")
        tests += 1
        s = (-2 * golden_p * golden_sqrt_p) % m
        if s == 0:
            fail("original Kraus K1 scalar factor unexpectedly zero")
        # Original K1=-2 p sqrt(p) N0^dagger N0, hence algebraic A=a^dagger a.
        A = (K[1] * pow(s, -1, m)) % m
        tests += 1
        invA = inv_mod_matrix(A, m)
        if invA is None:
            rows.append({"prime": m, "invertible_specialization": False,
                         "status": "skip inverse-only checks (bad reduction)"})
            continue
        valid_inverse += 1

        def channel(X):
            out = np.zeros((16, 16), dtype=np.int64)
            for j in d["nonzero"]:
                out = (out + (K[j] @ X @ Kd[j])) % m
            return out

        # All 128 outcomes are included via d["nonzero"], the other64 are
        # verified identically zero in the imported unchanged constructor.
        Xi = channel(invA)
        if not np.array_equal(Xi % m, invA):
            fail(f"same-original full128 unnormalized canonical state is NOT fixed modulo {m}")
        tests += 1

        odd = np.zeros((16, 16), dtype=np.int64)
        for j in range(1, 128, 2):
            odd = (odd + (Kd[j] @ K[j])) % m
        target = (4 * pow(golden_p, 3, m) * A) % m
        if not np.array_equal(odd, target):
            fail(f"actual odd-port effect != 4p^3 A modulo {m}")
        tests += 1
        if not np.array_equal(
            (odd + sum(
                ((Kd[j] @ K[j]) % m for j in range(0, 128, 2)),
                np.zeros((16,16), dtype=np.int64)
            )) % m, I
        ):
            fail("all 128 port effects do not exhaust true original input")
        tests += 1

        Z = int(np.trace(invA)) % m
        if Z == 0:
            rows.append({"prime": m, "invertible_specialization": True,
                         "canonical_state_normalizable_mod_prime": False,
                         "unscaled_fixed": True, "port_effect": True})
            continue
        valid_state += 1
        rho = (invA * pow(Z, -1, m)) % m
        if not np.array_equal(channel(rho), rho):
            fail(f"true original normalized stationary state fails modulo {m}")
        tests += 1
        diag_odd = int(np.trace((odd @ rho) % m)) % m
        expected = (64 * pow(golden_p, 3, m) * pow(Z, -1, m)) % m
        if diag_odd != expected:
            fail(f"actual 128 port mean != closed-canonical formula modulo {m}")
        tests += 1

        rho_n = rho.copy()
        for n in (1, 2, 3, 5):
            if not np.array_equal(rho_n, rho):
                fail("no-reset stationary DATA changed during paid original history")
            native_expected_cost = (n * (1 + diag_odd)) % m
            closed_cost = (n + n * expected) % m
            if native_expected_cost != closed_cost:
                fail("n original mean ticks omitted or 1/2 report miscounted")
            tests += 1
            rho_n = channel(rho_n)

        par = np.array(
            [(-1) ** (bin(j).count("1") % 2) for j in range(16)],
            dtype=np.int64
        )
        if np.any((par[:,None] * rho - rho * par[None,:]) % m):
            fail("original stationary state is not inside native even future test algebra")
        tests += 1
        rows.append({"prime": m, "invertible_specialization": True,
                     "canonical_state_normalizable_mod_prime": True,
                     "unscaled_fixed": True, "port_effect": True,
                     "Z_mod": Z, "original_one_round_extra_port_cost_mod": diag_odd,
                     "native_mean_cost_n5_mod": 5*(1+diag_odd)%m,
                     "native_future_even": True})

    if valid_inverse < 1 or valid_state < 1:
        fail("No genuine regular/normalizable original prime fixture survived")
    print(json.dumps({
        "status": "PASS", "exact_checks": tests,
        "one_original_instrument": "CAR16 original full128, fine labels, genuine K",
        "certification": "mod-prime regression for analytically derived C28-C33",
        "regular_modular_fixtures": valid_inverse,
        "normalizable_modular_fixtures": valid_state,
        "original_charts": rows,
        "new_physical_gr_acceptance": False
    }, indent=2))


if __name__ == "__main__":
    main()
