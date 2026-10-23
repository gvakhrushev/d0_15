#!/usr/bin/env python3
"""Original Book03 Golden gate: exact infinite-order phase and C1 word-source no-go.
Physical Cost−Info coherent same-execution writer remains UNPROVED.
"""
import math
import sympy as s
x=s.Symbol('x')
p=(s.sqrt(5)-1)/2
a=s.sqrt(p)
checks=0
def check(name,cond):
    global checks
    if not bool(cond):raise AssertionError(name)
    checks+=1
check('Golden polynomial identity',s.simplify(p+p*p-1)==0)
check('Golden a squared p',s.simplify(a*a-p)==0)
G=s.Matrix([[a,-p],[p,a]])
check('native Golden gate exactly orthogonal',all(s.simplify(v)==0 for v in (G.T*G-s.eye(2))))
check('native Golden gate determinant one',s.simplify(G.det()-1)==0)
# Root of unity would make 2cos(theta) totally real: FALSE.
f=s.minimal_polynomial(2*a,x)
check('exact algebraic minimal polynomial',s.expand(f-(x**4+4*x*x-16))==0)
check('irreducible over Q',s.factor(f)==f)
check('nonreal Galois conjugate',s.simplify(f.subs(x,s.I*s.sqrt(2+2*s.sqrt(5))))==0)
check('real Galois conjugate',s.simplify(f.subs(x,s.sqrt(-2+2*s.sqrt(5))))==0)
check('positive native angle branch',0<float(p)<1 and 0<float(a)<1)
theta=math.asin(float(p))
check('theta > p',theta>float(p))
check('p > Book03 formal ln(phi)',float(p)>math.log((1+math.sqrt(5))/2))
check('theta not ln(phi)',theta>math.log((1+math.sqrt(5))/2))
target=math.log((1+math.sqrt(5))/2)
best=min((abs(math.remainder(n*theta-target,2*math.pi)),n) for n in range(1,100001))
check('a fixed phase is approximated by OLD Golden powers',best[0]<1e-4)
print('PASS',checks,'exact native algebra + bounded phase-orbit controls')
print('minimal trace polynomial:',f)
print('theta:',theta,'lnphi:',target,'best native n<=100000:',best)
print('No field C1 source from a single integer-power lookup: a continuous map from connected field chart into a countable SO(2) orbit is constant.')
print('No real same-history phase/writer/clock/Info selected, GR_closed=false.')
