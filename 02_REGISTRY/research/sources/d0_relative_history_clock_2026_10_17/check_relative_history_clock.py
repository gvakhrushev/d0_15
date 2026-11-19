"""Finite matched-clock KL diagnostic, native radial exit marginal and 128-label chain test."""
import math
p=(math.sqrt(5)-1)/2
beta=2*p*p
d=0.063635191594344535

def kl(u,v):
    return u*math.log(u/v)+(1-u)*math.log((1-u)/(1-v))

def radial(L,t):
    eps=p*p/(64*L*L);n=128*L*L; lam=4*L*L*math.sin(math.pi/L)**2*d*(1+t)
    q=eps*lam*(1-eps*lam/4)
    return n,eps,q

expected=beta*4*math.pi**2*d*((1.1)*math.log(1.1)-.1)
for L in [8,16,32,64,128,256]:
    n,eps,q0=radial(L,0)
    _,_,q1=radial(L,.1)
    observed=n*kl(q1,q0)
    assert abs(observed-expected)<.001
    wrong=n*kl(q0,eps*eps*4*L*L*math.sin(math.pi/L)**2*d)
    assert wrong>observed
# 128 outcomes / nontrivial history-dependent mark probability: test KL chain identity.
eps=.01
weights=[(a+1)/sum(range(1,128)) for a in range(127)]
def probabilities(x,history):
    r=(1.4+.1*len([a for a in history if a]))*(1+.2*x)
    b=eps*r
    z=sum(weights[i]*(1+.1*x*((i+len(history))%4)) for i in range(127))
    return [1-b]+[b*weights[i]*(1+.1*x*((i+len(history))%4))/z for i in range(127)]
p0=probabilities(1,());q0=probabilities(0,())
D0=sum(a*math.log(a/b) for a,b in zip(p0,q0))
D2=0.;chain=D0
for a in range(128):
    P=probabilities(1,(a,));Q=probabilities(0,(a,))
    chain+=p0[a]*sum(u*math.log(u/v) for u,v in zip(P,Q))
    for b in range(128):
        r=p0[a]*P[b];s=q0[a]*Q[b]
        D2+=r*math.log(r/s)
assert abs(D2-chain)<1e-12, (D2,chain)
print('checks=matched_clock,wrong_clock,full_128_label_chain; status=PASS')
print('KL limit t=.1:',round(expected,12),'2-round error:',round(D2-chain,16))
