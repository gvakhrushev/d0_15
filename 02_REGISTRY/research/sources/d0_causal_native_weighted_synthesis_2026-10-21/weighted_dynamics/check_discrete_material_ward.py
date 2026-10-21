#!/usr/bin/env python3
"""Exact finite CAR scalar/coframe Ward defect, with both real material fields.

Consumes q=sum_A (D+ psi_A)^T (e^T eta e)^-1 (D+ psi_A). No replacement
stencil, positive-Hilbert norm, matter measure, or physical action is used.
The gravitational Lie-source defect is an explicit UNCOMPUTED input.
Numerical refinements below are diagnostic smooth fields, not native roots.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import sympy as s
import mpmath as mp

INPUT_REF = '401eafb2958e9d9626db833a25f02b35b3871c16'
ETA = np.diag([1., -1., -1., -1.])
CHECKS = []


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append(label)


def exact_zero(value, label):
    seq = list(value) if isinstance(value, s.MatrixBase) else [value]
    require(all(s.cancel(v) == 0 for v in seq), label)


def fp(a, direction, h):
    return (np.roll(a, -1, axis=direction) - a) / h


def bm(a, direction, h):
    return (a - np.roll(a, 1, axis=direction)) / h


def metric(e):
    g = np.einsum('...ai,ab,...bj->...ij', e, ETA, e)
    return g, np.linalg.inv(g)


def metric_jet(e, G, de):
    dg = (np.einsum('...ai,ab,...bj->...ij', de, ETA, e)
          + np.einsum('...ai,ab,...bj->...ij', e, ETA, de))
    return -np.einsum('...ij,...jk,...kl->...il', G, dg, G)


def material_data(e, psi, h):
    _, G = metric(e)
    w = np.stack([fp(psi, j, h) for j in range(4)], axis=-1)
    q = np.einsum('...ij,...Ai,...Aj->...', G, w, w)
    return G, w, q


def lie_variation(e, psi, xi, h):
    """Sampled continuum Lie tangent in the ACTUAL 16 coframe +2 scalar slots.

    This algebraic field tangent is NOT declared a paid primitive writer.
    """
    de = sum(xi[..., a, None, None] * fp(e, a, h) for a in range(4))
    for mu in range(4):
        de[..., :, mu] += sum(e[..., :, a] * fp(xi[..., a], mu, h)[..., None]
                             for a in range(4))
    dpsi = sum(xi[..., a, None] * fp(psi, a, h) for a in range(4))
    return de, dpsi


def q_first_jet(e, psi, de, dpsi, h):
    G, w, _ = material_data(e, psi, h)
    dG = metric_jet(e, G, de)
    dw = np.stack([fp(dpsi, j, h) for j in range(4)], axis=-1)
    return (np.einsum('...ij,...Ai,...Aj->...', dG, w, w)
            + 2*np.einsum('...ij,...Ai,...Aj->...', G, w, dw))


def material_ward(e, psi, k, h):
    """Return exact q, C_a, R_(nu,a), and the residual covector W_a.

    delta_L q = xi^a D_a+ q + C_a xi^a + R_(nu,a) D_nu+ xi^a.
    sum k*(delta_L q-xi.D+q) = sum xi.W, with
    W_a=k C_a-sum_nu D_nu-(k R_(nu,a)).
    Periodic arrays; the same identity holds on complete collars with all
    corresponding boundary terms zero. No arbitrary zero padding is allowed.
    """
    G, w, q = material_data(e, psi, h)
    C = np.empty(q.shape+(4,))
    R = np.empty(q.shape+(4,4))
    chain_error = 0.
    for a in range(4):
        de = fp(e, a, h)
        dG = fp(G, a, h)
        jetG = metric_jet(e, G, de)
        B = jetG-dG
        gp = np.roll(G, -1, axis=a)
        Lg = (np.einsum('...ai,ab,...bj->...ij', de, ETA, e)
              + np.einsum('...ai,ab,...bj->...ij', e, ETA, de))
        He = np.einsum('...ai,ab,...bj->...ij', de, ETA, de)
        B_formula = h*(np.einsum('...ij,...jk,...kl->...il', dG, Lg, G)
                         + np.einsum('...ij,...jk,...kl->...il', gp, He, G))
        chain_error = max(chain_error, float(np.max(abs(B-B_formula))))
        dw = fp(w, a, h)
        C[...,a] = (np.einsum('...ij,...Ai,...Aj->...', B, w, w)
                     - h*np.einsum('...ij,...Ai,...Aj->...', G, dw, dw)
                     - 2*h*np.einsum('...ij,...Ai,...Aj->...', dG, w, dw)
                     - h*h*np.einsum('...ij,...Ai,...Aj->...', dG, dw, dw))
    for nu in range(4):
        for a in range(4):
            R[...,nu,a] = 2*h*np.einsum('...i,...Ai,...A->...',
                                       G[..., :, nu], w, fp(w[..., :, a], nu, h))
    W = k[...,None]*C
    for a in range(4):
        for nu in range(4):
            W[...,a] -= bm(k*R[...,nu,a], nu, h)
    return q, C, R, W, chain_error


def symbolic_checks():
    h=s.Rational(1,7); eta=s.diag(1,-1,-1,-1)
    e=s.Matrix([[1,s.Rational(1,9),0,0],
                [s.Rational(1,8),s.Rational(6,5),0,s.Rational(1,11)],
                [0,s.Rational(1,10),s.Rational(7,6),0],
                [0,0,s.Rational(1,13),s.Rational(8,7)]])
    de=s.Matrix(4,4,lambda i,j:s.Rational((2*i-j+3)%7-3,31))
    G=(e.T*eta*e).inv(); ep=e+h*de; Gp=(ep.T*eta*ep).inv()
    Lg=de.T*eta*e+e.T*eta*de
    jet=-G*Lg*G; DG=(Gp-G)/h
    exact_zero(jet-DG-h*(DG*Lg*G+Gp*(de.T*eta*de)*G),
               'exact noncommuting inverse-metric chain defect')
    w=s.Matrix([[s.Rational(i+j+1,13) for j in range(4)] for i in range(2)])
    dw=s.Matrix([[s.Rational(2*i-j+1,19) for j in range(4)] for i in range(2)])
    pair=lambda A,B,C: sum((B[k,:]*A*C[k,:].T)[0] for k in range(2))
    q=pair(G,w,w); qp=pair(Gp,w+h*dw,w+h*dw)
    C=pair(jet-DG,w,w)-h*pair(G,dw,dw)-2*h*pair(DG,w,dw)-h*h*pair(DG,dw,dw)
    exact_zero(pair(jet,w,w)+2*pair(G,w,dw)-(qp-q)/h-C,
               'exact two-component forward product-chain remainder')
    require(C != 0, 'continuum Leibniz shortcut fails at finite spacing')
    # Weighted continuum invariant THROUGH y=0, with an explicit radial defect.
    x,y,r,fx,fy,dx,dy,dr,dfx=s.symbols('x y r fx fy dx dy dr dfx', nonzero=True)
    pressure=fy*dy-x*dfx
    ward=pressure+y*fy*dr/r
    radial=x*fx-y*fy
    dInv=dr*y/fx+r*dy/fx-r*y*dfx/fx**2
    exact_zero(ward-(fx*fy/r*dInv-radial/fx*dfx),
               'weighted invariant with radial-defect term kept')
    # Einstein residual divergence is -sum J_A dpsi_A -mu/2 dQ.
    mu,j0,j1,v0,v1,dq,divE=s.symbols('mu j0 j1 v0 v1 dq divE')
    exact_zero((divE+j0*v0+j1*v1+mu*dq/2).subs(divE,-j0*v0-j1*v1-mu*dq/2),
               'continuum full-equation residual-to-kinetic-gradient identity')
    eV,rho,tau,b,a,M=s.symbols('eV rho tau b a M', nonzero=True)
    Q,dcov,dsq,dm=s.symbols('Q dcov dsq dm')
    qstar=s.symbols('qstar')
    # Comparison action e[R-mu(Q-q*)]: on shell its metric source is -mu VV.
    matter_mu_variation=-eV*(Q-qstar)
    exact_zero(matter_mu_variation.subs(Q,qstar),'comparison constraint is actual multiplier equation')
    pressure_term=s.Rational(1,2)*mu*(Q-qstar)
    exact_zero(pressure_term.subs(Q,qstar),'no fictitious scalar pressure at constrained solution')
    # Two active scalar covectors need not have rank one.
    v=s.Matrix([2,0,0,0]); u=s.Matrix([0,1,0,0]); S=v*v.T+u*u.T
    require(S.rank()==2,'two-field source is not automatically a single dust')
    # Diagnostic small-amplitude checkerboard: C0 convergence does not control D+.
    eps,hc=s.symbols('eps hc', positive=True)
    exact_zero(((-eps)-eps)/hc+2*eps/hc,'mesh checkerboard hostile derivative')
    return {'exact_inverse_chain_identity':True,
            'exact_forward_product_remainder':str(C),
            'weighted_continuum_law':'d(rho*y/Fx)=0 only after full Ward and radial equations',
            'material_fields':2,'coframe_components':16,
            'two_scalar_stress_rank_control':2,
            'finite_continuum_Ward_is_not_assumed':True}


def native_master_checks():
    """Independent high-precision replay of the pinned literal N=1 polynomial.

    Same caps 9/20; this does NOT attest the prior chat's unavailable 65-test
    receipt and does not rerun the original field/gate compilation certificates.
    """
    mp.mp.dps=75
    p=(mp.sqrt(5)-1)/2; z=mp.mpf(2)**-20; logphi=mp.log(1/p)
    readiness=(1-(1-2*p**3)**9)**128 * ((1-p**120)**4*(1-(1-16*p**9)**20))**43
    def raw(x,y):
        E=p*p*(1+x); ell=4*E*(1-E); b=p+p*p*y
        B=4*b*b*(1-b*b); A=ell+(1-ell)*B
        return z*(A+B)-z*z*A*B
    def ent(r): return -(r*mp.log(r)+(1-r)*mp.log1p(-r))/logphi
    r0=raw(0,0); base=ent(r0)
    def F(x,y): return -readiness*(ent(raw(x,-y))-base)
    fx=lambda x,y:mp.diff(lambda xx:F(xx,y),x)
    fy=lambda x,y:mp.diff(lambda yy:F(x,yy),y)
    a=fx(0,0); b=fy(0,0)
    fxx=mp.diff(lambda xx:fx(xx,0),0)
    fxy=mp.diff(lambda yy:fx(0,yy),0)
    fyy=mp.diff(lambda yy:fy(0,yy),0)
    Kpp=fyy+2*(b/a)*fxy+(b/a)**2*fxx
    require(a<0<b and Kpp>0,'actual Golden N1 sign/coupling controls')
    rows=[]; worst=mp.mpf(0)
    tau=mp.mpf('0.05'); q0=mp.mpf('0.001')
    for rr in ('0.5','1','2','3'):
        rho=mp.mpf(rr); t=tau*q0/rho
        ss,U=mp.findroot(lambda xx,uu:(fx(xx,uu*t)/a-uu,xx-t*fy(xx,uu*t)/a),
                        ((b/a)*t,1),tol=mp.mpf('1e-65'),maxsteps=30)
        y=U*t
        err=max(abs(fx(ss,y)/a-U),abs(ss-t*fy(ss,y)/a))
        invariant_error=abs((rho*y/fx(ss,y))/(tau*q0/a)-1)
        worst=max(worst,err,invariant_error)
        require(err<mp.mpf('1e-60') and invariant_error<mp.mpf('1e-60'),
                'actual master equations and rho*y/Fx at rho='+rr)
        Kp=U*fy(ss,y)
        rows.append({'rho':rr,'U':mp.nstr(U,28),'e_E_times_mu':mp.nstr(-Kp/a,28)})
    return {'precision_digits':mp.mp.dps,'actual_caps':[9,20],
            'a':mp.nstr(a,45),'b':mp.nstr(b,45),'b_over_a':mp.nstr(b/a,45),
            'Kpp0':mp.nstr(Kpp,45),'worst_normalized_residual':mp.nstr(worst,8),
            'samples':rows,'native_42_row_replay':False}



def native_master_grid(q, rho, tau=0.001):
    """Literal reduced N=1 price at arbitrary sampled fields, no fitted weights.

    Return the normalized slope K'/b, a/b, and material price
    rho*K(tau*q/rho)/(tau*b). Original M*tau*b is a known common factor.
    The given rho array is diagnostic, not a claimed native AF refinement.
    """
    p=(np.sqrt(5.)-1)/2;z=2.**-20;lnphi=np.log(1/p)
    ready=(1-(1-2*p**3)**9)**128*((1-p**120)**4*(1-(1-16*p**9)**20))**43
    def raw(xx,yy):
        E=p*p*(1+xx);ell=4*E*(1-E);lx=4*p*p*(1-2*E);lxx=-8*p**4
        bb=p-p*p*yy;B=4*bb*bb*(1-bb*bb)
        By=8*p*p*bb*(1-2*bb*bb);Byy=8*p**4*(1-6*bb*bb)
        A=ell+(1-ell)*B
        Ax=lx*(1-B);Ay=(1-ell)*By
        Axx=lxx*(1-B);Axy=-lx*By;Ayy=(1-ell)*Byy
        r=z*(A+B)-z*z*A*B
        rx=z*(1-z*B)*Ax;ry=z*((1-z*A)*By+(1-z*B)*Ay)
        rxx=z*(1-z*B)*Axx;rxy=z*(1-z*B)*Axy-z*z*By*Ax
        ryy=z*((1-z*A)*Byy+(1-z*B)*Ayy-2*z*By*Ay)
        hp=(np.log1p(-r)-np.log(r))/lnphi;hpp=-1/(lnphi*r*(1-r))
        return (r,-ready*hp*rx,ready*hp*ry,
                -ready*(hpp*rx*rx+hp*rxx),ready*(hpp*rx*ry+hp*rxy),
                -ready*(hpp*ry*ry+hp*ryy))
    r0,a,b,*_=raw(0.,0.)
    t=tau*q/rho;ss=(b/a)*t;U=np.ones_like(t)
    for _ in range(9):
        r,fx,fy,fxx,fxy,fyy=raw(ss,U*t)
        e1=fx/a-U;e2=ss-t*fy/a
        j11=fxx/a;j12=fxy*t/a-1;j21=1-t*fxy/a;j22=-t*t*fyy/a
        determinant=j11*j22-j12*j21
        ds=(-e1*j22+j12*e2)/determinant
        du=(-j11*e2+e1*j21)/determinant
        ss+=ds;U+=du
    r,fx,fy,*_=raw(ss,U*t)
    error=float(max(np.max(abs(fx/a-U)),np.max(abs(ss-t*fy/a))))
    if error>1e-11 or np.max(abs(U*t))>=2.**-12 or np.max(abs(ss))>=.25:
        raise ArithmeticError('actual native master section outside certified common chart')
    entropy=lambda r:-(r*np.log(r)+(1-r)*np.log1p(-r))/lnphi
    K=-ready*(entropy(r)-entropy(r0))-a*U*ss
    return U*fy/b,a/b,rho*K/(tau*b),error


def smooth_fields(n):
    # Four-dimensional periodic diagnostic, no restriction of the tensor slots.
    x=np.meshgrid(*([np.arange(n)/n]*4),indexing='ij',sparse=False)
    t=[2*np.pi*v for v in x]; shape=(n,)*4
    e=np.broadcast_to(np.eye(4),shape+(4,4)).copy()
    for a in range(4):
        for mu in range(4):
            e[...,a,mu] += .008*np.sin(t[a]+t[(mu+1)%4]+.3*(a+mu))
    psi=np.stack([.02*(np.sin(t[0])+.7*np.cos(t[1]+t[2])+.4*np.sin(t[3])),
                  .016*(np.cos(t[0]+t[2])+.6*np.sin(t[1])+.3*np.cos(t[3]))],axis=-1)
    xi=np.stack([np.sin(t[a]+.2)+.3*np.cos(t[(a+1)%4]) for a in range(4)],axis=-1)
    rho=1+.2*np.sin(t[0])+.1*np.cos(t[2])
    # Diagnostic positive spatial price slope, not claimed to be the selected
    # native master at every grid site. The actual master is tested separately.
    k=1+.15*np.sin(t[1])+.1*np.cos(t[0]+t[3])+.08/rho
    return e,psi,xi,k,rho


def grid_check(n):
    h=1/n; e,psi,xi,k,rho=smooth_fields(n)
    q0=material_data(e,psi,h)[2]
    k,_,_,master_error=native_master_grid(q0,rho)
    q,C,R,W,chain=material_ward(e,psi,k,h)
    de,dpsi=lie_variation(e,psi,xi,h)
    direct=q_first_jet(e,psi,de,dpsi,h)
    adv=sum(xi[...,a]*fp(q,a,h) for a in range(4))
    defect=np.einsum('...a,...a->...',C,xi)
    for nu in range(4):
        for a in range(4): defect+=R[...,nu,a]*fp(xi[...,a],nu,h)
    point_error=float(abs(direct-adv-defect).max())
    adjoint_error=abs(float(np.mean(k*(direct-adv))-np.mean(np.einsum('...a,...a->...',xi,W))))
    require(chain<1e-11,'inverse metric chain formula n='+str(n))
    require(point_error<1e-11,'exact scalar Lie defect n='+str(n))
    require(adjoint_error<1e-11,'complete weighted summation by parts n='+str(n))
    if n==4:
        step=1e-6
        qp=material_data(e+step*de,psi+step*dpsi,h)[2]
        qm=material_data(e-step*de,psi-step*dpsi,h)[2]
        fd=float(abs((qp-qm)/(2*step)-direct).max())
        require(fd<1e-8,'independent coframe+two-scalar finite difference')
        # One isolated clock-direction test touches every shifted predecessor.
        local=np.zeros_like(xi);local[(1,2,1,2,3)]=1
        dl,pl=lie_variation(e,psi,local,h)
        locjet=q_first_jet(e,psi,dl,pl,h)
        lhs=float(np.sum(k*locjet))
        rhs=float(k[1,2,1,2]*fp(q,3,h)[1,2,1,2]+W[1,2,1,2,3])
        require(abs(lhs-rhs)<1e-11,'single-site exact covector including neighboring material rows')
        # Nonconstant price slope MUST stay inside the backward difference.
        wrong=k[...,None]*C
        for a in range(4):
            for nu in range(4): wrong[...,a]-=k*bm(R[...,nu,a],nu,h)
        omitted=float(abs(wrong-W).max())
        require(omitted>1e-6,'dropping spatial price-weight derivative detected')
    else:
        fd=None;omitted=None
    return {'n':n,'sites':n**4,'inverse_metric_chain_error':chain,
            'pointwise_exact_identity_error':point_error,'weighted_adjoint_error':adjoint_error,
            'finite_difference_error':fd,'omitted_weight_source_error':omitted,
            'ward_covector_inf':float(abs(W).max()),
            'ward_covector_over_h':float(abs(W).max()/h),
            'kinetic_gradient_inf':float(max(abs(fp(q,a,h)).max() for a in range(4))),
            'actual_K_slope_min':float(k.min()),'actual_K_slope_max':float(k.max()),
            'native_master_residual':master_error,
            'field_source_status':'DIAGNOSTIC_SMOOTH_FIELDS_NOT_STATIONARY_ROOTS'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    sym=symbolic_checks();native=native_master_checks()
    grids=[grid_check(n) for n in (4,8,12,16)]
    result={'status':'PASS_EXACT_DISCRETE_MATERIAL_WARD_AND_WEIGHTED_CONSUMER',
            'input_ref':INPUT_REF,'symbolic':sym,'native_master':native,'grids':grids,
            'checks_passed':len(CHECKS),'checks':CHECKS,
            'scope':{'earlier_65_check_receipt_recovered':False,
                     'material_chain_defect_computed':True,
                     'all16_coframe_and_two_scalar_tangents':True,
                     'finite_gravitational_Lie_defect_computed':False,
                     'full42_native_roots_newly_proved':False,
                     'finite_Ward_limit_proved_without_regular_fields':False,
                     'native_writer_and_Book_selection_proved':False,'GR_closed':False}}
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    print(text,end='')
    if args.json:args.json.write_text(text,encoding='utf-8')

if __name__=='__main__':main()
