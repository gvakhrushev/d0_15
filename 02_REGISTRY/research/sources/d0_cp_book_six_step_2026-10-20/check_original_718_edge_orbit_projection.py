#!/usr/bin/env python3
"""Original full 718-edge CP^2 Book source: symmetry collapse to ONE orbit functional.
Independent actual 33x33 (not just the three-zone reduced family) negative controls.
Research-only scalar Book source; no physical native full128/GR identification.
"""
import math
import numpy as np

n=(9,11,13)
z=np.repeat(np.arange(3),n)
ell=math.log((1+math.sqrt(5))/2)
edges=np.array([(u,v) for u in range(33) for v in range(33) if z[u]!=z[v]])
assert len(edges)==718
support=np.zeros((33,33));direction=np.zeros((33,33))
cycle={(0,1),(1,2),(2,0)}
for u,v in edges:
    support[u,v]=1
    direction[u,v]=1 if (z[u],z[v]) in cycle else -1
Gamma=np.array([.023608097393000222,-.026654303508226057,.003046206115225835])
pairs=((0,1),(1,2),(2,0))
def prediction(d):
    mean=[]
    for a,b in pairs:
        terms=[(d[u,v]+d[v,u])/2 for u in range(33) for v in range(u+1,33)
               if {z[u],z[v]}=={a,b}]
        assert len(terms)==n[a]*n[b]
        mean.append(sum(terms)/len(terms))
    return float(Gamma@np.array(mean))
def pressure(t,epsilon,d):
    K=support*np.exp(-ell*(1+t*d+epsilon*direction))
    eig=np.linalg.eigvals(K)
    return -math.log(max(eig.real))/ell
def mixed(d,h_t=.03,h_e=.05):
    def d2e(t):
        return (pressure(t,h_e,d)-2*pressure(t,0,d)+pressure(t,-h_e,d))/(h_e*h_e)
    return (d2e(h_t)-d2e(-h_t))/(2*h_t)
def symmetric_edge(u,v):
    mat=np.zeros((33,33))
    mat[u,v]=mat[v,u]=1.
    return mat
allAB=np.zeros((33,33))
for u,v in edges:
    if {z[u],z[v]}=={0,1}:allAB[u,v]=1
antisym=np.zeros((33,33));antisym[0,9]=1;antisym[9,0]=-1
tests=[
 ('AB all',allAB,.0001),
 ('AB single',symmetric_edge(0,9),5e-6),
 ('AB two-edge cancellation',symmetric_edge(0,9)-symmetric_edge(1,10),5e-6),
 ('BC single',symmetric_edge(9,20),5e-6),
 ('orientation-odd AB single',antisym,5e-6),
 ('uniform original Cost',support.copy(),5e-6)]
for name,d,tol in tests:
    target=prediction(d)
    measured=mixed(d)
    print(name,'exact source',target,'full33 finite difference',measured)
    assert abs(target-measured)<tol
assert abs(prediction(symmetric_edge(0,9))-Gamma[0]/99)<1e-15
assert abs(prediction(symmetric_edge(9,20))-Gamma[1]/143)<1e-15
assert all(abs(prediction(d))<1e-14 for _,d,_ in tests[-2:])
print('PASS ORIGINAL718 CP^2 Book orbit projector: 718 directed prices -> one scalar')
print('GR_closed=false; physical full128-to-Cost map still absent')
