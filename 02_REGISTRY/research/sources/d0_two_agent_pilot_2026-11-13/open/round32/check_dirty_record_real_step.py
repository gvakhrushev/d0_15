#!/usr/bin/env python3
"""Independent full actual transition stream with dirty XOR outputs on CAR leaf."""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,hashlib
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
spec=importlib.util.spec_from_file_location('b32_dispatch',D/'round15/source_dispatcher.py');mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());binding=json.loads((D/'round11/PERIODIC_SOURCE_BINDING.json').read_text());comp=json.loads((D/'round15/SOURCE_DISPATCH_COMPILATION.json').read_text())
def put(x,wires,value):
 for i,w in enumerate(wires):
  if (value>>i)&1:x|=1<<w
  else:x&=~(1<<w)
 return x
def get(x,wires):return sum(((x>>w)&1)<<i for i,w in enumerate(wires))
def pack(vals,widths):
 out=off=0
 for v,w in zip(vals,widths):assert 0<=v<2**w;out|=v<<off;off+=w
 return out
leafi=next(i for i,l in enumerate(binding['leaf_templates']) if l['name']=='X/plus3/15');leaf=binding['leaf_templates'][leafi];site=247;internal=binding['site_bindings'][site]['leaf_addresses_in_template_order'][leafi]
node=leaf['node']+1;leafcode=leafi+1;assert leaf['kind']=='CAR' and node>0
p=mod.step_plan(4);q=p['layout'];old=[pack(x,[15,7,2]) for x in [(node,5,1),(903,12,2),(139,71,3),(82,10,0)]]
dirty_new=[0xAD43F1,0x195A0F,0xF13055,0x7AC0DE];dirty_record=(1<<65)-1;state=0
for wires,v in zip(q['old_stack'],old):state=put(state,wires,v)
for wires,v in zip(q['new_stack'],dirty_new):state=put(state,wires,v)
for name,v in [('site',site),('choice',17),('ready',1),('record',dirty_record)]:state=put(state,q[name],v)
initial=state;readonly=set(sum(q['old_stack'],[])+q['site']+q['choice']+q['ready']);counts=Counter()
for gate in mod.transition_word(p,tables):
 op,*w=gate;assert w[-1] not in readonly and len(set(w))==len(w);counts[op]+=1
 if op=='X':state^=1<<w[0]
 elif op=='CX':
  if state&(1<<w[0]):state^=1<<w[1]
 elif op=='CCX':
  mask=(1<<w[0])|(1<<w[1])
  if state&mask==mask:state^=1<<w[2]
 else:raise ValueError(op)
# leaf pops: output stack y XOR (old[1],old[2],old[3],0).
for i,wires in enumerate(q['new_stack']):assert get(state,wires)==dirty_new[i]^(old[i+1] if i<3 else 0)
a=(internal<<4)|1;b=(internal<<4)|15;assert a!=0 and b!=a
instr=pack([0,leafcode,5,1,2,a,b],[1,9,7,2,2,22,22]);assert get(state,q['record'])==dirty_record^instr
for name in ('transition','flag','pattern_work','carries'):assert get(state,q[name])==0
assert get(state,sum(q['children'],[]))==0 and all(((state^initial)>>w)&1==0 for w in readonly)
expected=Counter(comp['walks']['H_q_before_inverse_PF']['step_counts']);expected.subtract(comp['lookup_gate_counts']['palette']);assert counts==expected
out={'status':'PASS_REAL_WIDTH_CAR_DIRTY_XOR_OUTPUTS','input_sha256':{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [D/'round15/source_dispatcher.py',D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round11/PERIODIC_SOURCE_BINDING.json']},
 'SITE_index':site,'CAR_internal_site':internal,'a':a,'b':b,'leaf_name':leaf['name'],'leaf_code':leafcode,'initial_record_all_65_bits_one':True,'new_stack_outputs_dirty':True,
 'actual_transition_gate_counts':dict(counts),'logical_gates_executed':sum(counts.values()),'all_inputs_unchanged_every_gate':True,'all_scratch_restored_zero':True,
 'scope':'one actual full transition stream, clean temporaries and arbitrary XOR output; not the full walk/native SELECT','GR_closed':False}
(P/'DIRTY_REAL_STEP_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
