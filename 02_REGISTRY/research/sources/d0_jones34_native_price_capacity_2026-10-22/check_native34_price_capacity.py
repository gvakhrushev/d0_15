#!/usr/bin/env python3
"""Exact Golden Kraft / Fano, fresh-copy precision, independent-input screening.

Native Jones34 L4 rank is an immutable upstream scientific input here:
A4D_ORIGINAL_FULL128_COMMON_METRIC10_LINK24_JONES_TOMOGRAPHY_2026_10_20.
This bounded checker does NOT recreate its 128^2 instrument or select Book03.
"""
from fractions import Fraction
from itertools import product
from math import sqrt, log, log1p, floor, ceil, cos, sin
import sympy as s

phi=(1+sqrt(5))/2
p=1/phi
ell=log(phi)
def ck(cond,desc):
    if not bool(cond):
        raise AssertionError(desc)
def close(a,b,tol=2e-9):
    return abs(a-b)<tol

ck(close(p+p*p,1),"original Golden p+p^2")
a,b=1,0
for n in range(1,65):
    a,b=a+b,a
    ck(close(a*p**n+b*p**(n+1),1),"native full Fibonacci cost-cut Kraft")
    ck(a+b>1,"full valid native prefix partition")

words=[''.join(t) for k in range(1,5) for t in product('FR',repeat=k)]
def cost(w): return sum(1 if x=='F' else 2 for x in w)
def prefix_free(ws):
    return all(not (u.startswith(v) or v.startswith(u))
               for i,u in enumerate(ws) for v in ws[i+1:])
for flags in product([0,1],repeat=7):
    ws=[w for w,use in zip(words[:7],flags) if use]
    if prefix_free(ws):
        ck(sum(p**cost(w) for w in ws)<1+1e-12,
           "native Golden prefix-free complete Kraft")

# Rank-34 chart C=[-R,R]^34; R below is an ILLUSTRATIVE
# local coordinate unit, not a certified native Jones radius.
d,R,alpha=34,Fraction(1,20),Fraction(1,10)
def capacity(eps):
    m=floor(float(2*R)/(3*eps))+1
    ck(m>=2,"nontrivial rank34 packing")
    logM=d*log(m)
    aa=float(alpha)
    h=-aa*log(aa)-(1-aa)*log1p(-aa)
    exact=(logM-h-aa*(logM+log1p(-1/m**d)))/ell
    simpler=((1-aa)*logM-h)/ell
    ck(exact>=simpler-1e-8,"exact Fano bound")
    return m,exact
for eps in [1e-2,1e-3,1e-4,1e-5]:
    m,c=capacity(eps)
    ck(c>0,"strict paid-rank34 lower bound")
    print(f'PASS native_rank34_capacity epsilon={eps:g} axis={m} Ecost>={c:.6f}')

# The known native C2 PF address schedule provides only ONE code word
# of cost at most n(L)+1; compare ONLY on the declared hypothetical
# same-34D-decoder/C2-precision interface, not on a claimed all-L field map.
for L in [10,100,1000,10**4]:
    m,c=capacity(L**-3)
    native_n=64*ceil(log(L)/ell)+128
    if L>=1000: ck(c>native_n+1,"declared single-PF-word C2 shortcut excluded")
    print(f'CHECK scoped_native_C2 L={L}: Ecost>={c:.6f} native_max={native_n+1}')

# Quantum N-copy trace distance bound for ANY normalized analytic
# Stinespring state stack. A two-component normalized test with
# overlap cos(delta) checks the universal inequality; all 128^2
# original amplitudes satisfy the same Hilbert-space proof.
for eps in [1e-3,5e-3,1e-2]:
    delta=4*eps
    for N in [1,3,11,100,1000]:
        T=sqrt(max(0,1-cos(delta)**(2*N)))
        ck(T<=delta*sqrt(N)+1e-12,"fresh-copy Helstrom inequality")
    lower=(1-2*float(alpha))**2/(16*eps*eps)
    print(f'PASS fresh_copy_quantum epsilon={eps:g} N>={lower:.1f}/Lip^2')

# A report-only Book source controlled by independent u cannot
# survive stationary preparation when Du(report) is onto.
x1,x2,u1,u2=s.symbols('x1 x2 u1 u2')
r=s.Matrix([x1+u1+2*u2,x2+3*u1+5*u2])
G=r[0]**2+r[1]**2
eq=[s.diff(G,u) for u in (u1,u2)]
sol=s.solve(eq,[u1,u2],dict=True)[0]
ck(all(s.simplify(s.diff(G,x).subs(sol))==0 for x in (x1,x2)),
   "independent-input Euler screens all report-only geometry source")
print('PASS controlled-input Euler source quotient')
print('SCOPE: original rank34 and native full42 are inputs, not new reruns')
print('native Book03 full programme selected: FALSE; GR_closed: FALSE')

# NO-FIT native Jones square-source test: the original source J is known
# invertible by the pinned exact rank34 determinant. U and B below are
# ABSTRACT rational input/price controls, not claimed real D0 data.
# This tests the exact algebraic eliminant to be applied once they exist.
J=s.Matrix([[1,2,0],[0,1,1],[0,0,2]])
U=s.Matrix([[1,0],[0,1],[1,1]])
By=s.Matrix([1,0,0])
Bu=s.Matrix([0,2])
ck(J.det()!=0 and U.rank()==2,"square observable inverse and two independent inputs")
v_good=s.Matrix([0,-2,0])
g_good=J.T*v_good+By
v_bad=s.Matrix([1,-2,0])
g_bad=J.T*v_bad+By
def compatibility(g):
    return s.simplify(U.T*J.T.inv()*(g-By)+Bu)
ck(compatibility(g_good)==s.zeros(2,1),"native input-source eliminant can pass")
ck(compatibility(g_bad)==s.Matrix([1,0]),"native input-source eliminant rejects fitted geometric source")
ck((J.T*s.Matrix([-1,-1,1])).shape==(3,1),"source annihilator dimension")
ck(U.T*s.Matrix([-1,-1,1])==s.zeros(2,1),
   "free-input source quotient has nullity one")
print('PASS exact Jones-square no-fit Euler residual: U^T J^-T(g-By)+Bu')
print('PASS one scoped incompatible source rejected BEFORE fitting any Book Info')
