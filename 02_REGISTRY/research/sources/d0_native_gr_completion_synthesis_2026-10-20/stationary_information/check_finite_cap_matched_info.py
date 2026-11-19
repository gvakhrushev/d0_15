#!/usr/bin/env python3
"""Exact finite geometric identities; read-only stdout, no assert statements."""
import json
import sympy as s

def need(test, label):
    if not bool(test):
        raise RuntimeError(label)

x,q,A,B,r=s.symbols('x q A B r', real=True)
t=s.symbols('t',real=True)
c,z=s.Rational(3,5),s.Rational(4,5)
f0,f1=1-2*t*t,2*t*(1-t*t)
alpha0=c*f0-z*f1
alpha1=z*f0+c*f1
xt=c*alpha0
dt=1-xt
q0=z*z
checked=[]
for N in (1,2,3,7,12):
    # Generic finite sums prove coefficients independently of branch values.
    EN=sum((1-q)**j for j in range(N))
    need(s.expand(q*EN-(1-(1-q)**N))==0,'finite survival sum')
    success=sum(q*(1-q)**j for j in range(N))
    fail=sum(j*q*(1-q)**j for j in range(N))+N*(1-q)**N
    need(s.expand(success-q*EN)==0,'success coefficient includes stopping')
    need(s.expand(fail-(1-q)*EN)==0,'failure coefficient includes abort')
    fullKL=success*A+fail*B
    need(s.expand(fullKL-EN*(q*A+(1-q)*B))==0,'full finite KL sum')

    # Generic finite overlap with s alpha1=d-2t² and d=1-x.
    overlap=sum(((1-x)-2*t*t)*x**j for j in range(N))+x**N
    expected=1-2*t*t*sum(x**j for j in range(N))
    need(s.expand(overlap-expected)==0,'finite overlap plus abort')
    actual=1-2*t*t*sum(xt**j for j in range(N))
    en0=EN.subs(q,q0)
    need(s.simplify(s.diff(actual,t,2).subs(t,0)+4*en0)==0,'finite QFI')
    stage=q0*s.log(q0/alpha1**2)+(1-q0)*s.log((1-q0)/alpha0**2)
    need(s.simplify(s.diff(en0*stage,t,2).subs(t,0)-16*en0)==0,'finite reverse KL second derivative')
    dirtysum=sum(r*B**j for j in range(N))
    need(s.expand((1-B)*dirtysum-r*(1-B**N))==0,'complete first-dirty sum')
    checked.append(N)

print(json.dumps({'status':'PASS','finite_caps_checked':checked,
 'overlap':'1-2t^2 sum_(j<N)(c alpha0)^j',
 'QFI':'16 E_N dt tensor dt',
 'reverse_KL':'E_N [q ln(q/alpha1^2)+(1-q)ln((1-q)/alpha0^2)]/ln(phi)',
 'abort':'retained exactly','scope':'different capped task, no Book binding'},indent=2))
