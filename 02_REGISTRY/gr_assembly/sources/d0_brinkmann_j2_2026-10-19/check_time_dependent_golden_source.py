#!/usr/bin/env python3
"""Bounded real-golden and time-dependent sourced Brinkmann verification.

Consumes original exact 40-Euler symbolic theorem in companion checker
and CORRECT twice-tick Book feedback source, NOT original physical full D0.
"""
import math,itertools
from collections import Counter
p=(math.sqrt(5)-1)/2
z=2**-20
a=p**6
L0=4*p**3
Q=1-z*L0
R=1-z*L0*(1+a)
lam=-2*(R/Q+a)/p**5

def fib(n):
    A,B=0,1
    for _ in range(n):
        A,B=B,A+B
    return A

def coverage(n,L):
    hits=Counter()
    def visit(rem,depth,left,width):
        if rem==0:
            site=tuple(min(L-1,int(L*(left[i]+width[i]/2))) for i in range(4))
            hits[site]+=1
            return
        j=depth%4
        w=width.copy();w[j]*=p
        visit(rem-1,depth+1,left.copy(),w)
        if rem>=2:
            w=width.copy();q=left.copy()
            q[j]+=p*w[j];w[j]*=p*p
            visit(rem-2,depth+1,q,w)
    visit(n,0,[0.]*4,[1.]*4)
    assert sum(hits.values())==fib(n+1)
    assert len(hits)==L**4
    assert min(hits.values())>0 and max(hits.values())>min(hits.values())
    return hits

def trial(n,L):
    h=1/L
    m=L//2
    velocities=[]
    for j in range(m):
        u=j*h
        rate=.025*(1+.2*math.cos(4*math.pi*u)+.12*math.sin(4*math.pi*u))
        angle=.15+2*math.pi*u+.2*math.sin(4*math.pi*u)+.17*math.cos(8*math.pi*u)
        velocities.append((rate*math.cos(angle),rate*math.sin(angle)))
    velocities += [(-a,-b) for a,b in velocities]
    E=[x*x+y*y for x,y in velocities]
    psi=[(0,0)]
    for j in range(L-1):
        psi.append(tuple(psi[-1][i]+h*velocities[j][i] for i in (0,1)))
    assert all(abs(psi[-1][i]+h*velocities[-1][i])<1e-13 for i in (0,1))
    kval=1.3
    alpha=math.acosh(2-math.cos(kval*h))/h

    def harmonic(j,x,y):
        u=j*h
        P3=x**3-3*x*y*y
        P4=x**4-6*x*x*y*y+y**4-h*h*(x*x+y*y)
        Wexp=math.exp(alpha*x)*math.cos(kval*y)
        return .15*math.sin(2*math.pi*u)*P3+.03*math.cos(4*math.pi*u)*P4+.02*math.cos(2*math.pi*u)*Wexp

    # Cartan solution forces one-u-tick lag: H(j) uses material E(j-1).
    def H(j,x,y):
        return -lam*E[(j-1)%L]*(x*x+y*y)+harmonic(j,x,y)

    max_poisson=max_source=0
    for j in range(L):
        for x,y in itertools.product((.15,.33,.57,.81),(-.22,.11,.44)):
            lap=(H(j+1,x+h,y)+H(j+1,x-h,y)+H(j+1,x,y+h)+H(j+1,x,y-h)-4*H(j+1,x,y))/h**2
            max_poisson=max(max_poisson,abs(lap+4*lam*E[j]))
            # Normalized true one-feedback first source:
            # d(f_native)=-lap/(2h), d(q_native)=-2 E[j]/h.
            max_source=max(max_source,abs(-lap/(2*h)+lam*(-2*E[j]/h)))
    assert max_poisson<1e-10 and max_source<1e-9
    hits=coverage(n,L)
    j_hodge=[2*(velocities[j][1]*psi[j][0]-velocities[j][0]*psi[j][1]) for j in range(L)]
    assert max(E)>min(E)>0
    print(f"L={L}, cost={n}, native F/R={fib(n+1)}, covered={len(hits)}")
    print(f"unequal count min/max={min(hits.values())}/{max(hits.values())}, E-range={min(E):.9f}..{max(E):.9f}")
    print(f"exact Poisson source residual={max_poisson:.3e}, full J2 Euler residual={max_source:.3e}")
    print(f"native scalar/top current range={min(j_hodge):.9f}..{max(j_hodge):.9f}")

if __name__=='__main__':
    assert abs(lam+23.416406751884)<1e-10
    trial(20,4)
    trial(24,8)
    print("PASS arbitrary time-dependent scalar and nonlinear harmonic Lorentz-star source, real old Fibonacci weights")
    print("SCOPE finite constructed complete AF J2 only; original physical D0⇒GR not promoted.")
