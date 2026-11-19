#!/usr/bin/env python3
"""Exact control: split dimensions do not determine the feedback source."""
import json
import sympy as s

t, z = s.symbols('t z', positive=True)
c = (1 - t**2) / (1 + t**2)
sn = 2 * t / (1 + t**2)
U = s.Matrix([[c, 0, -sn], [0, 1, 0], [sn, 0, c]])
I = s.eye(3)

PA = s.diag(1, 1, 0)
QA = I - PA
PB = s.diag(1, 0, 1)
QB = I - PB

def zero_matrix(M):
    return all(s.simplify(x) == 0 for x in M)

checks = []
def check(name, condition):
    if not bool(condition):
        raise RuntimeError('FAIL: ' + name)
    checks.append(name)

check('same fixed finite carrier', PA.shape == PB.shape == U.shape)
check('same retained and traced ranks', PA.rank() == PB.rank() == 2 and QA.rank() == QB.rank() == 1)
check('both are orthogonal complementary splits',
      PA*PA == PA and PB*PB == PB and QA*QA == QA and QB*QB == QB
      and zero_matrix(PA*QA) and zero_matrix(PB*QB))
check('same tick is orthogonal', zero_matrix(U.T*U - I))

FA = s.simplify(PA * U.T * QA * U * PA)
FB = s.simplify(PB * U.T * QB * U * PB)
check('first split has nonzero return', FA == s.diag(sn**2, 0, 0))
check('second split has zero return', zero_matrix(FB))

detA = s.factor(s.det(I - z*FA))
detB = s.factor(s.det(I - z*FB))
check('first full determinant', s.simplify(detA - (1 - z*sn**2)) == 0)
check('second full determinant', detB == 1)

JA_dt = s.factor(s.diff(-s.log(detA), t))
expected = 8*z*t*(1-t**2) / ((1+t**2)**3 * (1 - 4*z*t**2/(1+t**2)**2))
check('first source exact', s.simplify(JA_dt - expected) == 0)
at_half = s.factor(JA_dt.subs(t, s.Rational(1, 2)))
check('strictly positive rational control',
      at_half.subs(z, s.Rational(1, 2)) == s.Rational(96, 85))

result = {
    'status': 'PASS',
    'check_count': len(checks),
    'checks': checks,
    'same_split_dimensions': {'carrier': 3, 'retained': 2, 'traced': 1},
    'same_tick': 'orthogonal rotation in the (e1,e3) plane',
    'F_first': 'diag(4*t^2/(1+t^2)^2,0,0)',
    'F_second': '0',
    'J_first': '-log(1-4*z*t^2/(1+t^2)^2)',
    'J_second': '0',
    'dJ_first_dt': '8*z*t*(1-t^2)/((1+t^2)^3*(1-4*z*t^2/(1+t^2)^2))',
    'dJ_first_dt_at_t=z=1/2': '96/85',
    'dJ_second_dt': '0',
    'scope': 'abstract finite retained/traced interface only; no physical D0 cut selected'
}
print(json.dumps(result, indent=2, sort_keys=True))
