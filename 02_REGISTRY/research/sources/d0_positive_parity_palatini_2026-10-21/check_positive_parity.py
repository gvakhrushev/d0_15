#!/usr/bin/env python3
"""Exact positive-parity reporter algebra and measured-cut negative control."""
import sympy as S
p=(S.sqrt(5)-1)/2
m=2; K=S.Integer(4)
ds=[S.Rational(1,3),S.Rational(2,3)]
cs=[S.Integer(2),-S.Integer(1)]
def c(ok,msg):
    if not bool(ok): raise ArithmeticError(msg)
q=0
for d,a in zip(ds,cs):
    for x in (-1,1):
        for b in (-1,1):
            v=(1+x*d)*(1+b*a/K)/(4*m)
            c(v>=0,"positive")
            if x*b==1:q+=v
target=S.Rational(1,2)+sum(a*d for a,d in zip(cs,ds))/(2*m*K)
c(S.simplify(q-target)==0,"parity exact")
n=4
Sstar=2*4**n*sum(a*d for a,d in zip(cs,ds))
c(S.simplify(q-S.Rational(1,2)-Sstar/(4**(n+1)*m*K))==0,"Palatini gain")
c(q==S.Rational(1,2),"fair null")
eps=S.symbols("eps")
v=lambda A,D:S.Rational(1,2)+(A*D+cs[1]*ds[1])/(2*m*K)
c(S.diff(v(cs[0]+eps,ds[0]),eps).subs(eps,0)==ds[0]/(2*m*K),"coframe derivative")
c(S.diff(v(cs[0],ds[0]+eps),eps).subs(eps,0)==cs[0]/(2*m*K),"link derivative")
x=S.symbols("x",positive=True)
h=-(x*S.log(x)+(1-x)*S.log(1-x))/S.log(1/p)
c(S.simplify(S.diff(h,x).subs(x,S.Rational(1,2)))==0,"terminal entropy derivative")
d=S.symbols("d",positive=True)
HX=-((1+d)/2*S.log((1+d)/2)+(1-d)/2*S.log((1-d)/2))/S.log(1/p)
c(S.diff(HX,d).subs(d,S.Rational(1,2))!=0,"fully measured entropy extra")
print("PASS: parity positivity, original curvature gain, full geometric jets, information cut counterexample")
