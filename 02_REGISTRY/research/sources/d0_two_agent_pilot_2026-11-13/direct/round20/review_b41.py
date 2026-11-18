#!/usr/bin/env python3
"""Consume B41 analytically, certifying its original-constant norm premise."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import coframe_targets as t
P=Path(__file__).resolve().parent;B=t.loc.B/'round41';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((B/'PROPER_LINK_CHECK.json').read_text())
for p,digest in result['source_sha256'].items():assert h(Path(p))==digest
iv=t.Dyadic(256);c=t.constants(iv);S=iv.scale
assert c['k0'][1]<24*S and 7*c['pi'][1]<22*S
A=F(24)*4*F(22,7)**2/10000;assert A<F(12,125)
kbound=(F(12,125)+F(3,100))*F(5,16)/2
assert kbound<F(1,50) and 2*kbound+F(6,2**30)<F(1,20)
assert F(20,19)<F(9,7)<2 and 1-F(9,14)**2==F(115,196)
saved=json.loads((P/'B41_EXACT_CONSTANTS_CHECK.json').read_text())
assert saved['k0_interval_hex']==[hex(x) for x in c['k0']]
assert saved['pi_interval_hex']==[hex(x) for x in c['pi']]
out={'status':'PASS_CONSUMED_B41_STRUCTURE_WITH_EXACT_ORIGINAL_CONSTANTS',
     'B41_commit':'853a9024a','B41_files_sha256':{p.name:h(p) for p in sorted(B.iterdir()) if p.is_file()},
     'exact_constants_receipt_sha256':h(P/'B41_EXACT_CONSTANTS_CHECK.json'),'reviewer_source_sha256':h(Path(__file__)),
     'root_analytic_review':'For C=LDR^T with orthogonal L,R and diagonal strict contraction D, positive-root covariance gives J(C)=diag(L,R)J(D)diag(R^T,L^T). For proper Lorentz U, exterior singular norm equals ||U||; original field bound proves both defect gaps >=115/196.',
     'decimal_k0_metadata_replaced_by_exact_Golden_interval_bound':True,
     'h_zero_and_interval_pivot_classification_still_required_for_compiler':True,
     'B41_float_diagnostics_reexecuted_by_root':False,'native_proper_link_angles_consumed':False,
     'B42_actual_compiler_is_separate_pending_work':True,'full_Omega_loader_compiled':False,'GR_closed':False}
(P/'ROOT_REVIEW_B41.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
