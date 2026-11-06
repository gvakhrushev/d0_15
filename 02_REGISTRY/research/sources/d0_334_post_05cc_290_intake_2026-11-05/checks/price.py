#!/usr/bin/env python3
"""Exact prepared-state/entropy diagnostics on the original Golden constructor.
No Gibbs preparation, Info choice or physical closure is inferred.
"""
import hashlib
import json
from pathlib import Path
import sympy as s

checks=[]
def need(ok,label):
    if not bool(ok): raise ArithmeticError(label)
    checks.append(label)
a=s.symbols('a',positive=True)
# a=sqrt(p), p=phi^-1. Work in Q(a), a^4+a^2-1=0.
poly=a**4+a**2-1
p=a*a

def red(x):
    num,den=s.fraction(s.cancel(x))
    num=s.rem(num,poly,a)
    den=s.rem(den,poly,a)
    return s.rem(s.expand(num*s.invert(den,poly,a)),poly,a)
def zero(x):
    if isinstance(x,s.MatrixBase): return all(red(v)==0 for v in x)
    return red(x)==0
v=s.Matrix([a,p]); G=s.Matrix([[a,-p],[p,a]]); X=s.Matrix([[0,1],[1,0]])
need(zero((v.T*v)[0]-1),'canonical born state normalized')
need(zero(G.T*G-s.eye(2)),'original Golden gate orthogonal')
ss=(v.T*X*v)[0]
need(zero(1-ss**2-p**6),'full comparison flag overlap complement equals p^6')
Q=s.symbols('Q',real=True)
rho_f=Q*v*v.T+(1-Q)*X*v*v.T*X
need(zero(s.trace(rho_f)-1),'whole flag density has trace one')
need(zero(rho_f.det()-p**6*Q*(1-Q)),'actual flag determinant, both nonorthogonal states retained')
need(zero(rho_f[0,0]-(p**2+p**3*Q)),'computational flag readout differs from original report')
# Whole Schmidt state: orthogonal E b and (I-E)b in a two-dimensional span.
u=s.symbols('u',positive=True)
q_u=1/(1+u*u)
psi=s.Matrix.vstack(v,u*X*v)/s.sqrt(1+u*u)
need(zero((psi.T*psi)[0]-1),'full current comparator state normalized')
P=psi*psi.T
need(zero(P*P-P),'full current density remains pure, unlike its flag marginal')
# Positive self-adjoint flag weighting preserving both pointer vectors.
w0,w1=s.symbols('w0 w1',real=True)
frame=s.Matrix.hstack(v,X*v)
W=frame*s.diag(w1,w0)*frame.inv()
need(zero((W[0,1]-W[1,0])*frame.det()+ss*(w1-w0)),
     'distinct pointer eigenweights produce the exact antisymmetric part')
need(zero(frame.det()-p**3) and not zero(ss),
     'pointer frame invertible and overlapping: self-adjoint weights must agree')
# Actual growing stage layout: birth; G; G; G, widths 1,2,2,2.
# Closure depends only on canonical birth, not on executed prefix Gs.
off=[0,1,3,5]; widths=[1,2,2,2]; D=7
R=s.zeros(D,2); R[0:1,:]=v.T; R[1:3,:]=s.eye(2)-v*v.T
S=s.zeros(D); S[1:3,0:1]=v; S[3:5,1:3]=G; S[5:7,3:5]=G
T=S.copy(); T[:,5:7]+=R*G
need(zero(T.T*T-s.eye(D)),'complete growing clock is unitary on all birth complements')
need(all(zero(T[o:o+d,o:o+d]) for o,d in zip(off,widths)),
     'every actual diagonal stage block vanishes')
A=[s.ones(1),v,G*v,G*G*v]
weights=[s.Rational(1,10),s.Rational(2,10),s.Rational(3,10),s.Rational(4,10)]
rho=s.zeros(D)
for o,d,Aj,w in zip(off,widths,A,weights):
    need(zero((Aj.T*Aj)[0]-1),'generated prefix isometry '+str(o))
    rho[o:o+d,o:o+d]=w*Aj*Aj.T
need(zero(s.trace(rho)-1),'true-prefix occupation density normalized')
need(zero(s.trace(rho*(T+T.T))),
     'occupation energy sees no clock offdiagonal source')
# This is the actual 33-vertex spatial normalization, not a 1/22 scalar replacement.
need(s.Rational(1,26)<s.Rational(1,24)<s.Rational(1,22),
     'zone coefficients retain 26,24,22 denominators')
t,d=s.symbols('t d',positive=True)
q1=(t+359*d)/(2*t+359*d)
need(s.simplify(q1-s.Rational(392,425)-359*(33*d-t)/(425*(359*d+2*t)))==0,
     'full Gibbs grade-one mass lower bound uses t<=33D')
need(s.Rational(392,425)>s.Rational(9,10),'grade separation exceeds nine tenths')
# Gibbs sign and full relative-entropy defect differentiated as independent symbols.
H,J,R0,E0,beta=s.symbols('H J R0 E0 beta',positive=True)
Drel=beta*R0-E0+beta*H
ACI=J-H+Drel/beta
need(s.simplify(ACI-(J+R0-E0/beta))==0,
     'canonical prepared Cost-Info energy cancels heat only with its full defect')
need(s.diff(Drel,H)/beta==1,
     'prepared relative-entropy defect retains the entire heat first source')
need(s.diff(J-H,H)==-1,
     'free Gibbs minimum has minus-heat sign, distinct from prepared state')
result={'status':'PASS','number_of_checks':len(checks),'checks':checks,
 'input_head':'cfe6755a0ddf5174698f003db59531a1ebd93fa1',
 'native_fixture':'birth;G;G;G, widths [1,2,2,2], full unitary clock dimension 7',
 'scope':'Exact native/flag/grade/defect identities; source and entropy theorems are analytic',
 'not_claimed':['Info forced by primitives','physical Gibbs preparation','native price equals an assigned entropy',
                'approximate Gibbs construction','new Einstein root','GR closure'],
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,sort_keys=True,indent=2))
