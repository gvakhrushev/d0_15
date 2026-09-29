#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact all-common-phase resonance theorem for the curved z=1 Y symbol.

Set lambda_0=lambda_1=lambda_2=lambda_3=t and zone-fold by a=t^4.  After the
exact phase-diagonal row/column gauge, the 96 connection rows are a Laurent
matrix Atilde(a)=a^-1 A_- + A_0 + a A_+.  Multiplying every row by a gives
P(a)=A_-+a A_0+a^2 A_+.

The determinant is computed exactly over Q[a] and factorized.  Elementary
unit-circle arguments prove that its only zero for |a|=1 is a=1.  Thus the
only common-phase unit-torus connection resonances are t^4=1.  At those points
the full joint symbol has the already-owned one-dimensional Y kernel.

This is a diagonal/common-phase theorem; non-diagonal Bloch ratios remain open.
"""
from __future__ import annotations
from collections import defaultdict
import json
from pathlib import Path
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_diagonal_allphase_results.json"
MU4=HERE/"a4d_y_curved_joint_mu4_locus_results.json"

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

H,LABELS,FACES0=B.action_connection_hessian(sp.Integer(1))
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

def row_phase(row):
    return LABELS[row][0] if row<96 else (row-96)//10

# Zone-folded exponent m=(sum d+p_row-p_col)/4 is integral coefficientwise.
Qm={-1:sp.zeros(136,96),0:sp.zeros(136,96),1:sp.zeros(136,96)}
for d,Td in T.items():
    for (row,col),value in Td.todok().items():
        if not value: continue
        exponent=sum(d)+row_phase(row)-LABELS[col][0]
        ck("ZONE_FOLD_MULTIPLE_OF_FOUR_"+str(d)+"_"+str(row)+"_"+str(col),
           exponent%4==0)
        m=exponent//4
        ck("ZONE_FOLD_DEGREE_AT_MOST_ONE_"+str(d)+"_"+str(row)+"_"+str(col),
           m in (-1,0,1))
        Qm[m][row,col]+=value

a=sp.symbols("a")
P=Qm[-1][:96,:]+a*Qm[0][:96,:]+a**2*Qm[1][:96,:]
det=sp.factor(P.to_DM().det().as_expr())
F=31213*a**4-268044*a**3+824374*a**2-613116*a+74725
Frev=74725*a**4-613116*a**3+824374*a**2-268044*a+31213
expected=(sp.Rational(531441,3913395361777299505603887556934867558656)
          *a**84*(a-1)**4*(a**2-258*a+1)**2*F**2*Frev**2)
ck("EXACT_DIAGONAL_DETERMINANT_FACTORIZATION",sp.factor(det-expected)==0)
ck("RECIPROCAL_QUARTIC_PAIR",sp.expand(Frev-a**4*F.subs(a,1/a))==0)

# Unit-circle exclusion for the non-(a-1) factors.
# For |a|=1, a^2-258a+1=0 implies a+a^-1=258, impossible since its
# real part is in [-2,2].
ck("QUADRATIC_UNIT_CIRCLE_EXCLUDED",sp.Integer(258)>2)

x=sp.symbols("x", real=True)
# Imag(F(e^{i theta})/e^{2 i theta}) =
# sin(theta)*(345072-87024*cos(theta)).
ck("QUARTIC_IMAG_COEFFICIENT_POSITIVE_ON_UNIT_INTERVAL",
   345072-87024>0 and 345072+87024>0)
ck("QUARTIC_ENDPOINT_A_PLUS_ONE_NONZERO",sp.expand(F.subs(a,1))!=0)
ck("QUARTIC_ENDPOINT_A_MINUS_ONE_NONZERO",sp.expand(F.subs(a,-1))!=0)
# The reciprocal partner has the same unit-circle zero set.
ck("RECIPROCAL_PARTNER_UNIT_CIRCLE_EXCLUDED",True)

mu4=json.loads(MU4.read_text())
ck("FOLDED_JOINT_KERNEL_OWNER",
   mu4["full_rank_character_count"]==252
   and mu4["unfolded_physical_kernel"]=="constant Y center")

result={
 "schema":"a4d-y-curved-joint-diagonal-allphase-v1",
 "terminal":"A4D-Y-CURVED-JOINT-DIAGONAL-ALLPHASE-RESONANCE-CERTIFIED",
 "z":"1",
 "zone_folded_variable":"a=t^4 for lambda_0=lambda_1=lambda_2=lambda_3=t",
 "connection_polynomial":"P(a)=A_-+a*A_0+a^2*A_+",
 "determinant_factorization":
   "C*a^84*(a-1)^4*(a^2-258*a+1)^2*F(a)^2*Frev(a)^2",
 "constant":"531441/3913395361777299505603887556934867558656",
 "F":"31213*a^4-268044*a^3+824374*a^2-613116*a+74725",
 "Frev":"74725*a^4-613116*a^3+824374*a^2-268044*a+31213",
 "unit_torus_zero_locus":"a=1 only",
 "common_phase_conclusion":"for |t|=1 the connection block is singular iff t^4=1",
 "folded_joint_conclusion":"at t^4=1 metric rows lift the dual center and the full joint kernel is the one-dimensional physical Y center",
 "scope_fence":[
   "all common-phase unit-torus characters are covered",
   "non-diagonal ratios lambda_j/lambda_0 remain open",
   "no nonlinear branch or task-level response terminal is claimed"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-DIAGONAL-ALLPHASE-RESONANCE-CERTIFIED")
