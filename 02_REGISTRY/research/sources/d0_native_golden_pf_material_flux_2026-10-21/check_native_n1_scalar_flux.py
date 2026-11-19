#!/usr/bin/env python3
"""D0 exact N1 Golden-master material Euler on a finite temporal chain.
Actual original Golden n24/L8 site densities; actual original six-face
finite scalar (closed-form due to homogeneous rank2), no affine replacement.
Fixed endpoint scalar Dirichlet, solve via conserved nonlinear flux.
No 16+24 geometric root and no compulsory Book03 claim.
"""
import json, math, importlib.util
import numpy as np
from scipy.special import erfi
from scipy.optimize import brentq
from scipy.optimize._numdiff import approx_derivative
import mpmath as mp
mp.mp.dps=80
p=(mp.sqrt(5)-1)/2;z=mp.mpf(2)**-20;lnphi=mp.log(1/p)
# Exact same sigma-minus full-N1 Golden probability; static factor alpha*beta
# cancels from the MATERIAL Euler and does not get assumed free in the price.
def raw(x,y):
    E=p*p*(1+x);ell=4*E*(1-E)
    u=p-p*p*y;B=4*u*u*(1-u*u)
    A=ell+(1-ell)*B
    return 1-(1-z*B)*(1-z*A)
def native_y(x,y):
    E=p*p*(1+x);ell=4*E*(1-E)
    u=p-p*p*y;B=4*u*u*(1-u*u)
    by=-8*p*p*u*(1-2*u*u)
    A=ell+(1-ell)*B
    Q=1-z*B;R=1-z*A
    r=1-Q*R
    return -mp.log((1-r)/r)/lnphi * z*by*(R+Q*(1-ell))
# This is F_y / (alpha beta), since F_N=-alpha beta [h(r)-h(r0)];
# sign: -h'(r)r_y >0 because r_y<0.
assert native_y(mp.mpf(0),mp.mpf(0))>0
norm=native_y(mp.mpf(0),mp.mpf(0))

def ratio_native(x,y):return float(native_y(mp.mpf(str(x)),mp.mpf(str(y)))/norm)

def time_at_radius(r):
    return math.sqrt(math.pi/2)*(erfi(r/math.sqrt(2))-erfi(1/math.sqrt(2)))
def radius_at_time(t):
    return brentq(lambda r:time_at_radius(r)-t,.25,2.25,xtol=5e-15)
def coframe(r):
    A=math.sqrt(r)*math.exp(-r*r/4)
    B=math.exp(r*r/4)/math.sqrt(r)
    return A,B

def spin(r):return (0.5*(1-r**-2),math.exp(-r*r/4)/math.sqrt(r))
def BC(a,b):return math.sinh(a)*math.sinh(b)*(1-.5*(math.cosh(a)-1)*(math.cosh(b)-1))
def actual_star(t,h):
    r=radius_at_time(t); rn=radius_at_time(t+h)
    A,B=coframe(r)
    x,y=spin(r);xn,yn=spin(rn)
    temporal=r*r*math.sinh(h*(xn-x))+2*B*r*math.sinh(h*(yn-y))
    spatial=2*A*r*BC(h*x,h*y)+A*B*BC(h*y,h*y)
    return (temporal+spatial)/h**2

# Consume original 4D Golden nested box address-map count owner; DO NOT
# invent uniform site prior or independent stochastic PF data.
def native_counts(n,L):
    counts=[0]*(L**4)
    pv=(math.sqrt(5)-1)/2
    def rec(cost,depth,left,width):
        if cost==0:
            idx=0
            for i in range(4):
                idx=idx*L+min(L-1,max(0,int(L*(left[i]+width[i]/2))))
            counts[idx]+=1;return
        i=depth%4
        neww=list(width);neww[i]*=pv
        rec(cost-1,depth+1,left,neww)
        if cost>=2:
            ll=list(left);ww=list(width)
            ll[i]+=pv*ww[i];ww[i]*=pv*pv
            rec(cost-2,depth+1,ll,ww)
    rec(n,0,[0]*4,[1]*4)
    return counts

# Exact original finite h spatial finite N=1 scalar action and field source
# along one time chain with fixed geometry and scalar2's x-gradient.
def solve(L=8,n=24,sample=(4,4,4)):
    h=1/L;counts=native_counts(n,L)
    fib0,fib1=0,1
    for _ in range(n):fib0,fib1=fib1,fib0+fib1
    assert fib1==sum(counts)
    rho=[]
    for i in range(L):
        idx=((i*L+sample[0])*L+sample[1])*L+sample[2]
        rho.append(L**4*counts[idx]/fib1)
    times=[(i-(L-1)/2)*h for i in range(L)]
    r=[radius_at_time(t) for t in times]
    AB=[coframe(rr) for rr in r]
    a=[1/AA**2 for AA,BB in AB]
    gx=[-1/BB**2 for AA,BB in AB]
    fs=[actual_star(t,h) for t in times]
    tau=.05
    eps=math.sqrt(1/(2*23.41640675188407497289558))
    u0=[eps*AA**2 for AA,BB in AB]
    current0=[a[i]*u0[i] for i in range(L)]
    assert max(abs(v-eps) for v in current0)<2e-16
    q0=[a[i]*u0[i]**2+gx[i]*eps**2 for i in range(L)]
    assert max(abs(v) for v in q0)<2e-17

    def factor(i,u):
        qq=a[i]*u*u+gx[i]*eps*eps
        return ratio_native(-tau*fs[i]/rho[i],tau*qq/rho[i])
    def g(i,u):return factor(i,u)*a[i]*u
    def local_root(i,J):
        # Same N1 functional derivative; implicit nonlinear true scalar2 stress.
        # Nearby monotonic branch, no fitted matter source.
        lo=u0[i]*.45;hi=u0[i]*1.8
        assert g(i,lo)<J<g(i,hi),(i,J,g(i,lo),g(i,hi))
        return brentq(lambda u:g(i,u)-J,lo,hi,xtol=2e-15)
    totalOld=sum(u0)*h
    def roots(J):return [local_root(i,J) for i in range(L)]
    J=brentq(lambda J:h*sum(roots(J))-totalOld,eps*.6,eps*1.4,xtol=3e-15)
    us=roots(J)
    flux=[g(i,us[i]) for i in range(L)]
    q=[a[i]*us[i]**2+gx[i]*eps**2 for i in range(L)]
    # The original scalar1 Euler is the difference of two actual neighboring
    # native fluxes; material field values are reconstructed from these u_i.
    grad_before=[(g(i-1,u0[i-1])-g(i,u0[i]))/h for i in range(1,L)]
    grad_after=[(flux[i-1]-flux[i])/h for i in range(1,L)]
    assert abs(h*sum(us)-totalOld)<3e-13
    assert max(map(abs,grad_after))<1e-10
    assert max(map(abs,grad_before))>1e-5
    assert max(abs((us[i]-u0[i])) for i in range(L))<.05
    # Independent finite-difference variation of the ACTUAL nonlinear CQ F_N:
    # numerical analytic r, entropy; alpha beta is an external common positive
    # factor and does not alter the field Euler roots.
    def price_value(psi):
        vals=[(psi[i+1]-psi[i])/h for i in range(L)]
        total=mp.mpf('0')
        for i in range(L):
            qq=a[i]*vals[i]**2+gx[i]*eps**2
            rr=raw(-tau*fs[i]/rho[i],tau*qq/rho[i])
            H=-(rr*mp.log(rr)+(1-rr)*mp.log(1-rr))/lnphi
            total+=mp.mpf(str(rho[i]))*(-H)
        return total
    p0=[0.]
    for v in us:p0.append(p0[-1]+h*v)
    vars=np.array(p0,dtype=float)
    dx=1e-5
    finite=[]
    for j in range(1,L):
        pplus=vars.copy();pminus=vars.copy();pplus[j]+=dx;pminus[j]-=dx
        numerical=float((price_value(pplus)-price_value(pminus))/(2*dx))
        finite.append(numerical)
    # Norm: full original continuous price multiplies tau alpha beta, and
    # derivative of price for q includes F_y. Check with real multiplier.
    assert max(map(abs,finite))<1e-7,(max(map(abs,finite)),finite)
    return dict(L=L,n=n,site=sample,actual_rho=[round(v,9) for v in rho],
                actual_f=[round(v,8) for v in fs],flux_J=J,
                max_baseline_material_row=max(map(abs,grad_before)),
                max_solved_material_row=max(map(abs,grad_after)),
                max_true_full_CQ_price_secant=max(map(abs,finite)),
                max_abs_material_gradient_correction=max(abs(us[i]-u0[i]) for i in range(L)),
                max_resulting_true_material_q=max(map(abs,q)),
                fixed_dirichlet_boundary_diff=abs(h*sum(us)-totalOld),
                upstream_geometry_link_rows_solved=False,second_material_row_2D_solved=False,
                native_Book03_selected=False,GR_closed=False)

if __name__=='__main__':
    print(json.dumps(solve(),indent=2))
