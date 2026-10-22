#!/usr/bin/env python3
"""Original exact h0 UNPADDED N1 full42 root: FINE dephased+charged Golden
two-factor flags have a strictly NONZERO independent scalar1 Euler.
The already certified coarse-OR root is CONSUMED, not newly solved.
"""
from decimal import Decimal
from mpmath import iv
iv.dps=85
p=(iv.sqrt(5)-1)/2
z=iv.mpf(2)**-20
lnphi=iv.log(1/p)
roots=[('0.001370578581747874','-0.000016169093857131'),
       ('-0.000127665084908232','0.000005454102084650')]
def box(v):
    c=Decimal(v); eps=Decimal('1e-12')
    return iv.mpf([str(c-eps),str(c+eps)])
def cell(x,y):
    E=p*p*(1+x); L=4*E*(1-E)
    b=p-p*p*y;B=4*b*b*(1-b*b);A=L+(1-L)*B
    By=-8*p*p*b*(1-2*b*b);Ay=(1-L)*By
    u=z*A;v=z*B;r=u+v-u*v
    ry=z*(Ay*(1-v)+By*(1-u))
    hp=lambda q:iv.log((1-q)/q)/lnphi
    cy=(1-hp(r))*ry
    fy=(1-hp(u))*z*Ay+(1-hp(v))*z*By
    return r,ry,cy,fy
A,B=[cell(box(x),box(y)) for x,y in roots]
# Exact coarse true native 42 Euler: cy0*Dpsi(y0)+cy1*Dpsi(y1)=0.
# Therefore define the exact DIFFERENT fine future Euler eliminant:
coeff=A[3]-(A[2]/B[2])*B[3]
h=iv.mpf('0.183801524658179446663931692878752644250497528167344843803260291378571211')
e0=iv.mpf('0.781442592331451523116352760009308132346803183122126374918636094809048438')
psi1=iv.mpf('0.0164009174377790874496683841812282864696589150604001570884361892719081712')+iv.mpf(['-0.000204675721848868421695242589642',
                                                                                              '-0.000204675721848868421695242589641'])
tau=iv.mpf('.05')
DY0=2*tau*(e0**-2)*(psi1/h)/h
source=coeff*DY0
# ORIGINAL fixed N1 cost normalization, no fitted geometric coefficient:
E=p*p;L=4*E*(1-E);b=p;B0=4*b*b*(1-b*b);A0=L+(1-L)*B0
r=z*(A0+B0)-z*z*A0*B0
Lx=4*p*p*(1-2*E)
rx=z*Lx*(1-B0)*(1-z*B0)
hp=iv.log((1-r)/r)/lnphi
kappa=1/(tau*hp*rx)
scaled=source*kappa
checks=[]
def check(label,condition):
    assert bool(condition),label
    checks.append(label)
check('two true original h0 click rates above 1e-6',
      A[0].a>iv.mpf('1e-6') and B[0].a>iv.mpf('1e-6'))
check('first original matter click derivative negative',A[1].b<0)
check('second original matter click derivative negative',B[1].b<0)
check('first coarse score matter derivative positive',A[2].a>0)
check('second coarse score matter derivative positive',B[2].a>0)
check('actual original independent scalar1 field y0 source positive',
      DY0.a>iv.mpf('.0785'))
check('fine Euler eliminant coefficient >3.43e-11',coeff.a>iv.mpf('3.43e-11'))
check('fine Euler eliminant coefficient <3.44e-11',coeff.b<iv.mpf('3.44e-11'))
check('fine true h0 scalar1 Euler >2.6982e-12',source.a>iv.mpf('2.6982e-12'))
check('fine true h0 scalar1 Euler <2.6984e-12',source.b<iv.mpf('2.6984e-12'))
check('fixed original source normalization >38e6',kappa.a>iv.mpf('3.8e7'))
check('fixed original source normalization <39e6',kappa.b<iv.mpf('3.9e7'))
check('original normalized fine Euler >1.02e-4',scaled.a>iv.mpf('1.02e-4'))
check('original normalized fine Euler <1.04e-4',scaled.b<iv.mpf('1.04e-4'))
print('PASS',len(checks),'outward ORIGINAL h0 native 42-root FINE scalar1 checks')
print('before native N1 normalization',source)
print('original fixed N1 kappa',kappa)
print('after N1 normalization',scaled)
print('Coarse original unpadded 42 root exists exactly by CONSUMED interval theorem.')
print('Neither competing readout is yet selected as compulsory Book03, GR OPEN')
