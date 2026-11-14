#!/usr/bin/env python3
"""A36 backward: exact reduced output algebra and one SAM discriminator."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import json,sys
import sympy as s
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round36'))
import independent_outer_pairs as a36
plan=json.loads((D/'round36/INDEPENDENT_OUTER_PAIRS_PLAN.json').read_text())
review=json.loads((O/'round71/A36_INDEPENDENT_AUDIT.json').read_text())
assert review['status']=='PASS_CONDITIONAL_INDEPENDENT_A36_OUTER_ROWS_AUDIT'
for f,h in plan['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h
r=json.loads((D/'round30/SOURCE_RAW_MARK_REGISTRY.json').read_text())
assert len(r['source_slots'])==1372 and r['original_leaf_bindings_resolved_by_API']==72192
assert all(x['original_RAW_mark_checkpoint_after_stage_index']==1380 for x in r['source_slots'])
assert r['original_readers_executed_or_retained_records_created'] is False
plus=a36.endpoint_parts('backward','plus',2);minus=a36.endpoint_parts('backward','minus',2)
assert plus['pre']==minus['pre'] and plus['last_g']==minus['last_g']
np,nm,n0,T=a36.parameters()
for p,expected in [(plus,nm),(minus,np)]:
    c=a36.nb.counts(p['post_before_final'])
    assert c['G']==expected-1 and c['CX']==T-expected
    assert a36.core.b.physical_tree(p['last_g'])=={'op':'G','wires':[4]}
# Actual identity padding family consists only of 2- and 5-CX identities,
# here exhaustively check both primitive words on all columns.
layout=a36.core.g.namespace()['layout']; slots=[layout['aux_arbitrary'],layout['port'],layout['qubits']];ix={q:i for i,q in enumerate(slots)}
for length in (2,5):
    gates=list(a36.old.nb.expand(a36.old.padding(length),5))
    for initial in range(8):
        x=initial
        for gate in gates:
            c,t=map(ix.get,gate['wires'])
            if x>>c&1:x^=1<<t
        assert x==initial
# Exact tensor algebra even for a nontrivial unitary and entangled pure input.
G=s.Matrix([[0,-1],[1,0]]);I=s.eye(2);Z=s.diag(1,-1)
assert s.kronecker_product(G,I).T*s.kronecker_product(I,Z)*s.kronecker_product(G,I)==s.kronecker_product(I,Z)
bell=s.Matrix([1,0,0,1])/s.sqrt(2);rho=bell*bell.T
rho2=s.kronecker_product(G,I)*rho*s.kronecker_product(G,I).T
def trace_a(M):return s.Matrix([[sum(M[2*i+j,2*i+k] for i in range(2)) for k in range(2)] for j in range(2)])
assert trace_a(rho)==trace_a(rho2)
# Bound the SAME actual A30 per-SAM corner away from 1/sqrt(2), using its
# already owned native error and the original reference polynomial. This is
# only for a terminal SAM discriminator, not a new calibration or root.
p,x,y,z=s.symbols('p x y z'); E=p**2*(1+x);ell=4*E*(1-E);u=p+p**2*y;b=4*u**2*(1-u**2);A=ell+(1-ell)*b;poly=s.expand(1-(1-z*b)*(1-z*A))
for deriv in (s.diff(poly,x),s.diff(poly,y)):
    assert sum(abs(v) for v in s.Poly(deriv,p,x,y,z).coeffs())<2**21
assert s.rem(p**7-(13*p-8),p*p+p-1,p)==0
lo,hi=F(618033,10**6),F(618034,10**6)
assert lo*lo+lo<1<hi*hi+hi
p7upper=13*hi-8
ref_delta=F(1,2**1543);native_e=F(1,2**3231)
assert 50*2**21<2**27
c_lower=1-2*p7upper*(4+2**27*ref_delta)-native_e
assert c_lower>F(71,100)
# For real unit vectors a,b with <omega,a>,<omega,b>>71/100,
# <a,b>>2*(71/100)^2-1=41/5000. Common pre G^n0 is within
# 2delta_angle of identity, so X-coherence changes by at most 4delta_angle.
angle_delta=F(1,2**4852);t=F(1,2**1618)
gamma=2*F(71,100)**2-1;assert gamma==F(41,5000)
assert (F(1,2)-4*angle_delta)*gamma>F(1,300)
# sin(2t)>t for this t; two endpoint angle errors change a Z expectation
# by at most 4delta_angle.  Therefore + minus - exceeds t/151.
assert t< F(1,2) and t/F(150)-4*angle_delta>t/F(151)
# Check sign convention R(-t)^T Z R(-t)-R(t)^T Z R(t)=2 sin(2t) X.
c,q=s.symbols('c q',real=True);R=s.Matrix([[c,-q],[q,c]]);Rm=s.Matrix([[c,q],[-q,c]]);X=s.Matrix([[0,1],[1,0]])
assert Rm.T*Z*Rm-R.T*Z*R==4*c*q*X
# Reports and original owner require early marks, not automatic terminal WJ.
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
files=[Path(__file__),D/'round36/independent_outer_pairs.py',D/'round36/INDEPENDENT_OUTER_PAIRS_PLAN.json',D/'round30/source_mark_registry.py',D/'round30/SOURCE_RAW_MARK_REGISTRY.json',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round30/COMMON_RAW_SOURCE_MARKS_RU.md',D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',O/'round54/B54_PRODUCT_SOURCE_EXACT_RU.md',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',O/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',O/'round65/check_reference_secant_defect.py',O/'round65/certify_scalar_hessian_envelope.py',O/'round71/A36_INDEPENDENT_AUDIT.json',root/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md']
out={'status':'PASS_BACKWARD_OUTPUT_SUBSYSTEM_AND_CONDITIONAL_SAM_DISCRIMINATOR','same_full_prefix_through_A30_core':True,'same_checkpoint_registered_source_slots':1372,'same_registered_leaf_bindings':72192,'identity_on_complement_reduced_channel_for_all_inputs_and_references':True,'full_raw_history_or_temporal_records_equal':False,'terminal_SAM_Z_plus_minus_strict_gt':'t/151 conditional on original ideal product law, A30 native error and B58 exact SAM-controlled word','terminal_SAM_Z_required_by_original_task_proved':False,'terminal_full_WJ_required_by_original_H1_mark_list':False,'trace_SAM_admissible_for_specific_task_proved':False,'same_task_admission_or_FN_fidelity_proved':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'BACKWARD_OUTPUT_SUBSYSTEM_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'registered_marks':1372,'terminal_Z_lower':out['terminal_SAM_Z_plus_minus_strict_gt']}))
