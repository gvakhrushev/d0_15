#!/usr/bin/env python3
"""Independent FLOATING-POINT Frechet controls; never an interval certificate."""
import argparse,json,pathlib
import numpy as np
from scipy.linalg import block_diag, expm, expm_frechet, eigh
HERE=pathlib.Path(__file__).resolve().parent

def counts(n):
    a,b=1,1
    for _ in range(n):a,b=a+b,a
    return a,b

def pack(z):return np.concatenate([a.ravel() for a in z])

def inc(z):return block_diag(z[0],z[1]),z[0]
def reg(z):return block_diag(*(np.kron(A,np.eye(A.shape[0])) for A in z))
def trace(z):return sum(A.shape[0]*np.trace(A) for A in z)
def embed(z,n,N):
    for _ in range(N-n):z=inc(z)
    return reg(z)

def make_reduce(n,N):
    sizes=counts(n);basis=[]
    for b,d in enumerate(sizes):
        for i in range(d):
            for j in range(d):
                U=[np.zeros((a,a),dtype=complex) for a in sizes];U[b][j,i]=1
                basis.append((b,i,j,embed(tuple(U),n,N)/d))
    def reduce(X):
        out=[np.zeros((a,a),dtype=complex) for a in sizes]
        for b,i,j,E in basis:out[b][i,j]=np.trace(X@E)
        return tuple(out)
    return reduce

def step(z,a,b):return ((a+b)*z[0][:a,:a]+a*z[1])/a,(a+b)/b*z[0][a:,a:]
def log_h(X):
    lam,Q=eigh(X)
    if lam.min()<=0:raise AssertionError('positive exponential factor required')
    return (Q*np.log(lam))@Q.conj().T

def dlog(X,V):
    lam,Q=eigh(X);Y=Q.conj().T@V@Q
    dd=np.empty((len(lam),len(lam)))
    for i,x in enumerate(lam):
        for j,y in enumerate(lam):
            dd[i,j]=1/x if abs(x-y)<1e-12*max(1,x,y) else np.log(x/y)/(x-y)
    return Q@(dd*Y)@Q.conj().T

def run():
    errors={};neg={}
    def eq(name,x,y,tol=2e-9):
        err=float(np.linalg.norm(np.asarray(x)-np.asarray(y)));errors[name]=err
        if not err<tol:raise AssertionError((name,err))
    rng=np.random.default_rng(7082026)
    def herm(d):
        X=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));return (X+X.conj().T)/(2*np.sqrt(d))
    N,m,n=2,1,0;a,b=counts(N);D=a*a+b*b;beta=.7
    L=herm(D)+3*np.eye(D);H=herm(D);Q=herm(D)
    Z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));rho=Z@Z.conj().T;rho/=np.trace(rho)
    drho=1j*(Q@rho-rho@Q)
    B,dB=expm_frechet(-beta*L,-beta*H)
    RN,RM=make_reduce(n,N),make_reduce(m,N)
    Mn,Mm=RN(B),RM(B)
    Kn=tuple(-log_h(A)/beta for A in Mn);Km=tuple(-log_h(A)/beta for A in Mm)
    Tn=tuple(-dlog(A,V)/beta for A,V in zip(Mn,RN(dB)))
    Tm=tuple(-dlog(A,V)/beta for A,V in zip(Mm,RM(dB)))
    sn,sm=RN(rho),RM(rho);dsn,dsm=RN(drho),RM(drho)
    eq('full_partition',trace(Mn),np.trace(B));eq('complete_tower',pack(Mn),pack(step(Mm,*counts(n))))
    eq('noncommuting_tangent_tower',pack(RN(dB)),pack(step(RM(dB),*counts(n))))
    def pair(a,b):return sum(A.shape[0]*np.trace(A@B) for A,B in zip(a,b))
    Cn=np.trace(rho@L)-pair(sn,Kn);Cm=np.trace(rho@L)-pair(sm,Km)
    Cnm=pair(sm,Km)-pair(sn,Kn)
    eq('archive_remainder_telescope',Cn,Cm+Cnm)
    dC=np.trace(drho@(L-embed(Kn,n,N)))+np.trace(rho@H)-pair(sn,Tn)
    dCdirect=np.trace(drho@L+rho@H)-pair(dsn,Kn)-pair(sn,Tn)
    eq('moving_state_source_formula',dC,dCdirect)
    dCm=np.trace(drho@L+rho@H)-pair(dsm,Km)-pair(sm,Tm)
    dCnm=pair(dsm,Km)+pair(sm,Tm)-pair(dsn,Kn)-pair(sn,Tn)
    eq('full_source_telescope',dC,dCm+dCnm)
    for eps in (1e-4,2e-5):
        def evaluate(t):
            Lt=L+t*H;U=expm(1j*t*Q);rt=U@rho@U.conj().T
            Kt=tuple(-log_h(A)/beta for A in RN(expm(-beta*Lt)))
            return np.trace(rt@Lt)-pair(RN(rt),Kt)
        fd=(evaluate(eps)-evaluate(-eps))/(2*eps)
        eq('independent_central_difference_'+str(eps),fd,dC,2e-7)
    neg['omit_moving_state_source']=float(abs(dC-(np.trace(rho@H)-pair(sn,Tn))))
    neg['commuting_only_exponential_derivative']=float(np.linalg.norm(dB+beta*B@H))
    neg['log_of_transfer_is_transfer_of_log']=float(np.linalg.norm(pack(Kn)-pack(RN(L))))
    if min(neg.values())<1e-6:raise AssertionError('weak negative diagnostic')
    # Full n=0 mismatch reference, exact golden J from the native inclusion.
    p=(np.sqrt(5)-1)/2;aa=np.sqrt(p)
    J=np.zeros((5,2));J[0,0]=aa;J[4,0]=p;J[3,1]=1
    P=J@J.T;Lc=np.eye(5)-P;Vc=herm(5);RR=make_reduce(0,1)
    Bc,dBc=expm_frechet(-beta*Lc,-beta*Vc);Mc=RR(Bc)
    Tactual=tuple(-dlog(A,V)/beta for A,V in zip(Mc,RR(dBc)))
    Tclosed=tuple(A/B[0,0] for A,B in zip(RR(Bc@Vc),Mc))
    eq('native_commutant_reference_all_jets',pack(Tactual),pack(Tclosed))
    eq('native_tangent_unital',pack(tuple(A/B[0,0] for A,B in zip(RR(Bc),Mc))),np.ones(2))
    # Block weights: exact finite expression compared with its Gibbs tilt.
    max_ratio=0.
    for n in range(4):
        a,b=counts(n);A=herm(a)*.3;B0=herm(b)*.3
        EA,EB=expm(-beta*A),expm(-beta*B0)
        W=max(eigh(A)[0].max(),eigh(B0)[0].max())-min(eigh(A)[0].min(),eigh(B0)[0].min())
        U=herm(a);V=herm(b);norm=max(np.linalg.norm(U,2),np.linalg.norm(V,2))
        t=p**(n+1)
        zPF=t*np.trace(EA)+p*t*np.trace(EB)
        valPF=(t*np.trace(EA@U)+p*t*np.trace(EB@V))/zPF
        for r in range(1,6):
            ma,mb=counts(n+2*r);na,nb=counts(n+r);dim=na*na+nb*nb
            zC=ma*np.trace(EA)+mb*np.trace(EB)
            valC=(ma*np.trace(EA@U)+mb*np.trace(EB@V))/zC
            epsilon=a*b*p**(2*n+2*r+3)/dim
            bound=2*np.exp(beta*W)*epsilon*norm
            ratio=float(abs(valC-valPF)/bound);max_ratio=max(max_ratio,ratio)
            if ratio>1+1e-7:raise AssertionError(('PF source bound',n,r,ratio))
    return {'status':'PASS_FLOATING_POINT_DIAGNOSTICS_NOT_INTERVAL',
            'errors':errors,'negative_diagnostic_gaps':neg,'max_PF_source_bound_ratio':max_ratio,
            'full_random_carrier_dimension':D,'physical_admission':False,'new_Lean':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=run()
    if args.write:(HERE/'af_heat_numeric_result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
