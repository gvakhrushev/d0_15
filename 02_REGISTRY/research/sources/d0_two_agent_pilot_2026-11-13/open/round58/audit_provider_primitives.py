#!/usr/bin/env python3
"""Compact checks of actual family templates and read-only SAM/old factors.

Proof for all indices/depths is in B58 report; these checks cover real
metadata, frozen native DAGs, all SC6 leaves, and exact symbolic templates,
not a full flattening of the exponentially large word.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,itertools,json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round58';sys.path.insert(0,str(D/'round25'));import global_h1 as g
nb=g.nb;ns=g.namespace();L=ns['layout'];sam=set(L['SAM']);old=set([*L['spin'],L['oldRIGHT_witness']]);port=L['port'];spin=tuple(L['spin'])
def combine(f,h):return tuple(h[f[i]] for i in range(3))
def power(f,n):
 r=(0,1,2)
 while n:
  if n&1:r=combine(r,f)
  f=combine(f,f);n>>=1
 return r
def trans(t):
 op=t['op']
 if op=='seq':
  v=(0,1,2)
  for c in t['children']:v=combine(v,trans(c))
  return v
 if op=='repeat':return power(trans(t['child']),int(t['count']))
 return (1,0,2) if op=='SourceI' else (0,2,2)
def check_tree(t,forbidden_sam,old_local,allow_si=True):
 assert trans(t)[0]==0
 for x in nb.leaves(t):
  w=x['wires'];op=x['op']
  if op in ('G','CX'):assert w[-1] not in forbidden_sam and not old_local.intersection(w),(op,w)
  else:assert op=='SourceI' and allow_si and not forbidden_sam.intersection(w)
 return True
def inversions(t,port,spin,n=2):
 yield t
 for _ in range(n):t=nb.inverse_literal(t,port,spin);yield t
checks={}
# Complete real SC6 stream, including depth-1 leafwise actual inverse.
sc=g.sc6_word();mapping=ns['SC6_local_to_global'];stream=[nb.gate(x['op'],*(mapping[q] for q in x['wires'])) for x in sc]
for depth in (0,1):
 seq=nb.seq(*(nb.inverse_literal(x,port,spin) for x in reversed(stream))) if depth else nb.seq(*stream)
 assert check_tree(seq,sam,old);checks['actual_SC6_depth'+str(depth)]=len(stream)
# SITE global namespace: fully inspect ordinary emitted first/last trees and
# read-only targets, plus all fixed phase blocks (not its 2^K U masks).
lib=g.site_library();lay=g.ns.site_layout(ns);cmd=g.site.commands(lib,lay);assert len(cmd)>1
for z in (cmd[0],cmd[-1]):
 for depth in (0,1):
  blocks=g.site.selective_blocks(z,lay,depth);first=next(blocks);assert check_tree(first,sam,old)
for depth in (0,1):
 for t in g.site.gray_phase_blocks(g.site.phase_command(lib,lay),lay,depth):assert check_tree(t,sam,old)
checks['SITE_actual_boundary_templates']=True
# Production A19 controlled Choi prefix, all its real instructions and gates.
choi=g.choi.c;cl=choi.layout();cs=set(cl['SAM']);co=set([*cl['spin'],cl['oldRIGHT_witness']]);x=choi.inputs()
for depth in (0,1):
 rows=list(choi.prefix.prefix_blocks(x['prefix'],cl,controlled=True,reverse=bool(depth)))
 for t in rows:assert check_tree(t,cs,co)
checks['Choi_prefix_all_blocks_depth0_1']=len(rows)
# Concrete full B39 adapter fixed components, actual N=23 source layout.
al=choi.adapter_layout(cl);fixed=choi.adapter.fixed(al,int(x['phase']['phase_k']),int(x['phase']['correction_l']),x['h_k']);asts=[fixed['H'],fixed['correction'],*fixed['good'],*fixed['start']]
for t in asts:
 for d in inversions(t,cl['port'],tuple(cl['spin']),1):assert check_tree(d,cs,co)
checks['Choi_adapter_actual_fixed_blocks_each_depth0_1']=len(asts)
# Actual frozen fair and U-star DAGs, SAM-independent local interfaces.
fair=json.loads((O/'round31/NATIVE_FAIR_BANK.json').read_text());star=json.loads((O/'round37/CAR_USTAR_NATIVE.json').read_text())
for t in [fair['router_forward_DAG'],fair['router_literal_raw_inverse_DAG'],nb.seq(*fair['zero_and_kernel_forward']['gates']),nb.seq(*fair['zero_and_kernel_literal_inverse']),star['forward_DAG'],star['literal_raw_inverse_DAG']]:assert trans(t)[0]==0
checks['frozen_fair_and_CAR_Ustar_DAGs']=6
# Original SC6 mapping and actual local report mapper exclude every SAM;
# reports map only SITE, private range, port, spin, aux, old witness.
assert not sam.intersection(mapping)
for report in ns['reports']:
 assert report['private_start']>=2706 and report['private_width']>0
 for q in [0,7,8,ns['local_report']['logical_wire_count']-1,*range(ns['local_report']['logical_wire_count'],ns['local_report']['logical_wire_count']+5)]:
  assert g.ns.report_wire(ns,report,q) not in sam
assert [s['kind'] for s in g.stages(ns)].count('REPORT')==7
checks['report_namespace_7_private_ranges_no_SAM']=True
# Material / coframe / proper-link selected actual command family objects:
# selected targets/permutations are WORK; source proof generalizes to all rows.
slot=next(s for s in ns['source_slots'] if s['kind']=='CAR');car=g.ns.car_layout(ns,slot);mat=g.car.f.m;mlib=g.car.library()
for bank in ('q','y+','y-'):
 row=mlib['catalogue'][bank][0];rot=next(z for z in mlib['vectors'][row['vector_id']]['rotations'] if z['angle_id'] is not None)
 bound=mat.bind_plane(row,rot,car,mlib['angles']);assert bound['target'] not in sam and all(z['wires'][-1] not in sam for z in bound['permutation'])
 for rev in (False,True):
  for t in itertools.islice(mat.pair_blocks(bound,car,rev),3):assert check_tree(t,sam,old)
checks['CAR_material_actual_bank_templates']=3
# Complete actual CAR U-star and grade anchor boundaries, plus all fixed
# vacuum-stage blocks and real Fourier command metadata (no mask expansion).
for t in g.car.f.fixed_components(car):
 for d in inversions(t,port,spin,1):assert check_tree(d,sam,old)
v=g.car.v;vin=v.inputs()
for stage in ('RAW','H','VAC'):
 for t in v.fixed_blocks(stage,car,vin['boolean_k']):
  for d in inversions(t,port,spin,1):assert check_tree(d,sam,old)
commands=list(v.commands(vin['kappa'],car,vin['phase_k']))
for command in commands:
 assert command['target'] not in sam and command['target'] not in old
for command in commands[:3]:
 for d in (0,1):
  for t in itertools.islice(v.rotation_blocks(command,car,d),2):assert check_tree(t,sam,old)
checks['CAR_fixed_anchor_and_vacuum_all_command_targets']=len(commands)
# Actual coframe and proper-link catalogue boundary entries for every bank;
# all emitted target sets are checked without enumerating their Walsh masks.
cf=choi.coframe;link=choi.link;libcf=x['coframe'];liblink=x['link'];families={f['family']:f for f in liblink['families']};units=0;commands_seen=0
for bank in ('y+','y-','f','0','x+','x-','q'):
 rows=libcf['catalogue'][bank]
 for row in (rows[0],rows[-1]):
  for bound,depth in cf.sector_units(row,libcf,cl,True):
   assert bound['target'] not in cs|co and all(z['wires'][-1] not in cs|co for z in bound['permutation']);units+=1
   for t in itertools.islice(cf.unit_blocks(bound,depth,cl),2):assert check_tree(t,cs,co)
 entries=liblink['catalogue'][bank]
 for entry in (entries[0],entries[-1]):
  ll=link.bind_global(cl,entry)
  for command in link.commands(ll,entry,families[entry['family_id']],liblink['controlled_X']):
   assert command['target'] not in cs|co;commands_seen+=1
   for rev in (False,True):
    for t in itertools.islice(link.emit_command(command,ll,reverse=rev),2):assert check_tree(t,cs,co)
checks['Choi_coframe_actual_boundary_units']=units
checks['Choi_link_actual_boundary_commands']=commands_seen
# SITE, port, SAM, old constraints of source namespace apply to ALL source slots.
for slot in ns['source_slots']:
 il=g.ns.choi_layout(ns,slot) if slot['kind']=='Choi' else g.ns.car_layout(ns,slot)
 assert il['SAM']==L['SAM'] and il['port']==port and il['spin']==list(spin) and il['oldRIGHT_witness']==3
 if slot['kind']=='Choi':targets=il['address']+il['choi_input']+il['choi_output']+[il['branch'],il['phase_rebit'],*il['comparator_scratch'],il['aux_arbitrary']]
 else:targets=il['internal_SITE']+il['grade']+il['RIGHT']+[il['predicate_flag'],*il['predicate_work'],il['native_aux_arbitrary']]
 assert not sam.intersection(targets) and not old.intersection(targets) and port not in targets
checks['all_source_slot_WORK_roles_disjoint_SAM_old_port']=len(ns['source_slots'])
# B56 real odd CZ path is intentionally handled separately, not guessed paired.
assert trans(nb.seq(*(nb.gate(z.op,*z.wires) for z in g.report.s.cz.cz_word(5,6,port,spin))))[0]==2
paths=[D/'round14/native_boolean.py',D/'round13/compile_native_cz.py',D/'round16/source_select.py',D/'round17/report_assembly.py',D/'round18/material_preparation.py',D/'round18/car_frame.py',D/'round19/choi_prefix.py',D/'round20/coframe_native.py',D/'round21/choi_loader.py',D/'round22/full_choi_bank.py',D/'round22/gray_reflection.py',D/'round23/car_vacuum_prefix.py',D/'round24/full_car_source.py',D/'round25/global_h1.py',D/'round25/h1_namespace.py',D/'round25/reversible_report_stream.py',O/'round35/anchor_reflection.py',O/'round39/adapter_native.py',O/'round42/proper_link_native.py',O/'round45/site_native.py',O/'round31/NATIVE_FAIR_BANK.json',O/'round37/CAR_USTAR_NATIVE.json',O/'round21/SC6_FORWARD.jsonl',D/'round25/H1_NAMESPACE_PLAN.json']
out={'status':'PASS_COMPACT_FAMILY_TEMPLATES_AND_GLOBAL_WIRE_ROLES','checks':checks,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'full_global_word_expanded':False,'proof_scope':'inductive family argument required; finite template checks alone do not prove full program','physical_admission_or_marked_map_proved':False,'GR_closed':False}
(P/'PROVIDER_TEMPLATE_AND_WIRE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks':checks}),flush=True)
