#!/usr/bin/env python3
"""Native original G2STAR + SAME N=1 cap9/20 CQ price: one truly free
temporal node, fixed two-neighbor geometric/CAR collar; solve 42 genuine
independent FULL first-Euler components WITHOUT imposing pure boosts,
diagonal coframe or f=q=0 AFTER varying.

This is NUMERICAL finite stationarity under one FIXED original CQ
field/price interface, NOT an exact mathematical existence certificate,
compulsory Book03 full history, true native writer or continuum GR limit.
"""
from __future__ import annotations
import argparse,json,time,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm,svdvals
from scipy.optimize import root,least_squares
from scipy.optimize._numdiff import approx_derivative
from check_diagonal_coframe_cauchy_recurrence import clock,radius,golden_curve,comm
from check_star_rank2_seam import I,LORENTZ as L,KAPPA,ETA,star_density,matter_query
from full_n1_euler_analytic import full_source,star_node

def make_slab(n=2):
    """Consume the exact ORIGINAL four-diagonal Cauchy branch only as
    INITIAL GUESS, not as a constraint on any subsequent variation."""
    ts=np.linspace(clock(1.),clock(1.2),n+1)
    h=float(ts[1]-ts[0])
    amp=(2*KAPPA)**-.5
    k1=golden_curve(1.)[1]
    nodes=[]
    psi=np.zeros((n+1,2))
    for j in range(n):
        r=radius(ts[j]);rn=radius(ts[j+1])
        A,_,k2=golden_curve(r)
        k2n=golden_curve(rn)[2]
        S2=np.sinh(h*(k2n-k2))
        C12=comm(h*k1,h*k2)
        C22=comm(h*k2,h*k2)
        def equations(z):
            X,R=z
            return [(2*R*C12+C22/X)/h**2-X,
                    (2*R*S2+X*C22)/h**2+X**3]
        solved=root(equations,[A,r],tol=1e-11)
        X,R=solved.x
        assert solved.success and max(abs(np.array(equations(solved.x))))<1e-9
        k1next=k1+np.arcsinh(-(S2/X+X*C12)/R)/h
        U=np.array([I]+[expm(h*k*L[a])
                      for a,k in enumerate((k1,k2,k2))],dtype=float)
        nodes.append(dict(e=np.diag([X,1/X,R,R]),
                          U=U,v=np.array([[amp*X**2,0,0,0],
                                          [0,amp,0,0]],float)))
        psi[j+1,0]=psi[j,0]+h*amp*X**2
        k1=k1next
    last=np.array([I]+[expm(h*k*L[a])
                   for a,k in enumerate((k1,golden_curve(1.2)[2],
                                             golden_curve(1.2)[2]))],dtype=float)
    nodes.append(dict(e=np.diag([1,1,1.2,1.2]),U=last,
                      v=np.zeros((2,4))))
    return h,nodes,psi

def problem(n=2,weights=None):
    h,base,psi=make_slab(n)
    amp=(2*KAPPA)**-.5
    if weights is None:weights=[1.]*n
    assert len(weights)==n and min(weights)>0
    def fields(z):
        nodes=[dict(e=c['e'].copy(),U=c['U'].copy(),
                    v=c['v'].copy()) for c in base]
        ps=psi.copy()
        for j in range(1,n):
            x=z[(j-1)*42:j*42]
            nodes[j]['e']+=x[:16].reshape(4,4)
            for r in range(4):
                generator=sum(x[16+6*r+k]*L[k] for k in range(6))
                nodes[j]['U'][r]=expm(h*generator)@nodes[j]['U'][r]
            ps[j]+=x[40:42]
        for j in range(n):
            nodes[j]['v'][:]=0
            nodes[j]['v'][0,0]=(ps[j+1,0]-ps[j,0])/h
            nodes[j]['v'][1,0]=(ps[j+1,1]-ps[j,1])/h
            nodes[j]['v'][1,1]=amp
        return nodes
    def euler(z,detail=False):
        nodes=fields(z)
        s=full_source(nodes,h,weights,.05)
        residual=np.concatenate([
          np.r_[s['e'][j].ravel(),(h*s['U'][j]).ravel(),
                h*s['psi'][j]] for j in range(1,n)])
        return (residual,s,nodes) if detail else residual
    return h,base,psi,weights,fields,euler

def direct_CQ_value(nodes,h,weights):
    """INDEPENDENT full nonlinear price (not the Euler routine's wv).
    Preserves existing original readiness, Golden entropy and all based faces.
    """
    p=(np.sqrt(5.)-1.)/2.;z=2.**-20
    alpha=(1-(1-2*p**3)**9)**128
    beta=((1-p**120)**4*(1-(1-16*p**9)**20))**43
    lp=np.log(1/p)
    E0=p*p; ell0=4*E0*(1-E0)
    B0=4*p*p*(1-p*p)
    A0=ell0+(1-ell0)*B0
    r0=z*(A0+B0)-z*z*A0*B0
    def click(x,y):
        E=p*p*(1+x); ell=4*E*(1-E)
        b=p-p*p*y;B=4*b*b*(1-b*b)
        A=ell+(1-ell)*B
        return z*(A+B)-z*z*A*B
    def entropy(r):
        return -(r*np.log(r)+(1-r)*np.log(1-r))/lp
    def F(x,y):
        return -alpha*beta*(entropy(click(x,y))-entropy(r0))
    a=np.imag(F(1j*1e-20,0))/1e-20
    assert a<0
    out=0j
    tau=.05
    for j,rho in enumerate(weights):
        f=star_density(star_node(nodes[j]),star_node(nodes[j+1]),h)
        q=matter_query(nodes[j])
        out+=rho*F(-tau*f/rho,tau*q/rho)
    return out/(-tau*a)

def direct_coframe_second_variations(nodes,h,weights):
    """Independent 75-digit ORIGINAL N1 CQ PRICE second differences in
    two REAL raw coframe directions, without using the Euler derivative.
    The original literal six-face holonomies are re-evaluated every time.
    """
    from importlib.machinery import SourceFileLoader
    native_path=(Path(__file__).resolve().parents[4]/
       "02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py")
    Golden=SourceFileLoader("d0_native_n1_second_price",str(native_path)).load_module().GoldenMaster
    model=Golden(75)
    tau=.05
    def price(nn):
        value=model.a*0
        for j,rho in enumerate(weights):
            f=float(star_density(star_node(nn[j]),star_node(nn[j+1]),h).real)
            q=float(matter_query(nn[j]).real)
            value+=rho*model.F(-tau*f/rho,tau*q/rho)
        return value/(-tau*model.a)
    step=.0003
    base=price(nodes)
    values=[]
    for a,mu in ((0,0),(1,1)):
        terms=[]
        for sign in (-1,1):
            trial=[dict(e=c['e'].copy(),U=c['U'].copy(),v=c['v'].copy())
                   for c in nodes]
            trial[1]['e'][a,mu]+=sign*step
            terms.append(price(trial))
        values.append(float((terms[0]-2*base+terms[1])/(step*step)))
    assert values[0]>2 and values[1]<-.7,values
    return dict(d2_e00=values[0],d2_e11=values[1],
                native_positive_and_negative_curvature=True,
                numerical_unrestricted_original_coframe_minimum=False)

def direct_42_jets(nodes,h,weights):
    """Verify EACH of 42 sources directly from complex differentiation
    of the original N1 ENTROPY VALUE rather than differentiating a
    pre-assembled source. All true original coframe/Lorentz/material jets.
    """
    assert len(nodes)==3
    dx=1e-20
    out=[]
    for k in range(42):
        a=[dict(e=c['e'].astype(complex).copy(),
                U=c['U'].astype(complex).copy(),
                v=c['v'].astype(complex).copy()) for c in nodes]
        if k<16:
            a[1]['e'][k//4,k%4]+=1j*dx
        elif k<40:
            axis,gen=divmod(k-16,6)
            a[1]['U'][axis]=expm(1j*h*dx*L[gen])@a[1]['U'][axis]
        else:
            A=k-40
            a[0]['v'][A,0]+=1j*dx/h
            a[1]['v'][A,0]-=1j*dx/h
        out.append(np.imag(direct_CQ_value(a,h,weights))/dx)
    return np.array(out,float)

def run(weights=(1.,1.),n=2,limit=50):
    h,base,psi,rhos,fields,euler=problem(n,list(weights))
    z0=np.zeros(42*(n-1))
    before=euler(z0)
    t0=time.time()
    sol=least_squares(euler,z0,method='trf',x_scale='jac',
                      max_nfev=limit,ftol=1e-12,xtol=1e-12,gtol=1e-12)
    E,source,nodes=euler(sol.x,True)
    error=float(np.max(abs(E)))
    if n!=2 or error>3e-12:
        raise AssertionError(("bounded numerical root not confirmed",n,error))
    # INDEPENDENT full N1 entropy source in all 42 field directions.
    direct=direct_42_jets(nodes,h,rhos)
    diff=float(np.max(abs(direct-E)))
    assert diff<5e-12 and max(abs(direct))<5e-12,(diff,max(abs(direct)))
    # Full 42x42 numerical Jacobian of the EXACT source, not a 12-rank
    # projection. Collar-fixed variables are ONLY the one internal site.
    J=approx_derivative(euler,sol.x,method='3-point',abs_step=5e-6)
    vals=svdvals(J)
    assert len(vals)==42 and vals.min()>.03,(len(vals),vals.min())
    # At a whole-source stationary point, the 16 raw coframe-coordinate
    # rows/columns of the numerical Jacobian ARE the genuine Hessian of
    # the same CQ price along fixed link/scalar variations. No Lie-chart
    # correction is needed inside this pure coframe block.
    Hco=J[:16,:16]
    asym=float(np.max(abs(Hco-Hco.T)))
    eig=np.linalg.eigvalsh((Hco+Hco.T)/2)
    negative=int(np.count_nonzero(eig < -1e-3))
    positive=int(np.count_nonzero(eig > 1e-3))
    assert asym<1e-7 and negative==8 and positive==8,(asym,eig)
    second_direct=direct_coframe_second_variations(nodes,h,rhos)
    # Genuine original metric, nonflat SO(1,3) spatial based plaquettes
    # and rank-two REAL matter are checked independently.
    sig=[];comm=[];stress=[]
    for c in nodes[:-1]:
        ev=np.linalg.eigvalsh(c['e'].T@ETA@c['e'])
        assert (ev>0).sum()==1 and (ev<0).sum()==3
        sig.append([float(x) for x in ev])
        for axis,b in ((1,2),(1,3),(2,3)):
            P=c['U'][axis]@c['U'][b]@np.linalg.inv(c['U'][axis])@np.linalg.inv(c['U'][b])
            comm.append(float(np.linalg.norm(P-I)))
        T=sum(np.outer(p,p) for p in c['v'])
        stress.append(int(np.linalg.matrix_rank(T)))
        assert stress[-1]==2
    assert max(comm)>.01
    assert max(abs(source['f']))<.03 and max(abs(source['q']))<.001
    assert max(abs(-.05*source['f']/np.array(rhos)))<.25
    assert max(abs(.05*source['q']/np.array(rhos)))<2**-12
    assert not np.any(np.isnan(vals))
    return dict(status="PASS_NUMERICAL_COMPLETE_CONFIGURED_N1_42_EULER_SINGLE_INTERNAL",
      PF=list(weights),intervals=n,step=h,
      original_complete_source_max=error,
      direct_entire_n1_value_42_source_max=float(max(abs(direct))),
      analytic_vs_direct_entire_price_max=diff,
      original_euler_before=float(max(abs(before))),
      coframe_source_max=float(max(abs(source['e'][1:n].ravel()))),
      raw_link_source_max=float(max(abs(source['U'][1:n].ravel()))),
      scalar_source_max=float(max(abs(source['psi'][1:n].ravel()))),
      full_42by42_J_singular_min=float(vals.min()),
      full_42by42_J_singular_max=float(vals.max()),
      fixed_link_matter_original_coframe_Hessian=dict(
        positive=positive,negative=negative,
        eig_min=float(eig.min()),eig_max=float(eig.max()),
        symmetry_error_inf=asym,
        unrestricted_16coframe_minimum=False),
      independent_original_complete_price_second_jet=second_direct,
      Lorentz_metric_inertia=sig,
      original_spatial_based_holonomy_norms=comm,
      two_REAL_CAR_stress_ranks=stress,
      original_fstar=[float(x) for x in source['f']],
      original_twofield_q=[float(x) for x in source['q']],
      max_parameter_change=float(max(abs(sol.x))),nfev=int(sol.nfev),
      time_s=time.time()-t0,
      scope=dict(finite_float_root_not_validated_interval_existence=True,
       three_plus_intervals_stationary_root_proved=False,
       all42_original_field_directions_checked=True,
       full_nonlin_same_N1_not_sigma_plus=True,
       spatial_homogeneous_fields_and_PF=True,
       actual_native_AF_counts_used=False,
       original_primitive_writer_admitted=False,
       compulsory_complete_Book03_selected=False,
       GR_closed=False))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",type=Path)
    args=parser.parse_args()
    a=run((1.,1.))
    b=run((1.,2.))
    result=dict(status="PASS_TWO_FINITE_FULL42_NUMERICAL_CONFIGURED_CQ_ROOTS",
                witnesses=[a,b])
    content=json.dumps(result,indent=2)+"\n"
    print(content)
    if args.json:args.json.write_text(content)
