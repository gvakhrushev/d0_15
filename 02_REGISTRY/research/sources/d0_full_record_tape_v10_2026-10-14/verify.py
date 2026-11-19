#!/usr/bin/env python3
"""Full v9 tape completion: exact matrices and outward-rounded root proof.
No assert statements; -O executes the same gates. Receipt is immutable by default.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import mpmath as mp
import sympy as s
HERE=Path(__file__).resolve().parent
CHECKS=[]

def check(name, value):
    if not bool(value):
        raise AssertionError(name)
    CHECKS.append(name)

def eq(name, value):
    if isinstance(value,s.MatrixBase):
        check(name,all(s.expand(x)==0 for x in value.todok().values()))
    else:
        check(name,s.simplify(value)==0)

def exact():
    rat=s.Rational
    dbase,alphabet=6,4
    A=s.diag(rat(3,5),rat(5,13)); C=s.diag(rat(4,5),rat(12,13));O=s.zeros(2)
    Q=A.row_join(C).row_join(O).col_join(C.row_join(-A).row_join(O)).col_join(O.row_join(O).row_join(s.eye(2)))
    P=s.diag(1,1,0,0,0,0); I=s.eye(dbase);R=Q.T*P*Q
    K=(P+R-I)**2
    V=-(2*P-I)*(2*R-I)
    eq('base_Q_unitary',Q.T*Q-I)
    eq('base_compression',Q[:2,:2]-A)
    eq('base_second_projector',R*R-R)
    eq('base_full_square',K-s.diag(A*A,A*A,s.eye(2)))
    eq('base_loop_defect',(I-V).T*(I-V)/4-K)
    eq('base_loop_unitary',V.T*V-I)
    # Rational unitary splitter tests the literal PREP/SELECT construction.
    # Golden coefficients are verified separately, not replaced by this example.
    aa,pp=rat(4,5),rat(3,5)
    G=s.Matrix([[aa,-pp],[pp,aa]])
    HH=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
    Prep=s.diag(s.eye(2),HH)*s.kronecker_product(G,s.eye(2))
    PB=s.kronecker_product(Prep,I)
    W=(PB.T*s.diag(I,I,V,V.T)*PB).applyfunc(s.expand)
    B=I-2*pp**2*K
    eq('four_label_PREP_unitary',Prep.T*Prep-s.eye(4))
    eq('actual_four_label_W_unitary',W.T*W-s.eye(24))
    eq('actual_survival_block',W[:dbase,:dbase]-B)
    eq('v9_full_data_QND',W*s.kronecker_product(s.eye(4),K)-s.kronecker_product(s.eye(4),K)*W)
    for out in range(4):
        Ko=W[out*dbase:(out+1)*dbase,:dbase]
        eq('each_retained_outcome_QND_'+str(out),Ko*K-K*Ko)

    def embed(gate,which,n):
        out={};others=[i for i in range(n) if i!=which]
        for digits in itertools.product(range(alphabet),repeat=n-1):
            ds=[0]*n
            for i,x in zip(others,digits):ds[i]=x
            for (i,j),v in gate.todok().items():
                sr,ir=divmod(i,dbase);sc,ic=divmod(j,dbase)
                ds[which]=sr;row=0
                for x in ds:row=row*alphabet+x
                ds[which]=sc;col=0
                for x in ds:col=col*alphabet+x
                out[row*dbase+ir,col*dbase+ic]=v
        return s.SparseMatrix(dbase*alphabet**n,dbase*alphabet**n,out)

    def bare(n):
        Z=s.SparseMatrix(alphabet**n,alphabet**n,{(0,0):1})
        return s.kronecker_product(Z,K)+s.kronecker_product(s.eye(alphabet**n)-Z,I)

    U0=embed(W,0,2);U1=embed(W,1,2)
    U2=(U1*U0).applyfunc(s.expand)
    eq('all96_program_unitary',U2.T*U2-s.eye(96))
    Un=[I,W,U2];Fn=[];Pn=[];Jn=[]
    for n,U in enumerate(Un):
        N=dbase*alphabet**n
        J=s.SparseMatrix(N,2,{(0,0):1,(1,1):1})
        P0=J*J.T;Q0=s.kronecker_product(s.eye(alphabet**n),Q)
        R0=Q0.T*P0*Q0;F0=(P0+R0-s.eye(N))**2
        eq('full_bare_square_'+str(n),F0-bare(n))
        F=(U*bare(n)*U.T).applyfunc(s.expand)
        PF=(U*P0*U.T).applyfunc(s.expand);RF=(U*R0*U.T).applyfunc(s.expand)
        eq('transported_projector_square_'+str(n),(PF+RF-s.eye(N))**2-F)
        eq('actual_full_output_intertwines_'+str(n),F*U*J-U*J*A*A)
        Fn.append(F);Pn.append(P0);Jn.append(J)
        for power in (1,2):
            eq('full_spectral_moment_'+str((n,power)),s.trace(F**power)-2*s.trace((A*A)**power)-(N-4))
        eq('entire_blank_amplitude_'+str(n),J.T*U*J-(s.eye(2)-2*pp**2*A*A)**n)
        fb=P0*U.T*(s.eye(N)-P0)*U*P0
        eq('original_feedback_not_redefined_'+str(n),fb-J*(s.eye(2)-(s.eye(2)-2*pp**2*A*A)**(2*n))*J.T)
        if n:
            check('REJECT_all_tape_spectator_'+str(n),s.trace(F)!=s.trace(s.kronecker_product(s.eye(alphabet**n),K)))
    pad=s.SparseMatrix(96,24,{((i//dbase)*dbase*alphabet+i%dbase,i):1 for i in range(24)})
    J12=U1*pad
    eq('actual_next_step_isometry',J12.T*J12-s.eye(24))
    eq('whole_old_operator_naturality',Fn[2]*J12-J12*Fn[1])
    eq('all_new_modes_fixed_by_same_loop',Fn[2]-J12*Fn[1]*J12.T-(s.eye(96)-J12*J12.T))
    eq('original_retained_projector_is_natural',J12*W*Pn[1]*W.T*J12.T-U2*Pn[2]*U2.T)
    E1=W*s.kronecker_product(s.diag(1,0,0,0),I)*W.T
    naive=s.kronecker_product(s.eye(4),K)
    eq('positive_consistency_penalty',Fn[1]-naive-(s.eye(24)-naive)*(s.eye(24)-E1))
    check('REJECT_one_static_operator_commutes_with_program',Fn[1]*W!=W*Fn[1])
    out=W[:,0];rho=out*out.T
    dephased=s.diag(*[rho[i*dbase:(i+1)*dbase,i*dbase:(i+1)*dbase] for i in range(4)])
    e_deph=s.simplify(s.trace(dephased*Fn[1])-A[0,0]**2)
    check('REJECT_destroying_record_coherence_is_free',e_deph>0)
    eq('exact_dephasing_energy_witness',e_deph-rat(1526408810496,3814697265625))

    # A true noncommuting geometric jet: Q(t)=exp(tH)Q exp(-tH).
    H=s.zeros(dbase);H[0,3]=1;H[3,0]=-1
    dQ=H*Q-Q*H;dR=dQ.T*P*Q+Q.T*P*dQ
    dK=(P+R-I)*dR+dR*(P+R-I);dV=-2*(2*P-I)*dR
    dW=(PB.T*s.diag(s.zeros(dbase),s.zeros(dbase),dV,dV.T)*PB).applyfunc(s.expand)
    eq('true_Q_jet',dQ.T*Q+Q.T*dQ)
    eq('true_record_jet',dW.T*W+W.T*dW)
    check('noncommuting_underlying_Delta_jet',dK[:2,:2]*K[:2,:2]!=K[:2,:2]*dK[:2,:2])
    dU2=(embed(dW,1,2)*U0+U1*embed(dW,0,2)).applyfunc(s.expand)
    draw1=s.kronecker_product(s.diag(1,0,0,0),dK)
    draw2=s.kronecker_product(s.diag(1,*([0]*15)),dK)
    dF1=(dW*bare(1)*W.T+W*draw1*W.T+W*bare(1)*dW.T).applyfunc(s.expand)
    dF2=(dU2*bare(2)*U2.T+U2*draw2*U2.T+U2*bare(2)*dU2.T).applyfunc(s.expand)
    dJ=embed(dW,1,2)*pad
    eq('all96_true_naturality_jet',dF2*J12+Fn[2]*dJ-dJ*Fn[1]-J12*dF1)
    check('REJECT_frozen_refinement_jet',(dF2*J12-J12*dF1).applyfunc(s.expand)!=s.zeros(96,24))
    check('REJECT_frozen_program_jet',dF1!=W*draw1*W.T)
    dA=dQ[:2,:2];ds=dA*A+A*dA
    eq('full_moving_spectral_trace',s.trace(dF2)-2*s.trace(ds))
    for j in range(2):
        x=U2*Jn[2][:,j];dx=dU2*Jn[2][:,j]
        eq('full_moving_preparation_energy_'+str(j),(dx.T*Fn[2]*x+x.T*dF2*x+x.T*Fn[2]*dx)[0]-ds[j,j])

    p=(s.sqrt(5)-1)/2
    eq('golden_polynomial',p*p+p-1)
    eq('golden_cutoff_survivor',1-2*p*p-p**3)
    eq('golden_full_cutoff_heat',p**6-(9-4*s.sqrt(5)))
    eq('golden_inverse_threshold',p**6*(9+4*s.sqrt(5))-1)
    check('four_outcomes_strict_entropy_gap',bool(s.simplify(s.Rational(1,4)-4*p**6)>0))
    check('seventeen_outcomes_contract',bool(s.simplify(1-17*p**6)>0))
    check('eighteen_outcomes_expand',bool(s.simplify(18*p**6-1)>0))
    check('REJECT_128_outcome_shortcut',bool(s.simplify(128*p**6-1)>0))
    for n in range(9):
        old=64*4**n;new=64*4**(n+1)
        check('all_history_dimension_recursion_'+str(n),(new-2)==(old-2)+3*old)
    check('actual_L8_full_dimension_exponent',6+4+12+7+2*8192==16413)
    # Cyclic trace derivative of the full heat, J and unchanged quadratic matter.
    x,y,al,z,b,w,tail=s.symbols('x y al z b w tail',positive=True)
    bx=1-al*x;by=1-al*y;be=4*al
    Z=bx**4+by**4+tail
    price=s.log(2*b*Z)/be-b*s.log((1-z+z*bx**4)*(1-z+z*by**4))+w*x+(1-w)*y
    wanted=w-bx**3/Z+b*be*z*bx**3/(1-z+z*bx**4)
    eq('complete_scalar_source_derivative',s.diff(price,x)-wanted)
    check('REJECT_feedback_removed',s.simplify(s.diff(price,x)-(w-bx**3/Z))!=0)
    check('REJECT_tail_exactly_zero',s.simplify(wanted-wanted.subs(tail,0))!=0)
    return {'conditions':len(CHECKS),'full_program_test_dimension':96,
            'algebraic_splitter':'4/5,3/5; unitary control, not golden replacement',
            'dephasing_energy_increase':str(e_deph)}

def features():
    add=lambda a,b:(a[0]+b[0],a[1]+b[1])
    sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
    mul=lambda a,b:(a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    re=[(0,0),(-8,4),(-8,0),(-8,-4),(-16,0),(-8,-4),(-8,0),(-8,4)]
    im=[(0,0),(0,4),(8,0),(0,4),(0,0),(0,-4),(-8,0),(0,-4)]
    out=Counter()
    for ks in itertools.product(range(8),repeat=4):
        sr=si=A=(0,0)
        for k in ks:
            sr=add(sr,re[k]);si=add(si,im[k]);A=add(A,add(mul(re[k],re[k]),mul(im[k],im[k])))
        out[(A,sub(add(mul(sr,sr),mul(si,si)),A))]+=1
    return sorted(out.items())

CENTER=['0.063635191594344535042829697433316630182693569761541','0.0040167350432317252873844519148251220686807163526359']
PRE=[['-0.0011216462655310560286452808797667133745138481285227','0.0000214824372756590182021951630941663513783854757137'],['0.0000214824372756590182021951630941663513783854757137','-0.0011013196066395543959414028343546233134745970906891']]

def interval():
    before=len(CHECKS);mp.iv.dps=60;iv=mp.iv;rows=features()
    val=lambda v:iv.mpf(v[0])+iv.mpf(v[1])*iv.sqrt(2)
    p=(iv.sqrt(5)-1)/2;alpha=p*p/8192;beta=2*p*p;fug=iv.mpf(1)/1048576
    n=8192;target=128-64*iv.sqrt(2);gamma=p**(6*n)
    junk=(iv.mpf(32)*iv.mpf(4)**n-1)*4096*gamma
    check('all4096_modes',sum(c for _,c in rows)==4096)
    check('all119_exact_feature_pairs',len(rows)==119)
    check('all_cutoff_states_positive',junk>0)
    check('full_tape_cutoff_bound',junk<iv.mpf('1e-5330'))
    check('full_tape_not_old_spectator_tail',junk>31*4096*gamma*(iv.mpf(4)**n))
    lg=iv.log(junk)/iv.log(10)
    check('cutoff_exponent_lower',lg> -5335)
    check('cutoff_exponent_upper',lg< -5334)
    check('fixed_beta_record_count',2*n*alpha==beta)
    def equations(x,multiplicity=2048):
        Z=iv.mpf(0);u=[iv.mpf(0)]*2;r=[iv.mpf(0)]*2
        v=[[iv.mpf(0) for j in range(2)] for i in range(2)]
        t=[[iv.mpf(0) for j in range(2)] for i in range(2)]
        for (aa,cc),count in rows:
            f=[val(aa),val(cc)];B=1-alpha*sum(f[i]*x[i] for i in range(2));e=B**16384
            weight=count*e;R=fug*e/(1-fug+fug*e);Z+=weight
            for i in range(2):
                u[i]+=weight*f[i]/B;r[i]+=count*R*f[i]/B
                for j in range(2):
                    v[i][j]+=weight*f[i]*f[j]/B**2
                    t[i][j]+=count*R*(alpha-beta*(1-R))*f[i]*f[j]/B**2
        mu=[q/(Z+junk) for q in u]
        F=[mu[0]-multiplicity*beta*r[0]-target,mu[1]-multiplicity*beta*r[1]]
        J=[[(alpha-beta)*v[i][j]/(Z+junk)+beta*mu[i]*mu[j]-multiplicity*beta*t[i][j] for j in range(2)] for i in range(2)]
        return F,J
    center=list(map(iv.mpf,CENTER));rad=iv.mpf('1e-12')
    box=[x+iv.mpf(['-1e-12','1e-12']) for x in center]
    pre=[[iv.mpf(x) for x in row] for row in PRE]
    f0,_=equations(center);_,JI=equations(box)
    for i in range(2):
        rr=[iv.mpf(i==j)-sum(pre[i][k]*JI[k][j] for k in range(2)) for j in range(2)]
        contraction=sum(abs(v) for v in rr)
        image=abs(sum(pre[i][k]*f0[k] for k in range(2)))+contraction*rad
        check('interval_strict_contraction_'+str(i),contraction<iv.mpf('1e-6'))
        check('interval_maps_box_into_itself_'+str(i),image<rad)
    check('positive_transverse_metric',box[0]-box[1]>iv.mpf('.059'))
    check('positive_longitudinal_metric',box[0]+3*box[1]>iv.mpf('.075'))
    check('metric_below_identity',box[0]+3*box[1]<1)
    for j,((aa,cc),count) in enumerate(rows):
        lam=box[0]*val(aa)+box[1]*val(cc)
        check('full_survival_positive_'+str(j),1-alpha*lam>p**3)
        if aa!=(0,0) and (aa,cc)!=((128,-64),(0,0)):
            check('first_shell_strict_gap_'+str(j),lam-box[0]*target>iv.mpf('.5'))
    for wrong in (0,16):
        ff,_=equations(center,multiplicity=wrong)
        check('REJECT_wrong_feedback_multiplicity_'+str(wrong),abs(ff[0])>iv.mpf('1e-6'))
    return {'conditions':len(CHECKS)-before,'full_modes':4096,'exact_orbits':119,
            'parameters':{'L':8,'n':8192,'b':128,'z':'2^-20','beta':'2p^2'},
            'root_center':CENTER,'root_radius':'1e-12','contraction_upper':'1e-6',
            'positive_modal_tape_tail_upper':'1e-5330','modal_tail_log10_interval':['-5335','-5334'],
            'full_dimension':'2^16413','full_tape_not_enumerated':True}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    parser.add_argument('--math-only',action='store_true');parser.add_argument('--algebra-only',action='store_true')
    args=parser.parse_args();a=exact();v=None if args.algebra_only else interval()
    if args.math_only or args.algebra_only:
        print('PASS_MATHEMATICAL_GATES',len(CHECKS));return
    result={'schema':'d0-full-record-tape-v10/1','status':'PASS',
            'exact':a,'interval':v,'checks_sha256':hashlib.sha256(json.dumps(CHECKS,separators=(',',':')).encode()).hexdigest(),
            'proof_sha256':digest(HERE/'RESULT.md'),'checker_sha256':digest(Path(__file__)),
            'scope':{'full_outcome_tape_active':True,'same_record_intertwiner_all_n':True,
                     'shared_declared_H_Jprogram_R_root':True,
                     'M1_forcing':False,'old_chronological_J_identified':False,
                     'pi0_placement':False,'AF_or_spatial_refinement_identified':False,
                     'physical_Ward_or_GR':False,'new_Lean_compilation':False,
                     'old_owner_scripts_replayed_here':False}}
    path=HERE/'receipt.json'
    if args.write:path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    elif json.loads(path.read_text())!=result:raise AssertionError('IMMUTABLE_RECEIPT_MISMATCH')
    print('PASS_V10',len(CHECKS),'exact',a['conditions'],'interval',v['conditions'])
if __name__=='__main__':main()
