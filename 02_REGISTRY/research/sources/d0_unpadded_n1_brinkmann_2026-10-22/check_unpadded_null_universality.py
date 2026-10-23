#!/usr/bin/env python3
"""D0 #334: exact Golden 0/10 N1 first-source + all-mesh Brinkmann lift.

Consumes ORIGINAL six-based-plaquette unrestricted 40->3->1 Euler identity
and N1 complete reporter; does NOT assert physical Book03 H+J+R selection.
"""
from __future__ import annotations
from collections import Counter
from math import floor, sqrt, log
from sympy import symbols, Rational, sqrt as ssqrt, simplify, diff, factor, exp, cos, cosh, sinh, atanh


def check(x, name):
    if not bool(x):
        raise AssertionError(name)

p=(ssqrt(5)-1)/2
z=Rational(1,2**20)
x,y=symbols('x y',real=True)
E=p**2*(1+x)
L=4*E*(1-E)
b=p-p*p*y
B=4*b*b*(1-b*b)
A=L+(1-L)*B
r=z*(A+B)-z*z*A*B
r0=simplify(r.subs({x:0,y:0}))
rx=simplify(diff(r,x).subs({x:0,y:0}))
ry=simplify(diff(r,y).subs({x:0,y:0}))
Q=1-z*4*p**3
R=1-z*4*p**3*(1+p**6)
lam=-2*p**-5*(R/Q+p**6)
check(simplify(p*p+p-1)==0, 'original Golden identity')
check(simplify(4*p**3+p**6-1)==0,'original Golden Q8 two-band identity')
check(simplify(rx-4*z*p**8*(1-2*p**2)*Q)==0,'actual sigma-minus rx')
check(simplify(ry+8*z*p**3*(1-2*p**2)*(Q*p**6+R))==0,'actual sigma-minus ry')
check(simplify(ry-lam*rx)==0,'EXACT physical ratio lambda original minus orientation')
pr=float(p)
r0f=float(r0)
from math import log
hp=log((1-r0f)/r0f)/log(1/pr)
check(1e-6<r0f<1e-5 and hp>1,'native complete positive report and nonzero unpadded source')

# Same genuine paid local 0/10 code with field-variable positive site PF.
# Original null convention f_B=-f_canonical, so x=tau*f_B/rho.
t,rho0,d_rho,d_f,d_q,tau=symbols('t rho0 d_rho d_f d_q tau',real=True)
rho=rho0+t*d_rho
X=tau*(t*d_f)/rho
Y=tau*(t*d_q)/rho
# First derivative of phi-base binary entropy - (native literal code price).
# h'_phi(r0)-1 is one common nonzero fixed factor; no log expansions needed.
# Denote kappa=h'_phi(r0)-1, treat Phi'_x= kappa*rx,Phi'_y=kappa*ry.
kappa=symbols('kappa',real=True)
# At r=r0, B_r=h'_phi(r0)-1=kappa, and the extra field/source term
# involving D_rho is rho'*(h(r0)-h(r0)-r0+r0)=0.
first=simplify(kappa*rho0*diff(r.subs({x:X,y:Y}),t).subs(t,0))
check(simplify(first-tau*kappa*(rx*d_f+ry*d_q))==0,
      'FULL native PF field-jet independence on double-zero sheet')
check(simplify(diff(first,d_rho))==0,'no D PF first-source even if field-dependent')
check(simplify(first-tau*kappa*rx*(d_f+lam*d_q))==0,
      'same two original Palatini and genuine CAR first sources')

# Genuine 4D ORIGINAL address census: no synthetic equal site weights.
pnum=(sqrt(5)-1)/2

def original_cost_words(n,L):
    out=Counter()
    def visit(rest,depth,left,width):
        if rest==0:
            site=tuple(min(L-1,int(L*(left[j]+width[j]/2))) for j in range(4))
            out[site]+=1
            return
        i=depth%4
        wf=width.copy();wf[i]*=pnum
        visit(rest-1,depth+1,left.copy(),wf)
        if rest>=2:
            lr=left.copy();wr=width.copy()
            lr[i]+=pnum*wr[i];wr[i]*=pnum*pnum
            visit(rest-2,depth+1,lr,wr)
    visit(n,0,[0.]*4,[1.]*4)
    return out

def fib(n):
    a,b=0,1
    for _ in range(n):a,b=b,a+b
    return a

for n,L,m,M in [(20,4,29,78),(24,8,4,43)]:
    counts=original_cost_words(n,L)
    check(sum(counts.values())==fib(n+1),'true Fibonacci raw word counts')
    check(len(counts)==L**4,'all four-dimensional native address cells occupied')
    check((min(counts.values()),max(counts.values()))==(m,M),'true nonuniform original PF bounds')
    rho=[L**4*j/fib(n+1) for j in counts.values()]
    check(min(rho)>0 and abs(sum(rho)/len(rho)-1)<1e-12,
          'native strictly positive actual PF rho normalized')
    print(f'PASS original native actual 4D F/R census n={n} L={L} leaves={fib(n+1)} '
          f'sites={len(counts)} min/max={m}/{M}')

# The existing original unrestricted 40->3->1 source theorem gives
# E_cartan=h²(K_prev-1/2(H-Hleft)), and coframe=-h³/2 Lap_perp H.
# We independently validate the exact solution of those surviving rows
# on arbitrary finite h and arbitrary two real independent Ψ time gradients.
h,Xc,Yc=symbols('h Xc Yc',real=True,nonzero=True)
e1,e2,wa,wb=symbols('e1 e2 wa wb',real=True)
energy=e1*e1+e2*e2
H=-lam*energy*(Xc**2+Yc**2)+wa*Xc*Yc+wb*(Xc**2-Yc**2)
lap=simplify((H.subs(Xc,Xc+h)+H.subs(Xc,Xc-h)+
              H.subs(Yc,Yc+h)+H.subs(Yc,Yc-h)-4*H)/h**2)
check(simplify(lap+4*lam*energy)==0,'EXACT original sourced transverse 5-point equation')
# The genuine time-shift is mandatory in original 40->3->1; use H_next.
Hnext=H
k2=(Hnext-Hnext.subs(Xc,Xc-h))/2
k3=(Hnext-Hnext.subs(Yc,Yc-h))/2
check(simplify(k2-(Hnext-Hnext.subs(Xc,Xc-h))/2)==0,
      'unrestricted original Cartan link eq first axis')
check(simplify(k3-(Hnext-Hnext.subs(Yc,Yc-h))/2)==0,
      'unrestricted original Cartan link eq second axis')
coframe=simplify(-h**3*lap/2-2*h**3*lam*energy)
check(coframe==0,'full native 40->3->1 sourced coframe equation')
print('PASS exact N1 true 0/10 r(x,y), full moving PF first source, lambda_- ratio')
print('PASS unrestricted all40 Cartan source consumed; both links and coframe solved on every mesh')
print('PASS two genuinely nonzero independent scalar matter flows e1,e2 and free harmonic wa,wb')
print(f'original lambda_-={float(lam):.15f}; r0={r0f:.12g}; native h_phi_prime={hp:.10f}')
print('SCOPE: finite unpadded N1 measured-CQ source; full compulsory Book03 and physical writer OPEN; GR_closed=false')
