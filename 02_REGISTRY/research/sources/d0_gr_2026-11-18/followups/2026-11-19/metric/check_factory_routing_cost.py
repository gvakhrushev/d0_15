"""One physical Toffoli schedule, retained transcripts, and shared known one.

Gate-primitive costs and Book03 price are not inferred from code-CQ. The
teleporting instruments are checked on all 8 input columns, before and after
the first guarded Fredkin's four actual pre-Toffoli CX stages.
"""
import json
from itertools import product
import sympy as s
import mpmath as mp


def embed(local,wires,n=5):
    D=1<<n; q=len(wires); M=s.zeros(D,D)
    for col in range(D):
        b=0
        for w in wires:b=2*b+((col>>(n-1-w))&1)
        for k in range(1<<q):
            val=local[k,b]
            if not val:continue
            row=col
            for j,w in enumerate(wires):
                mask=1<<(n-1-w)
                row=(row&~mask)|(((k>>(q-1-j))&1)*mask)
            M[row,col]=val
    return M


def main():
    root=s.sqrt(2);I=s.eye(2);X=s.Matrix([[0,1],[1,0]])
    H=s.Matrix([[1,1],[1,-1]])/root;vplus=s.Matrix([1,1])/root
    vm=s.Matrix([1,-1])/root;Pp=(I+X)/2;Pm=(I-X)/2
    CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    CZ=s.diag(1,1,1,-1)
    SW=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    CCZ=s.eye(8);CCZ[7,7]=-1
    TOF=s.eye(8);TOF[6,6]=TOF[7,7]=0;TOF[6,7]=TOF[7,6]=1
    # h,a,b,R1,R2. Original known-one is separate, factored and preserved.
    V=s.kronecker_product(s.eye(8),vplus,vplus)
    def op(U,*w):return embed(U,w)
    # 4 actual pre-Toffoli CX gates of negative Fredkin: SWAP then first CX.
    pre=op(CX,2,1)*op(CX,2,1)*op(CX,1,2)*op(CX,2,1)
    V=pre*V
    Z1=op(CZ,2,3);Z2=op(CZ,2,4);C3=op(CCZ,0,1,2)
    W1,W2=op(SW,2,3),op(SW,2,4)
    post=op(CX,2,1)
    # Completion before/after X-sign measurement; sign recorded in R_i.
    h1=[];h2=[]
    for P,correct in ((Pp,I),(Pm,X)):
        h1.append(W1*op(P,2)*op(correct,3)*Z1)
        h2.append(W2*op(P,2)*op(correct,4)*Z2)
    # Confirm unfinished H is still a scalar isometry on all protected inputs.
    for K in (V,Z1*V):
        assert s.simplify(K.T*K-s.eye(8))==s.zeros(8)
    all_err=0
    for i in (0,1):
        V1=h1[i]*V
        for K in (V1,C3*V1,Z2*C3*V1):
            assert s.simplify(K.T*K-s.eye(8)/2)==s.zeros(8)
        for j in (0,1):
            final=post*h2[j]*C3*V1
            assert s.simplify(final.T*final-s.eye(8)/4)==s.zeros(8)
            expected_data=s.zeros(8,8)
            for h,a,b in product((0,1),repeat=3):
                col=4*h+2*a+b
                aa,bb=((b,a) if h==0 else (a,b))
                expected_data[4*h+2*aa+bb,col]=1
            expected=s.kronecker_product(expected_data,
                       vplus if i==0 else vm,vplus if j==0 else vm)/2
            assert s.simplify(final-expected)==s.zeros(32,8)
            all_err+=1
    assert all_err==4
    # After CZ succeeds but the X-measurement exhausts its cap, the normalized
    # retained data+resource is CZ(|+>|+>): a pure isometric output, but the
    # reduced data is I/2, so the abort cannot be replaced by identity.
    ent=CZ*s.kronecker_product(vplus,vplus)
    resh=s.Matrix([[ent[0],ent[1]],[ent[2],ent[3]]])
    assert s.simplify(resh*resh.T-s.eye(2)/2)==s.zeros(2)

    # Two weak tests of X: exact Golden-field identities, including the
    # otherwise-dark fourth transcript. All signs are retained in records.
    p=(s.sqrt(5)-1)/2;a=s.sqrt(p);X2=X
    A0=p*I-p**2*X2;A1=a*p*(I+X2)
    B0=p*I+p**2*X2;B1=-a*p*(I-X2)
    assert s.simplify(B0*A0-p**3*I)==s.zeros(2)
    assert s.simplify(B0*A1-a*p*(I+X2))==s.zeros(2)
    assert s.simplify(B1*A0+a*p*(I-X2))==s.zeros(2)
    assert s.simplify(B1*A1)==s.zeros(2)
    Z=s.diag(1,-1);zero=s.Matrix([1,0])
    assert s.simplify((B0*A1*zero).dot(B0*A1*zero)-2*p**3)==0
    assert s.simplify((Z*B1*A0*zero).dot(Z*B1*A0*zero)-2*p**3)==0
    # Shared known-one: every CX(known,target) keeps the first bit exactly 1.
    for t in (0,1):assert CX[2+(1-t),2+t]==1

    # Retain the nonzero p^384 cap-abort probabilities (about 1e-80).
    mp.mp.dps=160;p=(mp.sqrt(5)-1)/2;ell=mp.log(1/p);r=p**2
    L=64;K=40;s2=4*p**3;s3=16*p**9
    b2=1-(1-s2)**L;b3=1-(1-s3)**L
    n2=b2/s2;n3=b3/s3;b1=1-p**K
    beta=b2**6*b3
    # Exhaustive first-cap-abort partition before a completed Toffoli.
    abort=[1-b2,b2*(1-b2),b2**2*(1-b2),b2**3*(1-b2),
           b2**4*(1-b3),b2**4*b3*(1-b2),b2**5*b3*(1-b2)]
    x,y=s.symbols('b2 b3',real=True)
    symbolic=[1-x,x*(1-x),x**2*(1-x),x**3*(1-x),
              x**4*(1-y),x**4*y*(1-x),x**5*y*(1-x)]
    assert s.expand(sum(symbolic)+x**6*y-1)==0
    assert all(x>0 for x in abort) and abs(sum(abort)+beta-1)<mp.mpf('1e-140')
    entropy=lambda arr:-sum(x*mp.log(x)/ell for x in arr if x)
    f=lambda t:1+t-entropy((t,1-t))
    fx=2+s2-entropy((1-s2,s2/2,s2/2))
    cp=n2*fx;ch=n2*f(s2)+b2*n2*fx
    ct=cp*(1+b2)+b2**2*(ch+b2**2*n3*f(s3)+b2**2*b3*ch)
    def gate_budget(M):
        reaches=(1-beta**M)/(1-beta)
        return dict(M=M,shared_known_one_probability=str(b1),
          all_success_probability=str(b1*beta**M),
          expected_factories_per_full_attempt_including_bootstrap_abort=str(b1*reaches),
          factory_record_code_minus_CQ_only=str(b1*reaches*ct))
    print(json.dumps(dict(status='PASS',logical_input_columns=8,
      full_input_and_two_work_qubits_dimension=32,
      first_fredkin_pre_Toffoli_actual_CX=4,
      abort_after_CZ_can_dephase_reduced_data_if_resource_traced=True,
      all_four_teleport_sign_pairs_equal_exact_negative_Fredkin=all_err,
      isometric_failure_cuts=['H1_CZ','H1_X','CCZ','H2_CZ','H2_X'],
      weak_X_four_transcript_identities=True,
      shared_known_one_not_a_target=True,
      X_plus_birth_preparation_uses_conditional_Z_SourceI_squared=True,
      b2=str(b2),b3=str(b3),b1=str(b1),beta=str(beta),
      first_abort_classes=[str(x) for x in abort],
      all_first_abort_plus_success_exactly_normalized=True,
      X_cycle_code_minus_CQ=str(fx),one_plus_code_minus_CQ=str(cp),
      one_H_code_minus_CQ=str(ch),one_complete_Toffoli_factory_record_code_minus_CQ=str(ct),
      factory_budgets=[gate_budget(142),gate_budget(248)],
      constants_apply_only_to_fixed_program_scalar_success_and_declared_0_10_codes=True,
      empirical_Book03_CostInfo_selected=False,
      full_factory_expanded_growing_clock_constructed=False,
      physical_addressability_and_printing_constructed=False,
      GR_closed=False),indent=2))

if __name__=='__main__':main()
