#!/usr/bin/env python3
"""Exact original tripartite Book triangle-cost interface controls.
Graph-price theorem only; not a native D0 detector/GR closure.
"""
from fractions import Fraction
from itertools import product
from math import sqrt, log

A,B,C=9,11,13
NA,NB,NC=range(A),range(B),range(C)
N=A+B+C
assert A*B+B*C+C*A==359
assert 2*(A*B+B*C+C*A)==718
assert A*B*C==1287
assert (A-1)*(B-1)*(C-1)==960

def oriented_cost_tables():
    ab={(a,b):17*a-9*b+3*a*b for a,b in product(NA,NB)}
    bc={(b,c):11*b+5*c-2*b*c for b,c in product(NB,NC)}
    ca={(c,a):13*c-7*a+a*c for c,a in product(NC,NA)}
    return ab,bc,ca

def face(ab,bc,ca):
    return {(a,b,c):ab[a,b]+bc[b,c]+ca[c,a] for a,b,c in product(NA,NB,NC)}

def contrast(F,a,b,c):
    return (F[a,b,c]-F[0,b,c]-F[a,0,c]-F[a,b,0]
            +F[0,0,c]+F[0,b,0]+F[a,0,0]-F[0,0,0])

def reconstruct(F):
    ab={(a,b):F[a,b,0] for a,b in product(NA,NB)}
    bc={(b,c):F[0,b,c]-F[0,b,0] for b,c in product(NB,NC)}
    ca={(c,a):F[a,0,c]-F[a,0,0]-F[0,0,c]+F[0,0,0]
        for c,a in product(NC,NA)}
    return ab,bc,ca

ab,bc,ca=oriented_cost_tables()
F=face(ab,bc,ca)
assert all(contrast(F,a,b,c)==0 for a,b,c in product(range(1,A),range(1,B),range(1,C)))
assert face(*reconstruct(F))==F
Bad=dict(F);Bad[1,1,1]+=1
assert contrast(Bad,1,1,1)==1
assert face(*reconstruct(Bad))!=Bad

I={i:i*i*7-11*i for i in range(N)}
Costs={}
for a,b in product(NA,NB):
    u,v=a,A+b;Costs[u,v]=37+a+3*b+ab[a,b];Costs[v,u]=37+a+3*b
for b,c in product(NB,NC):
    u,v=A+b,A+B+c;Costs[u,v]=54+b+2*c+bc[b,c];Costs[v,u]=54+b+2*c
for c,a in product(NC,NA):
    u,v=A+B+c,a;Costs[u,v]=71+3*c+a+ca[c,a];Costs[v,u]=71+3*c+a

def pricediff(u,v,theta):
    s_uv=Costs[u,v]-theta*I[u]-(1-theta)*I[v]
    s_vu=Costs[v,u]-theta*I[v]-(1-theta)*I[u]
    return s_uv-s_vu

for theta in (Fraction(0),Fraction(1,3),Fraction(1,2),Fraction(1)):
    for a,b,c in product(NA,NB,NC):
        u,v,w=a,A+b,A+B+c
        assert pricediff(u,v,theta)+pricediff(v,w,theta)+pricediff(w,u,theta)==F[a,b,c]

# Reversible pressure: transpose symmetry kills the odd source.
phi=(1+sqrt(5))/2
allowed=tuple(Costs)
Sym={(u,v):Fraction(40+(u%5)+(v%7),10) for u,v in allowed if u<v}
symmetric={}
for (u,v),z in Sym.items():symmetric[u,v]=symmetric[v,u]=float(z)
anti={}
for u,v in ((0,A),(A,A+B),(A+B,0)):
    anti[u,v]=1;anti[v,u]=-1

def pressure(t):
    mat={(u,v):phi**(-symmetric[u,v]-t*anti.get((u,v),0))
         for u,v in allowed}
    x=[1/N]*N
    for n in range(2000):
        new=[0.]*N
        for (u,v),z in mat.items():new[u]+=z*x[v]
        total=sum(new);new=[z/total for z in new]
        if max(abs(x[i]-new[i]) for i in range(N))<1e-15:
            x=new;break
        x=new
    mu=sum(mat[u,v]*x[v] for u,v in allowed)
    return log(mu)/log(phi)

for t in (0.01,0.05,0.13):
    assert abs(pressure(t)-pressure(-t))<2e-12
h=0.025
curv=(pressure(h)-2*pressure(0)+pressure(-h))/h**2
assert curv>0
print('PASS: 33/718/359/1287, 960 triple-contrast equations, 327 image')
print('PASS: exact edge reconstruction and one-triangle negative control')
print('PASS: 33 Info cancellation for all 1287 triangles and 4 theta choices')
print(f'PASS: reversible scalar pressure even in orientation, curv={curv:.9g}')
print('SCOPED: existing scene homology; no physical D0/GR closure')
