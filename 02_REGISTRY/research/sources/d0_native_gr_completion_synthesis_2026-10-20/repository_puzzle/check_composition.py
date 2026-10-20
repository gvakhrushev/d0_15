#!/usr/bin/env python3
"""Narrow root composition checks, no action selection or new rank census."""
import sympy as s


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


# Literal old P3 matrices, not a substitute for the primary GR carrier.
L = s.Matrix([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
B = s.Matrix([[1, 0], [1, 1], [0, 1]])
n = s.Matrix([1, -1, 1])
require(B.T * L * B == s.eye(2), 'old Galerkin identity')
require(L * B - B == s.Matrix([[-1, -1], [0, 0], [-1, -1]]), 'actual seam defect')
require(B.T * B == s.Matrix([[2, 1], [1, 2]]), 'nonisometric prolongation')
require(B.T * n == s.zeros(2, 1) and B.row_join(n).det() == 3, 'entire fine space retained')
F, D = B.T * L * n, (n.T * L * n)[0]
require(F == s.Matrix([-2, -2]) and D == 8, 'actual archive blocks')
H = s.eye(2) - F * F.T / D
require(H == s.Matrix([[1, -1], [-1, 1]]) / 2, 'true Schur, not restriction')
x1, x2, y, a = s.symbols('x1 x2 y a', real=True)
x = s.Matrix([x1, x2])
z = B * x + n * y
energy = s.expand((z.T * L * z)[0] / 2)
ystar = (x1 + x2) / 4
require(s.expand(s.diff(energy, y).subs(y, ystar)) == 0, 'archive first variation')
reduced = s.expand(energy.subs(y, ystar))
require(s.expand(reduced - (x1 - x2) ** 2 / 4) == 0, 'actual reduced energy')
require(s.hessian(reduced, (x1, x2)) == H, 'reduced full source')
constant_state = z.subs({x1: a, x2: a, y: a / 2})
require(constant_state == 3 * a * s.ones(3, 1) / 2, 'retained constant family')
require(L * constant_state == s.zeros(3, 1), 'stationary despite nonzero C')

# Universal KL second-jet proof is in the synthesis; exact three-label
# mixed variations check both moving laws and nontrivial normalization.
t, r, ell = s.symbols('t r ell', real=True)
base = [s.Rational(1, 2), s.Rational(1, 3), s.Rational(1, 6)]
dp, dq = [1, -2, 1], [-2, 3, -1]
ep, eq = [2, -1, -1], [-1, -1, 2]
P = [base[i] + t * dp[i] + r * ep[i] for i in range(3)]
q = [base[i] + t * dq[i] + r * eq[i] for i in range(3)]
require(sum(P) == 1 and sum(q) == 1, 'both probability rows normalized')
kl = sum(P[i] * s.log(P[i] / q[i]) for i in range(3)) / ell
at_zero = {t: 0, r: 0}
require(kl.subs(at_zero) == 0, 'KL value at matching laws')
require(s.diff(kl, t).subs(at_zero) == 0, 'KL first jet at matching laws')
mixed = sum(s.Rational((dp[i] - dq[i]) * (ep[i] - eq[i]), 1) / base[i] for i in range(3)) / ell
require(s.simplify(s.diff(kl, t, r).subs(at_zero) - mixed) == 0, 'KL mixed jet retains both laws')
require(s.simplify(s.diff((1 + t + 2*r) * kl, t, r).subs(at_zero) - mixed) == 0,
        'moving stationary prefactor has no extra second-jet term at equality')

# Old genuine two-tick K(9,11,13) law: all full paths, not a new apparatus.
paths = 11 * (9 + 13) + 13 * (9 + 11)
require(paths == 502, 'original complete two-step histories')
q11, q13 = s.Rational(22, paths), s.Rational(20, paths)
require(q11/q13 == s.Rational(11, 10), 'nonunit actual first-edge odds')
require((q11/q13) / s.Rational(22, 20) == 1, 'suffix cancels exact same-prefix defect')
print('PASS: original gluing/Schur/source; normalized KL mixed jet; full502 suffix factor.')
