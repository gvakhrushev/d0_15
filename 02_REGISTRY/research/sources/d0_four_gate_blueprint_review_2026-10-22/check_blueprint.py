#!/usr/bin/env python3
"""Checks of the four-gate composition, not a new physical D0 closure.

Exact symbolic checks use SymPy; native Golden scalar diagnostics use mpmath.
The two-branch archive calculation is an exact linear-algebra control, not a
new implementation of the original 72,441-history writer. No private text is
embedded. No full42 root, Lean build, or repository-wide CI is asserted.
"""
from __future__ import annotations
import json
from fractions import Fraction as Q
from pathlib import Path
import sys
import sympy as s
from mpmath import mp

CHECKS: list[str] = []
def require(condition: bool, name: str) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def legendre_checks() -> dict:
    x, a = s.symbols('x a', real=True)
    lag = a*x-a*a/2
    h = s.hessian(lag, (x,a))
    schur = h[0,0]-h[0,1]*h[1,1]**-1*h[1,0]
    require(schur == 1, 'Legendre maximum has POSITIVE Schur correction')
    require(h[1,1] == -1, 'Auxiliary response block is negative, not positive')
    y1,y2 = s.symbols('y1 y2', real=True)
    q = 1+y1*y1-y2*y2
    price = q*q/2
    lag2 = a*q-a*a/2
    point = {y1:0,y2:0,a:1}
    H2 = s.hessian(price,(y1,y2)).subs(point)
    H3 = s.hessian(lag2,(y1,y2,a)).subs(point)
    require(H2 == s.diag(2,-2), 'Strictly convex operand cost can have a saddle pullback')
    require(H3 == s.diag(2,-2,-1), 'Exact Legendre lift retains and adds negative inertia')
    # Verify the block congruence used in the arbitrary-dimensional proof.
    A=s.Matrix([[2,1],[1,-2]]); B=s.Matrix([[1,2],[0,1]])
    D=-s.diag(2,3)
    H=A.row_join(B).col_join(B.T.row_join(D))
    T=s.eye(2).row_join(s.zeros(2)).col_join((-D.inv()*B.T).row_join(s.eye(2)))
    reduced=A-B*D.inv()*B.T
    target=reduced.row_join(s.zeros(2)).col_join(s.zeros(2).row_join(D))
    require(T.T*H*T == target, 'Block congruence: inertia(full)=inertia(reduced)+inertia(aux)')
    return {'reduced_toy_hessian':[[2,0],[0,-2]],
            'lifted_toy_hessian_diagonal':[2,-2,-1],
            'full46_negative_inertia':'negative(H42)+4, when the four response directions are independent'}


def modular_heat_checks() -> dict:
    f1,f2,z,beta,mu=s.symbols('f1 f2 z beta mu', positive=True)
    m1,m2=1-z*f1,1-z*f2
    heat=-mu+s.log(m1+m2)/beta
    book=-s.log(m1)-s.log(m2)
    vheat=s.simplify(s.diff(heat,f1)-s.diff(heat,f2))
    vbook=s.factor(s.diff(book,f1)-s.diff(book,f2))
    require(vheat==0, 'Trace-free band variation leaves proposed modular heat exactly constant')
    require(s.simplify(vbook-z*z*(f1-f2)/(m1*m2))==0,
            'Same variation has nonzero determinant derivative for unequal bands')
    mp.dps=80
    p=(mp.sqrt(5)-1)/2; zz=mp.mpf(2)**-20; bb=2*p*p
    B=4*p**3; A=B*(1+p**6); mult=528
    deriv=mult*zz*zz*(A-B)/((1-zz*A)*(1-zz*B))
    require(0<B<A<1, 'Unchanged native flat bands are distinct positive contractions')
    require(mp.mpf('2.5270e-11')<deriv<mp.mpf('2.5271e-11'),
            'Native 528+528 countercheck: modular cancellation is not an operator identity')
    # Derivative computed independently by high-precision scalar differentiation.
    def residual(t):
        mm1=1-zz*(A+t);mm2=1-zz*(B-t)
        return mp.log(mult*(mm1+mm2))/bb-mult*(mp.log(mm1)+mp.log(mm2))
    error=abs(mp.diff(residual,mp.mpf(0))-deriv)
    require(error<mp.mpf('1e-65'), 'Native direct derivative matches analytic trace-free source')
    # Correct replacement: separate spectral scale from shape, no counterterm.
    eigen=[mp.mpf('0.2'),mp.mpf('0.5'),mp.mpf('0.9')]
    d=len(eigen); trace=sum(eigen); beta_test=mp.mpf('0.7');mu_test=mp.mpf('.11')
    reverse_rel=sum(mp.log((trace/d)/e) for e in eigen)/d
    lhs=-mu_test+mp.log(trace)/beta_test-sum(mp.log(e) for e in eigen)
    rhs=d*reverse_rel+(1/beta_test-d)*mp.log(trace/d)+mp.log(d)/beta_test-mu_test
    require(abs(lhs-rhs)<mp.mpf('1e-70'), 'Exact corrected heat/logdet scale-shape decomposition')
    require(reverse_rel>0, 'Unequal positive spectrum has positive reverse relative entropy')
    return {'native_A0':mp.nstr(A,40),'native_B0':mp.nstr(B,40),
            'trace_free_heat_derivative':'0 (symbolic)',
            'trace_free_logdet_derivative':mp.nstr(deriv,40),
            'scalar_differentiation_error':mp.nstr(error,8),
            'direction_scope':'operator-space diagnostic, not an assertion that this is a supplied 42-field tangent'}


def root_checks() -> dict:
    a=Q('28.883');b0=Q('.036547');C=Q('1.69344e18');r=Q('1e-20');eps=Q('1e-22')
    q=b0+a*C*r
    selfmap=Q('3.01e-52')+q*r+a*eps
    require(q == Q('.5256632752'), 'Original unpadded source budget uses its actual Hessian defect')
    require(selfmap<r, 'Owned 1e-22 continuous source bound is a valid self-map budget')
    require(q+a*Q('.01')<1, 'Owned extra Lipschitz bound supplies uniqueness')
    require(a/(1-b0)>Q(29), 'Inverse defect .036547 is NOT the inverse Hessian norm')
    require(Q('1e-11')/Q('1e-24')==10**13, 'Claimed displacement lies beyond original root ball by 13 orders')
    require(Q('1e-7')/Q('1e-24')==10**17, 'Upper claimed displacement lies beyond original root ball by 17 orders')
    # A tiny pointwise residual plus an exact invertible base Hessian is NOT enough.
    x=s.symbols('x', real=True);epsilon=s.Rational(1,10**11)
    base=x;rest=epsilon-x+x*x
    require(s.simplify(base+rest)==x*x+epsilon, 'Smooth remainder can destroy all real roots')
    require(rest.subs(x,0)==epsilon and s.diff(base,x)==1,
            'No-root control still has tiny point residual and unit base inverse')
    return {'preconditioner_norm_bound':str(a),'inverse_defect_bound':str(b0),
            'inverse_hessian_norm_bound':float(a/(1-b0)),
            'owned_source_radius':'1e-20','owned_complete_source_sup_bound':'1e-22',
            'q_base':float(q),'self_map_radius_upper':float(selfmap),
            'new_full42_correction_evaluated':False}


def echo_checks() -> dict:
    # Exact state after a perfect echo, with an independent retained outcome copy.
    r=s.Rational(1,3)
    psi=s.Matrix([s.sqrt(1-r),0,0,s.sqrt(r)])
    rho=psi*psi.T
    rho_prog=s.Matrix(2,2,lambda i,j:sum(rho[2*i+k,2*j+k] for k in range(2)))
    X=s.Matrix([[0,1],[1,0]])
    require(rho_prog==s.diag(1-r,r), 'Retained orthogonal macro outcome tags dephase the program marginal')
    require(s.trace(X*rho_prog)==0, 'Perfect work echo does not restore program-only contrast with retained tags')
    joint=s.kronecker_product(X,X)
    contrast=s.simplify((psi.T*joint*psi)[0])
    require(s.simplify(contrast-2*s.sqrt(r*(1-r)))==0, 'Joint program/archive observable can recover global coherence')
    P0=s.diag(1,1,0,0)
    require(joint*P0-P0*joint != s.zeros(4), 'Joint coherence observable does not commute with outcome archive')
    require(s.trace(rho*rho)==1 and rho_prog.det()>0,
            'A globally pure state need not have a pure program marginal')
    P=s.Matrix([[s.Rational(1,2),s.Rational(1,2)],[s.Rational(1,2),s.Rational(1,2)]])
    U=s.eye(2)
    require(P*U.T*(s.eye(2)-P)*U*P==s.zeros(2),
            'Whole restored identity cycle has zero complementary feedback on the same cut')
    return {'program_only_contrast':'0','joint_contrast':str(contrast),
            'actual_full_writer_echo_compiled':False,
            'compulsory_Book03_projector_selected':False}


def information_checks() -> dict:
    mp.dps=80; p=(mp.sqrt(5)-1)/2; ell=mp.log(1/p)
    h=lambda r:-(r*mp.log(r)+(1-r)*mp.log(1-r))/ell
    k=lambda r:1+r-h(r)
    r0=mp.mpf(1)/4;r1=mp.mpf(3)/4;mean=(r0+r1)/2
    conditional=(k(r0)+k(r1))/2;mi=h(mean)-(h(r0)+h(r1))/2
    require(abs(conditional-k(mean)-mi)<mp.mpf('1e-70'),
            'Conditional code price = aggregated code price + site/bit mutual information')
    deriv=mp.diff(lambda t:(k(r0+t)+k(r1-t))/2,mp.mpf(0))
    require(abs(deriv+mp.log(3)/ell)<mp.mpf('1e-70'),
            'Conditional price has nonzero derivative along a fixed-mean direction')
    require(mi>0, 'Address information carries a real positive additional value')
    return {'fixed_mean_conditional_price_derivative':mp.nstr(deriv,30),
            'this_is_not_a_logdet_identity':True,
            'original_h0_and_hquarter_prices_kept_distinct':True}


def refinement_checks() -> dict:
    h,x=s.symbols('h x', positive=True)
    E=h**3*x+h**2
    require(s.simplify(E.subs(x,-1/h))==0, 'Consistency control root is exactly -1/h')
    require(E.subs(x,0)==h*h, 'Same control has O(h^2) residual at the target')
    require(s.diff(E,x)==h**3, 'Every finite Jacobian is invertible but inverse grows as h^-3')
    require(42-34==(16-10)+2, 'Eight missing coordinates are not identified by an arbitrary gauge label count')
    return {'consistency_counterexample':'E_h(x)=h^3*x+h^2; exact root=-1/h',
            'uniform_inverse_or_equivalent_stability_proven':False}


def main() -> None:
    results={
      'legendre':legendre_checks(), 'modular_heat':modular_heat_checks(),
      'root_certificate':root_checks(),'echo_archive':echo_checks(),
      'conditional_information':information_checks(),'refinement':refinement_checks()}
    payload={'status':'PASS_COMPOSITION_AUDIT_CONTROLS_NOT_GR_CLOSURE',
       'checks':len(CHECKS),'check_names':CHECKS,'results':results,
       'source_snapshot':'07a328a29843d5f21e0d5b4fec1b5ec0be923e3b',
       'new_full42_interval_root':False,'native_full_programme_constructed':False,
       'Lean_run':False,'GR_closed':False}
    print(json.dumps(payload,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
