#!/usr/bin/env python3
"""Exact structural and literal logical checks for the retained dispatcher."""
from collections import Counter
from pathlib import Path
import importlib.util,json,random,sys
import source_dispatcher as s

P=Path(__file__).resolve().parent
rng=random.Random(15031)
tables=json.loads((P/'SOURCE_DISPATCH_TABLES.json').read_text())
compiled=json.loads((P/'SOURCE_DISPATCH_COMPILATION.json').read_text())
dag,binding,palette=s.inputs();nodes=dag['nodes']
assert s.digest(P/'SOURCE_DISPATCH_TABLES.json')==compiled['table_sha256']
for rel,value in tables['inputs'].items():assert s.digest(P.parent/rel)==value
spec=importlib.util.spec_from_file_location('a15_owner_mass',P.parent/'round12/compile_source_selectors.py')
mass_module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mass_module;spec.loader.exec_module(mass_module)


def indices(rows):
    out={}
    for width,key,value in rows:
        assert 0<=key<1<<width and (width,key) not in out
        out[width,key]=value
    return out


ti=indices(tables['transition_rows']);pi=indices(tables['palette_rows']);ai=indices(tables['address_rows'])


def evaluate_transition(node,choice,ready):
    key=node | (choice<<15) | (ready<<21)
    code=ti.get((15,node),0)^ti.get((22,key),0)
    out=s.unpack(code,s.TRANS_WIDTHS);out[0]^=1
    assert out[0] and out[0]&(out[0]-1)==0
    return out


def reference(node,choice,ready):
    if node==0:return 0,0,0,[]
    n=nodes[node-1];op=n['op']
    if op=='add':args=[n['args'][choice]] if ready and choice<len(n['args']) else []
    elif op=='mul':args=n['args']
    else:args=[]
    negative=int(op=='const' and mass_module.K(n['a'],n['b']).sign()<0)
    leaf=next((i+1 for i,t in enumerate(binding['leaf_templates']) if t['node']==node-1),0)
    c=q=0;children=[]
    for j in args:
        children.append((j+1,c,q))
        if op=='mul':c+=nodes[j]['degree'][0];q+=nodes[j]['degree'][1]
    return len(args),negative,leaf,children


# All transition rows, and all abort/out-of-range choices at each add.
local_checks=0
reachable=sorted(set((key & 32767) for width,key in ti))
for node in reachable:
    n=nodes[node-1]
    cases=[(j,r) for j in range(64) for r in (0,1)] if n['op']=='add' else [(0,0),(63,1)]
    for choice,ready in cases:
        push,negative,leaf,children=reference(node,choice,ready)
        out=evaluate_transition(node,choice,ready)
        expected=[1<<push,negative,leaf]+sum([list(x) for x in children],[])+[0,0,0]*(4-push)
        assert out==expected,(node,choice,ready)
        local_checks+=1
    assert pi.get((15,node),0)==int(palette['node_to_palette'].get(str(node-1),0))
assert evaluate_transition(0,63,0)==[1]+[0]*14

# Every SITE/leaf binding, including CAR a!=0, full grade 15 and Choi padding.
address_checks=0
for site in binding['site_bindings']:
    for li,(leaf,address) in enumerate(zip(binding['leaf_templates'],site['leaf_addresses_in_template_order'])):
        kind,a,b=s.unpack(ai[17,site['SITE_index']|((li+1)<<8)],s.ADDRESS_WIDTHS)
        if leaf['kind']=='Choi':
            assert kind==1 and a==0
            assert b//1024==address and (b//32)%32==leaf['input'] and b%32==leaf['output']
        else:
            assert kind==2 and a//16==b//16==address
            assert [a%16,b%16]==leaf['cross_masks']
        address_checks+=1

# Reachable placements: ranges are inside the declared tensor copies. This
# explores all add alternatives without enumerating exponentially many walks.
placement_checks=0
for name,root in tables['roots'].items():
    stack=[(root['node'],0,0)];seen=set();limit=root['degree']
    while stack:
        node,c,q=stack.pop()
        if (node,c,q) in seen:continue
        seen.add((node,c,q));n=nodes[node-1]
        assert c+n['degree'][0]<=limit[0] and q+n['degree'][1]<=limit[1]
        placement_checks+=1
        if n['op']=='add':stack.extend((j+1,c,q) for j in n['args'])
        elif n['op']=='mul':
            dc=dq=0
            for j in n['args']:
                stack.append((j+1,c+dc,q+dq));dc+=nodes[j]['degree'][0];dq+=nodes[j]['degree'][1]

# Exhaust every bit pattern of the 7-bit addition primitive, not float values.
addition_cases=0
for width in (2,7):
    a=list(range(width));b=list(range(width,2*width));out=list(range(2*width,3*width));carry=list(range(3*width,4*width))
    word=list(s.xor_add_word(a,b,out,carry))
    for x in range(1<<width):
        for y in range(1<<width):
            initial=x | (y<<width)
            state=s.logic.apply_word(word,initial)
            assert s.logic.get(state,a)==x and s.logic.get(state,b)==y
            assert s.logic.get(state,out)==(x+y)%(1<<width)
            assert s.logic.get(state,carry)==0
            addition_cases+=1

# Small full QROM truth tables, with arbitrary nonzero XOR outputs.
qrom_cases=0
for width in range(1,8):
    controls=list(range(width));outputs=list(range(width,width+5));flag=width+5;work=list(range(width+6,2*width+6))
    rows=[[width,k,(3*k+5)%32] for k in range(1<<width)]
    word=list(s.lookup_word(rows,controls,outputs,flag,work))
    for x in range(1<<width):
        y=rng.randrange(32);initial=x|(y<<width)
        state=s.logic.apply_word(word,initial)
        assert s.logic.get(state,outputs)==y^((3*x+5)%32)
        assert s.logic.get(state,controls)==x and s.logic.get(state,[flag]+work)==0
        qrom_cases+=1
    assert Counter(g[0] for g in word)==s.lookup_counts(rows)


def table_step(stack,choice,ready,depth):
    node,c,q=stack[0];out=evaluate_transition(node,choice,ready);k=out[0].bit_length()-1
    children=[(out[3+3*i],c+out[4+3*i],q+out[5+3*i]) for i in range(k)]
    new=(children+stack[1:]+[(0,0,0)]*depth)[:depth]
    return new,(out[1],out[2],c,q)


# Fixed padded walks, including deliberately aborted slots and all top labels.
walk_checks=0
for name,root in tables['roots'].items():
    depth=root['stack_depth']
    for trial in range(300):
        top=trial%4;stack=[(root['node'],0,0) if top==0 else (0,0,0)]+[(0,0,0)]*(depth-1)
        used=set();pending=[] if top else [(root['node'],0,0)]
        for slot in range(root['slots']):
            node,c,q=stack[0]
            assert (node,c,q)==(pending[0] if pending else (0,0,0))
            n=nodes[node-1] if node else None
            choice=rng.randrange(len(n['args'])) if n and n['op']=='add' else 0
            ready=int(trial%5!=0 or slot%7!=0)
            new,rec=table_step(stack,choice,ready,depth)
            if pending:
                pending.pop(0)
                push,neg,leaf,children=reference(node,choice,ready)
                pending=[(j,c+dc,q+dq) for j,dc,dq in children]+pending
                assert len(pending)<=depth
                if leaf:
                    typ=binding['leaf_templates'][leaf-1]['kind'];copy=c if typ=='Choi' else q
                    assert (typ,copy) not in used;used.add((typ,copy))
            assert new[:len(pending)]==pending
            stack=new
        assert not pending and not any(any(frame) for frame in stack)
        walk_checks+=1

# Fully execute two ACTUAL table-based step circuits. These exercise arbitrary
# retained tails as bit strings; semantic validity is only needed for overflow.
literal=[]
cases=[]
mul=next(i+1 for i,n in enumerate(nodes) if n['op']=='mul' and len(n['args'])==4 and (15,i+1) in ti)
car=binding['leaf_templates'][-1]['node']+1
for node,choice,ready,site,c,q in [(mul,0,1,129,3,0),(car,0,1,247,0,1)]:
    plan=s.step_plan(11);w=plan['layout'];initial=0
    frames=[(node,c,q)]+[(rng.randrange(1,20000),rng.randrange(80),rng.randrange(2)) for _ in range(10)]
    for wires,frame in zip(w['old_stack'],frames):initial=s.logic.put(initial,wires,s.pack(frame,s.FRAME_WIDTHS))
    for key,value in [('choice',choice),('ready',ready),('site',site)]:initial=s.logic.put(initial,w[key],value)
    # The address must use the transition leaf, not the old XOR record.
    dirty_record=rng.getrandbits(len(w['record']))
    initial=s.logic.put(initial,w['record'],dirty_record)
    counts=Counter();readonly=set(sum(w['old_stack'],[])+w['choice']+w['ready']+w['site'])
    def checked_word():
        for gate in s.palette_word(plan,tables):
            assert gate[-1] not in readonly;counts[gate[0]]+=1;yield gate
        for gate in s.transition_word(plan,tables):
            assert gate[-1] not in readonly;counts[gate[0]]+=1;yield gate
    actual=s.logic.apply_word(checked_word(),initial)
    expected,rec=table_step(frames,choice,ready,11)
    for wires,frame in zip(w['new_stack'],expected):assert s.logic.get(actual,wires)==s.pack(frame,s.FRAME_WIDTHS)
    address=ai.get((17,site|(rec[1]<<8)),0)
    assert s.logic.get(actual,w['record'])==dirty_record^s.pack(list(rec)+s.unpack(address,s.ADDRESS_WIDTHS),plan['record_widths'])
    assert s.logic.get(actual,w['palette'])==pi.get((15,node),0)
    for key in ['transition','flag','pattern_work','carries']:
        assert s.logic.get(actual,w[key])==0,key
    assert s.logic.get(actual,sum(w['children'],[]))==0
    for wire in readonly:assert ((actual^initial)>>wire)&1==0
    assert dict(counts)==s.step_counts(plan,tables),(counts,s.step_counts(plan,tables))
    literal.append({'node':node,'SITE':site,'gate_count':sum(counts.values()),'counts':dict(counts)})
    print('PASS literal full step',node,flush=True)

# Inspect every chronological stage map: shared palette, per-attempt coins,
# retained first-success outputs, and the exact fixed number of steps.
stage_counts={}
for name,root in tables['roots'].items():
    counts=Counter();old_max=0;last=None
    for e in s.walk_events(tables,name):
        counts[e['kind']]+=1
        assert e['allocated_wires']>=old_max;old_max=e['allocated_wires']
        if 'map' in e:
            assert len(e['map'])==len(set(e['map']))==e['plan']['wire_count']
            assert min(e['map'])>=0 and max(e['map'])<e['allocated_wires']
        if e['kind']=='transition':
            q=e['plan']['layout'];last=[[e['map'][i] for i in f] for f in q['new_stack']]
        if e['kind']=='palette' and e['slot']>0:
            q=e['plan']['layout'];assert [[e['map'][i] for i in f] for f in q['old_stack']]==last
    assert counts['selector']==7*(root['slots']+1)
    assert counts['first_success']==root['slots']+1
    assert counts['palette']==counts['transition']==root['slots']
    assert old_max==compiled['walks'][name]['walk_logical_wire_count']
    stage_counts[name]=dict(counts)

out={'status':'PASS_EXACT_DISPATCHER_COMPONENT_AND_COMPOSITION_CHECKS',
     'inputs':{'source_dispatcher.py':s.digest(P/'source_dispatcher.py'),'SOURCE_DISPATCH_TABLES.json':s.digest(P/'SOURCE_DISPATCH_TABLES.json'),'SOURCE_DISPATCH_COMPILATION.json':s.digest(P/'SOURCE_DISPATCH_COMPILATION.json')},
     'local_transition_cases':local_checks,'SITE_leaf_addresses':address_checks,
     'all_reachable_node_copy_placements':placement_checks,'exhaustive_addition_cases':addition_cases,
     'exhaustive_small_QROM_cases':qrom_cases,'padded_walk_cases':walk_checks,
     'literal_actual_full_steps':literal,'chronological_stages':stage_counts,
     'all_full_walk_gates_executed':False,'native_bank_SELECT_implemented':False,
     'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'SOURCE_DISPATCH_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['inputs','literal_actual_full_steps','chronological_stages']}))
