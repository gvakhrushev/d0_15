#!/usr/bin/env python3
"""H.1 original finite-site all-column target, not its compiled gate word."""
from pathlib import Path
import hashlib,json,math
import numpy as np

d=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (d/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
assert len(rows)==256 and sum(r['N'] for r in rows)==10946
p=(math.sqrt(5)-1)/2;a=math.sqrt(p);v=np.array([a,p]);G=np.array([[a,-p],[p,a]])
site_v=v.copy();B=G.copy()
for _ in range(7):site_v=np.kron(site_v,v);B=np.kron(B,G)
chi=np.array([math.sqrt(r['N']/10946) for r in rows])
e0=np.eye(256)[:,0];K=np.outer(chi,e0)-np.outer(e0,chi);anchor=float(chi[0])
mm=lambda x,y:np.einsum('ij,jk->ik',x,y,optimize=False)
O=np.eye(256)+K+mm(K,K)/(1+anchor)
loader=mm(O,B.T)
orth=float(np.max(np.abs(mm(loader.T,loader)-np.eye(256))))
state=float(np.max(np.abs(np.einsum('ij,j->i',loader,site_v)-chi)))
assert anchor>0 and orth<1e-12 and state<1e-12
out=d/'SITE_LOADER_L4_CENTRE_NUMERIC.npz';np.savez_compressed(out,loader=loader,chi=chi)
result={'status':'PASS_NUMERIC_COMPLETE_SITE_TARGET_NOT_NATIVE_WORD','dimension':256,
        'site_born_qubits':8,'site_probability':'N_x/10946 = (1/256) rho_x',
        'target':'O_chi (G^tensor8)^T on all 256 columns',
        'positive_anchor':anchor,'orthogonality_error_float':orth,'born_mapping_error_float':state,
        'float_not_interval_certified':True,'native_site_loader_word_emitted':False,
        'future_site_marks_and_unprepare_paid':False,
        'target_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'GR_closed':False}
(d/'SITE_LOADER_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
