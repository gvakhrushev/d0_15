#!/usr/bin/env python3
"""Exact metric reconstruction and genuine fixed-protocol price controls.

Scope: the explicitly supplied D0 three-status/ten-sign candidate. This
is NOT a native compiler, proof of literal Book03 selection, large all42
lattice run or proof of uniform physical root recovery.
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction
import mpmath as mp
import sympy as sp

mp.mp.dps = 100
COUNT=0

def require(ok, description):
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise ArithmeticError(description)

def zero(A, description):
    require(all(sp.cancel(v)==0 for v in A),description)

def close(a,b,description,tolerance=mp.mpf('1e-65')):
    require(abs(a-b)<=tolerance*max(1,abs(a),abs(b)),description)

# Full non-unimodular original-style coframe. No unit-volume restriction.
eta=sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
e=sp.Matrix([[2,sp.Rational(1,3),0,sp.Rational(1,5)],
             [0,1,sp.Rational(1,7),0],
             [0,0,1,sp.Rational(1,4)],[0,0,0,2]])
E=e.det(); g=e.T*eta*e
volume=sp.Rational(3,2)  # Coordinate density of the SAME supplied volume form.
K=volume*g.inv()

def metric_of_density(T):
    return sp.sqrt(-T.det())*T.inv()

G=metric_of_density(K)
zero(G-volume*g/E,'kinetic metric from original weighted principal density')
zero(sp.sqrt(-G.det())*G.inv()-K,'exact reconstruction of the complete density')
require(E==4 and sp.sqrt(-K.det())==sp.Rational(9,16),'exact original determinants')
# Reconstruct all TEN symmetric coefficients by polarization, not a metric fit.
basis=[sp.eye(4)[:,i] for i in range(4)]
values={(i,): (basis[i].T*K*basis[i])[0] for i in range(4)}
for i in range(4):
    for j in range(i+1,4):
        vec=basis[i]+basis[j]
        values[(i,j)]=(vec.T*K*vec)[0]
K_rec=sp.zeros(4)
for i in range(4):
    K_rec[i,i]=values[(i,)]
    for j in range(i+1,4):
        K_rec[i,j]=K_rec[j,i]=(values[(i,j)]-values[(i,)]-values[(j,)])/2
zero(K_rec-K,'all ten kinetic coefficients read by polarization')
# An arbitrary non-volume-preserving coordinate chart change.
J=sp.Matrix([[2,sp.Rational(1,5),0,0],[0,3,sp.Rational(1,7),0],
             [0,0,1,sp.Rational(1,4)],[0,0,0,sp.Rational(1,2)]])
Jac=J.det(); require(Jac==3,'nonunit coordinate Jacobian')
e2=e*J.inv(); volume2=volume/Jac; g2=e2.T*eta*e2
K2=volume2*g2.inv(); G2=metric_of_density(K2)
zero(K2-J*K*J.T/Jac,'actual weight-one contravariant-density transport')
zero(G2-J.inv().T*G*J.inv(),'derived ordinary Lorentz metric is coordinate covariant')
wrongG=metric_of_density(volume*g2.inv())
require(wrongG!=G2,'freezing coordinate volume would NOT prove covariance')
# Every real symmetric K direction, not just coframe scale or diagonal changes.
t=sp.symbols('t',real=True)
for i in range(4):
    for j in range(i,4):
        dK=sp.zeros(4);dK[i,j]=1;dK[j,i]=1
        formula=sp.sqrt(-K.det())*(sp.trace(K.inv()*dK)*K.inv()/2-K.inv()*dK*K.inv())
        pert=K+t*dK
        direct=sp.diff(sp.sqrt(-pert.det()),t).subs(t,0)*K.inv()-sp.sqrt(-K.det())*K.inv()*dK*K.inv()
        zero(formula-direct,'all ten complete metric first derivatives')
# Spurious dimension-independent uniqueness is rejected: n=2 retains conformal freedom.
g_two=sp.diag(1,-1);g_two_scaled=7*g_two
zero(sp.sqrt(-g_two.det())*g_two.inv()-sp.sqrt(-g_two_scaled.det())*g_two_scaled.inv(),
     'two-dimensional conformal nonuniqueness control')

# The actual polynomial report and ALL source-dependent cut thermal terms.
p=(mp.sqrt(5)-1)/2; z=mp.mpf(2)**-20; beta=2*p*p
sR=128; M=72441; W=50549
a=2*10946*p**23
Zmin=M*(W-2)
eta_rat=Fraction(13,5)/(64*Fraction(1,2**20)*(1-Fraction(1,2**19))*Zmin)
eta_bound=mp.mpf(eta_rat.numerator)/eta_rat.denominator
require(eta_rat<Fraction(1,80000),'inherited exact thermal domination bound')

def report(x,y):
    u=p+p*p*y; ee=p*p*(1+x)
    ell=4*ee*(1-ee); b=4*u*u*(1-u*u)
    aa=ell+(1-ell)*b
    return 1-(1-z*b)*(1-z*aa)

def qs(r):return (1-a,a*(1-r),a*r)
def f(q):return 4*q*(1-q)
def fprime(q):return 4*(1-2*q)
def Jret(r):return -sR*sum(mp.log1p(-z*f(q)) for q in qs(r))
def Zheat(r):return mp.mpf(M*W-6)+2*sum(mp.exp(-beta*f(q)) for q in qs(r))
def Bcut(r):return mp.log(sR*Zheat(r))/beta+Jret(r)
def Jprime(r):
    u,v=a*r,a*(1-r)
    return a*sR*z*(fprime(u)/(1-z*f(u))-fprime(v)/(1-z*f(v)))
def Bprime(r):
    Z=Zheat(r)
    def c(q):return (sR*z/(1-z*f(q))-2*mp.exp(-beta*f(q))/Z)*fprime(q)
    return a*(c(a*r)-c(a*(1-r)))

r0=report(0,0)
rf=mp.diff(lambda x:report(x,0),0);rq=mp.diff(lambda y:report(0,y),0)
lam=-rq/rf;kappa=Bprime(r0)
require(kappa>0,'actual complete price has nonzero normalization')
ratios=[]
for r in (mp.mpf(0),r0,mp.mpf(1)/100,mp.mpf(1)/10,mp.mpf(1)/4):
    jj=Jprime(r);bb=Bprime(r)
    close(jj,mp.diff(Jret,r),'full feedback derivative')
    close(bb,mp.diff(Bcut,r),'moving complete heat-normalizer derivative')
    require(0<(1-eta_bound)*jj<=bb<=jj,'positive SAME-protocol source multiplier')
    ratios.append({'r':mp.nstr(r,20),'Bprime_over_Jprime':mp.nstr(bb/jj,30)})
# Equality of Hessian inertia at a stationary composite, NOT equality of actions.
center=mp.mpf(1)/100
r_saddle=lambda u,v: center+(u*u-v*v)/100
ht=mp.diff(lambda u:Jret(r_saddle(u,0)),0,2)
hc=mp.diff(lambda u:Bcut(r_saddle(u,0)),0,2)
close(hc/ht,Bprime(center)/Jprime(center),'stationary Hessians scale by actual positive gain')
require(mp.diff(lambda v:Bcut(r_saddle(0,v)),0,2)<0<hc,'saddle not reclassified as a minimum')

# EXACT matter Hessian on the actual nonlinear polynomial/full price,
# at a constant (zero-gradient) matter background. It determines its metric.
rhos=[mp.mpf(1)/2,mp.mpf(3)/4,mp.mpf(5)/4,mp.mpf(3)/2]
Fs=[mp.mpf(1)/7,-mp.mpf(2)/9,mp.mpf(1)/4,mp.mpf(2)/11]
cell=2;v=mp.matrix([mp.mpf(2)/3,-mp.mpf(1)/5,mp.mpf(3)/7,mp.mpf(1)/4])
inv_g=mp.matrix([[mp.mpf(str(g.inv()[i,j].p))/int(g.inv()[i,j].q) for j in range(4)] for i in range(4)])
q_v=(v.T*inv_g*v)[0]
kinetic_controls=[]
for power in (5,7,9,11):
    eps=mp.mpf(2)**-power
    rbar0=sum(rho*report(eps*ff/rho,0) for rho,ff in zip(rhos,Fs))/4
    y_der=mp.diff(lambda y:report(eps*Fs[cell]/rhos[cell],y),0)
    factor=(Bprime(rbar0)/kappa)*(y_der/rq)
    def actual_price(amplitude):
        rb=mp.mpf(0)
        for i,(rho,ff) in enumerate(zip(rhos,Fs)):
            qmatter=amplitude*amplitude*q_v if i==cell else 0
            rb+=rho*report(eps*ff/rho,-eps*qmatter/rho)/4
        return Bcut(rb)
    Hess=mp.diff(actual_price,0,2)
    predicted=-2*eps*Bprime(rbar0)*y_der*q_v/4
    close(Hess,predicted,'full real matter Hessian including all report and thermal terms')
    normalized=Hess/(2*lam*kappa*eps*rf)
    close(normalized,factor*q_v/4,'normalized kinetic density is internally fixed')
    require(factor>0 and abs(factor-1)/eps<2,'intrinsic finite-signal metric tends to density metric')
    kinetic_controls.append({'eps':'2^-'+str(power),'kinetic_density_factor':mp.nstr(factor,35),
                             'relative_metric_error_over_eps':mp.nstr(abs(factor-1)/eps,25)})

# The report is exactly polynomial; taking a field derivative is NOT the
# same as treating f and q as independent physical degrees of freedom.
px, zz, xx, yy=sp.symbols('p_alg z_alg x_report y_report')
ee=px**2*(1+xx); uu=px+px**2*yy
ll=4*ee*(1-ee); bb=4*uu**2*(1-uu**2)
aa=ll+(1-ll)*bb
rr=sp.Poly(sp.expand(1-(1-zz*bb)*(1-zz*aa)),xx,yy)
require(rr.degree(xx)==2 and rr.degree(yy)==8,'literal report bidegree (2,8)')
require(sp.expand(rr.coeff_monomial(xx**2*yy**8)+64*zz**2*px**20)==0,
        'exact highest report coefficient, no fitted source')
# Rational field maps admit exact denominator-cleared source equations.
u_alg=sp.symbols('u_alg')
rat=(u_alg**2+1)/(u_alg+2)
num,den=sp.fraction(sp.cancel(sp.diff(rat,u_alg)))
require(sp.expand(num)==u_alg**2+4*u_alg-1 and sp.expand(den-(u_alg+2)**2)==0,
        'denominator-cleared derivative keeps excluded poles explicit')

# A C2 rather than C1 source-consistency check of the SAME full action.
dFs=[mp.mpf(2)/7,mp.mpf(1)/9,-mp.mpf(3)/10,mp.mpf(1)/8]
ddFs=[mp.mpf(1)/3,-mp.mpf(1)/7,mp.mpf(2)/9,mp.mpf(1)/11]
Qs=[mp.mpf(1)/17,-mp.mpf(1)/13,mp.mpf(1)/19,mp.mpf(1)/23]
dQs=[mp.mpf(1)/29,-mp.mpf(1)/31,mp.mpf(2)/37,mp.mpf(1)/41]
ddQs=[mp.mpf(1)/43,mp.mpf(1)/47,-mp.mpf(2)/53,mp.mpf(1)/59]
base=Bcut(r0)
def I_target(t):
    return sum(ff+t*df+t*t*ddf/2+lam*(qq+t*dq+t*t*ddq/2)
               for ff,df,ddf,qq,dq,ddq in zip(Fs,dFs,ddFs,Qs,dQs,ddQs))/4
def Jnormalized(eps,t):
    rb=sum(rho*report(eps*(ff+t*df+t*t*ddf/2)/rho,
                       -eps*(qq+t*dq+t*t*ddq/2)/rho)
           for rho,ff,df,ddf,qq,dq,ddq in zip(rhos,Fs,dFs,ddFs,Qs,dQs,ddQs))/4
    return (Bcut(rb)-base)/(kappa*eps*rf)
c2_results=[]
for power in (4,6,8,10):
    eps=mp.mpf(2)**-power
    errors=[abs(mp.diff(lambda t:Jnormalized(eps,t),0,k)-mp.diff(I_target,0,k)) for k in range(3)]
    require(max(errors)/eps<2,'full nonlinear action has checked C2 error scale')
    c2_results.append({'eps':'2^-'+str(power),'errors_over_eps':[mp.nstr(x/eps,25) for x in errors]})
# First-source convergence does not alone imply exact critical points.
x,h=sp.symbols('x h',real=True)
S0=x**3/3;Sh=S0+h*x
require(sp.diff(Sh,x)==x*x+h,'exact root-recovery negative control')
# Check the contraction-radius arithmetic for the explicit theorem in the proof.
Kbound=Fraction(2);residual=Fraction(1,1000);hess_defect=Fraction(1,100);Lip=Fraction(3)
radius=2*Kbound*residual
contract=Kbound*(hess_defect+Lip*radius)
require(contract<=Fraction(1,2) and Kbound*residual+contract*radius<=radius,
        'quantitative root theorem constants map the ball into itself')

output={'status':'PASS_INTRINSIC_METRIC_HEAT_EQUIVALENCE_AND_C2_CONTROL',
        'checks':COUNT,'python':sys.version.split()[0],'sympy':sp.__version__,'mpmath_digits':mp.mp.dps,
        'pinned_source':'c7708742bea04684ffd6aed16774cfdf1b94b129',
        'metric_example':{'det_e':str(E),'volume_density':str(volume),
                         'metric_factor_relative_to_g':str(volume/E),'det_coordinate_J':str(Jac)},
        'exact_thermal_bound':str(eta_rat),'whole_price_source_ratios':ratios,
        'exact_finite_signal_kinetic_metric_controls':kinetic_controls,
        'whole_price_C2_controls':c2_results,
        'root_certificate_arithmetic':{'K':str(Kbound),'eta':str(residual),'delta':str(hess_defect),
                                      'L':str(Lip),'radius':str(radius),'contraction':str(contract)},
        'structural_controls_not_native_executions':True,
        'original_large_lattice_inverse_bound_established':False,
        'native_compilation_and_full_valuation_identified':False,
        'unconditional_GR_closed':False}
print(json.dumps(output,ensure_ascii=False,indent=2))
