"""Finite exact witnesses for the measured 20-stage Q8 reset and common readout."""
from itertools import product
from pathlib import Path
import re

import sympy as sp


root = Path(__file__).resolve().parents[7]
q8 = (root/"03_FORMALIZATION/D0/Claims/Q8DedekindMinimality.lean").read_text()
part = q8.split("def Q8 :", 1)[1].split("e :=", 1)[0]
table = [list(map(int, s.split(","))) for s in re.findall(r"!\[([\d, ]+)\]", part)]
assert len(table) == 8 and all(len(r)==8 for r in table)
reg = [sp.Matrix(8,8,lambda i,j:int(table[g][j]==i)) for g in range(8)]
ident = reg[0]
(z,) = (r for r in reg[1:] if r**2==ident)
assert ident == sp.eye(8) and z**2 == ident and z == z.T
assert all(z*r == r*z for r in reg)
ep, em = (ident+z)/2, (ident-z)/2
p = (sp.sqrt(5)-1)/2
a = sp.sqrt(p)
eq = lambda x: sp.simplify(x) == 0
assert eq(p+p**2-1)
assert eq(1-2*p**2-p**3)


def mass(k, rho, h):
    return sp.expand(sp.trace(h*k*rho*k.T))


# Reading f,c after the final CX uniquely identifies a true/wrong reset.
# The uncloned state is rho. The actual sqrt(p),p flag coefficients are explicit.
A,B,C = sp.symbols("A B C", positive=True)
forms = {(f, f ^ error): (a if f==0 else p)*(C*ident if not error else A*ident+B*z)
         for f,error in product(range(2), repeat=2)}
assert all(sp.simplify(forms[f,f] - (a if f==0 else p)*C*ident)==sp.zeros(8)
           for f in range(2))
for v,u in ((sp.eye(8)[:,0],sp.Rational(1,2)),
            ((ident[:,0]-z[:,0])/sp.sqrt(2),0),
            (sp.ones(8,1)/sp.sqrt(8),1)):
    rho = v*v.T
    total_bad = sum(mass(forms[f,1-f],rho,ident) for f in range(2))
    total_good = sum(mass(forms[f,f],rho,ident) for f in range(2))
    assert eq(total_bad - ((A-B)**2+4*A*B*u))
    assert eq(total_good-C*C)
    mr = sp.simplify(total_bad.subs({A:a*p,B:a*p}))
    assert eq(mr-4*p**3*u)

# Complete trace at a faithful fixed input vs common but singular readout.
v = sp.eye(8)[:,0]
h = v-2*z*v
rho, effect = v*v.T, h*h.T/5
assert effect*z != z*effect
assert mass(2*ident+z,rho,effect) == 0
assert sp.trace(rho*ep)==sp.Rational(1,2)
t,b,r,base=sp.symbols("t b r base",positive=True)
w = mass(t*ident+b*z,rho,effect)
assert eq(w/mass(ident,rho,effect)-(t-2*b)**2)
assert eq((mass(r*ident,rho,effect)+w)/mass(base*ident,rho,effect)
          -(r*r+(t-2*b)**2)/base**2)

# A general nonnegative context-dependent kernel can attain the factor four.
omega = sp.ones(8,1)/sp.sqrt(8)
odd = (v - z*v)/sp.sqrt(2)
read = v*v.T
assert eq((read*odd).norm()**2 - 4*(read*omega).norm()**2)
for left,right in product(reg,repeat=2):
    k = 3*left+2*right
    assert k*omega==5*omega
    assert (k*odd).norm()**2 <= 25

print("PASS: measured flag truth on three Q8 sectors, common singular readout, unequal effective reset costs, complete-trace bounds")
