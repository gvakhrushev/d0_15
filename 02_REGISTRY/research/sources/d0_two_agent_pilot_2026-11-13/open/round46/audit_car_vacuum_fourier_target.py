#!/usr/bin/env python3
"""Exact original B25 CAR vacuum/Fourier prefix target; not a native word."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import product
import json,numpy as np
P=Path(__file__).resolve().parent;B=P.parent;pf=B/'round21/ORIGINAL_PF_N20_L4.jsonl';fq=B/'round21/ORIGINAL_FOURIER128_L4.json';target=B/'round25/targets.py'
rows=[json.loads(x) for x in pf.read_text().splitlines()];kappa=json.loads(fq.read_text())['kappa'];assert len(rows)==256 and len(kappa)==64
F=np.zeros((256,128),dtype=np.int64);quadrants=Counter();table=bytearray()
for zi,row in enumerate(rows):
 z=row['site'];assert zi==64*z[0]+16*z[1]+4*z[2]+z[3]
 for k,v in enumerate(kappa):
  t=sum(x*y for x,y in zip(v,z))%4;quadrants[t]+=1;table.append(t);right=2*k+(t&1);sgn=-1 if t&2 else 1;F[zi,right]=sgn
assert quadrants=={0:4096,1:4096,2:4096,3:4096} and np.array_equal(np.matmul(F.T,F),128*np.eye(128,dtype=np.int64))
# Alternative source-equivalent state prep: one pair-index k controls at
# most eight quarter-turns on RIGHT type, with angle coefficients mod4.
coeff={};nactive=0;maxsum=0
for k,v in enumerate(kappa):
 seq=[]
 for mu,value in enumerate(v):
  for bit,a in ((2*(3-mu),value%4),(2*(3-mu)+1,(2*value)%4)):
   if a:seq.append((bit,a))
 coeff[k]=seq;nactive+=len(seq);maxsum=max(maxsum,sum(a for _,a in seq))
 assert len(seq)<=8
 for zi,row in enumerate(rows):
  t=sum(a*((zi>>bit)&1) for bit,a in seq)%4;want=sum(x*y for x,y in zip(v,row['site']))%4;assert t==want
assert nactive==318 and maxsum==18
# Construct the 4-grade m_* from RAW-to-zero: G(q0), CX(q0,q1..q3), X(q0).
# On zero grade, the first component reaches |1>, the second |14> exactly.
def grade_index(q0,afterX):return ((15 if q0 else 0)^1) if afterX else (15 if q0 else 0)
assert grade_index(0,True)==1 and grade_index(1,True)==14
out={'status':'EXACT_B25_CAR_VACUUM_FOURIER_TARGET_TABLE_NOT_NATIVE_COMPILATION','input_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in (pf,fq,target)},'site_labels':256,'kappa_labels':64,'right_dimensions':128,'quadrant_counts':dict(quadrants),'quadrant_table_sha256':sha256(bytes(table)).hexdigest(),'exact_F_transpose_F':'128 I_128','right_index':'2*k+type','amplitude':'F[z,right]/128','fresh_RAW_wires_for_one_4grade_8site_7right_copy':19,'logical_start':'19 RAW-to-zero; H(site8); H(right-k6); G(grade0); CX(grade0->grade1,2,3); X(grade0)','conditional_quadrant_X_nodes':quadrants[1]+quadrants[3],'conditional_minus_I_nodes':quadrants[2]+quadrants[3],'read_only_selector_bits':14,'shorter_controlled_quarter_turn_route':{'nonzero_coefficient_nodes':nactive,'max_nodes_per_k':8,'max_sum_coefficient_per_k':maxsum,'read_only_controls':7,'aux_clean_work':0,'all_16384_quadrants_checked':True,'full_all_column_extension_equivalence_to_unknown_owner_prefix_not_claimed':True},'conditional_phase_is_not_new_Info':True,'full_native_prefix_emitted':False,'physical_birth_admission_proved':False,'GR_closed':False}
(P/'CAR_VACUUM_FOURIER_TARGET.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','quadrant_counts','conditional_quadrant_X_nodes','conditional_minus_I_nodes')}))
