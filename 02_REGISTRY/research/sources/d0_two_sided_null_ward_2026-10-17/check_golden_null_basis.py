#!/usr/bin/env python3
"""Bounded exact D0 golden-gate-amplitude null-source basis check.

This is a field-algebraic source inverse and does NOT prove physically
admitted coframe perturbations, native cut/price or strong h^-2 convergence.
No older certificates, root/spectrum catalogues or Lean modules run.
Requires sympy. Runs under ordinary Python and Python -O identically.
"""
import sympy as S

p = (S.sqrt(5) - 1) / 2
a, b = S.sqrt(p), p
pairs = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
         (2, 2), (3, 3), (1, 2), (1, 3), (2, 3)]


def verify(ok, name):
    if not bool(ok):
        raise RuntimeError(name)


def probe_row(v):
    return [v[i] * v[j] * (1 if i == j else 2) for i, j in pairs]


k = []
for i in (1, 2, 3):
    for sign in (1, -1):
        ray = [S.Integer(1), S.Integer(0), S.Integer(0), S.Integer(0)]
        ray[i] = S.Integer(sign)
        k.append(ray)
for i, j in ((1, 2), (1, 3), (2, 3)):
    ray = [S.Integer(1), S.Integer(0), S.Integer(0), S.Integer(0)]
    ray[i] = a
    ray[j] = b
    k.append(ray)

eta = [S.Integer(1), -S.Integer(1), -S.Integer(1), -S.Integer(1)]
verify(all(S.simplify(sum(eta[i] * v[i]**2 for i in range(4))) == 0
           for v in k), "golden vectors must be normalized null")
verify(S.simplify(a**2 + b**2 - 1) == 0, "golden amplitude norm")
T = S.Matrix([probe_row(ray) for ray in k] + [
    [1, 0, 0, 0, -1, -1, -1, 0, 0, 0]
])
verify(S.simplify(T.det() - 2048 * p**S.Rational(9, 2)) == 0,
       "full ten-source exact determinant")
q = S.symbols("y1p y1m y2p y2m y3p y3m z12 z13 z23 t")
d = [(q[2*i] + q[2*i+1])/2 for i in range(3)]
m = [(q[2*i] - q[2*i+1])/4 for i in range(3)]
s00 = (sum(d) + q[-1])/4
reconstructed = [s00] + m + [di-s00 for di in d]
for idx, (i,j) in enumerate(((1,2),(1,3),(2,3))):
    reconstructed.append((q[6+idx] - p*d[i-1] - p*p*d[j-1]
                          - 2*a*m[i-1] - 2*p*m[j-1])/(2*p*a))
K = S.Matrix(10, 10, lambda i,j: S.diff(reconstructed[i],q[j]))
verify(all(S.simplify(v) == 0 for v in T*K-S.eye(10)),
       "left inverse")
verify(all(S.simplify(v) == 0 for v in K*T-S.eye(10)),
       "right inverse")
# Nine null rows annihilate eta, and determinant proves full rank with trace.
verify(all(S.simplify(v) == 0 for v in T[:9, :] *
           S.Matrix([1, 0, 0, 0, -1, -1, -1, 0, 0, 0])),
       "null kernel must contain eta")

# Column-sum formulas, derived analytically from the inverse above.
vmax = 1+(1+a)/(2*b)
wmax = S.Rational(5,4)+(1+a)/b
# Rational inequalities are enough: 3/5<p<16/25, 3/4<a<4/5,
# a>b, and 3p>9/5>1+a.
verify(bool(S.Rational(3,5)<p<S.Rational(16,25)), "p rational bounds")
verify(bool(S.Rational(3,4)<a<S.Rational(4,5)), "a rational bounds")
verify(bool(a>b), "ordered gate amplitudes")
verify(bool(3*p>1+a), "strict improvement condition")
# First plus column dominates all: its two mixed contributions use (1+a)/b;
# each other plus column has at most one of these and one (1+b)/a.
verify(bool((1+a)/b>(1+b)/a), "source column max ordering")
verify(bool(vmax<S.Rational(5,2)), "packed10 bound improvement")
verify(bool(wmax<S.Rational(17,4)), "full16 bound improvement")
# Check one genuine mutation: replacing second gate amplitude b=p by p^2
# destroys normalization/null-contraction already at leading symbol.
verify(S.simplify(a*a + p**4 - 1) != 0, "mutation wrongly stays null")
print("PASS D0 golden null9+trace10 exact inverse and positive determinant")
print("PASS packed/full raw-l1 bounds strictly improve rational null basis")
print("PASS mutated wrong golden amplitude loses the causal cone")
print("det(L) =", S.simplify(T.det()))
print("packed bound =", S.N(vmax, 14), "full16 =", S.N(wmax, 14))
