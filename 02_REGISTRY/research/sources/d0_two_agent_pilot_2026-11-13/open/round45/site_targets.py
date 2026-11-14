#!/usr/bin/env python3
"""Exact B25 SITE half-vector tree targets, with source-formula dedup only."""
from pathlib import Path
from math import gcd
import importlib.util,sys,json
P=Path(__file__).resolve().parent;B=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
spec=importlib.util.spec_from_file_location('b45_dyadic',D/'round18/material_targets.py');old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old);Dyadic=old.Dyadic
PF=B/'round21/ORIGINAL_PF_N20_L4.jsonl'
def source():
 rows=[json.loads(x) for x in PF.read_text().splitlines()];assert len(rows)==256
 for i,r in enumerate(rows):
  x=r['site'];assert len(x)==4 and all(0<=v<4 for v in x) and i==64*x[0]+16*x[1]+4*x[2]+x[3] and r['N']>0
 N=sum(r['N'] for r in rows);assert N==10946
 return [r['N'] for r in rows]
def tree_names():
 counts=source();N=sum(counts);nodes=[];angles={}
 for level in range(8):
  width=1<<(8-level);half=width//2
  for prefix in range(1<<level):
   start=prefix*width;left=sum(counts[start:start+half]);right=sum(counts[start+half:start+width]);anchor=start==0
   if anchor:spec={'type':'anchor','left_nonanchor':left-counts[0],'right_sum':right}
   else:
    d=gcd(left,right);spec={'type':'rational','left':left//d,'right':right//d}
   name=('a_'+str(spec['left_nonanchor'])+'_'+str(right)) if anchor else ('r_'+str(spec['left'])+'_'+str(spec['right']))
   assert name not in angles or angles[name]==spec;angles[name]=spec
   nodes.append({'level':level,'prefix':prefix,'target_bit':7-level,'control_bits':list(range(7,7-level,-1)),'pattern':[(prefix>>(level-1-j))&1 for j in range(level)],'angle_id':name})
 assert len(nodes)==255
 return counts,angles,nodes
def targets(iv,sp,counts):
 R=iv.rational;N=sum(counts);S=iv.scale
 if sp['type']=='anchor':
  c=iv.sqrt(R(counts[0],N));extra=iv.add(R(N+counts[0]+sp['left_nonanchor']),iv.mul(R(2*N),c));left=extra;right=R(sp['right_sum'])
 else:left=R(sp['left']);right=R(sp['right'])
 total=iv.add(left,right);assert left[0]>0 and right[0]>0
 return iv.sqrt(iv.div(left,total)),iv.sqrt(iv.div(right,total))
