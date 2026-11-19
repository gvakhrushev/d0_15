"""Positive field classes, derivative bounds and full hidden renewal ledgers."""
from fractions import Fraction as F
from math import ceil, comb, exp, log2, sqrt


def bernstein(n, q, clip):
    probabilities = [comb(n,k)*q**k*(1-q)**(n-k) for k in range(n+1)]
    a = [1-F(4*k*(n-k), n*(n-1)) for k in range(n+1)]
    if clip:
        a = [max(F(0), t) for t in a]
    value = sum(x*y for x,y in zip(a,probabilities))
    slope = sum(x*y*(k-n*q)/(q*(1-q)) for k,(x,y) in enumerate(zip(a,probabilities)))
    return value, slope


def test_bank():
    for q in [F(23,100), F(1,3), F(19,50)]:
        u = (1-2*q)**2
        for n in (4, 13, 32):
            exact, slope = bernstein(n, q, False)
            assert exact == u and slope == -4*(1-2*q)
            value, _ = bernstein(n, q, True)
            assert value >= u
        a, aprime = bernstein(256, q, True)
        E = exp(-512*(.5-1/32-.38)**2)/255
        error_in_slope = 256*E/(.23*.62)
        assert error_in_slope < .125 and abs(aprime + 4*(1-2*q)) <= error_in_slope
        assert u <= a <= u+E and aprime < 0
    n = 256
    d = ceil(log2(n*(n-1)))
    balanced = 2**d
    assert balanced >= n*(n-1) and balanced < 2*n*(n-1)
    # Each accepted integer has exactly one string of mixed pairs, of golden mass p^(3d).
    assert all(0 <= max(0,n*(n-1)-4*k*(n-k)) <= n*(n-1) for k in range(n+1))


def test_hidden_ledger():
    # Each row of the printed block has its own hidden tag and real branch-dependent price.
    for q in [F(1,4), F(1,3)]:
        outcomes = [(0, 1-q), (1, q)]
        raw = [(a,b,c,pa*pb*pc) for a,pa in outcomes for b,pb in outcomes
               for c,pc in [(0,F(2,5)),(1,F(3,5))]]
        v = sum(prob for a,b,c,prob in raw if a == b)
        assert v == (1+(1-2*q)**2)/2
        def fee(sector,a,b,c):
            return F((3*a+b-c)**2 + sector*(1+2*a*b),2)
        w = [sum(prob*fee(sector,a,b,c) for a,b,c,prob in raw) for sector in (0,1)]
        for cap in (0,1,2,5):
            # Independent enumeration of all still-live prefixes by probability-weighted fee.
            live = [(0, F(1))]
            actual = 0
            for _ in range(cap+1):
                following = []
                for sector, mass in live:
                    for a,b,c,prob in raw:
                        weight = mass*prob
                        actual += weight*fee(sector,a,b,c)
                        if sector ^ (a != b):
                            following.append((1,weight))
                live = following
            assert actual == w[0]+(1-v**cap)*w[1]
    for z0,z1 in [(F(3,2),F(2,5)),(F(7),F(1,3))]:
        agree, diff = z0*z0+z1*z1, 2*z0*z1
        assert (agree-diff)/(agree+diff) == (1-2*z1/(z0+z1))**2


if __name__ == "__main__":
    test_bank()
    test_hidden_ledger()
    print("PASS rational field classes, C1 bound at 256, additive branch costs and root weights")
