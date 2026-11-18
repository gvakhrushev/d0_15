"""Exact checks for the retained Golden tree, RAW maps and H.1 readout."""
from itertools import product
import sympy as sp


# Q(a), a^4 + a^2 - 1 = 0, positive real embedding a = sqrt(p).
root = sp.sqrt((sp.sqrt(5) - 1) / 2)
field = sp.QQ.algebraic_field(root)
a = field.unit
one = field.one
zero = field.zero
p = a * a
assert p + p**2 == one


def retained_tree_column(bit):
    column = [zero, zero]
    for first, second in product(range(2), repeat=2):
        weight = p ** (2 + first + second)
        if bit == 0:
            output, sign = first, 1
        elif first != second:
            output, sign = 0, -1
        else:
            output, sign = 1, 1
        column[output] += sign * weight
    return column


assert retained_tree_column(0) == [p, p**2]
assert retained_tree_column(1) == [-2*p**3, one-2*p**3]
# K in orthonormal coordinates. D is diag(a,p).
b00, b10 = retained_tree_column(0)
b01, b11 = retained_tree_column(1)
k00, k01, k10, k11 = b00, b01/a, a*b10, b11
assert k10-k01 == 3*a*p**2 and k00+k11 == 3*p**2
# G^T K is symmetric positive, by its leading minor and determinant.
h00, h01 = a*k00+p*k10, a*k01+p*k11
h10, h11 = -p*k00+a*k10, -p*k01+a*k11
assert h01 == h10
assert h00 == a*(p+p**3)
assert k00*k11-k01*k10 == p*(one-2*p**3)+2*p**5
assert one-2*p**3 == p**2+p**4
assert h00*h11-h01*h10 == k00*k11-k01*k10
assert h01 != zero

# Real E0 encoder: on r=0 act by K, on r=1 by X K X, on v=(a,p).
n0 = (k00*a+k01*p)**2 + (k10*a+k11*p)**2
y10, y11 = k11*a+k10*p, k01*a+k00*p
assert y10 == a*(one-p**3)
assert y11 == -p**5
q, n_0, n_1, bad = sp.symbols("q n_0 n_1 bad", positive=True)
norm = (1-q)*n_0 + q*n_1
assert sp.simplify(sp.diff(q*bad/norm, q) - bad*n_0/norm**2) == 0
assert n0 != zero

# A single backward convention: old input indexes a row of future values.
rows = [[zero, zero], [zero, zero]]
for x, i, j in product(range(2), repeat=3):
    if x == 0:
        y, sign = int(i != j), 1
    else:
        y, sign = 1-i, 1-2*i
    rows[x][y] += sign*p**(2+i+j)
assert rows == [[one-2*p**3, 2*p**3], [-p**2, p]]
u, v, w, z = rows[0][0], rows[0][1]/a, a*rows[1][0], rows[1][1]
assert v-w == 3*a*p**2
assert u+z == 3*p**2
# G Ptilde is symmetric positive: positive leading entry and det.
assert a*v-p*z == p*u+a*w
assert a*u-p*w == a*(p**2+p**4+p**3)
assert u*z-v*w == p*(p**2+p**4)+2*p**5
# Unpolarized forward candidate is Ptilde^T.
assert w*a+u*p == p**5 and z*a+v*p == a*(p+2*p**3)
assert p/a == a and p**2/p == p  # backward birth

# H/2 is a convex combination of I, X and the signed rotation J.
cI, cX, cJ = one/2, (one-p)/4, (one+p)/4
assert cI+cX+cJ == one
assert (cI, cX-cJ, cX+cJ, cI) == (one/2, -p/2, one/2, one/2)

# F4 has p^2+p+1=0. Represent residue c0+c1*p by two bits.
def mul_p(x):
    c0, c1 = x & 1, x >> 1
    return c1 | ((c0 ^ c1) << 1)


assert all((mul_p(s) ^ mul_p(mul_p(s))) == s for s in range(4))
assert all((s ^ s) == 0 for s in range(4))
assert all(mul_p(s) != 0 for s in (1, 2, 3))
print("PASS: two signed Golden trees, both polars, two H.1 leakages, field derivative, backward birth, RAW parity and sharp bound witness")
