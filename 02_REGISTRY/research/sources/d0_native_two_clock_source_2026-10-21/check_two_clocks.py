#!/usr/bin/env python3
"""Exact native axial block: two clock scales and paid input/field minima.

Analytical theorems, not this finite replay, establish all-horizon/refinement
claims. No assert: python -O executes every test. Author evidence only.
Requires numpy, scipy, sympy and mpmath. Run with OPENBLAS_NUM_THREADS=1.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import mpmath as mp
import sympy as sp
from scipy.optimize import brentq
import native_axial as native
import spectral_price as spectral

CHECKS=[]
mp.mp.dps=90

def require(test,label):
    if not bool(test): raise ArithmeticError(label)
    CHECKS.append(label)

def herm(a): return (a+a.conj().T)/2

def close(a,b,tol,label):
    err=float(np.linalg.norm(np.asarray(a)-np.asarray(b)))
    require(err<tol,label)
    return err

def power_jet(t,dt,n):
    out=np.eye(len(t),dtype=complex); dout=np.zeros_like(t)
    while n:
        if n&1:
            dout=dt@out+t@dout; out=t@out
        n>>=1
        if n:
            dt=dt@t+t@dt; t=t@t
    return out,dout

def exact_controls():
    b=sp.symbols('b',real=True); v2=1-b*b
    eig=[]
    for mask in range(256):
        k=spectral.pop(mask);o=sum(spectral.pop((mask>>(2*r))&3)==1 for r in range(4))
        t=sp.expand((1+b)**2/4+v2*sp.Rational(1,16)*(-1)**k*(8-2*k)+(1-b)**2*sp.Rational(1,16)*(4-2*o))
        eig.append(t)
        low=sp.cancel((t-b*b)/(1-b))
        require(low.subs(b,0)>=0 and low.subs(b,1)>=0,'T lower bound mask %d'%mask)
        if mask:
            high=sp.cancel(((3+b)/4-t)/(1-b))
            require(high.subs(b,0)>=0 and high.subs(b,1)>=0,'T upper bound mask %d'%mask)
    slow=[s for s,(k,o,u) in enumerate(spectral.keys) if u==1]
    require(len(slow)==128,'commutant of the axial involution has dimension128')
    require(sp.simplify(eig[127]-(3+b)/4)==0 and spectral.keys[127][2]==1,'exact attained slow gap mode')
    ds=[sp.Rational(8-(-1)**k*(8-2*k),16) for k,o,u in spectral.keys]
    require(min(ds[s] for s in slow if s)!=0 and min(ds[s] for s in slow if s)==sp.Rational(1,8),'minimum nontrivial slow decay coefficient is1/8')
    generators=[1]+[1^(1<<j) for j in range(1,8)]
    reached={0}
    for g in generators: reached|={x^g for x in list(reached)}
    require(len(reached)==256,'eight positive jump species span all error labels; padding proves Choi positivity at n>=8')
    require(np.array_equal(spectral.chi@spectral.chi.T,256*np.eye(256,dtype=np.int64)),'exact character-table orthogonality')
    p=(sp.sqrt(5)-1)/2
    require(sp.simplify(p*p+p-1)==0,'original Golden partition')
    require(bool(64*p**3>15) and bool((1/p)**12>256),'global minimum endpoint bounds without fitted constants')
    q0,a,h=sp.symbols('q0 a h',positive=True)
    # With q=p^2 a^2 h^2 sin^2(pi h)/16, this verifies both powers and constants.
    q=p*p*a*a*h*h*sp.sin(sp.pi*h)**2/16
    gap=q*(1-sp.sqrt(1-h*h*a*a))/4
    require(sp.simplify(sp.limit(gap/h**6,h,0)-sp.pi**2*p*p*a**4/128)==0,'exact physical gap coefficient at h^6')
    return {'class_count':len(spectral.classes),'slow_subspace_dimension':128,
            'positive_generators':generators,'uniform_faithful_Choi_horizon':8,
            'gap_leading':'pi^2 p^2 a^4 h^6 /128'}

def native_controls(mutation):
    L=4; a=2.4; f=native.native_axial(L,a)
    k,dk=f['K'],f['dK'];eye=native.I;q=f['q'];b=f['b'];nu=f['nu']
    complete=sum(native.adj(x)@x for x in k)
    dcomplete=sum(native.adj(dx)@x+native.adj(x)@dx for x,dx in zip(k,dk))
    e=sum(native.adj(x)@x for x in k[1::2])
    de=sum(native.adj(dx)@x+native.adj(x)@dx for x,dx in zip(k[1::2],dk[1::2]))
    close(complete,eye,2e-13,'all128 Kraus completeness')
    close(dcomplete,0*eye,2e-13,'all128 complete field-jet normalization')
    close(f['D']@f['D'],f['Delta'],3e-13,'actual native axial Dirac square is scalar')
    close(e,native.P*q*eye,2e-14,'actual original port-cost effect')
    close(de,2*native.P*q/a*eye,2e-14,'actual original port-cost field jet')
    for i in range(8):
        for j in range(8):
            close(f['majoranas'][i]@f['majoranas'][j]+f['majoranas'][j]@f['majoranas'][i],2*eye if i==j else 0*eye,2e-13,'CAR Clifford pair %d,%d'%(i,j))
    t=native.superop(k)
    dt=sum((np.kron(dx.conj(),x)+np.kron(x.conj(),dx) for x,dx in zip(k,dk)),np.zeros_like(t))
    maxerr=0.
    for s,x in enumerate(f['paulis']):
        kk,o,u=spectral.keys[s]
        tv=(1+b)**2/4+nu*nu/16*(-1)**kk*(8-2*kk)+(1-b)**2/16*(4-2*o)
        mm=1-q+q*u*tv
        out=(t@x.reshape(-1,order='F')).reshape(16,16,order='F')
        maxerr=max(maxerr,float(np.linalg.norm(out-mm*x)))
    require(maxerr<3e-13,'all256 exact-spectrum formulas against literal full128 channel')
    # Enumerate every two-round word independently, with no discarded label.
    words=np.einsum('aij,bjk->abik',k,k,optimize=True).reshape(16384,16,16)
    jwords=words.transpose(0,2,1).reshape(16384,256).T
    jdirect=jwords@jwords.conj().T
    j2=native.choi(t@t)
    close(jdirect,j2,1e-12,'all16384 ordered histories equal complete two-round Choi matrix')
    e2=spectral.evaluate(L,str(a),n=2)
    close(native.entropy(j2/16),float(e2['H']),2e-11,'whole coherent two-round spectrum equals error Fourier law')
    # Use only states whose true reference fits into 16 active oldRIGHT columns.
    rng=np.random.default_rng(20261021)
    r=rng.normal(size=(16,16))+1j*rng.normal(size=(16,16));rho=r@r.conj().T;rho/=np.trace(rho)
    vr,ur=np.linalg.eigh(rho); sr=(ur*np.sqrt(vr))@ur.conj().T
    comp=np.kron(sr.T,np.eye(16))@j2@np.kron(sr.T,np.eye(16))
    require(native.entropy(comp)<=native.entropy(j2/16)+1e-10,'uniform input beats retained purified random input')
    # Actual pointer Shannon is a DIFFERENT information cut.
    probs=np.einsum('aij,aij->a',words.conj(),words).real/16
    positive=probs>0;hp=-float(probs[positive]@np.log(probs[positive]))/native.ELL
    require(hp-float(e2['H'])>1e-3,'whole pointer entropy is not substituted for coherent entropy')
    # Positive Choi source at a well-resolved finite horizon.
    n=4096;tn,dtn=power_jet(t,dt,n);j=native.choi(tn)/16;dj=native.choi(dtn)/16
    vals,u=np.linalg.eigh(j)
    require(vals.min()>1e-5,'native finite diagnostic has strictly resolved Choi spectrum')
    lj=(u*np.log(vals))@u.conj().T
    hsrc=-float(np.trace(lj@dj).real)/native.ELL
    exact=spectral.evaluate(L,str(a),n=n)
    fsrc=n*native.P*2*q/a-hsrc
    close(fsrc,float(exact['fa']),2e-8,'original matrix field source equals exact spectral source')
    if mutation=='omit_port_source':
        fsrc=-hsrc
    close(fsrc,float(exact['fa']),2e-8,'paid source includes mandatory actual surplus-cost derivative')
    # Independent complete entropy input Euler, not a one-dimensional test.
    sj=(u*np.sqrt(16*vals))@u.conj().T
    zz=sj@(lj+np.eye(256))@sj
    grad=np.einsum('iaja->ij',zz.reshape(16,16,16,16)).T/native.ELL
    residual=float(np.linalg.norm(grad-np.trace(grad)/16*eye))
    require(residual<3e-9,'all255 free-input Euler rows at exact uniform input')
    # The physical h^-4 horizon has tiny true Choi eigenvalues. This is a
    # FLOATING diagnostic with an explicit log floor, not a positivity proof.
    af=.15; nf=128*L**4; ff=native.native_axial(L,af)
    tt=native.superop(ff['K'])
    dtt=sum((np.kron(dx.conj(),x)+np.kron(x.conj(),dx) for x,dx in zip(ff['K'],ff['dK'])),np.zeros_like(tt))
    ttf,dttf=power_jet(tt,dtt,nf)
    jf=native.choi(ttf)/16; djf=native.choi(dttf)/16
    vf,uf=np.linalg.eigh(jf); keep=vf>1e-12
    lg=(uf[:,keep]*np.log(vf[keep]))@uf[:,keep].conj().T
    sf=nf*native.P*2*ff['q']/af+float(np.trace(lg@djf).real)/native.ELL
    ef=spectral.evaluate(L,str(af),n=nf)
    close(nf*native.P*ff['q']-native.entropy(jf),float(ef['f']),2e-9,'physical horizon full128 matrix price agrees with spectral formula')
    close(sf,float(ef['fa']),2e-7,'physical horizon full128 matrix source agrees within declared log-resolution tolerance')
    return {'literal_eigen_identity_error':maxerr,'two_round_coherent_entropy':float(e2['H']),
            'two_round_pointer_entropy':hp,'input_Euler_residual':residual,
            'field_source_4096':float(exact['fa']),'matrix_field_source_4096':fsrc,
            'min_Choi_eigenvalue_4096':float(vals.min()),
            'physical_horizon_log_floor':1e-12,'physical_horizon_matrix_source':sf,
            'physical_horizon_exact_spectral_source':float(ef['fa'])}

def hessian_direction(probs,mask):
    out=mp.mpf(0)
    for g,x in enumerate(probs):
        y=probs[g^mask]
        ll=1/x if abs(x-y)<mp.mpf('1e-75')*max(x,y) else (mp.log(x)-mp.log(y))/(x-y)
        out+=x*y*ll
    return out/spectral.ell

def refinement_controls(mutation):
    p=spectral.p;ell=spectral.ell
    tau=mp.findroot(lambda x:p-2*mp.exp(-2*x)*mp.atanh(mp.exp(-2*x))/ell,mp.mpf('.49'))
    astar=mp.sqrt(tau/(8*mp.pi**2*p*p))
    # Mutation probes execute their decisive actual calculation immediately;
    # they need not repeat every unchanged refinement diagnostic first.
    if mutation=='replace_by_equilibrium':
        actual=spectral.evaluate(16,astar)
        close(float(mp.log(256)/ell),float(actual['H']),1e-4,'mixing and physical refinement cannot be interchanged')
    if mutation=='freeze_information_cut':
        ar=brentq(lambda aa:float(spectral.evaluate(16,str(aa))['fa']),.07,.3,xtol=3e-14)
        actual=spectral.evaluate(16,str(ar))
        close(float(2*p*actual['n']*actual['q']/ar),0,1e-5,'retained-reference information cut keeps its true field source')
    if mutation=='short_clock':
        actual=spectral.evaluate(16,astar)
        short=spectral.evaluate(16,astar,n=128*16**2)
        close(float(short['f']),float(actual['f']),.01,'old h^-2 physical clock cannot replace h^-4')
    rows=[]
    for L in [4,8,16,32,64]:
        d=spectral.evaluate(L,astar)
        r=brentq(lambda aa:float(spectral.evaluate(L,str(aa))['fa']),.07,.3,xtol=3e-14)
        at=spectral.evaluate(L,str(r))
        require(abs(float(at['fa']))<1e-9,'finite physical-scale source zero L=%d'%L)
        require(at['faa']>0,'positive finite physical-scale Hessian L=%d'%L)
        require(min(d['pi'])>0 and abs(mp.fsum(d['pi'])-1)<mp.mpf('1e-75'),'positive complete spectrum L=%d'%L)
        require(abs(mp.fsum(d['dpi']))<mp.mpf('1e-73'),'normalized source L=%d'%L)
        hh=float(hessian_direction(d['pi'],2));selected=float(hessian_direction(d['pi'],1))
        er_source=2*p*at['n']*at['q']/mp.mpf(str(r))
        require(er_source>0,'same-input record-plus-RIGHT has positive field source L=%d'%L)
        rows.append({'L':L,'rounds':d['n'],'a_min_diagnostic':r,'F_minus_paid_n':float(at['f']),
                     'scale_source_at_root':float(at['fa']),'scale_second_source':float(at['faa']),
                     'n_times_mixing_gap':float(d['ngap']),
                     'normal_input_Hessian_direction2':hh,'selected_input_Hessian_direction1':selected,
                     'ER_source_at_E_minimum':float(er_source)})
    require(all(rows[j+1]['a_min_diagnostic']<rows[j]['a_min_diagnostic'] for j in range(4)),'finite roots converge toward owned limiting source zero')
    require(rows[-1]['normal_input_Hessian_direction2']<rows[0]['normal_input_Hessian_direction2']/100,'genuine input inverse loses uniform coercivity')
    require(rows[-1]['n_times_mixing_gap']<mp.mpf('1e-5'),'physical h^-4 horizon has not equilibrated the input')
    slows=[];a=mp.mpf('.5');target=16*mp.pi**2*p**3*a
    for L in [8,16,32,64]:
        d=spectral.evaluate(L,a,n=128*L**6)
        sigma=8*mp.pi**2*p*p*a**4
        require(abs(float(d['ngap']-sigma/8))<.02,'slow h^-6 gap convergence L=%d'%L)
        require(d['fa']>0,'actual slow-clock reduced field source positive L=%d'%L)
        scaled=d['fa']/L**2
        require(abs(scaled-target)<mp.mpf('1.4'),'slow-clock source leading coefficient L=%d'%L)
        # Same declared blank-work Book corner; do not add it to CQ by decree.
        q=d['q'];qa=2*q/a;n=d['n'];z=mp.mpf(2)**-20
        surv=mp.exp(2*n*mp.log1p(-q/2))
        dJ=2048*z*surv*n*qa/((1-q/2)*(1-z+z*surv))
        require(dJ>=0,'true blank complementary source has retained sign L=%d'%L)
        slows.append({'L':L,'rounds':n,'h2_field_source':float(scaled),
                      'coherent_entropy':float(d['H']),'n_times_mixing_gap':float(d['ngap']),
                      'Book_source_log10':float(mp.log10(dJ))})
    require(abs(slows[-1]['h2_field_source']-float(target))<.03,'slow source reaches its exact predicted leading coefficient')
    return {'owned_tau_star':mp.nstr(tau,48),'a_star':mp.nstr(astar,48),
            'limit_F_minus_paid_n':float(spectral.limit(astar)['f']),
            'fast_clock_rows':rows,'slow_clock_rows':slows,
            'slow_scaled_source_target':float(target),
            'fast_limit_balanced_input_manifold_dimension':254}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path)
    ap.add_argument('--mutation',choices=['omit_port_source','replace_by_equilibrium','freeze_information_cut','short_clock'])
    args=ap.parse_args()
    result={'exact':exact_controls(),'native':native_controls(args.mutation),'refinement':refinement_controls(args.mutation)}
    result.update(status='PASS',check_count=len(CHECKS),checks=CHECKS,
                  scope={'GR_closed':False,'physical_Book_Info_selected':False,
                         'all_spatial42_root':False,'axial_CAR16_original128_outcomes':True,
                         'reference':'16 active Schmidt columns inside retained oldRIGHT128',
                         'numerical_roots_interval_certified':False,'independent_review':False,
                         'all_horizon_and_limit_theorems':'analytical proof; not finite extrapolation'})
    encoded=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if args.output: args.output.write_text(encoded,encoding='utf-8')
    print(encoded,end='')
if __name__=='__main__':main()
