#!/usr/bin/env python3
"""Scoped interval consumer: native exact UNPADDED original 42-root cannot be
stationary for BARE 2-cell old J2 return (original two-factor Golden click).
Uses distinctly supplied independent original h0 interval root and published
Golden operand enclosures; DOES NOT rerun full 1764 Hessian cert or assign Book03.
"""
from mpmath import iv
iv.dps=80
mp=lambda s:iv.mpf(str(s))
p=(iv.sqrt(5)-1)/2
ell=iv.log(1/p)
zeta=iv.mpf(1)/2**20
h=mp('0.183801524658179446663931692878752644250497528167344843803260291378571211')
tau=mp('0.05')
# deliberately wide source operand boxes for the already owned outward-interval
# h0 UNPADDED 42 root, originally published to >=15 decimal places.
x0=iv.mpf(['0.001369578581747874','0.001371578581747874'])
y0=iv.mpf(['-0.000017169093857131','-0.000015169093857131'])
x1=iv.mpf(['-0.000128665084908232','-0.000126665084908232'])
y1=iv.mpf(['0.000004454102084650','0.000006454102084650'])

def bern(x,y):
    E=p**2*(1+x)
    L=4*E*(1-E)
    b=p-p**2*y
    B=4*b*b*(1-b*b)
    A=L+(1-L)*B
    r=zeta*(A+B)-zeta**2*A*B
    By=-8*p**2*b*(1-2*b*b)
    ry=zeta*By*((1-L)*(1-zeta*B)+(1-zeta*A))
    kp=1-iv.log((1-r)/r)/ell
    jp=528/(1-r)
    return r,ry,kp,jp

def low(t):return float(t.a)
def up(t):return float(t.b)
r0,ry0,kp0,jp0=bern(x0,y0)
r1,ry1,kp1,jp1=bern(x1,y1)
delta=r0-r1
assert low(delta)>2.8e-11,(low(delta),up(delta))
assert up(ry0)<-4e-7
assert up(kp0)<-25 and up(kp1)<-25
# Actual original fixed collar (SHA pinned in inputs.py); scalar1 true temporal gradient.
e0=mp('0.781442592331451523116352760009308132346803183122126374918636094809048438')
psi10=mp('0')
psi11=mp('0.0164009174377790874496683841812282864696589150604001570884361892719081712')+iv.mpf(['-0.000204675721848868421695242589642','-0.000204675721848868421695242589641'])
g00=e0**(-2)
udu=(psi11-psi10)/h
assert low(udu)>0.08
# Original native scalar at first cell Q = g00 (psi11-psi10)^2/h^2 + ...
# y=tau*Q/rho with rho=1, and the legitimate independent original field
# coordinate psi11 varied at fixed original coframe, links, and collar.
dr0=ry0*tau*2*g00*udu/h
assert up(dr0)<-3.0e-8,(low(dr0),up(dr0))
# At exact native full42 root, the scalar1 Euler is:
# k'(r0) * dpsi r0 + k'(r1) * dpsi r1 =0.
# The exact old Book J2 block 528[-log(1-r0)-log(1-r1)] has derivative
# [j0' - j1' k0'/k1'] dr0, with NO HJR other contributions.
coef=jp0-jp1*kp0/kp1
assert low(coef)>0.0006,(low(coef),up(coef))
dJ=coef*dr0
assert up(dJ)<-1.8e-11,(low(dJ),up(dJ))
print('PASS: strict certified-root-consumer nonzero original Book J2 bare scalar Euler')
print('native h0 root r0-r1 interval:',low(delta),up(delta))
print('original scalar1 first-cell rate-gradient interval:',low(dr0),up(dr0))
print('bare J2 source coefficient interval:',low(coef),up(coef))
print('original Book J2 scalar1 derivative interval:',low(dJ),up(dJ))
print('EXACT old native 42 unpadded stationary root CONSUMED; actual selected complete HJR/Info/clock/writer not evaluated; GR_closed=false.')
