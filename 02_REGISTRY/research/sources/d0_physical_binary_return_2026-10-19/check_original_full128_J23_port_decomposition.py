#!/usr/bin/env python3
"""Exact original L=4 full128 J23 Shannon source split; pinned parent source data.

Consumes 02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/
COMPLETE_SHANNON_SOURCE.json from original #334. No 16x16x128 matrix replay.
"""
import json
import sympy as s
from pathlib import Path

HERE=Path(__file__).resolve().parent
src=HERE.parent/"d0_native_full128_order_readout_2026-10-19"/"COMPLETE_SHANNON_SOURCE.json"
j=json.loads(src.read_text())
assert j["status"]=="PASS_SCOPED_COMPLETE_FULL128_SHANNON_FIRST_SOURCE"
assert j["checks"]==29
assert j["probability_law"]["positive_outcomes"]==42
assert j["probability_law"]["zero_outcomes"]==86
v=s.sqrt(5);p=(v-1)/2;h=s.Rational(1,4)
eps=p**2*h**2/64;ell=s.log(1/p)
groups=[]
for entry in j["probability_law"]["groups"]:
    q=s.sympify(entry["probability"],locals={"sqrt":s.sqrt})
    dq=s.sympify(entry["source_sum"],locals={"sqrt":s.sqrt})
    groups.append((entry["multiplicity"],q,dq))
assert sum(k for k,q,dq in groups)==128
assert s.simplify(sum(k*q for k,q,dq in groups)-1)==0
assert s.simplify(sum(dq for k,q,dq in groups))==0
assert all(s.N(q)>0 for k,q,dq in groups if q!=0)

lam=s.Rational(288,25)
dlambda_tr=-s.Rational(144,25) # Tr[d Delta]/16, NOT scalar dDelta at J23.
q00,dq00=groups[0][1:]
assert s.simplify(q00-(1-2*p**2*h**2*lam/256)**2)==0
assert s.simplify(dq00+2*(1-2*p**2*h**2*lam/256)
                  *(p**2*h**2/128)*dlambda_tr)==0
dP_port1=s.sympify(j["known_original_golden_port_code"]["first_source_exact"],
                    locals={"sqrt":s.sqrt})
assert s.simplify(dP_port1-p*eps*dlambda_tr)==0

P_label=s.expand(eps*lam*(1-h**2*lam/256))
dP_label=s.simplify(eps*dlambda_tr*(1-h**2*lam/128))
assert s.simplify(P_label-(s.Rational(86157,5120000)
                          -28719*v/s.Integer(5120000)))==0
assert s.simplify(dP_label-(-s.Rational(42957,5120000)
                           +14319*v/s.Integer(5120000)))==0

# Original conditionals: q_port=(p²,p), original code reference=(p,p²).
H_port=s.simplify(2*p*p+p)
K_port=s.simplify(p-p*p)
assert s.simplify(H_port-(2-p))==0
assert s.simplify(K_port-p**3)==0

H_full=-sum(dq*s.log(q)/ell for k,q,dq in groups if q!=0)
H_hidden=s.simplify(H_port*dP_label)
H_reduced=s.simplify(H_full-H_hidden)
K_hidden=s.simplify(K_port*dP_label)
dP_port1_nonblank=s.simplify(p*dP_label)
dP_port1_blank=s.simplify(dP_port1-dP_port1_nonblank)
assert s.simplify(dP_port1_blank-p*eps*(h**2*lam/128)*dlambda_tr)==0

want=s.sympify(j["complete_pointer_shannon"]["first_source_numeric_70_digits"])
assert abs(float(s.N(H_full-want,30)))<1e-28
assert abs(float(s.N(H_reduced,35))
           -(-0.02859425100765720895831598578))<1e-13
assert abs(float(s.N(K_hidden,35))-(-0.000504352900214344))<1e-13

print("PASS: pinned original full128 42 positive / 86 zero-outcome first jets")
print("PASS: exact blank and original port1 pin lambda=288/25, Tr(dDelta)/16=-144/25")
print("PASS: nonblank effect and field source checked in Q(sqrt5)")
print(" D P_nonblank          =", dP_label)
print(" D H_full128           =", s.N(H_full,24))
print(" D H_reduced_labels    =", s.N(H_reduced,24))
print(" D H_hidden_port       =", s.N(H_hidden,24))
print(" D KL_hidden_port      =", s.N(K_hidden,24))
print(" D special blank port1 =", s.N(dP_port1_blank,24))
print("SCOPE: one-round J23 first jet; no arbitrary multi-round field or GR claim")
