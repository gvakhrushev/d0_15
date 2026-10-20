#!/usr/bin/env python3
"""Finite recovery of the original scalar Golden reporter, complete C1 source.

Exact algebra: Q(sqrt(5))[t], prefix-code completeness, arbitrary unitary block
with real scalar compression. Numerical application: original CAR16/null
operand, actual 256-word coherent Pauli scalarization, 128-column reference
as CAR16 x unchanged 8-dimensional spectator. Read-only except --output.
This is a conditional programme/interface theorem, not Book03 selection.
"""
from __future__ import annotations
import argparse, hashlib, json, math, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm
import sympy as S

P = (math.sqrt(5)-1)/2
checks: list[str] = []

def require(test: bool, name: str) -> None:
    if not test:
        raise AssertionError(name)
    checks.append(name)

def small(value: float, tol: float, name: str) -> None:
    require(float(value) < tol, f'{name}: {value:.3g} < {tol:.3g}')

def exact_algebra() -> dict:
    p=(S.sqrt(5)-1)/2
    t=S.symbols('t', real=True)
    for N in (1,2,3,5):
        rows=[]
        for b in (0,1):
            a=p**2+p*t if b==0 else p*S.sqrt(p)*(1-t)
            beta=p if b==0 else -p*S.sqrt(p)
            rows.append((S.expand(a*a),2+b,'clean'))
            for k in range(1,N+1):
                rows.append((S.expand(beta**2*(1-t*t)**2*t**(2*(k-1))),
                             2+b+2*k, f'recover{k}'))
            rows.append((S.expand(beta**2*(1-t*t)*t**(2*N)),
                         3+b+2*N,'unresolved'))
        require(S.simplify(sum(q for q,L,_ in rows)-1)==0,f'complete probabilities N={N}')
        require(S.simplify(sum(p**L for q,L,_ in rows)-1)==0,f'Golden Kraft complete N={N}')
        cost=sum(q*L for q,L,_ in rows)
        target=2+2*p+2*p**3*(1-t)-p*(1+t*t)*t**(2*N)
        require(S.simplify(cost-target)==0,f'full 0/10 record cost N={N}')
        require(S.simplify(S.diff(cost,t).subs(t,0)+2*p**3)==0,f'cost source N={N}')
        unresolved=sum(q for q,L,name in rows if name=='unresolved')
        require(S.simplify(unresolved-p*(1-t*t)*t**(2*N))==0,
                f'finite unresolved tail N={N}')
        # Only the two direct-clean probabilities have nonzero first derivative.
        for q,L,name in rows:
            if name!='clean':
                require(S.diff(q,t).subs(t,0)==0,f'even recovery probability {N}:{L}:{name}')
        # At t=0 positive leaves are p^4,p^2,p^3,p^3. Logs are exact integer powers.
        h0=4*p**4+2*p**2+6*p**3
        require(S.simplify(h0-(4-2*p))==0,f'pointer entropy at null N={N}')
        dh=-2*p**3*(-4)+2*p**3*(-3) # log_phi p^j = -j
        require(S.simplify(dh-2*p**3)==0,f'pointer entropy first source N={N}')
        require(S.simplify(cost.subs(t,0)-h0-4*p**3)==0,f'positive KL baseline N={N}')
        require(S.simplify(S.diff(cost,t).subs(t,0)-dh+4*p**3)==0,
                f'complete code-minus-pointer source N={N}')
        mean_recovery=p*(1-t*t)*sum(t**(2*k) for k in range(N))
        require(S.simplify(mean_recovery-p*(1-t**(2*N)))==0,
                f'paid recovery-count identity N={N}')
    # Exact non-Hermitian block unitary: left/right work frames differ.
    u=S.symbols('u',real=True)
    z=S.symbols('z',real=True)
    def red(M):
        return M.applyfunc(lambda x:S.rem(S.Poly(S.expand(x),z),S.Poly(z*z+t*t-1,z)).as_expr().expand())
    d=2; I=S.eye(d); O=S.zeros(d)
    V=S.Matrix([[0,1],[-1,0]])
    W=S.diag(1,-1)
    U=S.BlockMatrix([[t*I,z*V],[z*W,-t*W*V]]).as_explicit()
    inj=S.Matrix.vstack(I,O); proj=inj*inj.T; Q=S.eye(4)-proj
    require(red(U.T*U-S.eye(4))==S.zeros(4),'arbitrary left/right block unitary')
    J=Q*U*inj
    require(red(proj*U.T*J-(1-t*t)*inj)==S.zeros(4,2),'inverse cleanup success amplitude')
    failure=Q*U.T*J
    require(red(proj*U*failure+t*(1-t*t)*inj)==S.zeros(4,2),'alternating forward second recovery')
    twice=Q*U*failure
    require(red(twice-t*t*J)==S.zeros(4,2),'two-recovery unknown-work amplitude t^2')
    return {'null_code_cost':float(6*p),'null_pointer_entropy_phi':float(4-2*p),
            'null_net_KL_phi':float(4*p**3),
            'cost_source_dt':float(-2*p**3),
            'pointer_entropy_source_dt':float(2*p**3),
            'code_minus_pointer_source_dt':float(-4*p**3),
            'mean_recovery_calls_at_null':float(p)}

def creator(a: int) -> np.ndarray:
    c=np.zeros((16,16))
    for m in range(16):
        if not (m>>a)&1:
            c[m|(1<<a),m]=(-1)**((m&((1<<a)-1)).bit_count())
    return c
CRE=np.array([creator(a) for a in range(4)])

def E(a:int,b:int)->np.ndarray:
    x=np.zeros((4,4));x[a,b]=1;return x
ETA=E(0,1)+E(1,0)-E(2,2)-E(3,3)
N2=E(1,2)+E(2,0); N3=E(1,3)+E(3,0); NB2=E(0,2)+E(2,1)

def exterior(P:np.ndarray)->np.ndarray:
    out=np.zeros((16,16))
    for a in range(16):
        ia=[j for j in range(4) if a>>j&1]
        for b in range(16):
            if a.bit_count()!=b.bit_count():continue
            ib=[j for j in range(4) if b>>j&1]
            out[a,b]=np.linalg.det(P[np.ix_(ia,ib)]) if ia else 1.
    return out
HE=exterior(ETA)

def positive_root(M:np.ndarray)->np.ndarray:
    w,v=np.linalg.eigh((M+M.T)/2)
    if w.min()<.1:raise ValueError('strict Julia domain not satisfied')
    return (v*np.sqrt(w))@v.T

def walsh(X:np.ndarray)->np.ndarray:
    # Normalized 8-bit Walsh over the actual 256 selector labels.
    Y=X.copy();n=Y.shape[0];step=1
    while step<n:
        Z=Y.reshape((-1,2*step)+Y.shape[1:])
        A=Z[:,:step].copy();B=Z[:,step:].copy()
        Z[:,:step]=A+B;Z[:,step:]=A-B
        step*=2
    return Y/math.sqrt(n)

class ScalarReporter:
    def __init__(self,theta:float,base_x:float=-.00122444268454558,
                 base_y:float=-.00062444268454558):
        nu=.6; scale=P**8
        legs=nu*ETA
        C=[sum((legs[a,r]*CRE[a] for a in range(4)),np.zeros((16,16))) for r in range(4)]
        # Literal inverse-leg CAR polynomial for the u-x face, NOT a fitted scalar angle.
        D=C[0]@HE@C[2].T@HE-C[2]@HE@C[0].T@HE
        plaquette=expm(theta*NB2)@expm(base_x*N2+base_y*N3)
        self.T=scale*D@exterior(plaquette)
        self.t=float(np.trace(self.T)/16)
        I=np.eye(16)
        self.J=np.block([[self.T,positive_root(I-self.T@self.T.T)],
                         [positive_root(I-self.T.T@self.T),-self.T.T]])
        self.unitarity=float(np.max(np.abs(self.J.T@self.J-np.eye(32))))
        inds=np.arange(16)
        self.perm=np.array([inds^(j//16) for j in range(256)])
        self.sign=np.array([[(-1)**((int(i)&(j%16)).bit_count()) for i in self.perm[j]] for j in range(256)])
        self.sign_inv=np.array([[(-1)**((int(i)&(j%16)).bit_count()) for i in inds] for j in range(256)])
        self.inj=np.zeros((256,2,16,16));self.inj[0,0]=I
    def pauli(self,Y:np.ndarray,inverse:bool=False)->np.ndarray:
        return np.take_along_axis(Y,self.perm[:,None,:,None],axis=2)*(self.sign_inv if inverse else self.sign)[:,None,:,None]
    def U(self,X:np.ndarray,adjoint:bool=False)->np.ndarray:
        Y=self.pauli(walsh(X))
        Y=np.einsum('ij,ajk->aik',self.J.T if adjoint else self.J,Y.reshape(256,32,-1),optimize=True).reshape(X.shape)
        return walsh(self.pauli(Y,inverse=True))
    def clean(self,X:np.ndarray)->np.ndarray:
        Y=np.zeros_like(X);Y[0,0]=X[0,0];return Y
    def leaves(self,cap:int=2)->list[tuple[str,np.ndarray]]:
        Ui=self.U(self.inj)
        out=[]
        for b,Y in [(0,P*P*self.inj+P*Ui),(1,P*math.sqrt(P)*(self.inj-Ui))]:
            good=self.clean(Y);out.append((f'{b}:clean',good))
            bad=Y-good
            for k in range(1,cap+1):
                step=self.U(bad,adjoint=bool(k%2))
                good=self.clean(step);out.append((f'{b}:recover{k}',good))
                bad=step-good
            out.append((f'{b}:unresolved',bad))
        return out

def predicted(t:float,cap:int=2)->dict[str,tuple[float,int]]:
    out={}
    for b in (0,1):
        a=P*P+P*t if b==0 else P*math.sqrt(P)*(1-t)
        beta=P if b==0 else -P*math.sqrt(P)
        out[f'{b}:clean']=(a*a,2+b)
        for k in range(1,cap+1):
            out[f'{b}:recover{k}']=(beta*beta*(1-t*t)**2*t**(2*(k-1)),2+b+2*k)
        out[f'{b}:unresolved']=(beta*beta*(1-t*t)*t**(2*cap),3+b+2*cap)
    return out

def code_entropy(t:float,cap:int=2)->tuple[float,float,float]:
    r=predicted(t,cap)
    c=sum(q*L for q,L in r.values())
    h=-sum(q*math.log(q) for q,L in r.values() if q>0)/math.log(1/P)
    return c,h,c-h

def full_car_replay()->dict:
    zero=ScalarReporter(0.)
    small(zero.unitarity,2e-13,'actual original CAR Julia unitarity')
    small(abs(zero.t),1e-14,'original null CAR amplitude has t=0')
    Uinj=zero.U(zero.inj)
    small(np.max(np.abs(Uinj[0,0]-zero.t*np.eye(16))),1e-13,'full CAR16 coherent Pauli scalar compression')
    small(np.max(np.abs(zero.U(Uinj,adjoint=True)-zero.inj)),1e-13,'full work U inverse, no truncated output')
    max_prob_error=max_ref_error=max_success_error=0.
    for theta in (0.,-.7,.5):
        R=ScalarReporter(theta); leaves=R.leaves(2); formula=predicted(R.t,2)
        total=np.zeros((16,16))
        for label,Op in leaves:
            K=Op.reshape(-1,16);eff=K.T@K;prob=float(np.trace(eff)/16)
            q,L=formula[label]
            max_prob_error=max(max_prob_error,abs(prob-q))
            total+=eff
            # Full 128-column preparation: tensor eight untouched spectator states.
            gram128=np.kron(eff,np.eye(8))/128
            max_ref_error=max(max_ref_error,float(np.max(np.abs(gram128-q*np.eye(128)/128))))
            if 'unresolved' not in label:
                outside=Op-R.clean(Op)
                max_success_error=max(max_success_error,float(np.linalg.norm(outside)))
        small(np.max(np.abs(total-np.eye(16))),2e-13,f'complete finite source channel theta={theta}')
    small(max_prob_error,2e-13,'every literal final record probability')
    small(max_ref_error,2e-14,'all128 oldRIGHT conditional Gram, every outcome')
    small(max_success_error,1e-14,'resolved clean work exactly on original input cut')
    # Check whole amplitude first jet, not merely Born probabilities.
    h=2e-4
    minus=ScalarReporter(-h);plus=ScalarReporter(h)
    dt=(plus.t-minus.t)/(2*h)
    lm=dict(minus.leaves(2));lp=dict(plus.leaves(2))
    maxjet=0.
    for b in (0,1):
        beta=P if b==0 else -P*math.sqrt(P)
        expected={'clean':P if b==0 else -P*math.sqrt(P),
                  'recover1':0.,'recover2':-beta,'unresolved':0.}
        for suffix,amp in expected.items():
            lab=f'{b}:{suffix}'
            actual=(lp[lab]-lm[lab])/(2*h)
            maxjet=max(maxjet,float(np.linalg.norm(actual-dt*amp*zero.inj)))
    small(maxjet,2e-9,'complete operator first jet factors through dt times logical identity')
    # One inverse attempt has a non-scalar unresolved first amplitude;
    # two attempts remove precisely that obstruction.
    l1m=dict(minus.leaves(1));l1p=dict(plus.leaves(1))
    firstcap=sum(np.linalg.norm((l1p[f'{b}:unresolved']-l1m[f'{b}:unresolved'])/(2*h))**2 for b in (0,1))**.5
    require(firstcap>1e-3,'one attempt NOT a full first-jet cleanup')
    c0,H0,j0=code_entropy(0)
    fp=code_entropy(plus.t);fm=code_entropy(minus.t)
    numeric=[(a-b)/(2*h) for a,b in zip(fp,fm)]
    expected=[-2*P**3*dt,2*P**3*dt,-4*P**3*dt]
    small(max(abs(a-b) for a,b in zip(numeric,expected)),2e-9,'full paid record and pointer Info first sources on actual CAR field')
    return {'query_dimension':16,'selector_labels':256,'total_query_workspace_dimension':8192,
            'reference_columns':128,'reference_implementation':'CAR16 x untouched spectator8',
            'actual_null_plaquette_coefficients':[-.00122444268454558,-.00062444268454558],
            'fixed_contraction':P**8,'t_at_null':zero.t,'dt_d_opposite_null_link':dt,
            'whole_first_jet_error':maxjet,'one_attempt_unresolved_jet_norm':firstcap,
            'source_code':numeric[0],'source_pointer_Info_phi':numeric[1],
            'source_code_minus_pointer_Info_phi':numeric[2],
            'source_prediction':expected,'max_prob_error':max_prob_error,'max_reference_Gram_error':max_ref_error,
            'null_code_cost':c0,'null_pointer_entropy_phi':H0,'null_KL_phi':j0}

def irreversible_record_control()->dict:
    # Logical qubit and work 0,1,2: swap clean |0,0> with |1,0>,
    # clean |0,1> with |2,1>. PUP=0 but copying a resolved work address
    # turns an uncomputed reversible workspace into a protected record.
    U=np.eye(6)
    for i,j in ((0,2),(1,5)):
        U[i,i]=U[j,j]=0;U[i,j]=U[j,i]=1
    psi=np.zeros((6,2));psi[0,0]=psi[1,1]=1/math.sqrt(2)
    after=U@psi
    recovered=U.T@after
    small(np.max(np.abs(recovered-psi)),1e-14,'reversible fresh workspace can be restored')
    # Record the distinguishable work address before inversion; do not
    # erase that protected record afterwards. Fidelity of data+reference
    # to the input Bell state then falls to 1/2.
    density=np.zeros((12,12))
    for w in (1,2):
        block=np.zeros_like(after);block[2*w:2*w+2]=after[2*w:2*w+2]
        branch=(U.T@block).reshape(-1)
        density+=np.outer(branch,branch)
    v=psi.reshape(-1);fid=float(v@density@v)
    small(abs(fid-.5),1e-14,'copying protected inner history invalidates cleanup, not silently erased')
    return {'fidelity_after_forbidden_inner_readout':fid,
            'condition':'U inverse may act on fresh reversible work, never on separately protected old history'}

def main()->None:
    pa=argparse.ArgumentParser();pa.add_argument('--output',type=Path);args=pa.parse_args()
    result={'status':'AUTHOR_REPLAY_PASS_NOT_INDEPENDENT_ACCEPTANCE','input_ref':'d333307d031123aedf7a49b35a12ce5f7c17fc04',
            'exact_algebra':exact_algebra(),'actual_CAR_scalarization':full_car_replay(),
            'hostile_protected_history':irreversible_record_control(),
            'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':S.__version__},
            'physical_Book03_selected':False,'full128_energy_price_replaced':False,
            'GR_closed':False,'independent_acceptance':False}
    result['checks']=checks
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
