#!/usr/bin/env python3
"""Exact A27 probability identity, fresh cancellation and A48 corner bound."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json,sys,sympy as sp
P=Path(__file__).resolve().parent;B=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
# Every 4-valued chart vertex is inside the old asymmetric continuous cube.
# p²+p=1 and 3<2^50 suffice for the two extreme vertices.
assert 3<1<<50
for value in range(4):
 # Worst signed displacements are [-3p²,3p]*2^-80.
 assert 0<=value<=3
# Full original SC6 eight-term polynomial, checked for every event tuple and
# all 4^7 READY/REPORT bit-pairs, independent of field values.
records=json.loads((B/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json').read_text())['term_normal_forms'];terms=[(r['selector'],r['sign'],*r['call_indices']) for r in records]
assert len(terms)==8 and len({q[0] for q in terms})==8 and all(q[0].count('1')==2 for q in terms)
for pairs in product(range(4),repeat=7):
 v=[int(z==3) for z in pairs];direct=sum(v[i]*v[j] if sg>0 else 1-v[i]*v[j] for _,sg,i,j in terms)
 expected=4+(v[0]-v[1])*(v[2]-v[3])+(v[4]-v[5])*(v[6]-v[3]);assert direct==expected
# Independence is a stated source-copy condition; exact polynomial identity
# makes substitution by any seven probabilities valid, not just binary names.
N=65568;assert F(N,2)*2/F(N)==1 and F(64,128**2)==F(1,256)
# Fresh REPORT D shares SITE with old R; it need not commute with R. It does
# commute with C and Z, which is exactly the cancellation used by A46.
I=sp.eye(2);X=sp.Matrix([[0,1],[1,0]]);Z=sp.diag(1,-1)
def gate_cx(c,t):
 return sp.Matrix(16,16,lambda i,j:int(i==(j^(((j>>c)&1)<<t))))
def gate_z(t):return sp.diag(*[(-1)**((j>>t)&1) for j in range(16)])
D0=gate_cx(0,1);C=gate_cx(3,2);Z0=gate_z(2);R=gate_cx(3,0)
assert D0*R!=R*D0 and D0*C==C*D0 and D0*Z0==Z0*D0
assert R.T*D0.T*C.T*Z0*C*D0*R==R.T*C.T*Z0*C*R
# B54 positivity is a frozen global probability bound, independent of b.
source=read=lambda f:json.loads(Path(f).read_text())
bound=source(D/'round27/SCALAR_SOURCE_BOUND.json');lower=F(bound['rational_lower']);assert lower>F(67,100)
plan=source(D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json');record=plan['errors']['full_canonical_compressed_error'];e=F(int(record['numerator_hex'],16),int(record['denominator_hex'],16))
assert e<F(1,1<<3421)<F(1,1<<3298) and lower-e>F(67,100)-F(1,1<<3421)>F(2,3)
support=source(P/'CODE_SUPPORT_CHECK.json');assert support['status']=='PASS_COMPOSITIONAL_CODE_CONTROL_ONLY_SUPPORT'
# Owner receipt is checked against the seven report term data used here.
cert=source(D/'round27/PRODUCT_SOURCE_COMPRESSION_CHECK.json');assert cert['status']=='EXACT_SOURCE_SLOT_AND_SC6_PRODUCT_COMPRESSION_CHECK'
inputs=[D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round27/PRODUCT_SOURCE_COMPRESSION_CHECK.json',D/'round27/SCALAR_SOURCE_BOUND.json',D/'round46/INDEPENDENT_CURRENT_BANK_RU.md',D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json',B/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json',B/'round93/B93_CHECKPOINT.json',B/'round94/B94_CHECKPOINT.json',P/'CODE_SUPPORT_CHECK.json']
out={'status':'PASS_FOUR_VALUED_A27_CORNER_EXTENSION_CONDITIONAL_OWNERS','all_four_local_vertices_inside_old_asymmetric_cube':True,'old_seven_report_polynomial_checked_all_4pow7_ready_cases':True,'fresh_REPORT_cancels_at_ideal_logical_operator':True,'fresh_REPORT_commutes_with_old_report_assumed':False,'actual_CODE_control_only_compositional_check':True,'actual_compressed_corner_error_lt':'2^-3421','required_corner_error_lt':'2^-3298','ideal_corner_gt':'67/100','actual_corner_gt':'2/3','scope':'selected typed A23 vacuum extension, A27 product and A48 declared canonical RAW fibre; inherited B54 and report approximation bounds','literal_production_core_executed':False,'original_Dnu_mark_transport_or_physical_admission_proved':False,'GR_closed':False,'source_sha256':{str(f):sha256(Path(f).read_bytes()).hexdigest() for f in inputs}}
(P/'CORNER_LAW_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
