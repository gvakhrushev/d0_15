#!/usr/bin/env python3
"""Independent structural/Boolean review of A13 fixed logical selectors."""
from pathlib import Path
from itertools import product
from collections import Counter
import importlib.util,sys,json,hashlib,random
P=Path(__file__).resolve().parent
ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
D=ROOT/'round13';A=ROOT/'round12'
spec=importlib.util.spec_from_file_location('a13_review_selectors',D/'reversible_selectors.py');r=importlib.util.module_from_spec(spec);sys.modules[spec.name]=r;spec.loader.exec_module(r)

def apply(word,state):
 # Independent little-endian signed-control-free X/CX/CCX execution.
 for gate in word:
  op,*w=gate
  if op=='X':state^=1<<w[0]
  elif op=='CX':
   if state&(1<<w[0]):state^=1<<w[1]
  elif op=='CCX':
   mask=(1<<w[0])|(1<<w[1])
   if state&mask==mask:state^=1<<w[2]
  else:raise ValueError(op)
 return state

def insert(state,wires,value):
 for i,wire in enumerate(wires):
  if (value>>i)&1:state|=1<<wire
  else:state&=~(1<<wire)
 return state

def read(state,wires):return sum(((state>>w)&1)<<i for i,w in enumerate(wires))
# Literal truth tables for negative controls, including arbitrary dirty target.
literal_cases=0
for a,b,pa,pb,out in product((0,1),repeat=5):
 w=list(r.cc_signed(0,pa,1,pb,2));before=a|(b<<1)|(out<<2);after=apply(w,before)
 want=out^((a if pa else 1-a)&(b if pb else 1-b))
 assert after==a|(b<<1)|(want<<2) and all(g[-1] not in (0,1) for g in w);literal_cases+=1
# Independent exhaustive small equality and unsigned comparator circuits.
eq_cases=0
for n in range(0,6):
 controls=list(range(n));target=n;work=list(range(n+1,n+1+max(0,n-2)))
 for pattern in range(1<<n):
  word=list(r.pattern_gate(controls,pattern,target,work));assert all(g[-1] not in controls for g in word)
  for x in range(1<<n):
   for out in (0,1):
    state=x|(out<<target);assert apply(word,state)==x|((out^(x==pattern))<<target);eq_cases+=1
comp_cases=0
for n in range(1,6):
 reg=list(range(n));target=n;work=list(range(n+1,2*n+2));spectator=2*n+2
 for threshold in range(2**n+1):
  word=list(r.compare_xor(reg,threshold,target,work));assert all(g[-1] not in reg for g in word)
  for x in range(2**n):
   for y in (0,1):
    before=x|(y<<target)|(1<<spectator);after=apply(word,before)
    assert after==x|((y^(x<threshold))<<target)|(1<<spectator);comp_cases+=1
# independent lexicographic stopped-prefix ranking.
def prefixes(n):
 raw=[];pool=[set(),set()]
 for val in range(2**n):
  seq=[];cost=0
  for i in range(n):
   if cost>=n:break
   b=(val>>i)&1;cost+=1+b;seq.append(b)
  kind=cost-n;assert kind in (0,1);prefix=tuple(seq);pool[kind].add(prefix);raw.append((val,kind,prefix))
 ranks=[{seq:i for i,seq in enumerate(sorted(g))} for g in pool]
 return [[val,kind,ranks[kind][pre]] for val,kind,pre in raw]

sources=['INTERNAL_SELECTOR_PALETTE.json','TOP_SOURCE_SELECTOR_PALETTE.json','TEN_SIGN_REPORT_PALETTE.json'];rows_checked=0;zero_lengths=0;duplicate_boundaries=0;rank_codes=0;circuits=[]
for name in sources:
 pal=json.loads((A/name).read_text());path=D/name.replace('PALETTE','CIRCUIT');plan=json.loads(path.read_text());n=pal['golden_coins_n'];rw=plan['label_width'];q=plan['layout']
 full=[wire for wires in q.values() for wire in wires];assert len(set(full))==len(full)==plan['wire_count'] and set(full)==set(range(plan['wire_count']))
 codes=prefixes(n);assert plan['prefix_codes']==codes;rank_codes+=len(codes)
 assert len(plan['rows'])==2*len(pal['partitions'])
 for pos,row in enumerate(plan['rows']):
  j,k=divmod(pos,2);assert row['palette']==j and row['kind']==k
  partition=pal['partitions'][j];counts=[[int(v) for v in x] for x in partition['counts_ready_then_abort']]
  assert len(counts)==len(partition['weights'])+1
  t=0;expected=[];bounds=[];width=len(q['fair'])+len(q['rank'])
  for i,entry in enumerate(counts[:-1]):
   if entry[k]==0:zero_lengths+=1
   t+=entry[k];code=(1<<rw)|i;nextcode=((1<<rw)|(i+1)) if i+1<len(counts)-1 else 0;mask=code^nextcode
   if t and mask:expected.append([str(t),mask]);bounds.append(t)
  duplicate_boundaries+=sum(bounds[i]==bounds[i-1] for i in range(1,len(bounds)))
  assert row['boundaries']==expected and all(0<int(x[0])<=2**width for x in expected)
  # For every interval with nonzero width, both ends decode identically to direct cumulative lookup.
  cursor=0
  for label,pair in enumerate(counts):
   lo=cursor;cursor+=pair[k]
   if lo==cursor:continue
   expected_code=0 if label==len(counts)-1 else (1<<rw)|label
   for x in (lo,cursor-1):
    actual=0
    for threshold,mask in expected:
     if x<int(threshold):actual^=mask
    assert actual==expected_code
  rows_checked+=1
 invalid=list(range(len(pal['partitions']),2**len(q['palette'])))
 assert all(not any(row['palette']==j for row in plan['rows']) for j in invalid)
 circuits.append({'file':path.name,'actual_rows':len(plan['rows']),'invalid_palette_codes':len(invalid),'logical_gate_counts':plan['terminal_gate_counts']})
assert rows_checked==5170 and rank_codes==67
# Execute a separate selection of true-width row blocks with actual big-integer
# thresholds, dirty outputs, matched and unmatched control; no dense matrix.
actual_width_cases=0
for name in sources:
 path=D/name.replace('PALETTE','CIRCUIT');plan=json.loads(path.read_text());q=plan['layout'];eligible=[row for row in plan['rows'] if row['boundaries']]
 choices=[eligible[0],eligible[len(eligible)//2],eligible[-1]]
 for row in choices:
  word=list(r.row_word(plan,row));width=len(q['fair'])+len(q['rank']);threshold=int(row['boundaries'][0][0])
  for pos in sorted({0,min(2**width-1,threshold),threshold-1,2**width-1}):
   for matching in (0,1):
    # On a full-sized palette, toggle kind to produce an unselected row.
    kind=row['kind'] if matching else 1-row['kind'];j=row['palette'];old=(1<<len(q['output']))-1;state=0
    for key,val in [('palette',j),('kind',kind),('fair',pos%(2**len(q['fair']))),('rank',pos>>len(q['fair'])),('output',old)]:state=insert(state,q[key],val)
    expected=0
    if matching:
     for t,mask in row['boundaries']:
      if pos<int(t):expected^=mask
    assert apply(word,state)==insert(state,q['output'],old^expected);actual_width_cases+=1
# Hostile repeated threshold: both XOR masks are needed, including zero-width label.
# Codes [2,3,0] and counts [3,0,5] => two threshold-3 masks [1,3].
assert (1^3)==2 and 1!=2
# Full smaller selector: includes zero count, repeated threshold, invalid j, suffix, dirty y.
small={'golden_coins_n':2,'fair_bits_r':2,'partitions':[
 {'weights':[[1,0],[0,0]],'counts_ready_then_abort':[[0,1],[3,0],[5,3]]},
 {'weights':[[1,0],[0,0],[0,0]],'counts_ready_then_abort':[[2,0],[0,1],[6,1],[0,2]]},
 {'weights':[[1,0]],'counts_ready_then_abort':[[8,4],[0,0]]}]}
plan=r.make_plan(small);q=plan['layout'];word=list(r.selector_word(plan));readonly=set(q['palette']+q['golden']+q['fair']);assert all(g[-1] not in readonly for g in word)
pr={v:(k,rank) for v,k,rank in prefixes(2)};small_cases=0
for j,g,f,y in product(range(4),range(4),range(4),range(8)):
 state=0
 for key,val in [('palette',j),('golden',g),('fair',f),('output',y)]:state=insert(state,q[key],val)
 want=0
 if j<3:
  kind,rank=pr[g];x=rank*4+f;acc=0;part=small['partitions'][j]
  for label,pair in enumerate(part['counts_ready_then_abort']):
   acc+=pair[kind]
   if x<acc:
    if label<len(part['weights']):want=(1<<plan['label_width'])|label
    break
 result=apply(word,state);assert result==insert(state,q['output'],y^want)
 assert apply(reversed(word),result)==state;small_cases+=1
# First success full flags for both actual widths, arbitrary prior output + ready.
first_cases=0;rng=random.Random(2801)
for width in (2,6):
 plan=r.first_success_plan(7,width);q=plan['layout'];word=list(r.first_success_word(plan));readonly=set(q['labels']+q['ready']);assert all(g[-1] not in readonly for g in word)
 for flags in range(128):
  for _ in range(4):
   labels=[rng.randrange(1<<width) for _ in range(7)];y=rng.randrange(1<<width);ready=rng.randrange(2);state=0
   for key,val in [('labels',sum(v<<(i*width) for i,v in enumerate(labels))),('ready',flags),('output',y),('out_ready',ready)]:state=insert(state,q[key],val)
   idx=next((i for i in range(7) if flags>>i&1),None);want=0 if idx is None else labels[idx]
   result=apply(word,state);expect=insert(insert(state,q['output'],y^want),q['out_ready'],ready^(idx is not None))
   assert result==expect and apply(reversed(word),result)==state;first_cases+=1
assert (1^2)!=1  # XOR of all successes is not the first success.
files=[D/'reversible_selectors.py',D/'build_selector_circuits.py',D/'check_selector_circuits.py']+[D/x.replace('PALETTE','CIRCUIT') for x in sources]+[A/x for x in sources]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
res={'status':'PASS_INDEPENDENT_A13_STRUCTURE_AND_BOOLEAN_FIXTURES','input_sha256':{str(f):sha(f) for f in files},'negative_literal_truth_table_cases':literal_cases,'equality_cases':eq_cases,'comparator_cases':comp_cases,'actual_rows_independently_checked':rows_checked,'prefix_codes_independently_rebuilt':rank_codes,'zero_width_labels_seen':zero_lengths,'repeated_nonzero_boundaries_seen':duplicate_boundaries,'true_width_row_cases':actual_width_cases,'full_small_selector_cases':small_cases,'cap7_first_success_cases':first_cases,'invalid_palette_and_dirty_output_tested':True,'hostile_repeated_threshold_detected':True,'hostile_all_success_xor_detected':True,'circuit_summaries':circuits,'physical_native_word_executed':False,'full_READY_or_physical_C_proved':False,'GR_closed':False}
(P/'INDEPENDENT_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['status','actual_rows_independently_checked','zero_width_labels_seen','repeated_nonzero_boundaries_seen','full_small_selector_cases','cap7_first_success_cases']}))
