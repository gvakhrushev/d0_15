"""Rational enclosures, including logs; no floating-point sign certificate."""
from fractions import Fraction as Q
from math import isqrt
from dataclasses import dataclass
import json

BITS=72
TERMS=28

def sqrt_bounds(x):
    x=Q(x)
    if x<0: raise ValueError('negative square root')
    scale=1<<BITS
    n=isqrt((x.numerator*scale*scale)//x.denominator)
    lo=Q(n,scale)
    hi=lo if lo*lo==x else Q(n+1,scale)
    return lo,hi

def log_bounds(x):
    x=Q(x)
    if x<=0: raise ValueError('nonpositive logarithm')
    def series(y):
        z=(y-1)/(y+1)
        zz=z*z
        term=z; total=Q(0)
        for k in range(TERMS):
            total+=term/Q(2*k+1); term*=zz
        rem=2*abs(term)/(Q(2*TERMS+1)*(1-zz))
        return 2*total,2*total+rem
    k=0
    while x<1: x*=2; k-=1
    while x>=2: x/=2; k+=1
    lo,hi=series(x); l2,h2=series(Q(2))
    return (lo+k*l2,hi+k*h2) if k>=0 else (lo+k*h2,hi+k*l2)

@dataclass(frozen=True)
class I:
    lo:Q
    hi:Q=None
    def __post_init__(self):
        object.__setattr__(self,'lo',Q(self.lo))
        object.__setattr__(self,'hi',Q(self.lo if self.hi is None else self.hi))
        if self.lo>self.hi: raise ValueError('reversed interval')
    def __add__(self,o):
        o=as_i(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-as_i(o)
    def __rsub__(self,o):return as_i(o)+-self
    def __mul__(self,o):
        o=as_i(o);v=[x*y for x in (self.lo,self.hi) for y in (o.lo,o.hi)];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=as_i(o)
        if o.lo<=0<=o.hi: raise ValueError('zero denominator')
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return as_i(o)/self
    def __pow__(self,n):
        if n<0:return 1/(self**(-n))
        r=I(1)
        for _ in range(n):r=r*self
        return r
    def sqrt(self):return I(sqrt_bounds(self.lo)[0],sqrt_bounds(self.hi)[1])
    def log(self):return I(log_bounds(self.lo)[0],log_bounds(self.hi)[1])

def as_i(o):return o if isinstance(o,I) else I(o)

def derivative(j,e):
    p=(I(5).sqrt()-1)/2
    ell=-p.log()
    b=p**(3-j); v=p**(4-j)
    h=(2*b*e*(1-e)).sqrt()
    t=b*(1-e)+e/2
    dh=b*(1-2*e)/h
    probs=[t+h,t-h]+[b*(1-e)]*(1-j)+[v*(1-e)]*(2-j)
    deriv=[I(Q(1,2))-b+dh,I(Q(1,2))-b-dh]+[-b]*(1-j)+[-v]*(2-j)
    refs=[b,b]+[b]*(1-j)+[v]*(2-j)
    if min(P.lo for P in probs)<=0: raise ArithmeticError('support interval crossed')
    return sum((d*(P/r).log() for P,d,r in zip(probs,deriv,refs)),I(0))/ell

def certificate():
    L=Q(3,8);H=Q(25,64);N=16
    out=[]
    for j in (0,1):
        vals=[derivative(j,I(L+(H-L)*i/N,L+(H-L)*(i+1)/N)) for i in range(N)]
        lo=min(v.lo for v in vals);hi=max(v.hi for v in vals)
        # Publish simple exact bounds, checked against rational enclosures.
        target=(Q(2,5),Q(1)) if j==0 else (Q(3,2),Q(5,2))
        if not (lo>target[0] and hi<target[1]):
            raise ArithmeticError((j,float(lo),float(hi),target))
        out.append({'j':j,'strict_lower':str(target[0]),'strict_upper':str(target[1])})
    p=(I(5).sqrt()-1)/2
    if not (L<(p*p).lo<(p*p).hi<H):raise ArithmeticError('golden blank outside interval')
    return {'method':'Fraction interval arithmetic; rational square-root bounds; atanh logarithm with analytic tail',
            'effect_interval':[str(L),str(H)],'subintervals':N,'bits':BITS,'log_terms':TERMS,'derivative_bounds':out}

if __name__=='__main__':print(json.dumps(certificate(),sort_keys=True,indent=2))
