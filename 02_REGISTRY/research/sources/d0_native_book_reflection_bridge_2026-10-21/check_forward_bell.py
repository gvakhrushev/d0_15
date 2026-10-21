#!/usr/bin/env python3
"""Forward-only native Golden Bell overlap -> exact Book complementary source.

One forward circuit and a conjugate paid copy, never V^dagger.
Tests true all-column rank-one source and universal 1/D obstruction.
"""
from __future__ import annotations
import json,math
import numpy as np
import sympy as sp

p=(sp.sqrt(5)-1)/2
phi=1/p
z=sp.Rational(1,2**20)
a=sp.sqrt(p)
checks=[]
def ck(t,label):
    if not bool(t): raise ArithmeticError(label)
    checks.append(label)

def gate_on_one(gate,n,qubit):
    m=np.array([[1.0]])
    for k in range(n):m=np.kron(m,gate if k==qubit else np.eye(2))
    return m

def cnot(n,control,target):
    out=np.zeros((2**n,2**n),complex)
    for i in range(2**n):
        j=i
        if (i>>(n-1-control))&1:j^=1<<(n-1-target)
        out[j,i]=1.
    return out

g=np.array([[float(a),-float(p)],[float(p),float(a)]])
h=np.array([[1,1],[1,-1]],float)/math.sqrt(2)
X=np.array([[0,1],[1,0]],float)
# Register order report,work,report-copy,work-copy; choose D=2.
n=4
Bprep=cnot(n,1,3)@gate_on_one(h,n,1)@cnot(n,0,2)@gate_on_one(g,n,0)
# Native X on both report legs: reference has c0=p, c1=sqrt(p).
Bprep=cnot(n,1,3)@gate_on_one(h,n,1)@gate_on_one(X,n,0)@gate_on_one(X,n,2)@cnot(n,0,2)@gate_on_one(g,n,0)
Bellvec=Bprep[:,0]
ref=np.zeros(16,complex)
for b in (0,1):
    for w in (0,1):
        idx=b*8+w*4+b*2+w
        ref[idx]=(float(p) if b==0 else float(a))/math.sqrt(2)
ck(np.linalg.norm(Bellvec-ref)<1e-13,'fixed Golden+H+CNOT Bell inverse has correct native coefficients')
ck(np.linalg.norm(Bprep.conj().T@Bprep-np.eye(16))<1e-13,'fixed native Bell transform unitary')
ck(abs(np.vdot(Bellvec,Bellvec)-1)<1e-13,'Bell vector uses p+p^2 exactly')

def householder(psi):
    psi=np.array(psi,dtype=complex)
    e0=np.zeros_like(psi);e0[0]=1
    v=e0-psi
    if np.linalg.norm(v)<1e-12:return np.eye(len(psi))
    return np.eye(len(psi))-2*np.outer(v,v.conj())/np.vdot(v,v)

for x,y in [(.6,.8),(5/13,12/13),(.8,.6),(.96,.28)]:
    psi=np.array([x,0.,y,0.],complex)
    ck(abs(np.vdot(psi,psi)-1)<1e-12,'native two-record test state normalized')
    V=householder(psi)
    ck(np.linalg.norm(V.conj().T@V-np.eye(4))<1e-12,'forward reporter unitary')
    U=Bprep.conj().T@np.kron(V,np.conj(V))
    ret=U[0,0]
    r=float(abs(psi[2])**2+abs(psi[3])**2)
    expected=(float(p)*(1-r)+float(a)*r)/math.sqrt(2)
    ck(abs(ret-expected)<1e-12,'forward-only two-copy true amplitude matches original probability')
    ck(np.linalg.norm(U.conj().T@U-np.eye(16))<1e-12,'full two-copy U unitary')
    feedback=1-abs(ret)**2
    ck(abs(feedback-(1-(float(p)+(float(a)-float(p))*r)**2/2))<1e-12,
       'true full complement includes all Bell-failure states')
    # The reverse *reference* Bell word is fixed. No V^dagger appears in U.

# Exact gain, source sign, and strict positivity for every allowed report.
r=sp.symbols('r',real=True)
D=sp.symbols('D',positive=True)
t=(p+(a-p)*r)/sp.sqrt(D)
F=1-t**2
J=-sp.log(1-z*F)
ck(sp.simplify(sp.diff(F,r)+2*(a-p)*(p+(a-p)*r)/D)==0,
   'exact forward-only complement first source')
ck(sp.simplify(sp.diff(J,r)+2*z*(a-p)*(p+(a-p)*r)/(D*(1-z*F)))==0,
   'complete Book first jet with D penalty')
ck(float(sp.N(a-p))>0,'native Golden coefficients have strictly unequal amplitudes')
ck(float(sp.N(sp.diff(J,r).subs({r:sp.Rational(1,2),D:2})))<0,
   'Book source orientation agrees with minus-Shannon CQ')

L=4*p**3
Q=1-z*L
RR=1-z*L*(1+p**6)
r0=1-Q*RR
Hp=sp.log((1-r0)/r0)/sp.log(phi)
W=sp.symbols('W',positive=True)
gain=-sp.diff(J,r).subs(r,r0)/(W*Hp)
ck(float(sp.N(gain.subs({D:2,W:10})))>0,
   'all42 common source gain is positive on native N1 root')

# Compare native complete N1 matched-cost source and paired-book source on four
# truly independently varied report branches. Both are gradients of real values.
weights=[1,2,3,4]
coords=sp.symbols('x0:4',real=True)
rb=sum(w*q for w,q in zip(weights,coords))/sum(weights)
S_CQ=-sum(w*(q*sp.log(q)+(1-q)*sp.log(1-q))*(-1/sp.log(phi)) for w,q in zip(weights,coords))
# The above is -sum w*h_phi(q). Verify sign before comparing.
S_CQ=-sum(w*(-(q*sp.log(q)+(1-q)*sp.log(1-q))/sp.log(phi)) for w,q in zip(weights,coords))
B=J.subs({r:rb,D:2})
gain2=gain.subs({D:2,W:sum(weights)})
for i,v in enumerate(coords):
    dB=sp.diff(B,v).subs({x:r0 for x in coords})
    dS=sp.diff(S_CQ,v).subs({x:r0 for x in coords})
    ck(sp.simplify(dB-gain2*dS)==0,f'same-source independent native report copy {i}')

# Sharp dimension bound for ANY full-column probability representing
# Bell bra of unit norm on two outcome subspaces of equal dimension D:
# c0,c1 constant on each D-dimensional branch => D(c0^2+c1^2)<=1.
# In particular |t|<=1/sqrt(D), |t'|<=sqrt(2/D), |F'|<=2sqrt(2)/D.
for dim in (2,4,8,16,128,1024):
    for theta in (0.0,.1,.43,1.1,1.57,2.3):
        c0=math.cos(theta)/math.sqrt(dim)
        c1=math.sin(theta)/math.sqrt(dim)
        for prob in (0.0,.2,.5,.8,1.0):
            amp=c0*(1-prob)+c1*prob
            source=-2*amp*(c1-c0)
            ck(abs(source)<=2*math.sqrt(2)/dim+1e-13,
               f'universal full-column Bell source bound D={dim}')

# A coherent original archive cannot be declared physically prepared twice
# without paying two actual underlying full-input histories. A single source
# can even have a non-real phase; its conjugate is a second typed gate map.
complexpsi=np.array([.6,0,0,.8j],complex)
ck(abs(np.vdot(complexpsi,complexpsi)-1)<1e-13,'complex-phase actual history control')
complexamp=np.vdot(Bellvec,np.kron(complexpsi,np.conj(complexpsi)))
rcomplex=abs(complexpsi[2])**2+abs(complexpsi[3])**2
ck(abs(complexamp-((float(p)*(1-rcomplex)+float(a)*rcomplex)/math.sqrt(2)))<1e-12,
   'original complex phases cancel ONLY with supplied conjugate history')
wrongamp=np.vdot(Bellvec,np.kron(complexpsi,complexpsi))
ck(abs(wrongamp-complexamp)>1e-2,'identical rather than conjugate complex copy fails')

out={
  'status':'PASS', 'check_count':len(checks),
  'native':{'golden_p':str(sp.N(p,20)), 'n1_r0':str(sp.N(r0,20)),
            'forward_return':'(p+(sqrt(p)-p)*r)/sqrt(D)',
            'complete_complement':'1-(p+(sqrt(p)-p)*r)^2/D',
            'book_source_gain_D2_W10':str(sp.N(gain.subs({D:2,W:10}),20))},
  'full_column_no_free_gain':{'bound':'abs(dF/dr)<=2*sqrt(2)/D',
                             'universal_full_output_basis_required':True},
  'memory':{'V_inverse_uses':0, 'forward_conjugate_copy_required':True,
            'second_paid_initial_preparation_required':True,
            'unmeasured_full_record_source_cut_required':True},
  'scope':{'conditional_same_field_first_source':True,
           'native_conjugate_writer_admitted':False,
           'full_clock_Info_price_composed':False,
           'GR_closed':False}
}
print(json.dumps(out,indent=2,sort_keys=True))
