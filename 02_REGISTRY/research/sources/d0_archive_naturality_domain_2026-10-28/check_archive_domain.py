#!/usr/bin/env python3
"""Finite archive-algebra domain audit on the original Fibonacci inclusions.

No physical completeness claim. The algebra/normalizer controls are structural;
SourceI and the canonical conditional expectations use the owned matrices.
No old records, regular right columns or physical sources are discarded.
"""
from __future__ import annotations
import hashlib
import json
import math
import platform
from fractions import Fraction
from pathlib import Path
import numpy as np
import scipy
import scipy.linalg as la
import scipy.sparse as ss
import sympy as sp

COUNT = 0

def require(ok: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise ArithmeticError(message)

def near(a, b, message: str, tolerance: float = 3e-11) -> float:
    error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(error < tolerance, f'{message}: {error}')
    return error

def comm(a, b):
    return a@b-b@a

def fibpower(r: int) -> np.ndarray:
    return np.linalg.matrix_power(np.array([[1,1],[1,0]], dtype=np.int64), r)

P=(math.sqrt(5)-1)/2

class Inclusion:
    def __init__(self, old: tuple[int,int], r: int):
        self.old=tuple(old); self.r=r; self.m=fibpower(r)
        self.new=tuple(int(x) for x in self.m@np.array(old))
        self.offset={(b,a):sum(int(self.m[b,j])*old[j] for j in range(a))
                     for b in range(2) for a in range(2)}

    def embed(self, xs):
        return [la.block_diag(*[np.kron(np.eye(int(self.m[b,a])),xs[a]) for a in range(2)])
                for b in range(2)]

    def expectation(self, xs, spin: int=1):
        out=[]
        for a,da in enumerate(self.old):
            z=np.zeros((da*spin,da*spin),complex)
            for b in range(2):
                for c in range(int(self.m[b,a])):
                    start=(self.offset[b,a]+c*da)*spin
                    z+=P**(self.r+b-a)*xs[b][start:start+da*spin,start:start+da*spin]
            out.append(z)
        return out

    def gns(self):
        # Old and new regular matrix units are row-major, normalized by tau.
        oldoff=np.cumsum([0]+[d*d for d in self.old])
        newoff=np.cumsum([0]+[d*d for d in self.new])
        rows=[];cols=[];data=[]
        for a,da in enumerate(self.old):
            for b,db in enumerate(self.new):
                for c in range(int(self.m[b,a])):
                    base=self.offset[b,a]+c*da
                    for i in range(da):
                        for j in range(da):
                            rows.append(int(newoff[b]+(base+i)*db+base+j))
                            cols.append(int(oldoff[a]+i*da+j))
                            data.append(P**((self.r+b-a)/2))
        out=ss.coo_matrix((data,(rows,cols)),shape=(int(newoff[-1]),int(oldoff[-1]))).tocsr()
        near((out.T@out).toarray(),np.eye(int(oldoff[-1])),'original normalized GNS inclusion')
        return out

    def loops(self, phi: float):
        c,s=math.cos(2*phi),math.sin(2*phi)
        out=[];dot=[]
        for b,db in enumerate(self.new):
            L=np.eye(db,dtype=complex);D=np.zeros((db,db),complex)
            da=self.old[b];base=self.offset[b,b]
            require(self.m[b,b]>=2,'two real work copies exist')
            for r in range(da):
                inds=[base+r,base+da+r]
                L[np.ix_(inds,inds)]=[[c,-s],[s,c]]
                D[np.ix_(inds,inds)]=[[-2*s,-2*c],[2*c,-2*s]]
            near(L.conj().T@L,np.eye(db),'full paid-loop endpoint is unitary')
            out.append(L);dot.append(D)
        C=1-4*P**self.r*math.sin(phi)**2
        dC=-4*P**self.r*math.sin(2*phi)
        for actual in self.expectation(out):
            near(actual,C*np.eye(len(actual)),'original loop canonical cold value')
        for actual in self.expectation(dot):
            near(actual,dC*np.eye(len(actual)),'actual loop canonical first jet')
        return out,dot,C,dC

    def twirl(self, xs, spin: int=1):
        # Haar average over OLD U(d0) x U(d1), restricted to new left algebra.
        result=[]
        for b,db in enumerate(self.new):
            whole=np.zeros((db*spin,db*spin),complex)
            for a,da in enumerate(self.old):
                m=int(self.m[b,a]);start=self.offset[b,a]*spin
                block=xs[b][start:start+m*da*spin,start:start+m*da*spin]
                B=block.reshape(m,da,spin,m,da,spin)
                averaged=np.einsum('irujrv->iujv',B)/da
                # Copy/spin matrix averaged, old-row identity restored exactly.
                target=np.zeros_like(B)
                for row in range(da): target[:,row,:,:,row,:]=averaged
                whole[start:start+m*da*spin,start:start+m*da*spin]=target.reshape(m*da*spin,m*da*spin)
            result.append(whole)
        return result

def regular_left(xs):
    return ss.block_diag([ss.kron(ss.csr_matrix(X),ss.eye(len(X)),format='csr') for X in xs],format='csr')

def unit_basis(old):
    ans=[]
    for a,d in enumerate(old):
        for i in range(d):
            for j in range(d):
                xs=[np.zeros((n,n),complex) for n in old]
                xs[a][i,j]=1
                ans.append(xs)
    return ans

def exact_sourcei_control():
    Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    U=sp.diag(sp.eye(4),Li)
    X=sp.kronecker_product(sp.Matrix([[0,1],[1,0]]),sp.eye(4))
    Z=sp.diag(sp.eye(4),-sp.eye(4))
    psi=sp.Matrix([1,0,0,0,1,0,0,0])/sp.sqrt(2)
    require(U.T*U==sp.eye(8),'original SourceI exact complete unitarity')
    require(U.T*Z*U==Z,'all diagonal old-bit effects unchanged')
    require((psi.T*X*psi)[0]==1,'old coherent test initial value')
    require(((U*psi).T*X*(U*psi))[0]==0,'old coherent test disturbed by the native gate')
    delta=U.T*X*U-X
    require(delta.T*delta==2*sp.eye(8),'exact full quantum-archive defect sqrt2')
    require(U.T*(U*psi)==psi,'whole information remains reversibly recoverable')
    # An inherited central label becomes noncentral on refinement.
    inc=Inclusion((3,2),2)
    Q=inc.embed([np.zeros((3,3)),np.eye(2)])
    b=0;E=np.zeros((8,8));E[0,6]=1
    H=np.kron(Q[b],np.asarray(Li,float))
    oldtest=np.kron(E,np.eye(4))
    near(comm(H,oldtest),-np.kron(E,np.asarray(Li,float)),'actual inherited-marker witness')
    require(abs(la.norm(comm(H,oldtest),2)-1)<1e-13,'unit defect of inherited marker')
    # Since Q is now a diagonal noncentral projection, every diagonal test still commutes.
    for row in range(8):
        diag=np.zeros((8,8));diag[row,row]=1
        near(comm(H,np.kron(diag,np.eye(4))),np.zeros((32,32)),'all old row records fixed')
    return {'native_matrix':'controlled quaternion L_i, all eight columns',
            'classical_archive_effects_preserved':True,'closed_unitarity_preserved':True,
            'coherent_expectation_before':'1','coherent_expectation_after':'0',
            'full_archive_defect_exact':'sqrt(2)',
            'inherited_marker_current_sizes':list(inc.new),'inherited_marker_derivation_defect':1,
            'not_a_countermodel_to_all_D0_axioms':True}

def algebra_domain_controls():
    inc=Inclusion((2,1),2);spin=2
    units=[la.block_diag(*[np.kron(x,np.eye(spin)) for x in inc.embed(a)]) for a in unit_basis(inc.old)]
    dims=[n*spin for n in inc.new]
    n=sum(dims)
    rng=np.random.default_rng(282826)
    Xs=[]
    for d in dims:
        M=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
        Xs.append((M-M.conj().T)/12)
    HX=inc.twirl(Xs,spin)
    X=la.block_diag(*Xs);Y=la.block_diag(*HX)
    near(Y.conj().T,-Y,'twirled tangent remains skew')
    near(la.block_diag(*inc.twirl(HX,spin)),Y,'twirl idempotent')
    maxcomm=max(la.norm(comm(Y,A),2) for A in units)
    require(maxcomm<1e-12,'twirl in exact relative commutant')
    relative_distance=la.norm(X-Y,2)
    require(relative_distance>0.1,'test includes genuine archive disturbance')
    # Solve all [X,A]=0 in the true block-diagonal new left algebra.
    # This is a numerical rank control, not the proof of the dimension formula.
    allowed=[];off=0
    for d in dims:
        for i in range(d):
            for j in range(d):
                B=np.zeros((n,n),complex);B[off+i,off+j]=1
                allowed.append(B)
        off+=d
    constraint=np.column_stack([np.concatenate([comm(B,A).ravel() for A in units]) for B in allowed])
    singular=la.svdvals(constraint)
    rank=int(np.count_nonzero(singular>1e-10))
    expected=sum(int(inc.m[b,a])**2*spin**2 for b in range(2) for a in range(2))
    require(len(allowed)-rank==expected,'commutant dimension all new left matrix units')
    # Lie normalizer: [X,A] in A, not just zero. Project onto embedded A.
    Q,_=la.qr(np.column_stack([A.ravel() for A in units]),mode='economic')
    def outside_A(M):
        v=M.ravel();return v-Q@(Q.conj().T@v)
    normal=np.column_stack([np.concatenate([outside_A(comm(B,A)) for A in units]) for B in allowed])
    sn=la.svdvals(normal);rankn=int(np.count_nonzero(sn>1e-10))
    expectedn=expected+sum(d*d-1 for d in inc.old)
    require(len(allowed)-rankn==expectedn,'normalizer dimension includes shared old inner derivations')
    # Original real controls are a strictly smaller space; no new complex actuator.
    real_skew=[];offset=0
    for d in dims:
        for i in range(d):
            for j in range(i):
                B=np.zeros((n,n),complex);B[offset+i,offset+j]=1;B[offset+j,offset+i]=-1
                real_skew.append(B)
        offset+=d
    real_constraints=np.column_stack([np.concatenate([comm(B,A).ravel() for A in units]) for B in real_skew])
    real_normal=np.column_stack([np.concatenate([outside_A(comm(B,A)) for A in units]) for B in real_skew])
    real_c=len(real_skew)-int(np.count_nonzero(la.svdvals(real_constraints)>1e-10))
    real_n=len(real_skew)-int(np.count_nonzero(la.svdvals(real_normal)>1e-10))
    expect_real=sum((int(inc.m[b,a])*spin)*(int(inc.m[b,a])*spin-1)//2 for b in range(2) for a in range(2))
    require(real_c==expect_real and real_n==expect_real+sum(d*(d-1)//2 for d in inc.old),
            'real skew domain independently checked')
    # Fixed archive versus transported archive, explicit finite normalizer.
    v0=la.expm(np.array([[0.,.31],[-.31,0.]]));oldV=[v0,np.ones((1,1))]
    v=la.block_diag(*[np.kron(A,np.eye(spin)) for A in inc.embed(oldV)])
    W=la.expm(Y);U=v@W
    errs=[la.norm(U.conj().T@A@U-v.conj().T@A@v,2) for A in units]
    require(max(errs)<3e-12,'same old automorphism induces relative-commutant factor')
    # Polar repair is algebraic, not a newly physically executed gate.
    eps=.012
    Un=la.expm(eps*X)
    split=[];offset=0
    for d in dims:split.append(Un[offset:offset+d,offset:offset+d]);offset+=d
    Y0=la.block_diag(*inc.twirl(split,spin));W0,_=la.polar(Y0)
    distance=la.norm(Un-Y0,2)
    require(distance<1,'polar collar')
    require(la.norm(Un-W0,2)<=2*distance+1e-12,'finite polar repair bound')
    require(max(la.norm(comm(W0,A),2) for A in units)<2e-12,'polar unitary in relative commutant')
    return {'old_defining_sizes':list(inc.old),'new_defining_sizes':list(inc.new),'protected_dimension':spin,
            'whole_new_left_complex_dimension':len(allowed),'commutant_dimension':expected,
            'normalizer_identity_component_dimension':expectedn,
            'real_orthogonal_commutant_dimension':real_c,'real_orthogonal_normalizer_dimension':real_n,
            'smallest_nonzero_commutant_singular_value':float(singular[rank-1]),
            'max_commutant_test_error':float(maxcomm),
            'polar_original_to_average_distance':float(distance),
            'polar_repaired_distance':float(la.norm(Un-W0,2)),
            'normalizer_old_transport_error':float(max(errs)),
            'domain_physically_selected':False}


def actual_input_compatibility():
    # A_1=(M2+M1) -> A_3=(M5+M3), original faithful Golden traces.
    inc=Inclusion((2,1),2);spin=2
    def trace(xs, level):
        return sum(P**(level+1+b)*np.trace(X)/spin for b,X in enumerate(xs))
    def norm2(xs, level):
        return float(trace([X.conj().T@X for X in xs],level).real)
    units=unit_basis(inc.old)
    rng=np.random.default_rng(301026)
    X=[]
    for d in inc.new:
        B=rng.normal(size=(d*spin,d*spin))+1j*rng.normal(size=(d*spin,d*spin))
        X.append((B-B.conj().T)/10)
    projected=inc.embed(inc.expectation(X,spin))
    centered=[X[b]-projected[b] for b in range(2)]
    near(la.block_diag(*inc.expectation(centered,spin)),np.zeros((6,6)),
         'true AF expectation of centered generator vanishes')
    olda=[np.array([[0.,1.],[1.,0.]]),np.zeros((1,1))]
    a=inc.embed([np.kron(B,np.eye(spin)) for B in olda])
    olda=[np.kron(B,np.eye(spin)) for B in olda]
    first=[comm(a[b],centered[b]) for b in range(2)]
    firstcoarse=inc.expectation(first,spin)
    firsterr=near(la.block_diag(*firstcoarse),np.zeros((6,6)),
                  'all-input first archive jet can vanish for a NON-compatible tangent')
    energy=norm2(first,3)
    require(energy>1e-3,'second-order archive disturbance is real')
    second=inc.expectation([comm(first[b],centered[b]) for b in range(2)],spin)
    secondloss=-float(trace([olda[b]@second[b] for b in range(2)],1).real)
    near(secondloss,energy,'exact second-jet positive defect identity')
    values=[]
    for t in (.4,.02,.001):
        Us=[la.expm(t*B) for B in centered]
        rotated=[Us[b].conj().T@a[b]@Us[b] for b in range(2)]
        coarse=inc.expectation(rotated,spin)
        difference=[rotated[b]-a[b] for b in range(2)]
        direct=norm2(difference,3)
        formula=2*float(trace([olda[b].conj().T@(olda[b]-coarse[b]) for b in range(2)],1).real)
        near(direct,formula,'canonical-input defect norm from coarse archive effects')
        values.append({'t':t,'full_faithful_L2_defect_squared':direct,'coarse_effect_formula':formula})
    require(values[-1]['full_faithful_L2_defect_squared']>0,
            'zero first jet does not imply finite archive compatibility')
    # On a true fixed-law path, all old inputs see identity at every t.
    exact=inc.twirl(X,spin);U=[la.expm(B) for B in exact]
    maxerr=0.
    for old in units:
        old=[np.kron(A,np.eye(spin)) for A in old]
        fine=inc.embed(old)
        coarse=inc.expectation([U[b].conj().T@fine[b]@U[b] for b in range(2)],spin)
        maxerr=max(maxerr,max(la.norm(coarse[b]-old[b],2) for b in range(2)))
    require(maxerr<1e-12,'full original coarse old-law, no arbitrary fine-input preparation')
    return {'first_coarse_archive_derivative_error':firsterr,
            'positive_second_order_archive_energy':energy,
            'full_finite_identity_controls':values,
            'exact_compatible_path_max_old_effect_error':maxerr,
            'trace_used_only_as_faithful_certificate_not_Book_price':True,
            'proof_uses_original_canonical_input':True}


def canonical_source_control():
    inc=Inclusion((3,2),8);phi=math.acos(P)
    U,dU,C,dC=inc.loops(phi)
    J=inc.gns();regular=regular_left(U)
    cold=(J.conj().T@regular@J).toarray()
    dcold=(J.conj().T@regular_left(dU)@J).toarray()
    e=near(cold,C*np.eye(13),'actual all13 old matrix-unit input columns')
    de=near(dcold,dC*np.eye(13),'actual complete old input first derivative')
    leakage=(regular@J-J@ss.csr_matrix(cold)).toarray()
    near(leakage.conj().T@leakage,(1-C*C)*np.eye(13),
         'observable preservation does not imply zero GNS amplitude leakage')
    require(la.norm(leakage,2)>.1,'nonzero true canonical leakage remains')
    # All old quantum observables preserved, not merely diagonal records.
    maxerr=0.
    for a in unit_basis(inc.old):
        emb=inc.embed(a)
        for b in range(2):maxerr=max(maxerr,la.norm(comm(U[b],emb[b]),2))
    require(maxerr<2e-13,'full old archive law is transparent')
    z=2**-20;spectator=8;dinput=13*spectator
    D=1-z+z*C*C
    gain=dinput*z*C*C/D
    source=-2*dinput*z*C*dC/D
    lam=-2*dC/C
    near(source/gain,lam,'real source over same input gain')
    require(source>1e-6,'archive preservation does not force stationary price')
    def price(x):
        cc=1-4*P**8*math.sin(x)**2
        return -dinput*math.log1p(z*(cc*cc-1))
    h=2e-4
    fd=(-price(phi+2*h)+8*price(phi+h)-8*price(phi-h)+price(phi-2*h))/(12*h)
    fderr=near(source,fd,'independent actual scalar finite difference',1e-12)
    # Scoped complete homogeneous INTERNAL-clock bound at the owned copy-call length88.
    # No claim of replaying that emitted word or proving its physical admission.
    N=88;x=Fraction(2,55);q=x**N/math.factorial(N)
    A1=Fraction(176,359)/(1-x*x)*q/(1-q)**2
    heatbound=2*float(A1) # exact endpoint derivative norm 2
    # Strict rational separation, not comparison of rounded source values.
    pl,pu=Fraction(8,13),Fraction(13,21)
    source_lower=16*dinput*Fraction(1,2**20)*(1-4*pu**9)*pl**9*Fraction(39,50)
    require(pl*pl+pl-1<0<pu*pu+pu-1 and Fraction(39,50)**2<pl,
            'exact Golden and sqrt Golden enclosure')
    require(source_lower>Fraction(1,10**6) and 2*A1<source_lower/10,
            'rational full heat bound cannot cancel the original source')
    return {'AF_old_sizes':[3,2],'AF_new_sizes':list(inc.new),
            'AF_GNS_dimension_without_spectators':int(regular.shape[0]),
            'original_spin_times_oldRIGHT':spectator,'full_GNS_dimension':int(regular.shape[0])*spectator,
            'full_initial_rank':dinput,'GNS_compression_error':e,'GNS_first_derivative_error':de,
            'archive_commutator_error':float(maxerr),'true_GNS_leakage_norm':float(la.norm(leakage,2)),'cold':C,'full_return_source':source,
            'normalized_loop_source':lam,'finite_difference_error':fderr,
            'owned_88_call_heat_bound_consumed_not_replayed':heatbound,
            'strict_return_source_lower_bound':str(source_lower),
            'arbitrary_physical_clock_not_covered':True,
            'source_is_not_a_GR_root_test':True}

def cumulative_source_control():
    inc1=Inclusion((1,1),4);inc2=Inclusion(inc1.new,4)
    L1,dL1,C1,dC1=inc1.loops(.29);L2,dL2,C2,dC2=inc2.loops(.37)
    V1=inc2.embed(L1);V=[L2[b]@V1[b] for b in range(2)]
    def compress(xs):
        es=inc1.expectation(inc2.expectation(xs))
        return la.block_diag(*es)
    K=compress(V);s=C1*C2
    near(K,s*np.eye(2),'two-level actual AF canonical return')
    lam1=-2*dC1/C1;lam2=-2*dC2/C2;Lam=lam1+lam2
    z=2**-20;D=(1-z)*np.eye(2)+z*K.conj().T@K;R=la.inv(D)
    w=z*np.trace(K.conj().T@K@R).real
    def covector(dK):return -2*z*np.trace(R@K.conj().T@dK).real/(w*Lam)
    rng=np.random.default_rng(291026);tests=[]
    for j,inc,L in [(1,inc1,L1),(2,inc2,L2)]:
        X=[]
        for dim in inc.new:
            H=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
            H=(H-H.conj().T);H/=la.norm(H,2);X.append(H)
        Xbar=inc.twirl(X)
        nu=max(la.norm(X[b]-Xbar[b],2) for b in range(2))
        def deriv(xs):
            dlocal=[xs[b]@L[b] for b in range(2)]
            if j==1:return compress([L2[b]@inc2.embed(dlocal)[b] for b in range(2)])
            return compress([dlocal[b]@V1[b] for b in range(2)])
        source=covector(deriv(X));controlled=covector(deriv(Xbar))
        sbefore=C1 if j==1 else s
        budget=2*nu/(sbefore*Lam)
        require(abs(source-controlled)<=budget+1e-11,'full source defect amplification bound')
        tests.append({'stage':j,'actual_residual':source-controlled,'proved_bound':budget,'operator_defect':nu})
    # Needed field source is not twirled away: both loop angles remain.
    dV=[dL2[b]@V1[b]+L2[b]@inc2.embed(dL1)[b] for b in range(2)]
    near(covector(compress(dV)),1.,'actual linked scalar field derivative retains unit normalized gain')
    return {'old_sizes':[1,1],'intermediate_sizes':list(inc1.new),'final_sizes':list(inc2.new),
            'prefix_colds':[C1,C2],'real_Lambda':Lam,'source_defect_controls':tests,
            'only_genuine_compatibility_errors_are_bounded':True}

def main():
    out={'input_commit':'3ba25a162a7160c9a5c7692f19e5d8a8b9bf52e9',
         'native_closed_memory':exact_sourcei_control(),
         'full_archive_domain':algebra_domain_controls(),
         'actual_canonical_archive_compatibility':actual_input_compatibility(),
         'canonical_AF_source':canonical_source_control(),
         'cumulative_source':cumulative_source_control()}
    out.update({'checks':COUNT,'status':'PASS_ARCHIVE_ALGEBRA_DOMAIN_AND_SOURCE_CONTROLS',
                'GR_closed':False,'copy_uniform_from_full_archive_transparency':True,
                'full_archive_transparency_from_D0_closure':False,
                'physical_task_selection_proved':False,'original_native_88_call_replayed':False,
                'all_independent_binary_compiler_rows_replayed':False,'Lean_or_CI_run':False,
                'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()
