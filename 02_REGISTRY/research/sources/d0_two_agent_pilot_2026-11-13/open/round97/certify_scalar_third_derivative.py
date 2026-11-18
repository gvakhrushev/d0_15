#!/usr/bin/env python3
"""Uniform third derivative of B65's actual I_tau on the B21 cube."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sympy as s
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
b65=json.loads((O/'round65/SCALAR_HESSIAN_ENVELOPE.json').read_text());assert b65['status']=='PASS_EXPLICIT_CONSERVATIVE_SCALAR_HESSIAN_ENVELOPE'
# For unit h,k,l, D^r exp(Theta) has norm <=(sqrt6)^r exp(||Theta||).
# Four link/inverse factors: sum of the four directional costs <10.
L=F(17,16);P0=L**4;P1=F(14);P2=F(128);P3=F(1000)*P0
assert P0<F(4,3) and P3<2048
# Exterior degree k<=4, three marked directions, full Leibniz rule.
E0=F(4);E1=F(160);E2=F(6000)
E3=4*F(4,3)**3*2048+36*F(4,3)**2*128*14+24*F(4,3)*14**3
assert E3<2**18
# A11 scalar f: creator-commutator factor A has (A0,A1,A2,A3)<(2,4,4,0).
f0=1<<13;f1=1<<18;f2=1<<23
f3=6*F(800,9)*(3*4*E1+3*4*E2+2*E3)
assert f3<1<<29
# q has two coframe-linear and two matter-difference-linear factors. B65
# base norm 12, derivative ratios (1/2,1/2,16,16).
from itertools import combinations
ratios=(F(1,2),F(1,2),F(16),F(16))
q3=12*6*sum((ratios[i]*ratios[j]*ratios[k] for i,j,k in combinations(range(4),3)),F())
assert q3==19008 and q3<1<<15
q0=16;q1=1<<9;q2=1<<13
# Actual B25 reporter polynomial, exact coefficient sums on |p,x,y,z|<=1.
p,x,y,z=s.symbols('p x y z');E=p**2*(1+x);ell=4*E*(1-E);u=p+p**2*y;b=4*u**2*(1-u**2);A=ell+(1-ell)*b;r=s.expand(1-(1-z*b)*(1-z*A))
def coeff(v):return sum(abs(c) for c in s.Poly(v,p,x,y,z).coeffs())
assert coeff(s.diff(r,x,3))==0
assert coeff(s.diff(r,y,3))==5097600 and coeff(s.diff(r,y,3))<1<<23
# B65 gives rho>=1/2, eps=2^-1531, |r_x/r_x0|,|r_y/r_y0|<2,
# |r_xx/r_x0|<2^47, |r_yy/r_y0|<2^43; r_y0>2^-22.
eps=F(1,1<<1531);eprho=2*eps
nonlinear_f=3*eprho*(1<<47)*f1*f2
nonlinear_q=24*3*eprho*(1<<43)*q1*q2
cubic_q=24*eprho**2*(1<<45)*q1**3
M3=2*f3+48*q3+nonlinear_f+nonlinear_q+cubic_q
assert M3<1<<31
# Value and gradient for same fixed-reference univariate reporter chain.
Imax=2*f0+48*q0;I1=2*f1+48*q1
assert Imax<1<<15 and I1<1<<20
# Product quadratic cancellation from B95, with R_v<104, ||X_j||<1.
sigma=F(1,1<<80);bias=M3*sigma**2*104**3/3
assert bias<F(1,1<<109)
inputs=[O/'round65/SCALAR_HESSIAN_ENVELOPE.json',O/'round65/certify_scalar_hessian_envelope.py',O/'round21/CHART_ENVELOPE_RESULT.json',O/'round25/TARGETS_RU.md',O/'round95/QUADRATIC_LIFT_CHECK.json',D/'round11/source_operator_dag.py']
out={'status':'PASS_UNIFORM_I_TAU_THIRD_DERIVATIVE_ON_B21_CUBE','scope':'B25 fixed rho/reference/SITE, original normalized I_tau and B21 Euclidean raw chart; mixed unit directions','link_third_derivative_lt':'2^11','exterior_third_derivative_lt':'2^18','local_f_third_derivative_lt':'2^29','local_q_third_derivative_lt':'2^15','reporter_y_third_abs_coefficient_sum':5097600,'reporter_x_third_derivative_zero':True,'I_tau_value_lt':'2^15','I_tau_gradient_norm_lt':'2^20','I_tau_third_derivative_norm_lt':'2^31','born_product_scalar_quadratic_lift_bias_lt':'2^-109','quadratic_bias_requires_B95_born_product_state':True,'physical_admission_or_GR_proved':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in inputs}}
(P/'SCALAR_THIRD_DERIVATIVE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
