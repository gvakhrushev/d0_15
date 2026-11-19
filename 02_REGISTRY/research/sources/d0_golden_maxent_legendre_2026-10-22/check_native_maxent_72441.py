#!/usr/bin/env python3
"""True original 72,441 Golden F/R complete records: Book06 max-entropy
site-conditioned extension, exact Kraft-KL Pythagorean and off-null MI.
No compulsory Book03 Info/field writer or full physical GR selection claimed.
"""
from collections import Counter
from math import sqrt, log, log1p, fsum, sin, cos
p=(sqrt(5)-1)/2
ell=log(1/p)
ref=lambda t: ((1-t)*log((1-t)/p)+t*log(t/(p*p)))/ell
h=lambda t: -(t*log(t)+(1-t)*log1p(-t))/ell
D=lambda u,v: fsum(q*log(q/s) for q,s in zip(u,v))/ell
exact=[]; overs=[]
def rec(n,j,L,W):
    if n>=20:
        if n==20: exact.append(tuple(min(3,int(4*(L[k]+W[k]/2))) for k in range(4)))
        else:overs.append(n)
        return
    ax=j%4
    wf=W.copy();wf[ax]*=p;rec(n+1,j+1,L.copy(),wf)
    wr=W.copy();lr=L.copy();lr[ax]+=p*wr[ax];wr[ax]*=p*p
    rec(n+2,j+1,lr,wr)
rec(0,0,[0.]*4,[1.]*4)
counts=Counter(exact)
assert len(exact)==10946 and len(overs)==6765 and set(overs)=={21}
assert len(counts)==256 and min(counts.values())==29 and max(counts.values())==78
r0=1.8512395785208469e-6
r={z:r0*(1+.22*sin(2.9*z[0]+1.3*z[2])+.075*cos(1.7*z[1]+2.3*z[3])) for z in counts}
P=[];Pstar=[];Pbar=[];mu=[];costs=[]
ready_mass=2*len(exact)*p**23
bar=fsum((v/len(exact))*r[z] for z,v in counts.items())
def emit(q,s,b,reference,c):
    P.append(q);Pstar.append(s);Pbar.append(b);mu.append(reference);costs.append(c)
for _ in overs:emit(p**21,p**21,p**21,p**21,21)
for z in exact:
    emit(p**22,p**22,p**22,p**22,22)
    emit(p**24,p**24,p**24,p**24,24)
    for sign in (+1,-1):
        t=r[z]*(1+.35*sign);v=r[z]
        for bit,ex,prior in ((0,1,p),(1,2,p*p)):
            emit(p**23*(t if bit else 1-t),p**23*(v if bit else 1-v),
                 p**23*(bar if bit else 1-bar),p**23*prior,23+ex)
assert len(P)==72441 and all(abs(fsum(q)-1)<1e-10 for q in (P,Pstar,Pbar,mu))
H=lambda a:-fsum(q*log(q) for q in a)/ell
C=lambda a:fsum(q*c for q,c in zip(a,costs))
delta=D(P,Pstar);dstar=D(Pstar,mu);dMI=D(Pstar,Pbar)
assert C(Pstar)==C(P) or abs(C(Pstar)-C(P))<1e-11
assert H(Pstar)>H(P)
assert abs(D(P,mu)-(delta+dstar))<2e-11
assert abs(D(P,mu)-(delta+dMI+D(Pbar,mu)))<2e-11
assert abs(dstar-ready_mass*fsum(v/10946*ref(r[z]) for z,v in counts.items()))<2e-11
assert abs(dMI-ready_mass*(h(bar)-fsum(v/10946*h(r[z]) for z,v in counts.items())))<2e-11
assert abs(C(Pstar)-H(Pstar)-dstar)<2e-11
assert delta>1e-8 and dMI>0
zi=min(counts);zj=max(counts,key=lambda z:abs(r[z]-r[zi]))
wi,wj=counts[zi]/10946,counts[zj]/10946
kp=lambda t:1-log((1-t)/t)/ell
assert wi*wj+wj*(-wi)==0
assert abs(ready_mass*wi*wj*(kp(r[zi])-kp(r[zj])))>1e-8
print('PASS true original 72,441 fine ends; 256 unequal site counts; maxentropy/KL nested exact')
print('native fine KL',dstar,'hidden-prefix surplus',delta,'site×bit MI',dMI)
print('GR_closed=false: conditional site task/Book03 path Info, heat, clock, oldRIGHT still OPEN')
