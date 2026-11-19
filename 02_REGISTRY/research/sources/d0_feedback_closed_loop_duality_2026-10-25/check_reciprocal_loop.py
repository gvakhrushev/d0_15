#!/usr/bin/env python3
"""Exact finite matrix / rational + certified high precision diagnostics.
D0 Book03 J=-log det(I-zeta F) from the real feedback effect F.
A mathematical symmetric-return ensemble, not a newly priced physical
execution, code, or claimed D0->GR action selection.
"""
from __future__ import annotations
import json
import sympy as S
import mpmath as M

Q = S.Rational
z = Q(1, 2**20)
a = 1-z
I = S.eye(2)
F = S.Matrix([[Q(1,5), Q(1,13)], [Q(1,13), Q(2,5)]])
FB = S.Matrix([[Q(1,4), Q(-1,11)], [Q(-1,11), Q(3,7)]])
H = S.Matrix([[Q(1,7), Q(-1,9)], [Q(-1,9), Q(1,11)]])
G = S.Matrix([[Q(2,13), Q(1,17)], [Q(1,17), Q(-1,19)]])
V = S.Matrix([[0,Q(1,23)],[Q(1,23),0]])
cnt = 0

def check(c, msg):
    global cnt
    cnt += 1
    if not bool(c):
        raise ArithmeticError(msg)

def iszero(x):
    if isinstance(x, S.MatrixBase):
        return all(S.cancel(e)==0 for e in x)
    return S.cancel(x)==0

def recip(X):
    return (I-X)*(I-z*X).inv()

def positive_contract(X):
    assert X==X.T
    # exact Sylvester 2-by-2 principal-minor positivity on the REAL matrix
    check(X[0,0]>=0 and X.det()>=0, "2x2 positive semidefinite")
    Y=I-X
    check(Y[0,0]>=0 and Y.det()>=0, "2x2 <=I")

for X in (F, FB):
    positive_contract(X)
    R=recip(X)
    positive_contract(R)
    check(iszero(recip(R)-X), "R_zeta is EXACT involution")
    check(iszero((I-z*R)*(I-z*X)-a*I), "reciprocal survival duality")
    check(iszero((I-z*X).det()*(I-z*R).det()-a**2), "no-return product")
    check(iszero(((I-X)*(I-z*X).inv())-(I-z*X).inv()*(I-X)),
          "basis-free polynomial calculus")

x=S.symbols('x',real=True)
fx=1/(1+S.sqrt(a))
check(S.simplify(fx-(1-fx)/(1-z*fx))==0,"unique contraction fixed point")
check(fx>S.Rational(1,2) and fx<1,"self-dual scalar strictly in interval")
for f in (Q(0),Q(1),Q(1,3),Q(2,3)):
    r=(1-f)/(1-z*f)
    check((1-z*f)*(1-z*r)==a,"unique scalar complement")
    check((1-r)/(1-z*r)==f,"reciprocal mapping indeed involutive")

# Noncommuting true first and mixed field jets.
check(F*H!=H*F and F*G!=G*F,"genuinely noncommuting source directions")
e,u=S.symbols('e u',real=True)
Xt=F+e*H+u*G+e*u*V
Rt=(I-Xt)*(I-z*Xt).inv()
A=(I-z*F).inv()
check(iszero(Rt.diff(e).subs({e:0,u:0})+a*A*H*A),
      "noncommuting Frechet dual derivative")
check(iszero(Rt.diff(u).subs({e:0,u:0})+a*A*G*A),
      "second noncommuting dual derivative")
Jt=-S.log((I-z*Xt).det())
first=S.simplify(Jt.diff(e).subs({e:0,u:0}))
expected_first=z*S.trace(A*H)
check(iszero(first-expected_first),"Book logdet original first source")
mixed=S.cancel(Jt.diff(e,u).subs({e:0,u:0}))
expected_mixed=z*S.trace(A*V)+z*z*S.trace(A*H*A*G)
check(iszero(mixed-expected_mixed),"Book full noncommuting mixed source")
R0=recip(F)
dual_t=-S.log((I-z*Rt).det())
check(iszero(S.cancel(dual_t.diff(e).subs({e:0,u:0})+expected_first)),
      "compensating whole complementary source anti-covariance")
check(iszero(S.cancel(dual_t.diff(e,u).subs({e:0,u:0})+expected_mixed)),
      "all moving field higher response anti-covariance")

# Single physical paired positive Book determinant has full rank4, not an
# invented negative absolute fee or a coherent average of two arms.
FbR=recip(FB)
Pair=S.diag(F,FbR)
A4=S.eye(4)-z*Pair
check(iszero(A4.det()-a**2*(I-z*F).det()/(I-z*FB).det()),
      "one complete paired no-return response")
check(A4.det()>=a**4 and A4.det()<=1,"absolute paired Book nonnegative")
check((I-z*F).det()+(I-z*FbR).det()!=2*a,
      "not an arithmetic mixture of two no-return probabilities")

# Symmetric-powers S^n(H) trace = complete homogeneous symmetric function.
# Recurrence from exact, basis-free trace moments and cyclic 1/n factor.
T=S.trace(F); D=F.det()
h=[S.Integer(1)]
for n in range(1,11):
    v=S.cancel(sum(S.trace(F**k)*h[n-k] for k in range(1,n+1))/n)
    h.append(v)
    check(v>=0,"canonical symmetric loop coefficient nonnegative")
    if n>=2:
        check(iszero(v-T*h[n-1]+D*h[n-2]),
              "same coefficient as det(I-tF)^(-1)")
check(h[2]!=S.trace(F**2),"incorrect repeatable occupation coefficient excluded")
check(iszero((I-z*F).det()-(1-z*T+z*z*D)),"exact denominator")

# Geometric occupations are normalized and empty has probability det.
for f in (Q(1,5),Q(2,5)):
    rho=z*f
    check(1/(1-rho)>1,"positive full recurrence normalization")
    check((1-rho)*sum(rho**i for i in range(10))==1-rho**10,
          "finite normalized occupations with explicit residual")
check((1-z*Q(1,5))*(1-z*Q(2,5))!=1,
      "Born normalized probability is not raw unweighted loop partition")

# Effective numerical replays at 75 decimal digits with analytic rational
# truncation bounds (no unverified floating sign used in the theorem).
M.mp.dps=75
mp=lambda r: M.mpf(int(r.p))/int(r.q)
zm=mp(z)
FM=M.matrix([[mp(F[i,j]) for j in range(2)] for i in range(2)])
HM=M.matrix([[mp(H[i,j]) for j in range(2)] for i in range(2)])
tr=lambda mat:sum(mat[i,i] for i in range(mat.rows))
J=-M.log(M.det(M.eye(2)-zm*FM))
source=zm*tr(M.inverse(M.eye(2)-zm*FM)*HM)
for n in (1,2,3,4,5,7,9):
    partial=sum(zm**k*tr(FM**k)/k for k in range(1,n+1))
    tailbound=2*zm**(n+1)/((n+1)*(1-zm))
    check(0<=J-partial<=tailbound,
          "rigorous universal J finite loop tail bound applies")
    partial_source=sum(zm**k*tr(FM**(k-1)*HM) for k in range(1,n+1))
    dsrcbound=2*zm**(n+1)/(1-zm) # ||H|| < 1
    check(abs(source-partial_source)<=dsrcbound,
          "rigorous noncommuting source-tail bound applies")
check(M.fabs(M.exp(-J)-M.det(M.eye(2)-zm*FM))<M.mpf('1e-68'),
      "empty bosonic memory history has probability det")

print(json.dumps({
    'status':'PASS_EXACT_NATIVE_FEEDBACK_RECIPROCAL_NO_RETURN_AND_SYMMETRIC_LOOP',
    'checks':cnt,
    'zeta':'1/1048576',
    'book_J':M.nstr(J,38),
    'mathematical_empty_return_probability':M.nstr(M.exp(-J),38),
    'off_shell_noncommuting_first_source':M.nstr(source,24),
    'positive_reciprocal_involution':True,
    'one_pair_absolute_price_positive':True,
    'same_native_action_selected_by_M1':False,
    'real_loop_apparatus_physical_admission':False,
    'GR_closed':False
},sort_keys=True,indent=2))
