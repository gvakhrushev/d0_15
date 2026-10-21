#!/usr/bin/env python3
"""Exact original Golden nonblank pair: branch information fibre invisible in its mean."""
import sympy as s

def require(condition, message):
    if not bool(condition): raise ArithmeticError(message)
p=s.Symbol('p', positive=True)
# polynomial arithmetic in p^2+p-1
def red(x): return s.factor(s.Poly(s.expand(x),p).rem(s.Poly(p*p+p-1,p)).as_expr())
q0=p*p;q1=p
require(red(q0+q1)==1, "exact Golden identity 11")
h=red(2*q0+q1)
I0=red(h-s.Rational(3,2)*p); I1=I0+s.Rational(3,2)
require(red(q0*I0+q1*I1-h)==0, "exact Golden identity 14")
require(red(I1-I0-s.Rational(3,2))==0, "exact Golden identity 15")
# mean preserving vertical infinitesimal: gain changes +p f,-p^2 f.
v0=p;v1=-p*p
require(red(q0*v0+q1*v1)==0, "exact Golden identity 18")
require(red(v1-v0+1)==0, "exact Golden identity 19")
# At the base, absolute amplitude binding yields w_b^2 = a^2 q_b.
# N(f)/N(0)=q0 exp(2 ln(phi) p f)+q1 exp(-2 ln(phi)p^2 f)
ell=s.symbols('ell',positive=True)
prime=red(2*ell*(q0*v0+q1*v1))
second=red(4*ell**2*(q0*v0**2+q1*v1**2))
require(prime==0, "exact Golden identity 25")
require(red(second-4*ell**2*p**3)==0, "exact Golden identity 26")
# Source of action -log_phi norm^2: second derivative = -4 p^3 ln(phi)
curvature=red(-second/ell)
require(red(curvature+4*p**3*ell)==0, "exact Golden identity 29")
# Normalized Book q1 changes at the base with derivative -2 ln(phi) q0 q1
book_q1_prime=red(2*ell*(q0*q1)*(v1-v0))
require(red(book_q1_prime+2*ell*p**3)==0, "exact Golden identity 32")
# A common factor changes log norm but cannot restore the relative branch ratio.
print('PASS exact Golden fibre checks')
print('mean Info=', h,'; I0=',I0,'; I1=',I1)
print('d normalized Book q1 / df =',book_q1_prime)
print('d log_norm squared / df =',prime)
print('d² log_norm squared / df² =',second)
print('d²[-log_phi norm²]/df² =',curvature)
