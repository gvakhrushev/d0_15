#!/usr/bin/env python3
"""Use actual A29 transform/stream on bounded production providers."""
from pathlib import Path
from hashlib import sha256
import itertools,json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round58';sys.path.insert(0,str(D/'round29'));import gcx_compiler as c
g=c.old;nb=g.nb;ns=g.namespace();lay=ns['layout'];port=lay['port'];spin=tuple(lay['spin']);helper=lay['qubits'];cc=c.Compiler(port,spin,helper,1)
def all_nodes(t):
 if t['op']=='seq':
  for x in t['children']:yield from all_nodes(x)
 elif t['op']=='repeat':yield from all_nodes(t['child'])
 else:yield t
def check(t,compiler=cc):
 z,p,count=compiler.transform(t);assert p==0 and count['CZ']==0
 for leaf in all_nodes(z):assert leaf['op'] in ('G','CX') and not set(leaf['wires']).intersection(compiler.spin)
 return count
counts={}
# SC6 blocks are raw primitives, including individual SI: prove streaming
# across them, not only an artificially grouped good tree.
original=[nb.gate(z['op'],*(ns['SC6_local_to_global'][q] for q in z['wires'])) for z in g.sc6_word()]
for depth in (0,1):
 blocks=[nb.inverse_literal(t,port,spin) for t in reversed(original)] if depth else original
 pending=0;pairs=0;oldsi=0
 for block in blocks:
  t,pending,n=cc.transform(block,pending);assert n['CZ']==0;pairs+=n['Z']
  for leaf in all_nodes(t):assert leaf['op'] in ('G','CX')
  oldsi+=sum(1 for a in nb.leaves(block) if a['op']=='SourceI') if depth==0 else 0
 assert pending==0
 if depth==0:assert oldsi==8192 and pairs==4096
 counts['SC6_depth'+str(depth)+'_paired_SI']=pairs
# True A25 stage templates for SITE, SIGMA, PORT_ZERO; select full concrete
# DAGs without consuming giant loops.
for stage in ({'kind':'SITE'},{'kind':'SIGMA','report':0},{'kind':'PORT_ZERO'}):
 for depth in (0,1):
  block=next(g.stage_blocks(stage,ns,depth));check(block)
 counts[stage['kind']+'_actual_first_block_depth0_1']=True
# Complete actual fair bank macro at its local report port, depth0 and1.
r=g.report;rp=ns['local_report'];bank=json.loads((O/'round31/NATIVE_FAIR_BANK.json').read_text());tree=r.a.fair_bank_native(rp,0,bank);lp=rp['native_port'];ls=tuple(rp['native_spin']);lc=c.Compiler(lp,ls,rp['native_wire_count_including_oldRIGHT_witness'],1)
for t in (tree,nb.inverse_literal(tree,lp,ls)):check(t,lc)
counts['REPORT_actual_fair_bank_depth0_1']=True
# Actual REPORT READY compute and core (there are 10,249,327 flags, never
# flatten them); their inverse/uncompute are handled by same literal inverse.
for gate in (r.a.and_compute_gate(rp,0),r.a.and_core_gate(rp)):
 t=r.a.lower_gate(rp,g.boolean_k(),gate)
 for u in (t,nb.inverse_literal(t,lp,ls)):check(u,lc)
counts['REPORT_READY_compute_and_core_depth0_1']=True
# CAR source actual fixed STAR and reflection templates, at global addresses.
slot=next(x for x in ns['source_slots'] if x['kind']=='CAR');cl=g.ns.car_layout(ns,slot)
for t in g.car.f.fixed_components(cl):
 for u in (t,nb.inverse_literal(t,port,spin)):check(u)
counts['CAR_actual_fixed_STAR_reflection_depth0_1']=True
# Choi prefix real first block and B39 adapter real H/good/start/correction.
slot=next(x for x in ns['source_slots'] if x['kind']=='Choi');cl=g.ns.choi_layout(ns,slot);loader=g.choi.c;inp=loader.inputs()
tree=next(loader.prefix.prefix_blocks(inp['prefix'],cl,controlled=True));check(tree)
fix=loader.adapter.fixed(loader.adapter_layout(cl),int(inp['phase']['phase_k']),int(inp['phase']['correction_l']),inp['h_k'])
for tree in [fix['H'],fix['correction'],*fix['good'],*fix['start']]:check(tree)
counts['Choi_actual_prefix_and_184_adapter_fixed_blocks']=True
paths=[D/'round29/gcx_compiler.py',D/'round25/global_h1.py',D/'round25/reversible_report_stream.py',D/'round14/native_boolean.py',O/'round21/SC6_FORWARD.jsonl']
out={'status':'PASS_A29_TRANSDUCER_ACTUAL_FAMILY_TEMPLATES','checks':counts,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'complete_stream_executed':False,'all_families_coverage_depends_on_structural_induction':True,'GR_closed':False}
(P/'A29_PROVIDER_TRANSDUCER_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
