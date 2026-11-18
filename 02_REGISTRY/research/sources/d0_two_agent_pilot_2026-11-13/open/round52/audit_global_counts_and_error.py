#!/usr/bin/env python3
"""Rebuild A25 schedule, resource inventory and exact canonical-input bound."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from fractions import Fraction
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=P.parent
files={'global':D/'round25/GLOBAL_H1_PLAN.json','namespace':D/'round25/H1_NAMESPACE_PLAN.json','choi':D/'round22/FULL_CHOI_BANK_PLAN.json','car':D/'round24/FULL_CAR_SOURCE_PLAN.json','site':O/'round45/SITE_NATIVE_PLAN.json','report':D/'round17/GLOBAL_REPORT_COMPILATION.json'};h=lambda p:sha256(p.read_bytes()).hexdigest();pins={str(f):h(f) for f in files.values()};obj={name:json.loads(file.read_text()) for name,file in files.items()};p=obj['global'];ns=obj['namespace'];AX=('G_port','G_other','CX','SourceI')
for path,digest in p['source_sha256'].items():assert h(Path(path))==digest,path
banks=('y+','y-','f','0','x+','x-','q');schedule=[{'kind':'SITE'}];slots=[]
for i,b in enumerate(banks):
 r=ns['reports'][i];assert r['bank']==b;schedule.append({'kind':'SIGMA','report':i});ids=[j for j,z in enumerate(ns['source_slots']) if z['bank']==b];assert ids==r['source_slots'] and len(ids)==196;slots+=ids
 schedule.extend({'kind':'SOURCE','slot':j} for j in ids);schedule.append({'kind':'REPORT','report':i})
schedule.extend([{'kind':'PORT_ZERO'},{'kind':'SC6'}]);assert slots==list(range(1372)) and len(schedule)==1389 and p['forward_stage_schedule']==schedule

def ctr(obj):return Counter({k:int(obj.get(k,0)) for k in AX})
def plus(parts):
 out=Counter()
 for q in parts:out.update(q)
 return out
def mult(c,n):return Counter({k:n*v for k,v in c.items()})
def reverse(c):return Counter(G_port=c['G_port']+c['G_other'],G_other=0,CX=c['CX']+6*c['G_other'],SourceI=3*c['SourceI']+4*(c['G_port']+c['G_other']))
components={'SITE':ctr(obj['site']['native_inventories']['SITE_forward']),'SIGMA7':Counter(G_port=7,CX=42,SourceI=28),'Choi1260':Counter(),'CAR112':Counter(),'REPORT7':mult(ctr(obj['report']['native_forward_resources']),7),'PORT_ZERO':Counter(G_port=1,SourceI=4),'SC6':Counter(G_port=5888,CX=4096,SourceI=8192)}
for b in banks:
 components['Choi1260'].update(mult(ctr(obj['choi']['native_inventories'][b]['RAW_prepared_forward']),180))
 components['CAR112'].update(mult(ctr(obj['car']['all7_banks'][b]['native']['source_forward']),16))
for k,v in components.items():assert all(v[q]==int(p['global_native_counts']['components'][k][q]) for q in AX),k
A=plus(components.values());R=reverse(A);W=plus([A,R,Counter(SourceI=2)])
for name,value in [('A_forward',A),('A_literal_inverse',R),('W_literal_echo',W)]:assert all(value[q]==int(p['global_native_counts'][name][q]) for q in AX),name
calls=sum(W.values());assert calls==int(p['W_primitive_call_count_decimal']) and calls.bit_length()==p['W_primitive_call_count_bit_length']==4188
F=lambda x,y:Fraction(int(x,16),int(y,16));cn=obj['choi'];ce=F(cn['exact_error_numerators_hex'][2],cn['exact_error_denominators_hex'][2]);car_err=[]
for b in banks:
 z=obj['car']['all7_banks'][b];car_err.append(F(z['error_numerator_hex'],z['error_denominator_hex']))
site=F(obj['site']['error_numerator_hex'],obj['site']['error_denominator_hex']);assert site==18*Fraction(1,2**3264)
report=Fraction(obj['report']['seven_report_all_known_approximate_macros'],2**4096);assert obj['report']['seven_report_all_known_approximate_macros']==162754649904
parts={'Choi1260':1260*ce,'CAR112':16*sum(car_err,Fraction()),'SITE_once':site,'REPORT7':report,'SIGMA_PORT_SC6':Fraction()};eta=sum(parts.values(),Fraction())
for name,val in parts.items():
 saved=p['conditional_canonical_input_error_components'][name]
 if val:assert val==F(saved['numerator_hex'],saved['denominator_hex'])
 else:assert saved['exact_zero']
assert eta==F(p['canonical_input_error_bound']['numerator_hex'],p['canonical_input_error_bound']['denominator_hex']);assert eta<Fraction(1,2**3232)
assert 2*eta==F(p['compressed_reflection_error_bound']['numerator_hex'],p['compressed_reflection_error_bound']['denominator_hex']) and 2*eta<Fraction(1,2**3231)
for path,digest in pins.items():assert h(Path(path))==digest,path
out={'status':'PASS_INDEPENDENT_GLOBAL_SCHEDULE_INVENTORY_AND_INPUT_BOUND','input_sha256':pins,'source_pins_in_global_plan_unchanged':True,'stages':len(schedule),'source_slots':len(slots),'all_AXES_components_A_Ainverse_W_exact':True,'W_call_count_bits':calls.bit_length(),'all_error_fractions_match':True,'eta_canonical_RAW_input_lt':'2^-3232','compressed_reflection_error_lt':'2^-3231','scope':'Exact arithmetic against pinned provider plans; it is not an independent replay of all component angle certificates or a proof that physical original T2 target is this ideal word.','full_word_or_giant_repeats_executed':False,'physical_admission_marks_or_C_proved':False,'GR_closed':False}
(P/'GLOBAL_COUNTS_ERROR_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'stage_count':len(schedule),'bits':calls.bit_length(),'eta_lt':'2^-3232'}))
