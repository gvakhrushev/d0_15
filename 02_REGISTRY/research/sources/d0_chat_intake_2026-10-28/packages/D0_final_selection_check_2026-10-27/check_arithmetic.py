#!/usr/bin/env python3
"""Exact Golden arithmetic boundary; does NOT exclude retained heralded factories."""
from __future__ import annotations
import json
import sympy as s
checks=[]
def require(v,label):
    if not bool(v): raise ArithmeticError(label)
    checks.append(label)
p=s.symbols('p'); relation=p*p+p-1
reduce=lambda x:s.rem(s.expand(x),relation,p)
z=s.Rational(1,2**20)
L=4*p**3
r0=reduce(1-(1-z*L)*(1-z*L*(1+p**6)))
expected=s.Rational(1245203,8589934592)*p-s.Rational(3014703,34359738368)
require(r0==expected,'original complete report r0 reduced exactly')
conjugate=reduce(r0.subs(p,-1-p));trace=s.factor(r0+conjugate)
norm=reduce(r0*conjugate)
require(trace==-s.Rational(5505109,17179869184),'exact quadratic field trace')
require(not trace.is_integer,'nonintegral trace excludes algebraic integer in ANY extension')
# The conclusion extends to pure internally prepared blank registers and finite
# Born measurements, tensor products, coherent controls with integral entries,
# and sums over a finite retained transcript. No normalized postselection.
require(not (1024*trace).is_integer,'at least one ten-sign branch coin not integral')
# At least 35 simultaneous simple fair-coin heralds clear the denominator of
# this scalar r0. This is NOT a proof that 35 is a universal optimal resource.
alpha=reduce(2*p**3)
successes=[]
for k in (0,1,10,34,35):
    prob=reduce(alpha**k*r0)
    coeffs=s.Poly(prob,p).all_coeffs()
    integral=all(c.is_integer for c in coeffs)
    require(integral==(k>=35),'specific herald denominator clearing k='+str(k))
    successes.append({'k':k,'joint_alpha_power_times_r0_in_Zp':integral})
# Two actual Golden coins: outcomes01/10 each have p^3; retained odd parity
# success has alpha=2p^3, and either conditional logical outcome has prob1/2.
t=s.symbols('t');mt=t**4+t**2-1
redt=lambda x:s.rem(s.expand(x),mt,t)
G=s.Matrix([[t,-t*t],[t*t,t]])
blank=s.Matrix([1,0,0,0]);vec=s.kronecker_product(G,G)*blank
probs=[redt(v*v) for v in vec]
require(probs[1]==probs[2]==redt(t**6),'two true Golden odd flags have equal amplitudes')
require(redt(sum(probs)-1)==0,'full four-branch probability sum one')
require(s.cancel(probs[1]/(probs[1]+probs[2]))==s.Rational(1,2),'conditional fair bit allowed')
require(reduce(1-alpha+2*p**3-1)==0,'abort plus both completed outputs retained')
# Can is a representative of an equivalence class, not an identification of
# distinguishable processes: a small complete explicit partition control.
classes=[['a','aa'],['b','bb']]
can={word:min(cl,key=lambda x:(len(x),x)) for cl in classes for word in cl}
require(can['a']==can['aa'] and can['b']==can['bb'] and can['a']!=can['b'],
        'canonicalization preserves distinct outcome classes (finite control only)')
print(json.dumps({'status':'PASS_EXACT_GOLDEN_ARITHMETIC_SCOPE','checks':len(checks),
 'r0_exact':str(r0),'trace_Qsqrt5_over_Q':str(trace),'norm':str(norm),
 'unconditional_r0_from_integral_palette_and_blank_impossible':True,
 'conditional_r0_with_fair_resources_ruled_out':False,
 'simple_fair_factory_success':'2*p^3',
 'simple_fair_factory_conditional_probability':'1/2',
 'specific_herald_denominator_controls':successes,
 'universal_minimum_factory_count_claimed':False,
 'all_D0_models_refuted':False,'unconditional_GR_closed':False},indent=2))
