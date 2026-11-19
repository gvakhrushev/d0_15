#!/usr/bin/env python3
"""New finite-count/Book-source consumer of the original all128 instrument.

Analytical all-horizon theorems are in PROOF.md. Numerical tests are bounded
Fourier fixtures, not a primary spatial all42 root or native admission test.
No assert statements: python -O must execute every check.
"""
from __future__ import annotations
import json
from pathlib import Path
import argparse
import numpy as np
import sympy as sp
from scipy.linalg import expm, solve_sylvester

P = (np.sqrt(5.0)-1.0)/2.0
Z = 2.0**-20
RR = 128
EYE = np.eye(16, dtype=complex)
CHECKS: list[str] = []


def require(ok: bool, name: str) -> None:
    if not bool(ok):
        raise ArithmeticError(name)
    CHECKS.append(name)


def adj(x: np.ndarray) -> np.ndarray:
    return x.conj().T


def herm(x: np.ndarray) -> np.ndarray:
    return (x+adj(x))/2


def tr(x: np.ndarray) -> float:
    y = np.trace(x)
    if abs(y.imag)>1e-7*max(1.0,abs(y.real)):
        raise ArithmeticError('non-real scalar source')
    return float(y.real)


def root(x: np.ndarray) -> np.ndarray:
    l,u=np.linalg.eigh(herm(x))
    if l.min()<=0:
        raise ArithmeticError('nonpositive root input')
    return (u*np.sqrt(l))@adj(u)


def creators() -> list[np.ndarray]:
    order=(0,2,3,1)
    out=[]
    for r in range(4):
        c=np.zeros((16,16),complex)
        before=order[:order.index(r)]
        for bits in range(16):
            if not ((bits>>r)&1):
                c[bits|(1<<r),bits]=(-1)**sum((bits>>j)&1 for j in before)
        out.append(c)
    return out


def native(theta: float, nu: float=0.6, phases: tuple | None=None) -> tuple[np.ndarray,np.ndarray]:
    """Original Walsh/Julia/Golden128 formulas, adapted from pinned upstream.

    Five-point derivatives below test this proper role-1 boost derivative.
    This is an L4 Fourier block, with all16 CAR grades, not the entire lattice.
    """
    cs=creators()
    gen=cs[0]@adj(cs[1])+cs[1]@adj(cs[0])
    u=expm(theta*gen); du=u@gen
    words=[]; jets=[]
    if phases is None:
        phases=(1j,1j,-1.0,-1j)
    zero=np.zeros_like(EYE)
    for r,c in enumerate(cs):
        base=nu*c
        x=base@(u if r==1 else EYE)*phases[r]
        dx=base@du*phases[r] if r==1 else zero
        left=root(EYE-x@adj(x)); right=root(EYE-adj(x)@x)
        dl=solve_sylvester(left,left,-dx@adj(x)-x@adj(dx))
        dr=solve_sylvester(right,right,-adj(dx)@x-adj(x)@dx)
        l0=root(EYE-base@adj(base)); r0=root(EYE-adj(base)@base)
        for w,dw in zip(((x,left),(adj(x),right),(-base,-l0),(-adj(base),-r0)),
                        ((dx,dl),(adj(dx),dr),(zero,zero),(zero,zero))):
            words.extend((w,w)); jets.extend((dw,dw))
    rows=[]; drows=[]
    for lab in range(32):
        signs=[(-1)**(bin(lab&j).count('1')&1) for j in range(32)]
        for b in range(2):
            rows.append(sum((signs[j]*words[j][b] for j in range(32)),zero.copy())/32)
            drows.append(sum((signs[j]*jets[j][b] for j in range(32)),zero.copy())/32)
    a,da=rows[0],drows[0]
    k=[]; dk=[]
    for j,nj in enumerate(rows):
        v=adj(nj)@a; dv=adj(drows[j])@a+adj(nj)@da
        k.extend(((EYE if j==0 else zero)-2*P**2*v,-2*P*np.sqrt(P)*v))
        dk.extend((-2*P**2*dv,-2*P*np.sqrt(P)*dv))
    return np.asarray(k),np.asarray(dk)


def cp_star(k: np.ndarray,x: np.ndarray,w: np.ndarray) -> np.ndarray:
    return sum((w[j]*adj(k[j])@x@k[j] for j in range(len(k))),np.zeros_like(x))


def cp_forward(k: np.ndarray,x: np.ndarray,w: np.ndarray) -> np.ndarray:
    return sum((w[j]*k[j]@x@adj(k[j]) for j in range(len(k))),np.zeros_like(x))


def cp_jet(k: np.ndarray,dk: np.ndarray,x: np.ndarray,dx: np.ndarray,w: np.ndarray) -> np.ndarray:
    return sum((w[j]*(adj(dk[j])@x@k[j]+adj(k[j])@dx@k[j]+adj(k[j])@x@dk[j])
                for j in range(len(k))),np.zeros_like(x))


def power_jet(b: np.ndarray,db: np.ndarray,n: int) -> tuple[np.ndarray,np.ndarray]:
    a=EYE.copy(); da=np.zeros_like(EYE)
    for _ in range(n):
        da=db@a+b@da; a=b@a
    return a,da


def book(nmat: np.ndarray,dn: np.ndarray,a: np.ndarray,da: np.ndarray,z: float=Z) -> tuple[float,float]:
    r=np.linalg.inv(root(nmat))
    c=herm(r@adj(a)@a@r)
    ev=np.linalg.eigvalsh(c)
    if ev.min() < -1e-9 or ev.max()>1+1e-9:
        raise ArithmeticError('invalid normalized corner spectrum')
    value=-RR*float(np.log1p(z*(ev-1)).sum())
    g=adj(a)@a; dg=adj(da)@a+adj(a)@da
    q=(1-z)*nmat+z*g
    # An O(z) source formula avoids subtracting two O(1) traces at native z.
    h=z*np.linalg.solve(nmat,g@np.linalg.inv(q))
    source=RR*(tr(h@dn)-z*tr(np.linalg.solve(q,dg)))
    return value,source


def build(k: np.ndarray,dk: np.ndarray,n: int,t: float) -> tuple[list,np.ndarray,np.ndarray]:
    weights=np.exp(-t*(np.arange(128)%2))
    ns=[EYE.copy()]; dn=np.zeros_like(EYE)
    for _ in range(n):
        dn=cp_jet(k,dk,ns[-1],dn,weights)
        ns.append(cp_star(k,ns[-1],weights))
    return ns,dn,weights


def reverse_source(k: np.ndarray,dk: np.ndarray,ns: list,weights: np.ndarray,a: np.ndarray,da: np.ndarray) -> float:
    nmat=ns[-1]; g=adj(a)@a; dg=adj(da)@a+adj(a)@da
    q=(1-Z)*nmat+Z*g
    costate=RR*Z*np.linalg.solve(nmat,g@np.linalg.inv(q))
    source=-RR*Z*tr(np.linalg.solve(q,dg))
    for j in range(len(ns)-1,0,-1):
        local=cp_jet(k,dk,ns[j-1],np.zeros_like(EYE),weights)
        source+=tr(costate@local)
        costate=cp_forward(k,costate,weights)
    return float(source)


def count_effect(k: np.ndarray,n: int) -> np.ndarray:
    e1=cp_star(k,EYE,np.arange(128)%2)
    total=np.zeros_like(EYE)
    for _ in range(n):
        total=e1+cp_star(k,total,np.ones(128))
    return herm(total)


def new_symbolic_checks() -> dict:
    p,s,t,x=sp.symbols('p s t x', positive=True)
    k=sp.symbols('k', nonnegative=True)
    eta=1-p*(1-sp.exp(-t))
    # Exact weak-clock derivatives of log normalized blank survival.
    log_one=2*sp.log(1-s)-sp.log(1-2*p*(1-sp.exp(-t))*s)
    require(sp.simplify(sp.diff(log_one,s).subs(s,0)+2*eta)==0,'exact marked effective-clock coefficient')
    require(sp.simplify(sp.diff(log_one,s,2).subs(s,0)-(-2+4*p**2*(1-sp.exp(-t))**2))==0,'exact first nonlinear spectral correction')
    require(sp.simplify(sp.diff(eta,t)+p*sp.exp(-t))==0,'exact clock-mark derivative')
    require(sp.rem(sp.Poly((1-p)-p**2,p),sp.Poly(p**2+p-1,p)).as_expr()==0,'native phi identity gives eta=p^2+p exp(-t)')
    require(sp.rem(sp.Poly((1-p*(1-p**2))-p,p),sp.Poly(p**2+p-1,p)).as_expr()==0,'canonical raw cost-amplitude mark gives EXACT golden clock factor p')
    # Exact noncommuting 2x2 cotangent identity (no square roots).
    z=sp.symbols('z', positive=True)
    nm=sp.Matrix([[sp.Rational(3,4),sp.Rational(1,12)],[sp.Rational(1,12),sp.Rational(2,3)]])
    aa=sp.Matrix([[sp.Rational(1,3),sp.Rational(1,7)],[0,sp.Rational(1,4)]])
    gg=aa.T*aa; qq=(1-z)*nm+z*gg
    hh=nm.inv()-(1-z)*qq.inv()
    require(nm*gg!=gg*nm,'genuinely noncommuting rational source fixture')
    require(all(sp.cancel(v)==0 for v in hh-z*nm.inv()*gg*qq.inv()),'exact stable O(z) cotangent identity')
    l=sp.Matrix([[1+x,x],[0,1]])
    require(sp.cancel((((1-z)*l.T*nm*l+z*l.T*gg*l).det()/(l.T*nm*l).det())-qq.det()/nm.det())==0,
            'field-dependent GL determinant invariance control')
    # Rational one-round positive count contraction: Jensen tested on all pure states analytically, matrix fixture here.
    nn=sp.Matrix([[sp.Rational(3,4),0],[0,sp.Rational(1,2)]])
    bb=sp.diag(sp.Rational(1,2),sp.Rational(1,3))
    require(all(v>0 for v in (nn-bb.T*bb).eigenvals()),'strict complementary input for monotonicity proof')
    return {'effective_clock':'1-p*(1-exp(-t)) = p^2+p*exp(-t)',
            'native_clock_exponent':'8*pi^2*p^2*a^2',
            'symbolic_Oz_cotangent_identity':'EXACT'}


def native_checks() -> dict:
    theta=.08; t=.7
    k,dk=native(theta)
    zero=np.zeros_like(EYE)
    require(np.linalg.norm(cp_star(k,EYE,np.ones(128))-EYE)<2e-13,'literal native128 completeness')
    require(np.linalg.norm(cp_jet(k,dk,EYE,zero,np.ones(128)))<2e-13,'literal complete field jet')
    outcomes={}
    for n in (1,2,3,8,32):
        ns,dn,weights=build(k,dk,n,t)
        a,da=power_jet(k[0],dk[0],n)
        val,src=book(ns[-1],dn,a,da)
        rev=reverse_source(k,dk,ns,weights,a,da)
        require(abs(src-rev)<1e-12,'adjoint all-history source n='+str(n))
        count=count_effect(k,n)
        budget=float(np.linalg.eigvalsh(count).max())
        lower=np.exp(-t*budget)
        minimum=float(np.linalg.eigvalsh(herm(ns[-1])).min())
        require(minimum>=lower-2e-12,'count-budget lower bound n='+str(n))
        require(minimum>np.exp(-2*n*t),'strict improvement over absolute-tick bound n='+str(n))
        commnorm=np.linalg.norm(ns[-1]@adj(a)@a-adj(a)@a@ns[-1])
        if n==1:
            require(commnorm<1e-13,'one-round normalizer is a spectral function: commuting control')
        else:
            require(commnorm>1e-13,'noncommuting native source n='+str(n))
        dt=1e-5
        vals=[]
        for change in (-2*dt,-dt,dt,2*dt):
            kk,_=native(theta+change)
            nss,_,_=build(kk,np.zeros_like(kk),n,t)
            av=np.linalg.matrix_power(kk[0],n)
            vals.append(book(nss[-1],zero,av,zero)[0])
        fd=(vals[0]-8*vals[1]+8*vals[2]-vals[3])/(12*dt)
        require(abs(fd-src)<2e-10,'independent price finite difference n='+str(n))
        # Marker derivative: Nbar'=sum -count e^-t count K* K; obtain by CP recursion.
        nt=EYE.copy(); dnt=zero.copy()
        dw=-(np.arange(128)%2)*weights
        for _ in range(n):
            dnt=cp_star(k,dnt,weights)+cp_star(k,nt,dw)
            nt=cp_star(k,nt,weights)
        _,marker_src=book(nt,dnt,a,zero)
        require(marker_src<0,'true normalized Book marker monotonicity n='+str(n))
        outcomes[str(n)]={'J':val,'field_source':src,'reverse_source':rev,'finite_difference_source':fd,
                          'mark_source':marker_src,'count_operator_norm':budget,
                          'normalizer_min':minimum,'count_lower_bound':lower,
                          'old_absolute_lower_bound':float(np.exp(-2*n*t))}
    # New two-round coherent source estimate and history-count identity.
    v=np.matmul(k[:,None,:,:],k[None,:,:,:]).reshape(-1,16,16)
    dv=(np.matmul(dk[:,None,:,:],k[None,:,:,:])+np.matmul(k[:,None,:,:],dk[None,:,:,:])).reshape(-1,16,16)
    counts=((np.arange(128)%2)[:,None]+(np.arange(128)%2)[None,:]).ravel()
    ew=np.exp(-t*counts)
    nfull=np.einsum('h,hji,hjk->ik',ew,v.conj(),v,optimize=True)
    dnfull=np.einsum('h,hji,hjk->ik',ew,dv.conj(),v,optimize=True)+np.einsum('h,hji,hjk->ik',ew,v.conj(),dv,optimize=True)
    ns,dn,_=build(k,dk,2,t)
    require(np.linalg.norm(nfull-ns[-1])<3e-13,'all16384 marked histories agree with operator recurrence')
    require(np.linalg.norm(dnfull-dn)<3e-13,'all16384 marked first jets agree with operator recurrence')
    a,da=power_jet(k[0],dk[0],2)
    _,fullsrc=book(ns[-1],dn,a,da)
    _,frozensrc=book(ns[-1],zero,a,da)
    require(abs(fullsrc-frozensrc)>1e-7,'hostile frozen normalizer misses a real native source')
    _,physicalsrc=book(EYE,zero,np.exp(-t)*a,np.exp(-t)*da)
    require(abs(fullsrc-physicalsrc)>1e-7,'physical full-cost attenuation is not polar normalization')
    abst=np.exp(-t*(2+counts))
    failgram=np.einsum('h,hji,hjk->ik',1-abst,v.conj(),v,optimize=True)
    succgram=np.einsum('h,hji,hjk->ik',abst,v.conj(),v,optimize=True)
    require(np.linalg.norm(succgram+failgram-EYE)<2e-12,'all original failed attenuation histories restore full completeness')
    dgram=np.einsum('hji,hjk->ik',dv.conj(),dv,optimize=True)
    kt=float(np.sqrt(np.linalg.eigvalsh(herm(dgram)).max()))
    budget=outcomes['2']['count_operator_norm']
    eta=np.exp(-t*budget)
    bound=RR*16*Z/(1-Z)*kt/np.sqrt(eta)
    require(abs(outcomes['2']['field_source'])<=bound,'complete tape derivative gives true trace-source bound')
    # Wrong scalar-only mean bound: average charge does not control every input.
    q=np.diag([0.0,10.0]); nn=np.diag(np.exp(-.7*np.diag(q)))
    require(np.linalg.eigvalsh(nn).min()<np.exp(-.7*np.trace(q)/2),'hostile input-average is not operator budget')
    return {'native_boost_theta':theta,'cost_mark':t,'cases':outcomes,'complete_tape_derivative_norm_n2':kt,
            'absolute_source_bound_n2':bound,'history_count_n2':128**2}


def shell_checks() -> dict:
    # Direct use of exact first-shell formulas; no lattice or thermal-suite replay.
    result=[]; a=.7; t=.7
    eta=1-P*(1-np.exp(-t)); tau=8*np.pi**2*P**2*a*a
    xlim=np.exp(-eta*tau)
    jlim=-RR*128*np.log1p(Z*(xlim-1))
    slim=RR*128*Z*xlim/(1-Z+Z*xlim)*eta*(16*np.pi**2*P**2*a)
    olderr=None
    for ll in (4,8,16,32,64,128):
        h=1.0/ll; n=128*ll**4
        wh=4*np.sin(np.pi*h)**2; eps=P**2*h*h/64
        delta=a*a*wh; s=eps*delta/2; ds=eps*a*wh
        e1=2*P*s; de1=2*P*ds; kap=1-np.exp(-t)
        logn=n*np.log1p(-kap*e1)
        logx=n*(2*np.log1p(-s)-np.log1p(-kap*e1))
        dlx=n*(-2*ds/(1-s)+kap*de1/(1-kap*e1))
        x=np.exp(logx)
        j=-RR*128*np.log1p(Z*(x-1))
        dj=-RR*128*Z*x*dlx/(1-Z+Z*x)
        lower=np.exp(-t*n*e1)
        require(np.exp(logn)>=lower-1e-14,'physical-clock full-shell count budget L='+str(ll))
        require(np.isfinite(j) and np.isfinite(dj),'no absolute-baseline underflow in true source L='+str(ll))
        err=abs(j-jlim)+abs(dj-slim)
        if olderr is not None:
            require(olderr/err>3.5,'C1 asymptotic second-order numerical control L='+str(ll))
        olderr=err
        # Full native mark attenuation is a different execution. Even L4 underflows only in the physical mark, not normalized action.
        require(n*t>5000,'absolute physical attenuation has paid-baseline exponent L='+str(ll))
        result.append({'L':ll,'rounds':n,'excess_mean':n*e1,'normalizer_after_baseline_removal':np.exp(logn),
                       'J':j,'source_da':dj,'C1_error_to_limit':err})
    return {'physical_a':a,'t':t,'eta':eta,'tau':tau,'J_limit':jlim,'source_da_limit':slim,
            'mean_excess_limit':P*tau,'cases':result}



def canonical_archive_checks() -> dict:
    details=[]
    t=2*np.log(1/P)
    require(abs(1-P*(1-np.exp(-t))-P)<2e-16, 'canonical marker factor equals p numerically')
    labels=np.arange(128); ports=labels%2; select=labels//2
    perm=labels.copy(); perm[select!=0]=labels[select!=0]^1
    require(len(set(perm.tolist()))==128 and perm[0]==0 and perm[1]==1,
            'full finite record permutation keeps blank and orphan separately')
    newports=perm%2
    padding=1+newports-ports
    require(np.all(padding>=0) and np.max(padding)==2,
            'every logical port-cost padding is nonnegative and at most two ticks')
    require(np.all(1+ports+padding==2+newports),
            'every actual labelled padded cost is 2 plus the relabelled port')
    for ll in (8,16,32):
        h=1/ll; a=.7; b=.9
        phase=(np.exp(2j*np.pi*h),1.,1.,1.)
        ka,_=native(0.,h*a,phase); kb,_=native(0.,h*b,phase)
        dt=P**2*h**4/64
        la=ka[1:]/np.sqrt(dt)
        marked=ka*(P**ports)[:,None,None]
        permuted=marked[perm]
        require(np.linalg.norm(permuted[2:]-np.sqrt(P)*ka[2:])<1e-14,
                'all126 paired amplitudes intertwine exactly L='+str(ll))
        require(np.linalg.norm(permuted[0]-ka[0])<1e-14 and
                np.linalg.norm(permuted[1]-P*ka[1])<1e-14,
                'ordinary blank and special orphan retained L='+str(ll))
        wh=4*np.sin(np.pi*h)**2
        coeff=P**2*wh/128
        va=h*a; vb=h*b
        overlap=(1+va*vb+np.sqrt(1-va*va)*np.sqrt(1-vb*vb))/2
        scalar=1-coeff*(va*va+vb*vb-2*P*va*vb*overlap)
        cross=sum((P**(2*ports[j])*adj(kb[j])@ka[j] for j in range(128)), np.zeros_like(EYE))
        require(np.linalg.norm(cross-scalar*EYE)<4e-14,
                'allCAR16 exact marked cross formula L='+str(ll))
        orphan=float(np.linalg.norm(ka[1]/np.sqrt(dt),2))
        details.append({'L':ll,'orphan_scaled_operator_norm':orphan,'orphan_norm_over_h2':orphan/h**2})
    # Limit intertwining of noncommuting jump words: a generic matrix test, not another native fixture.
    l0=np.array([[0.,1.],[2.,0.]],complex)
    l1=np.array([[1.,0.],[0.,-1.]],complex)
    data=[l0,l1]
    require(np.linalg.norm(l0@l1-l1@l0)>1,'noncommuting ordered-data-word control')
    for k in (1,2,3,4):
        word=np.eye(2,dtype=complex)
        for j in range(k): word=data[j%2]@word
        for bits in range(1<<k):
            bs=[(bits>>j)&1 for j in range(k)]
            original=np.prod([P if bit==0 else np.sqrt(P) for bit in bs])
            # Original t-marked amplitudes whose swapped output labels equal bs.
            transformed=np.prod([P if (1-bit)==0 else P*np.sqrt(P) for bit in bs])
            require(np.linalg.norm((transformed/P**(k/2)-original)*word)<2e-14,
                    'ordered-sector time-density intertwining k=%d bits=%d'%(k,bits))
    return {'canonical_t':t,'event_time_factor':P,'port_permutation':'swap b for SELECT j!=0; fix both j=0 labels',
            'logical_padding_cost':'c_new=2+b_new; extra=1+b_new-b_old in {0,1,2}',
            'full_native_padding_factory_constructed':False,'finite_orphan_controls':details}

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    symbolic=new_symbolic_checks(); nf=native_checks(); shell=shell_checks(); archive=canonical_archive_checks()
    out={'status':'PASS','checks':len(CHECKS),'check_names':CHECKS,'symbolic':symbolic,
         'native_noncommuting':nf,'original_first_shell_application':shell,'canonical_complete_archive':archive,
         'scope':{'fresh_full_spatial_all42_check':False,'physical_Info_selected':False,
                  'native_polar_processor_admitted':False,'GR_closed':False}}
    text=json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.output: args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':
    main()
