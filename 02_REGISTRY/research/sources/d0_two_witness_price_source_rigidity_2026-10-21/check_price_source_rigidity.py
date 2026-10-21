#!/usr/bin/env python3
"""Exact source checks for the D0 two-witness curvature-correction test.

Run with Python >=3.10 and SymPy. No network, imported geometric tensor,
expected-output mutation, or assert statement is used. JSON goes to stdout.
The proof is in PROOF.md; finite checks do not replace its quantifiers.
"""
from __future__ import annotations

from functools import lru_cache
import json
import math
import sys

try:
    import sympy as s
except ImportError as exc:
    raise SystemExit("Install sympy before running this checker.") from exc

CHECKS: list[str] = []

def clean(expr):
    return s.factor(s.cancel(s.expand_power_base(expr, force=True)))

def zero(name: str, expr) -> None:
    value = clean(expr)
    if value != 0:
        value = s.simplify(value)
    if value != 0:
        raise ArithmeticError(f"{name}: nonzero residual {value}")
    CHECKS.append(name)

def true(name: str, condition: bool) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)

class DiagonalTimeMetric:
    """Full four-dimensional tensors; only coordinate 0 has dependence."""
    def __init__(self, time, entries):
        self.time = time
        entries = [s.sympify(x) for x in entries]
        self.g = s.diag(*entries)
        self.inv = s.diag(*(s.S.One / x for x in entries))
        if self.g.atoms(s.Float) or self.inv.atoms(s.Float):
            raise ValueError("The exact checker does not accept floating metrics.")

    def diff(self, value, index):
        return s.diff(value, self.time) if index == 0 else s.S.Zero

    @lru_cache(None)
    def gamma(self, a, m, n):
        return clean(sum(self.inv[a,j] * (self.diff(self.g[j,n],m)
            + self.diff(self.g[j,m],n) - self.diff(self.g[m,n],j)) / 2
            for j in range(4)))

    @lru_cache(None)
    def riemann(self, a, b, c, d):
        return clean(self.diff(self.gamma(a,d,b),c)
            - self.diff(self.gamma(a,c,b),d)
            + sum(self.gamma(a,c,k)*self.gamma(k,d,b)
                  - self.gamma(a,d,k)*self.gamma(k,c,b) for k in range(4)))

    @lru_cache(None)
    def ricci(self, m, n):
        return clean(sum(self.riemann(k,m,k,n) for k in range(4)))

    @lru_cache(None)
    def scalar(self):
        return clean(sum(self.inv[m,m]*self.ricci(m,m) for m in range(4)))

    def scalar_hessian(self, f, m, n):
        return clean(self.diff(self.diff(f,n),m)
            - sum(self.gamma(k,m,n)*self.diff(f,k) for k in range(4)))

    def box_scalar(self, f):
        return clean(sum(self.inv[i,i]*self.scalar_hessian(f,i,i)
                         for i in range(4)))

    @lru_cache(None)
    def dric(self, a, m, n):
        return clean(self.diff(self.ricci(m,n),a)
            - sum(self.gamma(k,a,m)*self.ricci(k,n)
                  + self.gamma(k,a,n)*self.ricci(m,k) for k in range(4)))

    @lru_cache(None)
    def ddric(self, a, b, m, n):
        return clean(self.diff(self.dric(b,m,n),a)
            - sum(self.gamma(k,a,b)*self.dric(k,m,n)
                  + self.gamma(k,a,m)*self.dric(b,k,n)
                  + self.gamma(k,a,n)*self.dric(b,m,k) for k in range(4)))

    def ricci_squared(self):
        return clean(sum(self.inv[i,i]*self.inv[j,j]*self.ricci(i,j)**2
                         for i in range(4) for j in range(4)))

    def euler_ricci_squared(self):
        R, Q = self.scalar(), self.ricci_squared()
        boxR = self.box_scalar(R)
        T = s.zeros(4)
        for m in range(4):
            for n in range(4):
                RR = sum(self.g[m,m]*self.riemann(m,a,n,b)
                    *self.inv[a,a]*self.inv[b,b]*self.ricci(a,b)
                    for a in range(4) for b in range(4))
                boxRic = sum(self.inv[a,a]*self.ddric(a,a,m,n)
                             for a in range(4))
                T[m,n] = clean(2*RR + boxRic
                    - self.scalar_hessian(R,m,n)
                    + self.g[m,n]*(boxR-Q)/2)
        return T

    def euler_scalar_function(self, f_value, f_prime):
        box = self.box_scalar(f_prime)
        return s.Matrix(4,4,lambda m,n: clean(f_prime*self.ricci(m,n)
            - self.g[m,n]*f_value/2 + self.g[m,n]*box
            - self.scalar_hessian(f_prime,m,n)))

    def divergence(self, T, n):
        return clean(sum(self.inv[m,m]*(self.diff(T[m,n],m)
            - sum(self.gamma(k,m,m)*T[k,n]
                  + self.gamma(k,m,n)*T[m,k] for k in range(4)))
            for m in range(4)))


def main() -> dict:
    b,d = s.symbols('b d', positive=True)
    E = s.exp(d*b*b/2)
    cross = DiagonalTimeMetric(b, [b*E,-E/b,-b*b,-b*b])
    expected_ric = s.diag(d,d/b**2,0,0)
    for i in range(4):
        for j in range(4):
            zero(f'cross.ricci.{i}{j}',cross.ricci(i,j)-expected_ric[i,j])
    zero('cross.scalar',cross.scalar())
    Q = cross.ricci_squared()
    zero('cross.ricci_squared',Q-2*d*d*s.exp(-d*b*b)/b**2)
    T = cross.euler_ricci_squared()
    expected = s.diag(d*(b*b*d-2)/(b**3*E),
                     d*(3*b*b*d+2)/(b**5*E),
                     -d*(b*b*d+2)/(b**2*E**2),
                     -d*(b*b*d+2)/(b**2*E**2))
    for i in range(4):
        for j in range(4):
            zero(f'cross.eulerQ.{i}{j}',T[i,j]-expected[i,j])
    zero('cross.eulerQ.trace',sum(cross.inv[i,i]*T[i,i] for i in range(4)))
    for j in range(4):
        zero(f'cross.eulerQ.divergence.{j}',cross.divergence(T,j))
    A = clean(T[2,2]/cross.g[2,2])
    zero('cross.transverse.ratio',A-d*(d*b*b+2)*s.exp(-d*b*b)/b**4)
    zero('cross.transverse.ratio.derivative',s.diff(A,b)
         +2*d*s.exp(-d*b*b)*(d*d*b**4+3*d*b*b+4)/b**5)
    true('cross.transverse.strictly_negative',s.ask(s.Q.negative(expected[2,2])) is True)
    f0,f1,beta = s.symbols('f0 f1 beta')
    correction = f1*expected_ric - f0*cross.g/2 + beta*T
    zero('cross.normalization.elimination',correction[2,2]/cross.g[2,2] +f0/2-beta*A)
    zero('cross.remaining.EH_coefficient',correction[0,0].subs({f0:0,beta:0})-f1*d)

    # Independent check: vary a transverse scale in the action density,
    # then integrate h, h', h'' by parts. No use of the Euler-tensor formula.
    h = s.Function('h')(b)
    N = s.sqrt(b*E)
    D = lambda value: clean(s.diff(value,b)/N)
    scales = [s.sqrt(E/b),b,b]
    H = [clean(D(s.log(a))) for a in scales]
    K0 = clean(sum(D(Hi)+Hi**2 for Hi in H))
    K = [clean(D(Hi)+Hi*sum(H)) for Hi in H]
    zero('independent.BianchiI.Q',Q-K0**2-sum(Ki**2 for Ki in K))
    Dh, DDh = D(h), D(D(h))
    dK0 = DDh+2*H[1]*Dh
    dK = [H[i]*Dh+(DDh+sum(H)*Dh if i==1 else 0) for i in range(3)]
    vol = b*b*E
    first = clean(vol*(Q*h+2*K0*dK0+sum(2*K[i]*dK[i] for i in range(3))))
    coeff = [clean(s.diff(first,s.diff(h,b,k))) for k in range(3)]
    EL = clean(coeff[0]-s.diff(coeff[1],b)+s.diff(coeff[2],b,2))
    zero('independent.action.transverse',EL-2*vol*T[2,2]/b**2)

    # Dust is a member of the already owned positive-multiplier class.
    t,eps,k = s.symbols('t eps k', positive=True)
    scale = t**s.Rational(2,3)
    dust = DiagonalTimeMetric(t,[1,-scale**2,-scale**2,-scale**2])
    R = dust.scalar()
    zero('dust.scalar',R+4/(3*t*t))
    for i in range(4):
        for j in range(4):
            Ein = clean(dust.ricci(i,j)-dust.g[i,j]*R/2)
            zero(f'dust.Einstein.{i}{j}',Ein-(4/(3*t*t) if i==j==0 else 0))
    Lam = 4/(3*eps**2*t*t)
    zero('dust.current',s.diff(t*t*Lam*eps,t))
    jac = 4/(3*eps**2*k)
    enative = t*t/jac
    zero('dust.native.volume',enative*Lam-k)
    zero('dust.native.density',enative*R+k*eps**2)
    zero('dust.native.current',s.diff(jac*eps,t))
    zero('dust.boxR.control',dust.box_scalar(R)+s.Rational(3,2)*R**2)

    r = -R
    m = s.symbols('m', real=True)
    f = r**m
    fp = -m*r**(m-1)
    Tf = dust.euler_scalar_function(f,fp)
    P = 6*m*m-7*m-1
    # Exact identities for arbitrary real m (r,t positive).
    for i in range(4):
        for j in range(4):
            target = (P*f/2 if i==j==0 else
                      (m-1)*P*f*scale**2/2 if i==j else 0)
            zero(f'dust.power.source.{i}{j}',s.powsimp(Tf[i,j]-target,force=True))
    mp,mm = (7+s.sqrt(73))/12,(7-s.sqrt(73))/12
    for label,root in [('plus',mp),('minus',mm)]:
        zero(f'dust.indicial.{label}',P.subs(m,root))
    true('dust.irrational.discriminant',math.isqrt(73)**2 != 73)
    true('dust.plus.between_one_and_two',bool(mp>1) and bool(mp<2))
    true('dust.minus.negative',bool(mm<0))
    # A C1 but not C2 invisible metric correction is real, not forgotten.
    true('dust.plus.second_derivative.nonzero',mp*(mp-1) != 0)
    EQdust=dust.euler_ricci_squared()
    ER2=dust.euler_scalar_function(R**2,2*R)
    for i in range(4):
        for j in range(4):
            zero(f'dust.quadratic.relation.{i}{j}',EQdust[i,j]-ER2[i,j]/3)
    zero('dust.R2.00',ER2[0,0]-8/t**4)

    # Anisotropic witnesses remove the isotropic fractional-power loophole.
    # sigma=-1 has a spacelike normal; coordinate 1 is its timelike coordinate.
    v,A,eps2,k2=s.symbols('v A eps2 k2',positive=True)
    a1=v*(v+A)**(-s.Rational(1,3))
    a2=(v+A)**s.Rational(2,3)
    V=v*(v+A)
    density=4/(3*V)
    uvar=s.Function('u')(v)
    fvar=s.Function('F')(v)
    anisotropic_results={}
    for sigma in (1,-1):
        label='timelike' if sigma==1 else 'spacelike'
        scene=DiagonalTimeMetric(v,[sigma,-sigma*a1**2,-a2**2,-a2**2])
        rv=scene.scalar()
        zero(f'anisotropic.{label}.R',rv+sigma*density)
        zero(f'anisotropic.{label}.volume',-scene.g.det()-V**2)
        for i in range(4):
            for j in range(4):
                gij=clean(scene.ricci(i,j)-scene.g[i,j]*rv/2)
                zero(f'anisotropic.{label}.Einstein.{i}{j}',
                     gij-(density if i==j==0 else 0))
        lam=density/eps2**2
        zero(f'anisotropic.{label}.current',s.diff(V*lam*sigma*eps2,v))
        qstar=sigma*eps2**2
        jac2=4/(3*eps2**2*k2)
        zero(f'anisotropic.{label}.native_volume',V*lam/jac2-k2)
        zero(f'anisotropic.{label}.native_trace',V*rv/jac2+k2*qstar)
        zero(f'anisotropic.{label}.native_current',s.diff(sigma*jac2*eps2,v))
        Evar=scene.euler_scalar_function(fvar,uvar)
        diffrow=clean(Evar[1,1]/scene.g[1,1]-Evar[2,2]/scene.g[2,2])
        zero(f'anisotropic.{label}.shear_row',
             diffrow+sigma*A*s.diff(uvar,v)/V)
        zero(f'anisotropic.{label}.Rprime',
             s.diff(rv,v)-sigma*4*(2*v+A)/(3*V**2))
        fpp=s.symbols('fpp')
        forced=clean(diffrow.subs(s.diff(uvar,v),fpp*s.diff(rv,v)))
        zero(f'anisotropic.{label}.forced_second_derivative',
             forced+4*A*(2*v+A)*fpp/(3*V**3))
        true(f'anisotropic.{label}.strict_coefficient',
             s.ask(s.Q.positive(4*A*(2*v+A)/(3*V**3))) is True)
        # A=0 deliberately recovers the old isotropic blind direction.
        zero(f'anisotropic.{label}.isotropic_control',forced.subs(A,0))
        anisotropic_results[label]={'R':str(rv),'difference':str(diffrow),
                                    'f_second_derivative_row':str(forced)}

    # Algebraic first-order connection equation: d f'(R)=f''(R)dR.
    eta = s.symbols('eta')
    zero('palatini.scalar.derivative',s.diff(2*R,t)-16/(3*t**3))
    true('palatini.dR.nonzero',s.diff(R,t) != 0)

    # Sharp boundary: genuine stationary elimination can produce
    # an irrational exponent from an algebraic-log two-variable price.
    x,u,alpha=s.symbols('x u alpha',positive=True)
    upstream=u*(s.log(u)-alpha*s.log(x)-1)
    zero('upstream.stationarity',s.diff(upstream,u)-(s.log(u)-alpha*s.log(x)))
    zero('upstream.root',s.expand_log(s.diff(upstream,u).subs(u,x**alpha),force=True))
    zero('upstream.reduced_price',s.expand_log(upstream.subs(u,x**alpha),force=True)+x**alpha)

    # A higher-curvature polynomial evades both witnesses: no universal
    # uniqueness claim follows from a successful quadratic/scalar test.
    rr,cc=s.symbols('R C2')
    invisible=(rr*cc)**2
    for name,var in [('R',rr),('C2',cc)]:
        zero(f'invisible.cross.{name}',s.diff(invisible,var).subs(rr,0))
        zero(f'invisible.dust.{name}',s.diff(invisible,var).subs(cc,0))
    true('invisible.not_identically_zero',invisible != 0)
    # A nontrivial higher-curvature correction stays invisible on the ENTIRE
    # two-scalar Einstein-multiplier class: det(G^mu_nu)^2. Rank is at most 2.
    TT=s.Matrix([[1,0],[0,1],[1,1],[2,-1]])
    B=s.diag(1,-1,-1,-1)*TT*TT.T
    zero('whole_class.rank_two.determinant',B.det())
    hdet=s.symbols('hdet')
    zero('whole_class.squared_ideal.first_derivative',s.diff(hdet**2,hdet).subs(hdet,0))
    kval=s.symbols('kval',nonzero=True)
    zero('whole_class.constant_curvature.control',(-3*kval*s.eye(4)).det()**2-6561*kval**8)
    scalejet=s.symbols('scalejet')
    scaled=s.exp(4*scalejet)*(s.exp(-8*scalejet)*81*kval**4)**2
    zero('whole_class.nonzero_scale_source',s.diff(scaled,scalejet).subs(scalejet,0)+12*6561*kval**8)
    # Gauss-Bonnet reduction of general quadratic metric actions.
    aa,bb,c0,K,Q0,R0,GB=s.symbols('a b c K Q R GB')
    zero('quadratic.Gauss_Bonnet',
         (aa*R0**2+bb*Q0+c0*K).subs(K,GB+4*Q0-R0**2)
         -((aa-c0)*R0**2+(bb+4*c0)*Q0+c0*GB))

    return {'status':'PASS','exact_identity_checks':len(CHECKS),
        'checks':CHECKS,'source_convention':'delta S = integral sqrt(-g) E_mn delta g^mn',
        'crossing_E_Q_diagonal':[str(expected[i,i]) for i in range(4)],
        'dust_scalar':'-4/(3*t**2)', 'dust_scalar_indicial':'6*m**2-7*m-1',
        'dust_indicial_roots':[str(mm),str(mp)],
        'independent_action_variation':'PASS',
        'anisotropic_source_rows':anisotropic_results,
        'native_Book_admission_proved':False,'GR_closed':False}

if __name__ == '__main__':
    try:
        print(json.dumps(main(),indent=2,sort_keys=True))
    except Exception as exc:
        print(f'FAIL: {exc}',file=sys.stderr)
        raise
