"""Complete fine effects, physical Fourier site covariance, and later inverse control."""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import sys

import numpy as np
import sympy as sp

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parents[7]
sys.path.insert(0,str(root/"02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source"))
import check_primary_car_preparation_source as car

# The real Fourier owner uses f/128 as the C row before the local grade amplitude.
F = np.array(car.fourier_numerators(),dtype=np.int64)
assert F.shape == (256,128)
assert np.array_equal(F.T@F,128*np.eye(128,dtype=np.int64))
assert np.all((F*F).sum(axis=1)==64)
site=(1,1,1,1)
row=F[car.site_index(site)]
pnum=np.outer(row,row)
assert np.array_equal(pnum@pnum,64*pnum)
assert np.trace(pnum)==64 and np.count_nonzero(row)>0

# A small single-site A=15 amplitude gives these exact local inverse-null-metric
# energies in units of its squared forward difference. All unspecified entries vanish.
def field(z):
    return int(z==site)
energies=[]
for z in car.SITES_LIST:
    dz=[field(car.step(z,i,1))-field(z) for i in range(4)]
    energies.append(2*dz[0]*dz[1]-dz[2]**2-dz[3]**2)
assert energies.count(-1)==2 and energies.count(0)==254
assert sum(energies)==-2

# Original prefix monomials of the ten-sign truth table (3); testing all 0..8
# monomials proves the covariance formula for their exact Golden combination.
# A material sign with mean t and the marked private RIGHT test have joint
# probability E[sign*R]=t, E[R]=1/128. Sum over the choice of one private copy
# in each of the eight material sign sources, leaving other generated banks alone.
t=Q(-1,311)
D=128
for degree in range(9):
    marginal=t**degree
    correction=Q(0)
    for a in range(8):
        moment=(t*t**(degree-1) if a<degree else marginal/D)
        correction+=moment-marginal/D
    assert correction==(1-Q(1,D))*degree*t**degree

# The eight-reader discrete extrapolation kills degrees 3,...,9 in the field
# signal, keeping degree 2; differentiating the matter-strength coefficient
# before or after the same finite sum is exact.
for n in range(2,10):
    assert sum(Q((-1)**(j-1)*comb(8,j),j*j)*j**n for j in range(1,9))==int(n==2)

# Fine classical labels can reveal a reference while the coarse flag stays scalar.
p=sp.symbols("p",positive=True)
z=sp.diag(1,0)
o=sp.diag(0,1)
effects=[p*z,p*o,(1-p)*z,(1-p)*o]
assert effects[0]+effects[1]==p*sp.eye(2)
assert all(a!=sp.trace(a)*sp.eye(2)/2 for a in effects)

# A later unitary acts on the very reference being compared. A controlled swap
# moves its correlated computational bit to a fresh blank: the old bit is
# retained, but the same late reference has a constant state.
for sign in (0,1):
    mark,right,fresh=sign,sign,0
    right,fresh=fresh,right
    assert (mark,right,fresh)==(sign,0,sign)
print("128 orthogonal Fourier columns; rank-one local bump, two nonzero spacelike cells; "
      "all nine ten-sign monomials, eight settings, scalar coarse counterexample and late cut verified.")
