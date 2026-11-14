#!/usr/bin/env python3
"""Exact mark-index, bank disjointness, RAW frames and reorder fixtures."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from collections import Counter
import json,sys,sympy as s
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round60';sys.path.insert(0,str(D/'round29'));import gcx_birth_clock as a29
old=a29.c.old;ns=old.namespace();L=ns['layout'];sam=set(L['SAM']);site=set(L['SITE']);roots=json.loads((O/'round25/SOURCE_LEAF_BINDING.json').read_text());templates=roots['leaf_templates'];rows=roots['site_bindings'];assert len(templates)==282 and len(rows)==256
# Actual source copy roles from all 7 banks: DATA/private/RIGHT are disjoint
# across slots, and all belong to their bank's disjoint numeric region.
seen=set();bybank=Counter();representative={};ranges=[]
for report in ns['reports']:
 lo=report['private_start'];hi=lo+report['private_width']+report['source_private_width'];ranges.append((lo,hi,report['bank']))
 assert lo>=2706 and hi<=L['qubits']
 for idx in report['source_slots']:
  slot=ns['source_slots'][idx];bybank[(slot['bank'],slot['kind'])]+=1
  if slot['kind']=='Choi':
   q=slot['source'];assert len(q)==22 and slot['address']==q[10:] and slot['choi_input']==q[5:10] and slot['choi_output']==q[:5]
   support=q+slot['private']
  else:
   q=slot['source'];assert len(q)==12 and slot['grade']==q[:4] and slot['internal_SITE']==q[4:] and len(slot['RIGHT'])==7
   support=q+slot['RIGHT']+slot['private']
  assert len(support)==len(set(support)) and not seen.intersection(support) and all(lo<=w<hi for w in support)
  assert not (sam|site|{0,1,2,3,L['port']}).intersection(support);seen.update(support)
  representative.setdefault((slot['bank'],slot['kind']),slot)
assert all(a[1]==b[0] for a,b in zip(ranges,ranges[1:])) and len(seen)>0
assert all(bybank[(bank,'Choi')]==180 and bybank[(bank,'CAR')]==16 for bank in ('y+','y-','f','0','x+','x-','q'))
# H3 geometric mark indices, computational output frame, physical m=0/3.
for bank in ('f','q'):
 for kind in ('Choi','CAR'):
  slot=representative[(bank,kind)];logical=slot['source']+(slot['RIGHT'] if kind=='CAR' else [])
  for m in (0,3):
   physical=[a29.physical_wire(q,m) for q in logical];assert len(physical)==len(set(physical)) and all(q>=m for q in physical)
counts=Counter();maxidx=0
for row in rows:
 assert len(row['leaf_addresses_in_template_order'])==282
 for t,addr in zip(templates,row['leaf_addresses_in_template_order']):
  if t['kind']=='Choi':
   i=t['input'];j=t['output'];assert 0<=addr<2049 and 0<=i<32 and 0<=j<32
   idx=(addr<<10)|(i<<5)|j;assert idx!=0 and idx<2**22
   assert t['anchor_moment_multiplier'] in (1,2);maxidx=max(maxidx,idx);counts['Choi']+=1
  else:
   assert t['kind']=='CAR' and 0<=addr<256 and t['cross_masks'][0]==1 and t['cross_masks'][1] in (0,15) and t['RIGHT_action']=='identity'
   counts['CAR']+=1
assert counts=={'Choi':69632,'CAR':2560}
# Exact output-frame counterexample: computational source state U|0> wants
# O; encoded source B U|0> wants B O B*. Applying encoded mark to unencoded
# source differs, even though both are conjugate representations.
p=(s.sqrt(5)-1)/2;a=s.sqrt(p);B=s.Matrix([[a,-p],[p,a]]);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);v=B*s.Matrix([1,0]);Pcomp=X*B.T;Penc=B*X*B.T
comp=Pcomp*v;enc=Penc*v;Oc=Z;Oe=B*Z*B.T
assert s.simplify((comp.T*Oc*comp)[0]+1)==0 and s.simplify((enc.T*Oe*enc)[0]+1)==0
mismatch=s.simplify((comp.T*Oe*comp)[0]+1);assert s.simplify(mismatch-2*p**2)==0
# Exact finite reorder: SAM=0, SITE=1, old=2, f=3, q=4. Both maps can
# control shared SAM/SITE yet act on disjoint source/report target.
def CNOT(control,target,n):
 M=s.zeros(2**n)
 for x in range(2**n):
  y=x^(1<<(n-1-target)) if (x>>(n-1-control))&1 else x;M[y,x]=1
 return M
def CCNOT(c1,c2,target,n):
 M=s.zeros(2**n)
 for x in range(2**n):
  y=x^(1<<(n-1-target)) if ((x>>(n-1-c1))&1) and ((x>>(n-1-c2))&1) else x;M[y,x]=1
 return M
Q=CNOT(0,4,5);R=CCNOT(0,1,3,5);assert Q*R==R*Q
# Identical ideal word does not give exact commutation for arbitrary native
# implementations using a shared dirty helper.
assert X*B!=B*X
# Same prepared fresh |0> can hide arbitrary dirty-column discrepancy.
ket0=s.Matrix([1,0]);plus=s.Matrix([1,1])/s.sqrt(2);minus=Z*plus
assert Z*ket0==ket0 and (plus.T*X*plus)[0]==1 and (minus.T*X*minus)[0]==-1
# Transport across an intervening source/report can extend an f-local mark.
T=CNOT(0,1,2);Of=s.kronecker_product(X,s.eye(2));rho=s.kronecker_product(plus,ket0);transport=T*Of*T.T
assert s.simplify((rho.T*Of*rho)[0]-1)==0
assert s.simplify(((T*rho).T*Of*(T*rho))[0])==0
assert s.simplify(((T*rho).T*transport*(T*rho))[0]-1)==0
# Prefix-isometry mark loss has TWO replacement terms; bound exactly.
err=old.__file__;plan=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text());e=plan['compressed_reflection_error_bound'];eold=F(int(e['numerator_hex'],16),int(e['denominator_hex'],16));census=json.loads((O/'round58/CZ_EXACT_OCCURRENCES.json').read_text());Rcount=2*int(census['W_nonCZ_SourceI_pair_count'])+4*census['W_CZ_total'];replace=F(Rcount,2**7432);mark=eold+2*replace;assert mark<F(1,2**3231)
# Actual A25 timing f REPORT before q source, not a claim of actual f loss.
stages=old.stages(ns);f_report=next(i for i,t in enumerate(stages) if t['kind']=='REPORT' and ns['reports'][t['report']]['bank']=='f');q_source=next(i for i,t in enumerate(stages) if t['kind']=='SOURCE' and ns['source_slots'][t['slot']]['bank']=='q');assert f_report<q_source
files=[D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/global_h1.py',D/'round25/GLOBAL_H1_PLAN.json',D/'round29/gcx_birth_clock.py',O/'round25/SOURCE_LEAF_BINDING.json',O/'round58/CZ_EXACT_OCCURRENCES.json']
out={'status':'PASS_ORIGINAL_MARK_INDICES_REORDER_AND_FRAME_BOUNDARIES','source_slots':sum(bybank.values()),'seven_banks_each_Choi_CAR':[180,16],'disjoint_source_operand_wires':len(seen),'leaf_indices_per_bank':dict(counts),'seven_banks_leaf_indices':7*sum(counts.values()),'max_choi_basis_index':maxidx,'choi_coframe_norm':'32784','choi_link_norm':'65568','CAR_Psi_norm':'128/sqrt(p)','raw_frame_mismatch_exact':'2p^2','controlled_disjoint_ideal_reorder_exact':True,'shared_native_helper_commutation_not_assumed':True,'canonical_fibre_not_dirty_columns':True,'source_mark_transport_fixture':True,'original_A25_f_report_stage':f_report,'original_A25_first_q_source_stage':q_source,'conservative_prefix_mark_error_per_unit_norm_lt':'2^-3231 conditional on prefix telescope','exact_old_plus_twice_replacement_scaled_float':float(mark*2**3231),'physical_old_mark_transport_or_reader_proved':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files},'physical_C_closed':False,'GR_closed':False}
(P/'H3_MARKS_REORDER_AND_FRAME_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'source_slots':out['source_slots'],'leaf_indices':out['seven_banks_leaf_indices'],'prefix_scaled':out['exact_old_plus_twice_replacement_scaled_float'],'stage_fq':[f_report,q_source]}),flush=True)
