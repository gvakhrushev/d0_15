#!/usr/bin/env python3
"""Native even-word density, endogenous prefix cut, original K(9,11,13) clock heat.
Exact rational finite identities plus explicit full-spectrum numerical controls.
Not a physical-admission or full native GR runtime-selection certificate.
"""
from __future__ import annotations
import collections,json,sys
from fractions import Fraction as F
import numpy as np
import sympy as s
import mpmath as mp
mp.mp.dps=80

count=0

def require(ok,message):
    global count
    count+=1
    if not bool(ok):raise ArithmeticError(message)

def zero(A,message):require(all(s.cancel(x)==0 for x in A),message)

def close(a,b,message,tol=1e-10):
    require(np.max(np.abs(np.asarray(a)-np.asarray(b)))<=tol*max(1.,np.max(np.abs(np.asarray(a))),np.max(np.abs(np.asarray(b)))),message)

# Exact algebraic irrationality obstruction: all cyclotomic trace conjugates
# lie in [-2,2], but this Golden conjugate lies below -2.
p=(s.sqrt(5)-1)/2
x=2*s.sqrt(5)-4
require(s.expand(x*x+8*x-4)==0,'Golden doubled-angle trace polynomial')
require(bool(-2*s.sqrt(5)-4 < -2),'opposite Golden conjugate excludes a root-of-unity angle')
require(s.simplify(2*(p-p*p)-x)==0,'literal G gives that doubled-angle trace')

# Every skew real Pauli word is a CNOT conjugate of local J, up to sign.
# Pauli convention P(a,b)=X^a Z^b, q=a dot b mod2; signs do not affect the span.
# CNOT c->t updates a_t ^= a_c, b_c ^= b_t.
orbits=[]
for n in range(2,7):
    pairs=[(c,t) for c in range(n) for t in range(n) if c!=t]
    seed=(1,1);seen={seed:0};queue=collections.deque([seed]);skew_preserved=True
    while queue:
        aa,bb=queue.popleft()
        for c,t in pairs:
            an=aa ^ (((aa>>c)&1)<<t)
            bn=bb ^ (((bb>>t)&1)<<c)
            v=(an,bn)
            skew_preserved=skew_preserved and (an&bn).bit_count()%2==1
            if v not in seen:seen[v]=seen[(aa,bb)]+1;queue.append(v)
    require(skew_preserved,'all conjugations preserve the real skew Pauli class')
    d=1<<n
    require(len(seen)==d*(d-1)//2,'all so(2^n) skew basis directions are reached')
    expected={(aa,bb) for aa in range(d) for bb in range(d) if (aa&bb).bit_count()%2}
    require(set(seen)==expected,'orbit equals the whole skew Pauli set, not just the right count')
    orbits.append({'qubits':n,'matrix_dimension':d,'skew_basis':len(seen),'max_CNOT_conjugation_length':max(seen.values())})
    if n<=3:
        mats=[]
        for aa,bb in sorted(seen):
            T=np.zeros((d,d),dtype=np.int64)
            for k in range(d):T[k^aa,k]=(-1)**((bb&k).bit_count())
            require(np.array_equal(T.T,-T) and np.array_equal(T@T,-np.eye(d,dtype=np.int64)),'actual skew Pauli matrix')
            mats.append(T.reshape(-1))
        stack=np.stack(mats)
        require(np.array_equal(stack@stack.T,d*np.eye(len(mats),dtype=np.int64)), 'all real skew basis matrices are exactly trace orthogonal')

# The count above checks the finite bit action; the all-n transitivity proof
# and Lie-generation argument are in PROOF.md, not inferred from samples.

def rot(q):
    return s.Matrix([[1-q*q,-2*q],[2*q,1-q*q]])/(1+q*q)

N=4;d=2
A=s.eye(d)
first=[rot(s.Rational(1,3)),rot(-s.Rational(2,5)),rot(s.Rational(1,7))]
frames=[A]
for g in first:
    A=g*A;frames.append(A)
P0=s.diag(1,0)
Z=s.diag(1,-1)
Ap=rot(s.Rational(1,2))
U=Ap.T*Z*Ap
last=U*A.T
stages=first+[last]
V=s.eye(d)
for g in stages:V=g*V
zero(V-U,'literal four-stage complete monodromy')
S=s.zeros(N*d);R=s.zeros(N*d);Pdyn=s.zeros(N*d)
for k,g in enumerate(stages):
    nxt=(k+1)%N
    S[nxt*d:(nxt+1)*d,k*d:(k+1)*d]=g
    R[k*d:(k+1)*d,k*d:(k+1)*d]=frames[k]
    Pdyn[k*d:(k+1)*d,k*d:(k+1)*d]=frames[k]*P0*frames[k].T
S0=s.zeros(N*d)
for k in range(N-1):S0[(k+1)*d:(k+2)*d,k*d:(k+1)*d]=s.eye(d)
S0[0:d,(N-1)*d:N*d]=U
zero(R.T*S*R-S0,'ALL clock columns: prefix gauge removes intermediate gates exactly')
zero(R.T*Pdyn*R-s.diag(*([P0]*N)),'retained cut is generated from actual prefixes')
C=(s.eye(N*d)-Pdyn)*S*Pdyn
Fclock=R.T*C.T*C*R
Fexpected=s.zeros(N*d)
Fend=P0*U.T*(s.eye(d)-P0)*U*P0
Fexpected[(N-1)*d:N*d,(N-1)*d:N*d]=Fend
zero(Fclock-Fexpected,'one autonomous step with generated cut has EXACT endpoint feedback')
require(s.trace(Fend)==s.Rational(576,625),'nonzero original reflection return effect')

# The ORIGINAL actual scene graph K(9,11,13), with actual degree normalization.
sizes=(9,11,13);scene=sum(sizes)
labels=np.repeat(np.arange(3),sizes)
Adj=(labels[:,None]!=labels[None,:]).astype(float)
require(int(Adj.sum()/2)==359,'literal original scene edge count')
deg=Adj.sum(axis=1)
require(set(deg.astype(int))=={20,22,24},'literal original scene degrees')
Rscene=np.diag(1/np.sqrt(deg+2))
B=Rscene@Adj@Rscene;Cscene=Rscene@Rscene
close(np.linalg.norm(Cscene,2),1/22,'actual internal-clock edge coefficient')

def twisted_shift(U,N):
    d=U.shape[0];T=np.zeros((N*d,N*d),dtype=U.dtype)
    for k in range(N-1):T[(k+1)*d:(k+2)*d,k*d:(k+1)*d]=np.eye(d)
    T[:d,(N-1)*d:]=U
    return T

def heat0(U,N):
    T=twisted_shift(U,N)
    return np.eye(scene*N*U.shape[0])-np.kron(B,np.eye(N*U.shape[0]))-np.kron(Cscene,T+T.conj().T)

def full_H01(U,N,beta):
    L=heat0(U,N)
    vals=np.linalg.eigvalsh(L)
    require(vals.min()>-1e-12,'actual normalized incidence heat is positive')
    d=U.shape[0]
    Z0=np.exp(-beta*vals).sum()
    # E-V =359*N*d for the entire scene x closed-clock graph.
    Z01=359*N*d+2*Z0
    return np.log(Z01)/beta,Z0

def rfloat(i,j,t,d=4):
    U=np.eye(d);c,ss=np.cos(t),np.sin(t)
    U[i,i]=U[j,j]=c;U[j,i]=ss;U[i,j]=-ss
    return U

beta=float(2*((np.sqrt(5)-1)/2)**2)
Rfixed=np.diag([1.,1.,-1.,-1.])
Nclock=4
Hs=[]
for theta in (0.,.21,.53):
    A=rfloat(0,2,theta)@rfloat(1,3,theta/3)
    UU=A.T@Rfixed@A
    HH,Z0=full_H01(UU,Nclock,beta)
    Hs.append({'angle':theta,'H01':float(HH),'Z0':float(Z0)})
    close(np.linalg.eigvalsh(UU),[-1.,-1.,1.,1.],'field-dependent reflection has the COMPLETE fixed spectrum')
for row in Hs[1:]:close(row['H01'],Hs[0]['H01'],'whole native stage/scene heat is field independent for ideal comparisons',tol=2e-12)

# Exact equitable partition of THIS original scene preserves ALL 33 modes.
# Each zone contributes n_j-1 true within-zone modes and one quotient mode.
betamp=2*((mp.sqrt(5)-1)/2)**2
sizesmp=[mp.mpf(v) for v in sizes];degreesmp=[mp.mpf(35-v) for v in sizes]
def scene_heat_trace(lam):
    quotient=mp.zeros(3)
    out=mp.mpf(0)
    for i in range(3):
        quotient[i,i]=1-lam/degreesmp[i]
        out+=(sizesmp[i]-1)*mp.exp(-betamp*(1-lam/degreesmp[i]))
        for j in range(i):
            quotient[i,j]=quotient[j,i]=-mp.sqrt(sizesmp[i]*sizesmp[j]/(degreesmp[i]*degreesmp[j]))
    vals=mp.eigsy(quotient,eigvals_only=True)
    return out+sum(mp.exp(-betamp*v) for v in vals)
def H01_from_phases(phases,N):
    Z0=mp.mpf(0)
    for phase in phases:
        for k in range(N):
            Z0+=scene_heat_trace(2*mp.cos((phase+2*mp.pi*k)/N))
    return mp.log(359*N*len(phases)+2*Z0)/betamp,Z0
baseHmp,baseZ0mp=H01_from_phases([mp.mpf(0),mp.mpf(0),mp.pi,mp.pi],Nclock)
close(float(baseHmp),Hs[0]['H01'],'all 30 within-zone modes plus 3 quotient modes equal the full 528-dimensional trace')
close(float(baseZ0mp),Hs[0]['Z0'],'equitable exact scene reduction retains the complete 0-grade trace')

# Non-reflection compiler error changes the monodromy heat; do not freeze it.
U0=Rfixed
baseH,_=full_H01(U0,Nclock,beta)
clock_controls=[]
for aerr in (.02,.05,.1):
    VV=rfloat(0,1,aerr)@U0
    delta=np.linalg.norm(VV-U0,2)
    Ldelta=np.linalg.norm(heat0(VV,Nclock)-heat0(U0,Nclock),2)
    require(Ldelta<=delta/11+1e-13,'literal full runtime heat operator error <= delta/11')
    Hnew,_=H01_from_phases([mp.mpf(str(aerr)),-mp.mpf(str(aerr)),mp.pi,mp.pi],Nclock)
    error=abs(Hnew-baseHmp)
    require(0<error<=mp.mpf(str(delta))/11,'nonzero complete H01 source error is controlled without dropping modes')
    clock_controls.append({'angle_error':aerr,'monodromy_error':float(delta),'H01_error':mp.nstr(error,35),'upper_bound':float(delta/11)})

# Actual density is proven for EVEN native words. Exact CNOT^2 identity permits
# a common finite audit clock without changing the completed operation.
CX=s.zeros(4)
for b0 in range(4):CX[b0^(1 if b0&2 else 0),b0]=1
zero(CX*CX-s.eye(4),'exact native identity padding: CNOT squared')

print(json.dumps({'status':'PASS_NATIVE_CLOCK_AND_FULL_COLUMN_COMPILER_CONTROLS',
 'checks':count,'python':sys.version.split()[0],'sympy':s.__version__,
 'skew_Pauli_CNOT_orbits':orbits,
 'exact_clock_columns':N*d,'end_feedback':'576/625',
 'original_scene_vertices':33,'original_scene_edges':359,
 'full_0grade_dimension_tested':33*Nclock*4,
 'full_0plus1_dimension_counted':(33+392)*Nclock*4,
 'ideal_reflection_heat_controls':Hs,'actual_clock_error_controls':clock_controls,
 'large_GR_native_word_emitted':False,'prepared_prefix_cut_selection_from_M1':False,
 'complete_Book_native_selection_proved':False,'raw216_closed':False,
 'unconditional_GR_closed':False},indent=2))
