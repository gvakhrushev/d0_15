#!/usr/bin/env python3
"""Compare real component DAG samples before/after actual A25 bindings."""
from pathlib import Path
from itertools import islice
from hashlib import sha256
import importlib.util,json,sys
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
sys.path[:0]=[str(D/'round22'),str(D/'round18')];ns=load('b50_namespace2',D/'round25/h1_namespace.py');choi=load('b50_choi2',D/'round22/full_choi_bank.py');car=load('b50_car2',D/'round24/full_car_source.py');site=load('b50_site2',O/'round45/site_native.py');a17=load('b50_a17',D/'round17/report_assembly.py')
f=D/'round25/H1_NAMESPACE_PLAN.json';p=json.loads(f.read_text());h=lambda x:sha256(x.read_bytes()).hexdigest()
for name,digest in p['source_sha256'].items():assert h(Path(name))==digest

def binds(a,b,keys):
 out={}
 for k in keys:
  aa=a[k] if isinstance(a[k],list) else [a[k]];bb=b[k] if isinstance(b[k],list) else [b[k]];assert len(aa)==len(bb)
  for x,y in zip(aa,bb):assert x not in out or out[x]==y;out[x]=y
 return out
def remap(t,m):
 op=t['op']
 if op=='seq':return {'op':'seq','children':[remap(c,m) for c in t['children']]}
 if op=='repeat':return {'op':'repeat','count':t['count'],'child':remap(t['child'],m)}
 return {'op':op,'wires':[m[w] for w in t['wires']]}
def compare(a,b,m):
 assert len(a)==len(b)
 for index,(x,y) in enumerate(zip(a,b)):assert remap(x,m)==y,index
 return len(a)
rows=[]
for report in p['reports']:
 for kind in ('Choi','CAR'):
  slots=[p['source_slots'][i] for i in report['source_slots'] if p['source_slots'][i]['kind']==kind]
  for slot in ([slots[0],slots[-1]] if report['bank']=='y+' else [slots[0]]):
   if kind=='Choi':
    default=choi.layout();bound=ns.choi_layout(p,slot);keys=['SAM','address','choi_input','choi_output','branch','phase_rebit','comparator_scratch','port','spin','aux_arbitrary','oldRIGHT_witness'];m=binds(default,bound,keys)
    old=list(islice(choi.raw_prepared_blocks(report['bank'],default),50));new=list(islice(choi.raw_prepared_blocks(report['bank'],bound),50));n=compare(old,new,m);stages='24 private RAW, 22 DATA RAW, first 4 joint Gray blocks'
   else:
    default=car.layout();bound=ns.car_layout(p,slot);keys=['SAM','internal_SITE','grade','RIGHT','predicate_flag','predicate_work','port','spin','native_aux_arbitrary','oldRIGHT_witness'];m=binds(default,bound,keys)
    old=list(islice(car.source_blocks(report['bank'],default),30));new=list(islice(car.source_blocks(report['bank'],bound),30));n=compare(old,new,m)
    old=list(islice(car.frame_blocks(report['bank'],default),3));new=list(islice(car.frame_blocks(report['bank'],bound),3));n+=compare(old,new,m);stages='3 predicate RAW, first 27 prefix blocks, first 3 actual A18 frame blocks'
   rows.append({'bank':report['bank'],'kind':kind,'walk':slot['walk'],'copy':slot['copy'],'actual_DAG_blocks_equal':n,'coverage':stages})
# B45 exact same actual source blocks under A25 site layout.
sd=site.layout();sb=ns.site_layout(p);sm=binds(sd,sb,['SITE','aux_arbitrary','port','spin','oldRIGHT_witness']);lib=site.library();site_n=compare(list(islice(site.site_blocks(lib,sd),20)),list(islice(site.site_blocks(lib,sb),20)),sm)
# A17 actual source RAW prefix: map through the actual A25 report_wire.
angle=json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text());k=int(angle['k']);plan=p['local_report'];N=plan['logical_wire_count'];reports=[]
for report in p['reports']:
 m={q:ns.report_wire(p,report,q) for q in list(range(9))+list(range(N,N+5))}
 first=list(islice(a17.report_native_blocks(plan,k),16))
 # Infer and verify all logical operands in these RAW prefix blocks, whose
 # source addresses can be much larger than the 23 designated native roles.
 for t in first:
  def visit(z):
   if z['op']=='seq':
    for c in z['children']:visit(c)
   elif z['op']=='repeat':visit(z['child'])
   else:
    for w in z['wires']:m[w]=ns.report_wire(p,report,w)
  visit(t)
 mapped=[remap(t,m) for t in first]
 assert all(p['layout']['aux_arbitrary'] not in leaf['wires'] for t in mapped for leaf in a17.s.nb.leaves(t))
 reports.append({'bank':report['bank'],'actual_initial_RAW_DAG_blocks_remapped':len(mapped)})
# Actual SC6 full primitive sequence mapped in place: no aux/old witness targets.
sc6=p['SC6_local_to_global'];gates=[json.loads(x) for x in (O/'round21/SC6_FORWARD.jsonl').read_text().splitlines()]
for gate in gates:
 ws=[sc6[w] for w in gate['wires']];assert p['layout']['aux_arbitrary'] not in ws and p['layout']['oldRIGHT_witness'] not in ws
 if gate['op']=='G':assert ws==[p['layout']['port']]
 if gate['op']=='CX':assert ws[0] in sc6[:19] and ws[1]==p['layout']['port']
 if gate['op']=='SourceI':assert ws==[p['layout']['port'],*p['layout']['spin']]
for name,digest in p['source_sha256'].items():assert h(Path(name))==digest,name
out={'status':'PASS_A25_ACTUAL_PROVIDER_DAG_REMAP_SAMPLES','A25_source_sha256':h(D/'round25/h1_namespace.py'),'A25_plan_sha256':h(f),'source_samples':rows,'B45_actual_SITE_blocks_compared':site_n,'A17_initial_RAW_remap_samples':reports,'SC6_entire_actual_primitive_forward_mapped':len(gates),'global_producer_report_reverse_or_full_A_emitted':False,'semantic_commutation_basis':'B48/B49 completed macro proofs and these concrete provider bindings; no inference at intermediate parity CX boundaries','whole_H1_T6_or_birth_mark_admission_proved':False,'GR_closed':False}
(P/'A25_ACTUAL_PROVIDER_REMAP_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'source_slot_samples':len(rows),'SITE_DAG_blocks':site_n,'SC6_gates':len(gates)}))
