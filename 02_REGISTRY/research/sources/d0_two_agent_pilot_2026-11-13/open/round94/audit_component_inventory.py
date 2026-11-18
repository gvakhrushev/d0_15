#!/usr/bin/env python3
"""Independent recurrence census of component SOURCE inventory receipts."""
from pathlib import Path
from collections import Counter
import json,sys
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48');sys.path.insert(0,str(A))
import two_bit_source_native as s
plan=json.loads((A/'TWO_BIT_SOURCE_COMPONENT_PLAN.json').read_text());x=s.inputs();ch=s.choi_layout();ca=s.car_layout()
def add(a,b):
 c=Counter(a);c.update(b);return c
def mul(a,n):return Counter({k:v*n for k,v in a.items()})
def inv(c):return Counter(G_port=c['G_port']+c['G_other'],G_other=0,CX=c['CX']+6*c['G_other'],SourceI=3*c['SourceI']+4*(c['G_port']+c['G_other']))
def price(node,port):
 op=node['op']
 if op=='seq':
  c=Counter()
  for x in node['children']:c.update(price(x,port))
  return c
 if op=='repeat':return mul(price(node['child'],port),int(node['count']))
 return Counter({('G_port' if node['wires'][0]==port else 'G_other') if op=='G' else op:1})
def dec(row,base=10):return Counter({k:int(v,base) for k,v in row.items()})
def eq(c,row):return all(c[k]==int(row.get(k,'0')) for k in ('G_port','G_other','CX','SourceI'))
pre=Counter()
for tree in s.old.prefix.prefix_blocks(x['prefix'],ch,True):pre.update(price(tree,ch['port']))
h=int(x['h_k']);phase=int(x['phase']['phase_k']);correct=int(x['level9']['correction_l']);N=23
X=Counter(G_other=4*h,CX=6,SourceI=2);CCX=Counter(G_port=6*h,G_other=6*h,CX=68,SourceI=24);H=Counter(G_other=2*h,CX=6,SourceI=2)
F=mul(X,2)+Counter(CX=2*N-1)+mul(CCX,2*N-3)
start=F+Counter(G_port=phase,G_other=phase,CX=8,SourceI=4)+inv(F);good=Counter(G_other=2*phase,CX=2)
reflection=Counter(G_other=(1<<46)*int(x['fixed']['joint_reflection_pi']['k']),CX=1<<46)
raw=lambda n:Counter(G_port=n,CX=6*n,SourceI=4*n)
choi={};car={}
for bank in s.BANKS:
 cv=pre+dec(x['local_plan']['coframe'][bank]['native_forward'])+dec(x['proper_upper']['bank_bounds'][bank]['forward_componentwise_upper_hex'],16)
 half=mul(H,2)+cv
 for _ in range(9):half=mul(half,2)+inv(half)+good+start
 half.update(G_other=correct);full=raw(46)+mul(reflection,2)+half+inv(half)
 row=plan['Choi_componentwise_resource_upper'][bank]
 for label,c in [('Omega_forward_upper',cv),('half_forward_upper',half),('source_forward_upper',full),('source_literal_inverse_upper',inv(full))]:assert eq(c,row[label]),(bank,label)
 choi[bank]=full
# Independently count vacuum native DAG and every Walsh Fourier command.
vac=Counter()
for stage in ('RAW','H','VAC'):
 for tree in s.vac.fixed_blocks(stage,ca,h):vac.update(price(tree,ca['port']))
for cmd in s.vac.commands(s.vac.inputs()['kappa'],ca,int(x['fixed']['fourier_pi_over_2']['k'])):
 K=cmd['K'];N0=1<<K;assert any(cmd['pattern']);neg=N0//2
 vac.update(G_port=neg*cmd['k'],G_other=neg*cmd['k'],CX=K*N0+6*neg,SourceI=4*neg)
for bank in s.BANKS:
 full=raw(3)+vac+dec(x['local_plan']['material']['frames'][bank]['native_forward']);row=plan['CAR_exact_resource_counts'][bank]
 for label,c in [('vacuum_prefix_forward',vac),('source_forward',full),('source_literal_inverse',inv(full))]:assert eq(c,row[label]),(bank,label)
 car[bank]=full
# Catalogue source counts: seven old banks plus independent current f/q.
total=s.site.inventory(x['site'])['SITE_forward']
for bank in s.BANKS:total.update(mul(choi[bank],180));total.update(mul(car[bank],16))
total.update(mul(choi['f'],180));total.update(mul(car['q'],16))
assert eq(total,plan['all_SOURCE_forward_componentwise_upper']) and eq(inv(total),plan['all_SOURCE_literal_inverse_componentwise_upper'])
out={'status':'PASS_ALL_CHOI_UPPER_AND_CAR_EXACT_COMPONENT_INVENTORIES','banks':7,'coframe_and_material_counts_reference':'B94 independently verified LOCAL_INVENTORY_CHECK','proper_link_counts_reference':'B93 componentwise upper, not actual','level9_recurrence_independent':True,'all_source_copy_multiplicities_checked':True,'full_exact_proper_link_inventory_evaluated':False,'GR_closed':False}
(P/'COMPONENT_INVENTORY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
