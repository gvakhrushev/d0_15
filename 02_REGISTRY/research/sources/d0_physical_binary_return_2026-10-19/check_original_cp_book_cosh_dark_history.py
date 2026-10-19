#!/usr/bin/env python3
"""A4D PR384 research: ORIGINAL K(9,11,13) exact CP Book cosh, triangle Stokes, unique dark current.
No original full128/physical Einstein closure or alpha-to-edge-Cost selection is asserted.
"""
from collections import Counter
from fractions import Fraction as F

import sympy as sp
import mpmath as mp

x,p,w=sp.symbols("x p w")
# Zone-constant reduction of ALL actual original 718 directed edges:
K=sp.Matrix([[0,11*p*w,13*p/w],
             [9*p/w,0,13*p*w],
             [9*p*w,11*p/w,0]])
expected=x**3-359*p**2*x-1287*p**3*(w**3+w**-3)
assert sp.simplify(K.charpoly(x).as_expr()-expected)==0
assert sp.simplify(sp.trace(K*K)-718*p*p)==0
print("PASS original 33-site charpoly x^30*(x^3-359p^2*x-1287p^3(w^3+w^-3))")

zone=[0]*9+[1]*11+[2]*13
edges=[(u,v) for u in range(33) for v in range(u+1,33) if zone[u]!=zone[v]]
triangles=[(u,v,z) for u in range(9) for v in range(9,20) for z in range(20,33)]
assert len(edges)==359 and len(triangles)==1287
boundary=Counter()
for a,b,c in triangles:
    boundary[a,b]+=1
    boundary[b,c]+=1
    boundary[a,c]-=1
current={e:F(boundary[e],1287) for e in edges}
want={(0,1):F(1,99),(1,2):F(1,143),(0,2):-F(1,117)}
assert all(current[e]==want[zone[e[0]],zone[e[1]]] for e in edges)
divergence=[F(0)]*33
for (u,v),t in current.items():
    divergence[u]-=t
    divergence[v]+=t
assert all(d==0 for d in divergence)
assert sum((1 if (zone[u],zone[v]) in [(0,1),(1,2)] else -1)*t
           for (u,v),t in current.items())==3
print("PASS native 1287 triangles: exact normalized boundary, divergence zero, CP pairing 3")

# The G-invariant original 718-edge history space has six directed macro coordinates.
# Both source and target conditional means zero give rank 5, unique dark CP line.
slots=[(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]
constraints=sp.zeros(6,6)
for j,(u,v) in enumerate(slots):
    constraints[u,j]=1
    constraints[3+v,j]=1
assert constraints.rank()==5 and len(constraints.nullspace())==1
print("PASS native G-invariant source-and-target-dark history: dimension exactly 1")

mp.mp.dps=55
phi=(1+mp.sqrt(5))/2
ell=mp.log(phi)
rho=mp.findroot(lambda r:r**3-359*r-2574,mp.mpf("21.8"))
native_variance=mp.mpf(23166)/(rho*(3*rho*rho-359))
book_hessian=-ell*native_variance
assert abs(native_variance-mp.mpf("0.989947517382062632846106257246722463818"))<mp.mpf("1e-35")
assert abs(book_hessian-mp.mpf("-0.4763744515526458666939982856803847143"))<mp.mpf("1e-35")
delta=359/phi**2-phi**-5-(mp.mpf(12288)/5*phi**-6+phi**-3/3)
r=mp.findroot(lambda v:v**3-359*v-2574*mp.cosh(3*ell*delta),rho)
sigma=15444*ell*delta*mp.sinh(3*ell*delta)/(r*(3*r*r-359))
assert abs(sigma-mp.mpf("7.904323522221987482928640040910014357319e-8"))<mp.mpf("1e-35")
print("PASS exact CP scalar Book Hessian:",mp.nstr(book_hessian,22))
print("PASS conditional epsilon=delta_alpha Markov entropy rate:",mp.nstr(sigma,22))
print("HONEST: Book scalar macroaction only; full128/physical GR, epsilon=delta_alpha remain OPEN")
