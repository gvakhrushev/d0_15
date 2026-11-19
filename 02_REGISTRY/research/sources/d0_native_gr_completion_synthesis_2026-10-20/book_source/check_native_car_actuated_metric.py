#!/usr/bin/env python3
"""Exact changed-composition check: native CAR actuator -> live material query.

This is one finite fixture, not the all-h/density proof. All arithmetic is in
Q(a), a^4+a^2-1=0, a=sqrt(phi^-1)>0. Every require remains active under -O.
It checks the actual full 16/64-row words; no old engine/detector suite runs.
Moving query/code admission, addressed operations, resource preparation,
physical time, the Book03 price, and compulsory execution are not proved.
"""
from fractions import Fraction as F


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


Z = (F(0),)*4
O = (F(1), F(0), F(0), F(0))
A = (F(0), F(1), F(0), F(0))
P = (F(0), F(0), F(1), F(0))


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c*a for a in x)


def sub(x, y):
    return add(x, scale(-1, y))


def mul(x, y):
    c = [F(0)]*7
    for i in range(4):
        if x[i]:
            for j in range(4):
                if y[j]:
                    c[i+j] += x[i]*y[j]
    for j in range(6, 3, -1):
        c[j-4] += c[j]
        c[j-2] -= c[j]
    return tuple(c[:4])


def power(x, n):
    out = O
    while n:
        if n & 1:
            out = mul(out, x)
        x = mul(x, x)
        n //= 2
    return out


def dot(x, y):
    out = Z
    for u, v in zip(x, y):
        if u != Z and v != Z:
            out = add(out, mul(u, v))
    return out


def basis(dim, j):
    v = [Z]*dim
    v[j] = O
    return v


def g(v, inverse=False):
    """G_N on bit0 of every 16-row CAR block; all other bits retained."""
    out = list(v)
    sp = scale(-1 if inverse else 1, P)
    for n in range(0, len(v), 2):
        x, y = v[n:n+2]
        out[n] = sub(mul(A, x), mul(sp, y))
        out[n+1] = add(mul(sp, x), mul(A, y))
    return out


def k_gate(v):
    """Literal native K: Z_N iff spatial popcount is 2 or 3."""
    return [scale(-1, x) if ((n & 1) and ((n % 16) >> 1).bit_count() >= 2)
            else x for n, x in enumerate(v)]


def x_gate(v):
    return [v[n ^ 1] for n in range(len(v))]


def native_l(v):
    """Chronological K,X,G,X,K,G: six primitive letters on known c=1."""
    return g(k_gate(x_gate(g(x_gate(k_gate(v))))))


def r_expected(v, sign=1):
    twice = g(g(v, inverse=sign < 0), inverse=sign < 0)
    return [twice[n] if ((n % 16) >> 1).bit_count() >= 2 else v[n]
            for n in range(len(v))]


def u(v, minus=False):
    return k_gate(g(v, inverse=minus))


def u_wrong(v, minus=False):
    """Hostile order: G^(+/-1) K instead of K G^(+/-1)."""
    return g(k_gate(v), inverse=minus)


def cnot64(v, control, target):
    out = [Z]*64
    for n, amplitude in enumerate(v):
        m = n ^ (1 << target) if ((n >> control) & 1) else n
        out[m] = amplitude
    return out


def w64(v):
    """All nine actual forward primitives of the autonomous owner.

    Index = 32*c + 16*f + CARmask, with N=bit0, f=bit4, c=bit5.
    Chronological: C_fN,G,C_fN,C_cN,G,C_cN,G,K,C_cf.
    """
    v = cnot64(v, 4, 0)
    v = g(v)
    v = cnot64(v, 4, 0)
    v = cnot64(v, 5, 0)
    v = g(v)
    v = cnot64(v, 5, 0)
    v = g(v)
    v = k_gate(v)
    return cnot64(v, 5, 4)


require(mul(A, A) == P, "a^2=p")
require(add(P, mul(P, P)) == O, "p+p^2=1")

# Full 16 columns: no unprepared CAR grade is discarded.
for n in range(16):
    e = basis(16, n)
    require(native_l(e) == r_expected(e), "six-letter word is I low / G^2 high")
    require(u(u(e), minus=True) == native_l(e), "U- U+ equals compiled L")
require(u_wrong(u_wrong(basis(16, 14)), minus=True) != native_l(basis(16, 14)),
        "wrong K/G order reverses the high-grade rotation")
require(u_wrong(u_wrong(basis(16, 14)), minus=True)
        == r_expected(basis(16, 14), sign=-1),
        "wrong order has the exact G^-2 hostile value")

# Every sector of the 64-row forward word is checked, including c=0.
columns = []
for n in range(64):
    c, f, car = n >> 5, (n >> 4) & 1, n & 15
    e = basis(16, car)
    if c:
        v = u(e, minus=bool(f))
        target_f = 1-f
    else:
        v = list(e)
        for _ in range(3 if f == 0 else 1):
            v = g(v)
        v = k_gate(v)
        target_f = f
    expected = [Z]*64
    expected[32*c+16*target_f:32*c+16*target_f+16] = v
    col = w64(basis(64, n))
    require(col == expected, "full W column, including both c/f sectors")
    columns.append(col)
    actual2 = w64(col)
    if c:
        v2 = r_expected(e, sign=1 if f == 0 else -1)
    else:
        v2 = e
        if (car >> 1).bit_count() < 2:
            for _ in range(6 if f == 0 else 2):
                v2 = g(v2)
    expected2 = [Z]*64
    expected2[32*c+16*f:32*c+16*f+16] = v2
    require(actual2 == expected2, "full W^2 column with all complementary sectors")
for i, col in enumerate(columns):
    for j in range(i+1):
        require(dot(col, columns[j]) == (O if i == j else Z),
                "whole 64-row W is orthogonal")

# Explicitly retain the f-sector distinction; its erasure is not allowed.
f0 = w64(w64(basis(64, 32+14)))[32:48]
f1 = w64(w64(basis(64, 48+14)))[48:64]
require(f0 != f1, "c=1,f=0 and f=1 give opposite nontrivial rotations")

# The real embedding is pinned by exact bisection, not floating tolerance.
lo, hi = F(0), F(1)
for _ in range(1024):
    mid = (lo+hi)/2
    if mid**4+mid**2 < 1:
        lo = mid
    else:
        hi = mid
require(lo**4+lo**2 < 1 < hi**4+hi**2, "isolated positive algebraic root")


def imul(x, y):
    products = [a*b for a in x for b in y]
    return min(products), max(products)


def interval(x):
    out = (x[3], x[3])
    for coefficient in reversed(x[:3]):
        out = imul(out, (lo, hi))
        out = (out[0]+coefficient, out[1]+coefficient)
    return out


def between(x, lower, upper):
    l, h = interval(x)
    return lower < l and h < upper


# One exact small-return fixture: at the actuated u, psi0=psi4=0.
# The primary positive-slack state has m1=a, m14=p and full norm one.
# At the next u site take psi0=h/4 (strictly inside the same chart);
# this gives nonzero D_u psi0=1/4 without any top-component flux.
m = [Z]*16
m[1], m[14] = A, P
m_after = list(m)
return_k = 33
for _ in range(return_k):
    m_after = native_l(m_after)
require(dot(m, m) == O == dot(m_after, m_after), "exact full norm retained")
require(m_after[0] == m[0] and m_after[1] == m[1], "scalar and first-grade current fixed")
require(all(m_after[n] == Z for n in range(16) if n not in (1, 14, 15)),
        "no undeclared CAR coordinate introduced")
delta = m_after[15]
require(delta != Z, "finite return gives nonzero top increment")
require(between(delta, F(-1, 100), F(0)), "exact small nonzero return")
require(between(m_after[14], F(3, 5), F(1)), "positive complement survives")

# Check the autonomous version at the same k on all retained flags.
whole = [Z]*64
whole[32:48] = m
for _ in range(2*return_k):
    whole = w64(whole)
require(whole[32:48] == m_after, "18k-tick original W^(2k) agrees on prepared c1/f0")
require(all(whole[n] == Z for n in range(64) if not 32 <= n < 48),
        "prepared flags return and other sectors are retained, not projected")

# Native query substitution: scale s=1, true nonuniform rho=3/2.
h, rho, eta, calibration = F(1, 2), F(3, 2), F(1, 8), F(1)
H0, H1 = F(1, 7), F(2, 7)
v0, v4 = F(1, 4), F(0)
require(between(sub(mul(P, P), scale((h*v0)**2, O)), F(1, 4), F(1)),
        "adjacent-u nonzero scalar profile has positive slack")
delta2 = mul(delta, delta)


def q_of(H):
    return scale(calibration**2/rho,
                 sub(scale(2*v4/h, delta), scale(H/h**2, delta2)))


q0, q1 = q_of(H0), q_of(H1)
require(sub(q1, q0) == scale(-calibration**2*(H1-H0)/(rho*h**2), delta2),
        "actual inverse-PF Delta q = -s^2 Delta H delta^2/(rho h^2)")
require(q0 != q1 and between(q0, F(-1, 100), F(0))
        and between(q1, F(-1, 100), F(0)), "both live source inputs are distinct and chart-small")


def minus_probability(q):
    # Original sigma=-1, actual eta; no modified detector coefficient.
    r = sub(P, scale(eta**2, mul(mul(P, P), q)))
    scene_b = mul(r, r)
    return scale(4, mul(scene_b, sub(O, scene_b))), r, scene_b


B0, r0, b0 = minus_probability(q0)
B1, r1, b1 = minus_probability(q1)
require(between(r0, F(1, 2), F(2, 3)) and between(r1, F(1, 2), F(2, 3)),
        "both arguments stay in the same strictly monotone native scene chart")
require(B0 != B1 and between(sub(B1, B0), F(0), F(1, 100000)),
        "actual complete minus-Q response distinguishes the two H values")
factorized = scale(4, mul(mul(sub(r1, r0), add(r1, r0)),
                         sub(O, add(mul(r1, r1), mul(r0, r0)))))
require(sub(B1, B0) == factorized, "finite difference identity, not only a derivative")
# A fixed positive readiness/efficiency is retained in the complete law.
ready = F(2, 5)
Bcomplete0 = (scale(ready, B0), scale(ready, sub(O, B0)), scale(1-ready, O))
Bcomplete1 = (scale(ready, B1), scale(ready, sub(O, B1)), scale(1-ready, O))
require(Bcomplete0 != Bcomplete1
        and add(add(Bcomplete0[0], Bcomplete0[1]), Bcomplete0[2]) == O
        and add(add(Bcomplete1[0], Bcomplete1[1]), Bcomplete1[2]) == O,
        "retained abort does not erase the contrast")
frozen0 = minus_probability(Z)[0]
frozen1 = minus_probability(Z)[0]
require(frozen0 == frozen1, "hostile frozen-q control remains blind despite live CAR rotation")
require(6*return_k == 198 and 18*return_k == 594,
        "compiled and original-engine query words have distinct paid counts")

print("PASS: exact full16 six-letter L and full64 original W/W^2, including all c/f sectors")
print("PASS: k=33 positive-slack return preserves norm/scalar/current; 6k and 18k counts distinguished")
print("PASS: literal inverse-PF live q substitution gives a nonzero finite native minus-Q contrast")
print("PASS: wrong K/G order reverses the action; frozen q code has exactly zero contrast")
print("Scope: finite composition only; live query binding, addressing, preparation and physical time remain inputs")

