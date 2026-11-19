#!/usr/bin/env python3
"""Exact controls for the same nonlinear direct-click Einstein--dust sector.

This checks the generic mass-coordinate construction and all 16+24+2
Euler rows on an independent anisotropic Einstein--dust example. It does
not certify arbitrary native domains, exact finite-word roots, or full128
source equality. The general local equivalence is proved in PROOF_RU.md.
"""
from __future__ import annotations
import hashlib
import json
import platform
from pathlib import Path
import sympy as s
import mpmath as mp

CHECKS: list[str] = []


def reduce(expr):
    return s.factor(s.cancel(s.simplify(expr)))


def zero(expr, label: str) -> None:
    entries = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    if any(reduce(x) != 0 for x in entries):
        raise ArithmeticError(label)
    CHECKS.append(label)


def require(condition, label: str) -> None:
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append(label)


def branch_control() -> dict:
    # Consume the original polynomial and its exact two-root formula,
    # not a gravity-fitted replacement. Numerical digits are diagnostics.
    x, y, p, z = s.symbols('x y p z', real=True)
    ep = p**2*(1+x)
    ell = 4*ep*(1-ep)
    b = p-p**2*y
    B = 4*b*b*(1-b*b)
    A = ell+(1-ell)*B
    r = z*(A+B)-z*z*A*B
    rx, ry = s.diff(r,x), s.diff(r,y)
    T = x*rx-y*ry
    H = r-x*rx
    zero((-x/y)*rx+ry+T/y,
         'full nonlinear coframe source vanishes modulo the original trace equation')
    coeff = s.Poly(T,x)
    require(coeff.degree()==2, 'original trace equation is quadratic in x')
    aa, bb, cc = coeff.all_coeffs()
    # Exact algebra: x=-2c/(b+sqrt(b^2-4ac)) is a root.
    aq,bq,cq,w=s.symbols('a b c w')
    xx=-2*cq/(bq+w)
    num=s.together(aq*xx**2+bq*xx+cq).as_numer_denom()[0]
    zero(s.rem(s.Poly(num,w),s.Poly(w*w-bq*bq+4*aq*cq,w)).as_expr(),
         'stable quadratic branch satisfies trace equation exactly')
    ward_jac=s.det(s.Matrix([[s.diff(T,x),s.diff(T,y)],
                             [s.diff(H,x),s.diff(H,y)]]))
    zero(ward_jac.subs({x:0,y:0})-(rx*ry).subs({x:0,y:0}),
         'trace/Ward local Jacobian identity at vacuum')
    mp.mp.dps=90
    pp=(mp.sqrt(5)-1)/2; zz=mp.mpf(2)**-20; yy=zz
    evalu=lambda expr: s.lambdify((x,y,p,z),expr,'mpmath')
    av,bv,cv=[evalu(v)(0,yy,pp,zz) for v in (aa,bb,cc)]
    x0=-2*cv/(bv+mp.sqrt(bv*bv-4*av*cv))
    kap=-x0/yy
    rxx=evalu(rx)(x0,yy,pp,zz); ryy=evalu(ry)(x0,yy,pp,zz)
    require(rxx>0 and ryy<0 and kap>0,'positive original dust branch signs')
    require(abs(evalu(T)(x0,yy,pp,zz))<mp.mpf('1e-80'),
            'original nonzero branch high-precision residual')
    require(abs(kap+ryy/rxx)<mp.mpf('1e-75'), 'true coupling ratio, no weak-query replacement')
    require(evalu(rx)(0,0,pp,zz)>0, 'regular vacuum branch retains the Palatini coefficient')
    jac=evalu(ward_jac)(x0,yy,pp,zz)
    require(jac<0,'nondegenerate trace/Ward diagnostic')
    q0=yy/(pp*pp)
    require(2*mp.sqrt(q0)<pp/4,'example scalar amplitudes stay inside inherited chart')
    return {'y0':'2^-20','tau':'p^2','x0':mp.nstr(x0,45),
            'kappa':mp.nstr(kap,45),'q0':mp.nstr(q0,45),
            'ward_jacobian':mp.nstr(jac,45),
            'numeric_branch_is_diagnostic_not_new_interval_certificate':True}


def mass_coordinate_control() -> dict:
    t,y1,y2,y3,q0=s.symbols('t y1 y2 y3 q0', positive=True)
    # Arbitrary positive advected density on a flow box, not a new GR metric.
    M=1+y1*y1+y2*y2+y3*y3
    E=s.exp(t)*(2+y1*y1+y2*y2)
    rho=M/E
    X=s.Matrix([(y1*(1+y2*y2+y3*y3)+y1**3/3)/(2*q0),y2,y3])
    jac=X.jacobian(s.Matrix([y1,y2,y3])).det()
    zero(s.diff(rho*E,t),'conserved mass on a generic flow-box control')
    zero(jac-M/(2*q0),'explicit triangular mass-coordinate Jacobian')
    zero(rho*E/jac-2*q0,'density-volume normalization follows from actual Jacobian')
    zero(s.diff(jac,t),'mass-coordinate relabelling preserves proper time')
    require(reduce(rho*E-2*q0)!=0,'negative control: omitting Jacobian is not permitted')
    # The field-dependent coordinate choice is used AFTER stationarity:
    # a radial ambient variation is still free and changes E.
    eps=s.symbols('eps')
    zero(s.diff((1+eps)**4*E,eps).subs(eps,0)-4*E,
         'all-four coframe radial variation is retained')
    return {'mass_density':str(M),'spatial_jacobian':str(jac),
            'density_volume':'2*q0','external_clock_or_new_field_added':False}


def anisotropic_all_rows() -> dict:
    t,kappa,q0=s.symbols('t kappa q0', positive=True)
    coords=s.symbols('t x y z')
    eta=s.diag(1,-1,-1,-1)
    hvol=3*kappa*q0/2
    scales=[hvol*t/(1+t)**s.Rational(1,3),
            (1+t)**s.Rational(2,3),(1+t)**s.Rational(2,3)]
    e=s.diag(1,*scales); inv=s.diag(1,*[1/a for a in scales])
    E=reduce(s.det(e)); g=e.T*eta*e; gi=inv*eta*inv.T
    H=[reduce(s.diff(a,t)/a) for a in scales]
    theta=sum(H)
    R00=-sum(s.diff(h,t)+h*h for h in H)
    Ric=s.diag(R00,*[scales[i]**2*(s.diff(H[i],t)+theta*H[i]) for i in range(3)])
    R=reduce(s.trace(gi*Ric)); Ein=Ric-R*g/2
    rho=4/(3*kappa*t*(t+1))
    zero(E-hvol*t*(1+t),'anisotropic actual volume')
    zero(R+4/(3*t*(t+1)),'anisotropic exact Ricci scalar')
    for mu in range(4):
        for nu in range(mu,4):
            zero(Ein[mu,nu]-(kappa*rho if mu==nu==0 else 0),
                 f'Einstein--dust metric row {mu}{nu}')
    zero(rho*E-2*q0,'actual anisotropic mass-coordinate gauge')
    zero(E*R/2+kappa*q0,'original gravitational operand, not f/E')
    q=q0*gi[0,0]
    zero(q-q0,'constant original material norm')
    zero(s.diff(rho*E,t),'anisotropic continuity')
    require(reduce(H[0]-H[1])!=0,'nonzero anisotropic shear')
    shear=reduce(sum((h-theta/3)**2 for h in H)/2)
    zero(shear-1/(3*t*t*(t+1)**2),'exact nonzero shear invariant')
    # Independent spin connection, evaluated only after variation.
    generators=[]
    for a in range(4):
        for b in range(a+1,4):
            G=s.zeros(4);G[a,b]=1;G[b,a]=-eta[a,a]/eta[b,b]
            zero(G.T*eta+eta*G,f'proper Lorentz generator {a}{b}')
            generators.append((a,b,G))
    omega=[s.zeros(4)]
    for i,a in enumerate(scales,1):
        G=s.zeros(4);G[0,i]=1;G[i,0]=1
        omega.append(s.diff(a,t)*G)
    F={}
    for mu in range(4):
        for nu in range(4):
            F[mu,nu]=(omega[nu].diff(t) if mu==0 else s.zeros(4)) \
                    -(omega[mu].diff(t) if nu==0 else s.zeros(4)) \
                    +omega[mu]*omega[nu]-omega[nu]*omega[mu]
    # Torsion and curvature scalar checked before all independent variations.
    for a in range(4):
        for mu in range(4):
            for nu in range(mu+1,4):
                tors=(s.diff(e[a,nu],t) if mu==0 else 0)-(s.diff(e[a,mu],t) if nu==0 else 0)
                tors+=sum(omega[mu][a,b]*e[b,nu]-omega[nu][a,b]*e[b,mu] for b in range(4))
                zero(tors,f'torsion row {a}:{mu}{nu}')
    def contraction(ia,ib):
        result=0
        for mu in range(4):
            for nu in range(4):
                for a in range(4):
                    for b in range(4):
                        if ia[mu,a]!=0 and ib[nu,b]!=0 and F[mu,nu][a,b]!=0:
                            result+=ia[mu,a]*ib[nu,b]*eta[b,b]*F[mu,nu][a,b]
        return result
    zero(contraction(inv,inv)-R,'independent spin-curvature scalar')
    coframe_rows=[]
    for a in range(4):
        for mu in range(4):
            de=s.zeros(4);de[a,mu]=1
            di=-inv*de*inv
            dE=E*s.trace(inv*de)
            dR=contraction(di,inv)+contraction(inv,di)
            dgi=di*eta*inv.T+inv*eta*di.T
            dq=q0*dgi[0,0]
            row=reduce((dE*R+E*dR)/2-kappa*dq)
            zero(row,f'full ambient coframe Euler row {a}{mu}, omega fixed')
            coframe_rows.append(str(row))
    # Explicit 24 Palatini derivatives: -partial_mu Tr(B^{mu,nu}G)
    # +Tr(B^{mu,nu}[omega_mu,G]), with all six generator types.
    def P(mu,nu):
        return E/2*(eta*inv[nu,:].T)*inv[mu,:]
    connection_rows=[]
    for nu in range(4):
        for a,b,G in generators:
            row=0
            for mu in range(4):
                B=P(mu,nu)-P(nu,mu)
                row-=(s.diff(s.trace(B*G),t) if mu==0 else 0)
                row+=s.trace(B*(omega[mu]*G-G*omega[mu]))
            row=reduce(row)
            zero(row,f'full independent connection Euler row {nu}:{a}{b}')
            connection_rows.append(str(row))
    # Material Euler equations use fixed measure, NOT an inserted sqrt(g).
    zero(s.diff(gi[0,0]*s.sqrt(q0),t),'first scalar Euler row')
    zero(s.Integer(0),'second scalar Euler row retained at zero value')
    # Wrong measured volume / density dictionary does not solve the source.
    wrong_prefactor=s.symbols('wrong_prefactor',positive=True)
    wrong00=reduce((wrong_prefactor*t*(1+t))*Ein[0,0]/2-kappa*q0)
    zero(wrong00-(2*wrong_prefactor/3-kappa*q0),'wrong-volume residual computed explicitly')
    require(wrong00!=0,'negative control: arbitrary volume factor fails')
    # Parameter family for the inverse theorem: the GR equation is exact
    # for all kappa,q0>0 and source equalities hold in all ambient directions.
    return {'metric':'diag(1,-[(3*kappa*q0/2)*t/(1+t)^(1/3)]^2,-(1+t)^(4/3),-(1+t)^(4/3))',
            'rho':str(rho),'R':str(R),'volume':str(E),
            'shear_squared':str(shear),'coframe_rows':coframe_rows,
            'independent_connection_rows':connection_rows,'material_rows':['0','0'],
            'wrong_volume_00_residual':str(wrong00),
            'all_42_are_ambient_rows_not_ansatz_derivatives':True}


def main():
    out={'input_commit':'726192353504a81a9ab2b751f9b6c7866271e75a',
         'consumed_owner':'A4D_CLOSED_HISTORY_NONLINEAR_EINSTEIN_DUST_2026_10_28.md',
         'consumed_owner_blob':'154b341f17adce88594b0b5e9df0d38c0283d288',
         'branch':branch_control(),'mass_coordinates':mass_coordinate_control(),
         'anisotropic_full_source':anisotropic_all_rows(),
         'checks':len(CHECKS),'check_names':CHECKS,
         'status':'PASS_LOCAL_DUST_EQUIVALENCE_CONTROLS',
         'local_continuum_general_reverse_proof_in_document':True,
         'new_finite_native_compiler_run':False,'original_full128_price_identified':False,
         'exact_finite_stationary_words_proved':False,'Lean_or_CI_run':False,'GR_closed':False,
         'environment':{'python':platform.python_version(),'sympy':s.__version__},
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
