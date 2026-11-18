#!/usr/bin/env python3
"""Dynamic signed basis-pair SELECT and its paid native-adjoint grammar.

Addresses, instruction fields and leaf delta are read-only at every primitive.
Only clean logical workspace and the stated quantum DATA copies are targets.
"""
from collections import Counter
from pathlib import Path
import hashlib,importlib.util,json,sys

P=Path(__file__).resolve().parent;D=P.parent
def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
logic=load('a16_logic',D/'round13/reversible_selectors.py')
nb=load('a16_native_boolean',D/'round14/native_boolean.py')
cz=load('a16_native_cz',D/'round13/compile_native_cz.py')
dispatch=load('a16_dispatch',D/'round15/source_dispatcher.py')


def gate(op,*w):return {'op':op,'wires':list(w)}
def seq(*children):return {'op':'seq','children':list(children)}
def adjoint(tree):return {'op':'adjoint','child':tree}
def conjugate(compute,body):return seq(compute,body,adjoint(compute))
def primitive_word(word):return seq(*(gate(op,*w) for op,*w in word))


def ideal_gates(tree,reverse=False):
    op=tree['op']
    if op=='adjoint':yield from ideal_gates(tree['child'],not reverse)
    elif op=='seq':
        for child in reversed(tree['children']) if reverse else tree['children']:
            yield from ideal_gates(child,reverse)
    else:
        assert op in ('X','CX','CCX','Z','CZ','H')
        yield (op,*tree['wires'])  # all individual ideal gates self-adjoint


def logical_counts(tree):
    if tree['op']=='adjoint':return logical_counts(tree['child'])
    if tree['op']=='seq':
        out=Counter()
        for child in tree['children']:out.update(logical_counts(child))
        return out
    return Counter({tree['op']:1})


def lower(tree,k,port,spin,aux):
    op=tree['op']
    if op=='seq':return nb.seq(*(lower(t,k,port,spin,aux) for t in tree['children']))
    if op=='adjoint':return nb.inverse_literal(lower(tree['child'],k,port,spin,aux),port,spin)
    w=tree['wires']
    if op=='CX':return nb.gate('CX',*w)
    if op=='Z':return nb.z_word(w[0],port,spin)
    if op=='CZ':return nb.seq(*(nb.gate(g.op,*g.wires) for g in cz.cz_word(*w,port,spin)))
    if op in ('X','H'):return nb.boolean_word(op,k,target=w[0],port=port,spin=spin)
    assert op=='CCX'
    return nb.boolean_word('CCX',k,control=w[:2],target=w[2],aux=aux,port=port,spin=spin)


def native_resource(tree,port):
    """Actual counts distinguish G on port: essential for literal raw inverse."""
    op=tree['op']
    if op=='seq':
        out=Counter()
        for child in tree['children']:out.update(native_resource(child,port))
        return out
    if op=='repeat':return Counter({a:int(tree['count'])*b for a,b in native_resource(tree['child'],port).items()})
    if op=='G':return Counter({'G_port' if tree['wires'][0]==port else 'G_other':1})
    return Counter({op:1})


def raw_reverse_resource(c):
    g=c['G_port']+c['G_other']
    return +Counter({'G_port':g,'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*g})


def resource_ir(tree,k):
    """Every logical wire is ordinary and distinct from the dedicated port."""
    op=tree['op']
    if op=='seq':
        out=Counter()
        for t in tree['children']:out.update(resource_ir(t,k))
        return out
    if op=='adjoint':return raw_reverse_resource(resource_ir(tree['child'],k))
    return Counter({'X':{'G_other':4*k,'CX':6,'SourceI':2},
                    'H':{'G_other':2*k,'CX':6,'SourceI':2},
                    'CCX':{'G_port':6*k,'G_other':6*k,'CX':68,'SourceI':24},
                    'CX':{'CX':1},'Z':{'CX':6,'SourceI':2},'CZ':{'CX':14,'SourceI':5}}[op])


def encode_resource(c):
    return {name:str(c[name]) for name in ('G_port','G_other','CX','SourceI')}


def error_count(tree):
    c=logical_counts(tree);return c['X']+c['H']+c['CCX']


def equality_toggle(data,label,m,diff,work):
    """m ^= [data==label], copying differences into clean work, no data flips."""
    assert len(data)==len(label)==len(diff)
    compute=seq(*(gate('CX',source,target) for x,a,t in zip(data,label,diff) for source,target in [(x,t),(a,t)]))
    predicate=primitive_word(logic.pattern_gate(diff,0,m,work))
    return conjugate(compute,predicate)


def pair_ir(data,a,b,h,delta,m,diff,work,q):
    """Target: controlled T_ab, sign (-1)^delta outside {a,b}.

    For a=b the extension is (-1)^delta I in the h=1 sector. On valid A11
    instructions a!=b. Workspace m/diff/work/q must enter computational zero.
    """
    n=len(data)
    assert n>=2 and len(a)==len(b)==len(diff)==n and len(work)>=n-2
    roles=data+a+b+[h,delta,m]+diff+work+[q]
    assert len(roles)==len(set(roles))
    member=seq(equality_toggle(data,a,m,diff,work),equality_toggle(data,b,m,diff,work))
    # Membership is the XOR of the two equalities. Individual flags are not
    # retained, because they would exchange when the DATA pair is swapped.
    sign=conjugate(gate('CCX',h,delta,q),seq(gate('Z',q),gate('CZ',q,m)))
    flip=seq(*(gate('CCX',q,label,x) for x,aa,bb in zip(data,a,b) for label in [aa,bb]))
    swap=conjugate(gate('CCX',h,m,q),flip)
    return conjugate(member,seq(sign,swap))


def pair_plan(n):
    l=dispatch.Layout();q={}
    for name,width in [('data',n),('a',n),('b',n),('h',1),('delta',1),('membership',1),('diff',n),('work',n-2),('phase_work',1)]:q[name]=l.new(width)
    tree=pair_ir(q['data'],q['a'],q['b'],q['h'][0],q['delta'][0],q['membership'][0],q['diff'],q['work'],q['phase_work'][0])
    return {'n':n,'wire_count':l.n,'layout':q,'logical_IR':tree}


def instruction_plan(degree):
    """One complete A15 instruction, all valid physical copies enumerated."""
    nc,nq=degree;l=dispatch.Layout()
    record=l.new(65);fields=dispatch.split_wires(record,[1,9,7,2,2,22,22])
    q=dict(zip(['negative','leaf','coffset','qoffset','kind','a','b'],fields))
    q['h']=l.new(1);q['choi']=[l.new(22) for _ in range(nc)]
    q['car']=[l.new(12) for _ in range(nq)]
    q['CAR_RIGHT']=[l.new(7) for _ in range(nq)]
    q['delta_choi']=l.new(nc);q['delta_car']=l.new(nq)
    for name,width in [('enabled',1),('enable_work',8),('membership',1),('diff',22),('member_work',20),('phase_work',1),('constant_work',1)]:q[name]=l.new(width)
    phase=conjugate(gate('CCX',q['h'][0],q['negative'][0],q['constant_work'][0]),gate('Z',q['constant_work'][0]))
    calls=[]
    for kind,offset,copies,deltas in [(1,q['coffset'],q['choi'],q['delta_choi']),(2,q['qoffset'],q['car'],q['delta_car'])]:
        controls=q['h']+q['kind']+offset
        for i,data in enumerate(copies):
            pattern=1|(kind<<1)|(i<<3)
            # h is first and positive, retaining exact h=0 inactive structure.
            enable=primitive_word(logic.pattern_gate(controls,pattern,q['enabled'][0],q['enable_work']))
            n=len(data)
            pair=pair_ir(data,q['a'][:n],q['b'][:n],q['enabled'][0],deltas[i],q['membership'][0],q['diff'][:n],q['member_work'][:n-2],q['phase_work'][0])
            calls.append({'kind':kind,'copy':i,'n':n,'IR':conjugate(enable,pair)})
    return {'degree':degree,'wire_count':l.n,'layout':q,'constant_phase_IR':phase,'copy_calls':calls,
            'copy_records_and_delta_read_only':True,'CAR_RIGHT_identity':True}


def instruction_ir(plan):return seq(plan['constant_phase_IR'],*(c['IR'] for c in plan['copy_calls']))


def count_instruction(plan,k):
    c=Counter();r=Counter();e=0
    for tree in [plan['constant_phase_IR']]+[t['IR'] for t in plan['copy_calls']]:
        c.update(logical_counts(tree));r.update(resource_ir(tree,k));e+=error_count(tree)
    return c,r,e


def map_ir(tree,mapping):
    op=tree['op']
    if op=='seq':return seq(*(map_ir(t,mapping) for t in tree['children']))
    if op=='adjoint':return adjoint(map_ir(tree['child'],mapping))
    return gate(op,*(mapping[i] for i in tree['wires']))


def walk_test_events(name,tables=None):
    """A15 chronological controller followed by real conditional source SELECT.

    The caller supplies the actual Choi/CAR banks and prepared fair/zero/Golden
    inputs. Different walks alias the common external SITE and otherwise use
    disjoint registers; the whole birth/clock assembler is still external.
    """
    if tables is None:tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text())
    records=[];end=None
    for event in dispatch.walk_events(tables,name):
        if event['kind']=='transition':records.append([event['map'][i] for i in event['plan']['layout']['record']])
        if event['kind']=='end':end=event
        else:yield {'kind':'controller','event':event}
    assert end is not None
    root=tables['roots'][name];plan=instruction_plan(root['degree']);l=dispatch.Layout();l.n=end['allocated_wires']
    # A single workspace/data/delta layout is used for all fixed slots.
    local_record=sum([plan['layout'][key] for key in ['negative','leaf','coffset','qoffset','kind','a','b']],[])
    mapping=dispatch.bind_layout(l,plan,[(local_record,records[0])])
    h=mapping[plan['layout']['h'][0]]
    yield {'kind':'quantum','role':'prepare_hadamard','IR':gate('H',h),'allocated_wires':l.n}
    constant=mapping[plan['layout']['constant_work'][0]]
    root_phase=conjugate(gate('CCX',h,end['top_identity_phase'][0],constant),gate('Z',constant))
    yield {'kind':'quantum','role':'top_identity_phase','IR':root_phase,'allocated_wires':l.n}
    for slot,record in enumerate(records):
        m=list(mapping)
        for a,b in zip(local_record,record):m[a]=b
        yield {'kind':'quantum','role':'constant_phase','slot':slot,'IR':map_ir(plan['constant_phase_IR'],m),'allocated_wires':l.n}
        for call in plan['copy_calls']:
            yield {'kind':'quantum','role':'copy_SELECT','slot':slot,'copy':call['copy'],'copy_kind':call['kind'],'IR':map_ir(call['IR'],m),'allocated_wires':l.n}
    yield {'kind':'quantum','role':'readout_hadamard','IR':gate('H',h),'allocated_wires':l.n}
    yield {'kind':'quantum','role':'report_sign_convention','IR':gate('X',h),'allocated_wires':l.n}
    q=plan['layout']
    yield {'kind':'end','allocated_wires':l.n,'source_sign_wire':h,
           'sign_convention':'1 means +1; 0 means -1, matching A12 report mask',
           'external_SITE':end['external_SITE'],
           'Choi_copies':[[mapping[i] for i in wires] for wires in q['choi']],
           'CAR_copies':[[mapping[i] for i in wires] for wires in q['car']],
           'CAR_RIGHT':[[mapping[i] for i in wires] for wires in q['CAR_RIGHT']],
           'leaf_delta_wires':[mapping[i] for i in q['delta_choi']+q['delta_car']],
           'all_READY_flags_untouched_by_SELECT':True}


def walk_native_blocks(name,k):
    """Complete lazy native gate-block grammar of controller plus source test.

    No banks or RAW births are silently supplied. The block stream includes
    billions of controller replacements and is not claimed to have run.
    """
    tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text())
    previous=json.loads((D/'round15/SOURCE_DISPATCH_COMPILATION.json').read_text())
    angle=json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())
    assert k==int(angle['k'])
    local=instruction_plan(tables['roots'][name]['degree'])
    size=previous['walks'][name]['walk_logical_wire_count']+local['wire_count']-65
    port=size;spin=(size+1,size+2);aux=size+3
    for event in walk_test_events(name,tables):
        if event['kind']=='controller':
            for op,*w in dispatch.event_word(event['event'],tables):yield lower(gate(op,*w),k,port,spin,aux)
        elif event['kind']=='quantum':yield lower(event['IR'],k,port,spin,aux)
        else:
            assert event['kind']=='end' and event['allocated_wires']==size


def main():
    angle=json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text());k=int(angle['k'])
    templates={}
    for n in (12,22):
        plan=pair_plan(n);size=plan['wire_count'];native=lower(plan['logical_IR'],k,size,(size+1,size+2),size+3)
        nb.validate_schema(native,size+5,size,(size+1,size+2),(size+4,))
        resource=native_resource(native,size)
        assert resource==resource_ir(plan['logical_IR'],k)
        reverse=nb.inverse_literal(native,size,(size+1,size+2))
        assert native_resource(reverse,size)==raw_reverse_resource(resource)
        templates[str(n)]={**plan,'native_forward_DAG':native,'native_literal_reverse_DAG':reverse,
            'native_layout':{'port':size,'spin':[size+1,size+2],'aux':size+3,'oldRIGHT':size+4},
            'logical_gate_counts':dict(logical_counts(plan['logical_IR'])),'approximate_occurrences':error_count(plan['logical_IR']),
            'native_forward_resources':encode_resource(resource),'native_raw_inverse_resources':encode_resource(raw_reverse_resource(resource))}
    (P/'DYNAMIC_PAIR_LIBRARY.json').write_text(json.dumps({'k':str(k),'templates':templates},separators=(',',':'))+'\n')
    tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());walks={};total_logical=Counter();total_resource=Counter();total_error=0
    previous=json.loads((D/'round15/SOURCE_DISPATCH_COMPILATION.json').read_text())
    for name,root in tables['roots'].items():
        plan=instruction_plan(root['degree']);logical,resource,error=count_instruction(plan,k)
        # Two H, one X for A12 bit convention, and top negative-identity phase.
        overhead=seq(gate('H',0),gate('H',0),gate('X',0),conjugate(gate('CCX',0,1,2),gate('Z',2)))
        lc=Counter({op:n*root['slots'] for op,n in logical.items()});lc.update(logical_counts(overhead))
        rc=Counter({op:n*root['slots'] for op,n in resource.items()});rc.update(resource_ir(overhead,k))
        ec=error*root['slots']+error_count(overhead)
        times=2 if name.startswith('H_f') else 8
        total_logical.update({op:times*n for op,n in lc.items()});total_resource.update({op:times*n for op,n in rc.items()});total_error+=times*ec
        walks[name]={'root':root,'instruction_logical_counts':dict(logical),'instruction_error_macros':error,
                     'walk_SELECT_test_logical_counts':dict(lc),'walk_SELECT_test_error_macros':ec,
                     'walk_SELECT_test_native_resources':encode_resource(rc),'walk_SELECT_test_literal_reverse_resources':encode_resource(raw_reverse_resource(rc)),
                     'chronological_grammar':'walk_test_events: A15 controller; H; top phase; each fixed instruction/copy SELECT; H; X sign convention',
                     'local_instruction_wire_count':plan['wire_count'],
                     'walk_logical_wires':previous['walks'][name]['walk_logical_wire_count']+plan['wire_count']-65,
                     'walk_native_wires_including_protected_oldRIGHT_witness':previous['walks'][name]['walk_logical_wire_count']+plan['wire_count']-60}
    # A15/A13/B31 counts are separate and must be included exactly once.
    old=json.loads((D/'round15/PREPROCESSOR_READY_COMPOSITION.json').read_text())['seven_report_known_approximate_macros']['sum']
    combined=old+7*total_error;bits=combined.bit_length()
    result={'status':'FINITE_DYNAMIC_SOURCE_SELECT_AND_HADAMARD_TARGET_TEST','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inputs_sha256':{str(f.relative_to(D)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [D/'round15/source_dispatcher.py',D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round15/SOURCE_DISPATCH_COMPILATION.json',D/'round15/PREPROCESSOR_READY_COMPOSITION.json',D/'round14/native_boolean.py',D/'round14/NATIVE_BOOLEAN_ANGLE.json',D/'round13/compile_native_cz.py']},
        'walks':walks,'one_report_SELECT_test_logical_counts':dict(total_logical),'one_report_SELECT_test_approximate_macros':total_error,
        'one_report_SELECT_test_native_resources':encode_resource(total_resource),
        'one_report_SELECT_test_literal_reverse_resources':encode_resource(raw_reverse_resource(total_resource)),
        'seven_report_all_known_approximate_macros':combined,'seven_report_all_known_error_strictly_below':f'2^-{4096-bits}',
        'compute_blocks_reversed_by_actual_native_adjoint':True,
        'instruction_addresses_and_delta_read_only_every_native_primitive':True,
        'h_zero_exact_inactive_on_clean_workspace_for_SELECT_only':True,
        'quantum_banks_prepared_here':False,'global_birth_clock_assembler_emitted':False,
        'full_H1_writer_emitted':False,'full_source_alpha_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'SOURCE_SELECT_COMPILATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['status','one_report_SELECT_test_logical_counts','seven_report_all_known_error_strictly_below']}))


if __name__=='__main__':main()
