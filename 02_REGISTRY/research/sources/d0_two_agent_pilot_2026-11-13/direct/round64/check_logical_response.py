"""Exact five-preparation bounds and coherent readout checks."""
from fractions import Fraction
from itertools import product
import sympy as sp


x = sp.Symbol("x", real=True)
minimal = x**4+x**2-1
floor = Fraction(7861513777, 10**10)
ceil = Fraction(7861513778, 10**10)


def reduced(value):
    num, den = sp.cancel(value).as_numer_denom()
    inverse = sp.invert(den, minimal, x)
    return sp.Poly(sp.rem(num*inverse, minimal, x), x, domain=sp.QQ)


def enclosure(poly):
    lower = upper = Fraction(0)
    for (degree,), coeff in poly.terms():
        c = Fraction(int(coeff.p), int(coeff.q))
        endpoints = c*floor**degree, c*ceil**degree
        lower += min(endpoints)
        upper += max(endpoints)
    return lower, upper


def inversion_check():
    assert floor**4+floor**2 < 1 < ceil**4+ceil**2
    probes = [(1, 0), (0, 1), (x, x**2), (x, -x**2), (x**2, x)]
    rows = []
    for a, b in probes:
        assert reduced(a*a+b*b-1).is_zero
        h = (a*a, 2*a*b, b*b)
        rows.append([-b*b*z for z in h] + [(1-b*b)*z for z in h])
    matrix = sp.Matrix(rows+[[1, 0, 1, 1, 0, 1]])
    det = reduced(matrix.det())
    assert det == reduced(544*x*x-336) and enclosure(det)[0] > 0
    inv = matrix.inv(method="DM")
    bounds = [sum(max(map(abs,enclosure(reduced(inv[i,j])))) for j in range(5)) for i in range(6)]
    assert max(bounds) < 7
    return float(max(bounds))


def hidden_response_check():
    # Rational independent fixture with two retained output memory coordinates.
    F0 = sp.Matrix([[3, 1], [1, 2]])
    F1 = sp.Matrix([[1, 0], [0, 2]])
    directions = [sp.Matrix(u) for u in [(1, 0), (0, 1), (4, 3), (4, -3), (3, 4), (3, -4)]]
    rows = []
    for u in directions:
        x0, x1 = u
        q = (u.T*F1*u)[0] / (u.T*(F0+F1)*u)[0]
        squares = (x0*x0, 2*x0*x1, x1*x1)
        rows.append([-q*z for z in squares]+[(1-q)*z for z in squares])
    truth = sp.Matrix([3,1,2,1,0,2])
    assert sp.Matrix(rows[:5]).rank() == 5 and sp.Matrix(rows)*truth == sp.zeros(6,1)
    # Complete computational identity can coexist with a perfect unused which-bit record.
    tag = sp.Matrix([[1,0], [0,0], [0,0], [0,1]])
    P0 = sp.diag(1,1,0,0)
    assert tag.T*P0*tag == sp.diag(1,0) and tag.T*(sp.eye(4)-P0)*tag == sp.diag(0,1)
    a, p = x, x**2
    v = sp.Matrix([a,p])
    reader = sp.kronecker_product(sp.Matrix([[-p,a]]),sp.eye(2))
    dark = reader*tag*v
    assert reduced((dark.T*dark)[0]-2*p**3).is_zero
    # A shared memory-sensitive false port can miss the tagged-bit failure on both words.
    bare = sp.kronecker_product(sp.eye(2),sp.Matrix([1,0]))
    false_port = sp.Matrix([p,0,-a,-a])
    assert (false_port.T*bare*v)[0] == (false_port.T*tag*v)[0] == 0
    assert (false_port.T*bare*sp.Matrix([1,0]))[0] == p
    # Certify 2+(1+sqrt(p²+p⁴))²/p³ < 16 by rational interval bounds.
    p_min, p_max = floor**2, ceil**2
    assert p_max**2+p_max**4 < Fraction(73,100)**2
    assert 2+(1+Fraction(73,100))**2/p_min**3 < 16


def eight_paths():
    # The signed table is expanded independently of a microscopic Cost/Info assignment.
    for i, j in product((0,1), repeat=2):
        phases = [(-1)**(i*(1-mid)+mid+mid*(1-j)+j) for mid in (0,1)]
        assert phases == ([1,1] if i == j else [-1,1])
        weights = [(x if i == mid else x**2)*(x if mid == j else x**2) for mid in (0,1)]
        assert reduced(sum(s*w for s,w in zip(phases,weights))-int(i==j)).is_zero
    # Positive uncorrelated path totals are not needed for the effect reconstruction.
    # Exercise a non-factorizable joint tariff: one middle-bit slice has rank two.
    totals = {(i,m,j):sp.Rational(1+i+2*m+3*j,9) for i,m,j in product((0,1),repeat=3)}
    assert sp.Matrix(2,2,lambda i,j:totals[i,0,j]).det() != 0
    M = sp.Matrix(2,2,lambda j,i:totals[i,1,j]+(1 if i==j else -1)*totals[i,0,j])
    F0 = M.T*sp.diag(1,0)*M
    F1 = M.T*sp.diag(0,1)*M
    assert M.det() != 0 and (F0+F1).det() == M.det()**2


def field_odds_check():
    q, t = sp.symbols("q t", positive=True)
    a, b, c, d, h = sp.symbols("a b c d h", positive=True)
    # Distinct native informative arms, with arbitrary positive row and column expenses.
    masses = sp.Matrix([[a*c*(1-q-t),a*d*(q+t)], [b*c*(1-q+t), b*d*(q-t)]])
    def odds(table):
        return sp.cancel(table[0,1]*table[1,0]/(table[0,0]*table[1,1]))
    expected = (q+t)*(1-q+t)/((q-t)*(1-q-t))
    assert sp.cancel(odds(masses)-expected) == 0
    assert sp.simplify(sp.log(odds(masses)).diff(t).subs(t,0)*q*(1-q)/2) == 1
    original_odds = odds(masses)
    masses[0,1] *= h
    assert sp.cancel(odds(masses)/original_odds) == h


if __name__ == "__main__":
    eight_paths()
    bound = inversion_check()
    hidden_response_check()
    field_odds_check()
    print(f"PASS: eight paths, five preparations (inverse row sum {bound:.7f} rounded), retained memory and four-cell field source")
