#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact transverse gap in fixed neighborhoods of all folded Y centers.

At z=1 remove the two cellwise Y directions carried by phase-0 and phase-2
role-0 spatial rotations.  The resulting rational 96x94 injection Bperp is
preserved by folded phase unfolding.

At lambda=(1,1,1,1), exact LDL proves
    (Q Bperp)^T (Q Bperp) - I/100 > 0,
hence sigma_min(Q Bperp)>1/10.  The exact common-phase covariance identifies
all four lambda^4=1 folded points.  Together with the independently pinned
global derivative bound ||d_j Q||_2<=22/7 and ||Bperp||_2=sqrt(3)<7/4,
Weyl gives sigma_min(Q(theta)Bperp)>1/20 throughout each L1 ball of radius
1/110 around a folded point.

This is a local uniform transverse theorem, not a global all-Bloch gap.
"""
from __future__ import annotations
from collections import defaultdict
import json
from pathlib import Path
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_folded_transverse_gap_results.json"
LIP=HERE/"a4d_y_curved_joint_torus_lipschitz_results.json"

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

H,LABELS,FACES0=B.action_connection_hessian(sp.Integer(1))
FACES=C.with_base_phases(FACES0)
_N=C.centers(H,LABELS,sp.Integer(1))
_A1,_A2,_M0,_M1,_M2,C0,_C1,_C2,_D=C.blocks_all(H,FACES,LABELS)
Q0=H.col_join(C0)
ck("FOLDED_Q0_SHAPE",Q0.shape==(136,96))

# Rational complement: remove the Y=(1,-1,1) direction independently on
# phase 0 and phase 2, retaining the two Euclidean-orthogonal-plane generators
# (1,1,0) and (0,1,1) in each three-rotation slot.
cols=[]
for idx,(phase,role,generator) in enumerate(LABELS):
    if role==0 and phase in (0,2) and generator in (3,4,5):
        continue
    e=sp.zeros(96,1); e[idx]=1; cols.append(e)
for phase in (0,2):
    v1=sp.zeros(96,1); v2=sp.zeros(96,1)
    base=(phase*4)*6
    v1[base+3]=1; v1[base+4]=1
    v2[base+4]=1; v2[base+5]=1
    cols.extend((v1,v2))
Bperp=sp.Matrix.hstack(*cols)
ck("TRANSVERSE_COMPLEMENT_SHAPE",Bperp.shape==(96,94) and Bperp.rank()==94)

# Its Gram matrix is identity except for two disjoint [[2,1],[1,2]] blocks,
# so the exact operator norm is sqrt(3).
Gbasis=Bperp.T*Bperp
eigs=Gbasis.eigenvals()
ck("BPERP_GRAM_SPECTRUM",eigs=={sp.Integer(1):92,sp.Integer(3):2})

M=Q0*Bperp
Gram=M.T*M
shifted=Gram-sp.eye(94)/100
L,D=shifted.LDLdecomposition(hermitian=False)
ck("LDL_RECONSTRUCTION",L*D*L.T==shifted)
ck("FOLDED_TRANSVERSE_GAP_GT_ONE_TENTH",
   all(sp.factor(D[i,i])>0 for i in range(94)))

# Compile the Laurent stencil only to certify the folded phase-unfolding law.
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

# Every monomial obeys sum(d)=p_col-p_row mod 4.  This is exactly the
# coefficientwise statement behind folded phase unfolding.
for d,Td in T.items():
    for (row,col),value in Td.todok().items():
        if value:
            ck("PHASE_COVARIANCE_"+str(d)+"_"+str(row)+"_"+str(col),
               (sum(d)-LABELS[col][0]+row_phase(row))%4==0)

for lam in (sp.Integer(1),sp.I,sp.Integer(-1),-sp.I):
    Qlam=sum((lam**sum(d)*Td for d,Td in T.items()),sp.zeros(136,96))
    Dc=sp.diag(*[lam**(-phase) for phase,role,g in LABELS])
    Dr=sp.diag(*(
        [lam**(-phase) for phase,role,g in LABELS]
        +[lam**(-phase) for phase in range(4) for _ in range(10)]
    ))
    ck("FOLDED_PHASE_UNFOLD_"+str(lam),Qlam*Dc==Dr*Q0)

lip=json.loads(LIP.read_text())
ck("PINNED_GLOBAL_DERIVATIVE_BOUND",
   lip["schema"]=="a4d-y-curved-joint-torus-lipschitz-v3"
   and all(x["operator_upper_bound"]=="22/7" for x in lip["coordinate_bounds"]))

# Quantitative Weyl estimate.  ||Bperp||=sqrt(3)<7/4, hence
# ||(Q(theta)-Q(q))Bperp|| < (22/7)*(7/4)*delta = (11/2)*delta.
# For delta<=1/110 this is <1/20.  The folded gap is >1/10.
ck("SQRT3_LT_SEVEN_FOUR",sp.Integer(3)<sp.Rational(49,16))
ck("RADIUS_ARITHMETIC",sp.Rational(11,2)*sp.Rational(1,110)==sp.Rational(1,20))

result={
 "schema":"a4d-y-curved-joint-folded-transverse-gap-v1",
 "terminal":"A4D-Y-CURVED-JOINT-FOLDED-TRANSVERSE-GAP-CERTIFIED",
 "z":"1",
 "domain_complement_dimension":94,
 "removed_subspace":"independent Y rotation directions on phase-0 and phase-2 role-0 links",
 "basis_gram_spectrum":{"1":92,"3":2},
 "folded_base_gap":"sigma_min(Q_folded Bperp) > 1/10",
 "folded_characters":["1","i","-1","-i"],
 "phase_unfolding":"Q(lambda) Dcol(lambda^-p)=Drow(lambda^-p) Q(1) for lambda^4=1",
 "global_derivative_bound":"||d_j Q||_2 <= 22/7",
 "neighborhood":"sum_j |theta_j-theta_j_folded| <= 1/110",
 "uniform_transverse_gap":"sigma_min(Q(theta) Bperp) > 1/20",
 "proof":"exact LDL at one folded point + exact folded covariance + Weyl perturbation bound",
 "scope_fence":[
   "covers four fixed L1 neighborhoods of folded characters",
   "does not classify the complement of those neighborhoods",
   "does not eliminate the Y center amplitude itself",
   "does not by itself prove nonlinear continuation or task-level response convergence"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-FOLDED-TRANSVERSE-GAP-CERTIFIED")
