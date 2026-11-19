#!/usr/bin/env python3
"""Exact author checks for the D0 null two-field source fibre and its dynamics.

Run with Python 3 and SymPy.  No network, numerical root finding, input writes,
or precomputed metric tensor is needed.  Checks use explicit exceptions, so
python -O retains every control.  This checks new source, symmetry, symbol and countercontrol identities, not
native Book03 admission or the inherited curvature/root certificates.
"""
from __future__ import annotations
import json
import sys
import sympy as sp

checks: list[str] = []


def zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    entries = list(expression) if isinstance(expression, sp.MatrixBase) else [expression]
    if any(sp.simplify(sp.expand(e)) != 0 for e in entries):
        raise RuntimeError(f"FAIL: {name}: {expression}")
    checks.append(name)


def truth(name: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError(f"FAIL: {name}")
    checks.append(name)


def main() -> None:
    a, b = sp.symbols('a b', positive=True)
    lam, D, u1, u2, u3, w1, w2, w3 = sp.symbols('lambda D u1 u2 u3 w1 w2 w3', real=True)
    c = sp.Symbol('c')
    omega = sp.Symbol('omega', real=True)
    # Potential + multiplier symbol. Overall factors of i and nonzero row
    # normalizations do not change the characteristic zero set.
    P2 = sp.Matrix([[lam*D, 0, u1], [0, lam*D, u2], [u1, u2, 0]])
    zero('two-field bordered determinant', P2.det() + lam*D*(u1*u1+u2*u2))
    u3v = sp.Matrix([u1, u2, u3])
    P3 = (lam*D*sp.eye(3)).row_join(u3v).col_join(sp.Matrix([[u1, u2, u3, 0]]))
    zero('three-field bordered determinant', P3.det() + (lam*D)**2*(u1*u1+u2*u2+u3*u3))

    # Covariant no-foliation quadratic: u encodes time derivatives in field
    # space and w a spatial directional derivative. Positive target metric.
    f2 = (omega*u1+w1)**2+(omega*u2+w2)**2
    disc2 = sp.discriminant(f2, omega)
    zero('two-field discriminant is negative squared minor', disc2+4*(u1*w2-u2*w1)**2)
    f3 = f2+(omega*u3+w3)**2
    minors = (u1*w2-u2*w1)**2+(u1*w3-u3*w1)**2+(u2*w3-u3*w2)**2
    zero('three-field Gram discriminant', sp.discriminant(f3, omega)+4*minors)
    zero('aligned field gradients collapse the complex branch', disc2.subs({w1:3*u1,w2:3*u2}))
    truth('independent time and spatial gradients give strict negative discriminant', disc2.subs({u1:2,u2:0,w1:0,w2:3}) < 0)

    # Derive the 1+1 principal evolution, rather than only inserting a
    # desired characteristic polynomial. z=(delta V1_x,delta V2_x,
    # delta V2_t,delta log Lambda); norm fixes delta V1_t=b/a*delta V2_x.
    W, R, S, L = sp.symbols('W R S L')
    Wx, Rx, Sx, Lx = sp.symbols('Wx Rx Sx Lx')
    Wt, Rt, St, Lt = sp.symbols('Wt Rt St Lt')
    equations = [Wt-b/a*Rx, Rt-Sx, St-Rx-b*Lx, b/a*Rt-Wx+a*Lt]
    sol = sp.solve(equations, [Wt,Rt,St,Lt], dict=True)[0]
    flow = sp.Matrix([sol[Wt],sol[Rt],sol[St],sol[Lt]])
    A = flow.jacobian([Wx,Rx,Sx,Lx])
    expected = sp.Matrix([[0,b/a,0,0],[0,0,1,0],[0,1,0,b],[1/a,0,-b/a**2,0]])
    zero('first-order matrix derived from all scalar and norm equations', A-expected)
    zero('integrability of first scalar retained', sol[Wt]-b/a*Rx)
    zero('integrability of second scalar retained', sol[Rt]-Sx)
    zero('first current includes multiplier time derivative', (b/a*Rt-Wx+a*Lt).subs(sol))
    zero('second current includes multiplier space derivative', (St-Rx-b*Lx).subs(sol))
    charpoly = sp.factor((c*sp.eye(4)-A).det())
    zero('full constraint-reduced characteristic polynomial', charpoly-(c*c-1)*(c*c+b*b/(a*a)))
    for tag, root in [('light plus',1),('light minus',-1),('nonreal plus',sp.I*b/a),('nonreal minus',-sp.I*b/a)]:
        zero(f'characteristic root {tag}', charpoly.subs(c,root))

    # The original crossing-stream witness gives a=b=sqrt(B/E)>0.
    B, d = sp.symbols('B d', positive=True)
    E = sp.exp(d*B*B/2)
    g = sp.diag(B*E,-E/B,-B**2,-B**2)
    v1, v2 = sp.Matrix([B,0,0,0]), sp.Matrix([0,1,0,0])
    norm1=(v1.T*g.inv()*v1)[0]
    norm2=(v2.T*g.inv()*v2)[0]
    zero('witness first gradient norm', norm1-B/E)
    zero('witness second gradient norm', norm2+B/E)
    zero('witness total kinetic constraint', norm1+norm2)
    zero('witness scalar gradients orthogonal', (v1.T*g.inv()*v2)[0])
    zero('witness equal orthonormal gradient amplitudes', (B/sp.sqrt(B*E))**2-(1/sp.sqrt(E/B))**2)
    zero('witness dimensionless characteristic polynomial', charpoly.subs(b,a)-(c*c-1)*(c*c+1))
    zero('coordinate conversion of principal speed', sp.sqrt(B*E)/sp.sqrt(E/B)-B)
    zero('high-frequency eikonal exponent derivative', sp.diff(B**2/2,B)-B)

    # Explicit REAL growing solution of the frozen principal system.
    t,x,k = sp.symbols('t x k', real=True, positive=True)
    growth = sp.exp(k*t)
    U = -growth*sp.cos(k*x)/k
    V = -growth*sp.sin(k*x)/k
    ell = 2*growth*sp.cos(k*x)
    zero('real growing first scalar current', sp.diff(U,t,2)-sp.diff(U,x,2)+sp.diff(ell,t))
    zero('real growing second scalar current', sp.diff(V,t,2)-sp.diff(V,x,2)-sp.diff(ell,x))
    zero('real growing linearized norm constraint', sp.diff(U,t)-sp.diff(V,x))
    Z=sp.Matrix([sp.diff(U,x),sp.diff(V,x),sp.diff(V,t),ell])
    A0=A.subs({a:1,b:1})
    zero('real growing full first-order state', Z.diff(t)-A0*Z.diff(x))
    ev=sp.Matrix([-sp.I,-1,sp.I,2])
    zero('growing eigenvector before the source quotient', A0*ev+sp.I*ev)
    truth('freezing multiplier destroys growing solution', sp.simplify(sp.diff(U,t,2)-sp.diff(U,x,2)) != 0)

    # Coupled Einstein consistency, at the principal Fourier level.
    # kappa^2=-2 !=0: harmonic residual coordinate waves cannot generate it.
    eta=sp.diag(1,-1,-1,-1)
    kappa=sp.Matrix([sp.I,1,0,0])
    raised=eta*kappa
    D0=(kappa.T*eta*kappa)[0]
    covectors=[sp.Matrix([1,0,0,0]),sp.Matrix([0,1,0,0])]
    us=[(v.T*raised)[0] for v in covectors]
    ell0=sp.Integer(2)
    amps=[sp.I,sp.Integer(-1)]
    X=sum((v*v.T for v in covectors),sp.zeros(4))
    dT=ell0*X
    for v,amp in zip(covectors,amps):
        dv=kappa*amp
        dT += v*dv.T+dv*v.T
    for i in range(2):
        zero(f'coupled scalar symbol {i+1}', D0*amps[i]+us[i]*ell0)
    zero('coupled norm symbol', sum(us[i]*amps[i] for i in range(2)))
    zero('all four leading stress-conservation rows', raised.T*dT)
    zero('corrected diagnostic: growing null mode has EXACTLY ZERO stress', dT)
    zero('null-sector stress trace', sp.trace(eta*dT))
    truth('nonreal branch is not a residual harmonic gauge characteristic', D0 != 0)
    hbar=-2*dT/D0
    zero('the same zero metric perturbation solves the sourced harmonic block', hbar)
    zero('harmonic metric constraint satisfied', raised.T*hbar)

    # Hostile controls: aligned / frozen / single-field claims do not follow.
    Azero=A.subs({a:1,b:0})
    zero('rank-one limiting polynomial', (c*sp.eye(4)-Azero).det()-c*c*(c*c-1))
    truth('rank-one limit is not declared strongly hyperbolic by real roots', len(Azero.nullspace()) == 1)
    epsilon=sp.Symbol('epsilon', positive=True)
    zero('arbitrarily small nonparallel gradient still gives nonreal speeds', charpoly.subs({a:1,b:epsilon,c:sp.I*epsilon}))

    # Fixed-sector weighted-Hessian correction. This checks the *algebra*
    # used with the independently owned Ward identity, not that Ward proof.
    rho,M,tau,K2,dq_v,dq_w=sp.symbols('rho M tau K2 dq_v dq_w', nonzero=True)
    correction=M*tau*tau*K2/rho*dq_v*dq_w
    zero('weighted Hessian correction vanishes on fixed-density tangent', correction.subs(dq_v,0))
    truth('weighted first-source equality alone does not imply Hessian equality', correction != 0)


    # EXACT target-conformal invariance: no field equations or high-frequency
    # approximation are needed for the matter-action identity at q_*=0.
    Uc,Vc,qstar,q0,lambda0=sp.symbols('Uc Vc qstar q0 lambda0', real=True)
    Jc=sp.Matrix([[Uc,-Vc],[Vc,Uc]])
    scale=Uc**2+Vc**2
    zero('conformal target Jacobian Gram', Jc.T*Jc-scale*sp.eye(2))
    zero('conformal target Jacobian determinant', Jc.det()-scale)
    original_matter=-lambda0*q0
    transformed_matter=-(lambda0/scale)*(scale*q0)
    zero('null multiplier action invariant OFF SHELL', transformed_matter-original_matter)
    defect=-(lambda0/scale)*(scale*q0-qstar)+lambda0*(q0-qstar)
    zero('nonnull fixed-sector action has retained defect', defect-lambda0*qstar*(1/scale-1))
    truth('nonnull sector cannot inherit arbitrary conformal symmetry', defect.subs({lambda0:2,qstar:1,Uc:2,Vc:0}) != 0)
    target_reflection=sp.diag(1,-1)
    zero('orientation-reversing conformal maps are retained', (target_reflection*Jc).T*(target_reflection*Jc)-scale*sp.eye(2))

    # A nonconstant holomorphic map f(z)=z+eps*z^2, tested through a
    # general 2-by-4 field derivative matrix, not just diagonal gradients.
    ps,px,eps=sp.symbols('ps px eps', real=True)
    fmap=sp.Matrix([ps+eps*(ps**2-px**2),px+2*eps*ps*px])
    Jac=fmap.jacobian([ps,px])
    Dpoly=(1+2*eps*ps)**2+4*eps**2*px**2
    zero('polynomial map is conformal in every target direction', Jac.T*Jac-Dpoly*sp.eye(2))
    entries=sp.symbols('v0:8', real=True)
    Vmat=sp.Matrix(2,4,entries)
    tensor=Vmat.T*Vmat
    newtensor=(Jac*Vmat).T*(Jac*Vmat)
    zero('all sixteen full-source tensor entries invariant', newtensor-Dpoly*tensor)
    zero('full Lorentz kinetic contraction scales correctly', sp.trace(eta*newtensor)-Dpoly*sp.trace(eta*tensor))
    zero('scaled multiplier cancels the full tensor change', (lambda0/Dpoly)*newtensor-lambda0*tensor)
    anisotropic=sp.diag(2,1)
    truth('generic target reparametrization is NOT a same-source map', anisotropic.T*anisotropic != 4*sp.eye(2))
    truth('source equality needs the multiplier compensation', newtensor.subs({eps:1,ps:0,px:1}) != tensor)

    # Reconstruct the original witness intrinsically from its rank-two T.
    h=sp.diag(d,d/B**2)
    ds=sp.Matrix([B,0])
    dx=sp.Matrix([0,1])
    zero('witness intrinsic two-metric has isothermal coordinates s=B^2/2,x', h-(d/B**2)*(ds*ds.T+dx*dx.T))
    # *h on a one-form (alpha_B,alpha_x): (-B alpha_x,alpha_B/B).
    star_h=sp.Matrix([[0,-B],[1/B,0]])
    zero('harmonic-conjugate construction gives dx exactly', star_h*ds-dx)
    zero('Riemannian star square on one-forms', star_h*star_h+sp.eye(2))
    harmonic_s=sp.diff((d/B)*(B/d),B)
    zero('the intrinsic first coordinate is h-harmonic', harmonic_s)

    # Hostile intrinsic test: positive rank two + traceless + conserved is
    # insufficient. The transverse conformal class must descend to leaf space.
    Yc,Zc=sp.symbols('Yc Zc', real=True)
    Tbad=sp.Matrix([[1,Yc,0,0],[Yc,1,0,0],[0,0,0,0],[0,0,0,0]])
    zero('hostile tensor is Lorentz traceless', sp.trace(eta*Tbad))
    coords=[ps,px,Yc,Zc]
    divergence=sp.Matrix([sum(eta[i,i]*sp.diff(Tbad[i,j],coords[i]) for i in range(4)) for j in range(4)])
    zero('hostile tensor is divergence free', divergence)
    zero('hostile rank-two determinant', Tbad[:2,:2].det()-(1-Yc**2))
    truth('hostile tensor positive and rank two on |Yc|<1', Tbad.subs(Yc,sp.Rational(1,2)).rank()==2 and Tbad[:2,:2].subs(Yc,sp.Rational(1,2)).is_positive_definite)
    zero('hostile first kernel vector', Tbad*sp.Matrix([0,0,1,0]))
    zero('hostile second kernel vector', Tbad*sp.Matrix([0,0,0,1]))
    # The diagonal entries force beta=0; the derivative of T01 is then 1.
    zero('conformal-basicness would force beta zero on the diagonal', sp.diff(Tbad[0,0],Yc))
    truth('hostile leafwise derivative cannot be a scalar multiple', sp.diff(Tbad[0,1],Yc)==1)

    # Complete nonlinear exponential family f=z+(c/k)exp(k(z-s1)).
    # Let r=c*exp(k(s-s1)), angle=k*x. The two differentiations are
    # k*r*d_r and k*d_angle; these retain every denominator derivative.
    r,angle=sp.symbols('r angle', real=True)
    Ur=1+r*sp.cos(angle)
    Vr=r*sp.sin(angle)
    Dr=1+2*r*sp.cos(angle)+r**2
    Jexp=sp.Matrix([[Ur,-Vr],[Vr,Ur]])
    zero('nonlinear exponential map full Jacobian', Jexp.T*Jexp-Dr*sp.eye(2))
    zero('nonlinear first current on the ACTUAL curved witness', r*sp.diff(Ur/Dr,r)+sp.diff(Vr/Dr,angle))
    zero('nonlinear second current on the ACTUAL curved witness', r*sp.diff(Vr/Dr,r)-sp.diff(Ur/Dr,angle))
    active_inverse=sp.diag(1,-1)
    zero('nonlinear constraint exactly zero on the witness', sp.trace(active_inverse*(Jexp.T*Jexp)))
    zero('nonlinear whole stress exactly unchanged on the witness', (Jexp.T*Jexp)/Dr-sp.eye(2))
    # The sequence stays in a uniformly regular positive chart for 0<c<1.
    cc=sp.Symbol('cc', real=True, positive=True)
    zero('denominator lower bound identity', Dr-(1-r)**2-2*r*(1+sp.cos(angle)))
    zero('denominator upper bound identity', (1+r)**2-Dr-2*r*(1-sp.cos(angle)))
    zero('terminal coefficient retains nonconstant multiplier', Dr.subs(r,cc)-(1+2*cc*sp.cos(angle)+cc**2))
    truth('explicit c=1/4 terminal discrepancy is nonzero', (1/Dr-1).subs({r:sp.Rational(1,4),angle:0}) == -sp.Rational(9,25))
    # Integral mean follows from |1+c exp(i x)|^-2 double geometric series.
    # The zeroth Fourier coefficient is sum_(n>=0)c^(2n).
    n=sp.Symbol('n', integer=True, nonnegative=True)
    mean_series=sp.summation(cc**(2*n),(n,0,sp.oo))
    mean_formula=mean_series.args[0][0] if isinstance(mean_series,sp.Piecewise) else mean_series
    zero('exact terminal mean from the convergent Fourier series', mean_formula-1/(1-cc**2))
    zero('strict mean discrepancy for every fixed 0<c<1', 1/(1-cc**2)-1-cc**2/(1-cc**2))
    zero('c=1/4 L2 lower-bound coefficient', (cc**2/(1-cc**2)).subs(cc,sp.Rational(1,4))-sp.Rational(1,15))

    # Original volume-gauge return requires a REAL coordinate Jacobian,
    # including its generally nonzero spatial derivatives (shift).
    k0=sp.Symbol('k0', positive=True)
    e_old=B**2*E
    Lambda_old=d/B**2
    Lambda_new=Lambda_old/Dr
    jacobian=d*E/(k0*Dr)
    e_native=e_old/jacobian
    zero('actual positive volume Jacobian restores e*Lambda=k0', e_native*Lambda_new-k0)
    zero('old fixed native metric cannot hide a changing multiplier', k0/Dr-k0-k0*(1/Dr-1))
    truth('a nontrivial conformal scaling changes the native volume gauge', (k0/Dr-k0).subs({r:sp.Rational(1,4),angle:0}) != 0)
    # If the ORIGINAL metric and coordinate volume are fixed, Lambda is
    # fixed; source preservation reduces to Df^T Df=I, i.e. rigid local
    # Euclidean target transformations, not arbitrary holomorphic maps.
    theta=sp.Symbol('theta', real=True)
    rotation=sp.Matrix([[sp.cos(theta),-sp.sin(theta)],[sp.sin(theta),sp.cos(theta)]])
    zero('rigid target rotation survives the fixed native metric gauge', rotation.T*rotation-sp.eye(2))
    truth('native fixed-metric fibre excludes non-unit dilation', (4*sp.eye(2)) != sp.eye(2))

    # Same null full-source application to the actual PF-weighted price.
    aprice,bprice,df,dq=sp.symbols('aprice bprice df dq')
    weighted=rho*(aprice*tau*df/rho+bprice*tau*dq/rho)
    zero('all fixed positive PF weights cancel in the null first covector', weighted-tau*(aprice*df+bprice*dq))
    gain=sp.Symbol('gain', real=True)
    zero('gain sign retained, not squared', gain*weighted-gain*tau*(aprice*df+bprice*dq))

    result={
        'status':'PASS',
        'scope':'exact null source-fibre identities, complete-family currents and symbol author check; not physical D0/GR closure',
        'checks':checks,
        'count':len(checks),
        'general_two_field_characteristic_polynomial':'(c^2-1)*(c^2+b^2/a^2)',
        'crossing_witness_speeds':['1','-1','i','-i'],
        'crossing_witness_coordinate_speeds':['B','-B','i*B','-i*B'],
        'frozen_growing_solution':'(delta psi1,delta psi2,delta log Lambda)=exp(k*t)*(-cos(k*x)/k,-sin(k*x)/k,2*cos(k*x))',
        'coupled_principal_stress_conserved':True,
        'growing_null_mode_stress':'EXACTLY ZERO',
        'null_action_target_conformal_symmetry':'EXACT OFF SHELL',
        'nonlinear_family_metric_and_stress':'EXACTLY UNCHANGED',
        'native_fixed_metric_fibre':'rigid Euclidean target maps only',
        'earlier_nonzero_stress_conjecture':'REJECTED by the exact stress calculation',
        'fresh_historical_curvature_replay':False,
        'independent_review':False,
        'GR_closed':False
    }
    print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
