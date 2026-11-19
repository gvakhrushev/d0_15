"""Positive Golden tickets reconstruct the full effect of the native blank."""
from fractions import Fraction as Q

import sympy as sp


def count_distribution(failures):
    weights = [Q(1)]
    for i in range(1, failures+1):
        updated = [Q(0)] * (len(weights)+1)
        for count, weight in enumerate(weights):
            updated[count] += weight*Q(i-1, i)
            updated[count+1] += weight/i
        weights = updated
    assert sum(weights) == 1
    return weights


def check_ticket_factors():
    z, p = sp.symbols("z p")
    # Independent 1/i marks on the real failures; the mark count is printed.
    factors = []
    for k in range(25):
        pgf = sum(sp.Rational(a.numerator,a.denominator)*z**r
                  for r,a in enumerate(count_distribution(k)))
        assert sp.expand(pgf - sp.prod(1+(z-1)/i for i in range(1,k+1))) == 0
        factors.append(pgf)
    for n in range(25):
        # Positive coefficient identity for every ordered sequence of n failures.
        # Use 1-p for the second ticket, exactly p^2 at the Golden value.
        value = sum(factors[k].subs(z,p)*factors[n-k].subs(z,1-p) for k in range(n+1))
        assert sp.Poly(value-1,p).is_zero
    y, v, u = sp.symbols("y v u", positive=True)
    # The normalized ordinary-progress comparison cancels a common per-failure
    # factor without identifying it with a Born likelihood.
    common = 1-v*(1-y)
    phi = lambda exponent: u*y*common**(-exponent)
    assert sp.simplify(phi(p)*phi(1-p)/phi(1)-u*y) == 0


def check_projectors():
    # Check the Jordan-block identity as effects, before tracing out old RIGHT.
    c1, c2 = sp.Rational(3,5), sp.Rational(5,13)
    P = sp.diag(1,0,1,0)
    def projector(c,s):
        return sp.Matrix([[c*c,c*s],[c*s,s*s]])
    A = sp.diag(projector(c1,sp.Rational(4,5)),projector(c2,sp.Rational(12,13)))
    eye = sp.eye(4)
    stack = [(P,1,0)]
    for n in range(1,7):
        op = A if n % 2 else P
        following = []
        for path, previous, hits in stack:
            for bit, project in ((1,op),(0,eye-op)):
                K = project*path
                h = hits+(bit==previous)
                effect = K.T*K
                assert effect == sp.diag(*[v for c in (c1,c2)
                                          for v in (c**(2*h)*(1-c*c)**(n-h),0)])
                following.append((K,bit,h))
        stack=following


def finite_resource_bounds():
    # The source has ||I-X||<.01 for the primary n=1 layer, ||DX||<16 for
    # the normalized A75 tangent. Y=X^j has j<=3 and ||DY||<=48.
    r, dy, cap = Q(3,100), 48, 12
    tail = r**(cap+1)/(1-r)
    gradient_tail = dy*(tail+(cap+1)*r**cap/(1-r)+r**(cap+1)/(1-r)**2)
    single_derivative = dy*(1/(1-r)+1/(1-r)**2)
    operator_error = 2*tail
    derivative_error = 2*(gradient_tail+tail*single_derivative)
    prob_min = 1-r-operator_error
    # ln(phi)>.48. Bound even the three-length log-derivative, sum |coeff|=4.
    from mpmath import iv
    assert iv.log((1+iv.sqrt(5))/2).a > .48
    price_error = 4*(derivative_error/prob_min+dy*operator_error/prob_min**2)/Q(48,100)
    assert operator_error < Q(4,10**20) and price_error < Q(1,10**13)
    # Fully bounded field-independent selectors. Fair bit from first unequal
    # pair, 32 fresh pairs per bit; up to 32 independent proposals per integer.
    # Each arm and k uses disjoint ready cells, even when the field never calls it.
    fair = 1-(1-Q(47,100))**32  # 2*p^3>.47
    assert 2*((iv.sqrt(5)-1)/2)**3 > .47
    widths = [(i-1).bit_length() for i in range(2,cap+1)]
    group = min(fair**width*Q(i,2**width) for i,width in zip(range(2,cap+1),widths))
    missed = 2*(cap-1)*(1-group)**32
    assert missed < Q(6,10**9)
    print('cap',cap, 'operator loss <',float(operator_error), 'three-length slope error <',float(price_error))
    print('maximum quantum checks',2*(cap+1),'Golden pairs for rank choices',2*32*32*sum(widths),
          'maximum mark tickets',2*cap,'probability not ready <',float(missed))


if __name__ == "__main__":
    check_ticket_factors()
    check_projectors()
    finite_resource_bounds()
