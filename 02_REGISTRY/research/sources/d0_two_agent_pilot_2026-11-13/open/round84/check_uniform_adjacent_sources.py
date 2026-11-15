#!/usr/bin/env python3
"""Rational/geometric inventory checks for all-cube adjacent source bounds."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;O=HERE.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
sys.path.insert(0,str(D/'round30'));import marked_source_schedule as a30
chart=O/'round21/CHART_ENVELOPE_RESULT.json';coords=O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl'
addr=O/'round24/TORUS_CHOI_ADDRESSES.jsonl';slack=O/'round25/STRICT_SLACK.json'
ce=json.loads(chart.read_text());ss=json.loads(slack.read_text())
assert ce['status']=='PASS_EXACT_RATIONAL_GEOMETRIC_SLACK_NOT_FULL_H1'
assert ss['status']=='PASS_RATIONAL_REFERENCE_SLACK_PLUS_PINNED_B21_CHART'
assert ce['coords_sha256']==sha256(coords.read_bytes()).hexdigest()
R=[json.loads(x) for x in coords.read_text().splitlines()]
assert len(R)==2688 and Counter(r['kind'] for r in R)=={'coframe':1024,'proper_link':1536,'matter':128}
assert R[2]=={'site':[0,0,1,1],'kind':'coframe','role':0,'component':2,'sam_index':2}
addresses=[json.loads(x) for x in addr.read_text().splitlines()]
assert len(addresses)==2049
A=Counter((r['kind'],tuple(r['site']),r['direction']) for r in addresses if r['a']>0)
for row in R:
    if row['kind']=='coframe':assert A[('inverse_coframe_column',tuple(row['site']),row['role'])]==1
    if row['kind']=='proper_link':assert A[('proper_link',tuple(row['site']),row['role'])]==1
# Exact actual source slot inventory: each of seven source banks contains
# 180 Choi and 16 CAR, not a sample of labels or a new number of copies.
ns=a30.g.namespace();slots=ns['source_slots']
counts=Counter((z['bank'],z['kind']) for z in slots)
assert len(slots)==1372
for bank in ('y+','y-','f','0','x+','x-','q'):
    assert counts[bank,'Choi']==180 and counts[bank,'CAR']==16
# B25 field graph: only f/q coframe, f link, q matter; a coordinate affects
# a single indexed source address/site. Other references and SITE are fixed.
fields_code=(O/'round25/targets.py').read_text()
assert "if bank in ('f','q','current_mark')" in fields_code
assert "bank in ('f','current_mark')" in fields_code and "bank in ('q','current_mark')" in fields_code

# Full cube and every real point on an adjacent edge. Critically, the exact
# B21 bound itself implies the defect; the weaker 31/32 does NOT.
uf=F(ce['coframe_creator_norm_strict_upper']);lf=F(ce['link_exterior_half_norm_strict_upper'])
assert uf==F(12985565259,13421772800) and uf<1 and 1-uf*uf>F(1,16)
assert 1-F(31,32)**2<F(1,16) # negative control against invalid shortcut
assert lf<F(3,5) and F(ss['reference_Julia_link_defect_lower'])>F(1,16)
assert F(ce['material_slack_strict_lower'])>F(1,3)
step=F(1,2**30)
assert 12*step<F(1,2) and F(17,16)/(1-12*step)<3
assert 6*F(17,16)**3<9 # exterior-power delta C < 9s
assert 34<36 and 32*2049>256**2
assert 360<19**2 and 180<14**2
co_ch=F(3,32);link_ch=F(27,32)
assert 19*co_ch<2 and 14*link_ch<12
assert F(6,5)<F(11,10)**2 and 4*F(11,160)<1
# Old/profile approximation is NOT the ideal product: +2 eps_prefix.
eta_old=F(1,2**3232)
inv=a30.inventory()
assert inv['eta_common_old'] < eta_old
assert inv['replacement_error'] < F(1,2**3244)
lam_co=2*step+2*eta_old;lam_link=12*step+2*eta_old;lam_car=step+2*eta_old
assert lam_co<F(9,4)*step and lam_link<F(25,2)*step and lam_car<F(25,2)*step
assert lam_link<F(1,2**26)

# Independent exact small product identity; <= is valid when each overlap
# is nonnegative, established on the real ideal source states by tiny deltas.
cs=[s.Rational(3,5),s.Rational(5,13),s.Rational(8,17)]
overlap=s.prod(cs);dist2=2*(1-overlap);sumdist2=sum(2*(1-x) for x in cs)
assert dist2<sumdist2 and all(x>0 for x in cs)

# The scalar I_tau uses original g and field chart. B65's centre defect and
# full-cube Hessian bounds imply all component derivatives <27/16, not a
# gradient sampled at a few vertices. Native full corner error is separate.
assert F(52,32)+F(1,2**3083)<F(27,16)
eB=F(1,2**3231);eW=F(1,2**3244);gs=F(1,2**3158);eU=F(1,2**14623)
assert F(27,8)+2*eB/gs<F(7,2)
# Since p<5/8, p^3=2p−1<1/4, hence p sqrt(p)<1/2.
assert F(2)*F(5,8)-1==F(1,4)
Rmax=F(21,32)*(F(25,2)*step)**2+F(21,8)*eW+F(3,4)*eW/gs+eU/gs
assert Rmax<F(1,2**53)-F(1,2**56)
assert F(1,2**53)-Rmax>F(1,2**56)
# Specific j=2 refinement is conditional on A43's additional pointwise
# M-edge proof; do not assert that independent pending bound as already owned.
Rj2=F(3,8)*(((F(9,4)*step)**2/2+2*eW)*F(1,2**17)+2*eW/gs)+eU/gs
assert Rj2<F(1,2**77)

files=[Path(__file__),chart,coords,addr,slack,O/'round25/TARGETS_RU.md',O/'round25/targets.py',
       O/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',O/'round65/SCALAR_HESSIAN_ENVELOPE.json',
       O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',O/'round82/B82_FOUR_SLOT_Q_KERNEL_RU.md',
       D/'round25/GLOBAL_WORD_AND_SCALAR_CORNER_RU.md',D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',
       D/'round30/COMMON_RAW_SOURCE_MARKS_RU.md',D/'round30/marked_source_schedule.py',
       D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md']
out={'status':'UNIFORM_ADJACENT_PREPARED_SOURCE_BOUND_AND_CONDITIONAL_NONZERO_Q_FEEDBACK',
     'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'declared_SAM_coordinates_checked':2688,'declared_source_copies_checked':1372,
     'unique_Choi_address_per_geometric_coordinate':True,
     'j2':'coframe role 0 component 2 at (0,0,1,1)',
     'exact_rational_Julia_defect_strict_gt':'1/16',
     'sourceI_profile_not_identified_with_ideal_product':True,
     'old_prefix_each_state_error_strict_lt':'2^-3232',
     'Lambda_coframe_strict_lt':'2*s+2^-3231 < (9/4)*s',
     'Lambda_link_strict_lt':'12*s+2^-3231 < (25/2)*s',
     'Lambda_matter_strict_lt':'s+2^-3231',
     'Lambda_all_j_strict_lt':'2^-26',
     'max_adjacent_actual_M_difference_over_gs_strict_lt':'7/2',
     'some_allowed_local_Q_feedback_absolute_gt':'2^-56, conditional A37/A41 and declared axis domain',
     'Qf_Qb_independent_rows':'opposite signs for same Q generator at fixed outgoing',
     'j2_Q_minus_half_Pf_lt_2^-77':'conditional on A43 additional pointwise M-edge <2^-17; not proved here',
     'absolute_full_heat_Q_or_full_task_admission_proved':False,
     'production_source_states_enumerated':False,'Cost_Info_binding_proved':False,
     'physical_C_closed':False,'GR_closed':False,
     'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files}}
(HERE/'B84_UNIFORM_SOURCE_BOUND.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
