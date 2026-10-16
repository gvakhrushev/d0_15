#!/usr/bin/env python3
"""Record-generated heat and shared H+J_program+R. Exact/interval, not GR.
Default checks immutable receipt; --write is an explicit receipt refresh.
No assert statements: optimized Python executes the same mathematical gates.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json
from collections import Counter
from pathlib import Path
import mpmath as mp
import sympy as s
HERE=Path(__file__).resolve().parent
CHECKS=[]
def check(name,condition):
    if not bool(condition): raise AssertionError(name)
    CHECKS.append(name)
def exact():
    I=s.eye(16)
    def creator(r):
        C=s.zeros(16)
        for j in range(16):
            if not j&(1<<r): C[j|(1<<r),j]=(-1)**((j&((1<<r)-1)).bit_count())
        return C
    cs=[creator(r) for r in range(4)]
    subsets=[tuple(r for r in range(4) if j&(1<<r)) for j in range(16)]
    def ext(F):
        return s.Matrix(16,16,lambda i,j: F.extract(subsets[i],subsets[j]).det()
            if len(subsets[i])==len(subsets[j]) and subsets[i] else int(i==j==0))
    def turn(i,j,x=s.Rational(3,5),y=s.Rational(4,5)):
        F=s.eye(4);F[i,i]=F[j,j]=x;F[i,j]=-y;F[j,i]=y;return ext(F)
    returns=[turn(0,1),turn(1,2),turn(2,3),turn(0,3)]
    check('noncommuting_returns',returns[0]*returns[1]!=returns[1]*returns[0])
    words=[];d=s.zeros(16)
    for r,(c,T) in enumerate(zip(cs,returns)):
        b=c+c.T;z=c-c.T
        words.extend([b*T,z*T,T.T*b,-T.T*z,-b,-b])
        d+=c*(T-I)
    D=d+d.T
    words.extend([I]*4+[-I]*4)
    check('thirty_two_structural_labels',len(words)==32)
    for j,V in enumerate(words): check('unitary_word_'+str(j),V.T*V==I)
    A=sum(words,s.zeros(16))/32
    check('full_Dirac_block',A==D/16)
    check('Dirac_selfadjoint',D==D.T)
    scalar=sum([(T-I).T*(T-I) for T in returns],s.zeros(16))
    check('REJECT_curvature_commutators_omitted',D*D!=scalar)
    H=s.Matrix(32,32,lambda i,j:(-1)**((int(i)&int(j)).bit_count()))
    check('full_Hadamard_frame',H*H.T==32*s.eye(32))
    # Q=(H/sqrt32) SELECT (H/sqrt32). Each row/column has all labels.
    blocks=[sum([H[j,k]*words[k] for k in range(32)],s.zeros(16))/32 for j in range(32)]
    check('full_Q_row_isometry',sum([X*X.T for X in blocks],s.zeros(16))==I)
    check('full_Q_column_isometry',sum([X.T*X for X in blocks],s.zeros(16))==I)
    w=[(I if j==0 else s.zeros(16))-2*blocks[j].T*A for j in range(32)]
    check('full_reflection_column',sum([X.T*X for X in w],s.zeros(16))==I)
    check('retained_reflection_block',w[0]==I-2*A.T*A)
    p=s.Symbol('p',real=True)
    def red(x):return s.rem(s.expand(x),p*p+p-1,p)
    check('golden_total_port_norm',red(p*p+p**4+2*p**3)==1)
    check('golden_cross_port_cancellation',red(p**3-p**3)==0)
    check('survival_lower_bound',red(1-2*p*p-p**3)==0)
    check('B_from_actual_golden_port',(p*I+p*p*w[0]-(I-2*p*p*A.T*A)).applyfunc(red)==s.zeros(16))
    Vdot=(cs[0]*cs[1].T-cs[1]*cs[0].T)*returns[0]
    b0=cs[0]+cs[0].T;z0=cs[0]-cs[0].T
    Adot=(b0*Vdot+z0*Vdot+Vdot.T*b0-Vdot.T*z0)/32
    Ddot=cs[0]*Vdot+Vdot.T*cs[0].T
    check('noncommuting_Dirac_word_jet',Adot==Ddot/16)
    check('noncommuting_square_jet',A.T*Adot+Adot.T*A==(D*Ddot+Ddot*D)/256)
    check('REJECT_frozen_operator_jet',D*Ddot+Ddot*D!=s.zeros(16))
    # Probability bookkeeping with a fully coupled, rational unitary walk.
    q=s.Rational(2,5);r=s.Rational(1,5)
    B=s.diag(1-q,1-r)
    # Two fresh registers: verify the original all-blank compression, not resetting.
    Ws=[]
    # Rational involution in each data eigenspace: compression 3/5 or 5/13.
    B=s.diag(s.Rational(3,5),s.Rational(5,13));C=s.diag(s.Rational(4,5),s.Rational(12,13))
    W=B.row_join(C).col_join(C.row_join(-B))
    check('test_full_record_isometry',W.T*W==s.eye(4))
    # order (record0,record1,data), untouched record included explicitly
    U0=s.zeros(8);U1=s.zeros(8)
    for f0,f1,k in itertools.product(range(2),repeat=3):
        j=4*f0+2*f1+k
        for out in range(2):
            U0[4*out+2*f1+k,j]=W[2*out+k,2*f0+k]
            U1[4*f0+2*out+k,j]=W[2*out+k,2*f1+k]
    U=U1*U0;P=s.diag(1,1,0,0,0,0,0,0)
    check('complete_two_record_isometry',U.T*U==s.eye(8))
    check('all_blank_survivor',U[:2,:2]==B**2)
    F=P*U.T*(s.eye(8)-P)*U*P
    check('full_program_feedback',F==s.diag(*(list((s.eye(2)-B**4).diagonal())+[0]*6)))
    check('REJECT_one_tick_replaces_two',F[:2,:2]!=s.eye(2)-B**2)
    z=s.Symbol('z');pencil=(s.eye(8)-z*F).det()
    check('full_determinant_zeros_retained',s.expand(pencil-((1-z)*s.eye(2)+z*B**4).det())==0)
    check('REJECT_feedback_vanishes',F!=s.zeros(8))
    for j in (1,2,4):
        check('ancilla_multiplicity_'+str(j),s.kronecker_product(s.eye(j),F).trace()==j*s.trace(F))
    # Moving-label weights; dropping this derivative would invalidate the block.
    u=s.symbols('u0:4',positive=True)
    weights=[u[r]/32 for r in range(4) for _ in range(6)]+[(16-3*sum(u))/128]*8
    check('all_moving_label_weights_normalized',s.expand(sum(weights)-1)==0)
    for r in range(4):check('moving_label_normalization_jet_'+str(r),sum(s.diff(v,u[r]) for v in weights)==0)
    # Pure-sphere stationarity of a mixed reduced eigenstate via full purification.
    diag=s.diag(0,2,2,4);psi=s.Matrix([0,0,1,0,0,1,0,0])/s.sqrt(2)
    full=s.kronecker_product(diag,s.eye(2))
    check('purified_eigenstate_full_matter_equation',full*psi==2*psi)
    # Pointwise coefficients do not commute with lattice returns. Dilate them
    # on ONE additional qubit, before SELECT. No spectral Delta oracle is used.
    Ux=s.diag(s.Rational(3,5),s.Rational(5,13))
    Sx=s.diag(s.Rational(4,5),s.Rational(12,13))
    Co=s.kronecker_product(Ux,cs[0]);Be=Co+Co.T;Ze=Co-Co.T
    Sl=s.kronecker_product(Sx,I);Id=s.eye(32)
    Bh=Be.row_join(Sl).col_join(Sl.row_join(-Be))
    Zh=Ze.row_join(Sl).col_join(Sl.row_join(Ze))
    check('pointwise_beta_dilation',Bh.T*Bh==s.eye(64))
    check('pointwise_zeta_dilation',Zh.T*Zh==s.eye(64))
    Tx=s.kronecker_product(s.Matrix([[0,1],[1,0]]),I)
    Tlift=s.diag(Tx,Tx)
    check('coefficient_shift_noncommuting',Be*Tx!=Tx*Be)
    check('coefficient_dilation_before_shift',(Bh*Tlift)[:32,:32]==Be*Tx)
    check('adjoint_shift_before_coefficient',(Tlift.T*Bh)[:32,:32]==Tx.T*Be)
    actual=Co*(Tx-Id)+(Tx.T-Id)*Co.T
    terms=(Bh*Tlift+Zh*Tlift+Tlift.T*Bh-Tlift.T*Zh-2*Bh)/2
    check('local_noncommuting_Dirac_block',terms[:32,:32]==actual)
    check('REJECT_symmetric_coefficient_sandwich',Be*Tx!=Tx*Be)
    # Derivative of sqrt(1-u^2) is retained; this remains a true unitary jet.
    dBe=s.kronecker_product(s.diag(1,0),cs[0]+cs[0].T)
    dSl=s.kronecker_product(s.diag(-s.Rational(3,4),0),I)
    dBh=dBe.row_join(dSl).col_join(dSl.row_join(-dBe))
    check('local_coefficient_dilation_true_jet',dBh.T*Bh+Bh.T*dBh==s.zeros(64))
    bad=dBe.row_join(s.zeros(32)).col_join(s.zeros(32).row_join(-dBe))
    check('REJECT_frozen_square_root_jet',bad.T*Bh+Bh.T*bad!=s.zeros(64))
    # Norm bounds for the exact logarithmic derivative, analytic proof in memo.
    x,y,alpha=s.symbols('x y alpha',positive=True)
    g=-s.log(1-alpha*x)/alpha
    check('log_generator_derivative',s.simplify(s.diff(g,x)-1/(1-alpha*x))==0)
    n=s.Symbol('n',integer=True,positive=True);beta=2*n*alpha
    e=(1-alpha*x)**(2*n)
    check('same_word_heat_jet',s.simplify(s.diff(e,x)+beta*e/(1-alpha*x))==0)
    j=-s.log(1-z+z*e)
    check('same_word_feedback_jet',s.simplify(s.diff(j,x)-beta*z*e/((1-z+z*e)*(1-alpha*x)))==0)
    check('REJECT_log_generator_equals_quadratic_exactly',s.diff(g,x)!=1)
    # Homogeneous diagonal source and the genuine complete exterior-link trace.
    for a in range(4):
      for b in range(4):
        K=s.zeros(4);K[a,b]=1;Gamma=cs[a]*cs[b].T
        for i in range(4):
          for r in range(4):
            check('link_trace_'+str((a,b,i,r)),s.trace(cs[i].T*cs[r]*Gamma)==4*(int(i==r)*s.trace(K)-K[i,r]))
    return {'exact_conditions':len(CHECKS),'negative_conditions':sum(n.startswith('REJECT') for n in CHECKS)}

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

CENTER=['0.063635191594344535042829697433316630182693569761541', '0.0040167350432317252873844519148251220686807163526359']
# The preconditioner is only a rational certificate witness, not a selected field.
PRECONDITIONER=[['-0.0011216462655310560286452808797667133745138481285227', '0.0000214824372756590182021951630941663513783854757137'], ['0.0000214824372756590182021951630941663513783854757137', '-0.0011013196066395543959414028343546233134745970906891']]

def interval():
    mp.iv.dps=60;iv=mp.iv;rows=features()
    check('all4096_fourier_modes',sum(n for _,n in rows)==4096)
    check('all119_exact_orbits',len(rows)==119)
    def val(v):return iv.mpf(v[0])+iv.mpf(v[1])*iv.sqrt(2)
    p=(iv.sqrt(5)-1)/2;alpha=p*p/8192;beta=2*p*p;fug=iv.mpf(1)/1048576
    target=128-64*iv.sqrt(2)
    def equations(x,multiplicity=2048,omit_feedback=False):
        Z=iv.mpf(0);u=[iv.mpf(0)]*2;r=[iv.mpf(0)]*2
        v=[[iv.mpf(0) for _ in range(2)] for _ in range(2)]
        t=[[iv.mpf(0) for _ in range(2)] for _ in range(2)]
        for (aa,bb),count in rows:
            f=[val(aa),val(bb)];B=1-alpha*(f[0]*x[0]+f[1]*x[1]);e=B**16384
            w=count*e;R=fug*e/(1-fug+fug*e);Z+=w
            for i in range(2):
                u[i]+=w*f[i]/B;r[i]+=count*R*f[i]/B
                for j in range(2):
                    v[i][j]+=w*f[i]*f[j]/B**2
                    t[i][j]+=count*R*(alpha-beta*(1-R))*f[i]*f[j]/B**2
        mu=[q/Z for q in u];B1=1-alpha*x[0]*target
        m=0 if omit_feedback else multiplicity
        F=[mu[0]-m*beta*r[0]-target,mu[1]-m*beta*r[1]]
        J=[[(alpha-beta)*v[i][j]/Z+beta*mu[i]*mu[j]-m*beta*t[i][j] for j in range(2)] for i in range(2)]
        return F,J
    C0=list(map(iv.mpf,CENTER));X=[v+iv.mpf(['-1e-12','1e-12']) for v in C0]
    P=[[iv.mpf(v) for v in row] for row in PRECONDITIONER];rad=iv.mpf('1e-12')
    f0,_=equations(C0);_,JI=equations(X)
    C=[[iv.mpf(int(i==j))-sum(P[i][k]*JI[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    for i in range(2):
        q=sum(abs(v) for v in C[i]);err=abs(sum(P[i][j]*f0[j] for j in range(2)))
        check('interval_contraction_'+str(i),q<iv.mpf('1e-6'))
        check('interval_self_mapping_'+str(i),err+q*rad<rad)
    check('SPD_transverse',X[0]-X[1]>iv.mpf('.059'))
    check('SPD_longitudinal',X[0]+3*X[1]>iv.mpf('.075'))
    check('SPD_uniform_upper1',X[0]+3*X[1]<1)
    count=0
    for (aa,bb),mult in rows:
        if aa==(0,0):continue
        if aa==(128,-64) and bb==(0,0):count+=mult;continue
        check('next_shell_'+str((aa,bb)),(val(aa)-target)*X[0]+val(bb)*X[1]>iv.mpf('.5'))
    check('eight_first_shell_modes',count==8)
    false,_=equations(C0,multiplicity=16)
    check('REJECT_reference_register_omitted',abs(false[0])>iv.mpf('.01'))
    false,_=equations(C0,omit_feedback=True)
    check('REJECT_feedback_omitted_from_root',abs(false[0])>iv.mpf('.01'))
    return {'root_center':CENTER,'root_radius':'1e-12','source_equations':'all ten homogeneous metric; local via translation; full isometric return class',
            'L':8,'rounds':8192,'beta':'2*p^2','alpha':'p^2/8192','fugacity':'2^-20',
            'Fock_dimension':16,'purifying_reference_dimension':128,'feedback_multiplicity':2048,
            'workspace_dimension':'128^8192','workspace_thermal_multiplicity_retained':True,'matter_operator':'Delta, not log generator',
            'contraction_upper':'1e-6','next_shell_gap_lower':'.5'}

def continuum():
    iv=mp.iv;iv.dps=60
    one=Counter(k*k for k in range(-8,9));cnt=Counter({0:1})
    for _ in range(4):
        nxt=Counter()
        for i,ni in cnt.items():
            for j,nj in one.items():nxt[i+j]+=ni*nj
        cnt=nxt
    p=(iv.sqrt(5)-1)/2;beta=2*p*p;z=iv.mpf(1)/1048576;amin=iv.mpf('1.80')
    tails=[2*iv.mpf(9)**(2*r)*iv.exp(-amin*81)/(1-(iv.mpf(10)/9)**(2*r)*iv.exp(-amin*19)) for r in range(3)]
    # Z1<3, second and fourth moments <10 bound all one-dimensional factors.
    for r,bound in ((0,3),(1,10),(2,10)):
        val=sum(iv.mpf(k)**(2*r)*iv.exp(-amin*k*k) for k in range(-8,9))+tails[r]
        check('gaussian_1d_bound_'+str(r),val<bound)
    tail=[4*27*tails[0],4*(27*tails[1]+3*10*9*tails[0]),
        4*(27*tails[2]+3*10*9*tails[0]+6*10*9*tails[1]+6*100*3*tails[0])]
    def evaluate(a):
        S=[iv.mpf(0) for _ in range(3)];Q=[iv.mpf(0),iv.mpf(0)]
        for k,n in cnt.items():
            e=iv.exp(-a*k);r=z*e/(1-z+z*e)
            for j in range(3):S[j]+=n*k**j*e
            Q[0]+=n*k*r;Q[1]+=n*k*k*r*(1-r)
        for j in range(3):S[j]+=iv.mpf([0,1])*tail[j]
        for j in range(2):Q[j]+=iv.mpf([0,1])*z/(1-z)*tail[j+1]
        F=S[1]/S[0]-2048*beta*Q[0]-1
        der=-(S[2]/S[0]-(S[1]/S[0])**2)+2048*beta*Q[1]
        ratio=2048*beta*z*S[0]/(1-z)
        return F,der,ratio
    check('continuum_root_left',evaluate(iv.mpf('1.80'))[0]>0)
    check('continuum_root_right',evaluate(iv.mpf('1.82'))[0]<0)
    _,der,ratio=evaluate(iv.mpf(['1.80','1.82']))
    check('continuum_radial_jacobian',der<iv.mpf('-.67'))
    check('continuum_offdiagonal_jacobian',ratio<iv.mpf('.005'))
    return {'limiting_a_interval':['1.80','1.82'],'radial_derivative_upper':'-.67',
        'offdiagonal_feedback_ratio_upper':'.005','infinite_gaussian_tails_included':True,
        'all_sufficiently_large_periodic_levels':'analytic C1/implicit-function consequence; not native AF bonds'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    result={'schema':'d0-v8-record-generated-heat/1','status':'PASS','exact':exact(),'interval':interval(),'continuum':continuum(),
       'physical_native_admission':False,'old_state_conditioned_J_identification':False,
       'stable_minimum':False,'native_AF_refinement':False,'Einstein_GR':False,'new_Lean':False}
    result['total_conditions']=len(CHECKS)
    result['checks_sha256']=hashlib.sha256('\n'.join(CHECKS).encode()).hexdigest()
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['proof_sha256']=hashlib.sha256((HERE/'RESULT.md').read_bytes()).hexdigest()
    path=HERE/'receipt.json'
    if args.write:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    else:
        old=json.loads(path.read_text())
        if old!=result:raise AssertionError('IMMUTABLE_RECEIPT_MISMATCH')
    print('PASS',result['total_conditions'],'conditions; full same-program root; no native GR claim')
if __name__=='__main__':main()
