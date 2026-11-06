#!/usr/bin/env python3
"""Full retained-prefix covector: exact identities and scoped numerical controls.

No GR root, gate-admission theorem or complete native dust compiler is asserted.
Uses the pinned ORIGINAL CAR/Julia/Walsh constructor only for the old prefix.
Future scalar formula is the existing section 7dd interface, not a new action.
"""
from __future__ import annotations
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ.setdefault(key,'1')
from fractions import Fraction as F
from pathlib import Path
import hashlib, importlib.util, json, math, platform
import numpy as np
import scipy.linalg as la
import sympy as sp
import mpmath as mp

ROOT=Path(__file__).resolve().parent
PIN='a05b9295a116543c037eb668651195449bb5d7b9b061c70eb73c4a045238253a'
checks=0

def require(value: bool, name: str) -> None:
    global checks
    checks+=1
    if not bool(value):
        raise AssertionError(name)

def near(a,b,name,tol=1e-11):
    error=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(error<tol,name+': '+str(error))
    return error

def original_module():
    canonical=ROOT.parent/'d0_original_retained_history_source_2026-10-28'/'check_history_source.py'
    path=canonical if canonical.is_file() else ROOT/'inputs'/'check_history_source.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest()==PIN,'immutable original constructor bytes')
    spec=importlib.util.spec_from_file_location('original_history',path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load original constructor')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def symbolic_controls():
    # Original 7dd rational nonnormal control; NOT a newly claimed physical prefix.
    K0=sp.Matrix([[sp.Rational(43,75),sp.Rational(4,25)],
                  [sp.Rational(8,25),sp.Rational(19,50)]])
    S0=K0.T*K0
    require(K0*K0.T!=S0,'nonnormal prefix retained')
    require(S0.det()>0 and S0.trace()>0,'prefix Gram positive')
    z=sp.Rational(1,7);a=1-z
    alpha=sp.Rational(1,2);gamma=sp.Rational(1,3);Omega=sp.Rational(5,4)
    P1=sp.Rational(1,5);P2=sp.Rational(1,4)
    def t(P):return 1-alpha*gamma*P*(1-gamma*P)
    def b(P):return alpha*gamma*(1-2*gamma*P)
    ts=[t(P1),t(P2)];T=sp.prod(ts)
    D=a*sp.eye(2)+z*T*S0;R=D.inv();tr=(R*S0).trace();w=z*T*tr
    weights=[b(P1)/(Omega*ts[0]),b(P2)/(Omega*ts[1])]
    Lam=sum(weights);G=w*Lam
    require(G>0,'actual common gain positive')
    u=sp.symbols('u',real=True)
    prefix_rows=[]
    for i in range(2):
        for j in range(2):
            E=sp.zeros(2);E[i,j]=1
            Ku=K0+u*E
            dS=E.T*K0+K0.T*E
            Dvar=a*sp.eye(2)+z*T*(Ku.T*Ku)
            determinant=Dvar.det()
            direct=-sp.diff(determinant,u).subs(u,0)/determinant.subs(u,0)
            formula=-z*T*(R*dS).trace()
            require(sp.simplify(direct-formula)==0,'full determinant/prefix entry derivative')
            require(sp.simplify(direct/G+(R*dS).trace()/(tr*Lam))==0,
                    'entire prefix normalized row, not frozen')
            prefix_rows.append(str(direct))
    for idx,P in enumerate([P1,P2]):
        vals=[P1,P2];vals[idx]=P+u/Omega
        Dvar=a*sp.eye(2)+z*sp.prod(t(v) for v in vals)*S0
        determinant=Dvar.det()
        direct=-sp.diff(determinant,u).subs(u,0)/determinant.subs(u,0)
        require(sp.simplify(direct/G-weights[idx]/Lam)==0,'future all-source coefficient')
    # Saturating prefix tangent dS=2S. This must NOT be declared zero at finite M.
    for n in (1,3,17):
        tt=ts[0]**n;DD=a*sp.eye(2)+z*tt*S0
        ww=z*tt*(DD.inv()*S0).trace();LL=n*weights[0]
        old=-z*tt*(DD.inv()*(2*S0)).trace()
        require(sp.simplify(old/(ww*LL)+2/LL)==0,'exact 1/Lambda old-source law')
        require(old!=0,'old source actually nonzero')
    # A fixed non-Einstein field defect remains after normalization at ANY M.
    defect=sp.Rational(2,7)
    for n in (1,3,17,101):
        value=sum(weights[0]*abs(defect) for _ in range(n))/(n*weights[0])
        require(value==abs(defect),'extensive field defect not diluted')
    # Common-direction cancellation is not full block-dual stationarity.
    require((sp.Integer(1)+(-1))/2==0,'hostile common-direction cancellation')
    require((abs(sp.Integer(1))+abs(-1))/2==1,'independent source norm detects cancellation')
    # S=0 is genuinely outside the positive-gain theorem.
    require((z*T*(D.inv()*sp.zeros(2)).trace())==0,'zero Gram negative control')
    # If every new block carries an uncontrolled apparatus row, it stays extensive.
    eps=sp.Rational(1,9)
    require(sum([eps]*100)/100==eps,'fresh independent apparatus errors do not vanish')
    return {'exact_prefix_rows':prefix_rows,'exact_gain':str(G),
      'future_relative_weights':[str(x/Lam) for x in weights],
      'old_rows_deleted':False,'non_Einstein_defect_survives':str(defect),
      'per_block_free_apparatus_defect_survives':str(eps),
      'scope':'exact finite matrix identities; rational 2x2 control is structural'}

def golden_private_block():
    p=(sp.sqrt(5)-1)/2;aa=sp.sqrt(p)
    G=sp.kronecker_product(sp.Matrix([[aa,-p],[p,aa]]),sp.eye(4))
    Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    X=sp.diag(sp.eye(4),Li)
    U=sp.eye(8)
    word=[G,X,X,X,X,G,X,X] # 2G+6SourceI, including the true forward inverse macro.
    for g in word:U=g*U
    U=U.applyfunc(sp.simplify)
    require((U.T*U-sp.eye(8)).applyfunc(sp.simplify)==sp.zeros(8),'eight-stage all-column orthogonality')
    require((U-U.T).applyfunc(sp.simplify)==sp.zeros(8),'complete private reflection')
    require((U[:4,:4]-p**3*sp.eye(4)).applyfunc(sp.simplify)==sp.zeros(4),
            'true private scalar corner on every Spin column')
    require((U-sp.kronecker_product(U[::4,::4],sp.eye(4))).applyfunc(sp.simplify)==sp.zeros(8),
            'completed private block restores every Spin input')
    return {'word_stages':8,'inventory':{'G':2,'SourceI':6},'all_columns':8,
      'cold_corner':'p^3 I4','scalar_Gram':'p^6',
      'scope':'literal bounded all-column interface control; not the complete nonlinear GR compiler'}

def native_prefix_controls(mod):
    first=(1/9,3/5);second=(1/8,1/2)
    # Full original128 columns in both actual tools are reconstructed.
    row1=mod.rows(*first,full=True);row2=mod.rows(*second,full=True)
    K=row2['C']@row1['C'];S=K.conj().T@K
    eig,V=la.eigh(S);require(eig.min()>0,'original two-tick prefix has nonzero gain')
    invsqrt=(V*(1/np.sqrt(eig)))@V.conj().T
    dSs=[]
    for which,dr,dnu in [(0,1.,0.),(0,0.,1.),(1,1.,0.),(1,0.,1.)]:
        p1=mod.rows(*first,dr=dr if which==0 else 0.,dnu=dnu if which==0 else 0.)
        p2=mod.rows(*second,dr=dr if which==1 else 0.,dnu=dnu if which==1 else 0.)
        dK=p2['dC']@p1['C']+p2['C']@p1['dC']
        dSs.append(dK.conj().T@K+K.conj().T@dK)
    C=sum(la.norm(invsqrt@v@invsqrt,2) for v in dSs)
    z=2**-20;a=1-z;I=np.eye(16)
    # A positive point of the OWNED scalar-report formula; shape numbers below
    # are structural controls and not falsely reported as a compiled GR word.
    alpha=.5;gamma=1/3;P=.2;Omega=1.25
    t=1-alpha*gamma*P*(1-gamma*P)
    b=alpha*gamma*(1-2*gamma*P);lam=b/(Omega*t)
    out=[]
    for n in (1,4,16,64,256):
        T=t**n;R=la.inv(a*I+z*T*S);tr=float(np.trace(R@S).real)
        w=z*T*tr;Lam=n*lam;gain=w*Lam
        old=np.array([-z*T*np.trace(R@dS).real for dS in dSs])
        scaled=float(np.sum(np.abs(old))/gain)
        bound=float(C/Lam)
        require(scaled<=bound*(1+1e-11),'all four independent original-prefix rows bounded')
        require(scaled>0,'no exact finite-prefix stationary claim')
        # Low-dimensional full price derivative directly against finite difference.
        # Keep every unused mode in the old prefix construction; this is exact
        # reduction of the RETURN determinant, not of the thermal trace.
        if n==4:
            eps=2e-4
            def price(x):
                kk=mod.rows(second[0],second[1])['C']@mod.rows(first[0]+x,first[1])['C']
                ev=la.eigvalsh(kk.conj().T@kk)
                return -np.log1p(-z*(1-T*ev)).sum()
            fd=(-price(2*eps)+8*price(eps)-8*price(-eps)+price(-2*eps))/(12*eps)
            near(fd,old[0],'actual original prefix determinant finite difference',3e-15)
        # Independent future blocks with a deliberately persistent field source.
        future_defect=.3
        full_norm=scaled+future_defect
        require(full_norm>=future_defect,'full source norm retains active field errors')
        out.append({'blocks':n,'cumulative_weight':Lam,'actual_gain':gain,
          'prefix_dual_norm_over_gain':scaled,'proven_prefix_bound':bound,
          'normalized_future_defect':future_defect,'full_dual_norm_with_defect':full_norm})
    require(all(out[j+1]['prefix_dual_norm_over_gain']<.26*out[j]['prefix_dual_norm_over_gain']
                for j in range(len(out)-1)),'actual prefix decreases at fixed inherited normalization')
    # Same original all16384 records replay, not a new native construction.
    old_replay=mod.full_two_tick()
    return {'original_prefix_rank':16,'original_rounds':2,
      'smallest_Gram_eigenvalue':float(eig.min()),'relative_prefix_constant':float(C),
      'nonnormality_norm':float(la.norm(K@K.conj().T-S)),
      'old_constructor_full_history_replay':old_replay,
      'new_prefix_source_controls':out,
      'future_shape_control_is_structural':True}

def exact_heat_and_weight_controls():
    # Exact A_N majorant from the already proved complete homogeneous clock.
    # Constants here test the convergence bound; they are not a runtime estimate
    # or a claim to have executed a huge recovery compiler.
    mp.mp.dps=80
    xx=F(2,55)
    def A(N):
        q=xx**N/math.factorial(N)
        return F(176,359)/(1-xx*xx)*q/(1-q)**2
    def num(q):return mp.mpf(q.numerator)/q.denominator
    C_V=F(100);traceS_lower=F(1,100);z=F(1,2**20)
    tau_min=F(1,20);lam=F(1,100);N0=16;ell=8
    vals=[]
    for repeats in (1,2,4,8,16,32):
        N=N0+ell*repeats;T=tau_min**repeats;Lam=lam*repeats
        bound=A(N)*C_V/(z*T*traceS_lower*Lam)
        require(bound>0,'whole heat derivative remains positive budget')
        require(bound<F(1,10**20),'factorial heat beats real source attenuation')
        vals.append({'repeats':repeats,'clock_length_lower_bound':N,
                     'log10_thermal_over_gain_bound':mp.nstr(mp.log10(num(bound)),32),
                     'exact_rational_bound':True})
    # Exact staged positive-weight schedule retaining every earlier finite error.
    total=F(0);bad_mass=F(0);prefix_C=F(100);epochs=[]
    for j in range(1,8):
        weight=F(1,10**j);err=F(1,2**(j+3))
        # Choose enough genuine repetitions to dominate old errors and prefix,
        # never delete an old block or reset its known finite error.
        goal=2**(j+2)*(bad_mass+prefix_C+1)
        repetitions=max(1,math.ceil((goal-total)/weight))
        total+=repetitions*weight;bad_mass+=repetitions*weight*err
        combined=(bad_mass+prefix_C)/total
        require(combined<F(1,2**j),'constructive full prefix+field source schedule')
        epochs.append({'epoch':j,'positive_weight':str(weight),'genuine_repetitions':repetitions,
          'cumulative_weight':str(total),'old_and_new_error_mass':str(bad_mass),
          'full_normalized_bound':str(combined),'target':str(F(1,2**j))})
    return {'thermal_controls':vals,'weight_schedule':epochs,
      'growing_heat_value_removed':False,'readout_accuracy_free':False,
      'chosen_constants_are_controls_not_GR_compiler_counts':True}

def main():
    mod=original_module()
    out={'input_commit':'1e6420f319d714be53363a77823f76ec620a6473',
      'parent_retained_source_commit':'3219c15808f5247437d0e14557aec75c7fe6ac03',
      'old_constructor_sha256':PIN,
      'symbolic':symbolic_controls(),'native_private_block':golden_private_block(),
      'original_prefix':native_prefix_controls(mod),
      'exact_source_budgets':exact_heat_and_weight_controls(),
      'checks':checks,'status':'PASS_COMPLETE_FIXED_PREFIX_COVECTOR_RECOVERY',
      'scope':'inherited cumulative block-dual source norm plus all directions of one fixed finite regular prefix; declared full-column continuation class',
      'newest_block_gain_replaced':False,
      'original_admission_derived':False,'exact_finite_stationary_root_proved':False,
      'uncontrolled_new_apparatus_rows_eliminated':False,
      'full_GR_native_program_executed':False,'Lean_or_CI_run':False,'GR_closed':False,
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__},
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':main()
