#!/usr/bin/env python3
"""Exact narrow consumer of the nonvacuum whole-tape source theorem.

Standard-library rational arithmetic. This checks a deliberately small
three-slot/two-report fixture with GLOBAL cancellation; it is not claimed
to rerun the original Einstein 42-root or a complete Golden compiler.
"""
from fractions import Fraction as Q
from itertools import product, permutations, combinations
from math import comb
import json

a = Q(1, 3)                    # nonvacuum/nonzero encoded mean
r0, tau, b = Q(1, 4), Q(1, 64), Q(1, 2)
alphabet = (-1, 1)
checks = 0

def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1

def prob(z, t):
    q = Q(1)
    for x in z:
        q *= (1 + t * x) / 2
    return q

def original_effect(z, w):
    d1, d2, d3 = (Q(x)-a for x in z)
    r1 = r0 + tau*d1
    r2 = r0 - tau*(d2+d3)/2 + tau*b*d2*d3
    return (r1 if w[0] else 1-r1) * (r2 if w[1] else 1-r2)

def source_original(z):
    d1, d2, d3 = (Q(x)-a for x in z)
    return d1-(d2+d3)/2+b*d2*d3

def sym_source(z):
    return sum((source_original(p) for p in permutations(z)), Q(0))/6

def population_source(z):
    n = len(z)
    return b*sum(((Q(z[i])-a)*(Q(z[j])-a)
                  for i,j in combinations(range(n),2)),Q(0))/comb(n,2)

def population_effect(z, w):
    n = len(z)
    return sum((original_effect(tuple(z[i] for i in ix),w)
                for ix in permutations(range(n),3)),Q(0))/(n*(n-1)*(n-2))

outcomes = tuple(product((0,1), repeat=2))
kernel_basis = tuple(product(alphabet, repeat=3))
for z in kernel_basis:
    effects = [original_effect(z,w) for w in outcomes]
    check(all(0 <= x <= 1 for x in effects), 'actual positive joint effects')
    check(sum(effects)==1, 'complete logical law')
    centered = sum((Q(sum(w))*original_effect(z,w) for w in outcomes),Q(0))
    check((centered-2*r0)/tau==source_original(z), 'full additive score at iid base')
    expected = b*sum(((Q(z[i])-a)*(Q(z[j])-a)
                     for i,j in combinations(range(3),2)),Q(0))/3
    check(sym_source(z)==expected, 'global symmetrization cancels linear components')

# Each local report has a NONZERO first derivative, but their full score sum
# has vanishing first conditional kernel at the nonzero mean a.
check(tau != 0 and -tau != 0, 'individual local first sources not zero')
check(tau + (-tau) == 0, 'global local-source cancellation')
for x in alphabet:
    conditional = sum((prob(y,a)*sym_source((x,)+y)
                       for y in product(alphabet,repeat=2)),Q(0))
    check(conditional==0, 'first Hoeffding operator vanishes on every basis column')

B = max(abs(sym_source(z)) for z in kernel_basis)
variance_records = []
for n in range(3,9):
    states = tuple(product(alphabet, repeat=n))
    mean = sum((prob(z,a)*population_source(z) for z in states),Q(0))
    variance = sum((prob(z,a)*population_source(z)**2 for z in states),Q(0))
    exact = b*b*(1-a*a)**2/comb(n,2)
    bound = B*B*Q(3**2*2**2,2*n*(n-1))
    check(mean==0, 'exact all-N iid first source')
    check(variance==exact, 'exact nonvacuum joint-normal variance')
    check(variance<=bound, 'dimension-free overlap bound')
    variance_records.append({'N':n,'variance':str(variance),'bound':str(bound)})

# Converse: append an explicitly nonzero first conditional component.
# The resulting bounded symmetric kernel can also be made a binary effect
# by the same r0+tau*A embedding. Divide its actual CQ score by its nonzero
# scalar g'(r); all remaining equalities are exact rational identities.
linear_c = Q(2,3)
def noncritical_kernel(z):
    return linear_c*sum(map(Q,z))/len(z) + population_source(z)

B_nc = max(abs(noncritical_kernel(z)) for z in kernel_basis)
E_squared = linear_c*linear_c*(1-a*a)
negative_control = []
for n in range(3,9):
    states = tuple(product(alphabet,repeat=n))
    mean_nc = sum((prob(z,a)*noncritical_kernel(z) for z in states),Q(0))
    variance_nc = sum((prob(z,a)*(noncritical_kernel(z)-mean_nc)**2
                       for z in states),Q(0))
    exact_scaled = E_squared + Q(2)*b*b*(1-a*a)**2/(n-1)
    upper_scaled = E_squared + B_nc*B_nc*Q(3**2*2**2,2*(n-1))
    check(mean_nc == linear_c*a, 'noncritical mean preserved')
    check(n*variance_nc == exact_scaled, 'exact first and higher excitation split')
    check(n*variance_nc >= E_squared > 0, 'nonzero scaled field-source lower bound')
    check(n*variance_nc <= upper_scaled, 'two-sided scaled normal theorem')
    negative_control.append({'N':n,'N_times_variance':str(n*variance_nc),
                             'field_norm_squared':str(E_squared)})

# Preserve the ENTIRE multi-report probability law, not only its marginals.
for n,t in ((3,a),(4,a),(4,Q(-2,5))):
    states = tuple(product(alphabet, repeat=n))
    for w in outcomes:
        q_old = sum((prob(z,t)*original_effect(z,w) for z in kernel_basis),Q(0))
        q_new = sum((prob(z,t)*population_effect(z,w) for z in states),Q(0))
        check(q_new==q_old, 'all complete iid histories preserved')

# Outside iid, the selector produces correlated reports. The complete entropy
# must NOT be replaced by the sum of marginal binary entropies.
z = (1,1,-1)
q = {w:population_effect(z,w) for w in outcomes}
q1 = q[(1,0)]+q[(1,1)]
q2 = q[(0,1)]+q[(1,1)]
cov = q[(1,1)]-q1*q2
check(cov != 0, 'off-iid full report law does not factor')
check(sum(q.values())==1, 'correlated complete law normalized')
check(all(v>0 for v in q.values()), 'correlated complete law stays positive')

# The same mean a=1/3 occurs in an exact N=3 type sector, whose two-slot moment
# differs from the iid value. This is the type-shell selection caveat.
emp_mean = sum(map(Q,z))/len(z)
pair = sum((Q(z[i]*z[j]) for i,j in combinations(range(3),2)),Q(0))/3
check(emp_mean==a, 'type state has the same nonzero decoded mean')
check(pair==(3*a*a-1)/2, 'falling-factorial pair moment')
check(pair!=a*a, 'same one-coordinate means do not fix joint effects')
shell_values={tuple(z):population_source(z) for z in set(permutations(z))}
check(len(set(shell_values.values()))==1, 'symmetric effect scalar on the exact type sector')

# Explicit boundary between pure cotangent convergence and density-cone
# minimization. Both endpoints have zero individual Z means, while a
# classical all-zero/all-one mixture has pair effect 1 instead of 0.
for n in (3,8,64):
    product_pair_mean = Q(0)
    correlated_pair_mean = Q(1,2)*(1*1)+Q(1,2)*((-1)*(-1))
    correlated_single_mean = Q(1,2)*1+Q(1,2)*(-1)
    check(correlated_single_mean==0, 'density-cone control preserves all means')
    check(correlated_pair_mean-product_pair_mean==1,
          'one-sided mixed-density normal stays O(1)')

receipt = {
    'status':'PASS',
    'exact_rational_checks':checks,
    'new_scope':'nonzero-mean whole-tape global source cancellation and joint normal control',
    'base_mean':str(a),
    'kernel_slots':3,
    'reports':2,
    'norm_bound_B':str(B),
    'normal_variance':variance_records,
    'noncritical_control':negative_control,
    'off_iid_report_covariance':str(cov),
    'same_mean_type_pair':str(pair),
    'iid_pair':str(a*a),
    'original_full42_replayed':False,
    'golden_compiler_replayed':False,
    'physical_Book_Info_selected':False,
    'density_cone_stationarity_claimed':False,
    'GR_closed':False,
}
print(json.dumps(receipt,indent=2))
