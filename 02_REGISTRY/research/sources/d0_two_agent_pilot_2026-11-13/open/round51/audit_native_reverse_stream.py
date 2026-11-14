#!/usr/bin/env python3
"""Independent literal AST inversion, A17 READY and bounded real A16 walk."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from itertools import zip_longest
from collections import Counter
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round25'));import reversible_report_stream as r
s=r.s;d=r.d;nb=r.nb;a=r.a;h=lambda f:sha256(f.read_bytes()).hexdigest();files=[D/'round25/reversible_report_stream.py',D/'round14/native_boolean.py',D/'round15/source_dispatcher.py',D/'round16/source_select.py',D/'round17/report_assembly.py',D/'round17/GLOBAL_REPORT_PLAN.json'];pins={str(x):h(x) for x in files};k=int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k'])
def inv(t,port,spin):
 op=t['op']
 if op=='seq':return nb.seq(*(inv(x,port,spin) for x in reversed(t['children'])))
 if op=='repeat':return nb.repeat(int(t['count']),inv(t['child'],port,spin))
 if op=='CX':return t
 if op=='SourceI':return nb.repeat(3,t)
 assert op=='G';q=t['wires'][0];src=nb.gate('SourceI',port,*spin);core=nb.seq(src,src,nb.repeat(1,nb.gate('G',port)),src,src)
 if q==port:return core
 def swap(x,y):return nb.seq(nb.gate('CX',x,y),nb.gate('CX',y,x),nb.gate('CX',x,y))
 return nb.seq(swap(q,port),core,swap(q,port))
def literal_depth(blocks,depth,port,spin):
 out=list(blocks)
 for _ in range(depth):out=[inv(t,port,spin) for t in reversed(out)]
 return out
def count(t,port):
 op=t['op']
 if op=='seq':
  c=Counter()
  for x in t['children']:c.update(count(x,port))
  return c
 if op=='repeat':return Counter({q:int(t['count'])*v for q,v in count(t['child'],port).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def total(ts,port):
 c=Counter()
 for t in ts:c.update(count(t,port))
 return c
def invprice(c):return Counter(G_port=c['G_port']+c['G_other'],G_other=0,CX=c['CX']+6*c['G_other'],SourceI=3*c['SourceI']+4*(c['G_port']+c['G_other']))
plan=json.loads((D/'round17/GLOBAL_REPORT_PLAN.json').read_text());ready=[]
for K in (3,5,8):
 p=deepcopy(plan);p['fair_bank_count']=min(3,K);p['READY_total_flags']=K;port=p['native_port'];spin=tuple(p['native_spin']);base=list(a.ready_native_blocks(p,k));prev=base
 for depth in range(4):
  actual=list(r.ready_blocks(p,k,depth));assert actual==prev,(K,depth);assert len(actual)==2*K-3
  if depth:assert +total(actual,port)==+invprice(last)
  last=total(actual,port);ready.append({'READY_flags':K,'literal_depth':depth,'actual_blocks':len(actual),'keeps_uncompute_native_depth':True})
  prev=[inv(t,port,spin) for t in reversed(prev)]
print(json.dumps({'READY_depth_checks':len(ready)}),flush=True)
# Exercise the actual A16 quantum walk source for q: retain the first and last
# actual source records and original IR, with controller words suppressed.
# This is a genuine owner program with bounded slots, not a full walk claim.
name='H_q_before_inverse_PF';tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());events=list(d.walk_events(tables,name));trans=[e for e in events if e['kind']=='transition'];assert len(trans)==18;subset=[trans[0],trans[-1],events[-1]]
old=(d.walk_events,d.event_word,r.event_word)
def limited(tt,n):assert n==name;yield from subset
def empty(*args,**kwargs):return iter(())
walk=[]
try:
 d.walk_events=limited;d.event_word=empty;r.event_word=empty;r.walk_structure.cache_clear()
 native=list(s.walk_native_blocks(name,k));size=r.walk_structure(name)[-1];port=size;spin=(size+1,size+2);assert len(native)==2+2*(1+4)+2
 prior=native
 for depth in range(3):
  actual=list(r.walk_blocks(name,k,depth));assert actual==prior,('A16 bounded quantum walk',depth);walk.append({'literal_depth':depth,'native_blocks':len(actual),'actual_retained_slots':[0,17],'controller_tuples_suppressed':True})
  prior=[inv(t,port,spin) for t in reversed(prior)]
finally:d.walk_events,d.event_word,r.event_word=old;r.walk_structure.cache_clear()
# Validate fixed root-phase and literal depths independently, with true local
# roles and the A17 mapping into global report addresses, not a fresh model.
structure=r.walk_structure(name);phase=structure[-2];size=structure[-1];port=size;spin=(size+1,size+2);tree=s.lower(phase,k,port,spin,size+3);localwalk=next(w for w in plan['walks'] if w['root']==name);gport=plan['native_port'];gspin=tuple(plan['native_spin']);mapping=lambda w:a.global_wire(localwalk,w) if w<localwalk['local_wires'] else gport+w-localwalk['local_wires']
for depth in range(4):
 left=a.remap_native(literal_depth([tree],depth,port,spin)[0],mapping);right=literal_depth([a.remap_native(tree,mapping)],depth,gport,gspin)[0];assert left==right
for path,digest in pins.items():assert h(Path(path))==digest,path
out={'status':'PASS_INDEPENDENT_READY_AND_A16_BOUNDED_LITERAL_REVERSE','source_sha256':pins,'READY_tests':ready,'bounded_actual_A16_quantum_walk':walk,'root_phase_native_map_commutes_with_literal_inverse_depths':4,'logical_controller_giant_word_executed':False,'native_huge_repeat_expanded':False,'physical_T6_or_marks_proved':False,'GR_closed':False}
(P/'A17_NATIVE_INDEPENDENT_REVERSE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'ready_checks':len(ready),'walk_depths':len(walk),'root_phase_depths':4}),flush=True)
