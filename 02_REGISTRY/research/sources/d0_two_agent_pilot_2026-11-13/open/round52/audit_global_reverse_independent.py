#!/usr/bin/env python3
"""Independent raw AST inverse of full SC6 plus all-stage bounded A/W fixture."""
from pathlib import Path
from itertools import zip_longest
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round25'));import global_h1 as g
nb=g.nb;plan=g.namespace();l=plan['layout'];p=l['port'];sp=tuple(l['spin']);f=D/'round25/global_h1.py';h=lambda x:sha256(x.read_bytes()).hexdigest();pin=h(f)
for path,digest in json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text())['source_sha256'].items():assert h(Path(path))==digest,path
def inv(t,p,sp):
 op=t['op']
 if op=='seq':return nb.seq(*(inv(x,p,sp) for x in reversed(t['children'])))
 if op=='repeat':return nb.repeat(int(t['count']),inv(t['child'],p,sp))
 if op=='CX':return t
 if op=='SourceI':return nb.repeat(3,t)
 assert op=='G';q=t['wires'][0];src=nb.gate('SourceI',p,*sp);core=nb.seq(src,src,nb.repeat(1,nb.gate('G',p)),src,src)
 if q==p:return core
 def swap(x,y):return nb.seq(nb.gate('CX',x,y),nb.gate('CX',y,x),nb.gate('CX',x,y))
 return nb.seq(swap(q,p),core,swap(q,p))
def invd(t,d,p,sp):
 for _ in range(d):t=inv(t,p,sp)
 return t
def blocks_depth(ts,d,p,sp):
 for _ in range(d):ts=[inv(t,p,sp) for t in reversed(ts)]
 return ts
def eq(left,right):
 n=0
 for a,b in zip_longest(left,right):assert a==b,('mismatch',n);n+=1
 return n
# Independently map every original SC6 primitive and its own literal inverse.
word=[json.loads(x) for x in (g.B/'round21/SC6_FORWARD.jsonl').read_text().splitlines()];mp=plan['SC6_local_to_global'];full=[]
for t in word:
 q=nb.gate(t['op'],*(mp[w] for w in t['wires']));full.append(q)
assert len(full)==18176
sc=[]
for depth in range(4):
 want=(invd(t,depth,p,sp) for t in (reversed(full) if depth%2 else full));got=g.stage_blocks({'kind':'SC6'},plan,depth);sc.append({'depth':depth,'actual_blocks':eq(got,want)})
print(json.dumps({'full_SC6_actual_blocks_checked':sum(x['actual_blocks'] for x in sc)}),flush=True)
# Distinct synthetic provider words encode every true source/report address.
# They are fixtures, not the giant true provider streams. Preserve the actual
# all-slot routing and all SIGMA/PORT steps; separately SC6 was tested above.
def tape(q,p,sp):return [nb.gate('CX',p,q),nb.repeat(2,nb.gate('G',q)),nb.gate('SourceI',p,*sp)]
def provider(ts,depth,p,sp):yield from blocks_depth(ts,depth,p,sp)
def ch(bank,lay,depth=0,extra_external=()):yield from provider(tape(lay['branch'],lay['port'],tuple(lay['spin'])),depth,lay['port'],tuple(lay['spin']))
def ca(bank,lay,depth=0,extra_external=()):yield from provider(tape(lay['predicate_flag'],lay['port'],tuple(lay['spin'])),depth,lay['port'],tuple(lay['spin']))
def si(lib,lay=None,depth=0):yield from provider(tape(lay['SITE'][0],lay['port'],tuple(lay['spin'])),depth,lay['port'],tuple(lay['spin']))
def rp(local,k,depth=0):yield from provider(tape(local['report_wire'],local['native_port'],tuple(local['native_spin'])),depth,local['native_port'],tuple(local['native_spin']))
short=word[:7]+word[-7:];original=(g.choi.raw_prepared_blocks,g.car.source_blocks,g.site.site_blocks,g.report.report_blocks,g.sc6_word,g.site_library)
try:
 g.choi.raw_prepared_blocks=ch;g.car.source_blocks=ca;g.site.site_blocks=si;g.report.report_blocks=rp;g.sc6_word=lambda:short;g.site_library=lambda:{}
 # Independent stage chronology, not constructed through g.stages or g.stage_blocks.
 expected=tape(l['SITE'][0],p,sp)
 for ri,rep in enumerate(plan['reports']):
  expected.append(invd(nb.gate('G',rep['sigma']),1,p,sp))
  for idx in rep['source_slots']:
   slot=plan['source_slots'][idx];q=slot['private'][0];expected.extend(tape(q,p,sp))
  rq=g.ns.report_wire(plan,rep,plan['local_report']['report_wire']);expected.extend(tape(rq,p,sp))
 expected.append(invd(nb.gate('G',p),1,p,sp));expected.extend(nb.gate(t['op'],*(mp[w] for w in t['wires'])) for t in short)
 checks=[]
 for depth in range(4):checks.append({'A_depth':depth,'compact_blocks':eq(g.A_blocks(plan,depth),blocks_depth(expected,depth,p,sp))})
 z=nb.seq(nb.gate('SourceI',p,*sp),nb.gate('SourceI',p,*sp));w=expected+[z]+blocks_depth(expected,1,p,sp)
 for depth in range(3):checks.append({'W_depth':depth,'compact_blocks':eq(g.W_blocks(plan,depth),blocks_depth(w,depth,p,sp))})
finally:g.choi.raw_prepared_blocks,g.car.source_blocks,g.site.site_blocks,g.report.report_blocks,g.sc6_word,g.site_library=original
assert h(f)==pin
out={'status':'PASS_INDEPENDENT_GLOBAL_LITERAL_REVERSE_FIXTURE','source_sha256':pin,'actual_SC6_all_blocks_depth0_to3':sc,'all_1389_stage_fixture':checks,'fixture_scope':'All true slot and report addresses, true 7 SIGMA and PORT_ZERO; SITE/SOURCE/REPORT replaced by short nontrivial synthetic G/CX/SourceI DAGs, SC6 reduced only in full-word fixture. All 18176 actual SC6 blocks checked separately.','G_repeats_and_full_providers_executed':False,'physical_admission_T6_or_C_proved':False,'GR_closed':False}
(P/'GLOBAL_LITERAL_REVERSE_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'fixture_checks':len(checks),'SC6_depths':len(sc)}))
