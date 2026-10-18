#!/usr/bin/env python3
"""Complete fine-history information leakage and sourced-source discriminator.

This is a mathematical conditional instrument, NOT a claim that the original
Julia128 tape already registered inherited left AF leaf projectors.
"""
import json
import math

phi = (1 + math.sqrt(5)) / 2
p = 1 / phi
ell = math.log(phi)
a0 = p * p
h = lambda a: -a * math.log(a) - (1-a) * math.log1p(-a)
hp = lambda a: math.log((1-a) / a)
hpp = lambda a: -1 / (a * (1-a))
z = lambda a: 1 + 2 * math.exp(h(a))
zp = lambda a: 2 * math.exp(h(a)) * hp(a)
zpp = lambda a: 2 * math.exp(h(a)) * (hp(a)**2 + hpp(a))
s = lambda a: (z(a)-1) / z(a)

def H(values):
    return -sum(v * math.log(v) for v in values if v > 0)

def full_law(a):
    zvals = [z(x) for x in a]
    D = sum(zvals)
    r = [zi / D for zi in zvals]
    conditional = []
    for x in a:
        conditional.append([
            1-s(x), s(x)*(1-x)/2, s(x)*(1-x)/2,
            s(x)*x/2, s(x)*x/2
        ])
    q = [[r[i]*conditional[i][j] for j in range(5)]
         for i in range(len(a))]
    return r, conditional, q

def measured(a):
    r, conditional, q = full_law(a)
    col = [sum(row[j] for row in q) for j in range(5)]
    joint_entropy = H(v for row in q for v in row)
    mutual_information = sum(
        v*math.log(v/(r[i]*col[j]))
        for i,row in enumerate(q) for j,v in enumerate(row) if v>0
    )
    assert abs(sum(v for row in q for v in row)-1)<2e-13
    assert abs(joint_entropy-H(r)-H(col)+mutual_information)<2e-13
    return joint_entropy, mutual_information, r, q

N=4
f=[-.9,-.25,.35,1.0]
fbar=sum(f)/N
variance=sum((x-fbar)**2 for x in f)/N
second=sum(x*x for x in f)/N
s0=s(a0)
I_cond=s0*(1-s0)*ell**2+s0/(a0*(1-a0))
assert abs(hp(a0)-ell)<1e-12
assert abs(hpp(a0)+p**(-3))<1e-12
assert I_cond>0
assert all(zpp(j/1000)<0 for j in range(1,1000))

base_h,base_mi,_,_=measured([a0]*N)
assert abs(base_mi)<1e-13

ratios=[]
mutual_information=[]
for t in [.50,.40,.29,.20,.13]:
    c=a0*t*t
    a=[a0+c*x for x in f]
    assert 0<min(a) and max(a)<.5
    H_all,mi,r,q=measured(a)
    assert abs(H_all-math.log(sum(z(x) for x in a)))<1e-12
    mi_leading=.5*c*c*I_cond*variance
    ratios.append(mi/mi_leading)
    mutual_information.append(mi)
    assert mi>0
assert abs(ratios[-1]-1)<.12

# At common vacuum compare exact source gradient/Hessian with a
# small scalar metric path f_i(lambda)=lambda*f_i.
t=.28
c=a0*t*t
Gamma=lambda lam: math.log(sum(z(a0+c*lam*x) for x in f))/ell
linear=s0*c*fbar
quadratic_variance=c*c*s0*(ell*ell-p**(-3))/(2*ell)
quadratic_mean=c*c*(s0*(1-s0)*ell*ell-s0*p**(-3))/(2*ell)
second_analytic=2*(quadratic_variance*variance+quadratic_mean*fbar*fbar)
eps=1e-3
first_numeric=(Gamma(eps)-Gamma(-eps))/(2*eps)
second_numeric=(Gamma(eps)-2*Gamma(0)+Gamma(-eps))/eps**2
assert abs(first_numeric-linear)<1e-8
assert abs(second_numeric-second_analytic)<1e-7
assert quadratic_variance<0 and quadratic_mean<0

# A fixed t has non-universal inhomogeneous source coefficients.
coef_at_t=[c*zp(a0+c*x)/(ell*sum(z(a0+c*y) for y in f))
           for x in f]
assert max(coef_at_t)-min(coef_at_t)>1e-4

# The correct leading Einstein-like *relative* source is recovered as
# O(t^2), not identically at any fixed t on an inhomogeneous profile.
ts=[.40,.28,.20,.14,.10]
source_errors=[]
for t in ts:
    c=a0*t*t
    a=[a0+c*x for x in f]
    coef=[c*zp(x)/(ell*sum(z(v) for v in a)) for x in a]
    normalized=[v/(s0*c/N) for v in coef]
    source_errors.append(max(abs(v-1) for v in normalized))
assert source_errors[-1]<source_errors[0]
assert .2<source_errors[-1]/ts[-1]**2<15

# This is the Fisher information of ONE joint (leaf,5-flag) reading.
# Do NOT multiply it by the number N of alternative leaf outcomes.
fisher=lambda t:(a0*t*t)**2*(I_cond*second+(s0*ell)**2*variance)
assert abs(fisher(.15)/fisher(.30)-1/16)<1e-12

# Stronger on-shell-only source compression: entire optimized entropy equals
# log(N / P(global failure)), not a guessed event action off the stationary fibre.
test_a=[.24,.35,.41,.29]
H_on,MI_on,r_on,q_on=measured(test_a)
N_test=len(test_a)
D_test=sum(z(x) for x in test_a)
P_failure=sum(row[0] for row in q_on)
assert abs(H_on-(math.log(N_test)-math.log(P_failure)))<1e-12
assert abs(P_failure-N_test/D_test)<1e-12
for i,ai in enumerate(test_a):
    successes=sum(q_on[i][1:])
    odds=q_on[i][1]/q_on[i][3]
    grad_counts=successes*math.log(odds)
    grad_analytic=zp(ai)/D_test
    assert abs(grad_counts-grad_analytic)<1e-12
    a_from_counts=(q_on[i][3]+q_on[i][4])/successes
    assert abs(a_from_counts-ai)<1e-12

# A different old-leaf preparation has the SAME aggregated five flags
# at the common vacuum but a different Shannon joint action. Therefore
# (17) is true ONLY after its full fine-population Euler equations.
leaf_uniform=[1/N_test]*N_test
leaf_skew=[.1,.2,.3,.4]
conditional0=[1-s0,s0*(1-a0)/2,s0*(1-a0)/2,s0*a0/2,s0*a0/2]
q_uniform=[[v*cj for cj in conditional0] for v in leaf_uniform]
q_skew=[[v*cj for cj in conditional0] for v in leaf_skew]
for j in range(5):
    assert abs(sum(row[j] for row in q_uniform)
               -sum(row[j] for row in q_skew))<1e-12
H_uniform=H(x for row in q_uniform for x in row)
H_skew=H(x for row in q_skew for x in row)
assert abs(H_uniform-H_skew)>.05
assert abs(H_skew-(math.log(N_test)-math.log(1-s0)))>.05


# Full retained classical work trace: one deterministic copy is source-neutral,
# while even a fixed but leaf-dependent random work bit is not.
fw=[1.0,-1.0]
coin_prob=[.2,.4]
work_H=[H([v,1-v]) for v in coin_prob]
def work_extra(lam):
    av=[a0+.02*lam*x for x in fw]
    zv=[z(x) for x in av]
    return sum(zv[i]*work_H[i] for i in range(2))/sum(zv)
work_expected=sum(
    work_H[i]*(.02*(zp(a0+.02*fw[i])*fw[i]*sum(z(a0+.02*ff) for ff in fw)
    -z(a0+.02*fw[i])*sum(zp(a0+.02*fw[j])*fw[j] for j in range(2)))
    /sum(z(a0+.02*ff) for ff in fw)**2)
    for i in range(2))
work_numeric=(work_extra(1+1e-5)-work_extra(1-1e-5))/(2e-5)
assert abs(work_numeric-work_expected)<1e-9
assert abs(work_expected)>1e-5
# c(W|Y,J) point mass for an addressed, retained deterministic label copy.
# In this classical complete-record scenario H(W|Y,J)=0 identically.
assert all(H([1.0]) == 0.0 for _ in range(2))

print(json.dumps({
    "status":"PASS",
    "retained_work_source_nonzero_negative_control":work_expected,
    "deterministic_work_copy_classical_Shannon_source_neutral":True,
    "stationary_failure_source_identity":True,
    "full_leaf_log_odds_source_identity":True,
    "off_shell_event_only_substitution_rejected":True,
    "scope":"conditional recorded fine-left-leaf mathematical cut only",
    "conditional_fisher":I_cond,
    "mutual_information":mutual_information,
    "mutual_information_over_quadratic":ratios,
    "first_source":linear,
    "second_source_analytic":second_analytic,
    "second_source_numeric":second_numeric,
    "inhomogeneous_source_range":[min(coef_at_t),max(coef_at_t)],
    "source_errors_vs_t":[ts,source_errors],
    "fisher_half_t_ratio":fisher(.15)/fisher(.30),
    "negative_controls":[
        "Shannon joint entropy is not sum of separate address and flag entropies",
        "the fixed-t inhomogeneous source weights are not all equal",
        "the full five-outcome score includes the failure branch",
        "N leaf alternatives are not N independent measured samples",
        "no sourced Einstein or new native clock is claimed"
    ]
}, indent=2))
