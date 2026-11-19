#!/usr/bin/env python3
"""Original K(9,11,13) Book scalar history archive: signed/signless Hodge.
Research/geometry consumer of exact #384 Book/Poisson owner; no physical
Cost-to-4D field selection or original full Book03 GR claim.
"""
import numpy as np
import sympy as s

part=np.array([0]*9+[1]*11+[2]*13,dtype=int)
counts=np.array([9,11,13])
N=len(part)
adj=(part[:,None]!=part[None,:]).astype(float)
E=int(adj.sum());und=int(E/2)
assert (N,E,und)==(33,718,359)
# Exact signed-incidence and unsigned-incidence ranks:
# oriented cycle space 359-32=327, signless edge stress 359-33=326.
edgelist=[(i,j) for i in range(N) for j in range(i+1,N) if adj[i,j]]
inc_minus=s.zeros(N,und);inc_plus=s.zeros(N,und)
for k,(i,j) in enumerate(edgelist):
    inc_minus[i,k]=1;inc_minus[j,k]=-1
    inc_plus[i,k]=inc_plus[j,k]=1
assert inc_minus.rank()==32
assert inc_plus.rank()==33
# The double-covered SOURCE/TARGET bipartite incidence has connected
# 66-node support because the ORIGINAL 33-vertex graph has triangles.
# Its rank is 66-1=65; dark double-centered flows E-65=653.
assert E-(2*N-1)==653
assert und-32==327 and und-33==326 and 327+326==653

x,t=s.symbols("x t",real=True)
et=s.exp(t)
M=s.Matrix([[0,11/et,13*et],
            [9*et,0,13/et],
            [9/et,11*et,0]])
pol=s.expand((x*s.eye(3)-M).det())
assert s.simplify(pol-(x**3-359*x-1287*(et**3+et**(-3))))==0
print("PASS: exact original three-zone chiral Perron cubic ρ³-359ρ-2574 cosh(3t)")

rho=float(np.linalg.eigvalsh(adj)[-1])
r=np.array([1/(rho+counts[z]) for z in part],dtype=float)
r/=np.linalg.norm(r)
pi=r**2
P=adj*(r[None,:]/(rho*r[:,None]))
mu=pi[:,None]*P
eye=np.eye(N)
assert np.max(np.abs(P.sum(axis=1)-1))<2e-13
assert np.max(np.abs(pi@P-pi))<2e-13
assert np.max(np.abs(mu-mu.T))<2e-13
assert np.max(np.abs((P+eye)@np.linalg.inv(P+eye)-eye))<5e-12

def projections(d):
    odd=(d-d.T)/2
    even=(d+d.T)/2
    mo=(P*odd).sum(axis=1)
    me=(P*even).sum(axis=1)
    # Exact reversal-odd Poisson from the real native Perron Markov chain.
    # pi.mo=0 because mu is symmetric and odd is antisymmetric.
    assert abs(pi@mo)<1e-13
    psi=np.linalg.solve(eye-P+np.outer(np.ones(N),pi),mo)
    # Original scene has triangles: -1 is not a P eigenvalue.
    # Thus the SIGNLESS Poisson equation has a UNIQUE solution.
    phi=np.linalg.solve(eye+P,me)
    co=odd+psi[None,:]-psi[:,None]
    ce=even-phi[:,None]-phi[None,:]
    assert np.max(np.abs((P*co).sum(axis=1)))<2e-12
    assert np.max(np.abs((P*ce).sum(axis=1)))<2e-12
    assert np.max(np.abs(co+co.T))<2e-12
    assert np.max(np.abs(ce-ce.T))<2e-12
    return float((mu*co**2).sum()),float((mu*ce**2).sum()),co,ce

# Original genuine directed Cost perturbation; NOT preselected 4D fields.
sign=np.array([[0,1,-1],[-1,0,1],[1,-1,0]])
d=sign[part[:,None],part[None,:]].astype(float)
vodd,veven,co,ce=projections(d)
assert veven<1e-27
ell=np.log((1+np.sqrt(5))/2)
analytic=23166/(rho*(3*rho*rho-359))
assert abs(vodd-analytic)<1e-12
assert abs(-ell*vodd-(-0.4763744515526456))<1e-11
# Cost odd projection lies in DARK653, not the owned rank32 future:
G=np.sqrt(mu)*co
J0score=np.sum(np.sqrt(P)*G,axis=1)
J1score=np.sum(np.sqrt(mu)*G,axis=0)/np.sqrt(pi)
assert np.max(np.abs(J0score))<2e-12
assert np.max(np.abs(J1score))<2e-12

# Unique zone-symmetric oriented circulation, a TRUE balanced history tangent:
# each original zone-to-zone flow is +/-1, spread over its primitive edges.
z=np.zeros((N,N))
for i in range(N):
    for j in range(N):
        if adj[i,j]:
            z[i,j]=d[i,j]/(counts[part[i]]*counts[part[j]])
assert np.max(np.abs(z.sum(axis=0)))<2e-14
assert np.max(np.abs(z.sum(axis=1)))<2e-14
pair=float((z*d).sum())
fisher_z=float(((z[adj.astype(bool)]**2)/mu[adj.astype(bool)]).sum())
assert abs(pair-6)<2e-13
# All original-zone-permutation-equivariant odd archive innovations form
# ONE dimension; hence this Hodge test SATURATES Cauchy-Schwarz.
assert abs(vodd-pair*pair/fisher_z)<1e-12

# A second actual original source: reversal-symmetric SINGLE edge pair.
local=np.zeros((N,N));local[0,9]=local[9,0]=1
oo,ee,_,_=projections(local)
assert oo<1e-26
assert abs(ell*ee-0.0013000035359633177)<1e-11

# Both exact gauge classes give zero full dark source.
potential=np.arange(N,dtype=float)**2/(N**2)
gradient=potential[:,None]-potential[None,:]
source_sum=(potential[:,None]+potential[None,:])*adj
o0,e0,_,_=projections(gradient*adj)
o1,e1,_,_=projections(source_sum)
assert max(o0,e0,o1,e1)<1e-24

print("PASS: exact graph ranks: full archive 685, future32, dark653=odd327+even326")
print("PASS: signed (I-P) and signless (I+P) native Poisson inverses on full33/718")
print("PASS: universal reversible parity, graph-coboundary and endpoint-sum negative controls")
print(f"PASS: native chiral Schur=-ln(phi)||G_odd||²={-ell*vodd:.15f}")
print(f"PASS: cycle-flow Cauchy saturation {pair**2/fisher_z:.15f}; exact cubic analytic {analytic:.15f}")
print(f"PASS: original local symmetric pair hidden source {-ell*ee:.15f}")
print("FIREWALL: original scalar Book macro-action ONLY; compulsory full H+J+R, native 4D mapping, GR CLOSED=false")
