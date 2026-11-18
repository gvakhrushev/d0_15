#!/usr/bin/env python3
"""One global ten-sign report: shared SITE, disjoint resources, real READY.

Source-bank and external SITE preparations remain explicit input obligations.
All other processor inputs have a finite RAW-v/zero/fair preparation grammar.
"""
from collections import Counter
from pathlib import Path
from bisect import bisect_right
import hashlib,importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sp=importlib.util.spec_from_file_location('a17_select',D/'round16/source_select.py')
s=importlib.util.module_from_spec(sp);sys.modules[sp.name]=s;sp.loader.exec_module(s)
B31=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round31')
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()


def contiguous(wires):
    assert wires and wires==list(range(wires[0],wires[0]+len(wires)))
    return [wires[0],len(wires)]


def collect_local_walk(name,tables):
    fair=[];golden=[];ready=[];first_record=None;end=None
    for event in s.dispatch.walk_events(tables,name):
        kind=event['kind']
        if kind=='selector':
            q=event['plan']['layout'];m=event['map']
            fair.append(contiguous([m[i] for i in q['fair']]))
            if q['golden']:golden.append(contiguous([m[i] for i in q['golden']]))
        elif kind=='first_success':ready.append(event['map'][event['plan']['layout']['out_ready'][0]])
        elif kind=='transition' and first_record is None:first_record=[event['map'][i] for i in event['plan']['layout']['record']]
        elif kind=='end':end=event
    assert end and first_record
    local=s.instruction_plan(tables['roots'][name]['degree']);l=s.dispatch.Layout();l.n=end['allocated_wires']
    record=sum([local['layout'][key] for key in ['negative','leaf','coffset','qoffset','kind','a','b']],[])
    mapping=s.dispatch.bind_layout(l,local,[(record,first_record)])
    q=local['layout'];sources=[]
    for kind,key in [('Choi','choi'),('CAR_DATA','car'),('CAR_RIGHT','CAR_RIGHT')]:
        for i,wires in enumerate(q[key]):sources.append({'kind':kind,'copy':i,'range':contiguous([mapping[a] for a in wires])})
    delta=[mapping[i] for i in q['delta_choi']+q['delta_car']]
    if delta:fair.append(contiguous(delta))
    return {'local_wires':l.n,'fair':fair,'golden':golden,'ready':ready,
            'sign':mapping[q['h'][0]],'source_buffers':sources,'source_delta':delta}


def global_wire(walk,wire):
    assert 0<=wire<walk['local_wires']
    return wire if wire<8 else walk['private_start']+wire-8


def merge_and_complement(ranges,start,stop):
    """Require disjoint half-open ranges; return all uncovered zero inputs."""
    result=[];at=start
    for a,n in sorted(ranges):
        assert n>0 and start<=a and a+n<=stop and a>=at,(a,n,at)
        if a>at:result.append([at,a-at])
        at=a+n
    if at<stop:result.append([at,stop-at])
    return result


def make_plan():
    tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text())
    local={name:collect_local_walk(name,tables) for name in tables['roots']}
    cursor=9;walks=[];fair=[];golden=[];ready=[];sources=[];signs=[]
    names=[('S1','H_f_before_inverse_PF'),('S2','H_f_before_inverse_PF')]+[(f'T{i+1}','H_q_before_inverse_PF') for i in range(8)]
    for label,root in names:
        v=local[root];walk={'label':label,'root':root,'local_wires':v['local_wires'],'private_start':cursor,'private_width':v['local_wires']-8}
        cursor+=walk['private_width'];walks.append(walk)
        mapq=lambda w:global_wire(walk,w)
        fair.extend([[mapq(a),n] for a,n in v['fair']]);golden.extend([[mapq(a),n] for a,n in v['golden']]);ready.extend(mapq(a) for a in v['ready'])
        signs.append(mapq(v['sign']))
        sources.extend([{**row,'walk':label,'range':[mapq(row['range'][0]),row['range'][1]]} for row in v['source_buffers']])
    post=json.loads((D/'round13/TEN_SIGN_REPORT_CIRCUIT.json').read_text())
    l=s.dispatch.Layout();l.n=cursor
    # A12 palettes enumerate sigma=-1,+1 outside the mask loop.
    mapping=s.dispatch.bind_layout(l,post,[(post['layout']['palette'],signs+[8])])
    fair.append(contiguous([mapping[i] for i in post['layout']['fair']]))
    golden.append(contiguous([mapping[i] for i in post['layout']['golden']]))
    postout=[mapping[i] for i in post['layout']['output']]
    ready.append(postout[-1]);report=l.new(1)[0];allready=l.new(1)[0]
    M=sum(n for a,n in fair);assert M==10248262
    K=M+len(ready);assert K==10249327
    and_start=l.n;l.n+=K-2
    compiler_end=l.n
    # Required prepared source state, fair output, Golden RAW, zero are disjoint.
    nonzero=fair+golden+[row['range'] for row in sources]
    zeros=merge_and_complement(nonzero,9,compiler_end)
    assert sum(n for _,n in golden)==76
    assert sum(row['range'][1] for row in sources)==4264
    bank_extra_start=compiler_end;logical_end=bank_extra_start+142*M
    prefix=0;fair_ranges=[]
    for a,n in fair:
        fair_ranges.append({'bank_index_start':prefix,'output_wire_start':a,'count':n});prefix+=n
    return {'schema':'d0.global.ten-sign.report.v1','incoming_shared_SITE':list(range(8)),
        'incoming_sigma_wire':8,'sigma_encoding':'0 -> -1; 1 -> +1',
        'walks':walks,'sign_wires_S1_S2_T1_to_T8':signs,
        'source_buffers':sources,'source_buffers_are_prepared_external_inputs':True,
        'postprocessor_file':'round13/TEN_SIGN_REPORT_CIRCUIT.json','postprocessor_map':mapping,
        'post_label_wire':postout[0],'post_READY_wire':postout[1],
        'report_wire':report,'report_encoding':'1 iff post READY and label0; A12 label0 means REPORT1',
        'all_READY_wire':allready,'selector_and_post_READY_wires':ready,
        'fair_bank_count':M,'fair_output_ranges':fair_ranges,'fair_bank_extra_start':bank_extra_start,
        'fair_bank_extra_width':142,'fair_bank_output_local':84,'fair_bank_READY_local':85,
        'Golden_RAW_ranges':golden,'processor_zero_ranges':zeros,
        'READY_total_flags':K,'READY_AND_work_range':[and_start,K-2],
        'compiler_region_end':compiler_end,'logical_wire_count':logical_end,
        'native_port':logical_end,'native_spin':[logical_end+1,logical_end+2],
        'native_aux_arbitrary':logical_end+3,'protected_oldRIGHT_witness':logical_end+4,
        'native_wire_count_including_oldRIGHT_witness':logical_end+5,
        'finite_native_stage_order':['prepare all processor zeros from distinct RAW v','all fixed B31 fair banks on distinct RAW v, output aliases assigned fair wires','ten A16 walks with common SITE and disjoint private intervals','A13 postprocessor with shared sigma and the ten actual sign outputs','coherent REPORT1 extraction','coherent conjunction of all fair/selector/post READY flags'],
        'RAW_birth_requirements':{'processor_zero':sum(n for a,n in zeros),'Golden_coins':76,'fair_banks_including_output':143*M},
        'bank_preparation_and_external_SITE_loader_included':False,'full_H1_writer_emitted':False,
        'physical_birth_stage_admission_proved':False,'physical_C_closed':False,'GR_closed':False}


def fair_output(plan,index):
    assert 0<=index<plan['fair_bank_count']
    rows=plan['fair_output_ranges'];starts=[r['bank_index_start'] for r in rows]
    row=rows[bisect_right(starts,index)-1]
    assert index<row['bank_index_start']+row['count']
    return row['output_wire_start']+index-row['bank_index_start']


def fair_bank_wire(plan,index,local,output=None):
    assert 0<=index<plan['fair_bank_count'] and 0<=local<148
    if local>=143:return plan['native_port']+local-143
    if local==84:return fair_output(plan,index) if output is None else output
    return plan['fair_bank_extra_start']+142*index+local-(local>84)


def ready_flag(plan,index):
    assert 0<=index<plan['READY_total_flags']
    if index<plan['fair_bank_count']:return fair_bank_wire(plan,index,85)
    return plan['selector_and_post_READY_wires'][index-plan['fair_bank_count']]


def and_compute_gate(plan,index):
    K=plan['READY_total_flags'];a=plan['READY_AND_work_range'][0]
    assert 0<=index<K-2
    if index==0:return ('CCX',ready_flag(plan,0),ready_flag(plan,1),a)
    return ('CCX',a+index-1,ready_flag(plan,index+1),a+index)


def and_core_gate(plan):
    K=plan['READY_total_flags'];a=plan['READY_AND_work_range'][0]
    return ('CCX',a+K-3,ready_flag(plan,K-1),plan['all_READY_wire'])


def ready_logical_word(plan):
    for i in range(plan['READY_total_flags']-2):yield and_compute_gate(plan,i)
    yield and_core_gate(plan)
    for i in reversed(range(plan['READY_total_flags']-2)):yield and_compute_gate(plan,i)


def remap_native(tree,mapper):
    if tree['op']=='seq':return s.nb.seq(*(remap_native(t,mapper) for t in tree['children']))
    if tree['op']=='repeat':return s.nb.repeat(int(tree['count']),remap_native(tree['child'],mapper))
    return s.nb.gate(tree['op'],*(mapper(w) for w in tree['wires']))


def lower_gate(plan,k,logical):
    return s.lower(s.gate(logical[0],*logical[1:]),k,plan['native_port'],tuple(plan['native_spin']),plan['native_aux_arbitrary'])


def fair_bank_native(plan,index,bank):
    output=fair_output(plan,index)
    mapq=lambda w:fair_bank_wire(plan,index,w,output)
    prefix=s.nb.seq(*(s.nb.gate(g['op'],*(mapq(w) for w in g['wires'])) for g in bank['zero_and_kernel_forward']['gates']))
    return s.nb.seq(prefix,remap_native(bank['router_forward_DAG'],mapq))


def ready_native_blocks(plan,k):
    for i in range(plan['READY_total_flags']-2):yield lower_gate(plan,k,and_compute_gate(plan,i))
    yield lower_gate(plan,k,and_core_gate(plan))
    for i in reversed(range(plan['READY_total_flags']-2)):
        yield s.nb.inverse_literal(lower_gate(plan,k,and_compute_gate(plan,i)),plan['native_port'],tuple(plan['native_spin']))


def report_native_blocks(plan,k):
    """Entire finite forward program for the explicitly stated input contract.

    The huge loop counts are exact; this is a generator, not an executed tape.
    RAW births are a separate enumerated input/admission requirement.
    """
    angle=json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text());assert int(angle['k'])==k
    port=plan['native_port'];spin=tuple(plan['native_spin'])
    for start,width in plan['processor_zero_ranges']:
        for wire in range(start,start+width):yield s.nb.rotation_power(wire,-1,port,spin)
    bank=json.loads((B31/'NATIVE_FAIR_BANK.json').read_text());assert int(bank['k'])==k
    for i in range(plan['fair_bank_count']):yield fair_bank_native(plan,i,bank)
    for walk in plan['walks']:
        def mapq(w):return global_wire(walk,w) if w<walk['local_wires'] else port+w-walk['local_wires']
        for block in s.walk_native_blocks(walk['root'],k):yield remap_native(block,mapq)
    post=json.loads((D/plan['postprocessor_file']).read_text());m=plan['postprocessor_map']
    for op,*w in s.logic.selector_word(post):yield lower_gate(plan,k,(op,*(m[i] for i in w)))
    # output ^= READY & NOT(label); retain both original decoder outputs.
    yield lower_gate(plan,k,('CX',plan['post_READY_wire'],plan['report_wire']))
    yield lower_gate(plan,k,('CCX',plan['post_READY_wire'],plan['post_label_wire'],plan['report_wire']))
    yield from ready_native_blocks(plan,k)


def main():
    plan=make_plan();(P/'GLOBAL_REPORT_PLAN.json').write_text(json.dumps(plan,separators=(',',':'))+'\n')
    angle=json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text());k=int(angle['k'])
    a13=json.loads((D/'round13/CIRCUIT_COMPILATION.json').read_text())['decoder_label_routing_counts_per_report']
    a15=json.loads((D/'round15/SOURCE_DISPATCH_COMPILATION.json').read_text())['ten_sign_report_controller_counts']
    a16=json.loads((D/'round16/SOURCE_SELECT_COMPILATION.json').read_text())
    bank=json.loads((B31/'NATIVE_FAIR_BANK.json').read_text())
    resources={}
    c=Counter(a13);c.update(a15);r=Counter()
    for op,count in c.items():
        one=s.resource_ir(s.gate(op,*range({'X':1,'CX':2,'CCX':3}[op])),k)
        r.update({a:count*b for a,b in one.items()})
    resources['A13_selectors_labels_post_and_A15_controller']=r
    resources['A16_quantum_SELECT_and_sign_tests']=Counter({a:int(b) for a,b in a16['one_report_SELECT_test_native_resources'].items() if int(b)})
    M=plan['fair_bank_count'];K=plan['READY_total_flags'];Z=plan['RAW_birth_requirements']['processor_zero']
    fair=s.native_resource(bank['router_forward_DAG'],143)
    for g in bank['zero_and_kernel_forward']['gates']:fair.update(s.native_resource(g,143))
    resources['B31_fair_banks_once']=Counter({a:M*b for a,b in fair.items()})
    resources['processor_RAW_v_to_zero']=Counter({'G_port':Z,'CX':6*Z,'SourceI':4*Z})
    cc=s.resource_ir(s.gate('CCX',0,1,2),k);inv=s.raw_reverse_resource(cc)
    resources['actual_READY_conjunction']=Counter({a:(K-1)*cc[a]+(K-2)*inv[a] for a in set(cc)|set(inv)})
    resources['REPORT1_extraction']=cc+Counter({'CX':1})
    total=Counter()
    for row in resources.values():total.update(row)
    previous=a16['seven_report_all_known_approximate_macros'];new=7*(2*K-3+1);combined=previous+new
    assert combined<2**38
    fair_gate_counts={'X':3*M,'CX':169*M,'CCX':56*M}
    result={'status':'EXPLICIT_GLOBAL_TEN_SIGN_REPORT_AND_RAW_RESOURCE_GRAMMAR',
      'source_sha256':h(Path(__file__)),'plan_sha256':h(P/'GLOBAL_REPORT_PLAN.json'),
      'input_sha256':{str(f):h(f) for f in [D/'round13/TEN_SIGN_REPORT_CIRCUIT.json',D/'round13/CIRCUIT_COMPILATION.json',D/'round15/SOURCE_DISPATCH_COMPILATION.json',D/'round16/source_select.py',D/'round16/SOURCE_SELECT_COMPILATION.json',D/'round14/NATIVE_BOOLEAN_ANGLE.json',B31/'NATIVE_FAIR_BANK.json']},
      'one_external_SITE':8,'ten_disjoint_walks':10,'prepared_Choi_copies':180,'prepared_CAR_copies_with_RIGHT':16,
      'prepared_external_source_qubits':4264,'fair_output_qubits':M,'Golden_RAW_qubits':76,
      'all_READY_flags':K,'all_READY_logical_CCX':2*K-3,
      'fresh_RAW_v_births_for_processor_and_fair':sum(plan['RAW_birth_requirements'].values()),
      'births_exclude_prepared_source_banks_and_external_SITE':True,
      'native_resources_by_stage':{name:s.encode_resource(r) for name,r in resources.items()},
      'native_forward_resources':s.encode_resource(total),'native_literal_raw_reverse_resources':s.encode_resource(s.raw_reverse_resource(total)),
      'fair_router_logical_counts_counted_once':fair_gate_counts,
      'seven_report_all_known_approximate_macros':combined,'seven_report_known_error_strictly_below':'2^-4058',
      'ready_inputs_immutable':True,'ideal_global_READY_is_previous_Q_pre':True,
      'full_source_bank_product_state_is_required_for_scalar_Beta':True,
      'source_bank_preparations_compiled':False,'physical_birth_permission_and_admission_proved':False,
      'full_H1_comparator_marks_clock_compiled':False,'full_H1_alpha_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'GLOBAL_REPORT_COMPILATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['status','fair_output_qubits','all_READY_flags','fresh_RAW_v_births_for_processor_and_fair','seven_report_known_error_strictly_below']}))


if __name__=='__main__':main()
