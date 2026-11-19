#!/usr/bin/env python3
"""Narrow checks of logarithmic preparation elimination.

No repository data are written, downloaded, or silently substituted. The
four-dimensional channel is an explicit test of the analytical theorem,
NOT a rerun of the original full128/4096-dimensional D0 calculation.
Run normally or with -O; checks use explicit exceptions, never assert.
"""
from __future__ import annotations
import json
from typing import Any
import sympy as sp
import mpmath as mp

checks: list[str] = []

def require(name: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError('FAILED: ' + name)
    checks.append(name)


def exact_checks() -> dict[str, Any]:
    p = (sp.sqrt(5) - 1) / 2
    eq = lambda x: sp.simplify(x) == 0
    require('golden_normalization', eq(p+p*p-1))
    require('mixture_new_mass', eq(p**2-p**4-p**3))
    require('native_stiffness', eq(p**3*p**2/256-p**5/256))
    require('native_value_coefficient', eq(sp.log(1/p)/(8*(p**5/256))-32*sp.log(1/p)/p**5))
    require('native_source_coefficient', eq(sp.log(1/p)/(4*(p**5/256))-64*sp.log(1/p)/p**5))
    x, eta = sp.symbols('x eta', positive=True)
    r = sp.symbols('r', real=True)
    f = -x*x*sp.log(x*x+eta)
    f2 = -2*sp.log(x*x+eta)-10*x*x/(x*x+eta)+4*x**4/(x*x+eta)**2
    require('regularized_entropy_second_derivative', eq(sp.diff(f,x,2)-f2))
    require('strong_convexity_remainder_factor', eq(6-10*r+4*r*r-(1-r)*(6-4*r)))
    require('radial_slope_lower_bound', eq(6-2*r-((1-r)*2+4)))
    # A full two-component material tangent; the local J T term is essential.
    c0 = sp.Matrix([sp.sqrt(p),p,0,0])
    tangent = sp.Matrix([0,0,1,0])
    J = sp.zeros(4); J[2,1]=1; J[1,2]=-1
    require('native_mask_norm', eq((c0.T*c0)[0]-1))
    require('horizontal_preparation_tangent', eq((c0.T*J*c0)[0]))
    require('parity_stiffness_norm', eq((J*c0).dot(J*c0)-p*p))
    effects = [sp.Rational(3,5)*sp.eye(4),sp.Rational(2,5)*sp.eye(4)]
    naive = 0; correct = 0
    for i,E in enumerate(effects):
        a=(c0.T*E*c0)[0]
        first=2*(tangent.T*E*J*c0)[0]
        second=2*(c0.T*E*J*tangent)[0]
        require('complete_mixed_material_cancellation_'+str(i),eq(first+second))
        naive += -p*p*first*sp.log(a)/sp.log(1/p)
        correct += -p*p*(first+second)*sp.log(a)/sp.log(1/p)
    require('full_M_vanishes_on_scalar_instrument',eq(correct))
    require('omitted_JT_creates_false_source',not eq(naive))
    # Parity-preserving effects noncommuting with the preparation/generator.
    a,k,d,e = sp.symbols('a k d e', real=True)
    E0=sp.diag(a,a,d,e); E0[2,3]=k; E0[3,2]=k
    t_remote=sp.Matrix([0,0,0,1])
    mixed=2*(t_remote.T*E0*J*c0)[0]+2*(c0.T*E0*J*t_remote)[0]
    require('remote_material_mixed_coefficient',eq(mixed-2*p*k))
    parity=sp.diag(-1,-1,1,1)
    require('effect_parity',E0*parity==parity*E0)
    require('generator_reverses_parity',J*parity==-parity*J)
    # The native measure normalization is an algebraic identity, not a limit.
    S=sp.symbols('S', positive=True)
    source=sp.symbols('source', real=True)
    require('finite_mesh_density_normalization',eq(S*(source/S)**2-source**2/S))
    return {'native_nu':'p^5/256','extra_mixed_term_required':True,
            'parameter_source':'-2 p^3 k log_phi(a/(1-a))',
            'geometric_remainder':'O(||matter||^2/log(1/||matter||))',
            'scalar_spectral_bound':'f_eta_second >= -2 log(epsilon^2+eta)-6'}


def numerical_checks() -> list[dict[str, Any]]:
    mp.mp.dps = 300
    p=(mp.sqrt(5)-1)/2; lp=mp.log(1/p)
    def parameters(g):
        return mp.mpf(3)/5+g/20,mp.mpf(2)/25+g/100,mp.mpf(1)/2,mp.mpf(2)/5
    def eigenvalues(g,t,a):
        q,k,d,e=parameters(g)
        b=mp.sqrt(p*p-t*t)
        u=q*(p+b*b)+e*t*t
        v=q*(p+b*b*mp.cos(a)**2)+d*b*b*mp.sin(a)**2+2*k*b*mp.sin(a)*t+e*t*t
        cross=q*(p+b*b*mp.cos(a))+k*b*mp.sin(a)*t+e*t*t
        overlap=p+b*b*mp.cos(a)+t*t
        out=[]
        for uu,vv,ww in [(u,v,cross),(1-u,1-v,overlap-cross)]:
            trace=p*uu+p*p*vv
            det=p**3*(uu*vv-ww*ww)
            # At exact a=0, the Gram has its proven zero eigenvalue.
            if a==0:
                low=mp.mpf(0)
            else:
                if det<0: raise RuntimeError('Negative test Gram determinant')
                low=2*det/(trace+mp.sqrt(trace*trace-4*det))
            out.extend([trace-low,low])
        return out
    def entropy(g,t,a):
        return -mp.fsum(v*mp.log(v)/lp for v in eigenvalues(g,t,a) if v!=0)
    def s1(g):
        q,k,_,_=parameters(g)
        return -2*p**3*k*mp.log(q/(1-q))/lp
    nu=p**5; g=mp.mpf('0.2'); s=s1(g); sg=mp.diff(s1,g)
    C=lp/(8*nu)
    target_a=-2*C*s; target_value=-C*s*s
    target_matter=-2*C*s*s; target_geometry=-2*C*s*sg
    q,k,d,e=parameters(g)
    H0=p**6*d-p**4*q; H1=p**6*(1-d)-p**4*(1-q)
    born0=nu*d; born1=nu*(1-d)
    beta_regular=(nu-H0*mp.log(q)-H1*mp.log(1-q)
                  -born0*mp.log(born0)-born1*mp.log(born1))/lp
    entropy_log_coefficient=nu/lp
    c_shift=(beta_regular/entropy_log_coefficient-1)/2
    require('old_new_mass_cancellation',abs(H0+H1+nu)<mp.mpf('1e-150'))
    report=[]
    previous_error=None
    for exponent in [3,6,12,24,48]:
        t=mp.power(10,-exponent); L=mp.log(1/t)
        expected=target_a*t/L
        derivative=lambda a: mp.diff(lambda aa:entropy(g,t,aa),a)
        # Secant uses the full analytic two-leaf Gram entropy, not its model.
        root=mp.findroot(derivative,(expected/2,expected),tol=mp.mpf('1e-250'),maxsteps=80)
        lambert_argument=s*t*mp.exp(-c_shift)/(4*entropy_log_coefficient)
        lambert_angle=s*t/(4*entropy_log_coefficient*mp.lambertw(lambert_argument,-1))
        require('lambert_improves_leading_log_'+str(exponent),
                abs(root/lambert_angle-1)<abs(root/expected-1))
        require('lambert_relative_accuracy_'+str(exponent),
                abs(root/lambert_angle-1)<100*t*t)
        require('positive_stationary_preparation_'+str(exponent),root>0)
        require('stationary_residual_'+str(exponent),abs(derivative(root))<mp.mpf('1e-230'))
        require('strict_local_curvature_'+str(exponent),mp.diff(derivative,root)>0)
        base=entropy(g,t,0); opt=entropy(g,t,root)
        dy=mp.diff(lambda gg:entropy(gg,t,root),g)-mp.diff(lambda gg:entropy(gg,t,0),g)
        dt=mp.diff(lambda tt:entropy(g,tt,root),t)-mp.diff(lambda tt:entropy(g,tt,0),t)
        require('full_value_decreases_'+str(exponent),opt<base)
        require('full_geometry_source_sign_'+str(exponent),dy<0)
        require('full_matter_source_sign_'+str(exponent),dt<0)
        require('complete_probability_mass_'+str(exponent),abs(mp.fsum(eigenvalues(g,t,root))-1)<mp.mpf('1e-150'))
        ratios=[root/expected,(opt-base)*L/(t*t)/target_value,dy*L/(t*t)/target_geometry,dt*L/t/target_matter]
        error=max(abs(x-1) for x in ratios)
        if previous_error is not None:
            require('asymptotic_error_decreases_'+str(exponent),error<previous_error)
        previous_error=error
        report.append({'matter_exponent':exponent,'angle_ratio':mp.nstr(ratios[0],18),
                       'value_ratio':mp.nstr(ratios[1],18),'geometry_source_ratio':mp.nstr(ratios[2],18),
                       'matter_source_ratio':mp.nstr(ratios[3],18),
                       'lambert_angle_relative_error':mp.nstr(abs(root/lambert_angle-1),8)})
    require('final_angle_relative_error',abs(ratios[0]-1)<mp.mpf('0.08'))
    require('final_value_relative_error',abs(ratios[1]-1)<mp.mpf('0.08'))
    require('final_geometry_source_relative_error',abs(ratios[2]-1)<mp.mpf('0.08'))
    require('final_matter_source_relative_error',abs(ratios[3]-1)<mp.mpf('0.08'))
    # Simultaneous inversion leaves the true whole record entropy unchanged.
    for t,a in [('0.03','0.02'),('0.1','-0.07')]:
        t=mp.mpf(t); a=mp.mpf(a)
        require('joint_parity_'+str(t),abs(entropy(g,t,a)-entropy(g,-t,-a))<mp.mpf('1e-150'))
    # Geometry affects the source: treating M as a constant would be wrong.
    require('nonzero_geometry_derivative_of_M',abs(sg)>mp.mpf('1e-3'))
    # Entire old-support spectrum stays faithful in this controlled example.
    for gg in [-mp.mpf('0.5'),mp.mpf('0.5')]:
        q,k,d,e=parameters(gg)
        low=(d+e-mp.sqrt((d-e)**2+4*k*k))/2
        high=(d+e+mp.sqrt((d-e)**2+4*k*k))/2
        require('strict_effect_'+str(gg),0<q<1 and 0<low<high<1)
    return report


def main() -> None:
    exact=exact_checks(); numerical=numerical_checks()
    result={'status':'PASS','checks':len(checks),'groups':['exact identities and full material source','full-record envelope and source asymptotics'],
            'exact':exact,'numerical_fixture':{'data_dimension':4,'oldRIGHT_dimension':1,'leaves':2,
            'precision_decimal_digits':300,'original_D0_spectral_replay':False,'values':numerical},
            'scope':{'analytic_proof_separate_from_finite_checks':True,'independent_review_performed':False,
                     'refinement_uniformity_proved':False,'Book_price_selected':False,'GR_closed':False},
            'check_names':checks}
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()
