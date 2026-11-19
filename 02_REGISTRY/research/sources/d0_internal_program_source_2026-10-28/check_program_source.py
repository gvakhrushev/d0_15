#!/usr/bin/env python3
"""Closed programme selection: literal child words and their true source charts.

The children are original G/CX/SourceI words. Their controlled direct sum is
an explicitly declared finite processor, NOT a proof of native controlled
actuation. All code branches and input columns remain in its full operators.
"""
from __future__ import annotations
import hashlib
import json
import math
import platform
from collections import Counter
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy.linalg as la
import sympy as s
from sympy.polys.matrices import DomainMatrix

COUNT = 0

def require(ok: bool, name: str) -> None:
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise ArithmeticError(name)


def near(a, b, name: str, tol: float = 1e-11) -> float:
    error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(error < tol, f'{name}: {error}')
    return error


def native_children():
    p=(s.sqrt(5)-1)/2
    aa=s.sqrt(p)
    field=s.QQ.algebraic_field(aa)
    def dm(M): return DomainMatrix.from_Matrix(s.Matrix(M)).convert_to(field)
    I=dm(s.eye(32))
    G=s.Matrix([[aa,-p],[p,aa]])
    Li=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    SI=s.diag(s.eye(4),Li)
    CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    def gate(op,wires):
        require(4 not in wires,'oldRIGHT not addressed')
        require(op!='SourceI' or wires==(0,2,3),'true SourceI frame')
        local={'G':G,'CX':CX,'SourceI':SI}[op]
        out=s.zeros(32); k=len(wires)
        for col in range(32):
            bits=[(col>>(4-j))&1 for j in range(5)]
            idx=sum(bits[w]<<(k-1-u) for u,w in enumerate(wires))
            for rowlocal in range(1<<k):
                x=local[rowlocal,idx]
                if x==0: continue
                bb=bits[:]
                for u,w in enumerate(wires): bb[w]=(rowlocal>>(k-1-u))&1
                row=sum(bb[u]<<(4-u) for u in range(5))
                out[row,col]=x
        ans=dm(out)
        require((ans.transpose().matmul(ans)-I).is_zero_matrix,'full32 primitive')
        return ans
    def swap(a,b): return [('CX',(a,b)),('CX',(b,a)),('CX',(a,b))]
    si=('SourceI',(0,2,3)); rr=swap(0,1)
    def inv(word):
        out=[]
        for op,w in word[::-1]:
            if op=='CX': out.append((op,w))
            elif op=='SourceI': out.extend([si]*3)
            else:
                r=[] if w[0]==0 else swap(w[0],0)
                out += r+[si,si,('G',(0,)),si,si]+r
        return out
    routed=rr+[('G',(0,))]+rr
    query=inv(routed)+rr+[si,si]+rr+routed
    v=[('G',(1,))]
    words=[v+inv(v)+query,v+query+inv(v)]
    require(len(query)==26 and all(len(w)==38 for w in words),'literal child durations')
    inventory={'G':4,'CX':24,'SourceI':10}
    require(all(dict(Counter(g[0] for g in w))==inventory for w in words),'literal matched inventory')
    cache={g:gate(*g) for w in words for g in w}
    W=[]
    for word in words:
        endpoint=I
        for g in word: endpoint=cache[g].matmul(endpoint)
        require((endpoint.transpose().matmul(endpoint)-I).is_zero_matrix,'whole child unitarity')
        W.append(endpoint)
    c=p**3; u=2*p*s.sqrt(p)
    expected=[s.kronecker_product(s.eye(2),s.Matrix([[c,u],[u,-c]]),s.eye(8)),
              s.kronecker_product(s.eye(2),s.diag(1,-1),s.eye(8))]
    for w,e in zip(W,expected):
        require((w-dm(e)).is_zero_matrix,'literal full32 endpoint')
        require((w.matmul(w)-I).is_zero_matrix,'child full reflection')
    P=dm(s.diag(*([1]*8+[0]*24)))
    require((P.matmul(W[0]).matmul(P)-P.scalarmul(field.from_sympy(c))).is_zero_matrix,'actual child corner c')
    require((P.matmul(W[1]).matmul(P)-P).is_zero_matrix,'actual child corner1')
    # Full64 processor stage product, no unstated native controlled-gate claim.
    Z=dm(s.zeros(32))
    I64=dm(s.eye(64))
    combined=I64
    for g0,g1 in zip(*words):
        a,b=cache[g0],cache[g1]
        block=a.hstack(Z).vstack(Z.hstack(b))
        combined=block.matmul(combined)
    controlled=W[0].hstack(Z).vstack(Z.hstack(W[1]))
    require((combined-controlled).is_zero_matrix,'full64 controlled schedule')
    require((combined.transpose().matmul(combined)-I64).is_zero_matrix,'full64 exact orthogonality')
    Code=dm(s.diag(*([1]*32+[0]*32)))
    require((combined.matmul(Code)-Code.matmul(combined)).is_zero_matrix,'programme record retained')
    num=[np.array(e.evalf(17),dtype=complex) for e in expected]
    ops=[[np.array(cache[g].to_Matrix().evalf(17),dtype=complex) for g in word] for word in words]
    return num,ops,{'child_raw_stages':38,'child_inventory':inventory,'child_columns':32,
        'controlled_scheduled_slots':38,'controlled_columns':64,'protected_rank':8,
        'native_controlled_primitive_admission_proved':False,
        'controlled_physical_duration_identified':False,
        'original_oldRIGHT_retained':True}


def exact_chart():
    a,z,c,R=s.symbols('a z c R',positive=True)
    q=s.symbols('q',nonnegative=True)
    b=c+(1-c)*q
    J=-R*s.log(1-z+z*b*b)
    w=R*z*c*c/(1-z+z*c*c)
    jq=s.simplify(s.diff(J,q).subs(q,0))
    ja=J.subs(q,s.sin(a)**2)
    require(s.simplify(s.diff(ja,a).subs(a,0))==0,'amplitude first derivative zero')
    require(s.simplify(s.diff(ja,a,2).subs(a,0)+4*(1-c)*w/c)==0,'true negative second source')
    forward=-R*s.log(1-z+z*c*c*s.cos(a)**2)
    require(s.simplify(s.diff(forward,a,2).subs(a,0)-2*w)==0,'fixed-cut forward preparation has different second source')
    require(s.simplify(jq+2*(1-c)*w/c)==0,'probability chart first source')
    effect=(1-b)/2
    require(s.simplify(jq/s.diff(effect,q)-4*w/c)==0,'report-normalized source recovered')
    # The q derivative is one-sided at the pure-programme boundary.
    p=(s.sqrt(5)-1)/2
    require(s.simplify((1-p**3)/2-p*p)==0,'native report gap p squared')
    return {'amplitude_first_source':'0',
            'amplitude_second_source':'-4*(1-c)*w/c',
            'one_sided_probability_source':'-2*(1-c)*w/c',
            'report_normalized_source':'4*w/c',
            'forward_only_fixed_cut_amplitude_second_source':'2*w',
            'programme_ray_is_not_a_minimum_if_c_lt_1':True}


def full_cold_programme(W,ops):
    U=la.block_diag(*W)
    i=np.eye(32,dtype=complex)[:,:8]
    E0=np.vstack([i,np.zeros_like(i)])
    p=(math.sqrt(5)-1)/2; c=p**3; z=2**-20
    maxerr=0.; maxferr=0.
    for a in (0.,.07,.23,.61,math.pi/2):
        for phase in (0.,.37):
            E=np.vstack([math.cos(a)*i,np.exp(1j*phase)*math.sin(a)*i])
            C=E.conj().T@U@E
            expected=(c+(1-c)*math.sin(a)**2)*np.eye(8)
            maxerr=max(maxerr,near(C,expected,'all protected input columns; true moving cut'))
            rot=np.array([[math.cos(a),-np.exp(-1j*phase)*math.sin(a)],
                          [np.exp(1j*phase)*math.sin(a),math.cos(a)]])
            Rt=np.kron(rot,np.eye(32))
            near(E0.conj().T@Rt.conj().T@U@Rt@E0,C,'fixed-cut complete programme echo is same compression')
            near(E0.conj().T@U@Rt@E0,math.cos(a)*c*np.eye(8),'one-sided preparation is not same programme echo')
            P=E@E.conj().T
            F=P@U.conj().T@(np.eye(64)-P)@U@P
            spectrum=la.eigvalsh((F+F.conj().T)/2)
            J=-np.log1p(-z*spectrum).sum()
            cold=1-(c+(1-c)*math.sin(a)**2)**2
            maxferr=max(maxferr,near(J,-8*math.log1p(-z*cold),'full64 determinant retains complement',1e-17))
    # Arbitrary code-changing, potentially work/protected-entangled tangent.
    rng=np.random.default_rng(281028)
    for _ in range(4):
        B=(rng.normal(size=(32,32))+1j*rng.normal(size=(32,32)))/30
        H=np.block([[np.zeros((32,32)), -B.conj().T],[B,np.zeros((32,32))]])
        dE=H@E0
        dC=dE.conj().T@U@E0+E0.conj().T@U@dE
        near(dC,np.zeros((8,8)),'entangled programme-changing preparation tangent')
        near(E0.conj().T@H@U@E0,np.zeros((8,8)),'off-code endpoint fault insertion')
    # Changes within the selected code branch remain genuine QUERY sources.
    L=np.kron(np.kron(np.eye(2),np.array([[0.,-1.],[1.,0.]])),np.eye(8))
    dU=la.block_diag(L@W[0]-W[0]@L,np.zeros((32,32)))
    dC=E0.conj().T@dU@E0
    u=math.sqrt(1-c*c)
    near(dC,-2*u*np.eye(8),'same-code law-change not removed')
    D=(1-z+z*c*c)*np.eye(8)
    source=-z*np.trace(la.solve(D,c*dC+c*dC.conj().T)).real
    w=8*z*c*c/(1-z+z*c*c)
    near(source/w,4*u/c,'existing free-QUERY normal survives unchanged',1e-10)
    # Full clock endpoint spectrum; no giant scene matrix is diagonalized.
    N=len(ops[0]);beta=2*p*p
    def phaseheat(U):
        phases=np.angle(la.eigvals(U))
        vals=[1-math.cos((theta+2*math.pi*k)/N) for theta in phases for k in range(N)]
        return 2*float(np.exp(-beta*np.asarray(vals)).sum())
    Zchildren=sum(phaseheat(wi) for wi in W)
    Zprogram=phaseheat(U)
    near(Zprogram,Zchildren,'all programme thermal sectors retained',1e-9)
    near(math.log(Zprogram)/beta-math.log(phaseheat(W[0]))/beta,math.log(2)/beta,'paid programme heat baseline',1e-12)
    return {'corner_error':maxerr,'whole_return_error':maxferr,
        'same_code_QUERY_source':float(source),'same_code_QUERY_source_over_w':float(source/w),
        'bare_clock_modes_both_grades':2*N*64,
        'homogeneous_scene_modes_if_same_clock_assigned':425*N*64,
        'extra_bare_heat_baseline':math.log(2)/beta,
        'large_heat_matrix_diagonalized':False,
        'same_N_assigned_only_to_declared_controlled_comparison':True}


def matrix_past():
    mp.mp.dps=100
    p=(mp.sqrt(5)-1)/2;c=p**3; z=mp.mpf(2)**-20
    results=[]
    for small in ('0.3','1e-20','0'):
        K=mp.matrix([[mp.mpf('.5'),mp.mpf('.12')],[0,mp.mpf(small)]])
        S=K.T*K
        tr=S[0,0]+S[1,1];det=mp.det(S)
        for oldT in ('1','1e-50'):
            T=mp.mpf(oldT)
            def price(q):
                b=c+(1-c)*q
                x=z*T*b*b/(1-z)
                return -mp.log1p(x*tr+x*x*det) # common full baseline handled separately
            x=z*T*c*c/(1-z)
            w=(x*tr+2*x*x*det)/(1+x*tr+x*x*det)
            g=mp.diff(price,0);h=mp.diff(lambda a:price(mp.sin(a)**2),0,2)
            relative=abs(g/w+2*(1-c)/c)
            require(relative<mp.mpf('1e-80'),'arbitrary retained past first source')
            require(abs(h/w+4*(1-c)/c)<mp.mpf('1e-80'),'arbitrary retained past second source')
            # Finite source measured in the real effect change, not +/- amplitude.
            q=mp.mpf('1e-8')
            contrast=(price(q)-price(0))/(-q*(1-c)/2)/w
            require(abs(contrast-4/c)<mp.mpf('1e-5'),'effect-spaced finite contrast')
            results.append({'past_minimum_diagonal':small,'other_return_T':oldT,
                'w':mp.nstr(w,25),'q_source_over_w':mp.nstr(g/w,25),
                'amplitude_Hessian_over_w':mp.nstr(h/w,25),
                'report_finite_contrast_over_w':mp.nstr(contrast,25)})
    J0=-8*mp.log(1-z+z*c*c)
    fullw=8*z*c*c/(1-z+z*c*c)
    return {'cases':results,'literal_child_J_gap':mp.nstr(J0,30),
            'literal_program_amplitude_Hessian':mp.nstr(-4*(1-c)*fullw/c,30),
            'zero_normalized_gain_assumed':False}


def mixed_price_and_selection():
    # Classical randomized programmes and coherent initial programmes are
    # different preparations; neither is silently substituted for the other.
    c=.31;z=.17;n=3
    J0=-n*math.log(1-z+z*c*c)
    coherent_derivative=-2*n*z*c*(1-c)/(1-z+z*c*c)
    classical_expected_derivative=-J0
    require(abs(coherent_derivative-classical_expected_derivative)>1e-3,'different programme preparations give different source')
    # A one-sided feasible descent is not constrained minimum-stationarity.
    require(coherent_derivative<0 and classical_expected_derivative<0,'silent programme favoured in both controls')
    # Any finite task list gives zero coherent first tangent at a pure code.
    corners=np.array([.23,.51,.81])
    v=np.array([1.,0.,0.]);dv=np.array([0.,.3,-.4])
    dc=2*np.dot(v*dv,corners)
    require(dc==0,'first programme derivative is blind to task selection')
    # Semantic derivative may distinguish tasks even though the Hilbert pullback does not.
    require(corners[1]!=corners[0],'programme semantic map not immersion at pure code')
    return {'coherent_q_derivative':coherent_derivative,
            'classical_average_q_derivative':classical_expected_derivative,
            'pure_programme_zero_does_not_select_Einstein':True,
            'exact_minimum_claimed':False}



def reflection_stationary_class():
    """Return-only theorem. A nonconstant full heat source is NOT erased."""
    def components(C,K,z=.19):
        r=len(C); I=np.eye(r)
        B=la.sqrtm(I-C@C)
        U=np.block([[C,B],[B,-C]])
        D=(1-z)*I+z*K.conj().T@C@C@K
        M=K@la.inv(D)@K.conj().T
        G=-z*(C@M+M@C)
        Q=la.block_diag(G,np.zeros((r,r)))
        comm=U@Q-Q@U
        return U,D,M,G,comm
    # Exact rational checks avoid interpreting a tiny float as a critical point.
    C=s.diag(-1,0,1); B=s.diag(0,1,0)
    U=C.row_join(B).col_join(B.row_join(-C))
    z=s.Rational(1,7)
    K=s.Matrix([[s.Rational(1,2),0,s.Rational(1,8)],
                [0,s.Rational(1,3),0],[0,0,s.Rational(2,5)]])
    def exact_comm(K):
        D=(1-z)*s.eye(3)+z*K.T*C*C*K
        M=K*D.inv()*K.T
        G=-z*(C*M+M*C)
        Q=s.diag(G,s.zeros(3))
        return U*Q-Q*U
    require(exact_comm(K)==s.zeros(6),'ternary compression plus compatible past is stationary')
    Kbad=K.copy();Kbad[0,1]=s.Rational(1,10)
    require(C**3==C,'same ternary corner retained')
    require(exact_comm(Kbad)!=s.zeros(6),'ternary corner alone insufficient for nonnormal past')
    # General full matrix controls; all directions are on the reflection orbit.
    rng=np.random.default_rng(4402810)
    largest_identity_error=0.;smallest_ratio=1e99;largest_fd_error=0.
    for idx in range(6):
        cs=np.array([.27,.48,.79])+.005*idx
        Q,_=la.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))
        Cf=Q@np.diag(cs)@Q.conj().T
        Kf=np.array([[.5,.08,.02],[.01,.31,.07],[0,.03,.42]],complex)
        U,D,M,G,comm=components(Cf,Kf)
        P=la.block_diag(np.eye(3),np.zeros((3,3)))
        H=U@P-P@U
        dU=H@U-U@H
        dc=dU[:3,:3]
        largest_identity_error=max(largest_identity_error,near(dc,-2*(np.eye(3)-Cf@Cf),'full reflection descent witness'))
        source=np.trace(G@dc).real
        pred=4*.19*np.trace(M@Cf@(np.eye(3)-Cf@Cf)).real
        near(source,pred,'matrix-history descent source')
        w=.19*np.trace(M@Cf@Cf).real
        floor=4*cs.min()*(1-cs.max()**2)/cs.max()**2
        require(source/w>=floor-1e-12,'uniform positive-collar normalized source bound')
        require(la.norm(H,2)<=1+1e-12,'witness generator has true norm at most1')
        require(la.norm(comm)>1e-4,'interior positive corner not stationary on full orbit')
        smallest_ratio=min(smallest_ratio,source/w)
        def price(t):
            E=la.expm(t*H);V=E@U@E.conj().T;cc=V[:3,:3]
            Dd=(1-.19)*np.eye(3)+.19*Kf.conj().T@cc@cc@Kf
            return -np.linalg.slogdet(Dd)[1]
        e=2e-4
        fd=(-price(2*e)+8*price(e)-8*price(-e)+price(-2*e))/(12*e)
        largest_fd_error=max(largest_fd_error,near(fd,source,'full scalar matrix-orbit source',1e-10))
    # Invertibility of the actual old corner is material to the classification.
    Csing=np.diag([.4,0.]);Ksing=np.diag([0.,.5])
    *_,comm=components(Csing,Ksing)
    near(comm,np.zeros((4,4)),'singular past can hide fractional corner')
    require(la.norm(Csing@Csing@Csing-Csing)>0,'invertible-past assumption cannot be dropped')
    return {'critical_class_for_invertible_K':'C^3=C and [C^2,K K*]=0',
            'uniform_positive_collar_floor':'4*c_min*(1-c_max^2)/c_max^2',
            'minimum_observed_source_over_w':smallest_ratio,
            'largest_matrix_identity_error':largest_identity_error,
            'largest_full_scalar_FD_error':largest_fd_error,
            'scope':'complete return at fixed K; full price only with proved neutral or bounded extra source',
            'singular_past_negative_control':True}


def main():
    W,ops,native=native_children()
    out={'scientific_input':'fd35893d77e4aa5f819bafa0c6428c8e7a8f1812',
         'native_children':native,'exact_charts':exact_chart(),
         'full_operator':full_cold_programme(W,ops),'retained_past':matrix_past(),
         'negative_controls':mixed_price_and_selection(),
         'global_reflection_stationarity':reflection_stationary_class()}
    out.update({'checks':COUNT,'status':'PASS_INTERNAL_PROGRAM_SOURCE_CHART',
        'GR_closed':False,'physical_controlled_evaluator_admitted':False,
        'task_law_selection_proved':False,'full_physical_variation_domain_proved':False,
        'new_native_primitive_claimed':False,'Lean_or_CI_run':False,
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':s.__version__},
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__': main()
