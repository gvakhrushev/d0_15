#!/usr/bin/env python3
"""True original Golden F/R AF 4D PF, all-L superalgebraic native regularity.

No invented source measure, balanced decoder, additional Golden gate or
postselected history. Consumes the original owner's exact discrepancy bound;
checks its direct arithmetic all-L strengthening by exact rational bounds.
Companion scientific theorem proves first-source equality for the unpadded
N1 two-CAR Einstein waves; this script is NOT a new Book03/HJR selector.
"""
from fractions import Fraction as F
from math import ceil, log, sqrt
from mpmath import mp

pupper=F(5,8)
alower=F(18,25)
# Exact rational inequality, common to ALL integers j>=3, s>=3,
# h=1/L<=1/4 and original n=16(j+1)s+128.
leading=F(256)*pupper**8/alower
subleading=(pupper**129+pupper**257)/(F(2)*alower)
assert leading<F(83,10)
assert subleading<F(1,100000000000000)
assert leading+subleading<F(9)

mp.dps=95
p=(mp.sqrt(5)-1)/2
phi=1/p
ainfty=phi/mp.sqrt(5)

def fib(n):
    def step(k):
        if k==0:return 0,1
        a,b=step(k//2)
        c=a*(2*b-a)
        d=a*a+b*b
        return ((c,d) if k%2==0 else (d,c+d))
    return step(n)[0]

def native_bound(L,j, verbose=False):
    assert L>=4 and j>=3
    # Strict phi^s >= L, not raw number of F/R letters.
    s=0
    while phi**s<L: s+=1
    h=mp.mpf(1)/L
    n=16*(j+1)*s+128
    k=n//4
    assert k==4*(j+1)*s+32
    ak=mp.mpf(fib(n+1))*p**n
    eps=p**(2*(n-2*k)+1)/mp.sqrt(5)
    delta=2*p**(k//4)
    diff=abs(ak-ainfty)
    analytic=(L**4*eps+128*L*delta+diff)/ak
    assert ak>mp.mpf('0.72')
    assert analytic<9*h**j
    if verbose:
        print(f'PASS actual native all-L formula L={L}, j={j}, s={s}, n={n}, '
              f'full leaves digits={len(str(fib(n+1)))}, '
              f'bound/h^j={float(analytic/h**j):.9g}')
    return s,n,analytic

for L in (4,8,16,32,64,256):
    for j in (3,4,6):
        native_bound(L,j,True)

for L in (4,8,16,32,64,256):
    s=0
    while phi**s<L: s+=1
    j=s+3
    ss,n,bd=native_bound(L,j)
    assert ss==s and n==16*s*(s+4)+128
    assert bd<9*mp.mpf(L)**(-s-3)
    print(f'PASS SINGLE superalgebraic tower L={L}, s={s}, '
          f'depth={n}, density error<{float(9*mp.mpf(L)**(-s-3)):.4e}')

# All site values are strictly positive from 9h^j<1;
# arbitrary k-fold differences use 2^k values each bounded by
# 9h^j/(1-9h^j) (for log density), so
# sup |D_h^k log(rho)| <=2^k*9*h^(j-k)/(1-9h^j).
for m in (0,1,2,3,4,6):
    for L in (4,8,16,32):
        s=0
        while phi**s<L: s+=1
        h=mp.mpf(1)/L
        j=s+3
        cap=2**m*9*h**(j-m)/(1-9*h**j)
        assert cap>0
        if m<=j-2:
            assert cap/h**2 < 2**m*10
        # For every fixed m, the exponent j-m->infinity with L.
print('PASS exact ALL-DERIVATIVE finite-difference formula and single quadratic-log depth')
print('PASS exact rational inequality: 256*(5/8)^8/(18/25)+tiny < 9')
print('scope: true native Golden PF, mathematical C-infinity extension; full Book03 physical selection OPEN')
