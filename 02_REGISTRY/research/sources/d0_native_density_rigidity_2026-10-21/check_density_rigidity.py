#!/usr/bin/env python3
"""Narrow new identities for full-price density rigidity; no old suite replay."""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import sys
import sympy as s
import mpmath as mp

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path)
args=parser.parse_args()
if args.repo is None:
    args.repo=Path(__file__).resolve().parents[4]
checks=[]
def check(name, condition):
    if not bool(condition):
        raise RuntimeError('FAILED: '+name)
    checks.append(name)
def zero(name, expr):
    check(name,s.factor(expr)==0)

packet=Path(__file__).resolve().parent
pins=json.loads((packet/'SOURCE_PINS.json').read_text())
for item in pins['inputs']:
    source=packet/item['snapshot_path'] if 'snapshot_path' in item else args.repo/item['path']
    check('pin:'+item['path'],hashlib.sha256(source.read_bytes()).hexdigest()==item['sha256'])

x,y,rx,ry,rxx,rxy,ryy,v1,v2,tprime,a,M,Mprime,Q=s.symbols('x y rx ry rxx rxy ryy v1 v2 tprime a M Mprime Q', nonzero=True)
# The induced variation uses density weight one for x and weight zero for y.
Fx,Fy,F,div,transport=s.symbols('Fx Fy F div transport')
raw=transport+x*Fx*div
integrated=-F*div+x*Fx*div
zero('fixed-measure-pressure-coefficient',integrated-(x*Fx-F)*div)
check('densitizing-y-changes-pressure',s.expand((x*Fx+y*Fy-F)*div-integrated)==y*Fy*div)
Acoef,Bcoef=s.symbols('Acoef Bcoef',nonzero=True)
linear=Acoef*x+Bcoef*y
zero('linear-nondensitized-pressure-is-b-y',linear-x*s.diff(linear,x)-Bcoef*y)
zero('linear-densitized-action-has-zero-pressure',linear-x*s.diff(linear,x)-y*s.diff(linear,y))

Mp=v2*(rx*tprime+ry)*rx+v1*(rxx*tprime+rxy)
Pdirect=v1*ry-x*Mp
Pfactored=v1*ry*(1-y*Mp/(v1*rx))
zero('pressure-factorization-with-exact-radial-residual',Pdirect-Pfactored+(x*rx-y*ry)*Mp/rx)
Yprime=a/(v1*rx)*(1-y*Mp/(v1*rx))
Kprime=v1**2*rx*ry/a
zero('normal-form-pressure-derivative',Kprime*Yprime-Pfactored)
T=x*rx-y*ry
Tx=rx+x*rxx-y*rxy
Ty=x*rxy-ry-y*ryy
zero('trace-branch-tangent',Tx*(-Ty/Tx)+Ty)
# Coordinate-invariant comparison is not assumed; this is the source ratio at
# one configuration with a genuinely spacetime-constant detector response.
vrN,vrM,deltar=s.symbols('vrN vrM deltar',nonzero=True)
zero('common-ambient-source-at-constant-response',vrM*deltar-vrM/vrN*(vrN*deltar))
vrrN,vrrM,dr2,d2r=s.symbols('vrrN vrrM dr2 d2r')
hN=vrN*d2r+vrrN*dr2
hM=vrM*d2r+vrrM*dr2
zero('hessian-extra-term-is-retained',hM-vrM/vrN*hN-(vrrM-vrM/vrN*vrrN)*dr2)
check('same-critical-set-does-not-force-same-hessian',s.expand((hM-vrM/vrN*hN).subs({vrM:2,vrN:1,vrrM:7,vrrN:3,dr2:1,d2r:5}))==1)
# These are full Jacobi constraints, not an assumed integrable family.
dx,dy,drv,drw=s.symbols('dx dy drv drw')
Px=-x*(v2*rx**2+v1*rxx)
Py=v1*ry-x*(v2*rx*ry+v1*rxy)
zero('linearized-pressure-on-trace-tangent',(Px*dx+Py*dy).subs(dx,tprime*dy)-Pdirect*dy)
zero('linearized-trace-selects-branch-tangent',(Tx*dx+Ty*dy).subs(dx,-Ty*dy/Tx))
zero('all-cap-jacobi-transfer-when-delta-r-vanishes',(hM-vrM/vrN*hN).subs(dr2,drv*drw).subs(drv,0))

# The price nonvanishing interval is available BEFORE extracting the branch.
pg=(s.sqrt(5)-1)/2
check('golden-full-rectangle-p-bound',s.Rational(3,5)<pg<s.Rational(5,8))
check('golden-full-rectangle-p-squared-bound',s.Rational(3,8)<pg**2<s.Rational(2,5))
check('full-rectangle-query-E',Fraction(3,8)*Fraction(3,4)>Fraction(1,4) and Fraction(2,5)*Fraction(5,4)==Fraction(1,2))
check('full-rectangle-query-b',Fraction(3,5)-Fraction(2,5*4096)>Fraction(1,2) and Fraction(5,8)+Fraction(2,5*4096)<Fraction(2,3))
check('full-rectangle-detector-lower-bound',Fraction(3,2)-Fraction(1,2**20)>1)

# Rational bounds consume the stated analytical estimates of the pinned owner.
eps=Fraction(1,4096)
check('owned-log-slope-domain',202*eps<Fraction(1,16))
lo=Fraction(15,16)**2*Fraction(1408,133)
hi=Fraction(16,15)*Fraction(17,16)*Fraction(4736,123)
check('exact-pressure-lower-bound',lo==Fraction(2475,266) and lo>9)
check('exact-pressure-upper-bound',hi==Fraction(80512,1845) and hi<44)

# Both source components and the real norm/coordinate normalization are kept.
e,rho,q0,lam,k,eta=s.symbols('e rho q0 lam k eta',positive=True)
zero('timelike-source-mass-normalization',(lam*q0/e-rho).subs(rho,lam*q0/e))
zero('trace-calibrates-mass-coordinate',(rx*k-ry*q0).subs(k,ry*q0/rx))
zero('constant-kinetic-geodesic-identity',s.diff(q0,y)/(2*q0))
t,X1,X2,X3=s.symbols('t X1 X2 X3', real=True)
C=2+X1**2+X2**2+X3**2
newX1=((2+X2**2+X3**2)*X1+X1**3/3)/k
J=s.Matrix([newX1,X2,X3]).jacobian([X1,X2,X3]).det()
zero('explicit-positive-spatial-mass-Jacobian',J-C/k)
zero('mass-density-transforms-to-constant',C/J-k)
zero('timelike-relabel-is-time-independent',s.diff(newX1,t))
nullX1=s.exp(t)*newX1
J4=s.Matrix([t,nullX1,X2,X3]).jacobian([t,X1,X2,X3]).det()
zero('null-density-coordinate-can-preserve-potential',J4-s.exp(t)*C/k)
zero('null-mass-density-transforms-to-constant',s.exp(t)*C/J4-k)

# Exact symbolic scaling of the optional finite PF normal-form remainder.
zvar,epsilon,b=s.symbols('zvar epsilon b',nonzero=True)
k2,k3=s.symbols('k2 k3')
K=b*zvar+k2*zvar**2/2+k3*zvar**3/6
for sign in (-1,1):
    Rem=(K.subs(zvar,sign*epsilon*y)-b*sign*epsilon*y)/(a*epsilon)
    zero('PF-linear-source-'+str(sign),s.diff(Rem,y).subs(y,0))
    zero('PF-quadratic-epsilon-'+str(sign),s.diff(Rem,y,2).subs(y,0)-epsilon*k2/a)

# Numerical differentiation tests the NEW pressure identity on the actual
# Golden detector. These fixtures are not the physical compiler parameters
# and finite examples do not prove the all-N theorem.
mp.mp.dps=85
p=(mp.sqrt(5)-1)/2
z=mp.mpf(2)**-20
alpha=mp.mpf(3)/5
beta=mp.mpf(5)/7
kappa=mp.mpf(54)
lnphi=mp.log(1/p)
def wfun(yy): return 1-2*(p+p*p*yy)**2
def cfun(yy): return 1-z+z*wfun(yy)**2
def Afun(yy): return 4*p**5*z*cfun(yy)*wfun(yy)**2
def Rfun(yy): return 1-cfun(yy)*(1-z+z*p**6*wfun(yy)**2)
def rfun(xx,yy): return Rfun(yy)+Afun(yy)*(xx-xx*xx/p)
def rx_fun(xx,yy): return Afun(yy)*(1-2*xx/p)
def ry_fun(xx,yy): return mp.diff(Rfun,yy)+mp.diff(Afun,yy)*(xx-xx*xx/p)
def tau_fun(yy):
    C0=mp.diff(Rfun,yy)/Afun(yy)
    kk=-yy*mp.diff(Afun,yy)/Afun(yy)
    disc=(1+kk)**2-4*(2+kk)*yy*C0/p
    return 2*yy*C0/(1+kk+mp.sqrt(disc))
def entropy(rr): return -(rr*mp.log(rr)+(1-rr)*mp.log1p(-rr))/lnphi
r0=rfun(mp.mpf(0),mp.mpf(0))
rows=[]
maxrel=mp.mpf(0)
for cap in (1,2,7,31):
    def value(rr): return alpha*(kappa-beta*entropy(rr))*sum((beta*rr)**j for j in range(cap))
    a0=mp.diff(value,r0)*rx_fun(0,0)
    def mm(yy):
        xx=tau_fun(yy)
        return mp.diff(value,rfun(xx,yy))*rx_fun(xx,yy)
    def pressure(yy):
        xx=tau_fun(yy)
        return value(rfun(xx,yy))-xx*mm(yy)
    for yn in (-1,-mp.mpf(1)/2,0,mp.mpf(1)/2,1):
        yy=mp.mpf(yn)*mp.mpf(2)**-12
        xx=tau_fun(yy)
        Pp=mp.diff(pressure,yy)
        Pformula=mp.diff(value,rfun(xx,yy))*ry_fun(xx,yy)*(1-yy*mp.diff(mm,yy)/mm(yy))
        rel=abs((Pp-Pformula)/a0)
        maxrel=max(maxrel,rel)
        check('actual-pressure-identity-cap%s-y%s'%(cap,yn),rel<mp.mpf('1e-65'))
        check('actual-normalized-nondegeneracy-cap%s-y%s'%(cap,yn),9<Pp/a0<44)
        check('trace-root-cap%s-y%s'%(cap,yn),abs(xx*rx_fun(xx,yy)-yy*ry_fun(xx,yy))<mp.mpf('1e-70'))
        rows.append({'cap':cap,'y':mp.nstr(yy,14),'Pprime_over_a':mp.nstr(Pp/a0,25)})

result={'status':'PASS','scope':'New density-rigidity identities; no old source-suite replay; finite fixtures do not establish infinite theorem',
        'checks':len(checks),'exact_lower_bound':str(lo),'exact_upper_bound':str(hi),
        'max_normalized_pressure_identity_error':mp.nstr(maxrel,12),
        'numeric_fixture':{'alpha':'3/5','beta':'5/7','kappa':'54','precision_digits':mp.mp.dps},
        'samples':rows,'checked_source_pins':len(pins['inputs'])}
print(json.dumps(result,indent=2,ensure_ascii=False))
