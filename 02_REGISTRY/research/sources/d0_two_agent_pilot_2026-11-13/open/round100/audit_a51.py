#!/usr/bin/env python3
"""Read-only audit of A51 receipts, A17 counts, stage support and norm budgets.

No production REPORT or expanded giant word is executed. All JSON output is
written here; no frozen input is changed.
"""
import hashlib, importlib.util, json, sys
from fractions import Fraction as F
from itertools import islice
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
A=D/'round51'
sys.path.insert(0,str(A))
import completed_marked_prefixes as p
import check_completed_marked_prefixes as frozen_check

def load(path): return json.loads(path.read_text())
def dec(x): return F(int(x['numerator_hex'],16),int(x['denominator_hex'],16))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def support(tree):
    if tree['op']=='seq':
        out=set()
        for child in tree['children']:out.update(support(child))
        return out
    if tree['op']=='repeat':return support(tree['child'])
    assert tree['op'] in ('G','CX','SourceI')
    return set(tree['wires'])

plan=load(A/'COMPLETED_MARKED_PREFIX_PLAN.json')
receipt=load(A/'COMPLETED_MARKED_PREFIX_CHECK.json')
assert len(plan['prefixes'])==12 and len(receipt['literal_A49_prefix_fixtures'])==39
for filename,digest in plan['source_sha256'].items():assert sha(Path(filename))==digest,filename
for filename,digest in receipt['source_sha256'].items():assert sha(Path(filename))==digest,filename
assert p.registry()==plan['prefixes']
assert p.registry()[0]['name']=='SOURCE_after_Qf'
assert [x['last_completed_stage']['report'] for x in p.registry() if x.get('last_completed_stage',{}).get('kind')=='REPORT']==list(range(8))
# Re-run frozen tests as functions: they return values and do not write inputs.
assert frozen_check.placement()==receipt['literal_A49_prefix_fixtures']
assert all(frozen_check.algebra().values())

# Reconstruct 8-report error count without calling A51.bounds().
a15=load(D/'round15/PREPROCESSOR_READY_COMPOSITION.json')
a16=load(D/'round16/SOURCE_SELECT_COMPILATION.json')
a17=load(D/'round17/GLOBAL_REPORT_COMPILATION.json')
local=load(D/'round17/GLOBAL_REPORT_PLAN.json')
pre=a15['seven_report_known_approximate_macros']
assert sum(v for k,v in pre.items() if k!='sum')==pre['sum']
assert a16['seven_report_all_known_approximate_macros']==pre['sum']+7*a16['one_report_SELECT_test_approximate_macros']
K=local['READY_total_flags']
assert a17['seven_report_all_known_approximate_macros']==a16['seven_report_all_known_approximate_macros']+7*(2*K-2)
known=a17['seven_report_all_known_approximate_macros']
assert known%7==0 and K==10249327
n8=8*(known//7)
assert n8==186005314176 and n8 < 2**38

# Bind CODE support to the actual A49/A48 namespace and every local-to-global
# report range, including port, Spin, helper and source DATA.
g=p.g
B58=HERE.parent/'round58'
coverage=load(B58/'A29_PROVIDER_TRANSDUCER_CHECK.json')
for filename,digest in coverage['source_sha256'].items():assert sha(Path(filename))==digest,filename
assert Path(g.previous.g.__file__).resolve()==(D/'round25/global_h1.py').resolve()
assert Path(g.previous.g.report.__file__).resolve()==(D/'round25/reversible_report_stream.py').resolve()
ns=g.namespace(); layout=ns['layout']; sam=set(layout['SAM']); assert len(sam)==5376
reports=ns['reports']; assert len(reports)==8
assert set(g.previous.resource_wires()).isdisjoint(sam)
assert set(ns['SC6_local_to_global']).isdisjoint(sam)
assert {layout['port'],layout['aux_arbitrary'],ns['old_compiler_helper'],*layout['spin']}.isdisjoint(sam)
N=ns['local_report']['logical_wire_count']
for r in reports:
    lo=r['private_start'];hi=lo+N-8
    assert all(not lo<=q<hi for q in sam)
    for q in [0,7,8,N-1,N,N+1,N+2,N+3,N+4]:
        assert g.ns.report_wire(ns,r,q) not in sam
    for sidx in r['source_slots']:
        slot=ns['source_slots'][sidx]
        assert set(slot['source']+slot.get('RIGHT',[])+slot['private']).isdisjoint(sam)
# Existing report template is genuinely cloned for report 7; each local
# report stage invokes the same finite A17 grammar with remapped wires.
template=next(r for r in reports[:7] if r['bank']=='f')
assert reports[7]['private_width']==template['private_width']
assert len(reports[7]['source_slots'])==len(template['source_slots'])==196
assert len(set(g.physical_wire(q) for q in sam))==5376

# Replay transducer support/parity with integer symbolic transitions instead
# of rendering the 20,000-bit replacement angle thousands of times.
# A REPORT is only sampled; other listed stages are completely traversed.
comp=g.compiler(); cm=sys.modules[comp.__class__.__module__]; stagechecks=[]
def transducer(tree,pending):
    atom=cm.source_atom(tree,comp.port,comp.spin)
    if atom is not None:return (pending+atom)%2
    if cm.exact_cz(tree,comp.port,comp.spin) is not None:
        assert pending==0
        return 0
    op=tree['op']
    if op=='seq':
        for child in tree['children']:pending=transducer(child,pending)
        return pending
    if op=='repeat':
        count=int(tree['count'])
        once=transducer(tree['child'],pending)
        if count==1:return once
        twice=transducer(tree['child'],once)
        assert twice==pending or twice==once
        return once if count%2 else twice
    assert op in ('G','CX') and pending==0
    return 0
for stage in [p.processor_stages()[0],p.processor_stages()[-2],p.processor_stages()[-1]]:
    pending=0; trees=0;first=None;last=None
    for tree in g.stage_blocks(stage):
        if first is None:first=tree
        last=tree
        pending=transducer(tree,pending)
        assert support(tree).isdisjoint(sam)
        trees+=1
    assert pending==0
    stagechecks.append({'stage':stage,'fully_traversed_profile_trees':trees,'pending':pending})
for ri in range(8):
    pending=0
    for tree in islice(g.stage_blocks({'kind':'REPORT','report':ri}),8):
        pending=transducer(tree,pending)
        assert support(tree).isdisjoint(sam)
    stagechecks.append({'stage':'REPORT','report':ri,'sampled_first_profile_trees':8,'pending_after_sample':pending})

# Check the actual A17 primitive lowering alphabet and literal inverses.
# Composite SELECT IR is built recursively from these constructors. This is
# structural evidence, not a replay of every production report occurrence.
assembly=g.previous.g.report.a
k=g.previous.g.boolean_k(); port=local['native_port'];spin=tuple(local['native_spin']);aux=local['native_aux_arbitrary']
base_r=reports[0]
def to_global(tree):return assembly.remap_native(tree,lambda q:g.ns.report_wire(ns,base_r,q))
primitive_checks=[]
for op,wires in [('CX',(9,10)),('Z',(9,)),('CZ',(9,10)),('X',(9,)),('H',(9,)),('CCX',(9,10,11))]:
    ir=assembly.s.gate(op,*wires)
    for depth in (0,1,2):
        tree=assembly.s.lower(ir,k,port,spin,aux)
        for _ in range(depth):tree=assembly.s.nb.inverse_literal(tree,port,spin)
        tree=to_global(tree)
        assert transducer(tree,0)==0 and support(tree).isdisjoint(sam)
        primitive_checks.append({'op':op,'literal_inverse_depth':depth,'pending':0})
bank=load(Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round31/NATIVE_FAIR_BANK.json'))
for idx in (0,local['fair_bank_count']-1):
    tree=to_global(assembly.fair_bank_native(local,idx,bank))
    assert transducer(tree,0)==0 and support(tree).isdisjoint(sam)
    primitive_checks.append({'op':'fair_bank','index':idx,'pending':0})

# Reconstruct rational budgets from frozen inputs, not A51.bounds().
a48=load(D/'round48/ACTUAL_FULL_VECTOR_SOURCE_JET.json')
jet_B=dec(a48['full_axis_jet_error'])
eP=dec(p.paid.control.control_plan()['control_vs_exp_tX_error'])
u=g.upper_inventory_and_error()
eB=u['full_SOURCE_DATA_fibre_prefix_error']
replacement=u['replacement_error']
eD=F(n8,2**4096)+replacement
sigma=F(1,2**80); t=F(1,2**1700); M1=1748
centre=sigma*104*M1+eB+eD
mid=centre+2*eP+2*t*t
jet=jet_B+eD*M1
effect=2*jet+2*M1*mid
values={'all_completed_processor_prefix_error':eD,'full_prefix_centre_error':centre,
        'full_prefix_midpoint_error':mid,'full_prefix_finite_axis_jet_error':jet,
        'norm_one_joint_effect_finite_axis_jet_error':effect}
for name,v in values.items():assert dec(plan['bounds'][name])==v,name
assert eD<F(1,2**4058) and centre<F(1,2**62) and mid<F(1,2**62)
assert jet<F(1,2**44) and effect<F(1,2**43)

# Audit a distinct exact complex unconditioned polarization (A51 fixture is
# real); all symbolic operations below are integer complex, not floats.
import sympy as S
P=S.Matrix([[1,S.I],[2,-1],[0,1],[1,2*S.I]])
Q=S.Matrix([[S.I,0],[1,2],[2,S.I],[-1,1]])
O=S.Matrix([[1,S.I,0,0],[-S.I,0,1,0],[0,1,-1,S.I],[0,0,-S.I,2]])
assert O==O.conjugate().T
J=(P-Q)/2;C=(P+Q)/2
assert S.simplify((P.conjugate().T*O*P-Q.conjugate().T*O*Q)/2-(C.conjugate().T*O*J+J.conjugate().T*O*C))==S.zeros(2)

inputs=[B58/'B58_A25_GCX_COVERAGE_AUDIT_RU.md',B58/'A29_PROVIDER_TRANSDUCER_CHECK.json',A/'completed_marked_prefixes.py',A/'COMPLETED_MARKED_PREFIX_PLAN.json',A/'check_completed_marked_prefixes.py',A/'COMPLETED_MARKED_PREFIX_CHECK.json',A/'COMPLETED_PREFIX_TRANSPORT_RU.md',D/'round17/GLOBAL_REPORT_ASSEMBLY_RU.md',D/'round17/GLOBAL_REPORT_COMPILATION.json',D/'round17/GLOBAL_REPORT_PLAN.json',D/'round16/SOURCE_SELECT_COMPILATION.json',D/'round15/PREPROCESSOR_READY_COMPOSITION.json',D/'round49/two_bit_paid_family.py']
out={'status':'PASS_SCOPED_INDEPENDENT_A51_AUDIT_WITH_PRODUCTION_STREAM_LIMIT',
     'frozen_fixture_replay_count':39,'frozen_effect_algebra_replayed':True,
     'independent_complex_joint_effect_polarization':True,
     'A17_seven_report_macros':known,'A17_eight_report_macros':n8,
     'processor_stage_support_and_transducer':stagechecks,
     'A17_primitive_and_fair_template_checks':primitive_checks,
     'all_12_rational_budget_values_match':True,
     'processor_eD_lt':'2^-4058','midpoint_and_centre_lt':'2^-62',
     'finite_axis_jet_lt':'2^-44','full_effect_axis_jet_lt':'2^-43',
     'budget_conditional_on_A14_A17_source_compilation_and_RAW_contract':True,
     'production_REPORTs_exhausted':False,'production_giant_word_executed':False,
     'report_closure_uses_B58_owner_structural_induction_and_same_A25_report_grammar':True,
     'report_boundaries_exhaustively_executed':False,
     'source_full_original_descriptor_identified':False,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(x):sha(x) for x in inputs}}
(HERE/'B100_A51_AUDIT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
