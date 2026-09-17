#!/usr/bin/env python3
"""Exact, independently computed three-reference test of the coupling axis.

Checks the actual fourteen-operation forward circuit for an arbitrary real
unit-quaternion axis, using polynomial reduction instead of sampled inputs.
"""
from pathlib import Path
from cert_runtime import output_path
import hashlib
import json
import sympy as S

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
paths=[
    "03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean",
    "03_FORMALIZATION/D0/Representation/CouplingAxisReadout.lean",
    "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
]
texts=[(ROOT/p).read_text() for p in paths]


def matrix(text, marker):
    body=text.split(marker,1)[1].split("!![",1)[1].split("]",1)[0]
    return S.Matrix([[S.sympify(v) for v in row.split(",")] for row in body.split(";")])


a,p,x,y,z=S.symbols("a p x y z")
unit=S.groebner([x*x+y*y+z*z-1],x,y,z)
full=S.groebner([a*a-p,p*p+p-1,x*x+y*y+z*z-1],a,p,x,y,z)


def reduce(v):
    return full.reduce(S.expand(v))[1]


def eq(A,B):
    return all(reduce(v)==0 for v in A-B)


checks=[]


def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)


B=matrix(texts[1],"def axis")
source=matrix(texts[0],"def left")
qa,qb,qc,qd=S.symbols("a b c d")
check("general axis agrees with source formula",B==source.subs({qa:0,qb:x,qc:y,qd:z},simultaneous=True))
axes=[B.subs(dict(zip((x,y,z),v))) for v in ((1,0,0),(0,1,0),(0,0,1))]
check("arbitrary unit axis preserves norm",eq(B.T*B,S.eye(4)))
check("arbitrary unit axis fourth power",eq(B**4,S.eye(4)))
golden=matrix(texts[2],"def gate")
split=S.kronecker_product(golden,S.eye(4))
local=S.diag(S.eye(4),B)
start=S.Matrix.vstack(S.eye(4),S.zeros(4))
port1=S.diag(S.zeros(4),S.eye(4))
weights=[]
for k,ref in enumerate(axes):
    C=ref*B*ref*B
    coordinate=(x,y,z)[k]
    weight=4*p**3*(1-coordinate**2)
    weights.append(weight)
    check(f"reference {k}: symmetric part",eq(C.T+C,(4*coordinate**2-2)*S.eye(4)))
    check(f"reference {k}: orthogonal comparison",eq(C.T*C,S.eye(4)))
    check(f"reference {k}: quadratic difference",eq((C-S.eye(4)).T*(C-S.eye(4)),4*(1-coordinate**2)*S.eye(4)))
    common=S.diag(ref,ref)
    circuit=[split,local,common]+[local]*3+[common]*3+[local]*2+[split]+[local]*2
    check(f"reference {k}: same fourteen forward operations",len(circuit)==14)
    F=start
    for stage,gate in enumerate(circuit,1):
        F=(gate*F).applyfunc(reduce)
        check(f"reference {k}: arbitrary-input norm at stage {stage}",eq(F.T*F,S.eye(4)))
    check(f"reference {k}: actual circuit second-port weight",eq(F.T*port1*F,weight*S.eye(4)))
    check(f"reference {k}: component reconstructed",S.simplify(1-weight/(4*p**3)-coordinate**2)==0)

check("three separate experiments obey sum rule",reduce(sum(weights)-8*p**3)==0)
check("third response predicted by first two",reduce(weights[2]-(8*p**3-weights[0]-weights[1]))==0)
check("sum agrees with independent splitter calibration",reduce(sum(weights)-8*p*p*(1-p*p))==0)
check("transverse squared component from i response",reduce(weights[0]-4*p**3*(y*y+z*z))==0)
check("overall sign is invisible to this protocol",all(S.expand(w-w.subs({x:-x,y:-y,z:-z},simultaneous=True))==0 for w in weights))
check("relative signs also remain invisible",all(S.expand(w-w.subs({y:-y}))==0 for w in weights))

# Two candidates already present in the original Q8, no new continuous constant.
wi=[S.expand(w.subs({x:1,y:0,z:0})) for w in weights]
wk=[S.expand(w.subs({x:0,y:0,z:1})) for w in weights]
check("original j probe cannot distinguish i and k",wi[1]==wk[1])
check("fixed i probe distinguishes them",wi[0]!=wk[0])

# An explicit rational mixed axis satisfies all matrix assumptions but differs
# on the additional probe; it is not asserted to be a source Q8 group element.
mixed={x:S.Rational(3,5),y:0,z:S.Rational(4,5)}
check("rational alternative has unit norm",sum(v*v for v in mixed.values())==1)
wm=[S.simplify(w.subs(mixed)/(4*p**3)) for w in weights]
check("mixed axis signature",wm==[S.Rational(16,25),1,S.Rational(9,25)])
check("non-unit axis violates norm",B.subs({x:1,y:1,z:0}).T*B.subs({x:1,y:1,z:0})!=S.eye(4))

for k,axis_vector in enumerate(((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))):
    profile=[S.simplify(w.subs(dict(zip((x,y,z),axis_vector)))/(4*p**3)) for w in weights]
    check(f"source quarter-turn {k}: same profile up to reference permutation",sorted(profile)==[0,1,1])
terminal=[S.eye(4),-S.eye(4)]+[sgn*ax for ax in axes for sgn in (1,-1)]
check("mixed quaternion is not an existing terminal action",all(B.subs(mixed)!=member for member in terminal))

# Whole-apparatus relabelling transports the REFERENCES, not just the unknown axis.
T=matrix(texts[1],"def relabelFrame")
T8=S.diag(T,T)
check("simultaneous relabelling preserves spin norm",T.T*T==S.eye(4))
check("simultaneous relabelling swaps i for k",T*axes[0]*T.T==axes[2])
check("simultaneous relabelling also changes j to minus j",T*axes[1]*T.T==-axes[1])
check("golden mixer unchanged under spin relabelling",eq(T8*split,split*T8))
check("port readout unchanged under spin relabelling",T8.T*port1*T8==port1)
for k,ref in enumerate(axes):
    old_C=ref*axes[0]*ref*axes[0]
    transported_ref=T*ref*T.T
    new_C=transported_ref*axes[2]*transported_ref*axes[2]
    check(f"whole comparison {k} is conjugate when references move",T*old_C*T.T==new_C)

result={
    "status":"PASS", "checks_passed":len(checks), "checks":checks,
    "scope":"Exact identification test in the pure unit-quaternion coupling class. Source Q8 alternatives are included; arbitrary real axes are not claimed M1-forced.",
    "source_sha256":{path:hashlib.sha256(text.encode()).hexdigest() for path,text in zip(paths,texts)},
    "responses":[str(w) for w in weights],
    "sum_rule":"w_i+w_j+w_k = 8*phi^(-3)",
    "source_i_signature_in_units_of_gamma":[0,1,1],
    "source_k_signature_in_units_of_gamma":[1,1,0],
    "mixed_signature_in_units_of_gamma":[str(v) for v in wm],
    "fixed_terminal_unlabelled_profile":[0,1,1],
    "unresolved":"Relative signs and physical admissibility of the coupling; this is not full-state or full-theory equivalence.",
}
output_path(__file__, "axis_verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in ("checks","source_sha256")},ensure_ascii=False,indent=2))
