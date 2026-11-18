#!/usr/bin/env python3
"""Exact algebraic no-false-positive test of actual native READY words."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');source=D/'round17/report_assembly.py';digest=sha256(source.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('b36_a17_ready',source);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
# Q[a], a=sqrt(p), p²+p=1, so a^4=1-a². Integer tuples use basis 1,a,a²,a³.
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(i+j for i,j in zip(x,y))
def mul_a(x):return (x[3],x[0],x[1]-x[3],x[2])
def mul_p(x):return (x[2],x[3],x[0]-x[2],x[1]-x[3])
def neg(x):return tuple(-v for v in x)
def run(word,initial):
 v={initial:one}
 for op,*w in word:
  out={}
  if op=='G':
   mask=1<<w[0]
   for x,z in v.items():
    bit=bool(x&mask);base=x&~mask
    c0=neg(mul_p(z)) if bit else mul_a(z);c1=mul_a(z) if bit else mul_p(z)
    out[base]=add(out.get(base,zero),c0);j=base|mask;out[j]=add(out.get(j,zero),c1)
  elif op=='CX':
   for x,z in v.items():
    y=x^(((x>>w[0])&1)<<w[1]);out[y]=add(out.get(y,zero),z)
  else:
   assert op=='SourceI'
   for x,z in v.items():
    bit=(x>>w[0])&1;spin=((x>>w[1])^(x>>w[2]))&1;y=x^(bit<<w[2]);c=neg(z) if bit and spin else z;out[y]=add(out.get(y,zero),c)
  v={i:z for i,z in out.items() if z!=zero}
 return v
casecounts={};gatecounts={}
for K in (3,4):
 andstart=K;outwire=2*K-2;port=outwire+1;spin=[port+1,port+2];aux=port+3
 plan={'fair_bank_count':0,'READY_total_flags':K,'selector_and_post_READY_wires':list(range(K)),
       'READY_AND_work_range':[andstart,K-2],'all_READY_wire':outwire,'native_port':port,'native_spin':spin,'native_aux_arbitrary':aux}
 trees=list(a.ready_native_blocks(plan,1));assert len(trees)==2*K-3
 for tree in trees:
  for leaf in a.s.nb.leaves(tree):
   if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in range(K)
   elif leaf['op']=='SourceI':assert not set(leaf['wires']).intersection(range(K))
 # Last K-2 blocks are actual literal adjoints, not repeated approximations.
 for i in range(K-2):
  fwd=trees[i];back=trees[-1-i];assert back==a.s.nb.inverse_literal(fwd,port,tuple(spin))
 word=[]
 for tree in trees:
  for g in a.s.nb.expand(tree,20000):word.append((g['op'],*g['wires']))
 gatecounts[str(K)]=len(word);count=0
 flags=range(2**K-1) if K==3 else [((1<<K)-1)^(1<<bit) for bit in range(K)]
 for flag,external in product(flags,range(16)):
  # AND work and allready are clean; port/spin/aux arbitrary basis inputs.
  initial=flag|(external<<port); result=run(word,initial)
  assert result=={initial:one},(K,flag,external,result);count+=1
 casecounts[str(K)]=count
# Hostile uncompute: falsely repeat approximate CCX instead of its literal
# inverse. With flags 110 in chronological order (binary 011), the last
# flag is 0, so the core is identity, but the remaining forward² is not I.
K=3;plan={'fair_bank_count':0,'READY_total_flags':3,'selector_and_post_READY_wires':[0,1,2],'READY_AND_work_range':[3,1],'all_READY_wire':4,'native_port':5,'native_spin':[6,7],'native_aux_arbitrary':8}
fwd=a.lower_gate(plan,1,a.and_compute_gate(plan,0));core=a.lower_gate(plan,1,a.and_core_gate(plan));bad=[]
for tree in (fwd,core,fwd):
 for g in a.s.nb.expand(tree,20000):bad.append((g['op'],*g['wires']))
assert run(bad,3)!={3:one}
assert sha256(source.read_bytes()).hexdigest()==digest
out={'status':'PASS_EXACT_SMALL_NATIVE_READY_NO_FALSE_POSITIVE','source_sha256':digest,'exact_coefficient_ring':'Z[a], a=sqrt(p), a^4+a²−1=0','SourceI_spin_representation':'exact native L_i = diag(J,-J), both spin bits included','actual_native_primitive_counts_by_flag_count':gatecounts,'all_failed_patterns_K3_arbitrary_port_spin_aux_columns':casecounts['3'],'each_failed_position_K4_arbitrary_port_spin_aux_columns':casecounts['4'],'ready_flags_untargeted_by_every_small_native_primitive':True,'literal_native_inverse_blocks_structurally_checked':True,'repeating_approximate_forward_leaves_failure_garbage':True,'proof_for_arbitrary_K':'first zero flag gives an exactly-zero fresh AND target via A14 first-or-second-control-zero identity; every later prefix target and final output stay zero; literal compute inverse exactly restores arbitrary entangled external state','limitations':'clean AND work and allready required; does not prove flags describe correct upstream states or scalar all-ready amplitude','GR_closed':False}
Path(__file__).with_name('EXACT_NATIVE_READY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
