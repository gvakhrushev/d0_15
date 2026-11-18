#!/usr/bin/env python3
"""Independent A18 seven CAR-frame accounting and actual stage order."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=D/'round18';sys.path.insert(0,str(P));spec=importlib.util.spec_from_file_location('b38_frame_inventory',P/'car_frame.py');f=importlib.util.module_from_spec(spec);sys.modules[spec.name]=f;spec.loader.exec_module(f)
lib=json.loads((P/'MATERIAL_PREPARATION_LIBRARY.json').read_text());inv=json.loads((P/'MATERIAL_PREPARATION_INVENTORY.json').read_text());pp=P/'CAR_FRAME_PLAN.json';plan=json.loads(pp.read_text());sha=lambda x:sha256(x.read_bytes()).hexdigest();plan_hash=sha(pp);assert inv['library_sha256']==sha(P/'MATERIAL_PREPARATION_LIBRARY.json')
for file,h in plan['inputs_sha256'].items():assert sha(Path(file))==h,file
lay=f.layout();U,Ui,R=f.fixed_components(lay);port=lay['port']
def count(t):
 op=t['op']
 if op=='seq':
  c=Counter()
  for x in t['children']:c.update(count(x))
  return c
 if op=='repeat':return Counter({a:int(t['count'])*v for a,v in count(t['child']).items()})
 if op=='G':return Counter({'G_port' if t['wires'][0]==port else 'G_other':1})
 return Counter({op:1})
def eq(c,d):return all(c[k]==int(d.get(k,0)) for k in ('G_port','G_other','CX','SourceI'))
def rev(c):return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
u,ui,r=count(U),count(Ui),count(R);assert +ui==+rev(u)
allcopies=Counter();banks={}
for bank in ('y+','y-','f','0','x+','x-','q'):
 c=u+ui+Counter({k:2*v for k,v in r.items()})
 if bank in ('q','y+','y-'):
  c.update({k:int(v) for k,v in inv['banks'][bank]['native_forward'].items()});c.update({k:int(v) for k,v in inv['banks'][bank]['native_literal_inverse'].items()})
 else:
  stages=list(f.frame_blocks(bank,lib));assert stages==[Ui,R,U,Ui,R,U]
  c.update(u);c.update(ui)
 assert eq(c,plan['banks'][bank]['native_forward']) and eq(rev(c),plan['banks'][bank]['native_literal_inverse'])
 assert plan['banks'][bank]['endpoint_is_exact_identity']==(bank in ('f','0','x+','x-'))
 allcopies.update({k:16*v for k,v in c.items()});banks[bank]={'resource_verified':True,'identity_exact':bank in ('f','0','x+','x-')}
assert eq(allcopies,plan['112_CAR_copy_conservative_forward_inventory']) and plan['112_CAR_copy_conservative_error_lt']=='2^-4084'
a17=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text());prior=a17['seven_report_all_known_approximate_macros'];combined=prior+112*28
assert prior==162754649904 and combined==162754653040 and combined<2**38
# Sample actual q finite subgrammar with one K11 and one K13 row. Verify full
# frame sequence including reverse/forward blocks without expanding repeats.
sampled={}
for label,row in [('K11',next(x for x in lib['catalogue']['q'] if not x['SAM_indices'])),('K13',next(x for x in lib['catalogue']['q'] if x['SAM_indices']))]:
 vid=row['vector_id'];rotation=next(x for x in lib['vectors'][vid]['rotations'] if x['angle_id'] is not None)
 mock={'catalogue':{'q':[row]},'vectors':{vid:{'rotations':[rotation]}},'angles':lib['angles']}
 stream=iter(f.frame_blocks('q',mock));assert [next(stream) for _ in range(3)]==[Ui,R,U]
 inverse=list(f.m.preparation_blocks('q',mock,lay,True));forward=list(f.m.preparation_blocks('q',mock,lay));assert len(inverse)==len(forward)
 for a,b in zip(inverse,stream):assert a==b
 # zip would have consumed one extra if a single iterable were shorter; here
 # both have equal fixed length, and next stage is the shared reflection.
 assert next(stream)==R
 for a,b in zip(forward,stream):assert a==b
 try:next(stream)
 except StopIteration:pass
 else:raise AssertionError('extra frame block')
 sampled[label]=len(forward)
assert sha(pp)==plan_hash
out={'status':'PASS_A18_SEVEN_CAR_FRAME_INVENTORIES_AND_ORDER','plan_sha256':sha(pp),'library_sha256':sha(P/'MATERIAL_PREPARATION_LIBRARY.json'),'banks':banks,'all_112_copy_resource_inventory_matches':True,'sampled_actual_q_K11_K13_blocks_each_direction':sampled,'same_reflection_used_twice':True,'predicate_zeros_required_and_not_prepared_here':3,'112_copy_error_lt':'2^-4084','A17_plus_conservative_CAR_coefficient':combined,'combined_known_error_lt':'2^-4058 conditional on compatible inputs, excluding missing graph pieces','unexpanded_full_program_executed':False,'GR_closed':False}
Path(__file__).with_name('A18_CAR_FRAME_INVENTORY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
