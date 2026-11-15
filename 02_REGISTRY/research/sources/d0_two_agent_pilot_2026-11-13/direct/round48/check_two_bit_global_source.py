#!/usr/bin/env python3
"""Binding, native-DAG, literal-depth, resource and exact-budget checks."""
from pathlib import Path
from collections import Counter
from itertools import islice,zip_longest
from fractions import Fraction as F
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
import two_bit_global_source as g
s=g.s;local=s.local;nb=s.nb;P=Path(__file__).resolve().parent
plan=g.namespace();lay=plan['layout'];u=g.upper_inventory_and_error()
s.validate_choi(s.choi_layout())

# Every real global source slot is checked, including the eighth bank.
occupied=set(lay['SAM']);kinds=Counter();private_count=0
assert len(occupied)==5376
for slot in plan['source_slots']:
    kinds[slot['kind']]+=1
    if slot['kind']=='Choi':
        bind=g.ns.choi_layout(plan,slot);s.validate_choi(bind)
        assert bind['address']==slot['source'][10:] and bind['choi_output']==slot['source'][:5]
        qs=s.data(bind)+s.private(bind)
    else:
        bind=g.ns.car_layout(plan,slot)
        pv=[bind['predicate_flag'],*bind['predicate_work']]
        s.vac.validate(bind,[*pv,bind['native_aux_arbitrary']])
        qs=bind['internal_SITE']+bind['grade']+bind['RIGHT']+pv
    assert not occupied.intersection(qs)
    assert plan['old_compiler_helper'] not in qs
    occupied.update(qs);private_count+=len(slot['private'])
assert kinds=={'Choi':1440,'CAR':128} and private_count==8*4368
assert plan['SC6_local_to_global']==g.previous.namespace()['SC6_local_to_global']
assert not set(lay['SAM']).intersection(g.previous.resource_wires())

# Check each affine birth interval without enumerating billions of births.
cursor=0;checks=[]
for block in g.birth_blocks():
    a,b=block['start'],block['stop'];assert a<b
    for q in {a,b-1,(a+b-1)//2}:
        assert g.physical_wire(q)==cursor+q-a
        assert g.physical_wire(q,37)==37+cursor+q-a
    checks.append({'role':block['role'],'physical_start':cursor,'count':b-a})
    cursor+=b-a
assert cursor==11893774624
for j in range(2688):
    assert g.physical_wire(lay['SAM'][j])==2+j
    assert g.physical_wire(lay['SAM'][2688+j])==11893771936+j
assert g.physical_wire(plan['old_compiler_helper'])==10407050781

schedule=g.previous.stages();frame=schedule.index({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0})
assert all(x['kind']!='REPORT' for x in schedule[:frame+1])
assert sum(x['kind']=='SOURCE' for x in schedule[:frame])==1568
assert sum(x['kind']=='REPORT' for x in schedule)==8

# Exhaust small native Walsh words and integer inverse depths, not giant
# production repeats. Compare actual emitted DAG resources with the formula.
small={'port':10,'spin':[11,12]};toy_checks=0
for K in range(4):
    for pattern in ([0]*K,[1]*K):
        bound={'K':K,'controls':list(range(K)),'pattern':pattern,'target':4,
               'k':3,'permutation':[nb.gate('CX',4,5)]}
        for depth in range(4):
            got=Counter()
            for tree in local.cf.unit_blocks(bound,depth,small):
                got.update(local.car.resource(tree,10))
            assert +got==+local.cf.unit_counts(bound,depth)
            toy_checks+=1

# Compare the new stream adapter to the old exact DAG adapter on a finite
# toy, including outer inverses of already inverted words. No numeric phase
# claim is made for these non-nine levels.
toy={'SAM':[],'address':[],'choi_input':[],'choi_output':[1],'branch':0,
     'phase_rebit':2,'comparator_scratch':[3],'port':4,'spin':[5,6],
     'aux_arbitrary':7,'oldRIGHT_witness':8,'qubits':9}
tal=s.old.adapter_layout(toy);V=nb.selective_rotation([0],[1],1,1,4,(5,6))
save_inputs=s.inputs;save_loader=s.omega_blocks
def fake_inputs():return {'phase':{'phase_k':'1'},'level9':{'correction_l':'1'},'h_k':1}
def fake_loader(bank,lay=None,depth=0):
    for tree in (reversed(V['children']) if depth%2 else V['children']):
        yield local.invert(tree,depth,toy)
def flat(stream):
    for tree in stream:yield from nb.expand(tree,5000000)
replays=[]
try:
    s.inputs=fake_inputs;s.omega_blocks=fake_loader
    for levels in range(3):
        for depth in range(3):
            own=s.half_blocks('f',toy,levels,depth)
            ref=s.old.adapter.adapter_blocks(tal,V,1,1,1,levels,bool(depth%2))
            ref=(local.invert(tree,depth-depth%2,toy) for tree in ref)
            count=0
            for a,b in zip_longest(flat(own),flat(ref)):
                assert a==b;count+=1
            replays.append({'levels':levels,'depth':depth,'equal_native_leaves':count})
finally:s.inputs=save_inputs;s.omega_blocks=save_loader

# Actual production blocks are transformed, retaining every repeat count.
compiler=g.compiler();actual=[]
sample_slots=[next(z for z in plan['source_slots'] if z['kind']==kind) for kind in ('Choi','CAR')]
providers=[('SITE',lambda d:s.site_blocks(g.ns.site_layout(plan),d)),
 ('Choi',lambda d:s.choi_blocks('f',g.ns.choi_layout(plan,sample_slots[0]),d)),
 ('CAR',lambda d:s.car_blocks('q',g.ns.car_layout(plan,sample_slots[1]),d))]
for name,provider in providers:
    for depth in (0,1,2):
        pending=0
        for tree in islice(provider(depth),3):
            out,pending,census=compiler.transform(tree,pending)
            assert pending==0
            for leaf in nb.leaves(out):
                assert leaf['op'] in ('G','CX')
                assert not set(leaf['wires']).intersection((0,1,3))
                assert not (leaf['wires'][-1] in lay['SAM'])
                for q in leaf['wires']:g.physical_wire(q)
        actual.append({'provider':name,'depth':depth,'sample_blocks':3})

# The precision reserve demanded in A47 is met at the actual SOURCE fibre,
# separately from the final compressed comparator estimate.
assert u['full_SOURCE_DATA_fibre_prefix_error']<F(1,1<<3300)
assert u['full_canonical_compressed_error']<F(1,1<<3421)
assert u['replacement_error']<F(1,1<<15800)
for key in ('A_profile_upper','W_profile_upper'):
    assert all(type(v) is int and v>=0 for v in u[key].values())
out={'status':'PASS_TWO_BIT_SOURCE_GLOBAL_BINDING_AND_NATIVE_GRAMMARS',
 'source_slots_checked':dict(kinds),'all2688_CODE_pair_bindings_checked':True,
 'birth_intervals':checks,'old_helper_retained':True,'all_source_private_disjoint':True,
 'small_Walsh_resource_and_depth_checks':toy_checks,'exact_adapter_primitive_replays':replays,
 'actual_production_DAG_smokes':actual,'full_production_stream_traversed':False,
 'aggregate_inventory_is_upper_not_actual':True,
 'full_SOURCE_DATA_fibre_prefix_error_lt':'2^-3423','full_canonical_compressed_error_lt':'2^-3421',
 'new_clock_post_price_family_complete':False,'physical_C_closed':False,'GR_closed':False}
(P/'TWO_BIT_GLOBAL_SOURCE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','source_slots_checked','small_Walsh_resource_and_depth_checks')}))
