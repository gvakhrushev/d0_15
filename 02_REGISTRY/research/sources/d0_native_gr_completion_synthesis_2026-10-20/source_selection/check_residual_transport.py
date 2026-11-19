"""Exact source-accounting controls; no unknown native R is assigned here."""
import sympy as s

y = s.symbols("y", real=True)
p = (s.sqrt(5)-1)/2
I = s.eye(2)
rho = s.Matrix([[s.Rational(1,2)+y/10, y/20],
                [y/20, s.Rational(1,2)-y/10]])
# The already owned scalar mark effect, on its supplied compression chart.
q = 2*p**3*(1-y)
E = q*I
sc, delta, W = 1+y*y, 2+y, y**3
R = s.Matrix([[y, y*y], [y*y, -y/3]])
G = sc*I+delta*E+R
S = s.trace(rho*G)+W
a, b = y+y*y, y*y+y**3
Rp = R-a*I-b*E
Gp = (sc+a)*I+(delta+b)*E+Rp
assert s.simplify(Gp-G) == s.zeros(2)
def split_source(c, d, r):
    return (s.diff(c,y)+s.diff(d,y)*q+d*s.diff(q,y)
            +s.trace(rho*r.diff(y))+s.trace(rho.diff(y)*r)+s.diff(W,y))
assert s.simplify(split_source(sc,delta,R)-s.diff(S,y)) == 0
assert s.simplify(split_source(sc+a,delta+b,Rp)-s.diff(S,y)) == 0
assert s.simplify(s.trace(rho*Rp).diff(y)-s.trace(rho*R).diff(y)) != 0

# A genuine conditional averaging projection with the original Golden pair.
# This is a linear-algebra control, not an invented native history partition.
M = s.diag(s.Matrix([[p,p*p],[p,p*p]]),s.Matrix([[p,p*p],[p,p*p]]))
assert s.simplify(M*M-M) == s.zeros(4)
c = s.Matrix([y,y,2*y,2*y])
k = s.Matrix([p*p,-p,0,0])
assert s.simplify(M*c-c) == s.zeros(4,1)
assert s.simplify(M*k) == s.zeros(4,1)
assert s.simplify(M*(c+y*k)-c) == s.zeros(4,1)
assert (c+y*k).diff(y) != c.diff(y)

# Moving weights have a source even when every leaf value is constant.
w = s.Matrix([s.Rational(1,2)+y,s.Rational(1,2)-y])
r = s.Matrix([1,-1])
assert r.diff(y) == s.zeros(2,1)
assert s.diff(w.dot(r),y) == 2
assert s.diff(w.dot(r),y).subs(y,0) != 0
assert w.dot(r).subs(y,0) == 0

# An invertible observation chart transports, rather than erases, a covector.
J = s.Matrix([[2,1],[1,1]])
v = s.Matrix([1,3])
assert J.det() != 0 and J.T.inv()*v != s.zeros(2,1)
assert J.T*(J.T.inv()*v) == v

# At a matching normalized distribution, relative entropy has zero first jet.
x = s.symbols("x", real=True)
D = (s.Rational(1,2)+x)*s.log(1+2*x)+(s.Rational(1,2)-x)*s.log(1-2*x)
assert D.subs(x,0) == 0 and s.diff(D,x).subs(x,0) == 0
assert s.diff(D,x,2).subs(x,0) == 4
# A signed relative price cocycle can instead have a nonzero diagonal jet.
C = x
assert C.subs(x,0) == 0 and s.diff(C,x).subs(x,0) == 1

# "Minimum discrepancy among all irrationals at every N" is already false at N=1.
# For the sequence {n alpha}, n=1,...,N, D*_1(alpha)=max(alpha,1-alpha).
alpha = s.Rational(1,2)+s.sqrt(2)/100
assert alpha > s.Rational(1,2) and alpha < p
print("PASS exact full residual differential under moving split and preparation")
print("PASS Golden conditional-projection kernel and moving-weight source controls")
print("PASS invertible covector transport and normalized relative-entropy first jet")
print("PASS finite discrepancy counterexample; no physical R, price, or Beatty map fitted")
