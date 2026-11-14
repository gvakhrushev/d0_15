#!/usr/bin/env python3
"""Stream A17's actual report or its literal inverse without a giant list.

Logical `reverse` below reverses the ORDER of an existing tuple stream; it
does not cancel paid native adjoints. Actual native inversions always retain
their integer depth and operate on the already lowered primitive DAG.
The two finite controller event sequences, their maps, source tables and
bounded predicates are cached. Memory is independent of the expanded native
primitive count; it is NOT constant memory or a one-event streaming bound.
"""
from pathlib import Path
from functools import lru_cache
import importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sp=importlib.util.spec_from_file_location('a25_report',D/'round17/report_assembly.py');a=importlib.util.module_from_spec(sp);sys.modules[sp.name]=a;sp.loader.exec_module(a)
s=a.s;d=s.dispatch;logic=s.logic;nb=s.nb
def ordered(xs,reverse=False):return reversed(xs) if reverse else iter(xs)
def small(word,reverse=False):yield from ordered(list(word),reverse)
def prefix_word(plan,reverse=False):
    q=plan['layout'];outputs=q['kind']+q['rank']
    for raw,kind,rank in ordered(plan['prefix_codes'],reverse):
        code=kind|(rank<<1)
        for bit in ordered(range(len(outputs)),reverse):
            if code>>bit&1:yield from small(logic.pattern_gate(q['golden'],raw,outputs[bit],q['pattern_work']),reverse)
def row_word(plan,row,reverse=False):
    q=plan['layout'];flag=q['row_flag'][0];controls=q['palette']+q['kind'];pattern=row['palette']|(row['kind']<<len(q['palette']))
    selector=list(logic.pattern_gate(controls,pattern,flag,q['pattern_work']))
    # S C O C^rev S^rev reverses to S C O^rev C^rev S^rev;
    # only the boundary order and O order reverse.
    yield from selector
    for threshold,mask in ordered(row['boundaries'],reverse):
        compute=list(logic.compare_xor(q['fair']+q['rank'],int(threshold),q['less'][0],q['borrows']))
        yield from compute
        for i in ordered(range(len(q['output'])),reverse):
            if mask>>i&1:yield ('CCX',flag,q['less'][0],q['output'][i])
        yield from reversed(compute)
    yield from reversed(selector)
def selector_word(plan,reverse=False):
    yield from prefix_word(plan)
    for row in ordered(plan['rows'],reverse):yield from row_word(plan,row,reverse)
    yield from prefix_word(plan,True)
def lookup_word(rows,controls,outputs,flag,work,reverse=False,base_rows_reversed=False):
    for width,key,value in ordered(rows,bool(reverse)^bool(base_rows_reversed)):
        if not value:continue
        predicate=list(logic.pattern_gate(controls[:width],key,flag,work));yield from predicate
        for bit in ordered(range(len(outputs)),reverse):
            if value>>bit&1:yield ('CX',flag,outputs[bit])
        yield from reversed(predicate)
def output_small(plan):
    q=plan['layout'];fields=d.split_wires(q['transition'],d.TRANS_WIDTHS);push,negative,leaf=fields[:3]
    for i,dest in enumerate(q['new_stack']):
        for count in range(5):
            if i<count:source=q['children'][i]
            else:
                index=i+1-count
                if index>=plan['depth']:continue
                source=q['old_stack'][index]
            for a0,b0 in zip(source,dest):yield ('CCX',push[count],a0,b0)
    rec=d.split_wires(q['record'],plan['record_widths']);old=d.split_wires(q['old_stack'][0],d.FRAME_WIDTHS)
    for source,dest in [(negative,rec[0]),(leaf,rec[1]),(old[1],rec[2]),(old[2],rec[3])]:
        for a0,b0 in zip(source,dest):yield ('CX',a0,b0)
def copy_outputs(plan,tables,reverse=False):
    q=plan['layout'];fields=d.split_wires(q['transition'],d.TRANS_WIDTHS);leaf=fields[2];rec=d.split_wires(q['record'],plan['record_widths'])
    def lut():return lookup_word(tables['address_rows'],q['site']+leaf,sum(rec[4:],[]),q['flag'][0],q['pattern_work'],reverse)
    if reverse:yield from lut();yield from small(output_small(plan),True)
    else:yield from output_small(plan);yield from lut()
def transition_word(plan,tables,reverse=False):
    q=plan['layout'];child=list(d.children_word(plan));controls=q['old_stack'][0][:15]+q['choice']+q['ready']
    # Preserve the ORIGINAL forward tail lookup(rows reversed, outputs
    # ascending). It is not silently identified with a literal reversal.
    stages=('X','LOOKUP','CHILD','OUTPUT','CHILD_REVERSE','LOOKUP_ROWS_REVERSE','X')
    for stage in ordered(stages,reverse):
        if stage=='X':yield ('X',q['transition'][0])
        elif stage.startswith('LOOKUP'):
            yield from lookup_word(tables['transition_rows'],controls,q['transition'],q['flag'][0],q['pattern_work'],reverse,stage=='LOOKUP_ROWS_REVERSE')
        elif stage=='OUTPUT':yield from copy_outputs(plan,tables,reverse)
        else:yield from ordered(child,bool(reverse)^(stage=='CHILD_REVERSE'))
def event_word(event,tables,reverse=False):
    kind=event['kind']
    if kind=='end':return
    if kind=='kind_init':yield from ordered(event['gates'],reverse);return
    if kind=='root_init':
        yield from lookup_word(event['rows'],event['controls'],event['outputs'],event['flag'],event['work'],reverse);return
    plan=event['plan'];q=plan['layout']
    if kind=='selector':word=selector_word(plan,reverse)
    elif kind=='first_success':word=ordered(list(logic.first_success_word(plan)),reverse)
    elif kind=='palette':word=lookup_word(tables['palette_rows'],q['old_stack'][0][:15],q['palette'],q['flag'][0],q['pattern_work'],reverse)
    else:
        assert kind=='transition';word=transition_word(plan,tables,reverse)
    yield from d.remap(word,event['map'])
@lru_cache(maxsize=2)
def walk_structure(name):
    tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());events=list(d.walk_events(tables,name))
    end=events[-1];assert end['kind']=='end';records=[[e['map'][i] for i in e['plan']['layout']['record']] for e in events if e['kind']=='transition']
    plan=s.instruction_plan(tables['roots'][name]['degree']);allocator=d.Layout();allocator.n=end['allocated_wires']
    record=sum([plan['layout'][key] for key in ('negative','leaf','coffset','qoffset','kind','a','b')],[])
    mapping=d.bind_layout(allocator,plan,[(record,records[0])]);h=mapping[plan['layout']['h'][0]];constant=mapping[plan['layout']['constant_work'][0]]
    root_phase=s.conjugate(s.gate('CCX',h,end['top_identity_phase'][0],constant),s.gate('Z',constant))
    return tables,events[:-1],records,plan,record,mapping,h,root_phase,allocator.n
def inverse(t,depth,port,spin):
    for _ in range(depth):t=nb.inverse_literal(t,port,spin)
    return t
def walk_blocks(name,k,depth=0):
    assert type(depth) is int and depth>=0
    tables,events,records,plan,record,mapping,h,root_phase,size=walk_structure(name)
    port=size;spin=(size+1,size+2);aux=size+3;reverse=bool(depth%2)
    def lower(ir):return inverse(s.lower(ir,k,port,spin,aux),depth,port,spin)
    stages=('CONTROLLER','H_BEGIN','ROOT_PHASE','SLOTS','H_END','X_END')
    for stage in ordered(stages,reverse):
        if stage=='CONTROLLER':
            for event in ordered(events,reverse):
                for op,*w in event_word(event,tables,reverse):yield lower(s.gate(op,*w))
        elif stage=='SLOTS':
            for slot in ordered(range(len(records)),reverse):
                m=list(mapping)
                for a0,b0 in zip(record,records[slot]):m[a0]=b0
                parts=[plan['constant_phase_IR'],*[call['IR'] for call in plan['copy_calls']]]
                for ir in ordered(parts,reverse):yield lower(s.map_ir(ir,m))
        elif stage=='ROOT_PHASE':yield lower(root_phase)
        else:yield lower(s.gate('X' if stage=='X_END' else 'H',h))
def ready_blocks(plan,k,depth=0):
    K=plan['READY_total_flags'];port=plan['native_port'];spin=tuple(plan['native_spin']);rev=bool(depth%2)
    stages=('COMPUTE','CORE','UNCOMPUTE')
    for stage in ordered(stages,rev):
        if stage=='CORE':
            yield inverse(a.lower_gate(plan,k,a.and_core_gate(plan)),depth,port,spin);continue
        intrinsic=int(stage=='UNCOMPUTE')
        for i in ordered(range(K-2),rev^bool(intrinsic)):
            yield inverse(a.lower_gate(plan,k,a.and_compute_gate(plan,i)),depth+intrinsic,port,spin)
def report_blocks(plan,k,depth=0):
    assert type(depth) is int and depth>=0
    angle=json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text());assert k==int(angle['k'])
    port=plan['native_port'];spin=tuple(plan['native_spin']);rev=bool(depth%2)
    stages=('ZERO','FAIR','WALKS','POST','EXTRACT','READY')
    for stage in ordered(stages,rev):
        if stage=='ZERO':
            for start,width in ordered(plan['processor_zero_ranges'],rev):
                for q in ordered(range(start,start+width),rev):yield inverse(nb.rotation_power(q,-1,port,spin),depth,port,spin)
        elif stage=='FAIR':
            bank=json.loads((a.B31/'NATIVE_FAIR_BANK.json').read_text());assert k==int(bank['k'])
            for i in ordered(range(plan['fair_bank_count']),rev):yield inverse(a.fair_bank_native(plan,i,bank),depth,port,spin)
        elif stage=='WALKS':
            for walk in ordered(plan['walks'],rev):
                def mapq(w):return a.global_wire(walk,w) if w<walk['local_wires'] else port+w-walk['local_wires']
                for t in walk_blocks(walk['root'],k,depth):yield a.remap_native(t,mapq)
        elif stage=='POST':
            post=json.loads((D/plan['postprocessor_file']).read_text());m=plan['postprocessor_map']
            for op,*w in selector_word(post,rev):yield inverse(a.lower_gate(plan,k,(op,*(m[i] for i in w))),depth,port,spin)
        elif stage=='EXTRACT':
            gates=[('CX',plan['post_READY_wire'],plan['report_wire']),('CCX',plan['post_READY_wire'],plan['post_label_wire'],plan['report_wire'])]
            for gate in ordered(gates,rev):yield inverse(a.lower_gate(plan,k,gate),depth,port,spin)
        else:yield from ready_blocks(plan,k,depth)
