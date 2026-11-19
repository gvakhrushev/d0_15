#!/usr/bin/env python3
"""Bounded controls of the paid selector / WHOLE-tape price application.

This is an exact finite control of the new identities, not a replay of the
original full128 instrument or an independent verification of Golden factories.
Only the entropy/score evaluations use floating logarithms.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product, combinations
from math import log, sqrt
from pathlib import Path
import json

COUNTS = {"exact": 0, "floating": 0}
GROUPS = {}


def exact(condition, label):
    COUNTS["exact"] += 1
    if not condition:
        raise AssertionError(label)


def near(a, b, label, tol=5e-12):
    COUNTS["floating"] += 1
    if abs(a - b) > tol:
        raise AssertionError((label, a, b, abs(a-b)))


def positive_float(value, label):
    COUNTS["floating"] += 1
    if not value > 0:
        raise AssertionError((label, value))


def selected_permutations(n, k):
    for labels in product(*(range(n-r) for r in range(k))):
        order = list(range(n))
        for r, label in enumerate(labels):
            j = r + label
            order[r], order[j] = order[j], order[r]
        yield labels, tuple(order)


def falling(n, k):
    result = 1
    for j in range(k):
        result *= n-j
    return result


start = dict(COUNTS)
for n in range(1, 8):
    for k in range(1, min(n, 4)+1):
        permutations = list(selected_permutations(n, k))
        first = [o[:k] for _, o in permutations]
        exact(len(first) == falling(n, k), "number of addressed alternatives")
        exact(len(set(first)) == len(first), "ordered injections occur once")
        exact(all(len(set(x)) == k for x in first), "no slot repeats")
        exact(all(sorted(o) == list(range(n)) for _, o in permutations),
              "whole-bank map is a permutation")
        exact(sum((F(1, falling(n,k)) for _ in first), F(0)) == 1,
              "coherent branch weights normalize")
for j in range(1, 65):
    m = (j-1).bit_length()
    success = F(j, 2**m)
    exact(success > F(1,2), "true label herald exceeds one half")
    exact(success <= 1, "label probability bound")
    exact(1-success < F(1,2), "exhaustion bound")
epsilon, k = F(1,1024), 17
cap = 0
while F(k, 2**cap) > epsilon/3:
    cap += 1
exact(F(k,2**cap) <= epsilon/3, "honest union cap")
GROUPS["coherent_partial_fisher_yates"] = {
    "checks": {k: COUNTS[k]-start[k] for k in COUNTS},
    "uniform_label_cap_example": cap,
}


BITS = tuple(product((0,1), repeat=2))


def r1(bit):
    return F(3,10) + F(1,10)*(1-2*bit)


def r2(bit):
    return F(1,2) + F(1,5)*(1-2*bit)


def old_effect(out, inputs):
    r = (r1(inputs[0]), r2(inputs[1]))
    return (r[0] if out[0] else 1-r[0]) * (r[1] if out[1] else 1-r[1])


def new_effect(n, out, bank_bits):
    return sum((old_effect(out, (bank_bits[order[0]], bank_bits[order[1]]))
                for _, order in selected_permutations(n,2)), F(0)) / falling(n,2)


def iid_probability(bits, t):
    result = F(1)
    for bit in bits:
        result *= (1+t*(1-2*bit))/2
    return result


start = dict(COUNTS)
for n in range(2,8):
    basis = tuple(product((0,1), repeat=n))
    for b in basis:
        effects = [new_effect(n,out,b) for out in BITS]
        exact(sum(effects,F(0)) == 1, "whole new instrument is complete")
        for out, e in zip(BITS,effects):
            sym = sum(((old_effect(out,(b[i],b[j]))+
                         old_effect(out,(b[j],b[i])))/2
                       for i,j in combinations(range(n),2)), F(0))
            sym /= n*(n-1)//2
            exact(e == sym, "ordered injection equals U-statistic symmetrization")
    for t in (F(0),F(1,3),F(-2,5)):
        old_r = (F(3,10)+t/F(10), F(1,2)+t/F(5))
        for out in BITS:
            q = sum((iid_probability(b,t)*new_effect(n,out,b) for b in basis),F(0))
            expected = ((old_r[0] if out[0] else 1-old_r[0]) *
                        (old_r[1] if out[1] else 1-old_r[1]))
            exact(q == expected, "complete iid joint tape is unchanged")

# An explicit unnormalized V has orthogonal integer permutation blocks.
# V/sqrt(M) is the coherent isometry; no numerical square root is needed.
n = 3
basis = tuple(product((0,1), repeat=n))
index = {b:i for i,b in enumerate(basis)}
orders = [o for _,o in selected_permutations(n,2)]
d, multiplicity = len(basis), len(orders)
v = [[0]*d for _ in range(d*multiplicity)]
for a, order in enumerate(orders):
    for col,b in enumerate(basis):
        row = index[tuple(b[j] for j in order)]
        v[a*d+row][col] = 1
for i in range(d):
    for j in range(d):
        exact(sum(row[i]*row[j] for row in v) == multiplicity*(i==j),
              "V* V = (N)_k I before normalization")
for out in BITS:
    diagonal = [old_effect(out,b[:2]) for _ in orders for b in basis]
    for i in range(d):
        for j in range(d):
            entry = sum((diagonal[z]*v[z][i]*v[z][j] for z in range(len(v))),F(0))
            entry /= multiplicity
            expected = new_effect(n,out,basis[i]) if i==j else F(0)
            exact(entry == expected, "full retained-selector compression")
GROUPS["whole_instrument_and_iid_law"] = {
    "checks": {k: COUNTS[k]-start[k] for k in COUNTS},
    "isometry_input_dimension": d,
    "isometry_retained_output_dimension": d*multiplicity,
}


phi = (1+sqrt(5))/2
ell = log(phi)


def entropy(probabilities):
    return -sum(float(p)*log(float(p))/ell for p in probabilities if p)


def terminal_price(q):
    return sum(float(p)*(2+sum(out)) for out,p in zip(BITS,q)) - entropy(q)


start = dict(COUNTS)
q_iid = [old_effect(out,(0,0))/4 + old_effect(out,(0,1))/4 +
         old_effect(out,(1,0))/4 + old_effect(out,(1,1))/4 for out in BITS]
q_correlated = [(old_effect(out,(0,0))+old_effect(out,(1,1)))/2 for out in BITS]
q_other = [F(1,10),F(1,5),F(3,10),F(2,5)]
pi, cost_t = (F(1,3),F(2,5),F(4,15)), (2,5,7)
gamma = pi[0]+pi[1]
baseline = sum(float(p)*c for p,c in zip(pi,cost_t))-entropy(pi)
for q in (q_iid,q_correlated,q_other):
    exact(sum(q,F(0)) == 1, "complete terminal distribution")
    full, full_cost = [], []
    for t in range(2):
        for out,p in zip(BITS,q):
            full.append(pi[t]*p)
            full_cost.append(cost_t[t]+2+sum(out))
    full.append(pi[2])
    full_cost.append(cost_t[2])
    exact(sum(full,F(0)) == 1, "all success and abort leaves retained")
    direct = sum(float(p)*c for p,c in zip(full,full_cost))-entropy(full)
    composed = baseline+float(gamma)*terminal_price(q)
    near(direct,composed,"exact paid complete-tape composition")

def marginals(q):
    return [sum((p for out,p in zip(BITS,q) if out[j]),F(0)) for j in range(2)]

def additive_binary_price(q):
    return sum(1+float(r)-entropy((1-r,r)) for r in marginals(q))

near(terminal_price(q_iid), additive_binary_price(q_iid), "additive only at iid law")
joint_entropy_correction = terminal_price(q_correlated)-additive_binary_price(q_correlated)
positive_float(joint_entropy_correction, "correlated tape cannot use sum of binary entropies")
correlation_source = log(float(q_correlated[0]*q_correlated[3]/
                              (q_correlated[1]*q_correlated[2])))/ell
positive_float(correlation_source, "whole source sees fixed-marginal correlation variation")
near(sum((2+sum(out)+(1+log(float(q)))/ell)*sign
         for out,q,sign in zip(BITS,q_correlated,(1,-1,-1,1))),
     correlation_source, "joint source versus false zero marginal source")

# At the product base the WHOLE source score reduces to the additive operator.
rs = marginals(q_iid)
score_const = 2+(1+sum(log(float(1-r)) for r in rs))/ell
score_coeff = [1+log(float(r/(1-r)))/ell for r in rs]
max_score_error = 0.0
for n in (2,3,4,5):
    for b in product((0,1),repeat=n):
        effect = [new_effect(n,out,b) for out in BITS]
        whole = sum((2+sum(out)+(1+log(float(q)))/ell)*float(e)
                    for out,q,e in zip(BITS,q_iid,effect))
        reduced = score_const + sum(score_coeff[j]*float(
            sum((e for out,e in zip(BITS,effect) if out[j]),F(0))) for j in range(2))
        max_score_error = max(max_score_error,abs(whole-reduced))
        near(whole,reduced,"ambient whole score at iid, including correlated tangents")
GROUPS["paid_complete_tape_entropy_and_source"] = {
    "checks": {k: COUNTS[k]-start[k] for k in COUNTS},
    "true_completion_probability": str(gamma),
    "correlated_minus_false_additive_price": joint_entropy_correction,
    "fixed_marginal_correlation_price_source": correlation_source,
    "maximum_additive_iid_score_error": max_score_error,
}


start = dict(COUNTS)
zeta, tau, lu, lv = F(1,2**20), F(1,512), F(2), F(3)
alphas = [64*lu*tau]*2+[64*lv*tau]*8
weight_sum, nonempty, bx, bz = F(0),F(0),F(0),F(0)
for flags in product((0,1),repeat=10):
    weight = F(1)
    for a,flag in zip(alphas,flags):
        weight *= a if flag else 1-a
    weight_sum += weight
    if any(flags):
        nonempty += weight
        # R_J=zeta*(I+a X+b Z), whose spectrum lies in [0,2 zeta].
        a = F(1 if flags[0] else -1,2)
        b = F(1 if flags[1] else -1,4)
        exact(abs(a)+abs(b) <= 1, "each subset effect bounded by 2 zeta")
        bx += weight*zeta*a
        bz += weight*zeta*b
empty = (1-64*lu*tau)**2*(1-64*lv*tau)**8
exact(weight_sum == 1, "actual independent flag weights normalize")
exact(nonempty == 1-empty, "actual all-fair branch mass")
exact(abs(bx)+abs(bz) <= 2*zeta*nonempty, "operator bound by exact mixture")
exact(2*zeta*nonempty <= 128*zeta*tau*(2*lu+8*lv), "actual tau gain bound")
GROUPS["attenuation_gain_mixture"] = {
    "checks": {k: COUNTS[k]-start[k] for k in COUNTS},
    "exact_nonempty_flag_mass": str(nonempty),
    "bound_uses_no_inverse_tau": True,
}


# Independent differentiation of the original collapsed report in the FREE
# polynomial ring Q[p,x,y,z], followed only then by p^2+p-1 reduction.
# This does not import the root checker's quadratic-number-field arithmetic.
class Poly:
    def __init__(self, terms=0):
        if isinstance(terms,dict):
            self.terms = {k:F(v) for k,v in terms.items() if v}
        else:
            self.terms = {(0,0,0,0):F(terms)} if terms else {}

    @staticmethod
    def cast(v):
        return v if isinstance(v,Poly) else Poly(v)

    def __add__(self, other):
        out = dict(self.terms)
        for k,v in self.cast(other).terms.items():
            out[k] = out.get(k,F(0))+v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k:-v for k,v in self.terms.items()})

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        out = {}
        for k,v in self.terms.items():
            for j,w in self.cast(other).terms.items():
                key = tuple(a+b for a,b in zip(k,j))
                out[key] = out.get(key,F(0))+v*w
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = Poly(1)
        for _ in range(n):
            out *= self
        return out

    def derivative(self, variable):
        out = {}
        for key,value in self.terms.items():
            if key[variable]:
                new = list(key)
                new[variable] -= 1
                out[tuple(new)] = value*key[variable]
        return Poly(out)

    def at_zero_xy(self):
        return Poly({k:v for k,v in self.terms.items() if k[1]==0 and k[2]==0})

    def reduce_p(self):
        out = {}
        for (np,nx,ny,nz),v in self.terms.items():
            a,b = 1,0
            for _ in range(np):
                a,b = b,a-b
            for power,c in ((0,a),(1,b)):
                key = (power,nx,ny,nz)
                out[key] = out.get(key,F(0))+v*c
        return {k:v for k,v in out.items() if v}


start = dict(COUNTS)
pp = Poly({(1,0,0,0):1})
xx = Poly({(0,1,0,0):1})
yy = Poly({(0,0,1,0):1})
zz = Poly({(0,0,0,1):1})
e = pp**2*(1+xx)
ll = 4*e*(1-e)
bb = pp-pp**2*yy
bprob = 4*bb**2*(1-bb**2)
aprob = ll+(1-ll)*bprob
rr = zz*(aprob+bprob)-zz**2*aprob*bprob
rx = rr.derivative(1).at_zero_xy()
ry = rr.derivative(2).at_zero_xy()
lzero = 4*pp**3
qzero = 1-zz*lzero
rzero = 1-zz*lzero*(1+pp**6)
exact(not (rr.at_zero_xy()-(1-qzero*rzero)).reduce_p(),
      "independent full polynomial constant")
exact(not (rx-4*zz*pp**11*qzero).reduce_p(),
      "independently differentiated geometric source")
exact(not (pp**5*qzero*ry+2*(rzero+pp**6*qzero)*rx).reduce_p(),
      "independently differentiated matter source ratio")
exact(not (128*zz*pp**11*qzero-32*rx).reduce_p(),
      "independent exact gain cancellation")
GROUPS["independent_original_report_differentiation"] = {
    "checks": {k: COUNTS[k]-start[k] for k in COUNTS},
    "arithmetic": "Q[p,x,y,z] differentiation, then p^2+p-1 recurrence",
    "root_checker_imported": False,
}

result = {
    "status": "PASS",
    "scope": "new finite coherent injection and complete-tape price identities",
    "assertions": COUNTS,
    "groups": GROUPS,
    "original_full128_replayed": False,
    "golden_gate_factory_proofs_replayed": False,
    "many_copy_degeneracy_theorem_reproved": False,
    "full_D0_price_selected": False,
    "GR_closed": False,
}
path = Path(__file__).with_name("RESULT_PAID_COHERENT_INJECTION.json")
path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
