"""Full-label fixed-layout heat secant: actual small native clock + exact bounds.

The complete 16-seed device, its paid common suffix, Book03 price and gain
are not built in this check. This consumes the published local heat theorem.
"""
import json
import math
import mpmath as mp
import numpy as np
from check_source_price import load_control, need
from check_local_gibbs_records import build,scene,scene_heat


def mm(a,b):return np.einsum('ik,kj->ij',a,b,optimize=False)


def main():
    ne,digest=load_control()
    p=float(ne.P);beta=2*p*p;x=beta/11;ell=math.log(1/p)
    B,C=scene();steps=128
    Sinf=sum(scene_heat(B,C,2*math.cos(2*math.pi*j/steps),beta) for j in range(steps))/steps
    s=float(Sinf[32,32]);m=math.exp(-2*beta)
    need(s>=m,'fixed physical scene lower heat bound')
    results={}
    for n in (2,3,4):
        L=2*n
        # build includes paid repeated CX pairs; its genuine growing clock
        # contains all born-complement layers and actual short-winding cut.
        T,cuts,g,V,J=build(ne,n-2)
        eig,W=np.linalg.eigh(T+T.T)
        coeff=np.array([scene_heat(B,C,w,beta)[32,32] for w in eig])
        local=mm(W*coeff[None,:],W.T)
        K=mm(mm(g,local[cuts[-1],cuts[-1]]),g.T)
        delta=p**(n+1)
        rho0=np.outer(V[:,0],V[:,0]);rho1=np.outer(V[:,1],V[:,1])
        u0=float(np.trace(mm(K,rho0)));u1=float(np.trace(mm(K,rho1)))
        halo=2*x**L/math.factorial(L)/(1-x/(L+1))
        err=float(np.linalg.norm(K-s*np.eye(K.shape[0]),ord=2))
        diff=abs(math.log(u1/u0))/delta
        bound=2*halo/(m*delta)
        # N=4 is near double-precision rounding, so the heat estimate carries
        # a deliberately explicit arithmetic margin in this test.
        need(err <= halo+8e-14,'published heat compression')
        need(diff <= bound+3e-11,'full old-programme secant bound')
        need(abs(float(np.trace(rho0))-1)<1e-12 and abs(float(np.trace(rho1))-1)<1e-12,'full unconditioned states')
        results[str(n)]={'physical_L':L,'clock_dimension':len(T),'raw_J_fixed':J,
          'rho_trace_distance':float(np.abs(np.linalg.eigvalsh(rho1-rho0)).sum()),
          'eL_analytic_upper':halo,'heat_error_measured':err,
          'log_heat_contrast_over_delta':diff,'analytic_bound':bound,
          'comparison_roundoff_margin':3e-11}
    # Independent full spatial/WORK test: retain their entanglement rather
    # than replacing it by a product scene marginal. A local WORK unitary
    # changes the joint state while preserving the spatial marginal.
    T,cuts,g,V,J=build(ne,0)
    eig,W=np.linalg.eigh(T+T.T); d=g.shape[0]
    H=np.zeros((33*d,33*d))
    for j,w in enumerate(eig):
        col=W[cuts[-1],j]
        H += np.kron(scene_heat(B,C,w,beta),np.outer(col,col))
    U=np.kron(np.eye(33),g);H=mm(mm(U,H),U.T)
    def heat(a):return float(np.einsum('i,ij,j->',a,H,a,optimize=False))
    psi=np.zeros(33*d);psi[0]=math.sqrt(.3);psi[d+1]=math.sqrt(.7)
    psi2=np.zeros_like(psi);psi2[1]=math.sqrt(.3);psi2[d]=math.sqrt(.7)
    heat0,heat1=heat(psi),heat(psi2)
    sp=.3*Sinf[0,0]+.7*Sinf[1,1]
    halo4=2*x**4/math.factorial(4)/(1-x/5)
    need(abs(heat0-sp)<halo4+3e-14 and abs(heat1-sp)<halo4+3e-14,'entangled scene full-operator heat')
    need(abs(math.log(heat1/heat0)) <= 2*halo4/m+2e-13,'same spatial marginal contrast')
    aa=np.zeros_like(psi);aa[0]=1
    ab=np.zeros_like(psi);ab[20*d]=1
    scene_diff=abs(math.log(heat(ab)/heat(aa)))
    scene_lead=abs(math.log(Sinf[20,20]/Sinf[0,0]))
    need(abs(scene_diff-scene_lead)<=2*halo4/m+2e-13,'moving scene term retained')
    need(scene_lead>1e-6,'moving scene term not identically zero')
    correlated={'common_spatial_marginal_kept':True,'spatial_work_entangled':True,
      'same_marginal_log_contrast':abs(math.log(heat1/heat0)),
      'moving_scene_log_contrast':scene_diff,'moving_scene_leading_term':scene_lead,
      'common_L4_error_bound':2*halo4/m}
    mp.mp.dps=180
    pp=(mp.sqrt(5)-1)/2;bb=2*pp**2;xx=bb/11;ll=mp.log(1/pp)
    asym={}
    for n in (4,8,20,40,80):
        L=2*n;d=pp**(n+1)
        ee=2*xx**L/mp.factorial(L)/(1-xx/(L+1))
        full=2*mp.exp(2*bb)*ee/(ll*d)
        asym[str(n)]={'L':L,'delta':mp.nstr(d,15),'e_L_upper':mp.nstr(ee,15),
                        'negative_log_phi_contrast_over_delta_bound_without_gain':mp.nstr(full,15)}
    out={'status':'PASS; fixed-scene and common-graph theorem; conditional full apparatus',
         'native_source_sha256':digest,'thermal_scene_state_fixed_and_uncorrelated':False,
         'correlated_scene_work_case':correlated,
         'programme_label_may_remain_in_carrier':True,'native_small_clock':results,
         'high_precision_asymptotic_bounds':asym,'independent_book_price_and_suffix_cost_identified':False,
         'full_physical_gain_and_actual_device_compiled':False,'GR_closed':False}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
