#!/usr/bin/env python3
"""Consume B37 actual fixed preparation, certificate, inverse and interface."""
from pathlib import Path
import hashlib,json
import material_targets as t
import material_preparation as m
import car_frame as frame
P=Path(__file__).resolve().parent;B=t.B/'round37';h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
r=json.loads((B/'RECEIPT.json').read_text())
for n,v in r['files'].items():assert h(B/n)==v,n
for n,v in r['upstream_sha256'].items():assert h(Path(n))==v,n
a=json.loads((B/'CAR_USTAR_NATIVE.json').read_text());k=int(a['k']);cert=a['certificate']
assert int(cert['L1_error_upper_numerator_hex'],16)<=1<<(cert['precision_bits']-4096)
assert a['literal_raw_inverse_DAG']==m.nb.inverse_literal(a['forward_DAG'],4,(5,6))
f=frame.resource(a['forward_DAG'],4);inv=frame.resource(a['literal_raw_inverse_DAG'],4)
assert f=={'G_port':4*k,'G_other':4*k,'CX':54,'SourceI':16}
assert +inv==+m.raw_inverse_counts(f)

# Root's independent streamed pair grammar matches the owned B37 order
# after flattening only seq containers; repetitions are NOT expanded.
lay=frame.layout();U,Ui,R=frame.fixed_components(lay)
bound={'K':3,'k':k,'target':lay['grade'][0],'controls':lay['grade'][1:],
       'pattern':[1,1,1],'permutation':[m.nb.gate('CX',lay['grade'][0],q) for q in lay['grade'][1:]]}
def flat(tree):
    if tree['op']=='seq':
        for c in tree['children']:yield from flat(c)
    else:yield tree
assert list(flat(U))==[leaf for block in m.pair_blocks(bound,lay) for leaf in flat(block)]
assert list(flat(Ui))==[leaf for block in m.pair_blocks(bound,lay,True) for leaf in flat(block)]

# Exact half-angle reduction. Compare squares and use positivity of every
# square root; no float is used to identify the target vector.
import sympy as s
p=(s.sqrt(5)-1)/2;rootp=s.sqrt(p)
assert s.simplify(p*p+p-1)==0
assert s.simplify(p*p/(2*(1+rootp))-(1-rootp)/2)==0
assert s.simplify((1+rootp)**2/(2*(1+rootp))-(1+rootp)/2)==0
checks={n:json.loads((B/n).read_text())['status'] for n in r['files'] if n.endswith('CHECK.json') or n.endswith('REPLAY.json')}
assert all(value.startswith('PASS') for value in checks.values())
out={'status':'PASS_B37_NATIVE_FIXED_PREPARATION_CONSUMED','B37_commit':'43c161649639cab63e7218843c1f12c90fde436f',
     'receipt_sha256':h(B/'RECEIPT.json'),'verified_files':r['files'],'verified_upstream':r['upstream_sha256'],
     'verified_checks':checks,'root_symbolic_half_angle_identity':True,
     'root_streamed_pair_equal_to_B37_forward_and_literal_inverse':True,
     'root_duplicate_full_B37_replay':False,'B37_independent_operator_error_lt':'2^-4142',
     'entire_giant_native_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B37.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'B37_checks':len(checks)}))
