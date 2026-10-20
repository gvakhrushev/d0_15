#!/usr/bin/env python3
"""D0 original K(9,11,13) all-history scalar Book CP^2/even shear exact check.
Finite original carrier only; NOT compulsory full128/Lorentz action or GR.
"""
from fractions import Fraction as F
import sympy as s
import mpmath as m
m.mp.dps=65
n=(9,11,13)
k=(99,143,117)  # AB, BC, CA: original 359 undirected edges
S=sum(k); B=2*n[0]*n[1]*n[2]
assert (S,B)==(359,2574)
a,b,c,u,v,w,q,x=s.symbols('a b c u v w q x',nonzero=True)
M=s.Matrix([[0,b*u*q,c*w/q],[a*u/q,0,c*v*q],[a*w*q,b*v/q,0]])
assert s.simplify((x*s.eye(3)-M).det()-(x**3-(a*b*u**2+b*c*v**2+c*a*w**2)*x-a*b*c*u*v*w*(q**3+q**-3)))==0
r,ss,bb,kk,L=s.symbols('r ss bb kk L',nonzero=True)
D=3*r**2-ss
rp=(2*kk*r+bb)/D
Aee=-9*L*bb/(r*D)
implicit=Aee*L*(-1+rp/r+(6*r*rp-2*kk)/D)
target=36*L**2*bb*r*(ss-3*kk)/D**3
num=s.together(implicit-target).as_numer_denom()[0]
assert s.rem(num,r**3-ss*r-bb,r)==0

def mul(X,Y):
    a,b,c,d=X; A,B,C,D=Y
    return(a*A,a*B+b*A,a*C+c*A,a*D+b*C+c*B+d*A)
def add(X,Y):return tuple(a+b for a,b in zip(X,Y))
J=[]
for ki in k:
    Sj=(S,-2*ki,0,0)
    Bj=(B,-B,9*B//2,-9*B//2)
    tt=[(3,0,0,0),(0,0,0,0),(2*S,-4*ki,0,0)]
    for z in range(3,121):tt.append(add(mul(Sj,tt[z-2]),mul(Bj,tt[z-3])))
    out={}
    for z in range(2,121):
        aa,bt,ce,de=tt[z]
        out[z]=-F(2,z)*(F(de,aa)-F(bt*ce,aa*aa))
    J.append(out)
for z in range(2,121):
    ab,bc,ca=(J[i][z] for i in range(3))
    assert 4*ab==31*ca and 4*bc==-35*ca and ab+bc+ca==0
for z in (2,3,4,5,7):assert all(J[i][z]==0 for i in range(3))
assert J[0][6]!=0
ell=m.log((1+m.sqrt(5))/2)
rho=m.findroot(lambda t:t**3-S*t-B,22)
D0=3*rho**2-S
C=72*B*ell**2*rho/(D0**3)
G=[C*j for j in (31,-35,4)]
assert abs(sum(G))<m.mpf('1e-60')
for z in (6,12,24,48,96,120):
    g=[m.mpf(J[i][z].numerator)/J[i][z].denominator*ell**2 for i in range(3)]
    if z==120:assert abs(g[0]-G[0])<m.mpf('1e-28')
    print('original closed loops',z,'mixed AB',m.nstr(g[0],21))
assert abs(G[0]-m.mpf('0.0236080973930002220715242711254'))<m.mpf('1e-25')
# Exact current-resistance check for several nonuniform reversible native Cost backgrounds.
for weights in ((1,1,1),('1.12','.86','1.09'),('.64','1.21','.82')):
    ww=[m.mpf(i) for i in weights]
    sw=sum(ki*z*z for ki,z in zip(k,ww));bw=B*m.fprod(ww)
    rw=m.findroot(lambda r:r**3-sw*r-bw,rho)
    dw=3*rw*rw-sw
    masses=[(2*ki*z*z*rw+bw)/(rw*dw) for ki,z in zip(k,ww)]
    assert abs(sum(1/z for z in masses)-rw*dw/bw)<m.mpf('1e-50')
    assert abs(sum(masses)-1)<m.mpf('1e-50')
print('PASS_ORIGINAL_BOOK_CP_SIX_STEP_SHEAR exact full33 quotient, all lengths, 31:-35:4, Perron and resistance')
print('GR_closed=false; physical full128/CAR/metric-to-Cost still not identified')

# ALL-amplitude observable q_i(epsilon) changes along one exact forced ray.
def q_even(epsilon):
    Bee=B*m.cosh(3*ell*epsilon)
    rr=m.findroot(lambda zz:zz**3-S*zz-Bee,rho)
    theta=2*S*rr/(2*S*rr+3*Bee)
    qq=[(2*ki*rr+Bee)/(2*S*rr+3*Bee) for ki in k]
    assert max(abs(qq[i]-(theta*k[i]/S+(1-theta)/3)) for i in range(3))<m.mpf('1e-59')
    return theta,qq
th0,q0=q_even(m.mpf(0))
for ep in ('0.000415216862356397865','0.1','0.3','0.8'):
    theta,qq=q_even(m.mpf(ep))
    line=2*(th0-theta)/(3*S)
    assert line>0
    assert all(abs(qq[i]-q0[i]-line*(31,-35,4)[i])<m.mpf('1e-59') for i in range(3))
    assert theta<th0
print('PASS_ORIGINAL_BOOK_CP_FINITE_AMPLITUDE_EXACT_PROBABILITY_RAY')
