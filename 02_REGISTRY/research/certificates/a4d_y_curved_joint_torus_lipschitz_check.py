#!/usr/bin/env python3
"""Exact unit-torus Lipschitz bound for the curved z=1 joint Bloch symbol.

The literal 136-by-96 symbol is compiled into its exact 21-term Laurent
stencil.  For each theta-coordinate, the derivative coefficient envelope is
formed entrywise.  On the unit torus,

  ||d_j Q(theta)||_2 <= sqrt(||E_j||_1 ||E_j||_infinity) = 22/7.

All arithmetic is rational.  This is a global perturbation bound, not by
itself an all-Bloch rank theorem.
"""
from __future__ import annotations
from collections import defaultdict
import json
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
ck("EXACT_NEAREST_DIFFERENCE_SUPPORT_21",len(support)==21 and set(support)==expected)

bounds=[]
ledgers=[]
for j in range(4):
    # Entrywise envelope for |d_j Q| on |lambda_r|=1.
    E=sp.zeros(136,96)
    for d in support:
        if d[j]:
            E += abs(d[j])*T[d].applyfunc(lambda x: abs(sp.Rational(x)))
    colmax=max(sum(E[i,k] for i in range(E.rows)) for k in range(E.cols))
    rowmax=max(sum(E[i,k] for k in range(E.cols)) for i in range(E.rows))
    ck("COLUMN_SUM_BOUND_"+str(j),colmax==sp.Rational(22,7))
    ck("ROW_SUM_BOUND_"+str(j),rowmax==sp.Rational(22,7))
    op=sp.sqrt(colmax*rowmax)
    ck("OPERATOR_BOUND_"+str(j),op==sp.Rational(22,7))
    bounds.append(op)
    ledgers.append({"axis":j,"max_column_sum":str(colmax),
                    "max_row_sum":str(rowmax),"operator_upper_bound":str(op)})

result={
 "schema":"a4d-y-curved-joint-torus-lipschitz-v2",
 "terminal":"A4D-Y-CURVED-JOINT-TORUS-LIPSCHITZ-CERTIFIED",
 "z":"1",
 "operator_shape":[136,96],
 "support":[list(d) for d in support],
 "support_size":len(support),
 "coordinate_bounds":ledgers,
 "global_bound":"||Q(theta)-Q(phi)||_2 <= (22/7) * sum_j |theta_j-phi_j|",
 "metric":"theta coordinates, lambda_j=exp(i theta_j)",
 "proof":"entrywise Laurent derivative envelope plus ||M||_2 <= sqrt(||M||_1 ||M||_infinity)",
 "scope_fence":[
   "global on the physical unit torus",
   "does not prove the all-Bloch zero locus",
   "does not itself give a positive transverse gap",
   "intended as the perturbation constant for local and finite-cover estimates"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-TORUS-LIPSCHITZ-CERTIFIED")
