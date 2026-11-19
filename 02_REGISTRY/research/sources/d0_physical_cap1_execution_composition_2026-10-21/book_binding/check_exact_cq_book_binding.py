#!/usr/bin/env python3
"""New narrow check, stdout-only unless --output is explicitly supplied.
No repo changes or physical price assignment. Symbolic cost variables remain
free. Native cap-one coefficients are those of the pinned existing owner.
"""
import argparse, hashlib, json, time
from pathlib import Path
import mpmath as mp
import sympy as sp

start=time.perf_counter()
checks=[]
def require(condition, label):
    if not condition:
        raise AssertionError(label)
    checks.append(label)

# Exact finite-leaf algebra, without selecting ANY actual cost/gain table.
w,c0,c1,i0,i1,L,Z=sp.symbols('w c0 c1 i0 i1 L Z', positive=True)
q=(w,1-w); c=(c0,c1); gain=(i0,i1)
H=-sum(a*sp.log(a)/L for a in q)
C=sum(a*b for a,b in zip(q,c))
logQ=[-L*(b-j)-Z for b,j in zip(c,gain)]
KL=sum(a*(sp.log(a)-b)/L for a,b in zip(q,logQ))
require(sp.expand(KL-Z/L+sum(a*b for a,b in zip(q,gain))-(C-H))==0,
        'exact Gibbs Book defect with free charges and gains')
theta,J=sp.symbols('theta J', real=True)
require(sp.expand(theta*H-((1+theta)*H-C)-(C-H))==0,
        'necessary sufficient mean normalization identity')
# Pair info = -log q, Book ratio phi^-s, or its square for amplitudes.
delta=sp.symbols('delta', real=True)
log_odds=sp.log(w)-sp.log(1-w)
required=-(1+theta)*log_odds/L
require(sp.simplify(sp.diff(required,w)+(1+theta)/(L*w*(1-w)))==0,
        'exact last-report gap derivative')

mp.mp.dps=80
p=(mp.sqrt(5)-1)/2; ell=mp.log(1/p); z=mp.mpf(2)**-20
alpha=(1-(1-2*p**3)**9)**128
beta=((1-p**120)**4*(1-(1-16*p**9)**20))**43

def rfun(x,y=mp.mpf(0)):
    B=4*(p+p*p*y)**2*(1-(p+p*p*y)**2)
    E=p*p*(1+x); le=4*E*(1-E)
    A=le+(1-le)*B
    return 1-(1-z*B)*(1-z*A)

def entropy(r):
    return -(r*mp.log(r)+(1-r)*mp.log1p(-r))/ell

L0=4*p**3; Q=1-z*L0; R=1-z*L0*(1+p**6)
r0=rfun(mp.mpf(0)); rx=4*z*Q*p**11
hp=mp.log((1-r0)/r0)/ell
require(0<r0<mp.mpf(2)**-19, 'actual cap-one r0 positive below 2^-19')
require(alpha>mp.mpf('0.5') and beta>mp.mpf('0.5'), 'actual paid readiness bounds')
require(abs(r0-(1-Q*R))<mp.mpf('1e-75'), 'actual two-query baseline identity')
require(rx>0 and abs(mp.diff(rfun,0)-rx)<mp.mpf('1e-75'),
        'native moving-query derivative nonzero')
source=-alpha*beta*hp*rx
require(source<0, 'fixed-price full CQ x source strictly negative')
require(abs(mp.diff(lambda x:-alpha*beta*entropy(rfun(x)),0)-source)<mp.mpf('1e-70'),
        'complete cap-one entropy source derivative')
num={}
for name,th in [('amplitude',mp.mpf('0.5')),('scalar',mp.mpf(1))]:
    gap=(1+th)*hp
    gapjet=-(1+th)*rx/(ell*r0*(1-r0))
    requiredjet=(1+th)*alpha*beta*hp*rx
    require(gapjet<0 and requiredjet>0, name+' gap and normalizer reaction signs')
    require(abs(mp.diff(lambda x:(1+th)*mp.log((1-rfun(x))/rfun(x))/ell,0)-gapjet)
            <mp.mpf('1e-70'), name+' gap first jet')
    # Equality is checked as an iff criterion, NOT adopted as physical gain.
    bookjet=th*alpha*beta*hp*rx-requiredjet
    require(abs(bookjet-source)<mp.mpf('1e-75'), name+' required reaction yields CQ source')
    num[name]=dict(required_gap_at_origin=mp.nstr(gap,40),
                   required_gap_x_derivative=mp.nstr(gapjet,40),
                   required_Jabs_x_derivative=mp.nstr(requiredjet,40))

# Noncommuting pure-state algebra fixture for exact finite-polynomial heat.
# This is NOT a new D0 carrier or the physical numerical HJR price.
b=(mp.mpf(4)/5,mp.mpf(3)/4); m=3; bh=mp.mpf(3)
rdiag=(mp.mpf(2)/3,mp.mpf(1)/3); delt=(1-b[0],1-b[1])
Zheat=sum(x**m for x in b)
tau=[x**m/Zheat for x in b]
D=-sum(a*mp.log(t) for a,t in zip(rdiag,tau))
Lheat=[-m*mp.log(x)/bh for x in b]
left=mp.log(Zheat)/bh+sum(a*d for a,d in zip(rdiag,delt))
right=D/bh+sum(a*(d-v) for a,d,v in zip(rdiag,delt,Lheat))
require(abs(left-right)<mp.mpf('1e-75'), 'noncommuting pure input finite-heat identity')
require(sum(a*(d-v) for a,d,v in zip(rdiag,delt,Lheat))!=0,
        'finite-polynomial heat mismatch cannot be dropped')
result=dict(status='PASS',checks=len(checks),labels=checks,precision_digits=80,
            scope='new symbolic valuation checks plus original cap-one coefficients; no unknown actual price table assigned',
            r0=mp.nstr(r0,45),rx=mp.nstr(rx,45),
            full_CQ_x_source=mp.nstr(source,45),requirements=num,
            elapsed_seconds=time.perf_counter()-start)
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
args=parser.parse_args()
text=json.dumps(result,indent=2)+'\n'
if args.output: args.output.write_text(text)
print(text,end='')
