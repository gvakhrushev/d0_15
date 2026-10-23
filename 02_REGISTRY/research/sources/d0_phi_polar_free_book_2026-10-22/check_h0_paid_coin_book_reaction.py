#!/usr/bin/env python3
"""D0 #334, original nonflat unpadded N1 h0 80-digit Book J2 and Golden fair
coin RAW source. Original full42 interval root is consumed, NOT replayed.
Complete measured Golden Cost-Shannon is separately exactly neutral.
"""
from decimal import Decimal
from mpmath import iv
iv.dps=80
p=(iv.sqrt(5)-1)/2
z=iv.mpf(2)**-20
lp=iv.log(1/p)
roots=[('0.001370578581747874','-0.000016169093857131'),
       ('-0.000127665084908232','0.000005454102084650')]
def box(x):
    q=Decimal(x);d=Decimal('1e-12')
    return iv.mpf([str(q-d),str(q+d)])
def derivatives(x,y):
    E=p*p*(1+x);L=4*E*(1-E)
    b=p-p*p*y;B=4*b*b*(1-b*b);A=L+(1-L)*B
    By=-8*p*p*b*(1-2*b*b);Ay=(1-L)*By
    r=z*(A+B)-z*z*A*B
    ry=z*(Ay*(1-z*B)+By*(1-z*A))
    k=1-iv.log((1-r)/r)/lp
    j=528/(1-r)
    w=z*(Ay/(1-z*A)**2+By/(1-z*B)**2)/ry
    return r,ry,k,j,w
(r0,ry0,k0,j0,w0),(r1,ry1,k1,j1,w1)=[
    derivatives(box(x),box(y)) for x,y in roots]
ratio=k0/k1
B=j0-ratio*j1
C=w0-ratio*w1
coin20=20*(p+2*p*p)/p**3
checks=[]
def check(k,v):
    assert bool(v),k
    checks.append(k)
check('true original first h0 N1 click in chart',r0.a>iv.mpf('1e-6'))
check('true original second h0 N1 click in chart',r1.a>iv.mpf('1e-6'))
check('original first CAR click y first source negative',ry0.b<0)
check('original second CAR click y first source negative',ry1.b<0)
check('original J2 42-root source mismatch >0 in eliminated units',B.a>0)
check('original J2 42-root source mismatch <.000861',B.b<iv.mpf('.000861'))
check('true GOLDEN 20bit raw coin work coefficient positive',C.a>0)
check('true GOLDEN 20bit raw coin coefficient <1.63e-6',C.b<iv.mpf('.00000163'))
check('real Golden fairbit mean CODE cost >117',coin20.a>iv.mpf(117))
check('real Golden fairbit mean CODE cost <118',coin20.b<iv.mpf(118))
share=coin20*C/(2*B)
check('RAW coin-work source fraction .1..12',share.a>iv.mpf('.10') and share.b<iv.mpf('.12'))
check('original Book raw scalar source sign', (B*ry0).b<0)
check('actual pure coin RAW scalar work same sign', (C*ry0).b<0)
print('PASS',len(checks),'80-digit original N1/J2/paid Golden intervals')
print('Book bare source coefficient',B)
print('Golden FAIR coin RAW work coefficient',C)
print('RAW work / Book ratio',share)
print('But COMPLETE Golden measured Cost-Shannon source =0 by exact pathwise identity.')
print('Book03 compulsory path Info/heats/oldRIGHT/physical GR remain OPEN')
