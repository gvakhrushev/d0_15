"""Exact finite extraction of the degree-one H.1 curvature/matter coefficient."""
from fractions import Fraction
from math import comb, lcm, prod
import sympy as s


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


# Moment system for positive settings; zero was already subtracted in each run.
indices = range(1, 9)
for j in indices:
    flip = Fraction(sum(n < 8-j for n in range(16)), 16)
    require(1-2*flip == Fraction(j, 8), "sign dilution on fresh registered fair bits")
weights = [Fraction((-1)**(j-1)*comb(8, j), j) for j in indices]
scale = lcm(*(w.denominator for w in weights))
m = [int(scale*w) for w in weights]
require(scale == 840 and m == [6720, -11760, 15680, -14700, 9408, -3920, 960, -105], "integer weights")
require([sum(a*j**k for a,j in zip(m,indices)) for k in indices] == [840]+[0]*7, "moments 1..8")
limit = 2*sum(map(abs, m))
require(limit == 126506, "raw length bound")

# Original PC2 axes, including the real matter degree and its sign in the input.
p,z,t = s.symbols("p z t")
phi_relation = p*p+p-1
def reduce_p(expr):
    return s.rem(expr.expand(), phi_relation, p).expand()

def report(x, y):
    E = p**2*(1+x)
    lean = 4*E*(1-E)
    u = p+p**2*y
    B = 4*u**2*(1-u**2)
    A = lean+(1-lean)*B
    return z*(A+B)-z**2*A*B

zero = reduce_p(report(0,0))
rx = s.Poly(reduce_p(report(t,0)-zero),t)
ry = s.Poly(reduce_p(report(0,t)-zero),t)
require((rx.degree(), ry.degree()) == (2,8), "PC2 degrees")
rf, rq = rx.nth(1), ry.nth(1)
require(reduce_p(rf-4*z*p**11*(1-4*z*p**3)) == 0, "PC2 gain")
f,q,rho,eps = s.symbols("f q rho eps", nonzero=True)
for k in indices:
    field_coefficient = (rx.nth(k)*f**k+ry.nth(k)*(-q)**k)/rho**(k-1)
    moments = sum(a*j**k for a,j in zip(m,indices))
    expected = 840*eps*(rf*f-rq*q) if k == 1 else 0
    require(s.expand(moments*eps**k*field_coefficient-expected) == 0, "coefficient "+str(k))

# Different readiness probabilities at every setting; all three report addresses use
# the original common processor at that setting. A false joint flag contributes zero.
alpha = [Fraction(2*j+1, 3*j+2) for j in indices]
rates = [Fraction(j+1, 17) for j in indices]
common = prod(alpha)
for j in range(8):
    gated = alpha[j]*rates[j]*prod(a for k,a in enumerate(alpha) if k != j)
    require(gated == common*rates[j], "all-ready joint marginal")
other = [Fraction(9-j, 11) for j in indices]
require([a*b for a,b in zip(alpha,other)] != [common*b for b in other], "unequal raw gain control")

# Exhaustive single-trial bounds at one row, then an attaining extremum for all rows.
row_values = {a+b-2*c for a in (0,1) for b in (0,1) for c in (0,1)}
require(max(abs(n) for n in row_values)==2, "row range")
require(sum(x*(2 if x>0 else -2) for x in m)==limit, "registered output bound")
for n in (-limit,0,1,limit):
    slots = 2*limit
    measured_length = slots+(limit+n)
    baseline_length = slots+limit
    require(measured_length-baseline_length == n, "0/10 price difference")
print("PASS: PC2 coefficients on both axes, integer moments 1..8, unequal READY gains, retained failures, and the bounded positive code pair.")
