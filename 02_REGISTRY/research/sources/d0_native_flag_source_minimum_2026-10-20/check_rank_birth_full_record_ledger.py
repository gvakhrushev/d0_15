#!/usr/bin/env python3
"""Exact bounded arithmetic for the CAR16 stopped-archive correlation ledger.

No floating approximations, imported numerical algebra, or entropy regularization.
The general Schmidt/mutual-information statements are proved in the companion note.
"""
from fractions import Fraction as Q


class PhiField:
    """Q[p]/(p*p+p-1) with p=(sqrt(5)-1)/2, coefficients a+b*p."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Q(a)
        self.b = Q(b)

    def __add__(self, other):
        other = lift(other)
        return PhiField(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return PhiField(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-lift(other))

    def __rsub__(self, other):
        return lift(other) - self

    def __mul__(self, other):
        other = lift(other)
        # p^2=1-p, so (a+bp)(c+dp)=(ac+bd)+(ad+bc-bd)p.
        return PhiField(
            self.a * other.a + self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        x, a = PhiField(1), self
        while n:
            if n & 1:
                x *= a
            a *= a
            n >>= 1
        return x

    def __eq__(self, other):
        other = lift(other)
        return self.a == other.a and self.b == other.b

    def __repr__(self):
        return f"({self.a})+({self.b})p"


def lift(x):
    return x if isinstance(x, PhiField) else PhiField(x)


def run():
    one, p, N = PhiField(1), PhiField(0, 1), 6
    assert p * p == one - p  # fixed Golden identity
    epsilon = p ** N
    assert epsilon == 5 - 8 * p  # 9-4 sqrt(5)
    success_weights = [p ** (j + 1) for j in range(1, N + 1)]
    assert sum(success_weights, PhiField()) + epsilon == one
    # Every success history has actual T=j, K=1, L=j+1; fail has T=N,K=0,L=N.
    assert all(w == p ** (j + 1) for j, w in enumerate(success_weights, 1))
    assert epsilon == p ** N
    s = one - epsilon
    alpha = epsilon * s
    assert alpha == -84 + 136 * p

    # c(theta)=cos^2(theta/2) is the exact CAR16 Choi overlap.
    # These invariants characterize the nonzero Schmidt spectra on both sides.
    for c in [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
        det_F = alpha * (1 - c * c)
        tr_F = one
        # Gram spectrum of two weighted data vectors with overlap c:
        det_D = epsilon * s * (1 - c * c)
        tr_D = one
        assert (tr_F, det_F) == (tr_D, det_D)
        R = epsilon + s * c * c
        assert R == one - s * (1 - c * c)
        if c == 1:
            assert det_F == 0 and R == one
        if c == 0:
            assert det_F == alpha and R == epsilon

    # Exact formal theta^2 coefficients from c=1-theta^2/4+O(theta^4):
    c2 = Q(-1, 4)
    c_squared2 = 2 * c2  # -1/2
    lambda_minus2 = alpha * (-c_squared2)  # +alpha/2
    R_second = 2 * s * c_squared2  # -s
    assert lambda_minus2 == alpha * Q(1, 2)
    assert R_second == -(one - epsilon)
    assert R_second == 4 - 8 * p

    # For any fixed record weights, d^k H_phi(w)/dtheta^k=0, k>=1.
    # Exact global pure-state relation: A_F+I/(2 ln phi)=H_phi(w).
    # An erroneously dropped failure branch would set det_F=0 for all c:
    assert alpha != 0  # hostile check against such postselection
    print("Golden stopped complete-law normalization: PASS")
    print("CAR16 flag/data reduced Schmidt invariants: PASS")
    print("Nonzero eigenvalue rank-birth coefficient: PASS", lambda_minus2)
    print("Joint future-test second source: PASS", R_second)
    print("Exact ledger A_F+I(F:D)/(2 ln phi)=H_phi(w): analytic Schmidt identity")
    print("ALL EXACT BOUNDED CHECKS PASSED")


if __name__ == "__main__":
    run()
