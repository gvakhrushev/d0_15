#!/usr/bin/env python3
"""Exact continuation of the supplied 12-channel model; no native-action claim.
Only local SymPy algebra is executed. --mutant deliberately breaks one identity.
"""
from __future__ import annotations
import argparse
import json
from itertools import combinations
from pathlib import Path
import sympy as S


def check_eq(a, b, name):
    if isinstance(a, S.MatrixBase) or isinstance(b, S.MatrixBase):
        residual = S.Matrix(a)-S.Matrix(b)
        good = all(S.simplify(x) == 0 for x in residual)
    else:
        good = S.simplify(a-b) == 0
    if not good:
        raise ArithmeticError(name)


def frame():
    ks, labels = [], []
    for i,j in combinations(range(4),2):
        for sign in (1,-1):
            k=S.zeros(4,1); k[i]=1; k[j]=sign
            ks.append(k); labels.append((i,j,sign))
    return labels,ks


def basis():
    out=[]
    for i in range(4):
        A=S.zeros(4); A[i,i]=1; out.append(A)
    for i,j in combinations(range(4),2):
        A=S.zeros(4); A[i,j]=A[j,i]=1/S.sqrt(2); out.append(A)
    return out


def curvature_at_origin(g, coords):
    """Gaussian curvature from the complete first/second metric jets."""
    at={x:0 for x in coords}
    ev=lambda expr:S.simplify(expr.subs(at))
    g0=g.applyfunc(ev); gi=g0.inv().applyfunc(S.simplify)
    dg=[g.diff(x).applyfunc(ev) for x in coords]
    ddg=[[g.diff(x).diff(y).applyfunc(ev) for y in coords] for x in coords]
    dgi=[(-gi*a*gi).applyfunc(S.simplify) for a in dg]
    gamma={}; dgamma={}
    for r in range(2):
      for i in range(2):
       for j in range(2):
        gamma[r,i,j]=S.simplify(sum(gi[r,l]*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j])/2 for l in range(2)))
        for k in range(2):
            dgamma[k,r,i,j]=S.simplify(sum(
                dgi[k][r,l]*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j])/2
                +gi[r,l]*(ddg[k][i][l,j]+ddg[k][j][l,i]-ddg[k][l][i,j])/2
                for l in range(2)))
    component=[]
    for r in range(2):
        component.append(S.simplify(dgamma[0,r,1,1]-dgamma[1,r,0,1]
           +sum(gamma[r,0,k]*gamma[k,1,1]-gamma[r,1,k]*gamma[k,0,1] for k in range(2))))
    return S.simplify(sum(g0[0,r]*component[r] for r in range(2))/g0.det())


def run(mutant='none'):
    p=(S.sqrt(5)-1)/2; s=S.simplify(p**3); w0=S.simplify(p**2)
    check_eq(1-4*s,s*s,'golden fold distance')
    labels,ks=frame(); bs=basis(); m=12
    M=S.Matrix([[(k.T*A*k)[0] for k in ks] for A in bs])
    R=S.Matrix([[3*(k.T*A*k)[0]-S.trace(A) for A in bs] for k in ks])
    a,b=S.symbols('a b', real=True)
    pairs={(0,1):a,(2,3):a,(0,2):b,(1,3):b,(0,3):-a-b,(1,2):-a-b}
    f=S.Matrix([pairs[i,j] for i,j,_ in labels]); K=f.jacobian([a,b])
    N=S.Matrix.hstack((K[:,0]+K[:,1])/S.sqrt(3), K[:,0]-K[:,1])
    check_eq(M*N,S.zeros(10,2),'vertical kernel')
    check_eq(N.T*N,8*S.eye(2),'vertical coordinate normalization')
    top=M/(24 if mutant=='half_metric' else 12)
    forward=top.col_join(N.T/8)
    inverse=R.row_join(N)
    check_eq(forward*inverse,S.eye(12),'finite 10+2 inverse')
    check_eq(inverse*forward,S.eye(12),'complete amplitude chart')
    eig=(R.T*R).eigenvals()
    if eig!={S.Integer(12):1,S.Integer(36):9}:
        raise ArithmeticError('right inverse norm')

    # Scalar branch and exact field metric, not merely its first jet.
    v=S.symbols('v', positive=True)
    w=(1-S.sqrt(1-4*v))/2
    check_eq(w*(1-w),v,'inverse variance')
    check_eq(S.diff(w,v),1/S.sqrt(1-4*v),'inverse derivative')
    check_eq(S.diff(w,v)**2/(4*v),1/(4*v*(1-4*v)),'full Fisher factor')
    eta=s*s/8
    check_eq(1-4*(s+eta),s*s/2,'uniform inverse lower gap')
    check_eq(1-4*(s-eta),3*s*s/2,'uniform inverse upper gap')

    # Exact cotangent transformation for arbitrary nonzero local derivatives.
    ds=S.symbols('d0:12', nonzero=True, real=True)
    D=S.diag(*ds)
    lift=(S.eye(12) if mutant=='freeze_inverse' else D.inv())*inverse
    check_eq(forward*D*lift,S.eye(12),'source chart keeps moving inverse')
    for j in range(12):
        r=S.eye(12)[:,j]; t=D.inv()*r
        E=R.T*t; Ez=N.T*t
        if mutant=='erase_internal': Ez=S.zeros(2,1)
        restored=D*(M.T*E/12+N*Ez/8)
        check_eq(restored,r,'complete nonlinear source recovery')

    # Entire homogeneous fixed-metric fibre, with phases left unchanged.
    variances=s*S.ones(12,1)+f
    q=sum((variances[j]*ks[j]*ks[j].T/12 for j in range(12)),S.zeros(4))
    check_eq(q,s*S.eye(4)/2,'finite isometric two-dimensional fibre')
    check_eq(sum(variances),12*s,'fixed variance sum not fixed code cost')
    check_eq(sum(z*z for z in f),8*(a*a+a*b+b*b),'internal norm')

    # Full field source includes integration-by-parts and a moving coefficient.
    x=S.symbols('x',real=True); u=S.Function('v')(x); e=S.Function('E')(x)
    c=1/(u*(1-4*u))
    ell=e*(u/12+c*S.diff(u,x)**2/48)
    actual=S.diff(ell,u)-S.diff(S.diff(ell,S.diff(u,x)),x)
    term=S.diff(c,u)*e*S.diff(u,x)**2/48
    if mutant=='drop_gradient_term': term=0
    expected=e/12+term-S.diff(c*e*S.diff(u,x)/24,x)
    check_eq(actual,expected,'full inhomogeneous metric pullback')

    # The two-field metric and two independent curvature calculations.
    z=S.symbols('z',positive=True)
    F=lambda t:1/(t*(1-4*t))
    g=S.Matrix([[F(z+a)+F(z-a-b),F(z-a-b)],
                [F(z-a-b),F(z+b)+F(z-a-b)]])/12
    g0=g.subs({a:0,b:0,z:s}).applyfunc(S.simplify)
    check_eq(g0,S.Matrix([[2,1],[1,2]])/(12*s**3),'internal target metric')
    curvature=curvature_at_origin(g,(a,b))
    shape_curvature=(1-8*z)**2/(z*(1-4*z))
    check_eq(curvature,shape_curvature,'intrinsic versus embedded target curvature')
    K0=S.simplify(curvature.subs(z,s))
    check_eq(K0,22+17*S.sqrt(5),'golden target curvature')

    # Same variance is the genuine two-tick error, not a fitted potential.
    ww=S.symbols('ww', positive=True)
    W=S.Matrix([[S.sqrt(1-ww),-S.sqrt(ww)],
                [S.sqrt(ww),S.sqrt(1-ww)]])
    P0=S.diag(1,0); Q0=S.eye(2)-P0; U2=W*W
    two_tick=P0*U2.T*Q0*U2*P0
    check_eq(two_tick,S.diag(4*ww*(1-ww),0),'actual two-tick error')
    zz=S.symbols('zeta', nonnegative=True)
    dv=1-4*zz*s
    cubic=(dv-4*zz*a)*(dv-4*zz*b)*(dv+4*zz*(a+b))
    reduced=dv**3-16*zz**2*dv*(a*a+a*b+b*b)+64*zz**3*a*b*(a+b)
    check_eq(cubic,reduced,'complete feedback invariant polynomial')
    # Each of the three matching variances occurs four times.
    J=-4*S.log(cubic)
    HessJ=J.diff(a,2).subs({a:0,b:0})
    check_eq(HessJ,128*zz**2/dv**2,'full feedback quadratic coefficient')
    # The same internal metric is the Hessian of a two-tick information potential.
    entropy2=lambda r:r*S.log(r)+(1-r)*S.log(1-r)
    psi=sum(entropy2(4*t) for t in [z+a,z+b,z-a-b])/48
    check_eq(S.hessian(psi,(a,b)),g,'two-tick Fisher potential')
    # Variable internal fields a=epsilon*x, b=epsilon*y give an actual
    # curved four-dimensional positive metric, not just target-space curvature.
    offset=S.symbols('offset',positive=True)
    graphK=curvature_at_origin(g+offset*S.eye(2),(a,b))
    dd=z*(1-4*z)
    expectedK=(1-8*z)**2*(1+8*offset*dd)/(dd*(1+4*offset*dd)**2*(1+12*offset*dd)**2)
    check_eq(graphK,expectedK,'actual graph metric curvature')

    # Full coherent spectrum versus outcome statistics.
    wvar=S.symbols('w',positive=True)
    P=S.Matrix([[1-wvar,S.sqrt(wvar*(1-wvar))],
                [S.sqrt(wvar*(1-wvar)),wvar]])
    check_eq(P*P,P,'complete coherent projector')
    check_eq(S.trace(P),1,'both branches retained')
    gphi=S.symbols('ell',positive=True)
    # log(mu) on one channel, with uniform channel address 1/12.
    logmu=S.diag(-S.log(12)-gphi,-S.log(12)-2*gphi)
    full_D=-S.log(12)-S.trace(P*logmu)
    check_eq(full_D,gphi*(1+wvar),'coherent relative entropy equals code cost')
    # Classical code/KL/entropy identity using exact golden reference weights.
    h=-wvar*S.log(wvar)-(1-wvar)*S.log(1-wvar)
    classical=(wvar*S.log(wvar)+(1-wvar)*S.log(1-wvar))/gphi+1+wvar
    check_eq(1+wvar-classical,h/gphi,'two declared Info contracts not conflated')

    # f_vv=f_ww/d^2+2 f_w/d^3 at the golden state.
    d=s
    Cvv=2/d**3
    Dvv=1/(s*gphi*d**2)
    Hvv=-1/(s*gphi*d**2)+2/d**3
    check_eq(Cvv-Dvv,Hvv,'fixed-metric second source identity')
    check_eq(Hvv,(2*gphi-1)/(s**3*gphi),'entropy negative curvature coefficient')
    # Rigorous ell<1/2: e>8/3>phi^2, no decimal sign guess.
    if not bool(S.Rational(8,3)>(1+p)**2):
        raise ArithmeticError('logphi sign certificate')
    # Entropy concavity in variance: derivative of the positive difference.
    t=S.symbols('t',positive=True)
    difference=t/(1-t*t)-S.atanh(t)
    check_eq(S.diff(difference,t),2*t*t/(1-t*t)**2,'strict entropy concavity')

    return {
        'scope':'exact nonlinear chart of specified full 24-state record model; not native admission or GR',
        'source_rank':10, 'retained_internal_dimensions':2,
        'finite_amplitude_chart':'v=w(1-w); Q=Mv/12; xi=N^T(v-s0*1)/8',
        'inverse':'v=s0*1+R(Q-Q0)+N*xi; w=(1-sqrt(1-4v))/2',
        'homogeneous_metric_right_inverse_bound':'6*sqrt(2)/p^3 on |v-s0|<=s0^2/8',
        'full_metric_contains_gradient_term':True,
        'homogeneous_fixed_metric_fibre':'v12=v34=s0+a, v13=v24=s0+b, v14=v23=s0-a-b; both signs',
        'internal_target_metric_at_golden':'[[2,1],[1,2]]/(12*p^9)',
        'internal_target_Gaussian_curvature':str(K0),
        'coherent_entropy':'log(12) for rho=P/12; independent of amplitudes and phases',
        'coherent_relative_entropy_over_logphi':'1+mean(w) relative to the explicitly diagonal golden reference',
        'conditional_classical_KL_quadratic':'(a*a+a*b+b*b)/(3*p^9*log(phi))',
        'conditional_code_cost_quadratic':'2*(a*a+a*b+b*b)/(3*p^9)',
        'conditional_gain_net_action_quadratic':'(2*log(phi)-1)*(a*a+a*b+b*b)/(3*p^9*log(phi))',
        'fixed_metric_fixed_minimum_code_budget':'only the golden amplitude on the lower branch',
        'two_tick_error':'4*v for each channel; full carrier keeps twelve zero modes',
        'full_feedback_on_fixed_metric':'-4*log(d^3-16*z^2*d*(a^2+a*b+b^2)+64*z^3*a*b*(a+b)); d=1-4*z*p^3',
        'full_feedback_quadratic':'64*z^2*(a^2+a*b+b^2)/(1-4*z*p^3)^2',
        'internal_metric_potential':'Hess[sum(r_i*log(r_i)+(1-r_i)*log(1-r_i))/48], r_i=4*v_i',
        'curved_positive_graph_scalar':'2*K_target*(1+8*x)/((1+4*x)^2*(1+12*x)^2); x=p^12/(2*epsilon^2)',
        'physical_Info_selected':False, 'nonlinear_spacetime_GR_closed':False,
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--mutant',choices=['none','half_metric','freeze_inverse','erase_internal','drop_gradient_term'],default='none')
    args=ap.parse_args()
    out=run(args.mutant)
    text=json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(text,encoding='utf8')
    print(text,end='')

if __name__=='__main__':main()
