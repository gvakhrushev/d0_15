#!/usr/bin/env python3
"""Validate dynamic signed pair specification against all real A15 address rows."""
from pathlib import Path
import json,hashlib
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
table=D/'round15/SOURCE_DISPATCH_TABLES.json';data=json.loads(table.read_text());rows=data['address_rows'];assert data['address_widths']==[2,22,22] and len(rows)==72192

def instruction(x,a,b,control,delta):
 # Logical contract only: a,b,delta/control untouched; zero work cleaned.
 m=(x==a)^(x==b)
 return x ^ ((a^b) if control and m else 0),(-1 if control and delta and not m else 1)
checks=0;kinds={1:0,2:0};nonzero_car=0
for width,key,val in rows:
 kind=val&3;a=(val>>2)&((1<<22)-1);b=(val>>24)&((1<<22)-1)
 assert width==17 and kind in kinds and a!=b and 0<=a<2**22 and 0<=b<2**22
 kinds[kind]+=1;nonzero_car+=kind==2 and a!=0
 candidates={a,b,0,(1<<22)-1,a^b,(a+1)%(1<<22),(b+1)%(1<<22)}
 for x in candidates:
  for h in (0,1):
   for delta in (0,1):
    y,phase=instruction(x,a,b,h,delta)
    expected=(b if x==a else a if x==b else x) if h else x
    expected_phase=-1 if h and delta and x not in (a,b) else 1
    assert (y,phase)==(expected,expected_phase)
    y2,phase2=instruction(y,a,b,h,delta)
    assert y2==x and phase*phase2==1
    checks+=1
assert kinds=={1:69632,2:2560} and nonzero_car==2560
out={'status':'PASS_DYNAMIC_CONSUMER_SPEC_REAL_A15_PAIRS','site_leaf_pairs':len(rows),'Choi_pairs':kinds[1],'CAR_pairs':kinds[2],'CAR_nonzero_a':nonzero_car,'representative_basis_control_cases':checks,'every_a_distinct_from_b':True,'proof_extension':'equality predicates partition all x into a,b,complement; each class obeys the checked algebra, hence identity holds on all 2^22 columns and linearly on all superpositions','consumer_contract':'leave selector histories,SITE,a,b,delta and nonselected copies unchanged; restore clean workspace; on selected physical copy controlled map x->x xor membership*(a xor b) and phase (-1)^(h*delta*(1-membership))','actual_native_gate_stream_executed':False,'A16_implementation_reviewed':False,'input_sha256':hashlib.sha256(table.read_bytes()).hexdigest(),'GR_closed':False}
Path(__file__).with_name('ACTUAL_LEAF_CONSUMER_SPEC_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
