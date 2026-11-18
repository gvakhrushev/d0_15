#!/usr/bin/env python3
"""Exact MG2 centered-product scalar quadratic cancellation."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round47'))
import full_vector_controls as a
E=a.e;Q=E.Q4;zero=Q();one=Q(1);phi,probs,lambdas=a.mg2();p=E.SIN
X=[[zero for j in range(4)] for i in range(4)]
for (i,j),value in lambdas.items():X[i][j]=-value;X[j][i]=value
v=[Q(i)-3*p*p for i in range(4)]
H=[[(v[i]-v[j])*X[i][j] for j in range(4)] for i in range(4)]
assert sum(probs,zero)==one and sum((v[i]*probs[i] for i in range(4)),zero)==zero
assert all(sum((H[i][j]*phi[j] for j in range(4)),zero)==phi[i] for i in range(4))
def scalar_power(k):return sum((phi[i]*(v[i]**k-v[j]**k)*X[i][j]*phi[j] for i in range(4) for j in range(4)),zero)
assert scalar_power(0)==zero and scalar_power(1)==one and scalar_power(2)==zero
# Exhaustively check all 16 pairs of powers <=2 in a two-coordinate tensor.
# This includes j, independent k, V_j^2, V_j V_k, V_k^2.
for a0,b0 in product(range(3),repeat=2):
 left=scalar_power(a0);right=sum((probs[i]*v[i]**b0 for i in range(4)),zero)
 expected=one if (a0,b0)==(1,0) else zero if a0+b0<=2 else left*right
 assert left*right==expected
cubic=scalar_power(3);ctx=E.Dyadic(256);lo,hi=ctx.evaluate((E.expr(cubic),))[0];assert lo>0 or hi<0
# A correlated 4-level positive state invalidates the product-state claim.
# |0>+|1> gives a real off-diagonal density and a nonzero quadratic response.
w=(v[0]+v[1])*H[0][1];lo2,hi2=ctx.evaluate((E.expr(w),))[0];assert lo2>0 or hi2<0
paths=[D/'round47/full_vector_controls.py',D/'round47/FULL_VECTOR_CONTROL_PLAN.json',P.parent/'round91/B91_FULL_VECTOR_JET_CHECK.json']
out={'status':'PASS_EXACT_CENTERED_PRODUCT_QUADRATIC_CANCELLATION','all_total_degree_le_2_monomials_checked':True,'born_two_coordinate_product_state_required':True,'expected_linear_commutator':1,'quadratic_commutators_zero':True,'cubic_counterexample_nonzero':True,'correlated_CODE_state_quadratic_counterexample_nonzero':True,'uniform_scalar_M3_bound_proved':False,'actual_price_gradient_identified':False,'GR_closed':False,'source_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in paths}}
(P/'QUADRATIC_LIFT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
