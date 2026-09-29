#!/usr/bin/env python3
"""Exact structural data for a rigorous torus cover of curved joint Bloch Q.

This owner does not claim the cover is complete.  It certifies the finite
Laurent support and computes rational upper bounds for coordinate derivative
Frobenius norms on (S^1)^4.  These bounds are the perturbation constants used
by the subsequent rational-center cover certificate.
"""
from __future__ import annotations
from collections import defaultdict
import json, math
from pathlib import Path
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_torus_lipschitz_results.json"

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

_H,LABELS,FACES0=B.action_connection_hessian(sp.Integer(1))
FACES=C.with_base_phases(FACES0)
IDX={x:i for i,x in enumerate(LABELS)}
UNIT=[B.I4[:,j] for j in range(4)]
T=defaultdict(lambda:sp.zeros(136,96))

for phase,a,b,locs,local,Hloc,factors in FACES:
    shifts=[(0,0,0,0),tuple(int(r==a) for r in range(4)),
            tuple(int(r==b) for r in range(4)),(0,0,0,0)]
    slot=[]
    for s in shifts: slot += [s]*6
    for ii,(_pi,_gi,gi) in enumerate(local):
        for jj,(_pj,_gj,gj) in enumerate(local):
            d=tuple(slot[jj][r]-slot[ii][r] for r in range(4))
            T[d][gi,gj]+=Hloc[ii,jj]
    u,v=[j for j in range(4) if j not in (a,b)]
    darea=[]
    for qa,qb in B.SYM:
        dS=B.metric_lift(qa,qb)
        darea.append(B.wedge(dS[:,u],UNIT[v])+B.wedge(UNIT[u],dS[:,v]))
    for pos,(q,role,inverse) in enumerate(locs):
        for g,X in enumerate(B.GEN):
            dFfactor=-X*factors[pos] if inverse else factors[pos]*X
            dP=B.I4
            for n,F in enumerate(factors):
                dP=dP*(dFfactor if n==pos else F)
            dF=(dP-B.linv(dP))/2
            dFb=B.biv(dF)
            gi=IDX[(q,role,g)]
            for mi,area in enumerate(darea):
                val=sp.cancel(B.orientation(a,b)*(area.T*B.G2*B.STAR*dFb)[0])
                T[shifts[pos]][96+10*phase+mi,gi]+=val

support=sorted(d for d,M in T.items() if M!=sp.zeros(136,96))
expected={(0,0,0,0)}
for r in range(4):
    e=[0]*4;e[r]=1;expected.add(tuple(e));e[r]=-1;expected.add(tuple(e))
for r in range(4):
    for s in range(4):
        if r!=s:
            d=[0]*4;d[r]=1;d[s]=-1;expected.add(tuple(d))
ck("NEAREST_DIFFERENCE_SUPPORT",set(support)<=expected)

# ||dQ/dtheta_j||_F <= sum_d |d_j| ||T_d||_F.
# Store exact squared coefficient norms and a conservative rational ceiling.
bounds=[]
terms={}
for d in support:
    n2=sp.factor(sum(x*x for x in T[d]))
    ck("STENCIL_NORM2_RATIONAL_"+str(d),n2.is_Rational)
    terms[str(d)]=str(n2)
for j in range(4):
    # ceil each sqrt(n2) to 1/1000, keeping a fully rational upper bound.
    b=sp.Rational(0)
    for d in support:
        if d[j]:
            n2=sp.Rational(terms[str(d)])
            q=sp.Rational(math.isqrt(int(n2.p*10**6//n2.q))+2,1000)
            while q*q<n2: q+=sp.Rational(1,1000)
            b+=abs(d[j])*q
    bounds.append(b)
    ck("DERIVATIVE_BOUND_POSITIVE_"+str(j),b>0)

result={
 "schema":"a4d-y-curved-joint-torus-lipschitz-v1",
 "support":[list(d) for d in support],
 "stencil_frobenius_norm2":terms,
 "coordinate_derivative_frobenius_upper_bounds":[str(x) for x in bounds],
 "metric":"theta coordinates, lambda_j=exp(i theta_j)",
 "use":"||Q(theta)-Q(phi)||_2 <= sum_j L_j |theta_j-phi_j|",
 "scope":"global exact-rational upper bounds; no torus-cover completeness claim"
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("SUPPORT_SIZE",len(support))
print("L_BOUNDS",*[str(x) for x in bounds])
print("TERMINAL A4D-Y-CURVED-JOINT-TORUS-LIPSCHITZ-CERTIFIED")
