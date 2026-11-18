"""Exact checks for the trace-line test using the published single-J2 symbol."""
from math import comb, factorial

import sympy as sp


def trace_and_mean():
    s, x = sp.symbols("s x")
    a = sp.Function("A")(s, x)
    f = s * a
    dilate = lambda v: s * sp.diff(v, s) + x * sp.diff(v, x)
    assert sp.simplify(2*f - dilate(f) - s*(a-dilate(a))) == 0
    # After the pointwise trace is imposed, global consistency of the mean
    # amounts to Gamma * average[(A + DA)/(A - DA)] = 0.
    assert sp.simplify(2*a/(a-dilate(a))-1-(a+dilate(a))/(a-dilate(a))) == 0


def owned_price_degree():
    # Polynomial arithmetic in X. Coefficients are exact rational functions
    # of field-independent parameters. p^2+p=1 is not needed for degree 10.
    x, p, z, t, k, offset = sp.symbols("x p z T k offset")
    poly = lambda expr: sp.Poly(expr, x)
    for orientation in (-1, 1):
        energy = poly(p**2*(1 + t*(offset-k*x)))
        born = poly(p+orientation*p**2*t*x)**2
        radial = 4*energy*(1-energy)
        report = 4*born*(1-born)
        q = 1-z*report
        ret = 1-z*(radial + (1-radial)*report)
        assert (report.degree(), radial.degree(), q.degree(), ret.degree()) == (4,2,4,6)
        assert sp.expand(q.LC()*ret.LC()-64*z**2*p**20*t**10*k**2) == 0
    # Directly check the eleventh-value obstruction on an exact Golden
    # instance as well as the identity for every lower monomial.
    assert sum(comb(10,j) for j in range(0,11,2)) == 512
    for n in range(11):
        diff = sum((-1)**j*comb(10,j)*j**n for j in range(11))
        assert diff == (factorial(10) if n == 10 else 0)
    field = sp.QQ.algebraic_field(sp.sqrt(5))
    pp = field.from_sympy((sp.sqrt(5)-1)/2)
    zz, step = field.convert(sp.Rational(1,2**20)), field.convert(sp.Rational(1,1024))
    kk = field.convert(2)
    def denominator(value):
        energy = pp**2*(1-kk*value)
        born = (pp+pp**2*value)**2
        radial, report = 4*energy*(1-energy), 4*born*(1-born)
        return (1-zz*report)*(1-zz*(radial+(1-radial)*report))
    delta = sum((-1)**j*comb(10,j)*denominator(step*j) for j in range(11))
    assert delta == factorial(10)*64*zz**2*pp**20*kk**2*step**10
    assert delta != field.zero


def scalar_solution():
    # Compute Ricci from the metric, then check the wave operator via its
    # actual density. Coordinate 0 may be the timelike or spacelike normal.
    u = sp.symbols("u", positive=True)
    exponents = [sp.Rational(1,2), sp.Rational(1,3), sp.Rational(1,6)]
    strength = 1-sum(n**2 for n in exponents)
    assert sum(exponents)==1 and strength==sp.Rational(11,18)
    deriv = lambda expr, j: sp.diff(expr,u) if j==0 else 0
    for signs in ((1,-1,-1,-1),(-1,1,-1,-1)):
        g = sp.diag(signs[0], *(signs[i+1]*u**(2*n) for i,n in enumerate(exponents)))
        gi = g.inv()
        conn = [[[sum(gi[i,m]*(deriv(g[m,k],j)+deriv(g[m,j],k)-deriv(g[j,k],m))
                      for m in range(4))/2 for k in range(4)] for j in range(4)] for i in range(4)]
        ric = sp.Matrix(4,4,lambda i,j: sp.simplify(sum(
            deriv(conn[k][i][j],k)-deriv(conn[k][k][i],j)
            +sum(conn[k][k][m]*conn[m][i][j]-conn[k][j][m]*conn[m][k][i]
                 for m in range(4)) for k in range(4))))
        assert ric==sp.diag(strength/u**2,0,0,0)
        assert sp.simplify(sp.sqrt(-g.det())-u)==0
        assert sp.diff(u*gi[0,0]*sp.diff(sp.log(u),u),u)==0
        assert (gi*ric).trace()==signs[0]*strength/u**2
        assert sp.Rational(3,5)**2+sp.Rational(4,5)**2==1


def two_matter_modes():
    from itertools import combinations_with_replacement
    def quadratic_row(v):
        return [v[i]*v[j]*(1 if i==j else 2)
                for i,j in combinations_with_replacement(range(len(v)),2)]
    three, four = sp.Rational(3,5), sp.Rational(4,5)
    probes = [(1,1,0,0),(1,-1,0,0),(1,0,1,0),(1,0,-1,0),
              (1,0,0,1),(1,0,0,-1),(1,three,four,0),
              (1,three,0,four),(1,0,three,four)]
    null_tests = sp.Matrix([quadratic_row(v) for v in probes])
    metric = sp.Matrix([1,0,0,0,-1,0,0,-1,0,-1])
    assert null_tests.rank()==9 and null_tests*metric==sp.zeros(9,1)
    def rows(u):
        u1,u2 = u
        return [quadratic_row([2*u1*a1,u1*a2+u2*a1,2*u2*a2])
                for a1,a2 in [(1,0),(0,1),(1,1)]]
    first_two = rows((1,0))+rows((0,1))
    assert sp.Matrix(first_two).rank()==5
    assert sp.Matrix(first_two+rows((1,1))).rank()==6
    # One choice of two independent gradients, including projected zeros.
    tests = [row for v in probes for row in rows((v[1],v[2]))]
    assert sp.Matrix(tests).rank()==6
    # A rank-one family cannot establish the theorem for general gradients.
    assert sp.Matrix([row for v in probes for row in rows((v[0],2*v[0]))]).rank()==3


if __name__ == "__main__":
    trace_and_mean()
    owned_price_degree()
    scalar_solution()
    two_matter_modes()
    print("PASS: trace/mean, J2 polynomial, exact differences, two Einstein witnesses, null tomography and polarization ranks")
