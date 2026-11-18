#!/usr/bin/env python3
"""Independently derive exact A29 G/CX inventory from old counts and B58 CZ census."""
from pathlib import Path
from hashlib import sha256
import json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round58'
f1=D/'round25/GLOBAL_H1_PLAN.json';f2=P/'CZ_EXACT_OCCURRENCES.json';f3=O/'round57/GADGET_G_POWER_CERTIFICATE.json';f4=D/'round29/GCX_BIRTH_CLOCK_PLAN.json'
a=json.loads(f1.read_text());b=json.loads(f2.read_text());cert=json.loads(f3.read_text());new=json.loads(f4.read_text());old=a['global_native_counts']['W_literal_echo'];k=int(cert['k_hex'],16);C=b['W_CZ_total'];Pcount=int(b['W_nonCZ_SourceI_pair_count']);rot=2*Pcount+4*C
Gold=int(old['G_port'])+int(old['G_other']);CXold=int(old['CX']);G=Gold+16*k*Pcount+32*k*C;CX=CXold-6*C+2*Pcount;L=G+CX
assert C==new['CZ_macro_replacements'] and Pcount==int(new['SourceI_pair_replacements']) and rot==int(new['rotation_power_blocks'])
assert G==int(new['native_counts']['G']) and CX==int(new['native_counts']['CX']) and L==int(new['native_call_count_L']) and L.bit_length()==new['native_call_count_bit_length']==11647
assert rot < 2**4188 and cert['rotation_norm_error_each_strict_lt']=='2^-7432'
assert new['total_RAW_births']==10407050782 and new['SourceI_calls']==0
out={'status':'PASS_INDEPENDENT_A29_EXACT_COUNTS','CZ_replacements':C,'SI_pair_replacements_hex':hex(Pcount),'rotation_blocks_hex':hex(rot),'rotation_blocks_bit_length':rot.bit_length(),'rotation_blocks_lt_2^4188':True,'G_count_hex':hex(G),'CX_count_hex':hex(CX),'L_hex':hex(L),'L_bit_length':L.bit_length(),'global_replacement_error_lt':'2^-3244 conditional on B58 structural coverage','new_births':new['total_RAW_births'],'old_history_equivalence_or_physical_admission_proved':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in (f1,f2,f3,f4)}}
(P/'A29_INDEPENDENT_COUNTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'C':C,'L_bits':L.bit_length(),'rot_bits':rot.bit_length(),'births':out['new_births']}))
