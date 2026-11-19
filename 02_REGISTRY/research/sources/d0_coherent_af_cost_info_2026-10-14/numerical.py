#!/usr/bin/env python3
"""Independent floating-point checks, NOT interval or full-theory proofs."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, block_diag, eigh
HERE=Path(__file__).resolve().parent
p=(np.sqrt(5.)-1)/2
lnphi=-np.log(p)
I=np.eye(2,dtype=complex)
rho=np.array([[.6,.1j],[-.1j,.4]],complex)
K0=np.diag([3/5,5/13]).astype(complex)
K1=np.array([[3/5,-4/5],[4/5,3/5]],complex)@np.diag([4/5,12/13])
X=np.array([[0,1j],[1j,0]],complex)/7
Y=np.array([[0,1j],[1j,0]],complex)/11

def ck(name,cond):
    if not bool(cond):raise AssertionError(name)

def gram(A,r):return np.array([[np.trace(x@r@y.conj().T) for y in A] for x in A])
def dg(A,dA,r,dr):return np.array([[np.trace(dx@r@y.conj().T+x@dr@y.conj().T+x@r@dy.conj().T) for y,dy in zip(A,dA)] for x,dx in zip(A,dA)])
def levels(t=0.,jets=False):
    k0=K0;k1=expm(t*X)@K1;r=expm(t*Y)@rho@expm(-t*Y)
    A,B=[k0],[k1];DA,DB=[np.zeros((2,2),complex)],[X@k1];dr=Y@r-r@Y
    out=[]
    for n in range(3):
        sa,sb=gram(A,r),gram(B,r)
        da,db=dg(A,DA,r,dr),dg(B,DB,r,dr)
        out.append((sa,sb,da,db))
        aa,bb=[k0@x for x in A]+B,[k1@x for x in A]
        daa,dbb=[k0@x for x in DA]+DB,[X@k1@x+k1@dx for x,dx in zip(A,DA)]
        A,B,DA,DB=aa,bb,daa,dbb
    return out

def logs(A):
    d,U=eigh(A)
    ck('faithful_log_test_stratum',d.min()>1e-9)
    return (U*np.log(d))@U.conj().T

def rel(A,B):return float(np.trace(A@(logs(A)-logs(B))).real)
def source(A,dA,B):return float(np.trace(dA@(logs(A)-logs(B))).real)/lnphi

def main():
    data=levels();out={'status':'PASS','method':'floating_point_diagnostics_not_interval','points':[]}
    fs=[];ds=[]
    for n,(A,B,dA,dB) in enumerate(data):
        M=block_diag(A,B);D=block_diag(dA,dB)
        ref=block_diag(np.eye(len(A))*p**(n+1),np.eye(len(B))*p**(n+2))
        value=rel(M,ref)/lnphi;jet=source(M,D,ref)
        eps=1e-5
        def at(t):
            x,y,*_=levels(t)[n];return rel(block_diag(x,y),ref)/lnphi
        finite=(at(eps)-at(-eps))/(2*eps)
        ck('full_noncommuting_source',abs(jet-finite)<3e-7)
        ck('source_not_frozen',abs(jet)>1e-5)
        P=np.diag(np.diag(M));correction=rel(M,P)/lnphi
        ck('coherence_decomposition',abs(value-rel(P,ref)/lnphi-correction)<1e-10)
        fs.append(value);ds.append(jet)
        out['points'].append({'level':n,'net_cost':value,'analytic_source':jet,'finite_difference':finite,'coherence_cost':correction,'smallest_eigenvalue':float(eigh(M,eigvals_only=True).min())})
    for n in range(2):
        A,B,_,_=data[n];F,W,dF,dW=data[n+1]
        fine=block_diag(F,W);dfine=block_diag(dF,dW)
        recovered=block_diag(p*A,B,p*p*A)
        gap=rel(fine,recovered)/lnphi
        sourcegap=float(np.trace(dfine@(logs(fine)-logs(recovered))).real)/lnphi
        ck('exact_finite_entropy_chain',abs(fs[n+1]-fs[n]-gap)<1e-10)
        ck('true_joint_source_chain',abs(ds[n+1]-ds[n]-sourcegap)<1e-9)
        ck('positive_information_increment',gap>0)
        out['points'][n+1]['increment']=gap
        out['points'][n+1]['increment_source']=sourcegap
    # Independent genuine noncommutative block state: no generated state ansatz.
    V=expm(.17j*np.array([[0,1,0],[1,0,1],[0,1,0]],complex))
    full=V@np.diag([.2,.3,.5])@V.conj().T
    X0=full[:2,:2];Y0=full[2:,2:];W0=np.array([[.25]],complex)
    # Make a valid A_(n+1)=M_3 + M_2 state (a=2,b=1).
    F=.75*full;W=np.diag([.1,.15]).astype(complex)
    A=F[:2,:2]+W;B=F[2:,2:]
    ref1=block_diag(p*p*np.eye(2),p**3*np.eye(1))
    ref2=block_diag(p**3*np.eye(3),p**4*np.eye(2))
    R=block_diag(p*A,B,p*p*A);sig=block_diag(F,W)
    ck('arbitrary_noncommuting_AF_chain',abs(rel(sig,ref2)-rel(block_diag(A,B),ref1)-rel(sig,R))<1e-10)
    print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
