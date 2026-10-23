"""Exact rational audit of the native age-clock source remainder.

The original native spectral values/first jets below are consumed from
the pinned #334 Ward owner, not obtained by a new full128 matrix replay.
All asserted inequalities use Fraction arithmetic. Floating numbers in
the final JSON are display previews of already certified inequalities.
No Book03 heat, information convention, or physical price is selected.
"""
from fractions import Fraction as F
from math import isqrt, factorial
import json

checks = []


def check(name, condition):
    checks.append({"name": name, "passed": bool(condition)})
    assert condition, name


def interval(q):
    return q if isinstance(q, tuple) else (F(q), F(q))


def add(a, b):
    a, b = interval(a), interval(b)
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    a = interval(a)
    return -a[1], -a[0]


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    a, b = interval(a), interval(b)
    products = [x*y for x in a for y in b]
    return min(products), max(products)


def div(a, b):
    b = interval(b)
    assert not b[0] <= 0 <= b[1]
    return mul(a, (1/b[1], 1/b[0]))


def absolute_bound(a):
    a = interval(a)
    return max(abs(a[0]), abs(a[1]))


def sqrt_interval(q, scale=10**30):
    q = F(q)
    assert q > 0
    n = isqrt(q.numerator * scale**2 // q.denominator)
    lo, hi = F(n, scale), F(n+1, scale)
    assert lo**2 <= q < hi**2
    return lo, hi


# Original exact two-band data at (r,nu)=(1/9,3/5).
mu = F(141489, 10240000)
h = F(69399, 5030720)
mu_r = -F(328779, 204800000)
h_r = -F(20040939, 9885993640)
mu_v = mu_r - mu*h_r/h
e_squared = mu*(mu-h)
e = sqrt_interval(e_squared)
t = sub(3, sqrt_interval(5))  # t=2/phi^2=3-sqrt(5).
lambda_minus = sub(mu, e)
lambda_plus = add(mu, e)

check("original positive two-band discriminant", e_squared > 0)
check("exact Golden thermal interval .76<t<.8", F(76,100) < t[0] < t[1] < F(8,10))
check("lambda_min>.01325", lambda_minus[0] > F(1325,100000))
check("lambda_max<.01456", lambda_plus[1] < F(1456,100000))
check("native harmonic mean h<.0138", F(0) < h < F(138,10000))
check("native one-port-null mu derivative positive and <.00044", F(0) < mu_v < F(44,100000))

q = F(12,1000)
check("native t lambda_max below q=.012", mul(t,lambda_plus)[1] < q)


def coefficient(k):
    assert k >= 1
    return (F(1,k+1)-F(2,k)+F(1,k*2**k)
            +sum((F(1,2**(k-j+1)*j) for j in range(1,k+1)),F(0)))


check("exact Taylor coefficient a1", coefficient(1) == F(-1,2))
check("exact Taylor coefficient a2", coefficient(2) == F(-1,24))
check("exact Taylor coefficient a3", coefficient(3) == F(1,24))
check("exact Taylor coefficient a4", coefficient(4) == F(47,960))

# The all-k |a_k|<=1 and moment-derivative inequality are proved in
# AGE_CLOCK_SOURCE.md and reviewed in INDEPENDENT_REVIEW.md. This expression
# sums their entire differentiated tail, not a finite truncation test.
tail_factor = (1+q)/(1-q)**3 - 1 - 4*q
check("entire differentiated Taylor tail positive", tail_factor > 0)
check("negative quadratic source dominates all later terms", q/6 + tail_factor < F(1,24))
source_upper = F(8,10)**2 * F(138,10000) * F(44,100000) * (F(1,24)+q/6+tail_factor)
check("rigorous native entropy-source magnitude below 1.8e-7", source_upper < F(18,10**8))

# Strict actual-source bounds for both the original boost and its port-null
# combination. These are interval evaluations of the differentiated spectral
# formulas, with rigorously enclosed sqrt(5) and sqrt(mu*(mu-h)).
for name, dm, dh in [("proper_boost",mu_r,h_r),("one_port_null",mu_v,F(0))]:
    de = div((2*mu-h)*dm-mu*dh, mul(2,e))
    dw = div(sub(mul(de,mu),mul(e,dm)),2*mu**2)
    check(name+": sum absolute band-weight jets <1", 2*absolute_bound(dw) < 1)
    for sign_name, lam, dlam in [("minus",lambda_minus,sub(dm,de)),("plus",lambda_plus,add(dm,de))]:
        b = sub(1,mul(t,lam))
        s = mul(b,b)
        ds = mul(mul(mul(-2,t),b),dlam)
        check(name+" "+sign_name+": .97<s<.98", F(97,100) < s[0] and s[1] < F(98,100))
        check(name+" "+sign_name+": absolute age-probability jet <.02", absolute_bound(ds) < F(2,100))

# g(s)<6 and g'(s)<100 on .97<s<.98 follow analytically from
# -s log(s)/(1-s)<1, log(50)<4, and g'(s)<=1/[s(1-s)].
exp4_partial = sum((F(4)**n/F(factorial(n)) for n in range(8)),F(0))
check("log50<4 via exact positive exp4 partial sum", exp4_partial > 50)
check("geometric entropy derivative bound below100", 1/(F(97,100)*F(2,100)) < 100)

cap = 4096
r = F(98,100)
entropy_tail = 6*r**cap
source_tail = r**cap*(8+F(2,100)*cap*6/r)
check("finite cap4096 entropy tail below7e-36", entropy_tail < F(7,10**36))
check("finite cap4096 source tail below6e-34", source_tail < F(6,10**34))
check("finite logarithmic Gibbs tail is positive", r**cap < F(2,100))

print(json.dumps({
    "scope":"exact rational spectral/remainder audit; original native spectral data consumed, no new full128 replay or physical Book03 identification",
    "pass_count":len(checks),
    "checks":checks,
    "exact_source_upper":str(source_upper),
    "display_only":{
        "source_upper":float(source_upper),
        "differentiated_tail_factor":float(tail_factor),
        "finite_cap_entropy_tail_bound":float(entropy_tail),
        "finite_cap_source_tail_bound":float(source_tail)
    }
},indent=2))
