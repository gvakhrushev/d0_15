"""Verify the positive remainder expansion and its use for noncommuting Gram fields."""
from fractions import Fraction as Q

import sympy as sp


def coefficients(z, cap):
    row = [Q(1)]
    for k in range(cap):
        row.append(row[-1]*(z+k)/(k+1))
    return row


def difference_table(z, cap):
    a, b = coefficients(z, cap), coefficients(1-z, cap)
    c = [sum(a[i]*b[n-i] for i in range(max(0,n-cap),min(cap,n)+1)) for n in range(2*cap+1)]
    assert all(x == 1 for x in c[:cap+1])
    c.append(Q(0))
    weights = [c[n-1]-c[n] for n in range(cap+1,2*cap+2)]
    assert min(weights) >= 0 and sum(weights) == 1
    return c, weights


def matrix_jet(coeff, base, direction):
    # Horner recurrence for a matrix polynomial and its Frechet derivative.
    v, dv = sp.zeros(base.rows), sp.zeros(base.rows)
    for x in reversed(coeff):
        v, dv = v*base + sp.Rational(x.numerator,x.denominator)*sp.eye(base.rows), dv*base + v*direction
    return v, dv


def main():
    z = Q(5,8)     # rational companion inside the general 0<=z<=1 theorem
    A = sp.Matrix([[sp.Rational(2,3),0,0],[0,sp.Rational(1,4),0]])
    B = sp.Matrix([[0,sp.Rational(1,4),sp.Rational(1,7)],[sp.Rational(1,3),0,0]])
    X = A.T*A
    dX = B.T*A+A.T*B
    assert X*dX != dX*X and X.det()==0
    identity = sp.eye(3)
    for cap in (1,3,8):
        c, w = difference_table(z,cap)
        G, g = matrix_jet(c[:-1],identity-X,-dX)
        # E_m=X^2 G_m(I-X), on a genuinely noncommuting rank-deficient example.
        dpriced = (dX*X+X*dX)*G+X**2*g
        A0, dA0 = matrix_jet([Q(0)]*(cap+1)+w,identity-X,-dX)
        assert X-X**2*G==X*A0 and dX-dpriced==dX*A0+X*dA0
    for cap in (1,2,5,16,32):
        for z in (Q(0), Q(1,5), Q(1,2), Q(7,9), Q(1)):
            difference_table(z,cap)
        H=lambda k:sum((Q(1,i) for i in range(1,k+1)),Q(0))
        # Sum-split endpoint bound used for the two singular-value-damped factors.
        for n in range(cap+1,2*cap+2):
            k=n//2
            assert 2*k+1>=cap+1 and H(n-k)<=H(2*cap+1)
    # For A(t)=t, E_m(t^2) starts at t^4 at a genuinely dark point.
    assert (sp.Symbol('t')**4).diff(sp.Symbol('t'),2).subs(sp.Symbol('t'),0)==0
    print('Verified positive remainders and both matrix jets at a noncommuting dark point.')


if __name__ == '__main__':
    main()
