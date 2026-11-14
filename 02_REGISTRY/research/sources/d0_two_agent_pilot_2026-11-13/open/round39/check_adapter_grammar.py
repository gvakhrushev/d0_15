#!/usr/bin/env python3
"""Small native instance: recursion, nested literal inverses and inventories."""
from pathlib import Path
from collections import Counter
import json,random
import adapter_native as a
# Reduced toy: actual owned macros and the very same recursion logic.
lay={'branch':0,'rebit':1,'data':[2],'V_private':[],'external':[],'start_controls':[0,2],
     'predicate_flag':3,'predicate_work':[],'port':4,'spin':[5,6],'aux_arbitrary':7,'oldRIGHT_witness':8,'qubits':9}
cv=a.nb.gate('CX',0,2);assert a.validate_loader(lay,cv)
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def ma(x):return x[3],x[0],x[1]-x[3],x[2]
def mp(x):return x[2],x[3],x[0]-x[2],x[1]-x[3]
def run(word,state):
 for op,*w in word:
  out={}
  if op=='G':
   for x,z in state.items():
    bit=(x>>w[0])&1;base=x&~(1<<w[0]);c0=neg(mp(z)) if bit else ma(z);c1=ma(z) if bit else mp(z)
    out[base]=add(out.get(base,zero),c0);q=base|(1<<w[0]);out[q]=add(out.get(q,zero),c1)
  elif op=='CX':
   for x,z in state.items():q=x^(((x>>w[0])&1)<<w[1]);out[q]=add(out.get(q,zero),z)
  else:
   assert op=='SourceI' and w==[4,5,6]
   for x,z in state.items():
    bit=(x>>4)&1;parity=((x>>5)^(x>>6))&1;q=x^(bit<<6);v=neg(z) if bit and parity else z;out[q]=add(out.get(q,zero),v)
  state={x:z for x,z in out.items() if z!=zero}
 return state
rng=random.Random(3901);reports=[]
for level in (0,1,2):
 forward=list(a.adapter_blocks(lay,cv,1,1,1,levels=level));back=list(a.adapter_blocks(lay,cv,1,1,1,levels=level,reverse=True));F=a.nb.seq(*forward);B=a.nb.seq(*back)
 # Actual flattened reverse must match literal raw inverse of the complete
 # forward word, even when a recursion contains an inverse-of-inverse.
 want=a.nb.inverse_literal(F,lay['port'],tuple(lay['spin']))
 def expand(t):return [(x['op'],*x['wires']) for x in a.nb.expand(t,10000000)]
 fw=expand(F);bw=expand(B);assert bw==expand(want)
 cases=list(range(512)) if level==0 else [rng.randrange(512) for _ in range(16 if level==1 else 4)]
 for col in cases:assert run(bw,run(fw,{col:one}))=={col:one},(level,col)
 reports.append({'levels':level,'forward_native_blocks':len(forward),'forward_primitive_calls':len(fw),'literal_inverse_primitive_calls':len(bw),'exact_true_spin_inverse_cases':len(cases)})
# Independently compare recurrence to actual emitter counts for full 22-data
# layout on first two levels, retaining actual inverse-of-inverse prices.
full=a.layout(w=0,external_count=3);cv=a.nb.gate('CX',full['branch'],full['data'][0]);assert a.validate_loader(full,cv,sam_controls=full['external'])
for level in (0,1,2):
 blocks=a.adapter_blocks(full,cv,1,1,1,levels=level);got=Counter()
 for x in blocks:got.update(a.native_counts(x,full['port']))
 expected,reverse=a.native_budget(0,1,1,1,{'CX':1},levels=level)
 assert +got==+expected,(level,got,expected)
 inv=Counter()
 for x in a.adapter_blocks(full,cv,1,1,1,levels=level,reverse=True):inv.update(a.native_counts(x,full['port']))
 assert +inv==+reverse,(level,inv,reverse)
# Deliberately forbidden phase rebit or flag use is detected before binding.
for wire in (full['rebit'],full['predicate_flag'],full['oldRIGHT_witness'],full['external'][0]):
 try:a.validate_loader(full,a.nb.gate('CX',full['data'][0],wire),sam_controls=full['external'])
 except AssertionError:pass
 else:raise AssertionError(('forbidden loader target accepted',wire))
out={'status':'PASS_NATIVE_ADAPTER_RECURSION_LITERAL_INVERSES_AND_COUNTS','toy_levels':reports,'full_22_data_layout_levels_resource_checked':[0,1,2],'actual_reverse_primitive_sequences_equal_literal_inverse':True,'loader_forbidden_phase_scratch_oldRIGHT_SAM_targets_rejected':True,'literal_inverse_of_inverse_not_simplified':True,'source_loader_is_toy_not_actual_Omega':True,'full_eight_level_giant_word_executed':False,'GR_closed':False}
Path(__file__).with_name('ADAPTER_GRAMMAR_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
