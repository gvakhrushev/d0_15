#!/usr/bin/env python3
"""Independent exact row-spectrum audit of original native K=1 fine/age CQ.

Original constructor: ee8de4635d24c668949ac9a0186616ab7d59f2ed.
Consumes the already owned stationary row-block identity; does not reclaim it.
New calculation: rational / quadratic-field Walsh row spectra, no SVD, with
all 128 physical row/port slots and the actual same-one-round age grouping.
No physical Book03 Info or all-in cost selection is asserted.
"""
import argparse
import json
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import sympy as s
import mpmath as mp

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--json',type=Path,metavar='PATH',
                    help='also write the JSON receipt to this explicit path')
args=parser.parse_args()

R=s.Rational
I=s.eye(16)
O=s.zeros(16)
imag=s.I
checks=[]
def check(test,name):
    if not bool(test): raise ArithmeticError(name)
    checks.append(name)
def clean(x): return s.expand(x)
def mc(x): return x.applyfunc(clean)
def zero(x): return all(clean(v)==0 for v in x)
def adj(x): return x.conjugate().T
def trace(x): return clean(s.trace(x))

order=(0,2,3,1)
cs=[]
for role in range(4):
    c=s.zeros(16)
    before=order[:order.index(role)]
    for bits in range(16):
        if not (bits>>role)&1:
            c[bits|(1<<role),bits]=(-1)**sum((bits>>j)&1 for j in before)
    cs.append(c)
G=cs[0]*adj(cs[1])+cs[1]*adj(cs[0])
check(zero(G**3-G),'exact original CAR boost cubic')
r=R(1,9); nu=R(3,5); dt=R(81,40)
U=I+R(9,40)*G+R(1,40)*G**2
dU=dt*U*G
h=R(69399,5030720); hr=-R(20040939,9885993640)
dn=-nu*hr/(2*h)
a=nu**2; da=2*nu*dn
c=R(881,800); dc=R(29889,16000)
b=a*c; db=da*c+a*dc
u=R(4,5); du=-da/(2*u)
v=s.sqrt(24142)/200; dv=-db/(2*v)
alpha=(u-1)/a
dalpha=clean((du*a-(u-1)*da)/a**2)
den=b*(b-a); dden=db*(2*b-a)-b*da
beta=clean((v-1-alpha*b)/den)
dbeta=clean((dv-dalpha*b-alpha*db)/den-beta*dden/den)

def boosted_root_jet(Y,dY):
    check(zero(mc(Y*(Y-a*I)*(Y-b*I))),'exact boosted Gram spectrum is in {0,a,b}')
    check(trace(Y)==4*(a+b) and trace(Y*Y)==4*(a*a+b*b),
          'exact boosted Gram multiplicities are 8,4,4')
    check(clean(1+alpha*a)==u and clean(1+alpha*b+beta*b*(b-a))==v and u>0 and v>0,
          'polynomial Julia square root takes positive spectral values')
    V=mc(I+alpha*Y+beta*Y*(Y-a*I))
    dV=mc(dalpha*Y+alpha*dY+dbeta*Y*(Y-a*I)
           +beta*(dY*(Y-a*I)+Y*(dY-da*I)))
    check(zero(mc(V*V)-(I-Y)),'exact boosted Julia positive-root square')
    check(zero(mc(dV*V+V*dV)+dY),'exact boosted Julia derivative square')
    return V,dV

words=[];jets=[]
phases=(imag,imag,-1,-imag)
for role,cr in enumerate(cs):
    base=nu*cr; dbase=dn*cr
    boost=U if role==1 else I
    dboost=dU if role==1 else O
    x=base*boost*phases[role]
    dx=(dbase*boost+base*dboost)*phases[role]
    P=cr*adj(cr); Q=adj(cr)*cr
    L0=I+(u-1)*P; dL0=du*P
    R0=I+(u-1)*Q; dR0=du*Q
    if role==1:
        Y=mc(x*adj(x)); dY=mc(dx*adj(x)+x*adj(dx))
        W=mc(adj(x)*x); dW=mc(adj(dx)*x+adj(x)*dx)
        L,dL=boosted_root_jet(Y,dY)
        Rr,dR=boosted_root_jet(W,dW)
    else:
        L,dL=L0,dL0; Rr,dR=R0,dR0
    for w,dw in zip(((x,L),(adj(x),Rr),(-base,-L0),(-adj(base),-R0)),
                    ((dx,dL),(adj(dx),dR),(-dbase,-dL0),(-adj(dbase),-dR0))):
        words.extend((w,w));jets.extend((dw,dw))
rows=[];drows=[]
for label in range(32):
    signs=[(-1)**((label&j).bit_count()&1) for j in range(32)]
    for col in range(2):
        rows.append(mc(sum((signs[j]*words[j][col] for j in range(32)),O)/32))
        drows.append(mc(sum((signs[j]*jets[j][col] for j in range(32)),O)/32))
check(all(zero(rows[j]) and zero(drows[j]) for j in range(64) if (j//2)&1),
      '32 exact-dark Walsh rows with exact-dark jets')
check(zero(mc(sum((adj(N)*N for N in rows),O))-I),'exact full Walsh row completeness')
check(zero(mc(sum((N*adj(N) for N in rows),O))-I),'exact full Walsh row co-completeness')
check(zero(mc(sum((adj(dN)*N+adj(N)*dN for N,dN in zip(rows,drows)),O))),
      'exact full Walsh completeness source')

# Each (lambda, d_lambda, multiplicity) is the actual row-Gram spectrum/jet.
spectra={}; classes={}; detailed={}
for j,(N,dN) in enumerate(zip(rows,drows)):
    if (j//2)&1: continue
    E=mc(adj(N)*N); dE=mc(adj(dN)*N+adj(N)*dN)
    eigen=[]
    if j%2==0:
        mu=trace(E)/16; dmu=trace(dE)/16
        variance=clean(trace(E*E)/16-mu**2)
        dvariance=clean(trace(E*dE)/8-2*mu*dmu)
        check(zero(mc((E-mu*I)**2)-variance*I),f'exact quadratic Gram identity row {j}')
        check(zero(mc((E-mu*I)*(dE-dmu*I)+(dE-dmu*I)*(E-mu*I))-dvariance*I),
              f'exact quadratic Gram first source row {j}')
        for sign in (-1,1):
            eigen.append((mu+sign*s.sqrt(variance),dmu+sign*dvariance/(2*s.sqrt(variance)),8))
        key=str((mu,variance,dmu,dvariance))
        detailed[str(j)]={'kind':'quadratic Gram','mu':str(mu),'variance':str(variance),
                          'dmu':str(dmu),'dvariance':str(dvariance)}
    else:
        check(zero(N-adj(N)),f'even Julia row {j} is Hermitian')
        groups=[]
        for spectator in range(4):
            mask=((spectator&1)<<2)+((spectator>>1)<<3)
            groups.extend(((mask,),(mask|3,),(mask|1,mask|2)))
        cover={(i,k) for group in groups for i in group for k in group}
        check(all(N[i,k]==0 and dN[i,k]==0 for i in range(16) for k in range(16) if (i,k) not in cover),
              f'exact scalar/two-mode block algebra row {j}')
        signature=[]
        for group in groups:
            if len(group)==1:
                n=N[group[0],group[0]];dn0=dN[group[0],group[0]]
                eigen.append((clean(n*n),clean(2*n*dn0),1))
                signature.append((n,dn0))
            else:
                q,w=group
                center=clean((N[q,q]+N[w,w])/2)
                dcenter=clean((dN[q,q]+dN[w,w])/2)
                radius=clean(((N[q,q]-N[w,w])/2)**2+N[q,w]*N[w,q])
                dradius=clean((N[q,q]-N[w,w])*(dN[q,q]-dN[w,w])/2
                             +dN[q,w]*N[w,q]+N[q,w]*dN[w,q])
                if radius==0:
                    eigen.append((clean(center**2),clean(2*center*dcenter),2))
                    signature.extend(((center,dcenter),(center,dcenter)))
                else:
                    for sign in (-1,1):
                        n=center+sign*s.sqrt(radius)
                        dn0=dcenter+sign*dradius/(2*s.sqrt(radius))
                        eigen.append((n*n,2*n*dn0,1))
                        signature.append((n,dn0))
        key=str(sorted([(str(clean(n*n)),str(clean(2*n*dn0))) for n,dn0 in signature]))
        detailed[str(j)]={'kind':'1x1 / 2x2 Hermitian Julia blocks'}
    spectra[j]=eigen
    classes.setdefault(key,[]).append(j)

mu0=s.sympify(detailed['0']['mu']); w0=s.sympify(detailed['0']['variance'])
dmu0=s.sympify(detailed['0']['dmu']); dw0=s.sympify(detailed['0']['dvariance'])
check(s.cancel((mu0**2-w0)/mu0-h)==0,'exact original inverse-square normalization h')
check(s.cancel(dmu0*(1+w0/mu0**2)-dw0/mu0)==0,'exact native v has dh=0')

mp.mp.dps=75
def val(x): return mp.mpf(str(s.N(x,85)))
def entropy_jet(eigs,scale=mp.mpf(1),dscale=mp.mpf(0)):
    S=mp.mpf(0);dS=mp.mpf(0);mass=mp.mpf(0);dmass=mp.mpf(0)
    for ev,dev,mult in eigs:
        q=scale*val(ev);dq=dscale*val(ev)+scale*val(dev)
        if ev==0:
            check(dev==0,'exact zero Gram mode has zero first source')
            continue
        check(q>0,'all retained nonzero algebraic Gram modes positive')
        S-=mult*q*mp.log(q);dS-=mult*dq*(mp.log(q)+1)
        mass+=mult*q;dmass+=mult*dq
    return S,dS,mass,dmass

p=(mp.sqrt(5)-1)/2;t=2*p*p;port=2*p*mp.sqrt(p)
Z=16/val(h)
delta=spectra[0]
# dh=0 implies dZ=0. All input eigenvalues are 1/(Z lambda).
initial=[];blank=[];nonblank_age=[]
for lam,dlam,mult in delta:
    l=val(lam);dl=val(dlam)
    q=1/(Z*l);dq=-q*dl/l
    B=1-t*l;dB=-t*dl
    initial.append((q,dq,mult))
    blank.append((B*B*q,2*B*dB*q+B*B*dq,mult))
    nonblank_age.append((q*(1-B*B),dq*(1-B*B)-q*2*B*dB,mult))
def ent_numeric(eigs):
    return (sum(-m*q*mp.log(q) for q,dq,m in eigs),
            sum(-m*dq*(mp.log(q)+1) for q,dq,m in eigs))
S0,dS0=ent_numeric(initial)
Sb,dSb=ent_numeric(blank)
Sa,dSa=ent_numeric(nonblank_age)
Sf,dSf=Sb,dSb
for j,eigs in spectra.items():
    if j:
        es,eds,_,_=entropy_jet(eigs,t*t/Z)
        Sf+=es;dSf+=eds
    es,eds,_,_=entropy_jet(eigs,port*port/Z)
    Sf+=es;dSf+=eds

# Rational interval source certificate. All elementary interval endpoints are
# exact Fractions, rounded outwards to dyadics. sqrt uses integer isqrt.
# log uses range reduction and the positive atanh series with a proven tail.
BITS=100; SCALE=1<<BITS; LOG_TERMS=34
def lower(x): return F((x.numerator*SCALE)//x.denominator,SCALE)
def upper(x): return -lower(-x)
class Interval:
    def __init__(self,lo,hi=None):
        lo=F(lo);hi=lo if hi is None else F(hi)
        if lo>hi: raise ArithmeticError('reversed interval')
        self.lo=lower(lo);self.hi=upper(hi)
    def __add__(self,other):
        other=as_iv(other);return Interval(self.lo+other.lo,self.hi+other.hi)
    __radd__=__add__
    def __neg__(self): return Interval(-self.hi,-self.lo)
    def __sub__(self,other): return self+-as_iv(other)
    def __rsub__(self,other): return as_iv(other)+-self
    def __mul__(self,other):
        other=as_iv(other);x=[self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi]
        return Interval(min(x),max(x))
    __rmul__=__mul__
    def __truediv__(self,other):
        other=as_iv(other)
        if other.lo<=0<=other.hi: raise ArithmeticError('interval division through zero')
        return self*Interval(1/other.hi,1/other.lo)
    def __rtruediv__(self,other): return as_iv(other)/self
    def __pow__(self,n):
        if n<0: return Interval(1)/(self**(-n))
        out=Interval(1)
        for _ in range(n): out=out*self
        return out
    def sqrt(self):
        if self.lo<0: raise ArithmeticError('sqrt of negative lower bound')
        def root_down(q): return F(isqrt((q.numerator<<(2*BITS))//q.denominator),SCALE)
        lo=root_down(self.lo);hi=root_down(self.hi)
        if hi*hi<self.hi: hi+=F(1,SCALE)
        return Interval(lo,hi)
    def log(self):
        if self.lo<=0: raise ArithmeticError('log of nonpositive lower bound')
        lo=log_fraction(self.lo);hi=log_fraction(self.hi)
        return Interval(lo.lo,hi.hi)
    def receipt(self):
        return {'lower_fraction':str(self.lo),'upper_fraction':str(self.hi),
                'lower_decimal':str(mp.mpf(self.lo.numerator)/self.lo.denominator),
                'upper_decimal':str(mp.mpf(self.hi.numerator)/self.hi.denominator)}
def as_iv(x): return x if isinstance(x,Interval) else Interval(x)
def log_unit(q):
    # 1 <= q <= 2. y in [0,1/3] gives a one-sided explicit remainder.
    y=(q-1)/(q+1);y2=y*y;term=y;total=F(0)
    for n in range(LOG_TERMS):
        total+=term/F(2*n+1);term*=y2
    remainder=2*term/F(2*LOG_TERMS+1)/(1-y2)
    return Interval(2*total,2*total+remainder)
LN2=log_unit(F(2))
@lru_cache(None)
def log_fraction(q):
    m=0
    while q<1: q*=2;m-=1
    while q>2: q/=2;m+=1
    return log_unit(q)+m*LN2
@lru_cache(None)
def algebraic_iv(expr):
    expr=s.sympify(expr)
    if expr.is_Rational: return Interval(F(int(expr.p),int(expr.q)))
    if expr.is_Add: return sum((algebraic_iv(a) for a in expr.args),Interval(0))
    if expr.is_Mul:
        out=Interval(1)
        for a in expr.args: out*=algebraic_iv(a)
        return out
    if expr.is_Pow:
        base,exponent=expr.args
        if exponent.is_Integer: return algebraic_iv(base)**int(exponent)
        if exponent==R(1,2): return algebraic_iv(base).sqrt()
        if exponent==-R(1,2): return 1/algebraic_iv(base).sqrt()
    raise ArithmeticError('unsupported exact algebraic expression '+str(expr))

ti=3-algebraic_iv(s.sqrt(5));Zi=algebraic_iv(16/h)
Ap=Interval(0)
for group in classes.values():
    for ev,dev,mult in spectra[group[0]]:
        if ev==0: continue
        ei=algebraic_iv(ev);dei=algebraic_iv(dev)
        Ap+=len(group)*mult*dei*(ei.log()+1)
delta_log_source=Interval(0);age_source_iv=Interval(0)
for ev,dev,mult in spectra[0]:
    ei=algebraic_iv(ev);dei=algebraic_iv(dev)
    delta_log_source+=mult*dei*(ti*ei/(2-ti*ei)).log()
    q=1/(Zi*ei);dq=-q*dei/ei
    B=1-ti*ei;dB=-ti*dei
    surv=B*B;dsurv=2*B*dB
    hb=-surv*surv.log()-(1-surv)*(1-surv).log()
    age_source_iv+=mult*(dq*hb+q*((1-surv)/surv).log()*dsurv)
conditional_source_iv=(ti*ti/Zi)*delta_log_source-(2*ti/Zi)*Ap
fine_gain_iv=conditional_source_iv+age_source_iv
check(conditional_source_iv.lo>F(5029,1000000) and conditional_source_iv.hi<F(5030,1000000),
      'exact rational interval: native K1 fine|age source lies in (0.005029, 0.005030)')
check(age_source_iv.hi<0,'exact rational interval: native K1 age gain source is negative')
check(fine_gain_iv.lo>0,'exact rational interval: native K1 fullfine gain source is positive')
check(conditional_source_iv.hi-conditional_source_iv.lo<F(1,10**23),
      'exact rational interval fine|age source width below 1e-23')
result={'scope':'independent original K1 fullfine/age source; owned stationary block identity consumed',
        'r':str(r),'nu':str(nu),'dnu_v':str(dn),'h':str(h),'hr':str(hr),
        'native_constructor_blob':'ee8de4635d24c668949ac9a0186616ab7d59f2ed',
        'exact_spectral_classes_with_v_jets':list(classes.values()),
        'live_rows':len(spectra),'physical_rows':64,'physical_ports_per_row':2,
        'initial_entropy':str(S0),'initial_source':str(dS0),
        'fine_CQ':str(Sf),'fine_CQ_source':str(dSf),
        'fine_gain':str(Sf-S0),'fine_gain_source':str(dSf-dS0),
        'age_CQ':str(Sb+Sa),'age_CQ_source':str(dSb+dSa),
        'age_gain':str(Sb+Sa-S0),'age_gain_source':str(dSb+dSa-dS0),
        'conditional_fine_given_age_DATA':str(Sf-Sb-Sa),
        'conditional_fine_given_age_DATA_source':str(dSf-dSb-dSa),
        'conditional_source_interval':conditional_source_iv.receipt(),
        'age_gain_source_interval':age_source_iv.receipt(),
        'fine_gain_source_interval':fine_gain_iv.receipt(),
        'row_entropy_derivative_interval':Ap.receipt(),
        'interval_method':{'dyadic_bits':BITS,'log_atanh_terms':LOG_TERMS,
                           'all_endpoints':'fractions.Fraction; outward-rounded arithmetic',
                           'sqrt':'integer isqrt with explicit upper endpoint',
                           'log':'range reduction plus positive atanh series and analytic tail'},
        'row_details':detailed,'checks_passed':len(checks),'checks':checks,
        'arithmetic':'exact rational/quadratic-field matrix identities and rational interval source proof; independent 75 decimal evaluation',
        'interval_certificate':True,'physical_Book03_Info_selected':False,'GR_closed':False}
encoded=json.dumps(result,indent=2)+'\n'
if args.json is not None:
    args.json.write_text(encoded)
print(encoded,end='')
