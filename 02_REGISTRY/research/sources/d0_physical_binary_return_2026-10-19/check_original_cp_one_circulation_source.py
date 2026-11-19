#!/usr/bin/env python3
"""Same ORIGINAL 718 scalar Book Cost Hessian: CP x arbitrary field = ONE orbit-average circulation.
Research only. No physical J23->Cost/Info map or full128 GR source selected.
"""
import random
import mpmath as mp

mp.mp.dps=55
q=mp.mpf
phi=(1+mp.sqrt(5))/2
ell=mp.log(phi)
n=[9,11,13]
labels=[i for i,size in enumerate(n) for _ in range(size)]
edges=[(u,v) for u in range(33) for v in range(33) if labels[u]!=labels[v]]
assert len(edges)==718
CP={(0,1):1,(1,2):1,(2,0):1,(1,0):-1,(2,1):-1,(0,2):-1}
M=mp.matrix([[n[j] if i!=j else 0 for j in range(3)] for i in range(3)])
ev,V=mp.eig(M)
rho=mp.findroot(lambda t:t**3-359*t-2574,q("21.8"))
ix=min(range(3),key=lambda i:abs(ev[i]-rho))
r=[mp.re(V[i,ix]) for i in range(3)]
if sum(r)<0:r=[-a for a in r]
r=[a/mp.sqrt(sum(n[i]*r[i]**2 for i in range(3))) for a in r]
mass={(0,1):q(n[0]*n[1])*r[0]*r[1]/rho,
      (1,2):q(n[1]*n[2])*r[1]*r[2]/rho,
      (0,2):q(n[0]*n[2])*r[0]*r[2]/rho}
j=q(3)/sum(1/a for a in mass.values())
mu={}
score={}
for u,v in edges:
    a,b=labels[u],labels[v]
    mu[u,v]=r[a]*r[b]/rho
    score[u,v]=q(CP[a,b])*j/mass[tuple(sorted((a,b)))]

def average_cost(dcost,i,k):
    vals=[dcost[u,v] for u,v in edges if (labels[u],labels[v])==(i,k)]
    return sum(vals)/len(vals)

def gamma(dcost):
    return ((average_cost(dcost,0,1)-average_cost(dcost,1,0))
          +(average_cost(dcost,1,2)-average_cost(dcost,2,1))
          +(average_cost(dcost,2,0)-average_cost(dcost,0,2)))

def full_mixed(dcost):
    # Affine in BOTH epsilon and original physical Cost coordinate:
    return -ell*sum(mu[u,v]*score[u,v]*dcost[u,v] for u,v in edges)

random.seed(20261019)
cases={
 "CP":{(u,v):q(CP[labels[u],labels[v]]) for u,v in edges},
 "symmetric_AB":{(u,v):q(int({labels[u],labels[v]}=={0,1})) for u,v in edges},
 "vertex_gradient":{(u,v):q(labels[u]-labels[v]) for u,v in edges},
 "arbitrary718":{(u,v):q(random.randrange(-17,18))/q(19) for u,v in edges}
}
info=[q(random.randrange(-9,10))/q(11) for _ in range(33)]
theta=q(2)/5
cases["arbitrary_vertex_Info"]={(u,v):-theta*info[u]-(1-theta)*info[v] for u,v in edges}
for name,dcost in cases.items():
    lhs=full_mixed(dcost)
    rhs=-ell*j*gamma(dcost)
    assert abs(lhs-rhs)<q("1e-43"),name
    if name in ("symmetric_AB","vertex_gradient","arbitrary_vertex_Info"):
        assert abs(lhs)<q("1e-43"),name
    print("PASS",name," full718 native Hessian=",mp.nstr(lhs,24),
          " one-circulation RHS=",mp.nstr(rhs,24))
variance=q(23166)/(rho*(3*rho*rho-359))
assert abs(gamma(cases["CP"])-6)<q("1e-50")
assert abs(full_mixed(cases["CP"])+ell*variance)<q("1e-45")
print("PASS EXACT ORIGINAL 718-TO-ONE CP FIELD-SOURCE SELECTOR")
print("native j=",mp.nstr(j,24)," ln(phi)*j=",mp.nstr(ell*j,24))
print("FIREWALL: nonaffine mixed Cost second jets remain; physical full128 J23 field-to-edge mapping and GR open")
