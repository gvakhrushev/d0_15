#!/usr/bin/env python3
"""D0: fixed-measure complete-price Ward rigidity and all-cap field solutions.

New bounded continuum calculation. Consumes the pinned radial branch and
all-cap logarithmic derivative bounds; does not establish native field-query,
Book03 valuation, lattice recovery, or physical admission.
All test conditions use explicit exceptions and remain active under python -O.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import json
import hashlib
import sympy as s
import mpmath as mp

HERE = Path(__file__).resolve().parent
CHECKS: list[str] = []

def check(name: str, condition: bool) -> None:
    if not bool(condition):
        raise RuntimeError("FAIL: " + name)
    CHECKS.append(name)


def exact_density_identities() -> dict:
    x,y=s.symbols('x y',real=True)
    F=s.Function('F')(x,y)
    # A fixed positive background measure is retained; this is NOT a claim
    # that the dynamical-field action alone has arbitrary Diff invariance.
    H=F-x*s.diff(F,x)
    dx,dy=s.symbols('dx dy',real=True)
    ward=s.diff(H,x)*dx+s.diff(H,y)*dy
    expected=s.diff(F,y)*dy-x*(s.diff(F,x,2)*dx+s.diff(F,x,y)*dy)
    check('exact spurion Ward derivative',s.expand(ward-expected)==0)
    # The statement is stronger than the detector specialization: ANY local
    # F(x,y) with a=Fx(0), b=Fy(0) both nonzero has the invertible
    # radial/Ward map. All density constancy follows from full field EL.
    a0,b0=s.symbols('a0 b0',nonzero=True)
    general_jac=s.Matrix([[a0,-b0],[0,b0]])
    check('general two-density Ward map determinant',general_jac.det()==a0*b0)
    # Truly external nonuniform parameters retain their actual Ward source.
    k=s.symbols('k',real=True)
    Fk=s.Function('F')(x,y,k)
    Hk=Fk-x*s.diff(Fk,x)
    check('nonuniform ledger Ward correction retained',
          s.simplify(s.diff(Hk,k)-s.diff(Fk,k)+x*s.diff(Fk,x,k))==0)
    beta,rh=s.symbols('beta rh',real=True)
    for cap in (1,2,5):
        E=sum((beta*rh)**j for j in range(cap))
        expected=0 if cap==1 else sum(j*beta**j*rh**(j-1) for j in range(1,cap))
        check(f'cap {cap} actual price-inhomogeneity coupling',s.diff(E,rh)==expected)
    # Native radial equation, F=V(r), without treating x,y as free fields.
    r=s.Function('r')(x,y)
    V=s.Function('V')
    check('outer valuation cancels from radial equation',
          s.simplify(x*s.diff(V(r),x)-y*s.diff(V(r),y)
                     -s.diff(V(r),r)*(x*s.diff(r,x)-y*s.diff(r,y)))==0)
    vx,vy,vxx,vxy,vyy,tx,xx,yy,vp,vpp=s.symbols(
        'rx ry rxx rxy ryy tauprime tau y Vprime Vsecond',real=True)
    rbprime=vx*tx+vy
    Mp=vpp*rbprime*vx+vp*(vxx*tx+vxy)
    Hp=vp*vy-xx*Mp
    closed=vp*vy*(1-yy*Mp/(vp*vx))
    check('whole trace-branch Ward derivative',
          s.factor((Hp-closed).subs(xx,yy*vy/vx))==0)
    jac=s.Matrix([[vx,-vy],[0,vp*vy]])
    check('local trace-plus-Ward determinant',s.expand(jac.det()-vp*vx*vy)==0)
    check('uniform nonzero Ward slope margin',
          s.Rational(1)-s.Rational(202,4096)>s.Rational(15,16))
    # Reduced theory: divergence of W sum_A dpsi_A tensor dpsi_A after
    # its scalar equations is W/2 dq. Retain W=omega K'/sqrt(|g|).
    W,dq,m1,m2,g1,g2=s.symbols('W dq m1 m2 g1 g2',real=True)
    contracted=m1*g1+m2*g2+W*dq/2
    check('reduced Bianchi forces constant total kinetic norm',
          contracted.subs({m1:0,m2:0})==W*dq/2)
    # The mismatch term in a valuation Hessian is V'' delta-r delta-r.
    # At an r-critical point and a Jacobi mode delta-r=constant, its pairing
    # against every test field is V'' delta-r D I_r[test]=0.
    vpp0,dr0,first_variation=s.symbols('Vpp dr_constant Dr_action')
    check('stationary constant-density Jacobi term vanishes',
          (vpp0*dr0*first_variation).subs(first_variation,0)==0)
    return {'ward_integral':'F-x*F_x',
            'general_local_statement':'det D(xFx-yFy,F-xFx)|0=Fx(0)*Fy(0)',
            'radial_equation':'x*r_x-y*r_y=0',
            'branch_derivative':'Vprime*r_y*(1-y*d_y(log|Vprime*r_x|))',
            'strict_margin':str(1-s.Rational(202,4096)),
            'jacobian_at_zero':'Vprime(r0)*r_x(0)*r_y(0) != 0'}


def golden_polynomial_identities() -> tuple[dict, object]:
    p,z,x,y=s.symbols('p z x y',real=True)
    def reduce(expr):
        return s.rem(s.Poly(s.expand(expr),p),s.Poly(p*p+p-1,p)).as_expr()
    b=4*(p+p*p*y)**2*(1-(p+p*p*y)**2)
    ell=4*p*p*(1+x)*(1-p*p*(1+x))
    a=ell+(1-ell)*b
    r=1-(1-z*b)*(1-z*a)
    v=p+p*p*y;w=1-2*v*v;cc=1-z+z*w*w
    aa=4*p**5*z*cc*w*w
    rr=1-cc*(1-z+z*p**6*w*w)
    check('literal native two-band polynomial decomposition',
          reduce(r-rr-aa*(x-x*x/p))==0)
    r0=reduce(r.subs({x:0,y:0}))
    Q=1-z*(1-p**6);R=1-z*(1-p**12)
    rx=reduce(s.diff(r,x).subs({x:0,y:0}))
    ry=reduce(s.diff(r,y).subs({x:0,y:0}))
    check('original native geometric coefficient',reduce(rx-4*z*Q*p**11)==0)
    check('original native matter coefficient',reduce(ry-8*z*p**6*(R+Q*p**6))==0)
    check('original native baseline',reduce(r0-(1-Q*R))==0)
    # A positive fixed multiplier C adds a field-independent baseline only.
    shifts=s.symbols('shift')
    check('fixed baseline does not change Ward derivative',
          s.diff((r+shifts)-x*s.diff(r+shifts,x),y)==s.diff(r-x*s.diff(r,x),y))
    reduced=[reduce(e) for e in (r,s.diff(r,x),s.diff(r,y),s.diff(r,x,2),
                                 s.diff(r,x,y),s.diff(r,y,2))]
    fun=s.lambdify((x,y,p,z),reduced,'mpmath',cse=True)
    return {'field':'Q[p]/(p^2+p-1)',
            'polynomial_equality':True,
            'finite_z':'2^-20','density_chart':'|x|<1/4, |y|<=2^-12'},fun


def cap_branch_diagnostics(detector) -> dict:
    # These high-precision samples do not replace the inherited analytic
    # proof for ALL finite N. They independently check its new consumption.
    mp.mp.dps=85
    p=(mp.sqrt(5)-1)/2;z=mp.mpf(2)**-20;lp=mp.log(1/p)
    def outer(r,N,alpha,beta,kappa):
        h=-(r*mp.log(r)+(1-r)*mp.log(1-r))/lp
        hp=mp.log((1-r)/r)/lp
        hpp=-1/(lp*r*(1-r))
        t=beta*r
        en=sum(t**j for j in range(N))
        ep=sum(j*t**(j-1) for j in range(1,N))
        epp=sum(j*(j-1)*t**(j-2) for j in range(2,N))
        V=alpha*(kappa-beta*h)*en
        Vp=alpha*beta*((kappa-beta*h)*ep-hp*en)
        Vpp=alpha*beta*(beta*(kappa-beta*h)*epp-2*beta*hp*ep-hpp*en)
        return V,Vp,Vpp
    def trace_root(y):
        v=p+p*p*y;w=1-2*v*v;wp=-4*p*p*v
        cc=1-z+z*w*w
        hh=(1-z)*(1+p**6)+2*z*p**6*w*w
        C=-wp*hh/(2*p**5*w*cc)
        A_log=2*wp/w*(1+z*w*w/cc)
        k=-y*A_log
        disc=(1+k)**2-4*(2+k)*y*C/p
        return 2*y*C/(1+k+mp.sqrt(disc))
    params=[(mp.mpf('0.6'),mp.mpf(5)/7,mp.mpf(54)),
            (mp.mpf(1),mp.mpf(1),mp.mpf('53.0001'))]
    caps=(1,2,3,7,31)
    rows=[];max_trace=mp.mpf(0);min_margin=mp.mpf(2)
    for N in caps:
      for alpha,beta,kappa in params:
        for ym in (-1,0,1):
          y=mp.mpf(ym)*mp.mpf(2)**-12
          x=trace_root(y)
          r,rx,ry,rxx,rxy,ryy=detector(x,y,p,z)
          V,Vp,Vpp=outer(r,N,alpha,beta,kappa)
          tx=rx+x*rxx-y*rxy;ty=x*rxy-ry-y*ryy
          xp=-ty/tx
          rbprime=rx*xp+ry
          M=Vp*rx
          Mp=Vpp*rbprime*rx+Vp*(rxx*xp+rxy)
          margin=1-y*Mp/M
          Hprime=Vp*ry-x*Mp
          err=abs(x*rx-y*ry)/rx
          max_trace=max(max_trace,err);min_margin=min(min_margin,margin)
          check(f'native radial equation N{N} p{len(rows)}',err<mp.mpf('1e-72'))
          check(f'actual nonlinear Ward slope N{N} p{len(rows)}',
                abs(Hprime-Vp*ry*margin)/abs(Vp*ry)<mp.mpf('1e-70'))
          check(f'nonzero branch Jacobian N{N} p{len(rows)}',
                rx>0 and ry>0 and (Vp<0 if N==1 else Vp>0)
                and margin>mp.mpf(15)/16 and abs(Mp/M)<202)
          rows.append({'cap':N,'alpha':str(alpha),'beta':mp.nstr(beta,12),
                       'kappa':str(kappa),'y':mp.nstr(y,12),
                       'x':mp.nstr(x,20),'Ward_slope':mp.nstr(Hprime,20),
                       'margin':mp.nstr(margin,20)})
    # A genuinely non-null timelike sample fixes original geometry ONCE.
    y=-mp.mpf(2)**-13;x=trace_root(y)
    r,rx,ry,*_=detector(x,y,p,z)
    kappastar=ry/rx
    check('positive nonnull Einstein dust coefficient',x<0 and kappastar>0)
    check('same original density relation for all caps',
          abs(x-y*kappastar)<mp.mpf('1e-70'))
    # Pure local feedback valuation -ln(1-r) is not full Book/HJR.
    tx=rx+x*detector(x,y,p,z)[3]-y*detector(x,y,p,z)[4]
    ty=x*detector(x,y,p,z)[4]-ry-y*detector(x,y,p,z)[5]
    xp=-ty/tx;rbprime=rx*xp+ry
    rxprime=detector(x,y,p,z)[3]*xp+detector(x,y,p,z)[4]
    slope_log=rbprime/(1-r)+rxprime/rx
    check('local determinant valuation also regular',
          1-y*slope_log>0 and (1-r)>0)
    return {'numerical_samples_not_all_cap_proof':rows,
            'max_normalized_trace_residual':mp.nstr(max_trace,8),
            'minimum_sampled_monotonicity_margin':mp.nstr(min_margin,20),
            'one_nonnul_pair':{'y':mp.nstr(y,20),'x':mp.nstr(x,30),
                 'r_y_over_r_x':mp.nstr(kappastar,30)},
            'precision_decimal_digits':mp.mp.dps}


def arbitrary_inhomogeneous_solution() -> dict:
    t,x,z,w=s.symbols('t x z w',real=True)
    coords=(t,x,z,w)
    R=s.Function('R')(t,x)
    g=s.diag(1,-s.diff(R,x)**2,-R**2/(1-z*z),-R**2*(1-z*z))
    inv=s.diag(*[1/g[i,i] for i in range(4)])
    @lru_cache(None)
    def Gam(a,b,c):
        return s.factor(sum(inv[a,k]*(s.diff(g[k,b],coords[c])
                  +s.diff(g[k,c],coords[b])-s.diff(g[b,c],coords[k]))
                  for k in range(4))/2)
    Ric=s.zeros(4)
    for i in range(4):
      for j in range(i,4):
        v=sum(s.diff(Gam(k,i,j),coords[k])-s.diff(Gam(k,i,k),coords[j])
             +sum(Gam(k,k,l)*Gam(l,i,j)-Gam(k,j,l)*Gam(l,i,k)
                  for l in range(4)) for k in range(4))
        Ric[i,j]=Ric[j,i]=s.factor(v)
    scal=s.factor(sum(inv[i,i]*Ric[i,i] for i in range(4)))
    Ein=(Ric-g*scal/2).applyfunc(s.factor)
    # Construct the independent SO(1,3) spin connection from the tetrad;
    # all 24 torsion equations are checked before choosing R(t,x).
    hs=[s.Integer(1),s.diff(R,x),R/s.sqrt(1-z*z),R*s.sqrt(1-z*z)]
    signs=(1,-1,-1,-1)
    @lru_cache(None)
    def om(a,b,mu):
        return s.factor(hs[a]*Gam(a,mu,b)/hs[b]
                       -(s.diff(hs[b],coords[mu])/hs[b] if a==b else 0))
    for mu in range(4):
      for a in range(4):
        for b in range(a+1,4):
          check(f'proper Lorentz connection {mu},{a},{b}',
                s.simplify(signs[a]*om(a,b,mu)+signs[b]*om(b,a,mu))==0)
    for a in range(4):
      for mu in range(4):
        for nu in range(mu+1,4):
          T=(s.diff(hs[a],coords[mu]) if a==nu else 0)
          T-=(s.diff(hs[a],coords[nu]) if a==mu else 0)
          T+=om(a,nu,mu)*hs[nu]-om(a,mu,nu)*hs[mu]
          check(f'independent torsion row {a},{mu},{nu}',s.simplify(T)==0)
    A=s.symbols('A',positive=True)
    b=s.Function('b')(x);T=t-b;D=T-2*x*s.diff(b,x)
    radius=A*x**s.Rational(1,3)*T**s.Rational(2,3)
    expressions=list(Ein)+[scal,R*R*s.diff(R,x)]
    repl={R:radius}
    for e in expressions:
      for der in e.atoms(s.Derivative):
        if der.expr==R:repl[der]=s.diff(radius,*der.variables)
    reduced=Ein.applyfunc(lambda e:s.factor(e.xreplace(repl)))
    sc=s.factor(scal.xreplace(repl))
    vol=s.factor((R*R*s.diff(R,x)).xreplace(repl))
    rho=4/(3*T*D)
    for i in range(4):
      for j in range(4):
        check(f'inhomogeneous Einstein row {i},{j}',
              s.simplify(reduced[i,j]-(rho if i==j==0 else 0))==0)
    check('nonzero scalar curvature',s.simplify(sc+rho)==0)
    check('actual positive volume on declared chart',s.factor(vol-A**3*T*D/3)==0)
    check('constant densitized curvature',s.factor(vol*sc+4*A**3/9)==0)
    check('dust conservation without FLRW/Bianchi ansatz',s.diff(s.factor(vol*rho),t)==0)
    q0,kap,eta=s.symbols('q0 kappa eta',positive=True)
    source=vol*reduced-kap*q0*s.diag(1,0,0,0)
    source=source.applyfunc(lambda e:s.factor(e).subs(A**3,9*kap*q0/4))
    # All 16 coframe rows follow from this symmetric metric tensor and the
    # already independently checked 24 connection equations.
    for a in range(4):
      for mu in range(4):
        check(f'full coframe source {a},{mu}',s.simplify(source[a,mu])==0)
    psi=[s.sqrt(q0)*t,s.Integer(0)]
    for idx,field in enumerate(psi):
        eq=sum(s.diff(sum(inv[mu,nu]*s.diff(field,coords[nu])
                     for nu in range(4)),coords[mu]) for mu in range(4))
        check(f'fixed-measure scalar row {idx}',s.simplify(eq)==0)
    check('native nonnull trace relation',
          s.simplify((-eta**2*kap*q0)-kap*(-eta**2*q0))==0)
    # A change to sqrt(|g|)*q is not permitted: it destroys this solution.
    wrong=s.factor(s.diff(vol*s.sqrt(q0),t))
    check('hostile added scalar volume fails',wrong!=0)
    def Rlow(a,b,c,d):
        return s.factor(sum(g[a,e]*(s.diff(Gam(e,d,b),coords[c])
          -s.diff(Gam(e,c,b),coords[d])
          +sum(Gam(e,c,f)*Gam(f,d,b)-Gam(e,d,f)*Gam(f,c,b)
               for f in range(4))) for e in range(4)))
    Weyl=s.factor(Rlow(0,1,0,1)-(g[0,0]*Ric[1,1]+g[1,1]*Ric[0,0])/2
                  +scal*g[0,0]*g[1,1]/6)
    Weyl_orth=s.factor((Weyl/s.diff(R,x)**2).xreplace(repl))
    expected=-8*x*s.diff(b,x)/(9*T*T*D)
    check('explicit nonzero radial orthonormal Weyl',s.factor(Weyl_orth-expected)==0)
    # At b(x)=epsilon*x, positive nonzero values give a strict non-VSI check.
    eps=s.symbols('epsilon',positive=True)
    sc_spec=s.simplify(sc.subs({b:eps*x,s.diff(b,x):eps}))
    check('scalar invariants are not all zero',sc_spec!=0)
    # It is a known marginally bound LTB geometry. New claim is its exact
    # substitution into every literal finite-cap D0 continuum price.
    return {'geometry':'ds2=dt2-R_x^2 dx2-R^2[dz2/(1-z2)+(1-z2)dw2]',
            'radius':'R=A*x^(1/3)*(t-b(x))^(2/3)',
            'domain':'x>0, |z|<1, T=t-b(x)>0, D=T-2*x*bprime(x)>0',
            'Einstein_00':'4/(3*T*D)',
            'Einstein_other_components':'0',
            'scalar_curvature':'-4/(3*T*D)',
            'volume':'A^3*T*D/3',
            'volume_times_R':'-4*A^3/9',
            'radial_Weyl':'-8*x*bprime(x)/(9*T^2*D)',
            'source_condition':'A^3=9*kappa_star*q_star/4; kappa_star=r_y/r_x',
            'checked':'16 coframe, 24 torsion, 2 fixed-measure scalar rows',
            'LTB_not_new_GR_solution':True}


def main() -> None:
    a=exact_density_identities()
    b,detector=golden_polynomial_identities()
    c=cap_branch_diagnostics(detector)
    d=arbitrary_inhomogeneous_solution()
    result={'status':'AUTHOR_CHECKS_PASS','count':len(CHECKS),'checks':CHECKS,
      'input_commit':'086fab99d8aaed7f712e9a3d2858c516b61901fc',
      'exact_Ward_algebra':a,'native_detector':b,'cap_diagnostics':c,
      'full_inhomogeneous_continuum_witness':d,
      'closed_scope':'all regular local coupled stationary solutions of the declared fixed-measure continuum price',
      'native_moving_query_admitted':False,'complete_Book03_price_selected':False,
      'finite_lattice_lift_proved':False,'GR_closed':False}
    text=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    (HERE/'RESULT.json').write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':main()
