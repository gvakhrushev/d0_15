#!/usr/bin/env python3
"""Independent A55 binding/prefix/jet audit; finite fixtures, no giant replay."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import islice
from types import SimpleNamespace
from unittest.mock import patch
import json,sys
import sympy as sp
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round55'));import regular_comparison_task as a55

def read(path):return json.loads(Path(path).read_text())
def digest(path):return sha256(Path(path).read_bytes()).hexdigest()
plan=read(D/'round55/REGULAR_COMPARISON_TASK.json')
check=read(D/'round55/REGULAR_COMPARISON_TASK_CHECK.json')
assert plan['status']=='REGULAR_FIELD_REQUESTS_BOUND_TO_ACTUAL_PAID_MARKED_FAMILY'
assert check['status']=='PASS_REGULAR_FIELD_REQUEST_AND_MARKED_PREFIX_BINDING'
for receipt in (plan,check):
    for name,expected in receipt['source_sha256'].items():assert digest(name)==expected,name

# Exhaust the finite ordinary label catalogue; count the separate gigantic
# post-probe set combinatorially rather than attempting to enumerate it.
labels=list(a55.original.catalogue());assert len(labels)==len(set(labels))==26881
counts=Counter(label.arm for label in labels)
assert counts==Counter(centre=1,matched=5376,Pf=5376,Qf=5376,Qb=5376,Pb=5376)
assert plan['ordinary_catalogue_count_per_fixed_field']==len(labels)
assert plan['post_probe_catalogue_count_per_fixed_field']=='2^5376*(2^5376-1)'
assert plan['total_catalogue_count_per_fixed_field']=='26881+2^5376*(2^5376-1)'
assert not plan['all_field_names_claimed_one_finite_catalogue']
assert not plan['parser_compiler_or_readback_execution_cost_claimed_free']

# Infinitely many distinct legal names occur even with one fixed label.
# Both numerator and denominator are canonical, with a common constructor.
field0=a55.FieldCentre(); fixed=a55.Label()
names=[]
for n in range(33,81):
    offsets=[F(0)]*2688;offsets[1337]=F(1,1<<n)
    field=a55.FieldCentre(tuple(offsets));packet=a55.Request(field,fixed).encode()
    assert a55.Request.decode(packet)==a55.Request(field,fixed)
    names.append(packet)
assert len(set(names))==48
base=json.loads(a55.Request(field0).encode()); illegal=[]
for key,value in [('program','hidden'),('reader','hidden'),('clock',4),('source',0)]:
    d=dict(base);d[key]=value;illegal.append(json.dumps(d,sort_keys=True,separators=(',',':')).encode())
# Canonical duplicate-key/whitespace forms must not turn into new datum.
illegal += [b' '+a55.Request(field0).encode(),a55.Request(field0).encode()+b'\n']
for packet in illegal:
    try:a55.Request.decode(packet)
    except (TypeError,ValueError):pass
    else:raise AssertionError('noncanonical or hidden input accepted')

# Different exact fields create separate actual-M providers, whereas every
# label on a field remains attached to the same per-instance target and cfg.
offsets=[F(0)]*2688;offsets[23]=F(1,1<<34);offsets[1800]=F(-1,1<<35)
field1=a55.FieldCentre(tuple(offsets));tasks=[a55.FieldTask(field0),a55.FieldTask(field1)]
targets=[]
for current in tasks:
    target=current.family.actual_core_target();targets.append(target)
    assert target.factory.__self__ is current.family.source
    assert current.family.source.field is current.family.source.sources.components.field is current.field
    for label in (a55.Label(),a55.Label('matched',1,1344),a55.Label('Pf',-1,2687),
                  a55.Label('Qf',1,0),a55.Label('Qb',-1,1344),a55.Label('Pb',1,2687),
                  a55.Label('post_probe',-1,plane=(0,(1<<5376)-1))):
        request=a55.Request(current.field,label);current.validate(request)
        assert current.family.actual_core_target() is target
        assert current.packet(request)['actual_padded_lengths_hex']['Nbase']==hex(current.family.cfg['Nbase'])
assert targets[0] is not targets[1]
assert all(tasks[0].family.cfg[k]==tasks[1].family.cfg[k] for k in ('coreL','controlL','postL','probeL','Lbase','Nbase','K'))
assert tasks[0].family.cfg['Nbase']!=a55.paid.paid.production_configuration()['Nbase']
for owner,foreign in ((tasks[0],field1),(tasks[1],field0)):
    try:owner.validate(a55.Request(foreign))
    except ValueError:pass
    else:raise AssertionError('cross-field request accepted')

# Compute field-independent processor stage lists directly from the actual
# global schedule, check uniqueness and validate dispatch at every mark.
schedule=a55.source.schedule();marker={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}
assert schedule.count(marker)==1
processor=schedule[schedule.index(marker)+1:]
assert Counter(x['kind'] for x in processor)==Counter(RAW_RESOURCE_FRAME=1,REPORT=8,PORT_ZERO=1,SC6=1)
registry=a55.prefixes.registry();assert len(registry)==12
assert [x['processor_stage_count'] for x in registry]==list(range(12))
assert len({x['name'] for x in registry})==12 and registry[0]['name']=='SOURCE_after_Qf'
assert registry[-1]['name']=='SC6'
assert all(z['kind'] not in ('SOURCE','SITE','SIGMA') for z in processor)
calls=[]
def fake_stage(z,depth=0):calls.append((z,depth));yield {'stage':z}
class IdentityCompiler:
    def stream(self,it):yield from it
for current in tasks:
    with patch.object(current.family.source,'stage_blocks',fake_stage), \
         patch.object(a55.source,'compiler',lambda:IdentityCompiler()), \
         patch.object(a55.source,'physical_tree',lambda x:x):
        for row in registry:
            calls.clear();out=list(current.processor_native_blocks(row['name']))
            want=processor[:row['processor_stage_count']]
            assert calls==[(z,0) for z in want] and out==[{'stage':z} for z in want]

# The provider is a literal prefix of a complete B105 word.  Use compact,
# noncommuting gate fixtures and inspect every location for both fields,
# every slot, both signs, three axis indices and both post-probe extremes.
nb=a55.paid.paid.native; e=a55.paid.paid.target.e
marks=['SOURCE_before_Qf']+[r['name'] for r in registry]
samples=[a55.Label()]+[a55.Label(arm,sign,axis) for arm in a55.original.ARMS
         for sign in (-1,1) for axis in (0,1344,2687)]
samples += [a55.Label('post_probe',s,plane=(0,(1<<5376)-1)) for s in (-1,1)]
assert len(samples)==33
assertions=0
for fidx,field in enumerate((field0,field1)):
    sam=(0,1,2);before=[nb.gate('G',3+fidx),nb.gate('CX',3+fidx,4+fidx)]
    mids=[[nb.gate('G',3),nb.gate('CX',3,4)] if j%2 else [nb.gate('G',4)] for j in range(11)]
    ret=[nb.gate('CX',4,3)]
    def core():
        yield from before
        yield {'op':'B82_CUT','name':a55.paid.paid.CUTS[0]}
        for group in mids:yield from group
        yield {'op':'B82_CUT','name':a55.paid.paid.CUTS[1]}
        yield from ret
    def control(axis,sign):
        if sign:yield nb.repeat(1 if sign>0 else 2,nb.gate('G',sam[axis%3]))
    def processor_factory(name):
        for group in mids[:a55.prefixes.descriptor(name)['processor_stage_count']]:yield from group
    def leaves(it):return [z for tree in it for z in e.leaves(tree)]
    cfg={'sam':sam,'controlL':6,'coreL':len(before)+sum(map(len,mids))+len(ret)+4,'postL':6,'probeL':6}
    fixture=a55.FieldTask.__new__(a55.FieldTask);fixture.field=field
    fixture.family=SimpleNamespace(cfg=cfg,_guard=lambda:None,source=SimpleNamespace(source_prefix_blocks=lambda:iter(before)))
    fixture.processor_native_blocks=processor_factory
    with patch.object(a55.paid.paid,'raw_control_factory',control):
        for label in samples:
            request=a55.Request(field,label)
            full=leaves(a55.paid.paid.family_blocks(cfg,core,lambda:iter([nb.gate('G',0)]),
                  control,lambda plane,sign:control(2,sign),**a55.asdict(label)))
            for mark in marks:
                actual=leaves(fixture.prefix_blocks(request,mark))
                n=cfg['controlL']+len(before)
                if mark!='SOURCE_before_Qf':
                    n+=cfg['controlL']+sum(map(len,mids[:a55.prefixes.descriptor(mark)['processor_stage_count']]))
                assert len(actual)==n and actual==full[:n]
                assertions+=1
assert assertions==2*33*13

# A constant-source counterexample: before Qf, Pf itself produces a
# nonzero finite jet while the geometric derivative is zero.  After Qf,
# opposite exact controls cancel. This bars silently moving the jet claim.
R=sp.Rational;v=sp.Matrix([1,0]);X=sp.Matrix([[0,-1],[1,0]])
tt=R(1,9); plus=(sp.eye(2)+tt*X)*(sp.eye(2)-tt*X).inv()
minus=(sp.eye(2)-tt*X)*(sp.eye(2)+tt*X).inv()
assert (plus*v-minus*v)/(2*tt)!=sp.zeros(2,1)
assert minus*plus*v==v and plus*minus*v==v

# Reconstruct the input bounds directly, not by importing frontier_bounds.
up=a55.source.upper_inventory_and_error();c=a55.paid.paid.control.control_plan()['control_vs_exp_tX_error']
ep=F(int(c['numerator_hex'],16),int(c['denominator_hex'],16))
sigma,t=F(1,1<<80),F(1,1<<1700);M1,M2=1748,3233036
eB=up['full_SOURCE_DATA_fibre_prefix_error'];eW=up['replacement_error']
assert eB<F(1,1<<3423) and eW<F(1,1<<15800)
report=read(D/'round17/GLOBAL_REPORT_COMPILATION.json');known=report['seven_report_all_known_approximate_macros']
assert known%7==0;eD=F(8*(known//7),1<<4096)+eW
extra=(eB+2*ep)/(sigma*t)+F(4,3)*104*M1*t*t
source_jet=sigma*104**2*M2+extra;jet=source_jet+eD*M1
mid=sigma*104*M1+eB+eD+2*ep+2*t*t;effect=2*jet+2*M1*mid
assert eD<F(1,1<<4058) and extra<F(1,1<<1642)
assert jet<F(1,1<<44) and mid<F(1,1<<62) and effect<F(1,1<<43)
enc=lambda v:{'numerator_hex':hex(v.numerator),'denominator_hex':hex(v.denominator)}
for key,v in [('all_completed_processor_prefix_error',eD),('full_prefix_finite_axis_jet_error',jet),
              ('full_prefix_midpoint_error',mid),('norm_one_joint_effect_finite_axis_jet_error',effect)]:
    assert plan['bounds'][key]==enc(v),key

b107=read(O/'round107/B107_REGULAR_SOURCE_RECOVERY_CHECK.json')
for name,expected in b107['input_sha256'].items():assert digest(name)==expected,name
assert b107['target_covector']==['DI_tau(Y)','-DI_tau(Y)/2','DI_tau(Y)/2','0']
assert plan['B107_off_shell_price_recovery']['target_covector']==b107['target_covector']
assert plan['B107_off_shell_price_recovery']['four_2688_axis_recovery_Euclidean_error_lt']=='2^-102'
assert plan['independent_or_pre_Qf_jets_claimed_geometric'] is False
assert plan['physical_fine_instrument_registered_or_measurement_inserted'] is False
assert plan['all_logical_sources_or_Vh_norm_or_Cost_Info_closed'] is False
assert not plan['physical_C_closed'] and not plan['GR_closed']
files=[D/'round55'/name for name in ('regular_comparison_task.py','REGULAR_COMPARISON_TASK.json',
       'check_regular_comparison_task.py','REGULAR_COMPARISON_TASK_CHECK.json','REGULAR_FIELD_TASK_AND_FRONTIERS_RU.md')]
files += [O/'round107/B107_REGULAR_SOURCE_RECOVERY_CHECK.json',O/'round107/B107_OFF_SHELL_FOUR_AXIS_SOURCE_RECOVERY_RU.md',Path(__file__)]
out={'status':'PASS_A55_BINDING_AND_PREFIX_JET_ON_DECLARED_TYPED_FIBRE',
     'ordinary_labels_exhausted':len(labels),'separate_post_probe_count_formula_verified':True,
     'distinct_rational_field_names_fixture':len(names),'hidden_program_or_reader_rejected':True,
     'actual_field_post_and_common_new_clock_binding':True,'processor_marks_all':len(registry),
     'literal_prefix_cases':assertions,'pre_Qf_non_geometric_counterexample':True,
     'uniform_full_vector_jet_lt':'2^-44','unconditioned_joint_effect_jet_lt':'2^-43',
     'B107_target_covector_and_scope_checked':True,'all_original_marks_or_physical_instrument_proved':False,
     'production_words_executed':False,'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):digest(f) for f in files}}
(P/'B108_A55_AUDIT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
