#!/usr/bin/env python3
"""Whole 359-variable literal scene minimum, not a fitted field source.

Consumes the same positive-conductance extension already declared in
A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md. It does NOT promote this class to
compulsory M1-admission or identify its degrees with 42 physical fields.
"""
from __future__ import annotations
import json
from fractions import Fraction as Q
import numpy as np
from scipy.linalg import expm
import check_scene_descent as core

CHECKS=[]
I=np.eye(33)
BETA,ZETA=core.BETA,core.ZETA
EDGES=np.array(core.EDGES)
ZONES=core.ZONES
SIZES=np.array([9,11,13])

def ck(name,condition):
    if not bool(condition):raise ArithmeticError(name)
    CHECKS.append(name)

def graph(w):
    A=np.zeros((33,33),dtype=np.result_type(w))
    A[EDGES[:,0],EDGES[:,1]]=w
    A[EDGES[:,1],EDGES[:,0]]=w
    degree=A.sum(axis=1)
    root=1/np.sqrt(degree)
    T=root[:,None]*A*root[None,:]
    return T,degree

def gradient(w):
    """Whole scalar B differentiated analytically before any balancing."""
    T,d=graph(w)
    heat=expm(-BETA*(I-T))
    M=heat/np.trace(heat)-2*ZETA*T@np.linalg.inv((1-ZETA)*I+ZETA*T@T)
    MTdiag=np.diag(M@T)
    i,j=EDGES[:,0],EDGES[:,1]
    return w*(2*M[i,j]/np.sqrt(d[i]*d[j])-MTdiag[i]/d[i]-MTdiag[j]/d[j])

def gap_coordinates(w):
    T,d=graph(w)
    Qzone=np.zeros((33,3))
    for z in range(3):
        q=np.where(ZONES==z,np.sqrt(d),0.)
        Qzone[:,z]=q/np.linalg.norm(q)
    B=Qzone.T@T@Qzone
    Tbar=Qzone@B@Qzone.T
    eig=np.linalg.eigvalsh(B)
    s=(eig[1]-eig[0])/2
    off=float(np.linalg.norm(T-Tbar,'fro')**2)
    return T,Qzone,B,Tbar,s,off

def main():
    # Rigorous rational lower bound: 3/4<beta<1; exp(-2beta)>exp(-2)>1/8.
    mu0=Q(1,352)-Q(2,2**20-1)
    ck('rational strict convexity wall positive',mu0>Q(28,10000))
    r=1/SIZES[ZONES]
    wstar=r[EDGES[:,0]]*r[EDGES[:,1]]
    Tstar,dstar=graph(wstar)
    eig=np.linalg.eigvalsh(Tstar)
    expected=np.sort(np.array([1,-.5,-.5]+[0.]*30))
    ck('balanced actual scene spectrum complete',np.max(np.abs(eig-expected))<2e-14)
    ck('all three total zone degrees exactly balanced numerically',
       max(abs(dstar[ZONES==z].sum()-2) for z in range(3))<2e-14)
    g=gradient(wstar)
    ck('ALL359 independent logarithmic edge Eulers vanish',np.max(np.abs(g))<3e-16)
    Hstar,Jstar,Zstar=core.price(Tstar)
    ck('full thermal trace retains all thirty dark modes',
       abs(Zstar-(1+30*np.exp(-BETA)+2*np.exp(-1.5*BETA)))<1e-13)
    ck('full feedback retains thirty eigenvalue-one modes',
       abs(Jstar+30*np.log1p(-ZETA)+2*np.log1p(-.75*ZETA))<1e-13)
    H0,J0,_=core.price(graph(np.ones(359))[0])
    ck('old unweighted scene has strictly higher COMPLETE price',H0+J0>Hstar+Jstar)
    # All 359x359 entries, analytic whole-price gradient, complex-step (no cutoff).
    hess=np.zeros((359,359));eps=1e-20
    for k in range(359):
        w=wstar.astype(complex);w[k]*=np.exp(1j*eps)
        hess[:,k]=np.imag(gradient(w))/eps
    symerr=float(np.max(np.abs(hess-hess.T)))
    ck('full 359x359 source Hessian symmetry',symerr<2e-14)
    he=np.linalg.eigvalsh((hess+hess.T)/2)
    ck('31 expected tangent zero modes, numerical not interval rank proof',np.max(np.abs(he[:31]))<2e-13)
    ck('remaining 328 directions positive numerically',he[31]>1e-7)
    tangents=[np.ones(359)]
    for z in range(3):
        vertices=np.flatnonzero(ZONES==z)
        for v in vertices[:-1]:
            a=np.zeros(33);a[v]=1;a[vertices[-1]]=-1
            tangents.append(a[EDGES[:,0]]+a[EDGES[:,1]])
    tangent=np.stack(tangents,axis=1)
    ck('31 independent explicit balancing tangents',np.linalg.matrix_rank(tangent)==31)
    tangent_error=float(np.max(np.abs(hess@tangent)))
    ck('whole Hessian annihilates all31 derived tangent columns',tangent_error<3e-14)
    rng=np.random.default_rng(913)
    smallest_gap_ratio=float('inf');max_stationary=0.;pincherr=0.
    for k in range(40):
        rr=np.empty(33)
        for z in range(3):
            vals=np.exp(rng.uniform(-2,2,SIZES[z]));rr[ZONES==z]=vals/vals.sum()
        balanced=np.exp(rng.uniform(-2,2))*rr[EDGES[:,0]]*rr[EDGES[:,1]]
        gs=float(np.max(np.abs(gradient(balanced))))
        max_stationary=max(max_stationary,gs)
        ck('different positive vertex profiles solve same all359 equations',gs<5e-16)
        hb,jb,_=core.price(graph(balanced)[0])
        ck('all balancing minima have same full scalar value',abs(hb+jb-Hstar-Jstar)<4e-14)
        w=balanced*np.exp(rng.uniform(-1.5,1.5,359))
        T,Qz,B,Tbar,s,off=gap_coordinates(w)
        average=np.zeros((33,33))
        for mask in range(8):
            U=np.zeros((33,33))
            for z in range(3):
                Pz=np.outer(Qz[:,z],Qz[:,z]);Iz=np.diag((ZONES==z).astype(float))
                sign=1 if mask>>z&1 else -1
                U+=Pz+sign*(Iz-Pz)
            average+=U@T@U.T/8
        err=float(np.linalg.norm(average-Tbar));pincherr=max(pincherr,err)
        ck('exact eight-sign pinch implemented with moving degree profiles',err<2e-13)
        h,j,_=core.price(T)
        gap=h+j-Hstar-Jstar
        lower=float(mu0)*(off/2+s*s)
        ck('quantitative full-action gap, no heat-only substitution',gap+1e-13>=lower>0)
        smallest_gap_ratio=min(smallest_gap_ratio,gap/lower)
    # Scene-blind spectral tensor coupling: arbitrary fixed report contraction.
    # This is a mathematical conditional consumer, not a claimed native compilation.
    S=np.array([[.22,.07,.03],[.07,-.31,.02],[.03,.02,.8]])
    ev,U=np.linalg.eigh(Tstar);se=np.linalg.eigvalsh(S)
    heat=np.exp(-BETA*(1-ev[:,None]*se[None,:]));Z=heat.sum()
    slope=np.sum(se[None,:]*heat/Z-2*ZETA*ev[:,None]*se[None,:]**2/
                 (1-ZETA+ZETA*ev[:,None]**2*se[None,:]**2),axis=1)
    M=(U*slope)@U.T
    i,j=EDGES[:,0],EDGES[:,1];dd=np.diag(M@Tstar)
    tensorgrad=wstar*(2*M[i,j]/np.sqrt(dstar[i]*dstar[j])-dd[i]/dstar[i]-dd[j]/dstar[j])
    ck('scene-blind retained tensor spectral coupling keeps all359 scene Eulers zero',np.max(np.abs(tensorgrad))<4e-16)
    # Off-shell scene stationarity and exact three-sector full-price reduction.
    Sprime=np.array([[.03,-.04,.01],[-.04,.02,.025],[.01,.025,-.01]])
    ck('report test jet is genuinely noncommuting',np.linalg.norm(S@Sprime-Sprime@S)>1e-3)
    sector_error=0.;moving_scene_error=0.
    def full_tensor_value(t):
        K=np.kron(Tstar,S+t*Sprime)
        ee=np.linalg.eigvalsh(K)
        return np.log(np.exp(-BETA*(1-ee)).sum())/BETA-np.log1p(-ZETA*(1-ee*ee)).sum()
    def sector_value(t):
        ss=np.linalg.eigvalsh(S+t*Sprime)
        zz=sum(mult*np.exp(-BETA*(1-lam*ss)).sum() for lam,mult in [(1,1),(-.5,2),(0,30)])
        jj=-sum(mult*np.log1p(-ZETA*(1-lam*lam*ss*ss)).sum() for lam,mult in [(1,1),(-.5,2),(0,30)])
        return np.log(zz)/BETA+jj
    for t in [-.3,0,.3]:
        sk=S+t*Sprime;ss=np.linalg.eigvalsh(sk)
        hw=np.exp(-BETA*(1-ev[:,None]*ss[None,:]));zz=hw.sum()
        sl=np.sum(ss[None,:]*hw/zz-2*ZETA*ev[:,None]*ss[None,:]**2/
            (1-ZETA+ZETA*ev[:,None]**2*ss[None,:]**2),axis=1)
        mm=(U*sl)@U.T;dd2=np.diag(mm@Tstar)
        gg=wstar*(2*mm[i,j]/np.sqrt(dstar[i]*dstar[j])-dd2[i]/dstar[i]-dd2[j]/dstar[j])
        moving_scene_error=max(moving_scene_error,float(np.max(np.abs(gg))))
        ck('all359 scene Eulers remain zero off-shell in report parameter',np.max(np.abs(gg))<5e-16)
        err=abs(full_tensor_value(t)-sector_value(t));sector_error=max(sector_error,float(err))
        ck('full99 value equals exact 1+2+30 sector formula',err<2e-13)
    st=1e-4
    d_full=(full_tensor_value(st)-full_tensor_value(-st))/(2*st)
    d_sector=(sector_value(st)-sector_value(-st))/(2*st)
    ck('full report source retained by exact sector reduction',abs(d_full-d_sector)<1e-9)
    # Spectral neutrality is NOT neutrality to an anchored scene readout.
    eps_anchor=1e-5
    ra=r.copy();rb=r.copy()
    ra[0]+=eps_anchor;ra[1]-=eps_anchor
    rb[0]-=eps_anchor;rb[1]+=eps_anchor
    ta=graph(ra[EDGES[:,0]]*ra[EDGES[:,1]])[0]
    tb=graph(rb[EDGES[:,0]]*rb[EDGES[:,1]])[0]
    anchor_source=((ta@ta)[0,0]-(tb@tb)[0,0])/(2*eps_anchor)
    ck('anchored readout changes along spectral minima, not a physical gauge',abs(anchor_source-.5)<1e-9)
    print(json.dumps({'status':'PASS_LITERAL_SCENE_GLOBAL_MINIMUM_AND_STATIONARY_ELIMINATION',
      'source_commit':'5a9764b20c2b7b481ec90d06a711ce3739f4e773',
      'independent_edge_variables':359,'retained_history_dimension':718,
      'rigorous_convexity_lower_rational':str(mu0),
      'minimum_spectrum':[1,-.5,-.5,'0 x30'],
      'minimum_weight_family':'w_uv=c r_u r_v; c>0; sum_(u in zone a) r_u=1 for each a',
      'positive_minimizer_family_dimension':31,
      'minimum_heat':Hstar,'minimum_feedback':Jstar,
      'unweighted_minus_minimum_full_price':H0+J0-Hstar-Jstar,
      'max359_euler_at_uniform_zone_minimum':float(np.max(np.abs(g))),
      'max359_euler_over40_positive_profiles':max_stationary,
      'hessian359_diagnostic':{'symmetry_error':symerr,'max_abs31_smallest':float(np.max(np.abs(he[:31]))),
          'min328_positive':float(he[31]),'max_eigenvalue':float(he[-1]),'tangent31_error':tangent_error,
          'rank_is_outward_interval_certified':False},
      'eight_sign_pinching_error':pincherr,'smallest_observed_gap_over_proved_lower':smallest_gap_ratio,
      'scene_functional_report_test':{'dimension':99,'max_sector_value_error':sector_error,
          'max_offshell_scene_euler':moving_scene_error,'whole_price_report_derivative':float(d_full),
          'reduced_price_report_derivative':float(d_sector),'is_native_full128_or_all42':False},
      'anchored_readout_source_on_minimum_family':float(anchor_source),
      'scene_blind_tensor_max359_euler':float(np.max(np.abs(tensorgrad))),
      'checks':len(CHECKS),'physical_weight_admission_proved':False,
      'all42_field_writer_compiled':False,'all_independent_apparatus_equations_solved':False,'GR_closed':False},indent=2))

if __name__=='__main__':main()
