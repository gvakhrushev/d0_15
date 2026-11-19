"""Exact integer certificates in Z[p], where p^2 = 1 - p and p > 0."""
import json
from typing import NamedTuple


class Golden(NamedTuple):
    a: int
    b: int

    def __add__(self, other):
        return Golden(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Golden(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        bd = self.b * other.b
        return Golden(self.a * other.a + bd, self.a * other.b + self.b * other.a - bd)

    def __pow__(self, n):
        if n < 0:
            raise ValueError("expected a nonnegative exponent")
        result, base = ONE, self
        while n:
            if n % 2:
                result = result * base
            base = base * base
            n //= 2
        return result

    def norm(self):
        return self.a**2 - self.a * self.b - self.b**2

    def mod(self, prime):
        return Golden(self.a % prime, self.b % prime)

    def sign(self):
        # 2*(a+b*p) = u+v*sqrt(5). Compare squared magnitudes only
        # when the summands have opposite signs.
        u, v = 2 * self.a - self.b, self.b
        sgn = lambda x: (x > 0) - (x < 0)
        if not u or not v or sgn(u) == sgn(v):
            return sgn(u) or sgn(v)
        return sgn(u) * sgn(u * u - 5 * v * v)


def check(condition, name):
    if not condition:
        raise ValueError(name)


ONE, TWO, P = Golden(1, 0), Golden(2, 0), Golden(0, 1)
PHI = ONE + P
check(P**2 + P == ONE and P * PHI == ONE, "golden relation")
x = P**3
check(x == ONE - TWO * P**2, "cos(2θ) with sin(θ)=p")
cos512 = x
for _ in range(9):
    cos512 = TWO * cos512**2 - ONE
previous, current = ONE, x.mod(13)
for _ in range(1, 512):
    previous, current = current, (TWO * x * current - previous).mod(13)
check(current == cos512.mod(13) == Golden(10, 11), "two Chebyshev recurrences")
q = P**2 + TWO * P**10 * (ONE - cos512)
other = ONE - q
check((q - P**2).sign() == 1 and (ONE - TWO * q).sign() == 1, "p^2 < q < 1/2")
check(q.mod(13) == Golden(1, 6), "q residue")
nq, no = q.norm() % 13, other.norm() % 13
nr = (no * pow(nq, -1, 13)) % 13
check((nq, no, nr) == (11, 3, 5), "three norm residues")
# Equivalent to 2/3 < log_phi((1-q)/q) < 3/4; no logarithm is evaluated.
check((other**3 - PHI**2 * q**3).sign() == 1, "lower bound for entropy slope")
check((PHI**3 * q**4 - other**4).sign() == 1, "upper bound for entropy slope")
print(json.dumps({
    "status": "PASS", "arithmetic": "exact integers in Z[p], with p^2+p=1 and p>0",
    "q_interval": ["p^2", "1/2"], "q_interval_open": True,
    "modulus": 13, "T512_basis_1_p": list(cos512.mod(13)),
    "q_basis_1_p": list(q.mod(13)), "norm_q": nq, "norm_one_minus_q": no,
    "norm_odds": nr, "entropy_slope_interval_open": ["2/3", "3/4"],
    "physical_price_selected": False
}, ensure_ascii=False, indent=2))
