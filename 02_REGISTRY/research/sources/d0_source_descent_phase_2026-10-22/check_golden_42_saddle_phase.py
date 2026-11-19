#!/usr/bin/env python3
"""Native Book03 FORMAL phase vs positive Golden weight at a 42D saddle.
Synthetic Hessian check; original h0 interval proof is consumed, NOT rerun.
"""
from math import pi,log,sqrt
import cmath
phi=(1+sqrt(5))/2
alpha=log(phi)
checks=0
def check(label,x):
    global checks
    if not x: raise AssertionError(label)
    checks+=1
check('native logarithmic constant positive',alpha>0)
h=[4.,-2.]+[1.]*20+[-1.]*20
check('genuine 42 field directions',len(h)==42)
check('unrestricted positive and negative eigendirections',any(x>0 for x in h) and any(x<0 for x in h))
check('nondegenerate Hessian',min(abs(x) for x in h)>0)
check('phase signature of symmetric synthetic test',sum(1 if x>0 else -1 for x in h)==0)
# Regulated exact Gaussian determinant on R^42, not original D0 H.
def exact(n,eps=1.):
    x=complex((2*pi)**21,0)
    for eig in h:
        x/=cmath.sqrt(eps+1j*n*alpha*eig)
    return x
def leading(n):
    mag=(2*pi/(n*alpha))**21
    for eig in h:
        mag/=sqrt(abs(eig))
    sign=sum(1 if eig>0 else -1 for eig in h)
    return mag*cmath.exp(-1j*pi*sign/4)
errs=[]
for n in (100,1000,10000,100000):
    z=exact(n); approx=leading(n)
    relative=abs(z/approx-1)
    errs.append(relative)
    check(f'quadratic stationary-phase contraction {n}',relative<0.1)
check('large action phase approximation improves on refinement',all(errs[i+1]<errs[i] for i in range(len(errs)-1)))
check('large n produces high precision phase',errs[-1]<1e-4)
for n in (5,10,20):
    check(f'positive Gibbs quadratic at saddle cannot normalize without field cutoff n={n}',min(1.+n*alpha*v for v in h)<0)
print(f'PASS {checks} Gaussian/Golden/42-saddle controls')
print('relative local-phase asymptotic errors',errs)
print('Book03 phase FORMAL: physical phase writer/complete work and GR_closed remain OPEN')
