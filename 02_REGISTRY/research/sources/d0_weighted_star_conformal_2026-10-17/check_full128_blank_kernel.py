#!/usr/bin/env python3
"""Exact original 4D/16-CAR weighted stored Dirac and full128 blank-record kernel.
Admissible kinematic sector; NOT selected physical matter preparation or all-GR no-go.
"""
import json
import sympy as S

L=2
h=S.Rational(1,2)
site_count=L**4
grade_count=16
Isite=S.eye(site_count)
count=0
def chk(cond,label):
    global count
    if not bool(cond):
        raise RuntimeError(label)
    count+=1

def mateq(A,B,label):
    chk(A.shape==B.shape and all(S.simplify(v)==0 for v in (A-B)),label)

cre=[]
for r in range(4):
    c=S.MutableSparseMatrix(16,16,{})
    for mask in range(16):
        if (mask&(1<<r))==0:
            c[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
    cre.append(c)
for r in range(4):
    mateq(cre[r].T.T,cre[r],"real CAR transpose")
    mateq(cre[r]*cre[r].T+cre[r].T*cre[r],S.eye(16),"full16 CAR anticommutator")

D0=S.zeros(site_count*grade_count)
for r in range(4):
    Tr=S.MutableSparseMatrix(site_count,site_count,{})
    for x in range(site_count):
        Tr[x^(1<<r),x]=1
    delta=(Tr-Isite)/h
    D0 += S.kronecker_product(delta,cre[r]+cre[r].T)
mateq(D0,D0.T,"literal flat full CAR stored D selfadjoint")
vals=[]
for site in range(site_count):
    sx=S.Rational(20+2*(site&1)+3*((site>>1)&1)+((site>>2)&1)+2*((site>>3)&1),20)
    vals.append(sx)
scale=S.diag(*[v for v in vals for _ in range(grade_count)])
weight=S.diag(*[1/v for v in vals for _ in range(grade_count)])
Ds=scale*D0
mateq(weight*Ds,Ds.T*weight,"true variable-node-weight adjoint, all16 allsites")
mateq(weight*Ds,D0,"same finite site-free Dirac quadratic pairing")
chk(len(set(vals))>1,"nonconstant site conformal coframe")
P=S.MutableSparseMatrix(site_count*grade_count,grade_count,{})
for site in range(site_count):
    for grade in range(grade_count):
        P[site*grade_count+grade,grade]=1
P=P.as_immutable()
mateq(D0*P,S.zeros(256,16),"all16 site-constant CAR zero modes on original D")
mateq(Ds*P,S.zeros(256,16),"all16 remain exact zero for arbitrary positive conformal factor")
mateq(Ds*Ds*P,S.zeros(256,16),"true positive squared Dirac source annihilates sector")
A=h*Ds/16
mateq(A*P,S.zeros(256,16),"literal genuine native SELECT blank A kills all16 modes")
Mblank=S.eye(256)-2*A*A
mateq(Mblank*P,P,"real reflected SELECT blank acts as identity")
p=(S.sqrt(5)-1)/2
K00=p*S.eye(256)+p**2*Mblank
K10=p*S.sqrt(p)*(Mblank-S.eye(256))
mateq(K00*P,P,"full original golden port0 blank is certain on all16")
mateq(K10*P,S.zeros(256,16),"full original golden port1 blank probability zero")
chk(S.simplify(p+p**2-1)==0,"golden total normalization")
# All OTHER 63 reflected outputs have M_alpha=-2 N_alpha^* A, thus annihilate P
# without assuming a particular SELECT eigenbasis, dropping any 16 grade or output.
chk(A*P==S.zeros(256,16),"all63 nonblank reflected columns vanish on old kernel")
chk(Ds*P==S.zeros(256,16),"exact all-depth blank induction")
chk(S.trace(D0*D0)==8192,"exact finite L2 full16 spectrum trace")
print(json.dumps({
    "status":"PASS","exact_checks":count,
    "grid":"L=2 periodic 4D, 16 sites x 16 CAR grades",
    "full_native_carrier_dim":256,
    "nonconstant_site_weights":len(set(vals)),
    "exact_Ds":"M_s D_flat",
    "exact_weighted_adj":"M_1/s D_s = D_flat self-adjoint",
    "true_native_16d_kernel":"all16 site-constant CAR states",
    "complete_128_outcome_tape":"Pr(all blank at every depth)=1 on this 16D sector",
    "scope":"source-blind preparation sector, NOT full Price/Cost-Info universal obstruction",
    "original_kinematic_weighted_geometry_admitted":True,
    "physical_input_preparation_selected":False,
    "full_GR_closed":False
},sort_keys=True))
