#!/usr/bin/env python3
"""Narrow exact algebraic controls for conditional Book03 Born aggregation."""
import json
import sympy as S
p=(S.sqrt(5)-1)/2
phi=1/p
z=S.Rational(1,2**20)
L=4*p**3
Q=1-z*L
R=1-z*L*(1+p**6)
r=1-Q*R
rp=4*z*Q*p**11
def check(ok,label):
    if not bool(ok): raise ArithmeticError(label)
check(S.simplify(p**2+p-1)==0,"Golden p")
check(0<float(r)<.5 and float(rp)>0,"genuine moving cap-one report")
gap=rp*S.log((1-r)/r)/(2*S.log(phi))
check(abs(float(S.N(gap,55))-2.6290078337537537e-7)<2e-19,"native source gap")
costs=[S.Rational(0),S.Rational(1),S.Rational(3,2)]
weights=[phi**(-v) for v in costs]
Z=sum(v*v for v in weights)
q=[v*v/Z for v in weights]
H=-sum(v*S.log(v)/S.log(phi) for v in q)
A=-S.log(Z)/(2*S.log(phi))
mean=sum(v*c for v,c in zip(q,costs))
check(abs(float(S.N(mean-H/2-A,60)))<1e-40,"exact half entropy identity")
t=[S.Rational(1,2),S.Rational(1,3),S.Rational(1,6)]
F=sum(v*c for v,c in zip(t,costs))+sum(v*S.log(v)/S.log(phi) for v in t)/2
D=sum(v*S.log(v/q0)/S.log(phi) for v,q0 in zip(t,q))
check(abs(float(S.N(F-A-D/2,60)))<1e-40,"exact relative entropy identity")
check(float(S.N(D))>0,"strict relative entropy")
alpha=S.Symbol("alpha",positive=True)
check(S.solve(S.Eq(1/alpha,2),alpha)==[S.Rational(1,2)],"unique coefficient")
print(json.dumps({"status":"PASS","q_cap1":str(S.N(r,28)),
"query_first_source_gap":str(S.N(gap,28)),
"born_coefficient":"1/2",
"full128_port_split_fixed":True,
"full128_fine_record_asymptotic_owned_not_replayed":True,
"physical_book03_selected":False,"GR_closed":False},indent=2,sort_keys=True))
