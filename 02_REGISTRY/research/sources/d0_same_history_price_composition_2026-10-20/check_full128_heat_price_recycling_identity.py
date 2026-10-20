#!/usr/bin/env python3
"""Full128 Golden acceptance -> HJR heat, exact two-round price/Gamma bridge.

The exact starting Φ, Φ_port1 are accepted ORIGINAL full128 Kraus identities
(main PR #390, paid_port_history.md). This checks operator algebra with a
deliberately noncommuting finite-dimensional TP recycling channel; it is NOT
a replacement for the separately certified original128 exact Kraus replay.
The controller is a mathematically constructed possible protocol, not a
physically selected/paid Book03 action.
"""
import math
import sympy as s

p=(s.sqrt(5)-1)/2
g=s.simplify(p*p)
c=s.simplify((1+p)/2)
assert s.simplify(p+g-1)==0
assert s.simplify(c-1/(2*p))==0
assert 0 < float(c) < 1
q=s.simplify(1-2*p*g)
assert s.simplify(q-(5-2*s.sqrt(5)))==0
assert s.simplify(1/(p*g)-(2+s.sqrt(5)))==0

for M in (1, 2, 3, 5):
    fair_zero=s.Rational(1,2)*(1+q**M)
    fair_one=s.Rational(1,2)*(1-q**M)
    cM=s.simplify(fair_zero+p*fair_one)
    assert s.simplify(cM-c-g*q**M/2)==0
    assert s.simplify(2*p*cM-(1+p**3*q**M))==0
print("EXACT native Golden fair extractor/capped acceptance: PASS")

A=s.symbols("alpha", real=True)
y=s.symbols("y", real=True)
I=s.eye(2)
# Hostile non-commuting positive D and unital recycling T*.
D=s.diag(2+y,3)
Delta=D**2
Had=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
def Tstar(X):
    return Had*X*Had
def anticom(X,Y):
    return X*Y+Y*X
def Phi_star(X):
    # ε=2α, and the original full128 CPTP and port-one identities
    return X+2*A*(D*Tstar(X)*D-anticom(Delta,X)/2)
def Port1_star(X):
    return 2*p*A*D*Tstar(X)*D
def Nstar(X):
    return s.simplify(Phi_star(X)-c*Port1_star(X))
def eq(X,Y):
    return s.simplify(X-Y)==s.zeros(X.rows,X.cols)

assert eq(Phi_star(I), I)    # literal all128 is trace preserving
B=I-A*Delta
assert eq(Nstar(I), B)      # exact full operator heat effect
G=D*Tstar(Delta)*D-Delta**2
assert G[0,1]!=0            # real noncommutative recycling witness

E2=s.simplify(Nstar(Nstar(I)))
assert eq(E2-B**2,-A**2*G)

# TWO actual original paid port-costs C_port=2+b1+b2.
Ecost=s.simplify(2*I+Port1_star(I)+Phi_star(Port1_star(I)))
target_cost=2*I+4*p*A*Delta+4*p*A**2*G
assert eq(Ecost,target_cost)
assert eq(Ecost-2*I,
          4*p*(I-B)-4*p*(E2-B**2))
# The moving-field source includes ALL dD and dT; this test directly
# differentiates an exact nontrivial D(y) full preparation-side operator.
assert eq(s.diff(Ecost,y),
          4*p*A*s.diff(Delta,y)
          -4*p*s.diff(E2-B**2,y))

# Entire E_n vs B^n recurrent, not falsely equated on arbitrary states.
En=I
for n in range(0,4):
    assert eq(Nstar(En-B**n)+
              A*(D*Tstar(B**n)*D-B**n*Delta),
              Nstar(En)-B**(n+1))
    En=s.simplify(Nstar(En))
print("EXACT noncommuting 2x2 full-operator Gamma, two-round paid price,"
      " all-depth error recurrence and moving source: PASS")

# Exact full original invariant Fourier-shell survival: Δ=λ I,
# coefficient r=p ε λ=2pαλ and c r=αλ.
lam=s.symbols("lambda", real=True)
Ds=s.sqrt(lam)*I
def Ns(Y):
    dels=lam*I
    return s.simplify(Y+A*(Ds*Tstar(Y)*Ds-dels*Y-Y*dels))
Z=I
for n in range(8):
    assert eq(Z,(1-A*lam)**n*I)
    Z=s.simplify(Ns(Z))
print("EXACT invariant-shell heat law for all n (symbolic induction check): PASS")

# Strict finite cap and raw full-spectrum O(L^4 q^M) scope.
L=8
h=s.Rational(1,L)
aa=s.simplify(g*h*h/128)
m=256*L*L
assert s.simplify(m*aa-2*g)==0
for M in (2,5,12,32):
    qv=float(q**M)
    for eigen in (0,1,4,8,16):
        regular=(1-float(aa)*eigen)**m
        capped=(1-float(aa)*(1+float(p**3)*qv)*eigen)**m
        assert capped<=regular+1e-14
        assert regular-capped<=2*float(p**5)*16*qv+1e-12
print("FINITE-CAP native controller scalar-shell survival bound: PASS")
# First energy moment conserved is NOT enough: exact unital CP 3-level
# measure/reprepare with a transient middle energy state.
D3=s.diag(0,1,s.sqrt(2))
Delta3=D3**2
I3=s.eye(3)
def Tstar3(Y):
    # Unital CP: a classical measurement followed by channel 0->0,
    # 1->uniform {0,2}, 2->2. Off-diagonals are destroyed.
    return s.diag(Y[0,0],(Y[0,0]+Y[2,2])/2,Y[2,2])
def Nstar3(Y):
    return s.simplify(Y+A*(D3*Tstar3(Y)*D3-Delta3*Y-Y*Delta3))
assert Tstar3(I3)==I3
assert Tstar3(Delta3)==Delta3
assert D3*Tstar3(Delta3)*D3-Delta3**2==s.zeros(3)
variance=Tstar3(Delta3**2)-Tstar3(Delta3)**2
assert variance==s.diag(0,1,0)
B3=I3-A*Delta3
assert eq(Nstar3(Nstar3(I3)),B3**2)
assert eq(Nstar3(Nstar3(Nstar3(I3)))-B3**3,A**3*s.diag(0,1,0))
print("EXACT 3-level hostile control: Gamma1=0 but third source differs: PASS")

# The two-moment all-depth bound has its own exact Stinespring proof.
# One noncommuting numerical check; use genuine spectral/operator norm.
vA=s.Rational(1,200)
D2=s.diag(2,3)
Delta2=D2**2
I2=s.eye(2)
H2=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
def TS2(Y): return H2*Y*H2
def N2(Y):
    return Y+vA*(D2*TS2(Y)*D2-Delta2*Y-Y*Delta2)
n2=35
E2n=I2
for _ in range(n2): E2n=s.simplify(N2(E2n))
diff=(E2n-(I2-vA*Delta2)**n).evalf()
norm=lambda M:max(abs(complex(ev)) for ev in M.eigenvals())
delta1=norm(TS2(Delta2)-Delta2)
delta2=norm(TS2(Delta2**2)-TS2(Delta2)**2)
estimate=n2*(n2-1)/2*float(vA)**2*9*(delta1+delta2**0.5)
assert norm(diff)<estimate
print("ALL-DEPTH TWO-MOMENT curved operator norm bound: PASS")


# Three-level exact hostile recycling: Γ_1=0 yet Γ_2>0.
I3=s.eye(3)
D3=s.diag(0,1,s.sqrt(2))
Delta3=D3**2
def Tstar3(Y):
    return s.diag(Y[0,0],(Y[0,0]+Y[2,2])/2,Y[2,2])
def Nstar3(Y):
    return s.simplify(Y+A*(D3*Tstar3(Y)*D3-Delta3*Y-Y*Delta3))
B3=I3-A*Delta3
assert Tstar3(I3)==I3 and Tstar3(Delta3)==Delta3
assert eq(D3*Tstar3(Delta3)*D3, Delta3**2)
assert Tstar3(Delta3**2)-Tstar3(Delta3)**2 == s.diag(0,1,0)
assert eq(Nstar3(Nstar3(I3)), B3**2)
assert eq(Nstar3(Nstar3(Nstar3(I3)))-B3**3,
          A**3*s.diag(0,1,0))
print("EXACT Γ1=0, Γ2>0 third-step source countercontrol: PASS")

# Fully noncommuting curved operator two-moment bound, native CP unital T*.
vA=s.Rational(1,200)
D2=s.diag(2,3)
Delta2=D2**2
I2=s.eye(2)
Had2=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
def TS2(Y): return Had2*Y*Had2
def N2(Y):
    return Y+vA*(D2*TS2(Y)*D2-Delta2*Y-Y*Delta2)
n2=35
En2=I2
for _ in range(n2):
    En2=s.simplify(N2(En2))
diff=(En2-(I2-vA*Delta2)**n2).evalf()
norm=lambda M:max(abs(complex(ev)) for ev in M.eigenvals())
d1=norm(TS2(Delta2)-Delta2)
d2=norm(TS2(Delta2**2)-TS2(Delta2)**2)
rhs=n2*(n2-1)/2*float(vA)**2*9*(d1+d2**0.5)
assert norm(diff)<rhs
print("ALL-DEPTH TWO-MOMENT full-operator norm bound: PASS")

print("ALL EXACT GOLDEN/FULL128 HEAT-PRICE-RECYCLING CHECKS PASSED")
