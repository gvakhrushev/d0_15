#!/usr/bin/env python3
"""Exercise actual A16 -> A17 -> A25 CZ mapping at real Hq endpoint slots."""
from pathlib import Path
from hashlib import sha256
import json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=Path(__file__).resolve().parent;sys.path.insert(0,str(D/'round29'));import gcx_compiler as c
g=c.old;r=g.report;s=r.s;nb=c.nb;ns=g.namespace();rp=ns['local_report'];walk=next(w for w in rp['walks'] if w['root']=='H_q_before_inverse_PF');name=walk['root'];tables,events,records,plan,record,mapping,h,root_phase,size=r.walk_structure(name)
assert len(records)==18 and len(plan['copy_calls'])==4 and size==walk['local_wires'];n=rp['logical_wire_count'];report=ns['reports'][0];compiler=c.production_compiler();k=g.boolean_k();checked=[]
for slot in (0,len(records)-1):
 m=list(mapping)
 for a,b in zip(record,records[slot]):m[a]=b
 for ci,call in enumerate(plan['copy_calls']):
  ir=s.map_ir(call['IR'],m);base=s.lower(ir,k,size,(size+1,size+2),size+3)
  for depth in (0,1):
   tree=nb.inverse_literal(base,size,(size+1,size+2)) if depth else base
   # Exact owner maps: walk local -> report local -> A25 global.
   def mapq(q):return r.a.global_wire(walk,q) if q<walk['local_wires'] else rp['native_port']+q-walk['local_wires']
   tree=r.a.remap_native(tree,mapq);tree=r.a.remap_native(tree,lambda q:g.ns.report_wire(ns,report,q))
   result,pending,count=compiler.transform(tree);assert pending==0 and count['CZ']==1 and count['CZ_depth_'+str(depth)]==1
   assert count['CZ_old_SourceI']==5*3**depth and count['CZ_old_CX']==14
   for leaf in nb.leaves(result):assert leaf['op'] in ('G','CX') and not set(leaf['wires']).intersection([0,1,3])
   checked.append([slot,ci,depth])
files=[D/'round29/gcx_compiler.py',D/'round25/reversible_report_stream.py',D/'round25/h1_namespace.py',D/'round25/H1_NAMESPACE_PLAN.json']
out={'status':'PASS_ACTUAL_HQ_CZ_END_SLOT_GLOBAL_REMAP','tested_slot_copy_depth':checked,'real_hq_record_count':len(records),'full_word_expanded':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'ACTUAL_GLOBAL_REMAP_CZ_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(checked)}),flush=True)
