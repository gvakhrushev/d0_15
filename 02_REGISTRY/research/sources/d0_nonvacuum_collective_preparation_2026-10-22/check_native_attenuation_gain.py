#!/usr/bin/env python3
"""Exact original ten-flag report bound and physical signal normalization.

This is a new bounded consumer of the published Golden table. It does not
rerun the geometric full42 root, any compiler, or any full Book action.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from decimal import Decimal, localcontext
import json

@dataclass(frozen=True)
class F:
    a: Q = Q(0)
    b: Q = Q(0)
    def __post_init__(self):
        object.__setattr__(self, 'a', Q(self.a))
        object.__setattr__(self, 'b', Q(self.b))
    @staticmethod
    def cast(x):
        return x if isinstance(x, F) else F(x)
    def __add__(self, other):
        o=F.cast(other); return F(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return F(-self.a,-self.b)
    def __sub__(self, other): return self+-F.cast(other)
    def __rsub__(self, other): return F.cast(other)+-self
    def __mul__(self, other):
        o=F.cast(other)
        return F(self.a*o.a+self.b*o.b,
                 self.a*o.b+self.b*o.a-self.b*o.b)
    __rmul__=__mul__
    def inverse(self):
        n=self.a*self.a-self.a*self.b-self.b*self.b
        if not n: raise ZeroDivisionError
        return F((self.a-self.b)/n,-self.b/n)
    def __truediv__(self, other): return self*F.cast(other).inverse()
    def __rtruediv__(self, other): return F.cast(other)*self.inverse()
    def __pow__(self, n):
        if n<0: return self.inverse()**(-n)
        out=F(1); base=self
        while n:
            if n&1: out=out*base
            base=base*base; n//=2
        return out
    def sign(self):
        # 2(a+b p)=(2a-b)+b sqrt(5), with exact rational comparison.
        a,b=2*self.a-self.b,self.b
        sa=(a>0)-(a<0); sb=(b>0)-(b<0)
        if not sa: return sb
        if not sb or sa==sb: return sa
        return sa if a*a>5*b*b else sb
    def __lt__(self,o): return (self-F.cast(o)).sign()<0
    def __le__(self,o): return (self-F.cast(o)).sign()<=0
    def __abs__(self): return self if self.sign()>=0 else -self
    def real(self):
        # Q(p) coefficients can be large conjugates with severe cancellation.
        # Embed at adaptive precision before formatting a float diagnostic.
        digits=max(len(str(abs(v))) for v in
                   (self.a.numerator,self.a.denominator,
                    self.b.numerator,self.b.denominator))
        with localcontext() as ctx:
            ctx.prec=2*digits+60
            pp=(Decimal(5).sqrt()-1)/2
            return float(Decimal(self.a.numerator)/Decimal(self.a.denominator)
                         +Decimal(self.b.numerator)/Decimal(self.b.denominator)*pp)
    def record(self): return {'a':str(self.a),'b':str(self.b)}

p=F(0,1); zeta=F(Q(1,2**20)); d=F(Q(1,64))
checks=0
def check(ok,label):
    global checks
    if not ok: raise AssertionError(label)
    checks+=1

def report(z,alpha_u,alpha_v):
    x=[F(zi)*(alpha_u if i<2 else alpha_v) for i,zi in enumerate(z)]
    l=4*p**2*(1+d*x[0])*(1-p**2*(1+d*x[1]))
    def btable(start):
        b=[p-p**2*d*x[start+j] for j in range(4)]
        return 4*b[0]*b[1]*(1-b[2]*b[3])
    b1,b2=btable(2),btable(6)
    a=l+(1-l)*b1
    return zeta*(a+b2)-zeta**2*a*b2

L0=4*p**3; M0=L0*(1+p**6)
Q0=1-zeta*L0; R0=1-zeta*M0
r0=1-Q0*R0
check(p*p+p==F(1),'Golden relation')
check(report((1,)*10,F(0),F(0))==r0,'all-off exact scalar reference')
check(F(0)<r0 and r0<2*zeta,'genuine rare report range')

# All 1024 eigenvalues of the actual diagonal pre-majority report effect,
# on an explicit admitted attenuation. Bounds below are analytic for every
# admitted alpha, including arbitrary correlated inputs.
depth=12; tau=p**depth; Lu,Lv=F(1),F(2)
au,av=64*Lu*tau,64*Lv*tau
check(F(0)<au and au<=1 and F(0)<av and av<=1,'real attenuation domain')
activity=1-(1-au)**2*(1-av)**8
union=2*au+8*av
check(activity<=union,'exact active-flag union bound')
max_delta=F(0); max_r=F(0); min_r=F(1)
for bits in product((-1,1),repeat=10):
    r=report(bits,au,av)
    check(F(0)<=r and r<=2*zeta,'actual full table effect range')
    delta=abs(r-r0)
    check(delta<=2*zeta*activity,'centered effect mixture bound')
    if max_delta<delta: max_delta=delta
    if max_r<r: max_r=r
    if r<min_r: min_r=r

# Original source coefficients, independently expanded from L, B, A.
Lx=4*p**2*(1-2*p**2)
By=-8*p**3*(1-2*p**2)
rx=zeta*Lx*(1-L0)*Q0
ry=zeta*By*((1-L0)*Q0+R0)
check(rx==4*zeta*p**11*Q0,'original geometric first-source gain')
check(ry/rx==-2*p**(-5)*(R0/Q0+p**6),'unchanged Einstein-CAR ratio')
check(F(0)<rx and ry<F(0),'nonzero opposite source signs')
C=128*zeta*(2*Lu+8*Lv)
check(2*zeta*union==tau*C,'linear tau factor is actual')
check(C/rx==32*(2*Lu+8*Lv)/(p**11*Q0),'signal factor cancels exactly')
for m in (12,20,40,80):
    tt=p**m; gu=64*Lu*tt; gv=64*Lv*tt
    activity_m=1-(1-gu)**2*(1-gv)**8
    check(F(0)<gu and gu<=1 and gv<=1,'deep Golden attenuation admitted')
    check(2*zeta*activity_m<=tt*C,'all four true-depth bounds')
    # No inference of cheap statistics: only the SOURCE ratio cancels.
    check((tt*C)/(tt*rx)==C/rx,'normalized source bound independent of depth')

receipt={
    'status':'PASS','exact_arithmetic':'Q(p), p^2+p-1=0',
    'exact_checks':checks,'actual_sign_columns':1024,
    'depth':depth,'Lambda_u':1,'Lambda_v':2,
    'r0':r0.record(),'r_x0':rx.record(),'r_y0':ry.record(),
    'report_range_diagnostic':[min_r.real(),max_r.real()],
    'actual_centered_norm_diagnostic':max_delta.real(),
    'linear_bound_diagnostic':(tau*C).real(),
    'actual_signal_ratio_bound':(C/rx).real(),
    'floating_diagnostics_are_not_certificates':True,
    'complete_Book_source_selected':False,'GR_closed':False,
}
print(json.dumps(receipt,indent=2))
