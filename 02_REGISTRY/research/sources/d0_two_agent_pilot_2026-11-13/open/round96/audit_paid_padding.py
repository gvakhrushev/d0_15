#!/usr/bin/env python3
"""One-pass paid padding: all lengths and all eight borrowed CODE columns."""
from pathlib import Path
from collections import Counter
import sys,json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round49');sys.path.insert(0,str(D))
import paid_padding as p
N=p.native

def simulate_cx(t,v):
 op=t['op']
 if op=='seq':
  for x in t['children']:v=simulate_cx(x,v)
  return v
 if op=='repeat':
  for _ in range(int(t['count'],16) if t['count'].startswith('0x') else int(t['count'])):v=simulate_cx(t['child'],v)
  return v
 assert op=='CX';c,q=t['wires'];return v^(((v>>c)&1)<<q)
for length in range(4,42):
 blocks=list(p.counted_pad(lambda:iter(()),length,[0,1,2]));assert sum(p.count(lambda:iter(blocks)).values())==length
 for v in range(8):
  out=v
  for tree in blocks:out=simulate_cx(tree,out)
  assert out==v
calls=0
def source():
 global calls
 calls+=1
 yield {'op':'repeat','count':'0x3','child':{'op':'G','wires':[3]}}
 yield {'op':'cut','name':'source_frontier'}
 yield {'op':'seq','children':[{'op':'CX','wires':[0,3]},{'op':'G','wires':[3]}]}
blocks=list(p.counted_pad(source,13,[0,1,2],tag_ops=('cut',)));assert calls==1
assert blocks.index({'op':'cut','name':'source_frontier'})==1
assert sum(p.count(lambda:iter(blocks),tag_ops=('cut',)).values())==13
try:list(p.counted_pad(source,8,[0,1,2],tag_ops=('cut',)));raise AssertionError('overrun accepted')
except AssertionError as ex:assert 'upper bound failed' in str(ex)
out={'status':'PASS_ONE_PASS_PAID_PADDING_FIXTURES','identity_lengths_checked':[4,41],'all_eight_CODE_columns':True,'tag_position_preserved':True,'one_pass_factory_calls':1,'DAG_repeat_calls_counted':True,'overrun_rejected':True,'production_word_executed':False,'GR_closed':False}
(P/'PAID_PADDING_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
