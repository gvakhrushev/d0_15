#!/usr/bin/env python3
"""Reproducible weighted/two-field continuation: exact rank-two non-VSI source,
correct volume representative, exact finite matter lift, and material Ward defect.

Consumes the CURRENT weighted Ward and stationary-form theorems. It does not
re-create a missing historical receipt, derive a physical Book selector, or
claim a complete finite all42 root. No existing repository file is modified.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import subprocess
import numpy as np
import sympy as s
import mpmath as mp
from scipy.optimize import brentq
from scipy.special import erfi
from native_master import GoldenMaster

INPUT_REF='401eafb2958e9d9626db833a25f02b35b3871c16'
CHECKS=[]

def require(ok, name):
    if not bool(ok):
        raise ArithmeticError('FAILED: '+name)
    CHECKS.append(name)

def zero(expr,name):
    if isinstance(expr,s.MatrixBase):
        ok=all(s.simplify(v)==0 for v in expr)
    else:
        ok=s.simplify(expr)==0
    require(ok,name)

def symbolic_ward():
    x,y,rho,fx,fy,dx,dy,dfx,drho=s.symbols('x y rho fx fy dx dy dfx drho', nonzero=True)
    T=x*fx-y*fy
    ward=fy*dy-x*dfx+y*fy*drho/rho
    invariant=drho*y/fx+rho*dy/fx-rho*y*dfx/fx**2
    zero(ward-fx*fy*invariant/rho+T*dfx/fx,'weighted_Ward_factorization_through_y_zero')
    a,tau,Q,U=s.symbols('a tau Q U',nonzero=True)
    zero((rho*y/fx).subs({y:U*tau*Q/rho,fx:a*U})-tau*Q/a,'current_owner_positive_y_convention')
    # Nonlinearity vanishes at Q=0 in first source, not in the full Hessian.
    b,k2,k3,M=s.symbols('b k2 k3 M',nonzero=True)
    q=s.symbols('q')
    K=b*q+k2*q*q/2+k3*q**3/6
    V=M*rho*K.subs(q,tau*Q/rho)
    zero(s.diff(V,Q).subs(Q,0)-M*tau*b,'uniform_linear_material_slope')
    zero(s.diff(V,Q,2).subs(Q,0)-M*tau*tau*k2/rho,'nonlinear_Hessian_not_deleted')
    # The weighted completion has an exact independent-upstream row too.
    pressure=s.diff(V,rho)
    expected=M*(K-q*s.diff(K,q)).subs(q,tau*Q/rho)
    zero(pressure-expected,'complete_moving_rho_source')
    zero(pressure.subs(Q,0),'null_family_density_source_of_material_term_zero')
    require(s.simplify(s.diff(pressure,Q,2).subs(Q,0))!=0,'rho_source_not_zero_off_null')
    # Positive joint target metric: two gradients of opposite SPACETIME norm,
    # not an internal target-space minus sign or a ghost assertion.
    eta=s.diag(1,-1,-1,-1)
    v1=s.Matrix([1,0,0,0]);v2=s.Matrix([0,1,0,0])
    stress=v1*v1.T+v2*v2.T
    zero((v1.T*eta*v1)[0]+(v2.T*eta*v2)[0],'total_Q_zero_with_two_nonzero_gradients')
    require(stress.rank()==2,'total_Q_zero_does_not_force_rank_one_dust')
    vp=(v1+v2)/s.sqrt(2);vm=(v1-v2)/s.sqrt(2)
    zero((vp.T*eta*vp)[0],'counterstream_plus_is_null')
    zero((vm.T*eta*vm)[0],'counterstream_minus_is_null')
    zero(vp*vp.T+vm*vm.T-stress,'two_counterstream_source_exact_decomposition')
    return {'convention':'y=+tau*Q/rho; sigma=-1 is already inside F',
            'weighted_invariant':'d(rho*y/F_x)=0',
            'reduced_constraint':'d Q_E=0',
            'two_field_converse':'LOCAL_WITH_SUPPLIED_POSITIVE_VOLUME_MATCH',
            'previous_65_check_receipt_recovered':False}

def geometry(g,derivative):
    inv=s.simplify(g.inv());n=g.rows
    @lru_cache(None)
    def Gamma(a,b,c):
        return s.simplify(sum(inv[a,d]*(derivative(g[d,c],b)+derivative(g[d,b],c)-derivative(g[b,c],d)) for d in range(n))/2)
    ric=s.Matrix(n,n,lambda a,b:s.simplify(sum(derivative(Gamma(c,a,b),c)-derivative(Gamma(c,a,c),b)+sum(Gamma(c,c,d)*Gamma(d,a,b)-Gamma(c,b,d)*Gamma(d,a,c) for d in range(n)) for c in range(n))))
    R=s.simplify(s.trace(inv*ric))
    return inv,Gamma,ric,R,s.simplify(ric-g*R/2)

def exact_rank2():
    r=s.symbols('r',positive=True)
    c,kappa,epsilon=s.symbols('c kappa epsilon',positive=True)
    exp=s.exp(r*r/2)
    g=s.diag(r*exp,-exp/r,-r*r,-r*r)
    def d(f,i):return s.diff(f,r) if i==0 else s.S.Zero
    inv,Ga,ric,R,G=geometry(g,d)
    v1=s.Matrix([r,0,0,0]);v2=s.Matrix([0,1,0,0]);P=v1*v1.T+v2*v2.T
    zero(ric-s.diag(1,r**-2,0,0),'seed_all_Ricci_components')
    zero(R,'seed_scalar_curvature_zero')
    zero(G-P/r**2,'seed_all_ten_Einstein_components')
    zero((v1.T*inv*v1)[0]+(v2.T*inv*v2)[0],'seed_total_kinetic_zero')
    e=r*r*exp
    zero(g.det()+e*e,'seed_volume_density')
    for j,v in enumerate((v1,v2)):
        current=e*(inv*v)/r**2
        zero(sum(d(current[i],i) for i in range(4)),f'seed_scalar_current_{j}')
    invariant=s.simplify(s.trace(inv*ric*inv*ric))
    zero(invariant-2*s.exp(-r*r)/r**2,'nonVSI_Ricci_squared_exact')
    require(invariant.subs(r,1)>0,'nonVSI_nonzero_invariant')
    require(G.rank()==2,'seed_Einstein_source_rank_two')
    # t satisfies dt/dr=exp(r^2/2)/c. r is a shorthand for r(t),
    # and derivative_t = c exp(-r^2/2) derivative_r on every component.
    qg=s.diag(c*c*r/exp,-exp/r,-r*r,-r*r)
    def dt(f,i):return s.simplify(c/exp*s.diff(f,r)) if i==0 else s.S.Zero
    qi,QGamma,Qric,QR,QG=geometry(qg,dt)
    w1=s.Matrix([epsilon*c*r/exp,0,0,0]);w2=s.Matrix([0,epsilon,0,0])
    Pnew=w1*w1.T+w2*w2.T
    enew=c*r*r;mu=1/(epsilon*epsilon*r*r)
    zero(QG-mu*Pnew,'mass_coordinate_all_ten_Einstein_components')
    zero(QR,'mass_coordinate_scalar_curvature_zero')
    zero((w1.T*qi*w1)[0]+(w2.T*qi*w2)[0],'mass_coordinate_total_kinetic_zero')
    zero(qg.det()+enew*enew,'mass_coordinate_volume_density')
    zero((enew*mu).subs(c,kappa*epsilon**2)-kappa,'native_finite_Golden_coupling_volume_match')
    # This is the actual fixed-measure field source: coefficient b/a=-kappa.
    zero((QG-kappa*Pnew/enew).subs(c,kappa*epsilon**2),'original_CQ_metric_source_after_volume_match')
    for j,w in enumerate((w1,w2)):
        current=qi*w
        zero(sum(dt(current[i],i) for i in range(4)),f'original_undensitized_scalar_equation_{j}')
    zero(s.simplify(s.trace(qi*Qric*qi*Qric))-invariant,'nonVSI_invariant_survives_required_clock_change')
    # One REAL coframe and all its Lorentz spin-connection equations.
    tetrad=s.diag(c*s.sqrt(r)*s.exp(-r*r/4),s.exp(r*r/4)/s.sqrt(r),r,r)
    eta=s.diag(1,-1,-1,-1);ti=tetrad.inv()
    zero(tetrad.T*eta*tetrad-qg,'original_coframe_real_and_nondegenerate')
    omega=[]
    for m in range(4):
        gamma=s.Matrix(4,4,lambda i,j:QGamma(i,m,j))
        de=tetrad.applyfunc(lambda v:dt(v,m))
        om=s.simplify((tetrad*gamma-de)*ti)
        omega.append(om)
        zero(om.T*eta+eta*om,f'spin_connection_Lorentz_direction_{m}')
    for a in range(4):
        for m in range(4):
            for n in range(m+1,4):
                Tor=dt(tetrad[a,n],m)-dt(tetrad[a,m],n)+sum(omega[m][a,b]*tetrad[b,n]-omega[n][a,b]*tetrad[b,m] for b in range(4))
                zero(Tor,f'Cartan_torsion_{a}_{m}_{n}')
    # A wrong fixed-coordinate interpretation fails BEFORE its inverse map.
    mismatch=s.simplify(G-kappa*P/e)
    require(mismatch!=s.zeros(4),'omitted_volume_matching_rejected')
    # rho enters neither source at x=y=0; preserve this as algebra, not a
    # new physical gauge or an assertion that independent upstream rows vanish.
    return {'seed_metric':'diag(r*exp(r^2/2),-exp(r^2/2)/r,-r^2,-r^2)',
            'seed_scalars':['r^2/2','x'],
            'seed_mu':'1/r^2','scalar_R':'0','source_rank':2,
            'Ricci_squared':str(invariant),
            'CQ_coordinates_not_execution_clock':'dt/dr=exp(r^2/2)/(kappa*epsilon^2)',
            'native_metric':'diag(c^2*r*exp(-r^2/2),-exp(r^2/2)/r,-r^2,-r^2)',
            'native_scalars':['epsilon*(r(t)^2-r0^2)/2','epsilon*x'],
            'native_c':'kappa*epsilon^2',
            'torsion_equations_checked':24,
            'not_VSI':True,'finite_geometric_root_claimed':False}

def native_master_checks(master):
    require(master.a<0 and master.b>0,'native_original_a_b_signs')
    require(master.k2>0,'native_original_K_second_derivative_positive')
    require(master.u1>0,'native_original_U_first_derivative_positive')
    p,z=master.p,master.z
    L=4*p**3;Q=1-z*L;R=1-z*L*(1+p**6)
    kappa=2*p**-5*(R/Q+p**6)
    require(abs(master.kappa-kappa)<mp.mpf('1e-55'),'finite_z_coupling_not_asymptotic_replacement')
    rows=[]
    q0=mp.mpf('0.001');tau=mp.mpf('0.05')
    for rho in (mp.mpf('.5'),mp.mpf(1),mp.mpf(2),mp.mpf(3)):
        t=tau*q0/rho
        x,u,k,kp=master.section(t)
        fy=master.fy(x,u*t);fx=master.fx(x,u*t)
        require(abs(x*fx-u*t*fy)<mp.mpf('1e-55'),'native_trace_root_rho_'+str(rho))
        require(abs(rho*(u*t)/fx-tau*q0/master.a)<mp.mpf('1e-50'),'native_weighted_invariant_rho_'+str(rho))
        require(abs(kp-u*fy)<mp.mpf('1e-60'),'native_master_envelope_rho_'+str(rho))
        rows.append({'rho':mp.nstr(rho,10),'U':mp.nstr(u,35),'e_times_mu':mp.nstr(-kp/master.a,35)})
    return {'precision_digits':mp.mp.dps,'K_pre':9,'L_gate':20,
            'a':mp.nstr(master.a,45),'b':mp.nstr(master.b,45),
            'kappa':mp.nstr(master.kappa,45),'K2':mp.nstr(master.k2,45),
            'U1':mp.nstr(master.u1,45),'weighted_samples':rows,
            'scope':'actual original scalar detector polynomial, NOT a rerun of its full compiler'}

def finite_matter_lift(kappa):
    aa,cc,ee=s.symbols('aa cc ee',positive=True)
    zero((ee*cc*aa)**2/(cc*cc*aa)+ee**2/(-1/aa),'exact_finite_matter_null_constraint_all_sites')
    zero(ee*cc*aa/(cc*cc*aa)-ee/cc,'exact_finite_time_current_constant_all_sites')
    eps=.1;c=float(kappa)*eps*eps
    rleft,rright=1.,1.2
    def clock(r):return np.sqrt(np.pi/2)*erfi(r/np.sqrt(2))/c
    t0,t1=clock(rleft),clock(rright)
    def radius(t):return brentq(lambda rr:clock(rr)-t,rleft-1e-8,rright+1e-8,xtol=5e-15)
    rows=[]
    previous=None
    for n in (16,32,64,128):
        grid=np.linspace(t0,t1,n+1);h=(t1-t0)/n
        mid=(grid[:-1]+grid[1:])/2
        rm=np.array([radius(t) for t in mid]);rv=np.array([radius(t) for t in grid])
        g00=c*c*rm*np.exp(-rm*rm/2);g11=-np.exp(rm*rm/2)/rm
        p0=eps*c*rm*np.exp(-rm*rm/2)
        psi=np.r_[0.,np.cumsum(h*p0)]
        exact=eps*(rv*rv-rleft*rleft)/2
        q=p0*p0/g00+eps*eps/g11
        j=p0/g00
        residual=float(np.max(abs(np.diff(j)/h)))
        require(np.max(abs(q))<2e-17,'finite_forward_Q_zero_'+str(n))
        require(residual<1e-10,'finite_actual_material_adjoint_zero_'+str(n))
        error=float(np.max(abs(psi-exact)))
        ratio=None if previous is None else previous/error
        if ratio is not None:require(3.95<ratio<4.05,'finite_midpoint_Oh2_diagnostic_'+str(n))
        # Original sitewise PF weights may be inhomogeneous: all receive t=0.
        rho=1+.4*np.sin(mid)
        require(np.all(rho>.5),'finite_positive_PF_weights_'+str(n))
        require(np.max(abs(q/rho))<4e-17,'finite_weighted_operand_zero_'+str(n))
        rows.append({'steps':n,'h':h,'Q_error':float(np.max(abs(q))),
                     'two_material_rows_error':residual,
                     'matter_amplitude_error':error,'error_ratio':ratio})
        previous=error
    return {'epsilon':eps,'r_interval':[rleft,rright],
            'coupling_kappa':float(kappa),'c':c,
            'actual_forward_material_stencil':True,'same_midpoint_readout':True,
            'geometric_Euler_rows_NOT_solved':True,'samples':rows}

def forward(f,j,h):return (np.roll(f,-1,axis=j)-f)/h

def backward(f,j,h):return (f-np.roll(f,1,axis=j))/h

def ward_fixture(d,n):
    h=2*np.pi/n
    axes=[np.arange(n)*h for _ in range(d)]
    xx=np.meshgrid(*axes,indexing='ij');shape=(n,)*d
    G=np.zeros((d,d)+shape)
    for i in range(d):G[i,i]=(1 if i==0 else -1)+.08*np.sin(xx[i])
    G[0,1]=G[1,0]=.025*np.cos(xx[0]+xx[1])
    fields=np.array([.07*np.sin(xx[0]+xx[1])+.03*np.cos(xx[-1]),
                     .05*np.cos(xx[0]-.4*np.sin(xx[1]))+.02*np.sin(xx[-1])])
    # Use integer harmonics for periodic smoothness, including at the seam.
    xi=np.array([.1*np.sin(xx[j]+xx[(j+1)%d]) for j in range(d)])
    p=np.array([[forward(f,j,h) for j in range(d)] for f in fields])
    DG=np.array([[ [forward(G[i,j],k,h) for j in range(d)] for i in range(d)] for k in range(d)])
    Dp=np.array([[[forward(p[a,j],k,h) for j in range(d)] for a in range(2)] for k in range(d)])
    Dxi=np.array([[forward(xi[j],k,h) for j in range(d)] for k in range(d)])
    q=np.einsum('ij...,ai...,aj...->...',G,p,p)
    dpsi=np.einsum('j...,aj...->a...',xi,p)
    dp=np.array([[forward(f,j,h) for j in range(d)] for f in dpsi])
    dG=np.zeros_like(G)
    for i in range(d):
        for j in range(d):
            for k in range(d):
                dG[i,j]+=xi[k]*DG[k,i,j]-G[k,j]*Dxi[k,i]-G[i,k]*Dxi[k,j]
    dq=np.einsum('ij...,ai...,aj...->...',dG,p,p)+2*np.einsum('ij...,ai...,aj...->...',G,p,dp)
    transport=sum(xi[j]*forward(q,j,h) for j in range(d))
    error=dq-transport
    explicit=np.zeros(shape);Cnu=np.zeros((d,)+shape)
    weight=1+.2*np.cos(xx[0])
    flux=np.zeros((d,d)+shape)
    for a in range(2):
        for i in range(d):
            for j in range(d):
                for v in range(d):
                    prod=DG[v,i,j]*(Dp[v,a,i]*p[a,j]+p[a,i]*Dp[v,a,j])
                    prod+=G[i,j]*Dp[v,a,i]*Dp[v,a,j]+h*DG[v,i,j]*Dp[v,a,i]*Dp[v,a,j]
                    Cnu[v]+=prod
                    explicit+=2*h*G[i,j]*p[a,i]*Dxi[j,v]*Dp[j,a,v]-h*xi[v]*prod
                    flux[j,v]+=weight*G[i,j]*p[a,i]*Dp[j,a,v]
    defect_coeff=np.array([2*sum(backward(flux[j,v],j,h) for j in range(d))+weight*Cnu[v] for v in range(d)])
    lhs=float(np.sum(weight*error)*h**d)
    rhs=float(-h*np.sum(xi*defect_coeff)*h**d)
    require(np.max(abs(error-explicit))<2e-14,f'exact_material_forward_Lie_defect_d{d}_n{n}')
    require(abs(lhs-rhs)<2e-12,f'full_weighted_summation_by_parts_d{d}_n{n}')
    # Riesz coefficient of the actual non-densitized scalar first source.
    source=np.array([weight*forward(q,v,h)-h*defect_coeff[v] for v in range(d)])
    require(abs(float(np.sum(weight*dq)*h**d)-float(np.sum(xi*source)*h**d))<2e-12,
            f'actual_material_Ward_covector_d{d}_n{n}')
    require(np.max(abs(error))>1e-9,f'finite_chain_rule_is_not_falsely_zero_d{d}_n{n}')
    return {'dimension':d,'side_sites':n,'h':h,'pointwise_defect':float(np.max(abs(error))),
            'defect_divided_by_h':float(np.max(abs(error))/h),
            'identity_error':float(np.max(abs(error-explicit))),
            'weighted_IBP_error':abs(lhs-rhs)}

def finite_ward():
    h,g,dg,p,dp,q,dq=s.symbols('h g dg p dp q dq')
    correction=dg*(dp*q+p*dq)+g*dp*dq+h*dg*dp*dq
    zero(((g+h*dg)*(p+h*dp)*(q+h*dq)-g*p*q)/h-(dg*p*q+g*(dp*q+p*dq))-h*correction,'exact_triple_forward_product_rule')
    samples=[ward_fixture(2,n) for n in (16,32,64)]
    samples.append(ward_fixture(4,6))
    return {'all_dimensions_formula_proved':True,'diagnostics':samples,
            'native_q_dictionary':'inverse metric times original forward scalar differences',
            'geometric_Lie_defect_computed':False,
            'consequence':'k D+q=-a e_geom+h R_material-r_extra; no term set to zero',
            'finite_Q_constancy_proved_for_all_roots':False}

def literal_coframe_bridge():
    # The maintained repository uses the sampled Lie tangent of the coframe,
    # not a separately sampled inverse-metric Lie tangent. Their difference
    # is an EXACT inverse-product defect; preserve it rather than rename it.
    d,n=4,5;h=2*np.pi/n;shape=(n,)*d
    xx=np.meshgrid(*([np.arange(n)*h]*d),indexing='ij')
    eta=np.diag([1.,-1.,-1.,-1.])
    e=np.zeros(shape+(4,4))
    for j in range(4):e[...,j,j]=1+.04*np.sin(xx[j])
    e[...,0,1]=.025*np.cos(xx[0]+xx[1])
    g=np.einsum('...ai,ab,...bj->...ij',e,eta,e);G=np.linalg.inv(g)
    fields=np.stack([.05*np.sin(xx[0]+xx[1]),.06*np.cos(xx[2]-xx[3])],axis=-1)
    p=np.stack([forward(fields,j,h) for j in range(d)],axis=-1)
    xi=np.stack([.1*np.sin(xx[j]+xx[(j+1)%d]) for j in range(d)],axis=-1)
    de=sum(xi[...,j,None,None]*forward(e,j,h) for j in range(d))
    for mu in range(d):
        de[..., :,mu]+=sum(e[..., :,j]*forward(xi[...,j],mu,h)[...,None] for j in range(d))
    def jetG(ee):
        dg=np.einsum('...ai,ab,...bj->...ij',ee,eta,e)+np.einsum('...ai,ab,...bj->...ij',e,eta,ee)
        return -np.einsum('...ij,...jk,...kl->...il',G,dg,G)
    glit=jetG(de)
    gmetric=sum(xi[...,v,None,None]*forward(G,v,h) for v in range(d))
    for mu in range(d):
        for lam in range(d):
            gmetric[...,mu,lam]-=sum(G[...,v,lam]*forward(xi[...,mu],v,h)+G[...,mu,v]*forward(xi[...,lam],v,h) for v in range(d))
    Bs=[];max_chain=0.
    for v in range(d):
        ev=forward(e,v,h);gv=forward(G,v,h);gp=np.roll(G,-1,axis=v)
        L=np.einsum('...ai,ab,...bj->...ij',ev,eta,e)+np.einsum('...ai,ab,...bj->...ij',e,eta,ev)
        He=np.einsum('...ai,ab,...bj->...ij',ev,eta,ev)
        B=jetG(ev)-gv
        formula=h*(np.einsum('...ij,...jk,...kl->...il',gv,L,G)+np.einsum('...ij,...jk,...kl->...il',gp,He,G))
        max_chain=max(max_chain,float(np.max(abs(B-formula))))
        require(np.max(abs(B-formula))<3e-14,'literal_coframe_inverse_chain_direction_'+str(v))
        Bs.append(B)
    Bxi=sum(xi[...,v,None,None]*Bs[v] for v in range(d))
    require(np.max(abs(glit-gmetric-Bxi))<3e-14,'literal_coframe_vs_metric_Lie_tangent_exact_difference')
    corr=np.stack([np.einsum('...ij,...Ai,...Aj->...',B,p,p) for B in Bs],axis=-1)
    diff=np.einsum('...ij,...Ai,...Aj->...',glit-gmetric,p,p)
    require(np.max(abs(diff-np.sum(xi*corr,axis=-1)))<3e-14,'literal_material_source_contains_B_not_zero')
    require(np.max(abs(corr))>1e-8,'coframe_chain_correction_really_nonzero')
    return {'dimension':4,'sites':n**d,'max_inverse_chain_identity_error':max_chain,
            'coframe_metric_material_correction_max':float(np.max(abs(corr))),
            'literal_source_balance':'k D+q=-a e_geom+h R_material-k B:p:p-r_extra',
            'coframe_and_inverse_metric_tangents_identified':False}

def verify_pins(repo):
    records=json.loads((Path(__file__).with_name('SOURCE_INPUTS.json')).read_text())['inputs']
    if repo is None:return {'checked':False,'reason':'offline standalone replay; use --repo for Git-object validation'}
    repo=Path(repo).resolve();out=[]
    for item in records:
        spec=INPUT_REF+':'+item['path']
        blob=subprocess.check_output(['git','-C',str(repo),'rev-parse',spec],text=True).strip()
        require(blob==item['git_blob'],'pinned_git_blob_'+Path(item['path']).name)
        out.append({'path':item['path'],'git_blob':blob})
    return {'checked':True,'objects':out}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',type=Path)
    ap.add_argument('--output',type=Path,help='Write a separate receipt; default is stdout only')
    args=ap.parse_args()
    pins=verify_pins(args.repo)
    result={'status':'PASS_WEIGHTED_TWO_FIELD_RANK2_AND_FINITE_MATERIAL_BRIDGE','input_ref':INPUT_REF}
    result['weighted_completion']=symbolic_ward()
    result['rank2_geometry']=exact_rank2()
    master=GoldenMaster(70)
    result['native_master']=native_master_checks(master)
    result['finite_matter']=finite_matter_lift(master.kappa)
    result['finite_Ward']=finite_ward()
    result['literal_coframe_bridge']=literal_coframe_bridge()
    result['input_pins']=pins
    result['checks_passed']=len(CHECKS)
    result['checks']=CHECKS
    result['scope']={'weighted_invariant_already_in_repository':True,
                     'rank_two_nonVSI_also_published_concurrently':True,
                     'new_exact_finite_material_lift':True,
                     'original_metric_on_null_density_branch':True,
                     'finite_matter_rows_exact_in_reduced_price':True,
                     'full_finite_16_coframe_24_link_rows_solved':False,
                     'native_field_writer_admission_proved':False,
                     'compulsory_Book_valuation_proved':False,
                     'independent_upstream_stationarity_proved':False,
                     'new_Lean_build':False,'independent_review':False,'GR_closed':False}
    text=json.dumps(result,indent=2,ensure_ascii=False)
    print(text)
    if args.output:args.output.write_text(text+'\n',encoding='utf-8')

if __name__=='__main__':main()
