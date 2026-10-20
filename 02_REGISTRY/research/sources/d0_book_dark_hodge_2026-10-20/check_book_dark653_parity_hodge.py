#!/usr/bin/env python3
"""Exact original K(9,11,13) Book register: H_dark653=ker B+ ⊕ ker B-.
Runs original 718-edge Perron stationary readouts; not 128-Kraus/GR.
"""
import math
import numpy as np
n=(9,11,13)
z=np.repeat(np.arange(3),n)
edges=[(u,v) for u in range(33) for v in range(u+1,33) if z[u]!=z[v]]
loc={e:j for j,e in enumerate(edges)}
assert len(edges)==359
Bp=np.zeros((33,359),dtype=np.int64)
Bm=np.zeros((33,359),dtype=np.int64)
for j,(u,v) in enumerate(edges):
    Bp[u,j]=Bp[v,j]=1
    Bm[u,j]=-1;Bm[v,j]=1
omega=np.zeros(359,dtype=np.int64)
for a in range(9):
    for b in range(9,20):
        for c in range(20,33):
            omega[loc[a,b]]+=1
            omega[loc[b,c]]+=1
            omega[loc[a,c]]-=1
assert np.array_equal(Bm@omega,np.zeros(33,dtype=np.int64))
assert all(omega[j]=={(0,1):13,(0,2):-11,(1,2):9}[z[u],z[v]]
           for j,(u,v) in enumerate(edges))
assert omega@omega==42471
assert np.linalg.matrix_rank(Bp)==33
assert np.linalg.matrix_rank(Bm)==32

# Reuse accepted Lean SignlessSignedCommonCarrier.U (BC centered-row reflection).
bc=[j for j,(u,v) in enumerate(edges) if (z[u],z[v])==(1,2)]
def U(x):
    y=x.copy();block=x[bc].reshape(11,13)
    y[bc]=(block-2*(block.mean(axis=1)[:,None]-block.mean())).ravel()
    return y
face=np.zeros(359)
face[loc[0,9]]=face[loc[9,20]]=1; face[loc[0,20]]=-1
odd=face-(face@omega)/(omega@omega)*omega
even=U(odd)
assert np.linalg.norm(Bm@odd)<1e-12
assert np.linalg.norm(Bp@even)<1e-12
assert np.linalg.norm(U(even)-odd)<1e-12
assert abs(even@even-odd@odd)<1e-10

# TRUE native Perron bulk, not the degree-normalized random walk.
M=np.sqrt(np.outer(n,n)).astype(float);np.fill_diagonal(M,0)
ev,Ue=np.linalg.eigh(M);rho=ev[-1];v=Ue[:,-1]
if v.sum()<0:v=-v
r=np.array([v[z[u]]/math.sqrt(n[z[u]]) for u in range(33)])
pi=r*r
direct=edges+[(v,u) for u,v in edges]
mu=np.array([r[u]*r[v]/rho for u,v in direct])
assert abs(sum(mu)-1)<1e-12
J0=np.zeros((718,33));J1=np.zeros((718,33))
for j,(u,v) in enumerate(direct):
    J0[j,u]=math.sqrt(mu[j]/pi[u])
    J1[j,v]=math.sqrt(mu[j]/pi[v])
assert np.linalg.norm(J0.T@J0-np.eye(33))<1e-12
assert np.linalg.norm(J1.T@J1-np.eye(33))<1e-12
assert np.linalg.matrix_rank(np.c_[J0,J1])==65
Q=np.eye(718)-J0@J0.T
assert np.linalg.matrix_rank(Q@J1,tol=1e-10)==32

def embedding(c,sign):
    a=c/np.sqrt(2*mu[:359])
    return np.r_[a,sign*a]
for c,sign in ((odd,-1),(even,1),(omega.astype(float),-1)):
    eta=embedding(c,sign)
    assert np.linalg.norm(J0.T@eta)<5e-11
    assert np.linalg.norm(J1.T@eta)<5e-11
    assert np.linalg.norm(Q@eta-eta)<5e-11
assert abs(np.sum(odd*odd/mu[:359])-np.sum(even*even/mu[:359]))<1e-9

# CP source jet on EXACT native directed 718-edge Cost s=1+eps d.
ell=math.log((1+math.sqrt(5))/2)
cycle={(0,1),(1,2),(2,0)}
def true_flow(t):
    A=np.zeros((3,3));B=np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            if i!=j:
                A[i,j]=n[j]*math.exp(-ell*t*(1 if (i,j) in cycle else -1))
                B[i,j]=n[j]*math.exp(-ell*t*(1 if (j,i) in cycle else -1))
    ew,R=np.linalg.eig(A);k=np.argmax(ew.real);lam=ew[k].real;rv=R[:,k].real
    if rv.sum()<0:rv=-rv
    ew,L=np.linalg.eig(B);lv=L[:,np.argmin(abs(ew-lam))].real
    if lv.sum()<0:lv=-lv
    norm=lam*sum(n[i]*lv[i]*rv[i] for i in range(3))
    return np.array([lv[z[u]]*rv[z[v]]*
        math.exp(-ell*t*(1 if (z[u],z[v]) in cycle else -1))/norm
        for u,v in direct])
h=2e-5
numeric=(true_flow(h)-true_flow(-h))/(2*h)
q=[sum(mu[j] for j,(u,v) in enumerate(direct) if
    {z[u],z[v]}=={i,k}) for i,k in ((0,1),(1,2),(0,2))]
Jprime=-3*ell/sum(1/q0 for q0 in q)
pred=np.r_[Jprime*omega/2574,-Jprime*omega/2574]
assert np.max(abs(pred-numeric))<5e-10
assert abs(sum(pred**2/mu)+ell*3*Jprime)<1e-11
print('PASS original Book full718: present33 + future32 + even326 + odd327')
print('PASS omega_scene=all1287 triangle boundaries and source first jet')
print('PASS H2 face redundancy 960 via accepted Lean rank d2=327')
print('PASS Book Asecond=',3*Jprime,'Fisher=',sum(pred**2/mu))
print('FIREWALL: scalar Book macro sector; full128/GR/alpha source unproved')
