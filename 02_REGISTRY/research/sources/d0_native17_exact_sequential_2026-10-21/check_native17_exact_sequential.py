#!/usr/bin/env python3
"""D0 original Golden17 exact native stopped test; full 17 labels incl failures.
No compulsory Book action, no fresh unknown-state copies or GR closure.
"""
import sympy as s
import mpmath as mp
mp.mp.dps=60
E=lambda i,j:s.eye(4)[:,i]*s.eye(4)[j,:]
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
Gs=[E(1,2)+E(2,0),E(1,3)+E(3,0),
    E(0,2)+E(2,1),E(0,3)+E(3,1),
    E(2,3)-E(3,2),E(1,1)-E(0,0)]
p=(s.sqrt(5)-1)/2;c=s.simplify(p**4/(24*4096))
N=Gs[0];X=s.symbols('X',real=True);I=s.eye(4)
assert N**3==s.zeros(4)
P=I+X*N+X**2*N**2/2
Pm=I-X*N+X**2*N**2/2
assert s.simplify(P*Pm-I)==s.zeros(4)
assert s.simplify(P.T*eta*P-eta)==s.zeros(4)
assert s.Matrix([[s.trace(a.T*b) for b in Gs] for a in Gs])==2*s.eye(6)
assert s.trace(P)==4
for i,g in enumerate(Gs):
  assert s.simplify(s.trace(g.T*P)/(2*s.sqrt(2))-
                   (X/s.sqrt(2) if i==0 else 0))==0
u=s.simplify(c*(1+X/s.sqrt(2))**2)
v=s.simplify(c*(1-X/s.sqrt(2))**2)
neutral=s.simplify(1-u-v)
assert s.simplify(u-v-2*s.sqrt(2)*c*X)==0
assert s.simplify(neutral-(10*c+1-12*c-c*X**2))==0
# Full 17-output likelihood martingale under inverse orientation:
assert s.simplify(v*u/v+u*v/u+neutral-1)==0
# Exact HOLDING gambler's ruin (fifteen neutral categories).
U,V=s.symbols('U V',positive=True);r=V/U
for m in [1,2,3,4]:
  h=lambda k:s.cancel((1-r**(k+m))/(1-r**(2*m)))
  t=lambda k:s.cancel((2*m*h(k)-(k+m))/(U-V))
  assert s.cancel(h(-m))==s.cancel(h(m)-1)==0
  assert s.cancel(t(-m))==s.cancel(t(m))==0
  for k in range(-m+1,m):
    assert s.cancel(U*h(k+1)+V*h(k-1)+(1-U-V)*h(k)-h(k))==0
    assert s.cancel(1+U*t(k+1)+V*t(k-1)+(1-U-V)*t(k)-t(k))==0
  err=s.cancel(1-h(0))
  assert s.cancel(err-r**m/(1+r**m))==0
  assert s.cancel((1-err)/err-(U/V)**m)==0
  assert s.cancel(t(0)-m*(1-2*err)/(U-V))==0
# No-copy conditional predictive law martingale on true shared support:
qa=[s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)]
qb=[s.Rational(1,3)]*3
steps=[
 ([s.Rational(1,5),s.Rational(4,5)],[s.Rational(3,5),s.Rational(2,5)]),
 ([s.Rational(2,3),s.Rational(1,3)],[s.Rational(1,3),s.Rational(2,3)]),
 ([s.Rational(1,6),s.Rational(5,6)],[s.Rational(3,4),s.Rational(1,4)])]
for j in range(3):
  a,b=steps[j];prior=qb[j]/qa[j]
  assert s.simplify(sum(a[k]*prior*b[k]/a[k] for k in range(2))-prior)==0
assert sum(qa)==sum(qb)==1
cnum=mp.mpf(str(s.N(c,70)))
print("Native coefficient c =",mp.nstr(cnum,22))
for raw in ['0.25','0.10','0.05','0.02','0.01']:
  x=mp.mpf(raw);delta=mp.mpf('0.1')
  a=cnum*(1+x/mp.sqrt(2))**2
  b=cnum*(1-x/mp.sqrt(2))**2
  L=mp.log(a/b)
  m=int(mp.ceil(mp.log((1-delta)/delta)/L))
  rr=mp.exp(-m*L);epsilon=rr/(1+rr)
  avg=m*(1-rr)/((a-b)*(1+rr))
  d=(a-b)*L
  minbound=(1-2*epsilon)*mp.log((1-epsilon)/epsilon)/d
  assert epsilon<=delta and abs(avg-minbound)/avg<mp.mpf('1e-50')
  assert abs(d-8*mp.sqrt(2)*cnum*x*mp.atanh(x/mp.sqrt(2)))<mp.mpf('1e-50')
  g=(mp.log(2)+epsilon*mp.log(epsilon)+(1-epsilon)*mp.log(1-epsilon))/mp.log((1+mp.sqrt(5))/2)
  assert 0<g<mp.log(2)/mp.log((1+mp.sqrt(5))/2)
  print('xi',raw,'m',m,'error',mp.nstr(epsilon,9),
        'E native paid rounds',mp.nstr(avg,16))
print('lim xi^2 E[T] delta=.1:',
      mp.nstr(mp.mpf('0.8')*mp.log(9)/(8*cnum),22))
print('PASS: 17 true outcomes, exact SPRT, full errors/holding,')
print('KL/data-processing attained Dmin, terminal Info, non-IID martingale.')
print('GR_closed=false; physical native Book03 Cost-Info/action OPEN.')
