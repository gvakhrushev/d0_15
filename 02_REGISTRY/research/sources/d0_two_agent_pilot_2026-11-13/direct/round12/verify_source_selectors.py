#!/usr/bin/env python3
"""Independent exact table/capacity decoder and full-input involution controls."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
add=lambda x,y:(x[0]+y[0],x[1]+y[1])
mul=lambda x,y:(x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
scale=lambda x,t:(x[0]*t,x[1]*t)
one=(F(1),F(0));p=(F(0),F(1));zero=(F(0),F(0))
def power(x,n):
 result=one
 for _ in range(n):result=mul(result,x)
 return result
def fibonacci(n):
 a,b=0,1
 for _ in range(n):a,b=b,a+b
 return a
def classify(bits,n):
 total=0;prefix=[]
 for bit in bits:
  if total>=n:break
  total+=1+bit;prefix.append(bit)
 assert total>=n
 return total-n,tuple(prefix)
def rank_prefix(prefix,n,kind):
 rank=0;total=0
 for bit in prefix:
  if bit:
   left_remaining=n-(total+1)
   if left_remaining>=0:rank+=fibonacci(left_remaining+(1 if kind==0 else 0))
   elif left_remaining==-1 and kind==1:rank+=1
  total+=1+bit
 assert total==n+kind
 return rank
checks=0;hashes={};palette_summary=[]
for filename in ['INTERNAL_SELECTOR_PALETTE.json','TOP_SOURCE_SELECTOR_PALETTE.json','TEN_SIGN_REPORT_PALETTE.json']:
 path=HERE/filename;obj=json.loads(path.read_text());hashes[filename]=hashlib.sha256(path.read_bytes()).hexdigest()
 n,r=obj['golden_coins_n'],obj['fair_bits_r'];D=int(obj['common_D_integer'])
 tau=F(D,2**r);assert tau==F(obj['ready_probability_rational']) and F(1,2)<tau<=1
 capacities=[2**r*fibonacci(n+1),2**r*fibonacci(n)]
 assert capacities==list(map(int,obj['capacity_by_prefix_kind']))
 leaf_mass={};rank_to_prefix={}
 for bits in product((0,1),repeat=n):
  kind,prefix=classify(bits,n);rank=rank_prefix(prefix,n,kind)
  rank_to_prefix[kind,rank]=prefix
  raw=power(p,sum(1+b for b in bits))
  leaf_mass[kind,prefix]=add(leaf_mass.get((kind,prefix),zero),raw)
 for (kind,prefix),weight in leaf_mass.items():
  assert weight==power(p,n+kind)
 for kind in (0,1):
  assert len([key for key in rank_to_prefix if key[0]==kind])==fibonacci(n+(1 if kind==0 else 0))
 for part in obj['partitions']:
  counts=[list(map(int,pair)) for pair in part['counts_ready_then_abort']]
  assert all(a>=0 and b>=0 for a,b in counts)
  assert [sum(pair[k] for pair in counts) for k in (0,1)]==capacities
  expected=[tuple(map(F,w)) for w in part['weights']]+[(1-tau,F(0))]
  sums=zero
  for j,(a,b) in enumerate(counts):
   actual=scale(mul((F(a),F(b)),power(p,n)),F(1,2**r))
   wanted=expected[j] if j==len(counts)-1 else scale(expected[j],tau)
   assert actual==wanted
   sums=add(sums,actual);checks+=1
  assert sums==one
  # Every nonempty interval's endpoints decode to its label. These are exact
  # integer rank comparisons; no probability division or finite precision.
  for kind in (0,1):
   offset=0
   for label,pair in enumerate(counts):
    length=pair[kind]
    for pos in ([] if length==0 else [offset,offset+length-1]):
     assert 0<=pos<capacities[kind]
     leaf_rank,fair_rank=divmod(pos,2**r)
     prefix=rank_to_prefix[kind,leaf_rank]
     assert rank_prefix(prefix,n,kind)*2**r+fair_rank==pos
     cumulative=0;decoded=None
     for q,row in enumerate(counts):
      cumulative+=row[kind]
      if pos<cumulative:decoded=q;break
     assert decoded==label;checks+=1
    offset+=length
 palette_summary.append({'file':filename,'partitions':len(obj['partitions']),'r':r,'n':n})

# Full-space rank-two operators, including the non-active complement.
def involution_basis(x,a,b,negative):
 active=x==a or x==b
 return (x^(a^b) if active else x),(-1 if negative and not active else 1)
for dim in (4,8,16):
 for a in range(dim):
  for b in range(a+1,dim):
   for x in range(dim):
    for negative in (False,True):
     y,s=involution_basis(x,a,b,negative);back,t=involution_basis(y,a,b,negative)
     assert back==x and s*t==1
    y,sp=involution_basis(x,a,b,False);_,sm=involution_basis(x,a,b,True)
    assert F(sp+sm,2)==(1 if x in (a,b) else 0)
    checks+=3
# Reusing the same fair selector for two copies is a real wrong operator:
# on |2,2> the correlated mixture is +1, while X_01 tensor X_01 is zero.
correlated=sum(involution_basis(2,0,1,s)[1]**2 for s in (False,True))/2
independent=sum(involution_basis(2,0,1,s)[1]*involution_basis(2,0,1,t)[1]
                for s,t in product((False,True),repeat=2))/4
assert correlated==1 and independent==0

summary=json.loads((HERE/'SELECTOR_COMPILATION.json').read_text())
internal=json.loads((HERE/'INTERNAL_SELECTOR_PALETTE.json').read_text())
top=json.loads((HERE/'TOP_SOURCE_SELECTOR_PALETTE.json').read_text())
post=json.loads((HERE/'TEN_SIGN_REPORT_PALETTE.json').read_text())
T=summary['padded_interpreter_slots_per_ten_sign_report'];caps=summary['retained_selector_caps']
M=T*caps['internal']*internal['fair_bits_r']+10*caps['top']*top['fair_bits_r']+post['fair_bits_r']+summary['leaf_involution_fair_bits_per_report']
G=T*caps['internal']*internal['golden_coins_n']+10*caps['top']*top['golden_coins_n']+post['golden_coins_n']
assert M==summary['selector_fair_qubits_per_report'] and G==summary['selector_Golden_qubits_per_report']
error=M*F(53,100)**caps['fair_plus_bank']+T*(1-F(internal['ready_probability_rational']))**caps['internal']+10*(1-F(top['ready_probability_rational']))**caps['top']
assert error==F(summary['combined_failure_union_bound_rational']) and error<=F(1,2)
assert not summary['full_native_READY_computed']
result={'status':'PASS_EXACT_SELECTOR_TABLES_AND_FULL_INPUT_INVOLUTION_CONTROLS','checks':checks,
        'palettes':palette_summary,'table_hashes':hashes,
        'retained_selector_caps':caps,'selector_fair_qubits_per_report':M,
        'selector_Golden_qubits_per_report':G,'ready_component_lower_bound':'1/2',
        'same_coin_two_copy_hostile_detected':True,
        'Boolean_or_native_factory_word_checked':False,'full_H1_READY_claimed':False,'GR_closed':False}
(HERE/'SELECTOR_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
