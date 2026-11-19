"""Actual Q and noisy H.1 centre, plus an independent finite-memory price example."""
from fractions import Fraction
from itertools import product
from mpmath import iv
import json

# Pair data x+y*p, p^2=1-p.
def mul(k,l):
    x,y=k
    z,w=l
    return (x*z+y*w,x*w+y*z-y*w)

def add(k,l):
    return (k[0]+l[0],k[1]+l[1])

def scale(k,a):
    return (a*k[0],a*k[1])

p=(0,1)
p2=mul(p,p)
p3=mul(p2,p)
p7=mul(mul(p3,p3),p)
x=add(scale(p,2),(-1,0)) # cos(2 theta_G)
for _ in range(9):
    x=add(scale(mul(x,x),2),(-1,0)) # cos(1024 theta_G)
Q=mul(scale(p7,2),add((1,0),scale(x,-1)))
noise=add(p2,mul(p3,Q))
assert all(isinstance(v,int) for row in (Q,noise) for v in row)

# Short interval route avoids cancellation in the exact giant coefficients.
iv.dps=90
p_i=(iv.sqrt(5)-1)/2
c=2*p_i-1
for _ in range(9):
    c=2*c*c-1
q_s=2*p_i**7*(1-c)
q_n=p_i**2+p_i**3*q_s
summary={}
for label,q,lo,hi,lower,upper in [('sharp',q_s,'.12921','.12922','3.9647','3.9649'),('noisy',q_n,'.41246','.41248','.7351','.7352')]:
    slope=iv.log((1-q)/q)/iv.log(1/p_i)
    d=1+3*q*q-slope
    assert iv.mpf(lo)<q and q<iv.mpf(hi)
    assert iv.mpf(lower)<slope and slope<iv.mpf(upper)
    summary[label]={'q':float(q.mid),'log_phi_odds':float(slope.mid),'three_success_cost_net_slope':float(d.mid)}

# Exact direct enumeration of real 0/10 rewards and pathwise derivative,
# checked against every independent coordinate, including both ends.
checks=0
for M in (4,5,7):
    q=Fraction(2,7)
    for j in range(M):
        grad=Fraction()
        for bits in product((0,1),repeat=M):
            prob=q**sum(bits)*(1-q)**(M-sum(bits))
            # The parser emits only 0 or 10; the extra ledger counts every
            # overlap in its successive TRUE labels.
            price=sum(len('10' if b else '0') for b in bits)
            price+=sum(bits[k]*bits[k+1]*bits[k+2] for k in range(M-2))
            score=1/q if bits[j] else -1/(1-q)
            grad+=prob*price*score
        n=sum(k<=j<=k+2 for k in range(M-2))
        assert grad==1+n*q*q
        checks+=1
    assert sum(3-sum(k<=j<=k+2 for k in range(M-2)) for j in range(M))==6
print(json.dumps({'status':'PASS','actual_centres':summary,'independent_exact_rows':checks,
                  'exact_Q_coordinates_digit_counts':[len(str(abs(v))) for v in Q]},indent=2))

# Integer Cauchy bound, independent of numerical precision.
for row in (Q,noise):
    tr=2*row[0]-row[1]
    assert abs(tr)-1>10**473
n=256
H=2**256
num_bound=3*H*(2*n-1)*n*n*16**(n-1)
assert 1+num_bound<10**473
print(f'PASS: cost bound has {len(str(1+num_bound))} digits; both conjugates exceed 10^473.')

# Golden powers in the two embeddings are bounded by (16181/10000)^256,
# which is strictly above phi^256 and still meets the exact threshold.
U_up=8*Fraction(16181,10000)**256
assert 1+(2448*U_up**4)**2 < 10**443
# A symbolic check of the quadratic elimination for arbitrary affine states.
import sympy as sp
q_sym,t0,t1,d0,d1,d2=sp.symbols('x t0 t1 d0 d1 d2')
y=sp.Symbol('y')
t=t0+t1*q_sym
d=d0+d1*q_sym+d2*q_sym**2
F=y*y-t*y+d
E=sp.diff(d,q_sym)**2-t*t1*sp.diff(d,q_sym)+d*t1*t1
assert sp.expand(sp.resultant(F,sp.diff(F,q_sym),y)-E)==0
print('PASS: exact two-state eliminant and the 256-power weight threshold.')

# Uniform catalogues for the fallback n-state bound, including degenerate
# spectra; tight quadratic case above takes precedence at two states.
from math import factorial
for size, exponent in ((3,60),(4,30),(5,13),(6,6)):
    u_bound=8*Fraction(16181,10000)**exponent
    a_bound=factorial(size)*(1+3*u_bound)**size
    res_bound=factorial(2*size-1)*(2*size+1)**size*a_bound**(2*size-1)
    assert 1+res_bound**2<10**473

# The frozen non-PF constant root and the repeated root must be removed.
# A nonconstant critical active root remains exactly in the scalar result.
e,z=sp.symbols('e z')
q=q_sym
active=3+q*q
F=(y-active)*(y-1)*(y+2)**2
D=sp.resultant(F,sp.diff(F,q)+z*sp.diff(F,y)+e,y)
first_e=sp.Poly(D,e).terms()[-1]
assert first_e[0]==(2,)
first_z=sp.Poly(first_e[1],z).terms()[-1]
assert first_z[0]==(1,)
assert first_z[1].subs(q,0)==0 and first_z[1].subs(q,1)!=0
print('PASS: four multi-state height bounds; identically repeated and constant roots removed.')
