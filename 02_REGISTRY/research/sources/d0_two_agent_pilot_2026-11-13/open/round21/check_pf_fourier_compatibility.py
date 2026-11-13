#!/usr/bin/env python3
"""Exact rational check: original L4 Fourier128 and n20 unequal PF counts.

This tests an explicit tempting identification; it does not assert that the
H.1 owner uses that identification, nor disprove another paid PF/RIGHT map.
"""
from fractions import Fraction
from pathlib import Path
import json
import numpy as np

d=Path(__file__).resolve().parent
sites=[json.loads(x) for x in (d/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
ks=json.loads((d/'ORIGINAL_FOURIER128_L4.json').read_text())['kappa']
c=(1,0,-1,0);s=(0,1,0,-1)
assert len(sites)==256 and len(ks)==64
B=np.empty((256,128),dtype=np.int64)
for i,row in enumerate(sites):
    x=row['site']
    for j,k in enumerate(ks):
        z=sum(a*b for a,b in zip(k,x))%4
        B[i,2*j]=c[z];B[i,2*j+1]=s[z]
counts=np.array([r['N'] for r in sites],dtype=np.int64)
gram0=B.T@B
assert np.array_equal(2*gram0,256*np.eye(128,dtype=np.int64))
weighted=B.T@(counts[:,None]*B)
numerator=2*weighted-10946*np.eye(128,dtype=np.int64)
ind=np.unravel_index(np.argmax(np.abs(numerator)),numerator.shape)
value=Fraction(int(numerator[ind]),128*10946)
assert value!=0
result={'status':'EXACT_NONUNIFORM_PF_VS_UNIFORM_FOURIER_HOSTILE_CHECK',
        'uniform_site_gram':'I_128/128 exactly',
        'naive_PF_weighted_gram_equals_I_128_over_128':False,
        'max_entry_residual_rational':str(value),'witness_indices':[int(i) for i in ind],
        'nonzero_entries':int(np.count_nonzero(numerator)),
        'scope':'rejects only naive multiplication of this uniform Fourier subfamily by sqrt(PF site probability); H.1 SITE and RIGHT may have a different actual paid map',
        'GR_closed':False}
(d/'PF_FOURIER_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result))
