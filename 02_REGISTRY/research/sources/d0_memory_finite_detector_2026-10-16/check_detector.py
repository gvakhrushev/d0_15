#!/usr/bin/env python3
"""Reproducible exact CAR logical detector and infinite-orbit SOS.
The declared full16 fixture is finite; physical detector admission is OPEN.
"""
from itertools import product
import json
import sympy as S

p=(S.sqrt(5)-1)/2
X=S.Matrix([[0,1],[1,0]])
Z=S.diag(1,-1)
Y=S.Matrix([[0,-S.I],[S.I,0]])
I=S.eye(2)
K=S.kronecker_product
checks=[]

def eq(name,a,b=0):
    if isinstance(a,S.MatrixBase) or isinstance(b,S.MatrixBase):
        good=all(S.simplify(v)==0 for v in S.Matrix(a)-S.Matrix(b))
    else:
        good=S.simplify(a-b)==0
    if not good:raise ArithmeticError(name)
    checks.append(name)

def demand(name,v):
    if not v:raise ArithmeticError(name)
    checks.append(name)

def context():
    contexts=[(K(Z,I),K(I,Z)),(K(X,I),K(I,X)),(K(X,Z),K(Z,X))]
    projectors=[];paulis=[]
    for j,(a,b) in enumerate(contexts):
        eq("commuting_%d"%j,a*b,b*a)
        block=[]
        for s,t in product((-1,1),repeat=2):
            E=(S.eye(4)+s*a)*(S.eye(4)+t*b)/4
            eq("idempotent_%d_%s_%s"%(j,s,t),E*E,E)
            eq("rank_one_%d_%s_%s"%(j,s,t),S.trace(E),1)
            block.append(E)
            projectors.append(E)
        eq("resolution_%d"%j,sum(block,S.zeros(4)),S.eye(4))
        paulis.extend((a,b,a*b))
    eq("YY_is_real_third_joint",paulis[8],K(Y,Y))
    eq("all_nine_Pauli_orthogonal",S.Matrix(9,9,
          lambda i,j:S.trace(paulis[i]*paulis[j])),4*S.eye(9))
    rho0=S.Matrix([[1,2,0,1],[0,1,1,2],[2,0,1,1],[1,0,0,1]])
    rho=rho0*rho0.T/S.trace(rho0*rho0.T)
    recovered=(S.eye(4)+sum((S.trace(rho*P)*P for P in paulis),S.zeros(4)))/4
    eq("real_logical_density_recovered",rho,recovered)
    rho_im=(S.eye(4)+K(Y,I)/3)/4
    demand("complex_counterexample_different",rho_im!=S.eye(4)/4)
    for i,E in enumerate(projectors):
        eq("complex_imaginary_sector_unseen_%02d"%i,
           S.trace(rho_im*E),S.trace(E)/4)
    demand("four_full16_PVM_not_complete",4*(16-1)<16*17//2-1)
    eq("minimum_full16_real_PVM_count",(135+14)//15,9)
    return projectors

def fock_code():
    create=[]
    for i in range(4):
        A=S.zeros(16)
        for mask in range(16):
            if not mask & (1<<i):
                A[mask|(1<<i),mask]=(-1)**bin(mask&((1<<i)-1)).count("1")
        create.append(A)
    anni=[A.T for A in create]
    Q=S.zeros(16,4)
    for j,mask in enumerate((0,1,14,15)):Q[mask,j]=1
    # No hidden reduction of the other 12 components.
    first=S.eye(16)
    for i in range(4):first*=S.eye(16)-create[i]*anni[i]
    for ia,ma in enumerate((0,1,14,15)):
        for ib,mb in enumerate((0,1,14,15)):
            E=first
            for k in sorted((j for j in range(4) if mb & (1<<j)),reverse=True):
                E=E*anni[k]
            for k in sorted((j for j in range(4) if ma & (1<<j)),reverse=True):
                E=create[k]*E
            eq("CAR_matrix_unit_%d%d"%(ia,ib),E,Q[:,ia]*Q[:,ib].T)
    contexts=context()
    for k in range(3):
        eq("full16_Fock_outcomes_%d"%k,
           sum((Q*E*Q.T for E in contexts[4*k:4*k+4]),S.zeros(16))
           +(S.eye(16)-Q*Q.T), S.eye(16))
    aa=S.Rational(7,48);bb=S.Rational(1,16)
    F=(aa-bb)*S.eye(4)+bb*S.ones(4)
    dirs=[S.Matrix([0,0,-1,1]),S.Matrix([0,1,0,-1]),
          S.Matrix([0,-1,1,0])]
    def gamma(v):
        return sum((v[i]*(create[i]+anni[i]) for i in range(4)),S.zeros(16))
    def kk(v):
        return sum((v[i]*(create[i]-anni[i]) for i in range(4)),S.zeros(16))
    B=[gamma(d)*kk(F[:,j+1]) for j,d in enumerate(dirs)]
    d=aa**2+3*bb**2;b=aa**2-4*aa*bb-bb**2
    G=(2*d-b)*S.eye(3)+b*S.ones(3)
    for i in range(3):
        eq("first_source_compression_%d"%i,Q.T*B[i]*Q,S.zeros(4))
        for j in range(3):
            eq("second_source_compression_%d%d"%(i,j),
               Q.T*B[i]*B[j]*Q,G[i,j]*S.eye(4))
    pp=S.ones(3)/3
    inv=pp/S.sqrt(4*(aa-bb)**2)+(S.eye(3)-pp)/S.sqrt(aa**2+4*aa*bb+7*bb**2)
    V=[Q]+[sum((B[r]*Q*inv[r,k] for r in range(3)),S.zeros(16,4))
           for k in range(3)]
    eq("full16_syndrome_unity",S.Matrix.hstack(*V).T*S.Matrix.hstack(*V),S.eye(16))
    return V

def orbit_and_obstruction(V):
    r=2*p-1;s=2*p*S.sqrt(p)
    eq("golden_phase_unitary",r**2+s**2,1)
    psi=[S.Matrix([-s,r,0,-1])/S.sqrt(2),
         S.Matrix([-s,r,s,-r])/S.sqrt(2),
         S.Matrix([-s,r,2*r*s,-(r**2-s**2)])/S.sqrt(2)]
    G=S.Matrix.hstack(*psi).T*S.Matrix.hstack(*psi)
    eq("three_history_Gram",G,
       S.Matrix([[1,p,p**6],[p,1,p],[p**6,p,1]]))
    eq("three_history_Gram_determinant",G.det(),8*p**7)
    rho=sum((u*u.T for u in psi),S.zeros(4))/3
    eq("three_history_density_exact",rho,
       S.Matrix.hstack(*psi)*S.Matrix.hstack(*psi).T/3)
    eq("three_history_density_trace",S.trace(rho),1)
    Q=V[0]
    bs=[S.Rational(1,5),-S.Rational(2,7),S.Rational(1,3),S.Rational(3,8)]
    M=bs[0]*Q*Q.T
    for i in range(1,4):M+=bs[i]*(V[i]*Q.T+Q*V[i].T)
    eq("good_M_is_hermitian",M,M.T)
    eq("common_M_on_logical_code",M*Q,
       sum((bs[i]*V[i] for i in range(4)),S.zeros(16,4)))
    means=[S.trace(rho*V[i].T*M*Q) for i in range(4)]
    for i in range(4):eq("four_real_syndrome_sources_%d"%i,means[i],bs[i])
    eq("nonlinear_SOS_vanishes_for_common_coefficients",
       S.trace(rho*Q.T*M*M*Q),sum(z*z for z in means))
    # Two-history false PASS, three-history strict positive residual.
    two=S.Matrix.hstack(psi[0],psi[1])
    w=psi[2]-two*(two.T*two).inv()*two.T*psi[2]
    eq("two_history_invisible_witness_0",(w.T*psi[0])[0],0)
    eq("two_history_invisible_witness_1",(w.T*psi[1])[0],0)
    eq("witness_strength", (w.T*w)[0],8*p**6)
    d=8*p**6
    demand("three_history_nonzero_SOS",float(d**3/3-d**4/9)>0)
    # On K, lambda_min(rho)>=4det(G)/(27), giving one global orbit bound.
    return {"gram_determinant":"8p^7",
            "uniform_error_multiplier":"27/(32p^7)",
            "two_history_hidden_norm_sq":"8p^6",
            "nonlinear_memory_SOS_bad_fixture":float(d**3/3-d**4/9)}

def main():
    V=fock_code()
    answer=orbit_and_obstruction(V)
    return {"scope":"real four-dimensional logical memory in full16 CAR; field M_v required",
            "checks":checks,"count":len(checks),"data":answer,
            "actual_M_v_computed":False,"native_detector_admitted":False,
            "GR_closed":False}
if __name__=="__main__":
    print(json.dumps(main(),ensure_ascii=False,sort_keys=True,indent=2))
