"""Integer Golden padding and type bounds on the original EIGHT prefix alphabet."""
from functools import lru_cache
from itertools import combinations_with_replacement
from math import comb, factorial, log, prod, sqrt


PHI = (1+sqrt(5))/2
P = 1/PHI
ALLOCATION = [5644800, 4939200, 4390400, 3087000, 1580544, 548800, 115200, 11025]


@lru_cache(maxsize=None)
def fib_pair(n):
    if n == 0:
        return 0, 1
    a,b = fib_pair(n//2)
    c,d = a*(2*b-a), a*a+b*b
    return (d,c+d) if n % 2 else (c,d)


def scaled_power_ge(exponent, denominator, numerator):
    f, following = fib_pair(exponent)
    lucas = 2*following-f
    right = 2*numerator-denominator*lucas
    return right <= 0 or 5*(denominator*f)**2 >= right**2


def padding(numerator, denominator):
    assert 0 < denominator <= numerator
    lo,hi = -1,1
    while not scaled_power_ge(hi,denominator,numerator):
        hi *= 2
    while hi-lo > 1:
        mid = (lo+hi)//2
        if scaled_power_ge(mid,denominator,numerator):
            hi = mid
        else:
            lo = mid
    return hi


def check_groups(multiplicities, group_mass, positive, tangent, n):
    dimension = len(group_mass)
    assert abs(sum(group_mass)-1) < 2e-12 and abs(sum(tangent)) < 2e-12
    alphabet = sum(multiplicities)
    alpha = [mass*P**t for mass,t in zip(group_mass,positive)]
    z = sum(alpha)
    pi = [x/z for x in alpha]
    score = [dx/x for dx,x in zip(tangent,group_mass)]
    best = float("-inf")
    winners = []
    total = 0.
    if dimension == 2:
        types = ([k,n-k] for k in range(n+1))
    else:
        types = ([seq.count(i) for i in range(dimension)]
                 for seq in combinations_with_replacement(range(dimension),n))
    for k in types:
        mult = factorial(n)//prod(factorial(x) for x in k)
        fine = mult*prod(m**x for m,x in zip(multiplicities,k))
        l = padding(alphabet**n, fine)
        assert scaled_power_ge(l, fine, alphabet**n)
        assert l == 0 or not scaled_power_ge(l-1, fine, alphabet**n)
        surcharge = sum(x*t for x,t in zip(k,positive))
        logweight = sum(x*log(b/m) for x,b,m in zip(k,group_mass,multiplicities)) + (l+surcharge)*log(P)
        typeprob = mult*prod(w**x for w,x in zip(pi,k))
        total += typeprob
        # The tolerance groups near-ties in this numeric cross-check; exact padding above.
        if logweight > best + 1e-10:
            best,winners = logweight,[k]
        elif abs(logweight-best) <= 1e-10:
            winners.append(k)
    assert abs(total-1) < 2e-11
    logtypes = log(comb(n+dimension-1,dimension-1))
    eps = (logtypes - log(P))/n
    objective = -best/n - log(alphabet)
    assert -2e-12 <= objective+log(z) <= eps+2e-12
    derivative = -sum(s*r for s,r in zip(score,pi))
    assert abs(derivative + sum(t*P**j for t,j in zip(tangent,positive))/z) < 1e-12
    for k in winners:
        nu = [x/n for x in k]
        kl = sum(x*log(x/r) for x,r in zip(nu,pi) if x)
        assert kl <= eps+1e-12
        l1 = sum(abs(x-y) for x,y in zip(nu,pi))
        assert l1 <= sqrt(2*eps)+2e-12
        actual = -sum(s*r for s,r in zip(score,nu))
        assert abs(actual-derivative) <= sqrt(2*eps)*max(map(abs,score))+2e-12
    return objective, derivative


def main():
    assert padding(1,1) == 0
    for n in (1,2,5,20,128,256):
        check_groups([3,5],[.72,.28],[0,1],[-.25,.25],n)
    fine36, over = fib_pair(37)[0], fib_pair(36)[0]
    assert (fine36, over) == (24157817,14930352)
    counts, masses, positive, tangent = [], [], [], []
    for j,number in enumerate(ALLOCATION):
        # Preserve actual prefix masses; the conditional readout values illustrate the general identity.
        q = P**2 + P**3*(.06+.01*j)
        weight = number*P**36
        counts.extend([number,number])
        masses.extend([weight*(1-q),weight*q])
        positive.extend([j%2,1-j%2])
        dq = (.04 if j%2 else -.05)*weight
        tangent.extend([-dq,dq])
    inactive = fine36-sum(ALLOCATION)
    assert inactive == 3840848
    counts.extend([inactive,over])
    masses.extend([inactive*P**36,over*P**37])
    positive.extend([0,0])
    tangent.extend([0.,0.])
    assert max(m/c for m,c in zip(masses,counts)) == P**36
    for n in (1,2,3):
        check_groups(counts,masses,positive,tangent,n)
    # Unknown common per-symbol energy and a moving absolute normalization.
    probs = [.13, .67, .20]
    tag = [0, 1, 1]
    for beta in [.41, 1., 2.6]:
        s = P**beta
        for scale in [.126, 3.19]:
            weights = [scale*w**beta for w in probs]
            raw_max, tilted_max = 0., 0.
            n = 8
            for seq in combinations_with_replacement(range(3),n):
                counts = [seq.count(j) for j in range(3)]
                mult = factorial(n)//prod(factorial(k) for k in counts)
                extra = padding(3**n,mult)
                base = prod(w**k for w,k in zip(weights,counts))*s**extra
                raw_max = max(raw_max,base)
                tilted_max = max(tilted_max,base*s**sum(k*t for k,t in zip(counts,tag)))
            C = sum(w**(1/beta) for w in weights)
            Z = sum(w**(1/beta)*P**t for w,t in zip(weights,tag))
            assert abs(Z/C-(1-(1-P)*.87))<1e-13
            for actual, expected in [(raw_max,C),(tilted_max,Z)]:
                err = -log(actual)/n - beta*log(3) + beta*log(expected)
                assert -1e-12 <= err <= beta*log(comb(n+2,2)/P)/n + 1e-12
    print("PASS exact integer padding, all 18 EIGHT groups, modal bounds and directional slopes")


if __name__ == "__main__":
    main()
