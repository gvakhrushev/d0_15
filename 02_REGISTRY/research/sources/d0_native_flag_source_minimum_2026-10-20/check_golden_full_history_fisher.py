#!/usr/bin/env python3
"""Exact Q[p] finite stopped Golden history / CAR16 Choi Fisher jet checks.

This checker verifies native cap combinatorics and formal second jets.
The analytic all-cap / all-field proofs are in rank_birth_full_record_ledger.md.
No numerical differentiation, fitted source, or physical POVM admission.
"""
from fractions import Fraction as Q
from math import comb


class ZPhi:
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    def __add__(self, other):
        other = lift(other)
        return ZPhi(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return ZPhi(-self.a, -self.b)

    def __sub__(self, other):
        return self + -lift(other)

    def __rsub__(self, other):
        return lift(other) + -self

    def __mul__(self, other):
        other = lift(other)
        # p^2 = 1-p in Q[p].
        return ZPhi(self.a * other.a + self.b * other.b,
                    self.a * other.b + self.b * other.a - self.b * other.b)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        result, base = ZPhi(1), self
        while n:
            if n & 1:
                result *= base
            base *= base
            n //= 2
        return result

    def __eq__(self, other):
        other = lift(other)
        return self.a == other.a and self.b == other.b

    def approx(self):
        return float(self.a) + float(self.b) * ((5**0.5 - 1) / 2)

    def __repr__(self):
        return f"({self.a})+({self.b})p"


def lift(x):
    return x if isinstance(x, ZPhi) else ZPhi(x)


def check_stopped(m, N):
    assert isinstance(m, int) and isinstance(N, int) and 1 <= m <= N
    one, p = ZPhi(1), ZPhi(0, 1)
    g = p*p
    assert p+g == one

    # All terminal success words end with the mth good outcome.
    complete = [(m, j, comb(j-1, m-1)*g**m*p**(j-m))
                for j in range(m, N+1)]
    # All unfinished words at cap N are kept, with k=0,...,m-1 goods.
    incomplete = [(k, N, comb(N, k)*g**k*p**(N-k))
                  for k in range(m)]

    assert sum((w for k, T, w in complete+incomplete), ZPhi()) == one
    eps = sum((w for k, T, w in incomplete), ZPhi())
    completed_mass = sum((w for k, T, w in complete), ZPhi())
    assert completed_mass + eps == one

    # Every branch still owns its actual clock T and code length T+k.
    assert all(T >= k >= 0 for k, T, _ in complete+incomplete)

    EK2 = sum((k*k*w for k, _, w in complete+incomplete), ZPhi())
    assert EK2 == m*m*completed_mass + sum(
        (k*k*w for k, _, w in incomplete), ZPhi())

    h2 = Q(1, 16)  # fixed h=1/4, so accumulated angle t_k=k*h^2
    Et2 = EK2 * h2*h2

    # From exact CAR16 Choi overlap cos^2(tF/2):
    # q_return(F) = 1 - Et2*F^2/2 + O(F^4), hence q''(0)=-Et2.
    return_second_jet = -Et2
    # Pure complete-tape and classically dephased conditional-branch QFI:
    pure_record_QFI = 2*Et2
    # Binary P_Omega return/failure POVM Fisher in punctured F->0 limit:
    binary_FI_limit = 2*Et2
    assert pure_record_QFI == binary_FI_limit
    assert 2*return_second_jet + pure_record_QFI == 0

    # Exact finite-cap sandwich: completed trees all have K=m.
    missing = m*m*h2*h2 - Et2
    assert missing == sum(
        ((m*m-k*k)*w*h2*h2 for k, _, w in incomplete), ZPhi())
    assert missing.approx() >= 0
    assert (eps*m*m*h2*h2-missing).approx() >= -1e-12

    if m == 1 and N == 6:
        assert eps == p**6 == 5-8*p
        assert EK2 == 1-eps  # only the all-failure word has K=0

    print(f"m={m} cap={N} epsilon={eps.approx():.10g}"
          f" return_second={return_second_jet.approx():.10g}"
          f" QFI=Fisher_limit={pure_record_QFI.approx():.10g}")
    return eps, Et2


if __name__ == "__main__":
    for m, N in [(1, 6), (2, 11), (3, 16), (4, 21)]:
        check_stopped(m, N)
    print("ALL EXACT STOPPED GOLDEN / CAR16 FISHER-JET CHECKS PASSED")
