#!/usr/bin/env python3
import sympy as s
sig,x,y=s.symbols('sigma x y',real=True)
j=s.Matrix([[0,-1],[1,0]])
s0=s.diag(x*j,y*j);d=4
D=s.diag(*([s.sqrt(1-sig**2*x*x)]*2+[s.sqrt(1-sig**2*y*y)]*2))
R=s.BlockMatrix([[sig*s0,D],[-D,-sig*s0]]).as_explicit()
rho=s.simplify(R*s.diag(s.eye(d)/d,s.zeros(d))*R.T)
A=-s0*s0
wanted=s.BlockMatrix([[sig**2*A,-sig*s0*D],[sig*D*s0,s.eye(d)-sig**2*A]]).as_explicit()/d
assert s.simplify(rho-wanted)==s.zeros(2*d)
assert s.simplify(rho*rho-rho/d)==s.zeros(2*d)
assert s.simplify(s.trace(rho)-1)==0
# Arbitrary symmetric within-port logarithms, including noncommuting entries.
def symmatrix(prefix):
 vals=s.symbols(prefix+':10',real=True);M=s.zeros(4);k=0
 for a in range(4):
  for b in range(a,4):M[a,b]=M[b,a]=vals[k];k+=1
 return M
lu,ll=symmatrix('u'),symmatrix('l')
quantum=-s.log(d)-s.trace(rho*s.diag(lu,ll))
closed=-s.log(d)-s.trace(ll)/d-sig**2*s.trace(A*(lu-ll))/d
assert s.simplify(quantum-closed)==0
# Fixed Golden prior: log μU=−logφ−log d; log μL=−2logφ−log d.
lg=s.symbols('logphi',positive=True)
qgold=(-s.log(d)-s.trace(rho*s.diag((-lg-s.log(d))*s.eye(d),(-2*lg-s.log(d))*s.eye(d))))/lg
assert s.simplify(qgold-(2-sig**2*s.trace(A)/d))==0
# Every coframe derivative through zeros x=y=0 remains regular.
for a in [x,y]:
 assert not s.diff(closed,a,2).has(s.log(x),s.log(y))
# Faithful off-block μ witness; its exact spectrum is 2/5,1/10 (twice each).
d2=s.sqrt(1-sig**2*x*x);r2=s.BlockMatrix([[sig*x*j,d2*s.eye(2)],[-d2*s.eye(2),-sig*x*j]]).as_explicit()
r2=r2*s.diag(s.eye(2)/2,s.zeros(2))*r2.T
O=s.BlockMatrix([[s.zeros(2),j],[-j,s.zeros(2)]]).as_explicit()
assert O.T==O and O*O==s.eye(4)
mu=(s.eye(4)+s.Rational(3,5)*O)/4
assert sorted(mu.eigenvals().keys())==[s.Rational(1,10),s.Rational(2,5)]
logmu=-s.log(5)*s.eye(4)+s.log(2)*O
hostile=-s.log(2)-s.trace(r2*logmu)
assert s.simplify(hostile-(s.log(s.Rational(5,2))+2*s.log(2)*sig*x*d2))==0
assert s.simplify(s.diff(hostile,x).subs(x,0)-2*s.log(2)*sig)==0
print('PASS full coherent output and constant spectrum; no dephasing')
print('PASS exact fixed block-diagonal Umegaki price and C2 quadratic field source')
print('PASS original Golden cost1/2 prior formula')
print('PASS faithful off-block reference creates a genuine O(sigma) hostile source')
