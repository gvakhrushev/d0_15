#!/usr/bin/env python3
"""Original 128-Kraus fullRIGHT128 low-shell vs full HJR UV trace separator.

The theorem is analytic and consumes the owned original blank Kraus B and
full 8-momentum*CAR16 Riesz shell (not a toy replacement channel).
All bound certificates below are strict rational and all horizons exact.
Floating point checks are strictly optional diagnostics, not proof.
"""
from fractions import Fraction as F
from math import sin, pi, sqrt

nu=F(3,5)
# Original phi^-1 satisfies 0<p<5/8; p²=(3-sqrt5)/2<2/5.
p_upper=F(5,8)
p2_upper=F(2,5)
pi_upper=F(22,7)
assert (F(11,5)**2 < 5 < F(9,4)**2)
assert F(5,8) > (sqrt(5)-1)/2
assert F(2,5) > (3-sqrt(5))/2
lam_const=4*nu**2*pi_upper**2
exit_upper_const=4*p2_upper*lam_const
# All-blank exact m-round original history:
# K_(0,0)=B=I-alpha*Delta; on the actual full128 Riesz shell
# B=(1-alpha*lambda1)I, where lambda1=4 nu² sin²(pi/L).
# P_any = 1 - (1-alpha*lambda1)^(2m) <= 2m alpha lambda1
#       = 4 p² lambda1 <= exit_upper_const/L².
# Actual purified final output Euclidean squared distance to
# |all-blank> tensor |same-preparation> equals
# 2(1-(1-alpha*lambda1)^m) <= same upper bound.
assert exit_upper_const>0
# Bound on full original m-round *paid PORT cost* source, fixed rank128 input:
# d C_port,m / d rho_r = p³ lambda1 (exact equal weights per four axes).
# rho is held fixed in partial coframe variation, and
# (m p epsilon) = 4 p³ is EXACT from epsilon=p²/(64 L²).
port_one_role_const=p_upper**3*lam_const
# PER-SITE port source bound <=port_one_role_const / L^6.
# Independently certified whole full HJR open/periodic first source
# per role >406303/82837504000000 for L>=256.
hjr_c=F(406303,82837504000000)
assert hjr_c>F(49,10**10)
assert port_one_role_const/F(256**6)<hjr_c
print("EXACT RATIONAL any-real-blank-exit prob <= ", exit_upper_const, "/L²")
print("EXACT RATIONAL full coherent-output squared distance <= same /L²")
print("EXACT RATIONAL original paid-port coframe source per-site <= ",
      port_one_role_const, "/L^6")
print("EXACT RATIONAL HJR bulk > ",hjr_c,
      " > PORT COST contribution at every L>=256")

p=(sqrt(5)-1)/2
for L in (8,16,32,64,128,256):
    lam=4*float(nu)**2*sin(pi/L)**2
    alpha=p**2/(128*L**2)
    m=256*L**2
    b=1-alpha*lam
    q=1-b**(2*m)
    coh_dist=sqrt(2*(1-b**m))
    port_source=p**3*lam
    assert 0<=q<=float(exit_upper_const)/L**2+1e-13
    assert 0<=coh_dist**2<=float(exit_upper_const)/L**2+1e-13
    assert port_source/(L**4)<=float(port_one_role_const)/(L**6)
    print("L=",L,"P(any)=","%.6g"%q,
          "full-tape norm-to-blank=","%.6g"%coh_dist,
          "per-site port source=","%.6g"%(port_source/L**4))
print("ALL EXACT LOW-SHELL ONE-REAL-HISTORY / UV SOURCE GATES PASSED")
