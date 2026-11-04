#!/usr/bin/env python3
"""Exact XF reader application; no entropy/physical-price selection asserted."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

a,t=s.symbols('a t',real=True)
p=a*a
poly=a**4+a*a-1
v=s.Matrix([a,p]); G=s.Matrix([[a,-p],[p,a]])
X=s.Matrix([[0,1],[1,0]]); Z=s.diag(1,-1)
checks=[]
def need(ok,label):
    if not bool(ok): raise ArithmeticError(label)
    checks.append(label)
def red(e):
    num,den=s.fraction(s.cancel(e))
    return s.cancel(s.rem(num,poly,a)/s.rem(den,poly,a)) if not den.has(a) else s.rem(s.rem(num,poly,a)*s.invert(s.rem(den,poly,a),poly,a),poly,a)
def mat(M): return M.applyfunc(red)
def eq(A,B): return A.shape==B.shape and all(red(e)==0 for e in A-B)
def kron(*M): return s.kronecker_product(*M)
def power(n):
    out=s.eye(2)
    for _ in range(n): out=mat(G*out)
    return out
I2=s.eye(2); I4=s.eye(4)
q0=s.diag(1,0);q1=I2-q0
CX=kron(q0,I2)+kron(q1,X)
Evec=s.Matrix([(1-t*t)/(1+t*t),2*t/(1+t*t)])
E=Evec*Evec.T; P=v*v.T
need(eq(E*E,E),'generic rational real field projector is idempotent')
need(not eq(E*P,P*E),'field projector and actual born input projector are not generically commuting')
def controlled(A): return kron(A,I2)+kron(I2-A,X)
F=mat(controlled(E)*controlled(P)); Q=red((v.T*E*v)[0])
need(eq(F.T*F,I4),'full XF comparison is exactly orthogonal for generic field')
need(eq(F*kron(v,v),kron(E*v,v)+kron((I2-E)*v,X*v)),
     'actual initialized XF output retains both nonorthogonal flag sectors')
R0=kron(I2,CX)
need(eq(R0.T*R0,s.eye(8)),'literal single-CX reader is orthogonal on all8 columns')
need(eq(R0*R0,s.eye(8)),'actual CX reader inverse is the same paid primitive')
need(red(s.trace(R0*kron(F,I2))-s.trace(F))==0,
     'actual one-CX reader full trace equals original XF full trace')
need(red(s.diff(s.trace(R0*kron(F,I2)),t)-4*s.diff(Q,t))==0,
     'all-column trace field derivative remains exactly4 DQ')
state=mat(R0*kron(F,I2)*kron(v,v,v))
blocks=[s.Matrix([state[2*j+i] for j in range(4)]) for i in range(2)]
probs=[red((w.T*w)[0]) for w in blocks]
bflag0=red(p*p+p**3*Q)
q1=red(p*p+p**4-p**6*Q)
need(red(sum(probs)-1)==0,'both actual pointer outcomes exhaust the initialized state')
need(red(probs[1]-q1)==0,'actual pointer-one law is p2+p4-p6 Q')
need(red(probs[1]-(p*p*bflag0+p*(1-bflag0)))==0,
     'actual pointer law keeps canonical-born noise conditioned on the real flag')
need(red(s.diff(probs[1],t)+p**6*s.diff(Q,t))==0,
     'actual pointer field source is exactly minus p6 DQ')
need(red((v.T*X*v)[0]-2*a*p)==0,
     'conditional fresh-pointer vectors remain nonorthogonal; no perfect copy is claimed')
cold=red((kron(v,v,v).T*state)[0]); overlap=2*a*p
need(red(cold-Q*(p+p*p*overlap)-(1-Q)*a*p*(1+overlap))==0,
     'full prepared return includes actual born pointer and every bank/flag amplitude')
need(red(s.diff(cold,t)-(p+p*p*overlap-a*p*(1+overlap))*s.diff(Q,t))==0,
     'complete prepared cold first-source keeps the real reader coefficient')
oldX=kron(I2,X,I2)
transported=mat(R0*oldX*R0.T)
need(eq(transported,kron(I2,X,X)),
     'pointer initially spectator acquires joint X reader for inherited flag-X mark')
need(not eq(transported*kron(I4,Z),kron(I4,Z)*transported),
     'pointer freshness alone does not make inherited transported marks diagonal')
oldE=kron(E,I2,I2)
need(eq(R0*oldE*R0.T,oldE),'original commuting fine report effects stay pointer diagonal')
need(eq(kron(R0,I2).T*kron(R0,I2),s.eye(16)),
     'actual last-spectator embedding is orthogonal on all16 columns')
need(red(s.trace(kron(R0*kron(F,I2),I2))-2*s.trace(F))==0,
     'actual last spectator doubles trace without selecting a flag sector')
# Refine by the original bank report E.  Every branch retains B, f, r.
branch_probs=[]
for bank_effect in (E,I2-E):
    branch=mat(kron(bank_effect,I2,I2)*state)
    branch_probs.append([red(sum(branch[2*j+i]**2 for j in range(4))) for i in range(2)])
k=red(p*p+p**4-p**6)
need(red(branch_probs[0][1]-Q*k)==0 and red(branch_probs[1][1]-(1-Q)*(1-k))==0,
     'original report-conditioned pointer-one probabilities are complementary fixed laws')
need(red(k-2*p**3)==0,
     'conditional pointer-one parameter for original E report is exactly2 p3')
need(red(probs[1]-(Q*k+(1-Q)*(1-k)))==0,
     'all original report and pointer branches are kept in the joint law')
lo,hi=[ab for ab,m in s.Poly(poly,a).intervals(eps=s.Rational(1,10**40)) if ab[0]>0 and m==1][0]
need(lo>0 and hi<1,'positive Golden root gives a strictly nonzero pointer gain p6')
need(red((p*p+p**4-p**6/s.Integer(2))-s.Rational(1,2))==0,
     'on Q from0 to1/2 the actual pointer probability runs from p2+p4 to1/2')
print(json.dumps(dict(status='PASS',check_count=len(checks),checks=checks,
    checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    literal_reader=dict(g_calls=0,cx_calls=1,births=1,chronology='CX(f,r)',free_inverse=False),
    exact=dict(pointer_one='p^2+p^4-p^6 Q',pointer_gain='-p^6',
               conditional_pointer_one='2p^3 on E; 1-2p^3 on complement',
               prepared_cold='Q(p+p^2 s)+(1-Q)ap(1+s), s=2ap',trace_gain='1'),
    scope=dict(generic_real_field=True,all_columns=True,complete_Cost_Info_selected=False,
               pointer_algebra_exhaustion_proved=False,GR_closed=False)),sort_keys=True,indent=2))
