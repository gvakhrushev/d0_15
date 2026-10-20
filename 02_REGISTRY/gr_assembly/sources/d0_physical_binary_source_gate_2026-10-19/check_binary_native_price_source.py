#!/usr/bin/env python3
"""Physical binary return/Book-price source check. Research-only, no GR closure."""
import math
phi=(1+math.sqrt(5))/2
p=1/phi
logphi=math.log(phi)
d=1056
L=4*p**3

def leaf_g(k):
    w=p**(2*k)
    return ((1-w*(1+L))*(1-w*(1+L*(1+p**6))))**d

def gmin(k):
    return (1-2*p**(2*k))**(2*d)

def matter_ratio(k):
    r=p**(2*k)/(1-p**(2*k))
    Q=1-r*L;R=1-r*L*(1+p**6)
    return 2/p**5*(R/Q+p**6)

assert gmin(9)<.5<gmin(10)
assert abs(leaf_g(10)-.759460770278)<1e-11
assert abs(matter_ratio(10)-23.416330696075)<1e-10

def fib(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

N=3
n0=fib(N+2);n1=fib(N+1);K=fib(2*N+9);D0=fib(N+8)
mu=[p**(N+1)]*n0+[p**(N+2)]*n1
assert abs(sum(mu)-1)<1e-13
pi0=D0/K
chi=K*p**(N+1)/D0
assert abs(mu[0]-chi*pi0)<1e-13

g0=leaf_g(10)
rates=[.8,-.2,.5,.4,-.1]+[0.]*n1
prep_vel=[-.7,.1,.4,-.2,.8,-.1,.3,-.5]
assert len(mu)==len(rates)==len(prep_vel)
Jtrace_deriv=K*pi0*sum(rates[:n0])
sum_mu_dJ=sum(u*v for u,v in zip(mu,rates))
assert abs(sum_mu_dJ-chi/K*Jtrace_deriv)<1e-12

def process(t):
    wt=[u*math.exp(t*v) for u,v in zip(mu,prep_vel)]
    total=sum(wt);wt=[u/total for u in wt]
    gs=[g0*math.exp(-2*t*v) for v in rates]
    assert all(0<g<1 for g in gs)
    contrast=sum(u*math.log((1-g)/g)/logphi for u,g in zip(wt,gs))
    mode=sum(-u*math.log(g)/logphi for u,g in zip(wt,gs))
    entropy=sum(u*(-g*math.log(g)-(1-g)*math.log(1-g))/logphi
                for u,g in zip(wt,gs))
    full=entropy-sum(u*math.log(u)/logphi for u in wt)
    return contrast,mode,entropy,full

eps=1e-6
found=[(x-y)/(2*eps) for x,y in zip(process(eps),process(-eps))]
kappa=g0*math.log(g0/(1-g0))
expected=[2/((1-g0)*logphi)*sum_mu_dJ,
          2/logphi*sum_mu_dJ,
          2*kappa/logphi*sum_mu_dJ]
for x,y in zip(found,expected): assert abs(x-y)<5e-8,(x,y)
vbar=sum(u*v for u,v in zip(mu,prep_vel))
dmu=[u*(v-vbar) for u,v in zip(mu,prep_vel)]
prep_entropy_source=-sum(du*math.log(u)/logphi for du,u in zip(dmu,mu))
assert abs(found[3]-(expected[2]+prep_entropy_source))<5e-8
assert abs(prep_entropy_source)>1e-5
moving_log_book_normalizer=.27
assert abs(found[3]-(found[3]-moving_log_book_normalizer/logphi))>.5

print("PASS: full Golden binary task, actual fixed oldRIGHT and moving preparation")
print("PASS: 3 operator source readings, signed entropy, nonzero prep and Book N")
print(f"g10={g0:.12f}, kappa={kappa:.12f}, lambda={matter_ratio(10):.12f}")
print("OPEN: physical admission, full Book price/normalizer, clocks and GR")
