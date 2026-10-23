#!/usr/bin/env python3
"""Original Golden 0/10 native c + beta*J2 never satisfies one-Golden
metric-weight 1 for any CONSTANT beta on an open curvature-only chart.
92 scoped sign checks, but the proof is the exact analytic sign chain.
No claim that physical Book heat/Info or selected 42-writer is absent.
"""
import mpmath as mp

mp.mp.dps=75
p=(mp.sqrt(5)-1)/2
z=mp.mpf(2)**(-20)
logphi=mp.log(1/p)
checks=0
def check(name,cond):
    global checks
    if not cond:raise AssertionError(name)
    checks+=1
B=4*p*p*(1-p*p)
def A(x):
    E=p*p*(1+x)
    L=4*E*(1-E)
    return L+(1-L)*B
def r(x):return 1-(1-z*A(x))*(1-z*B)
flat=r(0)
def H(v):return -(v*mp.log(v)+(1-v)*mp.log(1-v))/logphi
def c(x):return r(x)-H(r(x))-(flat-H(flat))
def j(x):return -528*(mp.log(1-r(x))-mp.log(1-flat))

check('old Golden p root',abs(p*p+p-1)<mp.mpf('1e-70'))
check('rare native flat click is positive',mp.mpf('1e-6')<flat<mp.mpf('1e-5'))
check('original A has negative curvature',mp.diff(A,0,2)<0)
check('original A_x nonzero',mp.diff(A,0)>0)
check('subtracted Golden 0/10 score vanishes at baseline',c(0)==0)
check('subtracted Book J2 score vanishes at baseline',j(0)==0)
for X in ['-0.003','-.002','-.001','-.0001','0',
          '.0001','.001','.002','.003']:
    x=mp.mpf(X)
    r1=mp.diff(r,x)
    r2=mp.diff(r,x,2)
    c2=mp.diff(c,x,2)
    c3=mp.diff(c,x,3)
    j2=mp.diff(j,x,2)
    j3=mp.diff(j,x,3)
    check('native positive field signal '+X,r1>0)
    check('native negative return curvature '+X,r2<0)
    check('native rigorous microscopic convexity '+X,c2>mp.mpf('1.0788e-6'))
    check('native strictly negative microscopic third jet '+X,c3<0)
    check('native strictly negative J2 second jet '+X,j2<0)
    check('native strictly negative J2 third jet '+X,j3<0)
    check('native J2 second sign exact A algebra '+X,
          mp.diff(A,x,2)*(1-z*A(x))+z*mp.diff(A,x)**2<0)
    check('native J2 third sign exact A algebra '+X,
          3*mp.diff(A,x,2)*(1-z*A(x))+2*z*mp.diff(A,x)**2<0)
check('second-source cancellation requires positive beta',
      -mp.diff(c,0,2)/mp.diff(j,0,2)>0)
check('third-source cancellation requires negative beta',
      -mp.diff(c,0,3)/mp.diff(j,0,3)<0)
beta2=-mp.diff(c,0,2)/mp.diff(j,0,2)
res3=mp.diff(c,0,3)+beta2*mp.diff(j,0,3)
check('exact third jet survives selected second-order beta',
      res3<mp.mpf('-4e-9'))
for val in ['-100','-1','-0.1','-.05','-0.001','0',
            '.001','.05','0.05006937','1','100']:
    beta=mp.mpf(val)
    d2=mp.diff(c,0,2)+beta*mp.diff(j,0,2)
    d3=mp.diff(c,0,3)+beta*mp.diff(j,0,3)
    check('all real constant J2 coefficients fail '+val,
          (beta<=0 and d2>0) or (beta>=0 and d3<0))
print('PASS',checks,'original Golden native 0/10/J2 open-chart algebra controls')
print('jxx',mp.nstr(mp.diff(j,0,2),21),
      'jxxx',mp.nstr(mp.diff(j,0,3),21))
print('cxx',mp.nstr(mp.diff(c,0,2),21),
      'cxxx',mp.nstr(mp.diff(c,0,3),21))
print('constant J2 second-jet cancelling beta',mp.nstr(beta2,22),
      'third jet still',mp.nstr(res3,22))
print('SCOPE: NO constant J2 mix restores weight-one Einstein scale.',
      'Full field-dependent Book HJR can be different; GR_closed=false.')
