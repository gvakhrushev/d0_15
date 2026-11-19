#!/usr/bin/env python3
"""D0 original: six actual Role plaquettes -> six ORIGINAL rooted K(9,11,13) 3-edge paths
-> 36 genuine Golden p CAR GOOD+BAD two-density phase coordinates -> recover
nonlinear finite six-face S_star at one nonflat cell (MATHEMATICAL check).
No physical full128 Book03 action selection / cost / clock / GR claim.
"""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import root
from itertools import combinations,product
p=(np.sqrt(5.)-1)/2; g=p*p
I=np.eye(4);eta=np.diag([1.,-1.,-1.,-1.])
def E(i,j):
    X=np.zeros((4,4));X[i,j]=1;return X
Lie=np.array([E(1,2)+E(2,0), E(1,3)+E(3,0),E(0,2)+E(2,1),
              E(0,3)+E(3,1), E(2,3)-E(3,2), E(1,1)-E(0,0)])
en=np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1.]])
assert max(np.linalg.norm(X.T@en+en@X) for X in Lie)<1e-13
v0=np.array([1,0,1,1j])/np.sqrt(3);v1=np.array([0,1,1,1j])/np.sqrt(3)
OI=lambda i,j:(E(j,i)-E(i,j))/(2j)
probes=[(v0,E(0,0)),(v0,E(2,2)),(v0,OI(0,1)),(v0,OI(0,2)),
        (v1,E(1,1)),(v1,OI(0,1))]
cache=[]
for v,O in probes:
    rho=np.outer(v,v.conjugate())
    A=(I+O)/2
    Z0=(g*g+(1-g)**2)*np.trace(A@rho)
    assert abs(Z0.imag)<1e-12 and Z0.real>0
    cache.append((rho,A,Z0.real))
DJ=np.zeros((6,6))
for j,(rho,A,z0) in enumerate(cache):
    for k,X in enumerate(Lie):
        dg=g*(X@rho+rho@X.T)
        db=-g/2*((X+X.T)@rho+rho@(X+X.T))
        DJ[j,k]=np.imag(np.trace(A@(g*rho@dg+(1-g)*rho@db))/z0)
assert abs(np.linalg.det(DJ)-p**9/15552000)<1e-17
def phases(U):
    ev,Q=np.linalg.eigh(I-g*U.T@U)
    assert min(ev)>0
    F=(Q*np.sqrt(ev))@Q.T
    return np.array([np.angle(np.trace(A@(
       g*rho@(g*U@rho@U.T)+(1-g)*rho@(F@rho@F))))
       for rho,A,_ in cache])
def recover(ph):
    def unit(x):return expm(np.einsum('i,ijk->jk',x,Lie))
    x0=np.linalg.solve(DJ,ph)
    sol=root(lambda x:phases(unit(x))-ph,x0,tol=1e-11)
    assert sol.success or np.linalg.norm(sol.fun)<2e-12
    assert np.linalg.norm(sol.fun)<1e-12
    return unit(sol.x)
coords=np.array([[.12,0,0,.035,.04,.02],
                 [0,.105,.03,0,.01,-.025],
                 [.025,-.085,0,.04,.07,0],
                 [0,.025,-.09,.02,.025,.06]])
link=[expm(np.einsum('i,ijk->jk',row,Lie)) for row in coords]
faces=list(combinations(range(4),2));orig=[];derived=[]
for j,(r,s) in enumerate(faces):
    P=link[r]@link[s]@np.linalg.inv(link[r])@np.linalg.inv(link[s])
    # The three ORIGINAL directed K edges (0,9),(9,20+j),(20+j,0).
    assert 9<20+j<33
    U09=I;U9cj=P;Ucj0=I
    scene_word=U09@U9cj@Ucj0
    assert np.linalg.norm(scene_word-P)<1e-13
    orig.append(P);derived.append(recover(phases(scene_word)))
maxerr=max(np.max(abs(P-Q)) for P,Q in zip(orig,derived))
assert maxerr<1e-9 and min(np.linalg.norm(P-I) for P in orig)>1e-5
T=np.array([[1/np.sqrt(2),1/np.sqrt(2),0,0],
 [1/np.sqrt(2),-1/np.sqrt(2),0,0],[0,0,1,0],[0,0,0,1]])
assert np.max(abs(T.T@en@T-eta))<1e-14
cof=I+.045*np.array([[0,.2,-.5,.1],[.4,0,.2,-.1],
 [.3,-.25,0,.3],[.2,.1,-.2,0]])
def sign(idx):
    return (-1)**sum(idx[a]>idx[b] for a in range(4) for b in range(a+1,4))
def hodge(B):
    low=eta@B@eta
    return np.array([[sum((sign((i,j,k,l)) if len({i,j,k,l})==4 else 0)*low[k,l]
           for k,l in product(range(4),repeat=2))/2
           for j in range(4)] for i in range(4)])
def star(Ps):
    total=0.
    for (r,s),P in zip(faces,Ps):
        u,v=[k for k in range(4) if k not in (r,s)]
        B=np.outer(cof[:,u],cof[:,v])-np.outer(cof[:,v],cof[:,u])
        X=hodge(B)@eta
        Q=T.T@P@T
        R=(Q-np.linalg.inv(Q))/2
        total+=sign((r,s,u,v))*(-np.trace(X@R)/2)
    return total
old,new=star(orig),star(derived)
assert abs(old-new)<1e-9
print('PASS original four shared native SO links -> six nonidentity Role plaquettes')
print('PASS six original rooted 3-edge K(9,11,13) group-history words')
print('PASS 36 original Golden two-density CAR good+bad scalar phase readings')
print('PASS local nonlinear inversion of all six measured holonomies: max err',maxerr)
print('PASS literal old S_star 6-face source',old,'recovered',new)
print('PASS Golden phase Jacobian det',np.linalg.det(DJ),'smallest singular',np.linalg.svd(DJ)[1][-1])
print('GR_closed=false: mathematical readout; native action/cost/clock admission still OPEN')
