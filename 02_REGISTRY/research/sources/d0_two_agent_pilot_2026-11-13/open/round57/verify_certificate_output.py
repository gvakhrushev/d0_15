#!/usr/bin/env python3
"""Fast independent consistency check; power enclosures were computed in B57.

Checks pins, actual exponents, exact targets, the recorded inequalities, and
conditional global count. It does not recompute the costly power intervals.
"""
from pathlib import Path
from math import isqrt
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;d=json.loads((P/'GADGET_G_POWER_CERTIFICATE.json').read_text());assert d['status']=='PASS_CERTIFIED_FOUR_POSITIVE_G_POWERS'
for f,sha in d['input_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==sha
k=int(d['k_hex'],16);assert k>0 and k.bit_length()==d['k_bit_length'];S=1<<d['precision_bits'];t=isqrt((S*S)//2);targets={2:((t,t+1),(t,t+1)),14:((t,t+1),(-t-1,-t)),4:((0,0),(S,S)),12:((0,0),(-S,-S))};summary={}
for m,(tc,ts) in targets.items():
 r=d['rotation_bounds'][str(m)];assert int(r['exponent_hex'],16)==m*k
 c=[int(x,16) for x in r['cos_interval_hex']];s=[int(x,16) for x in r['sin_interval_hex']];assert c[0]<=c[1] and s[0]<=s[1]
 def dist(a,b):return max(abs(a[0]-b[1]),abs(a[1]-b[0]))
 err=dist(c,tc)+dist(s,ts);assert err==int(r['operator_error_bound_num_hex'],16)
 direct=int(r['owner_direct_multiplier_operator_error_num_hex'],16);assert err*(1<<7432)<S and direct*(1<<7432)<S
 summary[str(m)]={'independent_error_bound_lt_2_to_minus':d['precision_bits']-err.bit_length(),'direct_error_bound_lt_2_to_minus':d['precision_bits']-direct.bit_length()}
assert d['old_W_L_bit_length']==4188 and 7432-2-4188==3242
out={'status':'PASS_OUTPUT_CONSISTENCY_NOT_A_POWER_RECOMPUTATION','k_bit_length':k.bit_length(),'precision_bits':d['precision_bits'],'rigorous_error_exponents':summary,'input_hashes_verified':True,'complete_compiler_or_physical_admission_proved':False}
(P/'CERTIFICATE_OUTPUT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
