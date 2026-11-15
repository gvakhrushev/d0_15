#!/usr/bin/env python3
"""Exact finite controls for the retained-record/codec carrier bound."""
from pathlib import Path
from hashlib import sha256
import json
import sympy as s

P=Path(__file__).resolve().parent
repo=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13')
owner=repo/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
code=repo/'02_REGISTRY/research/A4D_COMPLETE_CODE_CLASS_SOURCE_UNIVERSALITY_2026_10_19.md'
text=owner.read_text()
assert '## 7fv.' in text and 'delta<min(q,1-q)' in text and '(FV7)' in text
assert 'SAME-object decoder' in code.read_text()

# Three efficient full-rank, noncommuting binary instruments; all eight
# recorded histories are kept. This is a fixture, not a production replay.
U=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],
            [s.Rational(4,5),s.Rational(3,5)]])
D0=s.diag(s.Rational(3,5),s.Rational(4,5))
D1=s.diag(s.Rational(4,5),s.Rational(3,5))
assert D0*D0+D1*D1==s.eye(2)
rots=[s.eye(2),U,U**2]
ks=[(R*D0*R.T,R*D1*R.T) for R in rots]
assert all(a.T*a+b.T*b==s.eye(2) for a,b in ks)
assert ks[0][0]*ks[1][0]!=ks[1][0]*ks[0][0]
rho=s.diag(s.Rational(1,3),s.Rational(2,3))
blocks=[]
for x in range(8):
    K=s.eye(2)
    for j in range(3): K=ks[j][(x>>j)&1]*K
    sigma=K*rho*K.T
    assert sigma.det()>0
    blocks.append(sigma)
omega=s.diag(*blocks)
assert omega.rank()==16 and s.trace(omega)==1
assert 2*2*3 < omega.rank() <= 2*4*3

# Countercontrol: bank holds a perfect copy of x. Clearing the record by
# controlled XOR is reversible on the ACTUAL support, so a bank that holds
# the labels must not be counted as independent untouched capacity.
permutation=s.zeros(64)
for label in range(8):
    for bank in range(8):
        permutation[(label^bank)*8+bank,label*8+bank]=1
assert permutation.T*permutation==s.eye(64)
correlated=s.zeros(64)
for x in range(8): correlated[x*8+x,x*8+x]=s.Rational(1,8)
out=permutation*correlated*permutation.T
assert correlated.rank()==8 and out.rank()==8
assert all(out[i,i]==0 for i in range(8,64))
assert permutation.T*out*permutation==correlated

for M,d,b in [(8,9,5),(3,3,2),(16,17,12)]:
    assert 2**(b-1)*d<2**M<=2**b*d
receipt={'result':'PASS', 'fixture_M':3,'fixture_bank_dimension':2,
 'fixture_rank_full_retained_cq':int(omega.rank()),
 'strict_effects_and_all_records_positive':True,
 'correlated_bank_can_hold_labels_countercontrol':True,
 'capacity_bound':'2^b d_side D_bank >= 2^M rank(rho)',
 'M8_side9_min_bits':5,'not_a_physical_cost_or_Info_bound':True,
 'physical_C_closed':False,'GR_closed':False,
 'source_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in (owner,code)}}
(P/'B117_RETAINED_CODEC_CAPACITY_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
