#!/usr/bin/env python3
"""Narrow Decimal checks of the new weighted Ward/coordinate interface.

Uses the actual N=1 polynomial and readiness factors. This is an authored
high-precision diagnostic, not interval arithmetic or a finite-native replay.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import argparse
import json

getcontext().prec = 90
ZERO, ONE, TWO = D(0), D(1), D(2)
p = (D(5).sqrt()-ONE)/TWO
z = TWO**(-20)
lnphi = (ONE/p).ln()
alpha = (ONE-(ONE-TWO*p**3)**9)**128
beta = ((ONE-p**120)**4*(ONE-(ONE-D(16)*p**9)**20))**43
ready = alpha*beta
TOL = D('1e-69')
checks = []


def require(condition, label):
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def raw(x, y):
    E=p*p*(ONE+x)
    ell=D(4)*E*(ONE-E)
    ellx=D(4)*p*p*(ONE-TWO*E)
    ellxx=-D(8)*p**4
    bb=p+p*p*y
    B=D(4)*bb*bb*(ONE-bb*bb)
    By=D(8)*p*p*bb*(ONE-TWO*bb*bb)
    Byy=D(8)*p**4*(ONE-D(6)*bb*bb)
    A=ell+(ONE-ell)*B
    Ax=ellx*(ONE-B)
    Ay=(ONE-ell)*By
    Axx=ellxx*(ONE-B)
    Axy=-ellx*By
    Ayy=(ONE-ell)*Byy
    r=z*(A+B)-z*z*A*B
    rx=z*(ONE-z*B)*Ax
    ry=z*((ONE-z*A)*By+(ONE-z*B)*Ay)
    rxx=z*(ONE-z*B)*Axx
    rxy=z*(ONE-z*B)*Axy-z*z*By*Ax
    ryy=z*((ONE-z*A)*Byy+(ONE-z*B)*Ayy-TWO*z*By*Ay)
    return r,rx,ry,rxx,rxy,ryy


def entropy(r):
    return -(r*r.ln()+(ONE-r)*(ONE-r).ln())/lnphi


r0=raw(ZERO,ZERO)[0]
h0=entropy(r0)


def price(x,y):
    # Actual source orientation: F(x,y)=-alpha beta h(r(x,-y)) plus baseline.
    r,rx,ry,rxx,rxy,ryy=raw(x,-y)
    hp=((ONE-r)/r).ln()/lnphi
    hpp=-ONE/(lnphi*r*(ONE-r))
    return dict(F=-ready*(entropy(r)-h0),
                fx=-ready*hp*rx,
                fy=ready*hp*ry,
                fxx=-ready*(hpp*rx*rx+hp*rxx),
                fxy=ready*(hpp*rx*ry+hp*rxy),
                fyy=-ready*(hpp*ry*ry+hp*ryy))


base=price(ZERO,ZERO)
a,b=base['fx'],base['fy']


def solve2(j11,j12,j21,j22,r1,r2):
    det=j11*j22-j12*j21
    return (r1*j22-j12*r2)/det, (j11*r2-r1*j21)/det


def section(t):
    s=(b/a)*t
    U=ONE
    for _ in range(40):
        v=price(s,U*t)
        e1=v['fx']/a-U
        e2=s-t*v['fy']/a
        if max(abs(e1),abs(e2)) < D('1e-78'):
            break
        j11=v['fxx']/a
        j12=v['fxy']*t/a-ONE
        j21=ONE-t*v['fxy']/a
        j22=-t*t*v['fyy']/a
        ds,dU=solve2(j11,j12,j21,j22,-e1,-e2)
        s+=ds
        U+=dU
    else:
        raise AssertionError('stationary master Newton solve')
    v=price(s,U*t)
    j11=v['fxx']/a
    j12=v['fxy']*t/a-ONE
    j21=ONE-t*v['fxy']/a
    j22=-t*t*v['fyy']/a
    sp,Up=solve2(j11,j12,j21,j22,
                 -v['fxy']*U/a, (v['fy']+t*v['fyy']*U)/a)
    y=U*t
    yp=U+t*Up
    K=v['F']-a*U*s
    Kp=U*v['fy']
    Kpp=Up*v['fy']+U*(v['fxy']*sp+v['fyy']*yp)
    return dict(s=s,U=U,sp=sp,Up=Up,y=y,yp=yp,K=K,Kp=Kp,Kpp=Kpp,
                residual=max(abs(v['fx']/a-U),abs(s-t*v['fy']/a)),**v)


def run():
    require(a<0<b,'actual complete N1 slope signs')
    require(base['fxx']>0 and base['fxy']<0,'reflected native Hessian signs')
    Uprime0=(base['fxy']+(b/a)*base['fxx'])/a
    require(Uprime0>0,'nonzero original-to-reduced scale derivative')
    require(abs(section(ZERO)['Up']-Uprime0)<TOL,'auxiliary derivative agrees at zero')
    require(abs(b/a+D('23.41640675188407497289558206489525274426'))<D('1e-37'),
            'same finite Golden coupling')

    tau=D(1)/16
    q0=D('0.001')
    C=tau*q0
    rows=[]
    maxward=ZERO
    maxinv=ZERO
    for rr in ('0.5','1','1.5','2.25','3'):
        rho=D(rr)
        t=C/rho
        s=section(t)
        require(s['residual']<TOL,'actual weighted auxiliary section at rho='+rr)
        require(abs(s['s'])<D(1)/4 and abs(s['y'])<TWO**(-12),
                'common original operand chart at rho='+rr)
        # Differentiate P=F-s F_x along the independently solved branch.
        Pprime=(s['fy']*s['yp']-s['s']*(s['fxx']*s['sp']+s['fxy']*s['yp']))/s['yp']
        dy_dlogrho=-t*s['yp']
        ward=Pprime*dy_dlogrho+s['y']*s['fy']
        invariant=rho*s['y']/s['fx']
        inv_error=invariant-C/a
        maxward=max(maxward,abs(ward))
        maxinv=max(maxinv,abs(inv_error))
        require(abs(ward)<TOL,'weighted Ward with moving PF denominator at rho='+rr)
        require(abs(inv_error)<TOL,'rho*y/Fx invariant at rho='+rr)
        require(abs(Pprime*dy_dlogrho)>D('1e-12'),
                'dropping the weighted Ward term fails at rho='+rr)
        rows.append({k:str(s[k]) for k in ('s','y','U','Kp')} | {'rho':rr})

    # Positive dust FLRW, transformed to a prescribed time-varying PF profile.
    T=D('1.3')
    xpos=D('0.7')
    rho=ONE+T/3
    rhodot=ONE/3
    t=C/rho
    s=section(t)
    tdot=-t*rhodot/rho
    Kdot=s['Kpp']*tdot
    H=-q0*s['Kp']/a
    k=D(3)*H/4
    kdot=-D(3)*q0*Kdot/(D(4)*a)
    scale=T**(D(4)/3)
    gtt=ONE-scale*(kdot*xpos)**2
    gtx=-scale*kdot*k*xpos
    gxx=-scale*k*k
    det2=gtt*gxx-gtx*gtx
    invtt=gxx/det2
    invtx=-gtx/det2
    invxx=gtt/det2
    require(abs(invtt-ONE)<TOL,'pulled-back clock norm stays one')
    require(abs(invtx+kdot*xpos/k)<TOL,'induced contravariant shift retained')
    require(abs(gtt*invtx+gtx*invxx)<TOL,'actual metric inverse off-diagonal')
    evol=(-det2*scale*scale).sqrt()
    dust=D(4)/(D(3)*T*T)
    require(abs(evol*dust-H)<TOL,'prescribed positive mass-volume density')
    require(abs(q0*invtt-q0)<TOL,'constant reduced material norm')
    current_residual=Kdot-s['Kp']*kdot/k
    require(abs(current_residual)<TOL,'full scalar current including induced shift')
    require(abs(Kdot)>D('1e-10'),'dropping induced shift fails scalar equation')
    # Einstein tensor here is the tensorial pullback of the known dust FLRW tensor.
    metric_residual=a*evol*dust+s['Kp']*q0
    require(abs(metric_residual)<TOL,'pulled-back Einstein source coefficient')
    orig_evol=evol/(s['U']*s['U'])
    require(abs(s['fy']/(s['fx']*orig_evol)-s['Kp']/(a*evol))<TOL,
            'original Palatini and reduced metric source agree')
    ldot=s['Up']*tdot/s['U']
    require(abs(ldot)>D('1e-5'),'original nonnull coframe has nonzero determined torsion')

    # Sign check for the standard conformal identity: g=Minkowski, U=T^2.
    lp=TWO/T
    lpp=-TWO/(T*T)
    transformed00=-lpp+lp*lp/TWO+lpp+lp*lp/4
    transformedii=-lpp-lp*lp/4
    require(abs(transformed00-D(3)/(T*T))<TOL,'conformal Einstein 00 sign')
    require(abs(transformedii-ONE/(T*T))<TOL,'conformal Einstein spatial sign')

    return dict(status='PASS_WEIGHTED_WARD_AND_MASS_COORDINATE_CHECK',
                arithmetic='Decimal precision 90; diagnostic, not interval certificate',
                source_commit='086fab99d8aaed7f712e9a3d2858c516b61901fc',
                actual_native={k:str(v) for k,v in dict(alpha=alpha,beta=beta,r0=r0,
                                     a=a,b=b,ratio=b/a,Uprime0=Uprime0).items()},
                weighted_branch_samples=rows,
                max_abs_weighted_Ward_residual=str(maxward),
                max_abs_invariant_error=str(maxinv),
                time_dependent_coordinate_check={
                    'target_rho':'1+T/3','T':str(T),'q0':str(q0),'tau':str(tau),
                    'mass_density':str(H),'spatial_Jacobian':str(k),
                    'induced_inverse_metric_gTx':str(invtx),
                    'full_scalar_residual':str(current_residual),
                    'incorrect_zero_shift_residual':str(Kdot),
                    'original_log_scale_derivative':str(ldot)},
                checks=checks,
                scope={'actual_N1_master_law_used':True,
                       'arbitrary_prescribed_rho_theorem_is_analytical':True,
                       'FLRW_is_an_independent_diagnostic':True,
                       'finite_native_source_replay':False,
                       'continuum_Ward_claimed_on_finite_lattice':False,
                       'original_nonnull_metric_declared_GR':False,
                       'physical_readout_admission':False,'GR_closed':False})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=run()
    data=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.write_text(data,encoding='utf-8')
    print(result['status'])
    print('weighted Ward residual:',result['max_abs_weighted_Ward_residual'])
    print('rho*y/Fx invariant error:',result['max_abs_invariant_error'])
    print('incorrect zero-shift scalar residual:',
          result['time_dependent_coordinate_check']['incorrect_zero_shift_residual'])
