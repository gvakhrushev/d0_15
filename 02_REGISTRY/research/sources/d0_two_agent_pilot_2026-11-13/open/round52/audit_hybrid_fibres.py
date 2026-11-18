#!/usr/bin/env python3
"""Check ideal hybrid input fibres from actual A17/A25 range partitions."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');files=[D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',D/'round17/GLOBAL_REPORT_PLAN.json',D/'round22/FULL_CHOI_BANK_PLAN.json',D/'round24/FULL_CAR_SOURCE_PLAN.json'];h=lambda x:sha256(x.read_bytes()).hexdigest();pins={str(f):h(f) for f in files};ns,glob,local,choi,car=[json.loads(q.read_text()) for q in files];assert ns['local_report']==local
# A17 processor's compiler region is exactly partitioned into processor-zero,
# fair output, Golden RAW, and original source buffers. Sigma and SITE excluded.
intervals=[]
for a,n in local['processor_zero_ranges']:intervals.append((a,a+n,'zero'))
for z in local['fair_output_ranges']:intervals.append((z['output_wire_start'],z['output_wire_start']+z['count'],'fair'))
for a,n in local['Golden_RAW_ranges']:intervals.append((a,a+n,'golden'))
for z in local['source_buffers']:
 a,n=z['range'];intervals.append((a,a+n,'source'))
intervals.sort();pos=9;counts={x:0 for x in ('zero','fair','golden','source')}
for a,b,kind in intervals:
 assert a==pos and b>a,(pos,a,b,kind);counts[kind]+=b-a;pos=b
assert pos==local['compiler_region_end'] and counts=={'zero':21210979,'fair':10248262,'golden':76,'source':4264}
assert local['incoming_shared_SITE']==list(range(8)) and local['incoming_sigma_wire']==8
assert local['fair_bank_extra_start']==pos and pos+142*local['fair_bank_count']==local['logical_wire_count']
# Every source's private RAW interval appears only after its containing report
# local arena and before the next report arena; input data belong only to that
# report. No earlier report can access a later report's arena under A25 map.
reports=ns['reports'];slots=ns['source_slots'];N=local['logical_wire_count'];counter={'Choi':0,'CAR':0}
for i,r in enumerate(reports):
 report_start=r['private_start'];report_end=report_start+r['private_width'];assert r['private_width']==N-8 and r['source_private_start']==report_end
 at=report_end
 for idx in r['source_slots']:
  slot=slots[idx];assert slot['bank']==r['bank'];private=slot['private'];width=24 if slot['kind']=='Choi' else 3
  assert len(private)==width and private==list(range(at,at+width));at+=width;assert all(report_start<=q<report_end for q in slot['source'])
  if slot['kind']=='CAR':assert len(slot['RIGHT'])==7 and all(report_start<=q<report_end for q in slot['RIGHT'])
  counter[slot['kind']]+=1
 assert at==report_end+r['source_private_width']
 assert at==(reports[i+1]['private_start'] if i+1<len(reports) else ns['layout']['qubits'])
assert counter=={'Choi':1260,'CAR':112}
assert choi['RAW_prepared_generator_pays_private_initialization'] and car['predicate_RAW_wires']==3 and car['actual_private_output_is_not_assumed_exactly_clean']
assert glob['error_scope'].startswith('canonical product RAW WORK input')
for path,digest in pins.items():assert h(Path(path))==digest
out={'status':'PASS_CANONICAL_INPUT_HYBRID_FIBRE_PARTITION','input_sha256':pins,'A17_compiler_partition_wire_counts':counts,'A17_sigma_and_SITE_excluded_from_compiler_births':True,'report_local_arena_disjoint_across_all7':True,'source_private_RAW_groups_disjoint_and_prepared_only_in_own_source_stage':counter,'argument':'For the hybrid with ideal earlier stages and actual later stages, each later source DATA/private remains at canonical RAW before its own SOURCE stage because earlier components address only their own slot/report arena and named shared factors. The full clean-private input estimate permits arbitrary SAM, SITE, aux, port, Spin and entanglement with all previous/future factors. Actual leaky private outputs are not assumed clean.','scope':'Range/namespace proof depends on B48–B51 provider access/semantics; it does not establish the ideal report probability law, source product physical births, all-original-marks transport or actual physical admission.','all_dirty_helper_columns_against_old_T2_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'GLOBAL_HYBRID_FIBRES_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'compiler_partition':counts,'source_slots':counter}))
