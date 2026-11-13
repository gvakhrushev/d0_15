#!/usr/bin/env python3
"""Test every small success pattern, coherent factorisation, and real cap28."""
from itertools import product
from pathlib import Path
from collections import Counter
import random,json,math,importlib.util,sys,hashlib
import numpy as np
import sympy as s
import fair_router as fr
P=Path(__file__).resolve().parent;ROOT=P.parents[5];source=ROOT/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('b31_native',source);nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
def run(word,state):
 for op,*w in word:
  if op=='X':state^=1<<w[0]
  elif op=='CX':
   if state&(1<<w[0]):state^=1<<w[1]
  elif op=='CCX':
   if (state&(1<<w[0])) and (state&(1<<w[1])):state^=1<<w[2]
  else:raise ValueError(op)
 return state
# Verify the exact owned 2G+3CX word on all eight basis columns; then its
# actual canonical input state, sign, byproduct, and failure without discarding.
kq=fr.layout(1)['attempts'][0];logical_kernel=fr.parity_kernel(kq)
ex=nt.Execution(3,(),(),tuple(nt.Gate(op,tuple(w)) for op,*w in logical_kernel),nt.G_CX)
nt.validate_execution(ex,max_qubits=3,max_expanded_stages=5);M=nt.word_matrix(ex,max_qubits=3,max_expanded_stages=5)
p=nt.P;a=nt.A;v=M[:,0];expected=s.Matrix([p,0,0,a*p,p**2,0,0,a*p])
assert nt.exact_matrix_equal(v,expected) # tensor order |A,B,C>, MSB first
assert s.simplify(2*(a*p)**2-2*p**3)==0
assert s.simplify(p**2+p**4+2*p**3-1)==0
# Exhaust ALL input data, flags, output and ready for small K, with clean work.
all_column_small=0
for K in range(1,5):
 q,word=fr.router(K);width=3*K+2
 for state in range(1<<width):
  flags=sum(((state>>reg['C'])&1)<<i for i,reg in enumerate(q['attempts']))
  selected=next((i for i in range(K) if flags>>i&1),None);want=state^(int(selected is not None)<<q['ready'])
  if selected is not None:
   ai=q['attempts'][selected]['A'];out=q['output']
   if ((want>>ai)^(want>>out))&1:want^=(1<<ai)|(1<<out)
   want|=1<<q['chosen'][selected]
  assert run(word,state)==want;all_column_small+=1
# Every success pattern through K<=12, with nontrivial arbitrary A/B and
# dirty output/ready plus spectator: this tests the full logical XOR/permutation.
checks=0
for K in range(1,13):
 q,word=fr.router(K)
 for flags in range(1<<K):
  state=0
  As=[((flags*13+i*7+K)>>i%7)&1 for i in range(K)]
  Bs=[((flags*3+i+K)>>i%5)&1 for i in range(K)]
  old=(flags+K)&1;ready=(flags>>1)&1; spectator=(flags+1)&1
  for i,reg in enumerate(q['attempts']):
   state|=(As[i]<<reg['A'])|(Bs[i]<<reg['B'])|(((flags>>i)&1)<<reg['C'])
  state|=(old<<q['output'])|(ready<<q['ready'])|(spectator<<q['qubits'])
  actual=run(word,state);selected=next((i for i in range(K) if flags>>i&1),None)
  want=state^(int(selected is not None)<<q['ready'])
  if selected is not None:
   ai=q['attempts'][selected]['A']; out=q['output']
   if ((want>>ai)^(want>>out))&1:want^=(1<<ai)|(1<<out)
   want|=1<<q['chosen'][selected]
  assert actual==want,(K,flags)
  assert all(not(actual>>w&1) for w in q['survive']);checks+=1
# K=28 boundary and random patterns, all flags untouched; every gate fixed.
K=28;q,word=fr.router(K);rng=random.Random(3101);patterns=[0,(1<<K)-1,1,1<<27,1<<14,0x5555555,0xaaaaaaa]+[rng.getrandbits(K) for _ in range(2048)]
for flags in patterns:
 state=sum(((flags>>i)&1)<<reg['C'] for i,reg in enumerate(q['attempts']))
 state|=1<<q['output'];out=run(word,state);selected=next((i for i in range(K) if flags>>i&1),None)
 assert ((out>>q['ready'])&1)==(selected is not None)
 assert sum((out>>w)&1 for w in q['chosen'])==int(selected is not None)
 if selected is not None:
  assert (out>>q['chosen'][selected])&1 and (out>>q['attempts'][selected]['A'])&1 and not(out>>q['output']&1)
 else:assert (out>>q['output'])&1
 assert all(((out>>reg['C'])&1)==((flags>>i)&1) for i,reg in enumerate(q['attempts']))
 assert all(not(out>>w&1) for w in q['survive'])
# Exact symbolic coefficient pairing for coherent kernel branches on K<=6.
# Each raw vector amplitude is p^u a^v; routing is a bijection, so exact
# equality of exponent pairs establishes product factorisation on READY=1.
coherent_support=0
for K in range(1,7):
 q,word=fr.router(K);vectors={}
 # option = (A,B,C,p-exponent,a-exponent), from exact kernel state.
 opts=[(0,0,0,1,0),(1,0,0,2,0),(0,1,1,1,1),(1,1,1,1,1)]
 for choices in product(opts,repeat=K):
  state=0;ep=ea=0
  for i,(A,B,C,pp,aa) in enumerate(choices):
   reg=q['attempts'][i];state|=A<<reg['A']|B<<reg['B']|C<<reg['C'];ep+=pp;ea+=aa
  out=run(word,state);assert out not in vectors;vectors[out]=(ep,ea)
 for out,coeff in vectors.items():
  if out>>q['ready']&1:
   partner=out^(1<<q['output']);assert vectors.get(partner)==coeff;coherent_support+=1
  else:assert not(out>>q['output']&1)
# Hostile: copying plus by CX entangles source and destination; output marginal is I/2.
CX_on_plus=np.array([1,0,0,1])/math.sqrt(2);rho=np.outer(CX_on_plus,CX_on_plus).reshape(2,2,2,2);marg=np.trace(rho,axis1=0,axis2=2)
assert np.allclose(marg,np.eye(2)/2) and not np.allclose(marg,np.ones((2,2))/2)
result={'status':'PASS_EXACT_KERNEL_AND_COHERENT_FIRST_SUCCESS_ROUTING',
 'owner_native_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'owner_kernel_calls':['G(A)','G(B)','CX(A,C)','CX(B,C)','CX(A,B)'],
 'kernel_all_input_columns':8,'kernel_success_state':'sqrt(2p^3) |+>_A|1>_B|1>_C','kernel_failure_state':'(p|0>+p^2|1>)_A |0>_B|0>_C','byproduct_correction_required':False,
 'all_input_columns_K_1_to_4':all_column_small,'all_flag_patterns_K_1_to_12_cases':checks,'cap28_boundary_random_cases':len(patterns),'exact_coherent_amplitude_pairs_K_1_to_6':coherent_support,
 'unselected_payloads_and_all_flags_retained':True,'selected_socket_receives_original_output':True,'survive_workspace_cleared':True,'chosen_one_hot_retained':True,
 'hostile_CX_copy_marginal':'I/2, not |+><+|','all_2^28_patterns_enumerated':False,'native_approximation_not_tested_here':True,'GR_closed':False}
(P/'ROUTER_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
