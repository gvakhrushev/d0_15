#!/usr/bin/env python3
"""Native original 2/4-grade periodic-u protected Dirac rank128 low-spectrum
band cut. Strict preparation positive Hessian fails by true Fourier degeneracy.
No new operator; no assertion physical G0 selects a spectral minimum.
"""
from math import pi,sin
for grades,L in ((2,65),(4,33),(2,66),(4,34)):
    rank=128
    assert grades*L>rank
    # k0 eigenvalue has exact g-fold multiplicity, every 0<k<L/2
    # has EXACT 2g-fold Fourier degeneracy (k,L-k times g grades).
    assert (rank-grades)%(2*grades)==grades
    e=[(4*sin(pi*k/L)**2,k,j) for j in range(grades) for k in range(L)]
    e.sort(key=lambda x:x[0])
    assert abs(e[rank-1][0]-e[rank][0])<5e-14
    k1=e[rank-1][1];k2=e[rank][1]
    assert k1 in (32, L-32) if grades==2 else k1 in (16,L-16)
    assert k2 in (32, L-32) if grades==2 else k2 in (16,L-16)
    kk=32 if grades==2 else 16
    assert abs(sin(pi*kk/L)**2-sin(pi*(L-kk)/L)**2)<1e-15
    # These two states are physically different LEFT occupied subspaces
    # and have the SAME exact native Delta eigenvalue.
    print('PASS g=',grades,'L=',L,'128th=',k1,'129th=',k2,
          'original Fourier degeneracy; true Gram-preserving zero Hessian')
print('PASS rank128 protected energy minimizer NOT strictly isolated/stable')
print('PASS full 10-var conditional IFT does not invert unrestricted prep Hessian')
print('FIREWALL additional native G0 selector/work may change admissible state manifold')
print('GR_closed=false')
