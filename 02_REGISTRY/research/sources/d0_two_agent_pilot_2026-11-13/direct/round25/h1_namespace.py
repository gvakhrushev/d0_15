#!/usr/bin/env python3
"""Explicit global H.1 register binding; not yet a complete marked execution.

One shared SITE, 7 reports, all source copies and private RAW resources.
The native port is canonical born WORK and becomes the active SC6 output;
its G^-1 stays AFTER R_load, exactly where the owner places it.
"""
from pathlib import Path
from collections import Counter
import hashlib,json
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
BANKS=('y+','y-','f','0','x+','x-','q')
def choi_layout(plan,slot):
    assert slot['kind']=='Choi';g=plan['layout'];p=slot['private']
    return {'SAM':g['SAM'],'all_SAM':g['SAM'],'address':slot['address'],'choi_input':slot['choi_input'],'choi_output':slot['choi_output'],
            'modes':slot['choi_output'][:4],'julia_flag':slot['choi_output'][4],'branch':p[0],'phase_rebit':p[1],
            'comparator_scratch':p[2:],'port':g['port'],'spin':g['spin'],'aux_arbitrary':g['aux_arbitrary'],
            'oldRIGHT_witness':g['oldRIGHT_witness'],'qubits':g['qubits']}
def car_layout(plan,slot):
    assert slot['kind']=='CAR';g=plan['layout'];p=slot['private']
    return {'SAM':g['SAM'],'internal_SITE':slot['internal_SITE'],'grade':slot['grade'],'RIGHT':slot['RIGHT'],
            'predicate_flag':p[0],'predicate_work':p[1:],'native_aux_arbitrary':g['aux_arbitrary'],
            'port':g['port'],'spin':g['spin'],'oldRIGHT_witness':g['oldRIGHT_witness'],'qubits':g['qubits']}
def site_layout(plan):
    g=plan['layout']
    return {'SITE':g['SITE'],'aux_arbitrary':g['aux_arbitrary'],'port':g['port'],'spin':g['spin'],
            'oldRIGHT_witness':g['oldRIGHT_witness'],'qubits':g['qubits']}
def report_wire(plan,report,q):
    local=plan['local_report'];N=local['logical_wire_count'];l=plan['layout']
    assert type(q) is int and 0<=q<N+5
    if q<8:return l['SITE'][q]
    if q<N:return report['private_start']+q-8
    return [l['port'],*l['spin'],l['aux_arbitrary'],l['oldRIGHT_witness']][q-N]
def build():
    local=json.loads((D/'round17/GLOBAL_REPORT_PLAN.json').read_text())
    compilation=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    # Numeric oldRIGHT is one witness for an arbitrary further exact-I
    # external factor. A concrete physical old cut still needs actual binding.
    l={'spin':[0,1],'aux_arbitrary':2,'oldRIGHT_witness':3,'SAM':list(range(4,2692)),
       'SITE':list(range(2692,2700)),'SC6_selectors':list(range(2700,2705)),'port':2705}
    plan={'local_report':local,'layout':l};cursor=2706;reports=[];sources=[]
    for bank in BANKS:
        r={'bank':bank,'private_start':cursor,'private_width':local['logical_wire_count']-8};cursor+=r['private_width']
        r['sigma']=report_wire(plan,r,8);r['sigma_bit']=0;r['sigma_sign']=-1
        r['all_READY']=report_wire(plan,r,local['all_READY_wire']);r['REPORT']=report_wire(plan,r,local['report_wire'])
        r['native_port']=l['port'];r['native_spin']=l['spin'];r['native_aux']=l['aux_arbitrary'];r['source_slots']=[]
        car_right={(z['walk'],z['copy']):z for z in local['source_buffers'] if z['kind']=='CAR_RIGHT'}
        for row in local['source_buffers']:
            if row['kind']=='CAR_RIGHT':continue
            a,n=row['range'];w=[report_wire(plan,r,q) for q in range(a,a+n)]
            source={'bank':bank,'walk':row['walk'],'copy':row['copy'],'kind':'Choi' if row['kind']=='Choi' else 'CAR','source':w}
            if source['kind']=='Choi':
                assert n==22;source['private']=list(range(cursor,cursor+24));cursor+=24
                # A15/A16 read a little-endian flat basis index
                # (address<<10)|(input<<5)|output, NOT A22's default
                # human-facing register order. Bind roles, do not permute
                # an already prepared state for free.
                source['address']=w[10:];source['choi_input']=w[5:10];source['choi_output']=w[:5]
            else:
                assert n==12;right=car_right[(row['walk'],row['copy'])];a,n=right['range'];assert n==7
                source['RIGHT']=[report_wire(plan,r,q) for q in range(a,a+n)]
                # The A15 CAR instruction is (internal_site<<4)|grade.
                source['internal_SITE']=w[4:];source['grade']=w[:4];source['private']=list(range(cursor,cursor+3));cursor+=3
            r['source_slots'].append(len(sources));sources.append(source)
        assert Counter(sources[i]['kind'] for i in r['source_slots'])=={'Choi':180,'CAR':16}
        r['source_private_start']=r['private_start']+r['private_width'];r['source_private_width']=4368
        assert cursor==r['source_private_start']+r['source_private_width'];reports.append(r)
    l['qubits']=cursor
    sc6=[*l['SC6_selectors'],*[q for r in reports for q in (r['all_READY'],r['REPORT'])],l['port'],*l['spin'],l['oldRIGHT_witness']]
    assert len(sc6)==len(set(sc6))==23 and l['aux_arbitrary'] not in sc6
    births={'processor_and_fair':7*compilation['fresh_RAW_v_births_for_processor_and_fair'],'Choi_DATA':1260*22,'Choi_private':1260*24,
            'CAR_source':112*19,'CAR_private':112*3,'sigma':7,'external_SITE':8,'SC6_selector':5,'active_port':1}
    work=sum(births.values());assert work==10407048092 and cursor==work+2688+4
    plan.update({'status':'GLOBAL_H1_NAMESPACE_AND_INPUT_BINDING_CANDIDATE','reports':reports,'source_slots':sources,'SC6_local_to_global':sc6,
                 'WORK_RAW_birth_inventory':births,'WORK_RAW_birth_count':work,'separate_SAM_RAW_births':2688,
                 'protected_numeric_factor':['spin[0]','spin[1]','aux','oldRIGHT_witness'],'additional_oldD_is_exact_external_tensor_factor':True,
                 'canonical_WORK_input':'product of actual RAW v for the declared fresh inputs; not yet an admission proof',
                 'sigma_derivation':'sigma=-1 because H1 y=-q/(64*rho*Lambda); seven explicit RAW v to zero preparations',
                 'source_buffer_bit_encoding':{'Choi':'bit0..4 output j; bit5..9 input i; bit10..21 address a','CAR_DATA':'bit0..3 grade; bit4..11 internal site'},
                 'owner_A_chronology':['SITE preparation','R_load: source banks and their seven actual reports, sigma zeros included','paid active-port G^-1','original SC6 V'],
                 'owner_W_chronology':['actual A','central Z_active_port','leafwise literal inverse of actual A'],
                 'port_initialization_moved_before_R_load':False,'SITE_unprepare_occurs_in_outer_actual_A_inverse':True,
                 'SC6_FORWARD_calls':18176,'SC6_grouped_inverse_calls_not_used_as_literal':18176,'SC6_leafwise_inverse_calls':58112,
                 'T_forward_calls_including_port_inverse':18181,'T_leafwise_inverse_calls':58129,'T_Z_T_literal_total_calls':76312,
                 'complete_native_word_generator_implemented':False,'actual_global_T6_proved':False,'original_marked_history_equivalence_proved':False,
                 'physical_birth_stage_admission_proved':False,'physical_C_closed':False,'GR_closed':False})
    return plan
def main():
    p=build();h=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
    p['source_sha256']={str(q):h(q) for q in [Path(__file__),D/'round15/source_dispatcher.py',D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round17/GLOBAL_REPORT_PLAN.json',D/'round17/GLOBAL_REPORT_COMPILATION.json',D/'round22/FULL_CHOI_BANK_PLAN.json',D/'round24/FULL_CAR_SOURCE_PLAN.json',B/'round21/SC6_FORWARD.jsonl',B/'round25/TARGETS_RU.md']}
    (P/'H1_NAMESPACE_PLAN.json').write_text(json.dumps(p,indent=2)+'\n')
    print(json.dumps({'status':p['status'],'source_slots':len(p['source_slots']),'WORK_RAW_births':p['WORK_RAW_birth_count'],'numeric_qubits_with_old_witness':p['layout']['qubits']}))
if __name__=='__main__':main()
