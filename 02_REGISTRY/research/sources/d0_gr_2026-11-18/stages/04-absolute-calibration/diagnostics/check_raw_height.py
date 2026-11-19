"""Integer-only interval exclusion for q* from H.1 in the raw-tree height box."""
from bisect import bisect_left, insort
from fractions import Fraction
from math import isqrt

def add(v,w): return v[0]+w[0],v[1]+w[1]
def neg(v): return -v[0],-v[1]
def mul(v,w):
    a,b=v; c,d=w
    return a*c+b*d,a*d+b*c-b*d
def power(v,n):
    w=ONE
    for _ in range(n): w=mul(w,v)
    return w
def sub(v,w): return add(v,neg(w))
def times(n,v): return n*v[0],n*v[1]
def sgn_int(z): return (z>0)-(z<0)
def sgn(v):
    a,b=v
    c=2*a-b
    if c*b>=0: return sgn_int(c or b)
    return sgn_int(c)*sgn_int(c*c-5*b*b)
def frac_cmp(v,r): return sgn(sub(times(r.denominator,v),(r.numerator,0)))

ONE=(1,0)
p=(0,1)
c=(-1,2)
for _ in range(9): c=sub(times(2,mul(c,c)),ONE)
Q=mul(times(2,power(p,7)),sub(ONE,c))
target=add(power(p,2),mul(power(p,3),Q))
target_lo=Fraction(4124698805685,10**13)
target_hi=Fraction(4124698805686,10**13)
assert frac_cmp(target,target_lo)>0 and frac_cmp(target,target_hi)<0

def floor_kp(k): return (isqrt(5*k*k)-k)//2
S=10**30
for depth,bound,margin in ((1,9,Fraction(7,1000)),
                           (2,145,Fraction(2,100000)),
                           (3,2587,Fraction(3,10**7)),
                           (4,46370,Fraction(3,10**10))):
    # x'_k=x_k+k*sqrt(5), so k<=this certified convenient over-bound;
    # including extra algebraic integers can only strengthen the exclusion.
    B=power((1,1),6*depth)
    assert sgn(sub(times(bound+1,(1,2)),B))>0
    lower,upper=target_lo-margin,target_hi+margin
    assert 0<lower<upper<1
    seen=[0,S]
    for k in range(1,bound+1):
        ak=(floor_kp(k)+1)*S-floor_kp(k*S)-1  # floor(S*x_k)
        insort(seen,ak)
        # Interval arithmetic. If lower*x_k <= x_j <= upper*x_k,
        # its exact floor is inside the following integer interval.
        left=lower.numerator*ak//lower.denominator
        right=upper.numerator*(ak+1)//upper.denominator
        pos=bisect_left(seen,left)
        assert pos==len(seen) or seen[pos]>right, (depth,k,left,right)
    print("L =",depth,"proved |q - q_H.1| >",str(margin),"; k <=",bound)
