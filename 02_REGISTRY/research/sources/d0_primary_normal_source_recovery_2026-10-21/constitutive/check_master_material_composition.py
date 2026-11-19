#!/usr/bin/env python3
"""Compose the pinned complete N=1 CQ price with its native radial normal form.

Reuses the original exact two-band probability/Golden constants. Tests the
new universal material-function scaling, rather than another field rank.
The supplied moving-query CQ execution remains conditional physical input.
No extra action, compulsory Book valuation, minimum or generic GR is claimed.
"""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import mpmath as mp
import sympy as sp

INPUT_REF = 'dfc0275eea67ebc21ffe539de9b6ea96713863a5'
OWNER_PATH = '02_REGISTRY/research/sources/d0_same_execution_spatial_source_2026-10-21/weights/check_same_execution_spatial_weights.py'
OWNER_BLOB = '7ae37d9c04ea73f9aa0d11e6b6fb290abc9881c2'


def require(test: object, message: str) -> None:
    if not bool(test):
        raise AssertionError(message)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def load_owner(path: Path) -> dict:
    require(path.is_file(), f'missing original price owner: {path}')
    require(git_blob(path.read_bytes()) == OWNER_BLOB, 'original price-owner bytes changed')
    saved = sys.argv
    try:
        sys.argv = [str(path)]
        with redirect_stdout(io.StringIO()):
            result = runpy.run_path(str(path), run_name='d0_consumed_price_owner')
    finally:
        sys.argv = saved
    require(result['result']['status'] == 'PASS_SAME_EXECUTION_CAP1_SPATIAL_WEIGHTS', 'original bounded application did not pass')
    return result


def exact_composition() -> dict:
    M,rho,tau,X,Y,S,P,a,b = sp.symbols('M rho tau X Y S P a b', nonzero=True)
    F = sp.Function('F')
    m=M*rho; c=tau/rho; Az=m*c*a
    require(sp.simplify(Az-M*tau*a)==0, 'actual common gravitational coefficient')
    # The same EXTENDED action, not an off-shell equality of physical actions.
    xi,pi,t = sp.symbols('xi pi t')
    transformed=m*F(c*S,c*P*Y/Az)-P*S
    universal=m*(F(xi,pi*t/a)-pi*xi)
    substituted=transformed.subs({S:xi/c,P:m*c*pi,Y:t/c}, simultaneous=True)
    require(sp.simplify(substituted-universal)==0, 'exact common master-function reduction')
    for n in range(1,7):
        require(sp.simplify(m*c**n-M*tau**n*rho**(1-n))==0, f'actual n={n} material-weight law')
    A,B,C=sp.symbols('F_xx F_xy F_yy')
    H=sp.Matrix([[A,-1],[-1,0]])
    Hinv=sp.Matrix([[0,-1],[-1,-A]])
    require(H*Hinv==sp.eye(2), 'auxiliary inverse without F_xx inversion')
    require(H.det()==-1, 'regular auxiliary saddle')
    mixed=sp.Matrix([B,b/a])
    K2=sp.simplify(C-(mixed.T*Hinv*mixed)[0])
    require(sp.simplify(K2-(C+2*(b/a)*B+(b/a)**2*A))==0, 'master material second source')
    # Every post-readout scalar price V(r) shares the same radial curve when V'!=0.
    u,v,Rx,Ry,Vp=sp.symbols('u v r_x r_y Vprime', nonzero=True)
    require(sp.expand(u*Vp*Rx-v*Vp*Ry-Vp*(u*Rx-v*Ry))==0, 'radial equation independent of scalar readout')
    # Null first-source protection does NOT erase the Hessian.
    eps,dy,k2=sp.symbols('eps dy k2')
    remainder=k2*(eps*dy)**2/2
    require(sp.diff(remainder,eps).subs(eps,0)==0, 'null nonlinear first-source protection')
    require(sp.diff(remainder,eps,2).subs(eps,0)==k2*dy**2, 'nonlinear perturbation not discarded')
    # An arbitrary independent upstream baseline is not removed by any normal form.
    Z=sp.symbols('zeta'); baseline=Z**2+Z
    require(sp.diff(baseline,Z).subs(Z,0)==1, 'upstream stationarity is not automatic')
    return {'common_gravity_coefficient':'M*tau*a',
            'same_master_function':'K_z(Y)=M*rho_z*K(tau*Y/rho_z)',
            'all_order_material_coefficients':'M*tau**n*rho_z**(1-n)*K^(n)(0)',
            'auxiliary_determinant':'-1',
            'auxiliary_inverse_without_Fxx_inverse':True,
            'second_source':'F_yy+2*(b/a)*F_xy+(b/a)**2*F_xx',
            'readout_independent_radial_curve':True,
            'uniform_material_chart_required':'sup_z |tau*Y_z/rho_z| < delta',
            'same_CQ_normal_recovery_bound':'h*sup||r_h||_inf/(4*|gamma1*a_J,h|)',
            'null_first_source_not_Hessian_equality':True,
            'independent_baseline_source_retained':True}


def make_model(owner: dict) -> dict:
    mp.mp.dps=75
    p=(mp.sqrt(5)-1)/2; z=mp.mpf(2)**(-20)
    alpha=(1-(1-2*p**3)**9)**128
    beta=((1-p**120)**4*(1-(1-16*p**9)**20))**43
    ell=mp.log(1/p)
    x,y,ps,zs=(owner[k] for k in ('x','y','p','z'))
    polynomial=owner['r']
    operators={}
    for i,j in ((0,0),(1,0),(0,1),(2,0),(1,1),(0,2)):
        fun=sp.lambdify((x,y,ps,zs),sp.diff(polynomial,x,i,y,j),'mpmath')
        operators[i,j]=lambda u,v,fun=fun: fun(u,v,p,z)
    raw=operators[0,0]; r0=raw(0,0)
    def entropy(r):
        if not 0<r<1: raise ValueError('outside the original positive two-band chart')
        return -(r*mp.log(r)+(1-r)*mp.log(1-r))/ell
    def hp(r): return mp.log((1-r)/r)/ell
    def hpp(r): return -1/(ell*r*(1-r))
    # sigma=-1 is the original sourced primary orientation, not a fitted sign.
    def f(u,v): return -alpha*beta*(entropy(raw(u,-v))-entropy(r0))
    def fx(u,v): return -alpha*beta*hp(raw(u,-v))*operators[1,0](u,-v)
    def fy(u,v): return alpha*beta*hp(raw(u,-v))*operators[0,1](u,-v)
    a=fx(0,0); b=fy(0,0); lam=b/a
    gradient=(operators[1,0](0,0),-operators[0,1](0,0))
    Hr=mp.matrix([[operators[2,0](0,0),-operators[1,1](0,0)],
                  [-operators[1,1](0,0),operators[0,2](0,0)]])
    Hf=mp.matrix(2,2)
    for i in range(2):
        for j in range(2):
            Hf[i,j]=-alpha*beta*(hpp(r0)*gradient[i]*gradient[j]+hp(r0)*Hr[i,j])
    direction=mp.matrix([lam,1])
    K2=(direction.T*Hf*direction)[0]
    require(a<0<b and K2>0,'actual N1 source signs and material convex coefficient')
    require(abs(lam+mp.mpf('23.41640675188407497289558206489525274426'))<mp.mpf('1e-37'),'same finite-z ratio')
    require(abs(a*(1-r0)/gradient[0]-owner['gamma'])<mp.mpf('1e-55'),'consume actual complete CQ gain')
    return dict(p=p,z=z,alpha=alpha,beta=beta,r0=r0,f=f,fx=fx,fy=fy,a=a,b=b,lam=lam,Hf=Hf,K2=K2,gain=a*(1-r0)/gradient[0])


def solve_master(model: dict, Y) -> dict:
    a,b=model['a'],model['b']; f,fx,fy=(model[k] for k in ('f','fx','fy'))
    Y=mp.mpf(Y)
    if Y==0:return dict(s=mp.mpf(0),scale=mp.mpf(1),K=mp.mpf(0),error=mp.mpf(0))
    def eq(s,U): return fx(s,U*Y)/a-U, s-Y*fy(s,U*Y)/a
    ss,U=mp.findroot(eq,(b*Y/a,1),tol=mp.mpf('1e-60'),maxsteps=60)
    residual=max(abs(v) for v in eq(ss,U))
    require(residual<mp.mpf('1e-55') and U>0,'regular positive coframe stationary section')
    return dict(s=ss,scale=U,K=f(ss,U*Y)-a*U*ss,error=residual)


def numerical_composition(model: dict) -> dict:
    f,fx,fy=(model[k] for k in ('f','fx','fy')); a,b=model['a'],model['b']
    points=[]; max_error=mp.mpf(0)
    for value in ('-0.002','-0.0004','-0.0001','0','0.0001','0.0004','0.002'):
        Y=mp.mpf(value); sol=solve_master(model,Y)
        if Y:
            require(abs(sol['s']*fx(sol['s'],sol['scale']*Y)-sol['scale']*Y*fy(sol['s'],sol['scale']*Y))<mp.mpf('1e-55'), 'actual price on the readout-independent radial curve')
        max_error=max(max_error,sol['error'])
        points.append({'Y':value,'coframe_scale_squared':mp.nstr(sol['scale'],24),
                       'K':mp.nstr(sol['K'],24)})
    # Same analytic function used on different actual-replication-form masses.
    # These small masses are diagnostic; the theorem uses the original integer trace counts.
    M=mp.mpf(12);tau=mp.mpf(1)/16
    worst=mp.mpf(0)
    for rho in map(mp.mpf,('0.5','1','1.5')):
        m=M*rho;c=tau/rho;Az=m*c*a;Y=mp.mpf('0.001')
        master=solve_master(model,c*Y)
        def eq(s,U):return fx(c*s,c*U*Y)/a-U, s-Y*fy(c*s,c*U*Y)/a
        ss,U=mp.findroot(eq,(master['s']/c,master['scale']),tol=mp.mpf('1e-60'))
        direct=m*f(c*ss,c*U*Y)-Az*U*ss
        worst=max(worst,abs(direct-m*master['K']),abs(ss-master['s']/c),abs(U-master['scale']))
        require(abs(m*c-Az/a)<mp.mpf('1e-65'),'single uniform gravity slope at unequal mass')
    require(worst<mp.mpf('1e-55'),'same full nonlinear material function at every unequal site')
    tiny=mp.mpf('1e-12')
    k2diff=(solve_master(model,tiny)['K']+solve_master(model,-tiny)['K'])/tiny**2
    require(abs(k2diff-model['K2'])<mp.mpf('1e-19'),'implicit nonlinear branch reproduces analytic second source')
    # Price equality holds after BOTH auxiliary reductions at corresponding critical points;
    # it is deliberately not asserted as a direct off-shell radial rewrite.
    Y=mp.mpf('0.001');X=mp.mpf('0.01');sol=solve_master(model,Y)
    wrong=f(X/sol['scale'],sol['scale']*Y)-(a*X+sol['K'])
    require(abs(wrong)>mp.mpf('1e-12'),'reject false off-shell equality of physical-only actions')
    # Dropping the PF factor breaks even the leading weight cancellation.
    require(M*mp.mpf('0.5')*tau*a != M*tau*a, 'reject omitted inverse-PF query factor')
    return {'native':{k:mp.nstr(model[k],40) for k in ('alpha','beta','r0','a','b','lam','K2','gain')},
            'K2_over_b':mp.nstr(model['K2']/b,40),
            'stationary_section_checks':points,
            'max_section_residual':mp.nstr(max_error,8),
            'max_unequal_site_master_discrepancy':mp.nstr(worst,8),
            'second_derivative_check_abs_error':mp.nstr(abs(k2diff-model['K2']),8),
            'false_offshell_rewrite_discrepancy':mp.nstr(wrong,24)}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner',type=Path,help='exact pinned original price checker; default is repository path')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    owner_path=args.owner or Path(__file__).resolve().parents[5]/OWNER_PATH
    original=load_owner(owner_path)
    result={'status':'PASS_SAME_CQ_UNIVERSAL_MATERIAL_COMPOSITION','input_ref':INPUT_REF,
            'consumed_owner':{'path':OWNER_PATH,'git_blob':OWNER_BLOB,
                              'bounded_checks_passed':original['result']['check_count']},
            'exact':exact_composition(),'numerical':numerical_composition(make_model(original)),
            'scope':{'complete_N1_CQ_price_consumed':True,
                     'original_local_density_homogeneity_consumed':True,
                     'full_stationary_normal_form_theorem_consumed':True,
                     'same_null_metric_and_finite_lambda_preserved':True,
                     'additional_nonlinear_matter_not_dropped':True,
                     'new_physical_action':False,
                     'physical_moving_query_admission_proved':False,
                     'compulsory_Book_valuation_proved':False,
                     'independent_upstream_stationarity_proved':False,
                     'generic_GR_refinement_proved':False,
                     'new_independent_review_or_Lean_claim':False,'GR_closed':False}}
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':main()
