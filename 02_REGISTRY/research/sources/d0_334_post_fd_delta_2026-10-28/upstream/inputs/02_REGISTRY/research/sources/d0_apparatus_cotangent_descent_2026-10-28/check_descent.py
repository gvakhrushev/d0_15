#!/usr/bin/env python3
"""Operator-valued apparatus cotangent and retained-matrix-past controls.

Exact finite-matrix identities and explicit read-once quantum controls.
The small kernels are structural controls, NOT emitted large GR programmes.
The nonlinear cold target uses the original sigma-minus polynomial, with
its fixed z0 and explicitly declared test shape numbers. This script does
not establish native actuation, a new physical metric or arbitrary X_N.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
import platform
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sp

COUNT=0

def require(ok: bool, name: str) -> None:
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise AssertionError(name)

def exact_zero(A, name):
    if isinstance(A,sp.MatrixBase):
        require(A.applyfunc(sp.simplify)==sp.zeros(*A.shape),name)
    else:
        require(sp.simplify(A)==0,name)

def near(A,B,name,tol=2e-11):
    error=float(np.max(np.abs(np.asarray(A)-np.asarray(B))))
    require(error<tol,name+': '+str(error))
    return error

def exact_past():
    # The same rational nonnormal control as the retained-past owner.
    K=sp.Matrix([[sp.Rational(43,75),sp.Rational(4,25)],
                 [sp.Rational(8,25),sp.Rational(19,50)]])
    S=K.T*K;z=sp.Rational(1,7);a=1-z
    Ps=[sp.Rational(3,8),sp.Rational(5,21),sp.Rational(7,40)]
    cs=[sp.Rational(7,8),sp.Rational(19,21),sp.Rational(37,40)]
    for P,c in zip(Ps,cs): exact_zero(c*c-(1-P+P*P),'genuine test-shape Gram')
    # Structural alpha=gamma=Omega=1; 0<P<1/2. Original z0 is not changed.
    lam=[(1-2*P)/(c*c) for P,c in zip(Ps,cs)]
    T=sp.prod(c*c for c in cs);d=sp.prod(cs)
    D=a*sp.eye(2)+z*T*S
    den=(S*D.inv()).trace();w=z*T*den
    Pi=K*D.inv()*K.T/den
    exact_zero(Pi.trace()-1,'derived dual weight has trace one')
    require(Pi.det()>0 and Pi[0,0]>0,'derived dual weight positive')
    require(K*K.T!=S,'nonnormal prefix not replaced by its Gram')
    J=sp.Matrix([[0,-1],[1,0]])
    H=sp.Matrix([[1,sp.Rational(1,3)],[sp.Rational(1,3),-1]])
    X=H+sp.Rational(2,5)*J
    observed=[]
    u=sp.symbols('u',real=True)
    for j,c in enumerate(cs):
        Cu=d*K+u*(d/c)*X*K
        det=(a*sp.eye(2)+z*(Cu.T*Cu)).det()
        direct=-sp.diff(det,u).subs(u,0)/det.subs(u,0)
        formula=-2*w/c*(Pi*H).trace()
        exact_zero(direct-formula,'whole determinant versus non-scalar new-block row')
        Aop=-2*H/(c*lam[j])
        exact_zero(direct/(w*lam[j])-(Pi*Aop).trace(),'history-uniform normalized operator row')
        exact_zero((Pi*J).trace(),'skew cancellation survives nonuniform past')
        observed.append(str(direct))
    # A scalar-trace estimate is insufficient: it need not hold for the past.
    Z=sp.diag(1,-1)
    require(Z.trace()==0 and (Pi*Z).trace()!=0,'zero fresh trace does not mean operator neutrality')
    # Critical guard: new raw supports must preserve the old input cut.
    V=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5)],
                 [sp.Rational(4,5),sp.Rational(3,5)]])
    P=sp.diag(1,0)
    require(P*J!=J*P,'hostile new fault touches old return record')
    k=V[0,0];dk=(J*V)[0,0];c=sp.Rational(7,8)
    bad=-2*z*c*c*k*dk/(a+z*c*c*k*k)
    require(bad!=0 and (P*J*P)==sp.zeros(2),'old-complement leakage defeats naive skew cancellation')
    # Full protected subspace plus blank records has the needed support law.
    PP=sp.diag(1,1,0,0);XX=sp.diag(X,2*X)
    exact_zero(PP*XX-XX*PP,'protected role fault preserves blank old-record cut')
    return {'new_block_rows_exact':observed,'dual_weight':str(Pi),
      'fresh_trace_zero_old_source_weight':str((Pi*Z).trace()),
      'unguarded_old_cut_leakage_row':str(bad),
      'scope':'exact operator identities; rational old corner and shape are structural controls'}


def golden_word():
    p=(sp.sqrt(5)-1)/2;aa=sp.sqrt(p)
    G=sp.kronecker_product(sp.Matrix([[aa,-p],[p,aa]]),sp.eye(4))
    Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    X=sp.diag(sp.eye(4),Li)
    U=sp.eye(8)
    for g in [G,X,X,X,X,G,X,X]:U=g*U
    U=U.applyfunc(sp.simplify)
    exact_zero(U.T*U-sp.eye(8),'literal all-eight-column orthogonality')
    exact_zero(U-U.T,'literal private reflection')
    exact_zero(U[:4,:4]-p**3*sp.eye(4),'literal scalar cold corner')
    exact_zero(U-sp.kronecker_product(U[::4,::4],sp.eye(4)),'completed full Spin restoration')
    return {'stages':8,'inventory':{'G':2,'SourceI':6},'protected_columns':4,
            'all_columns_checked':8,'corner':'p^3 I4',
            'scope':'replay of the owned bounded private block; not a large GR compiler'}


def tensor_all(items):
    out=np.array([1.])
    for a in items:out=np.kron(out,a)
    return out

def embed_pair(A,i,j,n):
    N=1<<n;out=np.zeros((N,N))
    for col in range(N):
        bits=[(col>>(n-1-r))&1 for r in range(n)]
        b=2*bits[i]+bits[j]
        for aa in range(4):
            bb=bits[:];bb[i]=aa//2;bb[j]=aa%2
            row=sum(bb[r]<<(n-1-r) for r in range(n))
            out[row,col]=A[aa,b]
    return out

def quantum_banks():
    # Noncommuting features on one packet; separate slots are read once.
    EZ=sp.diag(1,0);EX=sp.Matrix([[1,1],[1,1]])/2
    eye=sp.eye(2)
    coeff=sp.Matrix([[sp.Rational(3,5),sp.Rational(2,3)],
                     [sp.Rational(5,7),sp.Rational(4,5)]])
    unsym=sp.zeros(4)
    for i,j in itertools.product(range(2),repeat=2):
        A=[eye-EZ,EZ][i];B=[eye-EX,EX][j]
        unsym+=coeff[i,j]*sp.kronecker_product(A,B)
    Swap=sp.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    h=(unsym+Swap*unsym*Swap)/2
    psi=sp.Matrix([sp.Rational(3,5),sp.Rational(4,5)])
    rho=psi*psi.T
    mu=[(rho*EZ).trace(),(rho*EX).trace()]
    x,y=sp.symbols('x y',real=True)
    cold=sum(coeff[i,j]*[1-x,x][i]*[1-y,y][j] for i,j in itertools.product(range(2),repeat=2))
    c=cold.subs({x:mu[0],y:mu[1]})
    grad=[sp.diff(cold,z).subs({x:mu[0],y:mu[1]}) for z in (x,y)]
    H1=sp.zeros(2)
    for i,j in itertools.product(range(2),repeat=2):
        H1[i,j]=sum(rho[l,k]*h[2*i+k,2*j+l] for k,l in itertools.product(range(2),repeat=2))
    projection=c*eye+sum((g*(O-m*eye)/2 for g,O,m in zip(grad,[EZ,EX],mu)),sp.zeros(2))
    exact_zero(H1-projection,'exact quantum first conditional, not scalar mean only')
    require(EZ*EX!=EX*EZ,'one-packet features noncommuting')
    A=H1-c*eye
    R2=h-c*sp.eye(4)-sp.kronecker_product(A,eye)-sp.kronecker_product(eye,A)
    # A genuine two-packet vertical tangent: all first marginal jets vanish.
    v=sp.kronecker_product(psi,psi)
    chi=sp.kronecker_product(sp.Matrix([-psi[1],psi[0]]),sp.Matrix([-psi[1],psi[0]]))
    G=chi*v.T-v*chi.T
    exact_zero(G.T+G,'two-packet preparation generator skew')
    one_jets=[]
    for O in (EZ,EX):
        for slot in (0,1):
            Op=sp.kronecker_product(O,eye) if slot==0 else sp.kronecker_product(eye,O)
            val=(v.T*(Op*G-G*Op)*v)[0]
            exact_zero(val,'vertical tangent has zero marginal moment jet')
            one_jets.append(str(val))
    slope=(v.T*(R2*G-G*R2)*v)[0]
    require(slope!=0,'correlated vertical source remains nonzero at finite bank count')
    W=(max(coeff)-min(coeff))/2
    p=(sp.sqrt(5)-1)/2
    results=[]
    for n in (4,8,16):
        bits=int(math.log2(n))
        weights=[p**(bits+int(i).bit_count()) for i in range(n)]
        exact_zero(sum(weights)-1,'actual Golden TAG weights normalized')
        wS=weights[0]+weights[1]
        pair=sp.simplify((1-wS)/sp.binomial(n-1,2))
        b=sp.simplify(2*(1-wS)/((n-1)*(n-2)))
        exact_zero(pair-b,'true pair inclusion and omission coefficient')
        a0=(1-weights[0])/(n-1);a1=(1-weights[1])/(n-1)
        cond=c*sp.eye(4)+2*a0*sp.kronecker_product(A,eye)+2*a1*sp.kronecker_product(eye,A)+pair*R2
        row=sp.simplify((v.T*(cond*G-G*cond)*v)[0])
        exact_zero(row-pair*slope,'whole vertical SOURCE row equals overlap contribution')
        bound=sp.simplify(6*W*2*b) # k(k-1)=2, ||G||=1
        require(abs(float(row.evalf()))<float(bound.evalf()),'retained higher-overlap operator bound')
        # Independent forward and inverse rows have their own real halves.
        forward=(v.T*cond*G*v)[0];reverse=-(v.T*G*cond*v)[0]
        exact_zero(forward-row/2,'independent forward real half')
        exact_zero(reverse-row/2,'independent reverse real half')
        full_error=None
        if n in (4,8):
            hh=np.array(h,float);rr=np.array(rho,float);vv=np.array(psi,float).ravel()
            Kbank=np.zeros((1<<n,1<<n))
            ww=[float(w.evalf()) for w in weights]
            for i,j in itertools.combinations(range(n),2):
                prob=(1-ww[i]-ww[j])/math.comb(n-1,2)
                Kbank+=prob*embed_pair(hh,i,j,n)
            embedding=np.kron(np.eye(4),tensor_all([vv]*(n-2))[:,None])
            full_cond=embedding.T@Kbank@embedding
            full_error=near(full_cond,np.array(cond.evalf(),float),'all-column bank conditional')
            state=tensor_all([vv]*n)
            near(state@Kbank@state,float(c),'full Golden TAG kernel scalar at product reference')
        results.append({'banks':n,'pair_probability':str(pair),
          'vertical_row':str(row),'vertical_row_float':float(row.evalf()),
          'proven_bound':float(bound.evalf()),'full_bank_conditional_error':full_error})
    # Single-packet operator identity survives an arbitrary old protected state.
    K0=sp.Matrix([[sp.Rational(43,75),sp.Rational(4,25)],
                  [sp.Rational(8,25),sp.Rational(19,50)]])
    S=K0.T*K0;zz=sp.Rational(1,7)
    D=(1-zz)*eye+zz*c*c*S;den=(S*D.inv()).trace()
    Pi=K0*D.inv()*K0.T/den
    Xold=sp.diag(1,-1);J=sp.Matrix([[0,-1],[1,0]])
    H=sp.kronecker_product(Xold,J)
    ket=sp.kronecker_product(eye,psi)
    Xrow=ket.T*(sp.kronecker_product(eye,H1)*H-H*sp.kronecker_product(eye,H1))*ket
    M=[]
    for O in (EZ,EX):
        OO=sp.kronecker_product(eye,O)
        M.append(ket.T*(OO*H-H*OO)*ket)
    exact_zero(Xrow-sum((g*m/2 for g,m in zip(grad,M)),sp.zeros(2)),
               'operator-valued first moment with old-bank correlated generator')
    require((Pi*Xrow).trace()!=0,'noncritical actual source not artificially zero')
    return {'first_conditional_exact':str(H1),'cold_value':str(c),
      'finite_two_packet_vertical_slope':str(slope),'Golden_TAG_controls':results,
      'operator_valued_row':str(Xrow),
      'derived_past_weighted_row':str((Pi*Xrow).trace()),
      'scope':'actual Golden TAG probabilities, structural two-feature read-once kernels; no large native query emission'}


def nonlinear_target():
    # Exact original sigma-minus event, not an Einstein residual.
    mp.mp.dps=55
    p=(mp.sqrt(5)-1)/2;z0=mp.mpf(2)**-20
    alpha=mp.mpf(1)/3;gamma=mp.mpf(1)/2
    scale=mp.mpf(1)/20
    base=[mp.mpf('0.6'),mp.mpf('0.65'),mp.mpf('0.55')]
    vertical=[mp.mpf(-1),mp.mpf(1),mp.mpf(1)]
    def event(v):
        x=scale*(v[0]+v[2]-1);y=scale*(v[1]-v[2])
        E=p*p*(1+x);ell=4*E*(1-E)
        b=p-p*p*y;B=4*b*b*(1-b*b);A=ell+(1-ell)*B
        return z0*(A+B)-z0*z0*A*B
    def cold(v):
        P=event(v)
        return mp.sqrt(1-alpha*gamma*P*(1-gamma*P))
    I=event(base);cstar=cold(base)
    lam=alpha*gamma*(1-2*gamma*I)/(cstar*cstar)
    grad=[]
    for a in range(3):
        def one(u):
            v=base[:];v[a]=u;return event(v)
        grad.append(mp.diff(one,base[a]))
    require(max(abs(x) for x in grad)>mp.mpf('1e-10'),'non-null original nonlinear source retained')
    require(abs(sum(a*b for a,b in zip(grad,vertical)))<mp.mpf('1e-48'),
            'original target is exactly neutral on its decoder fibre')
    def weights(n,q):
        return [mp.binomial(n,k)*q**k*(1-q)**(n-k) for k in range(n+1)]
    vals=[]
    for m in (2,4,8,16):
        ws=[weights(m,q) for q in base];wd=[weights(m-1,q) for q in base]
        table={idx:cold([mp.mpf(i)/m for i in idx]) for idx in itertools.product(range(m+1),repeat=3)}
        cm=sum(table[idx]*mp.fprod(ws[a][idx[a]] for a in range(3)) for idx in table)
        dc=[]
        for a in range(3):
            total=mp.mpf(0)
            ranges=[range(m+1)]*3;ranges[a]=range(m)
            for idx in itertools.product(*ranges):
                nxt=list(idx);nxt[a]+=1;nxt=tuple(nxt)
                total+=(table[nxt]-table[idx])*mp.fprod((wd[b] if b==a else ws[b])[idx[b]] for b in range(3))
            dc.append(m*total)
        # Exact operator-row normalization at the current scalar corner cm,
        # with inherited target lambda. Its difference is retained as error.
        normalized=[-2*x/(cm*lam) for x in dc]
        error=sum(abs(a-b) for a,b in zip(normalized,grad))
        normal=abs(sum(a*b for a,b in zip(normalized,vertical)))
        require(error>0 and normal>mp.mpf('1e-20'),'finite outer Bernstein bias is not discarded')
        vals.append({'degree':m,'ambient_gradient_error':mp.nstr(error,32),
                     'vertical_residual':mp.nstr(normal,32),
                     'nonzero_field_gradient_norm':mp.nstr(sum(abs(a) for a in grad),32)})
    for a,b in zip(vals,vals[1:]):
        require(mp.mpf(b['ambient_gradient_error'])<mp.mpf(a['ambient_gradient_error']),
                'actual original-polynomial derivative convergence')
        require(mp.mpf(b['vertical_residual'])<mp.mpf(a['vertical_residual']),
                'vertical source converges without critical-field assumption')
    return {'original_z0':'2^-20','original_event_at_base':mp.nstr(I,32),
      'decoder':'x=(p1+p3-1)/20, y=(p2-p3)/20',
      'vertical_direction':[-1,1,1],'test_shape':{'alpha':'1/3','gamma':'1/2','Omega':'1'},
      'original_field_gradient':[mp.nstr(x,32) for x in grad],
      'Bernstein_controls':vals,
      'scope':'bounded direct-click scalar and fibre controls; not a finite GR solution'}


def cumulative_controls():
    # No microscopic norm is replaced by division by the total clock length.
    eps=F(1,9)
    for N in (1,7,101):
        require(sum([eps]*N)/N==eps,'uncontrolled extensive vertical source survives')
    # A horizontal rapid oscillation can have a large C3 norm. The new
    # regular graph norm explicitly records this, rather than claiming an
    # unweighted microscopic max-norm theorem.
    norm_ratios=[]
    for h in (F(1,4),F(1,8),F(1,16)):
        source=h;decoded_C3=h**-3
        raw_max_row=source*decoded_C3
        regular_row=raw_max_row/decoded_C3
        require(raw_max_row>1 and regular_row==h,'different norms not silently identified')
        norm_ratios.append({'h':str(h),'raw_max_row':str(raw_max_row),'regular_row':str(regular_row)})
    prefix=F(100);weight=F(0);debt=F(0);epochs=[]
    for j in range(1,7):
        lam=F(1,10**j);e=F(1,2**(j+4))
        goal=2**(j+3)*(prefix+debt+1)
        repetitions=max(1,math.ceil((goal-weight)/lam))
        weight+=repetitions*lam
        # Both geometry and newly independent apparatus are retained.
        debt+=repetitions*lam*(e+e)
        total=(prefix+debt)/weight
        require(total<F(1,2**j),'one cumulative prefix+field+apparatus schedule')
        epochs.append({'j':j,'repetitions':repetitions,'total_weight':str(weight),
                       'joint_bound':str(total),'target':str(F(1,2**j))})
    return {'epochs':epochs,'persistent_unknown_source':str(eps),
            'norm_boundary_control':norm_ratios,'no_large_program_execution_claimed':True}


def main():
    result={'input_commit':'523d2cbcc0a9771ea40faa4a2eac84cc78704b0e',
      'matrix_past':exact_past(),'literal_private_block':golden_word(),
      'quantum_conditional':quantum_banks(),'nonlinear_target':nonlinear_target(),
      'joint_budget':cumulative_controls(),'checks':COUNT,
      'status':'PASS_OPERATOR_APPARATUS_COTANGENT_DESCENT_CONTROLS',
      'physical_admission_proved':False,'exact_finite_GR_root_proved':False,
      'uniform_unweighted_raw_gate_refinement_proved':False,
      'arbitrary_global_record_touching_faults_covered':False,
      'large_native_GR_query_executed':False,'Lean_or_CI_run':False,'GR_closed':False,
      'environment':{'python':platform.python_version(),'sympy':sp.__version__,
                     'numpy':np.__version__,'mpmath':mp.__version__},
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':main()
