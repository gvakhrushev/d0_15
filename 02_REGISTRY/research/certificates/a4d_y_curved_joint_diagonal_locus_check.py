#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact diagonal Bloch locus of the curved z=1 Y connection symbol.

Uses the exact rational Laurent stencil owner.  On the diagonal
lambda_0=...=lambda_3=zeta, reconstructs the Laurent determinant from six
independent finite-field DFTs, CRT/rational-reconstructs its monic degree-12
palindromic factor R(y), y=zeta^4, checks an independent seventh prime, and
uses an exact Sturm count after y+y^-1 reduction.

No floating rank or root tolerance enters the terminal.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.ntheory.modular import crt

import a4d_y_curved_joint_rational_stencil as S

OUT=Path(__file__).with_name("a4d_y_curved_joint_diagonal_locus_results.json")
PRIMES=[1000193,1301249,1700353,2200321,2901761,3801857]
VERIFY_PRIME=4700161
N=256

EXPECTED=[
    F(1),
    F(-1882182356,6799975),
    F(237616643554,47599825),
    F(-12444399281988,333198775),
    F(13785586047815,93295657),
    F(-765415626241816,2332391425),
    F(141967660183684,333198775),
    F(-765415626241816,2332391425),
    F(13785586047815,93295657),
    F(-12444399281988,333198775),
    F(237616643554,47599825),
    F(-1882182356,6799975),
    F(1),
]

def check(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)

check("STENCIL_21_CONNECTION_SHIFTS",len(S.ATERMS)==21)
check("STENCIL_5_METRIC_SHIFTS",len(S.QTERMS)==5)
check("DIAGONAL_CONNECTION_EXPONENTS",set(sum(d) for d in S.ATERMS)=={-1,0,1})

def modfrac(q,p):
    if q.denominator%p==0:
        raise AssertionError("BAD_PRIME_DENOMINATOR")
    return (q.numerator%p)*pow(q.denominator,-1,p)%p

def diagonal_groups(p):
    groups={e:np.zeros((96,96),dtype=np.int64) for e in (-1,0,1)}
    for d,E in S.ATERMS.items():
        M=groups[sum(d)]
        for (i,j),q in E.items():
            M[i,j]=(M[i,j]+modfrac(q,p))%p
    return groups

def eval_A(groups,z,p):
    return (
        groups[-1]*pow(int(z),-1,p)
        + groups[0]
        + groups[1]*int(z)
    )%p

def detmod(A,p):
    A=A.copy()%p
    n=A.shape[0]
    det=1
    for c in range(n):
        nz=np.flatnonzero(A[c:,c])
        if not len(nz):
            return 0
        r=c+int(nz[0])
        if r!=c:
            A[[c,r]]=A[[r,c]]
            det=(-det)%p
        piv=int(A[c,c])
        det=det*piv%p
        inv=pow(piv,-1,p)
        rows=np.arange(c+1,n)
        rows=rows[A[rows,c]!=0]
        if len(rows):
            fac=(A[rows,c].copy()*inv)%p
            A[rows,c:]=(A[rows,c:]-fac[:,None]*A[c,c:])%p
    return det%p

def primitive_256(p):
    check("PRIME_1_MOD_256_"+str(p),sp.isprime(p) and (p-1)%256==0)
    for a in range(2,1000):
        w=pow(a,(p-1)//256,p)
        if pow(w,128,p)==p-1:
            check("ROOT256_ORDER_"+str(p),pow(w,256,p)==1)
            return w
    raise AssertionError("NO_ORDER_256_ROOT")

def diagonal_root_mod_p(p):
    groups=diagonal_groups(p)
    w=primitive_256(p)
    vals=np.zeros(N,dtype=np.int64)
    z=1
    for j in range(N):
        vals[j]=detmod(eval_A(groups,z,p),p)*pow(z,96,p)%p
        z=z*w%p

    invN=pow(N,-1,p)
    coeff=[0]*N
    for k in range(N):
        wk=pow(w,(-k)%N,p)
        cur=1
        total=0
        for j in range(N):
            total=(total+int(vals[j])*cur)%p
            cur=cur*wk%p
        coeff[k]=total*invN%p

    allowed=set(48+4*k for k in range(25))
    check("DIAGONAL_SUPPORT_"+str(p),
          all((coeff[k]==0) == (k not in allowed) for k in range(N)))

    a=[coeff[48+4*k] for k in range(25)]
    lc=a[-1]
    check("DIAGONAL_LEADING_NONZERO_"+str(p),lc!=0)
    ilc=pow(lc,-1,p)
    monic=[x*ilc%p for x in a]

    root=[0]*13
    root[12]=1
    inv2=pow(2,-1,p)
    for deg in range(23,11,-1):
        known=0
        for i in range(12):
            j=deg-i
            if 0<=j<12:
                known=(known+root[i]*root[j])%p
        root[deg-12]=(monic[deg]-known)*inv2%p

    square=[0]*25
    for i in range(13):
        for j in range(13):
            square[i+j]=(square[i+j]+root[i]*root[j])%p
    check("DIAGONAL_PERFECT_SQUARE_"+str(p),square==monic)
    return root

def rational_reconstruct(a,m):
    a%=m
    bound=math.isqrt(m//2)
    r0,r1=m,a
    s0,s1=0,1
    while abs(r1)>bound:
        q=r0//r1
        r0,r1=r1,r0-q*r1
        s0,s1=s1,s0-q*s1
    num,den=r1,s1
    if den<0:
        num,den=-num,-den
    g=math.gcd(num,den)
    num//=g
    den//=g
    if den<=0 or abs(num)>bound or den>bound or (a*den-num)%m:
        raise AssertionError("RATIONAL_RECONSTRUCTION_FAILED")
    return F(num,den)

residues=[diagonal_root_mod_p(p) for p in PRIMES]
modulus=math.prod(PRIMES)
reconstructed=[]
for k in range(13):
    residue=int(crt(PRIMES,[row[k] for row in residues])[0])
    reconstructed.append(rational_reconstruct(residue,modulus))
check("CRT_RATIONAL_ROOT_MATCHES_PINNED",reconstructed==EXPECTED)

independent=diagonal_root_mod_p(VERIFY_PRIME)
expected_mod=[
    q.numerator%VERIFY_PRIME*pow(q.denominator,-1,VERIFY_PRIME)%VERIFY_PRIME
    for q in EXPECTED
]
check("INDEPENDENT_PRIME_REPLAY",independent==expected_mod)

y,x=sp.symbols("y x")
R=sum(sp.Rational(q.numerator,q.denominator)*y**i for i,q in enumerate(EXPECTED))
factor_expected=(
    (y-1)**2
    *(y**2-258*y+1)
    *(31213*y**4-268044*y**3+824374*y**2-613116*y+74725)
    *(74725*y**4-613116*y**3+824374*y**2-268044*y+31213)
    /sp.Integer(2332391425)
)
check("R_EXACT_FACTORIZATION",sp.factor(R-factor_expected)==0)
check("R_PALINDROMIC",sp.expand(y**12*R.subs(y,1/y)-R)==0)

T=[sp.Integer(2),x]
for _k in range(2,7):
    T.append(sp.expand(x*T[-1]-T[-2]))
red=sp.Rational(EXPECTED[6].numerator,EXPECTED[6].denominator)
for k in range(1,7):
    q=EXPECTED[6+k]
    red += sp.Rational(q.numerator,q.denominator)*T[k]
red=sp.factor(red)
red_expected=(
    (x-258)*(x-2)
    *(2332391425*x**4-39166777608*x**3+242345032216*x**2
      -663086611488*x+635224971280)
    /sp.Integer(2332391425)
)
check("PALINDROMIC_REAL_REDUCTION",sp.factor(red-red_expected)==0)

num=sp.Poly(sp.together(red).as_numer_denom()[0],x,domain=sp.QQ)
check("UNIT_CIRCLE_STURM_COUNT_ONE",sp.count_roots(num,-2,2)==1)
check("ONLY_ENDPOINT_X2",num.eval(2)==0 and sp.count_roots(sp.div(num,sp.Poly(x-2,x))[0],-2,2)==0)

result={
    "schema":"a4d-y-curved-joint-diagonal-locus-v1",
    "terminal":"A4D-Y-CURVED-JOINT-DIAGONAL-BLOCH-LOCUS-CERTIFIED",
    "background":"z=1 exact Y vacuum; standard solder",
    "diagonal_bloch":"lambda0=lambda1=lambda2=lambda3=zeta",
    "determinant_zero_polynomial_up_to_nonzero_rational_unit":"R(zeta^4)^2",
    "R_monic_degree12":[str(q) for q in EXPECTED],
    "R_factorization":str(sp.factor(factor_expected)),
    "palindromic_reduction":str(sp.factor(red_expected)),
    "unit_circle_sturm_count":1,
    "unit_circle_root":"y=1",
    "diagonal_unit_torus_conclusion":"det A(zeta,zeta,zeta,zeta)=0 iff zeta^4=1",
    "reconstruction_primes":PRIMES,
    "independent_verification_prime":VERIFY_PRIME,
    "scope_fence":[
        "exact diagonal Bloch line only",
        "does not prove transverse-to-diagonal joint injectivity",
        "does not prove the global all-Bloch locus or nonlinear range theorem",
    ],
}
check("RESULTS_MATCH_PINNED_JSON",result==json.loads(OUT.read_text()))
print("TERMINAL A4D-Y-CURVED-JOINT-DIAGONAL-BLOCH-LOCUS-CERTIFIED")
