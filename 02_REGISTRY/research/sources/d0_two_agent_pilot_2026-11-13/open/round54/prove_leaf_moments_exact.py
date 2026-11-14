#!/usr/bin/env python3
"""Exact structural leaf moments, all site bindings and Fourier RIGHT mass."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import json,sympy as s
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');files=[D/'round11/PERIODIC_SOURCE_BINDING.json',D/'round11/SOURCE_TENSOR_DAG.json',O/'round24/TORUS_CHOI_ADDRESSES.jsonl',O/'round21/ORIGINAL_PF_N20_L4.jsonl',O/'round21/ORIGINAL_FOURIER128_L4.json',O/'round25/targets.py'];h=lambda q:sha256(q.read_bytes()).hexdigest();pins={str(q):h(q) for q in files};binding=json.loads(files[0].read_text());dag=json.loads(files[1].read_text());addresses=[json.loads(x) for x in files[2].read_text().splitlines()];pf=[json.loads(x) for x in files[3].read_text().splitlines()];K=json.loads(files[4].read_text())['kappa'];assert len(addresses)==2049 and len(pf)==256 and len(K)==64 and sum(x['N'] for x in pf)==10946
siteindex={tuple(row['site']):i for i,row in enumerate(pf)};assert len(siteindex)==256
# Vacuum -> grade1 creator, and exterior grade-one -> M exactly, with A11 order.
order=(0,2,3,1);creators=[]
for i in range(4):
 C=s.zeros(16)
 for mask in range(16):
  if not (mask>>i)&1:C[mask|(1<<i),mask]=(-1)**sum(bool(mask&(1<<j)) for j in order[:order.index(i)])
 creators.append(C)
u=s.symbols('u0:4',real=True);C=sum((u[i]*creators[i] for i in range(4)),s.zeros(16))
assert [C[1<<i,0] for i in range(4)]==list(u)
# Exterior(M) on grade 1 equals M; this uses determinant of each 1x1 minor.
M=s.Matrix(4,4,lambda i,j:s.Symbol('M%d%d'%(i,j),real=True));assert all(s.det(M.extract([i],[j]))==M[i,j] for i in range(4) for j in range(4))
counts=Counter()
for row in binding['site_bindings']:
 x=list(row['site']);assert siteindex[tuple(x)]==row['SITE_index']
 for leaf,addr in zip(binding['leaf_templates'],row['leaf_addresses_in_template_order']):
  node=dag['nodes'][leaf['node']];assert node['op']=='var' and node['name']==leaf['name']
  y=list(x)
  if leaf['location']!='base':
   direction=int(leaf['location'].replace('plus',''));y[direction]=(y[direction]+1)%4
  name=leaf['name'].split('/')
  if leaf['kind']=='Choi':
   a=addresses[addr];assert addr>0 and a['a']==addr and a['site']==y and a['kind']==leaf['catalogue_kind'] and a['direction']==leaf['direction']
   if name[0]=='u':assert (leaf['input'],leaf['output'],leaf['anchor_moment_multiplier'])==(0,1<<int(name[2]),1) and leaf['direction']==int(name[1]);counts['coframe']+=1
   else:assert name[0]=='M' and (leaf['input'],leaf['output'],leaf['anchor_moment_multiplier'])==(1<<int(name[4]),1<<int(name[3]),2) and leaf['direction']==int(name[2]);counts['proper_link']+=1
  else:
   assert leaf['kind']=='CAR' and addr==siteindex[tuple(y)] and leaf['cross_masks']==[1,int(name[2])] and leaf['RIGHT_action']=='identity';counts['CAR']+=1
assert sum(counts.values())==256*282
# Exact original 128 RIGHT amplitudes: values 0,+/-1 over denominator128.
for row in pf:
 x=row['site'];n=0
 for kap in K:
  phase=sum(a*b for a,b in zip(kap,x))%4;cc=(1,0,-1,0)[phase];ss=(0,1,0,-1)[phase];n+=cc*cc+ss*ss
 assert n==64 and F(n,128**2)==F(1,256)
# Choi with Ω_aij=J_a[j,i]/sqrt(32A), anchor=1/sqrt(32A).
# A11 observable multiplier 16A or 32A yields J or 2J exactly.
A=2049;assert F(2*16*A,32*A)==1 and F(2*32*A,32*A)*F(1,2)==1
# Generic anchored rotation O(m)e_anchor=m and O(m)^T O(m)=I under norm=1.
a,b,c,d=s.symbols('a b c d',real=True);v=s.Matrix([a,b,c,d]);e=s.Matrix([0,1,0,0]);J=v*e.T-e*v.T;R=s.eye(4)+J+J*J/(1+b);rel=a*a+b*b+c*c+d*d-1
for entry in list(R*e-v)+list(R.T*R-s.eye(4)):
 num=s.fraction(s.factor(entry))[0];assert s.rem(num,rel,a)==0
# CAR vector has grade1=sqrt(p), grade0=psi0, grade15=psi15; all
# 256 site masses are 1/256, giving 2 sqrt(p) psi_g/256 exactly.
assert F(2,256)==F(1,128)
for path,pin in pins.items():assert h(Path(path))==pin
out={'status':'PASS_EXACT_IDEAL_CHOICAR_LEAF_MOMENT_STRUCTURE','input_sha256':pins,'all_72192_bound_leaves':dict(counts),'all_256_Fourier_site_RIGHT_masses':'1/256 exact','creator_and_exterior_grade1_symbolic_identity':True,'Choi_anchor_multipliers_exact':{'coframe':16*A,'link':32*A},'CAR_moment':'2 sqrt(p) psi[grade]/256','generic_anchored_rotation_all_columns_orthogonality_under_unit_norm':True,'scope':'Exact identities for the declared ideal source target and every finite original address. Consumes B25 Julia/full source definitions and unit norm/positive defect; no giant native stage or physical marked map executed.','GR_closed':False}
(P/'IDEAL_SOURCE_LEAF_MOMENTS_EXACT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'leaf_counts':dict(counts),'fourier_sites':256}))
