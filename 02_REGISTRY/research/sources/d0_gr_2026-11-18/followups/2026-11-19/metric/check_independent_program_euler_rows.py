"""Recorded 16-program code/CQ counterexample and symmetry identity.

This is one conditional, finite, explicitly stated ledger, not the complete
Book03 action, printer or all-path clock.
"""
import json
import math
import numpy as np

m=16;ell=math.log((1+math.sqrt(5))/2)
def h(t):return -t*math.log(t)-(1-t)*math.log(1-t)
def hp(t):return math.log((1-t)/t)
def value(t):
    return sum(1+x for x in t[:8])+sum(2-x for x in t[8:])-sum(h(x) for x in t)/ell

def gradient(t):return np.array([1-hp(x)/ell if i<8 else -1-hp(x)/ell for i,x in enumerate(t)])
t=np.full(m,.5);g=gradient(t)
assert np.all(g[:8]==1) and np.all(g[8:]==-1)
assert sum(g)==0
before=value(t);step=.01
new=np.array([.5-step]*8+[.5+step]*8)
after=value(new)
assert after<before and before>0 and after>0
# Exact code-Kraft identity: each partial term is KL(Bern(t)||Bern(p^2))
# or KL(Bern(t)||Bern(p)), divided by ln(phi).
p=(math.sqrt(5)-1)/2
def kl(x,y):return x*math.log(x/y)+(1-x)*math.log((1-x)/(1-y))
kl_value=(sum(kl(x,p*p) for x in new[:8])+sum(kl(x,p) for x in new[8:]))/ell
assert abs(kl_value-after)<1e-12
opt=np.array([p*p]*8+[p]*8)
assert abs(value(opt))<1e-12 and abs(float(np.mean(opt))-.5)<1e-15
# Independent weighted sum of code lengths for all 2^16 actual outcome
# strings at t=1/2; entropy is exactly m ln2 and output is a pure conditional
# record for each outcome.
mean=0.
for bits in range(1<<m):
    L=sum(1+((bits>>i)&1) for i in range(8))
    L+=sum(2-((bits>>i)&1) for i in range(8,16))
    mean+=L/(1<<m)
assert mean==24
assert abs(before-(24-16*math.log(2)/ell))<1e-12
# Independent straight variations remain invisible to their common diagonal.
assert abs(np.dot(g,np.ones(m)))<1e-14
assert np.linalg.norm(g)>0
# Symmetric differentiable scalar: at a diagonal point, all partials equal;
# check on a nonlinear symmetric polynomial, plus a correct antisymmetric
# perturbation which vanishes on the diagonal but not in individual rows.
x=np.full(m,.37)
coefficient=2*x+sum(x)*np.ones(m)
assert np.max(coefficient)-np.min(coefficient)<1e-14
anti=np.array([1.,-1.]+[0.]*(m-2))
assert np.dot(anti,np.ones(m))==0 and np.linalg.norm(anti)>0
p=(math.sqrt(5)-1)/2;delta=p**9
print(json.dumps({'status':'PASS','m':m,'all_outcome_strings_checked':1<<m,
 'mean_printed_code_length':mean,'initial_partial_code_minus_CQ':before,
 'independent_gradient_in_t':[float(v) for v in g],
 'common_diagonal_derivative':float(sum(g)),
 'opposite_parameter_step':step,'new_partial_value':after,
 'KL_expression_and_zero_global_minimum_checked':True,
 'global_minimum_preserves_average_program_parameter':True,
 'delta_for_N8':delta,'individual_gradient_in_q_magnitude':1/delta,
 'symmetric_ledger_diagonal_controls_all_m_rows':True,
 'full_native_printer_and_Book03_action_derived':False,
 'actual_full_source_has_this_asymmetry':False,'GR_closed':False},indent=2))
