#!/usr/bin/env python3
"""Paid initial-state Euler equations with the complete coherent native archive.

Author checks. Finite all128 diagnostics use the original CAR16 Fourier block,
not the full spatial all42 programme. No physical Book Info is selected.
Run with OPENBLAS_NUM_THREADS=1. No assert: optimized mode keeps every check.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import expm, solve

ELL = float(np.log((1 + np.sqrt(5.0)) / 2))
INPUT_BLOB = 'ee8de4635d24c668949ac9a0186616ab7d59f2ed'
CHECKS: list[str] = []

def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    CHECKS.append(label)

def adj(x): return x.conj().T

def herm(x): return (x + adj(x)) / 2

def vec(x): return x.reshape(-1, order='F')

def mat(x, d): return x.reshape(d, d, order='F')

def tr(x):
    v = np.trace(x)
    if abs(v.imag) > 1e-9 * max(1., abs(v.real)):
        raise ArithmeticError('non-real trace')
    return float(v.real)

def load_native():
    here = Path(__file__).resolve()
    rp = '02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/inputs/native_input.py'
    candidates = [p / rp for p in here.parents] + [here.parent / 'inputs/native_input.py']
    path = next((p for p in candidates if p.is_file()), None)
    if path is None:
        raise FileNotFoundError('Use the complete ZIP or the source repository')
    raw = path.read_bytes()
    sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(sha == INPUT_BLOB, 'immutable original full128 native input blob')
    spec = importlib.util.spec_from_file_location('native_input', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def entropy_log(a, floor=1e-14):
    v, u = np.linalg.eigh(herm(a))
    if v.min() < -1e-9:
        raise ArithmeticError('nonpositive density outside numerical tolerance')
    mask = v > floor
    ent = -float(np.dot(v[mask], np.log(v[mask]))) / ELL
    log = (u[:,mask] * np.log(v[mask])) @ adj(u[:,mask])
    return ent, log, v

def root(a):
    v, u = np.linalg.eigh(herm(a))
    if v.min() < -1e-9:
        raise ArithmeticError('nonpositive matrix')
    return (u * np.sqrt(np.maximum(v, 0))) @ adj(u)

def gibbs(y):
    w, u = np.linalg.eigh(herm(y))
    x = np.exp(-ELL * (w - w.min()))
    return (u * (x / x.sum())) @ adj(u)

def apply(t, x): return mat(t @ vec(x), x.shape[0])

def extend(t, g, d):
    r = g.shape[0] // d
    return np.einsum('abij,irjs->arbs', t.reshape(d,d,d,d,order='F'),
                     g.reshape(d,r,d,r), optimize=True).reshape(d*r,d*r)

def pure(c):
    v = c.reshape(-1)
    return np.outer(v, v.conj())

def choi(t, d):
    return herm(t.reshape(d,d,d,d,order='F').transpose(2,0,3,1).reshape(d*d,d*d))

def partial_out(x, d):
    return np.einsum('iaja->ij', x.reshape(d,d,d,d), optimize=True)

def power_jet(t, dt, n):
    a, da = t.copy(), dt.copy()
    out, dout = np.eye(len(t),dtype=complex), np.zeros_like(t)
    while n:
        if n & 1:
            dout = da @ out + a @ dout
            out = a @ out
        n >>= 1
        if n:
            da = da @ a + a @ da
            a = a @ a
    return out, dout

def field(m, r):
    d = 16; eye = np.eye(d,dtype=complex)
    k, dk = m.native(2*np.arctanh(r)); dk = dk * (2/(1-r*r))
    t = sum((np.kron(x.conj(),x) for x in k), np.zeros((d*d,d*d),complex))
    dt = sum((np.kron(dx.conj(),x)+np.kron(x.conj(),dx) for x,dx in zip(k,dk)),np.zeros_like(t))
    delta = herm((eye-k[0])/(2*m.P**2)); ddelta = herm(-dk[0]/(2*m.P**2))
    inv = np.linalg.inv(delta); dinv = -inv @ ddelta @ inv
    stationary = inv/tr(inv); ds = dinv/tr(inv)-inv*tr(dinv)/tr(inv)**2
    e = sum((adj(x)@x for x in k[1::2]),np.zeros_like(eye))
    de = sum((adj(dx)@x+adj(x)@dx for x,dx in zip(k[1::2],dk[1::2])),np.zeros_like(eye))
    rate = tr(stationary@e); drate = tr(ds@e+stationary@de)
    pp = np.outer(vec(eye),vec(stationary).conj())
    dpp = np.outer(vec(eye),vec(ds).conj())
    mm = np.eye(d*d)-adj(t)+pp
    yv = solve(mm,vec(e-rate*eye))
    y = herm(mat(yv,d))
    dy = herm(mat(solve(mm,vec(de-drate*eye)-(-adj(dt)+dpp)@yv),d))
    return dict(d=d,I=eye,K=k,dK=dk,T=t,dT=dt,rho=stationary,drho=ds,
                E=e,dE=de,rate=rate,drate=drate,Y=y,dY=dy)

def horizon(f, n):
    t, dt = power_jet(f['T'],f['dT'],n)
    y = f['Y']-herm(apply(adj(t),f['Y']))
    dy = f['dY']-herm(apply(adj(dt),f['Y'])+apply(adj(t),f['dY']))
    j = choi(t,f['d']); hj = root(j)
    return dict(n=n,T=t,dT=dt,Y=y,dY=dy,J=j,HJ=hj)

def free_value_gradient(h, rho):
    d = len(rho); hj = h['HJ']
    g = herm(hj @ np.kron(rho.T,np.eye(d)) @ hj)
    ent, log, vs = entropy_log(g)
    grad = h['Y']+partial_out(hj@(log+np.eye(d*d))@hj,d).T/ELL
    return tr(rho@h['Y'])-ent, herm(grad), float(vs.min())

def free_minimum(h, start, tol=3e-10, max_steps=160):
    rho = start.copy()
    for it in range(max_steps):
        value, grad, floor = free_value_gradient(h,rho)
        gp = grad-np.trace(grad)*np.eye(len(rho))/len(rho)
        residual = float(np.linalg.norm(gp))
        if residual < tol: break
        _, logr, _ = entropy_log(rho)
        step = ELL
        for attempt in range(15):
            eig, u = np.linalg.eigh(herm(logr-step*gp))
            w = np.exp(eig-eig.max()); trial=(u*(w/w.sum()))@adj(u)
            nv = free_value_gradient(h,trial)[0]
            if nv <= value + 1e-12: break
            step *= .5
        rho = trial
    value, grad, floor = free_value_gradient(h,rho)
    residual=float(np.linalg.norm(grad-tr(grad)*np.eye(len(rho))/len(rho)))
    return rho, dict(value=value,projected_gradient=residual,iterations=it+1,
                     min_input_eigenvalue=float(np.linalg.eigvalsh(rho).min()),min_archive_eigenvalue=floor)

def orbit_value_gradient(h, c, cut='E'):
    d=len(c); rho=c@adj(c)
    if cut=='E':
        g=herm(extend(h['T'],pure(c),d));ent,lg,v=entropy_log(g)
        back=extend(adj(h['T']),lg+np.eye(len(g)),d)
        jc=h['Y']@c+(back@c.reshape(-1)).reshape(c.shape)/ELL
    else:
        out=herm(apply(h['T'],rho));ent,lg,v=entropy_log(out)
        jc=(h['Y']+apply(adj(h['T']),(lg+np.eye(d))/ELL))@c
    a=jc@adj(c)-c@adj(jc)
    return tr(rho@h['Y'])-ent,a,float(v.min())

def envelope_source(f,h,rho):
    c=root(rho)
    g=herm(extend(h['T'],pure(c),f['d']))
    dg=herm(extend(h['dT'],pure(c),f['d']))
    _,lg,v=entropy_log(g)
    return h['n']*f['drate']+tr(rho@h['dY'])+tr(lg@dg)/ELL

def exact_controls():
    p=(sp.sqrt(5)-1)/2
    require(sp.simplify(p+p*p-1)==0,'exact Golden normalization of replacement-channel optimum')
    rstar=sp.diag(sp.Rational(3,4),sp.Rational(1,4))
    e=sp.diag(1,2); rate=sp.trace(rstar*e); y=e-rate*sp.eye(2)
    require(rate==sp.Rational(5,4) and sp.trace(rstar*y)==0,'exact replacement-channel Poisson gauge')
    phi_star=lambda x:sp.trace(rstar*x)*sp.eye(2)
    require(y-phi_star(y)==e-rate*sp.eye(2),'exact replacement-channel paid Poisson equation')
    require(sp.simplify(1/(1+p)-p)==0 and sp.simplify(p/(1+p)-p*p)==0,
            'exact free-spectrum Gibbs optimum is (p,p^2), not invariant (3/4,1/4)')
    require(sp.simplify(p-sp.Rational(3,4))!=0,'dynamical invariant and variational optimum are genuinely different')
    theta=sp.symbols('theta',real=True)
    u=sp.Matrix([[sp.cos(theta),-sp.sin(theta)],[sp.sin(theta),sp.cos(theta)]])
    lam=sp.diag(sp.Rational(3,4),sp.Rational(1,4))
    val=sp.simplify(sp.trace(u*lam*u.T*y))
    require(sp.simplify(sp.diff(val,theta,2).subs(theta,0))==1,'exact fixed-RIGHT orbit minimum has positive second variation')
    require(sp.simplify(sp.diff(val,theta,2).subs(theta,sp.pi/2))==-1,'exact reverse spectral assignment is not the minimum')
    # Rank-capped Gibbs uses r lowest energies; no extra purifying dimension.
    require(sp.simplify((1+p+p*p)-2)==0,'exact rank-two versus rank-three partition distinction')
    ji=sp.Matrix([1,0,0,1])*sp.Matrix([[1,0,0,1]])
    require(ji.rank()==1, 'exact identity-channel Choi is rank one, so the strict-convexity premise is necessary')
    require(sp.trace(lam)==1 and sp.simplify(sp.trace(u*lam*u.T)-1)==0,'exact fixed-RIGHT unitary variation retains trace and eigenvalues')
    return {'replacement_stationary_spectrum':['3/4','1/4'],
            'replacement_cost_rate':'5/4','replacement_Y':['-1/4','3/4'],
            'free_archive_input_spectrum':['p','p^2'],'rank_one_minimum':'lowest Y eigenvector'}

def native_checks(m):
    f=field(m,1/9);d=f['d'];I=f['I'];k=f['K']
    require(np.linalg.norm(sum((adj(x)@x for x in k),np.zeros_like(I))-I)<3e-14,'all128 original outcomes are retained and complete')
    require(np.linalg.norm(apply(f['T'],f['rho'])-f['rho'])<3e-14,'inherited original inverse-energy stationary state')
    require(np.linalg.norm(f['Y']-apply(adj(f['T']),f['Y'])-f['E']+f['rate']*I)<4e-13,'actual paid boundary solves native Poisson equation')
    require(abs(tr(f['rho']@f['Y']))<3e-13,'native Poisson gauge is retained')
    require(abs(f['drate']-tr(f['rho']@f['dE'])-tr(f['Y']@apply(f['dT'],f['rho'])))<3e-12,'stationary-rate adjoint source identity')
    require(np.linalg.norm(f['rho']@f['Y']-f['Y']@f['rho'])>1e-4,'native dynamically invariant input is not a stationary fixed-RIGHT price input in the limit')
    # One-round actual environment Gram vs the system/reference and Choi reductions.
    y,U=np.linalg.eigh(f['Y']);lam=np.array([3/32]*8+[1/32]*8)
    c0=U@np.diag(np.sqrt(lam));rho0=c0@adj(c0)
    psi=np.asarray([x@c0 for x in k]).reshape(128,-1)
    env=psi@adj(psi)
    dual=extend(f['T'],pure(c0),d)
    require(abs(entropy_log(env)[0]-entropy_log(dual)[0])<4e-12,'literal128 coherent record entropy equals joint DATA-RIGHT entropy')
    j=choi(f['T'],d); direct_j=sum((np.outer(vec(x),vec(x).conj()) for x in k),np.zeros_like(j))
    require(np.linalg.norm(j-direct_j)<3e-14,'native Choi index convention independently checks all Kraus columns')
    ch=root(j)@np.kron(rho0.T,I)@root(j)
    require(abs(entropy_log(ch)[0]-entropy_log(env)[0])<4e-12,'linear Choi entropy reduction equals actual complete coherent archive')
    # All128^2 histories on a rank-two reference; no monitored dephasing or postselection.
    c2=U[:,:2]@np.diag(np.sqrt([.75,.25]))
    words=(k[:,None,:,:]@k[None,:,:,:]).reshape(128**2,d,d)
    states=(words@c2).reshape(128**2,-1)
    direct_sr=states.T@states.conj()
    h2=horizon(f,2); dual_sr=extend(h2['T'],pure(c2),d)
    require(np.linalg.norm(direct_sr-dual_sr)<6e-14,'all16384 ordered histories reproduce full DATA-RIGHT state')
    prob=np.sum(abs(states)**2,axis=1)
    cost=(2+(np.arange(128)%2)[:,None]+(np.arange(128)%2)[None,:]).reshape(-1)
    rho2=c2@adj(c2)
    require(abs(float(prob.sum())-1)<4e-14,'all16384 probabilities sum to one')
    require(abs(float(prob@cost)-(2*(1+f['rate'])+tr(rho2@h2['Y'])))<6e-13,'all16384 paid histories agree with complete finite cost operator')
    require(abs(entropy_log(direct_sr)[0]-entropy_log(dual_sr)[0])<5e-12,'full two-round coherent entropy, not pointer Shannon entropy')
    pointer=-float(np.dot(prob[prob>0],np.log(prob[prob>0])))/ELL
    require(abs(pointer-entropy_log(dual_sr)[0])>1e-3,'hostile substitution of pointer entropy changes the price')
    # Native finite-horizon exact equations and long-horizon controls.
    limit_entropy=entropy_log(f['rho'])[0];right_entropy=entropy_log(np.diag(lam))[0]
    fixed_limit=float(lam@y)-limit_entropy-right_entropy
    sig=gibbs(f['Y'])
    logsig=entropy_log(sig)[1]; logstat=entropy_log(f['rho'])[1]
    gapval=tr(f['rho']@f['Y'])-entropy_log(f['rho'])[0]-(tr(sig@f['Y'])-entropy_log(sig)[0])
    rel=tr(f['rho']@(logstat-logsig))/ELL
    require(abs(gapval-rel)<2e-13 and rel>1e-3,'exact-form Gibbs relative-entropy gap tested on original nonstationary price input')
    free_limit=tr(sig@f['Y'])-entropy_log(sig)[0]-limit_entropy
    horizons={};samples={}
    for n in [64,512,2048,8192]:
        h=horizon(f,n);samples[n]=h
        jmin=float(np.linalg.eigvalsh(h['J']).min())
        require(jmin>1e-9,f'faithful Choi numerical diagnostic at original horizon {n}')
        ev,ag,emin=orbit_value_gradient(h,c0,'E')
        erv,rag,_=orbit_value_gradient(h,c0,'ER')
        out=herm(apply(h['T'],rho0));sr=herm(extend(h['T'],pure(c0),d))
        mi=entropy_log(out)[0]+right_entropy-entropy_log(sr)[0]
        require(abs(ev-erv+right_entropy-mi)<3e-12,f'exact archive-cut mutual-information identity at {n}')
        require(mi>-1e-9,f'full retained mutual information nonnegative at {n}')
        require(abs(tr(sr)-1)<5e-11,f'full coherent retained normalization at {n}')
        horizons[str(n)]={'fixed_RIGHT_price_minus_paid_rate':ev,'fixed_RIGHT_limit':fixed_limit,
                         'limiting_input_gradient_norm':float(np.linalg.norm(ag)),
                         'mutual_information':mi,'Choi_min_eigenvalue':jmin,
                         'joint_state_min_eigenvalue':emin}
    require(horizons['8192']['mutual_information']<3e-7,'native long-horizon cut difference reduces to fixed RIGHT entropy')
    require(abs(horizons['8192']['fixed_RIGHT_price_minus_paid_rate']-fixed_limit)<3e-7,'native full fixed-RIGHT price approaches derived boundary minimum')
    require(horizons['64']['mutual_information']>1,'deleting finite correlations is an invalid finite-horizon shortcut')
    # Exact finite convex input equation: numerical minimizer, not interval certification.
    h=samples[2048];rho,info=free_minimum(h,sig)
    require(info['projected_gradient']<2e-8,'all255 free input Euler coordinates solve the finite native entropy equation numerically')
    require(info['min_input_eigenvalue']>.02,'finite optimized input stays interior')
    value,grad,_=free_value_gradient(h,rho)
    require(np.linalg.norm(rho-f['rho'])>1e-2,'finite price minimizer is not the dynamical stationary density')
    require(value<free_value_gradient(h,f['rho'])[0]-1e-3,'actual finite coherent price lowers at the optimized input')
    require(np.linalg.norm(rho-sig)<.01,'finite input minimum is near the derived paid-boundary Gibbs state')
    # Check the exact gradient formula on a fully noncommuting trace-zero direction.
    rng=np.random.default_rng(1129);raw=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    x=herm(raw);x-=tr(x)*I/d;x/=np.linalg.norm(x)
    hh=2e-5
    fd=(free_value_gradient(h,rho+hh*x)[0]-free_value_gradient(h,rho-hh*x)[0])/(2*hh)
    require(abs(fd-tr(grad@x))<2e-8,'independent finite-difference full Choi entropy gradient')
    second=(free_value_gradient(h,rho+hh*x)[0]-2*value+free_value_gradient(h,rho-hh*x)[0])/hh**2
    bound=d*float(np.linalg.eigvalsh(h['J']).min())**2/ELL
    require(second>bound and bound>0,'native directional Hessian exceeds proved Choi strong-convexity lower bound')
    # Fixed Schmidt spectrum: true orbit minimization with full entropy, no eigenvalue change.
    c=c0.copy()
    for it in range(130):
        v,a,_=orbit_value_gradient(h,c)
        if np.linalg.norm(a)<1e-8:break
        step=4.
        for attempt in range(14):
            trial=expm(-step*a)@c
            nv=orbit_value_gradient(h,trial)[0]
            if nv<=v-1e-4*step*np.linalg.norm(a)**2+1e-13:break
            step/=2
        c=trial
    orbit_res=float(np.linalg.norm(orbit_value_gradient(h,c)[1]))
    require(orbit_res<3e-8,'actual finite fixed-RIGHT orbit Euler residual is small on every LEFT direction')
    require(np.linalg.norm(adj(c)@c-np.diag(lam))<4e-14,'optimized purification preserves entire specified RIGHT Gram')
    require(orbit_value_gradient(h,c)[0]<orbit_value_gradient(h,c0)[0]-1e-6,'finite mutual information shifts the limiting orbit minimizer')
    gap=float(y[8]-y[7]);hess=2*(lam[0]-lam[-1])*gap
    require(gap>.49 and hess>.06,'actual limiting protected-spectrum minimum has a separated spectral cut')
    # Envelope field derivative includes both paid boundaries and whole entropy.
    source=envelope_source(f,h,rho);dr=2e-4
    vals=[]
    for sign in [-1,1]:
        ff=field(m,1/9+sign*dr);hh=horizon(ff,2048)
        rr,ii=free_minimum(hh,gibbs(ff['Y']),tol=1e-9)
        require(ii['projected_gradient']<3e-8,f'neighboring finite input minimizer at sign {sign}')
        vals.append(2048*(1+ff['rate'])+ii['value'])
    fdsource=(vals[1]-vals[0])/(2*dr)
    require(abs(fdsource-source)<3e-5,'optimized complete-price source matches independent neighboring minimizers')
    asym_source=2048*f['drate']+tr(sig@f['dY'])+tr(entropy_log(f['rho'])[1]@f['drho'])/ELL
    require(abs(source-2048*f['drate'])>1e-3,'erasing paid/entropy boundary loses a nonzero geometric source')
    require(abs(tr(f['rho']@f['E'])-f['rate'])<1e-13,'dynamical rate is not replaced by input optimization')
    # Pure-state alternatives at the same field show that the information cut matters when RIGHT is free.
    pure_low=np.outer(U[:,0],U[:,0].conj())
    er_free_limit=float(y[0])-limit_entropy
    require(tr(pure_low@f['Y'])<tr(sig@f['Y'])-.1,'reference-adjoined entropy selects a different free-spectrum input')
    require(entropy_log(sig)[0]>5.,'complete record-only entropy retains the input Schmidt entropy')
    return {'fixture':'original full128, CAR16, L4 Fourier character (i,i,-1,-i), r=1/9',
            'reference_scope':'16 active Schmidt columns, isometrically embeddable in oldRIGHT128; not full-site rank128',
            'stationary_rate':f['rate'],'stationary_rate_r_source':f['drate'],
            'Y_eigenvalues':[float(v) for v in y], 'fixed_schmidt_spectrum':[float(v) for v in lam],
            'spectral_cut_gap':gap,'orbit_hessian_lower_bound':hess,
            'native_stationary_Y_commutator':float(np.linalg.norm(f['rho']@f['Y']-f['Y']@f['rho'])),
            'finite_free_input':info,'finite_free_vs_dynamic_norm':float(np.linalg.norm(rho-f['rho'])),
            'finite_free_vs_Gibbs_limit_norm':float(np.linalg.norm(rho-sig)),
            'finite_fixed_RIGHT_orbit_gradient':orbit_res,'finite_fixed_RIGHT_iterations':it+1,
            'finite_optimized_field_source':source,'independent_optimized_field_secant':fdsource,
            'asymptotic_optimized_field_source_at_n2048':asym_source,
            'free_record_limit':free_limit,'free_reference_adjoined_limit':er_free_limit,
            'horizons':horizons,'finite_Choi_Hessian_test':{'directional_second_difference':second,'proved_lower_bound_at_diagnostic_Choi':bound},
            'two_round_pointer_vs_coherent_gap':pointer-entropy_log(dual_sr)[0]}

def main():
    m=load_native();exact=exact_controls();native=native_checks(m)
    print(json.dumps({'status':'PASS','input_snapshot':'f64d4c3389b507c7e7fb66ace9480ed6191c463d',
      'native_input_blob':INPUT_BLOB,'check_count':len(CHECKS),'checks':CHECKS,
      'exact_controls':exact,'native_diagnostics':native,
      'scope':{'complete_coherent_archive':'kept; entropy evaluated by exact complementary spectral identity',
       'charged_component':'original port costs 1+b; other actual ledger terms not assigned',
       'finite_minimum_theorem':'analytical with faithful Choi and declared freely variable density',
       'fixed_RIGHT_minimum_theorem':'analytical finite-horizon existence and large-horizon branch under stated gap',
       'numerical_roots_interval_certified':False,'original_spatial_all42_root_transferred':False,
       'Book03_Info_selected':False,'resource_writer_admitted':False,'independent_review':False,
       'uniform_refinement_gap':False,'GR_closed':False}},ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__': main()
