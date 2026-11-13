#!/usr/bin/env python3
"""Finite reversible source-DAG control, with retained state and fixed slots.

Only classical instruction computation is implemented here. Executing the
instruction on quantum source copies is a separate SELECT consumer.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib, importlib.util, json, sys

P = Path(__file__).resolve().parent
D = P.parent
spec = importlib.util.spec_from_file_location('a15_logic', D/'round13/reversible_selectors.py')
logic = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = logic
spec.loader.exec_module(logic)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    return (json.loads((D/'round11/SOURCE_TENSOR_DAG.json').read_text()),
            json.loads((D/'round11/PERIODIC_SOURCE_BINDING.json').read_text()),
            json.loads((D/'round12/INTERNAL_SELECTOR_PALETTE.json').read_text()))


def pack(values, widths):
    out = shift = 0
    for value, width in zip(values, widths):
        assert 0 <= value < 1 << width
        out |= value << shift
        shift += width
    return out


def unpack(value, widths):
    out = []
    for width in widths:
        out.append(value & ((1 << width)-1))
        value >>= width
    assert value == 0
    return out


def golden_sign(a,b):
    """Exact sign of a+b p, p=(sqrt(5)-1)/2, for rational a,b."""
    a,b=Fraction(a),Fraction(b);x,y=2*a-b,b
    if not y:return (x>0)-(x<0)
    if not x:return (y>0)-(y<0)
    if (x>0)==(y>0):return 1 if x>0 else -1
    return (1 if x>0 else -1) if x*x>5*y*y else (1 if y>0 else -1)


# Transition outputs: push-count is one-hot XOR relative to push0=1;
# negative constant, leaf code, four (node, relative Choi, relative CAR).
TRANS_WIDTHS = [5, 1, 9] + [15, 7, 2]*4
FRAME_WIDTHS = [15, 7, 2]
ADDRESS_WIDTHS = [2, 22, 22]  # 0 dummy, 1 Choi, 2 CAR; a, b


def compile_tables():
    dag, binding, palette = inputs()
    nodes = dag['nodes']; reachable = set()
    def mark(i):
        if i in reachable:
            return
        reachable.add(i)
        for j in nodes[i].get('args', []):
            mark(j)
    for i in dag['roots'].values():
        mark(i)
    assert 0 not in reachable  # encoded zero is reserved for the empty stack
    visits, depth = [], []
    for n in nodes:
        a = n.get('args', [])
        visits.append(1 if not a else 1 + (max(visits[j] for j in a) if n['op']=='add' else sum(visits[j] for j in a)))
        depth.append(1 if not a else (max(depth[j] for j in a) if n['op']=='add' else max(depth[j]+len(a)-i-1 for i,j in enumerate(a))))
    leaf_codes = {n['node']: i+1 for i,n in enumerate(binding['leaf_templates'])}
    transition = []
    for i in sorted(reachable):
        node = nodes[i]; op = node['op']; args = node.get('args', [])
        choices = list(enumerate(args)) if op=='add' else [(None, None)]
        for choice, chosen in choices:
            children = [chosen] if op=='add' else args
            push = len(children)
            assert push <= 4
            # All seven reachable constants have a definite nonzero sign.
            if op=='const':
                assert golden_sign(node['a'],node['b']) != 0
            negative = int(op=='const' and golden_sign(node['a'],node['b']) < 0)
            fields = [(1 | (1<<push)) if push else 0, negative, leaf_codes.get(i,0)]
            dc = dq = 0
            for child in children:
                fields.extend([child+1, dc, dq])
                if op=='mul':
                    dc += nodes[child]['degree'][0]
                    dq += nodes[child]['degree'][1]
            fields += [0,0,0]*(4-push)
            # Add rows require READY=1; invalid/abort labels default to pop.
            width = 22 if op=='add' else 15
            key = i+1 if op!='add' else (i+1) | (choice<<15) | (1<<21)
            transition.append([width, key, pack(fields, TRANS_WIDTHS)])
    palette_rows = [[15,int(i)+1,int(j)] for i,j in palette['node_to_palette'].items()]
    addresses = []
    for site in binding['site_bindings']:
        for li, (leaf, address) in enumerate(zip(binding['leaf_templates'],site['leaf_addresses_in_template_order'])):
            if leaf['kind']=='Choi':
                kind,a,b = 1,0,(address<<10)|(leaf['input']<<5)|leaf['output']
            else:
                kind = 2
                a,b = [(address<<4)|mask for mask in leaf['cross_masks']]
            assert a != b
            key = site['SITE_index'] | ((li+1)<<8)
            addresses.append([17,key,pack([kind,a,b],ADDRESS_WIDTHS)])
    return {
        'schema':'d0.retained.source.dispatch.tables.v1',
        'node_encoding':'original node index + 1; zero means empty/dummy',
        'transition_widths':TRANS_WIDTHS, 'frame_widths':FRAME_WIDTHS,
        'address_widths':ADDRESS_WIDTHS,
        'roots':{name:{'node':i+1,'slots':visits[i],'stack_depth':depth[i], 'degree':nodes[i]['degree']} for name,i in dag['roots'].items()},
        'palette_rows':palette_rows, 'transition_rows':transition, 'address_rows':addresses,
        'inputs':{f'{r}/{n}':digest(D/r/n) for r,n in [('round11','SOURCE_TENSOR_DAG.json'),('round11','PERIODIC_SOURCE_BINDING.json'),('round12','INTERNAL_SELECTOR_PALETTE.json')]},
        'all_external_inputs_read_only':True,'native_bank_SELECT_implemented':False,'GR_closed':False}


class Layout:
    def __init__(self):
        self.n=0
    def new(self, width):
        out=list(range(self.n,self.n+width)); self.n+=width
        return out


def split_wires(wires, widths):
    result=[]; at=0
    for width in widths:
        result.append(wires[at:at+width]);at+=width
    assert at==len(wires)
    return result


def step_plan(depth):
    l=Layout()
    q={'old_stack':[l.new(24) for _ in range(depth)],'site':l.new(8),
       'choice':l.new(6),'ready':l.new(1),
       'palette':l.new(5),'new_stack':[l.new(24) for _ in range(depth)],
       'record':l.new(1+9+7+2+46),
       'transition':l.new(sum(TRANS_WIDTHS)),
       'children':[l.new(24) for _ in range(4)],
       'flag':l.new(1),'pattern_work':l.new(20),'carries':l.new(8)}
    return {'depth':depth,'layout':q,'wire_count':l.n,
            'record_fields':['negative_constant','leaf_code','Choi_copy_offset','CAR_copy_offset','kind','basis_a','basis_b'],
            'record_widths':[1,9,7,2,2,22,22]}


def lookup_word(rows, controls, outputs, flag, work):
    """XOR the table output. All inputs untouched; work cleaned each row."""
    for width,key,value in rows:
        if not value:
            continue
        predicate=list(logic.pattern_gate(controls[:width],key,flag,work))
        yield from predicate
        for bit,q in enumerate(outputs):
            if (value>>bit)&1:
                yield ('CX',flag,q)
        yield from reversed(predicate)


def xor_add_word(a,b,out,carry):
    """out ^= a+b (mod 2^w); all arguments disjoint; clean zero carries."""
    w=len(a);assert len(b)==len(out)==w and len(carry)>=w
    compute=[]
    for i in range(w-1):
        compute += [('CCX',a[i],b[i],carry[i+1]),('CCX',a[i],carry[i],carry[i+1]),('CCX',b[i],carry[i],carry[i+1])]
    yield from compute
    for i in range(w):
        yield ('CX',a[i],out[i]);yield ('CX',b[i],out[i]);yield ('CX',carry[i],out[i])
    yield from reversed(compute)


def palette_word(plan,tables):
    q=plan['layout']
    yield from lookup_word(tables['palette_rows'],q['old_stack'][0][:15],q['palette'],q['flag'][0],q['pattern_work'])


def transition_compute_word(plan,tables):
    q=plan['layout']
    yield ('X',q['transition'][0])  # default is pop one / push zero
    yield from lookup_word(tables['transition_rows'],q['old_stack'][0][:15]+q['choice']+q['ready'],q['transition'],q['flag'][0],q['pattern_work'])


def children_word(plan):
    q=plan['layout']; fields=split_wires(q['transition'],TRANS_WIDTHS)
    _,base_c,base_q=split_wires(q['old_stack'][0],FRAME_WIDTHS)
    for i,child in enumerate(q['children']):
        node,dc,dq=fields[3+3*i:6+3*i]
        target,co,qo=split_wires(child,FRAME_WIDTHS)
        for a,b in zip(node,target):yield ('CX',a,b)
        yield from xor_add_word(base_c,dc,co,q['carries'])
        yield from xor_add_word(base_q,dq,qo,q['carries'])


def copy_outputs_word(plan,tables):
    q=plan['layout']; fields=split_wires(q['transition'],TRANS_WIDTHS)
    push,negative,leaf=fields[:3]
    for i,dest in enumerate(q['new_stack']):
        for count in range(5):
            if i<count:
                source=q['children'][i]
            else:
                index=i+1-count
                if index>=plan['depth']:
                    continue
                source=q['old_stack'][index]
            for a,b in zip(source,dest):yield ('CCX',push[count],a,b)
    rec=split_wires(q['record'],plan['record_widths'])
    old=split_wires(q['old_stack'][0],FRAME_WIDTHS)
    for source,dest in [(negative,rec[0]),(leaf,rec[1]),(old[1],rec[2]),(old[2],rec[3])]:
        for a,b in zip(source,dest):yield ('CX',a,b)
    # Read the computed transition leaf, not the XOR destination record:
    # the address must not depend on a possibly nonzero old record value.
    yield from lookup_word(tables['address_rows'],q['site']+leaf,sum(rec[4:],[]),q['flag'][0],q['pattern_work'])


def transition_word(plan,tables):
    """Use the selected label after palette computation and A13 decoding.

    The old state and coin-derived label remain retained. New state and
    instruction are XOR outputs. Temporary transition/child work is restored.
    """
    yield from transition_compute_word(plan,tables)
    child=list(children_word(plan));yield from child
    yield from copy_outputs_word(plan,tables)
    yield from reversed(child)
    # Avoid materializing the 31k-row QROM word in order to reverse it.
    q=plan['layout']
    yield from lookup_word(reversed(tables['transition_rows']),q['old_stack'][0][:15]+q['choice']+q['ready'],q['transition'],q['flag'][0],q['pattern_work'])
    yield ('X',q['transition'][0])


def lookup_counts(rows):
    counts=Counter()
    for width,key,value in rows:
        if not value:continue
        word=logic.pattern_gate(list(range(width)),key,width,list(range(width+1,2*width)))
        counts.update({op:2*n for op,n in Counter(g[0] for g in word).items()})
        counts['CX']+=bin(value).count('1')
    return counts


def step_counts(plan,tables,table_counts=None):
    q=plan['layout']; c=table_counts or {name:lookup_counts(tables[name+'_rows']) for name in ('palette','transition','address')}
    # One palette query, transition compute/uncompute, child compute/uncompute,
    # shift/copy, and one address query. Palette remains retained after decoding.
    out=Counter(c['palette']);out.update(c['address'])
    out.update({op:2*n for op,n in c['transition'].items()});out['X']+=2
    out.update({op:2*n for op,n in Counter(g[0] for g in children_word(plan)).items()})
    for i in range(plan['depth']):
        for count in range(5):
            if i<count or i+1-count<plan['depth']:out['CCX']+=24
    out['CX']+=19
    return {op:out[op] for op in ('X','CX','CCX')}


def native_inventory(logical,library,reverse=False):
    field='literal_raw_inverse_inventory' if reverse else 'forward_inventory'
    total=Counter({'CX':logical['CX']})
    for op in ('X','CCX'):
        total.update({g:int(n)*logical[op] for g,n in library['templates'][op][field].items()})
    return {g:str(total[g]) for g in ('G','CX','SourceI')}


def bind_layout(allocator,plan,aliases):
    """Assign real global wires; aliases refer only to proven input interfaces."""
    mapping={}
    for local,global_wires in aliases:
        assert len(local)==len(global_wires)
        for a,b in zip(local,global_wires):
            assert a not in mapping
            mapping[a]=b
    for i in range(plan['wire_count']):
        if i not in mapping:mapping[i]=allocator.new(1)[0]
    assert len(set(mapping.values()))==len(mapping)
    return [mapping[i] for i in range(plan['wire_count'])]


def remap(word,mapping):
    for op,*w in word:yield (op,*(mapping[i] for i in w))


def walk_events(tables,name):
    """Fixed chronological stage grammar, including actual A13 label circuits.

    All source state and coin histories are retained. Native zero/fair births
    and execution of quantum leaf instructions are explicit external consumers.
    Stage maps can be enumerated without expanding the billions of gates.
    A fresh layout is used per walk; caller aliases its eight SITE wires with
    the common external SITE and otherwise allocates disjoint whole walks.
    """
    root=tables['roots'][name];l=Layout();site=l.new(8);kind=l.new(1)
    top=json.loads((D/'round13/TOP_SOURCE_SELECTOR_CIRCUIT.json').read_text())
    internal=json.loads((D/'round13/INTERNAL_SELECTOR_CIRCUIT.json').read_text())
    firsts=json.loads((D/'round13/FIRST_SUCCESS_CIRCUITS.json').read_text())
    by_width={p['label_width']:p for p in firsts.values()}
    assert top['label_width']==2 and internal['label_width']==6
    is_matter=int(name.startswith('H_q'))
    if is_matter:
        yield {'kind':'kind_init','gates':[('X',kind[0])],'allocated_wires':l.n}
    def selector_bank(decoder,palette_wires,output_alias=None):
        decoded=[]
        for attempt in range(7):
            m=bind_layout(l,decoder,[(decoder['layout']['palette'],palette_wires)])
            decoded.append([m[i] for i in decoder['layout']['output']])
            yield {'kind':'selector','plan':decoder,'map':m,'allocated_wires':l.n}
        first=by_width[decoder['label_width']];q=first['layout']
        aliases=[(q['labels'],sum([v[:-1] for v in decoded],[])),(q['ready'],[v[-1] for v in decoded])]
        if output_alias is not None:
            aliases += [(q['output'],output_alias[0]),(q['out_ready'],output_alias[1])]
        m=bind_layout(l,first,aliases)
        yield {'kind':'first_success','plan':first,'map':m,'allocated_wires':l.n,
               'selected_output':[m[i] for i in q['output']+q['out_ready']]}
    selected_top=None
    for event in selector_bank(top,kind+site):
        if event['kind']=='first_success':selected_top=event['selected_output']
        yield event
    old=[l.new(24) for _ in range(root['stack_depth'])];phase=l.new(1)
    flag=l.new(1)[0];work=l.new(1)
    yield {'kind':'root_init','controls':selected_top,'outputs':old[0][:15]+phase,
           'rows':[[3,4,root['node']],[3,6,1<<15]],'flag':flag,'work':work,'allocated_wires':l.n}
    for slot in range(root['slots']):
        plan=step_plan(root['stack_depth']);q=plan['layout']
        m=bind_layout(l,plan,[(sum(q['old_stack'],[]),sum(old,[])),(q['site'],site)])
        yield {'kind':'palette','plan':plan,'map':m,'slot':slot,'allocated_wires':l.n}
        for event in selector_bank(internal,[m[i] for i in q['palette']],([m[i] for i in q['choice']],[m[i] for i in q['ready']])):
            event['slot']=slot;yield event
        yield {'kind':'transition','plan':plan,'map':m,'slot':slot,'allocated_wires':l.n}
        old=[[m[i] for i in frame] for frame in q['new_stack']]
    yield {'kind':'end','allocated_wires':l.n,'external_SITE':site,'top_identity_phase':phase,
           'final_stack':old,'all_coin_history_retained':True}


def event_word(event,tables):
    kind=event['kind']
    if kind=='end':return
    if kind=='kind_init':yield from event['gates'];return
    if kind=='root_init':
        yield from lookup_word(event['rows'],event['controls'],event['outputs'],event['flag'],event['work']);return
    plan=event['plan']
    if kind=='selector':word=logic.selector_word(plan)
    elif kind=='first_success':word=logic.first_success_word(plan)
    elif kind=='palette':word=palette_word(plan,tables)
    else:
        assert kind=='transition';word=transition_word(plan,tables)
    yield from remap(word,event['map'])


def walk_word(tables,name):
    for event in walk_events(tables,name):yield from event_word(event,tables)


def native_walk_macros(tables,name,k):
    """Actual finite G/CX/SourceI DAG replacement for each scheduled gate.

    The integer k must be the certified A14 k. This iterator is intentionally
    lazy; the full astronomical leaf word has not been executed.
    """
    module_name='a15_native_boolean'
    if module_name not in sys.modules:
        sp=importlib.util.spec_from_file_location(module_name,D/'round14/native_boolean.py')
        nb=importlib.util.module_from_spec(sp);sys.modules[module_name]=nb;sp.loader.exec_module(nb)
    nb=sys.modules[module_name]
    for event in walk_events(tables,name):
        if event['kind']=='end':size=event['allocated_wires']
    angle=json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())
    assert k==int(angle['k'])
    port=size;spin=(size+1,size+2);aux=size+3
    for op,*w in walk_word(tables,name):
        if op=='CX':yield nb.gate('CX',*w)
        elif op=='X':yield nb.boolean_word('X',k,target=w[0],port=port,spin=spin)
        else:
            assert op=='CCX'
            yield nb.boolean_word('CCX',k,control=w[:2],target=w[2],aux=aux,port=port,spin=spin)


def main():
    tables=compile_tables();(P/'SOURCE_DISPATCH_TABLES.json').write_text(json.dumps(tables,separators=(',',':'))+'\n')
    tc={name:lookup_counts(tables[name+'_rows']) for name in ('palette','transition','address')}
    reports={};total=Counter()
    for name,root in tables['roots'].items():
        plan=step_plan(root['stack_depth']);counts=step_counts(plan,tables,tc)
        # Root initialization: one three-input predicate (top label=0, READY=1),
        # then copy the fixed root code; separate top label=2 phase record.
        code=root['node'];init=lookup_counts([[3,4,code],[3,6,1<<15]])
        n=2 if name.startswith('H_f') else 8
        # Top palette index is 2*SITE + root kind; eight matter walks pay X.
        if name.startswith('H_q'):init['X']+=1
        part=Counter({op:root['slots']*v for op,v in counts.items()});part.update(init)
        total.update({op:n*v for op,v in part.items()})
        reports[name]={'root':root,'step_plan':plan,'step_counts':counts,'root_initialization_counts':dict(init),'one_walk_counts':dict(part),
            'retained_state_bits_per_walk':(root['slots']+1)*24*root['stack_depth'],
            'retained_instruction_bits_per_walk':root['slots']*65,
            'retained_palette_bits_per_walk':root['slots']*5,
            'coins_and_A13_decoder_registers_counted_separately':True}
        stages=Counter()
        for event in walk_events(tables,name):
            stages[event['kind']]+=1
            if event['kind']=='end':reports[name]['walk_logical_wire_count']=event['allocated_wires']
        reports[name]['chronological_stage_counts']=dict(stages)
    library=json.loads((D/'round14/NATIVE_BOOLEAN_LIBRARY.json').read_text())
    approximate=7*(total['X']+total['CCX']);bound=approximate.bit_length()
    result={'status':'FINITE_REVERSIBLE_DAG_INSTRUCTION_CONTROLLER','table_sha256':digest(P/'SOURCE_DISPATCH_TABLES.json'),
       'source_sha256':digest(Path(__file__)),'lookup_gate_counts':{k:dict(v) for k,v in tc.items()},'walks':reports,
       'ten_sign_report_controller_counts':dict(total),'seven_report_approximate_macro_count':approximate,
       'seven_report_controller_error_strictly_below':'2^-'+str(4096-bound),
       'native_forward_inventory_per_report':native_inventory(total,library),
       'native_literal_reverse_inventory_per_report':native_inventory(total,library,True),
       'native_macro_library_sha256':digest(D/'round14/NATIVE_BOOLEAN_LIBRARY.json'),
       'fixed_slots_per_report':1054,'additional_fair_qubits':0,
       'assumptions':['All stated new output and workspace registers are computational zero at entry; physical births separately required.',
          'Top and each internal slot use the existing A13 coherent decoded labels; all slots including dummy consume their fixed attempts.',
          'A single common external SITE is a read-only input, distinct from CAR internal SITE.'],
       'full_dispatch_gate_stream_executed':False,'native_bank_SELECT_implemented':False,
       'all_H1_marks_reader_clock_proved':False,'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'SOURCE_DISPATCH_COMPILATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','ten_sign_report_controller_counts','seven_report_controller_error_strictly_below']}))


if __name__=='__main__':main()
