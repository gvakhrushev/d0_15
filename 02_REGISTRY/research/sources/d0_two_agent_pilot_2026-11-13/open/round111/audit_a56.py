#!/usr/bin/env python3
"""Independent A56 same-request, clock, finite-source and scope audit."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round56'));import complete_code_source as a56
def read(path):return json.loads(Path(path).read_text())
def digest(path):return sha256(Path(path).read_bytes()).hexdigest()
plan=read(D/'round56/COMPLETE_CODE_SOURCE_PLAN.json')
for path,h in plan['source_sha256'].items():assert digest(path)==h,path
assert plan==a56.build()
assert plan['physical_iota_Vh_identified'] is False
assert plan['native_finite_catalogue_equals_full_skew_space'] is False
assert plan['one_fixed_mesh_not_a_refining_limit'] is True
assert not plan['physical_C_closed'] and not plan['GR_closed']
for name in ('B109_FULL_SKEW_RECOVERY_CHECK.json',):
    receipt=read(O/'round109'/name)
    for path,h in receipt['input_sha256'].items():assert digest(path)==h,path
receipt=read(O/'round110/B110_ANALYTIC_HEAT_STATISTICAL_CHECK.json')
for path,h in receipt['input_sha256'].items():assert digest(path)==h,path
assert receipt['later_7fu_physical_C_withdrawal_preserved']
assert not receipt['path_is_native_paid_arbitrary_skew_family']

# The complete Book source identity must hold for every A55 request; the
# analytic recovery is at the centred graph, while existing finite +/-
# histories use the SAME centre Gamma and one field in each comparison.
task=a56.task
values=[F(0)]*2688;values[7]=F(1,1<<34);values[2500]=F(-1,1<<35)
fields=[task.FieldCentre(),task.FieldCentre(tuple(values))]
cases=0
for field in fields:
    owner=task.FieldTask(field)
    for arm,axis in product(('Pf','Qf','Qb','Pb'),(0,2687)):
        packets=[]
        for sign in (-1,1):
            req=task.Request(field,task.Label(arm,sign,axis))
            got=a56.section_packet(req);ref=owner.packet(req)
            for key in ('request_sha256','field_name_sha256','label','RAW_early_births',
                        'late_retention_pairs','actual_padded_lengths_hex','clock_layers_N_hex',
                        'clock_dimension_formula','input_rank','initial_carrier','closing_gate'):
                assert got[key]==ref[key],key
            assert got['determinant_power']==-1 and got['full_graded_heat_modes']=='425*D'
            assert got['source_identity_fixed_beta']=='-ell*dA_stat=dB-p^3*dH=dJ+beta*dH'
            assert 'same centre Gamma' in got['comparison_normalization']
            assert got['whole_physical_Cost_Info_identified'] is False
            packets.append(got);cases+=1
        assert packets[0]['request_sha256']!=packets[1]['request_sha256']
        for key in ('field_name_sha256','actual_padded_lengths_hex','clock_layers_N_hex'):
            assert packets[0][key]==packets[1][key]
assert cases==32
try:a56.section_packet(object())
except (TypeError,AttributeError,ValueError):pass
else:raise AssertionError('non-request accepted')

# Golden ring calculation independently verifies beta-1=-p^3, the source
# orientation and the failure of omitting beta*DH or reversing the sign.
sys.path.insert(0,str(D/'round47'));import full_vector_controls as ctl
Q=ctl.e.Q4;p=ctl.e.SIN;beta=2*p*p
assert p+p*p==Q(1) and beta-Q(1)==-p**3
for h,j in product((Q(0),Q(1),p,Q(F(-5,7))),repeat=2):
    dB=h+j;d_oriented=j+beta*h
    assert d_oriented==dB-p**3*h
    assert d_oriented==j+beta*h
assert (beta*Q(1)+Q(1)) != (Q(1)+Q(1))

# Stage count and dimension are independently derived from actual early
# births, all body stages, and each retention birth followed by a gate.
cfg=task.FieldTask(fields[0]).family.cfg
assert cfg['Nbase']==cfg['n']+cfg['Lbase']
assert cfg['Lbase']==cfg['coreL']+cfg['postL']+cfg['probeL']+4*cfg['controlL']
assert cfg['n']==11893774624 and cfg['K']==175604 and cfg['Nbase'].bit_length()==30833
assert cfg['Nbase']!=task.paid.paid.production_configuration()['Nbase']
layout_cases=0
for n in range(1,7):
    for body in (4,7,12,23):
        for K in range(0,7):
            stage_dims=[1<<j for j in range(n)]+[1<<n]*body
            for j in range(K):stage_dims.extend((1<<(n+j),1<<(n+j+1)))
            assert len(stage_dims)==n+body+2*K
            assert sum(stage_dims)==(1<<n)*(body-2+3*(1<<K))-1
            assert sum(stage_dims)>=1<<(n+K)
            layout_cases+=1
assert layout_cases==168

# Independent exact finite bound: B107 H+J coordinate error plus the
# source identity's p^3*heat contrast. Bound p^3<1, and use the NEW clock.
sigma_step=F(1,1<<1700);gamma0=F(8,3)*F(1,1<<3228)
heat=F(6*cfg['Nbase'],359)/(sigma_step*gamma0)*F(1,1<<(cfg['K']//4))
assert heat<F(1,1<<8139)
assert 4*2688<104**2
finite=F(1,1<<102)+104*heat
assert finite==a56.bounds()['finite_native_statistical_four_axis_l2']<F(1,1<<101)
analytic_heat=F(6*4*52,359)/gamma0*F(1,1<<(cfg['K']//4))
assert analytic_heat==a56.bounds()['analytic_heat_full_raw_dual']<F(1,1<<40672)
assert a56.bounds()['master_full_raw_dual']<F(1,1<<34)

# Full-skew plane-basis extrapolation: d=2^5376, each slot has d(d-1)/2
# planes.  Frobenius-to-trace-norm and B109's factor 52 give the safe
# interpolation envelope 104*d*sqrt(d-1)*e < 104*2^8064*e.
# With e<2^-8105 this EXTRA raw-dual error is <2^-34. This is only a
# sufficient uniform per-plane budget, not a native compiler or an
# automatic nonlinear arbitrary-X finite-difference theorem.
assert 3*5376//2==8064
plane_error=F(1,1<<8105)
plane_dual=104*(1<<8064)*plane_error
assert plane_dual<F(1,1<<34)
assert 104*(1<<8064)*F(1,1<<108)>1

# Illustrative sufficient allocation for finite-vs-analytic plane rows,
# conditional on a new compiler fitting a NEW body bound below 2^30833.
# It is not a construction or a claim that existing eP, t or K suffice.
t_candidate=F(1,1<<5658);K_candidate=191308
gs=F(1,1<<3208);z=F(1,1<<20)
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
assert bracket<16
assert bracket/16+F(1,6)<1
taylor=t_candidate**2*(bracket/16+F(1,6))/gs
control=2*F(1,1<<16976)/(t_candidate*gs)
finite_heat=F(6*(1<<30833),359)/(t_candidate*gamma0)*F(1,1<<(K_candidate//4))
analytic_one=F(6,359)/gamma0*F(1,1<<(K_candidate//4))
assert K_candidate%4==0
assert max(taylor,control,finite_heat,analytic_one)<F(1,1<<8108)
# One further independently paid/readout error <2^-8108 still leaves slack.
candidate_plane=taylor+control+finite_heat+analytic_one+F(1,1<<8108)
assert candidate_plane<F(1,1<<8105)

# A stricter illustrative precision target matching a 2^-75 added raw
# dual envelope, using the coarser 208*2^8064 conversion. This assumes a
# new certified q-bit plane-word grammar with its full operator error,
# and a remeasured new Nbase upper of 2^b, never an old clock by fiat.
T=6000;qbits=32768;body_bits=30833;K75=4*(body_bits+17375)
step75=F(1,1<<T)
mu75=F((1<<5375)+40*5376,1<<qbits)
plane_control75=2*mu75/(step75*gs)
plane_taylor75=step75**2*(bracket/16+F(1,6))/gs
plane_heat75=F(6*(1<<body_bits),359)/(step75*gamma0)*F(1,1<<(K75//4))
plane_analytic_heat75=F(6,359)/gamma0*F(1,1<<(K75//4))
assert max(plane_control75,plane_taylor75,plane_heat75,plane_analytic_heat75)<F(1,1<<8149)
plane75=plane_control75+plane_taylor75+plane_heat75+plane_analytic_heat75+F(1,1<<8150)
assert plane75<F(1,1<<8147)
assert 208*(1<<8064)*plane75<F(1,1<<75)
# With q=20000, these particular sufficient bounds cannot BOTH be <2^-75:
# Taylor decreases with T, control increases with T; tested thresholds overlap.
mu_old=F((1<<5375)+40*5376,1<<20000);dfac=208*(1<<8064)
assert dfac*F(1,1<<(2*5676))*(bracket/16+F(1,6))/gs>F(1,1<<75)
assert dfac*2*mu_old/(F(1,1<<3270)*gs)>F(1,1<<75)

files=[D/'round56'/x for x in ('complete_code_source.py','check_complete_code_source.py',
       'COMPLETE_CODE_SOURCE_RU.md','COMPLETE_CODE_SOURCE_PLAN.json')]
files += [O/'round107/B107_REGULAR_SOURCE_RECOVERY_CHECK.json',
          O/'round109/B109_FULL_SKEW_RECOVERY_CHECK.json',
          O/'round110/B110_ANALYTIC_HEAT_STATISTICAL_CHECK.json',Path(__file__)]
out={'status':'PASS_A56_CONDITIONAL_SAME_GRAPH_SOURCE_AND_DISTINCT_FINITE_SCOPE',
     'actual_A55_sign_axis_field_packets_checked':cases,'exact_small_stage_layouts_checked':layout_cases,
     'golden_beta_source_orientation_checked':True,'new_Nbase_K_and_425D_retained':True,
     'finite_native_MG2_statistical_four_axis_l2_lt':'2^-101',
     'analytic_full_skew_raw_error_lt':'2^-34','analytic_heat_raw_dual_lt':'2^-40672',
     'sufficient_extra_basis_interpolation_per_plane_error_lt':'2^-8105',
     'plane_interpolation_extra_raw_dual_lt':'2^-34',
     'plane_budget_is_not_an_actual_compiler_or_arbitrary_X_finite_theorem':True,
     'illustrative_allocation_if_new_Nbase_lt_2^30833':{
         'control_step':'2^-5658','control_operator_error_lt':'2^-16976',
         'retention_pairs':K_candidate,'independent_normalized_readout_error_lt':'2^-8108',
         'status':'conditional arithmetic only; remeasure new compiler and actual clock'},
     'stricter_illustrative_plane_allocation_for_added_dual_lt_2^-75':{
         'step_bits':T,'angle_precision_bits':qbits,
         'conditional_new_Nbase_bit_bound':body_bits,'retention_pairs_if_bound_holds':K75,
         'general_K_formula_for_new_Nbase_b_bits':'4*(b+17375)',
         'normalized_readout_error_lt':'2^-8150',
         'status':'not compiled or certified; remeasure changed word, padding and clock'},
     'old_q20000_sufficient_bounds_conflict_for_2^-75':True,
     'book_partition_law_is_explicit_premise':True,'7fu_withdraws_physical_C_closure':True,
     'physical_iota_Vh_or_complete_skew_native_family_proved':False,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):digest(f) for f in files}}
(P/'B111_A56_AUDIT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
