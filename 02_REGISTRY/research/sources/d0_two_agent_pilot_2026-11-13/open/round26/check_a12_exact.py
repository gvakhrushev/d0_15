#!/usr/bin/env python3
"""Independent exact-fraction review of A12 palettes, copy slots, and caps.
Reads only A11/A12. Writes B26 evidence. No native circuit is inferred.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
from collections import Counter
import json,hashlib
import numpy as np
P=Path(__file__).resolve().parent
ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
A11=ROOT/'round11';A12=ROOT/'round12'
load=lambda p:json.loads(p.read_text());dag=load(A11/'SOURCE_TENSOR_DAG.json');binding=load(A11/'PERIODIC_SOURCE_BINDING.json');summary=load(A12/'SELECTOR_COMPILATION.json')
names=['INTERNAL_SELECTOR_PALETTE.json','TOP_SOURCE_SELECTOR_PALETTE.json','TEN_SIGN_REPORT_PALETTE.json'];palettes=[load(A12/n) for n in names]
# Independent ring Q[p] implemented as pairs; p²=1−p.
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def mul(x,y):return (x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
def div(x,y):
 norm=y[0]*y[0]-y[0]*y[1]-y[1]*y[1];assert norm
 return mul(x,((y[0]-y[1])/norm,-y[1]/norm))
def scale(x,q):return (x[0]*q,x[1]*q)
def sign(x):
 a,b=x[0]*2-x[1],x[1]
 if b==0:return (a>0)-(a<0)
 if a==0:return (b>0)-(b<0)
 if (a>0)==(b>0):return (a>0)-(a<0)
 return ((a>0)-(a<0)) if a*a>5*b*b else ((b>0)-(b<0))
def powr(x,n):
 z=(F(1),F(0))
 for _ in range(n):z=mul(z,x)
 return z
def decode(x):return (F(x[0]),F(x[1]))
zero=(F(0),F(0));one=(F(1),F(0));p=(F(0),F(1))
def fold_sum(xs):
 z=zero
 for x in xs:z=add(z,x)
 return z

def fib(n):
 a,b=0,1
 for _ in range(n):a,b=b,a+b
 return a

palette_summaries=[]
for name,pal,expected_n,expected_r,nparts in zip(names,palettes,(0,1,6),(1374,1580,94),(25,512,2048)):
 assert len(pal['partitions'])==nparts and (pal['golden_coins_n'],pal['fair_bits_r'])==(expected_n,expected_r)
 n=pal['golden_coins_n'];r=pal['fair_bits_r'];D=int(pal['common_D_integer']);tau=F(D,2**r); assert F(pal['ready_probability_rational'])==tau and 0<tau<=1
 capacities=[2**r*fib(n+1),2**r*fib(n)];assert list(map(int,pal['capacity_by_prefix_kind']))==capacities
 pp=powr(p,n)
 for part in pal['partitions']:
  weights=[decode(x) for x in part['weights']];cnt=[[int(x),int(y)] for x,y in part['counts_ready_then_abort']]
  assert len(cnt)==len(weights)+1 and fold_sum(weights)==one and all(sign(x)>=0 for x in weights)
  assert all(a>=0 and b>=0 for a,b in cnt) and [sum(v[j] for v in cnt) for j in (0,1)]==capacities
  for w,c in zip(weights,cnt[:-1]):assert scale(mul((F(c[0]),F(c[1])),pp),F(1,2**r))==scale(w,tau)
  assert scale(mul(tuple(map(F,cnt[-1])),pp),F(1,2**r))==(1-tau,F(0))
 palette_summaries.append({'file':name,'partitions':nparts,'r':r,'n':n,'D':str(D),'tau':str(tau),'all_counts_capacity_and_branch_masses_exact':True})

# Recompute every node mass and disjoint copy interval lengths with A=2049.
A=2049;mass=[];visits=[];leaves=[];degrees=[]
for i,node in enumerate(dag['nodes']):
 typ=node['op'];args=node.get('args',[]);assert all(0<=j<i for j in args)
 if typ=='const':
  q=decode((node['a'],node['b']));weight=q if sign(q)>=0 else neg(q);visit=1;leaf=0;deg=(0,0)
 elif typ=='var':
  kind=node['kind'];weight=(F({'choi_coframe':16*A,'choi_link':32*A,'matter_X':1}[kind]),F(0));visit=1;leaf=1;deg=(0,1) if kind=='matter_X' else (1,0)
 elif typ=='add':
  weight=fold_sum(mass[j] for j in args);visit=1+max(visits[j] for j in args);leaf=max(leaves[j] for j in args);deg=tuple(max(degrees[j][k] for j in args) for k in (0,1))
 elif typ=='mul':
  weight=one
  for j in args:weight=mul(weight,mass[j])
  visit=1+sum(visits[j] for j in args);leaf=sum(leaves[j] for j in args);deg=tuple(sum(degrees[j][k] for j in args) for k in (0,1))
  # Independent child copy intervals [offset,offset+degree) do not overlap.
  for q in (0,1):
   start=0
   for j in args:
    assert start+degrees[j][q]<=deg[q];start+=degrees[j][q]
   assert start==deg[q]
 else:raise AssertionError(typ)
 assert list(deg)==node['degree'];mass.append(weight);visits.append(visit);leaves.append(leaf);degrees.append(deg)
roots=dag['roots'];assert len(dag['nodes'])==20402
for name,i in roots.items():assert mass[i]==decode(summary['source_root_masses_before_inverse_PF'][name]) and visits[i]==summary['source_walk_max_node_visits'][name] and leaves[i]==summary['source_walk_max_X_leaves'][name]
rf,rq=roots['H_f_before_inverse_PF'],roots['H_q_before_inverse_PF']
assert degrees[rf]==(82,0) and degrees[rq]==(2,2)
# Reachable add choices and node-to-common-palette weights, separately verify all.
reachable=set();stack=list(roots.values())
while stack:
 i=stack.pop()
 if i in reachable:continue
 reachable.add(i);stack.extend(dag['nodes'][i].get('args',[]))
internal,top,post=palettes; count_add=0
for i in reachable:
 n=dag['nodes'][i]
 if n['op']=='add':
  count_add+=1;ix=int(internal['node_to_palette'][str(i)]);weights=[decode(x) for x in internal['partitions'][ix]['weights']]
  assert weights==[div(mass[j],mass[i]) for j in n['args']]
assert count_add==3618
# All 512 top rows use exact inverse-PF once and one common Λ.
for index,(site_id,root_name) in enumerate(top['palette_keys']):
 row=binding['site_bindings'][site_id];w=scale(mass[roots[root_name]],F(row['inverse_PF_once'])/2**1525)
 weights=[decode(x) for x in top['partitions'][index]['weights']]
 assert weights==[w,scale(sub(one,w),F(1,2)),scale(sub(one,w),F(1,2))]
 assert sign(w)>0 and sign(sub(one,w))>0
# Independently construct r(eps*s,sigma*eps*t) in polynomial ring over Q[p].
def padd(a,b):
 o=dict(a)
 for k,v in b.items():o[k]=add(o.get(k,zero),v)
 return {k:v for k,v in o.items() if v!=zero}
def pmul(a,b):
 o={}
 for (i,j),x in a.items():
  for (k,l),y in b.items():o[i+k,j+l]=add(o.get((i+k,j+l),zero),mul(x,y))
 return {k:v for k,v in o.items() if v!=zero}
def pscale(a,c):return {k:mul(v,c) for k,v in a.items() if mul(v,c)!=zero}
onep={(0,0):one};S={(1,0):one};T={(0,1):one}
psub=lambda a,b:padd(a,pscale(b,(-one[0],-one[1])))
polys={}
for sigma in (-1,1):
 E=pscale(padd(onep,pscale(S,(F(1,64),F(0)))),powr(p,2))
 U=padd(pscale(onep,p),pscale(T,scale(powr(p,2),F(sigma,64))))
 ell=pscale(pmul(E,psub(onep,E)),(F(4),F(0)))
 U2=pmul(U,U);B=pscale(pmul(U2,psub(onep,U2)),(F(4),F(0)))
 whole=padd(ell,pmul(psub(onep,ell),B));z=(F(1,2**20),F(0))
 polys[sigma]=psub(onep,pmul(psub(onep,pscale(B,z)),psub(onep,pscale(whole,z))))
 assert len(polys[sigma])==27
 for (i,j),v in polys[sigma].items():assert v==decode(summary['original_report_coefficients'][str(sigma)][f'{i},{j}'])
for idx,(sigma,mask) in enumerate(post['palette_keys']):
 signs=[1 if mask>>j&1 else -1 for j in range(10)];b=zero
 for (i,j),v in polys[sigma].items():
  vscale=1
  for s in signs[:i]+signs[2:2+j]:vscale*=s
  b=add(b,scale(v,vscale))
 weights=[decode(x) for x in post['partitions'][idx]['weights']]
 assert weights==[b,sub(one,b)] and sign(b)>0 and sign(sub(one,b))>0
# Independent concrete fresh copy offsets for all 2f+8q signs in a report.
copy_layout=[];coff=moff=0
for sign_name,deg in [('S1',(82,0)),('S2',(82,0))]+[(f'T{i}',(2,2)) for i in range(1,9)]:
 copy_layout.append({'sign':sign_name,'Choi_half_open':[coff,coff+deg[0]],'CAR_half_open':[moff,moff+deg[1]]})
 coff+=deg[0];moff+=deg[1]
assert (coff,moff)==(180,16)
assert copy_layout[0]['Choi_half_open']==[0,82] and copy_layout[-1]['Choi_half_open']==[178,180]
assert copy_layout[-1]['CAR_half_open']==[14,16]
# All-dimensional normalized rank-two decomposition: exact integer matrices.
# Vplus=T_ab, Vminus=−Z_a Z_b T_ab. Spectator complement retained.
rank2cases=0
for d in (2,3,4,7):
 for a in range(d):
  for b in range(a+1,d):
   Tm=np.eye(d,dtype=np.int64);Tm[a,a]=Tm[b,b]=0;Tm[a,b]=Tm[b,a]=1
   Z=np.eye(d,dtype=np.int64);Z[a,a]=Z[b,b]=-1;V=-Z@Tm
   X=np.zeros((d,d),dtype=np.int64);X[a,b]=X[b,a]=1
   assert np.array_equal(Tm,Tm.T) and np.array_equal(V,V.T) and np.array_equal(Tm@Tm,np.eye(d,dtype=int)) and np.array_equal(V@V,np.eye(d,dtype=int))
   assert np.array_equal(Tm+V,2*X);rank2cases+=1
# Correlating two independent δ coins changes the full Hilbert operator.
I3=np.eye(3,dtype=np.int64);X=np.zeros((3,3),dtype=np.int64);X[0,1]=X[1,0]=1
Vp=I3.copy();Vp[0,0]=Vp[1,1]=0;Vp[0,1]=Vp[1,0]=1
Z=I3.copy();Z[0,0]=Z[1,1]=-1;Vm=-Z@Vp
correlated=(np.kron(Vp,Vp)+np.kron(Vm,Vm))//2
independent=(np.kron(Vp,Vp)+np.kron(Vp,Vm)+np.kron(Vm,Vp)+np.kron(Vm,Vm))//4
assert np.array_equal(independent,np.kron(X,X)) and correlated[8,8]==1 and independent[8,8]==0
# Equal READY effects alone do not make retained environment identical.
# Isometry |0> -> |0>|0>, |1> -> |1>|1>: K^T K=I, but |+> loses
# off-diagonal after tracing the environment. This is a scope control, not
# a claim that A12 makes this substitution.
K=np.array([[1,0],[0,0],[0,0],[0,1]],dtype=np.int64)
assert np.array_equal(K.T@K,np.eye(2,dtype=np.int64))
source=np.ones((2,2),dtype=np.int64);output=K@source@K.T
reduced=np.zeros((2,2),dtype=np.int64)
for a in range(2):
 for b in range(2):reduced[a,b]=sum(output[2*a+e,2*b+e] for e in range(2))
assert np.array_equal(reduced,np.eye(2,dtype=np.int64)) and source[0,1]==1 and reduced[0,1]==0
# Fixed walk and retained capacities. No inference to unbuilt Boolean network.
Tslots=2*visits[rf]+8*visits[rq];L=2*leaves[rf]+8*leaves[rq];assert (Tslots,L)==(1054,196)
ki,kt,kf=(summary['retained_selector_caps'][x] for x in ('internal','top','fair_plus_bank'))
taui=F(internal['ready_probability_rational']);taut=F(top['ready_probability_rational'])
assert Tslots*(1-taui)**ki<=F(1,8) and 10*(1-taut)**kt<=F(1,8)
M=Tslots*ki*internal['fair_bits_r']+10*kt*top['fair_bits_r']+post['fair_bits_r']+L
G=Tslots*ki*internal['golden_coins_n']+10*kt*top['golden_coins_n']+post['golden_coins_n']
assert (M,G)==(summary['selector_fair_qubits_per_report'],summary['selector_Golden_qubits_per_report'])
assert M*F(53,100)**kf<=F(1,4) and sign(sub(sub(one,scale(powr(p,3),F(2))),(F(53,100),F(0))))<0
union=M*F(53,100)**kf+Tslots*(1-taui)**ki+10*(1-taut)**kt
assert union<=F(1,2) and union==F(summary['combined_failure_union_bound_rational'])
assert summary['full_native_READY_computed'] is False
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[A11/'SOURCE_TENSOR_DAG.json',A11/'PERIODIC_SOURCE_BINDING.json',A12/'SELECTOR_COMPILATION.json']+[A12/n for n in names]
res={'status':'PASS_INDEPENDENT_EXACT_PALETTES_DAG_COPY_CAPS_REVIEW','input_sha256':{str(f):sha(f) for f in files},'palette_checks':palette_summaries,'nodes':len(dag['nodes']),'reachable_add_types':count_add,'top_site_type_rows':512,'post_sign_mask_rows':2048,'polynomial_coefficients_independently_rebuilt':54,'disjoint_copy_degrees_f_q':[list(degrees[rf]),list(degrees[rq])],
 'fresh_copy_layout_one_report':copy_layout,'rank2_exact_real_matrix_cases':rank2cases,'reused_coin_hostile_detected':True,'equal_ready_different_environment_hostile_detected':True,'walk_slots':Tslots,'fair_leaf_choices':L,'component_caps':{'internal':ki,'top':kt,'fair_plus':kf},'component_fair_qubits':M,'component_golden_qubits':G,'union_bound_float':float(union),'failure_union_bound_le_half':True,
 'limitations':['native Boolean/routing/Toffoli/fair-gate words not checked','no complete coherent first-success machine or mark/readout compiled','full native READY alpha not determined','no C or GR closure'],'GR_closed':False}
(P/'EXACT_REVIEW.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['status','nodes','reachable_add_types','top_site_type_rows','post_sign_mask_rows','rank2_exact_real_matrix_cases','union_bound_float']}))
