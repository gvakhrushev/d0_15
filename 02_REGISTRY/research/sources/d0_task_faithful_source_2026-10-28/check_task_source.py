#!/usr/bin/env python3
"""All-input task source and retained-history relative error checks.

Exact native test uses the owned G/CX/quaternion SourceI word. Other matrix
families test the proved theorem; they do not assert physical D0 admission.
"""
from __future__ import annotations
import hashlib, json, math
from collections import Counter
from pathlib import Path
import numpy as np
import scipy.linalg as la
import sympy as sp
from sympy.polys.matrices import DomainMatrix
import mpmath as mp

COUNT = 0

def require(ok, name):
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise ArithmeticError(name)


def near(a, b, name, tol=2e-11):
    err = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(err < tol, f'{name}: {err}')
    return err


def exact_native():
    p = (sp.sqrt(5)-1)/2
    a = sp.sqrt(p)
    field = sp.QQ.algebraic_field(a)
    def dm(M): return DomainMatrix.from_Matrix(sp.Matrix(M)).convert_to(field)
    Id = dm(sp.eye(32))
    G = sp.Matrix([[a, -p], [p, a]])
    Li = sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    SI = sp.diag(sp.eye(4), Li)
    CX = sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    def gate(op, wires):
        require(4 not in wires, 'oldRIGHT never addressed')
        local = {'G': G, 'CX': CX, 'SourceI': SI}[op]
        M = sp.zeros(32); k = len(wires)
        for col in range(32):
            bits = [(col >> (4-j)) & 1 for j in range(5)]
            j = sum(bits[w] << (k-1-u) for u,w in enumerate(wires))
            for i in range(1 << k):
                if local[i,j] == 0: continue
                bb = bits[:]
                for u,w in enumerate(wires): bb[w] = (i >> (k-1-u)) & 1
                row = sum(bb[u] << (4-u) for u in range(5))
                M[row,col] = local[i,j]
        ans = dm(M)
        require((ans.transpose().matmul(ans)-Id).is_zero_matrix, 'full32 primitive orthogonal')
        return ans
    def swap(x,y): return [('CX',(x,y)),('CX',(y,x)),('CX',(x,y))]
    si = ('SourceI',(0,2,3)); route = swap(0,1)
    def inverse(word):
        ans=[]
        for op,wires in reversed(word):
            if op == 'CX': ans.append((op,wires))
            elif op == 'SourceI': ans += [si]*3
            else:
                rr = [] if wires[0] == 0 else swap(wires[0],0)
                ans += rr+[si,si,('G',(0,)),si,si]+rr
        return ans
    vg = route+[('G',(0,))]+route
    query = inverse(vg)+route+[si,si]+route+vg
    V=[('G',(1,))]
    A=V+inverse(V)+query
    B=V+query+inverse(V)
    require(len(query)==26 and len(A)==len(B)==38, 'actual original lengths')
    inventory=dict(Counter(g[0] for g in A))
    require(inventory==dict(Counter(g[0] for g in B))=={'G':4,'CX':24,'SourceI':10}, 'same inventory')
    cache={g:gate(*g) for g in set(A+B)}
    def endpoint(word):
        out=Id
        for g in word: out=cache[g].matmul(out)
        return out
    WA,WB=endpoint(A),endpoint(B)
    c=p**3; u=2*p*sp.sqrt(p)
    QA=dm(sp.kronecker_product(sp.eye(2),sp.Matrix([[c,u],[u,-c]]),sp.eye(8)))
    Z=dm(sp.kronecker_product(sp.eye(2),sp.diag(1,-1),sp.eye(8)))
    require((WA-QA).is_zero_matrix and (WB-Z).is_zero_matrix,'native exact endpoints')
    defect=(WB-WA).scalarmul(field.from_sympy(sp.Rational(1,2)))
    require((defect.matmul(defect)-Id.scalarmul(field.from_sympy(p*p))).is_zero_matrix,'all-input effect defect norm exactly p')
    P=dm(sp.diag(*([1]*8+[0]*24)))
    require((P.matmul(defect).matmul(P)-P.scalarmul(field.from_sympy(p*p))).is_zero_matrix,'prepared report bias exactly p squared')
    s=sp.symbols('s',real=True)
    cc=c*sp.cos(2*s)-u*sp.sin(2*s)
    derivative=sp.diff((1-cc)/2,s).subs(s,0)
    require(sp.simplify(derivative-u)==0,'query source changes report law')
    # A genuine SAME-TASK pair; the full dirty-complement operators differ.
    X=('CX',(0,1))
    alias1=[X,X]+query
    alias2=[X]+query+[X]
    W1,W2=endpoint(alias1),endpoint(alias2)
    source=dm(sp.diag(*([1]*16+[0]*16)))
    require(len(alias1)==len(alias2)==28,'same-task raw lengths')
    require(Counter(g[0] for g in alias1)==Counter(g[0] for g in alias2),'same-task inventory')
    require((W1-WA).is_zero_matrix,'first alias equals original query on all columns')
    require(not (W1-W2).is_zero_matrix,'same task does not force identical complement')
    require((W1-W2).matmul(source).is_zero_matrix,'same complete16 source-output columns')
    require((W2.matmul(W2)-Id).is_zero_matrix,'second native alias remains reflection')
    return {'same_task_native_pair':{'raw_stages':28,'source_columns':16,
                'protected_rank':8,'different_full_operators':True,
                'inventory':dict(Counter(g[0] for g in alias1)),
                'same_complete_source_output':True},
            'raw_stages_per_word':38,'inventory':inventory,'columns':32,'protected_rank':8,
            'effect_operator_norm':'p','prepared_probability_gap':'p^2',
            'same_task':False,'AF272_replayed':False}


def task_fibres():
    C=np.array([[.42,.12],[.12,.67]])
    D=la.sqrtm(np.eye(2)-C@C)
    Q=np.block([[C,D],[D,-C]])
    i=np.vstack([np.eye(2),np.zeros((2,2))])
    near(Q@Q,np.eye(4),'actual full reflection')
    E=(np.eye(2)-C)/2
    def changed(s):
        O=np.array([[math.cos(s),-math.sin(s)],[math.sin(s),math.cos(s)]])
        B=la.block_diag(np.eye(2),O)
        return B.T@Q@B
    maxerr=0.; minchange=1.
    for s in (.2,.7,-.5):
        Qs=changed(s)
        maxerr=max(maxerr,near(i.T@(np.eye(4)-Qs)@i/2,E,'same effect on entire unprepared source'))
        minchange=min(minchange,la.norm(Qs-Q,2))
        require(la.norm(Qs-Q,2)>.03,'full implementation really differs')
        for y in (.1,.4,.9):
            R=np.array([[math.cos(y)],[math.sin(y)]])
            near(R.T@i.T@Qs@i@R,R.T@C@R,'all preparation pullbacks agree')
    # Same diagonal Born probabilities, different coherent task and first jet.
    E1=.3*np.eye(2); E2=E1+.08*np.array([[0.,1.],[1.,0.]])
    near(np.diag(E1),np.diag(E2),'classical basis probabilities match')
    plus=np.ones(2)/math.sqrt(2)
    require(abs(plus@(E2-E1)@plus-.08)<1e-14,'coherent input separates effects')
    require(abs(2*(E2-E1)[0,1]-.16)<1e-14,'same base value does not identify source')
    # Error tolerance alone places NO restriction on derivatives.
    epsilon=1e-6; freq=1e6
    require(abs(epsilon*freq-1)<1e-14,'small uniform error permits unit first derivative')
    # Full price is not a function of an arbitrary classical report channel.
    c=.6;u=.8
    reflection=np.array([[c,u],[u,-c]])
    rotation=np.array([[c,-u],[u,c]])
    require(abs(reflection[0,0]-rotation[0,0])<1e-15,'equal cold amplitude')
    require(la.norm(reflection@reflection-np.eye(2))<1e-14,'echo hypothesis met in first completion')
    require(la.norm(rotation@rotation-np.eye(2))>.1,'not met in second completion')
    return {'same_effect_error':maxerr,'minimum_full_query_change':float(minchange),
            'classical_only_law_is_insufficient':True,'small_error_is_not_tangent_constraint':True,
            'arbitrary_completion_not_identified_with_echo':True}


def memory_source():
    z=.19
    K=np.array([[.53,.17],[.04,.26]],complex)
    S=K.conj().T@K
    cs=[.61,.73,.84]; T=math.prod(c*c for c in cs)
    Dr=(1-z)*np.eye(2)+z*T*S
    inv=la.inv(Dr); w=z*T*np.trace(S@inv).real
    rho=K@inv@K.conj().T/np.trace(S@inv).real
    near(np.trace(rho),1,'true past density normalized')
    require(la.eigvalsh(rho).min()>0,'true past density positive')
    Xs=[np.array([[.03,.02j],[-.02j,-.01]]),np.array([[.01,.025],[.025,.04]]),np.array([[-.02,.01j],[-.01j,.03]])]
    worst=0.
    for j,X in enumerate(Xs):
        # delta C=-2 delta E. No artificial cancellation of the old matrix.
        dK=-2*math.prod(cs)/cs[j]*X@K
        dD=z*(math.prod(cs)*K.conj().T@dK+dK.conj().T@(math.prod(cs)*K))
        g=-np.trace(inv@dD).real
        expected=4*w/cs[j]*np.trace(rho@X).real
        worst=max(worst,near(g,expected,'full matrix past semantic source'))
        require(abs(g)<=4*w/cs[j]*la.norm(X,2)+1e-15,'source bound independent of past gap')
    # Query-free directions have zero semantic derivative; bad directions retain beta.
    for c in cs:
        u=math.sqrt(1-c*c)
        X=u*np.eye(2)
        near(4/c*np.trace(rho@X).real,4*u/c,'new owner beta recovered')
    return {'max_source_identity_error':worst,'past_condition':float(np.linalg.cond(S)),
            'w':float(w),'new_query_row_not_discarded':True}


def mp_return(S,T,z):
    a=1-z;tr=S[0,0]+S[1,1];det=mp.det(S)
    x=z*T/a
    small=mp.log1p(x*tr+x*x*det)
    full=-2*mp.log(a)-small
    w=(x*tr+2*x*x*det)/(1+x*tr+x*x*det)
    return full,small,w


def finite_relative_budget():
    mp.mp.dps=180
    z=mp.mpf(1)/7; records=[]
    for epsold in ('0.3','1e-30','0'):
        K=mp.matrix([[mp.mpf('0.5'),mp.mpf(1)/7],[0,mp.mpf(epsold)]])
        S=K.T*K
        for age in (0,30,120):
            M=mp.eye(2);eta=mp.mpf(0)
            for n in range(3):
                E=mp.matrix([[mp.mpf(n+1)/1000,mp.mpf((-1)**n)/1300],
                             [mp.mpf((-1)**n)/1300,-mp.mpf(n+2)/1700]])
                eig=mp.eigsy(E,eigvals_only=True)
                delta=max(abs(x) for x in eig)
                require(delta<1,'relative cold error collar')
                eta-=mp.log1p(-delta)
                M=(mp.eye(2)+E)*M
            T=mp.mpf(4)**(-age)*mp.mpf('.7')**6
            Shat=K.T*M.T*M*K
            full,small,w=mp_return(S,T,z)
            fullhat,smallhat,_=mp_return(Shat,T,z)
            difference=abs(smallhat-small) # exact stable full-price difference; baseline retained above
            bound=mp.expm1(2*eta)*w
            require(w>0 and difference<=bound,'uniform full-return relative error bound')
            records.append({'old_min_scale':epsold,'retention_exponent':age,
                            'w':mp.nstr(w,24),'actual_price_difference':mp.nstr(difference,24),
                            'proved_bound':mp.nstr(bound,24),'ratio':mp.nstr(difference/bound,24)})
    # Newest-only exact probability retention: scalar c_j need not share a source.
    for theta in ('-0.8','0.4','2.0'):
        s=mp.mpf(theta)
        _,_,w0=mp_return(S,mp.mpf('.02'),z)
        _,_,ws=mp_return(S,mp.mpf('.02')*mp.exp(s),z)
        require(min(1,mp.exp(s))*w0<=ws<=max(1,mp.exp(s))*w0,'true gain log-Lipschitz bound')
    require(mp_return(mp.zeros(2),mp.mpf(1),z)[2]==0,'zero gain explicitly excluded')
    return {'controls':records,'noncommuting_relative_factors':True,
            'past_rank_deficiency_allowed_if_nonzero':True,'full_baseline_retained':True}


def full_clock_control():
    # Structural parked echoes, not emitted native words or AF programme.
    def rot(s):return np.array([[math.cos(s),-math.sin(s)],[math.sin(s),math.cos(s)]])
    Z=np.diag([1.,-1.]);old=rot(.31)
    I2=np.eye(2);dim=8;N=7;beta=.7639320225002103
    def heat(s,t):
        A=rot(s);B=rot(t)
        ops=[np.kron(np.kron(old,I2),I2),np.kron(np.kron(I2,A),I2),
             np.kron(np.kron(I2,Z),I2),np.kron(np.kron(I2,A.T),I2),
             np.kron(np.kron(I2,I2),B),np.kron(np.kron(I2,I2),Z),
             np.kron(np.kron(I2,I2),B.T)]
        shift=np.zeros((N*dim,N*dim))
        for j,g in enumerate(ops):shift[((j+1)%N)*dim:((j+1)%N+1)*dim,j*dim:(j+1)*dim]=g
        Delta=np.eye(N*dim)-(shift+shift.T)/2
        return math.log(2*np.exp(-beta*la.eigvalsh(Delta)).sum())/beta
    ref=heat(.2,.4)
    errors=[abs(heat(s,t)-ref) for s,t in ((.6,-.2),(.7,1.1),(-.4,.8))]
    require(max(errors)<3e-13,'all-clock heat of parked echo spectrum unchanged')
    return {'clock_modes_per_grade':56,'both_grades':112,'max_heat_error':max(errors),
            'scope':'bare paired clock at fixed length; structural matrix test only'}


def main():
    out={'scientific_input':'d4c700f78572179ffb6fc98a12ca7e31fa2bc1b4',
         'native_task_change':exact_native(),'all_input_fibre':task_fibres(),
         'retained_matrix_source':memory_source(),'finite_relative_budget':finite_relative_budget(),
         'full_clock':full_clock_control()}
    out.update({'checks':COUNT,'status':'PASS_TASK_FAITHFUL_RETURN_SOURCE',
        'physical_task_admission_proved':False,'all_field_roots_proved':False,
        'GR_closed':False,'Lean_or_CI_run':False,
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False))
if __name__=='__main__':main()
