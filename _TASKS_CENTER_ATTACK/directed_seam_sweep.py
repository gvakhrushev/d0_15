#!/usr/bin/env python3
"""DIRECTED SEAM SWEEP (round 1): directed edge operators compressed to the OWNED dim-30 archive.
The symmetric-impossibility theorem forces the alpha seam into the directed class; directed owned
operators live on the edge carrier (Hashimoto B, flip J, family B+tJ). The owned raw maps S,T
(Xi-theorem) compress them to the 33-vertex carrier. Sweep: for each directed edge operator X,
build the vertex compression X_v = T X S^T (33x33, integer, generally NON-symmetric), split into
active (zone-sum, rank-3) / archive (kernel, dim-30) blocks, and compute the exact moment triple
  mu1 = Tr(B C)/rank,  mu2 = Tr(B N C),  mu3 = Tr(B N^2 C)   (N = archive block of X_v)
target: (1/3, 12288/5, 0). Also report the seam ranks. Everything exact (Fraction).
This is a SWEEP: null results are results. Exit 0 always (report-only), FAIL only on internal errors."""
from fractions import Fraction as F
import numpy as np

zones=[9,11,13]; n=33
zone_of=[]
for zi,z in enumerate(zones): zone_of+=[zi]*z
A=np.array([[1 if zone_of[i]!=zone_of[j] else 0 for j in range(n)] for i in range(n)],dtype=np.int64)
edges=[(i,j) for i in range(n) for j in range(n) if A[i,j]]
NE=len(edges); idx={e:k for k,e in enumerate(edges)}
S=np.zeros((n,NE),dtype=np.int64); T=np.zeros((n,NE),dtype=np.int64)
J=np.zeros((NE,NE),dtype=np.int64); B=np.zeros((NE,NE),dtype=np.int64)
for (u,v),k in idx.items():
    S[u,k]=1; T[v,k]=1; J[k,idx[(v,u)]]=1
    for w in range(n):
        if A[v,w] and w!=u: B[k,idx[(v,w)]]=1

# exact projector data: active = zone-indicator span (3), archive = kernel (30)
# use exact rational projections via block structure: P_act = sum_z (1/|z|) 1_z 1_z^T
Pact=np.zeros((n,n),dtype=object)
start=0
for z in zones:
    for i in range(start,start+z):
        for j in range(start,start+z):
            Pact[i,j]=F(1,z)
    start+=z
Iden=np.array([[F(1) if i==j else F(0) for j in range(n)] for i in range(n)],dtype=object)
Pker=Iden-Pact

def frac_mat(M): return np.array([[F(int(x)) for x in row] for row in M],dtype=object)
def mm(*Ms):
    R=Ms[0]
    for M in Ms[1:]: R=R@M
    return R
def tr(M): return sum(M[i,i] for i in range(M.shape[0]))

candidates={
 "X = Hashimoto B (directed non-backtracking)": B,
 "X = B - J (directed with flip subtracted)":   B-J,
 "X = B @ J (compose transfer with flip)":      B@J,
}
print(f"target: mu1=1/3, mu2=12288/5, mu3=0   (rank divisor = 3)")
for name,X in candidates.items():
    Xv=frac_mat(T@X@S.T)                      # 33x33 exact, directed
    Bs=mm(Pact,Xv,Pker)                       # active <- archive seam
    Cs=mm(Pker,Xv,Pact)                       # archive <- active
    Ns=mm(Pker,Xv,Pker)                       # archive block (directed)
    m1=tr(mm(Bs,Cs))/3
    m2=tr(mm(Bs,Ns,Cs))
    m3=tr(mm(Bs,Ns,Ns,Cs))
    seam_nonzero = any(Bs[i,j]!=0 for i in range(n) for j in range(n))
    print(f"{name}\n  seam nonzero: {seam_nonzero} | mu1={m1} mu2={m2} mu3={m3}")
    if m1!=0:
        print(f"  ratio mu2/(3*mu1) = {m2/(3*m1) if m1 else 'n/a'}  (target 12288/5 = 2457.6)")
print("SWEEP COMPLETE (report-only round 1)")
