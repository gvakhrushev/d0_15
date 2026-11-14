#!/usr/bin/env python3
"""Independent A25 all-slot namespace + original A15 basis bit-order audit."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,json,sys
import numpy as np
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
src=D/'round25/h1_namespace.py';f=D/'round25/H1_NAMESPACE_PLAN.json';p=json.loads(f.read_text());sha=lambda x:sha256(x.read_bytes()).hexdigest()
for path,digest in p['source_sha256'].items():assert sha(Path(path))==digest,path
local=json.loads((D/'round17/GLOBAL_REPORT_PLAN.json').read_text());assert p['local_report']==local
comp=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text());tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());bind=json.loads((D/'round11/PERIODIC_SOURCE_BINDING.json').read_text())
# True A15 packed lookup table independently reconstructed from source leaves.
rows=tables['address_rows'];assert len(rows)==256*282;checks=Counter();ix=0
for site in bind['site_bindings']:
 for li,(leaf,address) in enumerate(zip(bind['leaf_templates'],site['leaf_addresses_in_template_order'])):
  width,key,value=rows[ix];ix+=1;assert width==17 and key==site['SITE_index']+256*(li+1)
  kind=value&3;z=(value>>2)&((1<<22)-1);b=(value>>24)&((1<<22)-1)
  if leaf['kind']=='Choi':
   assert kind==1 and z==0 and b==(int(address)*1024+32*leaf['input']+leaf['output']);checks['Choi_table_rows']+=1
  else:
   assert kind==2 and (z,b)==tuple(int(address)*16+mask for mask in leaf['cross_masks']);checks['CAR_table_rows']+=1
assert ix==len(rows)
# Exhaust the *logical basis labels*; this is not simulation of native sources.
x=np.arange(1<<22,dtype=np.uint32);out=x&31;inp=(x>>5)&31;address=x>>10;assert np.array_equal(x,(address<<10)|(inp<<5)|out)
y=np.arange(1<<12,dtype=np.uint32);assert np.array_equal(y,((y>>4)<<4)|(y&15))
assert len(x)==4194304 and len(y)==4096
sys.path[:0]=[str(D/'round22'),str(D/'round18')];a22=load('b50_choi',D/'round22/full_choi_bank.py');a24=load('b50_car',D/'round24/full_car_source.py');ns=load('b50_ns',src);site=load('b50_site',O/'round45/site_native.py');l=p['layout'];assert l['spin']==[0,1] and l['aux_arbitrary']==2 and l['oldRIGHT_witness']==3
site_bound=ns.site_layout(p);assert site_bound=={'SITE':l['SITE'],'aux_arbitrary':l['aux_arbitrary'],'port':l['port'],'spin':l['spin'],'oldRIGHT_witness':l['oldRIGHT_witness'],'qubits':l['qubits']};site.validate(site_bound)
assert l['SAM']==list(range(4,2692)) and l['SITE']==list(range(2692,2700)) and l['SC6_selectors']==list(range(2700,2705)) and l['port']==2705
N=local['logical_wire_count'];expected_cursor=2706;offset=0;roles=Counter();sourceprivate=Counter()
for bank,report in zip(('y+','y-','f','0','x+','x-','q'),p['reports']):
 assert report['bank']==bank and report['private_start']==expected_cursor and report['private_width']==N-8
 def glob(w):return l['SITE'][w] if w<8 else report['private_start']+w-8
 for q in [0,7,8,N-1,N,N+1,N+2,N+3,N+4]:
  want=glob(q) if q<N else [l['port'],*l['spin'],l['aux_arbitrary'],l['oldRIGHT_witness']][q-N];assert ns.report_wire(p,report,q)==want
 assert report['sigma']==glob(8) and report['sigma_bit']==0 and report['sigma_sign']==-1
 assert report['all_READY']==glob(local['all_READY_wire']) and report['REPORT']==glob(local['report_wire'])
 assert (report['native_port'],report['native_spin'],report['native_aux'])==(l['port'],l['spin'],l['aux_arbitrary'])
 start=report['private_start'];end=start+report['private_width'];cursor=end
 expected_slots=[q for q in local['source_buffers'] if q['kind']!='CAR_RIGHT'];right={(q['walk'],q['copy']):q for q in local['source_buffers'] if q['kind']=='CAR_RIGHT'}
 assert report['source_slots']==list(range(offset,offset+len(expected_slots))) and len(expected_slots)==196
 source_intervals=[]
 for idx,row in zip(report['source_slots'],expected_slots):
  slot=p['source_slots'][idx];assert (slot['bank'],slot['walk'],slot['copy'])==(bank,row['walk'],row['copy'])
  w=[glob(i) for i in range(row['range'][0],sum(row['range']))];assert slot['source']==w and all(start<=v<end for v in w);assert all(ns.report_wire(p,report,q)==glob(q) for q in range(row['range'][0],sum(row['range'])))
  source_intervals.append((min(w),max(w)+1));private=slot['private'];assert private==list(range(cursor,cursor+len(private)));cursor+=len(private)
  if row['kind']=='Choi':
   assert slot['kind']=='Choi' and len(w)==22 and len(private)==24
   assert slot['choi_output']==w[0:5] and slot['choi_input']==w[5:10] and slot['address']==w[10:22]
   a=a22.layout();a.update({'SAM':l['SAM'],'all_SAM':l['SAM'],'address':w[10:22],'choi_input':w[5:10],'choi_output':w[:5],'modes':w[:4],'julia_flag':w[4],'branch':private[0],'phase_rebit':private[1],'comparator_scratch':private[2:],'port':l['port'],'spin':l['spin'],'aux_arbitrary':l['aux_arbitrary'],'oldRIGHT_witness':l['oldRIGHT_witness'],'qubits':l['qubits']});a.pop('private_clean_work',None);assert ns.choi_layout(p,slot)==a;a22.validate(a)
   roles['Choi']+=1;sourceprivate['Choi']+=len(private)
  else:
   assert row['kind']=='CAR_DATA' and slot['kind']=='CAR' and len(w)==12 and len(private)==3
   assert slot['grade']==w[:4] and slot['internal_SITE']==w[4:]
   rr=right[(row['walk'],row['copy'])];rw=[glob(i) for i in range(rr['range'][0],sum(rr['range']))];assert slot['RIGHT']==rw and len(rw)==7 and all(start<=q<end for q in rw);source_intervals.append((min(rw),max(rw)+1))
   a=a24.layout();a.update({'SAM':l['SAM'],'internal_SITE':w[4:],'grade':w[:4],'RIGHT':rw,'predicate_flag':private[0],'predicate_work':private[1:],'port':l['port'],'spin':l['spin'],'native_aux_arbitrary':l['aux_arbitrary'],'oldRIGHT_witness':l['oldRIGHT_witness'],'qubits':l['qubits']});a.pop('private_quantum_work',None);assert ns.car_layout(p,slot)==a;a24.validate(a)
   roles['CAR']+=1;sourceprivate['CAR']+=len(private)
 source_intervals.sort();assert all(a[1]<=b[0] for a,b in zip(source_intervals,source_intervals[1:]))
 assert report['source_private_start']==end and report['source_private_width']==cursor-end==4368
 expected_cursor=cursor;offset+=len(expected_slots)
assert expected_cursor==l['qubits'] and offset==len(p['source_slots'])==1372 and roles=={'Choi':1260,'CAR':112} and sourceprivate=={'Choi':30240,'CAR':336}
sc6=l['SC6_selectors']+sum(([r['all_READY'],r['REPORT']] for r in p['reports']),[])+[l['port'],*l['spin'],l['oldRIGHT_witness']];assert p['SC6_local_to_global']==sc6 and len(set(sc6))==23 and l['aux_arbitrary'] not in sc6
births={'processor_and_fair':7*comp['fresh_RAW_v_births_for_processor_and_fair'],'Choi_DATA':1260*22,'Choi_private':1260*24,'CAR_source':112*19,'CAR_private':112*3,'sigma':7,'external_SITE':8,'SC6_selector':5,'active_port':1};assert births==p['WORK_RAW_birth_inventory'] and sum(births.values())==p['WORK_RAW_birth_count']==10407048092
assert l['qubits']==sum(births.values())+2688+4
# Re-check inputs after the audit, so a simultaneous source edit is detected.
for path,digest in p['source_sha256'].items():assert sha(Path(path))==digest,path
out={'status':'PASS_A25_ALL_SLOT_ROLE_BINDING_AND_SOURCE_ADDRESS_ORDER','A25_source_sha256':sha(src),'A25_plan_sha256':sha(f),'A15_table_rows_checked':dict(checks),'all_Choi_22bit_labels_roundtrip':len(x),'all_CAR_12bit_labels_roundtrip':len(y),'A17_all_source_slots_checked':dict(roles),'actual_A25_provider_layouts_validated':{'A22_Choi':1260,'A24_CAR':112,'B45_SITE':1},'Choi_roles':'w[0:5]=output j, w[5:10]=input i, w[10:22]=address a','CAR_roles':'w[0:4]=grade, w[4:12]=internal SITE; separate 7 fresh RIGHT','SC6_23_roles_disjoint_and_correct':True,'seven_report_sigma_signs':-1,'WORK_RAW_birth_count':sum(births.values()),'separate_SAM_RAW_births':2688,'whole_H1_generator_emitted_or_executed':False,'physical_births_marks_admission_proved':False,'full_T6_or_physical_C_proved':False,'GR_closed':False}
(P/'A25_NAMESPACE_BIT_ORDER_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'source_slots':dict(roles),'lookup_rows':dict(checks),'Choi_labels':len(x),'CAR_labels':len(y)}))
