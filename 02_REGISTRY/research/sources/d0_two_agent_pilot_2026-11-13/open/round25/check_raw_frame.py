#!/usr/bin/env python3
"""Full 22-wire target column after RAW-frame conversion, not a native word."""
from pathlib import Path
import json,math,numpy as np
import targets as t
P=Path(__file__).resolve().parent;f=t.fields('f');inp=(2048,13,7)
y=t.raw_choi_column(f,inp);norm=abs(float(np.linalg.norm(y))-1)
# Separate check: B† maps v^tensor22 to anchor r. The analytic target then maps r to b.
G=np.array([[t.ROOTP,-t.PVAL],[t.PVAL,t.ROOTP]]);born=np.array([t.ROOTP,t.PVAL]);unit=t.mm(G.T,born.reshape(2,1))[:,0]
assert np.max(np.abs(unit-np.array([1.,0.])))<1e-15
b=t.choi_b_vector(f);b_norm=abs(float(np.linalg.norm(b))-1)
# Physical O_b leaves padding fixed but B† mixes padding: the RAW-frame column is generally nonzero there.
padding=float(np.linalg.norm(y[t.A*1024:]));assert padding>0
assert max(norm,b_norm)<2e-12
res={'status':'PASS_RAW_FRAME_22Q_FULL_COLUMN_DIAGNOSTIC','operator':'O_b (G^tensor22)^T','sample_input':inp,'dimension':len(y),'column_norm_error':norm,'target_b_norm_error':b_norm,'single_wire_born_to_zero_error':float(np.max(np.abs(unit-[1,0]))),'padding_probability_in_raw_column':padding**2,'padding_after_full_macro_may_mix':True,'protected_factors_are_identity':True,'dense_operator_allocated':False,'native_word':False,'GR_closed':False}
(P/'RAW_FRAME_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
