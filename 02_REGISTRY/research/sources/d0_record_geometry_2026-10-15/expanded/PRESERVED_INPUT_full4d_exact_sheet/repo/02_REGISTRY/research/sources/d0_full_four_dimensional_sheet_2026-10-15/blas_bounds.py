"""Rigorous normwise enclosures for binary64 real matrix products.
For inner dimension <=512, GAMMA=2^-38 exceeds gamma_(8n+32).
Products use IEEE binary64 operations (or FMA/higher precision, no worse).
Subnormal roundoff is bounded conservatively by 2^-1000 per entry.
The small-matrix interval kernel itself uses operationwise nextafter.
"""
import numpy as np
GAMMA=2.**-38
TINY=2.**-1000

def up(x):return np.nextafter(x,np.inf)
def upper_product(A,B):
 if A.shape[1]>512 or np.any(A<0) or np.any(B<0):raise ValueError('positive product scope')
 y=A@B
 if not np.all(np.isfinite(y)):raise ArithmeticError('nonfinite BLAS result')
 # Exact positive product <= computed/(1-gamma)+underflow allowance.
 return up(up(y/(1-GAMMA))+TINY)

def complex_left_residual(Br,Bi,Hr,Hi):
 # Midpoints rounded to binary64, radii include that rounding exactly.
 mr=Hr.l/2+Hr.h/2;mi=Hi.l/2+Hi.h/2
 rr=up(np.maximum(mr-Hr.l,Hr.h-mr));ri=up(np.maximum(mi-Hi.l,Hi.h-mi))
 br=np.abs(Br);bi=np.abs(Bi)
 mag=up(upper_product(up(br+bi),up(np.abs(mr)+np.abs(mi))))
 rad=upper_product(up(br+bi),up(rr+ri))
 pr=Br@mr-Bi@mi;pi=Br@mi+Bi@mr
 real=np.eye(Br.shape[0])-pr;imag=-pi
 # One common generous bound covers all real/imag products, sums, and I-.
 err=up(up(GAMMA*up(mag+1))+rad)
 return up(up(np.abs(real)+np.abs(imag))+up(2*err))
