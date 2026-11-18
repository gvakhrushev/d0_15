"""Exact central-sector checks using the project's interleaved Q8 basis."""
from fractions import Fraction as F
from itertools import product


def central(v):
    return [v[i ^ 1] for i in range(8)]


def squared_norm(v):
    return sum(x*x for x in v)


def even_mass(v):
    return sum((x+y)**2 for x,y in zip(v,central(v))) / F(4)


def mass_after(v, a, b):
    return squared_norm([a*x+b*y for x,y in zip(v,central(v))])


def run():
    # Every code vector in the finite check; the manuscript proves the whole cone.
    for v in product(range(3), repeat=8):
        n = squared_norm(v)
        if not n:
            continue
        overlap = sum(v[j]*v[j+1] for j in range(0,8,2))
        assert even_mass(v) == F(n,2) + overlap
        assert F(n,2) <= even_mass(v) <= n
        a,b = F(3,5), F(7,6)
        assert mass_after(v,a,b) == (a-b)**2*n + 4*a*b*even_mass(v)
        assert mass_after(v,a,b) >= (a*a+b*b)*n
    # The four spin columns of T^*, before their common 1/sqrt(2).
    for j in range(0,8,2):
        col = [int(i == j)-int(i == j+1) for i in range(8)]
        assert even_mass(col) == 0
        assert mass_after(col,F(2,3),F(2,3)) == 0
    unit = [1] + [0]*7
    assert even_mass(unit) == F(1,2)
    for c,d in ((F(1,2), F(3,5)), (F(1,3), F(2,3))):
        bright = [c*x for x in unit]
        wrong = [d*(x+y) for x,y in zip(unit,central(unit))]
        full = (even_mass(bright)+even_mass(wrong))/(squared_norm(bright)+squared_norm(wrong))
        assert full == (c*c/2+2*d*d)/(c*c+2*d*d) > F(1,2)
        assert even_mass(bright)/squared_norm(bright) == F(1,2)
        assert even_mass(wrong)/squared_norm(wrong) == 1
    print("Passed: 6560 positive-cone inputs, four odd spin columns, two complete/conditional outputs.")


if __name__ == "__main__":
    run()
