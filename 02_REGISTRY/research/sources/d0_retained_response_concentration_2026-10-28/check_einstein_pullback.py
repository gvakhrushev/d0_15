#!/usr/bin/env python3
"""Reproduce the 38 exact pullback/sign checks executed in the review.

Requires SymPy. This is the same rational tensor fixture and the same
38 checks as the original inline execution; only its deterministic JSON
receipt wrapper has been added. It is not a native-execution certificate
or a substitute for the general algebraic proof.
"""

import hashlib
import json
from pathlib import Path

import sympy as s


eta = s.diag(1, -1, -1, -1)
e = s.Matrix([[2, 1, 0, 0], [0, 1, 1, 0],
              [0, 0, 1, 1], [0, 0, 0, 1]])
m = s.Integer(8)
lam = -s.Rational(7, 3)
E = e.det()
a = s.sqrt(m / E)
eh = a * e
Eh = eh.det()
F = eh.inv()
X = (s.Matrix([1, 2, -1, 1]) * s.Matrix([1, 2, -1, 1]).T
     + s.Matrix([2, -1, 0, 1]) * s.Matrix([2, -1, 0, 1]).T)
R = {}
for mu in range(4):
    for nu in range(mu + 1, 4):
        for aa in range(4):
            for bb in range(aa + 1, 4):
                v = s.Rational((mu + 1) * (bb + 2)
                               - (nu + 2) * (aa + 1), 7)
                for mm, nn, ss in [(mu, nu, 1), (nu, mu, -1)]:
                    R[mm, nn, aa, bb] = ss * v
                    R[mm, nn, bb, aa] = -ss * v


def curvature(f):
    return sum(f[mu, aa] * f[nu, bb] * R.get((mu, nu, aa, bb), 0)
               for mu in range(4) for nu in range(4)
               for aa in range(4) for bb in range(4))


def kinetic(f):
    return s.trace((f * eta * f.T) * X)


Rh = curvature(F)
qh = kinetic(F)
gih = F * eta * F.T
Pi = s.zeros(4)
for cc in range(4):
    for rr in range(4):
        curv = sum(F[mu, cc] * F[rr, aa] * F[nu, bb]
                   * R.get((mu, nu, aa, bb), 0)
                   for mu in range(4) for aa in range(4)
                   for nu in range(4) for bb in range(4))
        mat = sum(F[mu, cc] * gih[rr, nu] * X[mu, nu]
                  for mu in range(4) for nu in range(4))
        Pi[cc, rr] = s.simplify(Eh * ((Rh / 2 + lam * qh) * F[rr, cc]
                                     - curv - 2 * lam * mat))
Q = s.trace(Pi.T * e)
Ee = a * (Pi - Q * e.inv().T / 2)
Em = a * Q / (2 * m)
t = s.symbols('t', real=True)
checks = []
checks.append(('exact action identity',
               s.simplify(m * (curvature(e.inv()) / 2
                               + lam * kinetic(e.inv()))
                          - Eh * (Rh / 2 + lam * qh)) == 0))
for cc in range(4):
    for rr in range(4):
        de = s.zeros(4)
        de[cc, rr] = 1
        et = e + t * de
        Ft = et.inv()
        direct = s.diff(m * (curvature(Ft) / 2 + lam * kinetic(Ft)),
                        t).subs(t, 0)
        checks.append((f'old coframe row {cc},{rr}',
                       s.simplify(direct - Ee[cc, rr]) == 0))
        eht = eh + t * de
        Fht = eht.inv()
        directh = s.diff(eht.det() * (curvature(Fht) / 2
                                     + lam * kinetic(Fht)),
                         t).subs(t, 0)
        checks.append((f'material coframe row {cc},{rr}',
                       s.simplify(directh - Pi[cc, rr]) == 0))
checks.append(('measure row',
               s.simplify(Em - curvature(e.inv()) / 2
                          - lam * kinetic(e.inv())) == 0))
checks.append(('measure trace Ward',
               s.simplify(2 * m * Em + s.trace(Ee.T * e)) == 0))
ve = s.Matrix(list(e))
wi = s.Matrix(list(e.inv().T))
B = s.eye(16) - ve * wi.T / 2
checks.append(('full16 inverse Jacobian', B * B == s.eye(16)))
checks.append(('full16 determinant', (a * B).det() == -(m / E)**8))
n = s.Matrix([s.Rational(5, 4), s.Rational(3, 4), 0, 0])
hn = -eta + 2 * eta * n * n.T * eta
L = s.Matrix([[s.Rational(5, 4), -s.Rational(3, 4), 0, 0],
              [-s.Rational(3, 4), s.Rational(5, 4), 0, 0],
              [0, 0, 1, 0], [0, 0, 0, 1]])
checks.append(('positive observer root', L * L == hn and L.T * eta * L == eta))
failed = [name for name, ok in checks if not ok]

receipt = {
    'status': 'PASS' if not failed else 'FAIL',
    'checks': len(checks),
    'check_names': [name for name, _ in checks],
    'failed': failed,
    'action': str(s.simplify(m * (curvature(e.inv()) / 2
                                  + lam * kinetic(e.inv())))),
    'trace': str(s.trace(Ee.T * e)),
    'measure': str(Em),
    'jacobian_determinant': str((a * B).det()),
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'Exact rational tensor sign/Jacobian/field-pullback fixture; '
             'not native execution or universal physical selection.',
}
print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
if failed:
    raise SystemExit(1)
