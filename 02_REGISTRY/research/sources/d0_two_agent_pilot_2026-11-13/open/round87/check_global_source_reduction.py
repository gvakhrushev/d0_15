#!/usr/bin/env python3
"""Independent B87 global source radius and dimension-free Q relation."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json,sys
import sympy as sp
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round30'));import marked_source_schedule as a30
coords=[json.loads(x) for x in (O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
C=Counter((tuple(r['site']),r['role']) for r in coords if r['kind']=='coframe')
L=Counter((tuple(r['site']),r['role']) for r in coords if r['kind']=='proper_link')
M=Counter(tuple(r['site']) for r in coords if r['kind']=='matter')
assert (len(C),set(C.values()),len(L),set(L.values()),len(M),set(M.values()))==(256,{4},256,{6},64,{2})
addresses=[json.loads(x) for x in (O/'round24/TORUS_CHOI_ADDRESSES.jsonl').read_text().splitlines()]
AC=Counter((r['kind'],tuple(r['site']),r['direction']) for r in addresses if r['a']>0)
assert all(AC['inverse_coframe_column',x,r]==1 for x,r in C)
assert all(AC['proper_link',x,r]==1 for x,r in L)
counts=Counter((x['bank'],x['kind']) for x in a30.g.namespace()['source_slots'])
assert sum(counts[b,'Choi'] for b in ('f','q'))==360 and counts['f','Choi']==180 and counts['q','CAR']==16
geo=json.loads((O/'round21/CHART_ENVELOPE_RESULT.json').read_text());u=F(geo['coframe_creator_norm_strict_upper']);slack=F(geo['material_slack_strict_lower'])
assert 1-u*u>F(1,16) and slack>F(1,3)
s=F(1,2**30);ep=F(1,2**3232);eB=F(1,2**3231);eW=F(1,2**3244);eU=F(1,2**14623);gs=F(1,2**3158)
inv=a30.inventory();assert inv['eta_common_old']<ep and inv['replacement_error']<eW
assert F(17,16)/(1-12*s)<3 and 6*F(17,16)**3<9
# Opposite vertices: 4 coframe components -> ||delta C||<=2s; six
# link generators -> ||delta C||<54s. Orthogonal Choi addresses.
co=F(3,16);link=F(81,16);assert F(24*2,256)==co and F(24*54,256)==link
co2=360*256*co**2;link2=180*256*link**2
# 64 sites, two varying material components, site mass 1/256, 16 copies.
# ||D m||^2 <= (1-p)/L < 6/5 < (11/10)^2.
assert F(6,5)<F(11,10)**2
car2=16*F(64,256)*2*F(11,10)**2
ideal=co2+link2+car2
assert co2==3240 and link2==1180980 and car2<F(20)
assert ideal<1089**2 and 1089*s+2*ep<1100*s
delta=1100*s
assert (delta+2*ep)<1  # source overlap positivity for tensor estimate
h=json.loads((O/'round65/SCALAR_HESSIAN_ENVELOPE.json').read_text())
assert h['I_tau_Hessian_raw_chart_norm_lt']=='2^25' and h['chosen_current_reference_full_covector_defect_lt']=='2^-3083'
tau=104*F(1,2**3083)+(2**25)*2704*s+eB/gs
assert tau<85
err=F(3,4)*(tau*(2*delta**2+2*eW)+eW/gs)+eU/gs
assert err<F(1,2**32)
# A44's arithmetic uses a looser 16*(11/10)^2 CAR bound; check independently.
a44ideal=co2+link2+16*F(11,10)**2
assert ideal<a44ideal<1089**2
sys.path.insert(0,str(D/'round44'));import joint_source_reduction as a44
b=a44.bounds();assert b['global_ideal_source_distance_squared_upper']==a44ideal*s*s
assert b['global_old_profile_source_distance_upper']==delta
assert b['centred_actual_M_spread_over_gs_upper']==tau
assert b['all_SAM_Qb_minus_half_Pf_dual_operator_norm_upper']==err
# Verify the exact cancellation, with a symbolic skew Y and symmetric S.
# V=diag prepared states, J=common reference; not a production simulation.
R=sp.Rational;I=sp.eye;S=sp.Matrix([[sp.Symbol('a',real=True),sp.Symbol('b',real=True)],[sp.Symbol('b',real=True),sp.Symbol('d',real=True)]])
vecs=[sp.Matrix([1,0]),sp.Matrix([R(3,5),R(4,5)]),sp.Matrix([R(5,13),R(12,13)])]
def bank(col):
 out=sp.zeros(6,3)
 for i,v in enumerate(col):out[2*i:2*i+2,i]=v
 return out
V=bank(vecs);J=bank([vecs[0]]*3);DD=V-J
x,y,z=sp.symbols('x y z',real=True);Y=sp.Matrix([[0,-x,-y],[x,0,-z],[y,z,0]])
assert V.T*V==I(3) and J.T*J==I(3)
phi=V.T*sp.kronecker_product(Y,S)*V;diag=V.T*sp.kronecker_product(I(3),S)*V
err0=phi-(diag*Y+Y*diag)/2
A=DD.T*sp.kronecker_product(I(3),S)*DD
rhs=DD.T*sp.kronecker_product(Y,S)*DD-(A*Y+Y*A)/2
assert sp.simplify(err0-rhs)==sp.zeros(3,3) and sp.simplify(err0.T+err0)==sp.zeros(3,3)
# Non-selfadjoint middle is a negative control: it must be handled by eW,
# not silently replaced by the reflected ideal identity.
Sn=sp.Matrix([[1,1],[0,-1]])
phin=V.T*sp.kronecker_product(Y,Sn)*V;dn=V.T*sp.kronecker_product(I(3),Sn)*V
en=phin-(dn*Y+Y*dn)/2
An=DD.T*sp.kronecker_product(I(3),Sn)*DD
assert sp.simplify(en-(DD.T*sp.kronecker_product(Y,Sn)*DD-(An*Y+Y*An)/2))!=sp.zeros(3,3)
# Exact cancellation of M Y M for any skew Y and any real vector.
m0,m1,m2,c0,c1,c2=sp.symbols('m0 m1 m2 c0 c1 c2',real=True)
MM=sp.diag(m0,m1,m2);chi=sp.Matrix([c0,c1,c2]);assert sp.simplify((chi.T*MM*Y*MM*chi)[0])==0
files=[Path(__file__),D/'round44/joint_source_reduction.py',D/'round44/JOINT_SOURCE_REDUCTION_PLAN.json',D/'round44/check_joint_source_reduction.py',D/'round44/JOINT_SOURCE_REDUCTION_CHECK.json',D/'round30/marked_source_schedule.py',
 O/'round21/CHART_ENVELOPE_RESULT.json',O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',
 O/'round24/TORUS_CHOI_ADDRESSES.jsonl',O/'round25/targets.py',O/'round65/SCALAR_HESSIAN_ENVELOPE.json',
 O/'round82/B82_FOUR_SLOT_Q_KERNEL_RU.md',O/'round84/B84_UNIFORM_ADJACENT_SOURCE_RU.md',
 O/'round86/B86_ORIGINAL_MARK_ADMISSION_RU.md']
out={'status':'PASS_CONDITIONAL_ALL_SAM_SKEW_FEEDBACK_REDUCTION',
 'global_label_coframe_addresses':256,'global_label_link_addresses':256,'global_label_matter_sites':64,
 'coframe_distance_squared_coefficient':str(co2),'link_distance_squared_coefficient':str(link2),
 'matter_distance_squared_coefficient_strict_lt':str(car2),'global_source_distance_strict_lt':'1100*s',
 'centre_spread_over_gs_strict_lt':'85','all_skew_Qb_minus_half_Pf_strict_lt':'2^-32',
 'formula_tested_symbolically_with_selfadjoint_middle':True,'non_selfadjoint_middle_negative_control':True,
 'runtime_scope':'analytic normalized feedback; every real SAM skew of operator norm <=1',
 'all_such_directions_paid_and_admitted':False,'full_heat_and_joint_stationarity_proved':False,
 'full_original_mark_Fn_admission':False,'GR_closed':False,
 'source_sha256':{str(f.resolve()):sha256(f.read_bytes()).hexdigest() for f in files}}
Path(__file__).with_name('B87_GLOBAL_SOURCE_REDUCTION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
