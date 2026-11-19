#!/usr/bin/env python3
"""Original full128: invariant preparation, retained reversal, paid boundary,
and a noncommuting finite Golden-normalizer source. Author checks only.

Run in the repository, or from the delivery ZIP containing inputs/native_input.py.
No assert is used: python -O performs exactly the same tests. Large-lattice,
physical Book Info, independent review, and GR closure are NOT asserted.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import solve

INPUT_PATH = '02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py'
INPUT_BLOB = 'ee8de4635d24c668949ac9a0186616ab7d59f2ed'
CHECKS: list[str] = []


def require(ok: bool, name: str) -> None:
    if not bool(ok):
        raise ArithmeticError(name)
    CHECKS.append(name)


def adj(a):
    return a.conj().T


def herm(a):
    return (a + adj(a)) / 2


def tr(a):
    t = np.trace(a)
    if abs(t.imag) > 2e-9 * max(1.0, abs(t.real)):
        raise ArithmeticError('unexpected complex trace')
    return float(t.real)


def vec(a):
    return a.reshape(-1, order='F')


def unvec(v):
    return v.reshape(16, 16, order='F')


def load_native():
    here = Path(__file__).resolve()
    candidates = [p / INPUT_PATH for p in here.parents]
    candidates.append(here.parent / 'inputs/native_input.py')
    found = next((p for p in candidates if p.is_file()), None)
    if found is None:
        raise FileNotFoundError('Pinned native source absent; use repository or complete ZIP')
    data = found.read_bytes()
    sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    require(sha == INPUT_BLOB, 'unchanged original native input Git blob')
    spec = importlib.util.spec_from_file_location('native_input', found)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def exact_algebra():
    # These are algebraic controls of the general theorem, not new native gates.
    d = 3
    I = sp.eye(d)
    q = sp.Rational(1, 3)
    def recycle(x):
        return q*x + (1-q)*sp.trace(x)*I/d
    E = [sp.zeros(d) for _ in range(d*d)]
    for n, e in enumerate(E):
        e[n//d, n%d] = 1
    def generator_matrix(D):
        Delta = D*D
        return sp.Matrix.hstack(*[sp.Matrix(list(recycle(D*e*D)-(Delta*e+e*Delta)/2)) for e in E])
    D = sp.diag(1, -2, 3)
    Delta = D*D
    rho = Delta.inv()/sp.trace(Delta.inv())
    require(recycle(D*rho*D)-(Delta*rho+rho*Delta)/2 == sp.zeros(d),
            'exact indefinite-Dirac inverse-square stationary state')
    require(len(generator_matrix(D).nullspace()) == 1,
            'exact regular algebra control: one-dimensional fixed space')
    Ds = sp.diag(0, 0, 3)
    ker = generator_matrix(Ds).nullspace()
    require(len(ker) == 4 and all(all(v[j] == 0 for j in [2,5,6,7,8]) for v in ker),
            'exact singular control: all and only the full two-dimensional dark algebra')
    H = sp.Matrix([[0,1,0],[1,1,1],[0,1,0]])
    t = sp.symbols('t', real=True)
    dt = (D+t*H)**2
    iv = Delta.inv(); div = -iv*(D*H+H*D)*iv
    drho = div/sp.trace(iv)-iv*sp.trace(div)/sp.trace(iv)**2
    require(sp.trace(drho) == 0, 'exact invariant-preparation derivative has zero trace')
    fixed_jet = recycle(H*rho*D+D*drho*D+D*rho*H) - ((D*H+H*D)*rho+Delta*drho+drho*Delta+rho*(D*H+H*D))/2
    require(fixed_jet == sp.zeros(d), 'exact full differentiated native-form stationary equation')
    frozen = recycle(H*rho*D+D*rho*H)-((D*H+H*D)*rho+rho*(D*H+H*D))/2
    require(frozen != sp.zeros(d), 'hostile frozen-preparation derivative is not stationary')
    # C_D inverse remains bounded even when D has both signs.
    vals = [sp.Rational(1),sp.Rational(-2),sp.Rational(3)]
    cs = [(x/y+y/x)/2 for x in vals for y in vals]
    require(all(abs(c) >= 1 for c in cs), 'exact signed Sylvester ratio bound')
    # Finite n=2 normalizer identity, noncommuting rational example.
    B = [sp.eye(2)/sp.sqrt(2), sp.Matrix([[0,1],[1,0]])/sp.sqrt(2)]
    D2 = sp.diag(1,2); Del = D2*D2
    T = lambda X: sum((b*X*b for b in B),sp.zeros(2))
    eta, eps = sp.symbols('eta eps', real=True)
    c = 1-eta
    Lop = lambda X: eta*D2*T(X)*D2-(Del*X+X*Del)/2
    N2 = sp.eye(2)+2*eps*Lop(sp.eye(2))+eps**2*Lop(Lop(sp.eye(2)))
    Nc = (sp.eye(2)-c*eps*Del)**2
    correction = -c*eta*eps**2*D2*(T(Del)-Del)*D2
    require((N2-Nc-correction).applyfunc(sp.simplify) == sp.zeros(2),
            'exact two-round noncommuting normalizer correction')
    diss = sp.trace(Del*(Del-T(Del)))
    norms = sum(sp.trace((b*Del-Del*b).T*(b*Del-Del*b)) for b in B)/2
    require(sp.simplify(diss-norms) == 0 and diss > 0,
            'exact recycling Dirichlet energy and strict noncommuting control')
    require(sp.simplify(sp.trace(N2-Nc)-c*eta*eps**2*diss) == 0,
            'exact normalizer trace correction keeps its positive coefficient')
    return {'regular_fixed_dimension':1,'singular_fixed_dimension':4,
            'rational_noncommuting_Dirichlet_energy':str(diss)}


def exact_native():
    # The literal CAR order, actual L4 Fourier phases, and role-1 boost.
    r = sp.symbols('r', real=True)
    I = sp.eye(16); order = (0,2,3,1); creators = []
    for role in range(4):
        C = sp.zeros(16)
        for bits in range(16):
            if not (bits>>role)&1:
                C[bits|(1<<role),bits] = (-1)**sum((bits>>j)&1 for j in order[:order.index(role)])
        creators.append(C)
    gen = creators[0]*creators[1].T+creators[1]*creators[0].T
    nu = sp.Rational(3,5)
    U = I + (2*r*r/(1-r*r))*gen**2+(2*r/(1-r*r))*gen
    require((U.subs(r,sp.Rational(1,9))-I-sp.Rational(1,40)*gen**2-sp.Rational(9,40)*gen) == sp.zeros(16),
            'exact native boost theta=log(5/4)')
    A = sp.zeros(16)
    for j,(C,phase) in enumerate(zip(creators,(sp.I,sp.I,-1,-sp.I))):
        X = nu*C*(U if j==1 else I)*phase
        A += X+X.conjugate().T-nu*C-nu*C.T
    A = (A/16).applyfunc(lambda x:sp.cancel(sp.expand_complex(x)))
    Delta = (A*A).applyfunc(lambda x:sp.factor(sp.expand_complex(x)))
    require((A.conjugate().T-A).applyfunc(sp.cancel) == sp.zeros(16), 'exact original full16 native A is Hermitian')
    mu = sp.factor(sp.trace(Delta)/16)
    var = sp.factor(sp.trace(Delta*Delta)/16-mu**2)
    dd = sp.factor(mu**2-var)
    ident = (Delta*Delta-2*mu*Delta+dd*I).applyfunc(lambda x:sp.factor(sp.expand_complex(x)))
    require(ident == sp.zeros(16), 'all256 exact entries of native quadratic minimal polynomial')
    inv = (2*mu*I-Delta)/dd
    require((Delta*inv-I).applyfunc(lambda x:sp.factor(sp.expand_complex(x))) == sp.zeros(16), 'all256 exact native inverse entries')
    harmonic = sp.factor(dd/mu)
    r0 = sp.Rational(1,9)
    require(harmonic.subs(r,r0) == sp.Rational(69399,5030720), 'exact native harmonic-energy value')
    dh = sp.factor(sp.diff(harmonic,r))
    require(dh.subs(r,r0) == -sp.Rational(20040939,9885993640), 'exact native proper-link harmonic-energy source')
    require(Delta.subs(r,0) == sp.Rational(9,640)*I, 'exact scalar base of same proper-link chart')
    D1 = Delta.diff(r).subs(r,0)
    b = sp.Rational(4,5)
    xi = []; zz = []
    for C in creators:
        xi.extend([C+C.T,sp.I*(C-C.T)]);zz.append(I-2*C*C.T)
    T0 = lambda X: ((1+b)**2/4)*X+(nu**2/16)*sum((x*X*x for x in xi),sp.zeros(16))+((1-b)**2/16)*sum((x*X*x for x in zz),sp.zeros(16))
    diss2 = sp.simplify(sp.trace(D1*(D1-T0(D1))))
    norm2 = sp.simplify(sp.trace((D1-T0(D1))**2))
    require(diss2 == sp.Rational(2349,64000000), 'exact native boost-squared Dirichlet coefficient')
    require(norm2 == sp.Rational(22761,6400000000), 'exact native recycling-defect squared norm')
    p = (sp.sqrt(5)-1)/2; eps=4*p*p; eta=p;c=1-p;z=sp.Rational(1,2**20)
    lam=sp.Rational(9,640); l=sp.symbols('l',real=True)
    NN=(1-c*eps*l)**2; GG=(1-eps*l/2)**4; QQ=(1-z)*NN+z*GG
    HH=1/NN-(1-z)/QQ
    h0=HH.subs(l,lam); hd=sp.diff(HH,l).subs(l,lam)
    q2=(-1/NN**2+(1-z)**2/QQ**2).subs(l,lam)
    coeff=128*(c*eta*eps**2*diss2*(h0+lam*hd)+q2*(c*eta*eps**2*lam)**2*norm2/2)
    coeff=sp.cancel(sp.radsimp(coeff))
    lo=sp.Rational(2418,10**12);hi=sp.Rational(2419,10**12)
    require(sp.ask(sp.Q.positive(coeff-lo)) is True and sp.ask(sp.Q.positive(hi-coeff)) is True,
            'exact Q(sqrt5) enclosure of positive full finite Book Hessian defect')
    require((1+(3+b)/4)/2 == sp.Rational(39,40), 'native unshifted-half recycling contraction bound 39/40')
    return {'r':r,'A':A,'Delta':Delta,'harmonic':harmonic,'dh':dh,
            'A0':np.asarray(A.subs(r,r0),dtype=complex),
            'dA0':np.asarray(A.diff(r).subs(r,r0),dtype=complex),
            'output':{'mean_Delta_at_r=1/9':str(mu.subs(r,r0)),
                      'harmonic_energy':'69399/5030720',
                      'harmonic_energy_r_source':'-20040939/9885993640',
                      'Dirichlet_r2_coefficient':str(diss2),
                      'finite_Book_r2_defect':str(sp.N(coeff,32)),
                      'finite_Book_r2_exact_enclosure':[str(lo),str(hi)],
                      'finite_Book_r2_exact_Qsqrt5':str(coeff),
                      'recycling_q_bound':'39/40'}}


def numerical_native(m, exact):
    r=1/9; theta=2*np.arctanh(r); jac=2/(1-r*r)
    K,dKtheta=m.native(theta);dK=dKtheta*jac
    I=np.eye(16,dtype=complex);A=exact['A0'];dA=exact['dA0']
    Delta=herm(A@A);dDelta=herm(dA@A+A@dA)
    eps=4*m.P**2
    require(np.linalg.norm(Delta-(I-K[0])/(2*m.P**2))<2e-15, 'original native K00 equals I-epsilon Delta/2')
    require(np.linalg.norm(dDelta+dK[0]/(2*m.P**2))<2e-14, 'original native blank-corner first jet')
    inv=np.linalg.inv(Delta);zz=tr(inv);rho=inv/zz
    dinv=-inv@dDelta@inv;drho=dinv/zz-inv*tr(dinv)/zz**2
    # Weighted-reversal phases are those of the ACTUAL Walsh rows.
    signs=[]
    for h in range(128):
        row=h//2;lab=row//2;coef=row%2
        signs.append((-1)**((lab>>1)&1) if coef==0 else 1)
    require(max(np.linalg.norm(A@k-s*adj(k)@A) for k,s in zip(K,signs))<3e-15,
            'all128 exact-owner weighted-reversal identities, numerical native realization')
    require(max(np.linalg.norm(dA@k+A@dk-s*(adj(dk)@A+adj(k)@dA)) for k,dk,s in zip(K,dK,signs))<2e-14,
            'all128 differentiated weighted-reversal identities')
    require(max(np.linalg.norm(A@k-adj(k)@A) for k in K)>1e-4,
            'hostile deletion of anti-Hermitian Walsh phases fails')
    Phi=lambda X:sum((k@X@adj(k) for k in K),np.zeros_like(I))
    Phij=lambda X:sum((dk@X@adj(k)+k@X@adj(dk) for k,dk in zip(K,dK)),np.zeros_like(I))
    require(np.linalg.norm(Phi(rho)-rho)<3e-15, 'same original full128 has inverse-square invariant density')
    require(np.linalg.norm(Phij(rho)+Phi(drho)-drho)<3e-14, 'full field/preparation stationary first jet')
    require(abs(tr(drho))<2e-14 and np.linalg.eigvalsh(rho).min()>0, 'normalized faithful native preparation')
    require(np.linalg.norm(Phij(rho))>1e-6, 'freezing induced preparation misses an actual field source')
    E=sum((adj(k)@k for k in K[1::2]),np.zeros_like(I))
    dE=sum((adj(dk)@k+adj(k)@dk for k,dk in zip(K[1::2],dK[1::2])),np.zeros_like(I))
    kap=tr(rho@E);dkap=tr(drho@E+rho@dE)
    require(np.linalg.norm(E-m.P*eps*Delta)<3e-15,'actual all-port1 effect, including orphan outcome')
    require(abs(tr(rho@Delta)-float(exact['harmonic'].subs(exact['r'],sp.Rational(1,9))))<3e-16,
            'native stationary energy agrees with exact rational value')
    require(abs(dkap-m.P*eps*float(exact['dh'].subs(exact['r'],sp.Rational(1,9))))<3e-14,
            'native stationary count source agrees with exact rational derivative')
    # Complete two-round tape. No paths are dropped or renormalized.
    probs=np.zeros((128,128));jets=probs.copy();frozen=probs.copy();flat=probs.copy()
    word_gap=0.0
    for j in range(128):
        for i in range(128):
            w=K[j]@K[i];dw=dK[j]@K[i]+K[j]@dK[i]
            probs[j,i]=tr(w@rho@adj(w))
            frozen[j,i]=tr(dw@rho@adj(w)+w@rho@adj(dw))
            jets[j,i]=frozen[j,i]+tr(w@drho@adj(w))
            flat[j,i]=tr(w@adj(w))/16
            word_gap=max(word_gap,float(np.linalg.norm(w-K[i]@K[j])))
    require(abs(probs.sum()-1)<3e-14 and abs(jets.sum())<3e-14, 'complete16384-history normalization and derivative')
    require(np.max(abs(probs-probs.T))<3e-17, 'complete native two-round stationary reversal law')
    require(np.max(abs(jets-jets.T))<3e-15, 'complete reversal first jet includes endogenous preparation')
    require(np.max(abs(frozen-frozen.T))>1e-8, 'frozen-preparation reversal-source hostile control')
    require(np.max(abs(flat-flat.T))>1e-10, 'flat input cannot replace the native invariant input')
    require(word_gap>0.005, 'reversal probabilities retain noncommuting memory words')
    pair_cost=(1+np.arange(128)%2)[:,None]+(1+np.arange(128)%2)[None,:]
    require(abs(float((pair_cost*probs).sum())-2*(1+kap))<3e-14,'complete stationary two-round actual paid cost')
    require(abs(float((pair_cost*jets).sum())-2*dkap)<3e-14,'complete paid-cost first jet from all histories')
    # Full input law and complete-history boundary by a native Poisson equation.
    S=sum((np.kron(k.conj(),k) for k in K),np.zeros((256,256),complex))
    dS=sum((np.kron(dk.conj(),k)+np.kron(k.conj(),dk) for k,dk in zip(K,dK)),np.zeros_like(S))
    Pproj=np.outer(vec(I),vec(rho).conj());dP=np.outer(vec(I),vec(drho).conj())
    MM=np.eye(256)-adj(S)+Pproj
    Yv=solve(MM,vec(E-kap*I));Y=herm(unvec(Yv))
    dY=herm(unvec(solve(MM,vec(dE-dkap*I)-(-adj(dS)+dP)@Yv)))
    require(np.linalg.norm(Y-unvec(adj(S)@vec(Y))-E+kap*I)<3e-13,'exact-equation native paid Poisson corrector')
    require(abs(tr(rho@Y))<3e-13 and abs(tr(drho@Y+rho@dY))<3e-12,'Poisson gauge and full moving-gauge derivative')
    R0=np.zeros_like(I);R0[0,0]=1
    dR0=np.zeros_like(I);dR0[0,3]=dR0[3,0]=1
    boundaries={}
    for n in [1,2,17,64]:
        state=R0.copy();dstate=np.zeros_like(I);cost=0.0;dcost=0.0
        count=np.zeros_like(I)
        for _ in range(n):
            cost+=1+tr(state@E);dcost+=tr(dstate@E+state@dE)
            dstate=unvec(dS@vec(state)+S@vec(dstate));state=unvec(S@vec(state))
            count=E+unvec(adj(S)@vec(count))
        val=n*(1+kap)+tr(R0@Y)-tr(state@Y)
        jet=n*dkap+tr(R0@dY)-tr(dstate@Y+state@dY)
        require(abs(val-cost)<3e-11,f'full actual {n}-round port cost equals rate plus both boundaries')
        require(abs(jet-dcost)<3e-10,f'full actual {n}-round port-cost-source identity')
        prep=tr(dR0@count)
        rhs=tr(dR0@Y)-tr(unvec(np.linalg.matrix_power(S,n)@vec(dR0))@Y)
        require(abs(prep-rhs)<3e-11,f'independent initial preparation source at horizon {n}')
        boundaries[str(n)]={'cost':cost,'field_source':dcost,'initial_preparation_source':prep}
    require(abs(boundaries['64']['initial_preparation_source'])>1e-3,
            'erasing the actual upstream paid boundary loses a nonzero source')
    long=unvec(np.linalg.matrix_power(S,16384)@vec(R0))
    require(np.linalg.norm(long-rho)<1e-7,'native finite repeated-run marginal reaches invariant preparation')
    boundary_limit=tr(dR0@Y)
    require(boundary_limit>0.3,'nonzero asymptotic absolute initial-preparation source persists')
    # A retained external reference: this is a marginal test, not record deletion.
    C=np.zeros((16,2),complex);C[0,0]=1/np.sqrt(2);C[3,1]=1/np.sqrt(2)
    gram=sum((adj(k@C)@(k@C) for k in K),np.zeros((2,2),complex))
    require(np.linalg.norm(gram-adj(C)@C)<3e-14,'unconditional retained reference Gram is unchanged')
    # Actual N_j rows, and exact finite n=2 normalizer beyond the scalar shell.
    Ai=np.linalg.inv(A);Ns=[-Ai@adj(k)/(2*m.P*np.sqrt(m.P)) for k in K[1::2]]
    T=lambda X:sum((adj(n)@X@n for n in Ns),np.zeros_like(I))
    require(np.linalg.norm(T(I)-I)<4e-14 and np.linalg.norm(sum((n@adj(n) for n in Ns),np.zeros_like(I))-I)<4e-14,
            'native recycling is both unital and trace preserving')
    energy=tr(Delta@(Delta-T(Delta)))
    comm_energy=sum(np.linalg.norm(n@Delta-Delta@n)**2 for n in Ns)/2
    require(abs(energy-comm_energy)<2e-17 and energy>1e-8,'actual native noncommuting Dirichlet energy')
    mark=2*np.log(1/m.P);eta=m.P;c=1-eta
    weights=np.exp(-mark*(np.arange(128)%2))
    N1=m.cp_star(K,I,weights);N2=m.cp_star(K,N1,weights)
    Nc=(I-c*eps*Delta)@(I-c*eps*Delta)
    correction=-c*eta*eps**2*A@(T(Delta)-Delta)@A
    require(np.linalg.norm(N2-Nc-correction)<5e-14,'actual full128 two-round Golden normalizer correction')
    require(np.linalg.norm(N2-Nc)>1e-6,'commuting spectral replacement fails on actual proper-link input')
    require(abs(tr(N2-Nc)-c*eta*eps**2*energy)<5e-14,'actual normalizer trace has derived positive defect')
    # Independent full-determinant check of the exact scalar-base Hessian defect.
    defect_secants={}
    for step_r in [0.02,0.01]:
        vals=[]
        for rr in [step_r,-step_r]:
            kk,ddk=m.native(2*np.arctanh(rr))
            de=herm((I-kk[0])/(2*m.P**2))
            ns,unused,ww=m.build(kk,ddk,2,mark)
            nc=(I-c*eps*de)@(I-c*eps*de)
            aa=kk[0]@kk[0];zero=np.zeros_like(I)
            jj,_=m.book(ns[-1],zero,aa,zero);jc,_=m.book(nc,zero,aa,zero)
            vals.append(jj-jc)
        estimate=sum(vals)/(2*step_r**2)
        expected=float(exact['output']['finite_Book_r2_defect'])
        require(abs(estimate-expected)<expected*0.003,
                f'independent full native Book determinant secant at r={step_r}')
        defect_secants[str(step_r)]=estimate
    # Independent finite-difference controls of actual field sources.
    step=2e-5
    def field_values(rr):
        kk,_=m.native(2*np.arctanh(rr));delv=herm((I-kk[0])/(2*m.P**2))
        iv=np.linalg.inv(delv);rh=iv/tr(iv)
        ef=sum((adj(k)@k for k in kk[1::2]),np.zeros_like(I))
        return rh,tr(rh@ef)
    samples=[field_values(r+j*step) for j in [-2,-1,1,2]]
    fd=(-samples[3][0]+8*samples[2][0]-8*samples[1][0]+samples[0][0])/(12*step)
    fdk=(-samples[3][1]+8*samples[2][1]-8*samples[1][1]+samples[0][1])/(12*step)
    require(np.linalg.norm(fd-drho)<2e-9,'five-point independent native preparation derivative')
    require(abs(fdk-dkap)<2e-10,'five-point independent native price-rate derivative')
    return {'native_r':r,'native_theta':theta,'invariant_density_extremes':np.linalg.eigvalsh(rho)[[0,-1]].tolist(),
            'stationary_surplus_rate':kap,'stationary_surplus_rate_r_source':dkap,
            'two_round_reversal_max_error':float(np.max(abs(probs-probs.T))),
            'two_round_reversal_jet_max_error':float(np.max(abs(jets-jets.T))),
            'frozen_preparation_reversal_jet_defect':float(np.max(abs(frozen-frozen.T))),
            'noncommuting_word_gap':word_gap,'paid_boundaries':boundaries,
            'asymptotic_initial_preparation_source':boundary_limit,
            'finite_16384_round_marginal_error':float(np.linalg.norm(long-rho)),
            'native_Dirichlet_energy':energy,'full_Book_defect_secants':defect_secants,'two_round_normalizer_nonspectral_norm':float(np.linalg.norm(N2-Nc))}


def main():
    m=load_native()
    algebra=exact_algebra();ex=exact_native();numeric=numerical_native(m,ex)
    result={'status':'PASS','input_commit':'dda8f5d8ce5950cce4278b1f5b7d63f826b2e8f2',
            'input_blob':INPUT_BLOB,'check_count':len(CHECKS),'checks':CHECKS,
            'exact_algebra':algebra,'exact_native':ex['output'],'native_diagnostic':numeric,
            'scope':{'native_invariant_preparation':'finite theorem under explicit recycling assumptions',
                     'all_horizon_reversal':'analytical with stationary data input',
                     'paid_initial_boundary':'retained, not assumed zero',
                     'valued_cost_component':'original port charges only; other actual charges and Info not assigned',
                     'native_Book_Info_selected':False,'primary_full42_price_root':False,
                     'independent_review':False,'uniform_mesh_gap_proved':False,'GR_closed':False}}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
