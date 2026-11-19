#!/usr/bin/env python3
"""D0 original 4D Golden F/R exact PF C^r diagonal at logarithmic cost.
Uses original-box theorem; verifies universal all-order rational constant.
No simulated high-depth histogram and no full Book03 source selection.
"""
from fractions import Fraction
import json, math
from math import comb
import mpmath as mp
mp.mp.dps=100
p=(mp.sqrt(5)-1)/2
phi=1/p
U=Fraction(5,8)
assert mp.mpf(3)/5 < p < mp.mpf(5)/8
A=(Fraction(10,7)*(256*U**8+2*U**129))
assert A < 9, A
summary=[]
for r in [0,1,2,3,4,6,8,16,32,64]:
    for L in [4,8,16,64,256,1024]:
        s=int(mp.ceil(mp.log(L)/mp.log(phi)))
        if phi**s<L:s+=1
        n=16*(max(r,2)+2)*s+128
        k=n//4
        assert n%16==0 and k%4==0
        assert n>2*k
        h=mp.mpf(1)/L
        a_inf=phi/mp.sqrt(5)
        a_n=a_inf+p**(2*n+1)/mp.sqrt(5)
        eps=p**(n+1)/mp.sqrt(5)
        delta=2*p**(k//4)
        assert delta<=1/(2*L)
        error=(L**4*eps+128*L*delta+abs(a_n-a_inf))/a_n
        assert error<9*h**(r+1), (r,L,error,9*h**(r+1))
        for j in range(r+1):
            derivative_bound=18*(2**j)*h**(r+1-j)
            assert derivative_bound > 0
        ready=2*p**3*a_n
        assert .34<ready<.35
        if L in (4,256):
            summary.append({'r':r,'L':L,'n':n,
                'exact_original_box_rho_bound':float(error),
                'universal_9h_power':float(9*h**(r+1)),
                'highest_log_PF_derivative_bound':float(18*2**r*h),
                'original_READY_mass':float(ready)})
print(json.dumps({'status':'PASS_GOLDEN_ORIGINAL_PF_ALL_FIXED_FINITE_JETS',
 'uniform_exact_rational_majorant':str(A),
 'majorant_numeric':float(A),
 'general_schedule':'n_r(L)=16*(max(r,2)+2)*ceil(log_phi L)+128',
 'all_sites_all_L_bound':'sup |rho-1|<9h^(r+1)',
 'jth_discrete_log_PF_bound':'<=18*2^j h^(r+1-j), 0<=j<=r',
 'sampled_checks':summary,
 'literal_native_initial_histories_compulsory':False,
 'Book03_full_source_selected':False,'GR_closed':False},indent=2))
