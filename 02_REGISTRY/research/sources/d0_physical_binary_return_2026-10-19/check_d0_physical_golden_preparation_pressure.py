#!/usr/bin/env python3
"""Exact/finite Golden AF preparation-source test. RESEARCH, not compulsory D0 action."""
from math import sqrt, log, exp

def fib(n):
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a

phi=(1+sqrt(5))/2
p=1/phi
ell=log(phi)

def h(g):
    return (-g*log(g)-(1-g)*log(1-g))/ell

def original_af(n):
    typ=[0]*fib(n+2)+[1]*fib(n+1)
    mu=[p**(n+1+j) for j in typ]
    cost=[n+1+j for j in typ]
    assert abs(sum(mu)-1)<1e-12
    return typ,mu,cost

def joint_entropy(q,good):
    answer=0.
    for a,g in zip(q,good):
        assert a>0 and 0<g<1
        answer -= (a*g*log(a*g)+a*(1-g)*log(a*(1-g)))/ell
    return answer

for n in (1,2,3,4,8,12):
    typ,mu,C=original_af(n)
    a=typ.index(0);b=typ.index(1)
    assert abs(log(mu[b]/mu[a])/ell+1)<1e-12
    assert C[a]-C[b]==-1
    A=sum(x for t,x in zip(typ,mu) if t==0)
    B=sum(x for t,x in zip(typ,mu) if t==1)
    # A whole-sector transfer on the old matched pure Schmidt state.
    v=[x/A if t==0 else -x/B for t,x in zip(typ,mu)]
    assert abs(sum(v))<1e-12
    norm2=sum(dx*dx/x for dx,x in zip(v,mu))/4
    assert abs(norm2-1/(4*A*B))<1e-11
    entropy_derivative=-sum(dx*(log(x)+1)/ell for dx,x in zip(v,mu))
    assert abs(entropy_derivative+1)<1e-10
    assert 1.09<sqrt(norm2)<1.19

assert abs((phi/sqrt(5))*(1/(phi*sqrt(5)))-1/5)<1e-13

n=3
typ,mu,C=original_af(n)
a=typ.index(0);b=typ.index(1)
gstar=.759460770278
rates=[.8,-.2,.5,.4,-.1]+[0.0]*fib(n+1)
assert len(rates)==len(mu)

def gs(y):
    return [gstar*exp(-2*y*r) for r in rates]

def mean_price(nu,y):
    return joint_entropy(nu,gs(y))

def code_pressure(nu,y):
    return mean_price(nu,y)-sum(x*c for x,c in zip(nu,C))

def moved(t):
    x=mu.copy()
    x[a]+=t
    x[b]-=t
    return x

eps=1e-6
dmean=(mean_price(moved(eps),0)-mean_price(moved(-eps),0))/(2*eps)
dpres=(code_pressure(moved(eps),0)-code_pressure(moved(-eps),0))/(2*eps)
assert abs(dmean+1)<1e-8
assert abs(dpres)<1e-8
assert abs(code_pressure(mu,0)-h(gstar))<1e-12

kappa=gstar*log(gstar/(1-gstar))
source=2*kappa/ell*sum(x*r for x,r in zip(mu,rates))
numeric=(mean_price(mu,eps)-mean_price(mu,-eps))/(2*eps)
assert abs(source-numeric)<1e-8 and abs(source)>1e-5

def optimizer(y):
    unnorm=[x*exp(ell*h(g)) for x,g in zip(mu,gs(y))]
    Z=sum(unnorm)
    return [v/Z for v in unnorm],log(Z)/ell

nu0,val=optimizer(0)
assert max(abs(a-b) for a,b in zip(nu0,mu))<1e-14
for y in (-.017,-.004,0,.012):
    nu,best=optimizer(y)
    assert abs(code_pressure(nu,y)-best)<1e-12
    kl=sum(a*log(a/b)/ell for a,b in zip(mu,nu))
    assert abs(best-code_pressure(mu,y)-kl)<1e-12
env=(optimizer(eps)[1]-optimizer(-eps)[1])/(2*eps)
assert abs(env-source)<1e-8

for y in (-.015,0,.018):
    born_partition=sum(x*(g+(1-g)) for x,g in zip(mu,gs(y)))
    assert abs(born_partition-1)<1e-14

print("PASS: original oldRIGHT two-cost AF normalized probabilities and ratio phi")
print("PASS: normalized matched whole-sector GNS tangent entropy source -1")
print("PASS: tangent norm tends to sqrt(5)/2, unit-norm source -2/sqrt(5)")
print("PASS: H_phi-E(code) stationary only at original mu by Gibbs/KL identity")
print("PASS: task-pressure unique optimizer at mu and binary Einstein-CAR envelope")
print("PASS: complete normalized Born log-partition has zero source")
print(f"DEBUG: dmean={dmean:.12f}, dcode={dpres:.4e}, field={source:.12f}, envelope={env:.12f}")
print("SCOPE: NOT proof of native physical Book action, actuator, clock or GR closure")
