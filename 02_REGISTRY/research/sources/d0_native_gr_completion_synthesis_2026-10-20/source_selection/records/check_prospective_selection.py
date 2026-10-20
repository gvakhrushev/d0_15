"""Conditional prospective-selection thresholds; no native task is asserted."""
import json
import argparse
import math
import time
from pathlib import Path

import sympy as sp

started = time.perf_counter()
p = (sp.sqrt(5)-1)/2
phi = 1/p
q1, q2 = p**2, 4*p**3
L = sp.Symbol("L", real=True)
D2 = q2*(4+L)-5
def eq(a,b):
    assert sp.simplify(sp.expand(a-b)) == 0, (a,b)

eq(D2, -5*p**6+q2*(L-1))
eq(p+p**2*phi**4, 2*phi)
eq(p+p**2*phi**5, 3*phi)
eq(p+p**2*phi**6, 4*phi+1)
eq(phi**8, 21*phi+13)
eq((p**2*4*phi**4)/(p+p**2*4*phi**4), q2)
eq(5*(q2-q1)-(1+D2), 4-5*p**2+q2*(1-L))
assert sp.simplify(p**2-sp.Rational(3,8)) > 0
assert sp.simplify(7-11*p) > 0
assert sp.simplify(q2-2*q1) > 0

pn = float(p); ell = math.log(1/pn)
q1n=float(q1);q2n=float(q2)
Ln=math.log(4)/ell; An=4+Ln; Dn=q2n*An-5
delta_star=(1+Dn)/(q2n-q1n)
theta=math.atan2(pn,math.sqrt(pn))
def divergence(q):
    return sum(x*math.log(x/mu)/ell
               for x,mu in ((1-q,pn),(q,pn**2)) if x>0)
def ptr(k,delta):
    q=math.sin(k*theta)**2
    # v0=delta, v1=0 is merely a nonnegative numerical example of
    # the specified conditional contract, not a supplied physical task.
    return k+divergence(q)+delta*(1-q)
def coh(k,delta):
    q=math.sin(k*theta)**2
    return k+1+q+delta*(1-q)
def g(delta):
    Z=pn+pn**2*(1/pn)**delta
    return 1-math.log(Z)/ell-Dn+delta*q2n

assert 4<delta_star<5
assert 6<An<7
assert g(4)>.5
checks=[]
for delta in (5,6):
    prices=[ptr(k,delta) for k in range(9)]
    assert min(range(len(prices)),key=prices.__getitem__)==2
    assert g(delta)>0
    assert An-delta>0
    for k in range(3,len(prices)):
        assert prices[k]-prices[2] >= g(delta)-1e-12
    checks.append(dict(delta=delta, all_k_ge_3_gap_lower_bound=g(delta),
                       source_factor_relative_to_kappa=An-delta,
                       prices_k0_through_k8=prices))
coh_prices=[coh(k,4) for k in range(9)]
assert min(range(len(coh_prices)),key=coh_prices.__getitem__)==2
coh_gap=1-3*float(p**6)
for k in range(3,len(coh_prices)):
    assert coh_prices[k]-coh_prices[2]>=coh_gap-1e-12

result=dict(
    baseline="4867b6d4",
    primitive_G_ticks=1,
    q1=q1n,q2=q2n,D2=Dn,
    terminal_gaps=dict(coherent_20=2+q2n,coherent_21=1+q2n-q1n,
                       pointer_20=1+Dn,pointer_21=1+Dn),
    sharp_pointer_positive_source_window=dict(lower_open=delta_star,upper_open=An,
                                              integer_differences=[5,6]),
    pointer_controls=checks,
    coherent_delta4=dict(source_factor_relative_to_kappa=-3,
                         all_k_ge_3_gap_lower_bound=coh_gap,
                         prices_k0_through_k8=coh_prices),
    full_window_all_k_ge_3_margin_strictly_greater_than=.5,
    runtime_seconds=time.perf_counter()-started,
    scope="Conditional on actual same bit-dependent field-independent continuation "
          "prices. No native compulsory task or global comparison beyond G^k asserted.",
)
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, help="Optional new receipt; default replay is read-only")
args = parser.parse_args()
if args.output:
    if args.output.resolve() == Path(__file__).resolve().parent/"prospective_results.json":
        raise SystemExit("Refusing to overwrite the saved research receipt")
    args.output.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
