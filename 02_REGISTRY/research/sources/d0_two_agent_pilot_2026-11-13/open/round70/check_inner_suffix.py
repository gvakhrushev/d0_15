#!/usr/bin/env python3
"""Check actual A30 middle-suffix SAM support without expanding giant word."""
from pathlib import Path
from itertools import islice
from hashlib import sha256
from fractions import Fraction
import json,sys
import sympy as sp
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round30'))
import marked_source_schedule as a
ns=a.g.namespace();lay=ns['layout'];sam=set(lay['SAM']);helper=lay['qubits']; old={0,1,3}
assert len(sam)==2688 and not sam.intersection(a.resource_wires()) and len(a.resource_wires())==29848
schedule=a.stages();ind=schedule.index({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0})
assert schedule[ind+1]['kind']=='RAW_RESOURCE_FRAME' and schedule[ind+1]['intrinsic_inverse_depth']==1
assert [s['kind'] for s in schedule[ind+2:]]==['REPORT']*7+['PORT_ZERO','SC6']
assert len(ns['SC6_local_to_global'])==23
assert not sam.intersection(ns['SC6_local_to_global'])
# All local report wire indices map into SITE, report private, or the fixed
# protected port/spin/aux/witness suffix, and never any SAM coordinate.
loc=ns['local_report'];N=loc['logical_wire_count'];samples=0
for report in ns['reports']:
    assert report['private_start']>=2706 and report['private_width']==N-8
    assert min(lay['SITE'])==2692 and max(lay['SITE'])==2699
    # The body of report_wire is an exact piecewise affine map over [0,N+5).
    probes={0,7,8,9,N-1,N,N+1,N+2,N+3,N+4}
    for q in probes:
        assert a.g.ns.report_wire(ns,report,q) not in sam
        samples+=1
# Support extraction from a compact literal DAG (without expanding repeat).
def wires(node):
    if node['op']=='seq':return set().union(*(wires(t) for t in node['children'])) if node['children'] else set()
    if node['op']=='repeat':return wires(node['child'])
    return set(node['wires'])
comp=a.c.production_compiler()
# Exhaust source-frame on both sides, including compiled literal inverse.
frame_ct=0
for stage,depth in [({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1},0),({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1},1)]:
    for tree in a.stage_blocks(stage,depth):
        assert not (wires(tree)&sam)
        result,pending,_=comp.transform(tree,0)
        assert pending==0 and not (wires(result)&sam) and not (wires(result)&old)
        frame_ct+=1
assert frame_ct==2*29848
# Full actual SC6, including source parity across blocks, both chronological
# directions. Report streams are sampled; their all-event scope is B58's
# separate inductive producer proof, not a giant enumerated run.
sc6ct=0
for depth in (0,1):
    pending=0
    for tree in a.stage_blocks({'kind':'SC6'},depth):
        assert not (wires(tree)&sam)
        result,pending,_=comp.transform(tree,pending)
        assert not (wires(result)&sam) and not (wires(result)&old)
        sc6ct+=1
    assert pending==0
assert sc6ct==2*18176
for depth in (0,1):
    for ri in range(7):
        for tree in islice(a.stage_blocks({'kind':'REPORT','report':ri},depth),128):
            assert not (wires(tree)&sam) and 3 not in wires(tree)
# Central sign and its translation are also disjoint from SAM and old.
z=a.c.nb.z_word(lay['port'],lay['port'],tuple(lay['spin']))
zout,pend,_=comp.transform(z,0)
assert pend==0 and not wires(zout)&(sam|old)
# Endpoint SAM diagonality alone does NOT imply arbitrary Q commutation.
Z=sp.diag(1,-1);J=sp.Matrix([[0,-1],[1,0]])
assert Z*J-J*Z!=sp.zeros(2)
# In contrast, explicit tensor-disjoint middle suffix commutes with any
# SAM/old unitary. Verify the algebraic pattern on a nontrivial fixture.
R=sp.Matrix([[0,-1],[1,0]]);X=sp.Matrix([[0,-1],[1,0]])
assert sp.kronecker_product(X,sp.eye(2))*sp.kronecker_product(sp.eye(2),R)==sp.kronecker_product(sp.eye(2),R)*sp.kronecker_product(X,sp.eye(2))
# The A30 replacement is an all-column comparison to the pre-compiler
# complete word, unlike the separate canonical-input geometric approximation.
inv=a.inventory();e=inv['replacement_error'];assert e<Fraction(1,2**3244)
assert e*2**3158<Fraction(1,2**86)
inputs=[Path(__file__),D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round25/global_h1.py',D/'round25/h1_namespace.py',D/'round25/reversible_report_stream.py',D/'round29/gcx_compiler.py',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',O/'round58/PROVIDER_TEMPLATE_AND_WIRE_CHECK.json',O/'round60/A30_COMMON_CHECKPOINT_INDEPENDENT.json',O/'round69/B69_ACTUAL_TASK_INPUTS_AND_ADMISSION_RU.md']
out={'status':'STRUCTURAL_MIDDLE_SUFFIX_SAM_COMMUTANT_CONDITIONAL_ON_B58_PROVIDER_INDUCTION','SAM_count':len(sam),'BR_inverse_trees_checked':frame_ct,'SC6_transducer_trees_checked':sc6ct,'report_samples_per_bank_per_direction':128,'report_local_mapping_probes':samples,'scope':'actual A30 compiled middle between checkpoint and reverse frame; relies on B58 structural report-family proof, not full expanded REPORT execution','exact_commutation_claim':'[S_actual,Q_SAM tensor I_WORK tensor Q_allowed_old]=0 when Q uses only untouched supports','endpoint_diagonal_does_not_imply_full_commutant':True,'replacement_all_column_error_lt':'2^-3244','conservative_e_over_gs_lt':'2^-86 conditional g*s>2^-3158','same_task_native_admission_proved':False,'full_H_plus_J_source_bound_proved':False,'exact_reflection_of_actual_A30_claimed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in inputs}}
(P/'INNER_SUFFIX_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'BR_trees':frame_ct,'SC6_trees':sc6ct,'samples':samples}))
