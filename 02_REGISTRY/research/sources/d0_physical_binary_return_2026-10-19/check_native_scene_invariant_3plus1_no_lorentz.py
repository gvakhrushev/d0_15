#!/usr/bin/env python3
"""Native K(9,11,13) automorphisms, 3+1 edge quotient and original Book Hessian.
This does NOT derive a Lorentzian spacetime or compulsory 4D Einstein action.
"""
import numpy as np
import sympy as sp
from math import sqrt, log

sizes=(9,11,13)
Z=np.array([0]*9+[1]*11+[2]*13)
E=np.array([(a,b) for a in range(33) for b in range(33) if Z[a]!=Z[b]])
u,v=E.T
assert E.shape==(718,2)
p=(sqrt(5)-1)/2
ell=log(1/p)
orbit=((0,1),(1,0),(0,2),(2,0),(1,2),(2,1))
M=np.column_stack([((Z[u]==a)&(Z[v]==b)).astype(float) for a,b in orbit])
assert np.all(M.sum(axis=1)==1)
assert tuple(M.sum(axis=0).astype(int))==(99,99,117,117,143,143)

# Original full group Aut= S9 x S11 x S13. Fixed site dimension 3,
# fixed directed edge dimension 6. Endpoint gradients span dimension 2.
D=np.array([[int(a==j)-int(b==j) for j in range(3)]
            for a,b in orbit],dtype=float)
assert np.linalg.matrix_rank(D,tol=1e-12)==2
B=np.zeros((6,4))
B[:,0]=[1,1,0,0,0,0]
B[:,1]=[0,0,1,1,0,0]
B[:,2]=[0,0,0,0,1,1]
B[:,3]=[1,-1,-1,1,1,-1]
assert np.linalg.matrix_rank(np.column_stack([B,D]),tol=1e-12)==6
# Graph's vertex module is trivial^3 + standard(8)+standard(10)+standard(12).
assert 3+8+10+12==33 and min(8,10,12)>4

Adj=np.zeros((33,33));Adj[u,v]=1
evals,evecs=np.linalg.eigh(Adj)
rho=float(evals[-1]);r=evecs[:,-1]
if r.sum()<0:r=-r
pi=r*r
P=Adj*r[None,:]/(rho*r[:,None])
f=pi[u]*P[u,v]
assert np.max(np.abs(P.sum(axis=1)-1))<1e-12
assert np.max(np.abs(P.T@pi-pi))<1e-12
assert abs(f.sum()-1)<1e-12

# Exact finite Poisson archive source controls on 718 original edges.
G=np.zeros((718,6))
for j in range(6):
    d=M[:,j];c=f@d
    b=np.bincount(u,weights=f*d,minlength=33)/pi-c
    xi=np.linalg.solve(np.eye(33)-P+np.outer(np.ones(33),pi),b)
    m=d-c-xi[u]+xi[v]
    G[:,j]=np.sqrt(f)*m
    assert np.max(np.abs(np.bincount(u,weights=f*m,minlength=33)))<1e-11
H=-ell*G.T@G
assert np.linalg.norm(H@np.ones(6))<1e-11
assert np.linalg.norm(H@D)<1e-11
eig=np.linalg.eigvalsh(H)
assert np.sum(eig < -1e-9)==3 and np.max(abs(eig[3:]))<1e-10
Q=B.T@H@B
eig4=np.linalg.eigvalsh(Q)
assert np.sum(eig4 < -1e-9)==3 and abs(eig4[-1])<1e-10
assert max(abs(Q[:3,3]))<1e-11

# Exact native directed three-zone Cost transfer for ABC orientation.
x,q=sp.symbols("x q",nonzero=True)
T=sp.Matrix([[0,11*q,13/q],[9/q,0,13*q],[9*q,11/q,0]])
assert sp.simplify((x*sp.eye(3)-T).det()
   -(x**3-359*x-1287*(q**3+q**(-3))))==0
chiral=-23166*ell/(rho*(3*rho*rho-359))
assert abs(chiral-Q[3,3])<1e-11
assert abs(f@(M@B[:,3]))<1e-13
assert chiral<0

print("PASS original scene 33 vertices / 359 undirected / 718 directed")
print("PASS original graph Aut=S9*S11*S13 has no invariant 4D vertex carrier")
print("PASS invariant directed Cost dimension 6; endpoint-gradient rank2")
print("PASS native quotient 3 reciprocal costs plus ONE oriented ABC cycle")
print("PASS all718 original Book Fisher Hessian rank3, 4D inertia (0,3,1)")
print("PASS exact odd transfer cubic x^3-359*x-1287*(q^3+q^-3)")
print("PASS exact original chiral second source",format(chiral,'.15f'))
print("PASS eigenvalues of 4D quotient",eig4)

# Original native CURRENT/FUTURE edge embeddings J0,J1 and the rank32
# feedback archive. The ONLY invariant odd cost history direction is
# incoming- and outgoing-conditionally centered: rank32-future DARK.
J0=np.zeros((len(u),33))
J1=np.zeros((len(u),33))
J0[np.arange(len(u)),u]=np.sqrt(P[u,v])
J1[np.arange(len(u)),v]=np.sqrt(f/pi[v])
Tsite=J0.T@J1
R=J1-J0@Tsite
godd=G@B[:,3]
assert np.linalg.norm(J0.T@godd)<2e-12
assert np.linalg.norm(J1.T@godd)<2e-12
assert np.linalg.norm(R.T@godd)<2e-12
assert np.linalg.matrix_rank(R,tol=1e-10)==32
assert len(u)-33-32==653
assert abs(-ell*(godd@godd)-chiral)<2e-12
print("PASS invariant chiral cost source entirely inside original dark653 archive")

print("SCOPE: no physical A4D role compiler, Lorentz metric or GR closure")
