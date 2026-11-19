"""Checks for the exact scalar port/adaptive stopped extension.

The physical stopping task and actual primitive ledger remain hypotheses.
"""
import json
import math
import time
import argparse
from pathlib import Path
import sympy as sp

started=time.perf_counter()
t,c,s=sp.symbols("t c s", real=True)
f0=1-2*t*t
f1=2*t*(1-t*t)
alpha0=c*f0-s*f1
alpha1=s*f0+c*f1
beta0=2*s*t*t
beta1=-2*c*t*t
q0=sp.expand(alpha0**2+beta0**2*(1-t*t))
q1=sp.expand(alpha1**2+beta1**2*(1-t*t))
assert sp.factor(q0+q1)==c*c+s*s
assert sp.simplify(sp.diff(q1,t).subs(t,0)-4*c*s)==0
assert sp.simplify((beta0**2+beta1**2)*(1-t*t)-4*t**4*(1-t*t)*(c*c+s*s))==0

p=(sp.sqrt(5)-1)/2
cg=p**3
sg=2*p*sp.sqrt(p)
assert sp.simplify(cg*cg+sg*sg-1)==0
q2=4*p**3
qp=8*p**sp.Rational(9,2)
assert sp.simplify(qp/q2**2-1/(2*p**sp.Rational(3,2)))==0
assert sp.simplify(q1.subs({c:cg,s:sg,t:0})-q2)==0

pn=float(p); ell=math.log(1/pn);theta=math.asin(pn)
def q(k,x=0.):
    co=math.cos(k*theta);si=math.sin(k*theta)
    return (si*(1-2*x*x)+2*co*x*(1-x*x))**2+4*co*co*x**4*(1-x*x)
def divergence(qq):
    return sum(a*math.log(a/b)/ell for a,b in ((1-qq,pn),(qq,pn*pn)) if a>0)
def a(k,T,x=0.):
    return T+k+divergence(q(k,x))
def ratio(k,T,x=0.):
    return a(k,T,x)/q(k,x)

def schedule(prefix,tail,T):
    # prefix choices are made after successive failures; thereafter repeat tail.
    survival=1.
    summed_cost=0.
    weighted_ratio=0.
    zero_success_cost=0.
    halt_mass=0.
    for k in prefix:
        qq=q(k)
        aa=a(k,T)
        summed_cost+=survival*aa
        if qq>1e-15:
            weighted_ratio+=survival*qq*(aa/qq)
            halt_mass+=survival*qq
        else:
            zero_success_cost+=survival*aa
        survival*=1-qq
    # Infinite fixed tail: E cost=survival*ratio; eventual halt mass=survival.
    summed_cost+=survival*ratio(tail,T)
    weighted_ratio+=survival*ratio(tail,T)
    halt_mass+=survival
    assert abs(halt_mass-1)<2e-14
    assert abs(summed_cost-weighted_ratio-zero_success_cost)<2e-12
    # Independently evaluate the Bellman recursion, including its exact tail.
    bellman=ratio(tail,T)
    for k in reversed(prefix):
        bellman=a(k,T)+(1-q(k))*bellman
    assert abs(bellman-summed_cost)<2e-12
    return dict(prefix=prefix,tail=tail,value=summed_cost,
                fixed2_value=ratio(2,T),excess=summed_cost-ratio(2,T),
                eventual_halt_mass=halt_mass)

controls=[]
for T in (5,30,50):
    for pre,tail in (([],2),([1],2),([0],2),([2,2,3],2),([2,1,7],2),([1,3,2],1)):
        v=schedule(pre,tail,T)
        assert v["excess"]>-2e-12
        if pre or tail!=2:
            assert v["excess"]>0
        v["T0"]=T
        controls.append(v)

# No uniform policy gap: one different action after m failures approaches zero.
late=[schedule([2]*m+[1],2,5)["excess"] for m in range(5)]
assert all(late[j+1]<late[j] for j in range(len(late)-1))

# Independent derivative of the scalar stopped objective with no target factor error.
eps=1e-6
numeric=(ratio(2,5,eps)-ratio(2,5,-eps))/(2*eps)
target=-(5-3)/(2*pn**1.5)
assert abs(numeric-target)<1e-7
result=dict(
    baseline="f22c1864",
    exact_symbolic_scalar_effects=True,
    adaptive_schedule_controls=controls,
    late_deviation_excesses=late,
    T0_5_source=dict(analytic=target,central_difference=numeric),
    runtime_seconds=time.perf_counter()-started,
    scope="Fixed stopped task, scalar fresh-work interface, unit G price, "
          "T0 in [5,50], complete fresh pointer Info, deterministic policies, "
          "finite expected actual cost. All-policy and value-envelope proof is analytical.",
)
parser=argparse.ArgumentParser()
parser.add_argument("--output",type=Path,help="Optional explicit JSON output path")
args=parser.parse_args()
if args.output is not None:
    args.output.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ("exact_symbolic_scalar_effects",
    "late_deviation_excesses","T0_5_source","runtime_seconds")},indent=2))
