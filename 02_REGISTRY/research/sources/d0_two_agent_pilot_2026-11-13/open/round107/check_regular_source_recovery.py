#!/usr/bin/env python3
"""Uniform off-centre four-row recovery on the frozen A54/B105 family.

Exact rational error composition, geometry/identity fixtures and SHA checks.
Consumes, rather than independently reproves, B65/B91/B95/B97/A50/A54/B106.
No production-sized path sum, native word or physical admission is claimed.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from unittest.mock import patch
import json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(O/'round105')); import regular_paid_family as b105
sys.path.insert(0,str(D/'round54')); import regular_global_source as a54
sys.path.insert(0,str(D/'round50')); import independent_price_rows as a50
import check_independent_price_rows as fixtures

def read(path):return json.loads(Path(path).read_text())
def digest(path):return sha256(Path(path).read_bytes()).hexdigest()
def verify_receipt(path):
    data=read(path)
    for name,expected in data.get('source_sha256',{}).items():
        assert digest(name)==expected,(str(path),name)
    return data

hess=verify_receipt(O/'round65/SCALAR_HESSIAN_ENVELOPE.json')
assert hess['status']=='PASS_EXPLICIT_CONSERVATIVE_SCALAR_HESSIAN_ENVELOPE'
assert hess['I_tau_Hessian_raw_chart_norm_lt']=='2^25'
assert hess['chosen_current_reference_full_covector_defect_lt']=='2^-3083'
third=verify_receipt(O/'round97/SCALAR_THIRD_DERIVATIVE_CHECK.json')
assert third['I_tau_third_derivative_norm_lt']=='2^31'
weight=verify_receipt(O/'round97/FIXED_POST_WEIGHT_CHECK.json')
assert weight['status']=='PASS_A49_BORN_PRODUCT_FIXED_POST_WEIGHTED_SCALAR_SOURCE'
quad=verify_receipt(O/'round95/QUADRATIC_LIFT_CHECK.json')
assert quad['status']=='PASS_EXACT_CENTERED_PRODUCT_QUADRATIC_CANCELLATION'
old_plan=verify_receipt(D/'round50/INDEPENDENT_PRICE_ROWS_PLAN.json')
assert old_plan['status']=='BOUNDED_FOUR_INDEPENDENT_MG2_AXIS_PRICE_ROWS_ON_A49'
for f in ('REGULAR_GLOBAL_SOURCE_PLAN.json','REGULAR_GLOBAL_SOURCE_CHECK.json'):
    verify_receipt(D/'round54'/f)
assert read(O/'round105/B105_REGULAR_PAID_CHECK.json')['status']=='PASS_B105_FIELD_BOUND_ACTUAL_POST_CONDITIONAL'
assert read(O/'round106/B106_A54_AUDIT_CHECK.json')['status'].startswith('PASS_A54_INTEGRATION_CONDITIONAL')
for receipt in (O/'round105/B105_REGULAR_PAID_CHECK.json',O/'round106/B106_A54_AUDIT_CHECK.json'):
    for name,expected in read(receipt)['input_sha256'].items():assert digest(name)==expected,name

# Actual A54 retains A48's non-SOURCE middle, binding, compiler and cuts.
# Explicitly check affine report interiors and helper support through A50's
# geometry routine, then exercise A54 dispatch on every middle stage/depth.
assert a54.namespace is b105.paid.source.namespace
assert a54.compiler is b105.paid.source.compiler
assert a54.physical_wire is b105.paid.source.physical_wire
support=a50.middle_support();assert support['actual_S_is_CODE_disjoint']
assert not support['actual_S_selfadjoint_or_return_equals_forward_inverse_assumed']
stages=a54.schedule();cut=stages.index({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0})
middle=stages[cut+1:]
assert Counter(z['kind'] for z in middle)==Counter(RAW_RESOURCE_FRAME=1,REPORT=8,PORT_ZERO=1,SC6=1)
calls=[]
def fake_stage(stage,depth):
    calls.append((stage,depth));yield ('middle',stage,depth)
source=a54.GlobalSource(a54.t.FieldCentre())
with patch.object(a54.previous,'stage_blocks',fake_stage):
    for stage in middle:
        for depth in (0,1,2):assert list(source.stage_blocks(stage,depth))==[('middle',stage,depth)]
assert len(calls)==3*len(middle)
assert tuple(b105.paid.CUTS)==('Qf_dagger_after_common_RAW_mark','Qb_before_return_bank')

# Exact field binding and recalculated length/heat, using the new A54 core.
up=a54.upper_inventory_and_error(); field=a54.t.FieldCentre()
fam=b105.RegularPaidFamily(a54,field,up['W_G_CX_upper']);cfg=fam.cfg
assert fam.actual_core_target().factory.__self__ is fam.source
assert cfg['Nbase'].bit_length()==30833 and cfg['K']==175604
assert cfg['Nbase']!=b105.paid.production_configuration()['Nbase']
assert fam.bounds()['post_corner_lower']>F(2,3)
assert 2688<52**2 and 4*2688<104**2 and 9*2688<156**2
sigma,t,gs,z=(F(1,1<<k) for k in (80,1700,3208,20))
a0=F(1,1<<3083); gradient=a0+F((1<<25)*52,1<<32)
assert gradient<F(1,2)
eW=up['replacement_error'];eM=up['full_canonical_compressed_error']
ep=up['full_SOURCE_DATA_fibre_prefix_error'];eU=cfg['post_error']
assert up['source_error']<=ep<F(1,1<<3423)
assert eM<F(1,1<<3421) and eW<F(1,1<<15800) and eU<F(1,1<<9247)
delta=156*1748*sigma+2*ep
assert delta<F(1,1<<61) and delta>F(1,1<<62)
tau=2*gradient*104+(1<<25)*sigma*104**2+eM/gs
assert tau<85
kernel=F(3,4)*(tau*(2*delta**2+2*eW)+eW/gs)
assert kernel<F(1,1<<116)
post=eU/gs;assert post<F(1,1<<6039)

# Same A50 finite reader estimates, with the *new* exact Nbase/K; no old
# heat, old clock length or small central gradient is substituted.
ctrl=b105.paid.control.control_plan()['control_vs_exp_tX_error']
eP=F(int(ctrl['numerator_hex'],16),int(ctrl['denominator_hex'],16))
gamma0=F(8,3)*z*gs
heat=F(6*cfg['Nbase'],359)/(t*gamma0)*F(1,1<<(cfg['K']//4))
assert heat*(1<<cfg['dimension_debt'])==fam.bounds()['heat_full_skew_dual_error']
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
taylor=t*t*bracket/(16*gs);control=2*eP/(t*gs)
assert heat<F(1,1<<8139) and taylor<F(1,1<<192) and control<F(1,1<<190)
finite=heat+taylor+control
scalar=F(1<<31)*sigma**2*104**3/3
gupper=F(1,1<<3061)
weight_error=F(3,2)*gupper*2*(1<<15)*3*F(3,2)*(1<<20)
corner=F(3,2)*eM/gs
assert scalar<F(1,1<<109) and weight_error<F(1,1<<3021) and corner<F(1,1<<212)
reduced=scalar+weight_error+corner
pf=reduced+post+finite
q=reduced/2+kernel+post+finite
pb=post+finite
joint2=2688*(pf**2+2*q**2+pb**2)
assert pf<F(1,1<<108) and q<F(1,1<<108) and pb<F(1,1<<189)
assert joint2<F(1,1<<204)
relation=kernel+F(3,2)*post+F(3,2)*finite
assert relation<F(1,1<<115)

# Show B95's exact quadratic cancellation survives nonzero field centre:
# the Y^2 constant drops, the linear response is 2Y, and centred quadratic
# expectation vanishes.  All numbers below are exact Q(sqrt(p)) elements.
sys.path.insert(0,str(D/'round47'));import full_vector_controls as ctl
algebra=ctl.e; Q=algebra.Q4
phi,prob,coeff=ctl.mg2();p=algebra.SIN;v=[Q(i)-3*p*p for i in range(4)]
X=[[Q() for _ in range(4)] for _ in range(4)]
for (i,j),value in coeff.items():X[i][j]=-value;X[j][i]=value
Y=Q(F(7,31)); ss=Q(F(1,1<<80))
comm=lambda vals:sum((phi[i]*(vals[i]-vals[j])*X[i][j]*phi[j] for i in range(4) for j in range(4)),Q())
assert comm([Y+ss*u for u in v])==ss
assert comm([(Y+ss*u)**2 for u in v])==2*Y*ss
fixture_results=fixtures.exact_checks()
assert len(fixture_results)==2

paths=[Path(__file__),D/'round54/regular_global_source.py',D/'round54/regular_source_native.py',
       D/'round54/REGULAR_GLOBAL_SOURCE_PLAN.json',D/'round54/REGULAR_GLOBAL_SOURCE_CHECK.json',
       O/'round105/regular_paid_family.py',O/'round105/B105_REGULAR_PAID_CHECK.json',
       O/'round106/B106_A54_AUDIT_CHECK.json',O/'round65/SCALAR_HESSIAN_ENVELOPE.json',
       O/'round95/QUADRATIC_LIFT_CHECK.json',O/'round97/SCALAR_THIRD_DERIVATIVE_CHECK.json',
       O/'round97/FIXED_POST_WEIGHT_CHECK.json',D/'round50/independent_price_rows.py',
       D/'round50/INDEPENDENT_PRICE_ROWS_PLAN.json',D/'round50/check_independent_price_rows.py']
length_hashes={k:sha256(hex(cfg[k]).encode()).hexdigest() for k in ('coreL','controlL','postL','probeL','Lbase','Nbase')}
out={'status':'PASS_OFF_SHELL_FOUR_AXIS_RECOVERY_ON_A54_B105_CONDITIONAL',
     'field_names':'exact rational |offset_j|<2^-32; same name in both signs',
     'target_covector':['DI_tau(Y)','-DI_tau(Y)/2','DI_tau(Y)/2','0'],
     'target_is_not_a_zero_claim':True,'axes':2688,'middle_CODE_disjoint_verified':True,
     'actual_M_dependent_post_fixed_per_field_across_all_arms':True,
     'gradient_uniform_bound_lt':'1/2','whole_label_prefix_distance_between':'2^-62 and 2^-61',
     'tau_over_gsigma_lt':'85','Q_kernel_lt':'2^-116',
     'Pf_Qf_Qb_each_recovery_error_lt':'2^-108','Pb_recovery_error_lt':'2^-189',
     'all_four_axes_recovery_error_l2_lt':'2^-102',
     'Qb_minus_half_Pf_finite_lt':'2^-115',
     'shifted_exact_product_quadratic_fixture':True,'noncommuting_middle_and_approx_post_negative_fixtures':True,
     'Nbase_bit_length':cfg['Nbase'].bit_length(),'K':cfg['K'],'exact_padded_length_sha256':length_hashes,
     'clock':'N=Nbase+2K; D=2^n*(Lbase-2+3*2^K)-1',
     'uses_actual_field_dependent_Gamma':True,'production_path_sum_or_word_executed':False,
     'full_physical_source_Vh_Info_or_admission_closed':False,'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):digest(f) for f in paths}}
(P/'B107_REGULAR_SOURCE_RECOVERY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('input_sha256','exact_padded_length_sha256')},indent=2))
