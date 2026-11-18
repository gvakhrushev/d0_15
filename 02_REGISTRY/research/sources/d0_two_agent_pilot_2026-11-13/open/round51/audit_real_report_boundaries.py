#!/usr/bin/env python3
"""Check real A17 report stream ends and global native address remapping."""
from pathlib import Path
from hashlib import sha256
from itertools import islice
from collections import Counter
import importlib.util,json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round25'));import reversible_report_stream as r;import h1_namespace as ns
nb=r.nb;a=r.a;h=lambda q:sha256(q.read_bytes()).hexdigest();files=[D/'round25/reversible_report_stream.py',D/'round25/h1_namespace.py',D/'round25/H1_NAMESPACE_PLAN.json',D/'round17/report_assembly.py',D/'round17/GLOBAL_REPORT_PLAN.json'];pins={str(q):h(q) for q in files};plan=json.loads((D/'round17/GLOBAL_REPORT_PLAN.json').read_text());full=json.loads((D/'round25/H1_NAMESPACE_PLAN.json').read_text());k=int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']);port=plan['native_port'];spin=tuple(plan['native_spin']);N=plan['logical_wire_count'];gp=full['layout']['port'];gs=tuple(full['layout']['spin']);rep=full['reports'][0]
def inv(t,p,sp):
 op=t['op']
 if op=='seq':return nb.seq(*(inv(x,p,sp) for x in reversed(t['children'])))
 if op=='repeat':return nb.repeat(int(t['count']),inv(t['child'],p,sp))
 if op=='CX':return t
 if op=='SourceI':return nb.repeat(3,t)
 assert op=='G';q=t['wires'][0];src=nb.gate('SourceI',p,*sp);c=nb.seq(src,src,nb.repeat(1,nb.gate('G',p)),src,src)
 if q==p:return c
 def swap(x,y):return nb.seq(nb.gate('CX',x,y),nb.gate('CX',y,x),nb.gate('CX',x,y))
 return nb.seq(swap(q,p),c,swap(q,p))
def invd(t,d,p,sp):
 for _ in range(d):t=inv(t,p,sp)
 return t
def remap(t):return a.remap_native(t,lambda q:ns.report_wire(full,rep,q))
zeros=(q for start,width in plan['processor_zero_ranges'] for q in range(start,start+width));first_zero=list(islice(zeros,4));rows=[]
for depth in range(4):
 got=list(islice(r.report_blocks(plan,k,depth),4));assert len(got)==4
 if depth%2==0:
  base=[nb.rotation_power(q,-1,port,spin) for q in first_zero];intrinsic=0;stage='ZERO'
 else:
  base=[a.lower_gate(plan,k,a.and_compute_gate(plan,i)) for i in range(4)];intrinsic=1;stage='READY_UNCOMPUTE'
 expected=[invd(t,depth+intrinsic,port,spin) for t in base];assert got==expected,(depth,stage)
 for t in base:
  assert remap(invd(t,depth+intrinsic,port,spin))==invd(remap(t),depth+intrinsic,gp,gs)
 rows.append({'depth':depth,'first_stage':stage,'actual_blocks':len(got),'intrinsic_inverse_depth':intrinsic,'true_inversion_depth':depth+intrinsic,'global_remap_exact':True})
assert list(islice(r.report_blocks(plan,k,0),16))==list(islice(a.report_native_blocks(plan,k),16))
for path,pin in pins.items():assert h(Path(path))==pin
out={'status':'PASS_ACTUAL_A17_OUTER_BOUNDARY_AND_A25_REMAP','input_sha256':pins,'actual_READY_total_flags':plan['READY_total_flags'],'actual_processor_zero_births':sum(n for q,n in plan['processor_zero_ranges']),'first_boundary_native_AST_checks':rows,'A17_forward_16_actual_blocks_equal':True,'all_stages_or_billion_blocks_executed':False,'no_giant_repeat_expanded':True,'physical_marks_and_admission_proved':False,'GR_closed':False}
(P/'A17_ACTUAL_BOUNDARY_REMAP_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'depth_boundaries':len(rows),'READY_flags':plan['READY_total_flags']}))
