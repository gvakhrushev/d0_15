#!/usr/bin/env python3
"""Exact finite solder obstruction on the selected Newton correction line.

Exact rational functions in QQ(t), with the same Cayley role convention and
stored base coframe ETA as the order-one owner. Two independently computed
solder Euler entries have numerator gcd t on the open Cayley chart. At t=0,
the old full Lorentz defect persists and every det/adj joint residual is zero.
Thus no point of THIS LINE at fixed ETA is full stationary for any of the
four-channel coefficients or affine translations. This does not exclude all
points of the seven-dimensional support or variable solder off this slice.

A separate exact unit-iterate control includes arbitrary free solder: the
solder Hessian is invertible at t=1, forcing degenerate zero solder there.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
from itertools import permutations
from pathlib import Path

import sympy as sp
from sympy import QQ, Rational
from sympy.polys.fields import field


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print('PASS_' + name)


p = Path(__file__).with_name('a4d_resolved_curved_stationary_e2_support7_order1_check.py')
spec = importlib.util.spec_from_file_location('support7_order1_owner', p)
owner = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(owner)

K,t=field('t',QQ)
zero,one=K.zero,K.one

def mc(a): return [[K.from_expr(a[i,j]) for j in range(a.cols)] for i in range(a.rows)]
def mz(n,m=None): return [[zero for _ in range(n if m is None else m)] for _ in range(n)]
def madd(a,b): return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def mscale(s,a): return [[s*x for x in row] for row in a]
def mmul(a,b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))),zero) for j in range(len(b[0]))] for i in range(len(a))]
def mt(a): return [list(r) for r in zip(*a)]
def minv(a):
 n=len(a); aug=[list(a[i])+[one if i==j else zero for j in range(n)] for i in range(n)]
 for k in range(n):
  pivot=next(i for i in range(k,n) if aug[i][k])
  aug[k],aug[pivot]=aug[pivot],aug[k]
  q=aug[k][k]; aug[k]=[x/q for x in aug[k]]
  for i in range(n):
   if i!=k and aug[i][k]:
    q=aug[i][k]; aug[i]=[x-q*y for x,y in zip(aug[i],aug[k])]
 return [r[n:] for r in aug]
def md(a):
 n=len(a); out=zero
 for perm in permutations(range(n)):
  inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
  v=one
  for i in range(n): v*=a[i][perm[i]]
  out+=(-1 if inversions%2 else 1)*v
 return out

def wedge(a,b): return [a[i]*b[j]-a[j]*b[i] for i,j in owner.PAIRS]
I=mc(sp.eye(4)); eta=mc(owner.ETA)
A=[madd(mc(a),mscale(t,mc(h))) for a,h in zip(owner.generators0,owner.H_by_role)]
den=[madd(I,mscale(-K.from_expr(Rational(1,2)),a)) for a in A]
U=[mmul(madd(I,mscale(K.from_expr(Rational(1,2)),a)),minv(d)) for a,d in zip(A,den)]
Ui=[mmul(mmul(eta,mt(u)),eta) for u in U]
assert all(mmul(u,ui)==I for u,ui in zip(U,Ui))
check('EXACT_LORENTZ_INVERSES', all(mmul(u,ui)==I for u,ui in zip(U,Ui)))
curves={}
for r,s in owner.PAIRS:
 P=mmul(mmul(mmul(U[r],U[s]),Ui[r]),Ui[s])
 Pi=mmul(mmul(eta,mt(P)),eta)
 C=mscale(K.from_expr(Rational(1,2)),madd(P,mscale(-one,Pi)))
 Ce=mmul(C,eta)
 c=[[Ce[i][j]] for i,j in owner.PAIRS]
 curves[(r,s)]=[x[0] for x in mmul(mc(owner.G2*owner.STAR),c)]

Theta=mc(owner.ETA)
grad=mz(4)
S=zero
for f, response in curves.items():
 r,s=f; u,v=[i for i in range(4) if i not in f]
 vu=[Theta[i][u] for i in range(4)]; vv=[Theta[i][v] for i in range(4)]
 sg=owner.orientation(f)
 S+=16*sg*sum((x*y for x,y in zip(wedge(vu,vv),response)),zero)
 for a in range(4):
  ea=[one if i==a else zero for i in range(4)]
  for b in range(4):
   dw=[zero]*6
   if b==u: dw=[x+y for x,y in zip(dw,wedge(ea,vv))]
   if b==v: dw=[x+y for x,y in zip(dw,wedge(vu,ea))]
   grad[a][b]+=16*sg*sum((x*y for x,y in zip(dw,response)),zero)
assert sum((Theta[i][j]*grad[i][j] for i in range(4) for j in range(4)),zero)==2*S

g=None
for row in grad:
 for v in row:
  if v:
   g=v.numer.monic() if g is None else g.gcd(v.numer).monic()

check('ALL_SOLDER_NUMERATOR_GCD_IS_T', g == t.numer)
P = K.from_expr(
    787729723*sp.Symbol('t')**5 + 11910201168580*sp.Symbol('t')**4
    + 57328162663980*sp.Symbol('t')**3 - 4300465765648*sp.Symbol('t')**2
    - 5810906816*sp.Symbol('t') + 29560863488)
Q = K.from_expr(
    32783181538633*sp.Symbol('t')**4 + 468038424932*sp.Symbol('t')**3
    - 1604236731760*sp.Symbol('t')**2 + 56982657472*sp.Symbol('t')
    + 3772793856)
q = 372817*t**2 - 4992*t - 2704
expected12 = -16*t*P/(13*(11*t-52)**2*(11*t+52)**2*(173*t-13))
expected13 = 16*t*Q/((173*t-13)*q**2)
check('SOLDER_12_EXACT_REDUCED_RATIONAL_FUNCTION', grad[1][2] == expected12)
check('SOLDER_13_EXACT_REDUCED_RATIONAL_FUNCTION', grad[1][3] == expected13)
check('P_Q_ARE_COPRIME', P.numer.gcd(Q.numer) == K.ring.one)
u, v, bezout = P.numer.gcdex(Q.numer)
check('EXPLICIT_BEZOUT_IDENTITY_ONE',
      bezout == K.ring.one and u*P.numer+v*Q.numer == K.ring.one)
print('OBSTRUCTION_POLYNOMIAL_P', str(P.as_expr()))
print('OBSTRUCTION_POLYNOMIAL_Q', str(Q.as_expr()))
print('BEZOUT_COEFFICIENTS_COMPUTED_EXACTLY', 'degrees', u.degree(), v.degree())

chart = [md(d) for d in den]
expected_chart = [
    -2*(173*t-13)*(173*t+13)/169,
    K.from_expr(2), -q/2704,
    -(11*t-52)*(11*t+52)/2704]
check('FOUR_EXACT_CAYLEY_CHART_FACTORS', chart == expected_chart)
chart_product = one
for d in chart:
    chart_product *= d
chart_square = chart_product.numer**2
for i, row in enumerate(grad):
    for j, value in enumerate(row):
        check(f'SOLDER_{i}_{j}_DENOMINATOR_ONLY_CHART_UNITS',
              chart_square.rem(value.denom) == K.ring.zero)
check('T_ZERO_AND_UNIT_INSIDE_CHART', all(
    d.numer.evaluate(0, point) != 0 for d in chart for point in (0, 1)))
print('CHART_DETERMINANTS', [str(d.as_expr()) for d in chart])

# A necessary full solder condition is grad=0. Its two entries reduce to
# t*P=t*Q=0, and Bezout forces t=0 over R (in fact in any characteristic-zero
# field). This is a genuine finite line obstruction, not a Taylor truncation.
check('BASE_SOLDER_EULER_ZERO', all(
    value.numer.evaluate(0, 0) == 0 for row in grad for value in row))
check('BASE_STORED_SOLDER_NONDEGENERATE', owner.ETA.det() == -1)
check('BASE_LORENTZ_DEFECT_NONZERO', list(owner.base_missing) ==
      [-16, 0, 16, 0, -32, 64, 0, -32])
for r, s in owner.PAIRS:
    p0 = owner.role0[r]*owner.role0[s]*owner.role0[r].inv()*owner.role0[s].inv()
    m0 = sp.eye(4)-p0
    check(f'BASE_FACE_{r}_{s}_DET_ADJ_BLIND',
          m0.det() == 0 and m0.adjugate() == sp.zeros(4))
# Every joint residual is det(Mf)*tg - Mg*adj(Mf)*tf, zero here for arbitrary
# translations. Every quadratic residual channel has zero first derivative.
# Hence the nonzero base link defect cannot be repaired by those channels.
check('STAR_FIRST_PATH_COEFFICIENT',
      S.diff(t).as_expr().subs(sp.Symbol('t'), 0) == sp.Rational(8384, 13))
check('SOLDER_SCALE_FIRST_PATH_COEFFICIENT',
      (2*S).diff(t).as_expr().subs(sp.Symbol('t'), 0) == sp.Rational(16768, 13))

# Hostile extension of the unit point: test all 16 free solder entries,
# rather than relying on a single gradient at fixed ETA.
Hunit = sp.zeros(16)
for f, response in curves.items():
    u0, v0 = [i for i in range(4) if i not in f]
    response1 = sp.Matrix([z.as_expr().subs(sp.Symbol('t'), 1) for z in response])
    for a in range(4):
        for c in range(4):
            val = 16*owner.orientation(f)*(owner.wedge(
                sp.eye(4)[:, a], sp.eye(4)[:, c]).T*response1)[0]
            Hunit[4*a+u0,4*c+v0] += val
            Hunit[4*c+v0,4*a+u0] += val
check('UNIT_SOLDER_HESSIAN_SYMMETRIC', Hunit == Hunit.T)
check('UNIT_SOLDER_HESSIAN_INVERTIBLE', Hunit.rank() == 16 and Hunit.det() != 0)
check('UNIT_HESSIAN_REPRODUCES_LITERAL_SOLDER_GRADIENT',
      Hunit*sp.Matrix(list(owner.ETA)) == sp.Matrix([
          value.as_expr().subs(sp.Symbol('t'),1) for row in grad for value in row]))
print('EXACT_SCOPE: selected one-dimensional Newton line at fixed ETA, any four-channel c and b')
print('RESULT: solder stationarity forces t=0; base full link stationarity fails')
print('UNIT_POINT_FREE_SOLDER_RESULT: Htheta invertible, so solder-critical Theta=0 is degenerate')
print('STATUS: seven independent amplitudes and their full finite coupled equations remain open')
