#!/usr/bin/env python3
import sympy as s
p=(s.sqrt(5)-1)/2; phi=1/p
r=s.symbols('r',positive=True)
H=-(r*s.log(r)+(1-r)*s.log(1-r))/s.log(phi)
g=1+r-H
def eq(a,b):
    if s.simplify(a-b)!=0: raise ArithmeticError((a,b))
eq(p*p+p,1)
eq(s.diff(g,r).subs(r,s.Rational(1,2)),1)
eq(s.simplify(s.diff(g,r).subs(r,p*p)),0)
eq(s.diff(g,r,2),1/(s.log(phi)*r*(1-r)))
t1,t2,d1,d2=s.symbols('t1 t2 d1 d2',real=True)
prob=s.Rational(1,2)+(t1*d1+t2*d2)/4
subs={t1:s.Rational(1,2),t2:-s.Rational(1,4),d1:s.Rational(1,3),d2:s.Rational(2,3)}
eq(prob.subs(subs),s.Rational(1,2))
eq(s.diff(prob,t1).subs(subs),s.Rational(1,12))
eq((s.diff(g,r).subs(r,prob)*s.diff(prob,t1)).subs(subs),s.Rational(1,12))
print("PASS: true Golden stationary probability, strict convexity and missing 1/12 writer source")
