#!/usr/bin/env python3
"""Self-contained exact arithmetic for finite horizontal reciprocity and Golden-port source.
Research-only consumer. Original #334/#381 128-outcome/Kraus replays NOT run here.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import sqrt

@dataclass(frozen=True)
class Q5:
    a: F
    b: F = F(0)

    def __add__(self, other):
        other = other if isinstance(other, Q5) else Q5(F(other))
        return Q5(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q5) else -Q5(F(other)))

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        other = other if isinstance(other, Q5) else Q5(F(other))
        return Q5(self.a * other.a + 5 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Q5) else Q5(F(other))
        den = other.a * other.a - 5 * other.b * other.b
        assert den != 0
        return Q5((self.a * other.a - 5 * self.b * other.b) / den,
                  (self.b * other.a - self.a * other.b) / den)

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        out = Q5(F(1))
        for _ in range(exponent):
            out *= self
        return out

    def numeric(self):
        return float(self.a) + float(self.b) * sqrt(5)


def q(a, b=0, den=1):
    return Q5(F(a, den), F(b, den))


def dot(u, v):
    return sum((x * y for x, y in zip(u, v)), F(0))


# Exact off-shell calculus identity for A(q,K):
# 1/2 K0^2 + q0 K0 + q1 K1 + q0 K0 K1 + q0^2 K1/3 + K1^4/4.
# At q=(1/2,1/3), K(z)=(z,z^2), z=2, u=(3,-2), w=(-1,2):
q0, q1 = F(1, 2), F(1, 3)
k0, k1 = F(2), F(4)
L = ((F(1), q0), (q0, 3 * k1 * k1))
B = ((1 + k1, F(0)), (k0 + 2 * q0 / 3, F(1)))
v, u, w = (F(1), F(4)), (F(3), F(-2)), (F(-1), F(2))
Lmul = lambda x: (dot(L[0], x), dot(L[1], x))
Bmul = lambda x: (dot(B[0], x), dot(B[1], x))
s = tuple(a + b for a, b in zip(Lmul(w), Bmul(u)))
r = Lmul(v)
mixed = dot(v, Bmul(u))
assert mixed == dot(v, s) - dot(r, w) == F(35)
print("PASS exact off-shell reciprocal identity: 35 = <v,s> - <Lv,w>")

# Simple connected stationary sheet: L=diag(1,0), B=[[1,0],[2,3]].
# K(z)=(0,z) and q=0 are K-stationary; d E_Q / dz=(2,3).
L0 = ((F(1), F(0)), (F(0), F(0)))
B0 = ((F(1), F(0)), (F(2), F(3)))
v0 = (F(0), F(1))
allowed_u = (F(3), F(-2))
allowed_w = (F(-3), F(0))
assert tuple(dot(row, allowed_w) + dot(row, allowed_u)
             for row in ()) == ()  # explicit empty shape check only
assert (dot(L0[0], allowed_w) + dot(B0[0], allowed_u),
        dot(L0[1], allowed_w) + dot(B0[1], allowed_u)) == (0, 0)
assert dot(v0, (dot(B0[0], allowed_u), dot(B0[1], allowed_u))) == 0
bad_u = (F(2), F(3))
assert dot(B0[1], bad_u) == F(13)  # L0 cannot produce its second row
assert dot((F(2), F(3)), bad_u) == F(13)
# Upstream owned rank inputs, not a fresh matrix replay:
assert 88 - 80 == 8 and 40 - (88 - 80) == 32
print("PASS horizontal toy: liftable dimension 1, blocked direction has drift 13")
print("PASS rank bookkeeping: owner ranks (80,88) imply 8 visible, 32 liftable of 40")

# Both z=+-1 solve d_z[(z^2-1)^2 + t z]=0 at t=0,
# but d_t A differs: this forbids using only endpoint stationarity.
for z in (F(1), F(-1)):
    assert 4 * z * (z * z - 1) == 0
assert F(1) != F(-1)
print("PASS hostile disconnected stationary roots: different metric responses")

# SAME original full128 one-round Golden nonblank port, from #381.
# p=phi^-1, code (p,p^2), actual nonblank ports (p^2,p).
p = q(-1, 1, 2)
assert p + p**2 == q(1)
assert p**3 == p - p**2
h = q(1, 0, 4)
lam, dlam = q(288, 0, 25), q(-144, 0, 25)
eps = p**2 * h**2 / q(64)
dP = eps * (q(1) - h**2 * lam / q(128)) * dlam
dK_port = p**3 * dP
assert dP == q(-42957, 14319, 5120000)  # owned original J23 result
assert dK_port == q(157509, -71595, 5120000)
normalized = dK_port / (h**2)
assert normalized == q(157509, -71595, 320000)
# For a hypothetical bounded first-shell family with dlam_h -> -144/25,
# the ONE-round (not n~h^-2) h^-2 source has a nonzero limit:
ir_if_dlam_persists = p**5 * dlam / q(64)
assert ir_if_dlam_persists == q(99, -45, 200)
assert abs(dK_port.numeric() + 0.0005043529002143443973) < 1e-15
assert abs(normalized.numeric() + 0.00806964640342951) < 1e-14
assert abs(ir_if_dlam_persists.numeric() + 0.00811529493745268) < 1e-14
print("PASS actual first-shell J23 Golden-port Q(sqrt5) source, exact")
print(" D KL_native_port =", dK_port, "=", dK_port.numeric())
print(" h^-2 D KL_native_port =", normalized.numeric())
print(" conditional one-round h->0 limit =", ir_if_dlam_persists.numeric())
print("SCOPE: conditional full-code KL contribution, link tangent;")
print("       no full Book action, h-refining J23 sequence or GR theorem.")
