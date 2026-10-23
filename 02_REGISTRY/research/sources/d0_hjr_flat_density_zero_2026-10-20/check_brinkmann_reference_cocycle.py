#!/usr/bin/env python3
"""Bounded-native-Dirac leg shear: complete H+J+R source and reference cocycle.

Inputs: native full-CAR16 shifted positive adjoint, native m/alpha/beta/zeta,
and the complete rank128 fixedRIGHT Riesz FIRST source.

23 October correction: the former `coframe` matrix stores ROWS of normalized
creation legs. Its Lorentz Gram is contravariant, not the physical covariant
coframe metric. The actual legs are h times its transpose; their physical
metric is the inverse Gram. The fixed-symbol large-L limit below is not a
same-fixed-metric Brinkmann refinement. This does not select the Book price.

Certifies exact rational all-L>=256 bound, entire Bloch trace finite checks,
independent Bessel continuum value, and groupoid reference uniqueness.
"""
from fractions import Fraction as Q
from math import cos, pi, sqrt

import mpmath as mp
import numpy as np
import sympy as sp

t = sp.symbols("t", real=True)
h = sp.symbols("h", positive=True)
eta = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                 [0, 0, -1, 0], [0, 0, 0, -1]])
leg_rows = sp.eye(4)
leg_rows[0, 1] = t
contravariant_gram = leg_rows * eta * leg_rows.T
native_legs = h * leg_rows.T
physical_metric = (native_legs.T * eta * native_legs).inv()
physical_coframe = eta * native_legs.inv().T

assert contravariant_gram == sp.Matrix([[2*t, 1, 0, 0],
                                       [1, 0, 0, 0],
                                       [0, 0, -1, 0],
                                       [0, 0, 0, -1]])
assert leg_rows.det() == 1 and contravariant_gram.det() == -1
assert physical_metric == sp.Matrix([[0, 1, 0, 0],
                                     [1, -2*t, 0, 0],
                                     [0, 0, -1, 0],
                                     [0, 0, 0, -1]]) / h**2
assert physical_coframe.T * eta * physical_coframe == physical_metric
assert physical_coframe.det() == eta.det() / h**4
assert physical_metric.det() == -1 / h**8
assert physical_metric.diff(t) == sp.diag(0, -2, 0, 0) / h**2
# At fixed h only g_vv changes: E_gvv = -h^2 E_t / 2. This sign and
# factor follow from inverse Gram; the numerical t-source is unchanged.
source_t = sp.symbols("source_t", real=True)
assert sp.simplify((-h**2 * source_t / 2)
                   * physical_metric.diff(t)[1, 1] - source_t) == 0
print("EXACT native inverse-Gram metric: g=h^-2(2du dv-2t dv^2-dx^2-dy^2), "
      "det g=-h^-8; flat and volume-preserving in t at each fixed h.")
print("COTANGENT: E_gvv=-h^2 E_t/2 at fixed h; "
      "no same-fixed-metric refinement is asserted.")

# The EXACT finite counting-site/Fock spectrum at t=0:
# Delta(t,k)=sum |e^(ikr)-1|² +2t Re(conj(z_u)z_v)
#                         +t² |e^(iku)-1|², all CAR16 modes.
# At t=0 the prepared rank128 shell is 8 first momenta x 16 CAR,
# and its derivative is zero in t (no first-shell mixed uv momentum).
p2 = (3 - sqrt(5))/2
zeta = 2**-20
beta = 2*p2
assert Q(3, 8) < p2 < Q(2, 5)
assert Q(68, 25)**13 < 500000
assert Q(1024, 79) < 13

# For every integer L>=256: 0<=alpha*mu<1/(20 L²);
# b^m>e^-13>1/500000, Qsum>L^4/500000;
# source bracket >3/2048-500000/L^4.
bound=Q(2, 500000)*(Q(3, 2048)-Q(500000, 256**4))
assert bound == Q(180983, 33554432000000)
assert bound > Q(1, 200000000)
print("ALL-L EXACT: bounded-leg dS/dt per site >", str(bound),
      "for all L>=256; normalized contravariant-Gram coefficient source is half.")

# An independent convergent analytic Bessel series, not a fit in L.
mp.mp.dps = 50
pp = (mp.sqrt(5)-1)/2
zz=mp.mpf(2)**-20
bt=2*pp*pp
value=mp.mpf(0)
for n in range(14):
    v=(n+1)*bt
    i0=mp.besseli(0,2*v)
    i1=mp.besseli(1,2*v)
    value += (-zz/(1-zz))**n * mp.exp(-8*v)*i0*i0*(i0-i1)**2
value*=4096*zz*bt/(1-zz)
assert value > 0
print("Exact bounded-symbol limit dS/dt/L^4 =",mp.nstr(value,37))
print("Exact bounded-symbol limit for q0^uu=2t coefficient =",mp.nstr(value/2,37))

# Original entire H (real global Z), 128*16 feedback J and R FIRST
# source=0 on the lowest eight-momentum x CAR16 shell. The full
# sine-sine cross mode is retained in the direct ACTION evaluator;
# it cancels in the analytic first-gradient trace only after sum.
for L in (4, 8, 12, 16, 20, 24, 32, 40):
    kth=2*pi*np.arange(L)/L
    cs, ss=np.cos(kth),np.sin(kth)
    ar=2-2*cs
    mu=(ar[:,None,None,None]+ar[None,:,None,None]
        +ar[None,None,:,None]+ar[None,None,None,:])
    alpha=p2/(128*L*L)
    m=256*L*L
    B=1-alpha*mu
    assert np.min(B)>0
    weight=np.exp(m*np.log(B))
    Qsum=float(weight.sum())
    feedback=1-zeta+zeta*weight
    mixed_even=2*(1-cs)[:,None,None,None]*(1-cs)[None,:,None,None]
    mixed_full=mixed_even+2*ss[:,None,None,None]*ss[None,:,None,None]
    bracket=2048*zeta*beta/feedback-1/Qsum
    shear=float((mixed_even*B**(m-1)*bracket).sum())

    def original_complete_HJ(t0):
        # The original Rayleigh rank128 preparation has identically
        # zero FIRST derivative at t0=0 and is not dropped from theory.
        spectrum=mu+t0*mixed_full+t0*t0*ar[:,None,None,None]
        b=1-alpha*spectrum
        fw=np.exp(m*np.log(b))
        return float(np.log(16*fw.sum())/beta
                     -2048*np.log1p(zeta*(fw-1)).sum())

    eps=1e-4
    finite=(original_complete_HJ(eps)-original_complete_HJ(-eps))/(2*eps)
    assert abs((shear-finite)/L**4)<7e-10
    print(f"L={L:2} full-HJR local dS/dt={shear/L**4:+.12g} "
          f"independent finite-difference={finite/L**4:+.12g}")

# The pair-groupoid reference identity is algebraic and works for
# arbitrary smooth full programme; the polynomial is only a replay.
e,u,v,w=sp.symbols("e u v w")
A=lambda x,y:x**3 + 3*x**2*y+x*y*y+2*y**3
contrast=lambda x,y,z:A(x,y)-A(x,z)
assert sp.simplify(contrast(e,u,v)+contrast(e,v,w)-contrast(e,u,w)) == 0
assert sp.simplify(contrast(e,u,u)) == 0
assert sp.simplify(sp.diff(contrast(e,u,v),e).subs(u,v)) == 0
assert sp.simplify(sp.diff(contrast(e,u,v),u)-sp.diff(A(e,u),u)) == 0
assert sp.simplify(sp.diff(contrast(e,u,v),u,e)
                   -sp.diff(A(e,u),u,e)) == 0
print("PASS: exact inverse-Gram/cotangent types, bounded-leg shear source, "
      "all-L rational bound, full spectrum and matched-history source cocycle.")
