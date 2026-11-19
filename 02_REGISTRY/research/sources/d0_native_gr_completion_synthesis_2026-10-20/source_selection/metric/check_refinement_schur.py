"""Exact algebraic controls; no native physical map is assumed."""
import sympy as s

def schur(H, kept):
    n=H.rows
    eliminated=[i for i in range(n) if i not in kept]
    A=H.extract(kept,kept)
    if not eliminated:
        return A
    B=H.extract(kept,eliminated)
    C=H.extract(eliminated,eliminated)
    return s.simplify(A-B*C.inv()*B.T)

# All variables (coarse boundary x2, old interior y2, new interior z2).
T=s.Matrix([[1,0,2,0,0,1],
            [0,1,0,1,1,0],
            [0,0,1,0,2,1],
            [0,0,0,1,0,1],
            [0,0,0,0,1,0],
            [0,0,0,0,0,1]])
D=s.diag(2,3,-5,7,11,13)
H=T.T*D*T
# Saddle allowed; elimination is actual stationary Schur.
assert schur(schur(H,[0,1,2,3]),[0,1])==schur(H,[0,1])

# Fine source boundary2, interior2; coarse boundary1.
Kf=s.Matrix([[3,1],[1,4]])
A=s.Matrix([[2,1],[1,3]])
Q=s.Matrix([[1,2],[0,1]])
Hf=(Kf+Q*A.inv()*Q.T).row_join(Q).col_join(Q.T.row_join(A))
assert schur(Hf,[0,1])==Kf
B=s.Matrix([[2],[3]])
Lift=s.diag(B,s.eye(2))
assert schur(Lift.T*Hf*Lift,[0])==B.T*Kf*B
assert B.T*Kf*B==s.Matrix([[60]])
assert Kf[0,0]!=60

# Two half-weight parallel boundary slots reproduce one coarse form.
assert s.Matrix([[1,1]])*s.diag(s.Rational(1,2),s.Rational(1,2))*s.Matrix([[1],[1]])==s.Matrix([[1]])

# Nonlinear boundary readout needs the traction term away from stationarity.
x=s.symbols('x')
b=x+x*x
W=s.Rational(3,2)*b*b+5*b
assert s.diff(W,x,2).subs(x,0)==13
assert 3+5*s.diff(b,x,2).subs(x,0)==13
assert s.diff(W,x,2).subs(x,0)!=3

# Both midpoint records approximate the same target but are not restrictions.
h=s.symbols('h',positive=True)
coarse=h*(h/2)**2
fine=(h/2)*((h/4)**2+(3*h/4)**2)
assert s.simplify(coarse-h**3/4)==0
assert s.simplify(fine-5*h**3/16)==0
assert s.simplify(fine-coarse)==h**3/16

print('PASS exact stationary Schur associativity including saddle internal blocks')
print('PASS boundary pullback congruence and noninvariance-of-matrix hostile control')
print('PASS nonlinear boundary map traction term cannot be dropped away from stationarity')
print('PASS midpoint common-target recovery differs from literal finite-level restriction')
print('Scope: algebraic transport criterion, not construction of actual native HJR refinement')
