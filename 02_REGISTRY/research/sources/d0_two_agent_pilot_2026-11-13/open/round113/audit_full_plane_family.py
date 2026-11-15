#!/usr/bin/env python3
"""Independent finite-plane family, price and marked-prefix audit."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from types import SimpleNamespace
from unittest.mock import patch
import json,sys
import sympy as sp
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round57'));import full_plane_family as a
def read(path):return json.loads(Path(path).read_text())
def digest(path):return sha256(Path(path).read_bytes()).hexdigest()

# Owner has explicitly frozen these five files.  Check both receipts and
# regenerate the in-memory plan only; no owner path is written here.
owner_files=[D/'round57'/name for name in ('full_plane_family.py','FULL_PLANE_FAMILY_PLAN.json',
             'check_full_plane_family.py','FULL_PLANE_FAMILY_CHECK.json','FULL_NATIVE_PLANE_SOURCE_RU.md')]
assert all(path.is_file() for path in owner_files)
owner_plan=read(owner_files[1]);owner_check=read(owner_files[3])
assert owner_plan['status']=='FOUR_NATIVE_CODE_PLANE_FAMILIES_ON_REMEASURED_COMMON_CLOCK'
assert owner_check['status']=='PASS_FULL_PLANE_REQUESTS_FACTORIES_PREFIXES_CLOCK_AND_DUAL_BUDGET'
for receipt in (owner_plan,owner_check):
    for path,h in receipt['source_sha256'].items():assert digest(path)==h,path
assert owner_plan==json.loads(json.dumps(a.build()))

# Exact same-corner feedback cancellation at the NEW K: no transfer of an
# old numeric heat, or of an old unfrozen Gamma, is used in this algebra.
eta,c0,dc,cref,gs0,z0=sp.symbols('eta c0 dc cref gs z',nonzero=True)
den=1-z0+eta*c0*c0
dJ=-2*eta*c0*dc/den;Gamma=4*eta*cref*gs0/den
assert sp.cancel(dJ/Gamma+c0*dc/(2*cref*gs0))==0
assert sp.diff(sp.cancel(dJ/Gamma),eta)==0

# Consume, do not replay, the already certified B112 high precision input.
b112=read(O/'round112/B112_PLANE_PRECISION_CHECK.json')
assert b112['status']=='PASS_32768_GRID_AND_PAID_CODE_ONLY_PLANE_PRECISION'
for path,h in b112['input_sha256'].items():assert digest(path)==h,path
pn,q,cert=a.grid.uniform_grid();macro=a.grid.Macros();k8=macro.ks['pi8']
assert q.bit_length()==32773 and 1<=k8<=q
fields=[a.FieldCentre(),a.FieldCentre(tuple(F((j%7)-3,1<<38) for j in range(2688)))]
instances=[a.FullPlaneTask(field) for field in fields];cfg=instances[0].cfg;old=instances[0].bound.family.cfg
m=5376;L=1<<(m-1)
plane=Counter(G=L*q+40*m*k8,CX=(m-1)*L+2*(m-1)+4*m)
assert plane==cfg['plane_upper']
assert cfg['controlL']==max(old['controlL'],sum(plane.values())+4)
assert cfg['controlL']>=sum(plane.values())+4 and cfg['controlL']>=old['controlL']
for key in ('coreL','postL','probeL','sam','n'):assert cfg[key]==old[key]
assert cfg['Lbase']==cfg['coreL']+cfg['postL']+cfg['probeL']+4*cfg['controlL']
assert cfg['Nbase']==cfg['n']+cfg['Lbase'] and cfg['Nbase'].bit_length()==38150
assert cfg['K']==4*(cfg['Nbase'].bit_length()+17375)==222100
assert cfg['Nbase']!=old['Nbase'] and cfg['K']!=old['K']
assert all(cfg[k]==instances[1].cfg[k] for k in ('controlL','coreL','postL','probeL','Lbase','Nbase','K'))
for current in instances:
    family=current.bound.family;target=family.actual_core_target()
    assert target.factory.__self__ is family.source
    assert family.source.field is family.source.sources.components.field is current.field
    assert family.actual_core_target() is target
assert instances[0].bound.family.actual_core_target() is not instances[1].bound.family.actual_core_target()

# Actual high-precision provider: first compact DAG for the 0--1 plane is
# exactly the signed certified G power on the first bound CODE wire.
# No production Walsh masks, repeat leaves or giant matrices are expanded.
for inst in instances:
    for sign in (-1,1):
        power=a.grid.plane_power(sign,5376,6000)
        expected=a.paid.native.repeat(power,a.paid.native.gate('G',cfg['sam'][0]))
        assert next(inst.native_plane_blocks((0,1),sign))==expected
        for arm in a.ARMS:
            label=a.PlaneLabel(arm,sign,(0,1))
            physical=-sign if arm in ('Qf','Pb') else sign
            block=next(inst.control_provider(label)(0,physical))
            pp=a.grid.plane_power(physical,5376,6000)
            assert block==a.paid.native.repeat(pp,a.paid.native.gate('G',cfg['sam'][0]))

# Independent exact price error: compare finite plane H+J to analytic H+J,
# explicitly including Cayley angle, independently compiled +/- words,
# new-clock finite heat and analytic heat. Zero reading error is the exact
# mathematical value; an optional normalized per-row allowance is separate.
t=F(1,1<<6000);gs=F(1,1<<3208);z=F(1,1<<20);gamma0=F(8,3)*z*gs
mu=F(L+40*m,1<<32768)
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
taylor=t*t*(bracket/16+F(1,6))/gs
control=2*mu/(t*gs)
heat=F(6*cfg['Nbase'],359)/(t*gamma0)*F(1,1<<(cfg['K']//4))
analytic_heat=F(6,359)/gamma0*F(1,1<<(cfg['K']//4))
factor=208*(1<<8064)
row=taylor+control+heat+analytic_heat
assert mu<F(1,1<<27392) and max(taylor,control,heat,analytic_heat)<F(1,1<<8149)
assert factor*row<F(1,1<<75)
for reading in (F(0),F(1,1<<8150)):
    result=a.bounds(cfg,normalized_reading_error=reading)
    assert result['plane_operator_error']==mu
    assert result['finite_Taylor_and_Cayley']==taylor
    assert result['native_control_error']==control
    assert result['finite_heat_per_plane']==heat
    assert result['analytic_heat_per_plane']==analytic_heat
    assert result['finite_vs_analytic_row']==row+reading
    assert result['dimension_factor']==factor
    assert result['finite_vs_analytic_full_raw_dual']==factor*(row+reading)<F(1,1<<75)
    assert result['full_analytic_target_error']==a.analytic.bounds()['feedback_full_raw_dual']+208*analytic_heat
    assert result['finite_full_raw_target_error']==result['full_analytic_target_error']+factor*(row+reading)<F(1,1<<34)

# Actual request encoding, four slot signs, all existing label kinds, and
# rejection of malformed or foreign field requests without giant expansion.
labels=[a.PlaneLabel(arm,sign,plane) for arm in a.ARMS for sign in (-1,1)
        for plane in ((0,1),(1,(1<<5376)-1))]
labels += [a.LegacyLabel()]+[a.LegacyLabel(arm,sign,axis)
          for arm in a.prior.original.ARMS for sign in (-1,1) for axis in (0,2687)]
labels += [a.LegacyLabel('post_probe',s,plane=(0,(1<<5376)-1)) for s in (-1,1)]
assert len(labels)==39
for inst in instances:
    for label in labels:
        req=a.Request(inst.field,label);assert a.Request.decode(req.encode())==req
        record=inst.packet(req)
        assert record['actual_padded_lengths_hex']['Nbase']==hex(cfg['Nbase'])
        assert record['late_retention_pairs']==222100
        shape=inst.legacy_shape(label);signs=a.paid.slot_signs(shape.arm,shape.sign)
        if type(label) is a.PlaneLabel:
            assert sum(v!=0 for v in signs.values())==1
            assert signs[label.arm]==(-label.sign if label.arm in ('Qf','Pb') else label.sign)
try:instances[0].validate(a.Request(fields[1]))
except ValueError:pass
else:raise AssertionError('cross-field request accepted')

# Compact, independent whole-word/prefix fixture through A57's OWN wrapper.
# Literal words use 3 CODE wires, small k and noncommuting middle gates; the
# big SOURCE/post are represented by distinct finite paid fixture streams.
nb=a.paid.native;e=a.paid.target.e;reg=a.prior.prefixes.registry()
marks=['SOURCE_before_Qf']+[row['name'] for row in reg]
assert len(marks)==13
small_labels=[a.PlaneLabel(arm,s,plane) for arm in a.ARMS for s in (-1,1)
              for plane in ((0,1),(1,7))]
small_labels += [a.LegacyLabel()]+[a.LegacyLabel(arm,s,axis)
                 for arm in a.prior.original.ARMS for s in (-1,1) for axis in (0,2)]
small_labels += [a.LegacyLabel('post_probe',s,plane=(0,7)) for s in (-1,1)]
assert len(small_labels)==39
class FixtureMacros:
    power=nb.Macros.power;pi8=nb.Macros.pi8;z=nb.Macros.z;x=nb.Macros.x
    def __init__(self):self.ks={'pi8':1}
fixtures=0
for fidx,field in enumerate(fields):
    sam=(0,1,2);before=[nb.gate('G',3),nb.gate('CX',3,4)]
    middle=[[nb.gate('G',4),nb.gate('CX',4,3)] if j%2 else [nb.gate('G',3)] for j in range(11)]
    ret=[nb.gate('CX',3,4),nb.gate('G',3)]
    def core():
        yield from before
        yield {'op':'B82_CUT','name':a.paid.CUTS[0]}
        for group in middle:yield from group
        yield {'op':'B82_CUT','name':a.paid.CUTS[1]}
        yield from ret
    def processor(name):
        for group in middle[:a.prior.prefixes.descriptor(name)['processor_stage_count']]:yield from group
    def control(axis,sign):
        if sign:yield nb.repeat(1 if sign>0 else 2,nb.gate('G',sam[axis%3]))
    def flatten(it):return [gate for tree in it for gate in e.leaves(tree)]
    toy_upper=a.paid.old.plane_upper(3,2,1)
    toy={'sam':sam,'controlL':sum(toy_upper.values())+4,
         'coreL':len(before)+sum(map(len,middle))+len(ret)+4,'postL':6,'probeL':6}
    inst=a.FullPlaneTask.__new__(a.FullPlaneTask);inst.field=field;inst.cfg=toy
    family=SimpleNamespace(_guard=lambda:None,source=SimpleNamespace(
        compiled_core_with_cuts=core,source_prefix_blocks=lambda:iter(before)),
        actual_post_blocks=lambda:iter([nb.gate('G',0),nb.gate('G',1)]),
        actual_probe_blocks=lambda plane,sign:control(0,sign))
    inst.bound=SimpleNamespace(family=family,processor_native_blocks=processor)
    calls=[]
    def fake_power(sign,m):calls.append(sign);return 1 if sign>0 else 2
    with patch.object(a,'plane_power',fake_power),patch.object(a.grid,'Macros',FixtureMacros), \
         patch.object(a.paid,'raw_control_factory',control):
        for label in small_labels:
            request=a.Request(field,label);calls.clear();full=flatten(inst.word_blocks(request))
            if type(label) is a.PlaneLabel:
                expected=-label.sign if label.arm in ('Qf','Pb') else label.sign
                assert calls==[expected]
            for mark in marks:
                part=flatten(inst.prefix_blocks(request,mark))
                n=toy['controlL']+len(before)
                if mark!='SOURCE_before_Qf':
                    n+=toy['controlL']+sum(map(len,middle[:a.prior.prefixes.descriptor(mark)['processor_stage_count']]))
                assert len(part)==n and part==full[:n]
                fixtures+=1
assert fixtures==2*39*13

paths=[Path(__file__),*owner_files,
       O/'round112/B112_PLANE_PRECISION_CHECK.json',O/'round112/plane_grid_32768.py',
       O/'round111/B111_A56_AUDIT_CHECK.json',D/'round55/regular_comparison_task.py',
       O/'round105/regular_paid_family.py',D/'round56/complete_code_source.py']
out={'status':'PASS_A57_FOUR_PLANE_FAMILY_ON_FROZEN_OWNER',
     'new_Nbase_bit_length':cfg['Nbase'].bit_length(),'new_K':cfg['K'],
     'new_control_upper_G_bits':plane['G'].bit_length(),'new_control_upper_CX_bits':plane['CX'].bit_length(),
     'two_field_common_clock_and_actual_post_binding':True,
     'request_roundtrips':2*len(labels),'whole_word_prefix_fixture_cases':fixtures,
     'signed_four_slots_and_legacy_labels_checked':True,
     'finite_plane_row_terms':'t^2*(bracket/16+1/6)/gs+2mu/(t*gs)+finiteHeat+analyticHeat',
     'same_corner_feedback_over_new_Gamma_exact_K_cancellation':True,
     'finite_interpolant_vs_analytic_dual_lt':'2^-75','finite_target_dual_lt':'2^-34',
     'exact_mathematical_price_reading_error':0,'optional_normalized_per_row_reading_reserve':'2^-8150',
     'physical_reader_executed_or_free':False,'joint_arbitrary_X_native_finite_theorem':False,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):digest(f) for f in paths}}
(P/'B113_A57_AUDIT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
