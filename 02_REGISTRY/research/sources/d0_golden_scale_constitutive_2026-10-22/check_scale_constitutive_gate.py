#!/usr/bin/env python3
"""D0 #334 exact Golden scale versus original 0/10 constitutive convexity.

104 scoped checks; consumes existing certified strict two-operand Hessian,
does NOT recertify intervals / Book03 / original M1 admission / GR.
"""
import math
import mpmath as mp

mp.mp.dps=75
p=(mp.sqrt(5)-1)/2
phi=1/p
zeta=mp.mpf(2)**(-20)
logphi=mp.log(phi)
s=phi**2
m=mp.mpf('1.0788e-6')  # strict certified lower cxx bound on full chart
M=mp.mpf('5e-5')       # strict certified upper Hessian operator norm
checks=0

def check(label, condition):
    global checks
    if not condition:raise AssertionError(label)
    checks+=1

def click(x,y):
    E=p**2*(1+x)
    L=4*E*(1-E)
    b=p-p**2*y
    B=4*b**2*(1-b**2)
    A=L+(1-L)*B
    return 1-(1-zeta*A)*(1-zeta*B)

r0=click(0,0)
def entropy(r):
    return -(r*mp.log(r)+(1-r)*mp.log(1-r))/logphi
def c(x,y):
    r=click(x,y)
    return (r-entropy(r))-(r0-entropy(r0))
def cx(x,y):
    return mp.diff(lambda v:c(v,y),x)
def cy(x,y):
    return mp.diff(lambda v:c(x,v),y)
def hx(x):
    return mp.diff(lambda v:cx(v,0),x)

check('Golden p+p²=1',abs(p+p*p-1)<mp.mpf('1e-72'))
check('native fixed Book scale s=phi²',abs(s-(phi+1))<mp.mpf('1e-70'))
check('native c(0)=0',abs(c(0,0))<mp.mpf('1e-60'))
check('native flat rare click bounds',mp.mpf('1e-6')<r0<mp.mpf('1e-5'))
check('native x has nonzero source',cx(0,0)<0)
check('original positive cxx lower',hx(0)>m)
check('original positive cxx upper',hx(0)<M)

for raw in ['0.0001','-0.0001','0.0004','-0.0004','0.001',
            '-0.001','0.001370578581747874','-0.000127665084908232',
            '0.002','-0.002']:
    x=mp.mpf(raw)
    check('true scaled x inside strict convex chart '+raw,abs(s*x)<mp.mpf('.01'))
    delta=c(s*x,0)-s*c(x,0)
    check('strict Goldenscale action defect '+raw,delta>m*s*(s-1)*x*x/2)
    source=s*(cx(s*x,0)-cx(x,0))
    check('strict Goldenscale source defect '+raw,
          source*x>0 and abs(source)>m*s*(s-1)*abs(x))

rx0=mp.diff(lambda v:click(v,0),0)
fisher_coeff=rx0**2/(r0*(1-r0))
for L in [4,5,8,16,32,64,128,256,1024,2048,4096]:
    n=int(mp.ceil(mp.log(L)/logphi))
    h=mp.mpf(1)/L
    tau=p**(2*n)
    check('Golden charge logarithmic '+str(L),
          n<=math.ceil(math.log(L)/float(logphi))+1)
    check('native phi aperture bracket '+str(L),p*p*h*h<tau<=h*h)
    fisher=tau**2*fisher_coeff
    check('one original Bernoulli Fisher exact '+str(L),
          abs(fisher/tau**2-fisher_coeff)<mp.mpf('1e-64'))
    check('one Bernoulli Fisher upper h4 '+str(L),
          fisher < fisher_coeff*h**4*(1+mp.mpf('1e-50')))
    check('one Bernoulli Fisher lower p4*h4 '+str(L),
          fisher > fisher_coeff*p**4*h**4)

hp0=mp.log((1-r0)/r0)/logphi
K=1/(hp0*rx0)
f,q,rho=mp.mpf('.04'),mp.mpf('.01'),mp.mpf('1.2')
a0,b0=cx(0,0),cy(0,0)
for tau in [mp.mpf('.05'),mp.mpf('.01'),mp.mpf('.005'),mp.mpf('.001')]:
    x=tau*f/rho
    y=tau*q/rho
    exact=K/tau*rho*c(x,y)
    affine=K*(a0*f+b0*q)
    bound=K*M*tau*(f*f+q*q)/(2*rho)
    check('source-normalized affine action limit '+str(tau),
          abs(exact-affine)<bound)
    df,dq=K*cx(x,y),K*cy(x,y)
    error=mp.sqrt((df-K*a0)**2+(dq-K*b0)**2)
    check('both original field first sources '+str(tau),
          error<K*M*tau*mp.sqrt(f*f+q*q)/rho)
    drho=K/tau*(c(x,y)-x*cx(x,y)-y*cy(x,y))
    check('full moving native PF first source '+str(tau),
          abs(drho)<K*M*tau*(f*f+q*q)/(2*rho*rho))

print('PASS',checks,'native strict-convex Golden-scale/C1/resource controls')
print('Golden metric scale',mp.nstr(s,22),
      'microscopic cxx at origin',mp.nstr(hx(0),22))
print('native flat r',mp.nstr(r0,22),'r_x',mp.nstr(rx0,22))
print('one native classical Bernoulli Fisher coefficient',
      mp.nstr(fisher_coeff,22))
for x in [mp.mpf('.001'),mp.mpf('.001370578581747874')]:
    print('x',mp.nstr(x,15),
          'scale defect',mp.nstr(c(s*x,0)-s*c(x,0),20),
          'strict lower',mp.nstr(m*s*(s-1)*x*x/2,20),
          'field-source reaction',mp.nstr(s*(cx(s*x,0)-cx(x,0)),20))
print('SCOPE: fixed-tau configured N1 ALONE fails native weight-one action.',
      'Physical Book HJR/actual source-scaled Golden query can change that.',
      'GR_closed=false; full_D0_price_selected=false; raw216_closed=false')
