#!/usr/bin/env python3
"""D0 original Golden PF depth + exact two-real-CAR time-layer Euler elimination.

No new law, detector, source, or physical Book03 selection. Original Golden
N1 analytic r(x,-y), original L8 true F/R-box counts, and original rank-two
finite six-face star are reused. mpmath.iv is used for a whole-rectangle
analytic curvature bound; subsequent floating nonlinear root is a diagnostic.
"""
import math,json
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
from scipy.special import erfi

p=(math.sqrt(5)-1)/2
z=2**-20
ph=1/p
lnphi=math.log(ph)
alpha=(1-(1-2*p**3)**9)**128
beta=((1-p**120)**4*(1-(1-16*p**9)**20))**43
mult=alpha*beta
kappa=2*p**-5*((1-z*4*p**3*(1+p**6))/(1-z*4*p**3)+p**6)
assert abs(kappa-23.416406751884075)<1e-12

def native_derivatives(x,y):
    """F_y,F_yy of the same sigma-minus N1 CQ GoldenMaster F(x,y)."""
    raw=-y
    u=p+p*p*raw
    E=p*p*(1+x)
    ell=4*E*(1-E)
    B=4*u*u*(1-u*u)
    A=ell+(1-ell)*B
    r=1-(1-z*B)*(1-z*A)
    assert 0<r<.5
    B1=(8*u-16*u**3)*p*p
    B2=(8-48*u*u)*p**4
    T=(1-z*A)+(1-ell)*(1-z*B)
    r1=z*B1*T
    r2=z*(B2*T-2*z*(1-ell)*B1**2)
    hp=math.log((1-r)/r)/lnphi
    Fy=mult*hp*r1
    Fyy=mult*(r1*r1/(r*(1-r)*lnphi)-hp*r2)
    return r,Fy,Fyy

def iv_positive_box():
    iv=mp.iv;iv.dps=45
    P=(iv.sqrt(5)-1)/2;Z=iv.mpf(1)/2**20
    x=iv.mpf([-1/128,1/128]);y=iv.mpf([-1/128,1/128])
    u=P-P*P*y;E=P*P*(1+x);ell=4*E*(1-E)
    B=4*u*u*(1-u*u);A=ell+(1-ell)*B
    r=1-(1-Z*B)*(1-Z*A)
    B1=(8*u-16*u**3)*P*P;B2=(8-48*u*u)*P**4
    T=(1-Z*A)+(1-ell)*(1-Z*B)
    r1=Z*B1*T;r2=Z*(B2*T-2*Z*(1-ell)*B1**2)
    lp=iv.log(1/P);hp=iv.log((1-r)/r)/lp
    yy=hp*r1
    y2=r1*r1/(r*(1-r)*lp)-hp*r2
    # Any fixed orthogonal spatial contribution qperp is allowed, provided
    # |Y-Yperp|<=1/128; the radial eigenvalue is Fy+2(Y-Yperp) Fyy.
    radial=yy+2*iv.mpf([-1/128,1/128])*y2
    def lo(v):return float(v.a)
    def hi(v):return float(v.b)
    assert lo(r)>0 and hi(r)<.5
    assert lo(yy)>1e-5 and lo(radial)>1e-5
    assert lo(y2)>0
    return dict(rectangle=[-1/128,1/128],r=[lo(r),hi(r)],
                normalized_Fy=[lo(yy),hi(yy)],
                normalized_Fyy=[lo(y2),hi(y2)],
                normalized_longitudinal_eigenvalue=[lo(radial),hi(radial)],
                alpha_beta=mult)

def original_counts(n,L):
    counts=np.zeros(L**4,dtype=int)
    def visit(rem,dep,left,width):
        if rem==0:
            index=0
            for a in range(4):
                index=index*L+max(0,min(L-1,int(math.floor(L*(left[a]+width[a]/2)))))
            counts[index]+=1
            return
        axis=dep%4
        wf=width.copy();wf[axis]*=p
        visit(rem-1,dep+1,left.copy(),wf)
        if rem>=2:
            lr=left.copy();wr=width.copy();lr[axis]+=p*wr[axis];wr[axis]*=p*p
            visit(rem-2,dep+1,lr,wr)
    visit(n,0,[0.]*4,[1.]*4)
    f0,f1=0,1
    for _ in range(n+1):f0,f1=f1,f0+f1
    assert counts.sum()==f0 and np.min(counts)>0
    return counts

def pf_depth_proof(L):
    h=1/L
    s=int(math.ceil(math.log(L)/math.log(ph)))
    n=64*s+128;k=n//4
    am=(1/p)/math.sqrt(5)
    an=(1-p**(2*n+1)*(-1)**(n+1)/math.sqrt(5)) if False else (am+(-1)**n *p**(2*n+1)/math.sqrt(5))
    eps=p**(2*(n-2*k)+1)/math.sqrt(5)
    delta=2*p**(k//4)
    raw=(L**4*eps+128*L*delta+p**(2*n+1)/math.sqrt(5))/an
    assert delta<=1/(2*L)
    assert raw<9*h**3
    e=9*h**3
    d1=(2*e)/(1-e)/h
    d2=(4*e)/(1-e)/(h*h)
    assert d1<36*h*h and d2<72*h
    return dict(L=L,Golden_cost=n,letter_prefix_length=k,bound_rho_minus_one=raw,
         claimed_rho_bound=9*h**3,log_gradient_bound=36*h*h,
         log_second_diff_bound=72*h,delta=delta,epsilon=eps,
         ready_probability=2*an*p**3)

def time_at_radius(R):
    return math.sqrt(math.pi/2)*(erfi(R/math.sqrt(2))-erfi(1/math.sqrt(2)))
def radius(t):
    return brentq(lambda R: time_at_radius(R)-t, .54,1.9,xtol=2e-14)
def native_star_finite(t,h):
    R=radius(t);RN=radius(t+h)
    a=math.sqrt(R)*math.exp(-R*R/4)
    b=math.exp(R*R/4)/math.sqrt(R)
    k1=lambda v:(1-v**-2)/2
    k2=lambda v:math.exp(-v*v/4)/math.sqrt(v)
    BC=lambda q,w: math.sinh(q)*math.sinh(w)*(1-.5*(math.cosh(q)-1)*(math.cosh(w)-1))
    tm=R*R*math.sinh(h*(k1(RN)-k1(R)))+2*b*R*math.sinh(h*(k2(RN)-k2(R)))
    sp=2*a*R*BC(h*k1(R),h*k2(R))+a*b*BC(h*k2(R),h*k2(R))
    return (tm+sp)/(h*h)

def solve_material_time_chain(L,n,site_xyz=(1,1,1)):
    cnt=original_counts(n,L)
    h=1/L
    idx=lambda t:((t*L+site_xyz[0])*L+site_xyz[1])*L+site_xyz[2]
    densities=np.array([L**4*cnt[idx(t)]/sum(cnt) for t in range(L)],dtype=float)
    ts=(np.arange(L)-L//2+1)*h
    r=np.array([radius(t) for t in ts])
    AA=np.sqrt(r)*np.exp(-r*r/4)
    g=1/AA**2
    amp=(2*kappa)**(-.5)
    perp=-(amp**2)*AA**2 # original second real CAR scalar: v_x=amp, g^xx=-AA**2
    fu=np.array([native_star_finite(t,h) for t in ts])
    tau=.05
    x=-tau*fu/densities
    u0=amp*AA**2
    boundary=float(h*np.sum(u0))
    def yy(i,ui):return tau*(g[i]*ui**2+perp[i])/densities[i]
    def J(i,ui):
        y=yy(i,ui)
        assert abs(x[i])<1/128 and abs(y)<1/128 and abs(tau*g[i]*ui**2/densities[i])<1/128
        return g[i]*ui*native_derivatives(x[i],y)[1]
    J0=np.array([J(i,u0[i]) for i in range(L)])
    rootmin,rootmax=.5*min(J0),1.5*max(J0)
    def ui_for_J(i,Jvalue):
        lo,hi=.35*u0[i],1.65*u0[i]
        assert J(i,lo)<Jvalue<J(i,hi), (i,Jvalue,J(i,lo),J(i,hi))
        return brentq(lambda v:J(i,v)-Jvalue,lo,hi,xtol=6e-16)
    def disp(Jvalue):return h*sum(ui_for_J(i,Jvalue) for i in range(L))
    while disp(rootmin)>boundary:rootmin*=.8
    while disp(rootmax)<boundary:rootmax*=1.25
    Jstar=brentq(lambda j:disp(j)-boundary,rootmin,rootmax,xtol=2e-18)
    ustar=np.array([ui_for_J(i,Jstar) for i in range(L)])
    Ji=np.array([J(i,ustar[i]) for i in range(L)])
    yynew=np.array([yy(i,ustar[i]) for i in range(L)])
    fluxerr=max(abs(Ji-Jstar))
    boundaryerr=abs(h*sum(ustar)-boundary)
    # Full TRUE native N1 functional variation by separately varying the
    # actual two point scalar field, not a fitted flux residual.
    def native_action(mid):
        psi=np.concatenate(([0.],np.array(mid),[boundary]))
        u=np.diff(psi)/h
        tot=0.
        for i in range(L):
            q=tau*(g[i]*u[i]**2+perp[i])/densities[i]
            if not (-1/128<q<1/128):raise ValueError('outside native chart')
            E=p*p*(1+x[i]);ell=4*E*(1-E)
            ub=p-p*p*q;bb=4*ub*ub*(1-ub*ub);aaa=ell+(1-ell)*bb
            prob=1-(1-z*bb)*(1-z*aaa)
            H=-(prob*math.log(prob)+(1-prob)*math.log1p(-prob))/lnphi
            rbaseline=1.8512395784882028e-6
            Hb=-(rbaseline*math.log(rbaseline)+(1-rbaseline)*math.log1p(-rbaseline))/lnphi
            tot+=densities[i]*(-mult)*(H-Hb)
        return tot
    psi=np.concatenate(([0.],np.cumsum(ustar*h)))
    graderr=0
    # Differentiation of this full complete CQ PRICE by high accuracy symmetric
    # finite-difference (diagnostic, while exact Euler identity follows above)
    dsteps=2e-5
    for k in range(1,L):
        mval=psi[1:-1].copy();mval[k-1]+=dsteps
        pval=native_action(mval);mval[k-1]-=2*dsteps
        nval=native_action(mval)
        graderr=max(graderr,abs((pval-nval)/(2*dsteps)))
    gradient_size=max(abs(J0[:-1]-J0[1:]))
    assert fluxerr<1e-11 and boundaryerr<5e-14
    assert graderr<2e-9
    assert max(abs(yynew))<1/128 and max(abs(x))<1/128
    corr=max(abs(ustar-u0))
    # Longitudinal Hessian on the exact root: Hzz=B^T diag(2 tau g *
    # [Fy+2 ypart Fyy]) B/h², SPD, since original interval control.
    stiff=[]
    for i in range(L):
        _,Fy,Fyy=native_derivatives(x[i],yynew[i]);part=tau*g[i]*ustar[i]**2/densities[i]
        stiff.append(2*tau*g[i]*(Fy+2*part*Fyy))
    H=np.zeros((L-1,L-1))
    for i in range(L):
        for a,coef in ((i,-1),(i+1,1)):
            if not 1<=a<=L-1:continue
            for b,coef2 in ((i,-1),(i+1,1)):
                if not 1<=b<=L-1:continue
                H[a-1,b-1]+=stiff[i]*coef*coef2/(h*h)
    eig=np.linalg.eigvalsh(H)
    assert min(eig)>0
    return dict(L=L,n=n,original_count_sum=int(cnt.sum()),true_density_counts=[int(cnt[idx(i)]) for i in range(L)],
                densities=[float(x) for x in densities],h=h,tau=tau,
                original_n1_f=[float(x) for x in fu],
                current_before=[float(x) for x in J0],
                current_after=float(Jstar),
                original_current_jump=float(gradient_size),
                final_current_error=float(fluxerr),final_scalar_Euler_from_whole_CQ=float(graderr),
                max_existing_scalar_gradient_change=float(corr),
                max_new_native_material_argument=float(max(abs(yynew))),
                fixed_boundary_error=float(boundaryerr),
                scalar_Hessian_min_eigenvalue=float(min(eig)),
                scalar_Hessian_max_eigenvalue=float(max(eig)),
                period_scalar1_values=psi.tolist())



def raw_native_F(x,y):
    """Existing sigma-minus GoldenMaster.F(x,y), not the sigma-plus gate."""
    u=p-p*p*y;E=p*p*(1+x);ell=4*E*(1-E)
    B=4*u*u*(1-u*u);A=ell+(1-ell)*B
    r=1-(1-z*B)*(1-z*A)
    rb=1.8512395784882028e-6
    entropy=lambda q:-(q*math.log(q)+(1-q)*math.log1p(-q))/lnphi
    return -mult*(entropy(r)-entropy(rb))

def raw_native_Fx(x,y):
    u=p-p*p*y;E=p*p*(1+x);ell=4*E*(1-E)
    B=4*u*u*(1-u*u);A=ell+(1-ell)*B
    r=1-(1-z*B)*(1-z*A)
    drdx=z*(1-z*B)*4*p*p*(1-2*E)*(1-B)
    return -mult*math.log((1-r)/r)/lnphi*drdx

def solve_two_real_scalar_slab(L,n,site_xyz=(1,1,1)):
    """All 2*(L-1) independent temporal material Euler rows, exact flux.

    The second real scalar has its actual x-spatial slope amp and a nonzero
    prescribed time-boundary difference, hence this is not a zero-copy slot.
    """
    cnt=original_counts(n,L);h=1/L
    idx=lambda t:((t*L+site_xyz[0])*L+site_xyz[1])*L+site_xyz[2]
    rho=np.array([L**4*cnt[idx(i)]/sum(cnt) for i in range(L)],float)
    ts=(np.arange(L)-L//2+1)*h
    r=np.array([radius(t) for t in ts])
    A=np.sqrt(r)*np.exp(-r*r/4)
    g=1/A**2
    amp=(2*kappa)**(-.5)
    # Actual second real CAR scalar has a fixed x-slope amp and g^xx=-A^2.
    fixed_spatial=-amp**2*A**2
    f=np.array([native_star_finite(t,h) for t in ts])
    tau=.05
    x=-tau*f/rho
    boundary=np.array([h*np.sum(amp*A**2),.006*L*h])
    direction=boundary/np.linalg.norm(boundary)
    def ypart(i,m):return tau*(g[i]*m*m+fixed_spatial[i])/rho[i]
    def jmag(i,m):
        y=ypart(i,m)
        assert abs(x[i])<1/128 and abs(y)<1/128 and abs(tau*g[i]*m*m/rho[i])<1/128,(i,x[i],y)
        return g[i]*m*native_derivatives(x[i],y)[1]
    reference=np.linalg.norm(np.column_stack([amp*A*A,np.full(L,.006)]),axis=1)
    vals=np.array([jmag(i,reference[i]) for i in range(L)])
    def mag_from_J(i,J):
        lo,hi=.30*reference[i],1.7*reference[i]
        assert jmag(i,lo)<J<jmag(i,hi),(i,J)
        return brentq(lambda m:jmag(i,m)-J,lo,hi,xtol=6e-16)
    def disp(J):return h*sum(mag_from_J(i,J) for i in range(L))
    a,b=.5*min(vals),1.5*max(vals)
    assert disp(a)<np.linalg.norm(boundary)<disp(b)
    flux=brentq(lambda j:disp(j)-np.linalg.norm(boundary),a,b,xtol=3e-18)
    mags=np.array([mag_from_J(i,flux) for i in range(L)])
    U=mags[:,None]*direction[None,:]
    Y=np.array([ypart(i,mags[i]) for i in range(L)])
    currents=np.array([g[i]*U[i]*native_derivatives(x[i],Y[i])[1] for i in range(L)])
    assert np.linalg.norm(h*np.sum(U,axis=0)-boundary,np.inf)<3e-14
    assert max(np.linalg.norm(v-flux*direction,np.inf) for v in currents)<2e-20
    psi=np.vstack((np.zeros(2),np.cumsum(U*h,axis=0)))
    psi[-1]=boundary
    def action(mid,shift=0):
        zz=np.vstack((np.zeros(2),np.asarray(mid).reshape(L-1,2),boundary))
        us=np.diff(zz,axis=0)/h
        total=0.
        df=np.array([1 if k%3==0 else (-.5 if k%3==1 else .25) for k in range(L)])
        for i in range(L):
            q=tau*(g[i]*(us[i]@us[i])+fixed_spatial[i])/rho[i]
            xx=x[i]-tau*shift*df[i]/rho[i]
            total+=rho[i]*raw_native_F(xx,q)
        return total
    mid=psi[1:-1].copy()
    dx=2e-5
    err=0.
    for k in range(L-1):
        for j in range(2):
            m1=mid.copy();m2=mid.copy()
            m1[k,j]+=dx;m2[k,j]-=dx
            err=max(err,abs((action(m1)-action(m2))/(2*dx)))
    assert err<1e-9,err
    dphi=[1 if k%3==0 else (-.5 if k%3==1 else .25) for k in range(L)]
    env=-tau*sum(raw_native_Fx(x[i],Y[i])*dphi[i] for i in range(L))
    # The true reduced derivative differentiates a SOURCE that has ALREADY
    # moved according to its nonlinear material Euler, not a frozen psi.
    def optimized_action_for_shift(shift):
        xx=x-tau*shift*np.array(dphi)/rho
        def j_at(i,m):
            y=ypart(i,m)
            return g[i]*m*native_derivatives(xx[i],y)[1]
        def mag_j(i,J):
            lo,hi=.3*reference[i],1.7*reference[i]
            return brentq(lambda m:j_at(i,m)-J,lo,hi,xtol=6e-16)
        def fun(J):return h*sum(mag_j(i,J) for i in range(L))-np.linalg.norm(boundary)
        Jnew=brentq(fun,.5*min(vals),1.5*max(vals),xtol=3e-18)
        mm=np.array([mag_j(i,Jnew) for i in range(L)])
        pp=np.vstack((np.zeros(2),np.cumsum(mm[:,None]*direction[None,:]*h,axis=0)))
        pp[-1]=boundary
        return action(pp[1:-1],shift)
    sh=2e-3
    source_secant=(optimized_action_for_shift(sh)-optimized_action_for_shift(-sh))/(2*sh)
    assert abs(source_secant-env)<5e-11,(env,source_secant)
    H=np.zeros((2*(L-1),2*(L-1)))
    for i in range(L):
        _,FY,FYY=native_derivatives(x[i],Y[i])
        Ylong=tau*g[i]*(mags[i]**2)/rho[i]
        local=2*tau*g[i]*(FY*np.eye(2)+2*Ylong*FYY*np.outer(direction,direction))
        for k,sgn in ((i,-1),(i+1,1)):
            if not 1<=k<=L-1:continue
            for j,sgn2 in ((i,-1),(i+1,1)):
                if not 1<=j<=L-1:continue
                H[2*(k-1):2*k,2*(j-1):2*j]+=sgn*sgn2*local/h**2
    eig=np.linalg.eigvalsh(H)
    assert eig[0]>0
    return dict(L=L,n=n,original_PF_site_counts=[int(cnt[idx(i)]) for i in range(L)],
      rho=[float(q) for q in rho],two_real_matter_flux=[float(v) for v in flux*direction],
      maximum_complete_CQ_temporal_material_Euler=float(err),
      boundary_difference=[float(v) for v in boundary],
      fixed_endpoint_error=float(np.linalg.norm(h*np.sum(U,axis=0)-boundary,np.inf)),
      full_2D_material_Hessian_min_eigenvalue=float(eig[0]),
      full_2D_material_Hessian_max_eigenvalue=float(eig[-1]),
      field_source_envelope=float(env),
      field_source_optimized_actual_secant=float(source_secant),
      field_source_envelope_error=float(abs(source_secant-env)),
      nonzero_scalar2_temporal_flux=bool(abs(currents[0,1])>1e-15),
      max_native_argument=float(max(abs(Y))))

def main():
    box=iv_positive_box()
    pf=[pf_depth_proof(L) for L in (4,8,16,32,64,128)]
    sims=[solve_material_time_chain(4,20),solve_material_time_chain(8,24)]
    sims2=[solve_two_real_scalar_slab(4,20),solve_two_real_scalar_slab(8,24)]
    print(json.dumps({'status':'PASS_EXACT_FORMULA_AND_SCOPED_NATIVE_DIAGNOSTIC',
     'Golden_F_y_interval_without_alpha_beta':box,
     'actual_Golden_PF_uniform_C2_refinement':pf,
     'original_nonlinear_N1_one_scalar_time_layer':[dict(x) for x in sims],
     'original_nonlinear_N1_TWO_REAL_scalar_time_layer':[dict(x) for x in sims2],
     'science_scope':{'two_real_scalar_temporal_Euler_exact_by_flux':True,
      'fixed_temporal_boundaries':True,'original_negative_Golden_orientation':True,
      'actual_L4_L8_native_F_R_counts':True,
      'nonflat_true_six_face_local_density':True,
      'two_real_scalar_spatial_Euler_automatic':False,
      'coframe16_link24_joint_stationarity':False,
      'full_Book03_absolute_Info_selected':False,
      'finite_all42_exact_root':False,'physical_GR_closed':False}},indent=2))
if __name__=='__main__':main()
