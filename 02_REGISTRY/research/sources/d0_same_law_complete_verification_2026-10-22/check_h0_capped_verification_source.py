#!/usr/bin/env python3
"""Strict outward h0 unpadded exact 42 root: capped same-law verification score.
The h0 exact root, root interval and original based geometry are CONSUMED.
The selected capped same-data verification task is MATHEMATICAL, not compulsory D0.
"""
from decimal import Decimal
from mpmath import iv
iv.dps=85
p=(iv.sqrt(5)-1)/2
ell=iv.log(1/p)
zeta=iv.mpf(2)**-20
tau=iv.mpf('.05')
checks=[]
def check(label,cond):
    if not bool(cond):
        raise AssertionError(label)
    checks.append(label)
def box(s,width='1e-12'):
    x=Decimal(s);w=Decimal(width)
    return iv.mpf([str(x-w),str(x+w)])

def cell(x,y):
    E=p*p*(1+x);L=4*E*(1-E)
    b=p-p*p*y;B=4*b*b*(1-b*b)
    A=L+(1-L)*B
    By=-8*p*p*b*(1-2*b*b)
    Ay=(1-L)*By
    r=zeta*(A+B)-zeta*zeta*A*B
    ry=zeta*(Ay*(1-zeta*B)+By*(1-zeta*A))
    return r,ry

roots=[('0.001370578581747874','-0.000016169093857131'),
       ('-0.000127665084908232','0.000005454102084650')]
(r0,ry0),(r1,ry1)=[cell(box(x),box(y)) for x,y in roots]
check('first real root click strictly greater than second',r0.a>r1.b)
check('both original click rates strictly in certified positive chart',r1.a>iv.mpf('1.8e-6') and r0.b<iv.mpf('1.9e-6'))

# TRUE signed original scalar1 from original h0 rational collar and 42-root centre.
h=iv.mpf('0.183801524658179446663931692878752644250497528167344843803260291378571211')
e00=iv.mpf('0.781442592331451523116352760009308132346803183122126374918636094809048438')
psi1=iv.mpf('0.0164009174377790874496683841812282864696589150604001570884361892719081712')+iv.mpf(['-0.000204675721848868421695242589642','-0.000204675721848868421695242589641'])
DY0=2*tau*e00**-2*psi1/h**2
Dr0=ry0*DY0
check('first original independent scalar1 makes click decrease',Dr0.b<0)

# ORIGINAL exact native normalization kappa from certified_model.CQ.
E=p*p; L=4*E*(1-E);b=p;B=4*b*b*(1-b*b);A=L+(1-L)*B
rflat=zeta*(A+B)-zeta*zeta*A*B
rxflat=zeta*4*p*p*(1-2*E)*(1-B)*(1-zeta*B)
hprime=iv.log((1-rflat)/rflat)/ell
kappa=1/(tau*hprime*rxflat)
check('true original N1 normalization enclosed',kappa.a>iv.mpf('3.8e7') and kappa.b<iv.mpf('3.9e7'))

def kl(r):return 1+r+(r*iv.log(r)+(1-r)*iv.log(1-r))/ell

def klp(r):return 1-iv.log((1-r)/r)/ell

def capp(r,M):
    L=3-r**M-(1-r)**M
    dL=M*((1-r)**(M-1)-r**(M-1))
    return L*kl(r), L*klp(r)+dL*kl(r)

for M in [2,64,1000]:
    val0,D0=capp(r0,M)
    val1,D1=capp(r1,M)
    # Exact original coarse native N1 42-root equation consumes:
    # klp(r0)*Dr0 + klp(r1)*Dr1=0; Dr1 eliminated algebraically.
    coef=D0-(klp(r0)/klp(r1))*D1
    raw=coef*Dr0
    norm=raw*kappa
    check(f'M={M} h0 native capped scalar residual strictly negative',norm.b<0)
    check(f'M={M} h0 residual bounded in code normalization',abs(norm).b < (iv.mpf('.00001') if M==2 else iv.mpf('.01')))
    print('M',M,'source_raw',raw,'source_originalN1_normalized',norm)

# SAME STOPPED TAPE: conditional no-click Book J2 is essentially C1-exact
# at cap64 even though the COMPLETE paid data-clock source fails at h0.
book_value_tail=528*r0**65/(65*(1-r0))
book_j2_derivative_tail=528*r0**64/(1-r0)
check('J2 conditional harmonic cap64 value error < 1e-369',book_value_tail.b<iv.mpf('1e-369'))
check('J2 conditional harmonic cap64 derivative error < 1e-360',book_j2_derivative_tail.b<iv.mpf('1e-360'))

# A cap large enough makes the original unbounded score C1-converge.
M=10**7
_,D0=capp(r0,M);_,D1=capp(r1,M)
coef=D0-(klp(r0)/klp(r1))*D1
s=coef*Dr0*kappa
check('10 million capped same-law source very close to uncapped native root',abs(s).b<iv.mpf('.0001'))
print('M',M,'source_originalN1_normalized',s)
print('PASS',len(checks),'STRICT OUTWARD h0 42-root matched-verification cap/source controls')
print('All h0 N1 full42 existence and 1764 Hessian bounds CONSUMED; no physical Book source selected, GR_closed=false')
