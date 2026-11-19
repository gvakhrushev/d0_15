"""Exact conditional clocks and block padding on a changing four-outcome law."""
from fractions import Fraction as F
from math import comb


def paired_registered(q):
    independent = [(b, q if b else 1-q) for b in (0, 1)]
    paid = 2*(1+2*q*(1-q))
    equality_ticks = sum(x*y*2*(i == j) for i,x in independent for j,y in independent)
    return paid, equality_ticks


def compositions(m, d):
    if d == 1:
        yield (m,)
        return
    for k in range(m+1):
        for tail in compositions(m-k, d-1):
            yield (k, *tail)


def tariff(law):
    # Joint outcomes J=0/1, T=0/1, including histories with empty empirical cells.
    value = F(1)
    for i in (0, 2):
        mass = law[i] + law[i+1]
        if mass:
            value += 2*law[i]*law[i+1]/mass
    return value


def differential(law, direction):
    value = 0
    for i in (0, 2):
        a, b = law[i:i+2]
        da, db = direction[i:i+2]
        value += 2*(da*b*b + db*a*a)/(a+b)**2
    return value


def empirical(m, law, direction):
    total = derivative = 0
    for counts in compositions(m, len(law)):
        prob, score, left = F(1), F(), m
        for n, p, dp in zip(counts, law, direction):
            prob *= comb(left, n)*p**n
            score += n*dp/p
            left -= n
        amount = tariff(tuple(F(n,m) for n in counts))
        total += prob*amount
        derivative += prob*amount*score
    return total, derivative


def main():
    for num in range(101):
        q = F(num,100)
        assert sum(paired_registered(q)) == 4
        assert paired_registered(1-q) == paired_registered(q)

    # Fixed P(J)=1/2, marginals Q unchanged while the two conditional rows change.
    law = (F(3,8), F(1,8), F(1,4), F(1,4))
    direction = (F(-1,16), F(1,16), F(1,16), F(-1,16))
    assert sum(direction) == direction[1]+direction[3] == 0
    assert differential(law, direction) == F(1,16)
    for m in (2, 5, 12):
        observed, slope = empirical(m, law, direction)
        # For known mass a=1/2, E[N]=m/2; each nonempty sample variance loses one count.
        factor = 1 - F(2,m)*(1-F(1,2)**m)
        assert observed == 1 + factor*(tariff(law)-1)
        assert slope == factor*differential(law, direction)
        print("block", m, "transverse tariff derivative after empirical payment",
              differential(law, direction)-slope)
    print("101 paired conditional clocks have exactly field-independent total work")


if __name__ == "__main__":
    main()
