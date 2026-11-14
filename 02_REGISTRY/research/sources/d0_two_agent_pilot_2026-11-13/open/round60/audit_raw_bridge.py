#!/usr/bin/env python3
"""Independent explicit resource-bank bridge, counts and error arithmetic."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round60';sys.path.insert(0,str(D/'round29'));import gcx_compiler as c
g=c.old;nb=c.nb;ns=g.namespace();layout=ns['layout'];port=layout['port'];spin=tuple(layout['spin']);sam=set(layout['SAM']);site=set(layout['SITE']);count={'Choi':0,'CAR':0};allw=set()
for row in ns['source_slots']:
 data=row['source']+(row['RIGHT'] if row['kind']=='CAR' else [])
 assert len(data)==(22 if row['kind']=='Choi' else 19)
 assert len(data)==len(set(data)) and not allw.intersection(data)
 assert not set(data).intersection(sam|site|{0,1,2,3,port})
 allw.update(data);count[row['kind']]+=len(data)
assert count=={'Choi':27720,'CAR':2128} and len(allw)==29848
# One actual old G, its 1st and 2nd literal native inverses, as they appear
# in A and A† for B;B†. Full finite DAG counts, not a free G^-1.
q=next(iter(allw));assert q!=port;F0=nb.gate('G',q);F1=nb.inverse_literal(F0,port,spin);F2=nb.inverse_literal(F1,port,spin);trees=[F0,F1,F2,F1]
from collections import Counter
oldsum=sum((Counter(nb.counts(t)) for t in trees),Counter());assert oldsum=={'G':4,'CX':18,'SourceI':24}
compiler=c.production_compiler();newsum=Counter();npairs=0
for t in trees:
 out,pending,num=compiler.transform(t);assert pending==0 and num['CZ']==0;npairs+=num['Z'];newsum.update(nb.counts(out))
k=compiler.k;assert npairs==12 and newsum=={'G':4+192*k,'CX':42}
R=json.loads((O/'round58/CZ_EXACT_OCCURRENCES.json').read_text());rot_old=2*int(R['W_nonCZ_SourceI_pair_count'])+4*R['W_CZ_total'];rot_new=rot_old+24*len(allw);assert rot_new<2**4188
plan=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text());e=plan['compressed_reflection_error_bound'];oldbound=F(int(e['numerator_hex'],16),int(e['denominator_hex'],16));rep=F(rot_new,2**7432);assert rep<F(1,2**3244) and oldbound+rep<F(1,2**3231) and oldbound+2*rep<F(1,2**3231)
paths=[D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',D/'round29/gcx_compiler.py',O/'round58/CZ_EXACT_OCCURRENCES.json',O/'round57/GADGET_G_POWER_CERTIFICATE.json']
out={'status':'PASS_EXPLICIT_DATA_RAW_BRIDGE_COUNTS','choi_resource_wires':count['Choi'],'CAR_resource_wires':count['CAR'],'total_distinct_resource_data_wires':len(allw),'excludes_SAM_external_SITE_port_and_old':True,'forward_and_inverse_actual_depths':[0,1,2,1],'old_extra_per_wire':{'G':4,'CX':18,'SourceI':24},'new_extra_per_wire':{'G':'4+192k','CX':42,'rotation_power_blocks':24},'new_total_rotation_blocks_lt':'2^4188','replacement_error_lt':'2^-3244','endpoint_and_prefix_marks_both_lt':'2^-3231 before mark norm factors','all_original_marks_or_reader_admission_proved':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths}}
(P/'RAW_RESOURCE_BRIDGE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'resource_wires':len(allw),'old_gate_counts':dict(oldsum),'rotation_bits':rot_new.bit_length()}))
