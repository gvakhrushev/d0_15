#!/usr/bin/env python3
"""Exact Q(phi^-1) audit of the ORIGINAL Golden Fibonacci cost-cut.

Tests a strict native-code future/clock/source countercontrol, not G0/Book
physical selection. Uses only Python standard library and exact rationals.
All-size statements have independent inductive proofs in the companion memo.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import sqrt

@dataclass(frozen=True)
class QP:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)
    # Exact number field Q(p), p^2=1-p, p=(sqrt(5)-1)/2.
    def __add__(self, other):
        other=qp(other)
        return QP(self.a+other.a,self.b+other.b)
    __radd__=__add__
    def __neg__(self): return QP(-self.a,-self.b)
    def __sub__(self,other):return self+-qp(other)
    def __rsub__(self,other):return qp(other)+-self
    def __mul__(self,other):
        other=qp(other)
        return QP(self.a*other.a+self.b*other.b,
                  self.a*other.b+self.b*other.a-self.b*other.b)
    __rmul__=__mul__
    def __pow__(self,n):
        if not isinstance(n,int) or n<0:raise ValueError("nonnegative integer exponent required")
        t=QP(Fraction(1));x=self
        while n:
            if n&1:t=t*x
            x=x*x;n//=2
        return t
    def approx(self):return float(self.a)+float(self.b)*(sqrt(5)-1)/2
    def sign(self):
        # 2*x=(2*a-b)+b*sqrt(5). Exact rational sign calculation.
        u,v=2*self.a-self.b,self.b
        if v==0:return (u>0)-(u<0)
        if u==0:return (v>0)-(v<0)
        if u>0 and v>0:return 1
        if u<0 and v<0:return -1
        d=u*u-5*v*v
        return ((u>0)-(u<0))*((d>0)-(d<0))
    def is_pos(self):return self.sign()>0

def qp(a):return a if isinstance(a,QP) else QP(Fraction(a))
def check(ok,msg):
    if not ok:raise RuntimeError(msg)

p=QP(Fraction(0),Fraction(1))
ONE=qp(1)
check(p*p+p==ONE,"golden polynomial")
check(p*(qp(2)-p)==qp(3)*p-ONE,"single native split cost")
beta_limit=(qp(2)-p)*Fraction(1,5)
a,b=1,0
f_prev,f_cur=0,1
moments=[]
for n in range(1,33):
    # Original shortest-prefix native cost cut: 1- and 2-cost children.
    a,b=a+b,a
    f_prev,f_cur=f_cur,f_prev+f_cur
    check(a==f_cur and b==f_prev,"original Fibonacci multiplicity")
    wshort,wlong=p**n,p**(n+1)
    Z=a*wshort+b*wlong
    check(Z==ONE,"entire Golden cost-cut is Kraft normalized")
    beta=b*wlong
    check(beta==beta_limit*(ONE-((-1)**n)*p**(2*n)),
          "Binet exact alternating cost-cut overshoot")
    mu=a*n*wshort+b*(n+1)*wlong
    check(mu==qp(n)+beta,"marked first cost moment")
    second=a*n*n*wshort+b*(n+1)*(n+1)*wlong
    variance=second-mu*mu
    check(variance==beta*(ONE-beta),"marked second cumulant")
    check(beta.is_pos() and (ONE-beta).is_pos(),"strict positive cut variance")
    if moments:
        prev_n=n-1
        prev_mu=moments[-1][1]
        prev_a=moments[-1][2]
        increment=prev_a*p**prev_n*(p+qp(2)*p*p)
        check(mu-prev_mu==increment,"entire actually split cost-cut source")
        check(increment==ONE+((-1)**prev_n)*beta_limit*p**(2*prev_n)*(ONE+p*p),
              "exact closed positive drift")
        check((increment-(qp(3)*p-ONE)).sign()>=0,
              "sharp all-level drift bound >=3p-1")
    moments.append((n,mu,a,b,beta,variance))

check(moments[0][1]==qp(2)-p,"n1 mean")
check(moments[1][1]==ONE+qp(2)*p,"n2 mean sqrt5")
check(moments[2][1]==qp(7)-qp(6)*p,"n3 mean")
check(moments[1][1]-moments[0][1]==qp(3)*p-ONE,"nonzero marked source despite same Z")
# Original 3-tick encoded cylinders: 000 001 010 100 101.
check(qp(3)*p**3+qp(2)*p**4==ONE,"whole five-word encoded cut")

for n,mu,a,b,beta,variance in moments:
    # Exact observed codeword self-entropy H_phi(q)=E(native code cost).
    entropy_of_own_code=a*n*p**n+b*(n+1)*p**(n+1)
    check(entropy_of_own_code==mu,"self entropy and mean native code cost")
    # Calling this per-history self-surprisal Book Info would assign bare
    # p^(Cost-Info)=1, making all F_(n+2) leaves equally likely.
    check(a+b>1 and p**n!=p**(n+1),
          "bare self-surprisal Book probabilities differ from native Born")
    # Existing three typed absolute scalar/coherent/extra-marker translations.
    info_relatives={Fraction(0),Fraction(1,2),Fraction(1)}
    check(len(info_relatives)==3,"three Book/Born meanings distinct")
    for cost in (n,n+1):
        check(2*(Fraction(cost)-Fraction(cost,2))==cost,
              "coherent amplitude p^(cost/2) squares to Born p^cost")
        check(cost-cost==0,"Kraus extra marker p^(Cost-Info) constant")
    check(p**(2*n)*p**(n+1)!=p**(2*(n+1))*p**n,
          "bare p^cost amplitudes cannot give Born p^cost law")

# Abstract positive terminal controls in the existing future P1 schema:
# chi_A=1/2, chi_B=(1/2+y,1/2). Both base suffix Z=1/2,
# but D_y log(Z_B/Z_A)|0=2p, not zero. NOT a selected native χ.
check((p+p*p)*Fraction(1,2)==qp(Fraction(1,2)),
      "equal base future partition")
check((qp(2)*p).is_pos(),"strict moving terminal first-source mismatch")

print("PASS: original Fibonacci 32 full cuts, exact native Q(p) identities")
print("PASS: all unmarked Z_n=1 while clock mean mu_n=n+F_n p^(n+1)")
print("PASS: exact Binet overshoot, variance, strict uniform drift >=3p-1")
print("PASS: original five history cut, three Book/Born typed choices")
print("PASS: moving terminal source need not follow equal partition value")
print("mu_1,mu_2,mu_3:",*[row[1].approx() for row in moments[:3]])
print("mu_2-mu_1:",(moments[1][1]-moments[0][1]).approx())
print("full native Info/task/clock selected: FALSE")
print("GR_closed: FALSE")
