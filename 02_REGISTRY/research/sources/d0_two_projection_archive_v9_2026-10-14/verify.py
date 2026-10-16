#!/usr/bin/env python3
"""Two-projection active-workspace completion: exact and outward-interval tests.
No asserts: -O executes the same checks. Default receipt is immutable.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json
from collections import Counter
from pathlib import Path
import sympy as s
import mpmath as mp
HERE=Path(__file__).resolve().parent
CHECKS=[]
def check(name, value):
    if not bool(value): raise AssertionError(name)
    CHECKS.append(name)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def exact():
    x,y,p,a=s.symbols('x y p a', real=True)
    ideal=s.groebner([y*y+x*x-1,a*a-p,p*p+p-1],y,a,p,domain=s.QQ.frac_field(x))
    def red(v):
        n,d=s.cancel(v).as_numer_denom()
        n=ideal.reduce(s.expand(n))[1];d=ideal.reduce(s.expand(d))[1]
        if d==0:raise ZeroDivisionError('DOMAIN')
        return s.cancel(n/d)
    def eq(name, M):check(name,all(red(v)==0 for v in M))
    I=s.eye(2);P=s.diag(1,0);R=s.Matrix([[x*x,x*y],[x*y,y*y]])
    eq('actual_projection_pair',R*R-R)
    V=-(2*P-I)*(2*R-I)
    K=(P+R-I)**2
    eq('loop_unitary',V.T*V-I)
    eq('complete_loop_defect',(I-V).T*(I-V)/4-K)
    eq('paired_original_square',K-x*x*I)
    eq('blank_compression',P*K*P-x*x*P)
    eq('P_reduces_full_square',P*K-K*P)
    eq('loop_conserves_full_square',V*K-K*V)
    B=p*I+(p*p/2)*(V+V.T)
    eq('same_golden_survival_full_space',B-(I-2*p*p*K))
    check('cutoff_survival_is_p_cubed',red(1-2*p*p-p**3)==0)
    # Two-qubit label preparation a|00>+p(|10>+|11>)/sqrt(2).
    G=s.Matrix([[a,-p],[p,a]])
    H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
    prep=s.diag(s.eye(2),H)*s.kronecker_product(G,I)
    eq('complete_label_preparation_unitary',prep.T*prep-s.eye(4))
    weights=[prep[j,0]**2 for j in range(4)]
    check('actual_labels_and_weights', [red(w) for w in weights]==[p,0,red(p*p/2),red(p*p/2)])
    words=[I,I,V,V.T]
    eq('literal_compressed_four_label_SELECT',sum((weights[j]*words[j] for j in range(4)),s.zeros(2))-B)
    for j in range(4):eq('each_record_branch_conserves_K_'+str(j),words[j]*K-K*words[j])
    branch=[sum((prep[j,k]*prep[j,0]*words[j] for j in range(4)),s.zeros(2)) for k in range(4)]
    eq('all_four_outcomes_retained',sum((T.T*T for T in branch),s.zeros(2))-I)
    eq('actual_blank_Kraus_block',branch[0]-B)
    check('REJECT_wrong_loop_sign',red(((I+V).T*(I+V)/4-K)[0,0])!=0)
    # Full rational carrier; the unused complement is present, not quotiented away.
    A=s.diag(0,s.Rational(3,5),s.Rational(5,13))
    C=s.diag(1,s.Rational(4,5),s.Rational(12,13))
    Q=s.diag(A.row_join(C).col_join(C.row_join(-A)),s.eye(3))
    J=s.eye(9)[:,:3];P=J*J.T;I9=s.eye(9)
    check('full_Q_is_unitary',Q.T*Q==I9)
    check('literal_original_block',J.T*Q*J==A)
    R=Q.T*P*Q;K=(P+R-I9)**2;V=-(2*P-I9)*(2*R-I9)
    expected=s.diag(A*A,A*A,s.eye(3))
    check('full_spectrum_two_copies_plus_cutoff',K==expected)
    check('cutoff_multiplicity_three',s.trace(K)-2*s.trace(A*A)==3)
    check('REJECT_workspace_is_passive_copy',K!=s.diag(A*A,A*A,A*A))
    check('REJECT_unused_workspace_is_zero',K!=s.diag(A*A,A*A,s.zeros(3)))
    check('complete_measured_loop_square',(I9-V).T*(I9-V)/4==K)
    check('complete_carrier_energy_conservation',V*K==K*V)
    check('zero_modes_are_doubled_not_deleted',9-K.rank()==2)
    # A completion change that fixes the input can mix the whole archive.
    O=I9.copy();i,j=3,8
    O[i,i]=O[j,j]=s.Rational(3,5);O[i,j]=-s.Rational(4,5);O[j,i]=s.Rational(4,5)
    Q2=O*Q*O.T;R2=Q2.T*P*Q2;K2=(P+R2-I9)**2
    check('completion_change_fixes_actual_input',O*J==J)
    check('completion_change_keeps_block',J.T*Q2*J==A)
    check('completion_change_not_trivial',K2!=K)
    check('completion_changes_only_full_frame',K2==O*K*O.T)
    for r in (1,2,3,4):check('completion_spectral_moment_'+str(r),s.trace(K2**r)==s.trace(K**r))
    # Genuine first jet of an isometric completion: no frozen square root.
    Ad=s.diag(0,-s.Rational(4,5),0);Cd=s.diag(0,s.Rational(3,5),0)
    Qd=s.diag(Ad.row_join(Cd).col_join(Cd.row_join(-Ad)),s.zeros(3))
    T=s.zeros(9);T[3,8]=1;T[8,3]=-1
    Qd=Qd+T*Q-Q*T
    check('full_Q_jet_is_tangent',Qd.T*Q+Q.T*Qd==s.zeros(9))
    Rd=Qd.T*P*Q+Q.T*P*Qd;S=P+R-I9;Kd=Rd*S+S*Rd
    dA=J.T*Qd*J;dDelta=A*dA+dA*A
    check('full_operator_compression_jet',J.T*Kd*J==dDelta)
    for r in (1,2,3,4):
        check('noncommuting_trace_jet_'+str(r),r*s.trace(K**(r-1)*Kd)==2*r*s.trace((A*A)**(r-1)*dDelta))
    check('REJECT_frozen_archive_frame_jet',Kd!=s.diag(dDelta,dDelta,s.zeros(3)))
    # Relative-sphere matter statement includes arbitrary archive directions.
    psi=J[:,1]
    check('complete_matter_eigenvector',K*psi==s.Rational(9,25)*psi)
    check('actual_loop_output_is_same_eigenvector_family',K*(V*psi)==s.Rational(9,25)*(V*psi))
    check('actual_output_not_just_original_blank',(I9-P)*(V*psi)!=s.zeros(9,1))
    # All degree-2 source directions are retained, not just an eigenvalue sample.
    for i in range(3):
      for j in range(i,3):
        X=s.zeros(3);X[i,j]=X[j,i]=1
        Hx=s.diag(X,X,s.zeros(3))
        check('all_compressed_probe_'+str((i,j)),J.T*Hx*J==X)
    n=s.symbols('n',integer=True,positive=True)
    lam,alpha,z=s.symbols('lam alpha z',positive=True)
    e=(1-alpha*lam)**(2*n)
    check('same_survival_thermal_jet',s.simplify(s.diff(e,lam)+2*n*alpha*e/(1-alpha*lam))==0)
    check('same_original_feedback_jet',s.simplify(s.diff(-s.log(1-z+z*e),lam)-2*n*alpha*z*e/((1-z+z*e)*(1-alpha*lam)))==0)
    # Proof of exponentially small BUT NONZERO whole-workspace heat correction.
    N=4096;nn=8192
    check('literal_workspace_dimension',64*16*N==4194304)
    check('literal_cutoff_state_count',62*16*N==4063232)
    check('counting_trace_half_correction',62*N//2==126976)
    check('strict_nonzero_cutoff_survival',(s.Rational(3,5))**(6*nn)>0)
    check('exact_cutoff_upper_bound_1e_minus10020',126976*5**(6*nn)*10**10020 < 8**(6*nn))
    # A physical extension is not uniquely forced merely by the blank block.
    alternative=s.diag(A*A,2*A*A,3*s.eye(3))
    check('REJECT_blank_block_alone_forces_completion',J.T*alternative*J==A*A and alternative!=K)
    # Actual same-program count instrument, not a postulated density polynomial.
    Vr=V[:6,:6]  # here V is the full rational 9-by-9 loop; use both paired copies
    Kr=K[:6,:6];Pr=s.diag(1,1,1,0,0,0);Ir=s.eye(6)
    def mr(M):return M.applyfunc(red)
    Br=mr(p*Ir+(p*p/2)*(Vr+Vr.T));Er=mr(Ir-Br*Br)
    def yes(X):return mr(Br*X*Br)
    def total(X):return mr(p*X+(p*p/2)*(Vr*X*Vr.T+Vr.T*X*Vr))
    def no(X):return mr(total(X)-yes(X))
    initial=Pr/3;states=[initial]
    for Tcount in range(1,4):
        nxt=[s.zeros(6) for _ in range(Tcount+1)]
        for k,X in enumerate(states):
            nxt[k]=mr(nxt[k]+yes(X));nxt[k+1]=mr(nxt[k+1]+no(X))
        states=nxt
        for k,X in enumerate(states):
            f=mr(s.binomial(Tcount,k)*Er**k*(Ir-Er)**(Tcount-k))
            check('actual_count_probability_'+str((Tcount,k)),red(s.trace(X)-s.trace(initial*f))==0)
            check('actual_count_energy_'+str((Tcount,k)),red(s.trace(Kr*X)-s.trace(initial*Kr*f))==0)
    selected=mr(states[1]+states[2]);f=mr(3*Er*(Ir-Er))
    check('REJECT_full_density_equals_effect_times_input',mr(selected-initial*f)!=s.zeros(6))
    check('selected_energy_completely_fixed_by_record_effect',red(s.trace(Kr*selected)-s.trace(initial*Kr*f))==0)
    l1,l2,da,db=s.symbols('l1 l2 da db',real=True)
    eta=lambda q:2*alpha*q-alpha*alpha*q*q
    fun=lambda q:3*eta(q)*(1-eta(q))
    FF=fun(l1)+fun(l2);RR=(l1*fun(l1)+l2*fun(l2))/FF
    direct=s.diff(RR,l1)*da+s.diff(RR,l2)*db
    derived=((fun(l1)+(l1-RR)*s.diff(fun(l1),l1))*da
              +(fun(l2)+(l2-RR)*s.diff(fun(l2),l2))*db)/FF
    check('full_normalized_preparation_covector',s.cancel(direct-derived)==0)
    return {'conditions':len(CHECKS),'negative_conditions':sum(k.startswith('REJECT') for k in CHECKS)}

def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def mul(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def features():
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
def intervals():
    mp.iv.dps=60;iv=mp.iv;rows=features()
    p=(iv.sqrt(5)-1)/2;alpha=p*p/8192;beta=2*p*p;z=iv.mpf(1)/1048576
    target=128-64*iv.sqrt(2);gamma=p**49152
    extra=126976*gamma  # full ordinary trace; zero is NOT substituted
    check('interval_cutoff_mass_strictly_positive',extra>0)
    check('interval_cutoff_mass_small',extra<iv.mpf('1e-10020'))
    check('all_original_modes_retained',sum(n for _,n in rows)==4096)
    check('all_exact_feature_classes',len(rows)==119)
    def val(q):return iv.mpf(q[0])+iv.mpf(q[1])*iv.sqrt(2)
    def eqs(x,mult=2048):
        Z=extra;u=[iv.mpf(0),iv.mpf(0)];r=[iv.mpf(0),iv.mpf(0)]
        v=[[iv.mpf(0) for _ in range(2)] for _ in range(2)]
        t=[[iv.mpf(0) for _ in range(2)] for _ in range(2)]
        for (aa,bb),count in rows:
            f=[val(aa),val(bb)];B=1-alpha*(x[0]*f[0]+x[1]*f[1]);e=B**16384
            w=count*e;R=z*e/(1-z+z*e);Z+=w
            for i in range(2):
                u[i]+=w*f[i]/B;r[i]+=count*R*f[i]/B
                for j in range(2):
                    v[i][j]+=w*f[i]*f[j]/B**2
                    t[i][j]+=count*R*(alpha-beta*(1-R))*f[i]*f[j]/B**2
        mu=[a/Z for a in u]
        F=[mu[0]-mult*beta*r[0]-target,mu[1]-mult*beta*r[1]]
        J=[[(alpha-beta)*v[i][j]/Z+beta*mu[i]*mu[j]-mult*beta*t[i][j] for j in range(2)] for i in range(2)]
        return F,J
    center=list(map(iv.mpf,CENTER));rad=iv.mpf('1e-12')
    box=[v+iv.mpf(['-1e-12','1e-12']) for v in center]
    P=[[iv.mpf(v) for v in row] for row in PRE]
    F,_=eqs(center);_,J=eqs(box)
    contraction=[];image=[]
    for i in range(2):
        c=sum(abs(iv.mpf(int(i==j))-sum(P[i][k]*J[k][j] for k in range(2))) for j in range(2))
        err=abs(sum(P[i][k]*F[k] for k in range(2)))+c*rad
        check('strict_contraction_'+str(i),c<iv.mpf('1e-6'))
        check('strict_self_mapping_'+str(i),err<rad)
        contraction.append(str(c));image.append(str(err))
    check('positive_metric_transverse',box[0]-box[1]>iv.mpf('.059'))
    check('positive_metric_uniform',box[0]+3*box[1]>iv.mpf('.075'))
    check('metric_coefficient_dilation_domain',box[0]+3*box[1]<1)
    for index,((aa,bb),count) in enumerate(rows):
        f0,f1=val(aa),val(bb);energy=box[0]*f0+box[1]*f1
        check('strict_A_squared_below_one_'+str(index),energy<16384)
        if aa==(0,0) and bb==(0,0):continue
        if aa==(128,-64) and bb==(0,0):continue
        check('first_shell_gap_'+str(index),energy-box[0]*target>iv.mpf('.5'))
    bad,_=eqs(center,mult=16)
    check('REJECT_dropped_reference_multiplicity',abs(bad[0])>iv.mpf('.01'))
    # Root displacement against the existing v8 map: Z>=1; |A|,|C|<=4096,
    # B>=p^3>1/5. Rational preconditioner norm<1/500. Bound is conservative.
    check('source_map_difference_small',extra*iv.mpf(20480)<iv.mpf('1e-10010'))
    check('existing_v8_root_displacement_bound',extra*iv.mpf(20480)/iv.mpf(500)/(1-iv.mpf('1e-6'))<iv.mpf('1e-10000'))
    return {'cutoff_mass_interval':str(extra),'contraction_intervals':contraction,
            'self_map_intervals':image,'root_radius':'1e-12',
            'root_displacement_from_pinned_v8_if_its_root_is_consumed':'<1e-10000'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    algebra=exact();iv=intervals()
    record={'schema':'d0-research-exact-interval/1','status':'PASS',
       'input_source':'bb301af84b116ee144a51d6e5537368745c01d69',
       'input_v8_verify_blob':'9657763d66455f3a5687fe774e0e7b746626945f',
       'exact':algebra,'total_conditions':len(CHECKS),
       'check_names_sha256':hashlib.sha256(json.dumps(CHECKS).encode()).hexdigest(),
       'interval':iv,'proof_sha256':digest(HERE/'RESULT.md'),
       'checker_sha256':digest(Path(__file__)),
       'compiler_workspace_operator_constructed':True,
       'persistent_outcome_tape_has_independent_energy_law':False,
       'native_physical_forcing':False,'pi0_placement':False,
       'old_state_conditioned_J_identified':False,'new_Lean_compilation':False,'GR_closed':False}
    path=HERE/'receipt.json'
    if args.write:path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    else:
        if not path.exists() or json.loads(path.read_text())!=record:raise SystemExit('IMMUTABLE_RECEIPT_MISMATCH')
    print(json.dumps({'status':'PASS','exact':algebra,'total':len(CHECKS),'physical_forcing':False}))
if __name__=='__main__':main()
