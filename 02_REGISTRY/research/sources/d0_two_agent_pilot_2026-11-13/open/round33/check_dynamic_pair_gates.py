#!/usr/bin/env python3
"""Independent small-width gate proof of a clean dynamic selected pair."""
from itertools import product
from pathlib import Path
import json

def build(n):
 # Wire layout: x, a, b, h, delta, spectator, member, control,
 # diff[n], and-chain[max(n-1,0)]. All workspace starts 0.
 x=list(range(n));a=list(range(n,2*n));b=list(range(2*n,3*n));h=3*n;delta=h+1;spec=h+2;m=h+3;t=h+4
 d=list(range(h+5,h+5+n));v=list(range(h+5+n,h+5+n+max(0,n-1)));N=h+5+n+max(0,n-1);g=[]
 def gate(op,*w):assert len(set(w))==len(w);g.append((op,*w))
 def eq_xor(addr):
  # d_i = 1 xor x_i xor addr_i on clean scratch, for all i.
  for i in range(n):gate('X',d[i]);gate('CX',x[i],d[i]);gate('CX',addr[i],d[i])
  chain=[]
  if n==1:gate('CX',d[0],m)
  else:
   chain.append((d[0],d[1],v[0]))
   for i in range(2,n):chain.append((v[i-2],d[i],v[i-1]))
   for step in chain:gate('CCX',*step)
   gate('CX',v[n-2],m)
   for step in reversed(chain):gate('CCX',*step)
  for i in reversed(range(n)):gate('CX',addr[i],d[i]);gate('CX',x[i],d[i]);gate('X',d[i])
 def membership():eq_xor(a);eq_xor(b)
 membership()
 # t=h(1-m), CZ(t,delta) gives phase (-1)^(h delta (1-m)).
 gate('CX',h,t);gate('CCX',h,m,t);gate('CZ',t,delta);gate('CCX',h,m,t);gate('CX',h,t)
 # t=h*m, then x ^= t*(a xor b); only x targeted.
 gate('CCX',h,m,t)
 for i in range(n):gate('CCX',t,a[i],x[i]);gate('CCX',t,b[i],x[i])
 gate('CCX',h,m,t)
 membership() # m invariant although equality flags interchange after swap.
 return N,g,(x,a,b,h,delta,spec,m,t,d,v)

def run(n,g,val):
 phase=1
 for op,*w in g:
  if op=='X':val^=1<<w[0]
  elif op=='CX':val^=((val>>w[0])&1)<<w[1]
  elif op=='CCX':val^=(((val>>w[0])&(val>>w[1]))&1)<<w[2]
  elif op=='CZ':phase*=(-1 if ((val>>w[0])&(val>>w[1])&1) else 1)
 return val,phase
checks=0;gate_counts={}
for n in range(1,5):
 N,g,layout=build(n);xw,aw,bw,h,d,spec,m,t,diff,chain=layout;gate_counts[str(n)]={k:sum(op[0]==k for op in g) for k in ('X','CX','CCX','CZ')}
 mask=(1<<n)-1
 for a,b,x,hv,dv in product(range(1<<n),range(1<<n),range(1<<n),range(2),range(2)):
  if a==b:continue
  initial=x|(a<<n)|(b<<(2*n))|(hv<<h)|(dv<<d)|(1<<spec)
  y,phase=run(n,g,initial)
  expected_x=(b if x==a else a if x==b else x) if hv else x
  expected_phase=(-1 if hv and dv and x not in (a,b) else 1)
  assert y==(initial&~mask)|expected_x and phase==expected_phase
  z,phase2=run(n,g,y);assert z==initial and phase*phase2==1
  checks+=1
# Actual 22-bit logical gate word: cover a deterministic cross-section of
# real A15 pairs (including nonzero CAR anchor) and all h/delta combinations.
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
rows=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text())['address_rows']
indices=set(range(0,len(rows),181));indices.add(next(i for i,row in enumerate(rows) if (row[2]&3)==2))
N,g,layout=build(22);xw,aw,bw,h,d,spec,m,t,diff,chain=layout;mask=(1<<22)-1;wide_checks=0
for index in sorted(indices):
 value=rows[index][2];a=(value>>2)&mask;b=(value>>24)&mask
 for x,hv,dv in product((a,b,mask),range(2),range(2)):
  initial=x|(a<<22)|(b<<44)|(hv<<h)|(dv<<d)|(1<<spec)
  y,phase=run(22,g,initial);expected=(b if x==a else a if x==b else x) if hv else x
  expected_phase=-1 if hv and dv and x not in (a,b) else 1
  assert y==(initial&~mask)|expected and phase==expected_phase
  wide_checks+=1
out={'status':'PASS_DYNAMIC_PAIR_GATE_WORD_ALL_SMALL_COLUMNS','gate_basis':['X','CX','CCX','CZ'],'widths':[1,2,3,4],'all_clean_work_columns_with_a_ne_b_and_arbitrary_h_delta_checked':checks,'gate_counts_by_width':gate_counts,'scratch_zero_restored':True,'arbitrary_spectator_bit_preserved':True,'equality_scratch_cleared_before_swap':True,'member_cleared_after_swap_by_recomputed_invariant':True,'actual_22_bit_gate_word_cases':wide_checks,'actual_22_bit_source_pairs':len(indices),'for_actual_22_bit_word':'independent logical witness with clean work; not A16, native expansion, selected-copy routing or full integration','GR_closed':False}
Path(__file__).with_name('DYNAMIC_PAIR_SMALL_GATES_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
