#!/usr/bin/env python3
"""All-original718 Book Cost−Info Hessian = native 685-archive metric;
symmetric AB Cost innovation = native 32-future archive, oriented cycle
innovation wholly in 653 dark archive. RESEARCH, no full D0 GR claim.
"""
import math
import numpy as np

phi=(1+math.sqrt(5))/2
p=1/phi
ell=math.log(phi)
N=33
zone=np.array([0]*9+[1]*11+[2]*13)
edges=np.array([(u,v) for u in range(N) for v in range(N)
                if zone[u]!=zone[v]], dtype=int)
assert edges.shape==(718,2)
u,v=edges[:,0],edges[:,1]
E=len(u)

def native(t=0.):
    K=np.zeros((N,N))
    sym_AB=(np.minimum(zone[u],zone[v])==0)&(np.maximum(zone[u],zone[v])==1)
    K[u,v]=p*np.exp(-ell*t*sym_AB)
    eigen,R_eig=np.linalg.eigh(K)
    lam=float(eigen[-1])
    right=R_eig[:,-1]
    if right.sum()<0:right=-right
    assert right.min()>0
    pi=right**2
    P=np.zeros((N,N))
    P[u,v]=K[u,v]*right[v]/(lam*right[u])
    f=pi[u]*P[u,v]
    assert abs(sum(pi)-1)<2e-14
    assert abs(f.sum()-1)<2e-14
    assert np.max(np.abs(P.sum(axis=1)-1))<2e-14
    assert np.max(np.abs(P.T@pi-pi))<2e-14
    return lam,pi,P,f

lam,pi,P,f=native()
J0=np.zeros((E,N))
J1=np.zeros((E,N))
J0[np.arange(E),u]=np.sqrt(P[u,v])
J1[np.arange(E),v]=np.sqrt(f/pi[v])
assert np.linalg.norm(J0.T@J0-np.eye(N))<1e-12
assert np.linalg.norm(J1.T@J1-np.eye(N))<1e-12
T=J0.T@J1
assert np.linalg.norm(T-T.T)<1e-12
R=J1-J0@T
F=np.eye(N)-T@T
assert np.linalg.norm(R.T@R-F)<1e-12
eigen_F=np.linalg.eigvalsh(F)
assert sum(eigen_F>1e-9)==32
assert E-N==685 and (E-N)-32==653
print("PASS native scene 718 edges / 33 vertices, current Q rank685, future R rank32, dark653")

# Existing ORIGINAL all-history scalar flow Hessian at its native stationary root.
# H[z,z]=(||z/sqrt(f)||²-||out(z)/sqrt(pi)||²)/ln(phi)
#         =||Q z/sqrt(f)||²/ln(phi).
z=np.zeros(E)
for (x,y),sgn in { (0,9):.5,(9,0):.5,(0,20):-.5,(20,0):-.5 }.items():
    idx=np.flatnonzero((u==x)&(v==y))
    assert len(idx)==1
    z[idx[0]]=sgn
assert abs(z.sum())<1e-14
assert np.max(abs(np.bincount(u,weights=z,minlength=N)
                  -np.bincount(v,weights=z,minlength=N)))<1e-14
w=z/np.sqrt(f)
Qw=w-J0@(J0.T@w)
row=np.bincount(u,weights=z,minlength=N)
H_formula=(np.dot(w,w)-sum(row*row/pi))/ell
H_archive=np.dot(Qw,Qw)/ell
assert abs(H_formula-H_archive)<1e-10 and H_archive>0
print("PASS all-path Book flow Hessian = original current-archive squared norm")

# An ANY-edge-price native Poisson innovation g is in current Q archive;
# its squared norm is exactly the negative history Schur curvature.
def response(d):
    c=float(f@d)
    b=np.bincount(u,weights=f*d,minlength=N)/pi-c
    assert abs(pi@b)<2e-13
    # The rank-one correction fixes the zero-pi-mean Poisson gauge.
    L=np.eye(N)-P+np.outer(np.ones(N),pi)
    xi=np.linalg.solve(L,b)
    assert abs(pi@xi)<1e-11
    assert np.linalg.norm((np.eye(N)-P)@xi-b)<1e-11
    m=d-c-xi[u]+xi[v]
    g=np.sqrt(f)*m
    assert np.linalg.norm(J0.T@g)<1e-11
    assert abs(float(z@d)-float(Qw@g))<1e-10
    hist_curvature=-ell*float(g@g)
    return c,xi,m,g,hist_curvature

# TRUE original symmetric K9↔K11 edge Cost source: all718 native edges.
ab=((np.minimum(zone[u],zone[v])==0)&
    (np.maximum(zone[u],zone[v])==1)).astype(float)
c,xi,m,g,curvature=response(ab)
alpha=np.where(zone==2,-.5,.5)
assert np.max(abs(ab-(alpha[u]+alpha[v])))<1e-14
chi=alpha+xi
h=np.sqrt(pi)*chi
assert np.linalg.norm(g-R@h)<3e-12
assert abs(ell*(h@F@h)+curvature)<3e-13
assert abs(c-0.2947622241032769)<3e-12
assert abs(curvature+0.1297284254564436)<3e-12
# Full native Perron action check: -log_phi lambda(t)
def action(t):return -math.log(native(t)[0])/ell
step=.002
hessian_fd=(action(step)-2*action(0)+action(-step))/(step**2)
assert abs(hessian_fd-curvature)<1e-6
print("PASS ORIGINAL symmetric native AB Cost: g = (J1−J0*T)*h EXACT")
print("PASS entire historical Schur = −ln(phi)*hᵀ(I−T²)h =",curvature)
print("PASS native Cost first source =",c,"independent Hessian FD =",hessian_fd)

# Oriented ORIGINAL directed-primitive Cost probe. The physical admissibility
# of reversal-odd Cost variations is unproved; this is a strict operator test.
forward=((zone[u]==0)&(zone[v]==1))|((zone[u]==1)&(zone[v]==2))|((zone[u]==2)&(zone[v]==0))
dcirc=np.where(forward,1.,-1.)
assert np.max(abs(dcirc+np.array([
    dcirc[np.flatnonzero((u==v[k])&(v==u[k]))[0]]
    for k in range(E)])))<1e-14
cc,xi2,m2,g2,curvature2=response(dcirc)
assert abs(cc)<1e-12
assert np.linalg.norm(J1.T@g2)<1e-11
projection32=R@(np.linalg.pinv(R)@g2)
assert np.linalg.norm(projection32)<2e-11
assert abs(curvature2+0.4763744515526456)<4e-12
assert curvature2<0
print("PASS directed cycle: g lies in Q archive but orthogonal to ALL future rank32")
print("PASS 653-dimensional future-dark archive curvature =",curvature2)
print("CONCLUSION: rank32 universal history-source identification FALSE on all directed Costs")
print("SCOPE: actual scalar Book history rate, not full noncommutative D0 action, physical reversal rule, or GR")
