"""Exact stopped likelihood exponents, score variance, and native calibration contrast."""
from fractions import Fraction as F
from math import isclose, log, sqrt


def words(cap):
    # (human-readable record, number of same-sector steps, number of changes)
    yield ('P', 1, 0)
    for n in range(cap):
        yield ('B' * (n+1) + 'P', n, 2)
    yield ('B' * (cap+1), cap, 1)


def bernoulli_divergence(u, v):
    return float(u)*log(float(u/v)) + float(1-u)*log(float((1-u)/(1-v)))


def law(u, cap):
    return [(u**stay * (1-u)**change, stay, change) for _, stay, change in words(cap)]


def verify_at(u, v, cap):
    inventory = law(u, cap)
    assert sum(q for q, _, _ in inventory) == 1
    n = 2-u**cap
    assert sum(q*s for q,s,_ in inventory) == u*n
    assert sum(q*t for q,_,t in inventory) == (1-u)*n
    score = [(q, s/u-t/(1-u)) for q,s,t in inventory]
    assert sum(q*g for q,g in score) == 0
    assert sum(q*g*g for q,g in score) == n/(u*(1-u))
    target = law(v, cap)
    kl = sum(float(q)*log(float(q/r)) for (q,_,_), (r,_,_) in zip(inventory,target))
    assert isclose(kl, float(n)*bernoulli_divergence(u,v), rel_tol=1e-12, abs_tol=1e-14)
    return kl


def main():
    p=(sqrt(5)-1)/2
    v0,v1 = p**12, p**18
    assert isclose((p-p*p)**4, v0) and isclose((p-p*p)**6, v1)
    intercept = log((1-v1)/(1-v0))
    slope = log(v1/v0)-intercept
    assert 0.00293736 < intercept < 0.00293738 and -2.89021 < slope < -2.89020
    total = 0
    for field in [F(1,4), F(1,3), F(3,8)]:
        u = (1-2*field)**2
        for cap in [0,1,2,5,12,25]:
            for v in [F(1,11), F(1,4), F(9,10)]:
                verify_at(u, v, cap)
            inventory = law(u, cap)
            n = 2-u**cap
            logs = []
            for v in (v0,v1):
                logs.append(sum(float(q)*(log(float(q))-s*log(v)-t*log(1-v))
                                for q,s,t in inventory))
            assert isclose((logs[0]-logs[1])/float(n), intercept + slope*float(u),
                           abs_tol=2e-14)
            # Two-coordinate chart as an arithmetic identity. No external
            # setting is inserted into the physical H.1 controller.
            gradient = (F(2,3),F(-5,7))
            b = F(1,21)
            for i in range(2):
                for j in range(2):
                    dui = -4*(1-2*field)*b*gradient[i]
                    duj = -4*(1-2*field)*b*gradient[j]
                    gram = sum(q*(s/u-t/(1-u))**2*dui*duj for q,s,t in inventory)
                    assert gram == 16*n*b*b*gradient[i]*gradient[j]/(1-u)
            total += 1
    print(f'{total} full capped fields/trees; exact score variance, all directional entries')
    print('references', v0, v1, 'intercept', intercept, 'slope', slope)


if __name__=='__main__':
    main()
