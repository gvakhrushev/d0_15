#!/usr/bin/env python3
"""Compare reversed streams to the owning tuple and actual native histories."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from itertools import zip_longest
import hashlib,json
import reversible_report_stream as r
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=r.d;logic=r.logic;nb=r.nb
def pick(rows):
    return [rows[i] for i in sorted(set([*range(min(3,len(rows))),len(rows)//2,*range(max(0,len(rows)-3),len(rows))]))]
def compare(own,reference):
    n=0
    for a,b in zip_longest(own,reference):assert a==b,(n,a,b);n+=1
    return n
reports=[]
# Real control widths and real palette/prefix values, with bounded row
# samples. Every forward tuple is compared to the original owning routine;
# the reverse reference is the actual materialized bounded forward word.
for file in ('TOP_SOURCE_SELECTOR_CIRCUIT.json','INTERNAL_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json'):
    plan=json.loads((r.D/'round13'/file).read_text());plan['rows']=pick(plan['rows'])
    original=list(logic.selector_word(plan))
    for rev in (False,True):reports.append({'kind':'selector','file':file,'reverse':rev,'tuples':compare(r.selector_word(plan,rev),reversed(original) if rev else original)})
tables=json.loads((r.D/'round15/SOURCE_DISPATCH_TABLES.json').read_text())
bounded=dict(tables)
for key in ('transition_rows','palette_rows','address_rows'):bounded[key]=pick(tables[key])
event_kinds=set()
for name in tables['roots']:
    events=list(d.walk_events(tables,name))
    selected=[]
    for kind in ('kind_init','root_init','selector','first_success','palette','transition'):
        matches=[e for e in events if e['kind']==kind]
        if matches:selected.extend([matches[0],matches[-1]])
    for event in selected:
        e=deepcopy(event)
        if e['kind']=='selector':e['plan']['rows']=pick(e['plan']['rows'])
        original=list(d.event_word(e,bounded));event_kinds.add(e['kind'])
        for rev in (False,True):reports.append({'kind':e['kind'],'root':name,'reverse':rev,'tuples':compare(r.event_word(e,bounded,rev),reversed(original) if rev else original)})
assert event_kinds=={'kind_init','root_init','selector','first_success','palette','transition'}
# This specifically checks the owner's nonliteral logical-uncompute lookup
# convention, including non-palindromic order among output CX operations.
plan=d.step_plan(3);original=list(d.transition_word(plan,bounded))
assert list(r.transition_word(plan,bounded))==original and list(r.transition_word(plan,bounded,True))==list(reversed(original))

# The finite walk metadata are compared to every original controller event,
# its records and terminal allocation; giant event gate streams are not run.
walks=[]
for name in tables['roots']:
    tt,events,records,plan,record,mapping,hh,phase,size=r.walk_structure(name)
    owned=list(d.walk_events(tables,name));assert events==owned[:-1]
    original_records=[[e['map'][i] for i in e['plan']['layout']['record']] for e in owned if e['kind']=='transition'];assert records==original_records
    previous=json.loads((r.D/'round15/SOURCE_DISPATCH_COMPILATION.json').read_text())
    assert size==previous['walks'][name]['walk_logical_wire_count']+plan['wire_count']-65
    assert mapping[plan['layout']['h'][0]]==hh
    walks.append({'root':name,'controller_events':len(events),'retained_records':len(records),'native_local_size':size})

# Whole-report fixture preserves real addresses and true huge k. It replaces
# only repetition counts and two opaque providers by explicitly bounded
# actual DAGs, so all outer native ordering and literal depth can be compared
# directly to A17. No huge native G repeat is expanded.
p=json.loads((r.D/'round17/GLOBAL_REPORT_PLAN.json').read_text());p=deepcopy(p)
p['processor_zero_ranges']=[[p['processor_zero_ranges'][0][0],2]];p['fair_bank_count']=2;p['walks']=p['walks'][:2];p['READY_total_flags']=5
k=int(json.loads((r.D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']);port=p['native_port'];spin=tuple(p['native_spin'])
old=(r.a.fair_bank_native,r.s.walk_native_blocks,r.walk_blocks,r.logic.selector_word,r.selector_word)
def fair(plan,index,bank):return nb.seq(nb.repeat(k,nb.gate('G',r.a.fair_output(plan,index))),nb.gate('CX',r.a.fair_output(plan,index),plan['report_wire']))
def walk_base(name,k):
    size=r.walk_structure(name)[-1]
    return [nb.seq(nb.gate('G',8),nb.gate('SourceI',size,size+1,size+2)),nb.repeat(2,nb.gate('G',9))]
def walk_owned(name,k):yield from walk_base(name,k)
def walk_reversible(name,k,depth=0):
    size=r.walk_structure(name)[-1]
    for t in r.ordered(walk_base(name,k),bool(depth%2)):yield r.inverse(t,depth,size,(size+1,size+2))
def selector_base(plan):
    q=plan['layout'];return [('X',q['output'][0]),('CCX',q['palette'][0],q['fair'][0],q['output'][1])]
def sel_owned(plan):yield from selector_base(plan)
def sel_reversible(plan,reverse=False):yield from r.ordered(selector_base(plan),reverse)
fixture=[]
try:
    r.a.fair_bank_native=fair;r.s.walk_native_blocks=walk_owned;r.walk_blocks=walk_reversible;r.logic.selector_word=sel_owned;r.selector_word=sel_reversible
    previous=list(r.a.report_native_blocks(p,k))
    for depth in range(4):
        actual=list(r.report_blocks(p,k,depth));assert actual==previous,('report literal depth',depth)
        count=Counter()
        for t in actual:count.update(r.s.native_resource(t,port))
        fixture.append({'literal_depth':depth,'actual_native_blocks':len(actual),'compact_G_repeats_not_expanded':True})
        previous=[nb.inverse_literal(t,port,spin) for t in reversed(previous)]
finally:r.a.fair_bank_native,r.s.walk_native_blocks,r.walk_blocks,r.logic.selector_word,r.selector_word=old

out={'status':'PASS_BOUNDED_MEMORY_LITERAL_REPORT_REVERSAL','source_sha256':{str(q):h(q) for q in [Path(__file__),P/'reversible_report_stream.py',r.D/'round17/report_assembly.py',r.D/'round16/source_select.py',r.D/'round15/source_dispatcher.py',r.D/'round13/reversible_selectors.py']},
     'owning_logical_word_order_checks':reports,'original_transition_tail_order_preserved':True,'all_finite_walk_metadata_checked':walks,
     'whole_report_actual_literal_depth_fixture':fixture,'rows_in_word_tests_bounded_samples':True,
     'full_report_billions_of_blocks_enumerated':False,'giant_G_repeats_executed':False,
     'logical_order_reversal_is_not_native_inverse_cancellation':True,'physical_C_closed':False,'GR_closed':False}
(P/'REPORT_REVERSE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'word_order_checks':len(reports),'whole_report_depths':len(fixture)}))
