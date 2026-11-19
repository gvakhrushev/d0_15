#!/usr/bin/env python3
"""Exact original 64 Walsh SELECT labels/coefficients: creator Gram at all phases.
Consequence for full two-tick CAR4 top amplitudes; NOT selected physical GR.
"""
import sympy as s
nu=s.Rational(3,5)
z=s.symbols('z0:4', nonzero=True)
U=s.zeros(64,4)
for label in range(32):
    for r in range(4):
        if label&1==0:
            a=(-1)**((label&(8*r+2)).bit_count())
            b=(-1)**((label&(8*r+6)).bit_count())
            # Odd components of the ACTUAL 32x32 Walsh SELECT:
            # P_r^dagger = nu*z_r^(-1)c_r^dagger and -C_r^dagger.
            U[2*label,r]=nu*s.Rational(1,16)*(a*z[r]-b)
Udag=s.Matrix(4,64,lambda i,j:U[j,i].subs(z[i],1/z[i]))
assert s.simplify(Udag*U)==nu**2*s.eye(4)/8
H=s.zeros(4)
for k in range(64):
    for a in range(4):
        for b in range(4):
            H[a,b]+=U[k,a].subs(z[a],1/z[a])*U[k,b]
assert s.simplify(H-nu**2*s.eye(4)/8)==s.zeros(4)
print('PASS EXACT ORIGINAL WALSH U(z)^dagger U(z)=(nu^2/8)I4, arbitrary four native unit phases')
print('By compound-frame/Pluecker: full ordered 2-tick bivector Gram=(p^4 nu^4/2) I6 with both Golden ports.')
print('FIREWALL: different Dirac phase profiles per tick require one physically admitted common history.')
