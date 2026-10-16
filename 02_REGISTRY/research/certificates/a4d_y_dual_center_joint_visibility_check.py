#!/usr/bin/env python3
"""Exact joint visibility of the second z=1 Y-connection center.

The boost-dual direction integrates to an exact connection-stationary path, but
its metric response is staggered between the four fast phases. Hence it is not
a smooth-source joint modulus near d=0.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
import a4d_y_slow_exact_plane_check as E

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"02_REGISTRY/research/certificates/a4d_y_dual_center_joint_visibility_results.json"
I=sp.eye(4); ETA=E.ETA
SYM=[(a,b) for a in range(4) for b in range(a,4)]

def check(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n)

d=sp.symbols("d", real=True)
Y=E.GEN[3]-E.GEN[4]+E.GEN[5]
B=E.GEN[0]+E.GEN[1]+E.GEN[2]
U=E.cayley_simple(Y,3,sp.Integer(1))
Cm=E.cayley_simple(B,-3,-d)
Cp=E.cayley_simple(B,-3,d)
wave=[U*Cm,I,E.linv(U)*Cp,I]
link=lambda x,r: wave[sum(x)%4] if r==0 else I
solder=lambda x:I

edge_rows=[]
metric=[]
for p in range(4):
    site=(0,p,0,0)
    rows=[E.edge_euler(solder,link,site,role,g) for role in range(4) for g in E.GEN]
    edge_rows.append(rows)
    R=E.solder_euler(solder,link,site)
    vals=[]
    for a,b in SYM:
        q=sp.zeros(4);q[a,b]=q[b,a]=1
        dS=ETA*q/2
        vals.append(sp.factor(sum(R[i,j]*dS[i,j] for i in range(4) for j in range(4))))
    metric.append(vals)

check("ALL_96_CONNECTION_ROWS_ZERO",all(v==0 for rows in edge_rows for v in rows))
f=4*d/(3*d*d-4)
v=[0,0,0,0,-f,f,f,-f,f,-f]
check("PHASE01_METRIC_RESPONSE",metric[0]==v and metric[1]==v)
check("PHASE23_METRIC_RESPONSE",metric[2]==[-x for x in v] and metric[3]==[-x for x in v])
check("FOUR_PHASE_AVERAGE_ZERO",all(sum(metric[p][i] for p in range(4))==0 for i in range(10)))
# Near d=0, denominator is nonzero and phase erasure forces numerator d=0.
phase_gap=[sp.factor(metric[2][i]-metric[0][i]) for i in range(10)]
check("SMOOTH_SOURCE_ERASURE_FORCES_D_ZERO",
      any(g!=0 for g in phase_gap) and
      sp.gcd(sp.Poly(sp.together(phase_gap[4]*(3*d*d-4)),d),sp.Poly(d,d)).degree()==1)

result={
 "schema":"a4d-y-dual-center-joint-visibility-v1",
 "base":"z=1 exact Y vacuum; standard solder",
 "dual_path":"phase0 U*Cayley(B,-d), phase2 U^-1*Cayley(B,+d), B=K1+K2+K3",
 "connection_euler":"all 96 rows vanish identically",
 "metric_coordinate_order":[f"q{a}{b}" for a,b in SYM],
 "phase01_response":["0","0","0","0","-f","f","f","-f","f","-f"],
 "phase23_response":["0","0","0","0","f","-f","-f","f","-f","f"],
 "f":"4*d/(3*d^2-4)",
 "four_phase_average":"zero",
 "smooth_source_conclusion":"for |d| small, phase erasure forces d=0",
 "terminal":"A4D-Y-DUAL-CENTER-CONNECTION-MODULUS-BUT-SMOOTH-SOURCE-VISIBLE"
}
if OUT.exists():
    check("RESULTS_MATCH_PINNED_JSON",result==json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
print("TERMINAL",result["terminal"])
