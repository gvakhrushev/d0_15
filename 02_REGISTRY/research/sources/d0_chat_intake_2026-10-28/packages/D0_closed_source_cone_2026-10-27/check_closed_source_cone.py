#!/usr/bin/env python3
"""D0 #334: whole-query source cone; no unconditional GR or native admission claim."""
from __future__ import annotations
import itertools, json, platform
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
import sympy as s
mp.mp.dps=170
CHECKS=0

def require(ok,msg):
    global CHECKS
    CHECKS+=1
    if not bool(ok): raise ArithmeticError(msg)
def near(a,b,msg,tol='1e-115'):
    require(abs(a-b)<=mp.mpf(tol)*max(1,abs(a),abs(b)),msg)
p,x,y,z=s.symbols('p x y z',real=True)
z0=s.Rational(1,2**20)
E=p*p*(1+x); u=p+p*p*y
ell=4*E*(1-E); bb=4*u*u*(1-u*u); aa=ell+(1-ell)*bb
R=s.rem(s.expand(1-(1-z*bb)*(1-z*aa)),p*p+p-1,p)
r0e=R.subs({x:0,y:0,z:z0})
rfe=s.diff(R,x).subs({x:0,y:0,z:z0}); rqe=s.diff(R,y).subs({x:0,y:0,z:z0})
def pair(expr):
    cp=s.Poly(s.rem(s.expand(expr),p*p+p-1,p),p)
    return Q(cp.nth(0)),Q(cp.nth(1))
def mul(a,b):
    a0,a1=a;b0,b1=b
    return a0*b0+a1*b1,a0*b1+a1*b0-a1*b1
def power(n):
    out=(Q(1),Q(0));base=(Q(0),Q(1))
    while n:
        if n&1:out=mul(out,base)
        base=mul(base,base);n//=2
    return out
lo,hi=Q(0),Q(1)
for _ in range(300):
    mid=(lo+hi)/2
    if mid*mid+mid-1<0:lo=mid
    else:hi=mid
def bounds(v):
    a,b=v
    return (a+b*lo,a+b*hi) if b>=0 else (a+b*hi,a+b*lo)

# DIFFERENT full queries, not multiple implementations of the same report.
base=s.Poly(s.expand(R.subs({x:x/64,y:-y/64,z:z0})),x,y)
coeffs={ij:pair(c) for ij,c in base.terms()}
require(len(coeffs)==27,'whole original 3x9 polynomial retained')
rows_all=[];table_controls=[]
for m in range(6):
    cm={ij:mul(c,power(m*ij[1])) for ij,c in coeffs.items()};rows=[]
    for signs in itertools.product((-1,1),repeat=10):
        ps=(1,signs[0],signs[0]*signs[1]);pt=[1]
        for sg in signs[2:]:pt.append(pt[-1]*sg)
        v=[Q(0),Q(0)]
        for (i,j),c in cm.items():
            w=ps[i]*pt[j];v[0]+=w*c[0];v[1]+=w*c[1]
        v=tuple(v);bl,bu=bounds(v)
        require(0<bl<=bu<1,'strict positive complete branch and complement')
        rows.append(v)
    require(tuple(sum(v[j] for v in rows)/1024 for j in range(2))==pair(r0e),'actual null baseline')
    sm,tm=Q(2,7),Q(-3,11);average=[Q(0),Q(0)]
    for signs,v in zip(itertools.product((-1,1),repeat=10),rows):
        w=Q(1)
        for k,sg in enumerate(signs):w*=(1+sg*(sm if k<2 else tm))/2
        average[0]+=w*v[0];average[1]+=w*v[1]
    target=pair(R.subs({x:s.Rational(sm.numerator,sm.denominator)/64,y:-p**m*s.Rational(tm.numerator,tm.denominator)/64,z:z0}))
    require(tuple(average)==target,'exact complete nonlinear sign-table law')
    rows_all+=rows;table_controls.append({'query_index':m,'retained_sign_words':len(rows)})
D=max(c.denominator for row in rows_all for c in row)
require(D&(D-1)==0,'common dyadic denominator')
original=[(int(D*a),int(D*b)) for a,b in rows_all]
transformed=original+[(D-a,-b) for a,b in original];depth=0
while any(min(v)<0 for v in transformed):
    transformed=[(a+b,a) for a,b in transformed];depth+=1
    require(depth<300,'common prefix positivity search terminates')
for old,new in zip(original,transformed[:len(original)]):
    require(mul(power(depth),new)==old,'integer prefix threshold reproduces true probability')

# Exact derivative with factored readiness squared, stable at arbitrarily small alpha.
a,r,zz,ss=s.symbols('a r z s',positive=True)
d=lambda q:1-4*zz*q*(1-q)
jp=lambda q:4*zz*(1-2*q)/d(q)
kappa=ss*a*(jp(a*r)-jp(a*(1-r)))
stable=8*ss*zz*a*a*(1-2*r)*(1-2*zz+2*a*zz-4*a*a*r*(1-r)*zz)/(d(a*r)*d(a*(1-r)))
require(s.cancel(kappa-stable)==0,'factored full three-status derivative')
t=s.symbols('t',real=True)
require(s.cancel(s.diff(jp(t),t)+8*zz*(1-2*zz+4*zz*t*(1-t))/d(t)**2)==0,'strict curvature formula')
for M in (0,1,2,7,20):
    v=(Q(0),Q(0))
    for m in range(M+1):pm=power(m+2);v=(v[0]+pm[0],v[1]+pm[1])
    tail=power(M+1)
    require((v[0]+tail[0],v[1]+tail[1])==(1,0),'all Golden cylinders and overflow retained')
require(s.rem(s.expand((1-p*p)*2*p-(1-p**3)),p*p+p-1,p)==0,'dilute coefficient identity')
pp=(mp.sqrt(5)-1)/2;zeta=mp.mpf(2)**-20;spectator=128
# Evaluate exact coefficients only at runtime; avoid float literals.
Rfn=s.lambdify((x,y),R.subs(z,z0),modules='mpmath',cse=True)
# The lambdified expressions still have symbol p; use a three-argument function.
R3=s.lambdify((p,x,y),R.subs(z,z0),modules='mpmath',cse=True)
Rx3=s.lambdify((p,x,y),s.diff(R,x).subs(z,z0),modules='mpmath',cse=True)
Ry3=s.lambdify((p,x,y),s.diff(R,y).subs(z,z0),modules='mpmath',cse=True)
Rfn=lambda x,y:R3(pp,x,y)
Rx=lambda x,y:Rx3(pp,x,y)
Ry=lambda x,y:Ry3(pp,x,y)
r0=Rfn(0,0);rf=Rx(0,0);rq=Ry(0,0);lam0=-rq/rf

def dd(q):return 1-4*zeta*q*(1-q)
def k(a,r):
    return 8*spectator*zeta*a*a*(1-2*r)*(1-2*zeta+2*a*zeta-4*a*a*r*(1-r)*zeta)/(dd(a*r)*dd(a*(1-r)))
def j(q):return -mp.log1p(-4*zeta*q*(1-q))
def phi(a,r):return spectator*(j(1-a)+j(a*(1-r))+j(a*r))
def eff(M,a):
    ws=[k(a*pp**(m+2),r0) for m in range(M+1)];ds=mp.fsum(ws)
    return lam0*mp.fsum(w*pp**m for m,w in enumerate(ws))/ds,ds
coin=(2*pp**3)**94;Cratio=1/((1-zeta)*(1-2*zeta));ensembles=[]
for ready in (mp.mpf(1),mp.mpf(2)/5,coin):
    ref,_=eff(150,ready);vals=[]
    for M in (0,2,6,12,24,48):
        la,ds=eff(M,ready);bound=abs(lam0)*Cratio*pp**(2*M+1)
        require(abs(la-ref)<=bound,'analytic infinite-source tail estimate')
        require(lam0-mp.mpf('1e-140')<=la<0,'positive gravitational source cone')
        vals.append({'M':M,'lambda_M':mp.nstr(la,45),'error_against_M150':mp.nstr(abs(la-ref),12),'proved_tail_bound':mp.nstr(bound,12)})
    ratio=ref/lam0
    require((1-zeta)*(1-2*zeta)/(2*pp)<=ratio<=Cratio/(2*pp),'nonzero all-query limiting coefficient')
    ensembles.append({'common_ready_factor':mp.nstr(ready,35),'lambda_M150':mp.nstr(ref,50),'finite_depths':vals})

Fv=[mp.mpf(2)/7,-mp.mpf(3)/11,mp.mpf(5)/13,mp.mpf(1)/9]
Qv=[mp.mpf(3)/8,mp.mpf(1)/10,-mp.mpf(2)/9,mp.mpf(4)/15]
rhos=[mp.mpf(1)/2,mp.mpf(3)/4,mp.mpf(5)/4,mp.mpf(3)/2];vol=mp.mpf(1)/4
near(vol*sum(rhos),1,'actual unequal spatial weights')
M=6;ready=mp.mpf(2)/5;eps=mp.mpf(1)/64
la,ds=eff(M,ready);gain=eps*rf*ds
full_null=mp.fsum(k(ready*pp**(m+2),r0)*eps*vol*mp.fsum(rf*Fv[i]-pp**m*rq*Qv[i] for i in range(4)) for m in range(M+1))
expected=gain*vol*mp.fsum(Fv[i]+la*Qv[i] for i in range(4))
near(full_null,expected,'exact complete all-query null covector')
blocks=[]
for m in range(4):
    aj=ready*pp**(m+2);rm=mp.mpf(1)/(7*(1+m))
    blocks += [1-4*zeta*q*(1-q) for q in (1-aj,aj*(1-rm),aj*rm)]
near(-spectator*mp.log(mp.det(mp.diag(blocks))),mp.fsum(phi(ready*pp**(m+2),mp.mpf(1)/(7*(1+m))) for m in range(4)),
     'whole direct-sum logdet with every failure block')
Fs=[mp.mpf(1)/7,-mp.mpf(1)/9,mp.mpf(2)/11,mp.mpf(1)/13]
Qs=[mp.mpf(1)/17,mp.mpf(2)/19,-mp.mpf(1)/23,mp.mpf(1)/29]
def rbar(m,ee,tangent=mp.mpf(0)):
    return vol*mp.fsum(rhos[i]*Rfn(ee*(Fs[i]+tangent*Fv[i])/rhos[i],-ee*pp**m*(Qs[i]+tangent*Qv[i])/rhos[i]) for i in range(4))
def total(ee,tangent=mp.mpf(0)):
    return mp.fsum(phi(ready*pp**(m+2),rbar(m,ee,tangent)) for m in range(M+1))
source_target=vol*mp.fsum(Fv[i]+la*Qv[i] for i in range(4));controls=[]
for exponent in (4,6,8,10):
    ee=mp.mpf(2)**-exponent;gam=ee*rf*ds
    actual=mp.fsum(k(ready*pp**(m+2),rbar(m,ee))*ee*vol*mp.fsum(
      Rx(ee*Fs[i]/rhos[i],-ee*pp**m*Qs[i]/rhos[i])*Fv[i]
      -pp**m*Ry(ee*Fs[i]/rhos[i],-ee*pp**m*Qs[i]/rhos[i])*Qv[i] for i in range(4)) for m in range(M+1))/gam
    numerical=mp.diff(lambda tt:total(ee,tt),0)/gam
    near(actual,numerical,'entire nonlinear multireport price derivative')
    err=abs(actual-source_target)
    controls.append({'eps':f'2^-{exponent}','source_error':mp.nstr(err,28),'error_over_eps':mp.nstr(err/ee,28)})
require(all(mp.mpf(controls[i+1]['source_error'])<mp.mpf(controls[i]['source_error']) for i in range(3)),'computed source residual decreases')
# Exact substitution into the owned full all40 reduction, not a full replay.
h,xx,yy,lam,en,A2,B2,A3,B3=s.symbols('h xx yy lambda E A2 B2 A3 B3',nonzero=True,real=True)
H=-lam*en*(xx*xx+yy*yy)+A2*(xx*xx-yy*yy)+2*B2*xx*yy+A3*(xx**3-3*xx*yy*yy)+B3*(3*xx*xx*yy-yy**3)
lap=s.expand((H.subs(xx,xx+h)+H.subs(xx,xx-h)+H.subs(yy,yy+h)+H.subs(yy,yy-h)-4*H)/h**2)
require(s.simplify(lap+4*lam*en)==0,'exact finite ensemble nonvacuum Poisson roots')
# Negative controls are not full-core countermodels.
require(rf+(-rf)==0,'opposite query orientations can cancel the geometric first source')
require(s.diff(r0e+z0*x*x,x).subs(x,0)==0,'positive quadratic-only query has no linear gravity source')
require(abs(la-lam0)>mp.mpf('1e-3'),'new ensemble is not relabelled old coupling')
extra=mp.diff(lambda a0:phi(a0,r0),mp.mpf(2)/5)
require(abs(extra)>mp.mpf('1e-8'),'field-dependent readiness adds a real source')
# Actual query dilution: independent Golden masks and fair-sign resources.
w0,tm=s.symbols('w t',real=True)
mean=0
for B in (0,1):
    for T in (-1,1):
        for F in (-1,1):
            prob=(w0 if B else 1-w0)*(1+tm*T)/2*s.Rational(1,2)
            Tout=T if B else F
            mean+=prob*Tout
require(s.simplify(mean-w0*tm)==0,'coherent masked sign has the actual diluted marginal')
for degree in range(9):
    require(s.expand(mean**degree-(w0*tm)**degree)==0,'independent masked signs preserve all eight tensor moments')
# Shared masks would give a different polynomial (not silently allowed).
require(s.expand(w0*tm**2-(w0*tm)**2)!=0,'one reused mask is not two independent masks')
eta=2*pp**3
require(bounds(pair((2*p**3)**8-p*p))[1]<0,'exact paid-resource tail decays faster than Golden programme tail')
Cz=6*zeta/((1-2*zeta)*(1-zeta)**2)
closed_refinement=[]
ldil=lam0/(2*pp)
for M0 in (1,2,4,8,12,24,48):
    alpha=eta**(8*M0) # aux factory readiness set to one ONLY in this numerical control
    lm,_=eff(M0,alpha)
    error=abs(lm-ldil)
    bound=abs(lam0)*(pp**(2*M0+1)+2*Cz*pp**2*alpha)
    require(error<=bound,'explicit all-query plus paid-resource coupling bound')
    closed_refinement.append({'M':M0,'fair_resource_readiness_upper':mp.nstr(alpha,20),
        'lambda_M':mp.nstr(lm,48),'error_to_analytic_limit':mp.nstr(error,20),'proved_bound':mp.nstr(bound,20)})
# Check the multiplier bound used for the proof of the full double limit.
for aa0 in (mp.mpf(1),mp.mpf(2)/5,coin):
    for m in range(12):
        tt0=aa0*pp**(m+2)
        C0=8*spectator*zeta*(1-2*zeta)*(1-2*r0)
        Wfactor=k(tt0,r0)/(C0*tt0**2)
        require(1-mp.mpf('1e-140')<=Wfactor<=1+Cz*tt0+mp.mpf('1e-140'),
                'exact positivity and linear readiness-relative correction')
output={'status':'PASS_CLOSED_SOURCE_CONE_AND_UNARY_ENSEMBLE','checks':CHECKS,
'python':platform.python_version(),'sympy':s.__version__,'mpmath_digits':mp.mp.dps,
'input_repo_head':'d42fd03b06522ce6e5eadc3fd51339e0b82274e6',
'finite_different_query_tables':table_controls,'common_dyadic_denominator_exponent':D.bit_length()-1,
'common_Golden_prefix_depth_for_queries_0_to_5':depth,'lambda_original':mp.nstr(lam0,50),
'dilute_unary_coefficient':mp.nstr(lam0/(2*pp),50),'ensembles':ensembles,'common_resource_refinement':closed_refinement,
'nonlinear_source_controls':controls,'moving_readiness_source_control':mp.nstr(extra,40),
'scope':{'positive_source_cone_and_exact_complete_price_composition':True,
'finite_query_ensemble_exact_Brinkmann_roots_by_owned_all40_substitution':True,
'countable_unary_ensemble_tail_bound':True,'all_query_plus_growing_resource_limit':True,'all_possible_D0_requests_in_class_proved':False,
'whole_catalogue_and_active_cut_selected_from_Book00_01':False,'original_all40_solver_replayed':False,
'huge_native_circuit_compiled_or_executed':False,'generic_exact_root_recovery':False,
'Lean_or_CI_run':False,'unconditional_GR_closed':False}}
text=json.dumps(output,ensure_ascii=False,indent=2)+'\n'
Path(__file__).with_name('result.json').write_text(text,encoding='utf-8');print(text,end='')
