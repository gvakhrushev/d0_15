"""Exact Golden identities for the compiler corollary; no physical task selected."""
import sympy as s

p=(s.sqrt(5)-1)/2
phi=(1+s.sqrt(5))/2
L=s.symbols("L",real=True)  # L=log_phi(4); order bounds proved in the note.
q1=p**2
q2=4*p**3
A=4+L
D2=q2*A-5

def equal(x,y):
    assert s.simplify(s.expand(x-y))==0

equal(p+p**2,1)
equal(p**6+q2,1)
equal(phi**11,89*phi+55)
equal(phi**8,21*phi+13)
equal(phi**3,2*phi+1)
equal(2+D2-6*(q2-q1),q2*(L-s.Rational(11,4)))
equal(2*3+D2-1,A*q2)
equal((1+D2)-4*(q2-q1),4*p*(p**2*L-1))
equal(5*(q2-q1)-(1+D2),4-5*p**2+q2*(1-L))
equal(4-5*p**2-2*q2,7-11*p)

# Exact real algebraic inequalities. The logarithm inequalities follow
# monotonically from these powers; no rounded logarithm acceptance.
assert s.simplify(phi-1)>0
assert s.simplify(2-phi)>0
assert 89*2+55==233
assert 233<4**4
assert s.simplify(phi**3-4)>0
assert s.simplify(4-phi**2)>0
assert s.simplify(64-phi**8)>0
assert s.simplify(p**2-s.Rational(3,8))>0
assert s.simplify(7-11*p)>0
assert s.simplify(q2-q1)>0
assert s.simplify(1-q2)>0

# Exact integer exclusion used after 6<delta<7.
assert [n for n in range(0,8) if 6<n<7]==[]
# Exact opportunities after 4<delta_star<5 and 6<A<7.
assert [n for n in range(0,8) if 4<n<7]==[5,6]

print("PASS exact compiler-threshold Golden identities")
print("PASS exact power inequalities imply log_phi(4)>11/4 and 6<A<7")
print("PASS integer compiler ell_G>=2 has no positive-source integer opportunity")
print("Scope: conditional fixed-prefix G^k family; actual unit-G compiler and task admission remain premises")
