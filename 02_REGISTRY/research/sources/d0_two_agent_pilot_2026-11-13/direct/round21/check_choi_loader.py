#!/usr/bin/env python3
"""All-source namespace/coverage checks and exact lazy-adapter integration."""
from pathlib import Path
from collections import Counter
from itertools import islice,zip_longest
import hashlib,json
import choi_loader as c
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((P/'CHOI_LOADER_PLAN.json').read_text());x=c.inputs();lay=c.layout();al=c.adapter_layout(lay)
for p,digest in plan['source_and_library_sha256'].items():assert h(Path(p))==digest,p
assert json.loads((P/'ROOT_REVIEW_B42.json').read_text())['internal_depth2_and_outer_depth3_price_bug_fixed_and_replayed']
assert plan['layout']==lay and plan['B39_adapter_layout']==al
readonly=set(lay['SAM']+[lay['branch']]);forbidden={lay['phase_rebit'],*lay['comparator_scratch'],lay['oldRIGHT_witness']}
select_readonly=readonly|set(lay['address']);protected_select=forbidden|set(lay['choi_input'])
prefix_count=0
for block in c.prefix.prefix_blocks(x['prefix'],lay,True):
    c.adapter.validate_loader(al,block,lay['SAM'])
    for leaf in c.nb.leaves(block):
        assert not set(leaf['wires'])&forbidden
        if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in readonly
    prefix_count+=1

# Existing A20 and B42 primitive bindings keep their identical wire numbers;
# the former only adds untouched B39 rebit/comparator to its declared size.
oldlay=c.coframe.layout()
for key in ('SAM','address','choi_input','choi_output','branch','port','spin','aux_arbitrary','oldRIGHT_witness'):assert oldlay[key]==lay[key]
linklay=c.link.prefix_compatible_global_layout()
for key,value in linklay.items():assert lay[key]==value,(key,'B42 namespace mismatch')
cat=c.coframe.t.loc.catalogue();coverage={};cf_units=0;link_commands=0;maxK=0
families={f['family']:f for f in x['link']['families']}
for bank in ('y+','y-','f','0','x+','x-','q'):
    expected={kind:set() for kind in ('inverse_coframe_column','proper_link')}
    for row in c.coframe.t.loc.sectors(cat[bank]):
        if row['kind'] in expected:expected[row['kind']].add((row['a'],tuple(row['SAM_indices']),tuple(row['SAM_pattern'])))
    for stage,kind in [('coframe','inverse_coframe_column'),('link','proper_link')]:
        rows=x[stage]['catalogue'][bank]
        actual={(row['address'],tuple(row['SAM_indices']),tuple(row['SAM_pattern'])) for row in rows}
        assert actual==expected[kind] and len(actual)==len(rows)
    assert {r[0] for r in expected['inverse_coframe_column']}==set(range(1,1025))
    assert {r[0] for r in expected['proper_link']}==set(range(1025,2049))
    for row in x['coframe']['catalogue'][bank]:
        for bound,depth in c.coframe.sector_units(row,x['coframe'],lay):
            wires=set(bound['controls']+[bound['target']]);assert not wires&protected_select
            assert bound['target'] not in select_readonly
            assert not any(g['wires'][-1] in select_readonly or set(g['wires'])&protected_select for g in bound['permutation'])
            cf_units+=1
    for row in x['link']['catalogue'][bank]:
        local=c.link.bind_global(lay,row)
        for cmd in c.link.commands(local,row,families[row['family_id']],x['link']['controlled_X']):
            wires=set(cmd['controls']+[cmd['target']]);assert not wires&protected_select
            assert cmd['target'] not in select_readonly
            if cmd['kind']=='fock':assert {cmd['cx_control'],cmd['cx_target']}<=set(lay['modes'])
            assert len(cmd['controls'])<=23
            maxK=max(maxK,len(cmd['controls']));link_commands+=1
    coverage[bank]={'coframe':len(expected['inverse_coframe_column']),'link':len(expected['proper_link']),'anchor':1,'padding':2047}
assert cf_units==294144 and maxK==23

# B39 fixed blocks on the new actual namespace have the original inventories.
fixed=c.adapter.fixed(al,int(x['phase']['phase_k']),int(x['phase']['correction_l']),x['h_k'])
for tree in [fixed['H'],*fixed['good'],*fixed['start'],fixed['correction']]:
    c.nb.validate_schema(tree,lay['qubits'],lay['port'],tuple(lay['spin']),(lay['oldRIGHT_witness'],))
    for leaf in c.nb.leaves(tree):assert not set(leaf['wires'])&set(lay['SAM'])
for bank in coverage:
    cv,cv_inv,half,half_inv=c.counts(bank)
    assert +cv_inv==+c.adapter.raw_inverse_counts(cv)
    assert +half_inv==+c.adapter.raw_inverse_counts(half)
c.error_bounds()

# Compare the adapted provider grammar to B39's original one-DAG interface
# using a completely specified native toy controlled rotation. This tests
# actual emitted primitive order, including every nested literal inversion.
toy={'SAM':[],'address':[],'choi_input':[],'choi_output':[1],'branch':0,'phase_rebit':2,
     'comparator_scratch':[3],'port':4,'spin':[5,6],'aux_arbitrary':7,'oldRIGHT_witness':8,'qubits':9}
tal=c.adapter_layout(toy)
V=c.nb.selective_rotation([0],[1],1,1,4,(5,6))
saved_inputs=c.inputs;saved_loader=c.omega_blocks
def toy_loader(bank,lay=None,inverse_depth=0):
    parts=V['children']
    for tree in (reversed(parts) if inverse_depth%2 else parts):yield c.inverted(tree,inverse_depth,toy)
def flattened(blocks):
    for tree in blocks:yield from c.nb.expand(tree,5000000)
def compare(a,b):
    count=0
    for left,right in zip_longest(a,b):assert left==right,(count,left,right);count+=1
    return count
toy_reports=[]
try:
    c.inputs=lambda:{'phase':{'phase_k':'1','correction_l':'1'},'h_k':1};c.omega_blocks=toy_loader
    for levels in range(3):
        for depth in range(3):
            own=c.half_blocks('f',toy,levels,inverse_depth=depth)
            original=c.adapter.adapter_blocks(tal,V,1,1,1,levels=levels,reverse=bool(depth%2))
            reference=(c.inverted(tree,depth-depth%2,toy) for tree in original)
            leaves=compare(flattened(own),flattened(reference))
            toy_reports.append({'levels':levels,'outer_inverse_depth':depth,'actual_primitive_leaves_equal_to_B39':leaves})
finally:c.inputs=saved_inputs;c.omega_blocks=saved_loader

# B35 U private anchor and its OUTER predicate require disjoint wires.
private=plan['half_vector_private_clean_wires'];outer_flag=2739;outer_work=list(range(2740,2784))
joint=al['data']+private
assert len(joint)==len(set(joint))==46 and len(outer_work)==44
assert not set(joint+[lay['port'],*lay['spin'],lay['aux_arbitrary'],lay['oldRIGHT_witness']])&{outer_flag,*outer_work}
out={'status':'PASS_COMPLETE_OMEGA_AND_B39_PROVIDER_INTEGRATION',
     'plan_sha256':h(P/'CHOI_LOADER_PLAN.json'),'checker_sha256':h(Path(__file__)),
     'all_bank_coverage':coverage,'actual_prefix_blocks_checked':prefix_count,
     'all_coframe_bound_units_checked':cf_units,'all_proper_link_commands_checked':link_commands,'max_link_controls':maxK,
     'actual_existing_provider_wire_numbers_unchanged':True,'phase_rebit_comparator_and_oldRIGHT_exact_loader_spectators':True,
     'B39_provider_vs_original_DAG_exact_primitive_replays':toy_reports,
     'full_controlled_Omega_operator_error_lt':'2^-3250','half_vector_anchor_isometry_error_lt':'2^-3230',
     'half_private_clean_wires':24,'outer_B35_joint_anchor_width':46,'outer_B35_comparator_requires_45_additional_wires':True,
     'full_giant_word_executed':False,'outer_B35_reflection_compiled':False,'physical_H1_admission_and_Cost_Info_proved':False,
     'physical_C_closed':False,'GR_closed':False}
(P/'CHOI_LOADER_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'source_sectors':sum(v['coframe']+v['link'] for v in coverage.values()),'B39_exact_provider_replays':len(toy_reports)}))
