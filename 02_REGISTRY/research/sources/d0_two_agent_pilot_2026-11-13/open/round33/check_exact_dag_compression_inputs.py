#!/usr/bin/env python3
"""Independently check algebraic data for actual source compression (not SELECT)."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
load=lambda rel:json.loads((D/rel).read_text())
files=['round11/SOURCE_TENSOR_DAG.json','round11/PERIODIC_SOURCE_BINDING.json','round12/INTERNAL_SELECTOR_PALETTE.json','round12/TOP_SOURCE_SELECTOR_PALETTE.json','round15/SOURCE_DISPATCH_TABLES.json']
dag,binding,internal,top,dispatch=map(load,files); nodes=dag['nodes']
Z=(F(0),F(0));O=(F(1),F(0));P=(F(0),F(1))
def q(a,b=0):return F(a),F(b)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def sub(a,b):return add(a,neg(b))
def mul(a,b):return a[0]*b[0]+a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1]
def div(a,b):
 n=b[0]*b[0]-b[0]*b[1]-b[1]*b[1];assert n
 return mul(a,((b[0]-b[1])/n,-b[1]/n))
def sign(a):
 u=2*a[0]-a[1];v=a[1]
 if not v:return (u>0)-(u<0)
 if not u:return (v>0)-(v<0)
 if (u>0)==(v>0):return (u>0)-(u<0)
 return ((u>0)-(u<0)) if u*u>5*v*v else ((v>0)-(v<0))
def power(a,n):
 b=O
 for _ in range(n):b=mul(b,a)
 return b
def decode(pair):return q(*pair)
reachable=set();todo=list(dag['roots'].values())
while todo:
 i=todo.pop()
 if i not in reachable:reachable.add(i);todo.extend(nodes[i].get('args',[]))
masses=[];degrees=[];checked_add=0
for i,n in enumerate(nodes):
 typ=n['op'];args=n.get('args',[])
 if typ=='const':
  c=q(n['a'],n['b']);m=neg(c) if sign(c)<0 else c;deg=(0,0)
 elif typ=='var':
  m=q({'choi_coframe':16*binding['A_active'],'choi_link':32*binding['A_active'],'matter_X':1}[n['kind']]);deg=(0,1) if n['kind']=='matter_X' else (1,0)
 elif typ=='add':
  m=Z
  for j in args:m=add(m,masses[j])
  deg=tuple(max(degrees[j][k] for j in args) for k in (0,1))
 elif typ=='mul':
  m=O
  for j in args:m=mul(m,masses[j])
  deg=tuple(sum(degrees[j][k] for j in args) for k in (0,1))
 else:raise AssertionError(typ)
 assert tuple(n['degree'])==deg
 masses.append(m);degrees.append(deg)
 if i in reachable:
  assert sign(m)>0
  if typ=='add':
   pal=internal['partitions'][internal['node_to_palette'][str(i)]]
   assert [decode(w) for w in pal['weights']]==[div(masses[j],m) for j in args]
   checked_add+=1
assert checked_add==len(internal['node_to_palette'])
for palette in (internal,top):
 tau=F(palette['ready_probability_rational']);r=palette['fair_bits_r'];n=palette['golden_coins_n'];assert F(1,2)<tau<=1
 for part in palette['partitions']:
  weights=[decode(w) for w in part['weights']];assert sum((sign(w)<0 for w in weights))==0
  total=Z
  for w in weights:total=add(total,w)
  assert total==O and len(part['counts_ready_then_abort'])==len(weights)+1
  for w,count in zip(weights,part['counts_ready_then_abort'][:-1]):
   assert min(map(int,count))>=0 and div(mul(q(*count),power(P,n)),q(2**r))==mul(q(tau),w)
  assert div(mul(q(*part['counts_ready_then_abort'][-1]),power(P,n)),q(2**r))==q(1-tau)
for j,(site,name) in enumerate(top['palette_keys']):
 assert j==2*site+list(dag['roots']).index(name)
 root=dag['roots'][name];rhoinv=F(binding['site_bindings'][site]['inverse_PF_once']);w=div(mul(masses[root],q(rhoinv)),q(2**1525))
 assert sign(w)>0 and sign(sub(O,w))>0
 expected=[w,div(sub(O,w),q(2)),div(sub(O,w),q(2))]
 assert [decode(x) for x in top['partitions'][j]['weights']]==expected
out={'status':'PASS_ACTUAL_OPERATOR_COMPRESSION_ALGEBRA_INPUTS','nodes':len(nodes),'reachable_nodes':len(reachable),'add_nodes_checked':checked_add,'internal_palettes':len(internal['partitions']),'site_kind_top_palettes':len(top['partitions']),'all_degrees_and_masses_recomputed':True,'all_actual_first_attempt_success_weights_tau_times_requested':True,'top_positive_negative_identity_weights_equal':True,'independent_site_control_is_required':True,'what_this_is':'exact coefficient and tensor-degree input verification, not an execution of A16 SELECT','input_sha256':{f:hashlib.sha256((D/f).read_bytes()).hexdigest() for f in files},'physical_C_closed':False,'GR_closed':False}
Path(__file__).with_name('ACTUAL_COMPRESSION_INPUTS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
