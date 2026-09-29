#!/usr/bin/env python3
"""Exact small-z splitting of the 16-dimensional flat Y connection kernel.

Uses the exact rational identity H(z)=P(z)/(4+3 z^2), deg P <= 4, then
performs two nested Schur reductions. The final order-six 4x4 block has rank 2.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix
import a4d_y_curved_response_quotient_check as B

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"02_REGISTRY/research/certificates/a4d_y_small_amplitude_kernel_splitting_results.json"
z=sp.symbols("z"); D=4+3*z*z

def check(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n)

def mj(M): return [[str(sp.factor(M[i,j])) for j in range(M.cols)] for i in range(M.rows)]

def run(write=False):
    Hz,labels,_=B.action_connection_hessian(z)
    Pk=[sp.zeros(96) for _ in range(5)]
    maxdeg=0
    for i in range(96):
        for j in range(96):
            e=Hz[i,j]
            if e==0: continue
            pe=sp.Poly(sp.cancel(D*e),z)
            check("COMMON_DENOMINATOR_ENTRY",pe.is_univariate)
            maxdeg=max(maxdeg,pe.degree())
            for k in range(5): Pk[k][i,j]=pe.nth(k)
    check("COMMON_NUMERATOR_DEGREE_LE4",maxdeg<=4)

    q=[sp.Rational(0)]*7
    q[0]=sp.Rational(1,4)
    for n in range(2,7,2): q[n]=-sp.Rational(3,4)*q[n-2]
    H=[]
    for n in range(7):
        M=sp.zeros(96)
        for k in range(min(4,n)+1): M+=Pk[k]*q[n-k]
        H.append(M)

    H0=H[0]
    N=sp.Matrix.hstack(*H0.nullspace())
    check("FLAT_KERNEL_DIM16",N.cols==16)
    _,rem=N.T.rref(); rem=list(rem)
    keep=[i for i in range(96) if i not in rem]
    R=sp.zeros(96,80)
    for c,i in enumerate(keep): R[i,c]=1
    check("FLAT_SPLIT_BASIS",sp.Matrix.hstack(R,N).det()!=0)

    Ar=[R.T*M*R for M in H]
    Br=[R.T*M*N for M in H]
    Cr=[N.T*M*R for M in H]
    Dr=[N.T*M*N for M in H]
    A0i=DomainMatrix.from_Matrix(Ar[0]).convert_to(QQ).inv().to_Matrix()
    X=[A0i]
    for n in range(1,7):
        T=sp.zeros(80)
        for j in range(1,n+1): T+=Ar[j]*X[n-j]
        X.append((-A0i*T).applyfunc(sp.cancel))
    Ks=[]
    for n in range(7):
        K=Dr[n].copy()
        for i in range(n+1):
            for j in range(n-i+1): K-=Cr[i]*X[j]*Br[n-i-j]
        Ks.append(K.applyfunc(sp.factor))
    ranks=[K.rank() for K in Ks]
    check("FIRST_SCHUR_RANKS",ranks==[0,0,12,12,14,14,14])

    V=sp.Matrix.hstack(*Ks[2].nullspace())
    check("K2_KERNEL_DIM4",V.cols==4)
    _,rm=V.T.rref(); rm=list(rm)
    keep2=[i for i in range(16) if i not in rm]
    W=sp.zeros(16,12)
    for c,i in enumerate(keep2): W[i,c]=1
    A=[W.T*Ks[n]*W for n in range(2,7)]
    Bv=[W.T*Ks[n]*V for n in range(3,7)]
    Db=[V.T*Ks[n]*V for n in range(4,7)]
    Ai=DomainMatrix.from_Matrix(A[0]).convert_to(QQ).inv().to_Matrix()
    Xi=[Ai]
    for n in range(1,3):
        T=sp.zeros(12)
        for j in range(1,n+1): T+=A[j]*Xi[n-j]
        Xi.append((-Ai*T).applyfunc(sp.cancel))
    Es=[]
    for n in range(3):
        E=Db[n].copy()
        for p in range(n+1):
            for qn in range(n-p+1): E-=Bv[p].T*Xi[qn]*Bv[n-p-qn]
        Es.append(E.applyfunc(sp.factor))
    check("E4_ZERO",Es[0]==sp.zeros(4))
    check("E5_ZERO",Es[1]==sp.zeros(4))
    target=sp.diag(0,0,sp.Rational(9,8),sp.Rational(3,8))
    check("E6_EXACT",Es[2]==target)
    check("E6_RANK2",Es[2].rank()==2)
    V2=V*sp.Matrix.hstack(*Es[2].nullspace())
    check("FINAL_KERNEL_DIM2",V2.cols==2)

    idx={lab:i for i,lab in enumerate(labels)}
    y=sp.zeros(96,1); d=sp.zeros(96,1)
    for ph,sg in ((0,1),(2,-1)):
        for g,c in ((3,1),(4,-1),(5,1)): y[idx[(ph,0,g)],0]=sg*c
    for ph,sg in ((0,-1),(2,1)):
        for g in (0,1,2): d[idx[(ph,0,g)],0]=sg
    cy=sp.Matrix(list(next(iter(sp.linsolve((N,y))))))
    cd=sp.Matrix(list(next(iter(sp.linsolve((N,d))))))
    check("Y_TANGENT_FINAL",sp.Matrix.hstack(V2,cy).rank()==2)
    check("DUAL_TANGENT_FINAL",sp.Matrix.hstack(V2,cd).rank()==2)

    data={
      "schema":"a4d-y-small-amplitude-kernel-splitting-v1",
      "base":"flat period-four Y family, connection Hessian after exact 80-dimensional flat-range elimination",
      "hessian_rational_form":{"common_denominator":"4+3*z^2","common_numerator_degree_at_most":4},
      "flat_kernel_dimension":16,
      "effective_series_ranks":{f"K{i}":ranks[i] for i in range(7)},
      "after_K2_kernel_dimension":4,
      "proper_degenerate_reduction":{"E4":mj(Es[0]),"E5":mj(Es[1]),"E6":mj(Es[2]),"E6_rank":2,"final_kernel_dimension":2},
      "final_kernel_contains":["Y tangent","boost-dual tangent"],
      "scaling":{"twelve_transverse_modes":"O(z^2)","two_soft_transverse_modes":"O(z^6)","two_exact_center_modes":"identically zero","worst_transverse_inverse_loss":"O(z^-6)"},
      "terminal":"A4D-Y-SMALL-AMPLITUDE-KERNEL-SPLITTING-CERTIFIED",
      "nonclaim":"this is the zero-slow-momentum connection Hessian splitting; it does not by itself prove the h-uniform nonlinear response theorem"
    }
    if write:
        OUT.write_text(json.dumps(data,indent=2)+"\n"); print("WROTE",OUT)
    else:
        check("RESULTS_MATCH_PINNED_JSON",data==json.loads(OUT.read_text()))
    print("TERMINAL",data["terminal"])
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--write",action="store_true"); a=ap.parse_args(); run(a.write)
